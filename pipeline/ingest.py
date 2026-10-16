"""Stage 1 (Prepare): stream the review CSV, profile it, hash it and load the run DB.

Usage:
    python -m pipeline.ingest --input data/raw/spotify_reviews_18months.csv --out runs/<run_id>

Writes <out>/ingestion_report.json, <out>/data_manifest.json and <out>/state.sqlite.
The CSV is streamed with the stdlib csv module (multiline-safe, BOM-safe); raw
string values are stored exactly as parsed, never coerced.
"""
from __future__ import annotations

import argparse
import codecs
import csv
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from array import array
from collections import Counter
from datetime import datetime
from pathlib import Path

from . import config
from .hashing import ROW_HASH_RULE, SOURCE_FIELDS, file_sha256, row_sha256, text_sha256
from .state import RunState, utc_now

BATCH_ROWS = 5000
EXAMPLE_LIMIT = 20


def git_commit() -> dict:
    """Current code commit and dirty flag, or None values outside a repo / before the first commit."""
    def run(*args):
        try:
            out = subprocess.run(["git", *args], cwd=config.REPO_ROOT, capture_output=True, text=True, timeout=10)
            return out.stdout.strip() if out.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            return None
    commit = run("rev-parse", "HEAD")
    status = run("status", "--porcelain")
    return {"commit": commit, "dirty": bool(status) if status is not None else None}


def _length_stats(lengths: array) -> dict:
    if not lengths:
        return {"count": 0}
    s = sorted(lengths)
    pct = lambda p: s[min(len(s) - 1, int(p * (len(s) - 1) + 0.5))]  # nearest-rank
    return {
        "count": len(s), "min": s[0], "max": s[-1], "mean": round(sum(s) / len(s), 2),
        "median": statistics.median(s), "p90": pct(0.90), "p95": pct(0.95), "p99": pct(0.99),
        "total_chars": sum(s),
    }


def _write_json(path: Path, obj) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def ingest(input_path, out_dir, db_path=None, force: bool = False) -> dict:
    """Run the full ingest; returns the ingestion report dict."""
    t0 = time.monotonic()
    input_path, out_dir = Path(input_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(db_path) if db_path else out_dir / "state.sqlite"

    if db_path.exists():
        if not force:
            raise FileExistsError(f"{db_path} already exists; use a new --out dir or --force to rebuild")
        for suffix in ("", "-wal", "-shm", "-journal"):
            Path(str(db_path) + suffix).unlink(missing_ok=True)

    size_bytes = input_path.stat().st_size
    source_sha = file_sha256(input_path)
    with open(input_path, "rb") as fb:
        has_bom = fb.read(3) == codecs.BOM_UTF8

    # Profiling accumulators (bounded memory: one dict entry per distinct text, one per id).
    # Whole-file stats use check_submission.py `profile` semantics so they can be compared 1:1.
    seen_ids: set[str] = set()
    first_id_by_text: dict[bytes, str] = {}
    dup_ids, dup_id_examples = 0, []
    missing = Counter({f: 0 for f in SOURCE_FIELDS})       # blank after .strip() (checker rule)
    empty_string = Counter({f: 0 for f in SOURCE_FIELDS})  # exactly ""
    ratings: Counter = Counter()
    months: Counter = Counter()
    first_ts = last_ts = None
    ts_bad, ts_bad_examples = 0, []
    empty_exact = whitespace_only = multiline = 0
    malformed, malformed_examples = 0, []
    distinct_nonblank = reused_nonblank = 0
    distinct_text_chars = 0
    lengths = array("L")  # chars per loaded nonblank row
    status_counts = Counter()
    parsed_rows = hashlib.sha256()  # sha256 over each row's raw 32-byte digest, in file order

    src_buf, rec_buf = [], []
    row_index = -1
    now = utc_now()
    with open(input_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f, strict=True)
        header = next(reader, None)
        if header is None:
            raise ValueError("empty CSV")
        missing_cols = [c for c in SOURCE_FIELDS if c not in header]
        if missing_cols:
            raise ValueError(f"CSV header missing columns {missing_cols}; got {header}")
        col = {name: header.index(name) for name in SOURCE_FIELDS}
        state = RunState(db_path)  # created only after the header is valid

        with state.transaction():
            for row_index, fields in enumerate(reader):
                bad_shape = len(fields) != len(header)
                if bad_shape:
                    malformed += 1
                    if len(malformed_examples) < EXAMPLE_LIMIT:
                        malformed_examples.append({"row_index": row_index, "line": reader.line_num, "n_fields": len(fields)})
                    fields = (fields + [""] * len(header))[: len(header)]
                row = {name: fields[i] for name, i in col.items()}
                rid, text, ts = row["review_id"], row["review_text"], row["review_timestamp"]

                # -- whole-file profile (every parsed row, like the checker) --
                rsha = row_sha256(row)
                parsed_rows.update(bytes.fromhex(rsha))
                for name in SOURCE_FIELDS:
                    v = row[name]
                    if v == "":
                        empty_string[name] += 1
                    if not v.strip():
                        missing[name] += 1
                blank = not text.strip()
                if text == "":
                    empty_exact += 1
                elif blank:
                    whitespace_only += 1
                if "\n" in text or "\r" in text:
                    multiline += 1
                ratings[row["review_rating"]] += 1
                months[ts[:7]] += 1
                first_ts = min(first_ts, ts) if first_ts else ts
                last_ts = max(last_ts, ts) if last_ts else ts
                try:
                    datetime.fromisoformat(ts)
                except ValueError:
                    ts_bad += 1
                    if len(ts_bad_examples) < EXAMPLE_LIMIT:
                        ts_bad_examples.append(ts)

                if rid in seen_ids:  # keep the first occurrence; later ones are reported, not loaded
                    dup_ids += 1
                    if len(dup_id_examples) < EXAMPLE_LIMIT:
                        dup_id_examples.append({"review_id": rid, "row_index": row_index})
                    continue
                seen_ids.add(rid)

                # -- exact-text dedup over loaded rows --
                tsha = text_sha256(text)
                key = bytes.fromhex(tsha)
                cache_source_id = first_id_by_text.get(key)
                if cache_source_id is None:
                    first_id_by_text[key] = cache_source_id = rid
                    if not blank:
                        distinct_nonblank += 1
                        distinct_text_chars += len(text)
                elif not blank:
                    reused_nonblank += 1
                if not blank:
                    lengths.append(len(text))

                if bad_shape:
                    status, reason = "quarantined", "malformed_row"
                elif blank:
                    status, reason = "quarantined", "empty_review_text"
                else:
                    status, reason = "pending", None
                status_counts[status] += 1

                src_buf.append(tuple(row[n] for n in SOURCE_FIELDS))
                rec_buf.append((rid, row_index, rsha, tsha, cache_source_id, status, reason, now))
                if len(src_buf) >= BATCH_ROWS:
                    state.insert_rows(src_buf, rec_buf)
                    src_buf, rec_buf = [], []
            if src_buf:
                state.insert_rows(src_buf, rec_buf)

    state.analyze()
    total_rows = row_index + 1
    loaded = total_rows - dup_ids
    db_counts = state.status_counts()
    assert db_counts == {s: status_counts.get(s, 0) for s in db_counts}, (db_counts, status_counts)

    report = {
        "generated_at": utc_now(),
        "source": {"path": str(input_path), "bytes": size_bytes, "sha256": source_sha, "utf8_bom": has_bom},
        "header": header,
        "row_hash_rule": ROW_HASH_RULE,
        # Same keys/semantics as `check_submission.py profile` output, for a direct diff.
        "checker_profile": {
            "file_sha256": source_sha,
            "parsed_rows_sha256": parsed_rows.hexdigest(),
            "counts": {"records": total_rows, "duplicate_review_ids": dup_ids,
                       "empty_review_text": empty_exact + whitespace_only,
                       "missing_app_version": missing["app_version"]},
            "reviews_by_month": dict(months),
            "reviews_by_rating": dict(ratings),
            "first_review": first_ts,
            "last_review": last_ts,
        },
        "rows": {"total": total_rows, "loaded": loaded, "malformed_field_count": malformed,
                 "malformed_examples": malformed_examples},
        "review_text": {
            "empty_exact": empty_exact,
            "whitespace_only": whitespace_only,
            "nonblank_rows": total_rows - empty_exact - whitespace_only,
            "multiline_rows": multiline,
            "distinct_nonblank_texts": distinct_nonblank,
            "rows_reusing_earlier_text": reused_nonblank,
            "distinct_nonblank_text_chars": distinct_text_chars,
            "dedup_rule": "exact raw text, sha256 of UTF-8 bytes, no normalization",
        },
        "missing_by_column": dict(missing),
        "missing_rule": "value.strip() == '' (same as check_submission.py profile)",
        "empty_string_by_column": dict(empty_string),
        "duplicate_review_ids": {"count": dup_ids, "examples": dup_id_examples,
                                 "handling": "first occurrence loaded, later ones skipped"},
        "rating_distribution": dict(sorted(ratings.items())),
        "timestamps": {
            "min": first_ts,
            "max": last_ts,
            "min_max_rule": "string comparison (ISO 'YYYY-MM-DD HH:MM:SS' sorts chronologically)",
            "not_iso_parseable": ts_bad,
            "not_iso_parseable_examples": ts_bad_examples,
            "per_month": dict(sorted(months.items())),
        },
        "text_length_chars_nonblank": _length_stats(lengths),
        "status_counts": db_counts,
        "quarantine_reasons": {r: n for r, n in state.conn.execute(
            "SELECT reason, COUNT(*) FROM records WHERE status='quarantined' GROUP BY reason")},
        "db_path": str(db_path),
        "elapsed_s": round(time.monotonic() - t0, 2),
    }
    manifest = {
        "created_at": utc_now(),
        "source_path": str(input_path),
        "source_bytes": size_bytes,
        "source_sha256": source_sha,
        "row_count": total_rows,
        "loaded_row_count": loaded,
        "row_hash_rule": ROW_HASH_RULE,
        "code": git_commit(),
        "python": platform.python_version(),
        "outputs": {"ingestion_report": "ingestion_report.json", "run_db": db_path.name},
    }
    state.set_meta("data_manifest", manifest)
    state.close()
    _write_json(out_dir / "ingestion_report.json", report)
    _write_json(out_dir / "data_manifest.json", manifest)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Stream, profile and load the review CSV into a run DB.")
    ap.add_argument("--input", required=True, help="path to spotify_reviews_18months.csv")
    ap.add_argument("--out", required=True, help="run directory for reports and state.sqlite")
    ap.add_argument("--db", help="run DB path (default: <out>/state.sqlite)")
    ap.add_argument("--force", action="store_true", help="delete and rebuild an existing run DB")
    args = ap.parse_args(argv)
    try:
        report = ingest(args.input, args.out, db_path=args.db, force=args.force)
    except (FileExistsError, ValueError) as e:
        print(f"ingest failed: {e}", file=sys.stderr)
        return 1
    t = report["review_text"]
    print(json.dumps({
        "rows": report["rows"]["total"],
        "status_counts": report["status_counts"],
        "distinct_nonblank_texts": t["distinct_nonblank_texts"],
        "rows_reusing_earlier_text": t["rows_reusing_earlier_text"],
        "missing_by_column": report["missing_by_column"],
        "elapsed_s": report["elapsed_s"],
        "out": str(Path(args.out)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
