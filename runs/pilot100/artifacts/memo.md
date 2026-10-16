# Put next quarter's effort into billing_support: the Premium-gated controls issue ranks first and billing and support together carry the second-largest complaint load.

*Decision memo generated 2026-10-16T21:36:37.756772Z by `claude-sonnet-5-5` from saved aggregates of run `pilot100`; numbers in parentheses are claim IDs from `claims.csv`. Status: **validated**.*

## Scope

- 100 source reviews; 100 classified, 0 quarantined (none), 0 pending.
- Intent mix: cancellation 6, complaint 45, request 3, praise 41, unclear 5. needs_review flagged on 16.0% of labelled records.
- Complaint and cancellation records grouped into 17 issues (priority_score = severity_sum = complaint_count x mean_severity; sort score desc, issue_id asc).

## Where the complaints are

| focus area | topics | complaints | severity sum | mean severity | share |
|---|---|---|---|---|---|
| access | access | 2 | 8 | 4.000000 | 0.0392 |
| usability | usability | 11 | 28 | 2.545455 | 0.2157 |
| playback | playback | 5 | 16 | 3.200000 | 0.098 |
| billing_support | billing, support | 10 | 29 | 2.900000 | 0.1961 |

## Situation

The run labelled every review in the sample, and complaints are the largest intent group, so the ranking reflects a broad pattern of dissatisfaction rather than a few outliers.
Per-topic complaint load puts usability first and billing_support second, with playback and access far behind. The ranking weights severity as well as volume, which is why the order of issues differs from the order of topics.
The top-ranked issue, billing.premium_only_controls, has 10 (C1) complaints and a priority score of 29 (C4). The second-ranked issue, other.general_negative, has 13 (C5) complaints but a lower score of 26 (C8) because its mean severity is only 2.000000 (C7).
The third-ranked issue, usability.ads_interruptions, scores 18 (C12) from 7 (C9) complaints at a mean severity of 2.571429 (C11). Access and playback issues each score 8 (C16) and 8 (C20), with high severity per review but very few complaints.

## Top issues (baseline ranking)

| rank | issue | name | complaints | severity sum | mean severity | priority |
|---|---|---|---|---|---|---|
| 1 | `billing.premium_only_controls` | Basic music controls locked behind Premium | 10 | 29 | 2.900000 | 29 |
| 2 | `other.general_negative` | Recent update made app feel useless | 13 | 26 | 2.000000 | 26 |
| 3 | `usability.ads_interruptions` | Frequent ads interrupt listening on free tier | 7 | 18 | 2.571429 | 18 |
| 4 | `access.login_failure` | Password rejected and account not accessible | 2 | 8 | 4.000000 | 8 |
| 5 | `playback.crash_wont_open` | App crashes or stalls on loading screen | 2 | 8 | 4.000000 | 8 |

**`billing.premium_only_controls`** (Basic music controls locked behind Premium): It is the top-ranked issue, with 10 (C1) complaints, a severity sum of 29 (C2), and a mean severity of 2.900000 (C3). Customers say that picking songs, playing next, and skipping now require Premium, and that basic listening feels paywalled after an update.
  - review `a78d831a-69f4-428a-9235-cfdd9775c509`: "This app is killing it self and forcing you to pay premium for basic things like just listening to music."
  - review `d146397f-4a94-4980-be00-ae9212eca3a7`: "This was fine till the last update, now you can't even pick a certain song without Spotify premium, and now you can only skip 6 songs, like please just let the songs fit my mood!"
  - review `ad730d1a-829a-4dc4-9561-7e1cd07e2c30`: "Why it requires premium just to play next music / to choose music ??"

**`other.general_negative`** (Recent update made app feel useless): It has the most complaints, 13 (C5), but a low mean severity of 2.000000 (C7), giving a score of 26 (C8). Reviewers describe a recent update that removed basic player features. Some of this may overlap with the Premium-gating issue, though the data do not show how much.
  - review `45c561b9-cc47-4d80-95d3-f0d20bc84af3`: "The update made the app useless ...."
  - review `b47c203f-366e-4409-922d-cd52aa8bbef6`: "Used to love the app but recent update is very disappointing bye Spotify"
  - review `7084ced1-0428-4093-9328-442f74719b4f`: "I am using Spotify from past two years From last update they removed basic features of music player"

**`usability.ads_interruptions`** (Frequent ads interrupt listening on free tier): The third-ranked issue has 7 (C9) complaints and a score of 18 (C12). Free-tier users report ads every one or two songs, and one says they are uninstalling. It is the main driver of the usability topic's complaint load.
  - review `3e8bdc92-4934-457e-85cc-8b9d14bf51c0`: "Decent,just let me have a solid 4-5 songs without an ad bro, it's always every 1 or 2 song then instant ads, that's all thanks"
  - review `c2738a4f-e57c-46bc-a4ad-8ec5a4b5d5cd`: "Soo trash wayy to many ads I don't want premium but too much ads"
  - review `035213ba-b1b9-411c-b028-70296e5f0e73`: "I m using this app from 5 to 6 year but now m uninstald this app cz his premium adds are everywhere now ."

## Recommendation: billing_support

The highest-priority issue, billing.premium_only_controls, sits in this area with a score of 29 (C4), ahead of every other named issue. Its 10 (C1) complaints at a mean severity of 2.900000 (C3) make it both frequent and fairly severe. Billing and support together hold the second-largest topic complaint load, close behind usability. Reviewers tie the complaint to a recent update, and the same update-and-removed-features theme appears in the second-ranked other.general_negative issue, so work on how paywalled controls are presented and communicated may address part of that complaint too. This is an argument from complaint patterns, not from measured revenue or churn effects.

Claims cited: C1, C3, C4, C5, C8.

## Alternatives

- **usability**: It has the largest topic complaint load, driven by usability.ads_interruptions, which scores 18 (C12) from 7 (C9) complaints, and reviewers say ad frequency is pushing them to uninstall. *Why not now:* Its top issue ranks third, below the Premium-gating issue at 29 (C4), and ad load is closely tied to the free-versus-Premium model, so it is best handled alongside the billing_support work rather than ahead of it.
- **playback**: playback.crash_wont_open has a mean severity of 4.000000 (C19), and a crash or a stuck loading screen leaves a user unable to use the app at all. *Why not now:* It has only 2 (C17) complaints and a score of 8 (C20), far below the leading issues, so the evidence does not support it as the quarter's main focus. It may still merit a targeted fix.
- **access**: access.login_failure has a mean severity of 4.000000 (C15), the highest of any ranked issue, because users cannot get into their accounts. *Why not now:* It has only 2 (C13) complaints and a score of 8 (C16), which is too small a base to justify a quarter-long focus. Monitor it and handle it as a bug fix.

## Limitations

- Reviews are self-selected public text, so they over-represent unhappy and highly motivated users and cannot be read as the whole user base.
- Complaint counts are small for several issues, so rankings among the lower issues are unstable and a few reviews could change them.
- Severity is a classifier-assigned score, and some reviews were flagged for human review, so individual labels may be wrong.
- The data show no revenue, churn, or user-count information, so recommendations are based only on complaint frequency and severity.
- The other.general_negative issue is a catch-all and may overlap with specific issues such as Premium-gated controls.

## Claims appendix

| claim | issue | metric | value |
|---|---|---|---|
| C1 | `billing.premium_only_controls` | complaint_count | 10 |
| C2 | `billing.premium_only_controls` | severity_sum | 29 |
| C3 | `billing.premium_only_controls` | mean_severity | 2.900000 |
| C4 | `billing.premium_only_controls` | priority_score | 29 |
| C5 | `other.general_negative` | complaint_count | 13 |
| C6 | `other.general_negative` | severity_sum | 26 |
| C7 | `other.general_negative` | mean_severity | 2.000000 |
| C8 | `other.general_negative` | priority_score | 26 |
| C9 | `usability.ads_interruptions` | complaint_count | 7 |
| C10 | `usability.ads_interruptions` | severity_sum | 18 |
| C11 | `usability.ads_interruptions` | mean_severity | 2.571429 |
| C12 | `usability.ads_interruptions` | priority_score | 18 |
| C13 | `access.login_failure` | complaint_count | 2 |
| C14 | `access.login_failure` | severity_sum | 8 |
| C15 | `access.login_failure` | mean_severity | 4.000000 |
| C16 | `access.login_failure` | priority_score | 8 |
| C17 | `playback.crash_wont_open` | complaint_count | 2 |
| C18 | `playback.crash_wont_open` | severity_sum | 8 |
| C19 | `playback.crash_wont_open` | mean_severity | 4.000000 |
| C20 | `playback.crash_wont_open` | priority_score | 8 |
| C21 | `usability.ui_redesign` | complaint_count | 3 |
| C22 | `usability.ui_redesign` | severity_sum | 7 |
| C23 | `usability.ui_redesign` | mean_severity | 2.333333 |
| C24 | `usability.ui_redesign` | priority_score | 7 |
| C25 | `catalog.lyrics` | complaint_count | 2 |
| C26 | `catalog.lyrics` | severity_sum | 4 |
| C27 | `catalog.lyrics` | mean_severity | 2.000000 |
| C28 | `catalog.lyrics` | priority_score | 4 |
| C29 | `catalog.missing_content` | complaint_count | 2 |
| C30 | `catalog.missing_content` | severity_sum | 4 |
| C31 | `catalog.missing_content` | mean_severity | 2.000000 |
| C32 | `catalog.missing_content` | priority_score | 4 |
| C33 | `downloads.offline_needs_internet` | complaint_count | 1 |
| C34 | `downloads.offline_needs_internet` | severity_sum | 4 |
| C35 | `downloads.offline_needs_internet` | mean_severity | 4.000000 |
| C36 | `downloads.offline_needs_internet` | priority_score | 4 |
| C37 | `other.unrelated` | complaint_count | 2 |
| C38 | `other.unrelated` | severity_sum | 4 |
| C39 | `other.unrelated` | mean_severity | 2.000000 |
| C40 | `other.unrelated` | priority_score | 4 |
