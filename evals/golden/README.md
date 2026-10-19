# Golden 50: human labels

- **Source:** `golden_50_to_label.csv` from the course dataset. These 50 reviews are separate from every development file.
- **Labeler:** Matt Wong, by hand, on 2026-10-16. Labels were entered as short codes in a chat with Claude and transcribed verbatim to `human_codes.csv`.
- **Model inputs:** these labels are never sent to any model. They are used only to score predictions after the fact.

## Code format

A code is topic letter, intent letter, severity number:

- **Topic:** `a` access, `u` usability, `p` playback, `d` downloads, `c` catalog, `b` billing, `s` support, `o` other.
- **Intent:** `x` cancellation, `c` complaint, `r` request, `p` praise, `u` unclear.

There are three one-character shortcuts:

| Shortcut | Meaning |
|---|---|
| `+` | other / praise / 1 (general praise) |
| `-` | other / complaint / 2 (general complaint) |
| `?` | other / unclear / 1 (unreadable or off-topic) |

## Entry corrections (recorded, with the originals kept)

Rows 38, 41, 43 and 45 were first entered as `cp2` / `cp3`. Read in key order that is catalog / **praise** with
severity 2–3, which breaks the shared rule that praise has severity 1. On 2026-10-16 Matt asked Claude to use its
judgment on these four; the re-entered codes are in `code`, the original entries stay in `original_code`:

| n | original | re-entered | reading |
|---|---|---|---|
| 38 | cp2 | cc3 | "Lyrics not getting loaded, can't go back to or start song where wanted. Pathetic update": catalog / complaint / 3 |
| 41 | cp3 | ur1 | "The only thing Spotify lacks is the ability to organize saved albums/artists into collections": usability / request / 1 |
| 43 | cp3 | pc3 | "I can't even play the songs that I like and I can't rewind songs": playback / complaint / 3 |
| 45 | cp3 | dc4 | "paying for subscribing but unable to play in offline mode really?": downloads / complaint / 4 |

The other 46 codes are Matt's as typed. The scorer (`python -m pipeline.evals golden`) uses `code` and reports
all 50 rows for every field.
