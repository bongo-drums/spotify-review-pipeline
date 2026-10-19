"""Put specific quarantined texts back in the queue after a code fix. Offline; writes an audit line.

    python -m pipeline.requeue --run runs/full --refusals            # refused-as-a-batch texts -> one text per request
    python -m pipeline.requeue --run runs/full --evidence-index      # single-span texts rejected for an out-of-range index
    python -m pipeline.requeue --run runs/full --refusals --evidence-index --dry-run

Only quarantines caused by the enricher's own output (never `empty_review_text`) are touched. Each requeued
head text gets attempts reset to 1 (one retry left under the fixed code) and a `reason` that the batch runner
understands: `batch_refusal:...` means "send alone". Every call that already happened stays in the log.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .enricher import split_sentences
from .state import RunState, utc_now


def select(state: RunState, refusals: bool, evidence_index: bool) -> dict[str, list[str]]:
    picked: dict[str, list[str]] = {"refusal": [], "evidence_index": []}
    rows = state.conn.execute(
        "SELECT r.review_id, r.reason, s.review_text FROM records r JOIN source s USING(review_id) "
        "WHERE r.status='quarantined' AND r.review_id = r.cache_source_id AND r.reason != 'empty_review_text'").fetchall()
    for rid, reason, text in rows:
        reason = reason or ""
        if refusals and reason.startswith("refusal"):
            picked["refusal"].append(rid)
        elif evidence_index and reason.startswith("invalid_record:evidence sentence") and len(split_sentences(text)) == 1:
            picked["evidence_index"].append(rid)
    return picked


def requeue(state: RunState, picked: dict[str, list[str]], dry_run: bool) -> dict:
    now = utc_now()
    out = {"at": now, "dry_run": dry_run, "heads": {k: len(v) for k, v in picked.items()}, "rows": 0}
    if dry_run:
        return out
    with state.transaction() as c:
        for kind, ids in picked.items():
            new_reason = "batch_refusal: requeued one-per-request after a refused multi-review request" if kind == "refusal" \
                else "requeued: evidence index on a single-sentence text (validator fix)"
            for i in range(0, len(ids), 500):
                chunk = ids[i:i + 500]
                cur = c.execute(
                    f"UPDATE records SET status='pending', attempts=1, reason=?, updated_at=? "
                    f"WHERE status='quarantined' AND cache_source_id IN ({','.join('?' * len(chunk))})",
                    [new_reason, now, *chunk])
                out["rows"] += cur.rowcount
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Requeue specific quarantined texts after a code fix (offline).")
    ap.add_argument("--run", required=True)
    ap.add_argument("--refusals", action="store_true")
    ap.add_argument("--evidence-index", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)
    if not (args.refusals or args.evidence_index):
        print("nothing selected: pass --refusals and/or --evidence-index", file=sys.stderr)
        return 1
    run_dir = Path(args.run)
    with RunState(run_dir / "state.sqlite") as state:
        picked = select(state, args.refusals, args.evidence_index)
        out = requeue(state, picked, args.dry_run)
        out["counts_after"] = state.status_counts()
    if not args.dry_run:
        with open(run_dir / "requeue_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(out) + "\n")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
