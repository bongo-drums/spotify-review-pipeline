"""Stage 5 (Rank): the reproducible baseline ranking and the aggregate table. Code only, no model calls.

    complaint_count = membership count          severity_sum = sum of member severities
    mean_severity   = severity_sum / count       priority_score = severity_sum  (= count x mean, exact)

Ordered by priority_score descending, then issue_id ascending; ranks from 1. Means are exported
to six decimals with decimal half-up rounding; every other number is an integer string, exactly
as check_submission.py recomputes them.

    python -m pipeline.rank --run runs/<run_id>     # regenerates membership, ranking, claims, aggregates
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from .enricher import INTENTS, TOPICS
from .grouping import build_membership, write_membership_csv
from .state import RunState, utc_now

RANKING_COLUMNS = ("rank", "issue_id", "complaint_count", "severity_sum", "mean_severity", "priority_score")
CLAIM_METRICS = ("complaint_count", "severity_sum", "mean_severity", "priority_score")
CLAIMS_TOP_K = 10
# The assignment's decision question: where should the next quarter of product effort go?
FOCUS_AREAS = {"access": ("access",), "usability": ("usability",), "playback": ("playback",),
               "billing_support": ("billing", "support")}


def mean_string(total: int, n: int) -> str:
    return str((Decimal(total) / Decimal(n)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


def rank(membership: list[dict]) -> list[dict]:
    """Baseline ranking rows (all values strings, as exported)."""
    sums: dict[str, list[int]] = defaultdict(list)
    for m in membership:
        sums[m["issue_id"]].append(int(m["severity"]))
    rows = [{"issue_id": iid, "complaint_count": len(v), "severity_sum": sum(v), "priority_score": sum(v)}
            for iid, v in sums.items()]
    rows.sort(key=lambda r: (-r["priority_score"], r["issue_id"]))
    out = []
    for i, r in enumerate(rows, 1):
        out.append({"rank": str(i), "issue_id": r["issue_id"], "complaint_count": str(r["complaint_count"]),
                    "severity_sum": str(r["severity_sum"]),
                    "mean_severity": mean_string(r["severity_sum"], r["complaint_count"]),
                    "priority_score": str(r["priority_score"])})
    return out


def write_csv(path: Path, columns, rows: list[dict]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(columns))
        w.writeheader()
        for r in rows:
            w.writerow({c: r[c] for c in columns})
    return len(rows)


def build_claims(ranking: list[dict], top_k: int = CLAIMS_TOP_K) -> list[dict]:
    """claim_id,issue_id,metric,value for the top issues: the only numbers the memo may state."""
    claims, n = [], 0
    for r in ranking[:top_k]:
        for metric in CLAIM_METRICS:
            n += 1
            claims.append({"claim_id": f"C{n}", "issue_id": r["issue_id"], "metric": metric, "value": r[metric]})
    return claims


def aggregates(state: RunState, ranking: list[dict], membership: list[dict], issues: list[dict] | None = None,
               run_id: str | None = None) -> dict:
    """Everything the memo and dashboard read: counts, distributions, per-topic complaint load, trends."""
    counts = state.status_counts()
    quarantine = {r: n for r, n in state.conn.execute(
        "SELECT reason, COUNT(*) FROM records WHERE status='quarantined' GROUP BY reason")}
    by_topic, by_intent, by_sev, by_sent, by_month_topic = Counter(), Counter(), Counter(), Counter(), Counter()
    sev_sum_topic, complaints_topic, needs_review, n = Counter(), Counter(), 0, 0
    sentiment_total = 0.0
    for r in state.conn.execute(
            "SELECT json_extract(r.label,'$.topic') t, json_extract(r.label,'$.intent') i, json_extract(r.label,'$.severity') v, "
            "json_extract(r.label,'$.sentiment') m, json_extract(r.label,'$.needs_review') nr, substr(s.review_timestamp,1,7) mo "
            "FROM records r JOIN source s USING(review_id) WHERE r.status='completed'"):
        n += 1
        by_topic[r["t"]] += 1
        by_intent[r["i"]] += 1
        by_sev[str(r["v"])] += 1
        by_sent[str(r["m"])] += 1
        sentiment_total += float(r["m"])
        needs_review += int(bool(r["nr"]))
        if r["i"] in ("complaint", "cancellation"):
            complaints_topic[r["t"]] += 1
            sev_sum_topic[r["t"]] += int(r["v"])
            by_month_topic[(r["mo"], r["t"])] += 1
    months = sorted({mo for mo, _ in by_month_topic})
    focus = {}
    for area, topics in FOCUS_AREAS.items():
        cc = sum(complaints_topic[t] for t in topics)
        ss = sum(sev_sum_topic[t] for t in topics)
        focus[area] = {"topics": list(topics), "complaint_count": cc, "severity_sum": ss,
                       "mean_severity": mean_string(ss, cc) if cc else None,
                       "share_of_complaints": round(cc / len(membership), 4) if membership else None}
    name_by_id = {i["issue_id"]: i for i in (issues or [])}
    top = [{**r, "name": name_by_id.get(r["issue_id"], {}).get("name"),
            "summary": name_by_id.get(r["issue_id"], {}).get("summary")} for r in ranking[:CLAIMS_TOP_K]]
    return {
        "generated_at": utc_now(), "run_id": run_id,
        "records": {"total": sum(counts.values()), **counts, "quarantine_reasons": quarantine,
                    "completed_fraction": round(counts["completed"] / sum(counts.values()), 6) if counts else None},
        "labelled": n,
        "by_topic": {t: by_topic[t] for t in TOPICS}, "by_intent": {i: by_intent[i] for i in INTENTS},
        "by_severity": {str(k): by_sev[str(k)] for k in range(1, 6)},
        "by_sentiment": dict(sorted(by_sent.items())),
        "mean_sentiment": round(sentiment_total / n, 4) if n else None,
        "needs_review": {"count": needs_review, "fraction": round(needs_review / n, 4) if n else None},
        "complaints": {"total": len(membership), "by_topic": {t: complaints_topic[t] for t in TOPICS},
                       "severity_sum_by_topic": {t: sev_sum_topic[t] for t in TOPICS}},
        "focus_areas": focus,
        "complaints_by_month_topic": {mo: {t: by_month_topic[(mo, t)] for t in TOPICS if by_month_topic[(mo, t)]} for mo in months},
        "issues": len(ranking), "top_issues": top,
        "ranking_rule": "priority_score = severity_sum = complaint_count x mean_severity; sort score desc, issue_id asc",
    }


def run_rank(state: RunState, run_dir, run_id: str | None = None) -> dict:
    """Regenerate membership.csv, ranking.csv, claims.csv and aggregates.json from the run DB. Offline."""
    art = Path(run_dir) / "artifacts"
    art.mkdir(parents=True, exist_ok=True)
    membership = build_membership(state)
    write_membership_csv(membership, art / "membership.csv")
    ranking = rank(membership)
    write_csv(art / "ranking.csv", RANKING_COLUMNS, ranking)
    claims = build_claims(ranking)
    write_csv(art / "claims.csv", ("claim_id", "issue_id", "metric", "value"), claims)
    issues = None
    issues_path = art / "issues.json"
    if issues_path.exists():
        issues = json.loads(issues_path.read_text(encoding="utf-8")).get("issues")
    agg = aggregates(state, ranking, membership, issues, run_id or Path(run_dir).name)
    (art / "aggregates.json").write_text(json.dumps(agg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"membership_rows": len(membership), "issues": len(ranking), "claims": len(claims),
            "top": ranking[:5], "focus_areas": agg["focus_areas"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Regenerate the baseline ranking from saved outputs (no model calls).")
    ap.add_argument("--run", required=True, help="run directory with state.sqlite")
    args = ap.parse_args(argv)
    run_dir = Path(args.run)
    with RunState(run_dir / "state.sqlite") as state:
        out = run_rank(state, run_dir)
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
