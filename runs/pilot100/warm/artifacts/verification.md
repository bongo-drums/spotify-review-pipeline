# Verification (blind re-label of a declared random sample)

- Verifier: `claude-haiku-5-5`, config `verify-v1|claude-haiku-5-5|657b15226010`, separate prompt (sha256 657b15226010), never shown the enricher's labels.
- Sample: 10 of 100 (min(population, max(min_n, ceil(frac * population))), frac 0.01, min 10, seed `verify-v1|100`).
- Verified 10 records; 0 verifier outputs were invalid.
- Calls: 0 succeeded, 0 failed, $0.000000.

| field | agreement |
|---|---|
| topic | 1.0 |
| intent | 0.9 |
| severity | 0.9 |
| joint | 0.8 |

Severity MAE 0.1; within one level 1.0.

## Planted-error test

5 stored enricher labels were deliberately corrupted in memory (max(5, ceil(0.5 * verified)) records; field cycles topic, severity, intent); the comparison flagged 5 of them (detection rate 1.0).

| review_id | field | original | planted | verifier said | flagged |
|---|---|---|---|---|---|
| c2738a4f-e57c-46bc-a4ad-8ec5a4b5d5cd | topic | usability | playback | usability | True |
| 9f3794ed-4f4b-4430-a548-9cfd2d0c0084 | severity | 1 | 5 | 1 | True |
| 2ffdf599-a0d5-4c01-bf26-025215d44c06 | intent | cancellation | praise | cancellation | True |
| 9e3a706c-f502-4664-a23f-33f3480eca64 | topic | other | downloads | other | True |
| dcff57c6-abd6-413b-b255-aec3dc34fcbd | severity | 4 | 1 | 4 | True |

## Disagreements (enricher vs verifier)

- `0b52ac4e-1982-46ed-aeaa-74eedaefb5c9` enricher other/praise/1 vs verifier other/unclear/1: "Sexy app"
- `c2738a4f-e57c-46bc-a4ad-8ec5a4b5d5cd` enricher usability/complaint/3 vs verifier usability/complaint/2: "Soo trash wayy to many ads I don't want premium but too much ads"
