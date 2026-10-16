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
