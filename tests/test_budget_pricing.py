import csv
import threading

import pytest

from pipeline import pricing
from pipeline.budget import BudgetExceeded, SpendLedger


# ---- budget ---------------------------------------------------------------

def test_reservation_overflow(tmp_path):
    ledger = SpendLedger(tmp_path / "ledger.sqlite", cap_usd=1.00, run_id="pilot")
    a = ledger.reserve(0.60)
    with pytest.raises(BudgetExceeded):
        ledger.reserve(0.50)  # 0.60 outstanding + 0.50 > 1.00
    ledger.commit(a, 0.30)
    b = ledger.reserve(0.70)  # 0.30 committed + 0.70 == cap: allowed
    with pytest.raises(BudgetExceeded):
        ledger.reserve(0.01)
    ledger.release(b)
    s = ledger.summary()
    assert s["committed_usd"] == pytest.approx(0.30)
    assert s["outstanding_reservations_usd"] == 0
    assert s["remaining_usd"] == pytest.approx(0.70)
    with pytest.raises(ValueError):
        ledger.commit(a, 0.1)  # already closed


def test_cap_shared_across_processes_and_runs(tmp_path):
    path = tmp_path / "ledger.sqlite"
    first = SpendLedger(path, cap_usd=1.00, run_id="pilot")
    first.commit(first.reserve(0.80), 0.80)
    first.close()
    second = SpendLedger(path, cap_usd=1.00, run_id="full")  # fresh connection, different run
    with pytest.raises(BudgetExceeded):
        second.reserve(0.25)
    second.reserve(0.20)


def test_release_orphans(tmp_path):
    path = tmp_path / "ledger.sqlite"
    crashed = SpendLedger(path, cap_usd=1.00, run_id="r")
    crashed.reserve(0.90)  # process "dies" without commit/release
    resumed = SpendLedger(path, cap_usd=1.00, run_id="r")
    with pytest.raises(BudgetExceeded):
        resumed.reserve(0.20)
    assert resumed.release_orphans() == 1
    resumed.reserve(0.20)


def test_thread_safe_reservations(tmp_path):
    ledger = SpendLedger(tmp_path / "ledger.sqlite", cap_usd=1.00)
    ok, refused = [], []

    def worker():
        for _ in range(10):
            try:
                ok.append(ledger.reserve(0.05))
            except BudgetExceeded:
                refused.append(1)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(ok) == 20 and len(refused) == 60  # exactly $1.00 reserved, never more


# ---- pricing --------------------------------------------------------------

USAGE = {"input_tokens": 10_000, "cache_creation_input_tokens": 2_000,
         "cache_read_input_tokens": 50_000, "output_tokens": 3_000}


def test_cost_arithmetic_haiku_standard_and_batch():
    rates = pricing.load_rates()
    expected = (10_000 * 0.10 + 2_000 * 0.125 + 50_000 * 0.01 + 3_000 * 0.50) / 1e6
    assert pricing.cost_of(USAGE, "claude-haiku-5-5", "standard", rates) == pytest.approx(expected)
    assert pricing.cost_of(USAGE, "claude-haiku-5-5", "batch", rates) == pytest.approx(expected / 2)


def test_doubling_rates_doubles_cost(tmp_path):
    src = pricing.config.RATES_CSV_PATH
    doubled = tmp_path / "rates.csv"
    with open(src, newline="") as f, open(doubled, "w", newline="") as g:
        reader = csv.DictReader(f)
        w = csv.DictWriter(g, fieldnames=reader.fieldnames)
        w.writeheader()
        for row in reader:
            row["usd_per_mtok"] = str(float(row["usd_per_mtok"]) * 2)
            w.writerow(row)
    for model in ("claude-haiku-5-5", "claude-sonnet-5-5"):
        for tier in ("standard", "batch"):
            base = pricing.cost_of(USAGE, model, tier, pricing.load_rates(src))
            assert pricing.cost_of(USAGE, model, tier, pricing.load_rates(doubled)) == pytest.approx(2 * base)


def test_usage_object_and_unknown_model():
    class Usage:  # mimics the SDK usage object (attributes, None for absent cache fields)
        input_tokens = 1_000_000
        output_tokens = 0
        cache_creation_input_tokens = None
        cache_read_input_tokens = None

    assert pricing.cost_of(Usage(), "claude-sonnet-5-5", "standard") == pytest.approx(2.00)
    with pytest.raises(KeyError):
        pricing.cost_of(USAGE, "no-such-model", "standard")


def test_long_prompt_guard_and_max_cost():
    with pytest.raises(ValueError):
        pricing.cost_of({"input_tokens": 100_001}, "claude-haiku-5-5")
    # worst case bills the prompt at cache_write_5m (0.125) plus full output
    assert pricing.max_cost("claude-haiku-5-5", "standard", 10_000, 2_000) == pytest.approx(
        (10_000 * 0.125 + 2_000 * 0.50) / 1e6)
