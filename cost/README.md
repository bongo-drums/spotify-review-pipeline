# cost/ — the 100-review cost and runtime calculator

Everything here is reproducible without an API key. Opening or importing the calculator never
starts a paid call.

## Offline replay (default; no key, no network)

```bash
python cost/calculator.py
```

Reads the saved pilot measurements (`runs/pilot100/pilot_report.json`, `cost/usage.csv`), the dated
editable rates in `cost/rates.csv` and the full-file profile in `runs/full/ingestion_report.json`;
recomputes the pilot bill as `billed_tokens x usd_per_mtok / 1,000,000` per mutually exclusive billing
item; projects the full run; writes `cost/estimate.json` and `cost/report.md`.

Editable controls: `--budget`, `--rates`, `--max-workers`, `--fallback-frac`, `--verifier-frac`,
`--fixed-usd`, `--output-cap`, `--remaining-pilot-texts`, `--params-from` (which measured run drives the
projection: `pilot100`, `pilot500` or `pilot10000`). Doubling every rate in a copy of `rates.csv` doubles
the API subtotal and leaves measured time unchanged; changing the projected population never changes
the recorded 100-review results.

## Explicit pilot execution (paid; needs `PIPELINE_ANTHROPIC_API_KEY`)

```bash
python -m pipeline.keycheck                       # credential, rates, ledger, model IDs, two tiny real requests
python -m pipeline.pilot --input data/raw/extracted/cost_100.csv \
    --manifest data/raw/extracted/manifest.json --out runs/pilot100 --max-usd 0.25
```

The pilot runs the actual pipeline on `cost_100.csv` unchanged with an empty result cache and one
worker: enrich (<=50 reviews per request, Haiku, thinking off, structured output, cached system
prompt), verify (blind sample, separate prompt), group (membership by code, one Haiku naming call),
rank (code), recommend (one Sonnet memo call, numbers validated against `claims.csv`). It then repeats
the same input against the saved result cache (`warm`): zero enrichment calls and zero downstream calls
are expected and the wall-clock is measured. Every attempted call, failures included, is saved.

## Files

| file | contents |
|---|---|
| `calculator.py` | offline replay and projection (this folder's program) |
| `rates.csv` | editable prices per model, tier and billing unit, with dated source links |
| `usage.csv` | one row per charged billing item per call: request id, run, phase, role, model, tier, unit, tokens, rate, USD, price source |
| `pilot_records.jsonl` | one row per pilot review id: status, contract row hash, common labels, `cache_source_id` for exact-text reuse |
| `pilot_calls.jsonl` | every attempted call of the pilot run, all stages, with usage, timing, validation result and error text |
| `estimate.json` | calculator output: measured section, projection inputs, every scenario |
| `report.md` | the measured-100 table, stage costs and times, full-run scenarios, budget warnings, chosen controls |

Spend evidence beyond this folder: `runs/ledger.sqlite` is the shared spend ledger every run reserves
against (`python -m pipeline.budget` prints it). Local compute is reported as unknown, never as zero.
