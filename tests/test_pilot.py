"""End-to-end pilot run against a fake Anthropic client (no network, no key)."""
import csv
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from pipeline import pilot as pl
from pipeline.budget import SpendLedger
from pipeline.enricher import SYSTEM_PROMPT
from tests.conftest import HEADER

SYS_TOKENS = 1500
_REVIEW = re.compile(r"^#(\d+)\n(.*)$", re.M)


def _rule(text: str) -> dict:
    t = text.lower()
    if "ads" in t:
        return {"t": "usability", "s": "ads_interruptions", "n": "complaint", "v": 3, "m": 1, "e": ["ads"]}
    if "login" in t:
        return {"t": "access", "s": "login_failure", "n": "complaint", "v": 4, "m": 0, "e": []}
    if "love" in t or "great" in t:
        return {"t": "other", "s": "general_positive", "n": "praise", "v": 1, "m": 4, "e": ["Spotify"]}
    if "uninstall" in t:
        return {"t": "playback", "s": "crash_wont_open", "n": "cancellation", "v": 4, "m": 0, "e": []}
    return {"t": "other", "s": "general_negative", "n": "complaint", "v": 2, "m": 1, "e": []}


class FakeMessages:
    """Deterministic stand-in for client.messages: labels by keyword, with two planted failures.

    A text containing INVALID always gets a subtopic that does not belong to its topic
    (-> retried once, then quarantined). A text containing SKIP is omitted from the first
    response that includes it (-> retried, then completed).
    """

    def __init__(self):
        self.calls = []
        self.seen = {}

    def count_tokens(self, **kw):
        return SimpleNamespace(input_tokens=SYS_TOKENS + 5)

    def create(self, **kw):
        assert kw["system"][0]["text"] == SYSTEM_PROMPT and kw["thinking"] == {"type": "disabled"}
        self.calls.append(kw)
        user = kw["messages"][0]["content"]
        records, n_sent = [], 0
        for m in _REVIEW.finditer(user):
            k, body = int(m.group(1)), m.group(2)
            n_sent += 1
            times = self.seen[body] = self.seen.get(body, 0) + 1
            if "SKIP" in body and times == 1:
                continue
            rec = {"i": k, **_rule(body), "q": body.count("] ") - 1, "r": False}
            if "INVALID" in body:
                rec["s"] = "price"
            records.append(rec)
        first = len(self.calls) == 1
        usage = SimpleNamespace(input_tokens=12 * n_sent, cache_creation_input_tokens=SYS_TOKENS if first else 0,
                                cache_read_input_tokens=0 if first else SYS_TOKENS, output_tokens=45 * len(records))
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=json.dumps({"reviews": records}))],
                               stop_reason="end_turn", stop_details=None, usage=usage, model=kw["model"], _request_id="req_fake")


def _client():
    return SimpleNamespace(messages=FakeMessages())


@pytest.fixture
def cost_csv(tmp_path):
    rows = []
    phrases = ["Ads every song", "Love this app", "Great music. Love it!", "Cannot login anymore", "Uninstalling now",
               "Worst update ever", "Meh"]
    for i in range(100):
        if i == 7:
            text = ""                                    # quarantined at ingest
        elif i == 11:
            text = "INVALID label please. Second sentence."
        elif i == 23:
            text = "SKIP me the first time"
        elif i in (40, 41, 42):
            text = "Love this app"                        # exact duplicates of row 1
        else:
            text = f"{phrases[i % len(phrases)]} #{i}"
        rows.append([f"id-{i:03d}", text, str(1 + i % 5), "0", "9.0.1", f"2025-01-{1 + i % 28:02d} 10:00:00"])
    path = tmp_path / "cost_100.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(rows)
    manifest = tmp_path / "manifest.json"
    import hashlib
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest.write_text(json.dumps({"files": [{"name": "cost_100.csv", "sha256": sha, "rows": 100}]}))
    return path, manifest


def test_manifest_check_shapes(cost_csv, tmp_path):
    path, manifest = cost_csv
    r = pl.check_manifest(manifest, path)
    assert r["found_entry"] and r["sha256_matches"] is True
    other = tmp_path / "m2.json"
    other.write_text(json.dumps({"cost_100.csv": "0" * 64}))
    r = pl.check_manifest(other, path)
    assert r["found_entry"] and r["sha256_matches"] is False
    assert pl.check_manifest(None, path)["found_entry"] is False
    assert "error" in pl.check_manifest(tmp_path / "missing.json", path)


def test_pilot_end_to_end_and_resume(cost_csv, tmp_path):
    path, manifest = cost_csv
    out, ledger = tmp_path / "pilot100", tmp_path / "ledger.sqlite"
    client = _client()
    cost_dir = tmp_path / "cost"
    report = pl.run_pilot(path, out, manifest, max_usd=0.25, ledger_path=ledger, client=client,
                          phases=("cold", "warm", "replay"), cost_dir=cost_dir)

    assert report["status"] == "ok" and report["manifest_check"]["sha256_matches"] is True
    assert report["system_prompt_tokens"] == SYS_TOKENS + 5
    # 100 rows: 1 empty, rows 40-42 share one text -> 97 distinct nonblank texts -> 2 cold requests;
    # the two retries (SKIP, INVALID) ride along in the second request (50 + 47 + 2 = 99 texts sent)
    assert report["input"]["distinct_texts"] == 97
    cold, warm, replay = report["phases"]["cold"], report["phases"]["warm"], report["phases"]["replay"]
    assert cold["calls"] == 2 and cold["texts"] == 99
    assert cold["failed_calls"] == 0 and replay["calls"] == 2 and replay["texts"] == cold["texts"]
    assert cold["calls_detail"][0]["cache_creation_input_tokens"] == SYS_TOKENS
    assert all(c["cache_read_input_tokens"] == SYS_TOKENS for c in cold["calls_detail"][1:])
    assert replay["usage"]["cache_creation_input_tokens"] == 0 and replay["usage"]["cache_read_input_tokens"] == 2 * SYS_TOKENS
    # warm = saved result cache, zero enrichment calls; the INVALID text was never labelled so it stays pending
    assert warm["enrichment_calls"] == 0 and warm["cost_usd"] == 0.0 and warm["wall_s"] >= 0
    assert warm["rows_completed_from_cache"] == 98 and warm["result_cache_entries"] == 96
    assert warm["counts"] == {"pending": 1, "completed": 98, "quarantined": 1} and warm["pending_text_ids"] == ["id-011"]
    assert (out / "warm" / "state.sqlite").exists() and (out / "warm" / "checkpoint.json").exists()
    counts = report["final_counts"]
    assert counts == {"pending": 0, "completed": 98, "quarantined": 2}
    assert report["labels"]["quarantine_reasons"]["empty_review_text"] == 1
    q = [r for r in report["labels"]["quarantine_reasons"] if r.startswith("invalid_record:subtopic")]
    assert len(q) == 1 and "(attempt 2)" in q[0]
    assert report["labels"]["cold_replay_agreement"]["identical_on_all_fields"] == 1.0
    assert report["run_spent_usd"] > 0 and report["ledger"]["committed_usd"] == pytest.approx(report["run_spent_usd"])
    assert report["ledger"]["outstanding_reservations_usd"] == 0
    assert cold["per_text"]["output_tokens"] > 0 and cold["call_duration_s"]["mean"] >= 0

    # evidence is an exact substring; duplicates were completed from the cache, not re-sent
    with open(out / "labels.csv", newline="", encoding="utf-8") as f:
        rows = {r["review_id"]: r for r in csv.DictReader(f)}
    # rows 40-42 share one text: one request labels the whole group (cache_source_id = first id)
    assert rows["id-041"]["status"] == "completed" and rows["id-041"]["cache_source_id"] == "id-040"
    assert rows["id-041"]["topic"] == rows["id-040"]["topic"] == "other"
    assert rows["id-001"]["evidence_quote"] == "Love this app #1"
    assert rows["id-002"]["evidence_quote"] == "#2" and rows["id-002"]["evidence_sentence"] == "2"  # 3rd sentence
    assert rows["id-023"]["status"] == "completed" and rows["id-023"]["attempts"] == "2"
    assert rows["id-011"]["status"] == "quarantined" and rows["id-001"]["sentiment"] == "1.0"

    # cost/ evidence per COST_CALCULATOR.md section 5
    recs = [json.loads(l) for l in (cost_dir / "pilot_records.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(recs) == 100 and report["cost_evidence"]["pilot_records"] == 100
    by_id = {r["review_id"]: r for r in recs}
    assert by_id["id-001"]["status"] == "completed" and by_id["id-001"]["evidence_quote"] == "Love this app #1"
    assert by_id["id-001"]["sentiment"] == 1.0 and by_id["id-001"]["label_config"] == report["label_config"]
    assert by_id["id-041"]["cache_source_id"] == "id-040" and "cache_source_id" not in by_id["id-040"]
    assert by_id["id-007"] == {"review_id": "id-007", "source_sha256": by_id["id-007"]["source_sha256"],
                               "status": "quarantined", "reason": "empty_review_text", "attempts": 0}
    calls = [json.loads(l) for l in (cost_dir / "pilot_calls.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(calls) == 4 and {c["phase"] for c in calls} == {"initial", "replay"}
    assert all(c["role"] == "enrich" and c["outcome"] == "succeeded" and c["workers"] == 1 for c in calls)
    assert sum(len(c["review_ids"]) for c in calls if c["phase"] == "initial") == 99
    with open(cost_dir / "usage.csv", newline="", encoding="utf-8") as f:
        usage_rows = list(csv.DictReader(f))
    assert {r["unit"] for r in usage_rows} == {"input", "cache_write_5m", "cache_read", "output"}
    assert sum(float(r["cost_usd"]) for r in usage_rows) == pytest.approx(report["run_spent_usd"], abs=1e-6)
    assert all(r["price_source_url"].startswith("https://") for r in usage_rows)
    assert (out / "checkpoint.json").exists() and (out / "ingestion_report.json").exists()
    with open(out / "pilot_report.json") as f:
        assert json.load(f)["status"] == "ok"

    # resume: nothing pending, warm already recorded -> no new API calls, ledger unchanged
    n_calls = len(client.messages.calls)
    again = pl.run_pilot(path, out, manifest, max_usd=0.25, ledger_path=ledger, client=client, cost_dir=cost_dir)
    assert again["resumed"] and len(client.messages.calls) == n_calls
    assert again["phases"]["warm"]["enrichment_calls"] == 0 and again["phases"]["warm"]["rows_completed_from_cache"] == 98
    assert again["ledger"]["committed_usd"] == pytest.approx(report["ledger"]["committed_usd"])


def test_pilot_stops_at_run_cap_and_global_cap(cost_csv, tmp_path):
    path, manifest = cost_csv
    client = _client()
    report = pl.run_pilot(path, tmp_path / "capped", None, max_usd=0.00001, ledger_path=tmp_path / "l.sqlite", client=client,
                          cost_dir=tmp_path / "c1")
    assert report["status"] == "stopped_run_cap" and client.messages.calls == []
    assert report["final_counts"]["pending"] == 99 and report["ledger"]["committed_usd"] == 0  # 99 nonblank rows

    # global cap: ledger nearly spent by another run
    ledger = tmp_path / "shared.sqlite"
    other = SpendLedger(ledger, cap_usd=1.0, run_id="full")
    other.commit(other.reserve(0.999), 0.999)
    other.close()
    import pipeline.config as cfg
    old = cfg.SPEND_CAP_USD
    cfg.SPEND_CAP_USD = 1.0
    try:
        report = pl.run_pilot(path, tmp_path / "global", None, max_usd=0.25, ledger_path=ledger, client=client,
                              cost_dir=tmp_path / "c2")
    finally:
        cfg.SPEND_CAP_USD = old
    assert report["status"] == "stopped_global_cap" and client.messages.calls == []


def test_pilot_dry_run_makes_no_calls(cost_csv, tmp_path):
    path, manifest = cost_csv
    client = _client()
    out = tmp_path / "dry"
    report = pl.run_pilot(path, out, manifest, ledger_path=tmp_path / "l.sqlite", client=client, dry_run=True,
                          cost_dir=tmp_path / "c")
    assert client.messages.calls == [] and report["dry_run"]
    est = report["dry_run_estimate"]
    assert est["requests"] == 2 and est["texts"] == 97 and 0 < est["worst_case_usd_one_pass"] < 0.05
    assert report["final_counts"]["pending"] == 99 and report["ledger"]["committed_usd"] == 0
    # a real run afterwards starts from clean attempts
    real = pl.run_pilot(path, out, manifest, ledger_path=tmp_path / "l.sqlite", client=client, cost_dir=tmp_path / "c")
    assert real["status"] == "ok" and real["final_counts"]["completed"] == 98


def test_cli_missing_input_and_bad_phase(tmp_path, capsys):
    assert pl.main(["--input", str(tmp_path / "nope.csv"), "--out", str(tmp_path / "o"), "--ledger", str(tmp_path / "l")]) == 1
    assert pl.main(["--input", "x", "--out", "y", "--phases", "hot", "--cost-dir", str(tmp_path / "c")]) == 1


def test_calculator_offline_replay_and_rate_doubling(cost_csv, tmp_path, capsys):
    path, manifest = cost_csv
    out, cost_dir = tmp_path / "pilot100", tmp_path / "cost"
    report = pl.run_pilot(path, out, manifest, ledger_path=tmp_path / "l.sqlite", client=_client(), cost_dir=cost_dir)
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cost"))
    import calculator
    root = Path(__file__).resolve().parent.parent
    full = root / "runs" / "full" / "ingestion_report.json"
    est_path, md_path = tmp_path / "estimate.json", tmp_path / "report.md"
    base_args = ["--pilot", str(out / "pilot_report.json"), "--full", str(full), "--ledger", str(tmp_path / "l.sqlite"),
                 "--out", str(est_path), "--report", str(md_path)]
    assert calculator.main(base_args) == 0
    est = json.loads(est_path.read_text())
    m = est["measured"]
    assert m["input"]["rows"] == 100 and m["records"]["completed"] == 98 and m["records"]["distinct_nonempty_texts"] == 97
    assert m["api_cost_usd"] == pytest.approx(report["run_spent_usd"], abs=5e-6)  # both sides round to 6 dp
    assert m["warm"]["enrichment_calls"] == 0 and m["cold"]["calls"] == 2 and m["stage"]["workers"] == 1
    assert est["population"]["distinct_texts"] == 484189
    sc = est["scenarios"]
    k = "base/exact_text_reuse/batch"
    assert sc[k]["requests"] == 9684 and est["recommended"] == k and sc[k]["within_budget"]
    assert sc[k]["total"] < sc["base/exact_text_reuse/standard"]["total"] < sc["base/no_reuse/standard"]["total"]
    assert sc["conservative/no_reuse/standard"]["total"] > sc["base/no_reuse/standard"]["total"]
    assert sc[k]["already_committed"] > 0
    md = md_path.read_text()
    assert "API total" in md
    rec_line = next(l for l in md.splitlines() if l.startswith("| base | exact_text_reuse | batch |"))
    assert "OVER BUDGET" not in rec_line
    assert any("OVER BUDGET" in l for l in md.splitlines() if l.startswith("| conservative | no_reuse | standard |"))
    assert "| base | exact_text_reuse | batch |" in capsys.readouterr().out

    # T3: doubling every rate with usage fixed doubles API spend and leaves measured time unchanged
    doubled = tmp_path / "rates2.csv"
    with open(root / "cost" / "rates.csv", newline="") as f, open(doubled, "w", newline="") as g:
        r = csv.DictReader(f)
        w = csv.DictWriter(g, fieldnames=r.fieldnames)
        w.writeheader()
        for row in r:
            row["usd_per_mtok"] = str(float(row["usd_per_mtok"]) * 2)
            w.writerow(row)
    assert calculator.main(base_args + ["--rates", str(doubled), "--out", str(tmp_path / "e2.json")]) == 0
    e2 = json.loads((tmp_path / "e2.json").read_text())
    assert e2["measured"]["api_cost_usd"] == pytest.approx(2 * m["api_cost_usd"], abs=2e-8)
    assert e2["measured"]["cold"]["wall_clock_s"] == m["cold"]["wall_clock_s"]
    assert e2["scenarios"][k]["main_run"] == pytest.approx({u: 2 * v for u, v in sc[k]["main_run"].items()}, rel=1e-3)

    # a tiny budget flags every scenario
    assert calculator.main(base_args + ["--budget", "0.01", "--out", str(tmp_path / "e3.json")]) == 0
    assert "OVER BUDGET" in md_path.read_text() and json.loads((tmp_path / "e3.json").read_text())["recommended"] is None

    # no pilot yet: assumptions mode still produces every scenario
    assert calculator.main(["--pilot", str(tmp_path / "none.json"), "--full", str(full), "--ledger", str(tmp_path / "l2.sqlite"),
                            "--out", str(tmp_path / "e4.json"), "--report", str(tmp_path / "r4.md")]) == 0
    e4 = json.loads((tmp_path / "e4.json").read_text())
    assert e4["measured"] is None and e4["params"]["source"].startswith("ASSUMPTIONS") and e4["scenarios"][k]["total"] > 0


def test_keycheck_without_credential(tmp_path, monkeypatch, capsys):
    from pipeline import keycheck
    for var in ("PIPELINE_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setattr(keycheck, "load_dotenv", lambda *a, **k: None)
    assert keycheck.main(["--ledger", str(tmp_path / "l.sqlite")]) == 1
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False and out["credential"]["ok"] is False
    assert out["rates"]["ok"] and "claude-haiku-5-5" in out["rates"]["models"]
    assert out["ledger"]["remaining_usd"] == 20.0 and out["models"] == {"skipped": "no credential"}
    monkeypatch.setenv("PIPELINE_ANTHROPIC_API_KEY", "sk-ant-test-0000")
    assert keycheck.credential_status() == {"ok": True, "source": "PIPELINE_ANTHROPIC_API_KEY",
                                            "prefix": "sk-ant-…", "length": 16}
