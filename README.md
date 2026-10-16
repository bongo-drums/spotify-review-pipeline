# Spotify review pipeline

Course final assignment: classify ~660k Spotify app reviews with `claude-haiku-5-5` under a
hard **$20** API cap, then group, rank and recommend. Plan and schedule: `docs/PLAN.md`.
Label definitions: `labels/definitions.md`. Golden set: `evals/golden/`.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill PIPELINE_ANTHROPIC_API_KEY (never committed; .env is git-ignored)
```

In a Claude Code cloud environment, add `PIPELINE_ANTHROPIC_API_KEY=sk-ant-...` under
Environment variables instead (the name `ANTHROPIC_API_KEY` is reserved there and not passed through).

The course dataset (link in `docs/ASSIGNMENT.md`, checksums in `docs/course/manifest.json`) goes in
`data/raw/extracted/` (git-ignored). `bash scripts/fetch_dataset.sh` downloads and verifies it; in a
Claude Code cloud environment put that line in the Setup script so every session has the data.
The course spec files are kept in `docs/course/` (grading contract, calculator spec, checker).

## Before any paid run

```bash
python -m pipeline.keycheck          # credential, rates.csv, ledger, model IDs, one tiny real request
python -m pytest -q                  # everything else runs offline against a fake client
```

`keycheck` sends one enricher-shaped request (thinking off, structured output, cached system
prompt) so a wrong parameter fails here for a fraction of a cent, not during the pilot.
Add `--no-smoke` to skip the paid request.

## 100-review cold/warm pilot

```bash
python -m pipeline.pilot --input data/raw/extracted/cost_100.csv \
    --manifest data/raw/extracted/manifest.json --out runs/pilot100 --max-usd 0.25
python cost/calculator.py            # projects the full run from runs/pilot100/pilot_report.json
```

* `--dry-run` builds every request and prints the worst-case cost without calling the API.
* `--max-usd` is a per-run stop; the shared ledger in `runs/ledger.sqlite` enforces the $20 cap
  across every run (`python -m pipeline.budget` shows it).
* Re-running with the same `--out` resumes: labelled texts are never re-sent.
* Phases: `cold` (real run, empty result cache), `warm` (same input against the saved result
  cache: zero enrichment calls, measured wall-clock). `--phases cold,warm,replay` adds a paid
  replay of the cold requests to measure provider prompt-cache reads and label stability.
* Outputs in `runs/pilot100/`: `pilot_report.json`, `labels.csv` (one row per review, evidence quotes
  are exact substrings), `checkpoint.json`, `ingestion_report.json`, `warm/`. Evidence for the
  calculator spec lands in `cost/`: `pilot_records.jsonl`, `pilot_calls.jsonl`, `usage.csv`.

`cost/calculator.py` is the offline replay: it recomputes the pilot bill from `usage.csv` and the
dated, editable `cost/rates.csv`, then projects the full run (base and conservative scenarios, with
and without exact-text reuse, standard and Batch tiers, verifier sample, capped Sonnet fallback,
remaining pilots, fixed memo cost) and writes `cost/estimate.json` and `cost/report.md`. Scenarios
over `--budget` are flagged. Without a pilot report it uses the assumptions listed in the file and says so.

## Layout

| Path | What |
|---|---|
| `pipeline/ingest.py` | Stage 1: stream, profile, hash and load the CSV into a run DB |
| `pipeline/enricher.py` | Stage 2 request builder + output validator (prompt, schema, evidence expansion) |
| `pipeline/pilot.py` | Cold/warm pilot runner (standard tier) |
| `pipeline/state.py`, `pipeline/budget.py`, `pipeline/pricing.py` | Run DB, spend ledger, rate card |
| `cost/rates.csv`, `cost/calculator.py` | Editable prices and the cost projection |
