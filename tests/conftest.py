"""Shared fixtures: a small synthetic review CSV with the awkward cases."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

HEADER = ["review_id", "review_text", "review_rating", "review_likes", "app_version", "review_timestamp"]

ROWS = [
    ["r1", "Great app, love it", "5", "3", "8.9.1", "2024-01-05 10:00:00"],
    ["r2", 'Line one\nline two with "quotes", and a comma', "2", "0", "8.9.1", "2024-01-20 11:30:00"],
    ["r3", "", "1", "0", "8.9.2", "2024-02-01 09:00:00"],                      # empty text
    ["r4", "   \t ", "3", "1", "", "2024-02-11 12:00:00"],                     # whitespace-only, no version
    ["r5", "Great app, love it", "5", "0", "", "2024-02-15 08:15:00"],          # duplicate of r1, no version
    ["r6", "Ads every song 😡", "1", "12", "8.9.3", "2024-03-03 18:45:00"],
    ["r7", "Great app, love it", "4", "0", "8.9.3", "2024-03-09 07:00:00"],     # duplicate of r1
    ["r8", 'Line one\nline two with "quotes", and a comma', "2", "1", "8.9.3", "2024-03-10 22:10:00"],  # dup of r2
]


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Write ROWS as a UTF-8-with-BOM CSV using CRLF line endings (csv default)."""
    path = tmp_path / "reviews.csv"
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(ROWS)
    return path


@pytest.fixture
def ingested(sample_csv, tmp_path):
    """Run ingest on the sample CSV; returns (report, out_dir)."""
    from pipeline.ingest import ingest

    out = tmp_path / "run"
    return ingest(sample_csv, out), out
