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
import zlib from "node:zlib";
import type { Pool } from "pg";

const DATA_DIR = process.env.DASHBOARD_DATA_DIR || path.join(process.cwd(), "data");
const SCHEMA = path.join(process.cwd(), "db", "schema.sql");
let inflight: Promise<SeedResult> | null = null;

export type SeedResult = { seeded: boolean; done?: boolean; run_id?: string; counts?: Record<string, number>; reason?: string };

function recordsPath(): string | null {
  for (const name of ["records.jsonl.gz", "records.jsonl"]) {
    const p = path.join(DATA_DIR, name);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

function recordLines(file: string) {
  const raw = fs.createReadStream(file);
  const input = file.endsWith(".gz") ? raw.pipe(zlib.createGunzip()) : raw;
  return readline.createInterface({ input, crlfDelay: Infinity });
}

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

/** Create the schema if needed and load the committed snapshot. Resumable and time-budgeted: a call that runs out
 *  of budget returns done=false, and the next call continues from the rows already present (insertion follows file
 *  order, so the existing count is the offset). Idempotent for a run already fully loaded unless force. */
export async function seedFromSnapshot(pool: Pool, force = false, budgetMs = 40_000): Promise<SeedResult> {
  if (inflight) return inflight;
  inflight = (async () => {
    const t0 = Date.now();
    const over = () => Date.now() - t0 > budgetMs;
    if (!fs.existsSync(path.join(DATA_DIR, "run.json"))) return { seeded: false, done: true, reason: "no snapshot in web/data" };
    await pool.query(fs.readFileSync(SCHEMA, "utf-8"));
    const run = readJson<any>("run.json");
    const membership = readJson<any[]>("membership.json");
    const present = (await pool.query("SELECT 1 FROM runs WHERE run_id = $1", [run.run_id])).rows.length > 0;
    const counts: Record<string, number> = {};
    if (present && force) {
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
    }
    if (!present || force) {
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
    }
    // membership: continue from the rows already present
    const haveM = (await pool.query("SELECT COUNT(*)::int AS n FROM membership WHERE run_id = $1", [run.run_id])).rows[0].n;
    counts.membership_total = membership.length;
    counts.membership = haveM;
    for (let i = haveM; i < membership.length && !over(); i += 2000) {
      const chunk = membership.slice(i, i + 2000).map((m) => [run.run_id, m.issue_id, m.review_id]);
      counts.membership += await insertRows(pool, "membership", ["run_id", "issue_id", "review_id"], chunk, 2000);
    }
    if (over()) return { seeded: true, done: false, run_id: run.run_id, counts };
    // records: stream the (possibly gzipped) file, skipping the rows already present
    const file = recordsPath();
    const haveR = (await pool.query("SELECT COUNT(*)::int AS n FROM records WHERE run_id = $1", [run.run_id])).rows[0].n;
    counts.records = haveR;
    if (!file) return { seeded: true, done: true, run_id: run.run_id, counts };
    const cols = ["run_id", "review_id", "status", "reason", "cache_source_id", "topic", "subtopic", "intent", "severity", "sentiment",
      "needs_review", "evidence_quote", "month", "review_rating"];
    let buf: any[][] = [], seen = 0, stopped = false;
    const rl = recordLines(file);
    for await (const line of rl) {
      if (!line.trim()) continue;
      seen += 1;
      if (seen <= haveR) continue;
      const r = JSON.parse(line);
      buf.push([run.run_id, r.review_id, r.status, r.reason, r.cache_source_id, r.topic, r.subtopic, r.intent, r.severity, r.sentiment,
        r.needs_review, r.evidence_quote, r.month, r.review_rating]);
      if (buf.length >= 1000) {
        counts.records += await insertRows(pool, "records", cols, buf, 1000);
        buf = [];
        if (over()) { stopped = true; break; }
      }
    }
    rl.close();
    if (buf.length && !stopped) counts.records += await insertRows(pool, "records", cols, buf, 1000);
    return { seeded: true, done: !stopped, run_id: run.run_id, counts };
  })().finally(() => { inflight = null; });
  return inflight;
}
