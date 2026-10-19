# Put next quarter's effort on usability: it carries the largest complaint load, and its top named issue, ads interrupting free listeners, is a defined, fixable problem

*Decision memo generated 2026-10-16T21:22:21.928306Z by `claude-sonnet-5-5` from saved aggregates of run `pilot500`; numbers in parentheses are claim IDs from `claims.csv`. Status: **validated**.*

## Scope

- 500 source reviews; 500 classified, 0 quarantined (none), 0 pending.
- Intent mix: cancellation 19, complaint 219, request 12, praise 219, unclear 31. needs_review flagged on 13.6% of labelled records.
- Complaint and cancellation records grouped into 22 issues (priority_score = severity_sum = complaint_count x mean_severity; sort score desc, issue_id asc).

## Where the complaints are

| focus area | topics | complaints | severity sum | mean severity | share |
|---|---|---|---|---|---|
| access | access | 10 | 39 | 3.900000 | 0.042 |
| usability | usability | 53 | 134 | 2.528302 | 0.2227 |
| playback | playback | 30 | 103 | 3.433333 | 0.1261 |
| billing_support | billing, support | 47 | 132 | 2.808511 | 0.1975 |

## Situation

All reviews in the run were classified. Of the labelled reviews, complaints and praise are the two largest intents, so the negative signal is substantial but not overwhelming.
The top-ranked issue, other.general_negative, scores 133 (C4) from 66 (C1) complaints at a mean severity of 2.015152 (C3). It is a catch-all for post-update disappointment and has no single fixable component, so it is a poor target for a focused team.
The second-ranked issue, billing.premium_only_controls, scores 110 (C8) from 40 (C5) complaints at a mean severity of 2.750000 (C7). Customers object to song selection, skipping and next-track controls requiring Premium.
The third-ranked issue, usability.ads_interruptions, scores 74 (C12) from 29 (C9) complaints at a mean severity of 2.551724 (C11).
Playback and access issues are less frequent but more severe per complaint: playback.stops_skips_glitches has a mean severity of 3.461538 (C15) and access.login_failure has 3.777778 (C19).

## Top issues (baseline ranking)

| rank | issue | name | complaints | severity sum | mean severity | priority |
|---|---|---|---|---|---|---|
| 1 | `other.general_negative` | Recent update removed basic features and users are unhappy | 66 | 133 | 2.015152 | 133 |
| 2 | `billing.premium_only_controls` | Basic playback controls locked behind Premium paywall | 40 | 110 | 2.750000 | 110 |
| 3 | `usability.ads_interruptions` | Frequent ads interrupt listening for free users | 29 | 74 | 2.551724 | 74 |
| 4 | `playback.stops_skips_glitches` | Music stops halfway and voice assistant fails to play | 13 | 45 | 3.461538 | 45 |
| 5 | `access.login_failure` | Cannot log in and app shows false no-internet error | 9 | 34 | 3.777778 | 34 |

**`other.general_negative`** (Recent update removed basic features and users are unhappy): It tops the ranking at 133 (C4) priority from 66 (C1) complaints, driven by customers saying a recent update removed basic features. It is diffuse and low in per-complaint severity (2.015152 (C3)), so it needs breaking down into specific features before it can be assigned to a team.
  - review `45c561b9-cc47-4d80-95d3-f0d20bc84af3`: "The update made the app useless ...."
  - review `b47c203f-366e-4409-922d-cd52aa8bbef6`: "Used to love the app but recent update is very disappointing bye Spotify"
  - review `7084ced1-0428-4093-9328-442f74719b4f`: "I am using Spotify from past two years From last update they removed basic features of music player"

**`billing.premium_only_controls`** (Basic playback controls locked behind Premium paywall): Second-ranked at 110 (C8) priority from 40 (C5) complaints with mean severity 2.750000 (C7). Customers describe basic controls as locked behind Premium after an update. It is largely a monetisation and policy choice rather than a defect.
  - review `a78d831a-69f4-428a-9235-cfdd9775c509`: "This app is killing it self and forcing you to pay premium for basic things like just listening to music."
  - review `d146397f-4a94-4980-be00-ae9212eca3a7`: "This was fine till the last update, now you can't even pick a certain song without Spotify premium, and now you can only skip 6 songs, like please just let the songs fit my mood!"
  - review `ad730d1a-829a-4dc4-9561-7e1cd07e2c30`: "Why it requires premium just to play next music / to choose music ??"

**`usability.ads_interruptions`** (Frequent ads interrupt listening for free users): Third-ranked at 74 (C12) priority from 29 (C9) complaints at mean severity 2.551724 (C11). Reviewers cite ads after every song or two and say they do not want to be pushed into Premium. It is the main issue inside the usability area, which has the largest complaint load of the four focus areas.
  - review `3e8bdc92-4934-457e-85cc-8b9d14bf51c0`: "Decent,just let me have a solid 4-5 songs without an ad bro, it's always every 1 or 2 song then instant ads, that's all thanks"
  - review `c2738a4f-e57c-46bc-a4ad-8ec5a4b5d5cd`: "Soo trash wayy to many ads I don't want premium but too much ads"
  - review `035213ba-b1b9-411c-b028-70296e5f0e73`: "I m using this app from 5 to 6 year but now m uninstald this app cz his premium adds are everywhere now ."

**`playback.stops_skips_glitches`** (Music stops halfway and voice assistant fails to play): Fourth-ranked at 45 (C16) priority from 13 (C13) complaints, but with a high mean severity of 3.461538 (C15). Reviewers report music stopping mid-song, not resuming, and voice-assistant playback failing.
  - review `9c9757da-6b99-4c95-a0e7-0661ee858027`: "There is some bugs like music adjustment doesn't work Perporly plz do something about this bug"
  - review `46ff0c74-5e86-4e5b-b4cd-36201aab0f9e`: "I am unable to use my Google assistant on the app.it says playing your Spotify playlist but do not play the songs"
  - review `6c257eba-3dca-49f6-b7f0-4c4484d81e26`: "Keep stopping halfway while playing music and it dun go back to where they stop and start playing a new song for you."

**`access.login_failure`** (Cannot log in and app shows false no-internet error): Fifth-ranked at 34 (C20) priority from 9 (C17) complaints, with the highest mean severity of the named issues at 3.777778 (C19). Affected customers cannot reach their account at all.
  - review `12efd15d-4d4f-4a71-8e71-69d03b6f983a`: "I can't login to the app, it keep saying that there's no internet connection, whereas everything else on my phone is connected to the internet."
  - review `32fb340f-4f9f-4551-8dae-755221e58d6a`: "It not letting me into my account and there are to many ads"

## Recommendation: usability

Usability has the largest share of complaints of any focus area, ahead of billing_support, playback and access. Its named issue, usability.ads_interruptions, ranks third at 74 (C12) priority from 29 (C9) complaints. Unlike the first-ranked other.general_negative, which is too diffuse to assign, ad load and interruption frequency are concrete product behaviours a team can measure and tune. Reviewers say the ad frequency itself pushes them away, for example 'every 1 or 2 song then instant ads', and some report uninstalling. Work here should start with ad cadence for free users and extend to the update-related feature complaints that overlap with the diffuse top issue.

Claims cited: C9, C11, C12, C1, C4.

## Alternatives

- **billing_support**: billing.premium_only_controls ranks second at 110 (C8) priority from 40 (C5) complaints, and billing and support combined carry the second-largest complaint load among the four areas. *Why not now:* The complaints are about which controls sit behind Premium, which is a pricing and packaging decision rather than a defect. A product team cannot fix it without a commercial policy change, and the data gives no evidence on revenue impact.
- **playback**: playback.stops_skips_glitches has a high mean severity of 3.461538 (C15), so the complaints that exist are serious, and the failures are real bugs with clear fixes. *Why not now:* The issue has far fewer complaints (13 (C13)) and a lower priority score (45 (C16)) than the top three issues, so fixing it addresses a smaller share of dissatisfaction.
- **access**: access.login_failure has the highest mean severity (3.777778 (C19)) among the named issues, and a customer who cannot log in cannot use the product at all. *Why not now:* Only 9 (C17) complaints put it fifth by priority score (34 (C20)), and access has the smallest complaint load of the four areas. It is better handled as a targeted bug fix than as a quarter-long focus.

## Limitations

- Reviews are self-selected public text, so they over-represent frustrated and highly motivated users and cannot be read as the full customer base.
- Severity scores come from automated classification, and a meaningful fraction of records were flagged as needing review, so individual labels may be wrong.
- The data does not support claims about churn, revenue or user counts, and complaint counts are not adjusted for how many users each issue affects.
- other.general_negative is a catch-all category, so its rank reflects grouped dissatisfaction rather than one identifiable problem.
- The evidence pack is a small set of verbatim quotes per issue and may not represent every complaint in that issue.

## Claims appendix

| claim | issue | metric | value |
|---|---|---|---|
| C1 | `other.general_negative` | complaint_count | 66 |
| C2 | `other.general_negative` | severity_sum | 133 |
| C3 | `other.general_negative` | mean_severity | 2.015152 |
| C4 | `other.general_negative` | priority_score | 133 |
| C5 | `billing.premium_only_controls` | complaint_count | 40 |
| C6 | `billing.premium_only_controls` | severity_sum | 110 |
| C7 | `billing.premium_only_controls` | mean_severity | 2.750000 |
| C8 | `billing.premium_only_controls` | priority_score | 110 |
| C9 | `usability.ads_interruptions` | complaint_count | 29 |
| C10 | `usability.ads_interruptions` | severity_sum | 74 |
| C11 | `usability.ads_interruptions` | mean_severity | 2.551724 |
| C12 | `usability.ads_interruptions` | priority_score | 74 |
| C13 | `playback.stops_skips_glitches` | complaint_count | 13 |
| C14 | `playback.stops_skips_glitches` | severity_sum | 45 |
| C15 | `playback.stops_skips_glitches` | mean_severity | 3.461538 |
| C16 | `playback.stops_skips_glitches` | priority_score | 45 |
| C17 | `access.login_failure` | complaint_count | 9 |
| C18 | `access.login_failure` | severity_sum | 34 |
| C19 | `access.login_failure` | mean_severity | 3.777778 |
| C20 | `access.login_failure` | priority_score | 34 |
| C21 | `playback.connectivity` | complaint_count | 10 |
| C22 | `playback.connectivity` | severity_sum | 34 |
| C23 | `playback.connectivity` | mean_severity | 3.400000 |
| C24 | `playback.connectivity` | priority_score | 34 |
| C25 | `usability.ui_redesign` | complaint_count | 12 |
| C26 | `usability.ui_redesign` | severity_sum | 27 |
| C27 | `usability.ui_redesign` | mean_severity | 2.250000 |
| C28 | `usability.ui_redesign` | priority_score | 27 |
| C29 | `playback.crash_wont_open` | complaint_count | 6 |
| C30 | `playback.crash_wont_open` | severity_sum | 21 |
| C31 | `playback.crash_wont_open` | mean_severity | 3.500000 |
| C32 | `playback.crash_wont_open` | priority_score | 21 |
| C33 | `billing.subscription_activation` | complaint_count | 6 |
| C34 | `billing.subscription_activation` | severity_sum | 20 |
| C35 | `billing.subscription_activation` | mean_severity | 3.333333 |
| C36 | `billing.subscription_activation` | priority_score | 20 |
| C37 | `catalog.missing_content` | complaint_count | 8 |
| C38 | `catalog.missing_content` | severity_sum | 19 |
| C39 | `catalog.missing_content` | mean_severity | 2.375000 |
| C40 | `catalog.missing_content` | priority_score | 19 |
