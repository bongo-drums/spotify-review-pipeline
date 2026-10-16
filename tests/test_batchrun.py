"""Batch-tier runner against a fake Message Batches client: submit, poll, collect, retry, reconcile after a crash."""
import json
import re
from pathlib import Path
from types import SimpleNamespace

from pipeline import batchrun
from pipeline.budget import SpendLedger
from pipeline.ingest import ingest
from tests.test_pilot import _rule

_REVIEW = re.compile(r"^#(\d+)\n(.*)$", re.M)


class FakeBatches:
    """Each created batch ends on the first retrieve; one request per batch errors when its text says ERROR."""

    def __init__(self):
        self.batches = {}
        self.created = []

    def create(self, requests):
        bid = f"msgbatch_{len(self.batches) + 1:03d}"
        self.batches[bid] = list(requests)
        self.created.append(bid)
        return SimpleNamespace(id=bid, processing_status="in_progress")

    def retrieve(self, bid):
        n = len(self.batches[bid])
        return SimpleNamespace(id=bid, processing_status="ended",
                               request_counts=SimpleNamespace(processing=0, succeeded=n, errored=0, expired=0, canceled=0))

    def results(self, bid):
        for req in self.batches[bid]:
            user = req["params"]["messages"][0]["content"]
            if "ERROR" in user:
                yield SimpleNamespace(custom_id=req["custom_id"], result=SimpleNamespace(
                    type="errored", error=SimpleNamespace(error=SimpleNamespace(type="api_error", message="boom"))))
                continue
            records = []
            for m in _REVIEW.finditer(user):
                k, body = int(m.group(1)), m.group(2)
                records.append({"i": k, **_rule(body), "q": 0, "r": False})
            usage = SimpleNamespace(input_tokens=10 * len(records), cache_creation_input_tokens=0, cache_read_input_tokens=1500,
                                    output_tokens=45 * len(records))
            msg = SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps({"reviews": records}))],
                                  stop_reason="end_turn", stop_details=None, usage=usage)
            yield SimpleNamespace(custom_id=req["custom_id"], result=SimpleNamespace(type="succeeded", message=msg))


def _csv(tmp_path, n=130):
    import csv
    from tests.conftest import HEADER
    rows = []
    for i in range(n):
        text = "ERROR please" if i == 5 else ("" if i == 7 else f"Love this app #{i}")
        rows.append([f"id-{i:03d}", text, "5", "0", "9.0.1", "2025-01-01 10:00:00"])
    path = tmp_path / "r.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    return path


def test_batchrun_dry_run_then_real_run_with_retry(tmp_path):
    path = _csv(tmp_path)
    out, ledger = tmp_path / "full", tmp_path / "ledger.sqlite"
    ingest(path, out)
    client = SimpleNamespace(messages=SimpleNamespace(batches=FakeBatches()))
    dry = batchrun.BatchRunner(out, max_usd=1.0, batch_requests=2, poll_s=0, ledger_path=ledger, client=client, dry_run=True)
    d = dry.run()
    dry.close()
    assert d["requests"] == 3 and d["texts"] == 129 and d["batches"] == 2 and d["worst_case_usd"] > 0
    assert d["counts"]["pending"] == 129 and client.messages.batches.created == []

    r = batchrun.BatchRunner(out, max_usd=1.0, batch_requests=100, poll_s=0, ledger_path=ledger, client=client)
    s = r.run()
    # batch 1: 3 requests (129 texts); the request holding the ERROR text fails as a whole, so its 50 texts are
    # re-sent one per request in batch 2: 49 succeed, the ERROR text fails again -> quarantined after MAX_ATTEMPTS
    assert s["batches"] == 2 and s["requests"] == 53
    assert s["counts"] == {"pending": 0, "completed": 128, "quarantined": 2}
    rows = {row[0]: row for row in r.state.conn.execute("SELECT review_id, status, reason, attempts FROM records")}
    assert rows["id-005"][1] == "quarantined" and rows["id-005"][3] == 2 and rows["id-005"][2].startswith("batch_errored (attempt 2)")
    assert rows["id-006"][1] == "completed" and rows["id-006"][3] == 2
    calls = list(r.state.conn.execute("SELECT status, service_tier, phase, cost_usd_estimate FROM calls"))
    assert len(calls) == 53 and sum(c[0] == "failed" for c in calls) == 2 and all(c[1] == "batch" and c[2] == "initial" for c in calls)
    assert all(row[0] == "collected" for row in r.state.conn.execute("SELECT status FROM batch_jobs"))
    led = r.ledger.summary()
    assert led["outstanding_reservations_usd"] == 0 and abs(led["committed_usd"] - r.run_spent()) < 1e-6  # summary rounds to 6 dp
    assert (out / "checkpoint.json").exists()
    r.close()


def test_batchrun_reconciles_in_flight_batch_after_crash(tmp_path):
    path = _csv(tmp_path, n=60)
    out, ledger = tmp_path / "full", tmp_path / "ledger.sqlite"
    ingest(path, out)
    client = SimpleNamespace(messages=SimpleNamespace(batches=FakeBatches()))
    r = batchrun.BatchRunner(out, max_usd=1.0, batch_requests=100, poll_s=0, ledger_path=ledger, client=client)
    reqs = r.next_batch_requests()
    bid = r.submit(reqs)                       # "crash" right after submission: nothing collected
    assert r.ledger.summary()["outstanding_reservations_usd"] > 0
    r.close()
    r2 = batchrun.BatchRunner(out, max_usd=1.0, batch_requests=100, poll_s=0, ledger_path=ledger, client=client, resumed=True)
    s = r2.run()
    assert s["reconciled"] == 1 and client.messages.batches.created == ["msgbatch_001", "msgbatch_002"]   # retry batch (singles)
    assert s["counts"] == {"pending": 0, "completed": 58, "quarantined": 2} and r2.ledger.summary()["outstanding_reservations_usd"] == 0
    assert {row[0] for row in r2.state.conn.execute("SELECT phase FROM calls")} == {"resume"}
    r2.close()
