"""Offline 100-review cost/runtime calculator (COST_CALCULATOR.md). No API key, no model calls.

    python cost/calculator.py                 # offline replay -> prints tables, writes cost/report.md
    python cost/calculator.py --rates other.csv --assumptions other.json --no-write

Inputs (all in this folder, all editable):
  usage.csv          measured per-call billed tokens from the real pilot (one row per call x unit)
  rates.csv          dated per-1M-token prices per model x tier x unit
  pilot_summary.json measured counts and wall-clock times for the cold and warm runs
  assumptions.json   full-run assumptions (budget, record counts, scenarios)

Formula, per mutually exclusive billing unit (input excludes cache reads/writes, as in the API's usage):
  item_cost = tokens x usd_per_mtok / 1,000,000 ;  total = sum(item_cost)
Stdlib only, so it runs without the pipeline's dependencies.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
UNITS = ("input", "cache_write_5m", "cache_read", "output")


def load_rates(path) -> dict:
    rates = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rates[(r["model"].strip(), r["tier"].strip(), r["unit"].strip())] = float(r["usd_per_mtok"])
    return rates


def rate(rates, model, tier, unit) -> float:
    try:
        return rates[(model, tier, unit)]
    except KeyError:
        raise SystemExit(f"rates.csv has no price for {model} / {tier} / {unit}") from None


def load_usage(path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return [dict(r, tokens=int(r["tokens"])) for r in csv.DictReader(f)]


# ---- measured --------------------------------------------------------------

def measured(usage, rates, summary) -> dict:
    """Recompute the pilot's API cost from usage x rates, per run kind (cold/warm) and role."""
    out = {}
    for kind in ("cold", "warm"):
        rows = [u for u in usage if u["run_kind"] == kind]
        by_role = defaultdict(lambda: {"tokens": dict.fromkeys(UNITS, 0), "cost_usd": 0.0, "requests": set()})
        for u in rows:
            b = by_role[u["role"]]
            b["tokens"][u["unit"]] += u["tokens"]
            b["cost_usd"] += u["tokens"] * rate(rates, u["model"], u["tier"], u["unit"]) / 1e6
            b["requests"].add(u["request_id"])
        run = summary[kind]
        api = sum((b["cost_usd"] for b in by_role.values()), 0.0)
        records = run["records"]
        out[kind] = {
            "records": records, "completed": run["completed"], "quarantined": run["quarantined"],
            "pending": run["pending"], "unique_texts": run["unique_nonblank_texts"],
            "result_cache_hits": run["result_cache_hits"],
            "attempts": run["enrich"]["attempts"], "failed_attempts": run["enrich"]["failed_attempts"],
            "retried_records": run["enrich"]["retried"],
            "roles": {k: {"requests": len(v["requests"]), "tokens": v["tokens"], "cost_usd": v["cost_usd"]}
                      for k, v in by_role.items()},
            "api_cost_usd": api,
            "logged_cost_usd": run["enrich"]["cost_usd"],
            "time_s": run["time_s"],
            "throughput_records_per_s": records / run["time_s"]["end_to_end"] if run["time_s"]["end_to_end"] else None,
            "cost_per_1000_rows_usd": api / records * 1000 if records else None,
            "cost_per_completed_usd": api / run["completed"] if run["completed"] else None,
        }
    return out


# ---- full-run estimate -----------------------------------------------------

def profile(m_cold) -> dict:
    """Per-request prefix tokens and per-review tokens measured on the cold run's enrichment calls."""
    enr = m_cold["roles"].get("enrich")
    if not enr or not enr["requests"]:
        raise SystemExit("no measured enrichment calls in usage.csv; run the paid pilot first")
    t, n_req = enr["tokens"], enr["requests"]
    reviews = m_cold["unique_texts"] + m_cold["retried_records"]  # texts actually sent, retries included
    return {
        "requests": n_req,
        "reviews_sent": reviews,
        "prefix_tokens_per_request": (t["cache_write_5m"] + t["cache_read"]) / n_req,
        "input_tokens_per_review": t["input"] / reviews,
        "output_tokens_per_review": t["output"] / reviews,
    }


def enrich_cost(n_texts, batch, prof, rates, model, tier, hit, out_mult) -> float:
    req = math.ceil(n_texts / batch)
    prefix = req * prof["prefix_tokens_per_request"]
    cached = prefix * hit
    uncached_prefix = prefix - cached
    return (cached * rate(rates, model, tier, "cache_read")
            + uncached_prefix * rate(rates, model, tier, "cache_write_5m")
            + n_texts * prof["input_tokens_per_review"] * rate(rates, model, tier, "input")
            + n_texts * prof["output_tokens_per_review"] * out_mult * rate(rates, model, tier, "output")) / 1e6


def estimate(prof, rates, a, model, throughput) -> dict:
    tier = a["full_run_tier"]
    out = {}
    for name, s in a["scenarios"].items():
        if s["fallback_fraction"] > a["max_fallback_fraction"]:
            raise SystemExit(f"scenario {name}: fallback_fraction exceeds the declared max_fallback_fraction")
        rows = {}
        for reuse, n in (("with_reuse", a["distinct_nonempty_texts"]), ("no_reuse", a["nonempty_rows"])):
            work = n * (1 + s["retry_fraction"])
            enr = enrich_cost(work, a["batch_size"], prof, rates, model, tier,
                              s["prefix_cache_hit_rate"], s["output_tokens_multiplier"])
            ver = enrich_cost(n * s["verify_fraction"], a["batch_size"], prof, rates, a["verify_model"], tier,
                              s["prefix_cache_hit_rate"], s["output_tokens_multiplier"])
            fb = enrich_cost(n * s["fallback_fraction"], a["fallback_batch_size"], prof, rates,
                             a["fallback_model"], tier, s["prefix_cache_hit_rate"], s["output_tokens_multiplier"])
            fo = a["fixed_overhead"]
            fixed = (fo["input_tokens"] * rate(rates, fo["model"], fo["tier"], "input")
                     + fo["output_tokens"] * rate(rates, fo["model"], fo["tier"], "output")) / 1e6
            total = enr + ver + fb + fixed
            rows[reuse] = {
                "texts": n, "requests": math.ceil(work / a["batch_size"]),
                "enrich_usd": enr, "verify_usd": ver, "fallback_usd": fb, "fixed_overhead_usd": fixed,
                "total_usd": total, "over_budget": total > a["budget_usd"],
                "standard_tier_hours_at_measured_throughput":
                    (work / throughput / a["max_concurrency"] / 3600) if throughput else None,
            }
        out[name] = rows
    return out


# ---- report ----------------------------------------------------------------

def fmt(x, nd=4):
    return "unknown" if x is None else (f"${x:,.{nd}f}" if isinstance(x, float) else str(x))


def render(summary, m, prof, est, a, rates_path) -> str:
    cold, warm = m["cold"], m["warm"]
    s = summary["settings"]["enrich"]
    L = ["# 100-review pilot: measured cost and runtime, and full-run estimate", "",
         f"Generated offline by `python cost/calculator.py` from `usage.csv`, `{Path(rates_path).name}`, "
         "`pilot_summary.json` and `assumptions.json`. No API key or model calls.", "",
         "## Measured on `cost_100.csv`", "",
         f"- Input: `{summary['input']['file']}`, sha256 `{summary['input']['sha256']}` "
         "(matches `manifest.json`), 100 IDs.",
         f"- Enricher: provider `{s['provider']}`, model `{s['model']}`, effort `{s['effort']}`, thinking "
         f"`{s['thinking']}`, `{s['prompt_version']}` / `{s['schema_version']}`, batch size {s['batch_size']}, "
         f"{s['workers']} worker, `{s['tier']}` tier, max {s['max_output_tokens_per_request']} output tokens per request.",
         f"- label_config: `{s['label_config']}`",
         f"- Stages not run in this pilot yet: {', '.join(summary['stages_not_run']) or 'none'} "
         "(their cost is unmeasured, not zero).", "",
         "| | Cold run | Warm run |", "|---|---|---|"]
    for label, key in [("Completed", "completed"), ("Quarantined", "quarantined"), ("Pending", "pending"),
                       ("Unique texts", "unique_texts"), ("Result-cache hits", "result_cache_hits"),
                       ("Enrichment attempts", "attempts"), ("Failed attempts", "failed_attempts"),
                       ("Records retried", "retried_records")]:
        L.append(f"| {label} | {cold[key]} | {warm[key]} |")
    for unit in UNITS:
        L.append(f"| Tokens: {unit} | {cold['roles'].get('enrich', {}).get('tokens', {}).get(unit, 0):,} | "
                 f"{warm['roles'].get('enrich', {}).get('tokens', {}).get(unit, 0):,} |")
    L += [f"| API cost (usage x rates) | {fmt(cold['api_cost_usd'], 6)} | {fmt(warm['api_cost_usd'], 6)} |",
          f"| API cost logged at run time | {fmt(cold['logged_cost_usd'], 6)} | {fmt(warm['logged_cost_usd'], 6)} |",
          f"| Wall clock, end to end (s) | {cold['time_s']['end_to_end']} | {warm['time_s']['end_to_end']} |",
          f"| Ingest / enrich (s) | {cold['time_s']['ingest']} / {cold['time_s']['enrich']} | "
          f"{warm['time_s']['ingest']} / {warm['time_s']['enrich']} |",
          f"| Throughput (records/s) | {cold['throughput_records_per_s']:.2f} | {warm['throughput_records_per_s']:.2f} |",
          f"| Cost per 1,000 input rows | {fmt(cold['cost_per_1000_rows_usd'], 5)} | "
          f"{fmt(warm['cost_per_1000_rows_usd'], 5)} |",
          f"| Cost per completed record | {fmt(cold['cost_per_completed_usd'], 7)} | "
          f"{fmt(warm['cost_per_completed_usd'], 7)} |",
          "| Local compute | unknown (not API spend) | unknown |", "",
          f"Warm run made zero enrichment calls: **{summary['warm_zero_enrichment_calls']}**.", "",
          "## Measured token profile used for the estimate", "",
          f"- Prefix (system prompt + schema) per request: {prof['prefix_tokens_per_request']:,.0f} tokens",
          f"- Uncached input per review: {prof['input_tokens_per_review']:,.1f} tokens",
          f"- Output per review: {prof['output_tokens_per_review']:,.1f} tokens", "",
          f"## Full-run estimate ({a['rows_total']:,} rows; {a['nonempty_rows']:,} nonempty; "
          f"{a['empty_text_quarantines']} empty-text quarantines; tier `{a['full_run_tier']}`)", "",
          "| Scenario | Reuse | Texts | Requests | Enrich | Verify | Fallback | Fixed | Total | Budget |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for name, rows in est.items():
        for reuse, r in rows.items():
            flag = "**OVER BUDGET**" if r["over_budget"] else f"within ${a['budget_usd']:.2f}"
            L.append(f"| {name} | {reuse} | {r['texts']:,} | {r['requests']:,} | {fmt(r['enrich_usd'], 2)} | "
                     f"{fmt(r['verify_usd'], 2)} | {fmt(r['fallback_usd'], 2)} | {fmt(r['fixed_overhead_usd'], 2)} | "
                     f"{fmt(r['total_usd'], 2)} | {flag} |")
    L += ["", "Scenario assumptions are in `assumptions.json`. Verify, fallback and fixed overhead reuse the "
          "measured enrichment token profile (or declared token counts) until those stages are measured. "
          "Batch-tier turnaround is not measured (the Batch API allows up to 24 h).", "",
          "| Scenario | Standard-tier hours at the measured throughput and max_concurrency |", "|---|---|"]
    for name, rows in est.items():
        h = rows["with_reuse"]["standard_tier_hours_at_measured_throughput"]
        L.append(f"| {name} | {'unknown' if h is None else f'{h:,.1f}'} |")
    L.append("")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Offline replay of the 100-review pilot cost calculator.")
    ap.add_argument("--usage", default=HERE / "usage.csv")
    ap.add_argument("--rates", default=HERE / "rates.csv")
    ap.add_argument("--summary", default=HERE / "pilot_summary.json")
    ap.add_argument("--assumptions", default=HERE / "assumptions.json")
    ap.add_argument("--report", default=HERE / "report.md")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args(argv)
    summary = json.loads(Path(args.summary).read_text(encoding="utf-8"))
    a = json.loads(Path(args.assumptions).read_text(encoding="utf-8"))
    rates = load_rates(args.rates)
    m = measured(load_usage(args.usage), rates, summary)
    model = summary["settings"]["enrich"]["model"]
    prof = profile(m["cold"])
    est = estimate(prof, rates, a, model, m["cold"]["throughput_records_per_s"])
    report = render(summary, m, prof, est, a, args.rates)
    if not args.no_write:
        Path(args.report).write_text(report, encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
