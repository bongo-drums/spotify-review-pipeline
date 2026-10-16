# Put next quarter's effort into usability: it carries the largest complaint load of any focus area, and ads interruptions is the top-ranked issue that sits inside it.

*Decision memo generated 2026-10-16T21:59:19.287460Z by `claude-sonnet-5-5` from saved aggregates of run `pilot10000`; numbers in parentheses are claim IDs from `claims.csv`. Status: **validated**.*

## Scope

- 10,000 source reviews; 9,999 classified, 1 quarantined (fallback_invalid_record:evidence sentence 3 out of range 0..0 (claude-sonnet-5-5): 1), 0 pending.
- Intent mix: cancellation 331, complaint 4,216, request 307, praise 4,332, unclear 813. needs_review flagged on 18.5% of labelled records.
- Complaint and cancellation records grouped into 31 issues (priority_score = severity_sum = complaint_count x mean_severity; sort score desc, issue_id asc).

## Where the complaints are

| focus area | topics | complaints | severity sum | mean severity | share |
|---|---|---|---|---|---|
| access | access | 177 | 675 | 3.813559 | 0.0389 |
| usability | usability | 1,082 | 2,669 | 2.466728 | 0.238 |
| playback | playback | 563 | 1,785 | 3.170515 | 0.1238 |
| billing_support | billing, support | 879 | 2,433 | 2.767918 | 0.1933 |

## Situation

Review complaints split across four focus areas; usability holds the largest share of complaints, followed by billing_support, then playback, with access the smallest.
The top-ranked issue overall, other.general_negative, is a catch-all about the app feeling worse after an update. It has no single focus area, so it cannot be assigned to a team directly.
Of the issues that map cleanly to a focus area, billing.premium_only_controls ranks second and usability.ads_interruptions ranks third by priority score. Access.login_failure has the highest mean severity of the five but the smallest volume.

## Top issues (baseline ranking)

| rank | issue | name | complaints | severity sum | mean severity | priority |
|---|---|---|---|---|---|---|
| 1 | `other.general_negative` | App feels worse and less useful after recent update | 1390 | 2828 | 2.034532 | 2828 |
| 2 | `billing.premium_only_controls` | Basic music controls locked behind Premium paywall | 712 | 2016 | 2.831461 | 2016 |
| 3 | `usability.ads_interruptions` | Frequent ads interrupt listening for free users | 586 | 1397 | 2.383959 | 1397 |
| 4 | `playback.stops_skips_glitches` | Music stops randomly or skips during playback | 319 | 987 | 3.094044 | 987 |
| 5 | `access.login_failure` | Cannot log in, app reports false no-internet error | 155 | 594 | 3.832258 | 594 |

**`other.general_negative`** (App feels worse and less useful after recent update): Highest priority score at 2828 (C4), driven by volume (1390 (C1) complaints) rather than severity (mean 2.034532 (C3)). Customers tie it to recent updates, but the label is too broad to act on without further triage.
  - review `45c561b9-cc47-4d80-95d3-f0d20bc84af3`: "The update made the app useless ...."
  - review `b47c203f-366e-4409-922d-cd52aa8bbef6`: "Used to love the app but recent update is very disappointing bye Spotify"
  - review `9c9757da-6b99-4c95-a0e7-0661ee858027`: "There is some bugs like music adjustment doesn't work Perporly plz do something about this bug"

**`billing.premium_only_controls`** (Basic music controls locked behind Premium paywall): Second-ranked at 2016 (C8), with 712 (C5) complaints at mean severity 2.831461 (C7). Customers describe basic controls such as choosing a song, playing the next track and skipping as locked behind Premium.
  - review `a78d831a-69f4-428a-9235-cfdd9775c509`: "This app is killing it self and forcing you to pay premium for basic things like just listening to music."
  - review `d146397f-4a94-4980-be00-ae9212eca3a7`: "This was fine till the last update, now you can't even pick a certain song without Spotify premium, and now you can only skip 6 songs, like please just let the songs fit my mood!"
  - review `ad730d1a-829a-4dc4-9561-7e1cd07e2c30`: "Why it requires premium just to play next music / to choose music ??"

**`usability.ads_interruptions`** (Frequent ads interrupt listening for free users): Third-ranked at 1397 (C12) with 586 (C9) complaints at mean severity 2.383959 (C11). Reviewers report ads every one or two songs, and one says they are uninstalling over it.
  - review `3e8bdc92-4934-457e-85cc-8b9d14bf51c0`: "Decent,just let me have a solid 4-5 songs without an ad bro, it's always every 1 or 2 song then instant ads, that's all thanks"
  - review `c2738a4f-e57c-46bc-a4ad-8ec5a4b5d5cd`: "Soo trash wayy to many ads I don't want premium but too much ads"
  - review `035213ba-b1b9-411c-b028-70296e5f0e73`: "I m using this app from 5 to 6 year but now m uninstald this app cz his premium adds are everywhere now ."

**`playback.stops_skips_glitches`** (Music stops randomly or skips during playback): Fourth-ranked at 987 (C16) with 319 (C13) complaints at mean severity 3.094044 (C15). Reviewers say music stops mid-track and does not resume, even on a strong connection.
  - review `6c257eba-3dca-49f6-b7f0-4c4484d81e26`: "Keep stopping halfway while playing music and it dun go back to where they stop and start playing a new song for you."
  - review `179d79f7-d052-490f-a9d6-f97525b32642`: "Love Spotify, but since I got my new phone, it keeps randomly stopping, like it would with no Internet, but I have full bars."

**`access.login_failure`** (Cannot log in, app reports false no-internet error): Fifth-ranked at 594 (C20) from 155 (C17) complaints, but with the highest mean severity of the five (3.832258 (C19)). Reviewers cannot log in and get a false no-internet error while other apps work.
  - review `12efd15d-4d4f-4a71-8e71-69d03b6f983a`: "I can't login to the app, it keep saying that there's no internet connection, whereas everything else on my phone is connected to the internet."
  - review `c64af4d8-ac17-48fe-ae38-fd54b41b16b1`: "App says no internet connection available, but clearly I do otherwise how else did would I have downloaded the update?"

## Recommendation: usability

Usability has the largest complaint load of the four areas, and its main named issue, usability.ads_interruptions, is the third-ranked issue overall at 1397 (C12) from 586 (C9) complaints. Among the issues that map to a single team, it is the second-largest after billing.premium_only_controls (2016 (C8)), and the quotes describe ad frequency specifically (ads after every one or two songs), which is a concrete, testable thing to change. Its mean severity (2.383959 (C11)) is lower than playback or access, so the case rests on volume, not on how badly each user is hurt.

Claims cited: C9, C11, C12, C8.

## Alternatives

- **billing_support**: billing.premium_only_controls is the second-ranked issue at 2016 (C8) with mean severity 2.831461 (C7), higher than the ads issue. The billing_support area has the second-largest complaint load. *Why not now:* The complaints are about which features sit behind Premium, which is a packaging and pricing decision rather than a defect, and the reviews give no evidence on how changing it would affect the free-to-paid relationship. Ads and the paywall are also entangled in the quotes, so the usability work can proceed and inform that decision.
- **playback**: playback.stops_skips_glitches is a real defect with a clear symptom, music stopping midway on a good connection, and a mean severity (3.094044 (C15)) well above the ads issue. *Why not now:* Its volume is much smaller (319 (C13) complaints against 586 (C9) for ads), and playback's overall complaint load is well below usability's.
- **access**: access.login_failure has the highest mean severity (3.832258 (C19)), and the false no-internet error blocks users from the app entirely. *Why not now:* It has the smallest volume (155 (C17) complaints) and the lowest priority score of the five (594 (C20)); access is the smallest area by complaint load. It is a good candidate for a targeted bug fix rather than a quarter-long focus.

## Limitations

- Reviews are self-selected public text, so they over-represent people motivated to complain and are not a measure of the whole user base.
- The top-ranked issue, other.general_negative, is a catch-all and could hide problems from several focus areas; it is not attributed to any of them here.
- One record was quarantined and a share of labels are flagged for review, so classifications carry some error.
- Priority score multiplies volume by severity, so a high-volume, low-severity issue can outrank a rarer but more damaging one, as login failure shows.
- The data contain no revenue, churn or user counts, so this memo cannot size business impact.

## Claims appendix

| claim | issue | metric | value |
|---|---|---|---|
| C1 | `other.general_negative` | complaint_count | 1390 |
| C2 | `other.general_negative` | severity_sum | 2828 |
| C3 | `other.general_negative` | mean_severity | 2.034532 |
| C4 | `other.general_negative` | priority_score | 2828 |
| C5 | `billing.premium_only_controls` | complaint_count | 712 |
| C6 | `billing.premium_only_controls` | severity_sum | 2016 |
| C7 | `billing.premium_only_controls` | mean_severity | 2.831461 |
| C8 | `billing.premium_only_controls` | priority_score | 2016 |
| C9 | `usability.ads_interruptions` | complaint_count | 586 |
| C10 | `usability.ads_interruptions` | severity_sum | 1397 |
| C11 | `usability.ads_interruptions` | mean_severity | 2.383959 |
| C12 | `usability.ads_interruptions` | priority_score | 1397 |
| C13 | `playback.stops_skips_glitches` | complaint_count | 319 |
| C14 | `playback.stops_skips_glitches` | severity_sum | 987 |
| C15 | `playback.stops_skips_glitches` | mean_severity | 3.094044 |
| C16 | `playback.stops_skips_glitches` | priority_score | 987 |
| C17 | `access.login_failure` | complaint_count | 155 |
| C18 | `access.login_failure` | severity_sum | 594 |
| C19 | `access.login_failure` | mean_severity | 3.832258 |
| C20 | `access.login_failure` | priority_score | 594 |
| C21 | `usability.controls_navigation` | complaint_count | 205 |
| C22 | `usability.controls_navigation` | severity_sum | 564 |
| C23 | `usability.controls_navigation` | mean_severity | 2.751220 |
| C24 | `usability.controls_navigation` | priority_score | 564 |
| C25 | `playback.crash_wont_open` | complaint_count | 115 |
| C26 | `playback.crash_wont_open` | severity_sum | 398 |
| C27 | `playback.crash_wont_open` | mean_severity | 3.460870 |
| C28 | `playback.crash_wont_open` | priority_score | 398 |
| C29 | `usability.ui_redesign` | complaint_count | 157 |
| C30 | `usability.ui_redesign` | severity_sum | 361 |
| C31 | `usability.ui_redesign` | mean_severity | 2.299363 |
| C32 | `usability.ui_redesign` | priority_score | 361 |
| C33 | `catalog.missing_content` | complaint_count | 114 |
| C34 | `catalog.missing_content` | severity_sum | 298 |
| C35 | `catalog.missing_content` | mean_severity | 2.614035 |
| C36 | `catalog.missing_content` | priority_score | 298 |
| C37 | `usability.queue_playlist_mgmt` | complaint_count | 112 |
| C38 | `usability.queue_playlist_mgmt` | severity_sum | 293 |
| C39 | `usability.queue_playlist_mgmt` | mean_severity | 2.616071 |
| C40 | `usability.queue_playlist_mgmt` | priority_score | 293 |
