# Verification (blind re-label of a declared random sample)

- Verifier: `claude-haiku-5-5`, config `verify-v1|claude-haiku-5-5|657b15226010`, separate prompt (sha256 657b15226010), never shown the enricher's labels.
- Sample: 85 of 8447 (min(population, max(min_n, ceil(frac * population))), frac 0.01, min 10, seed `verify-v1|8447`).
- Verified 170 records; 0 verifier outputs were invalid.
- Calls: 4 succeeded, 0 failed, $0.003289.

| field | agreement |
|---|---|
| topic | 0.8588 |
| intent | 0.9176 |
| severity | 0.8882 |
| joint | 0.7176 |

Severity MAE 0.1118; within one level 1.0.

## Planted-error test

85 stored enricher labels were deliberately corrupted in memory (max(5, ceil(0.5 * verified)) records; field cycles topic, severity, intent); the comparison flagged 83 of them (detection rate 0.9765).

| review_id | field | original | planted | verifier said | flagged |
|---|---|---|---|---|---|
| 3abe5d3f-36b6-426a-86fc-64b779843197 | topic | playback | downloads | playback | True |
| 3f062954-0210-419c-8000-9c3ef0bd081d | severity | 1 | 5 | 1 | True |
| e92c5097-1df4-427f-a658-8d1f798779eb | intent | praise | complaint | praise | True |
| 054b71b4-b817-46df-a632-97049443a7ed | topic | other | downloads | other | True |
| 5bbcc1f5-7c55-4547-98ce-a13c7f9cf318 | severity | 2 | 5 | 2 | True |
| 31ca2110-9a65-4818-a288-e504654cdadc | intent | praise | cancellation | praise | True |
| 936d19a5-5522-4acb-8458-04f3d2853b7b | topic | other | support | other | True |
| a66cc931-d7eb-4cad-9c34-c60cd16e0684 | severity | 3 | 1 | 3 | True |
| 1ccd69c3-47c8-422a-95df-fe8062cb9cad | intent | complaint | request | complaint | True |
| 51e97cad-d6e4-40cb-b8a8-a066f1d653e1 | topic | other | playback | other | True |
| 83458151-0b0c-4a5f-ba34-d8cb3c413a93 | severity | 1 | 5 | 1 | True |
| b90dbe13-789b-40ca-bdf3-19bc56ea6006 | intent | request | complaint | request | True |
| 25de360e-bcbd-44a2-9aeb-7ae7905df2e5 | topic | other | billing | other | True |
| 13b6c0f3-9c57-4b0c-a63f-e4adaa806b45 | severity | 1 | 5 | 1 | True |
| f1848566-efb8-42f0-9370-0c686d0a038a | intent | praise | complaint | praise | True |
| 0629557c-88ef-4032-beaa-399ef427cf6c | topic | billing | other | billing | True |
| de004ea0-b2fd-459b-9330-b50df88e0ddd | severity | 1 | 5 | 1 | True |
| 2c7f3221-4b60-4751-a9a6-f3dd4c82d174 | intent | complaint | praise | complaint | True |
| 28e8c56b-4ef4-4538-8065-40da88b6c0b3 | topic | catalog | usability | usability | False |
| db03946a-8639-4814-91a8-eeb9554269de | severity | 3 | 1 | 2 | True |
| ad5a5352-e890-4ec8-b763-3cd8c790ab3a | intent | complaint | request | complaint | True |
| 69179d01-e32f-44d4-bddc-254ee23bfc7e | topic | downloads | catalog | downloads | True |
| 38da1d43-47bb-4038-9713-eee76166bfc2 | severity | 1 | 5 | 1 | True |
| dfa19984-51f2-4130-af9e-49d062026e18 | intent | praise | request | unclear | True |
| 4ba5f31f-52fa-4dae-983e-c13346728254 | topic | support | playback | support | True |
| b7757405-e586-4630-977e-5017ec555033 | severity | 1 | 5 | 1 | True |
| c1011c5e-b912-4028-a8c5-4fac0f7f1614 | intent | request | cancellation | request | True |
| 3a140235-8639-4f22-832d-ad82adf987a7 | topic | other | support | other | True |
| e05d7809-2f2c-439a-9181-00835c225725 | severity | 1 | 5 | 1 | True |
| e0600fd6-8152-40e7-886a-664fdbcd5704 | intent | complaint | praise | complaint | True |
| 499565fb-1238-4fc1-827d-c03e3b9cc692 | topic | other | playback | other | True |
| 7b9a159f-47fb-43b4-b8e3-cb0ffc5a7f1b | severity | 1 | 5 | 1 | True |
| 85ab63b9-4a26-4919-a042-4cb50bb29967 | intent | praise | unclear | praise | True |
| a9fbce72-b1e1-4fd5-a9ef-4d23a7dad8eb | topic | billing | downloads | other | True |
| 4da2e6f1-77e2-4c37-832f-8e9729e2dd25 | severity | 3 | 1 | 3 | True |
| 4edbc09b-88ec-4507-9013-ee8f962d780f | intent | praise | request | praise | True |
| 05ba5c2d-0dcf-424e-8f88-930c9114fd83 | topic | other | usability | other | True |
| 7e4ac518-ef1a-4c8c-98a5-d0f45a78b7ee | severity | 3 | 1 | 3 | True |
| a03a7f80-269d-49ba-a287-0a61844be98f | intent | praise | complaint | praise | True |
| 6c33d793-5965-481c-861e-4a8bb63dcf7c | topic | other | catalog | other | True |
| d03bd0a7-1e00-4ec1-83eb-d3c3d3761317 | severity | 3 | 1 | 3 | True |
| 6f9cf2f1-c516-48f9-bc19-f41b2c5ed150 | intent | complaint | praise | complaint | True |
| b96b79c7-feed-4d01-8e07-9fab649c307d | topic | downloads | catalog | downloads | True |
| 446eea99-fb26-42cb-907a-91d924d4cdb1 | severity | 3 | 1 | 2 | True |
| 1904a093-2e86-43d0-977b-b8cdc513cbf3 | intent | complaint | request | complaint | True |
| 7aef94ea-10a1-4153-9a56-cd070194ac0e | topic | catalog | access | catalog | True |
| be8e94a1-3da2-4d0e-bf0f-c50b7a872167 | severity | 4 | 1 | 4 | True |
| 21664d05-ee1a-4afc-b22b-dfbbcda03755 | intent | praise | request | praise | True |
| 97632279-b3e8-43f7-b880-e0bb6c32e4d9 | topic | playback | usability | playback | True |
| 5650dbb7-7525-46e7-87b7-a75197c48ec7 | severity | 1 | 5 | 1 | True |
| 6263d7a9-a576-4005-b2f1-f863610ada44 | intent | complaint | unclear | complaint | True |
| 3e503f9c-5c5b-4edc-bfd6-a19104c0822e | topic | other | playback | other | True |
| ba528c10-26e9-4c98-b95c-725f7a8e6fb1 | severity | 1 | 5 | 1 | True |
| cf6166ae-d71a-4839-9add-088645ad3b78 | intent | complaint | praise | complaint | True |
| dc3d0e35-dfc6-4d4d-8755-531277cc2394 | topic | usability | other | usability | True |
| b01dbec6-0fd8-4b86-ad51-b95c79f57f1f | severity | 1 | 5 | 1 | True |
| 6b41b629-1730-43f1-8fba-9e3119d8d892 | intent | complaint | request | complaint | True |
| 43f6f40c-2588-440f-a642-1b060b44ea77 | topic | usability | downloads | usability | True |
| 794d0d73-f0b6-4c70-9eff-f73d669c18af | severity | 3 | 1 | 3 | True |
| 4b91eb26-b345-4c9c-85f5-bd141a8e13a1 | intent | praise | request | praise | True |
| 3569509e-6d73-47ee-8146-72959e672385 | topic | playback | other | downloads | True |
| 4966b59e-cf09-4881-b3ea-34fd4118a553 | severity | 2 | 5 | 3 | True |
| 5caa9852-09b5-4a86-9a50-ba9417d75134 | intent | complaint | unclear | complaint | True |
| b4c337dc-73da-4adb-a0ba-8b08a9aafa4a | topic | other | access | other | True |
| 4e3a58be-6219-4fe1-9938-89615427109d | severity | 1 | 5 | 2 | True |
| be6eef1d-03e0-4655-8d17-dcac67bae7c9 | intent | complaint | praise | unclear | True |
| ff0217f6-9473-404b-83da-56c1fd4ac8aa | topic | other | downloads | other | True |
| cdad6c38-9712-4d88-97c4-7ff5f11b46df | severity | 2 | 5 | 2 | True |
| 6c1db2d1-d70e-443a-8631-b7d97b4bffd4 | intent | complaint | request | request | False |
| e3e2dda7-7e9b-4774-ae56-6c27f7523edc | topic | other | support | other | True |
| 5732bb57-d172-4f4c-a7b2-225cf1d58747 | severity | 2 | 5 | 2 | True |
| 643f6d2e-7fd6-43da-8b9a-b8bf5c0be519 | intent | praise | request | praise | True |
| a6c6cf89-cab8-46a6-b5de-b49bbaedb81b | topic | other | playback | other | True |
| 3cdb5635-b2bc-43a0-808d-267bde5f6ce7 | severity | 2 | 5 | 2 | True |
| bec8127c-3880-4f4f-87aa-69f95b704826 | intent | complaint | unclear | complaint | True |
| d58b74e7-bc8c-469c-9c08-b87ed4c18062 | topic | other | billing | other | True |
| 483049e6-afb2-4eea-9b96-a6119fbf932c | severity | 1 | 5 | 1 | True |
| 81c589b8-4e22-4e5d-aa91-641004be5744 | intent | praise | cancellation | praise | True |
| fdfc27f7-cbec-4295-93fb-58f97d3cf9a7 | topic | other | usability | other | True |
| 732871c8-f75d-456b-b6f3-1328d14b4d0d | severity | 2 | 5 | 2 | True |
| 7457d478-da43-4804-8f18-7d1df456adf6 | intent | request | praise | request | True |
| 08c07310-e802-4a88-bd97-2a5f240c0b44 | topic | other | catalog | other | True |
| ea04c626-5d7a-422f-8f45-f36ae4cb6ff5 | severity | 2 | 5 | 2 | True |
| da23c377-bf6a-4a30-a4d7-bb2ad8ef9761 | intent | complaint | cancellation | complaint | True |
| 70e9885e-6fe9-41a6-a822-86540e4cf464 | topic | other | access | other | True |

## Disagreements (enricher vs verifier)

- `09135020-7fea-45ae-a2b8-0dc2460f424e` enricher usability/complaint/2 vs verifier usability/request/2: "The app is great but I can't play the same song again and again so it needs a few changes and it's not user friendly"
- `0ab0d890-5d22-4cbf-9069-608d76338001` enricher playback/request/2 vs verifier usability/request/2: "please fix the jam or bring back how it was before, it has never worked for me or my friends"
- `0ca67f4d-af81-4d04-bb59-7705d7843dc5` enricher other/praise/1 vs verifier other/unclear/1: "Gd"
- `1904a093-2e86-43d0-977b-b8cdc513cbf3` enricher playback/complaint/3 vs verifier playback/complaint/2: "I love this app but sometimes the song keeps stop playing"
- `28e8c56b-4ef4-4538-8065-40da88b6c0b3` enricher catalog/praise/1 vs verifier usability/praise/1: "So far I've enjoyed using this app. I made a playlist for my party and I also have one for more holiday. Brilliant."
- `2d065b1d-6f0c-43e5-9955-e4a7c7c0d172` enricher catalog/complaint/2 vs verifier other/complaint/2: "Spotify wrapped is no longer available in Bangladesh."
- `3569509e-6d73-47ee-8146-72959e672385` enricher playback/complaint/4 vs verifier downloads/complaint/4: "Not at all pleased with this app would recomend you tube premium. Offline mode does not work at all. All my playlists are missing."
- `3abe5d3f-36b6-426a-86fc-64b779843197` enricher playback/complaint/3 vs verifier playback/cancellation/3: "I'm not sure what's going on with this app now, but if it decides to start playing music when it connects to your car (like it should) it will only play the current song and stop. Then when you open t"
- `3d564cc0-2597-4d20-a995-d391f3aee96e` enricher support/praise/1 vs verifier other/praise/1: "Outstanding response,no complaints at all"
- `3f062954-0210-419c-8000-9c3ef0bd081d` enricher playback/praise/1 vs verifier other/praise/1: "Excellent for TV"
- `446eea99-fb26-42cb-907a-91d924d4cdb1` enricher billing/complaint/3 vs verifier billing/complaint/2: "you deserves 5 star but I gave you only 2 stars because when you started premium on your app it became worst."
- `4966b59e-cf09-4881-b3ea-34fd4118a553` enricher billing/complaint/2 vs verifier billing/complaint/3: "Should have been made as just a paid app. With every other music streaming app, you can pick what you actually want to listen to and not have to worry about the app deciding to play a song from a comp"
- `49b7b0b9-9b18-4dee-ab8f-47f615dcc23d` enricher other/complaint/2 vs verifier catalog/complaint/2: "Worst listen in any other app"
- `4ba5f31f-52fa-4dae-983e-c13346728254` enricher support/complaint/2 vs verifier support/complaint/3: "Ko nhớ tên đăng nhập, muốn tìm hỗ trợ mà ko thấy chỗ gửi email nhờ hỗ trợ ở đâu luôn. Mua premium rồi mà coi như bỏ, cskh chán."
- `4e3a58be-6219-4fe1-9938-89615427109d` enricher access/praise/1 vs verifier support/praise/2: "Edit: I was logged out of my account because I was in a different country but the support team was very reactive and helpful. Thanks to them, I have access to my account again. I put 4 stars because t"
- `5650dbb7-7525-46e7-87b7-a75197c48ec7` enricher catalog/praise/1 vs verifier other/praise/1: "I don't have any podcast! But I enjoy it! Very much!"
- `57796843-b718-441a-921d-8dfac3fbc679` enricher usability/complaint/3 vs verifier usability/complaint/2: "This is too much they should probably make the whole platform and user interface paid this is too much ads and lyrics were ok we get it but this is too much very disappointed and dissatisfied with the"
- `5bbcc1f5-7c55-4547-98ce-a13c7f9cf318` enricher other/complaint/2 vs verifier other/cancellation/2: "If they keep updating versions to push certain content I'm done with this app. I love Spotify but almost every update has been worse than it's predecessor"
- `5ffa18b3-9b17-412e-9423-f5dde307e3a0` enricher usability/complaint/2 vs verifier usability/complaint/3: "Going to add my voice to the chorus here - the new UI is absolutely horrendous. I truly don't know how to find new music anymore, which used to be the biggest thing that made Spotify stand out from th"
- `64c28a3c-97cc-43fd-acd0-a1f3bf07414b` enricher catalog/request/1 vs verifier usability/request/2: "how come canvas is no longer an option for some users?"
- `69179d01-e32f-44d4-bddc-254ee23bfc7e` enricher downloads/request/1 vs verifier downloads/request/2: "they should add listen to offline music for free"
- `6c1db2d1-d70e-443a-8631-b7d97b4bffd4` enricher usability/complaint/2 vs verifier playback/request/2: "Really good, beautiful placement and design but would be nice for it to play without app open in the background."
- `6c53aaa3-ff14-4f9f-b95f-7aa552a8ef28` enricher billing/cancellation/3 vs verifier billing/complaint/3: "I am using Spotify from more than 2 years .and it used to be most convenient app for listening music.. But after this latest update it is turning out to be worst...as you cannot even play songs from m"
- `6ceeda8d-be8e-42f8-a815-e22fea0fc973` enricher usability/praise/1 vs verifier catalog/praise/1: "Easy to navigate great selection"
- `7e4ac518-ef1a-4c8c-98a5-d0f45a78b7ee` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Spotify's free subscription is the worst. I can't loop the song, shuffle play,or press play-back button. What kind of music app doesn't provide basic functions? But I can't even play songs that I want"
- `83458151-0b0c-4a5f-ba34-d8cb3c413a93` enricher usability/praise/1 vs verifier other/praise/1: "I love it so much it's really easy and there's no ads"
- `936d19a5-5522-4acb-8458-04f3d2853b7b` enricher other/unclear/2 vs verifier other/complaint/2: "Add was same it geting diatribe other wise it is better"
- `93ad8fd0-ffec-470d-9470-17805358f77b` enricher playback/praise/1 vs verifier catalog/praise/1: "Good app this was very amazing and good sound all song is available in this app"
- `97632279-b3e8-43f7-b880-e0bb6c32e4d9` enricher playback/complaint/4 vs verifier playback/complaint/3: "Very worst app, whatever list of songs I play it's not playing. It playing on its own."
- `99d27ae0-644e-4c12-99ec-361563448936` enricher catalog/praise/1 vs verifier other/praise/1: "Really good app for listening to music and podcasts"
- `a0164fc6-572f-48ad-9b64-81cf714a7199` enricher other/praise/1 vs verifier catalog/praise/1: "Good app i love bts txt black pink"
- `a66cc931-d7eb-4cad-9c34-c60cd16e0684` enricher playback/complaint/3 vs verifier usability/cancellation/3: "The update honestly sucks, I don't know why but it just doesn't let me play the music i wanted! Like i would just press the song and it will be a completely different song 😤 it's so frustrating especi"
- `a9fbce72-b1e1-4fd5-a9ef-4d23a7dad8eb` enricher billing/praise/1 vs verifier other/praise/1: "Okay it's back to being how it should be"
- `b01dbec6-0fd8-4b86-ad51-b95c79f57f1f` enricher catalog/praise/1 vs verifier other/praise/1: "Best Music App.. Music quality:- Excellent Collection:- Mind Blowing"
- `be6eef1d-03e0-4655-8d17-dcac67bae7c9` enricher other/complaint/2 vs verifier other/unclear/1: "Booooooooooo"
- `bec8127c-3880-4f4f-87aa-69f95b704826` enricher usability/complaint/2 vs verifier catalog/complaint/2: "Great experience but i wish when listening to "new music" it wouldn't pull music from my liked songs😕"
- `becd24a0-470c-44f7-b210-c8ed10fc281c` enricher catalog/request/2 vs verifier playback/complaint/3: "App is good but you should provide with lyrics for the new songs and why the hell this app shows no internet connection even though when I'm connected with the internet.my internet work's fine but not"
- `c06049f9-4df9-4f97-9878-5225f50225d5` enricher billing/complaint/2 vs verifier other/complaint/2: "Why is the free working is so so stupied"
- `c1011c5e-b912-4028-a8c5-4fac0f7f1614` enricher other/request/1 vs verifier playback/request/1: "Will we be getting hifi any time soon?"
- `cf6166ae-d71a-4839-9add-088645ad3b78` enricher usability/complaint/3 vs verifier usability/complaint/2: "DON'T DOWNLOAD THIS:Such a worst app ... that always plays adds instead of songs ...if want to enjoy music free without adds don't download this app .."
- `da0c8e5c-d062-450d-897e-f9038c693a8f` enricher usability/complaint/3 vs verifier usability/complaint/2: "Horrible, lo de cuatros anuncios de seguido es fatal, en media hora seis"
- `db03946a-8639-4814-91a8-eeb9554269de` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Eti andi, patalu search chesthe , not found anta."
- `de580808-1a58-4c61-8664-7c521cb39adf` enricher usability/complaint/3 vs verifier usability/complaint/2: "I wanna shuffle my music. Clearly there's a shuffle indicator beside the but green play button. But when I hit it it just plays the last song I was listening too like hot damn"
- `dfa19984-51f2-4130-af9e-49d062026e18` enricher other/praise/1 vs verifier other/unclear/1: "I mean, it's Spotify."
- `e05d7809-2f2c-439a-9181-00835c225725` enricher playback/praise/1 vs verifier other/praise/1: "This was amazing because I play my song and back my screen easily"
- `e37747bd-775f-4ab3-9f41-e606c89211ce` enricher usability/complaint/3 vs verifier usability/complaint/2: "So many adds...after every song there is at least five adds you can't skip...absolutely ridiculous"
- `e66536b0-850e-45a1-b5b4-2ce29c070980` enricher usability/complaint/3 vs verifier usability/request/2: "Car Mode was taken away, then brought back, and now removed yet again. I guess Spotify cares LESS about your safety and more about you buying their "Car Thing" product. Bring back the Car Mode option "
- `fa78036b-b855-4694-bea0-e1bb541c69f5` enricher other/cancellation/2 vs verifier other/unclear/1: "Hate Spotify and Truecaller 😡😡 ban Spotify and Truecaller 😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡😡"
