# Golden 50: model vs human labels

Scored 2026-10-16T22:40:08.553233Z from run `runs/golden50`. 50 of 50 golden reviews have a model prediction (0 abstentions count as disagreements). Intent denominator 50 (rows [] unresolved).

| field | agreement | macro F1 |
|---|---|---|
| topic | 0.72 | 0.5317 |
| intent | 0.86 | 0.7368 |
| severity | 0.82 | 0.6741 |
| joint (topic, severity, resolved intent) | 0.62 | |

Severity MAE 0.22; within one level 0.96.

## Confusions (human -> model)

- **topic**: other->usability (4), other->catalog (3), playback->billing (2), support->other (1), support->playback (1), other->billing (1), billing->catalog (1), usability->other (1)
- **intent**: unclear->complaint (3), unclear->request (2), unclear->praise (1), complaint->cancellation (1)
- **severity**: 1->2 (3), 2->3 (2), 3->4 (2), 2->4 (1), 1->3 (1)

## Disagreements (for the human error analysis)

| n | review_id | human | model | needs_review | text |
|---|---|---|---|---|---|
| 4 | `991b6b3a-f511-458a-a5b7-234f78048fb5` | other/complaint/2 | usability/complaint/2 (ads_interruptions) | False | Ads were okay, but limited functionality..it's just too much |
| 6 | `0c6ca545-3f89-4da6-b3db-1a352371fb6e` | support/complaint/2 | other/complaint/2 (general_negative) | False | Hate this application 🤮🤮🤮🤮🤮🤮 |
| 9 | `b5ee7834-a0eb-4c15-9c7b-935831021922` | other/praise/1 | catalog/praise/1 (missing_content) | False | Spotify is awesome and and very diverse :) |
| 11 | `947821dc-b356-45dc-a0bc-1903728fad40` | playback/complaint/2 | playback/complaint/3 (stops_skips_glitches) | False | Very good but wen I play my song it o ly plays a little bit then it stops I updated my phone and it worked but it happend again they need to fix this issue |
| 12 | `723f07de-9881-4049-8680-1a9e25652914` | support/complaint/3 | playback/complaint/4 (crash_wont_open) | False | Update: I reached out to Spotify Support and with some help from Sarah I was able to get the app working again. Old Post:Normally, the app works great, and I us |
| 17 | `ac6cd66d-a9d2-42a4-afb8-2f84beff7fd1` | other/unclear/1 | catalog/praise/1 (missing_content) | True | Lhat ng song nasa spotify |
| 19 | `46842184-32f8-4088-ac15-2a700a7e94ed` | other/unclear/1 | catalog/complaint/2 (lyrics) | True | asem, lirik nya kdang gaada kek mana?? |
| 24 | `372d4e67-59cc-4c54-879f-3e8a202ee554` | other/unclear/1 | usability/request/2 (ads_interruptions) | True | Please ye ads ko thoda kumm Karo harr ek song ke baad ad 🙏🙄 |
| 25 | `47f1406d-4918-4d60-9647-5ca8e610caca` | playback/complaint/2 | playback/complaint/4 (stops_skips_glitches) | False | Very poor updates as we cannot playback the songs and most bad updates are happening it is affecting the spotify quality |
| 29 | `3ddb3f4e-f7b9-430b-b335-eadc6d321f46` | playback/complaint/3 | billing/cancellation/3 (premium_only_controls) | False | Deleting this App. The new update suck, we can't choose our fvrt songs after some clicks, we can't CHOOSE song after a song played, and we can't turn off shuffl |
| 30 | `16d640e9-b281-4746-9562-c7dbcf7126b6` | playback/complaint/3 | billing/complaint/3 (premium_only_controls) | False | It's my best music app but now it's not...everything basic features is premium.... |
| 31 | `8cc4fad4-26ec-47b7-96e8-49c7da714eca` | other/unclear/1 | other/complaint/2 (general_negative) | True | I hate this app and sweden .I love islam |
| 32 | `215463ae-95b7-4481-8747-1754b68f31fa` | playback/complaint/3 | playback/complaint/4 (crash_wont_open) | False | What is happening with Spotify?? Recently I'm trying to play a song but it doesn't working. So I unstalled and thn again install it now I can't even open the ap |
| 33 | `46c0b49f-83a1-427e-8f0b-cef62e3c94b5` | other/unclear/1 | usability/complaint/3 (ads_interruptions) | False | Are you out of your mind? This is dangerous! Listening to music in a normal volume and suddenly an add starts and my ears feel like they explode!! Stop this BS, |
| 34 | `283b5843-a992-464f-b1dc-9dc7281ff390` | other/unclear/1 | billing/request/1 (price) | True | Beth, we all got to give me a free dollar to go with 3 months, bro I can't be like |
| 37 | `2aa566c6-b98d-4513-b900-83702a8db8eb` | other/praise/1 | usability/praise/1 (ads_interruptions) | False | Nice app, very less advertising |
| 44 | `5fba12ea-4980-4f25-a129-f830a3974fd2` | billing/praise/1 | catalog/praise/1 (recommendations) | False | I find Spotify very good, it finds and play whatever music you want and also adds songs that you might like, judging from your playlist if you choose to arrange |
| 47 | `d2f3874f-d15d-4a2f-bb97-4f1213defa46` | usability/complaint/2 | usability/complaint/3 (ads_interruptions) | False | Too expensive and the free version is pretty much unusable with constant ads... Every two or three songs.. Forget it |
| 48 | `99b93e31-9f15-4daa-88ac-349ab0419c48` | usability/complaint/2 | other/complaint/2 (general_negative) | True | This update very bad for everyone.old Spotify. we all want. |

## Per-class detail

### topic

| class | support | predicted | precision | recall | F1 |
|---|---|---|---|---|---|
| billing | 1 | 3 | 0.0 | 0.0 | 0.0 |
| catalog | 2 | 6 | 0.3333 | 1.0 | 0.5 |
| downloads | 1 | 1 | 1.0 | 1.0 | 1.0 |
| other | 32 | 26 | 0.9231 | 0.75 | 0.8276 |
| playback | 6 | 5 | 0.8 | 0.6667 | 0.7273 |
| support | 2 | 0 | None | 0.0 | 0.0 |
| usability | 6 | 9 | 0.5556 | 0.8333 | 0.6667 |

### intent

| class | support | predicted | precision | recall | F1 |
|---|---|---|---|---|---|
| complaint | 19 | 21 | 0.8571 | 0.9474 | 0.9 |
| praise | 20 | 21 | 0.9524 | 1.0 | 0.9756 |
| request | 1 | 3 | 0.3333 | 1.0 | 0.5 |
| unclear | 10 | 4 | 1.0 | 0.4 | 0.5714 |

### severity

| class | support | predicted | precision | recall | F1 |
|---|---|---|---|---|---|
| 1 | 31 | 27 | 1.0 | 0.871 | 0.931 |
| 2 | 12 | 12 | 0.75 | 0.75 | 0.75 |
| 3 | 6 | 7 | 0.5714 | 0.6667 | 0.6154 |
| 4 | 1 | 4 | 0.25 | 1.0 | 0.4 |

