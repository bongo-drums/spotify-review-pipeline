/**
 * Backend data access. Two sources, same shape:
 *  - Postgres (Supabase) when DATABASE_URL or SUPABASE_DB_URL is set: tables from web/db/schema.sql,
 *    loaded by `python -m pipeline.publish --run runs/<id> --db $SUPABASE_DB_URL`.
 *  - File snapshot (web/data/*.json, from `python -m pipeline.publish --run runs/<id>`) for local
 *    development and for a build without a database. The UI never knows which one answered.
 */
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";

export type Issue = {
  issue_id: string; rank: number; topic: string; subtopic: string; name: string; summary: string;
  complaint_count: number; severity_sum: number; mean_severity: string; priority_score: number;
  examples: { review_id: string; quote: string }[];
};
export type RecordRow = {
  review_id: string; status: string; reason: string | null; cache_source_id: string | null; topic: string | null;
  subtopic: string | null; intent: string | null; severity: number | null; sentiment: number | null;
  needs_review: boolean | null; evidence_quote: string | null; month: string | null; review_rating: string | null;
};
export type Claim = { claim_id: string; issue_id: string; metric: string; value: string };
export type RunInfo = {
  run_id: string; published_at: string; source_sha256: string; row_count: number; label_config: string | null;
  memo_status: string | null; memo_model: string | null;
};

const DSN = process.env.DATABASE_URL || process.env.SUPABASE_DB_URL || "";
const DATA_DIR = process.env.DASHBOARD_DATA_DIR || path.join(process.cwd(), "data");

export function sourceName(): "postgres" | "files" {
  return DSN ? "postgres" : "files";
}

// ---- Postgres --------------------------------------------------------------------

let pool: import("pg").Pool | null = null;
let seeded = false;
async function pg() {
  if (!pool) {
    const { Pool } = await import("pg");
    pool = new Pool({ connectionString: DSN, max: 3, ssl: DSN.includes("localhost") ? undefined : { rejectUnauthorized: false } });
  }
  if (!seeded) {
    // First request on an empty database: create the schema and load the committed snapshot (see lib/seed.ts).
    const { tablesExist, seedFromSnapshot } = await import("./seed");
    const ok = await tablesExist(pool);
    const n = ok ? (await pool.query("SELECT COUNT(*)::int AS n FROM runs")).rows[0].n : 0;
    if (!ok || n === 0) await seedFromSnapshot(pool);
    seeded = true;
  }
  return pool;
}

export async function getPool() {
  return pg();
}

async function latestRunId(): Promise<string> {
  const p = await pg();
  const r = await p.query("SELECT run_id FROM runs ORDER BY published_at DESC LIMIT 1");
  if (!r.rows.length) throw new Error("no runs published");
  return r.rows[0].run_id;
}

// ---- files -------------------------------------------------------------------------

function readJson<T>(name: string): T {
  return JSON.parse(fs.readFileSync(path.join(DATA_DIR, name), "utf-8")) as T;
}

async function fileRecords(filter: (r: RecordRow) => boolean, limit: number): Promise<RecordRow[]> {
  const out: RecordRow[] = [];
  const file = path.join(DATA_DIR, "records.jsonl");
  if (!fs.existsSync(file)) return out;
  const rl = readline.createInterface({ input: fs.createReadStream(file, "utf-8") });
  for await (const line of rl) {
    if (!line.trim()) continue;
    const r = JSON.parse(line) as RecordRow;
    if (filter(r)) {
      out.push(r);
      if (out.length >= limit) break;
    }
  }
  return out;
}

// ---- public API ---------------------------------------------------------------------

export async function getRun(): Promise<RunInfo> {
  if (!DSN) return readJson<RunInfo>("run.json");
  const p = await pg();
  const r = await p.query("SELECT * FROM runs ORDER BY published_at DESC LIMIT 1");
  return r.rows[0];
}

export async function getAggregates(): Promise<Record<string, any>> {
  if (!DSN) return readJson("aggregates.json");
  const p = await pg();
  const r = await p.query("SELECT data FROM aggregates WHERE run_id = $1", [await latestRunId()]);
  return r.rows[0]?.data ?? {};
}

export async function getIssues(): Promise<Issue[]> {
  if (!DSN) return readJson<Issue[]>("issues.json");
  const p = await pg();
  const r = await p.query("SELECT * FROM issues WHERE run_id = $1 ORDER BY rank", [await latestRunId()]);
  return r.rows.map((x) => ({ ...x, mean_severity: String(x.mean_severity) }));
}

export async function getIssue(issueId: string): Promise<{ issue: Issue; reviews: RecordRow[]; member_count: number } | null> {
  const issues = await getIssues();
  const issue = issues.find((i) => i.issue_id === issueId);
  if (!issue) return null;
  if (!DSN) {
    const membership = readJson<{ issue_id: string; review_id: string }[]>("membership.json");
    const ids = new Set(membership.filter((m) => m.issue_id === issueId).map((m) => m.review_id));
    const reviews = await fileRecords((r) => ids.has(r.review_id), 25);
    return { issue, reviews, member_count: ids.size };
  }
  const p = await pg();
  const run = await latestRunId();
  const reviews = await p.query(
    "SELECT r.* FROM membership m JOIN records r ON r.run_id = m.run_id AND r.review_id = m.review_id " +
      "WHERE m.run_id = $1 AND m.issue_id = $2 ORDER BY r.severity DESC, r.review_id LIMIT 25",
    [run, issueId],
  );
  const count = await p.query("SELECT COUNT(*)::int AS n FROM membership WHERE run_id = $1 AND issue_id = $2", [run, issueId]);
  return { issue, reviews: reviews.rows, member_count: count.rows[0].n };
}

export async function getClaims(): Promise<Claim[]> {
  if (!DSN) return readJson<Claim[]>("claims.json");
  const p = await pg();
  const r = await p.query("SELECT claim_id, issue_id, metric, value FROM claims WHERE run_id = $1", [await latestRunId()]);
  return r.rows;
}

export async function getMemo(): Promise<{ status: string | null; model: string | null; markdown: string; json: any; validation: any }> {
  if (!DSN) return readJson("memo.json");
  const p = await pg();
  const r = await p.query("SELECT status, model, markdown, body, validation FROM memo WHERE run_id = $1", [await latestRunId()]);
  const row = r.rows[0];
  return row ? { status: row.status, model: row.model, markdown: row.markdown, json: row.body, validation: row.validation }
             : { status: null, model: null, markdown: "", json: null, validation: null };
}

export async function getReview(reviewId: string): Promise<RecordRow | null> {
  if (!DSN) return (await fileRecords((r) => r.review_id === reviewId, 1))[0] ?? null;
  const p = await pg();
  const r = await p.query("SELECT * FROM records WHERE run_id = $1 AND review_id = $2", [await latestRunId(), reviewId]);
  return r.rows[0] ?? null;
}
