"""Hashing rules for source rows, review texts and files.

All hashing lives here so that the source-row rule can be swapped in one place.
"""
from __future__ import annotations

import hashlib
import json

SOURCE_FIELDS = (
    "review_id",
    "review_text",
    "review_rating",
    "review_likes",
    "app_version",
    "review_timestamp",
)

# Identifier written into reports/manifests so outputs say which rule produced them.
ROW_HASH_RULE = (
    "GRADING_CONTRACT.md v1 / check_submission.py row_sha: sha256(utf8(json.dumps([review_id, review_text, "
    "review_rating, review_likes, app_version, review_timestamp], ensure_ascii=False, separators=(',',':'), "
    "sort_keys=True, allow_nan=False)))"
)


def canonical(value) -> str:
    """Compact JSON exactly as check_submission.py's canonical() serializes it."""
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False)


def row_sha256(row: dict) -> str:
    """Source-row hash defined by GRADING_CONTRACT.md (matches check_submission.py `row_sha`).

    SHA-256 of the UTF-8 compact JSON *list* of the six original field strings in
    contract order. Strings are hashed exactly as parsed: no trimming, Unicode
    normalization or type coercion. tests/test_contract_hash.py checks this
    against the course checker on real rows.
    """
    values = ["" if row.get(k) is None else row[k] for k in SOURCE_FIELDS]
    return hashlib.sha256(canonical(values).encode("utf-8")).hexdigest()


def text_sha256(text: str) -> str:
    """Hash the raw review text (exact bytes, no normalization) for the label cache."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path) -> str:
    """Stream a file from disk and return its sha256 hex digest."""
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()
