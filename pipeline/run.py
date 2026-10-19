"""The staged program: one input CSV path in, every stage out, no chat pasting.

    python -m pipeline.run --input data/raw/extracted/checkpoint_500.csv --out runs/pilot500 --max-usd 0.50
    python -m pipeline.run --input ... --out runs/x --limit 200      # stop after 200 texts (saved progress)
    python -m pipeline.run --input ... --out runs/x                  # resume: finishes pending work, phase=resume
    python -m pipeline.run --input ... --out runs/x --export grading # also write the grading folder

Stages, in order: ingest (once) -> enrich (<=50 reviews/request, saved after every request) -> verify
(blind sample) -> group -> rank -> recommend. Re-running with the same --out resumes: completed
texts are never re-sent and cached downstream outputs are reused. Ctrl-C is safe at any point: the
run DB only ever holds whole batches, the open spend reservation is released, and
<out>/checkpoints/checkpoint_before.json is written; the next run writes checkpoint_after.json.
Standard tier, one worker. The Batch-tier full run is `python -m pipeline.batchrun`.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from . import config
from .budget import BudgetExceeded
from .enricher import FALLBACK_MODEL, MAX_REVIEWS_PER_REQUEST, MODEL
from .fallback import DEFAULT_MAX_FRAC
from .export import export_grading
from .ingest import ingest
from .llm import stage_summary
from .memo import MODEL as MEMO_MODEL
from .pilot import DOWNSTREAM, Pilot, RunCapExceeded, _write_json, check_manifest
from .state import utc_now
from .verifier import DEFAULT_FRAC, DEFAULT_MIN_N

ALL_STAGES = ("enrich", *DOWNSTREAM)


def completed_ids(state) -> list[str]:
    return [r[0] for r in state.conn.execute("SELECT review_id FROM records WHERE status='completed' ORDER BY review_id")]


def write_checkpoint(pilot: Pilot, name: str) -> dict:
    """Snapshot completed_ids. checkpoint_before is written once: a later limited stop must not move it,
    or resume-phase calls made in between would look like re-processing of checkpointed IDs."""
    path = pilot.out_dir / "checkpoints" / name
    if name == "checkpoint_before.json" and path.exists():
        snap = json.loads(path.read_text(encoding="utf-8"))
        return {k: v for k, v in snap.items() if k != "completed_ids"} | {"kept_existing": True}
    ids = completed_ids(pilot.state)
    snap = {"created_at": utc_now(), "run_id": pilot.run_id, "completed_count": len(ids), "completed_ids": ids,
            "counts": pilot.state.status_counts()}
    (pilot.out_dir / "checkpoints").mkdir(parents=True, exist_ok=True)
    _write_json(pilot.out_dir / "checkpoints" / name, snap)
    return {k: v for k, v in snap.items() if k != "completed_ids"}


def run(input_path, out_dir, *, manifest=None, max_usd=1.0, stages=ALL_STAGES, limit=None, memo_model=MEMO_MODEL,
        verify_frac=DEFAULT_FRAC, verify_min_n=DEFAULT_MIN_N, batch_size=MAX_REVIEWS_PER_REQUEST, ledger_path=None,
        client=None, export=None, full_ingestion=None, fallback_frac=DEFAULT_MAX_FRAC) -> dict:
    input_path, out_dir = Path(input_path), Path(out_dir)
    if not input_path.exists():
        raise FileNotFoundError(input_path)
    if not (out_dir / "state.sqlite").exists():
        ingest(input_path, out_dir)
    from .state import RunState
    with RunState(out_dir / "state.sqlite") as probe:   # resume = earlier enrichment calls exist (a dry run also creates the DB)
        resumed = probe.conn.execute("SELECT 1 FROM calls WHERE stage='enrich' LIMIT 1").fetchone() is not None
    downstream = tuple(s for s in stages if s in DOWNSTREAM)
    pilot = Pilot(out_dir, input_path, model=MODEL, max_usd=max_usd, ledger_path=ledger_path, client=client, limit=limit,
                  resumed=resumed, stages=downstream, memo_model=memo_model, verify_frac=verify_frac, verify_min_n=verify_min_n,
                  batch_size=batch_size, fallback_frac=fallback_frac)
    report = {"run_id": pilot.run_id, "started_at": utc_now(), "status": "ok", "resumed": resumed,
              "phase": pilot.contract_phase, "stages": list(stages), "input": {"path": str(input_path), **check_manifest(manifest, input_path)},
              "counts_before": pilot.state.status_counts(), "max_usd": max_usd, "limit": limit}
    try:
        if resumed:
            released = pilot.ledger.release_orphans(pilot.run_id)
            if released:
                pilot.log(f"released {released} orphaned reservation(s) from a previous process")
        if "enrich" in stages:
            pilot.measure_system_prompt()
            try:
                report["enrich"] = pilot.run_cold()
            except KeyboardInterrupt:
                report["status"] = "interrupted"
                report["checkpoint_before"] = write_checkpoint(pilot, "checkpoint_before.json")
                pilot.log(f"interrupted: {report['checkpoint_before']['completed_count']} completed records saved; "
                          f"re-run the same command to resume")
                return report
            if limit is not None and pilot.state.status_counts()["pending"]:
                report["status"] = "stopped_at_limit"
                report["checkpoint_before"] = write_checkpoint(pilot, "checkpoint_before.json")
                pilot.log(f"stopped at --limit with {report['checkpoint_before']['completed_count']} completed; pending work remains")
                return report
            if resumed and (out_dir / "checkpoints" / "checkpoint_before.json").exists():
                report["checkpoint_after"] = write_checkpoint(pilot, "checkpoint_after.json")
        if downstream:
            report["downstream"] = pilot.run_downstream()
    except RunCapExceeded as e:
        report["status"], report["stopped_because"] = "stopped_run_cap", str(e)
        pilot.log(f"STOP: {e}")
    except BudgetExceeded as e:
        report["status"], report["stopped_because"] = "stopped_global_cap", str(e)
        pilot.log(f"STOP: {e}")
    finally:
        report["counts_after"] = pilot.state.status_counts()
        report["checkpoint"] = pilot.state.export_checkpoint(out_dir / "checkpoint.json", run_id=pilot.run_id)
        report["labels_csv_rows"] = pilot.export_labels_csv(out_dir / "labels.csv")
        report["cost_by_stage"] = {r[0]: round(r[1], 6) for r in pilot.state.conn.execute(
            "SELECT stage, COALESCE(SUM(cost_usd_estimate),0) FROM calls WHERE run_id=? GROUP BY stage", (pilot.run_id,))}
        report["stage_calls"] = {st: stage_summary(pilot.state, pilot.run_id, st) for st in ("enrich", "verify", "group", "memo")}
        report["stage_calls"]["fallback"] = stage_summary(pilot.state, pilot.run_id, "enrich", model=FALLBACK_MODEL)
        report["stage_calls"]["enrich"] = stage_summary(pilot.state, pilot.run_id, "enrich", model=MODEL)
        heads = pilot.state.conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(LENGTH(s.review_text)),0) FROM records r JOIN source s USING(review_id) "
            "WHERE r.review_id = r.cache_source_id AND r.status != 'quarantined'").fetchone()
        report["input"].update({"rows": pilot.state.record_count(), "distinct_texts": heads[0], "distinct_text_chars": heads[1]})
        report["model"], report["label_config"], report["tier"] = pilot.model, pilot.cfg, pilot.tier
        report["run_spent_usd"] = round(sum(report["cost_by_stage"].values()), 6)
        report["ledger"] = pilot.ledger.summary()
        report["events"] = pilot.events
        report["finished_at"] = utc_now()
        if export and report["status"] == "ok":
            report["export"] = export_grading(out_dir, export, full_ingestion)
        _write_json(out_dir / "run_report.json", report)
        pilot.close()
    return report


def main(argv=None) -> int:
    import signal
    signal.signal(signal.SIGINT, signal.default_int_handler)   # Ctrl-C / SIGINT -> KeyboardInterrupt even when a parent shell ignored it
    load_dotenv(config.REPO_ROOT / ".env")
    ap = argparse.ArgumentParser(description="Run the staged pipeline on an input CSV.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--out", required=True, help="run directory (its name is the run_id)")
    ap.add_argument("--manifest", help="dataset manifest.json to verify the input checksum")
    ap.add_argument("--max-usd", type=float, default=1.0, help="hard cap for this run, all stages")
    ap.add_argument("--stages", default=",".join(ALL_STAGES))
    ap.add_argument("--limit", type=int, help="enrich at most this many distinct texts, then stop with saved progress")
    ap.add_argument("--memo-model", default=MEMO_MODEL)
    ap.add_argument("--verify-frac", type=float, default=DEFAULT_FRAC)
    ap.add_argument("--verify-min-n", type=int, default=DEFAULT_MIN_N)
    ap.add_argument("--fallback-frac", type=float, default=DEFAULT_MAX_FRAC, help="max fraction of distinct texts routed to Sonnet")
    ap.add_argument("--batch-size", type=int, default=MAX_REVIEWS_PER_REQUEST)
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    ap.add_argument("--export", help="also write the grading folder here when the run completes")
    ap.add_argument("--full-ingestion", help="ingestion_report.json of the full file (for a subset run's export)")
    args = ap.parse_args(argv)
    stages = tuple(s.strip() for s in args.stages.split(",") if s.strip())
    bad = [s for s in stages if s not in ALL_STAGES]
    if bad:
        print(f"run failed: unknown stage(s) {bad}", file=sys.stderr)
        return 1
    try:
        report = run(args.input, args.out, manifest=args.manifest, max_usd=args.max_usd, stages=stages, limit=args.limit,
                     memo_model=args.memo_model, verify_frac=args.verify_frac, verify_min_n=args.verify_min_n,
                     batch_size=args.batch_size, ledger_path=args.ledger, export=args.export, full_ingestion=args.full_ingestion,
                     fallback_frac=args.fallback_frac)
    except (FileNotFoundError, FileExistsError, ValueError) as e:
        print(f"run failed: {e}", file=sys.stderr)
        return 1
    summary = {k: report.get(k) for k in ("status", "run_id", "phase", "counts_after", "cost_by_stage", "run_spent_usd",
                                          "stopped_because", "checkpoint_before", "checkpoint_after")}
    summary["ledger_remaining_usd"] = report["ledger"]["remaining_usd"]
    if report.get("downstream"):
        d = report["downstream"]
        summary["downstream"] = {"wall_s": d["wall_s"], "model_calls": d["model_calls"],
                                 "verify": {k: d["verify"][k] for k in ("verified", "agreement", "planted_errors")} if "verify" in d else None,
                                 "issues": d.get("group", {}).get("issues"), "memo_status": d.get("recommend", {}).get("status"),
                                 "fallback": {k: d["fallback"][k] for k in ("eligible", "routed", "completed", "still_quarantined", "cost_usd")} if "fallback" in d else None}
    print(json.dumps(summary, indent=2, default=str))
    return 0 if report["status"] in ("ok", "stopped_at_limit", "interrupted") else 2


if __name__ == "__main__":
    sys.exit(main())
