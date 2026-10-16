"""The 100-review cold/warm pilot (COST_CALCULATOR.md section 2). PAID: a few cents.

Usage:
    python -m pipeline.pilot --input data/raw/extracted/cost_100.csv \
        --manifest data/raw/extracted/manifest.json --out runs/pilot100 --max-usd 0.25

Cold run: fresh run DB with an empty result cache, one worker, real enrichment calls.
Warm run: a second fresh run DB that imports the cold run's result cache; it must make
zero enrichment calls under the same label_config.

Writes <out>/pilot_summary.json and the submission evidence in cost/:
pilot_records.jsonl, pilot_calls.jsonl, usage.csv, pilot_summary.json.
Stages after enrichment (verify, group, rank, memo) are not built yet; the summary
lists them as not run instead of reporting zero cost for them.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import sys
import time
from pathlib import Path

from . import config, enrich, pricing
from .budget import SpendLedger
from .hashing import file_sha256
from .ingest import git_commit, ingest
from .state import RunState, utc_now

COST_DIR = config.REPO_ROOT / "cost"
GOLDEN_DIR = (config.REPO_ROOT / "evals" / "golden").resolve()
NOT_YET_BUILT = ["verify", "group", "rank", "memo"]


def verify_input(input_path: Path, manifest_path: Path) -> dict:
    """The pilot must use cost_100.csv unchanged: check bytes and sha256 against manifest.json."""
    if GOLDEN_DIR in input_path.resolve().parents:
        raise ValueError("refusing to send anything under evals/golden/ to a model")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest["files"][input_path.name]
    actual = {"bytes": input_path.stat().st_size, "sha256": file_sha256(input_path)}
    if actual != {"bytes": expected["bytes"], "sha256": expected["sha256"]}:
        raise ValueError(f"{input_path.name} does not match manifest.json: {actual} != {expected}")
    return {"file": input_path.name, **actual, "manifest_sha256": file_sha256(manifest_path)}


def _run_one(kind: str, input_path: Path, run_dir: Path, client, ledger_path, run_cap: float | None,
             cache_from: Path | None) -> dict:
    run_id = f"pilot100-{kind}-{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}"
    wall0 = time.monotonic()
    t = time.monotonic()
    report = ingest(input_path, run_dir)
    ingest_s = time.monotonic() - t

    state = RunState(run_dir / "state.sqlite")
    ledger = SpendLedger(ledger_path, run_id=run_id)
    imported = 0
    if cache_from is not None:
        imported = enrich.import_label_cache(state, cache_from, enrich.label_config())
    enricher = enrich.Enricher(state, ledger, client, run_id, phase="initial", run_cap_usd=run_cap,
                               log_path=run_dir / "enrich_calls.jsonl")
    t = time.monotonic()
    stats = enricher.run()
    enrich_s = time.monotonic() - t
    snap = state.export_checkpoint(run_dir / "checkpoint_final.json", run_id=run_id)
    state.close()
    ledger.close()
    wall_s = time.monotonic() - wall0
    counts = stats["status_counts"]
    return {
        "kind": kind, "run_id": run_id, "run_dir": str(run_dir), "finished_at": utc_now(),
        "records": report["rows"]["total"],
        "unique_nonblank_texts": report["review_text"]["distinct_nonblank_texts"],
        "result_cache_entries_imported": imported,
        "result_cache_hits": stats["cache_completed"],
        "completed": counts["completed"], "quarantined": counts["quarantined"], "pending": counts["pending"],
        "enrich": {k: stats[k] for k in ("requests", "attempts", "failed_attempts", "retried", "usage")}
                  | {"cost_usd": round(stats["cost_usd"], 8)},
        "time_s": {"ingest": round(ingest_s, 3), "enrich": round(enrich_s, 3), "end_to_end": round(wall_s, 3)},
        "completed_ids_sha256": snap["completed_ids_sha256"],
    }


def export_records(run_dir: Path, path: Path) -> int:
    """One record per pilot ID with the contract's row hash and common labels."""
    conn = RunState(run_dir / "state.sqlite")
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for r in conn.conn.execute("SELECT * FROM records ORDER BY row_index"):
            rec = {"review_id": r["review_id"], "source_sha256": r["source_sha256"], "status": r["status"]}
            if r["status"] == "completed":
                label = json.loads(r["label"])
                rec |= {k: label[k] for k in ("topic", "intent", "sentiment", "severity", "entities",
                                              "evidence_quote", "needs_review")}
                rec |= {"subtopic": label["subtopic"], "label_config": r["label_config"]}
                if r["cache_source_id"] != r["review_id"]:
                    rec["cache_source_id"] = r["cache_source_id"]
            else:
                rec["reason"] = r["reason"] or "pending"
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    conn.close()
    return n


def export_calls(runs: list[dict], calls_path: Path, usage_path: Path) -> int:
    """pilot_calls.jsonl (contract role names) and usage.csv (one row per call x billing unit)."""
    n = 0
    with open(calls_path, "w", encoding="utf-8") as fc, open(usage_path, "w", newline="", encoding="utf-8") as fu:
        w = csv.writer(fu)
        w.writerow(["run_kind", "run_id", "request_id", "call_id", "role", "model", "tier", "unit", "tokens"])
        for run in runs:
            log = Path(run["run_dir"]) / "enrich_calls.jsonl"
            if not log.exists():
                continue
            for line in log.read_text(encoding="utf-8").splitlines():
                e = json.loads(line)
                out = {
                    "request_id": e["request_id"] or e["call_id"], "call_id": e["call_id"],
                    "run_kind": run["kind"], "run_id": e["run_id"], "role": "enrich", "phase": e["phase"],
                    "outcome": e["outcome"], "review_ids": e["request_review_ids"], "model": e["model"],
                    "label_config": e["label_config"], "effort": enrich.EFFORT, "thinking": "disabled",
                    "service_tier": e["service_tier"], "attempt": e["attempt"], "stop_reason": e["stop_reason"],
                    "error": e["error"], "started_at": e["started_at"], "ended_at": e["ended_at"],
                    "duration_s": e["duration_s"], "cost_usd": e["cost_usd_estimate"],
                }
                for field in pricing.USAGE_UNITS:
                    out[field] = e.get(field)
                fc.write(json.dumps(out, ensure_ascii=False) + "\n")
                for field, unit in pricing.USAGE_UNITS.items():
                    if e.get(field):
                        w.writerow([run["kind"], e["run_id"], out["request_id"], e["call_id"], "enrich",
                                    e["model"], e["service_tier"], unit, e[field]])
                n += 1
    return n


def run_pilot(input_path, manifest_path, out_dir, *, client, ledger_path=None, run_cap=0.25,
              force=False, cost_dir=COST_DIR) -> dict:
    input_path, manifest_path, out_dir = Path(input_path), Path(manifest_path), Path(out_dir)
    identity = verify_input(input_path, manifest_path)
    if out_dir.exists():
        if not force:
            raise FileExistsError(f"{out_dir} exists; pass --force to delete it and run a new paid pilot")
        shutil.rmtree(out_dir)
    ledger_path = ledger_path or config.LEDGER_DB_PATH

    cold = _run_one("cold", input_path, out_dir / "cold", client, ledger_path, run_cap, cache_from=None)
    warm = _run_one("warm", input_path, out_dir / "warm", client, ledger_path, run_cap,
                    cache_from=out_dir / "cold" / "state.sqlite")
    ledger = SpendLedger(ledger_path)
    summary = {
        "generated_at": utc_now(),
        "input": identity,
        "code": git_commit(),
        "settings": {"enrich": {"provider": "anthropic", "model": enrich.MODEL, "effort": enrich.EFFORT,
                                "thinking": "disabled", "prompt_version": enrich.PROMPT_VERSION,
                                "schema_version": enrich.SCHEMA_VERSION, "label_config": enrich.label_config(),
                                "batch_size": enrich.MAX_BATCH, "retry_batch_size": enrich.RETRY_BATCH,
                                "workers": 1, "tier": "standard",
                                "max_output_tokens_per_request": enrich.max_output_tokens(enrich.MAX_BATCH)}},
        "stages_not_run": NOT_YET_BUILT,
        "cold": cold,
        "warm": warm,
        "warm_zero_enrichment_calls": warm["enrich"]["attempts"] == 0,
        "ledger_after": ledger.summary(),
    }
    ledger.close()
    (out_dir / "pilot_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    cost_dir = Path(cost_dir)
    cost_dir.mkdir(parents=True, exist_ok=True)
    summary["exports"] = {
        "pilot_records": export_records(out_dir / "cold", cost_dir / "pilot_records.jsonl"),
        "pilot_calls": export_calls([cold, warm], cost_dir / "pilot_calls.jsonl", cost_dir / "usage.csv"),
    }
    (cost_dir / "pilot_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the PAID 100-review cold/warm pilot.")
    ap.add_argument("--input", default="data/raw/extracted/cost_100.csv")
    ap.add_argument("--manifest", default="data/raw/extracted/manifest.json")
    ap.add_argument("--out", default="runs/pilot100")
    ap.add_argument("--max-usd", type=float, default=0.25, help="per-run sub-cap (cold and warm each)")
    ap.add_argument("--ledger", default=os.fspath(config.LEDGER_DB_PATH))
    ap.add_argument("--force", action="store_true", help="delete an existing --out and rerun (costs money)")
    args = ap.parse_args(argv)
    try:
        client = enrich.make_client()
        s = run_pilot(args.input, args.manifest, args.out, client=client, ledger_path=args.ledger,
                      run_cap=args.max_usd, force=args.force)
    except (enrich.EnrichAborted, FileExistsError, ValueError) as e:
        print(f"pilot stopped: {e}", file=sys.stderr)
        return 2
    brief = {k: s[k] for k in ("warm_zero_enrichment_calls", "ledger_after", "stages_not_run")}
    for kind in ("cold", "warm"):
        r = s[kind]
        brief[kind] = {k: r[k] for k in ("completed", "quarantined", "pending", "result_cache_hits", "enrich",
                                         "time_s")}
    print(json.dumps(brief, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
