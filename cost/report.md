# 100-review pilot: measured cost and full-run projection

Generated offline by `cost/calculator.py` from `/home/user/spotify-review-pipeline/runs/pilot100/pilot_report.json` and `/home/user/spotify-review-pipeline/cost/rates.csv` (rates dated 2026-10-16). No API calls. Re-run: `python cost/calculator.py`.

## Measured on cost_100.csv (cold run, one worker, empty result cache)

- Input: `data/raw/extracted/cost_100.csv` sha256 `c884ac3b9be5066995d5063f96ad9af6e5e082975788c1684c4f6b6ea661dd0e` (100 rows); manifest match: True
- Stage enrich: anthropic `claude-haiku-5-5`, effort low, thinking disabled, tier standard, label_config `labels-v1|claude-haiku-5-5|68d569ab095d`, ≤50 reviews/request, 1 worker
- Stage verify: `claude-haiku-5-5`, max(10, ceil(frac x completed heads)), blind, separate prompt; verified 10, agreement {'topic': 1.0, 'intent': 0.9, 'severity': 0.9, 'joint': 0.8}, planted errors {'planted': 5, 'detected': 5, 'detection_rate': 1.0}
- Stage group: `claude-haiku-5-5` named 17 issues from 51 complaint/cancellation records; stage rank: code only; stage memo: `claude-sonnet-5-5`, status validated
- Records: 100 completed, 0 quarantined {}, 0 pending; 100 distinct texts, 0 rows via exact-text reuse
- Requests: enrich 3 succeeded, 0 failed attempts, 2 texts re-sent after invalid output; all stages 6 succeeded, 1 failed attempts (kept in `pilot_calls.jsonl`)

### Enrichment bill (tier actually used)

| billing item | tokens | USD per MTok | USD |
|---|---|---|---|
| input | 3,944 | 0.1 | 0.00039440 |
| cache_write_5m | 2,813 | 0.125 | 0.00035162 |
| cache_read | 5,626 | 0.01 | 0.00005626 |
| output | 5,743 | 0.5 | 0.00287150 |
| **enrich total** | | | **0.00367378** |

### Cost and time by stage

| stage | model | calls | failed | texts | input | cache write | cache read | output | USD | seconds |
|---|---|---|---|---|---|---|---|---|---|---|
| enrich | claude-haiku-5-5 | 3 | 0 | 102 | 3,944 | 2,813 | 5,626 | 5,743 | 0.003674 | 19.257 |
| verify | claude-haiku-5-5 | 1 | 0 | 10 | 378 | 1,334 | 0 | 294 | 0.000352 | 2.171 |
| group | claude-haiku-5-5 | 1 | 0 | 30 | 2,415 | 553 | 0 | 1,210 | 0.000916 | 7.587 |
| memo | claude-sonnet-5-5 | 1 | 1 | 13 | 2,175 | 1,334 | 0 | 1,881 | 0.026495 | 18.091 |
| **API total** | | | | | | | | | **0.031436** | 47.106 |

- Cost per 1,000 input rows: $0.3144; per completed record: $0.000314
- Cold wall-clock: enrichment 19.257 s over 3 sequential calls (mean 6.419 s), throughput 5.297 texts/s; downstream stages 27.849 s; end to end 47.106 s; provider prompt-cache reads 5,626 tokens
- Warm run (saved result cache, same input): 0.039 s end to end (0.023 s to complete 100 rows from cache), 0 enrichment calls, 0 downstream calls, incremental API cost $0
- Local compute: unknown (not measured; one laptop/container process, no GPU)

## Refresh after the 500 and 10,000 checkpoints

| run | rows | completed | distinct texts | enrich calls | failed attempts | input tok/text | output tok/text | s/call | API USD | USD per 1,000 rows | verify agreement |
|---|---|---|---|---|---|---|---|---|---|---|---|
| pilot100 | 100 | 100 | 100 | 3 | 1 | 38.667 | 56.304 | 6.419 | 0.0314 | 0.3144 | {'topic': 1.0, 'intent': 0.9, 'severity': 0.9, 'joint': 0.8} |
| pilot500 | 500 | 500 | 479 | 10 | 0 | 37.994 | 56.376 | 8.753 | 0.0493 | 0.0986 | {'topic': 0.8, 'intent': 0.8, 'severity': 0.8, 'joint': 0.8} |
| pilot10000 | not usable (stopped_at_limit) | | | | | | | | | | |

## Projection inputs

- parameters from: **measured pilot100**
- per text: 0.4062 input tokens/char + 6 framing, 56.304 output tokens; system prompt 1963 tokens per request (cached after the first); 6.419 s per enrich call; verifier 3.515e-05 USD/text, 2.171 s per call
- population: 660,622 rows → 660,609 nonempty classifications + 13 empty-text quarantines; 484,189 distinct texts with exact-text reuse
- controls: budget $20.00, output cap 4000 tokens/request, max workers 4, max fallback fraction 0.01, verifier sample 0.01 (min 10), fixed group+memo $0.0548 (2x measured group+memo), remaining pilots 10,021 texts, already committed $0.2321
- scenarios: {"base": {"retry_overhead": 0.02, "fallback_frac": 0.005, "output_factor": 1.0, "cache_write_frac": 0.02}, "conservative": {"retry_overhead": 0.1, "fallback_frac": 0.01, "output_factor": 1.2, "cache_write_frac": 0.1}}

## Full-run scenarios (API spend only)

| scenario | reuse | tier | requests | main (cache) | main (no cache) | verifier | Sonnet fallback | pilots | fixed | committed | **total** | vs budget | std-tier hours (1 / N workers) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | exact_text_reuse | standard | 9,684 | $16.41 | $18.12 | $0.17 | $1.61 | $0.34 | $0.05 | $0.23 | **$18.82** | +1.18 | 17.67 / 4.42 |
| base | exact_text_reuse | batch | 9,684 | $8.21 | $9.06 | $0.09 | $1.61 | $0.17 | $0.05 | $0.23 | **$10.36** | +9.64 | async |
| base | no_reuse | standard | 13,213 | $21.75 | $24.07 | $0.24 | $2.13 | $0.33 | $0.05 | $0.23 | **$24.73** | -4.73 ⚠ OVER BUDGET | 24.11 / 6.03 |
| base | no_reuse | batch | 13,213 | $10.87 | $12.03 | $0.12 | $2.13 | $0.16 | $0.05 | $0.23 | **$13.57** | +6.43 | async |
| conservative | exact_text_reuse | standard | 9,684 | $20.87 | $22.54 | $0.19 | $3.21 | $0.43 | $0.05 | $0.23 | **$24.99** | -4.99 ⚠ OVER BUDGET | 19.05 / 4.76 |
| conservative | exact_text_reuse | batch | 9,684 | $10.44 | $11.27 | $0.09 | $3.21 | $0.22 | $0.05 | $0.23 | **$14.25** | +5.75 | async |
| conservative | no_reuse | standard | 13,213 | $27.78 | $30.05 | $0.26 | $4.26 | $0.42 | $0.05 | $0.23 | **$33.00** | -13.00 ⚠ OVER BUDGET | 26.0 / 6.5 |
| conservative | no_reuse | batch | 13,213 | $13.89 | $15.02 | $0.13 | $4.26 | $0.21 | $0.05 | $0.23 | **$18.77** | +1.23 | async |

Elapsed-time model: standard tier = (enrich requests + verifier requests) × seconds/call ÷ workers; Batch tier is asynchronous. Recommended: **base/exact_text_reuse/batch**.

Formulas: item_cost = billed_tokens × (usd_per_mtok ÷ 1,000,000); categories input / cache_write_5m / cache_read / output are mutually exclusive; the tier actually used for the pilot is standard; Batch prices appear only in projections. The verifier is priced from its measured per-text cost; group and memo run once and are carried as a fixed cost with a 2x margin; the Sonnet fallback is capped by the declared fraction.
