"""Shared configuration (paths and the spend cap). Values can be overridden by env vars."""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Hard API spend cap shared by pilots, the full run and every later stage.
DEFAULT_SPEND_CAP_USD = 20.00
SPEND_CAP_USD = float(os.environ.get("SPEND_CAP_USD", DEFAULT_SPEND_CAP_USD))

# One ledger DB for ALL runs, so every run draws from the same cap.
LEDGER_DB_PATH = Path(os.environ.get("LEDGER_DB_PATH", REPO_ROOT / "runs" / "ledger.sqlite"))

RATES_CSV_PATH = Path(os.environ.get("RATES_CSV_PATH", REPO_ROOT / "cost" / "rates.csv"))

# Claude Code cloud environments reserve the name ANTHROPIC_API_KEY for their own login and do
# not pass it into the shell, so the pipeline reads its key under a pipeline-specific name first.
API_KEY_VARS = ("PIPELINE_ANTHROPIC_API_KEY", "ANTHROPIC_API_KEY")


def api_key() -> tuple[str | None, str | None]:
    """(key, env var name) for the first set variable in API_KEY_VARS, else (None, None)."""
    for var in API_KEY_VARS:
        val = os.environ.get(var)
        if val:
            return val, var
    return None, None
