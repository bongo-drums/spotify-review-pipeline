# 100-review pilot: measured cost and full-run projection

Generated offline by `cost/calculator.py` from `/home/user/spotify-review-pipeline/runs/pilot100/pilot_report.json` and `/home/user/spotify-review-pipeline/cost/rates.csv` (rates dated 2026-10-16). No API calls. Re-run: `python cost/calculator.py`.

## No pilot report yet

Projection below uses the stated assumptions in `calculator.py`.

## Projection inputs

- per text: 0.303 input tokens/char + 6 framing, 48 output tokens; system prompt 1531 tokens per request (cached after the first); 6.0 s per call
- population: 660,622 rows → 660,609 nonempty classifications + 13 empty-text quarantines; 484,189 distinct texts with exact-text reuse
- controls: budget $20.00, output cap 4000 tokens/request, max workers 4, max fallback fraction 0.01, verifier sample 0.01, fixed memo/grouping $0.50, remaining pilots 10,500 texts, already committed $0.0000
- scenarios: {"base": {"retry_overhead": 0.02, "fallback_frac": 0.005, "output_factor": 1.0, "cache_write_frac": 0.02}, "conservative": {"retry_overhead": 0.1, "fallback_frac": 0.01, "output_factor": 1.2, "cache_write_frac": 0.1}}

## Full-run scenarios (API spend only)

| scenario | reuse | tier | requests | main (cache) | main (no cache) | verifier | Sonnet fallback | pilots | fixed | committed | **total** | vs budget |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | exact_text_reuse | standard | 9,684 | $13.81 | $15.14 | $0.14 | $1.35 | $0.30 | $0.50 | $0.00 | **$16.10** | +3.90 |
| base | exact_text_reuse | batch | 9,684 | $6.90 | $7.57 | $0.07 | $1.35 | $0.15 | $0.50 | $0.00 | **$8.98** | +11.02 |
| base | no_reuse | standard | 13,213 | $18.36 | $20.17 | $0.18 | $1.80 | $0.29 | $0.50 | $0.00 | **$21.13** | -1.13 ⚠ OVER BUDGET |
| base | no_reuse | batch | 13,213 | $9.18 | $10.08 | $0.09 | $1.80 | $0.15 | $0.50 | $0.00 | **$11.72** | +8.28 |
| conservative | exact_text_reuse | standard | 9,684 | $17.58 | $18.88 | $0.18 | $2.70 | $0.38 | $0.50 | $0.00 | **$21.34** | -1.34 ⚠ OVER BUDGET |
| conservative | exact_text_reuse | batch | 9,684 | $8.79 | $9.44 | $0.09 | $2.70 | $0.19 | $0.50 | $0.00 | **$12.27** | +7.73 |
| conservative | no_reuse | standard | 13,213 | $23.47 | $25.24 | $0.23 | $3.59 | $0.37 | $0.50 | $0.00 | **$28.17** | -8.17 ⚠ OVER BUDGET |
| conservative | no_reuse | batch | 13,213 | $11.73 | $12.62 | $0.12 | $3.59 | $0.19 | $0.50 | $0.00 | **$16.13** | +3.87 |

Elapsed-time model: standard tier = requests × seconds/call ÷ workers; Batch tier is asynchronous. Recommended: **base/exact_text_reuse/batch**.

Formulas: item_cost = billed_tokens × (usd_per_mtok ÷ 1,000,000); categories input / cache_write_5m / cache_read / output are mutually exclusive; the tier actually used for the pilot is standard; Batch prices appear only in projections.
