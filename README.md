# Spotify review pipeline

Course final assignment: classify ~660k Spotify app reviews with `claude-haiku-5-5` under a
hard **$20** API cap, then group, rank and recommend. Plan and schedule: `docs/PLAN.md`.
Label definitions: `labels/definitions.md`. Golden set: `evals/golden/`.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env        # fill ANTHROPIC_API_KEY (never committed; .env is git-ignored)
```

The course dataset is unzipped to `data/raw/extracted/` (git-ignored). The pilot expects
`cost_100.csv` and `manifest.json` there; the full run expects `spotify_reviews_18months.csv`.

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
* Outputs in `runs/pilot100/`: `pilot_report.json` (per-phase tokens, cost, wall-clock, cold/warm
  label agreement), `labels.csv` (one row per review, evidence quotes are exact substrings),
  `checkpoint.json`, `ingestion_report.json`.

`cost/calculator.py` prices the 484,189 distinct texts on the standard and Batch tiers, with and
without a working prompt cache, plus the verifier sample, the Sonnet fallback, the remaining
pilots and the memo. Without a pilot report it uses the assumptions listed in the file and says so.

## Layout

| Path | What |
|---|---|
| `pipeline/ingest.py` | Stage 1: stream, profile, hash and load the CSV into a run DB |
| `pipeline/enricher.py` | Stage 2 request builder + output validator (prompt, schema, evidence expansion) |
| `pipeline/pilot.py` | Cold/warm pilot runner (standard tier) |
| `pipeline/state.py`, `pipeline/budget.py`, `pipeline/pricing.py` | Run DB, spend ledger, rate card |
| `cost/rates.csv`, `cost/calculator.py` | Editable prices and the cost projection |
