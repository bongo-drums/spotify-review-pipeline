"""Export the grading folder described in GRADING_CONTRACT.md from a run directory. No model calls.

    python -m pipeline.export --run runs/full --out grading \
        [--full-ingestion runs/full/ingestion_report.json]

Files: run.json, ingestion.json, records.jsonl(.gz), membership.csv, ranking.csv, claims.csv,
calls.jsonl, checkpoint_before.json, checkpoint_after.json (the last two are copied from
<run>/checkpoints/ when the interruption/resume demo saved them).
"""
from __future__ import annotations

import argparse
import gzip
import json
import shutil
import sys
from pathlib import Path

from .state import RunState

VERSION = "a5-audit-v1"
ROLES = ("enrich", "verify", "group", "memo")
RECORD_FIELDS = ("topic", "intent", "sentiment", "severity", "entities", "evidence_quote", "needs_review")
PHASE_MAP = {"cold": "initial", "cold_resume": "resume", "initial": "initial", "resume": "resume"}


def _write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def export_records(state: RunState, path: Path, compress: bool) -> dict:
    counts = {"completed": 0, "quarantined": 0, "pending_as_quarantined": 0, "cache_aliases": 0}
    opener = (lambda p: gzip.open(p, "wt", encoding="utf-8")) if compress else (lambda p: open(p, "w", encoding="utf-8"))
    with opener(path) as f:
        for r in state.conn.execute("SELECT review_id, source_sha256, cache_source_id, status, label, label_config, reason "
                                    "FROM records ORDER BY row_index"):
            rec = {"review_id": r["review_id"], "source_sha256": r["source_sha256"]}
            if r["status"] == "completed":
                lab = json.loads(r["label"])
                rec["status"] = "completed"
                rec.update({k: lab[k] for k in RECORD_FIELDS})
                rec["label_config"] = r["label_config"]
                rec["subtopic"] = lab.get("subtopic")
                if r["cache_source_id"] != r["review_id"]:
                    rec["cache_source_id"] = r["cache_source_id"]
                    counts["cache_aliases"] += 1
                counts["completed"] += 1
            else:
                rec["status"] = "quarantined"
                if r["status"] == "pending":  # an unfinished run: account for the row honestly, it is not a success
                    rec["reason"] = "not_classified_run_incomplete"
                    counts["pending_as_quarantined"] += 1
                else:
                    rec["reason"] = r["reason"] or "unknown"
                    counts["quarantined"] += 1
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return counts


def export_calls(state: RunState, run_id: str, path: Path) -> dict:
    n, by_role = 0, {}
    with open(path, "w", encoding="utf-8") as f:
        for r in state.conn.execute("SELECT * FROM calls WHERE run_id=? ORDER BY started_at", (run_id,)):
            if r["stage"] not in ROLES:
                continue
            ids = json.loads(r["request_review_ids"] or "[]")
            entry = {"request_id": r["call_id"], "role": r["stage"], "review_ids": ids, "model": r["model"],
                     "phase": PHASE_MAP.get(r["phase"], r["phase"]),
                     "outcome": "failed" if r["status"] == "failed" else "succeeded",
                     "label_config": r["label_config"] if r["stage"] == "enrich" else (r["label_config"] or None),
                     "input_tokens": int(r["input_tokens"] or 0), "output_tokens": int(r["output_tokens"] or 0),
                     "cache_creation_input_tokens": int(r["cache_creation_input_tokens"] or 0),
                     "cache_read_input_tokens": int(r["cache_read_input_tokens"] or 0),
                     "service_tier": r["service_tier"], "validation": r["status"], "error": r["error"],
                     "attempt": r["attempt"], "started_at": r["started_at"], "duration_s": r["duration_s"],
                     "cost_usd": r["cost_usd_estimate"]}
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            n += 1
            by_role[r["stage"]] = by_role.get(r["stage"], 0) + 1
    return {"calls": n, "by_role": by_role}


def export_grading(run_dir, out_dir, full_ingestion_report=None, compress: bool | None = None) -> dict:
    run_dir, out_dir = Path(run_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((run_dir / "data_manifest.json").read_text(encoding="utf-8"))
    ingestion = json.loads(Path(full_ingestion_report or run_dir / "ingestion_report.json").read_text(encoding="utf-8"))
    run = {"version": VERSION, "analysis_count": manifest["row_count"], "analysis_sha256": manifest["source_sha256"],
           "classification_input_fields": ["review_text"], "allow_multi_issue": False}
    _write_json(out_dir / "run.json", run)
    _write_json(out_dir / "ingestion.json", ingestion["checker_profile"])
    info = {"run": run, "out": str(out_dir)}
    with RunState(run_dir / "state.sqlite") as state:
        if compress is None:
            compress = state.record_count() > 50_000
        for stale in ("records.jsonl", "records.jsonl.gz"):
            (out_dir / stale).unlink(missing_ok=True)
        info["records"] = export_records(state, out_dir / ("records.jsonl.gz" if compress else "records.jsonl"), compress)
        info["calls"] = export_calls(state, run_dir.name, out_dir / "calls.jsonl")
    art = run_dir / "artifacts"
    for name in ("membership.csv", "ranking.csv", "claims.csv"):
        src = art / name
        if src.exists():
            shutil.copyfile(src, out_dir / name)
        else:
            info.setdefault("missing", []).append(name)
    for name in ("checkpoint_before.json", "checkpoint_after.json"):
        src = run_dir / "checkpoints" / name
        if src.exists():
            shutil.copyfile(src, out_dir / name)
        else:
            info.setdefault("missing", []).append(name)
    _write_json(out_dir / "export_info.json", {**info, "note": "written by pipeline.export; not part of the contract's file list"})
    return info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Export the GRADING_CONTRACT.md folder from a run (offline).")
    ap.add_argument("--run", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--full-ingestion", help="ingestion_report.json of the FULL file when the run is a subset")
    ap.add_argument("--gzip", action="store_true", help="write records.jsonl.gz (default above 50k rows)")
    args = ap.parse_args(argv)
    info = export_grading(args.run, args.out, args.full_ingestion, compress=True if args.gzip else None)
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
