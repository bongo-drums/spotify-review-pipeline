#!/usr/bin/env python3
"""Project the full-run cost from the 100-review pilot (or from stated assumptions before it).

Usage:  python cost/calculator.py [--pilot runs/pilot100/pilot_report.json]
                                  [--full runs/full/ingestion_report.json] [--out cost/estimate.json]

Reads per-text token averages from the pilot report, scales them to the full population of
distinct nonblank texts (from the full ingestion report), and prices the main run on the
standard and Batch tiers with and without a working prompt cache. Adds the verifier sample,
the capped Sonnet fallback, the remaining pilots, the fixed memo/grouping allowance, and what
the ledger has already committed. Every input is printed next to the result so it can be
checked by hand; nothing here calls the API.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from pipeline import pricing  # noqa: E402
from pipeline.budget import SpendLedger  # noqa: E402
from pipeline.config import LEDGER_DB_PATH, SPEND_CAP_USD  # noqa: E402
from pipeline.enricher import MAX_REVIEWS_PER_REQUEST, MODEL, SYSTEM_PROMPT, max_output_tokens  # noqa: E402

FALLBACK_MODEL = "claude-sonnet-5-5"
FRAMING_TOKENS_PER_TEXT = 6  # "#k\n[0] " markers: fixed per review, independent of its length

# Used only when no pilot report exists. Replace by measured numbers after the pilot.
ASSUMPTIONS = {
    "chars_per_input_token": 3.3,      # short, multilingual, emoji-heavy text tokenizes worse than prose
    "output_tokens_per_text": 48,      # one compact record with short keys
    "system_prompt_tokens": round(len(SYSTEM_PROMPT) / 3.5),
    "seconds_per_call": 6.0,
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pilot_params(report: dict) -> dict:
    """Per-text measurements from a pilot report's cold phase (first cache write excluded)."""
    cold = report["phases"]["cold"]
    if not cold["calls"]:
        raise ValueError("pilot report has no successful cold calls")
    texts = cold["texts"]
    chars = report["input"]["distinct_text_chars"]
    usage = cold["usage"]
    in_per_text = usage["input_tokens"] / texts
    avg_chars = chars / report["input"]["distinct_texts"]
    rate = max((in_per_text - FRAMING_TOKENS_PER_TEXT) / avg_chars, 0.1)  # tokens per char of review text
    sys_tokens = report.get("system_prompt_tokens") or (usage["cache_creation_input_tokens"] // max(1, sum(
        1 for c in cold["calls_detail"] if c["cache_creation_input_tokens"]) or 1))
    return {
        "source": report["input"]["path"], "run_id": report["run_id"], "model": report["model"],
        "pilot_texts": texts, "pilot_avg_chars_per_text": round(avg_chars, 2),
        "input_tokens_per_text": round(in_per_text, 3),
        "input_tokens_per_char": round(rate, 4), "framing_tokens_per_text": FRAMING_TOKENS_PER_TEXT,
        "output_tokens_per_text": round(usage["output_tokens"] / texts, 3),
        "system_prompt_tokens": int(sys_tokens),
        "seconds_per_call": cold["call_duration_s"]["mean"] if cold["call_duration_s"] else None,
        "warm_seconds_per_call": (report["phases"]["warm"]["call_duration_s"] or {}).get("mean")
        if report["phases"].get("warm") else None,
        "cold_cost_per_text_usd": cold["per_text"]["cost_usd"],
        "cache_worked": usage["cache_read_input_tokens"] > 0,
        "cold_warm_agreement": (report.get("labels") or {}).get("cold_warm_agreement"),
    }


def assumed_params() -> dict:
    a = ASSUMPTIONS
    return {"source": "ASSUMPTIONS (no pilot report yet)", "model": MODEL,
            "input_tokens_per_char": round(1 / a["chars_per_input_token"], 4),
            "framing_tokens_per_text": FRAMING_TOKENS_PER_TEXT,
            "output_tokens_per_text": a["output_tokens_per_text"], "system_prompt_tokens": a["system_prompt_tokens"],
            "seconds_per_call": a["seconds_per_call"], "cache_worked": None}


def price(tokens: dict, model: str, tier: str, rates) -> float:
    """Price aggregate token totals (whole-run sums, so pricing.cost_of's per-request
    long-prompt guard does not apply; every individual request stays ~3K tokens)."""
    return sum(tokens.get(f, 0) * rates[(model, tier, unit)] for f, unit in pricing.USAGE_UNITS.items()) / 1_000_000


def project(params: dict, population: dict, rates, *, batch_size: int, cache_write_frac: float,
            verifier_frac: float, fallback_frac: float, fixed_usd: float, remaining_pilot_texts: int,
            committed_usd: float, concurrency: int, cap_usd: float) -> dict:
    n = population["distinct_texts"]
    chars = population["distinct_text_chars"]
    s = params["system_prompt_tokens"]
    requests = math.ceil(n / batch_size)
    user_in = n * params["framing_tokens_per_text"] + chars * params["input_tokens_per_char"]
    out = n * params["output_tokens_per_text"]
    writes = max(1, math.ceil(requests * cache_write_frac))

    def main_run(tier: str, cached: bool) -> dict:
        if cached:
            usage = {"input_tokens": user_in, "cache_creation_input_tokens": writes * s,
                     "cache_read_input_tokens": (requests - writes) * s, "output_tokens": out}
        else:
            usage = {"input_tokens": user_in + requests * s, "output_tokens": out}
        usage = {k: int(round(v)) for k, v in usage.items()}
        return {"usd": round(price(usage, params["model"], tier, rates), 4), "tokens": usage}

    scenarios = {f"{tier}_{'cached' if c else 'uncached'}": main_run(tier, c)
                 for tier in ("standard", "batch") for c in (True, False)}

    # Verifier: same model, a separate prompt of similar size, on a random sample.
    verifier = {k: round(v["usd"] * verifier_frac, 4) for k, v in scenarios.items()}
    # Sonnet fallback on hard cases only: same per-text tokens at Sonnet rates, standard tier.
    fb_n = math.ceil(n * fallback_frac)
    fb_req = math.ceil(fb_n / batch_size)
    fb_usage = {"input_tokens": int(fb_n * params["framing_tokens_per_text"] + chars * fallback_frac * params["input_tokens_per_char"]),
                "cache_creation_input_tokens": s, "cache_read_input_tokens": (fb_req - 1) * s,
                "output_tokens": int(fb_n * params["output_tokens_per_text"])}
    fallback_usd = round(price(fb_usage, FALLBACK_MODEL, "standard", rates), 4)
    # Remaining pilots (500 + 10,000) on the standard tier, cached.
    per_text_cached_std = scenarios["standard_cached"]["usd"] / n
    pilots_usd = round(remaining_pilot_texts * per_text_cached_std, 4)

    totals = {}
    for k, v in scenarios.items():
        total = v["usd"] + verifier[k] + fallback_usd + pilots_usd + fixed_usd + committed_usd
        totals[k] = {"main_run": v["usd"], "verifier": verifier[k], "sonnet_fallback": fallback_usd,
                     "remaining_pilots": pilots_usd, "fixed_memo_grouping": fixed_usd,
                     "already_committed": round(committed_usd, 4), "total": round(total, 4),
                     "headroom_vs_cap": round(cap_usd - total, 4), "within_cap": total <= cap_usd}
    secs = params.get("seconds_per_call")
    wall = {"standard_sequential_h": round(requests * secs / 3600, 2) if secs else None,
            f"standard_{concurrency}_workers_h": round(requests * secs / concurrency / 3600, 2) if secs else None,
            "batch": "asynchronous; most batches finish within an hour, guaranteed within 24 h"}
    return {"population": population, "requests": requests, "batch_size": batch_size,
            "cache_writes_assumed": writes, "params": params, "main_run": scenarios, "totals": totals,
            "wall_clock": wall, "cap_usd": cap_usd,
            "recommended": "batch_cached" if totals["batch_cached"]["within_cap"] else None}


def _fmt_table(est: dict) -> str:
    rows = ["| scenario | main run | verifier | Sonnet fallback | pilots left | fixed | committed | **total** | headroom |",
            "|---|---|---|---|---|---|---|---|---|"]
    for k, t in est["totals"].items():
        rows.append(f"| {k} | ${t['main_run']:.2f} | ${t['verifier']:.2f} | ${t['sonnet_fallback']:.2f} | "
                    f"${t['remaining_pilots']:.2f} | ${t['fixed_memo_grouping']:.2f} | ${t['already_committed']:.2f} | "
                    f"**${t['total']:.2f}** | ${t['headroom_vs_cap']:.2f} |")
    return "\n".join(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Project full-run cost from the pilot.")
    ap.add_argument("--pilot", default=str(REPO_ROOT / "runs" / "pilot100" / "pilot_report.json"))
    ap.add_argument("--full", default=str(REPO_ROOT / "runs" / "full" / "ingestion_report.json"))
    ap.add_argument("--rates", default=None)
    ap.add_argument("--ledger", default=str(LEDGER_DB_PATH))
    ap.add_argument("--out", default=str(REPO_ROOT / "cost" / "estimate.json"))
    ap.add_argument("--batch-size", type=int, default=MAX_REVIEWS_PER_REQUEST)
    ap.add_argument("--cache-write-frac", type=float, default=0.02, help="share of requests that re-write the cache")
    ap.add_argument("--verifier-frac", type=float, default=0.01)
    ap.add_argument("--fallback-frac", type=float, default=0.005)
    ap.add_argument("--fixed-usd", type=float, default=0.50, help="issue naming + memo + recommendations")
    ap.add_argument("--remaining-pilot-texts", type=int, default=10_500, help="500 + 10,000 pilots still to run")
    ap.add_argument("--concurrency", type=int, default=4)
    args = ap.parse_args(argv)

    rates = pricing.load_rates(args.rates)
    full = load_json(args.full)
    population = {"source": args.full, "rows": full["rows"]["total"],
                  "nonblank_rows": full["review_text"]["nonblank_rows"],
                  "distinct_texts": full["review_text"]["distinct_nonblank_texts"],
                  "distinct_text_chars": full["review_text"]["distinct_nonblank_text_chars"]}
    pilot_path = Path(args.pilot)
    if pilot_path.exists():
        report = load_json(pilot_path)
        if report.get("status") not in ("ok",) or not report.get("phases", {}).get("cold", {}).get("calls"):
            print(f"note: pilot report {pilot_path} has status {report.get('status')!r} and no usable cold calls; "
                  f"falling back to assumptions", file=sys.stderr)
            params = assumed_params()
        else:
            params = pilot_params(report)
    else:
        print(f"note: no pilot report at {pilot_path}; using stated assumptions", file=sys.stderr)
        params = assumed_params()
    try:
        ledger = SpendLedger(args.ledger)
        committed = ledger.summary()["committed_usd"]
        ledger.close()
    except Exception:  # noqa: BLE001 - a missing/locked ledger must not block an estimate
        committed = 0.0

    est = project(params, population, rates, batch_size=args.batch_size, cache_write_frac=args.cache_write_frac,
                  verifier_frac=args.verifier_frac, fallback_frac=args.fallback_frac, fixed_usd=args.fixed_usd,
                  remaining_pilot_texts=args.remaining_pilot_texts, committed_usd=committed,
                  concurrency=args.concurrency, cap_usd=SPEND_CAP_USD)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(est, indent=2) + "\n", encoding="utf-8")

    p = est["params"]
    print(f"Inputs: {p['source']}")
    print(f"  model {p['model']}; system prompt {p['system_prompt_tokens']} tok; "
          f"{p['input_tokens_per_char']} input tok/char + {p['framing_tokens_per_text']} framing tok/text; "
          f"{p['output_tokens_per_text']} output tok/text; cache worked: {p['cache_worked']}")
    pop = est["population"]
    print(f"Population: {pop['distinct_texts']:,} distinct texts ({pop['nonblank_rows']:,} nonblank rows), "
          f"{pop['distinct_text_chars']:,} chars -> {est['requests']:,} requests of {est['batch_size']}")
    print()
    print(_fmt_table(est))
    print()
    print(f"Wall clock: {est['wall_clock']}")
    print(f"Recommended: {est['recommended'] or 'NONE WITHIN CAP'}  (cap ${est['cap_usd']:.2f}); written {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
