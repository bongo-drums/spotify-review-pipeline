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

## Entry inconsistencies (recorded, not corrected)

Rows 38, 41, 43 and 45 were entered as `cp2` / `cp3`. Read in key order, that is catalog / **praise** with severity 2–3, which breaks the shared rule that praise has severity 1. Matt was asked to confirm and chose not to re-enter them. To avoid substituting anyone else's judgment:

- `topic` and `severity` are kept as typed.
- `intent` is marked **unresolved** for these four. They are counted in the ambiguous-case total and excluded from intent agreement, with the denominator reported as 46.
