"""Full-corpus enrichment on the Message Batches API (50% off), with the same safety rails as the pilot.

    python -m pipeline.batchrun --input data/raw/extracted/spotify_reviews_18months.csv --out runs/full \
        --max-usd 12 --dry-run                       # count requests, price the worst case, no API calls
    python -m pipeline.batchrun --input ... --out runs/full --max-usd 12 --batch-requests 1000
    python -m pipeline.batchrun --input ... --out runs/full --max-usd 12 --downstream   # verify/group/rank/memo after

How it works
  * pending distinct texts are packed into requests of <= 50 reviews; up to --batch-requests requests
    form one Message Batch (custom_id = our call id);
  * before a batch is submitted, its worst-case cost (batch-tier rates, max_tokens of output) is
    reserved in the shared ledger and checked against --max-usd; the submission is recorded in the
    run DB (`batch_jobs`, `batch_requests`) BEFORE the API call returns, so an interrupted process can
    reconcile the in-flight batch instead of re-sending it (and paying twice);
  * results are fetched when the batch ends; every request becomes one call row (succeeded or
    failed) and its labels are committed atomically with RunState.commit_batch, exactly like the
    standard-tier pilot. Invalid records are retried once in a later batch, then quarantined;
  * Ctrl-C at any point is safe: the server keeps processing, and the next start resumes by polling
    the unfinished batches first; checkpoint.json is refreshed after every batch.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv

from . import config, pricing
from .budget import BudgetExceeded, SpendLedger
from .enricher import MAX_ATTEMPTS, MAX_REVIEWS_PER_REQUEST, MODEL, build_request, estimate_prompt_tokens, label_config, parse_response
from .ingest import ingest
from .llm import RunCapExceeded, make_client
from .pilot import DOWNSTREAM, Pilot, _write_json
from .state import RunState, utc_now

STAGE, TIER = "enrich", "batch"
BATCH_DDL = """
CREATE TABLE IF NOT EXISTS batch_jobs (
    batch_id       TEXT PRIMARY KEY,          -- local job id (known before the API answers)
    api_batch_id   TEXT,                      -- provider's message batch id once submitted
    run_id         TEXT,
    phase          TEXT,
    n_requests     INTEGER,
    n_texts        INTEGER,
    reservation_id TEXT,
    reserved_usd   REAL,
    status         TEXT NOT NULL CHECK (status IN ('submitting','in_progress','collected','failed')),
    submitted_at   TEXT,
    ended_at       TEXT,
    collected_at   TEXT,
    error          TEXT
);
CREATE TABLE IF NOT EXISTS batch_requests (
    custom_id   TEXT PRIMARY KEY,
    batch_id    TEXT NOT NULL REFERENCES batch_jobs(batch_id),
    review_ids  TEXT NOT NULL,
    head_ids    TEXT NOT NULL,
    max_tokens  INTEGER,
    collected   INTEGER NOT NULL DEFAULT 0
);
"""


class BatchRunner:
    def __init__(self, out_dir, *, model=MODEL, max_usd: float, batch_requests: int = 1000, poll_s: int = 60,
                 ledger_path=None, client=None, dry_run=False, rates=None, resumed=False):
        self.out_dir = Path(out_dir)
        self.run_id = self.out_dir.name
        self.model, self.max_usd, self.batch_requests, self.poll_s = model, float(max_usd), batch_requests, poll_s
        self.dry_run = dry_run
        self.rates = rates if rates is not None else pricing.load_rates()
        self.cfg = label_config(model)
        self.state = RunState(self.out_dir / "state.sqlite")
        self.state.conn.executescript(BATCH_DDL)
        cols = {r[1] for r in self.state.conn.execute("PRAGMA table_info(batch_jobs)")}
        if "api_batch_id" not in cols:   # DB created by an earlier version of this table
            self.state.conn.execute("ALTER TABLE batch_jobs ADD COLUMN api_batch_id TEXT")
        self.ledger = SpendLedger(ledger_path, run_id=self.run_id)
        self._client = client
        self.phase = "resume" if resumed else "initial"
        self.events: list[str] = []
        self.system_tokens: int | None = None

    @property
    def client(self):
        if self._client is None:
            self._client = make_client()
        return self._client

    def log(self, msg: str) -> None:
        self.events.append(f"{utc_now()} {msg}")
        print(msg, file=sys.stderr, flush=True)

    def close(self):
        self.state.close()
        self.ledger.close()

    def run_spent(self) -> float:
        return float(self.state.conn.execute(
            "SELECT COALESCE(SUM(cost_usd_estimate),0) FROM calls WHERE run_id=?", (self.run_id,)).fetchone()[0])

    # ---- building ---------------------------------------------------------------

    def next_batch_requests(self) -> list[dict]:
        """Up to batch_requests requests of <= 50 pending distinct texts each.

        Texts whose previous request failed as a whole (API error, expiry) are re-sent one per request,
        so a single bad text cannot take 49 good ones down with it a second time.
        """
        groups = self.state.pending_text_groups(self.batch_requests * MAX_REVIEWS_PER_REQUEST)
        heads = [g["cache_source_id"] for g in groups]
        reasons = {}
        for i in range(0, len(heads), 500):
            chunk = heads[i:i + 500]
            reasons.update({r[0]: r[1] for r in self.state.conn.execute(
                f"SELECT review_id, reason FROM records WHERE review_id IN ({','.join('?' * len(chunk))})", chunk)})
        singles = [g for g in groups if (reasons.get(g["cache_source_id"]) or "").startswith("batch_")]
        normal = [g for g in groups if g not in singles]
        chunks = [[g] for g in singles] + [normal[i:i + MAX_REVIEWS_PER_REQUEST] for i in range(0, len(normal), MAX_REVIEWS_PER_REQUEST)]
        reqs = []
        for chunk in chunks[: self.batch_requests]:
            texts = [g["review_text"] for g in chunk]
            params = build_request(texts, self.model)
            reqs.append({"custom_id": uuid.uuid4().hex, "params": params, "groups": chunk,
                         "est_prompt": estimate_prompt_tokens(params, self.system_tokens),
                         "est_max": pricing.max_cost(self.model, TIER, estimate_prompt_tokens(params, self.system_tokens),
                                                     params["max_tokens"], self.rates)})
        return reqs

    # ---- submit / collect -----------------------------------------------------------

    def submit(self, reqs: list[dict]) -> str:
        est_max = sum(r["est_max"] for r in reqs)
        if self.run_spent() + est_max > self.max_usd + 1e-9:
            raise RunCapExceeded(f"next batch could cost ${est_max:.4f}; run has spent ${self.run_spent():.4f} of --max-usd {self.max_usd:.2f}")
        reservation = self.ledger.reserve(est_max, call_id=f"batch-{self.run_id}")
        local_id = f"local-{uuid.uuid4().hex}"
        with self.state.transaction() as c:   # record intent before the network call
            c.execute("INSERT INTO batch_jobs(batch_id,run_id,phase,n_requests,n_texts,reservation_id,reserved_usd,status,submitted_at) "
                      "VALUES (?,?,?,?,?,?,?,'submitting',?)",
                      (local_id, self.run_id, self.phase, len(reqs), sum(len(r["groups"]) for r in reqs), reservation.reservation_id,
                       est_max, utc_now()))
            c.executemany("INSERT INTO batch_requests(custom_id,batch_id,review_ids,head_ids,max_tokens) VALUES (?,?,?,?,?)",
                          [(r["custom_id"], local_id, json.dumps([rid for g in r["groups"] for rid in g["review_ids"]]),
                            json.dumps([g["cache_source_id"] for g in r["groups"]]), r["params"]["max_tokens"]) for r in reqs])
        self.state.set_meta(f"reservation:{local_id}", {"reservation_id": reservation.reservation_id, "amount_usd": est_max,
                                                        "call_id": reservation.call_id, "run_id": reservation.run_id})
        try:
            batch = self.client.messages.batches.create(requests=[{"custom_id": r["custom_id"], "params": r["params"]} for r in reqs])
        except BaseException as e:
            with self.state.transaction() as c:
                c.execute("UPDATE batch_jobs SET status='failed', error=?, ended_at=? WHERE batch_id=?",
                          (f"{type(e).__name__}: {str(e)[:300]}", utc_now(), local_id))
            self.ledger.release(reservation)
            raise
        with self.state.transaction() as c:
            c.execute("UPDATE batch_jobs SET api_batch_id=?, status='in_progress' WHERE batch_id=?", (batch.id, local_id))
        self.log(f"submitted batch {batch.id} (job {local_id}): {len(reqs)} requests, {sum(len(r['groups']) for r in reqs)} texts, "
                 f"reserved worst case ${est_max:.4f}")
        return local_id

    def api_id(self, job_id: str) -> str:
        return self.state.conn.execute("SELECT api_batch_id FROM batch_jobs WHERE batch_id=?", (job_id,)).fetchone()[0]

    def wait(self, job_id: str):
        batch_id = self.api_id(job_id)
        while True:
            b = self.client.messages.batches.retrieve(batch_id)
            if b.processing_status == "ended":
                return b
            rc = b.request_counts
            self.log(f"batch {batch_id} {b.processing_status}: processing={rc.processing} succeeded={rc.succeeded} "
                     f"errored={rc.errored} expired={rc.expired} canceled={rc.canceled}; next poll in {self.poll_s}s")
            time.sleep(self.poll_s)

    def collect(self, job_id: str) -> dict:
        """Fetch results, commit every request atomically, settle the ledger reservation."""
        from .budget import Reservation
        batch_id = job_id
        api_batch_id = self.api_id(job_id)
        meta = self.state.get_meta(f"reservation:{job_id}")
        reqs = {r["custom_id"]: dict(r) for r in self.state.conn.execute(
            "SELECT * FROM batch_requests WHERE batch_id=? AND collected=0", (batch_id,))}
        totals = {"succeeded": 0, "failed": 0, "completed": 0, "quarantined": 0, "retried": 0, "cost_usd": 0.0}
        for item in self.client.messages.batches.results(api_batch_id):
            req = reqs.get(item.custom_id)
            if req is None:
                continue
            head_ids = json.loads(req["head_ids"])
            groups = self._groups_for(head_ids)
            texts = [g["review_text"] for g in groups]
            base = {"call_id": item.custom_id, "run_id": self.run_id, "stage": STAGE, "phase": self.phase, "model": self.model,
                    "label_config": self.cfg, "request_review_ids": head_ids, "attempt": 1, "service_tier": TIER,
                    "started_at": None, "ended_at": utc_now(), "duration_s": None}
            if item.result.type != "succeeded":
                err = getattr(getattr(item.result, "error", None), "error", None)
                msg = f"{item.result.type}: {getattr(err, 'type', '')} {getattr(err, 'message', '')}".strip()
                attempts = self._attempts(head_ids)
                retries, quarantines = [], []
                for g in groups:
                    done = attempts.get(g["review_ids"][0], 0) + 1
                    (quarantines if done >= MAX_ATTEMPTS else retries).append(
                        {"review_ids": g["review_ids"], "reason": f"batch_{item.result.type} (attempt {done}): {msg[:160]}"})
                counts = self.state.commit_batch([], quarantines, {**base, "status": "failed", "error": msg[:300]}, retries)
                totals["failed"] += 1
            else:
                msg_obj = item.result.message
                usage = msg_obj.usage
                cost = pricing.cost_of(usage, self.model, TIER, self.rates)
                parsed = parse_response(msg_obj, texts)
                attempts = self._attempts(head_ids)
                results, retries, quarantines = [], [], []
                for k, g in enumerate(groups):
                    if k in parsed.labels:
                        results.append({"review_ids": g["review_ids"], "label": parsed.labels[k], "label_config": self.cfg})
                        continue
                    reason = parsed.invalid[k]
                    done = attempts.get(g["review_ids"][0], 0) + 1
                    if reason.startswith("refusal") and len(groups) > 1 and done < MAX_ATTEMPTS:
                        # the whole request was refused; re-send each text alone so one review cannot sink 49 others
                        retries.append({"review_ids": g["review_ids"], "reason": f"batch_{reason}"})
                    elif reason.startswith("refusal") or done >= MAX_ATTEMPTS:
                        quarantines.append({"review_ids": g["review_ids"], "reason": f"{reason} (attempt {done})"})
                    else:
                        retries.append({"review_ids": g["review_ids"], "reason": reason})
                row = {**base, "status": "invalid" if (parsed.invalid and not parsed.labels) else "success",
                       "error": parsed.error or (f"{len(parsed.invalid)} invalid records" if parsed.invalid else None),
                       "input_tokens": getattr(usage, "input_tokens", 0) or 0,
                       "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
                       "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
                       "output_tokens": getattr(usage, "output_tokens", 0) or 0, "cost_usd_estimate": cost}
                counts = self.state.commit_batch(results, quarantines, row, retries)
                totals["succeeded"] += 1
                totals["cost_usd"] += cost
            for k in ("completed", "quarantined", "retried"):
                totals[k] += counts[k]
            with self.state.transaction() as c:
                c.execute("UPDATE batch_requests SET collected=1 WHERE custom_id=?", (item.custom_id,))
        missing = [cid for cid in reqs if not self.state.conn.execute(
            "SELECT collected FROM batch_requests WHERE custom_id=?", (cid,)).fetchone()[0]]
        for cid in missing:   # the API returned no result for a request we sent: treat as failed, retry its texts
            req = reqs[cid]
            head_ids = json.loads(req["head_ids"])
            groups = self._groups_for(head_ids)
            self.state.commit_batch([], [], {"call_id": cid, "run_id": self.run_id, "stage": STAGE, "phase": self.phase, "model": self.model,
                                             "label_config": self.cfg, "request_review_ids": head_ids, "attempt": 1, "service_tier": TIER,
                                             "status": "failed", "error": "no result returned for custom_id", "ended_at": utc_now()},
                                    [{"review_ids": g["review_ids"], "reason": "batch_no_result"} for g in groups])
            with self.state.transaction() as c:
                c.execute("UPDATE batch_requests SET collected=1 WHERE custom_id=?", (cid,))
            totals["failed"] += 1
        if meta:
            res = Reservation(meta["reservation_id"], meta["amount_usd"], meta.get("run_id"), meta.get("call_id"))
            try:
                self.ledger.commit(res, totals["cost_usd"], call_id=f"batch-{api_batch_id}")
            except ValueError:
                self.log(f"reservation for {batch_id} was already settled")
        with self.state.transaction() as c:
            c.execute("UPDATE batch_jobs SET status='collected', collected_at=?, ended_at=COALESCE(ended_at, ?) WHERE batch_id=?",
                      (utc_now(), utc_now(), batch_id))
        self.state.export_checkpoint(self.out_dir / "checkpoint.json", run_id=self.run_id)
        self.log(f"collected batch {api_batch_id}: {totals['succeeded']} ok, {totals['failed']} failed requests; "
                 f"{totals['completed']} completed, {totals['quarantined']} quarantined, {totals['retried']} to retry; ${totals['cost_usd']:.4f}")
        return totals

    def _groups_for(self, head_ids: list[str]) -> list[dict]:
        out = []
        for hid in head_ids:
            text = self.state.conn.execute("SELECT review_text FROM source WHERE review_id=?", (hid,)).fetchone()[0]
            ids = [r[0] for r in self.state.conn.execute(
                "SELECT review_id FROM records WHERE cache_source_id=? AND status='pending' ORDER BY row_index", (hid,))]
            out.append({"cache_source_id": hid, "review_text": text, "review_ids": ids or [hid]})
        return out

    def _attempts(self, head_ids: list[str]) -> dict:
        return {r[0]: r[1] for r in self.state.conn.execute(
            f"SELECT review_id, attempts FROM records WHERE review_id IN ({','.join('?' * len(head_ids))})", head_ids)}

    # ---- main loop --------------------------------------------------------------------

    def reconcile(self) -> int:
        """Collect batches a previous process left in flight (never re-send them)."""
        open_jobs = [(r[0], r[1]) for r in self.state.conn.execute(
            "SELECT batch_id, api_batch_id FROM batch_jobs WHERE status IN ('in_progress','submitting') ORDER BY submitted_at")]
        n = 0
        for bid, api_id in open_jobs:
            if not api_id:   # crashed between the local record and the API answer: outcome unknown, nothing was charged
                self.log(f"job {bid} never got an API id (process died mid-submit); its reservation is released and its texts stay pending")
                with self.state.transaction() as c:
                    c.execute("UPDATE batch_jobs SET status='failed', error='no API id recorded', ended_at=? WHERE batch_id=?", (utc_now(), bid))
                self.ledger.release_orphans(self.run_id)
                continue
            self.log(f"reconciling in-flight batch {api_id}")
            self.wait(bid)
            self.collect(bid)
            n += 1
        return n

    def run(self) -> dict:
        t0 = time.monotonic()
        summary = {"batches": 0, "requests": 0, "texts": 0, "cost_usd": 0.0, "dry_run": self.dry_run}
        if not self.dry_run:
            summary["reconciled"] = self.reconcile()
        while True:
            reqs = self.next_batch_requests()
            if not reqs:
                break
            if self.dry_run:
                summary["batches"] += 1
                summary["requests"] += len(reqs)
                summary["texts"] += sum(len(r["groups"]) for r in reqs)
                summary["worst_case_usd"] = summary.get("worst_case_usd", 0.0) + sum(r["est_max"] for r in reqs)
                # park the groups so the loop advances; restored below
                self.state.commit_batch([], quarantines=[{"review_ids": g["review_ids"], "reason": "dry_run"} for r in reqs for g in r["groups"]])
                continue
            bid = self.submit(reqs)
            self.wait(bid)
            tot = self.collect(bid)
            summary["batches"] += 1
            summary["requests"] += len(reqs)
            summary["texts"] += sum(len(r["groups"]) for r in reqs)
            summary["cost_usd"] += tot["cost_usd"]
        if self.dry_run:
            self.state.conn.execute("UPDATE records SET status='pending', attempts=0, reason=NULL WHERE reason='dry_run'")
        summary["wall_s"] = round(time.monotonic() - t0, 1)
        summary["counts"] = self.state.status_counts()
        return summary


def main(argv=None) -> int:
    load_dotenv(config.REPO_ROOT / ".env")
    ap = argparse.ArgumentParser(description="Batch-tier enrichment of a (large) review CSV.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-usd", type=float, required=True, help="hard cap for this run (the $20 ledger cap still applies)")
    ap.add_argument("--batch-requests", type=int, default=1000, help="requests per Message Batch (<= 50 texts each)")
    ap.add_argument("--poll", type=int, default=60, help="seconds between status polls")
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--downstream", action="store_true", help="after enrichment: verify, group, rank, recommend (standard tier)")
    args = ap.parse_args(argv)
    out = Path(args.out)
    resumed = (out / "state.sqlite").exists()
    if not resumed:
        ingest(args.input, out)
    runner = BatchRunner(out, max_usd=args.max_usd, batch_requests=args.batch_requests, poll_s=args.poll,
                         ledger_path=args.ledger, dry_run=args.dry_run, resumed=resumed)
    report = {"run_id": runner.run_id, "started_at": utc_now(), "tier": TIER, "model": runner.model, "label_config": runner.cfg,
              "phase": runner.phase, "resumed": resumed, "max_usd": args.max_usd, "batch_requests": args.batch_requests}
    status = "ok"
    try:
        report["enrich"] = runner.run()
        if args.downstream and not args.dry_run and runner.state.status_counts()["pending"] == 0:
            pilot = Pilot(out, args.input, max_usd=args.max_usd, ledger_path=args.ledger, resumed=resumed, stages=DOWNSTREAM)
            try:
                report["downstream"] = pilot.run_downstream()
            finally:
                pilot.state.close()
                pilot.ledger.close()
    except KeyboardInterrupt:
        status = "interrupted"
        runner.log("interrupted: any submitted batch keeps running server-side; re-run the same command to collect it")
    except RunCapExceeded as e:
        status, report["stopped_because"] = "stopped_run_cap", str(e)
    except BudgetExceeded as e:
        status, report["stopped_because"] = "stopped_global_cap", str(e)
    finally:
        report["status"] = status
        report["counts"] = runner.state.status_counts()
        report["run_spent_usd"] = round(runner.run_spent(), 6)
        report["ledger"] = runner.ledger.summary()
        report["events"] = runner.events
        report["finished_at"] = utc_now()
        _write_json(out / ("batchrun_dry_run.json" if args.dry_run else "batchrun_report.json"), report)
        runner.close()
    print(json.dumps({k: report.get(k) for k in ("status", "run_id", "phase", "enrich", "counts", "run_spent_usd", "stopped_because")},
                     indent=2, default=str))
    return 0 if status == "ok" else 2


if __name__ == "__main__":
    sys.exit(main())
