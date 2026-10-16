# Verification (blind re-label of a declared random sample)

- Verifier: `claude-haiku-5-5`, config `verify-v1|claude-haiku-5-5|657b15226010`, separate prompt (sha256 657b15226010), never shown the enricher's labels.
- Sample: 10 of 479 (min(population, max(min_n, ceil(frac * population))), frac 0.01, min 10, seed `verify-v1|479`).
- Verified 10 records; 0 verifier outputs were invalid.
- Calls: 1 succeeded, 0 failed, $0.000381.

| field | agreement |
|---|---|
| topic | 0.8 |
| intent | 0.8 |
| severity | 0.8 |
| joint | 0.8 |

Severity MAE 0.3; within one level 0.9.

## Planted-error test

5 stored enricher labels were deliberately corrupted in memory (max(5, ceil(0.5 * verified)) records; field cycles topic, severity, intent); the comparison flagged 5 of them (detection rate 1.0).

| review_id | field | original | planted | verifier said | flagged |
|---|---|---|---|---|---|
| 27aeb125-266a-47c9-85f5-bd8a56b4d6c3 | topic | playback | downloads | access | True |
| 4e4c0ec8-e42b-4428-b192-d527c3384aab | severity | 1 | 5 | 1 | True |
| bc1c4825-00c5-458d-ac00-098ce729c76d | intent | unclear | request | praise | True |
| d146397f-4a94-4980-be00-ae9212eca3a7 | topic | billing | usability | billing | True |
| 21915fcd-9a35-48ba-b277-6296c4154603 | severity | 3 | 1 | 3 | True |

## Disagreements (enricher vs verifier)

- `27aeb125-266a-47c9-85f5-bd8a56b4d6c3` enricher playback/praise/1 vs verifier access/complaint/3: "Have been a customer for years and have always been satisfied. I have worked remotely without cell or internet and I like that I can still play all my collections."
- `bc1c4825-00c5-458d-ac00-098ce729c76d` enricher billing/unclear/2 vs verifier other/praise/1: "Best app ever... GET PRENIUM ITS WORTH TRUST!!! uuhhh yeah thats abt it!!! love spotify... m eyah"
