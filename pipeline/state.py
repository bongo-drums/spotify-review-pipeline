"""SQLite run store: record statuses, raw source rows, call log, label cache.

One run DB per run directory (e.g. runs/<run_id>/state.sqlite), WAL mode.
Every batch result is committed in a single transaction so a crash or Ctrl-C
never leaves a half-applied batch, and resume never double-counts.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

STATUSES = ("pending", "completed", "quarantined")

# Shared with budget.py, which creates the same table in the cross-run ledger DB.
SPEND_LEDGER_DDL = """
CREATE TABLE IF NOT EXISTS spend_ledger (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id         TEXT,
    kind           TEXT NOT NULL CHECK (kind IN ('reserve','commit','release')),
    amount_usd     REAL NOT NULL,
    call_id        TEXT,
    reservation_id TEXT NOT NULL,
    created_at     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ledger_reservation ON spend_ledger(reservation_id);
"""

SCHEMA = """
CREATE TABLE IF NOT EXISTS source (
    review_id        TEXT PRIMARY KEY,
    review_text      TEXT NOT NULL,
    review_rating    TEXT NOT NULL,
    review_likes     TEXT NOT NULL,
    app_version      TEXT NOT NULL,
    review_timestamp TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS records (
    review_id       TEXT PRIMARY KEY REFERENCES source(review_id),
    row_index       INTEGER NOT NULL UNIQUE,
    source_sha256   TEXT NOT NULL,
    text_sha256     TEXT NOT NULL,
    cache_source_id TEXT NOT NULL,
    status          TEXT NOT NULL CHECK (status IN ('pending','completed','quarantined')),
    reason          TEXT,
    attempts        INTEGER NOT NULL DEFAULT 0,
    label           TEXT,
    label_config    TEXT,
    updated_at      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_records_status_cache ON records(status, cache_source_id);
CREATE INDEX IF NOT EXISTS idx_records_cache_status ON records(cache_source_id, status);
CREATE INDEX IF NOT EXISTS idx_records_text ON records(text_sha256);
CREATE INDEX IF NOT EXISTS idx_records_heads ON records(row_index) WHERE review_id = cache_source_id;

CREATE TABLE IF NOT EXISTS calls (
    call_id                     TEXT PRIMARY KEY,
    run_id                      TEXT,
    stage                       TEXT,
    phase                       TEXT,
    model                       TEXT,
    label_config                TEXT,
    request_review_ids          TEXT,
    attempt                     INTEGER,
    status                      TEXT CHECK (status IN ('success','failed','invalid','retry')),
    error                       TEXT,
    input_tokens                INTEGER,
    cache_creation_input_tokens INTEGER,
    cache_read_input_tokens     INTEGER,
    output_tokens               INTEGER,
    service_tier                TEXT,
    started_at                  TEXT,
    ended_at                    TEXT,
    duration_s                  REAL,
    cost_usd_estimate           REAL
);

CREATE TABLE IF NOT EXISTS label_cache (
    text_sha256      TEXT NOT NULL,
    label_config     TEXT NOT NULL,
    label            TEXT NOT NULL,
    source_review_id TEXT NOT NULL,
    created_at       TEXT NOT NULL,
    PRIMARY KEY (text_sha256, label_config)
);

CREATE TABLE IF NOT EXISTS verifications (
    review_id        TEXT PRIMARY KEY REFERENCES records(review_id),
    run_id           TEXT,
    verifier_config  TEXT NOT NULL,
    call_id          TEXT,
    label            TEXT,
    status           TEXT NOT NULL CHECK (status IN ('verified','invalid')),
    error            TEXT,
    agree_topic      INTEGER,
    agree_intent     INTEGER,
    agree_severity   INTEGER,
    severity_diff    INTEGER,
    created_at       TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stage_cache (
    stage        TEXT NOT NULL,
    input_sha256 TEXT NOT NULL,
    output       TEXT NOT NULL,
    call_id      TEXT,
    created_at   TEXT NOT NULL,
    PRIMARY KEY (stage, input_sha256)
);

CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
""" + SPEND_LEDGER_DDL

CALL_COLUMNS = (
    "call_id", "run_id", "stage", "phase", "model", "label_config", "request_review_ids",
    "attempt", "status", "error", "input_tokens", "cache_creation_input_tokens",
    "cache_read_input_tokens", "output_tokens", "service_tier", "started_at", "ended_at",
    "duration_s", "cost_usd_estimate",
)


def utc_now() -> str:
    """UTC timestamp in ISO 8601 with a Z suffix."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def canonical_json(obj) -> str:
    """Deterministic JSON used for stored labels."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def connect(path, schema: str = SCHEMA) -> sqlite3.Connection:
    """Open a SQLite DB in WAL mode with autocommit; transactions are explicit."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), isolation_level=None, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(schema)
    return conn


def _ids(item: dict) -> list[str]:
    """Accept either `review_ids` (list) or a single `review_id`."""
    if "review_ids" in item:
        return list(item["review_ids"])
    return [item["review_id"]]


def _chunks(ids: list, size: int = 500):
    """Split id lists to stay far below SQLite's bound-parameter limit."""
    for i in range(0, len(ids), size):
        yield ids[i:i + size]


def _marks(ids) -> str:
    return ",".join("?" * len(ids))


def _update_ids(conn, sql: str, params: list, ids: list) -> int:
    """Run `sql AND review_id IN (...)` over id chunks; return total rows changed.

    Callers write `+status='pending'`: the unary plus stops SQLite from scanning the
    status index (hundreds of thousands of rows) instead of the review_id primary key.
    """
    changed = 0
    for chunk in _chunks(ids):
        changed += conn.execute(f"{sql} AND review_id IN ({_marks(chunk)})", [*params, *chunk]).rowcount
    return changed


class RunState:
    """Thin wrapper around one run DB. Safe to share across threads (one lock)."""

    def __init__(self, path):
        self.path = Path(path)
        self.conn = connect(self.path)
        self.lock = threading.RLock()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    @contextmanager
    def transaction(self):
        """BEGIN IMMEDIATE ... COMMIT, or ROLLBACK on any exception."""
        with self.lock:
            self.conn.execute("BEGIN IMMEDIATE")
            try:
                yield self.conn
            except BaseException:
                self.conn.execute("ROLLBACK")
                raise
            else:
                self.conn.execute("COMMIT")

    # ---- ingest -----------------------------------------------------------

    def insert_rows(self, source_rows: Iterable[tuple], record_rows: Iterable[tuple]) -> None:
        """Bulk insert (call inside `transaction()`).

        source_rows: (review_id, review_text, review_rating, review_likes, app_version, review_timestamp)
        record_rows: (review_id, row_index, source_sha256, text_sha256, cache_source_id, status, reason, updated_at)
        """
        self.conn.executemany("INSERT INTO source VALUES (?,?,?,?,?,?)", source_rows)
        self.conn.executemany(
            "INSERT INTO records (review_id,row_index,source_sha256,text_sha256,cache_source_id,"
            "status,reason,attempts,updated_at) VALUES (?,?,?,?,?,?,?,0,?)",
            record_rows,
        )

    def analyze(self) -> None:
        """Refresh planner statistics (run after bulk loads)."""
        with self.lock:
            self.conn.execute("ANALYZE")

    def record_count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]

    def set_meta(self, key: str, value) -> None:
        with self.lock:
            self.conn.execute(
                "INSERT INTO meta(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, canonical_json(value)),
            )

    def get_meta(self, key: str, default=None):
        row = self.conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else default

    # ---- batch commits ----------------------------------------------------

    def _insert_call(self, call_row: dict) -> str:
        unknown = set(call_row) - set(CALL_COLUMNS)
        if unknown:
            raise ValueError(f"unknown call columns: {sorted(unknown)}")
        row = dict(call_row)
        row.setdefault("call_id", uuid.uuid4().hex)
        if isinstance(row.get("request_review_ids"), (list, tuple)):
            row["request_review_ids"] = json.dumps(list(row["request_review_ids"]))
        cols = list(row)
        self.conn.execute(
            f"INSERT INTO calls ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
            [row[c] for c in cols],
        )
        return row["call_id"]

    def record_call(self, call_row: dict) -> str:
        """Log a call on its own (e.g. a failed request with no results)."""
        with self.transaction():
            return self._insert_call(call_row)

    def commit_batch(self, results, quarantines=(), call_row: dict | None = None, retries=()) -> dict:
        """Apply one request's outcome atomically: call log + labels + quarantines.

        results:     [{"review_ids": [...], "label": {...}, "label_config": "..."}]
                     All ids in one result must share the same text (one text group).
                     Ids become `completed`; the label is also stored in label_cache.
        quarantines: [{"review_ids": [...], "reason": "..."}] -> `quarantined`.
        retries:     [{"review_ids": [...], "reason": "..."}] -> attempts+1, stay `pending`.
        Only `pending` records change, so re-applying a batch never double-counts.
        Any exception rolls back everything, including the call row.
        """
        now = utc_now()
        counts = {"completed": 0, "quarantined": 0, "retried": 0, "call_id": None}
        with self.transaction() as c:
            if call_row is not None:
                counts["call_id"] = self._insert_call(call_row)
            for res in results:
                ids = _ids(res)
                label_json = canonical_json(res["label"])
                cfg = res["label_config"]
                texts = set()
                for chunk in _chunks(ids):
                    texts.update(tuple(r) for r in c.execute(
                        f"SELECT DISTINCT text_sha256, cache_source_id FROM records "
                        f"WHERE review_id IN ({_marks(chunk)})", chunk))
                if len(texts) != 1:
                    raise ValueError(f"result ids must map to exactly one known text, got {len(texts)}: {ids[:5]}")
                tsha, source_id = texts.pop()
                counts["completed"] += _update_ids(
                    c, "UPDATE records SET status='completed', label=?, label_config=?, reason=NULL, "
                       "attempts=attempts+1, updated_at=? WHERE +status='pending'",
                    [label_json, cfg, now], ids)
                c.execute(
                    "INSERT OR IGNORE INTO label_cache(text_sha256,label_config,label,source_review_id,created_at) "
                    "VALUES (?,?,?,?,?)",
                    (tsha, cfg, label_json, source_id, now),
                )
            for q in quarantines:
                counts["quarantined"] += _update_ids(
                    c, "UPDATE records SET status='quarantined', reason=?, attempts=attempts+1, updated_at=? "
                       "WHERE +status='pending'",
                    [q["reason"], now], _ids(q))
            for r in retries:
                counts["retried"] += _update_ids(
                    c, "UPDATE records SET attempts=attempts+1, reason=?, updated_at=? WHERE +status='pending'",
                    [r.get("reason"), now], _ids(r))
        return counts

    # ---- downstream stages --------------------------------------------------

    def commit_verifications(self, rows: list[dict], call_row: dict | None = None) -> int:
        """Store blind re-labels for sampled records together with their call row (one transaction)."""
        now = utc_now()
        with self.transaction() as c:
            call_id = self._insert_call(call_row) if call_row is not None else None
            for r in rows:
                c.execute(
                    "INSERT OR REPLACE INTO verifications(review_id,run_id,verifier_config,call_id,label,status,error,"
                    "agree_topic,agree_intent,agree_severity,severity_diff,created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (r["review_id"], r.get("run_id"), r["verifier_config"], call_id,
                     canonical_json(r["label"]) if r.get("label") is not None else None, r["status"], r.get("error"),
                     r.get("agree_topic"), r.get("agree_intent"), r.get("agree_severity"), r.get("severity_diff"), now))
        return len(rows)

    def stage_cache_get(self, stage: str, input_sha256: str):
        row = self.conn.execute("SELECT output FROM stage_cache WHERE stage=? AND input_sha256=?",
                                (stage, input_sha256)).fetchone()
        return json.loads(row[0]) if row else None

    def stage_cache_put(self, stage: str, input_sha256: str, output, call_row: dict | None = None) -> str | None:
        """Save a downstream model output keyed by its exact inputs, with its call row (one transaction)."""
        with self.transaction() as c:
            call_id = self._insert_call(call_row) if call_row is not None else None
            c.execute("INSERT OR REPLACE INTO stage_cache(stage,input_sha256,output,call_id,created_at) VALUES (?,?,?,?,?)",
                      (stage, input_sha256, canonical_json(output), call_id, utc_now()))
        return call_id

    def copy_downstream_cache_from(self, other: "RunState") -> dict:
        """Warm run: carry the result cache, verifications and stage cache over from a previous run DB."""
        labels = [tuple(r) for r in other.conn.execute(
            "SELECT text_sha256, label_config, label, source_review_id, created_at FROM label_cache")]
        ver = [tuple(r) for r in other.conn.execute(
            "SELECT review_id, run_id, verifier_config, call_id, label, status, error, agree_topic, agree_intent, "
            "agree_severity, severity_diff, created_at FROM verifications")]
        sc = [tuple(r) for r in other.conn.execute("SELECT stage, input_sha256, output, call_id, created_at FROM stage_cache")]
        with self.transaction() as c:
            c.executemany("INSERT OR IGNORE INTO label_cache VALUES (?,?,?,?,?)", labels)
            known = {r[0] for r in c.execute("SELECT review_id FROM records")}
            c.executemany("INSERT OR IGNORE INTO verifications VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                          [v for v in ver if v[0] in known])
            c.executemany("INSERT OR IGNORE INTO stage_cache VALUES (?,?,?,?,?)", sc)
        return {"label_cache": len(labels), "verifications": len(ver), "stage_cache": len(sc)}

    # ---- work queue -------------------------------------------------------

    def pending_text_groups(self, limit: int) -> list[dict]:
        """Up to `limit` distinct pending texts (in source order), each with all pending review_ids.

        Returns [{"cache_source_id", "text_sha256", "review_text", "review_ids"}]. Send one
        text per group to the model, then commit the label for every id in the group.
        """
        with self.lock:
            heads = self.conn.execute(
                """
                SELECT h.review_id, h.text_sha256, s.review_text
                FROM records h JOIN source s ON s.review_id = h.review_id
                WHERE h.review_id = h.cache_source_id
                  AND EXISTS (SELECT 1 FROM records p
                              WHERE p.cache_source_id = h.review_id AND p.status = 'pending')
                ORDER BY h.row_index
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            groups = []
            for head_id, tsha, text in heads:
                ids = [r[0] for r in self.conn.execute(
                    "SELECT review_id FROM records WHERE cache_source_id=? AND status='pending' ORDER BY row_index",
                    (head_id,),
                )]
                groups.append({"cache_source_id": head_id, "text_sha256": tsha,
                               "review_text": text, "review_ids": ids})
            return groups

    def apply_cache_hits(self, label_config: str) -> int:
        """Complete every pending record whose text already has a label for `label_config`.

        Completed-by-cache rows get reason='label_cache' for traceability. Returns rows updated.
        """
        with self.transaction() as c:
            cur = c.execute(
                """
                UPDATE records SET status='completed', label_config=:cfg, reason='label_cache',
                       updated_at=:now,
                       label=(SELECT lc.label FROM label_cache lc
                              WHERE lc.text_sha256 = records.text_sha256 AND lc.label_config = :cfg)
                WHERE status='pending'
                  AND EXISTS (SELECT 1 FROM label_cache lc
                              WHERE lc.text_sha256 = records.text_sha256 AND lc.label_config = :cfg)
                """,
                {"cfg": label_config, "now": utc_now()},
            )
            return cur.rowcount

    # ---- reporting --------------------------------------------------------

    def status_counts(self) -> dict:
        counts = dict.fromkeys(STATUSES, 0)
        for status, n in self.conn.execute("SELECT status, COUNT(*) FROM records GROUP BY status"):
            counts[status] = n
        return counts

    def completed_ids_sha256(self) -> tuple[str, int]:
        """sha256 over sorted completed review_ids joined by '\\n' (streamed), plus the count."""
        h, n = hashlib.sha256(), 0
        cur = self.conn.execute("SELECT review_id FROM records WHERE status='completed' ORDER BY review_id")
        for (rid,) in cur:
            h.update((("\n" if n else "") + rid).encode("utf-8"))
            n += 1
        return h.hexdigest(), n

    def export_checkpoint(self, path=None, run_id: str | None = None) -> dict:
        """Snapshot of progress; written atomically to `path` as JSON if given."""
        with self.lock:
            digest, n = self.completed_ids_sha256()
            snap = {
                "created_at": utc_now(),
                "run_id": run_id,
                "db_path": str(self.path),
                "counts": self.status_counts(),
                "completed_ids_count": n,
                "completed_ids_sha256": digest,
                "completed_ids_hash_rule": "sha256('\\n'.join(sorted(completed review_ids)))",
                "label_cache_entries": self.conn.execute("SELECT COUNT(*) FROM label_cache").fetchone()[0],
                "calls": self.conn.execute("SELECT COUNT(*) FROM calls").fetchone()[0],
            }
        if path is not None:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(path.suffix + ".tmp")
            tmp.write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")
            os.replace(tmp, path)
        return snap
