/**
 * Self-seeding: when the database has no tables or no runs yet, the backend creates the schema (web/db/schema.sql)
 * and loads the snapshot committed in web/data (written by `python -m pipeline.publish --run runs/<id>`).
 * This lets a deployment that holds DATABASE_URL populate its own database without any machine that can open a
 * Postgres connection to Supabase. `pipeline.publish --db` / `--rest` remain the loaders for larger runs;
 * /api/admin/seed?run=<id> re-seeds on demand from the same snapshot.
 */
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import type { Pool } from "pg";

const DATA_DIR = process.env.DASHBOARD_DATA_DIR || path.join(process.cwd(), "data");
const SCHEMA = path.join(process.cwd(), "db", "schema.sql");
let inflight: Promise<SeedResult> | null = null;

export type SeedResult = { seeded: boolean; run_id?: string; counts?: Record<string, number>; reason?: string };

function readJson<T>(name: string): T {
  return JSON.parse(fs.readFileSync(path.join(DATA_DIR, name), "utf-8")) as T;
}

export async function tablesExist(pool: Pool): Promise<boolean> {
  const r = await pool.query("SELECT to_regclass('public.runs') AS t");
  return r.rows[0]?.t != null;
}

async function insertRows(pool: Pool, table: string, columns: string[], rows: any[][], batch = 500): Promise<number> {
  let n = 0;
  for (let i = 0; i < rows.length; i += batch) {
    const chunk = rows.slice(i, i + batch);
    const values: any[] = [];
    const tuples = chunk.map((row, r) => `(${row.map((_, c) => `$${r * row.length + c + 1}`).join(",")})`);
    for (const row of chunk) values.push(...row);
    await pool.query(`INSERT INTO ${table} (${columns.join(",")}) VALUES ${tuples.join(",")} ON CONFLICT DO NOTHING`, values);
    n += chunk.length;
  }
  return n;
}

/** Create the schema if needed and load the committed snapshot (idempotent for a run_id already present unless force). */
export async function seedFromSnapshot(pool: Pool, force = false): Promise<SeedResult> {
  if (inflight) return inflight;
  inflight = (async () => {
    if (!fs.existsSync(path.join(DATA_DIR, "run.json"))) return { seeded: false, reason: "no snapshot in web/data" };
    await pool.query(fs.readFileSync(SCHEMA, "utf-8"));
    const run = readJson<any>("run.json");
    const present = await pool.query("SELECT 1 FROM runs WHERE run_id = $1", [run.run_id]);
    if (present.rows.length && !force) return { seeded: false, run_id: run.run_id, reason: "run already loaded" };
    const client = await pool.connect();
    try {
      await client.query("BEGIN");
      for (const t of ["memo", "claims", "membership", "records", "issues", "aggregates", "runs"]) {
        await client.query(`DELETE FROM ${t} WHERE run_id = $1`, [run.run_id]);
      }
      await client.query("COMMIT");
    } catch (e) {
      await client.query("ROLLBACK");
      throw e;
    } finally {
      client.release();
    }
    const counts: Record<string, number> = {};
    counts.runs = await insertRows(pool, "runs", ["run_id", "published_at", "source_sha256", "row_count", "label_config", "memo_status", "memo_model"],
      [[run.run_id, run.published_at, run.source_sha256, run.row_count, run.label_config, run.memo_status, run.memo_model]]);
    counts.aggregates = await insertRows(pool, "aggregates", ["run_id", "data"], [[run.run_id, JSON.stringify(readJson("aggregates.json"))]]);
    const issues = readJson<any[]>("issues.json");
    counts.issues = await insertRows(pool, "issues",
      ["run_id", "issue_id", "rank", "topic", "subtopic", "name", "summary", "complaint_count", "severity_sum", "mean_severity", "priority_score", "examples"],
      issues.map((i) => [run.run_id, i.issue_id, i.rank, i.topic, i.subtopic, i.name, i.summary, i.complaint_count, i.severity_sum,
        i.mean_severity, i.priority_score, JSON.stringify(i.examples ?? [])]));
    const claims = readJson<any[]>("claims.json");
    counts.claims = await insertRows(pool, "claims", ["run_id", "claim_id", "issue_id", "metric", "value"],
      claims.map((c) => [run.run_id, c.claim_id, c.issue_id, c.metric, c.value]));
    const memo = readJson<any>("memo.json");
    counts.memo = await insertRows(pool, "memo", ["run_id", "status", "model", "markdown", "body", "validation"],
      [[run.run_id, memo.status, memo.model, memo.markdown, JSON.stringify(memo.json), JSON.stringify(memo.validation)]]);
    const membership = readJson<any[]>("membership.json");
    counts.membership = await insertRows(pool, "membership", ["run_id", "issue_id", "review_id"],
      membership.map((m) => [run.run_id, m.issue_id, m.review_id]), 2000);
    const cols = ["run_id", "review_id", "status", "reason", "cache_source_id", "topic", "subtopic", "intent", "severity", "sentiment",
      "needs_review", "evidence_quote", "month", "review_rating"];
    let buf: any[][] = [];
    counts.records = 0;
    const rl = readline.createInterface({ input: fs.createReadStream(path.join(DATA_DIR, "records.jsonl"), "utf-8") });
    for await (const line of rl) {
      if (!line.trim()) continue;
      const r = JSON.parse(line);
      buf.push([run.run_id, r.review_id, r.status, r.reason, r.cache_source_id, r.topic, r.subtopic, r.intent, r.severity, r.sentiment,
        r.needs_review, r.evidence_quote, r.month, r.review_rating]);
      if (buf.length >= 1000) {
        counts.records += await insertRows(pool, "records", cols, buf, 1000);
        buf = [];
      }
    }
    if (buf.length) counts.records += await insertRows(pool, "records", cols, buf, 1000);
    return { seeded: true, run_id: run.run_id, counts };
  })().finally(() => { inflight = null; });
  return inflight;
}
