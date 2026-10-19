#!/usr/bin/env python3
"""Offline 100-review cost/runtime calculator (COST_CALCULATOR.md). Never calls the API.

Default (offline replay):
    python cost/calculator.py                      # reads runs/pilot100/pilot_report.json + cost/rates.csv
Options:
    --pilot PATH        pilot report (default runs/pilot100/pilot_report.json)
    --rates PATH        editable dated rates (default cost/rates.csv); doubling every rate doubles API spend
    --budget USD        declared spending limit (default $20); scenarios above it are flagged
    --refresh PATHS     run_report.json files of the 500 / 10,000 checkpoints (default: those that exist)
    --params-from NAME  which measured run drives the projection: pilot100 (default) or a --refresh run id
    --max-workers N --fallback-frac F --verifier-frac F --fixed-usd USD --output-cap N   editable controls
Writes cost/estimate.json and cost/report.md. Paid pilot execution is a separate command:
    python -m pipeline.pilot --input data/raw/extracted/cost_100.csv ...

Measured numbers come from the pilot's saved usage, stage by stage (enrich, verify, group, memo).
The projection scales the measured per-text enrichment tokens to the 484,189 distinct texts of
runs/full/ingestion_report.json, prices the verifier from its measured per-text cost, and carries the
measured group + memo cost once (with a 2x margin) as the fixed overhead. Every input is shown next to
its result. Local compute is reported as unknown, never as zero.
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
VERIFY_MIN_N = 10
DOWNSTREAM_STAGES = ("fallback", "verify", "group", "memo")   # fallback = Sonnet re-labels of texts Haiku failed twice
FIXED_MARGIN = 2.0           # group + memo are run once; allow one validation retry each

# Used only when no pilot report exists. Replaced by measured numbers after the pilot.
ASSUMPTIONS = {
    "chars_per_input_token": 3.3,      # short, multilingual, emoji-heavy text tokenizes worse than prose
    "output_tokens_per_text": 48,      # one compact record with short keys
    "system_prompt_tokens": round(len(SYSTEM_PROMPT) / 3.5),
    "seconds_per_call": 6.0,
    "fixed_usd": 0.50,                 # issue naming + memo, once
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


def stage_cost(summary: dict, tier: str, rates) -> dict:
    """Recompute one stage's bill from its saved usage; the stage's model comes from its call log."""
    model = (summary.get("models") or [None])[0]
    if not model or not summary.get("calls"):
        return {"calls": 0, "failed_calls": summary.get("failed_calls", 0), "texts": 0, "model": model, "usd": 0.0,
                "usage": summary.get("usage", {}), "wall_s": 0.0}
    usd = round(price(summary["usage"], model, tier, rates), 8)
    return {"calls": summary["calls"], "failed_calls": summary.get("failed_calls", 0), "texts": summary.get("texts", 0),
            "model": model, "usage": summary["usage"], "usd": usd, "wall_s": summary.get("wall_s_sum_of_calls", 0.0),
            "usd_per_text": round(usd / summary["texts"], 8) if summary.get("texts") else None}


# ---- measured ---------------------------------------------------------------

def measured(report: dict, rates) -> dict:
    """Recompute the pilot bill from saved usage (per call, per stage) and the editable rates."""
    cold = report["phases"]["cold"]
    if not cold["calls"]:
        raise ValueError("pilot report has no successful cold calls")
    tier = report["tier"]
    calls = [c for c in cold["calls_detail"] if c["status"] in ("success", "invalid")]
    usage = {k: sum(c[k] or 0 for c in calls) for k in pricing.USAGE_UNITS}
    by_unit = {unit: {"tokens": usage[f], "usd_per_mtok": rates[(report["model"], tier, unit)],
                      "usd": round(usage[f] * rates[(report["model"], tier, unit)] / 1e6, 8)}
               for f, unit in pricing.USAGE_UNITS.items()}
    enrich_usd = round(sum(u["usd"] for u in by_unit.values()), 8)
    stages = {"enrich": {"calls": cold["calls"], "failed_calls": cold["failed_calls"], "texts": cold["texts"], "model": report["model"],
                         "usage": usage, "usd": enrich_usd, "wall_s": cold["wall_s_sum_of_calls"],
                         "usd_per_text": round(enrich_usd / cold["texts"], 8)}}
    for st in DOWNSTREAM_STAGES:
        stages[st] = stage_cost(report.get("stage_calls", {}).get(st, {}), tier, rates)
    api_usd = round(sum(s["usd"] for s in stages.values()), 8)
    rows = report["input"]["rows"]
    counts = report["final_counts"]
    texts = cold["texts"]
    n_distinct = report["input"]["distinct_texts"]
    chars = report["input"]["distinct_text_chars"]
    in_per_text = usage["input_tokens"] / texts
    avg_chars = chars / n_distinct
    warm = report["phases"].get("warm") or {}
    wall_cold = cold["wall_s_sum_of_calls"]   # one worker: calls never overlap, so the sum is wall-clock
    downstream_wall = sum(stages[st]["wall_s"] for st in DOWNSTREAM_STAGES)
    sc = report.get("stages_cold") or {}
    ver = sc.get("verify") or {}
    return {
        "input": {"path": report["input"]["path"], "sha256": report["input"]["sha256"], "rows": rows,
                  "manifest_sha256_matches": report["manifest_check"].get("sha256_matches")},
        "stage": {"role": "enrich", "provider": "anthropic", "model": report["model"], "effort": report.get("effort", EFFORT),
                  "thinking": report.get("thinking", "disabled"), "label_config": report["label_config"],
                  "prompt_sha256": report["prompt_sha256"], "batch_size": report["batch_size"],
                  "workers": report.get("workers", 1), "tier": tier},
        "other_stages": {"verify": {"model": stages["verify"]["model"], "sample_rule": f"max({VERIFY_MIN_N}, ceil(frac x completed heads)), blind, separate prompt",
                                    "verified": ver.get("verified"), "agreement": ver.get("agreement"),
                                    "planted_errors": ver.get("planted_errors")},
                         "group": {"model": stages["group"]["model"], "issues": (sc.get("group") or {}).get("issues"),
                                   "membership_rows": (sc.get("group") or {}).get("membership_rows")},
                         "memo": {"model": report.get("memo_model") or stages["memo"]["model"],
                                  "status": (sc.get("recommend") or {}).get("status")}},
        "records": {"completed": counts["completed"], "quarantined": counts["quarantined"], "pending": counts["pending"],
                    "quarantine_reasons": report["labels"]["quarantine_reasons"],
                    "distinct_nonempty_texts": n_distinct, "texts_sent": texts,
                    "rows_completed_via_exact_text_reuse": rows - counts["quarantined"] - n_distinct},
        "requests": {"succeeded": cold["calls"], "failed_attempts": cold["failed_calls"],
                     "retried_texts": texts - n_distinct,
                     "all_stages_succeeded": sum(s["calls"] for s in stages.values()),
                     "all_stages_failed_attempts": sum(s["failed_calls"] for s in stages.values())},
        "usage": usage, "cost_by_unit": by_unit, "enrich_cost_usd": enrich_usd, "stages": stages,
        "api_cost_usd": api_usd,
        "cost_per_1000_input_rows_usd": round(api_usd / rows * 1000, 6),
        "cost_per_completed_record_usd": round(api_usd / counts["completed"], 8) if counts["completed"] else None,
        "cold": {"wall_clock_s": wall_cold, "calls": cold["calls"], "call_duration_s": cold["call_duration_s"],
                 "throughput_texts_per_s": round(texts / wall_cold, 3) if wall_cold else None,
                 "prompt_cache_read_tokens": usage["cache_read_input_tokens"],
                 "downstream_wall_s": round(downstream_wall, 3), "end_to_end_wall_s": round(wall_cold + downstream_wall, 3)},
        "warm": {"wall_clock_s": warm.get("wall_s"), "enrich_wall_s": warm.get("enrich_wall_s"),
                 "enrichment_calls": warm.get("enrichment_calls"), "downstream_calls": warm.get("downstream_calls"),
                 "rows_completed_from_result_cache": warm.get("rows_completed_from_cache"),
                 "incremental_api_cost_usd": warm.get("cost_usd"), "counts": warm.get("counts")},
        "replay": report["phases"].get("replay") if report["phases"].get("replay", {}).get("calls") else None,
        "local_compute": "unknown (not measured; one laptop/container process, no GPU)",
        "per_text": {"input_tokens": round(in_per_text, 3), "input_tokens_per_char": round(max((in_per_text - FRAMING_TOKENS_PER_TEXT) / avg_chars, 0.1), 4),
                     "output_tokens_per_text": round(usage["output_tokens"] / texts, 3), "avg_chars": round(avg_chars, 2),
                     "system_prompt_tokens": int(report.get("system_prompt_tokens") or usage["cache_creation_input_tokens"] or ASSUMPTIONS["system_prompt_tokens"]),
                     "seconds_per_call": (cold["call_duration_s"] or {}).get("mean"),
                     "verify_usd_per_text": stages["verify"].get("usd_per_text"),
                     "verify_seconds_per_call": round(stages["verify"]["wall_s"] / stages["verify"]["calls"], 3) if stages["verify"]["calls"] else None,
                     "fixed_measured_usd": round(stages["group"]["usd"] + stages["memo"]["usd"], 6)},
    }


def refresh_from_run(path: Path, rates) -> dict | None:
    """Per-text parameters and cost from a later checkpoint run (pipeline.run's run_report.json)."""
    if not path.exists():
        return None
    r = load_json(path)
    sc = r.get("stage_calls") or {}
    enr = sc.get("enrich") or {}
    if r.get("status") != "ok" or not enr.get("calls") or not r.get("input", {}).get("distinct_texts"):
        return {"run_id": r.get("run_id"), "path": str(path), "usable": False, "status": r.get("status"),
                "note": "only a completed run (status ok) is used; partial runs would understate cost per row"}
    tier = r.get("tier", "standard")
    stages = {st: stage_cost(sc.get(st, {}), tier, rates) for st in ("enrich", *DOWNSTREAM_STAGES)}
    texts, chars = enr["texts"], r["input"]["distinct_text_chars"]
    in_per_text = enr["usage"]["input_tokens"] / texts
    avg_chars = chars / r["input"]["distinct_texts"]
    api_usd = round(sum(s["usd"] for s in stages.values()), 6)
    rows = r["input"]["rows"]
    return {"run_id": r["run_id"], "path": str(path), "usable": True, "status": r["status"], "rows": rows,
            "completed": r["counts_after"]["completed"], "quarantined": r["counts_after"]["quarantined"],
            "distinct_texts": r["input"]["distinct_texts"], "texts_sent": texts, "enrich_calls": enr["calls"],
            "failed_attempts": sum(s["failed_calls"] for s in stages.values()),
            "api_cost_usd": api_usd, "cost_per_1000_input_rows_usd": round(api_usd / rows * 1000, 6),
            "stages": {k: {"usd": v["usd"], "calls": v["calls"], "wall_s": v["wall_s"]} for k, v in stages.items()},
            "verify": (r.get("downstream") or {}).get("verify", {}).get("agreement"),
            "per_text": {"input_tokens": round(in_per_text, 3),
                         "input_tokens_per_char": round(max((in_per_text - FRAMING_TOKENS_PER_TEXT) / avg_chars, 0.1), 4),
                         "output_tokens_per_text": round(enr["usage"]["output_tokens"] / texts, 3), "avg_chars": round(avg_chars, 2),
                         "system_prompt_tokens": None, "seconds_per_call": round(enr["wall_s_sum_of_calls"] / enr["calls"], 3),
                         "verify_usd_per_text": stages["verify"].get("usd_per_text"),
                         "verify_seconds_per_call": round(stages["verify"]["wall_s"] / stages["verify"]["calls"], 3) if stages["verify"]["calls"] else None,
                         "fixed_measured_usd": round(stages["group"]["usd"] + stages["memo"]["usd"], 6)}}


def assumed_params() -> dict:
    a = ASSUMPTIONS
    return {"input_tokens_per_char": round(1 / a["chars_per_input_token"], 4), "output_tokens_per_text": a["output_tokens_per_text"],
            "system_prompt_tokens": a["system_prompt_tokens"], "seconds_per_call": a["seconds_per_call"],
            "verify_usd_per_text": None, "verify_seconds_per_call": None, "fixed_measured_usd": None}


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
            n_verify = max(VERIFY_MIN_N, math.ceil(verifier_frac * n))
            verify_requests = math.ceil(n_verify / batch_size)
            for tier in ("standard", "batch"):
                cached = {"input_tokens": user_in, "cache_creation_input_tokens": writes * s,
                          "cache_read_input_tokens": (requests * work - writes) * s, "output_tokens": out_tok}
                uncached = {"input_tokens": user_in + requests * work * s, "output_tokens": out_tok}
                main = {k: round(price({kk: int(round(vv)) for kk, vv in u.items()}, model, tier, rates), 4)
                        for k, u in (("prompt_cache", cached), ("no_prompt_cache", uncached))}
                if params.get("verify_usd_per_text"):
                    # measured on the standard tier; the verifier runs on the same tier as the main run
                    tier_factor = 0.5 if tier == "batch" else 1.0
                    verifier = round(n_verify * params["verify_usd_per_text"] * work * tier_factor, 4)
                    verifier_basis = "measured verify cost per text x sample size"
                else:
                    verifier = round(main["prompt_cache"] * verifier_frac, 4)
                    verifier_basis = "assumed: verifier_frac x main run cost"
                fb_n = math.ceil(n * sc["fallback_frac"])
                fb_usage = {"input_tokens": int(fb_n * FRAMING_TOKENS_PER_TEXT + chars * sc["fallback_frac"] * params["input_tokens_per_char"]),
                            "cache_creation_input_tokens": s, "cache_read_input_tokens": (math.ceil(fb_n / batch_size) - 1) * s,
                            "output_tokens": int(fb_n * params["output_tokens_per_text"])}
                fallback = round(price(fb_usage, FALLBACK_MODEL, "standard", rates), 4)
                pilots = round(remaining_pilot_texts * main["prompt_cache"] / n, 4)
                total = main["prompt_cache"] + verifier + fallback + pilots + fixed_usd + committed_usd
                secs, vsecs = params.get("seconds_per_call"), params.get("verify_seconds_per_call") or params.get("seconds_per_call")
                std_h = ((requests * work * secs) + (verify_requests * vsecs if vsecs else 0)) / 3600 if secs else None
                out[f"{name}/{reuse}/{tier}"] = {
                    "scenario": name, "reuse": reuse, "tier": tier, "texts": n, "requests": requests,
                    "assumptions": sc, "main_run": main, "verifier": verifier, "verifier_texts": n_verify, "verifier_basis": verifier_basis,
                    "sonnet_fallback": fallback, "fallback_texts": fb_n,
                    "remaining_pilots": pilots, "fixed_memo_grouping": fixed_usd, "already_committed": round(committed_usd, 4),
                    "total": round(total, 4), "headroom_vs_budget": round(budget_usd - total, 4),
                    "within_budget": total <= budget_usd,
                    "wall_clock_h": {"standard_1_worker": round(std_h, 2) if std_h and tier == "standard" else None,
                                     f"standard_{max_workers}_workers": round(std_h / max_workers, 2) if std_h and tier == "standard" else None,
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
                  f"- Stage verify: `{m['other_stages']['verify']['model']}`, {m['other_stages']['verify']['sample_rule']}; verified {m['other_stages']['verify']['verified']}, "
                  f"agreement {m['other_stages']['verify']['agreement']}, planted errors {m['other_stages']['verify']['planted_errors']}",
                  f"- Stage group: `{m['other_stages']['group']['model']}` named {m['other_stages']['group']['issues']} issues from {m['other_stages']['group']['membership_rows']} complaint/cancellation records; "
                  f"stage rank: code only; stage memo: `{m['other_stages']['memo']['model']}`, status {m['other_stages']['memo']['status']}",
                  f"- Records: {r['completed']} completed, {r['quarantined']} quarantined {r['quarantine_reasons']}, {r['pending']} pending; "
                  f"{r['distinct_nonempty_texts']} distinct texts, {r['rows_completed_via_exact_text_reuse']} rows via exact-text reuse",
                  f"- Requests: enrich {m['requests']['succeeded']} succeeded, {m['requests']['failed_attempts']} failed attempts, {m['requests']['retried_texts']} texts re-sent after invalid output; "
                  f"all stages {m['requests']['all_stages_succeeded']} succeeded, {m['requests']['all_stages_failed_attempts']} failed attempts (kept in `pilot_calls.jsonl`)",
                  "", "### Enrichment bill (tier actually used)", "", "| billing item | tokens | USD per MTok | USD |", "|---|---|---|---|"]
        for unit, u in m["cost_by_unit"].items():
            lines.append(f"| {unit} | {u['tokens']:,} | {u['usd_per_mtok']} | {u['usd']:.8f} |")
        lines += [f"| **enrich total** | | | **{m['enrich_cost_usd']:.8f}** |", "",
                  "### Cost and time by stage", "", "| stage | model | calls | failed | texts | input | cache write | cache read | output | USD | seconds |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
        for name, s in m["stages"].items():
            u = s.get("usage") or {}
            lines.append(f"| {name} | {s.get('model') or '-'} | {s['calls']} | {s['failed_calls']} | {s['texts']} | {u.get('input_tokens', 0):,} | "
                         f"{u.get('cache_creation_input_tokens', 0):,} | {u.get('cache_read_input_tokens', 0):,} | {u.get('output_tokens', 0):,} | "
                         f"{s['usd']:.6f} | {s['wall_s']} |")
        lines += [f"| **API total** | | | | | | | | | **{m['api_cost_usd']:.6f}** | {m['cold']['end_to_end_wall_s']} |", "",
                  f"- Cost per 1,000 input rows: ${m['cost_per_1000_input_rows_usd']:.4f}; per completed record: ${m['cost_per_completed_record_usd']:.6f}",
                  f"- Cold wall-clock: enrichment {m['cold']['wall_clock_s']} s over {m['cold']['calls']} sequential calls "
                  f"(mean {m['cold']['call_duration_s']['mean'] if m['cold']['call_duration_s'] else '?'} s), throughput {m['cold']['throughput_texts_per_s']} texts/s; "
                  f"downstream stages {m['cold']['downstream_wall_s']} s; end to end {m['cold']['end_to_end_wall_s']} s; "
                  f"provider prompt-cache reads {m['cold']['prompt_cache_read_tokens']:,} tokens",
                  f"- Warm run (saved result cache, same input): {m['warm']['wall_clock_s']} s end to end ({m['warm']['enrich_wall_s']} s to complete "
                  f"{m['warm']['rows_completed_from_result_cache']} rows from cache), {m['warm']['enrichment_calls']} enrichment calls, "
                  f"{m['warm']['downstream_calls']} downstream calls, incremental API cost ${m['warm']['incremental_api_cost_usd']}",
                  f"- Local compute: {m['local_compute']}", ""]
        if m.get("replay"):
            lines += [f"- Optional paid replay of the cold requests: {m['replay']['calls']} calls, ${m['replay']['cost_usd']}, usage {m['replay']['usage']}", ""]
    else:
        lines += ["## No pilot report yet", "", "Projection below uses the stated assumptions in `calculator.py`.", ""]
    if est.get("refresh"):
        lines += ["## Refresh after the 500 and 10,000 checkpoints", "",
                  "| run | rows | completed | distinct texts | enrich calls | failed attempts | input tok/text | output tok/text | s/call | API USD | USD per 1,000 rows | verify agreement |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        if m:
            p = m["per_text"]
            lines.append(f"| pilot100 | {m['input']['rows']} | {m['records']['completed']} | {m['records']['distinct_nonempty_texts']} | {m['cold']['calls']} | "
                         f"{m['requests']['all_stages_failed_attempts']} | {p['input_tokens']} | {p['output_tokens_per_text']} | {p['seconds_per_call']} | "
                         f"{m['api_cost_usd']:.4f} | {m['cost_per_1000_input_rows_usd']:.4f} | {m['other_stages']['verify']['agreement']} |")
        for rf in est["refresh"]:
            if not rf.get("usable"):
                lines.append(f"| {rf.get('run_id')} | not usable ({rf.get('status')}) | | | | | | | | | | |")
                continue
            p = rf["per_text"]
            lines.append(f"| {rf['run_id']} | {rf['rows']:,} | {rf['completed']:,} | {rf['distinct_texts']:,} | {rf['enrich_calls']} | {rf['failed_attempts']} | "
                         f"{p['input_tokens']} | {p['output_tokens_per_text']} | {p['seconds_per_call']} | {rf['api_cost_usd']:.4f} | "
                         f"{rf['cost_per_1000_input_rows_usd']:.4f} | {rf['verify']} |")
        lines.append("")
    p = est["params"]
    lines += ["## Projection inputs", "",
              f"- parameters from: **{p['source']}**",
              f"- per text: {p['input_tokens_per_char']} input tokens/char + {FRAMING_TOKENS_PER_TEXT} framing, {p['output_tokens_per_text']} output tokens; "
              f"system prompt {p['system_prompt_tokens']} tokens per request (cached after the first); {p.get('seconds_per_call')} s per enrich call; "
              f"verifier {p.get('verify_usd_per_text')} USD/text, {p.get('verify_seconds_per_call')} s per call",
              f"- population: {est['population']['rows']:,} rows → {FULL_NONEMPTY:,} nonempty classifications + {FULL_EMPTY} empty-text quarantines; "
              f"{est['population']['distinct_texts']:,} distinct texts with exact-text reuse",
              f"- controls: budget ${c['budget_usd']:.2f}, output cap {c['output_token_cap']} tokens/request, max workers {c['max_workers']}, "
              f"max fallback fraction {c['max_fallback_frac']}, verifier sample {c['verifier_frac']} (min {VERIFY_MIN_N}), fixed group+memo ${c['fixed_usd']:.4f} ({c['fixed_source']}), "
              f"remaining pilots {c['remaining_pilot_texts']:,} texts, already committed ${est['already_committed_usd']:.4f}",
              f"- scenarios: {json.dumps(SCENARIOS)}", "",
              "## Full-run scenarios (API spend only)", "",
              "| scenario | reuse | tier | requests | main (cache) | main (no cache) | verifier | Sonnet fallback | pilots | fixed | committed | **total** | vs budget | std-tier hours (1 / N workers) |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, s in est["scenarios"].items():
        flag = "" if s["within_budget"] else " ⚠ OVER BUDGET"
        h = s["wall_clock_h"]
        hours = f"{h['standard_1_worker']} / {h[f'standard_{c['max_workers']}_workers']}" if s["tier"] == "standard" else "async"
        lines.append(f"| {s['scenario']} | {s['reuse']} | {s['tier']} | {s['requests']:,} | ${s['main_run']['prompt_cache']:.2f} | ${s['main_run']['no_prompt_cache']:.2f} | "
                     f"${s['verifier']:.2f} | ${s['sonnet_fallback']:.2f} | ${s['remaining_pilots']:.2f} | ${s['fixed_memo_grouping']:.2f} | ${s['already_committed']:.2f} | "
                     f"**${s['total']:.2f}** | {s['headroom_vs_budget']:+.2f}{flag} | {hours} |")
    lines += ["", f"Elapsed-time model: standard tier = (enrich requests + verifier requests) × seconds/call ÷ workers; Batch tier is asynchronous. "
              f"Recommended: **{est['recommended'] or 'none within budget'}**.", "",
              "Formulas: item_cost = billed_tokens × (usd_per_mtok ÷ 1,000,000); categories input / cache_write_5m / cache_read / output are mutually exclusive; "
              "the tier actually used for the pilot is standard; Batch prices appear only in projections. The verifier is priced from its measured per-text "
              "cost; group and memo run once and are carried as a fixed cost with a 2x margin; the Sonnet fallback is capped by the declared fraction."]
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
    ap.add_argument("--fixed-usd", type=float, default=None,
                    help="issue naming + memo, once (default: 2x the measured group+memo cost, else $0.50)")
    ap.add_argument("--remaining-pilot-texts", type=int, default=None,
                    help="pilot texts still to run (default: 10,500 minus checkpoint runs found via --refresh)")
    ap.add_argument("--refresh", nargs="*", default=None,
                    help="run_report.json files of later checkpoints (default: runs/pilot500 and runs/pilot10000 if present)")
    ap.add_argument("--params-from", default="pilot100", help="pilot100 or the run_id of a --refresh run")
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

    refresh_paths = ([Path(p) for p in args.refresh] if args.refresh is not None else
                     [REPO_ROOT / "runs" / name / "run_report.json" for name in ("pilot500", "pilot10000")])
    refresh = [r for r in (refresh_from_run(p, rates) for p in refresh_paths) if r is not None]
    remaining = args.remaining_pilot_texts
    if remaining is None:
        remaining = max(0, 10_500 - sum(r["distinct_texts"] for r in refresh if r.get("usable")))

    if meas:
        params = {**meas["per_text"], "source": "measured pilot100"}
    else:
        params = {**assumed_params(), "source": "ASSUMPTIONS (no pilot report yet)"}
    if args.params_from != "pilot100":
        src = next((r for r in refresh if r.get("usable") and r["run_id"] == args.params_from), None)
        if src is None:
            print(f"--params-from {args.params_from}: no usable refresh run with that id; keeping {params['source']}", file=sys.stderr)
        else:
            params = {**params, **{k: v for k, v in src["per_text"].items() if v is not None}, "source": f"measured {src['run_id']}"}
    model = meas["stage"]["model"] if meas else MODEL
    if args.fixed_usd is not None:
        fixed_usd, fixed_source = args.fixed_usd, "--fixed-usd"
    elif params.get("fixed_measured_usd"):
        fixed_usd, fixed_source = round(FIXED_MARGIN * params["fixed_measured_usd"], 4), f"{FIXED_MARGIN:g}x measured group+memo"
    else:
        fixed_usd, fixed_source = ASSUMPTIONS["fixed_usd"], "assumption"
    try:
        ledger = SpendLedger(args.ledger)
        committed = ledger.summary()["committed_usd"]
        ledger.close()
    except Exception:  # noqa: BLE001 - a missing/locked ledger must not block an estimate
        committed = 0.0
    scenarios = project(params, population, rates, model=model, batch_size=args.batch_size, verifier_frac=args.verifier_frac,
                        fixed_usd=fixed_usd, remaining_pilot_texts=remaining, committed_usd=committed,
                        max_workers=args.max_workers, budget_usd=args.budget, output_cap=args.output_cap)
    for k, s in scenarios.items():  # declared fallback cap overrides a scenario's fraction when lower
        s["assumptions"] = {**s["assumptions"], "fallback_frac": min(s["assumptions"]["fallback_frac"], args.fallback_frac)}
    pick = [k for k, s in scenarios.items() if s["within_budget"] and s["reuse"] == "exact_text_reuse" and s["tier"] == "batch"]
    est = {"generated_by": "cost/calculator.py (offline)", "pilot_report": str(pilot_path), "rates_path": str(rates_path),
           "rates_retrieved_on": ", ".join(retrieved), "measured": meas, "refresh": refresh, "params": params, "population": population,
           "controls": {"budget_usd": args.budget, "output_token_cap": args.output_cap, "max_workers": args.max_workers,
                        "max_fallback_frac": args.fallback_frac, "verifier_frac": args.verifier_frac, "fixed_usd": fixed_usd,
                        "fixed_source": fixed_source, "remaining_pilot_texts": remaining},
           "already_committed_usd": committed, "scenarios": scenarios,
           "recommended": "base/exact_text_reuse/batch" if "base/exact_text_reuse/batch" in pick else (pick[0] if pick else None)}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(est, indent=2) + "\n", encoding="utf-8")
    write_report_md(Path(args.report), est)

    if meas:
        print(f"Measured (cold, 1 worker): ${meas['api_cost_usd']:.6f} all stages (enrich ${meas['enrich_cost_usd']:.6f}) for {meas['input']['rows']} rows, "
              f"{meas['records']['completed']} completed / {meas['records']['quarantined']} quarantined, "
              f"{meas['cold']['wall_clock_s']} s enrich + {meas['cold']['downstream_wall_s']} s downstream cold, "
              f"{meas['warm']['wall_clock_s']} s warm with {meas['warm']['enrichment_calls']} enrichment and {meas['warm']['downstream_calls']} downstream calls")
    else:
        print("Measured: none yet (assumptions mode)")
    for r in refresh:
        if r.get("usable"):
            print(f"Refresh {r['run_id']}: {r['rows']:,} rows, ${r['api_cost_usd']:.4f}, ${r['cost_per_1000_input_rows_usd']:.4f} per 1,000 rows, "
                  f"{r['per_text']['input_tokens']} in / {r['per_text']['output_tokens_per_text']} out tokens per text")
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
