# Where the next quarter of product effort should go

> **Draft written by Claude in Matt's voice, for Matt to edit before submission.** Every number below is a claim from
> `runs/full/artifacts/claims.csv` (claim ID in parentheses) or a code-computed aggregate from
> `runs/full/artifacts/aggregates.json`. The model-generated memo this is based on is
> `runs/full/artifacts/memo.md`; the dashboard shows the same figures. Delete this note once reviewed.

**Recommendation: put the quarter into usability, with the ad experience for free listeners as the headline project,
and fund one playback reliability fix alongside it.**

## What the data says

We classified 660,602 of the 660,622 reviews in the 18-month window (20 quarantined: 13 empty texts and 7 the
models could not label validly twice). 271,505 reviews are complaints and 25,007 are explicit cancellations;
together they form the 296,512 records that the ranking counts. 290,644 reviews are praise, so the corpus is not a
complaints inbox, which makes the complaint patterns more meaningful, not less.

By focus area, usability carries 67,674 complaints (22.8% of all complaint and cancellation records), billing and
support together 57,894 (19.5%), playback 35,291 (11.9%) and access 11,164 (3.8%). Severity runs the other way:
access complaints average 3.86 on the shared 1 to 5 scale, playback 3.17, billing and support 2.79, usability 2.48.

The baseline ranking (priority = complaint count × mean severity) puts five issues far ahead of the rest:

| rank | issue | complaints | mean severity | priority |
|---|---|---|---|---|
| 1 | `other.general_negative`, general dissatisfaction with no specific fault | 92,441 (C1) | 2.024297 (C3) | 187,128 (C4) |
| 2 | `billing.premium_only_controls`, basic controls locked behind Premium | 46,885 (C5) | 2.825275 (C7) | 132,463 (C8) |
| 3 | `usability.ads_interruptions`, ads after nearly every song | 37,000 (C9) | 2.418243 (C11) | 89,475 (C12) |
| 4 | `playback.stops_skips_glitches`, playback stuck, wrong song, stutter | 19,189 (C13) | 3.107301 (C15) | 59,626 (C16) |
| 5 | `access.login_failure`, cannot log in or open the app | 9,651 (C17) | 3.880116 (C19) | 37,447 (C20) |

## Why usability, and not billing

The top-ranked issue is a catch-all. "Worst update ever" with no detail is counted as `other` by the shared
definitions, so it tells us people are unhappy but not what to build. Among issues a team can act on, the
premium-only-controls issue (C8) outranks ads (C12), and it sits in billing. I still recommend usability, for
three reasons.

1. **Usability is the larger pool.** Its area total (67,674 complaints) exceeds billing and support combined
   (57,894), and its issues are concrete: ad frequency, controls and navigation, queue and playlist management,
   and the redesign.
2. **The two top actionable issues are the same experience seen from two sides.** Reviewers who say "can't pick a
   song without Premium" and reviewers who say "an ad every song" are both describing the free tier. Ad frequency
   is a product lever (frequency caps, ad-free sessions after a video ad that actually work); the paywall is a
   pricing decision. The quarter should go to the lever product can pull.
3. **The golden set shows how thin the billing/usability boundary is.** In my own labels I put free-tier limits
   under playback; the shared definitions put them under billing. A different, equally defensible reading moves
   `billing.premium_only_controls` into usability and makes the usability area larger still. The recommendation
   does not depend on which side of that line the issue lands.

## What I would not do this quarter, and why

- **Billing and support.** Changing what Premium gates is a revenue decision with effects outside this dataset.
  The reviews show the friction (C5, C8) but not the churn or revenue trade-off, so I would hand the evidence to
  pricing rather than spend product's quarter on it.
- **Playback.** Mean severity is high (C15) and `playback.stops_skips_glitches` is a core-function failure, but the
  volume is about half of ads (C13 vs C9). I would fund one targeted reliability fix for the stuck-offline and
  wrong-song reports and track whether the count moves, not make it the quarter's theme.
- **Access.** Login failures are the most severe issue per review (C19) but the smallest by far (C17). This is a bug
  queue, not a quarter.

## Limitations

- Reviews are self-selected public text; counts are complaints, not users, and say nothing about revenue or churn.
- Labels come from a classifier. A blind re-check of 4,842 texts agreed on topic 84%, intent 91% and severity 84%
  of the time; 16.2% of records were flagged `needs_review` by the classifier itself.
- The ranking is deliberately simple (count × severity) and reproducible; it is not a business-weighted score.
- The catch-all issue overlaps with every specific one; some of its 92,441 complaints are about ads or the paywall
  without saying so.
