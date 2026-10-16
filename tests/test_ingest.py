import json
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import ROWS
from pipeline.hashing import row_sha256, text_sha256
from pipeline.ingest import ingest
from pipeline.state import RunState

REPO = Path(__file__).resolve().parent.parent


def test_counts_and_profile(ingested, sample_csv):
    report, out = ingested
    assert report["source"]["utf8_bom"] is True
    assert report["header"][0] == "review_id"  # BOM stripped from the first column name
    assert report["rows"]["total"] == 8
    assert report["rows"]["malformed_field_count"] == 0
    t = report["review_text"]
    assert t["empty_exact"] == 1
    assert t["whitespace_only"] == 1
    assert t["nonblank_rows"] == 6
    assert t["multiline_rows"] == 2
    assert t["distinct_nonblank_texts"] == 3
    assert t["rows_reusing_earlier_text"] == 3
    assert report["missing_by_column"]["app_version"] == 2
    assert report["missing_by_column"]["review_text"] == 2  # checker rule: blank after strip()
    assert report["empty_string_by_column"]["review_text"] == 1
    cp = report["checker_profile"]
    assert cp["counts"] == {"records": 8, "duplicate_review_ids": 0, "empty_review_text": 2, "missing_app_version": 2}
    assert cp["first_review"] == "2024-01-05 10:00:00" and len(cp["parsed_rows_sha256"]) == 64
    assert report["duplicate_review_ids"]["count"] == 0
    assert report["rating_distribution"] == {"1": 2, "2": 2, "3": 1, "4": 1, "5": 2}
    assert report["timestamps"]["min"] == "2024-01-05 10:00:00"
    assert report["timestamps"]["max"] == "2024-03-10 22:10:00"
    assert report["timestamps"]["per_month"] == {"2024-01": 2, "2024-02": 3, "2024-03": 3}
    assert report["status_counts"] == {"pending": 6, "completed": 0, "quarantined": 2}

    manifest = json.loads((out / "data_manifest.json").read_text())
    assert manifest["row_count"] == 8
    assert manifest["source_bytes"] == sample_csv.stat().st_size
    assert len(manifest["source_sha256"]) == 64
    assert json.loads((out / "ingestion_report.json").read_text())["rows"]["total"] == 8


def test_raw_values_preserved_and_hashed(ingested):
    _, out = ingested
    with RunState(out / "state.sqlite") as st:
        src = st.conn.execute("SELECT * FROM source WHERE review_id='r2'").fetchone()
        rec = st.conn.execute("SELECT * FROM records WHERE review_id='r2'").fetchone()
    raw = dict(zip(["review_id", "review_text", "review_rating", "review_likes", "app_version", "review_timestamp"], ROWS[1]))
    assert dict(src) == raw  # embedded newline, quotes and comma survive exactly
    assert rec["source_sha256"] == row_sha256(raw)
    assert rec["text_sha256"] == text_sha256(raw["review_text"])


def test_quarantine_and_cache_source(ingested):
    _, out = ingested
    with RunState(out / "state.sqlite") as st:
        rows = {r["review_id"]: dict(r) for r in st.conn.execute("SELECT * FROM records")}
    for rid in ("r3", "r4"):
        assert rows[rid]["status"] == "quarantined"
        assert rows[rid]["reason"] == "empty_review_text"
        assert rows[rid]["attempts"] == 0
    assert {rows[r]["cache_source_id"] for r in ("r1", "r5", "r7")} == {"r1"}
    assert rows["r8"]["cache_source_id"] == "r2"
    assert rows["r6"]["cache_source_id"] == "r6"
    assert [r["row_index"] for r in sorted(rows.values(), key=lambda r: r["row_index"])] == list(range(8))


def test_refuses_existing_db_without_force(ingested, sample_csv):
    _, out = ingested
    with pytest.raises(FileExistsError):
        ingest(sample_csv, out)
    assert ingest(sample_csv, out, force=True)["rows"]["total"] == 8


def test_cli(sample_csv, tmp_path):
    out = tmp_path / "cli_run"
    proc = subprocess.run(
        [sys.executable, "-m", "pipeline.ingest", "--input", str(sample_csv), "--out", str(out)],
        cwd=REPO, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["status_counts"]["quarantined"] == 2
    assert (out / "state.sqlite").exists()
