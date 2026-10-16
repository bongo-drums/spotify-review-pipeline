# Label definitions (label set `labels-v1`)

> **Status: DRAFT by Claude, pending Matt's review.** Boundary calls marked ⚖️ are judgment calls that Matt should confirm or change before the golden set is labeled.
> Every example is a real review from `analysis_10000.csv`, a development file, quoted verbatim. None come from `golden_50_to_label.csv`.

The primary labels and their precedence are fixed by `GRADING_CONTRACT.md`. This file adds worked examples and optional subtopics, which the grouping stage uses as stable issue IDs.

## Decision procedure (applied to the review text only; stars are never used)

1. **Intent**, using this precedence: `cancellation` > `complaint` > `request` > `praise` > `unclear`.
   - `cancellation`: explicitly leaving, uninstalling or cancelling, or threatening to.
   - `complaint`: a negative experience, including mixed praise and criticism, and generic "bad app".
   - `request`: wants a change without reporting a failure.
   - `praise`: positive only.
   - `unclear`: meaningless, unrelated or unsupported-language text, and bare boycott slogans.
2. **Topic**: the problem with the highest supported severity. On a tie, the first specific problem mentioned. For positive reviews, the first specific praised feature. General praise or criticism is `other`.
3. **Severity**, using the shared 1–5 scale. Angry language, stars, an expensive plan, a crash mention or cancellation intent do not raise severity on their own.
4. **needs_review** is `true` when the impact or topic cannot be determined from the text: mixed languages, sarcasm, missing context, or two equally severe problems.

## Topics with examples and subtopics

| Topic | Subtopics (issue keys) | Example (dev set) → labels |
|---|---|---|
| `access` | `login_failure`, `account_locked_hacked`, `signup` | "Would not let me in on Spotify 😡" → access / complaint / sev 4 / login_failure |
| `usability` | `ads_interruptions`, `ui_redesign`, `controls_navigation`, `queue_playlist_mgmt`, `notifications_widgets` | "Ads keep replaying and it's the same two!? …" → usability / complaint / sev 3 / ads_interruptions |
| `playback` | `crash_wont_open`, `stops_skips_glitches`, `connectivity`, `audio_quality`, `background_play`, `battery_resource` | "Buggy, really buggy. App just crashes randomly all the time…" → playback / complaint / sev 3 / crash_wont_open |
| `downloads` | `offline_needs_internet`, `downloads_disappear`, `download_fails` | "Why does it need internet to play downloaded songs? …" → downloads / complaint / sev 4 / offline_needs_internet |
| `catalog` | `missing_content`, `search`, `recommendations`, `lyrics`, `podcasts` | "It would be nice to give Bhojpuri songs here also. And ads appear minimal" → catalog / request / sev 1 / missing_content |
| `billing` | `price`, `premium_only_controls`, `charges_refunds`, `subscription_activation` | "…forcing you to pay premium for basic things like just listening to music." → billing / complaint / sev 3 / premium_only_controls |
| `support` | `no_response`, `unhelpful_response`, `positive_support` | "so i was having problem with logging but Spotify team contact asap !! great response from the devs" → support / praise / sev 1 / positive_support ⚖️ |
| `other` | `general_negative`, `general_positive`, `unrelated` | "Hate this app" → other / complaint / sev 2 / general_negative |

## Severity examples

| Sev | Example (dev set) | Why |
|---|---|---|
| 1 | "Great app, It has all the songs I like." | Praise, no problem. Topic `catalog`, because the specific praised feature is the song selection. |
| 1 | "I want the Spotify Wrapped again" | Pure feature request. Intent `request`. |
| 2 | "Absolutely hate the new front page. Ugly, difficult, plays music out loud for no reason." | Dislike of a redesign. ⚖️ "plays music out loud for no reason" could argue for 3. |
| 2 | "Nice app … but the subscribtion is way to expensive" | Price complaint, no functional loss. billing / complaint. |
| 3 | "It's great, but it keeps opening multiple mini-player notifications … unable to remove unless I completely restart my phone." | A degraded function with a workaround. usability / notifications_widgets. |
| 4 | "Why does it constantly need internet to open up downloaded playlists? …" | Offline listening, a core task, is blocked. |
| 5 | "Crazy thieve company I feel regret to use it" → **not 5** | Accusation without an explicit financial harm, so sev 2 with needs_review. A real 5 needs an explicit unauthorized charge, privacy exposure or lost data. |

## Boundary calls for Matt to confirm ⚖️

1. **Free-tier limits** ("can't skip songs without premium", forced shuffle): `billing / premium_only_controls`, because the contract says explicitly premium-only controls are billing. Ads go to `usability / ads_interruptions`.
2. **Positive support stories** (login problem solved by support): topic `support`, intent `praise`, sev 1. The alternative is `access`, sev 1.
3. **"worst update ever" with no detail**: `other / complaint / sev 2`. Don't infer a defect.
4. **"Boycott"** alone: `other / unclear / sev 1`, following the contract's bare-boycott rule.
5. **Non-English text** (e.g. "Thik thak hi hai", "Sb kuch to band kr diya hai"): classify when the meaning is clear enough. Otherwise `unclear` with `needs_review=true`. The text is never translated in the evidence quote.
6. **"It is the best App" with 1 star**: classify the text (praise). Stars are metadata only.
