"""Our row_sha256 must equal the course checker's row_sha (GRADING_CONTRACT.md)."""
import csv
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import pytest

from pipeline.hashing import SOURCE_FIELDS, row_sha256

DATA = Path(__file__).resolve().parent.parent / "data" / "raw" / "extracted"
CHECKER = DATA / "check_submission.py"
FULL_CSV = DATA / "spotify_reviews_18months.csv"

needs_data = pytest.mark.skipif(not (CHECKER.exists() and FULL_CSV.exists()),
                                reason="course dataset not present (data/raw/ is gitignored)")


def test_known_vector():
    """Hash is over a JSON *list* in contract order, compact, non-ASCII kept as UTF-8."""
    row = {"review_id": "a", "review_text": 'Héllo\n"x"', "review_rating": "5",
           "review_likes": "0", "app_version": "", "review_timestamp": "2023-01-01 00:00:00"}
    expected = hashlib.sha256('["a","Héllo\\n\\"x\\"","5","0","","2023-01-01 00:00:00"]'.encode()).hexdigest()
    assert row_sha256(row) == expected
    assert row_sha256(dict(reversed(list(row.items())))) == expected  # dict order irrelevant


@pytest.fixture(scope="module")
def checker():
    # The course-provided zero-API checker; loaded as a module only to call its row_sha.
    spec = importlib.util.spec_from_file_location("course_check_submission", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@needs_data
def test_matches_checker_on_real_rows(checker):
    assert tuple(checker.FIELDS) == SOURCE_FIELDS
    picked, kinds = [], {"multiline": 0, "empty_text": 0, "no_version": 0, "non_ascii": 0}
    for i, row in enumerate(checker.csv_rows(FULL_CSV)):
        text = row["review_text"]
        tags = [k for k, hit in (("multiline", "\n" in text), ("empty_text", not text.strip()),
                                 ("no_version", not row["app_version"].strip()),
                                 ("non_ascii", not text.isascii())) if hit and kinds[k] < 5]
        for k in tags:
            kinds[k] += 1
        if i < 200 or tags:
            picked.append(row)
        if i >= 200 and all(v >= 5 for v in kinds.values()):
            break
    assert all(v >= 5 for v in kinds.values()), kinds
    for row in picked:
        assert row_sha256(row) == checker.row_sha(row), row["review_id"]


@needs_data
def test_our_csv_parse_matches_checker(checker):
    """Our csv.reader + header mapping yields the same field strings as the checker's DictReader."""
    with open(FULL_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f, strict=True)
        header = next(reader)
        ours = ({k: fields[header.index(k)] for k in SOURCE_FIELDS} for fields in reader)
        for a, b in itertools.islice(zip(ours, checker.csv_rows(FULL_CSV)), 5000):
            assert json.dumps(a, sort_keys=True) == json.dumps({k: b[k] for k in SOURCE_FIELDS}, sort_keys=True)
