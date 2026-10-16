"""The offline calculator on a fake-client pilot: the instructor checks in COST_CALCULATOR.md section 5."""
import csv
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

from test_enrich import DATA, fake_client

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("calculator", REPO / "cost" / "calculator.py")
calc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc)


@pytest.fixture(scope="module")
def cost_dir(tmp_path_factory):
    from pipeline import pilot
    if not DATA.exists():
        pytest.skip("course dataset not present")
    tmp = tmp_path_factory.mktemp("pilot")
    out = tmp / "cost"
    pilot.run_pilot(DATA / "cost_100.csv", DATA / "manifest.json", tmp / "p", client=fake_client(),
                    ledger_path=tmp / "l.sqlite", cost_dir=out)
    for name in ("rates.csv", "assumptions.json"):
        shutil.copy(REPO / "cost" / name, out / name)
    return out


def _run(d, **files):
    summary = json.loads((d / "pilot_summary.json").read_text())
    a = json.loads((files.get("assumptions") or d / "assumptions.json").read_text())
    rates = calc.load_rates(files.get("rates") or d / "rates.csv")
    m = calc.measured(calc.load_usage(d / "usage.csv"), rates, summary)
    prof = calc.profile(m["cold"])
    return m, calc.estimate(prof, rates, a, "claude-haiku-5-5", m["cold"]["throughput_records_per_s"])


def test_replay_matches_logged_cost(cost_dir):
    m, est = _run(cost_dir)
    assert m["cold"]["api_cost_usd"] == pytest.approx(m["cold"]["logged_cost_usd"], rel=1e-6)
    assert m["warm"]["api_cost_usd"] == 0 and m["warm"]["attempts"] == 0
    assert est["base"]["with_reuse"]["total_usd"] < est["base"]["no_reuse"]["total_usd"]
    assert calc.main(["--usage", str(cost_dir / "usage.csv"), "--rates", str(cost_dir / "rates.csv"),
                      "--summary", str(cost_dir / "pilot_summary.json"),
                      "--assumptions", str(cost_dir / "assumptions.json"),
                      "--report", str(cost_dir / "report.md")]) == 0
    assert "Full-run estimate" in (cost_dir / "report.md").read_text()


def test_doubling_rates_doubles_api_cost_only(cost_dir, tmp_path):
    doubled = tmp_path / "rates2.csv"
    with open(cost_dir / "rates.csv", newline="") as f, open(doubled, "w", newline="") as g:
        r = csv.DictReader(f)
        w = csv.DictWriter(g, fieldnames=r.fieldnames)
        w.writeheader()
        for row in r:
            w.writerow(row | {"usd_per_mtok": str(float(row["usd_per_mtok"]) * 2)})
    m1, e1 = _run(cost_dir)
    m2, e2 = _run(cost_dir, rates=doubled)
    assert m2["cold"]["api_cost_usd"] == pytest.approx(2 * m1["cold"]["api_cost_usd"])
    assert m2["cold"]["time_s"] == m1["cold"]["time_s"]
    assert e2["base"]["with_reuse"]["total_usd"] == pytest.approx(2 * e1["base"]["with_reuse"]["total_usd"])


def test_projected_count_does_not_change_measured(cost_dir, tmp_path):
    a = json.loads((cost_dir / "assumptions.json").read_text())
    a["distinct_nonempty_texts"] *= 3
    p = tmp_path / "a.json"
    p.write_text(json.dumps(a))
    m1, e1 = _run(cost_dir)
    m2, e2 = _run(cost_dir, assumptions=p)
    assert m1 == m2
    assert e2["base"]["with_reuse"]["total_usd"] > e1["base"]["with_reuse"]["total_usd"]
