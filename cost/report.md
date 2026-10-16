# 100-review pilot: measured cost and full-run projection

Generated offline by `cost/calculator.py` from `/home/user/spotify-review-pipeline/runs/pilot100/pilot_report.json` and `/home/user/spotify-review-pipeline/cost/rates.csv` (rates dated 2026-10-16). No API calls. Re-run: `python cost/calculator.py`.

## Measured on cost_100.csv (cold run, one worker, empty result cache)

- Input: `data/raw/extracted/cost_100.csv` sha256 `c884ac3b9be5066995d5063f96ad9af6e5e082975788c1684c4f6b6ea661dd0e` (100 rows); manifest match: True
- Stage enrich: anthropic `claude-haiku-5-5`, effort low, thinking disabled, tier standard, label_config `labels-v1|claude-haiku-5-5|68d569ab095d`, ≤50 reviews/request, 1 worker
- Records: 100 completed, 0 quarantined {}, 0 pending; 100 distinct texts, 0 rows via exact-text reuse
- Requests: 3 succeeded, 0 failed attempts, 3 texts re-sent after invalid output

| billing item | tokens | USD per MTok | USD |
|---|---|---|---|
| input | 4,081 | 0.1 | 0.00040810 |
| cache_write_5m | 0 | 0.125 | 0.00000000 |
| cache_read | 8,439 | 0.01 | 0.00008439 |
| output | 5,879 | 0.5 | 0.00293950 |
| **API total** | | | **0.00343199** |

- Cost per 1,000 input rows: $0.0343; per completed record: $0.000034
- Cold wall-clock: 20.33 s over 3 sequential calls (mean 6.777 s); throughput 5.066 texts/s; provider prompt-cache reads 8,439 tokens
- Warm run (saved result cache): 0.033 s, 0 enrichment calls, 100 rows from cache, incremental API cost $0.0
- Local compute: unknown (not measured; one laptop/container process, no GPU)

## Projection inputs

- per text: 0.4181 input tokens/char + 6 framing, 57.078 output tokens; system prompt 1963 tokens per request (cached after the first); 6.777 s per call
- population: 660,622 rows → 660,609 nonempty classifications + 13 empty-text quarantines; 484,189 distinct texts with exact-text reuse
- controls: budget $20.00, output cap 4000 tokens/request, max workers 4, max fallback fraction 0.01, verifier sample 0.01, fixed memo/grouping $0.50, remaining pilots 10,500 texts, already committed $0.0038
- scenarios: {"base": {"retry_overhead": 0.02, "fallback_frac": 0.005, "output_factor": 1.0, "cache_write_frac": 0.02}, "conservative": {"retry_overhead": 0.1, "fallback_frac": 0.01, "output_factor": 1.2, "cache_write_frac": 0.1}}

## Full-run scenarios (API spend only)

| scenario | reuse | tier | requests | main (cache) | main (no cache) | verifier | Sonnet fallback | pilots | fixed | committed | **total** | vs budget |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | exact_text_reuse | standard | 9,684 | $16.66 | $18.37 | $0.17 | $1.63 | $0.36 | $0.50 | $0.00 | **$19.33** | +0.67 |
| base | exact_text_reuse | batch | 9,684 | $8.33 | $9.18 | $0.08 | $1.63 | $0.18 | $0.50 | $0.00 | **$10.73** | +9.27 |
| base | no_reuse | standard | 13,213 | $22.07 | $24.39 | $0.22 | $2.16 | $0.35 | $0.50 | $0.00 | **$25.31** | -5.31 ⚠ OVER BUDGET |
| base | no_reuse | batch | 13,213 | $11.03 | $12.19 | $0.11 | $2.16 | $0.18 | $0.50 | $0.00 | **$13.99** | +6.01 |
| conservative | exact_text_reuse | standard | 9,684 | $21.18 | $22.85 | $0.21 | $3.26 | $0.46 | $0.50 | $0.00 | **$25.62** | -5.62 ⚠ OVER BUDGET |
| conservative | exact_text_reuse | batch | 9,684 | $10.59 | $11.42 | $0.11 | $3.26 | $0.23 | $0.50 | $0.00 | **$14.69** | +5.31 |
| conservative | no_reuse | standard | 13,213 | $28.18 | $30.45 | $0.28 | $4.32 | $0.45 | $0.50 | $0.00 | **$33.73** | -13.73 ⚠ OVER BUDGET |
| conservative | no_reuse | batch | 13,213 | $14.09 | $15.22 | $0.14 | $4.32 | $0.22 | $0.50 | $0.00 | **$19.28** | +0.72 |

Elapsed-time model: standard tier = requests × seconds/call ÷ workers; Batch tier is asynchronous. Recommended: **base/exact_text_reuse/batch**.

Formulas: item_cost = billed_tokens × (usd_per_mtok ÷ 1,000,000); categories input / cache_write_5m / cache_read / output are mutually exclusive; the tier actually used for the pilot is standard; Batch prices appear only in projections.
