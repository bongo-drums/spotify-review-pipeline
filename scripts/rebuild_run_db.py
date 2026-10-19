"""Rebuild a run's git-ignored state.sqlite from its source CSV and committed labels.csv, so pipeline.publish can run
from a fresh checkout.

    python scripts/rebuild_run_db.py --run runs/pilot10000 --input data/raw/extracted/analysis_10000.csv

Re-ingests the CSV (checksum must match the run's data_manifest.json) into <run>/state.sqlite without touching the
committed reports, then restores status, reason, attempts and the label JSON of every record from <run>/labels.csv.
Only what publish reads is restored: calls, verifications and caches are not.
"""
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline.hashing import file_sha256  # noqa: E402
from pipeline.ingest import ingest  # noqa: E402
from pipeline.state import utc_now  # noqa: E402


def restore_labels(run_dir: Path) -> dict:
    rows = list(csv.DictReader(open(run_dir / "labels.csv", newline="", encoding="utf-8")))
    agg_path = run_dir / "artifacts" / "aggregates.json"
    label_config = json.loads(agg_path.read_text(encoding="utf-8")).get("label_config") if agg_path.exists() else None
    con = sqlite3.connect(run_dir / "state.sqlite")
    con.row_factory = sqlite3.Row
    db = {r["review_id"]: r["cache_source_id"] for r in con.execute("SELECT review_id, cache_source_id FROM records")}
    if len(db) != len(rows):
        raise SystemExit(f"records in DB ({len(db)}) != rows in labels.csv ({len(rows)})")
    bad = [r["review_id"] for r in rows if db.get(r["review_id"]) != r["cache_source_id"]]
    if bad:
        raise SystemExit(f"{len(bad)} records whose cache_source_id differs from labels.csv (wrong input CSV?)")
    now = utc_now()
    upd = []
    for r in rows:
        if r["status"] == "completed":
            sent = float(r["sentiment"])
            label = {"topic": r["topic"], "subtopic": r["subtopic"], "intent": r["intent"], "severity": int(r["severity"]),
                     "sentiment": sent, "sentiment_level": int(round((sent + 1) * 2)),
                     "entities": json.loads(r["entities"] or "[]"), "evidence_sentence": int(r["evidence_sentence"]),
                     "evidence_quote": r["evidence_quote"], "needs_review": r["needs_review"] == "True"}
            upd.append(("completed", None, int(r["attempts"] or 0), json.dumps(label, ensure_ascii=False), label_config, now,
                        r["review_id"]))
        else:
            upd.append((r["status"], r["reason"] or None, int(r["attempts"] or 0), None, None, now, r["review_id"]))
    with con:
        con.executemany("UPDATE records SET status=?, reason=?, attempts=?, label=?, label_config=?, updated_at=? "
                        "WHERE review_id=?", upd)
    counts = dict(con.execute("SELECT status, COUNT(*) FROM records GROUP BY status").fetchall())
    missing_quote = con.execute(
        "SELECT COUNT(*) FROM records r JOIN source s USING(review_id) WHERE r.label IS NOT NULL "
        "AND instr(s.review_text, json_extract(r.label,'$.evidence_quote')) = 0").fetchone()[0]
    con.close()
    return {"status_counts": counts, "evidence_quotes_not_in_text": missing_quote}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Rebuild <run>/state.sqlite from the source CSV and labels.csv.")
    ap.add_argument("--run", required=True, help="run directory with labels.csv and data_manifest.json")
    ap.add_argument("--input", required=True, help="the CSV the run was made from")
    ap.add_argument("--force", action="store_true", help="replace an existing state.sqlite")
    args = ap.parse_args(argv)
    run_dir, src = Path(args.run), Path(args.input)
    manifest = json.loads((run_dir / "data_manifest.json").read_text(encoding="utf-8"))
    sha = file_sha256(src)
    if sha != manifest["source_sha256"]:
        raise SystemExit(f"input sha256 {sha[:12]} does not match the run manifest {manifest['source_sha256'][:12]}")
    db = run_dir / "state.sqlite"
    if db.exists() and not args.force:
        raise SystemExit(f"{db} exists; pass --force to rebuild it")
    with tempfile.TemporaryDirectory() as tmp:  # reports go to a temp dir so the committed ones stay untouched
        ingest(src, Path(tmp), db_path=db, force=args.force)
    out = restore_labels(run_dir)
    out["db"] = str(db)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
