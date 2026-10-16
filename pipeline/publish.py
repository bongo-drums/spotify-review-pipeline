"""Load a finished run into the dashboard database (Supabase Postgres) — or write the same tables as JSON.

    python -m pipeline.publish --run runs/pilot10000                 # JSON snapshot into web/data/ (file-backed dev mode)
    python -m pipeline.publish --run runs/pilot10000 --db "$SUPABASE_DB_URL"   # load Postgres (needs psycopg)

Tables (schema in web/db/schema.sql): runs, aggregates, issues, membership, records, claims, memo.
Everything comes from the run DB and runs/<id>/artifacts; nothing is recomputed and no model is called.
The web backend (web/) reads these tables and serves them to the dashboard.
"""
from __future__ import annotations

import argparse
import csv
import json
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


def write_json_snapshot(run_dir: Path, out_dir: Path, max_records: int | None = 20000) -> dict:
    """File-backed mode for local development: the web API reads these files when no DATABASE_URL is set."""
    data = load_run(run_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in ("run", "aggregates", "issues", "claims", "memo"):
        (out_dir / f"{name}.json").write_text(json.dumps(data[name], ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "membership.json").write_text(json.dumps(data["membership"], ensure_ascii=False) + "\n", encoding="utf-8")
    n = 0
    with RunState(run_dir / "state.sqlite") as state, open(out_dir / "records.jsonl", "w", encoding="utf-8") as f:
        for rec in records_iter(state):
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
    ap.add_argument("--out", default=str(config.REPO_ROOT / "web" / "data"), help="snapshot directory (JSON mode)")
    ap.add_argument("--max-records", type=int, default=20000, help="JSON mode: cap on records.jsonl rows")
    args = ap.parse_args(argv)
    run_dir = Path(args.run)
    out = load_postgres(run_dir, args.db) if args.db else write_json_snapshot(run_dir, Path(args.out), args.max_records)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
