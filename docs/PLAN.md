# Final Assignment Plan: Spotify Review Pipeline

Due **Tue Oct 20, 2026, 11:59 pm PT**. Hard API spending cap: **$20.00 total** across pilots, the full run, verification, grouping, the memo and dashboard recommendations. A persistent spend ledger enforces it in code.

## Key decisions

| Decision | Choice | Why |
|---|---|---|
| Enricher / verifier model | `claude-haiku-5-5`, thinking off, structured output | $0.10 in / $0.50 out per MTok. A bounded classification task needs no reasoning tokens. |
| Fallback / memo model | `claude-sonnet-5-5`, capped | Used only for hard cases (≤0.5% of records) and a handful of memo and grouping calls. |
| Full-run tier | Message Batches API (50% off) | Cuts cost in half. Pilots run on the standard tier so we can measure cold/warm wall-clock time. |
| Request size | ≤50 reviews per request | Required by the assignment. A cached system prompt amortizes the instructions. |
| Output size | Compact per-review records | Output tokens are 5× the price of input. The evidence quote is picked by sentence index and expanded by code, so it is always an exact substring. |
| Reuse | Exact-text cache keyed by `sha256(text) + label_config` | 660,609 nonempty texts collapse to 484,189 distinct ones, so every original ID is kept with its `cache_source_id`. |
| State | SQLite run DB with atomic per-batch commits | Gives resume, record statuses and no double-counting. |
| Hosting | Supabase Postgres, plus a Next.js dashboard with API routes on Vercel | The backend reads the DB and serves the dashboard. Recommendations are generated once from saved aggregates and stored. |

## Pre-pilot budget (replaced by measured numbers after the 100-review pilot)

| Item | Estimate |
|---|---|
| Pilots: 100 cold + warm, 500, 10,000 | ~$0.40 |
| Full enrichment, 484k distinct texts, Batch tier | ~$4–8 |
| Verifier: 1% random sample, blind | ~$0.10 |
| Sonnet fallback, capped at 0.5% | ≤$2 |
| Issue naming + memo + dashboard recommendations | <$0.50 |
| **Planned total** | **~$7–11, with a hard stop at $20** |

## Stages (each has an input, output, owner, failure behavior and stop rule)

1. **Prepare** (code): stream all 660,622 rows with a multiline-safe parser, profile them, hash sources, dedupe exact texts and quarantine the 13 empty texts. Outputs: `ingestion_report.json`, `data_manifest.json`, pending queue.
2. **Classify** (Haiku enricher): topic, intent, severity, sentiment, entities, evidence quote and needs_review. Invalid output is retried once, then quarantined. Errors get bounded backoff. Spend reservations are made before dispatch.
3. **Verify** (Haiku verifier, separate prompt): blindly re-labels a declared random sample. Code compares the two labels. Also runs planted-error and prompt-injection test copies.
4. **Group** (code + small model): builds stable issue IDs from topic × subtopic for complaint and cancellation records. The model only suggests names, from bounded examples.
5. **Rank** (code): `priority = complaint_count × mean_severity = severity_sum`. Sorted by score descending, then issue ID ascending. Reproducible offline.
6. **Recommend** (Sonnet memo writer): reads only the aggregates and an evidence pack. Code validates every cited ID and number against `claims.csv`.

## Schedule

| Day | Claude | You (Matt) |
|---|---|---|
| Fri 10/16 | Scaffold, ingestion, labels draft, enricher, labeling tool | Create the repo, unblock dataset access and API key, review label definitions |
| Sat 10/17 | 100-review cold/warm pilot and calculator, 500 run, verifier, injection and planted-error tests | **Hand-label golden 50**, approve scale-up after seeing pilot cost |
| Sun 10/18 | Golden eval, 10k checkpoint, full run via Batch API | Record the interruption/resume demo, write the golden error analysis |
| Mon 10/19 | Group, rank, memo, `grading/` export plus checker, Supabase and Vercel deploy | Review the memo argument, edit recommendation and alternatives in your voice |
| Tue 10/20 | README rubric map, final checks | "One failure in my words" section, final read-through, submit |

## Parts that must be yours (to show this is joint work)

1. **Golden 50 labels.** These must be human labels. The tool shows each review with the definitions, and you choose the labels. Claude never pre-fills them.
2. **Label definitions review.** Claude drafts severity examples and subtopics. You adjust the boundary calls you disagree with, and those edits ship under your commits.
3. **Scale-up approvals.** After each pilot, you decide whether the measured cost justifies the next step.
4. **Golden error analysis.** You write up 3–5 disagreements: what the model got wrong, and whether your own label was debatable.
5. **Interruption/resume recording.** You run the command, hit Ctrl-C mid-run, resume, and screen-record it.
6. **Memo argument.** The model drafts from saved numbers only. You check the reasoning and rewrite the recommendation and alternatives in your own voice.
7. **README "design choices" and "one failure" sections.** These are in your own words, because you'll need to explain them in class.
8. **Accounts and keys.** Anthropic, Supabase and Vercel, never pasted into chat.
