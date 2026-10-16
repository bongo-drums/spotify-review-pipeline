# Cost and runtime calculator (100-review pilot)

Spec: `COST_CALCULATOR.md` in the course dataset ZIP.

## Offline replay (default, no API key, no model calls)

```sh
python cost/calculator.py
```

This reads `usage.csv`, `rates.csv`, `pilot_summary.json` and `assumptions.json`, recomputes every API cost as `tokens × usd_per_mtok / 1,000,000` per billing unit, prints the measured and estimated tables, and writes `report.md`. It needs only the Python standard library, and importing it makes no calls.

To check the arithmetic, edit `rates.csv` (doubling every rate doubles the API subtotals and leaves measured time unchanged) or `assumptions.json` (changing projected counts changes only the estimate).

## Explicit paid pilot (costs about $0.003 and reserves at most $0.25 per run)

```sh
cp .env.example .env            # then fill ANTHROPIC_API_KEY locally; .env is gitignored
python -m pipeline.keycheck     # free: reports which env vars are set and makes one count_tokens call
python -m pipeline.pilot --input data/raw/extracted/cost_100.csv \
    --manifest data/raw/extracted/manifest.json --out runs/pilot100 --max-usd 0.25
python cost/calculator.py
```

The pilot refuses to run if `cost_100.csv` differs from `manifest.json` (byte count and SHA-256). It then runs:

1. **Cold run.** Fresh run DB and an empty result cache, one worker, `claude-haiku-5-5` with thinking disabled at effort `low`, standard tier, 50 reviews per request.
2. **Warm run.** Fresh run DB that imports only the cold run's result cache. It must make zero enrichment calls.

Every paid request first reserves its worst-case cost in the shared ledger (`runs/ledger.sqlite`, $20 global cap). It then commits the cost computed from the response's `usage`. Failed attempts are logged too. Timeouts book their worst-case cost until they are reconciled against the Anthropic console.

## Files

| File | Contents |
|---|---|
| `calculator.py` | Offline calculator |
| `rates.csv` | Dated per-1M-token prices by model, tier and unit, with source links |
| `assumptions.json` | Editable full-run assumptions: budget, counts, base and conservative scenarios, maximum fallback fraction |
| `usage.csv` | Measured billed tokens, one row per call × unit, keyed by provider `request_id` (written by the pilot) |
| `pilot_calls.jsonl` | Every attempted call with run ID, role, phase, outcome, model, settings, usage, timing and cost (written by the pilot) |
| `pilot_records.jsonl` | One result per pilot ID with the contract row hash and common labels (written by the pilot) |
| `pilot_summary.json` | Measured counts and wall-clock times for the cold and warm runs (written by the pilot) |
| `report.md` | Rendered tables (written by `calculator.py`) |

Local compute is not API spend and is marked `unknown`, not zero.
