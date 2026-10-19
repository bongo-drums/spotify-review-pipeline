-- Dashboard database (Supabase Postgres). Loaded by `python -m pipeline.publish --run runs/<id> --db $SUPABASE_DB_URL`.
-- Every table is keyed by run_id so several runs (pilot10000, full) can coexist; the API serves the latest by default.

CREATE TABLE IF NOT EXISTS runs (
    run_id        TEXT PRIMARY KEY,
    published_at  TIMESTAMPTZ NOT NULL,
    source_sha256 TEXT NOT NULL,
    row_count     INTEGER NOT NULL,
    label_config  TEXT,
    memo_status   TEXT,
    memo_model    TEXT
);

CREATE TABLE IF NOT EXISTS aggregates (          -- pipeline/ranking.py aggregates.json, verbatim
    run_id TEXT PRIMARY KEY REFERENCES runs(run_id) ON DELETE CASCADE,
    data   JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS issues (              -- ranking.csv joined with issues.json names and example quotes
    run_id          TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    issue_id        TEXT NOT NULL,
    rank            INTEGER NOT NULL,
    topic           TEXT NOT NULL,
    subtopic        TEXT NOT NULL,
    name            TEXT NOT NULL,
    summary         TEXT,
    complaint_count INTEGER NOT NULL,
    severity_sum    INTEGER NOT NULL,
    mean_severity   NUMERIC(10,6) NOT NULL,
    priority_score  INTEGER NOT NULL,
    examples        JSONB NOT NULL DEFAULT '[]',  -- [{review_id, quote}] from the evidence pack
    PRIMARY KEY (run_id, issue_id)
);
CREATE INDEX IF NOT EXISTS idx_issues_rank ON issues(run_id, rank);

CREATE TABLE IF NOT EXISTS membership (          -- one row per (issue, review): the traceable evidence link
    run_id    TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    issue_id  TEXT NOT NULL,
    review_id TEXT NOT NULL,
    PRIMARY KEY (run_id, issue_id, review_id)
);

CREATE TABLE IF NOT EXISTS records (             -- processed review data: one row per source review id
    run_id          TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    review_id       TEXT NOT NULL,
    status          TEXT NOT NULL,
    reason          TEXT,
    cache_source_id TEXT,
    topic           TEXT,
    subtopic        TEXT,
    intent          TEXT,
    severity        SMALLINT,
    sentiment       REAL,
    needs_review    BOOLEAN,
    evidence_quote  TEXT,
    month           TEXT,
    review_rating   TEXT,
    PRIMARY KEY (run_id, review_id)
);
CREATE INDEX IF NOT EXISTS idx_records_issue ON records(run_id, topic, subtopic, intent);

CREATE TABLE IF NOT EXISTS claims (              -- claims.csv: the only numbers the memo may state
    run_id   TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    claim_id TEXT NOT NULL,
    issue_id TEXT NOT NULL,
    metric   TEXT NOT NULL,
    value    TEXT NOT NULL,
    PRIMARY KEY (run_id, claim_id)
);

CREATE TABLE IF NOT EXISTS memo (                -- the AI-generated recommendation, generated once from saved aggregates
    run_id     TEXT PRIMARY KEY REFERENCES runs(run_id) ON DELETE CASCADE,
    status     TEXT,
    model      TEXT,
    markdown   TEXT,
    body       JSONB,
    validation JSONB
);
