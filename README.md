# Spotify review pipeline

Course final assignment: classify the 660,622-review Spotify dataset with `claude-haiku-5-5` under a hard
**$20** API cap, verify a blind sample, group complaints into issues, rank them reproducibly, and write a
decision memo whose every number is checked against saved aggregates. Plan and schedule: `docs/PLAN.md`.
Label definitions: `labels/definitions.md`. Course spec files: `docs/course/`.

**Status (2026-10-16):** the staged program is complete and measured on the 100, 500 and 10,000-review
checkpoints. The full 660k Batch-tier run, the interruption/resume recording and the dashboard deploy
are the remaining steps (see *What is not done yet*).

## Rubric map

| Rubric criterion | Evidence |
|---|---|
| **Deliverable quality** | |
| Accessible code, setup, artifacts | this README; `pip install -r requirements.txt`; every stage is a `python -m pipeline.<stage>` command; offline commands need no key |
| Architecture, shared schema, provenance | [Architecture](#architecture) below; `pipeline/state.py` (one run DB: `source`, `records`, `calls`, `label_cache`, `verifications`, `stage_cache`); `label_config` = label set + model + prompt/schema sha on every record and call; contract row hashes (`pipeline/hashing.py`, checked against the course checker in `tests/test_contract_hash.py`) |
| Memo numbers linked to calculations and evidence | `pipeline/memo.py`: the model may only reference numbers as `{C7}` claim placeholders; code substitutes values from `claims.csv`, rejects unknown claims, issue IDs or review IDs, and flags any typed digits. Memos: `runs/pilot500/artifacts/memo.md`, `runs/pilot10000/artifacts/memo.md` (claims appendix at the bottom of each) |
| Coherent recommendation, alternatives, limitations | memo sections *Recommendation*, *Alternatives*, *Limitations*; Matt's rewrite of the recommendation in his own voice is pending (see below) |
| **Testing & evaluation** | |
| 50 human labels, per-field comparison, error analysis | `evals/golden/human_codes.csv` (Matt, by hand), scorer `pipeline/evals.py golden`, results `evals/golden/results.md` (agreement, macro F1, confusions, every disagreement listed); Matt's written error analysis is pending |
| Independent verification, planted-error and injection tests | blind verifier with a separate prompt: `pipeline/verifier.py`, reports in `runs/*/artifacts/verification.md`; planted-error detection in the same report; prompt-injection test `evals/injection/results.md` (48 synthetic copies, 0 followed the injected instruction) |
| Real 100-review cold/warm pilot, offline calculator, retry/spend/recovery controls (T3) | `cost/README.md`, `cost/report.md`, `cost/estimate.json`, `cost/usage.csv`, `cost/pilot_calls.jsonl`, `cost/pilot_records.jsonl`, `runs/pilot100/pilot_report.json`; controls: `pipeline/budget.py` (shared ledger, reserve-before-send), bounded backoff and per-run cap in `pipeline/llm.py` / `pipeline/pilot.py`, resume demonstrated in `tests/test_stages.py` and on the 10,000 checkpoint (`runs/pilot10000/checkpoints/`), batch reconciliation in `tests/test_batchrun.py` |
| **Working result** | |
| Full ingestion, record coverage, successful classification | `runs/full/ingestion_report.json` (660,622 rows, 13 empty-text quarantines, 484,189 distinct texts, parsed-rows digest identical to the checker's profile); full classification not yet run (needs the go-ahead below) |
| Runnable staged program, bounded calls, saved handoffs, demonstrated resume | `python -m pipeline.run --input <csv> --out runs/<id>`; <=50 reviews per request; every batch committed atomically; `--limit` stop + resume on the 10k checkpoint produced `checkpoint_before.json` / `checkpoint_after.json`; `python -m pipeline.rank --run runs/<id>` regenerates the ranking offline |
| Reproducible baseline ranking, deployed dashboard with grounded recommendations | `pipeline/ranking.py` (Decimal half-up means, exact checker arithmetic, `tests/test_stages.py`); grading export `python -m pipeline.export` passes `check_submission.py` on the 10k checkpoint (`runs/pilot10000/self-check.json`); dashboard not yet deployed (needs Supabase and Vercel credentials) |

## Architecture

```
CSV ─▶ ingest ─▶ run DB (SQLite, WAL) ─▶ enrich ─▶ verify ─▶ group ─▶ rank ─▶ recommend ─▶ export
       profile,     source / records /    Haiku,     Haiku,     code +     code      Sonnet      grading/
       hash, dedupe calls / caches        ≤50/req    blind 1%   1 Haiku    only      1 call      folder
```

| Stage | Module | Model role | Input → output (saved handoff) |
|---|---|---|---|
| Prepare | `pipeline/ingest.py` | none | CSV → `state.sqlite` (`source`, `records` with contract row hash, exact-text `cache_source_id`, 13 `empty_review_text` quarantines), `ingestion_report.json`, `data_manifest.json` |
| Classify | `pipeline/enricher.py` + `pipeline/pilot.py` | `enrich`: `claude-haiku-5-5`, thinking off, effort low, structured output, cached system prompt, ≤50 reviews/request | pending texts → `records.label` (topic, subtopic, intent, severity, sentiment, entities, evidence quote chosen by sentence index and expanded by code so it is always an exact substring, needs_review) + `calls` rows; invalid records retried once then quarantined |
| Verify | `pipeline/verifier.py` | `verify`: Haiku, separate prompt, never sees enricher labels | seeded sample `max(10, 1%)` of model-labelled texts → `verifications` table, `artifacts/verification.{json,md}` with agreement, severity MAE, planted-error detection |
| Group | `pipeline/grouping.py` | `group`: one Haiku call names issues from a bounded evidence pack | complaint/cancellation records → `membership.csv` (issue_id = `topic.subtopic`), `issues.json`, `evidence_pack.json` |
| Rank | `pipeline/ranking.py` | none | `ranking.csv` (`priority_score = severity_sum`), `claims.csv`, `aggregates.json` |
| Recommend | `pipeline/memo.py` | `memo`: `claude-sonnet-5-5`, aggregates and evidence pack only | `memo.json`, `memo.md` with claim IDs on every issue number |
| Export | `pipeline/export.py` | none | `grading/` folder per `GRADING_CONTRACT.md` |

Cross-cutting: `pipeline/budget.py` is one spend ledger (`runs/ledger.sqlite`) shared by every run; each paid
call reserves its worst case first and commits the real cost after. `pipeline/llm.py` adds bounded backoff and
logs failed attempts. Downstream model outputs are cached by the sha256 of exactly what was sent
(`stage_cache`), so a rerun on unchanged inputs makes zero calls (the warm pilot shows 0 enrichment and 0
downstream calls). `pipeline/batchrun.py` is the Batch-tier runner for the full corpus: it records a batch
locally before submitting, reserves its worst case, and on restart reconciles in-flight batches instead of
re-sending them.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill PIPELINE_ANTHROPIC_API_KEY (never committed; .env is git-ignored)
bash scripts/fetch_dataset.sh   # downloads and verifies the course dataset into data/raw/extracted (git-ignored)
```

In a Claude Code cloud environment add `PIPELINE_ANTHROPIC_API_KEY=sk-ant-...` under Environment variables
(the name `ANTHROPIC_API_KEY` is reserved there) and put the fetch line in the Setup script.

## Commands

Offline (no key, no calls):

```bash
python -m pytest -q                               # 37 tests against a fake client, incl. the course checker on an export
python cost/calculator.py                         # offline replay of the 100-review pilot and full-run projection
python -m pipeline.rank --run runs/pilot10000     # regenerate membership, ranking, claims, aggregates from saved labels
python -m pipeline.export --run runs/pilot10000 --out grading --full-ingestion runs/full/ingestion_report.json
python -m pipeline.budget                         # shared spend ledger status
python -m pipeline.batchrun --input data/raw/extracted/spotify_reviews_18months.csv --out runs/full --max-usd 12 --dry-run
```

Paid (each run reserves against the $20 ledger and stops at its own `--max-usd`):

```bash
python -m pipeline.keycheck                       # credential, rates, ledger, model IDs, one Haiku + one Sonnet smoke request
python -m pipeline.pilot --input data/raw/extracted/cost_100.csv \
    --manifest data/raw/extracted/manifest.json --out runs/pilot100 --max-usd 0.25     # cold + warm, all stages
python -m pipeline.run --input data/raw/extracted/checkpoint_500.csv --out runs/pilot500 --max-usd 0.60
python -m pipeline.run --input data/raw/extracted/analysis_10000.csv --out runs/pilot10000 --max-usd 1.50 --limit 2500
python -m pipeline.run --input data/raw/extracted/analysis_10000.csv --out runs/pilot10000 --max-usd 1.50  # resume
python -m pipeline.evals golden                   # classify the golden 50, then score against evals/golden/human_codes.csv
python -m pipeline.evals injection                # 12 reviews x 4 injected instructions through the enricher
```

Interruption/resume demo (to be recorded): start any `pipeline.run`, press Ctrl-C after a few `cold:` lines,
re-run the same command. The run DB only ever holds whole batches, the open spend reservation is released, and
`checkpoints/checkpoint_before.json` is written on interruption; the resumed run finishes the pending texts with
`phase=resume` and writes `checkpoint_after.json`.

## Measured results so far

| Run | Rows | Completed / quarantined | Enrich calls | API cost (all stages) | Enrich wall-clock | Verify agreement (topic / intent / severity) | Memo |
|---|---|---|---|---|---|---|---|
| `runs/pilot100` cold | 100 | 100 / 0 | 3 | $0.0314 (enrich $0.0037) | 19.3 s | 1.0 / 0.9 / 0.9 (n=10) | validated |
| `runs/pilot100` warm | 100 | 100 from cache | 0 | $0 | 0.04 s end to end | reused | cached |
| `runs/pilot500` | 500 | 500 / 0 | 10 | $0.0493 | 88 s | 0.8 / 0.8 / 0.8 (n=10) | validated |
| `runs/pilot10000` | 10,000 | see `runs/pilot10000/run_report.json` | | | | | |

Full-run projection (`cost/report.md`): base scenario with exact-text reuse on the Batch tier about **$10.7**
including verifier, capped Sonnet fallback and fixed memo cost; the same run on the standard tier about $19, and
three of the eight scenarios exceed $20. Recommended: Batch tier. Worst-case reservation for the full run at
batch rates: $12.47 (`runs/full/batchrun_dry_run.json`).

Golden 50 (`evals/golden/results.md`): topic 0.66, intent 0.85 (n=46), severity 0.76, joint 0.54; severity MAE
0.30. Most topic disagreements are praise that the human coded as general (`other`) and the model tied to a
specific praised feature, and non-English text the human coded `unclear` and the model classified. These are
the cases for the written error analysis.

Injection (`evals/injection/results.md`): 46 of 48 synthetic copies returned valid structured output, 0 followed
the injected instruction, every evidence quote was an exact substring; 2 copies produced an out-of-range
evidence index (would be retried, then quarantined in a real run).

## Layout

| Path | What |
|---|---|
| `pipeline/` | ingest, enricher, pilot (cold/warm), run (staged program), verifier, grouping, ranking, memo, export, batchrun, evals, keycheck, budget, pricing, state |
| `cost/` | calculator, rates, usage, pilot evidence, report (see `cost/README.md`) |
| `runs/<id>/` | per-run outputs: `labels.csv`, `artifacts/` (membership, ranking, claims, aggregates, issues, verification, memo), reports; run DBs are git-ignored |
| `evals/` | golden labels and scoring, injection test |
| `labels/definitions.md` | label set `labels-v1` with examples and boundary calls |
| `docs/` | plan, assignment brief, course spec files and checker |
| `tests/` | offline tests against a fake client |

## What is not done yet

1. **Full 660k run** on the Batch tier (`pipeline.batchrun`), then `verify/group/rank/recommend`, the grading
   export and the self-check. Waiting on the go-ahead and the Batch-tier confirmation.
2. **Interruption/resume recording** (Matt runs it on the full run).
3. **Golden error analysis**, **memo recommendation in Matt's voice**, **README "design choices" and "one
   failure" sections** (Matt).
4. **Dashboard**: Supabase Postgres + Next.js on Vercel, reading the saved aggregates, ranking, membership and
   memo. Needs `SUPABASE_*` and `VERCEL_TOKEN` in the environment.
5. Decide the four golden rows (38, 41, 43, 45) recorded with an unresolved intent.
