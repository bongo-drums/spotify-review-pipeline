# Golden 50: model vs human labels

Scored 2026-10-16T21:19:54.709967Z from run `runs/golden50`. 50 of 50 golden reviews have a model prediction (0 abstentions count as disagreements). Intent denominator 46 (rows [38, 41, 43, 45] unresolved).

| field | agreement | macro F1 |
|---|---|---|
| topic | 0.66 | 0.3938 |
| intent | 0.8478 | 0.8098 |
| severity | 0.76 | 0.687 |
| joint (topic, severity, resolved intent) | 0.54 | |

Severity MAE 0.3; within one level 0.94.

## Confusions (human -> model)

- **topic**: other->usability (4), other->catalog (3), playback->billing (2), support->other (1), support->playback (1), other->billing (1), catalog->usability (1), catalog->playback (1), billing->catalog (1), catalog->downloads (1), usability->other (1)
- **intent**: unclear->complaint (3), unclear->request (2), unclear->praise (1), complaint->cancellation (1)
- **severity**: 2->3 (3), 3->4 (3), 1->2 (3), 2->4 (1), 1->3 (1), 3->1 (1)

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
| 38 | `8c0546b0-ce43-4a36-9d33-9f979e98d522` | catalog/?/2 | catalog/complaint/3 (lyrics) | False | 1-Lyrics not getting loaded, 2-can't go back to or start song where to wanted. Pathetic update |
| 41 | `b58dd6f0-ad88-4319-b6db-58afb60c37c1` | catalog/?/3 | usability/request/1 (queue_playlist_mgmt) | False | The only thing Spotify lacks is the ability to organize saved  albums/artists into collections. Would definitely deserve 5 stars if it  included this feature. |
| 43 | `dceb14e7-2df0-422f-bb2b-73d7c373159a` | catalog/?/3 | playback/complaint/3 (stops_skips_glitches) | False | I gave one star because I can't give any less than that. the new update is sooooooo annoying like I can't even play the songs that I like and I can't rewind son |
| 44 | `5fba12ea-4980-4f25-a129-f830a3974fd2` | billing/praise/1 | catalog/praise/1 (recommendations) | False | I find Spotify very good, it finds and play whatever music you want and also adds songs that you might like, judging from your playlist if you choose to arrange |
| 45 | `ac4e860a-c042-49cc-90f3-189591c336ac` | catalog/?/3 | downloads/complaint/4 (offline_needs_internet) | False | paying for subscribing but unable to play in offline mode really? |
| 47 | `d2f3874f-d15d-4a2f-bb97-4f1213defa46` | usability/complaint/2 | usability/complaint/3 (ads_interruptions) | False | Too expensive and the free version is pretty much unusable with constant ads... Every two or three songs.. Forget it |
| 48 | `99b93e31-9f15-4daa-88ac-349ab0419c48` | usability/complaint/2 | other/complaint/2 (general_negative) | True | This update very bad for everyone.old Spotify. we all want. |

## Per-class detail

### topic

| class | support | predicted | precision | recall | F1 |
|---|---|---|---|---|---|
| billing | 1 | 3 | 0.0 | 0.0 | 0.0 |
| catalog | 5 | 6 | 0.3333 | 0.4 | 0.3636 |
| other | 32 | 26 | 0.9231 | 0.75 | 0.8276 |
| playback | 5 | 5 | 0.6 | 0.6 | 0.6 |
| support | 2 | 0 | None | 0.0 | 0.0 |
| usability | 5 | 9 | 0.4444 | 0.8 | 0.5714 |

### intent

| class | support | predicted | precision | recall | F1 |
|---|---|---|---|---|---|
| complaint | 16 | 18 | 0.8333 | 0.9375 | 0.8824 |
| praise | 20 | 21 | 0.9524 | 1.0 | 0.9756 |
| unclear | 10 | 4 | 1.0 | 0.4 | 0.5714 |

### severity

| class | support | predicted | precision | recall | F1 |
|---|---|---|---|---|---|
| 1 | 30 | 27 | 0.963 | 0.8667 | 0.9123 |
| 2 | 13 | 12 | 0.75 | 0.6923 | 0.72 |
| 3 | 7 | 7 | 0.4286 | 0.4286 | 0.4286 |

