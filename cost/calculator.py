#!/usr/bin/env python3
"""Offline 100-review cost/runtime calculator (COST_CALCULATOR.md). Never calls the API.

Default (offline replay):
    python cost/calculator.py                      # reads runs/pilot100/pilot_report.json + cost/usage.csv
Options:
    --pilot PATH   pilot report (default runs/pilot100/pilot_report.json)
    --rates PATH   editable dated rates (default cost/rates.csv); doubling every rate doubles API spend
    --budget USD   declared spending limit (default $20); scenarios above it are flagged
    --max-workers N --fallback-frac F --output-cap N   editable controls, printed with the result
Writes cost/estimate.json and cost/report.md. Paid pilot execution is a separate command:
    python -m pipeline.pilot --input data/raw/extracted/cost_100.csv ...

Measured numbers come from the pilot's saved usage; the full-run projection scales the measured
per-text tokens to the 484,189 distinct texts from runs/full/ingestion_report.json. Every input is
shown next to its result. Local compute is reported as unknown, never as zero.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline import pricing  # noqa: E402
from pipeline.budget import SpendLedger  # noqa: E402
from pipeline.config import LEDGER_DB_PATH, SPEND_CAP_USD  # noqa: E402
from pipeline.enricher import EFFORT, MAX_REVIEWS_PER_REQUEST, MODEL, SYSTEM_PROMPT, OUTPUT_TOKENS_PER_REVIEW  # noqa: E402

FALLBACK_MODEL = "claude-sonnet-5-5"
FRAMING_TOKENS_PER_TEXT = 6  # "#k\n[0] " markers: fixed per review, independent of its length
FULL_ROWS, FULL_NONEMPTY, FULL_EMPTY = 660_622, 660_609, 13

# Used only when no pilot report exists. Replaced by measured numbers after the pilot.
ASSUMPTIONS = {
    "chars_per_input_token": 3.3,      # short, multilingual, emoji-heavy text tokenizes worse than prose
    "output_tokens_per_text": 48,      # one compact record with short keys
    "system_prompt_tokens": round(len(SYSTEM_PROMPT) / 3.5),
    "seconds_per_call": 6.0,
}
SCENARIOS = {  # multipliers applied on top of measured per-text usage
    "base": {"retry_overhead": 0.02, "fallback_frac": 0.005, "output_factor": 1.0, "cache_write_frac": 0.02},
    "conservative": {"retry_overhead": 0.10, "fallback_frac": 0.01, "output_factor": 1.2, "cache_write_frac": 0.10},
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def price(tokens: dict, model: str, tier: str, rates) -> float:
    """billed units x price per unit, summed over the mutually exclusive usage categories."""
    return sum(tokens.get(f, 0) * rates[(model, tier, unit)] for f, unit in pricing.USAGE_UNITS.items()) / 1_000_000


# ---- measured ---------------------------------------------------------------

def measured(report: dict, rates) -> dict:
    """Recompute the pilot bill from saved usage (per call) and the editable rates."""
    cold = report["phases"]["cold"]
    if not cold["calls"]:
        raise ValueError("pilot report has no successful cold calls")
    calls = [c for c in cold["calls_detail"] if c["status"] in ("success", "invalid")]
    usage = {k: sum(c[k] or 0 for c in calls) for k in pricing.USAGE_UNITS}
    by_unit = {unit: {"tokens": usage[f], "usd_per_mtok": rates[(report["model"], report["tier"], unit)],
                      "usd": round(usage[f] * rates[(report["model"], report["tier"], unit)] / 1e6, 8)}
               for f, unit in pricing.USAGE_UNITS.items()}
    api_usd = round(sum(u["usd"] for u in by_unit.values()), 8)
    rows = report["input"]["rows"]
    counts = report["final_counts"]
    texts = cold["texts"]
    n_distinct = report["input"]["distinct_texts"]
    chars = report["input"]["distinct_text_chars"]
    in_per_text = usage["input_tokens"] / texts
    avg_chars = chars / n_distinct
    warm = report["phases"].get("warm") or {}
    wall_cold = cold["wall_s_sum_of_calls"]   # one worker: calls never overlap, so the sum is wall-clock
    return {
        "input": {"path": report["input"]["path"], "sha256": report["input"]["sha256"], "rows": rows,
                  "manifest_sha256_matches": report["manifest_check"].get("sha256_matches")},
        "stage": {"role": "enrich", "provider": "anthropic", "model": report["model"], "effort": report.get("effort", EFFORT),
                  "thinking": report.get("thinking", "disabled"), "label_config": report["label_config"],
                  "prompt_sha256": report["prompt_sha256"], "batch_size": report["batch_size"],
                  "workers": report.get("workers", 1), "tier": report["tier"]},
        "records": {"completed": counts["completed"], "quarantined": counts["quarantined"], "pending": counts["pending"],
                    "quarantine_reasons": report["labels"]["quarantine_reasons"],
                    "distinct_nonempty_texts": n_distinct, "texts_sent": texts,
                    "rows_completed_via_exact_text_reuse": rows - counts["quarantined"] - n_distinct},
        "requests": {"succeeded": cold["calls"], "failed_attempts": cold["failed_calls"],
                     "retried_texts": texts - n_distinct},
        "usage": usage, "cost_by_unit": by_unit, "api_cost_usd": api_usd,
        "cost_per_1000_input_rows_usd": round(api_usd / rows * 1000, 6),
        "cost_per_completed_record_usd": round(api_usd / counts["completed"], 8) if counts["completed"] else None,
        "cold": {"wall_clock_s": wall_cold, "calls": cold["calls"], "call_duration_s": cold["call_duration_s"],
                 "throughput_texts_per_s": round(texts / wall_cold, 3) if wall_cold else None,
                 "prompt_cache_read_tokens": usage["cache_read_input_tokens"]},
        "warm": {"wall_clock_s": warm.get("wall_s"), "enrichment_calls": warm.get("enrichment_calls"),
                 "rows_completed_from_result_cache": warm.get("rows_completed_from_cache"),
                 "incremental_api_cost_usd": warm.get("cost_usd"), "counts": warm.get("counts")},
        "replay": report["phases"].get("replay") if report["phases"].get("replay", {}).get("calls") else None,
        "local_compute": "unknown (not measured; one laptop/container process, no GPU)",
        "per_text": {"input_tokens": round(in_per_text, 3), "input_tokens_per_char": round(max((in_per_text - FRAMING_TOKENS_PER_TEXT) / avg_chars, 0.1), 4),
                     "output_tokens_per_text": round(usage["output_tokens"] / texts, 3), "avg_chars": round(avg_chars, 2),
                     "system_prompt_tokens": int(report.get("system_prompt_tokens") or usage["cache_creation_input_tokens"] or ASSUMPTIONS["system_prompt_tokens"]),
                     "seconds_per_call": (cold["call_duration_s"] or {}).get("mean")},
    }


def assumed_params() -> dict:
    a = ASSUMPTIONS
    return {"input_tokens_per_char": round(1 / a["chars_per_input_token"], 4), "output_tokens_per_text": a["output_tokens_per_text"],
            "system_prompt_tokens": a["system_prompt_tokens"], "seconds_per_call": a["seconds_per_call"]}


# ---- projection ---------------------------------------------------------------

def project(params: dict, population: dict, rates, *, model, batch_size, verifier_frac, fixed_usd,
            remaining_pilot_texts, committed_usd, max_workers, budget_usd, output_cap) -> dict:
    chars_full = population["distinct_text_chars"]
    s = params["system_prompt_tokens"]
    out = {}
    for name, sc in SCENARIOS.items():
        for reuse, n in (("exact_text_reuse", population["distinct_texts"]), ("no_reuse", population["nonblank_rows"])):
            chars = chars_full if reuse == "exact_text_reuse" else population["nonblank_chars"]
            requests = math.ceil(n / batch_size)
            work = 1 + sc["retry_overhead"]
            user_in = (n * FRAMING_TOKENS_PER_TEXT + chars * params["input_tokens_per_char"]) * work
            out_tok = n * params["output_tokens_per_text"] * sc["output_factor"] * work
            writes = max(1, math.ceil(requests * sc["cache_write_frac"]))
            for tier in ("standard", "batch"):
                cached = {"input_tokens": user_in, "cache_creation_input_tokens": writes * s,
                          "cache_read_input_tokens": (requests * work - writes) * s, "output_tokens": out_tok}
                uncached = {"input_tokens": user_in + requests * work * s, "output_tokens": out_tok}
                main = {k: round(price({kk: int(round(vv)) for kk, vv in u.items()}, model, tier, rates), 4)
                        for k, u in (("prompt_cache", cached), ("no_prompt_cache", uncached))}
                verifier = round(main["prompt_cache"] * verifier_frac, 4)
                fb_n = math.ceil(n * sc["fallback_frac"])
                fb_usage = {"input_tokens": int(fb_n * FRAMING_TOKENS_PER_TEXT + chars * sc["fallback_frac"] * params["input_tokens_per_char"]),
                            "cache_creation_input_tokens": s, "cache_read_input_tokens": (math.ceil(fb_n / batch_size) - 1) * s,
                            "output_tokens": int(fb_n * params["output_tokens_per_text"])}
                fallback = round(price(fb_usage, FALLBACK_MODEL, "standard", rates), 4)
                pilots = round(remaining_pilot_texts * main["prompt_cache"] / n, 4)
                total = main["prompt_cache"] + verifier + fallback + pilots + fixed_usd + committed_usd
                secs = params.get("seconds_per_call")
                out[f"{name}/{reuse}/{tier}"] = {
                    "scenario": name, "reuse": reuse, "tier": tier, "texts": n, "requests": requests,
                    "assumptions": sc, "main_run": main, "verifier": verifier, "sonnet_fallback": fallback,
                    "remaining_pilots": pilots, "fixed_memo_grouping": fixed_usd, "already_committed": round(committed_usd, 4),
                    "total": round(total, 4), "headroom_vs_budget": round(budget_usd - total, 4),
                    "within_budget": total <= budget_usd,
                    "wall_clock_h": {"standard_1_worker": round(requests * work * secs / 3600, 2) if secs and tier == "standard" else None,
                                     f"standard_{max_workers}_workers": round(requests * work * secs / max_workers / 3600, 2) if secs and tier == "standard" else None,
                                     "batch": "asynchronous, typically < 1 h, guaranteed < 24 h" if tier == "batch" else None},
                }
    return out


def write_report_md(path: Path, est: dict) -> None:
    m, c = est.get("measured"), est["controls"]
    lines = ["# 100-review pilot: measured cost and full-run projection", "",
             f"Generated offline by `cost/calculator.py` from `{est['pilot_report']}` and `{est['rates_path']}` "
             f"(rates dated {est['rates_retrieved_on']}). No API calls. Re-run: `python cost/calculator.py`.", ""]
    if m:
        st, r = m["stage"], m["records"]
        lines += ["## Measured on cost_100.csv (cold run, one worker, empty result cache)", "",
                  f"- Input: `{m['input']['path']}` sha256 `{m['input']['sha256']}` ({m['input']['rows']} rows); manifest match: {m['input']['manifest_sha256_matches']}",
                  f"- Stage enrich: {st['provider']} `{st['model']}`, effort {st['effort']}, thinking {st['thinking']}, tier {st['tier']}, "
                  f"label_config `{st['label_config']}`, ≤{st['batch_size']} reviews/request, {st['workers']} worker",
                  f"- Records: {r['completed']} completed, {r['quarantined']} quarantined {r['quarantine_reasons']}, {r['pending']} pending; "
                  f"{r['distinct_nonempty_texts']} distinct texts, {r['rows_completed_via_exact_text_reuse']} rows via exact-text reuse",
                  f"- Requests: {m['requests']['succeeded']} succeeded, {m['requests']['failed_attempts']} failed attempts, {m['requests']['retried_texts']} texts re-sent after invalid output",
                  "", "| billing item | tokens | USD per MTok | USD |", "|---|---|---|---|"]
        for unit, u in m["cost_by_unit"].items():
            lines.append(f"| {unit} | {u['tokens']:,} | {u['usd_per_mtok']} | {u['usd']:.8f} |")
        lines += [f"| **API total** | | | **{m['api_cost_usd']:.8f}** |", "",
                  f"- Cost per 1,000 input rows: ${m['cost_per_1000_input_rows_usd']:.4f}; per completed record: ${m['cost_per_completed_record_usd']:.6f}",
                  f"- Cold wall-clock: {m['cold']['wall_clock_s']} s over {m['cold']['calls']} sequential calls "
                  f"(mean {m['cold']['call_duration_s']['mean'] if m['cold']['call_duration_s'] else '?'} s); throughput {m['cold']['throughput_texts_per_s']} texts/s; "
                  f"provider prompt-cache reads {m['cold']['prompt_cache_read_tokens']:,} tokens",
                  f"- Warm run (saved result cache): {m['warm']['wall_clock_s']} s, {m['warm']['enrichment_calls']} enrichment calls, "
                  f"{m['warm']['rows_completed_from_result_cache']} rows from cache, incremental API cost ${m['warm']['incremental_api_cost_usd']}",
                  f"- Local compute: {m['local_compute']}", ""]
        if m.get("replay"):
            lines += [f"- Optional paid replay of the cold requests: {m['replay']['calls']} calls, ${m['replay']['cost_usd']}, usage {m['replay']['usage']}", ""]
    else:
        lines += ["## No pilot report yet", "", "Projection below uses the stated assumptions in `calculator.py`.", ""]
    p = est["params"]
    lines += ["## Projection inputs", "",
              f"- per text: {p['input_tokens_per_char']} input tokens/char + {FRAMING_TOKENS_PER_TEXT} framing, {p['output_tokens_per_text']} output tokens; "
              f"system prompt {p['system_prompt_tokens']} tokens per request (cached after the first); {p.get('seconds_per_call')} s per call",
              f"- population: {est['population']['rows']:,} rows → {FULL_NONEMPTY:,} nonempty classifications + {FULL_EMPTY} empty-text quarantines; "
              f"{est['population']['distinct_texts']:,} distinct texts with exact-text reuse",
              f"- controls: budget ${c['budget_usd']:.2f}, output cap {c['output_token_cap']} tokens/request, max workers {c['max_workers']}, "
              f"max fallback fraction {c['max_fallback_frac']}, verifier sample {c['verifier_frac']}, fixed memo/grouping ${c['fixed_usd']:.2f}, "
              f"remaining pilots {c['remaining_pilot_texts']:,} texts, already committed ${est['already_committed_usd']:.4f}",
              f"- scenarios: {json.dumps(SCENARIOS)}", "",
              "## Full-run scenarios (API spend only)", "",
              "| scenario | reuse | tier | requests | main (cache) | main (no cache) | verifier | Sonnet fallback | pilots | fixed | committed | **total** | vs budget |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, s in est["scenarios"].items():
        flag = "" if s["within_budget"] else " ⚠ OVER BUDGET"
        lines.append(f"| {s['scenario']} | {s['reuse']} | {s['tier']} | {s['requests']:,} | ${s['main_run']['prompt_cache']:.2f} | ${s['main_run']['no_prompt_cache']:.2f} | "
                     f"${s['verifier']:.2f} | ${s['sonnet_fallback']:.2f} | ${s['remaining_pilots']:.2f} | ${s['fixed_memo_grouping']:.2f} | ${s['already_committed']:.2f} | "
                     f"**${s['total']:.2f}** | {s['headroom_vs_budget']:+.2f}{flag} |")
    lines += ["", f"Elapsed-time model: standard tier = requests × seconds/call ÷ workers; Batch tier is asynchronous. "
              f"Recommended: **{est['recommended'] or 'none within budget'}**.", "",
              "Formulas: item_cost = billed_tokens × (usd_per_mtok ÷ 1,000,000); categories input / cache_write_5m / cache_read / output are mutually exclusive; "
              "the tier actually used for the pilot is standard; Batch prices appear only in projections."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Offline 100-review cost/runtime calculator (no API calls).")
    ap.add_argument("--pilot", default=str(REPO_ROOT / "runs" / "pilot100" / "pilot_report.json"))
    ap.add_argument("--full", default=str(REPO_ROOT / "runs" / "full" / "ingestion_report.json"))
    ap.add_argument("--rates", default=None)
    ap.add_argument("--ledger", default=str(LEDGER_DB_PATH))
    ap.add_argument("--out", default=str(REPO_ROOT / "cost" / "estimate.json"))
    ap.add_argument("--report", default=str(REPO_ROOT / "cost" / "report.md"))
    ap.add_argument("--budget", type=float, default=SPEND_CAP_USD, help="declared spending limit in USD")
    ap.add_argument("--batch-size", type=int, default=MAX_REVIEWS_PER_REQUEST)
    ap.add_argument("--output-cap", type=int, default=OUTPUT_TOKENS_PER_REVIEW * MAX_REVIEWS_PER_REQUEST)
    ap.add_argument("--max-workers", type=int, default=4)
    ap.add_argument("--fallback-frac", type=float, default=0.01, help="declared maximum Sonnet fallback fraction")
    ap.add_argument("--verifier-frac", type=float, default=0.01)
    ap.add_argument("--fixed-usd", type=float, default=0.50, help="issue naming + memo + recommendations, once")
    ap.add_argument("--remaining-pilot-texts", type=int, default=10_500, help="500 + 10,000 pilots still to run")
    args = ap.parse_args(argv)

    rates_path = Path(args.rates or (REPO_ROOT / "cost" / "rates.csv"))
    rates = pricing.load_rates(rates_path)
    with open(rates_path, newline="", encoding="utf-8") as f:
        retrieved = sorted({r["retrieved_on"] for r in csv.DictReader(f)})
    full = load_json(args.full)
    population = {"source": args.full, "rows": full["rows"]["total"], "nonblank_rows": full["review_text"]["nonblank_rows"],
                  "nonblank_chars": full["text_length_chars_nonblank"]["total_chars"],
                  "distinct_texts": full["review_text"]["distinct_nonblank_texts"],
                  "distinct_text_chars": full["review_text"]["distinct_nonblank_text_chars"]}
    pilot_path = Path(args.pilot)
    meas = None
    if pilot_path.exists():
        report = load_json(pilot_path)
        if report.get("status") == "ok" and report.get("phases", {}).get("cold", {}).get("calls"):
            meas = measured(report, rates)
        else:
            print(f"note: pilot report {pilot_path} has status {report.get('status')!r} and no usable cold calls; "
                  f"falling back to assumptions", file=sys.stderr)
    else:
        print(f"note: no pilot report at {pilot_path}; using stated assumptions", file=sys.stderr)
    params = {**meas["per_text"], "source": "measured pilot"} if meas else {**assumed_params(), "source": "ASSUMPTIONS (no pilot report yet)"}
    model = meas["stage"]["model"] if meas else MODEL
    try:
        ledger = SpendLedger(args.ledger)
        committed = ledger.summary()["committed_usd"]
        ledger.close()
    except Exception:  # noqa: BLE001 - a missing/locked ledger must not block an estimate
        committed = 0.0
    scenarios = project(params, population, rates, model=model, batch_size=args.batch_size, verifier_frac=args.verifier_frac,
                        fixed_usd=args.fixed_usd, remaining_pilot_texts=args.remaining_pilot_texts, committed_usd=committed,
                        max_workers=args.max_workers, budget_usd=args.budget, output_cap=args.output_cap)
    for k, s in scenarios.items():  # declared fallback cap overrides a scenario's fraction when lower
        s["assumptions"] = {**s["assumptions"], "fallback_frac": min(s["assumptions"]["fallback_frac"], args.fallback_frac)}
    pick = [k for k, s in scenarios.items() if s["within_budget"] and s["reuse"] == "exact_text_reuse" and s["tier"] == "batch"]
    est = {"generated_by": "cost/calculator.py (offline)", "pilot_report": str(pilot_path), "rates_path": str(rates_path),
           "rates_retrieved_on": ", ".join(retrieved), "measured": meas, "params": params, "population": population,
           "controls": {"budget_usd": args.budget, "output_token_cap": args.output_cap, "max_workers": args.max_workers,
                        "max_fallback_frac": args.fallback_frac, "verifier_frac": args.verifier_frac, "fixed_usd": args.fixed_usd,
                        "remaining_pilot_texts": args.remaining_pilot_texts},
           "already_committed_usd": committed, "scenarios": scenarios,
           "recommended": "base/exact_text_reuse/batch" if "base/exact_text_reuse/batch" in pick else (pick[0] if pick else None)}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(est, indent=2) + "\n", encoding="utf-8")
    write_report_md(Path(args.report), est)

    if meas:
        print(f"Measured (cold, 1 worker): ${meas['api_cost_usd']:.6f} for {meas['input']['rows']} rows, "
              f"{meas['records']['completed']} completed / {meas['records']['quarantined']} quarantined, "
              f"{meas['cold']['wall_clock_s']} s cold, {meas['warm']['wall_clock_s']} s warm with {meas['warm']['enrichment_calls']} calls")
    else:
        print("Measured: none yet (assumptions mode)")
    print(f"Params: {params}")
    print()
    print("| scenario | reuse | tier | total | vs budget |")
    print("|---|---|---|---|---|")
    for k, s in scenarios.items():
        print(f"| {s['scenario']} | {s['reuse']} | {s['tier']} | ${s['total']:.2f} | {s['headroom_vs_budget']:+.2f}{'' if s['within_budget'] else ' OVER BUDGET'} |")
    print()
    print(f"Recommended: {est['recommended'] or 'NONE WITHIN BUDGET'} (budget ${args.budget:.2f}); wrote {out} and {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
