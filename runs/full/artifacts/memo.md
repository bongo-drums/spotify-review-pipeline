# Put next quarter's effort into usability: it carries the heaviest complaint load of the four areas and holds the third-ranked issue, ads interruptions.

*Decision memo generated 2026-10-19T22:49:17.650439Z by `claude-sonnet-5-5` from saved aggregates of run `full`; numbers in parentheses are claim IDs from `claims.csv`. Status: **validated**.*

## Scope

- 660,622 source reviews; 660,602 classified, 20 quarantined (empty_review_text: 13, fallback_invalid_record:evidence sentence 2 out of range 0..1 (claude-sonnet-5-5): 1, fallback_invalid_record:subtopic 'controls_navigation' not under topic 'playback' (claude-sonnet-5-5): 1, fallback_invalid_record:subtopic 'general_positive' not under topic 'catalog' (claude-sonnet-5-5): 2, fallback_invalid_record:subtopic 'offline_needs_internet' not under topic 'playback' (claude-sonnet-5-5): 1, refusal:bio (attempt 2): 2), 0 pending.
- Intent mix: cancellation 25,007, complaint 271,505, request 19,265, praise 290,644, unclear 54,181. needs_review flagged on 16.2% of labelled records.
- Complaint and cancellation records grouped into 32 issues (priority_score = severity_sum = complaint_count x mean_severity; sort score desc, issue_id asc).

## Where the complaints are

| focus area | topics | complaints | severity sum | mean severity | share |
|---|---|---|---|---|---|
| access | access | 11,164 | 43,087 | 3.859459 | 0.0377 |
| usability | usability | 67,674 | 168,167 | 2.484957 | 0.2282 |
| playback | playback | 35,291 | 111,766 | 3.166983 | 0.119 |
| billing_support | billing, support | 57,894 | 161,309 | 2.786282 | 0.1953 |

## Situation

The run labelled nearly all records, with only a handful quarantined, so the aggregates cover essentially the full review set.
Usability has the largest share of complaints among the four focus areas, ahead of billing_support, then playback, then access. Access is the smallest by volume but has the highest mean severity of the four.
The baseline ranking is led by other.general_negative, a catch-all of broad dissatisfaction that does not map to any one focus area. The second-ranked issue, billing.premium_only_controls, sits in billing_support. The third-ranked issue is usability.ads_interruptions.

## Top issues (baseline ranking)

| rank | issue | name | complaints | severity sum | mean severity | priority |
|---|---|---|---|---|---|---|
| 1 | `other.general_negative` | General complaints about Spotify's business tactics and app | 92441 | 187128 | 2.024297 | 187128 |
| 2 | `billing.premium_only_controls` | Key features locked behind a paid premium subscription | 46885 | 132463 | 2.825275 | 132463 |
| 3 | `usability.ads_interruptions` | Frequent ads interrupt listening for free users | 37000 | 89475 | 2.418243 | 89475 |
| 4 | `playback.stops_skips_glitches` | Playback gets stuck, plays wrong songs, or stutters | 19189 | 59626 | 3.107301 | 59626 |
| 5 | `access.login_failure` | App shows errors or will not open for login | 9651 | 37447 | 3.880116 | 37447 |

**`other.general_negative`** (General complaints about Spotify's business tactics and app): It tops the baseline ranking on volume (92441 (C1)) and priority score (187128 (C4)), but mean severity is the lowest of the five (2.024297 (C3)). It is broad dissatisfaction rather than a specific fault, so it gives product teams little to act on directly.
  - review `7c5bf637-f2d0-4453-a0b3-c86f45203ba7`: "I am fully disgusted with Spotify & the very cunning manipulation of the public with Spotifys way of attempting to get business."
  - review `6adc8bd8-9953-4c40-a345-b935aa322b83`: "It is youse for audio songs app but it is consume data like i see video in some app."
  - review `1c5465bb-b754-4fdc-8b51-ae9e6853981c`: "Wrost app ..."

**`billing.premium_only_controls`** (Key features locked behind a paid premium subscription): Reviewers object to features such as downloads and individual track choice sitting behind a paid tier. Complaint count is 46885 (C5) and priority score is 132463 (C8), with higher mean severity (2.825275 (C7)) than ads. It is the strongest single issue inside billing_support.
  - review `34a12e69-bdf1-4890-a426-13bed973ac77`: "I just want to download a song and I have to pay"
  - review `8b5826e0-569a-4f7d-9053-b95a4a2b2532`: "best music quality but not able to chose your songs individually without premium"
  - review `90a11b0f-aad7-45ba-bacc-088d39c0cf8a`: "A week ago I could now it isn't an option I have, everyone else with the link can join."

**`usability.ads_interruptions`** (Frequent ads interrupt listening for free users): Free-tier listening interrupted by ads draws 37000 (C9) complaints, for a priority score of 89475 (C12) at mean severity 2.418243 (C11). Reviewers describe ads after nearly every song and call it annoying; some also say premium is good, so the friction sits in the free experience.
  - review `6dbe91f5-31ef-4d58-b368-89d568c91456`: "If you want to hear 3 commercials for 1 song then this is the app for you how many billions of dollars do they need ?"
  - review `c71cea9c-0ba7-4cd6-bda3-03b043a6a6fb`: "It says that if u watch a short ad it would give u 30 mins of interrupted listing but it gives ad every time a song end and its kind of annoyin to be honest 1/10 alot of people font have the money to buy the premium."
  - review `a606e006-1a06-4fe7-8aab-52a66e6f33bc`: "I need music wherever I go whatever o do and Spotify is great for that but these days we get adds to frequently so it's a but annoying but premium is great and music quality is perfect"

**`playback.stops_skips_glitches`** (Playback gets stuck, plays wrong songs, or stutters): Stuck offline mode, wrong songs playing and Android stuttering are core-function failures. Priority score is 59626 (C16) on 19189 (C13) complaints, with mean severity (3.107301 (C15)) well above ads or premium-only controls.
  - review `82adc2a2-1626-4fb6-bf2b-f8396b3667ce`: "Stuck in offline mode won't let me do anything"
  - review `b3da207e-888d-40bd-bd5d-11f376f5eeda`: "Every time I play my favorite song, it plays another song and I hate it."
  - review `71c3a08a-ff3a-45a5-a797-088d6649caa3`: "The stuttering on Android devices hasn't been fixed!!!"

**`access.login_failure`** (App shows errors or will not open for login): Login errors and an app that will not open block use entirely, and this issue has the highest mean severity of the five (3.880116 (C19)). Volume is the smallest (9651 (C17)), giving a priority score of 37447 (C20).
  - review `470b836e-9027-4e6f-9673-c0aad1b03c0b`: "Shows an error every time I try to log in."
  - review `07a3e007-76df-45e7-98aa-72aa93781208`: "i can't open my account, I can't open Spotify."
  - review `3d9c548f-1c89-44f2-bc65-9fbde01fa6ab`: "I can't even open the app anymore."

## Recommendation: usability

Usability has the largest share of complaints of the four areas, and its ads issue is the highest-ranked issue that belongs to a single focus area and is not a catch-all or a pricing-model question: 37000 (C9) complaints and a priority score of 89475 (C12). Mean severity is moderate (2.418243 (C11)), so the case rests on breadth, not on severity. Reviewers describe the specific friction (ads after almost every song), which gives the team a concrete surface to work on. The top-ranked issue, other.general_negative (187128 (C4)), is too diffuse to assign.

Claims cited: C9, C11, C12, C4.

## Alternatives

- **billing_support**: It holds the second-ranked issue, billing.premium_only_controls, with a higher priority score (132463 (C8)) than ads (89475 (C12)) and a second-largest complaint share, so it is a close contender. *Why not now:* The complaints are largely about which features sit behind the paid tier, which is a pricing and packaging decision rather than a defect. It is a leadership call, not a product-effort workstream, and the review text cannot show how users would respond to changes.
- **playback**: Playback complaints are more severe (3.107301 (C15)) than ads (2.418243 (C11)) and describe failures of the core listening function. *Why not now:* Volume is lower (19189 (C13) complaints against 37000 (C9) for ads) and the priority score is lower (59626 (C16) against 89475 (C12)), so a quarter of effort reaches fewer complaints.
- **access**: Login failure has the highest mean severity (3.880116 (C19)), and an app that will not open blocks the user completely. *Why not now:* Access is the smallest area by complaint volume (9651 (C17) complaints) and the lowest priority score (37447 (C20)). It looks better suited to a targeted fix than to a quarter-long focus.

## Limitations

- Reviews are self-selected public text; they over-represent unhappy and highly motivated users and cannot be read as the whole user base.
- Severity and topic labels come from automated classification, and a sizable fraction of records was flagged for review, so individual labels may be wrong.
- The baseline ranking multiplies complaint count by mean severity and does not account for user reach, revenue, churn or engineering cost, none of which are in the data.
- The top-ranked issue, other.general_negative, is a catch-all category, so its rank reflects labelling breadth more than a specific fault.
- The evidence pack contains only a few quotes per issue and is illustrative, not a representative sample.

## Claims appendix

| claim | issue | metric | value |
|---|---|---|---|
| C1 | `other.general_negative` | complaint_count | 92441 |
| C2 | `other.general_negative` | severity_sum | 187128 |
| C3 | `other.general_negative` | mean_severity | 2.024297 |
| C4 | `other.general_negative` | priority_score | 187128 |
| C5 | `billing.premium_only_controls` | complaint_count | 46885 |
| C6 | `billing.premium_only_controls` | severity_sum | 132463 |
| C7 | `billing.premium_only_controls` | mean_severity | 2.825275 |
| C8 | `billing.premium_only_controls` | priority_score | 132463 |
| C9 | `usability.ads_interruptions` | complaint_count | 37000 |
| C10 | `usability.ads_interruptions` | severity_sum | 89475 |
| C11 | `usability.ads_interruptions` | mean_severity | 2.418243 |
| C12 | `usability.ads_interruptions` | priority_score | 89475 |
| C13 | `playback.stops_skips_glitches` | complaint_count | 19189 |
| C14 | `playback.stops_skips_glitches` | severity_sum | 59626 |
| C15 | `playback.stops_skips_glitches` | mean_severity | 3.107301 |
| C16 | `playback.stops_skips_glitches` | priority_score | 59626 |
| C17 | `access.login_failure` | complaint_count | 9651 |
| C18 | `access.login_failure` | severity_sum | 37447 |
| C19 | `access.login_failure` | mean_severity | 3.880116 |
| C20 | `access.login_failure` | priority_score | 37447 |
| C21 | `usability.controls_navigation` | complaint_count | 12586 |
| C22 | `usability.controls_navigation` | severity_sum | 34296 |
| C23 | `usability.controls_navigation` | mean_severity | 2.724932 |
| C24 | `usability.controls_navigation` | priority_score | 34296 |
| C25 | `playback.crash_wont_open` | complaint_count | 7529 |
| C26 | `playback.crash_wont_open` | severity_sum | 25825 |
| C27 | `playback.crash_wont_open` | mean_severity | 3.430070 |
| C28 | `playback.crash_wont_open` | priority_score | 25825 |
| C29 | `usability.queue_playlist_mgmt` | complaint_count | 8100 |
| C30 | `usability.queue_playlist_mgmt` | severity_sum | 21908 |
| C31 | `usability.queue_playlist_mgmt` | mean_severity | 2.704691 |
| C32 | `usability.queue_playlist_mgmt` | priority_score | 21908 |
| C33 | `catalog.missing_content` | complaint_count | 7949 |
| C34 | `catalog.missing_content` | severity_sum | 20790 |
| C35 | `catalog.missing_content` | mean_severity | 2.615423 |
| C36 | `catalog.missing_content` | priority_score | 20790 |
| C37 | `usability.ui_redesign` | complaint_count | 8614 |
| C38 | `usability.ui_redesign` | severity_sum | 19129 |
| C39 | `usability.ui_redesign` | mean_severity | 2.220687 |
| C40 | `usability.ui_redesign` | priority_score | 19129 |
