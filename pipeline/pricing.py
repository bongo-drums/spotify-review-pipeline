"""Token pricing from the editable cost/rates.csv.

Usage categories are mutually exclusive, as in Anthropic's `usage` object:
`input_tokens` excludes cache reads and cache writes, so

  cost = input*input_rate + cache_creation*cache_write_5m_rate
       + cache_read*cache_read_rate + output*output_rate      (rates per 1M tokens)
"""
from __future__ import annotations

import csv
from pathlib import Path

from . import config

TIERS = ("standard", "batch")
UNITS = ("input", "cache_write_5m", "cache_read", "output")

# usage field -> rate unit
USAGE_UNITS = {
    "input_tokens": "input",
    "cache_creation_input_tokens": "cache_write_5m",
    "cache_read_input_tokens": "cache_read",
    "output_tokens": "output",
}

# claude-haiku-5-5 has a second, higher rate card for prompts over 100K tokens
# which is NOT seeded in rates.csv; refuse to price such requests silently.
LONG_PROMPT_THRESHOLD = {"claude-haiku-5-5": 100_000}

Rates = dict[tuple[str, str, str], float]  # (model, tier, unit) -> USD per 1M tokens


def load_rates(path=None) -> Rates:
    """Read rates.csv into {(model, tier, unit): usd_per_mtok}."""
    rates: Rates = {}
    with open(Path(path or config.RATES_CSV_PATH), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tier, unit = row["tier"].strip(), row["unit"].strip()
            if tier not in TIERS or unit not in UNITS:
                raise ValueError(f"bad rates.csv row: {row}")
            rates[(row["model"].strip(), tier, unit)] = float(row["usd_per_mtok"])
    return rates


def _get(usage, field: str) -> int:
    """Read a usage field from a dict or an SDK usage object; missing/None -> 0."""
    val = usage.get(field) if isinstance(usage, dict) else getattr(usage, field, None)
    return int(val or 0)


def cost_of(usage, model: str, tier: str = "standard", rates: Rates | None = None) -> float:
    """USD cost of one response's usage for `model` on `tier` ('standard' or 'batch')."""
    rates = rates if rates is not None else load_rates()
    if tier not in TIERS:
        raise ValueError(f"tier must be one of {TIERS}, got {tier!r}")
    prompt_tokens = sum(_get(usage, f) for f in USAGE_UNITS if f != "output_tokens")
    limit = LONG_PROMPT_THRESHOLD.get(model)
    if limit is not None and prompt_tokens > limit:
        raise ValueError(f"{model} prompt of {prompt_tokens} tokens exceeds {limit}; long-prompt rates not seeded")
    total = 0.0
    for field, unit in USAGE_UNITS.items():
        n = _get(usage, field)
        if n:
            try:
                rate = rates[(model, tier, unit)]
            except KeyError:
                raise KeyError(f"no rate for model={model!r} tier={tier!r} unit={unit!r} in rates.csv") from None
            total += n * rate / 1_000_000
    return total


def max_cost(model: str, tier: str, prompt_tokens: int, max_output_tokens: int,
             rates: Rates | None = None) -> float:
    """Worst-case cost for a budget reservation: every prompt token billed at the
    priciest input category (usually cache_write_5m) plus max_tokens of output."""
    rates = rates if rates is not None else load_rates()
    in_rate = max(rates[(model, tier, u)] for u in ("input", "cache_write_5m", "cache_read"))
    return (prompt_tokens * in_rate + max_output_tokens * rates[(model, tier, "output")]) / 1_000_000
