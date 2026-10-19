"""Load a finished run into the dashboard database (Supabase Postgres) — or write the same tables as JSON.

    python -m pipeline.publish --run runs/pilot10000                 # JSON snapshot into web/data/ (file-backed dev mode)
    python -m pipeline.publish --run runs/pilot10000 --db "$SUPABASE_DB_URL"   # load Postgres directly (needs psycopg)
    python -m pipeline.publish --run runs/pilot10000 --rest          # load over HTTPS via Supabase's REST API:
                                                                     # reads SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY
                                                                     # from the environment; tables must already exist
                                                                     # (paste web/db/schema.sql into the SQL editor once)

Tables (schema in web/db/schema.sql): runs, aggregates, issues, membership, records, claims, memo.
Everything comes from the run directory; nothing is recomputed and no model is called. Records come from the run
DB when it is present, otherwise from labels.csv plus the source CSV (run DBs are git-ignored, so a fresh clone
can still publish a committed run). The web backend (web/) reads these tables and serves them to the dashboard.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

from . import config
from .state import RunState, utc_now

SCHEMA_SQL = (config.REPO_ROOT / "web" / "db" / "schema.sql")


def load_run(run_dir: Path) -> dict:
    art = run_dir / "artifacts"
    agg = json.loads((art / "aggregates.json").read_text(encoding="utf-8"))
    issues = json.loads((art / "issues.json").read_text(encoding="utf-8"))["issues"]
    names = {i["issue_id"]: i for i in issues}
    with open(art / "ranking.csv", newline="", encoding="utf-8") as f:
        ranking = list(csv.DictReader(f))
    with open(art / "claims.csv", newline="", encoding="utf-8") as f:
        claims = list(csv.DictReader(f))
    with open(art / "membership.csv", newline="", encoding="utf-8") as f:
        membership = list(csv.DictReader(f))
    memo_json = json.loads((art / "memo.json").read_text(encoding="utf-8")) if (art / "memo.json").exists() else {}
    memo_md = (art / "memo.md").read_text(encoding="utf-8") if (art / "memo.md").exists() else ""
    pack = json.loads((art / "evidence_pack.json").read_text(encoding="utf-8")) if (art / "evidence_pack.json").exists() else {}
    manifest = json.loads((run_dir / "data_manifest.json").read_text(encoding="utf-8"))
    issue_rows = []
    for r in ranking:
        nm = names.get(r["issue_id"], {})
        issue_rows.append({"issue_id": r["issue_id"], "rank": int(r["rank"]), "topic": r["issue_id"].split(".")[0],
                           "subtopic": r["issue_id"].split(".", 1)[1], "name": nm.get("name") or r["issue_id"],
                           "summary": nm.get("summary") or "", "complaint_count": int(r["complaint_count"]),
                           "severity_sum": int(r["severity_sum"]), "mean_severity": r["mean_severity"],
                           "priority_score": int(r["priority_score"]),
                           "examples": pack.get(r["issue_id"], {}).get("examples", [])})
    return {"run": {"run_id": run_dir.name, "published_at": utc_now(), "source_sha256": manifest["source_sha256"],
                    "row_count": manifest["row_count"], "label_config": agg.get("label_config"),
                    "memo_status": memo_json.get("status"), "memo_model": memo_json.get("model")},
            "aggregates": agg, "issues": issue_rows, "membership": membership, "claims": claims,
            "memo": {"status": memo_json.get("status"), "model": memo_json.get("model"), "markdown": memo_md,
                     "json": memo_json.get("memo"), "validation": memo_json.get("validation")}}


def records_iter(state: RunState):
    for r in state.conn.execute(
            "SELECT r.review_id, r.status, r.reason, r.cache_source_id, r.label, s.review_timestamp, s.review_rating "
            "FROM records r JOIN source s USING(review_id) ORDER BY r.row_index"):
        lab = json.loads(r["label"]) if r["label"] else {}
        yield {"review_id": r["review_id"], "status": r["status"], "reason": r["reason"],
               "cache_source_id": r["cache_source_id"] if r["cache_source_id"] != r["review_id"] else None,
               "topic": lab.get("topic"), "subtopic": lab.get("subtopic"), "intent": lab.get("intent"),
               "severity": lab.get("severity"), "sentiment": lab.get("sentiment"), "needs_review": lab.get("needs_review"),
               "evidence_quote": lab.get("evidence_quote"), "month": (r["review_timestamp"] or "")[:7],
               "review_rating": r["review_rating"]}


def records_iter_files(run_dir: Path, source_csv: Path | None = None):
    """Same rows as records_iter, from labels.csv + the source CSV (timestamp, rating) when no run DB exists."""
    manifest = json.loads((run_dir / "data_manifest.json").read_text(encoding="utf-8"))
    src = Path(source_csv) if source_csv else (config.REPO_ROOT / manifest["source_path"])
    meta: dict[str, tuple[str, str]] = {}
    with open(src, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            meta[row["review_id"]] = (row["review_timestamp"], row["review_rating"])
    with open(run_dir / "labels.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ts, rating = meta.get(r["review_id"], ("", None))
            completed = r["status"] == "completed"
            yield {"review_id": r["review_id"], "status": r["status"], "reason": r["reason"] or None,
                   "cache_source_id": r["cache_source_id"] if r["cache_source_id"] != r["review_id"] else None,
                   "topic": r["topic"] or None, "subtopic": r["subtopic"] or None, "intent": r["intent"] or None,
                   "severity": int(r["severity"]) if completed and r["severity"] else None,
                   "sentiment": float(r["sentiment"]) if completed and r["sentiment"] else None,
                   "needs_review": (r["needs_review"] == "True") if completed else None,
                   "evidence_quote": r["evidence_quote"] or None, "month": ts[:7], "review_rating": rating}


def iter_records(run_dir: Path, source_csv: Path | None = None):
    if (run_dir / "state.sqlite").exists():
        with RunState(run_dir / "state.sqlite") as state:
            yield from records_iter(state)
    else:
        yield from records_iter_files(run_dir, source_csv)


# ---- Supabase REST (HTTPS only; for environments without raw Postgres egress) ----------

REST_TABLES_IN_DELETE_ORDER = ("memo", "claims", "membership", "records", "issues", "aggregates", "runs")


def _request(method: str, url: str, key: str, body=None, prefer: str | None = None) -> tuple[int, str]:
    import urllib.error
    import urllib.request
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        **({"Prefer": prefer} if prefer else {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def load_rest(run_dir: Path, base_url: str, key: str, source_csv: Path | None = None, batch: int = 1000,
              request=_request, log=None) -> dict:
    log = log or (lambda m: print(m, file=sys.stderr, flush=True))
    base = base_url.rstrip("/") + "/rest/v1"
    status, text = request("GET", f"{base}/runs?select=run_id&limit=1", key)
    if status != 200:
        raise SystemExit(f"cannot read table runs ({status}): {text[:200]}\n"
                         f"Create the tables once by pasting web/db/schema.sql into the Supabase SQL editor, then retry.")
    data = load_run(run_dir)
    run_id = data["run"]["run_id"]
    for t in REST_TABLES_IN_DELETE_ORDER:
        st, tx = request("DELETE", f"{base}/{t}?run_id=eq.{run_id}", key, prefer="return=minimal")
        if st not in (200, 204):
            raise SystemExit(f"delete from {t} failed ({st}): {tx[:200]}")
    counts = {}

    def post(table: str, rows: list[dict]):
        for i in range(0, len(rows), batch):
            chunk = rows[i:i + batch]
            st, tx = request("POST", f"{base}/{table}", key, chunk, prefer="return=minimal")
            if st not in (200, 201):
                raise SystemExit(f"insert into {table} failed ({st}): {tx[:300]}")
            counts[table] = counts.get(table, 0) + len(chunk)

    r = data["run"]
    post("runs", [r])
    post("aggregates", [{"run_id": run_id, "data": data["aggregates"]}])
    post("issues", [{"run_id": run_id, **i} for i in data["issues"]])
    post("claims", [{"run_id": run_id, **c} for c in data["claims"]])
    m = data["memo"]
    post("memo", [{"run_id": run_id, "status": m["status"], "model": m["model"], "markdown": m["markdown"],
                   "body": m["json"], "validation": m["validation"]}])
    post("membership", [{"run_id": run_id, "issue_id": x["issue_id"], "review_id": x["review_id"]} for x in data["membership"]])
    buf = []
    for rec in iter_records(run_dir, source_csv):
        buf.append({"run_id": run_id, **rec})
        if len(buf) >= batch * 2:
            post("records", buf)
            buf = []
            if counts.get("records", 0) % 50000 < batch * 2:
                log(f"records loaded: {counts['records']:,}")
    if buf:
        post("records", buf)
    return {"db": "supabase-rest", "run_id": run_id, "counts": counts}


def write_json_snapshot(run_dir: Path, out_dir: Path, max_records: int | None = 20000) -> dict:
    """File-backed mode for local development: the web API reads these files when no DATABASE_URL is set."""
    data = load_run(run_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in ("run", "aggregates", "issues", "claims", "memo"):
        (out_dir / f"{name}.json").write_text(json.dumps(data[name], ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "membership.json").write_text(json.dumps(data["membership"], ensure_ascii=False) + "\n", encoding="utf-8")
    n = 0
    with open(out_dir / "records.jsonl", "w", encoding="utf-8") as f:
        for rec in iter_records(run_dir):
            if max_records is not None and n >= max_records:
                break
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return {"out": str(out_dir), "issues": len(data["issues"]), "membership": len(data["membership"]), "records_written": n}


def load_postgres(run_dir: Path, dsn: str) -> dict:
    try:
        import psycopg
    except ImportError as e:  # pragma: no cover
        raise SystemExit("pip install 'psycopg[binary]' to load Postgres") from e
    data = load_run(run_dir)
    run_id = data["run"]["run_id"]
    with psycopg.connect(dsn) as conn, conn.cursor() as cur:
        cur.execute(SCHEMA_SQL.read_text(encoding="utf-8"))
        for t in ("memo", "claims", "membership", "records", "issues", "aggregates", "runs"):
            cur.execute(f"DELETE FROM {t} WHERE run_id = %s", (run_id,))
        r = data["run"]
        cur.execute("INSERT INTO runs(run_id, published_at, source_sha256, row_count, label_config, memo_status, memo_model) "
                    "VALUES (%s,%s,%s,%s,%s,%s,%s)", (run_id, r["published_at"], r["source_sha256"], r["row_count"],
                                                     r["label_config"], r["memo_status"], r["memo_model"]))
        cur.execute("INSERT INTO aggregates(run_id, data) VALUES (%s, %s)", (run_id, json.dumps(data["aggregates"])))
        cur.executemany("INSERT INTO issues(run_id, issue_id, rank, topic, subtopic, name, summary, complaint_count, severity_sum, "
                        "mean_severity, priority_score, examples) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        [(run_id, i["issue_id"], i["rank"], i["topic"], i["subtopic"], i["name"], i["summary"], i["complaint_count"],
                          i["severity_sum"], i["mean_severity"], i["priority_score"], json.dumps(i["examples"])) for i in data["issues"]])
        cur.executemany("INSERT INTO claims(run_id, claim_id, issue_id, metric, value) VALUES (%s,%s,%s,%s,%s)",
                        [(run_id, c["claim_id"], c["issue_id"], c["metric"], c["value"]) for c in data["claims"]])
        m = data["memo"]
        cur.execute("INSERT INTO memo(run_id, status, model, markdown, body, validation) VALUES (%s,%s,%s,%s,%s,%s)",
                    (run_id, m["status"], m["model"], m["markdown"], json.dumps(m["json"]), json.dumps(m["validation"])))
        with cur.copy("COPY membership(run_id, issue_id, review_id) FROM STDIN") as cp:
            for row in data["membership"]:
                cp.write_row((run_id, row["issue_id"], row["review_id"]))
        n = 0
        with RunState(run_dir / "state.sqlite") as state, cur.copy(
                "COPY records(run_id, review_id, status, reason, cache_source_id, topic, subtopic, intent, severity, sentiment, "
                "needs_review, evidence_quote, month, review_rating) FROM STDIN") as cp:
            for rec in records_iter(state):
                cp.write_row((run_id, rec["review_id"], rec["status"], rec["reason"], rec["cache_source_id"], rec["topic"],
                              rec["subtopic"], rec["intent"], rec["severity"], rec["sentiment"], rec["needs_review"],
                              rec["evidence_quote"], rec["month"], rec["review_rating"]))
                n += 1
        conn.commit()
    return {"db": "postgres", "run_id": run_id, "issues": len(data["issues"]), "membership": len(data["membership"]), "records": n}


def main(argv=None) -> int:
    from dotenv import load_dotenv
    load_dotenv(config.REPO_ROOT / ".env")
    ap = argparse.ArgumentParser(description="Publish a run to the dashboard database or a JSON snapshot.")
    ap.add_argument("--run", required=True)
    ap.add_argument("--db", help="Postgres DSN (e.g. $SUPABASE_DB_URL); omitted -> JSON snapshot")
    ap.add_argument("--rest", action="store_true", help="load over HTTPS using SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY from the environment")
    ap.add_argument("--source-csv", help="source CSV for timestamps/ratings when the run DB is absent (default: data_manifest source_path)")
    ap.add_argument("--out", default=str(config.REPO_ROOT / "web" / "data"), help="snapshot directory (JSON mode)")
    ap.add_argument("--max-records", type=int, default=20000, help="JSON mode: cap on records.jsonl rows")
    args = ap.parse_args(argv)
    run_dir = Path(args.run)
    if args.rest:
        url, key = os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            print("--rest needs SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY in the environment (never on the command line)", file=sys.stderr)
            return 1
        out = load_rest(run_dir, url, key, Path(args.source_csv) if args.source_csv else None)
    elif args.db:
        out = load_postgres(run_dir, args.db)
    else:
        out = write_json_snapshot(run_dir, Path(args.out), args.max_records)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
