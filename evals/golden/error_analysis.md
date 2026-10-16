# Golden 50: error analysis

> **Draft for Matt to edit.** Claude wrote this from `results.md` and the review texts; the judgments below are
> proposals. Matt labelled the 50 reviews by hand (`human_codes.csv`) and decides which of these calls stand.
> Delete this note once reviewed.

Scores (`results.md`): topic agreement 0.66, intent 0.85 (46 resolved rows), severity 0.76, joint 0.54; severity
MAE 0.30 and 94% of severities within one level. The model never abstained. The numbers look worse than the
10,000-review blind verification (topic 0.86, intent 0.92, severity 0.89) because the golden disagreements are
mostly *definition* disagreements between how I labelled and how `labels/definitions.md` reads, not random
model errors. Three patterns explain 17 of the 23 disagreements.

## Pattern 1: general praise vs. "first specific praised feature" (7 rows)

I used the `+` shortcut (other / praise / 1) for almost every positive review. The contract says a positive
review takes *the first specific praised feature* and only general praise is `other`. The model followed the
contract: "Spotify is awesome and very diverse" became `catalog` (row 9), "Nice app, very less advertising"
became `usability / ads_interruptions` (row 37), "it finds and plays whatever music you want and also adds songs
you might like" became `catalog / recommendations` (row 44, which I had coded `billing`, a slip).

**Verdict:** the model is closer to the definitions than my labels. Rows 9 and 37 are debatable ("diverse" and
"less advertising" are thin as features); row 44 is my error. For the final run this pattern does not touch the
ranking, because praise records are excluded from issue membership.

## Pattern 2: non-English text I coded `unclear` (5 rows)

Rows 17, 19, 24, 31 and 34 are Tagalog, Indonesian, Hindi/Urdu or garbled English that I marked `?`
(other / unclear / 1). The definitions say to classify when the meaning is clear and to set `needs_review`
otherwise. The model did exactly that and flagged `needs_review=true` on four of the five. Two of its readings
are plainly right: "asem, lirik nya kdang gaada kek mana??" is a complaint that lyrics are sometimes missing
(`catalog / lyrics`, row 19), and "Please ye ads ko thoda kumm Karo harr ek song ke baad ad" is a request for
fewer ads (`usability / ads_interruptions / request`, row 24).

**Verdict:** my `?` was a labelling shortcut, not a judgment that the text is meaningless. The model's labels
stand; the `needs_review` flag is the right mechanism, and it is what the dashboard surfaces.

## Pattern 3: premium-only controls are billing, not playback (2 rows)

Row 29: "Deleting this App ... we can't CHOOSE song after a song played, and we can't turn off shuffle option.
They are pushing us to upgrade to Premium." I coded playback / complaint / 3; the model coded
billing / premium_only_controls / cancellation / 3. Row 30 is the same split. Boundary call 1 in
`labels/definitions.md` puts free-tier limits under billing, and the intent precedence puts "deleting this app"
under cancellation.

**Verdict:** the model is right on both fields under the definitions; I labelled the symptom (cannot play what
I want) rather than the cause (a paywall). This is the single most consequential boundary in the whole
dataset, because `billing.premium_only_controls` is the second-ranked issue in the 10k run. If I had changed
the definition instead, that issue would move into `usability` and the recommendation would change with it.

## Individual cases worth a second look

- **Row 12** (support story): "Update: I reached out to Spotify Support ... got the app working again. Old
  Post: ... it keeps crashing every time." I coded support / complaint / 3. The model coded
  playback / crash_wont_open / 4 with the crash sentence as evidence. Boundary call 2 says a problem that support
  solved is `support / praise / 1`. Neither of us followed it. My label is defensible (the review is about
  support), the model's severity of 4 is defensible (the app would not open), and the definitions should say
  which part of an "Update:" review wins. I would add: *the update wins when it reports a resolution.*
- **Row 33**: "Listening to music in a normal volume and suddenly an add starts and my ears feel like they
  explode!!" I coded `?`; the model coded usability / ads_interruptions / complaint / 3. My label is wrong; I
  must have misread it as rant. The model's 3 is right: music plays, ads interrupt it.
- **Row 47**: "the free version is pretty much unusable with constant ads... Every two or three songs." Both
  of us said usability / complaint; I gave severity 2, the model 3. The definitions' own example ("ads interrupt
  but music plays") is a 3, so the model is consistent with the rubric. I would keep 3.
- **Row 48**: "This update very bad for everyone.old Spotify. we all want." I inferred a redesign complaint
  (usability / 2); the model refused to infer a defect (other / general_negative / 2, `needs_review`). The
  contract's "worst update ever" rule supports the model.
- **Rows 38, 41, 43, 45**: I typed `cp2`/`cp3` (catalog / praise / 2-3), which contradicts the rule that praise
  is severity 1. The scorer keeps my topic and severity and leaves intent unresolved for these four. Reading
  them again: 38 and 43 are complaints (lyrics not loading; cannot play or rewind songs), 41 is a feature request
  (organise saved albums into collections), 45 is a complaint (paid but cannot play offline). I will re-enter
  them as `cc3`, `ur1`, `cc3`/`pc3`, `dc4` once I have decided, and re-run `python -m pipeline.evals golden`.

## What I take from this

1. Where the model and I disagree on **topic**, the definitions usually side with the model. The fix is to my
   labels and, for the support/update case, to the definitions, not to the prompt.
2. **Intent** is the most reliable field (0.85 here, 0.92 in the blind check); the misses are my `?` shortcuts.
3. **Severity** disagreements are one level apart in 47 of 50 cases, and in the three larger gaps (rows 25, 32,
   34) the model read a blocked core task where I read a degraded one; the texts support either reading.
4. For the business result, the pattern that matters is #3: the billing/usability boundary moves the second-
   ranked issue. The memo states the issue ID so a reader can see where it would land under the other rule.
