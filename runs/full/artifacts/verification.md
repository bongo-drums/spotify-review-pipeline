# Verification (blind re-label of a declared random sample)

- Verifier: `claude-haiku-5-5`, config `verify-v1|claude-haiku-5-5|657b15226010`, separate prompt (sha256 657b15226010), never shown the enricher's labels.
- Sample: 4842 of 484182 (min(population, max(min_n, ceil(frac * population))), frac 0.01, min 10, seed `verify-v1|484182`).
- Verified 4842 records; 0 verifier outputs were invalid.
- Calls: 97 succeeded, 0 failed, $0.091536.

| field | agreement |
|---|---|
| topic | 0.841 |
| intent | 0.9052 |
| severity | 0.8437 |
| joint | 0.6745 |

Severity MAE 0.1609; within one level 0.9961.

## Planted-error test

2421 stored enricher labels were deliberately corrupted in memory (max(5, ceil(0.5 * verified)) records; field cycles topic, severity, intent); the comparison flagged 2384 of them (detection rate 0.9847).

| review_id | field | original | planted | verifier said | flagged |
|---|---|---|---|---|---|
| 57c87180-46e1-4365-b220-9d13a59444d0 | topic | billing | support | billing | True |
| e626c6a7-672b-4d11-b772-c7991723f015 | severity | 1 | 5 | 1 | True |
| 428d84ed-cb47-468a-9553-23f86865c226 | intent | praise | complaint | praise | True |
| c657c8ee-d6d8-4913-9ada-afe7ca1c71b7 | topic | other | downloads | playback | True |
| 609a9f9d-7dbb-4556-8fd7-f216d78beff9 | severity | 1 | 5 | 1 | True |
| 8f424b7c-ffaf-488f-845a-33ad6f700e8f | intent | complaint | praise | complaint | True |
| 5b8de521-7b75-4e0e-a46a-ffe513929b58 | topic | usability | access | usability | True |
| 1d9a392d-72f5-4d92-abad-480ec9f56ebe | severity | 3 | 1 | 2 | True |
| 01036c2b-70ba-4214-b008-73250998b920 | intent | praise | unclear | praise | True |
| 9bead5a3-d10f-4369-8c66-a057520fa874 | topic | other | playback | other | True |
| 513ec475-c018-4359-a2a1-553cdc132c8f | severity | 1 | 5 | 1 | True |
| cb6f2d6a-a766-4159-927c-74229d5755be | intent | complaint | cancellation | complaint | True |
| 6630e202-b273-456b-ad63-28299c4b4611 | topic | downloads | usability | downloads | True |
| 0b71dd3a-2058-463c-a400-b4176d70b601 | severity | 3 | 1 | 2 | True |
| 9bcc48fa-4057-42de-8156-c6877df26cea | intent | praise | complaint | praise | True |
| 7dda4e64-5b64-44e7-aa88-e4cb5258e76b | topic | usability | downloads | usability | True |
| 47f6da99-fcba-4b33-abfe-7aa36c5de32f | severity | 1 | 5 | 1 | True |
| c25708b2-55f9-4f1e-bb42-21dbbeea536b | intent | request | unclear | request | True |
| 75f1696a-ffd4-432b-9d7d-2c98e129eda1 | topic | other | catalog | other | True |
| 54a46927-e523-4d3c-abfe-b48be536c208 | severity | 2 | 5 | 2 | True |
| 0ded4d5c-d2a3-447c-9fd4-4d7d2bcc5d12 | intent | complaint | request | complaint | True |
| cd7b3b63-9c7d-4185-81f6-0e48b1838754 | topic | other | access | other | True |
| 568fcd9c-a340-4129-b08a-69a7d8415f69 | severity | 3 | 1 | 3 | True |
| 9ae985bc-bb62-4999-910e-2857e2e9c8fd | intent | praise | request | praise | True |
| 627f56e6-ed6f-4824-bf21-717a17274988 | topic | billing | usability | usability | False |
| 47e9388c-89cd-4564-85e5-7def2ac97b09 | severity | 1 | 5 | 1 | True |
| f22fc7e4-a958-4199-9992-6d62ed493f3d | intent | praise | complaint | praise | True |
| ad662ca1-4ca6-4e38-b344-93c198664406 | topic | catalog | downloads | other | True |
| e71e28ea-87a1-44bb-b898-ff87153b8e77 | severity | 4 | 1 | 3 | True |
| fc567fb3-9ee1-41bc-9c83-ff2d6db25480 | intent | request | unclear | complaint | True |
| 4203edb1-d91e-4875-bd6a-b44479a74154 | topic | other | playback | other | True |
| 5532da2c-8d1b-4c7c-a92b-a49ced02091e | severity | 3 | 1 | 3 | True |
| 61f80002-5ff2-44e5-b359-68c7794f8807 | intent | praise | unclear | praise | True |
| 0ad290da-ca30-4d5a-b00a-8c2cd998c672 | topic | other | billing | other | True |
| 1912e7f5-a292-4d75-adb1-603df533fa21 | severity | 2 | 5 | 2 | True |
| 939f59b6-20cf-4318-93e2-1e7ebaa5bd17 | intent | complaint | cancellation | complaint | True |
| 0cd6f853-1193-49e7-b489-018d63ee2def | topic | catalog | support | catalog | True |
| d6284e21-db16-4bfa-9e91-97ef48eb8dcd | severity | 3 | 1 | 2 | True |
| eb3a2183-d16c-46bb-9bf5-f9e71292970a | intent | complaint | unclear | complaint | True |
| d69f1528-389d-4056-b268-cd897c1d5f7a | topic | catalog | usability | catalog | True |
| 230b7c7b-bbf0-4e27-83fb-31b3dccd853f | severity | 1 | 5 | 1 | True |
| 52312301-c457-43f5-adda-19151bf7e39e | intent | praise | cancellation | praise | True |
| 5b07c0c3-f553-4019-a00b-9a9c546c9caa | topic | catalog | billing | catalog | True |
| f227b91d-3bfd-43b3-a043-7292ffd17d15 | severity | 3 | 1 | 3 | True |
| e4332ab5-7d63-4249-b268-742086231fdb | intent | complaint | request | complaint | True |
| a206cfcd-50a3-46e0-888a-57223ae5135b | topic | other | downloads | other | True |
| 0b6910d5-dc3c-4608-97fe-3489d0acf8af | severity | 3 | 1 | 3 | True |
| f8d0c5d7-77b7-4fbf-8702-8b8af049f950 | intent | complaint | cancellation | complaint | True |
| 471e2b62-db15-4a78-b64a-6ef4b6313b94 | topic | usability | access | billing | True |
| cd670d55-844d-4319-9c32-bfc94239073d | severity | 2 | 5 | 2 | True |
| 35749081-c99b-4173-8d1b-b9d5c634b867 | intent | complaint | unclear | complaint | True |
| c1b2ecc1-4201-4d1b-989a-6cc98117c6fc | topic | other | playback | other | True |
| 46a0f98f-9113-4688-9ef0-2ca28920ffe8 | severity | 1 | 5 | 1 | True |
| c11786e5-ffdc-41f0-a3a0-4407c3b87af5 | intent | praise | cancellation | praise | True |
| 7a9bff6a-b81e-4c10-b90a-ef7841637a63 | topic | billing | downloads | billing | True |
| 8dae563b-4290-4ada-b901-23b3ec099f21 | severity | 4 | 1 | 4 | True |
| 6a1adf7d-51e3-4ce1-8551-b19b5cdae28c | intent | unclear | cancellation | unclear | True |
| 50a2ed47-bf0c-43ea-bcf6-499f2b52d963 | topic | other | usability | other | True |
| eefafac5-4a74-4469-b626-ca929e6ef521 | severity | 1 | 5 | 1 | True |
| ad33c661-3768-4224-bb2c-381989a1cf9a | intent | complaint | cancellation | complaint | True |
| e3efe4a7-21f9-4735-8d4f-b801960bad00 | topic | usability | support | usability | True |
| e7756b1b-301a-4047-a99b-f5d20ffc960e | severity | 2 | 5 | 2 | True |
| 18837295-4e7a-493a-ae54-9dd3ee08ad6e | intent | request | cancellation | request | True |
| 1a4b1750-0433-465a-bf0b-6949c8e66ca0 | topic | billing | support | other | True |
| e3d74528-ba66-4ad3-8124-e5c1f732626e | severity | 1 | 5 | 1 | True |
| 13b94f13-59f6-45a2-a89c-70fdc6164015 | intent | praise | cancellation | praise | True |
| a6eb9bc2-0338-4b01-8e59-206baa4d8658 | topic | usability | billing | usability | True |
| cef9c6fd-c8bb-47ac-8c54-38d3a562bede | severity | 2 | 5 | 2 | True |
| 4285e41f-fa24-4c9e-9436-137d78ece079 | intent | praise | unclear | praise | True |
| 0e4833b1-53e7-4898-8803-b98aa276c43d | topic | other | support | other | True |
| 4607d898-3914-4cb8-80a2-224706a95f16 | severity | 3 | 1 | 2 | True |
| d4a77bc8-5a43-4f5f-96ce-5ed87a67f076 | intent | praise | request | praise | True |
| 08f37dce-0916-4581-915e-12bf97d366d0 | topic | catalog | other | playback | True |
| 2d5fe26b-bcf9-4efd-8c6e-a05fadcf67a6 | severity | 2 | 5 | 2 | True |
| b983237c-18a5-40af-aeae-41d7a670d319 | intent | complaint | unclear | complaint | True |
| 95502086-d697-4c02-b868-0a0c3dea322d | topic | billing | downloads | catalog | True |
| 3be8722b-375b-4429-9682-814716cd87df | severity | 3 | 1 | 3 | True |
| 5c4f0648-93eb-4ac6-a243-7017e234fe8f | intent | complaint | praise | complaint | True |
| 4eb21ab3-4c23-4a6d-ba5d-d0a8b6f4f4a2 | topic | usability | downloads | billing | True |
| 96a1ddd1-a455-44d4-a259-3ff9d07eb257 | severity | 1 | 5 | 1 | True |
| c6456f9d-35a1-4a1f-abef-c4e443eb2dd9 | intent | complaint | request | complaint | True |
| 12626a65-20c9-4343-96c7-cac7564e99fb | topic | access | billing | access | True |
| 3b5ee478-6184-4d69-865e-033c87232e4b | severity | 1 | 5 | 1 | True |
| df61f25d-17a9-4d14-ada3-693b7e5e09fb | intent | unclear | praise | unclear | True |
| dcdd71ac-ecbe-46cc-9e11-751c88e841c5 | topic | catalog | billing | catalog | True |
| fe0ad324-ee21-4e28-b995-2108f300dd3b | severity | 3 | 1 | 3 | True |
| 134cd431-1f06-45b1-b418-f2cfbfb260aa | intent | request | cancellation | request | True |
| 479b5d4f-cfb7-4284-87cd-9af4fac64f93 | topic | other | downloads | other | True |
| 6d7b08fc-97ef-4d79-9198-db3d131b626c | severity | 2 | 5 | 2 | True |
| 0552875e-7837-4c36-b77c-129cd32f89a7 | intent | unclear | complaint | unclear | True |
| cd810400-ddb9-4271-83ad-30dbacefd028 | topic | catalog | downloads | other | True |
| 792f1ad6-f092-4ba1-ab6f-357108bc2afa | severity | 1 | 5 | 1 | True |
| 268d713b-0028-4a1a-bdf7-6e337840793d | intent | unclear | cancellation | unclear | True |
| 66762fc0-3dcf-41c6-ab24-d953795c26eb | topic | playback | billing | other | True |
| 6720e463-fed7-4e2f-bb59-7d5c1f1f8dcd | severity | 3 | 1 | 3 | True |
| e14b5396-a0b9-4b82-a267-9cf328821fa5 | intent | complaint | cancellation | complaint | True |
| 079e00e8-95d9-4ea6-ac0e-97123f98ea77 | topic | other | billing | other | True |
| 6a722f94-d205-46e1-838c-a59cbeec3eb9 | severity | 3 | 1 | 3 | True |
| 91d5aa0a-8317-4070-825f-2218e4c99546 | intent | praise | complaint | praise | True |
| 39d8cd31-0661-4daf-a510-73ac229af67d | topic | catalog | support | catalog | True |
| 8f41ea09-81d7-431e-9df7-b583361c2063 | severity | 3 | 1 | 3 | True |
| aab827b7-65a3-4956-a95a-90798dee6c0a | intent | praise | cancellation | praise | True |
| 7edebe9c-fd55-4995-b700-8dd578c84ba5 | topic | other | catalog | other | True |
| 7cd93271-beb0-4950-b355-14820514a85b | severity | 2 | 5 | 2 | True |
| 62152af7-526f-4a33-8244-b7ae7eca50c4 | intent | unclear | cancellation | unclear | True |
| 1fb7e1eb-eb0c-4823-9983-d174cab59521 | topic | usability | playback | usability | True |
| bcd0a07a-81f9-4cec-a454-9978a772ff75 | severity | 1 | 5 | 1 | True |
| 04262e8a-722e-48c3-b429-3a6fa0ab8d47 | intent | request | complaint | request | True |
| dd9ba46f-662b-43d7-95fe-87629177f267 | topic | billing | usability | billing | True |
| a7aae37f-be39-4e05-8dbb-b35fb672501e | severity | 2 | 5 | 2 | True |
| 412be643-5561-4f7b-b5cd-c179b5ba46d9 | intent | complaint | unclear | complaint | True |
| e594a286-e25e-4247-97c6-3c8d10cc8fe8 | topic | other | support | other | True |
| b288cbd7-d36a-4cdb-8805-18ae566a6269 | severity | 1 | 5 | 1 | True |
| 67f1bfa5-ffe9-4c4d-a935-4244fee48f2c | intent | praise | cancellation | praise | True |
| a023cda0-15a9-4da7-a073-218a207dd473 | topic | usability | catalog | usability | True |
| 699fda5e-7664-4882-a912-7574acf75978 | severity | 2 | 5 | 2 | True |
| 05359400-8b62-4e5d-b28e-4e951b0d0afb | intent | complaint | request | complaint | True |
| 331c5488-3046-471b-93ca-b1de12443db4 | topic | downloads | usability | downloads | True |
| 624c7248-a861-44c6-b71d-4aeb018e9c05 | severity | 1 | 5 | 1 | True |
| 87c6b7dd-414f-4a97-8b35-ec231446de78 | intent | praise | request | praise | True |
| 15dbd53f-b713-4a9d-9dd1-e7254e2696cc | topic | billing | other | billing | True |
| beac4fb3-afa8-4a3d-a31e-be686fdc299d | severity | 3 | 1 | 2 | True |
| df77019a-06a7-4e58-8a75-5b92f4b680b6 | intent | praise | complaint | praise | True |
| 7e66dcbf-e4a7-4b42-b72f-6356932ec3bd | topic | other | catalog | usability | True |
| d7c9ebb1-0ed4-4a67-b8a8-893c83477793 | severity | 1 | 5 | 1 | True |
| 57f2180a-71b3-4059-862c-adc92aa28b6b | intent | complaint | praise | complaint | True |
| aa105518-bf36-47da-9c1f-6bc5b7383120 | topic | billing | support | billing | True |
| 07959cdd-7861-4b2f-bb2f-fcfc5787335e | severity | 3 | 1 | 2 | True |
| 7d209acb-0721-429e-ae8a-73e64ae0ed8a | intent | praise | unclear | praise | True |
| 3d47bb00-de10-4069-a58e-5c8615648440 | topic | other | downloads | other | True |
| f2ee4586-9667-40cb-bde0-dcdb0bf63619 | severity | 3 | 1 | 2 | True |
| 03d3fd25-1daf-46d5-aa8f-f248a2815d70 | intent | complaint | cancellation | complaint | True |
| d42943c7-58cd-4518-b9b6-dd002e3ec960 | topic | usability | access | billing | True |
| c3fb1945-1cae-40e0-8c24-ded4094b86d7 | severity | 1 | 5 | 1 | True |
| fa65b646-0068-417d-9a22-5512b88f7956 | intent | complaint | unclear | complaint | True |
| dbe0a781-a1d1-44ec-a442-306d65729c00 | topic | other | playback | other | True |
| 3393c703-7ebf-43c9-aa0d-91b2f892dd07 | severity | 4 | 1 | 4 | True |
| 556ecb0a-7109-4150-b88b-4247d6b09acd | intent | praise | cancellation | praise | True |
| 844987e8-a6d5-4c1b-a2e4-f819be06aa7d | topic | other | billing | other | True |
| afd82b05-d873-42e6-a4e8-b15632704f2a | severity | 3 | 1 | 3 | True |
| 8443b4c1-9c55-4318-9b0a-06ad2a4ed20f | intent | complaint | request | complaint | True |
| a4736a25-1bc3-4147-9d8d-3425ea62ff21 | topic | other | usability | other | True |
| ecfdcc45-8740-4132-b337-b48541d2445e | severity | 1 | 5 | 1 | True |
| 9c1ba7bd-0a68-43d5-b6a2-4f721651342f | intent | complaint | cancellation | complaint | True |
| 49af0bc1-744e-48c8-a1fb-3b42dfbfeb93 | topic | billing | playback | billing | True |
| 0358c078-3675-4d90-a2d1-2424ea0bcf97 | severity | 1 | 5 | 1 | True |
| 16ff5620-e534-4836-bc3a-c575ca93c5ca | intent | praise | complaint | praise | True |
| 5dce4886-0eab-42ad-8125-24b8de56af6d | topic | catalog | billing | catalog | True |
| 7dbfd988-9152-488f-8a81-b7baa7cd88f5 | severity | 1 | 5 | 1 | True |
| e00b6d60-50b5-4cef-a5a2-612e26a3570b | intent | complaint | praise | complaint | True |
| 98c466d7-9fbd-49fb-8fcb-5b7a07c20178 | topic | usability | billing | usability | True |
| 3e6ee421-579e-4c9b-bf14-0ed3c0065e53 | severity | 4 | 1 | 4 | True |
| a1dd4050-54e5-4872-a708-72d19239ff48 | intent | complaint | request | complaint | True |
| 0e1bdb1d-aaf8-4397-a834-7f8ad76eea41 | topic | other | support | other | True |
| 492396a1-ba2e-4437-b150-877123ececa7 | severity | 3 | 1 | 2 | True |
| 4d7a9175-fde0-46ca-8c1a-ee1eaf024a04 | intent | praise | request | praise | True |
| 8604d557-aee9-4ada-88c9-371b11e1c667 | topic | other | playback | other | True |
| 2d477e7c-588a-4548-ae6d-6ee00d306335 | severity | 3 | 1 | 2 | True |
| e2b98395-b490-4fe7-88b9-2c90d1112b37 | intent | complaint | unclear | complaint | True |
| 5c1f67d8-8bb2-4974-b848-8c78dfefb816 | topic | catalog | playback | playback | False |
| 732cdb3b-9fec-4564-aed5-832604e852f9 | severity | 2 | 5 | 2 | True |
| 8b951807-110d-4e80-8635-1fdb3e4127dd | intent | complaint | praise | complaint | True |
| 95ddab83-9f34-405d-8dd7-72b04cf05234 | topic | playback | catalog | playback | True |
| 1bc5918d-7d1d-4c22-8d02-f5b1e043aeb4 | severity | 1 | 5 | 1 | True |
| bdc082e6-f310-439a-abfc-bba19c42e099 | intent | praise | unclear | praise | True |
| f19ad3ae-68a6-483e-bb79-8ed8423bbfb2 | topic | access | billing | access | True |
| 461ec313-441a-4ffb-aec6-7fb1cb400da9 | severity | 2 | 5 | 2 | True |
| 41c2df6f-3207-4652-af27-fc31503d750a | intent | praise | request | praise | True |
| cb77d6f5-e0bf-4c7c-9a71-3ff832f9896e | topic | usability | playback | usability | True |
| a242f778-aa89-499e-b12a-f2cac8b7130d | severity | 2 | 5 | 2 | True |
| 066faeea-bfa8-48a6-ac75-eb7643cb9e02 | intent | complaint | unclear | complaint | True |
| e3ad31d5-c5db-4b69-81a1-7f76baee24ef | topic | other | downloads | other | True |
| c961f255-52ca-40d3-afe9-5841bd648963 | severity | 3 | 1 | 3 | True |
| 68f165f2-9e06-4739-a698-d4a2b803cf3c | intent | praise | cancellation | praise | True |
| 85656761-eac2-45fa-8519-d5f68746b8de | topic | other | support | other | True |
| 66b21cfa-c0ef-4750-9943-63830f516dc5 | severity | 2 | 5 | 2 | True |
| 3bb1298c-173b-4e5b-bcf5-8dad707260c6 | intent | complaint | request | complaint | True |
| 30dfaa16-dc27-43bc-8d62-c4f9892c77b4 | topic | other | playback | billing | True |
| 2615e156-82ad-4e36-89eb-e2148aaccd68 | severity | 1 | 5 | 1 | True |
| c5707b32-5c14-41a5-bef4-6873aa81f96b | intent | complaint | cancellation | complaint | True |
| e20c8f6c-bfff-43ee-aa8c-c6bd1f34f84b | topic | usability | other | usability | True |
| 602103a3-51d1-4324-b565-87f646c53194 | severity | 2 | 5 | 2 | True |
| 63495200-369d-41f0-ad84-3783346019db | intent | complaint | unclear | complaint | True |
| ac9e57b3-682f-46e1-b731-bef9fec422da | topic | other | usability | other | True |
| 1746250a-d4bb-43cc-88f0-4d4fe882f4c3 | severity | 2 | 5 | 2 | True |
| ab2ee509-a037-460a-9fac-12077bc8b818 | intent | complaint | praise | complaint | True |
| c757c929-4dcf-4923-be8f-cd95bcaa8368 | topic | billing | playback | billing | True |
| 9a8d7339-8c96-41c1-ac39-b69b4f39fd51 | severity | 2 | 5 | 3 | True |
| 36adca4e-f915-40cf-883b-00cf7e5bc51f | intent | complaint | request | complaint | True |
| 8b783e01-7a4b-47d3-ba7b-9508430871f7 | topic | usability | playback | usability | True |
| d6591c11-34ad-495c-b8ec-9d96413b9016 | severity | 1 | 5 | 1 | True |
| 63ba8842-e275-41e8-9e26-6be3af82a9ae | intent | complaint | cancellation | complaint | True |
| a35c3d15-774f-403d-b57f-8cf1bed594b6 | topic | other | downloads | other | True |
| 7d5e739d-8cae-4adc-b932-7db9cf635205 | severity | 3 | 1 | 3 | True |
| be4781b2-9d2e-4e10-8233-b945a924e249 | intent | praise | complaint | praise | True |
| 027058ec-95d8-4543-8039-3764227e9624 | topic | other | support | other | True |
| b6c3dc45-7c95-4b74-b013-8b004763bee0 | severity | 2 | 5 | 2 | True |
| f95a49af-cff1-458a-96a0-ecdb4a12aab1 | intent | cancellation | request | cancellation | True |
| 1ed281fc-7181-4660-a355-1d657f9a4073 | topic | other | playback | other | True |
| 834a0ae5-e8c5-49df-8136-35cc0c7dd6f5 | severity | 3 | 1 | 3 | True |
| e0f07183-3116-499c-bade-c60bdde79bb1 | intent | complaint | request | complaint | True |
| df6ad4e2-c10f-4b9a-9dc2-953d41e13d29 | topic | billing | downloads | usability | True |
| 90d5a05a-e630-456f-871b-b049522fb42d | severity | 2 | 5 | 2 | True |
| 01e934ec-6d63-4fba-851c-0512c041f41b | intent | praise | request | praise | True |
| bd329ac3-278b-4643-b059-2f78d005d6e9 | topic | usability | downloads | usability | True |
| 717a4c8c-47d9-47e8-9e19-b86a44944e6e | severity | 1 | 5 | 1 | True |
| 4a8b8a95-e3c2-4217-a292-37ccfa3371b0 | intent | praise | complaint | praise | True |
| 2899631a-a9b7-4dcb-bca9-7c7e991d51ea | topic | other | catalog | other | True |
| b7b125b2-12b3-45bb-8e36-043dcb449c60 | severity | 2 | 5 | 2 | True |
| 68c078fb-c17f-4bcd-8b9d-1d94d9d06e1e | intent | complaint | praise | complaint | True |
| dae1c7fb-3883-4fcc-84b3-513091229740 | topic | usability | playback | usability | True |
| e3f89cfd-beb5-445d-a0f5-5de862bab326 | severity | 1 | 5 | 1 | True |
| f15a73f4-6800-4fc4-90e5-e91f7d58dcc5 | intent | praise | unclear | praise | True |
| 2b6f26b9-0e2f-4640-b55c-50941cfc2f92 | topic | usability | billing | usability | True |
| a8773260-fcfc-477b-9052-de5414e7bdee | severity | 3 | 1 | 3 | True |
| adbc02e1-beb6-449a-9144-a517de16d520 | intent | complaint | cancellation | complaint | True |
| c70a4aa7-e198-495b-b49f-0f08deb6b1c5 | topic | other | support | other | True |
| b1e546c1-1605-4b17-9bab-559eac78951f | severity | 1 | 5 | 1 | True |
| e1f7e984-b794-4bfd-b3a6-73806cc55b30 | intent | cancellation | praise | cancellation | True |
| 3ec55d53-d640-4a84-af7b-671861cb0058 | topic | catalog | other | downloads | True |
| f679bf7b-8f1d-4e63-be40-fb162f5fc6c6 | severity | 3 | 1 | 3 | True |
| e096f354-b63d-49b6-8feb-00fa5b63555a | intent | unclear | complaint | unclear | True |
| 0e26fff3-736f-4614-b7f2-a0f83443b724 | topic | billing | downloads | usability | True |
| 59b7ffe9-47d2-48df-a383-4ddc7f1de2a9 | severity | 2 | 5 | 2 | True |
| 268012c8-0599-4c90-81e7-cd8e709e7f9f | intent | praise | unclear | praise | True |
| 0ad8e11f-4c4a-4b77-b400-2e383c72ff70 | topic | usability | downloads | usability | True |
| 30ca67b9-c244-4b6e-bcf1-0d82ac66c538 | severity | 1 | 5 | 1 | True |
| ef7aa0ec-d4b7-4660-8cfc-dae860bbc196 | intent | praise | request | praise | True |
| 96f05a01-bd30-4971-9c94-78d29388afa6 | topic | usability | support | usability | True |
| f0700501-0b34-48d1-a989-de2d916cf92f | severity | 3 | 1 | 2 | True |
| 69ce9831-e723-4e63-b0aa-d10f9bf60a3d | intent | complaint | unclear | complaint | True |
| 503f6c80-1546-4cde-9629-1b1dc521d2e1 | topic | billing | support | billing | True |
| b91100a4-f523-42b0-b74a-7808864c8077 | severity | 1 | 5 | 1 | True |
| a0492ffa-5198-4aad-91fc-aa440eb43c5e | intent | praise | cancellation | praise | True |
| f80122a8-b5ce-4b5e-9c7d-1924efdc7b8e | topic | usability | billing | usability | True |
| c60684fe-33c5-47f7-91a0-6c290a7c5902 | severity | 2 | 5 | 2 | True |
| 2ee66224-99b3-4fbb-8563-0f2f256f06a0 | intent | complaint | request | complaint | True |
| 627c3fd7-9baf-478f-b321-ccd2e68988a9 | topic | downloads | playback | downloads | True |
| e072ea4c-c201-4db5-9ee8-b613f52508dc | severity | 1 | 5 | 1 | True |
| 72556ae9-e6e6-40c4-ab0d-61e8bcc52381 | intent | complaint | cancellation | complaint | True |
| 84cb3461-9cbc-4ea1-924f-284edac0d6bd | topic | catalog | other | catalog | True |
| ac034031-6d4d-490d-ad66-7a96b3e61701 | severity | 4 | 1 | 3 | True |
| 57457b9d-e1d5-4b0e-a84d-73de3d289ccf | intent | unclear | request | unclear | True |
| fb60cfff-57ae-411b-bc27-a78d653ca069 | topic | other | billing | other | True |
| 18e631e5-3a9f-434a-9487-bcfe325e889c | severity | 3 | 1 | 3 | True |
| 391cdd01-00cf-4d3f-8b99-3c2c46cb5132 | intent | praise | cancellation | praise | True |
| 78ca2f65-fc86-4a19-a2f6-6f7910db7655 | topic | usability | downloads | usability | True |
| 6c50e432-2aba-434a-b1dd-73de86c6f3de | severity | 3 | 1 | 3 | True |
| 59191da4-93c7-4f20-82ad-3f89409c21de | intent | praise | unclear | praise | True |
| a7875312-aa46-474f-80c6-6eefcdcbf9cb | topic | usability | support | usability | True |
| 3cf36b69-b26d-4add-84dd-81a0793cd061 | severity | 1 | 5 | 1 | True |
| e48f3290-beb8-44b5-acbd-baddd8e34550 | intent | complaint | cancellation | complaint | True |
| b127b23f-1596-40bd-a14d-4e31f98a5ccb | topic | billing | support | billing | True |
| 09cc6c77-6296-480b-aeb1-8ad446000008 | severity | 1 | 5 | 1 | True |
| b3ecf62d-29bb-41d6-b1aa-f2ffd81c0d8f | intent | praise | complaint | praise | True |
| 92b7df5e-72d4-4990-9b70-ede3c1c09427 | topic | other | downloads | other | True |
| 9dcba40a-6f43-4056-acb2-d25d3bb9b1d7 | severity | 1 | 5 | 1 | True |
| ad0313aa-46b3-4203-8786-3dcc60d4a618 | intent | complaint | praise | complaint | True |
| 8db2e85b-7b09-4260-8006-0e7b7ab13be2 | topic | billing | catalog | billing | True |
| 7a2a914b-3215-4764-ae38-8ffb07a3e0f9 | severity | 2 | 5 | 2 | True |
| 87dbd360-7400-44b7-9237-2001c7205efc | intent | praise | unclear | praise | True |
| ec02c40b-45e5-494e-887d-0206ee1e8998 | topic | other | playback | other | True |
| cce42bfa-f986-49e7-93e9-2f6407a862ad | severity | 1 | 5 | 1 | True |
| 95ba6632-7387-4a46-ac3e-856ff8b3f4ff | intent | unclear | praise | unclear | True |
| 349ed340-e3ed-426f-9fe4-9941cff8a737 | topic | other | billing | other | True |
| 044f0ed4-3ef7-4744-a332-e449589eab2a | severity | 1 | 5 | 1 | True |
| 4538b8b4-42b5-474c-b0d4-0ae63b7e217f | intent | cancellation | praise | cancellation | True |
| 72c9842b-f476-4e1b-bf25-d384f80507d3 | topic | other | usability | other | True |
| 3a116966-7584-4db8-a788-12ee589ec4fc | severity | 3 | 1 | 3 | True |
| 4edbb113-4202-4c20-a517-26bcb9a08ca3 | intent | praise | cancellation | praise | True |
| c12f02ea-0a7c-4c95-9a06-9a45bd36f2ef | topic | other | catalog | other | True |
| 681a5be0-d272-4537-8b1d-feb97724ccc6 | severity | 1 | 5 | 1 | True |
| f3797e3e-1b88-4934-8b81-340ab4bebd17 | intent | complaint | request | unclear | True |
| 1e7c7726-6bee-4802-8967-7ea8842c3f5b | topic | other | access | other | True |
| e4718dcd-ceb5-41ae-ac0b-9f8fb5dcad58 | severity | 2 | 5 | 2 | True |
| 01b882dd-5d36-4b78-95da-725d13d00c08 | intent | complaint | cancellation | complaint | True |
| 440c0c22-7277-46b7-a2fb-03a67d7c4e32 | topic | other | downloads | other | True |
| 72fc7b1b-4fc2-4cca-a3de-f1e4a9e95ffe | severity | 1 | 5 | 1 | True |
| 73f1a35f-7b89-4e60-b528-ea0b8d298067 | intent | cancellation | praise | complaint | True |
| 5040873e-db2d-4193-a724-b4462b2968d0 | topic | other | support | other | True |
| e5f29539-9180-4e5a-94ae-c1427f5fccd3 | severity | 1 | 5 | 1 | True |
| 69f5c3f0-a0dc-4539-aa75-78ad2da4ceaa | intent | praise | cancellation | praise | True |
| ce5a24ea-0526-4a95-a2e4-e5c983dcf33a | topic | other | playback | other | True |
| 1ffafd76-bbd0-4fac-9fd6-0a8a477c9882 | severity | 3 | 1 | 3 | True |
| bf634c6c-7dc1-45f0-ac5c-9e0f9a1c8f64 | intent | complaint | request | complaint | True |
| a9c4b138-2c09-42be-a2c7-82335721cbcc | topic | other | billing | other | True |
| fb57da0a-c2c8-45fd-a46f-60867e280992 | severity | 3 | 1 | 3 | True |
| fdfa793b-c471-4d33-9c4e-1cf79c102c8c | intent | complaint | cancellation | complaint | True |
| 780de029-6836-4ff4-a7b4-422f41af0bce | topic | other | usability | other | True |
| 064d4d1b-916a-4291-b0b2-2afd7cb784e1 | severity | 2 | 5 | 2 | True |
| 6b716cb2-4c97-4d89-91bc-0dacc6a1cd42 | intent | complaint | unclear | complaint | True |
| 0134371e-3198-46d0-87bf-614db6ac8e6d | topic | other | catalog | other | True |
| 39f74f83-8ad5-452b-9243-3ff845cc3f73 | severity | 1 | 5 | 1 | True |
| aaf37034-b23c-4177-ac70-f16470df65a5 | intent | praise | cancellation | praise | True |
| c71352e6-4774-46c8-8b05-d5a308534cdd | topic | playback | downloads | usability | True |
| f34b0b3d-f718-4bd7-85c9-c6bbefcbf640 | severity | 1 | 5 | 1 | True |
| c550ef5d-1619-44c5-8dd5-a3e86d563a91 | intent | praise | unclear | praise | True |
| 541a4eab-f5f2-458b-abac-50da11eaf07f | topic | catalog | access | catalog | True |
| b1621bf2-fbdd-48ed-b434-f7504b1539c1 | severity | 2 | 5 | 2 | True |
| 72865a7e-3317-4a4a-9d42-80650b748664 | intent | praise | request | praise | True |
| efb39daa-19f2-4184-b3e6-c201b134f8bb | topic | playback | usability | playback | True |
| 640dad66-b371-4e33-a92b-0d851334f4eb | severity | 2 | 5 | 2 | True |
| 56f59df0-3480-4ebc-97ef-3cfa2c44d531 | intent | praise | complaint | unclear | True |
| 0f659a3d-c79f-4264-837e-e79cd1b650e8 | topic | usability | catalog | usability | True |
| 0b7d8ddf-2bf5-4026-91b6-631d6addd6b4 | severity | 1 | 5 | 1 | True |
| 8a38eea2-6c9a-43e1-aec5-18d7383b2101 | intent | praise | cancellation | praise | True |
| 2c28ff00-4f64-4da9-9a17-4a53bc58b786 | topic | access | support | access | True |
| fe1fa727-9362-4a25-9f75-6033bcc4fece | severity | 1 | 5 | 1 | True |
| 80a552c8-2e67-4681-baf2-516690fda74b | intent | complaint | request | complaint | True |
| 82b0ca3d-14bb-4803-9b1b-60eab5ba986e | topic | usability | downloads | usability | True |
| e323dd32-fd86-405f-b1f1-965ab58e5a8a | severity | 3 | 1 | 2 | True |
| e3d85377-419c-4fbe-a930-9d0f37fd6e70 | intent | praise | request | praise | True |
| 1ce02af0-b491-4a7c-9079-890bee2c5b46 | topic | catalog | usability | catalog | True |
| 67465fe0-d64d-4c94-adfb-c18cf5b17558 | severity | 4 | 1 | 3 | True |
| 59d3ede5-d9a5-4dea-b873-e39091d581fd | intent | praise | complaint | praise | True |
| 2b0d24e3-db9b-4e5f-80f1-f097362675af | topic | other | access | other | True |
| aaa6882e-0e8c-49ca-b18c-0d0df524df8a | severity | 1 | 5 | 1 | True |
| 4a6c9774-2f97-4990-ba50-c0ce650b2518 | intent | complaint | praise | complaint | True |
| 4f353a3a-c11b-474f-b738-4e0ff3de1793 | topic | other | downloads | other | True |
| bc63ddc0-8f46-40a9-8db8-548a4b47190d | severity | 3 | 1 | 3 | True |
| 5e83cf35-83c1-453e-b13b-6edb2787081b | intent | complaint | request | complaint | True |
| f40c8899-de3e-4b9c-88d8-6aeb8504c2a2 | topic | other | support | other | True |
| de6e8632-67c0-4b0f-8b90-f74262c85b22 | severity | 1 | 5 | 1 | True |
| 572b90e4-72b9-4fdd-8f05-b75fff1f7073 | intent | complaint | cancellation | complaint | True |
| cdd9f2ea-0d02-44ca-8534-c1bfae329056 | topic | catalog | other | catalog | True |
| 47f6c0df-3dfd-4ffe-837e-0a39f8ffb720 | severity | 3 | 1 | 3 | True |
| 19bd0b41-437a-4837-b6b3-2b5251f9dddc | intent | complaint | unclear | complaint | True |
| 11508fa9-1e7a-4b5d-a3aa-40169046dfe5 | topic | usability | other | usability | True |
| f42af116-2c67-4ae9-8d57-575fdc0fb7ac | severity | 2 | 5 | 2 | True |
| 2aa1c0b5-7962-42ce-b39c-a0a6327d4369 | intent | complaint | praise | complaint | True |
| 97435998-d843-4b28-87e1-bab16c9d64a1 | topic | other | usability | other | True |
| 77ff56c0-9f0c-4c91-9304-7771090e166f | severity | 1 | 5 | 1 | True |
| d99d47c3-c3f2-40a1-a83b-a98dc6462c49 | intent | praise | unclear | praise | True |
| d7c5b421-c4df-44b6-aab3-97724e2651b8 | topic | usability | support | billing | True |
| 88a0a603-2308-48c7-8c20-763a0957b215 | severity | 1 | 5 | 1 | True |
| de22a2fc-cdd8-439a-905b-2cc5d4807ff1 | intent | request | complaint | request | True |
| 07f84395-3a7b-493b-b223-03049223bd66 | topic | billing | support | billing | True |
| 07ba5ebd-3adb-44df-ba20-615f09b32191 | severity | 1 | 5 | 1 | True |
| ba14a07d-6f37-43a6-a38f-b08d71a24c6a | intent | unclear | request | unclear | True |
| 6d00c70c-45b3-4318-951a-fd7704451340 | topic | other | downloads | other | True |
| f5b1e3c7-2346-4013-a466-c075781efdb6 | severity | 3 | 1 | 2 | True |
| 13bc1bdc-644d-4be5-a948-9d7483c8110d | intent | praise | cancellation | praise | True |
| 8d49670c-a479-4cb3-b5d8-1f0c93581b5b | topic | other | support | other | True |
| 604277de-8e3e-43ec-b3eb-d926b08f8423 | severity | 1 | 5 | 1 | True |
| 408f3ff5-3acb-413e-bf7b-26217174b209 | intent | complaint | request | complaint | True |
| 4c729ce0-c7e6-4026-b4ec-b44577766d51 | topic | usability | catalog | catalog | False |
| 746d99f8-1c84-4f9a-bcf6-7f45d609a4d5 | severity | 1 | 5 | 1 | True |
| 183d31b8-62e8-41b2-a634-31adc59d8d75 | intent | praise | request | praise | True |
| 7eb9da54-e043-4bb8-8c02-9041345a3cbe | topic | other | billing | other | True |
| 0ade8145-9f10-4f59-954e-7a6db1cd0219 | severity | 1 | 5 | 1 | True |
| 48a48022-9af6-4096-9c46-8d90caa14a61 | intent | complaint | unclear | complaint | True |
| c2d8d99f-46fb-4cb1-ab20-07b0cb4689d3 | topic | other | usability | other | True |
| 79694b14-5b24-4f66-a5cc-bafc421c12b0 | severity | 3 | 1 | 2 | True |
| ed64ca6e-7197-4f03-90a5-e545d73d476f | intent | complaint | praise | complaint | True |
| 02c18b1f-abdf-440a-a48a-aa1f9ec375c2 | topic | usability | support | usability | True |
| 708bc543-a7ae-4fec-bfb8-2787825ba295 | severity | 3 | 1 | 2 | True |
| 7167313c-241f-4555-8cd3-18ae5eb5fb52 | intent | complaint | request | request | False |
| e53a6c27-a3a0-477b-9485-3cd666e8b416 | topic | playback | downloads | playback | True |
| de4e920b-a17b-4a41-9782-ae7d4cf95431 | severity | 2 | 5 | 2 | True |
| 1fbbe37e-bc74-44e0-bd8f-0f5a317b642b | intent | unclear | praise | unclear | True |
| 83bf81da-2481-423b-afd3-dbcd24a5faa3 | topic | billing | usability | other | True |
| 59e372fb-8458-404a-a937-ae84fbbe961c | severity | 1 | 5 | 1 | True |
| b55c5f0a-58f9-4ca6-91f9-407910f261f7 | intent | praise | complaint | praise | True |
| fe9e1142-be1c-4f12-8f5f-7a9aecdb1a25 | topic | billing | catalog | billing | True |
| d2f2f760-f77a-4025-90ad-afd36dbe584e | severity | 1 | 5 | 1 | True |
| c78e2b1e-01fd-4811-b779-1718f20e7ea5 | intent | complaint | praise | complaint | True |
| 4b0a5d0e-d3af-4283-ae44-85c10c01c559 | topic | usability | catalog | usability | True |
| 103a88ce-7592-4dd5-888e-cb42345387f2 | severity | 1 | 5 | 1 | True |
| 775f085d-f2cf-413f-aa16-5fcbc3e6f63c | intent | complaint | request | complaint | True |
| 8c481a92-34f8-4a74-8f03-a800c57010f1 | topic | other | billing | other | True |
| 2b9372eb-7c02-4a64-bd69-fc65942bd5d0 | severity | 3 | 1 | 2 | True |
| 3ada93e5-79a9-4c9b-ad90-f92ac8856e5e | intent | praise | request | praise | True |
| 669b741f-4e8b-459e-a339-9aae29a7915f | topic | other | usability | other | True |
| fa35b3ab-4158-4a1a-b706-605c758fab62 | severity | 1 | 5 | 1 | True |
| b574daec-4134-4a88-84ed-a56da3f8f16e | intent | complaint | unclear | complaint | True |
| c557d9cd-85a0-4d71-9f23-34018a21d0be | topic | other | catalog | other | True |
| 8541c4d8-e3b9-499d-aafe-b13b19aa015f | severity | 1 | 5 | 1 | True |
| d787fac1-0210-4c17-b741-a7b7580cd061 | intent | cancellation | request | cancellation | True |
| e2f6660a-bc1e-4938-a0bd-cca8c45361c1 | topic | other | access | other | True |
| 21ee6038-7367-4f2e-a02d-4a5242631346 | severity | 1 | 5 | 1 | True |
| cf5b42f7-8d21-47bd-9d46-8a6b48a3b90e | intent | complaint | request | complaint | True |
| aa222bc5-085f-4df9-9232-f257e6081c3c | topic | other | downloads | other | True |
| 1187d87a-0e2d-4a2d-a64f-61456fae67cc | severity | 2 | 5 | 2 | True |
| 1650b245-213d-4d81-bfbb-0004182689ee | intent | praise | request | praise | True |
| ba32e8d2-d3b6-4a49-a8f5-f3aa4aed041c | topic | billing | catalog | billing | True |
| 3b5605ae-0529-4fde-8715-1648ce120862 | severity | 1 | 5 | 1 | True |
| 9f27dace-25f0-4626-bbc6-6be99f7b2e84 | intent | complaint | unclear | complaint | True |
| a68c40bb-e4a2-4284-bc91-b1d445a0f53e | topic | billing | access | billing | True |
| eb1f02c5-317e-4aea-b0d4-622cfdbfd9a4 | severity | 3 | 1 | 3 | True |
| 7249e791-ba30-4abc-b8e2-4a56e885ad3a | intent | complaint | praise | unclear | True |
| 4f975206-8531-4844-983d-b3ec2a2773eb | topic | catalog | playback | catalog | True |
| 201f85a6-7734-476b-9739-0f9e492e06e9 | severity | 1 | 5 | 1 | True |
| 0cd74926-335e-4a5f-8c75-d5b8414471c7 | intent | complaint | request | complaint | True |
| 0f72a94f-546e-45ce-b9c6-74cf9072f2e4 | topic | other | usability | other | True |
| 3ffab298-a326-43e9-b954-5099885e1eef | severity | 3 | 1 | 2 | True |
| e36cc761-ee14-4d82-b461-989ee4723fbb | intent | complaint | cancellation | complaint | True |
| dc0d64c9-ebd2-4c43-9a65-977951ffb53c | topic | playback | other | playback | True |
| 8a2790f0-9e00-4a3d-9630-832b89693e78 | severity | 3 | 1 | 3 | True |
| 170f6756-8303-4d68-92f5-8c301b7a8ace | intent | complaint | unclear | complaint | True |
| 9f109e0b-6ae7-464f-9bf6-c52e3595bbf8 | topic | other | access | other | True |
| 8d21fbab-61e6-4a6c-bec6-dc9894f84e98 | severity | 1 | 5 | 1 | True |
| e965cbd3-6cca-44de-bd8d-999cd559eb84 | intent | request | unclear | complaint | True |
| 53362b6a-cb58-4da4-9b0a-605e7e36d3b0 | topic | usability | billing | usability | True |
| 13e0c0b1-461f-43f3-9202-3668e4124dfd | severity | 2 | 5 | 3 | True |
| fac0fcee-eda1-4fb7-b083-43cd17693d5b | intent | unclear | cancellation | unclear | True |
| aa64b4f4-7d50-4a87-a2bf-a4cfc8c33711 | topic | playback | usability | playback | True |
| cdb83af0-0e8b-41d0-9410-8cf0428e1699 | severity | 3 | 1 | 2 | True |
| e0eecf6b-2487-496f-873b-89e9c2806759 | intent | praise | request | praise | True |
| 40ffd17b-0820-4a6b-95cf-c0fec4eb24c9 | topic | catalog | other | other | False |
| a4e38e75-1d1e-4b25-83c9-927f67e04103 | severity | 1 | 5 | 1 | True |
| edef95a2-df25-4753-8403-9ef1d54cedd3 | intent | complaint | unclear | complaint | True |
| d5583d07-d0f6-493a-8527-f521e2cfd254 | topic | usability | other | usability | True |
| 9c32f1f1-38de-45be-b9b7-afaa567a86d8 | severity | 3 | 1 | 3 | True |
| 018a6fb9-7a65-4faa-8ab7-350d154a0b21 | intent | cancellation | request | cancellation | True |
| e067963d-028f-4cd9-a05d-c788bb0ecac6 | topic | other | usability | other | True |
| e2f15cdd-ba54-427e-8cc9-e9fc03d2c82d | severity | 1 | 5 | 1 | True |
| 0e5e0d66-80f7-46d0-8c1f-0a4b521f2e27 | intent | complaint | request | complaint | True |
| 2056a41c-e62d-4032-8835-759c9b17e65c | topic | billing | playback | billing | True |
| bfc2929e-d73e-4fbe-b75d-c9e6067845bd | severity | 2 | 5 | 1 | True |
| 266fdbe9-ff3f-4928-a7b5-bad92b386155 | intent | complaint | cancellation | complaint | True |
| c88667d3-8831-447b-a42d-e785e8094cc1 | topic | billing | support | billing | True |
| 9221932c-3b35-4804-897e-8346d6dc4f87 | severity | 1 | 5 | 1 | True |
| f1d91114-bce2-44c4-ab31-74644e0ff90d | intent | complaint | unclear | complaint | True |
| bbc97f8e-8c4a-46dc-916a-ab23373973be | topic | playback | support | playback | True |
| b0591db9-c097-4362-9b68-41cf84aa02b9 | severity | 3 | 1 | 3 | True |
| cba17a1f-d9f2-4c7a-a673-9df9febf02b9 | intent | request | unclear | unclear | False |
| 3f42bc85-c2fd-47b6-baf5-bdbfcaf237bc | topic | catalog | downloads | other | True |
| 3dc167cd-942d-4c48-a48a-aa7a71861dcb | severity | 1 | 5 | 1 | True |
| 04046170-43b2-4ce7-9f64-8105704c6468 | intent | praise | unclear | praise | True |
| fd9789e9-4f54-4c0f-830a-fca0f5d87f5e | topic | billing | access | billing | True |
| ae9ed310-ede2-4df9-9698-461ff010f377 | severity | 3 | 1 | 3 | True |
| 912c5a3f-be17-417f-8d76-a33cde076f58 | intent | complaint | cancellation | complaint | True |
| 3d0e0e0e-e1b6-4eb2-b259-c71063d9ac3f | topic | other | billing | other | True |
| 1ccb0d41-53bd-43c9-84d3-28d07ce60c6d | severity | 3 | 1 | 3 | True |
| c7de67f9-4af7-4f27-a08a-e5a96ba8a13f | intent | complaint | unclear | complaint | True |
| 58541fbb-b102-4f28-8027-ce6bf8dcb954 | topic | other | usability | other | True |
| 6e55e944-3a4a-461f-bf08-75c120dfa50c | severity | 2 | 5 | 2 | True |
| f81b2c38-a47d-4296-984b-3a9f7b13736b | intent | complaint | praise | complaint | True |
| 2d4353d0-7418-43c2-ad2d-1b2dc23c3f70 | topic | other | catalog | other | True |
| 426c7e03-0285-42ed-bf97-0b05cca626f3 | severity | 3 | 1 | 2 | True |
| d0864f83-decc-48c4-a47d-55c2d8661d30 | intent | complaint | request | complaint | True |
| 5489910d-a6aa-4a31-b61c-3c63c2fee42e | topic | other | access | other | True |
| e2c989be-2e7f-4beb-8f15-a0dffc637d45 | severity | 1 | 5 | 1 | True |
| 896ac32b-572c-41e1-b9ad-93c8138b8072 | intent | complaint | cancellation | complaint | True |
| 74c9bb31-b0be-48b0-9892-2fa8934df4c3 | topic | catalog | access | other | True |
| d5f282a7-4752-47aa-85b0-3ae6905063a2 | severity | 2 | 5 | 2 | True |
| 71436504-e38b-49cb-b58e-7d24241cb6b0 | intent | praise | complaint | praise | True |
| 75fd4b5e-22df-4f60-bc28-bb7ea2f3c45f | topic | other | support | other | True |
| 565f96aa-449a-4fe6-8519-5daee2cd81ae | severity | 1 | 5 | 1 | True |
| 7cee483e-63d3-4a1d-afe8-217cf974203c | intent | unclear | complaint | cancellation | True |
| 07bea8df-a3aa-4540-96b4-056868bab8e4 | topic | catalog | other | catalog | True |
| e73edbac-9ac0-4d8a-b106-662b25cc0b14 | severity | 3 | 1 | 3 | True |
| 499a3772-141d-4628-89c0-ddac72d1fbd7 | intent | praise | unclear | praise | True |
| 67788933-9b7d-4e82-a7df-cb5b1a95dabd | topic | billing | downloads | billing | True |
| 0aea8c71-494b-4879-adb6-578791a33f7e | severity | 1 | 5 | 1 | True |
| 1c026b49-eb0d-45f9-82b7-85334b7469a4 | intent | unclear | praise | unclear | True |
| 22a3e968-97de-4001-9fed-714212c80a7d | topic | other | usability | catalog | True |
| 4c165ae6-baac-4053-81b8-41d1f671a470 | severity | 1 | 5 | 1 | True |
| 6274bc9b-4e35-4d13-9aa4-ddcc1e70aa71 | intent | praise | complaint | praise | True |
| 8296fa13-e092-4acb-8d8f-684150759776 | topic | access | billing | access | True |
| 8677a17d-dd24-414c-961a-4d56238acc59 | severity | 3 | 1 | 2 | True |
| 9bba0661-e160-4272-a7e1-6d7942889db3 | intent | request | unclear | complaint | True |
| cdac6ddd-979f-440f-8f0f-5e05280d92a5 | topic | usability | playback | usability | True |
| 6e7253bc-6749-4c78-9d51-6bb8672758ac | severity | 1 | 5 | 1 | True |
| 356a4de0-a5e1-42ea-b68d-a7c971d2b677 | intent | cancellation | complaint | complaint | False |
| 42283854-e0e1-4397-97e9-02ad957609da | topic | other | downloads | other | True |
| a883d6fe-4216-4d87-841b-f2f40267c9c6 | severity | 2 | 5 | 2 | True |
| b57d8256-cd4b-4871-a899-f9dd3b53b630 | intent | praise | request | praise | True |
| 2e82f1ee-538b-4ede-8744-d3430bfd8303 | topic | usability | access | usability | True |
| f00c8679-c9ac-4e9b-8cab-b401fc05a1b4 | severity | 1 | 5 | 2 | True |
| 580ba88c-94b0-44bd-b436-8dd2815daa6e | intent | praise | complaint | praise | True |
| 79ddb624-5b43-4f8e-a75c-503262bbd63c | topic | usability | catalog | usability | True |
| 269f21dc-ffdd-4ad6-a119-b23af52352b7 | severity | 1 | 5 | 1 | True |
| 4d8ae185-05ed-447d-948e-d42606ca693d | intent | praise | cancellation | praise | True |
| b1f07892-dc5b-4c8d-8a50-eb2e7b0f72dd | topic | usability | other | usability | True |
| a0f1357b-ee7d-4bf7-8f57-d5e5e3837107 | severity | 2 | 5 | 2 | True |
| d3cd1c0c-815b-4e8f-8bba-6bca98f32d19 | intent | praise | unclear | praise | True |
| 3012a3be-cac0-4c7b-9e4f-90a16e3827c5 | topic | billing | other | billing | True |
| 635fbc9d-7d8d-47ff-b502-40753cdbad3e | severity | 1 | 5 | 1 | True |
| 570a1d6a-9e76-45a1-b1e1-1361a5afa8d9 | intent | complaint | cancellation | complaint | True |
| 7ee65321-1ba4-43f7-933d-964610ecb809 | topic | other | catalog | other | True |
| 6fb13378-6e0b-4b86-a3eb-df39e5179d88 | severity | 1 | 5 | 1 | True |
| decd414c-e51a-4440-9525-f3e7c9e5d291 | intent | complaint | unclear | complaint | True |
| 1b807418-ef98-4206-b285-bd27439e1d2e | topic | other | access | other | True |
| 28d4e961-c1fa-4fc4-b170-cedf002cb721 | severity | 2 | 5 | 2 | True |
| 39f5bfc9-e9f2-4298-92e2-8c3a27161d89 | intent | praise | cancellation | praise | True |
| f6e7e20d-ed73-4904-a2d7-3db01eda931f | topic | usability | billing | usability | True |
| f8f78610-b4e8-4432-91a9-827fec588ea7 | severity | 2 | 5 | 2 | True |
| dabaf5e4-6809-46f4-9263-e9a192e45c91 | intent | complaint | request | complaint | True |
| 7f139568-7ae9-4c1e-b4e5-668e3d3ce244 | topic | billing | catalog | billing | True |
| 8f9fcd2a-fe0f-4b07-8caa-47f641adb9af | severity | 2 | 5 | 2 | True |
| bbef4418-d5b8-4b2c-9c99-6f92709077e7 | intent | complaint | cancellation | complaint | True |
| 5bcb663a-8b47-4da4-b875-33ab7a6b9f32 | topic | other | playback | other | True |
| 8f6c4322-3f2e-4a76-b2f6-eaeb0718d486 | severity | 1 | 5 | 1 | True |
| c41e8470-ff48-48fa-aeaf-bf165cfe7889 | intent | praise | complaint | praise | True |
| 26c4ccee-f836-4403-bb73-35cf5fe28949 | topic | other | billing | other | True |
| 78693fe1-2453-4850-ad94-0daf49c24fb7 | severity | 1 | 5 | 1 | True |
| 2d65ea48-8483-4d6c-a4ce-d90b05a57e75 | intent | request | unclear | request | True |
| ed329826-9bef-4f06-a49b-0fa3eb844102 | topic | billing | other | billing | True |
| 7067dede-7d5e-4ad8-bb1b-16d0e32f8895 | severity | 1 | 5 | 1 | True |
| 9a1fa877-34a0-48d5-aebd-814210734a01 | intent | complaint | request | complaint | True |
| d9253f2c-4187-421f-971b-a2157b615c18 | topic | other | catalog | other | True |
| df381a96-2ee8-47d5-8b3a-de9f43ee847b | severity | 2 | 5 | 2 | True |
| 81cf3873-ca60-4ff0-b57f-9c905563c877 | intent | complaint | cancellation | complaint | True |
| 0d361ea6-3089-41c2-9e0f-4cd6a04f0dd8 | topic | other | access | other | True |
| 7ab8cfdb-9928-4dfb-9f03-c795e0c1afec | severity | 1 | 5 | 1 | True |
| 219a4bdc-8892-40c6-8409-6fea1105693c | intent | complaint | unclear | complaint | True |
| c23ae4f7-916e-49f3-b248-3f6be0737874 | topic | billing | usability | billing | True |
| ba8df0e9-4db7-478c-92f1-b4f974dcfafe | severity | 2 | 5 | 2 | True |
| 134c483d-91ea-4f9e-afec-c4f8af54f83c | intent | complaint | praise | complaint | True |
| fd9b0f82-bcee-46d6-9288-06c93d3f5040 | topic | usability | access | usability | True |
| ca5981e9-7310-47ef-a922-3c4ca15b8d33 | severity | 2 | 5 | 2 | True |
| 46326e74-b47d-4bde-b860-ef1018549a48 | intent | cancellation | complaint | cancellation | True |
| 6dabed25-e32e-4287-9f21-4381c16a9085 | topic | billing | access | billing | True |
| 8c1f8566-75af-4be7-bc22-ea5aebf0f7ff | severity | 3 | 1 | 3 | True |
| a7b0309c-6e97-4f7f-84f1-e882fec757ae | intent | praise | request | praise | True |
| 8c0e9938-48c2-4ef4-a494-946ce59cdfaf | topic | other | billing | other | True |
| ff390581-ea9f-40d5-8b3e-f6b07212a08b | severity | 1 | 5 | 1 | True |
| 7c3469a2-353d-4bb0-a5e4-6580e2c9c1fd | intent | complaint | unclear | complaint | True |
| 5e23c05c-cfd9-404e-a329-7342e88f7ca4 | topic | other | usability | other | True |
| b0c4fc8c-a60c-4863-a12a-2fc8a8a90e63 | severity | 3 | 1 | 2 | True |
| 103cf67a-5e31-4fbf-a68a-239f89375eec | intent | complaint | praise | complaint | True |
| f83eccef-d5fb-4673-8a71-bd31f66bbbe7 | topic | usability | support | usability | True |
| eb961763-f88f-444c-bc54-f69b65bd5d55 | severity | 3 | 1 | 3 | True |
| af0daf1d-da2f-4600-b5e3-a7de5e73c0dc | intent | praise | unclear | praise | True |
| d2e6c4dd-e769-4b04-88e3-54d67801bbe7 | topic | billing | support | billing | True |
| fe883ac9-15f2-4730-ac1f-072be351b763 | severity | 2 | 5 | 1 | True |
| 3e84bf4c-a0af-4aa4-9ed0-41165060159a | intent | unclear | praise | unclear | True |
| 600d54e6-c55c-4cbe-9005-e52bdc695e65 | topic | other | downloads | other | True |
| 150e8a71-7e6d-4eb4-b866-4626246a1c30 | severity | 1 | 5 | 1 | True |
| aa5f1215-8e16-4ae9-ba64-182af40d6036 | intent | complaint | unclear | complaint | True |
| 7295e8e0-626b-49e3-9e1d-598beb9a9082 | topic | other | support | other | True |
| d84a82e7-2ea9-4aee-9adf-b5e2b7ae656c | severity | 3 | 1 | 2 | True |
| 28124287-e59a-473d-8ad4-cb09ec350cf1 | intent | complaint | praise | complaint | True |
| 4e956c1f-5418-4c86-b671-061055a295aa | topic | other | playback | other | True |
| fcd209ee-6f0b-4e45-b865-bc9d75f7b127 | severity | 2 | 5 | 3 | True |
| cb2c2bbf-ffee-46c7-837c-cd64d1140f50 | intent | complaint | request | complaint | True |
| a823beed-143c-4535-80fd-f10a3b8992a5 | topic | billing | downloads | billing | True |
| 27173e8e-560e-4b4e-95c3-81cd807d49c6 | severity | 3 | 1 | 2 | True |
| b22f04ff-504b-4bd5-ba94-759ef58f7fc9 | intent | complaint | cancellation | complaint | True |
| 3283e743-a79b-4390-a4f5-1115b96d83e6 | topic | other | usability | other | True |
| 7e84c02c-a28b-483f-a5c6-bf4052bdbbfb | severity | 1 | 5 | 1 | True |
| e7992ef1-119f-4ad8-8afd-a6d9742d6be0 | intent | complaint | unclear | complaint | True |
| d044eeb8-c991-4a4a-86f9-b3aab0e97b02 | topic | catalog | usability | catalog | True |
| 5d5eff94-c08c-4638-a588-82b7bbbee148 | severity | 1 | 5 | 1 | True |
| 5b650e42-c328-42cd-a9d5-05aeb1bcabdd | intent | complaint | praise | complaint | True |
| 585bce4e-f621-4fbc-961f-6a02438de912 | topic | usability | playback | usability | True |
| b0a57f61-03e0-402a-93c9-d37aafe49df7 | severity | 1 | 5 | 1 | True |
| a75bda02-8d11-4e07-9ef8-176064cd4b63 | intent | complaint | request | complaint | True |
| 1af1ada5-96a9-4592-8801-c9f65b19554c | topic | downloads | other | usability | True |
| 6d99c5e6-f14e-4ea2-b759-f09de8c4683f | severity | 2 | 5 | 2 | True |
| 5b57a101-42fc-4dd6-bf86-de1f8720aa85 | intent | praise | request | praise | True |
| f1e6d6d7-f15f-4b93-8c6c-04d0f17e827b | topic | other | support | other | True |
| 486f3f7d-b223-4963-9391-dd60f1d58615 | severity | 1 | 5 | 1 | True |
| 35971978-c18b-46cb-b804-32cdfc15650f | intent | complaint | unclear | complaint | True |
| 061206d3-d0ce-48df-93e7-32a3275104e0 | topic | catalog | other | other | False |
| cbf92d8e-a735-4829-a04c-d2bb3f924ee1 | severity | 1 | 5 | 1 | True |
| 5f7f950c-cd45-4ae1-9680-19217944a031 | intent | complaint | praise | complaint | True |
| 1817f2ae-2d69-4318-9e6b-5ca9f172175e | topic | other | billing | other | True |
| 78f730b8-a70d-44a9-9ce4-a0f53dea2577 | severity | 1 | 5 | 1 | True |
| 6587f338-8f46-4574-9258-b9c5e0342890 | intent | complaint | request | complaint | True |
| 99586e83-90bb-4f6e-8f89-ba1e9cb2dd86 | topic | usability | downloads | usability | True |
| 35e83902-9362-4f5a-ad30-2aed8b742233 | severity | 2 | 5 | 2 | True |
| 5eb487ba-5205-43a5-877e-200dd07e3b82 | intent | unclear | praise | unclear | True |
| 69118058-9209-4479-add2-684ddde152a8 | topic | usability | support | usability | True |
| 9ef30dff-c655-4cab-9b95-9d0c8345e509 | severity | 2 | 5 | 2 | True |
| 84d62ea6-8b4e-4710-b324-e92bb53b9720 | intent | praise | complaint | praise | True |
| 01e092ee-92fd-44d8-901d-c50a1aae5108 | topic | other | access | other | True |
| f16fedfc-51bf-4257-9a55-ab2a624f1ee1 | severity | 4 | 1 | 4 | True |
| a42b33fe-19f2-4d35-bc26-6a229dd63955 | intent | complaint | praise | complaint | True |
| 5d00a0fd-b169-4128-bbac-0cd66a69720c | topic | playback | support | playback | True |
| e239af92-de9a-4726-9908-d578492ed1f0 | severity | 1 | 5 | 1 | True |
| 6b723a94-bd89-4f63-9cf4-8c8a3b72ba62 | intent | praise | unclear | praise | True |
| 209d7242-bd9d-4ddb-9e97-c9c725aa9a37 | topic | usability | access | usability | True |
| cdf6a760-6440-4127-889b-d6bf462ad568 | severity | 2 | 5 | 2 | True |
| d0b83072-33bd-447c-9dca-e444fa0da4b1 | intent | praise | request | praise | True |
| 86687f97-5b37-4c7b-9fbc-05b1071cd193 | topic | other | playback | other | True |
| 4d5ad3c7-fcb3-4a92-8e26-5c4d042e360e | severity | 1 | 5 | 1 | True |
| 6baf0378-bbc2-48c3-badf-db6958c1882e | intent | complaint | unclear | complaint | True |
| f009d84d-d39c-4141-a99f-7f89f96688d2 | topic | other | billing | other | True |
| afe3b36d-1a5f-4683-b40f-167580f64738 | severity | 2 | 5 | 2 | True |
| bd7cda6b-2f5b-46f7-87ba-8f00aa89fb26 | intent | complaint | praise | complaint | True |
| ea6bb037-dd27-4d1f-9b98-fafbaf14a5d7 | topic | other | usability | other | True |
| 4c363266-24e0-46f8-bc39-41e7e07d296a | severity | 3 | 1 | 4 | True |
| 2949d8dd-8977-45c2-8020-8e4a88fb94d7 | intent | complaint | request | complaint | True |
| c6ed7fca-751e-438f-abe2-82ff98880683 | topic | billing | playback | billing | True |
| 8fe7c61b-7f78-4439-bcf7-8cc092752fc5 | severity | 1 | 5 | 1 | True |
| 3c9a742c-991f-4b33-9f6d-68817f53dcf5 | intent | request | complaint | complaint | False |
| 79f7cb81-527c-46e6-b969-195dfffea20d | topic | other | access | other | True |
| 03fbd0c3-a72d-460e-8781-ae175318af58 | severity | 2 | 5 | 2 | True |
| 08eee679-5b2d-4379-afa1-39d8300310b1 | intent | unclear | request | unclear | True |
| a4d82fa0-9e87-4a75-88c2-7afe121647c3 | topic | other | downloads | other | True |
| b5ea3a8e-5609-4bf0-b35f-cdfefd221fca | severity | 3 | 1 | 3 | True |
| 3b167fba-be43-4caf-881c-a6a31ec20980 | intent | praise | cancellation | praise | True |
| 7ca8a59d-fc62-4946-a8c0-f0f4c5b2494b | topic | other | support | usability | True |
| 30c4322b-cb61-4f35-9c29-82cbc0669954 | severity | 1 | 5 | 1 | True |
| 9a86534c-eb3e-4fca-b02b-4c2d39ea8791 | intent | complaint | request | complaint | True |
| 49923a9f-4a62-4424-91ee-b4f9f81679bb | topic | other | playback | other | True |
| 33004bc3-f4a2-4426-b6f0-399962b294d6 | severity | 2 | 5 | 2 | True |
| 36649bc6-259c-43f1-8475-6a35b33de0b8 | intent | complaint | cancellation | complaint | True |
| 0f213d6f-aaea-4636-ada8-7b7f77e14b9a | topic | other | billing | catalog | True |
| 8c5a63ef-381a-4b8e-acc7-507346509f77 | severity | 2 | 5 | 2 | True |
| edce2ad0-672a-4788-906f-e2dba0c14dcb | intent | unclear | request | unclear | True |
| 8041fd9d-6193-4de3-a042-df01b423c1fe | topic | playback | catalog | playback | True |
| 296b33e6-6824-43f7-8725-74009a73820f | severity | 2 | 5 | 2 | True |
| 1f0115cf-3d73-43fb-8c64-26ef8f83da84 | intent | cancellation | request | cancellation | True |
| d5e31a96-970e-4b47-a368-ac49430f3b92 | topic | access | billing | access | True |
| 3707f118-1f2e-47a6-a945-c1e48772e0b7 | severity | 1 | 5 | 1 | True |
| 3e4ea1c9-9ecc-415b-af14-b7091def0323 | intent | praise | unclear | praise | True |
| 2e142ca6-7d94-4cc4-bfe2-f056cde7939c | topic | billing | support | billing | True |
| afce5800-2b40-418d-a974-c2630ded1802 | severity | 3 | 1 | 3 | True |
| 92532bd5-032c-422d-9079-6a6b2efc9c7f | intent | complaint | cancellation | complaint | True |
| 981d1985-0077-4b23-b067-8805c7b5b609 | topic | other | downloads | other | True |
| b2080e8c-4696-4836-abf6-5465c7363d27 | severity | 1 | 5 | 1 | True |
| e8bee1e5-b0a9-4b0e-8cd0-bbdf675f0057 | intent | complaint | unclear | complaint | True |
| 97ed8527-e3c1-4d11-b060-c28a4d90fa71 | topic | other | support | other | True |
| cecacbc1-fbbb-4cc4-bf54-192ceb5ba898 | severity | 1 | 5 | 1 | True |
| e569be3b-6686-4441-93c9-06e92b1efd13 | intent | unclear | complaint | unclear | True |
| c7bff642-dc4e-4058-ad37-4d1c253ade23 | topic | billing | access | usability | True |
| a0515d46-ec79-4ead-b9ca-17c3cb1e5196 | severity | 1 | 5 | 1 | True |
| f304b004-afbc-4845-978a-c0103e4a1b14 | intent | praise | unclear | praise | True |
| a99d07bf-f881-4e16-bd5d-72f4c2b77d15 | topic | other | billing | other | True |
| dcc1abca-aeb6-45cb-b385-c117432bf062 | severity | 3 | 1 | 3 | True |
| b552038e-a50d-4aa7-9dcc-886ca2dd911d | intent | praise | request | praise | True |
| 9c3a1248-b68e-4a62-97ea-f70aed9a76d1 | topic | other | usability | other | True |
| 5c2e7235-37aa-40aa-802b-ea2423e117b0 | severity | 1 | 5 | 1 | True |
| 43f2b1f1-f7bd-42c9-b239-7365b5e4390e | intent | praise | complaint | praise | True |
| 0ebb65ab-8e07-4322-9b67-1ece9f4af4df | topic | other | catalog | other | True |
| 5d1bc120-7658-4b7e-8df3-7a1b4a9cb041 | severity | 1 | 5 | 1 | True |
| 17ea8fd3-bbad-4910-84a8-e0bff29ea452 | intent | praise | cancellation | praise | True |
| fd47199c-ac0c-49a4-b8be-d5b3dcf8a220 | topic | other | access | other | True |
| dcddbd55-d8f6-43e7-b3fc-6825b15bb11b | severity | 2 | 5 | 2 | True |
| bad6feba-20d5-4892-85ab-fb8651db000f | intent | complaint | request | complaint | True |
| 0bf39ac8-5314-4e6f-a6ab-50a093141dda | topic | other | downloads | other | True |
| 84090917-7506-4a8a-bde2-599b6835c654 | severity | 3 | 1 | 3 | True |
| 1911f37a-e2f2-4789-b97e-da9d9229e0b1 | intent | praise | request | praise | True |
| e3e43c11-6e69-4657-92a9-aa25897e3ea5 | topic | catalog | downloads | catalog | True |
| 16f7d7c0-ebeb-4867-9788-3ea748ddbc13 | severity | 1 | 5 | 1 | True |
| a2f6d08a-e03e-40a3-b5a3-3ef15b1e4c0f | intent | request | cancellation | request | True |
| 085f566a-8bf7-4d8d-b18f-e1a0b5f2d582 | topic | billing | access | billing | True |
| 8bd965a7-8e38-471f-a77d-e8b0d5027404 | severity | 1 | 5 | 1 | True |
| 92c23c7b-1dda-454c-8973-16b4463b8192 | intent | praise | cancellation | praise | True |
| 6d73fb32-b4b0-4c9e-b593-e8d9e632fa4d | topic | other | billing | other | True |
| 1bd8c47a-e769-4a1a-b0c8-f7d1ac3812d9 | severity | 1 | 5 | 1 | True |
| 25f9a9b3-2929-4722-802b-fe662cfe677b | intent | unclear | cancellation | unclear | True |
| 35abb03b-abd4-4a44-8226-4214b2199a3b | topic | other | usability | other | True |
| f0d961dc-4f24-4684-92a0-36f68db238ff | severity | 4 | 1 | 4 | True |
| fa250e8f-b242-464b-84aa-207b68e707d1 | intent | praise | request | praise | True |
| 0dc45ff2-6ed0-4454-9f09-c74023108e1a | topic | usability | support | usability | True |
| 8dcf3b7d-fe7a-4a8b-9b4b-27e6bd3537a7 | severity | 1 | 5 | 1 | True |
| 0c37b23e-e937-4565-8ff4-e477fe21ddfb | intent | praise | complaint | praise | True |
| 004cd387-7d39-4a0d-bc58-9ed4c540b200 | topic | billing | support | billing | True |
| f98a19bc-77d8-4686-b431-49742abf0d03 | severity | 1 | 5 | 1 | True |
| 807e1a23-155b-4d38-8e96-2b2175a19903 | intent | complaint | praise | complaint | True |
| 3d0b6809-ded9-43b5-ae94-ba515d68c436 | topic | billing | usability | billing | True |
| bf915f07-869c-44e0-b710-9983d4be6213 | severity | 3 | 1 | 3 | True |
| 4814a5fa-d4bf-40b8-974b-b0e18e5aa3a0 | intent | complaint | request | complaint | True |
| a83b9531-95a4-4881-b3ff-e2098f29ac50 | topic | access | other | access | True |
| 6b2d0c30-cbca-400b-8d4d-58c10be0ca31 | severity | 3 | 1 | 3 | True |
| c9cf87a8-a97a-4e6d-970e-5ec30b39120a | intent | complaint | cancellation | complaint | True |
| 6f113621-fb57-4ae3-8fc8-50f0af9cadf9 | topic | other | playback | other | True |
| de7101c8-f619-4712-9e01-405740fed9e7 | severity | 2 | 5 | 2 | True |
| 19da7278-4720-42f4-ba49-a3a90e7c7415 | intent | complaint | unclear | cancellation | True |
| 1988442f-820b-45d6-9ff9-848b96f54463 | topic | catalog | playback | other | True |
| 38874d20-4d46-434b-b451-701e2ecbda59 | severity | 3 | 1 | 3 | True |
| 09a631ab-fe58-4f05-96e4-e996f8723bf8 | intent | complaint | praise | complaint | True |
| 76bfe666-137e-486f-9575-5b59e5b72884 | topic | access | playback | access | True |
| a9e7e2fd-26b4-45df-b456-68bdb7537a8c | severity | 1 | 5 | 1 | True |
| 57a50895-bd3a-4fb8-bd98-15c2c8406241 | intent | praise | unclear | praise | True |
| 919e20cd-5270-463f-b029-0fafeebb9e5f | topic | other | catalog | other | True |
| fce59a14-f4bf-4275-92c7-4450d7b180a7 | severity | 2 | 5 | 2 | True |
| 8b91063b-1819-48bb-82bc-be406bf14e17 | intent | praise | request | praise | True |
| 6242a78b-c3aa-4a9b-85b0-36acaa056371 | topic | other | access | other | True |
| d78c963c-70c9-4141-96aa-79a793eb8e12 | severity | 1 | 5 | 1 | True |
| 1e90ca41-057e-4c4b-8ace-208794ad19af | intent | cancellation | praise | cancellation | True |
| accef9fa-e6e0-4995-bfed-94125147c28f | topic | billing | usability | billing | True |
| 5b5efece-0d92-43cb-8704-15b9b114ae05 | severity | 1 | 5 | 1 | True |
| 0e117fd9-a53c-4db6-b2de-769df815e6e5 | intent | complaint | praise | request | True |
| 73cff778-8f9d-458a-99bd-72adefe24552 | topic | other | support | other | True |
| 6fb9e7ba-7e59-4464-995b-e09ccb7d9bec | severity | 1 | 5 | 1 | True |
| d54da0b8-d5ce-434f-bd68-9e5bc783e062 | intent | complaint | request | complaint | True |
| 71215b2b-a91a-4a83-adde-68022e3e3b6e | topic | billing | access | billing | True |
| 425b38b6-c8e2-4dbd-bd4b-bb71eecf50cb | severity | 1 | 5 | 1 | True |
| 7296e19f-0401-411d-af60-15878bde507c | intent | praise | request | praise | True |
| 92019f83-d5bd-4f40-8592-7769e7e92155 | topic | playback | access | playback | True |
| 5239907a-e2b4-4788-af7b-c29cd8ee9a79 | severity | 3 | 1 | 3 | True |
| 1a17fbf1-831c-49d7-9876-f214f8f061fd | intent | praise | complaint | praise | True |
| 5e97bf6e-82dd-4deb-a366-d8c3aaead924 | topic | other | usability | other | True |
| 7fd2552e-65ab-46b1-b9c1-08dca8120b70 | severity | 2 | 5 | 2 | True |
| 419e2ada-b8ce-4d5f-900f-dbdeab99556f | intent | complaint | praise | complaint | True |
| f5027e10-a188-447f-9eb7-6e35fb30be4c | topic | catalog | usability | other | True |
| 809ae547-37e7-4e96-9864-985c8fc22d35 | severity | 1 | 5 | 1 | True |
| 729a759a-0b83-4afc-aac4-e7eab3a057a6 | intent | complaint | request | complaint | True |
| fab269d9-7594-46f6-ad7c-81a9f7c50ccd | topic | other | access | other | True |
| ec169ea8-5ae7-4641-9b3a-336e5ae2a7db | severity | 1 | 5 | 1 | True |
| 990adc65-d92e-43e4-87ea-adc928960256 | intent | complaint | cancellation | complaint | True |
| 6e6059f3-94b0-4154-98cb-681c2cc7617c | topic | other | downloads | other | True |
| 96e9161c-5f95-417f-ad6f-997ce7d097ec | severity | 1 | 5 | 1 | True |
| 09407626-5e51-45a8-86f2-62f15e448ac7 | intent | unclear | request | unclear | True |
| 32eebfbe-4891-4137-a4a8-8b1150deb1d7 | topic | other | support | other | True |
| 05a04ad1-5036-424b-bb38-c648427a627a | severity | 2 | 5 | 2 | True |
| c8f80910-18ca-4af4-96f0-50bbbcbcc2e2 | intent | unclear | complaint | unclear | True |
| 44adc04a-2d07-46cd-ae68-b205de0211da | topic | other | playback | playback | False |
| d4260e76-bca7-48bb-bb6c-80cf4e7f2be2 | severity | 4 | 1 | 4 | True |
| dbad8bc5-bbcd-4701-92a2-9ce5fe5a0b2f | intent | praise | unclear | praise | True |
| 252b6a8b-2519-4176-b1a9-be2346b9ebb1 | topic | other | billing | other | True |
| e63bc361-db6e-43e3-b2d4-12fc493988f4 | severity | 2 | 5 | 2 | True |
| 61afa613-f400-44f2-b517-465f029f2b5a | intent | request | complaint | request | True |
| 2b6abe39-1880-4713-8ba6-97e28d3a25e3 | topic | other | usability | other | True |
| 2f1964f2-ab07-4397-b9fc-2f50dfe47b23 | severity | 3 | 1 | 2 | True |
| 681aef2e-d8ba-49aa-8960-f36589b98b8b | intent | praise | complaint | praise | True |
| 9cec28c9-4f72-4e79-ac8a-ac74da1e1c79 | topic | other | catalog | other | True |
| dd0f0789-85d0-4b83-b58f-e64722be5bbf | severity | 1 | 5 | 1 | True |
| 4b0c0a33-a91a-4e5a-8701-ea9d358211e8 | intent | praise | cancellation | praise | True |
| c2b6b320-eebc-499c-b0b1-a4522efbef4e | topic | usability | playback | usability | True |
| dfa50e19-08bd-45b9-abc7-48c3fdb092bf | severity | 4 | 1 | 4 | True |
| 6973ffd2-6cfc-4492-a073-8857d41268a9 | intent | request | praise | request | True |
| 9bd272eb-fd82-4b23-8e1c-90159bf059f9 | topic | other | downloads | downloads | False |
| ee9a0ac0-e299-42c8-9ee9-90ffbe9b7c9c | severity | 3 | 1 | 2 | True |
| c4671833-7bc0-4c19-80eb-e5cbf085cef1 | intent | praise | request | unclear | True |
| 656c3314-a881-45e8-a172-5072fb5f6e41 | topic | other | support | other | True |
| d752ebc6-a139-486b-9d41-bc8e399c0aa2 | severity | 4 | 1 | 3 | True |
| 187c30dc-05d9-4cf6-bc3d-743e013e0706 | intent | unclear | request | unclear | True |
| e65afa39-9e71-413a-921c-ce43b981d724 | topic | other | playback | other | True |
| 2a123213-83f5-4b0f-a3e8-29ddee56569e | severity | 2 | 5 | 1 | True |
| 96ed9dd3-a5ad-4f03-8128-dfba67bfe713 | intent | complaint | praise | complaint | True |
| e83429cd-0055-426a-ac53-69ef0132c34f | topic | billing | downloads | billing | True |
| b6733978-cbdd-40db-9ca0-edf75d6f52cd | severity | 2 | 5 | 2 | True |
| 94ab6394-899e-4188-85af-97bde9980f3e | intent | complaint | request | complaint | True |
| ec8f0efa-cb17-4769-afb0-6b06c6c4a84e | topic | usability | downloads | usability | True |
| acbbc140-0040-4d63-9d1c-ae604c0645d3 | severity | 3 | 1 | 2 | True |
| 0e80cb31-e6fb-4541-b73b-4f54b7457e6d | intent | praise | request | praise | True |
| 9af69ebc-7374-4613-b10a-3fba12cc033d | topic | billing | playback | billing | True |
| f6a66852-27aa-4b65-bb92-5ff7c550a5d3 | severity | 1 | 5 | 1 | True |
| 2bcd8503-5c72-416d-8beb-737e86d97b67 | intent | praise | complaint | complaint | False |
| 20d57e34-7aa6-4c36-a858-d1d9760ca505 | topic | billing | support | billing | True |
| daef4ba1-24db-4d5a-8bc5-f377af4ba0a0 | severity | 1 | 5 | 1 | True |
| 104205ca-e739-4bea-b22a-7c275f7bf0fa | intent | praise | cancellation | praise | True |
| fddd4a7c-f26d-4cac-b93f-c7c8a489f068 | topic | other | downloads | other | True |
| 1e11b0d3-9888-45b2-bb6a-789e843796bb | severity | 1 | 5 | 1 | True |
| 502dacf6-3039-4ebc-8937-3c3ce46f6861 | intent | unclear | cancellation | unclear | True |
| a73cbea8-c7fc-431c-8f46-6b053492e8c1 | topic | playback | usability | playback | True |
| 70c24b0d-301c-4a2e-a5a9-f5f35110d981 | severity | 3 | 1 | 2 | True |
| 1be58e85-d31f-4c91-8c3d-df96a597d94f | intent | praise | request | praise | True |
| 3a5b8f91-5b9d-4498-83da-cbceb6aa74d8 | topic | other | playback | other | True |
| 5fff087b-0dc9-4efd-877d-bf57805e617d | severity | 2 | 5 | 2 | True |
| b70adee4-b466-4c3d-ba2f-789324b5d96f | intent | praise | complaint | praise | True |
| 96819a34-58dc-44f4-b795-e1c98104381e | topic | other | billing | other | True |
| 6392db0d-0451-452a-827b-106fb2fe2009 | severity | 1 | 5 | 1 | True |
| 16bcc18e-0a36-4a18-a8e9-30ea5dfb5c62 | intent | praise | cancellation | praise | True |
| 18500efa-d08f-4468-85f9-23851c64b238 | topic | catalog | support | other | True |
| 77c2a41e-d93e-49c6-a14f-25dafc4db0b3 | severity | 1 | 5 | 1 | True |
| f2a52414-81bd-406d-8676-76313bef944b | intent | complaint | request | complaint | True |
| f6205cb1-d22e-4158-ad06-cdd0dde60957 | topic | playback | other | usability | True |
| 83904150-4a72-4d1c-bab2-4d6f0ba79bdf | severity | 1 | 5 | 1 | True |
| 2e3c48df-b224-428c-8b5e-1fbcb557860e | intent | complaint | cancellation | complaint | True |
| 7fe9f573-5c20-4473-bfef-8ee7b1ed5b66 | topic | catalog | billing | catalog | True |
| 1611f876-214d-43c3-a30f-0f68b6e2d7cd | severity | 1 | 5 | 1 | True |
| 9fde5d4b-9213-4b85-b3b8-880aab8d9b9c | intent | complaint | unclear | complaint | True |
| ebbce37c-d946-4d9f-bbdb-5916ea1b0b68 | topic | other | downloads | other | True |
| d2722daa-453d-444c-b8ee-24987776f99f | severity | 3 | 1 | 2 | True |
| e4d1c0e7-9882-4476-930c-9bb35e0665b9 | intent | praise | cancellation | praise | True |
| 9bd366f6-0ebf-4437-9fa1-52a52571b15d | topic | other | support | other | True |
| 48ff5a7d-ead1-4eba-a952-198db27cf817 | severity | 3 | 1 | 3 | True |
| 04caf4b1-41f7-4ee1-95f6-277efacdc9d2 | intent | praise | unclear | praise | True |
| 2c2ea2f6-6136-4d76-ac4b-0e8b6cbf1d7d | topic | catalog | other | catalog | True |
| 4a934ee1-69aa-4968-8b92-a607b48f7165 | severity | 1 | 5 | 1 | True |
| d05adc24-526c-498e-9003-fd82a44f338f | intent | complaint | cancellation | complaint | True |
| af3c5af5-cf77-41a6-a99c-3153827be920 | topic | other | billing | other | True |
| 8559579a-7c11-4416-9a69-623afebec253 | severity | 1 | 5 | 1 | True |
| 5c3c5366-38a8-47a2-99dd-249e45685e16 | intent | praise | complaint | complaint | False |
| b7e025bf-b789-4b37-baad-85d628a3ff4e | topic | other | usability | other | True |
| 60fec3a7-fa7b-4237-b8d8-fb7e893385a8 | severity | 1 | 5 | 1 | True |
| 340826fa-a1d4-4d25-bf57-0a06742dc539 | intent | complaint | praise | complaint | True |
| d852db2a-983c-4ad7-9224-74d622617737 | topic | catalog | usability | catalog | True |
| 422d8563-afc1-45a7-b8be-46092a54bc0f | severity | 1 | 5 | 1 | True |
| 59fd956f-6b9e-4941-b6b7-7c7edfe007c3 | intent | praise | unclear | unclear | False |
| 3a06231d-70e2-444b-aa73-848ebc3098b5 | topic | other | access | other | True |
| 10b09a91-1725-403d-8390-8d108792ee7b | severity | 3 | 1 | 3 | True |
| dcc2d541-46bb-4c55-84ed-c662483b47ba | intent | praise | request | praise | True |
| a5cb4464-67d9-48a6-864f-618123ebbc41 | topic | billing | usability | billing | True |
| eaa53e32-1a72-4db8-a1e0-edc09f719751 | severity | 2 | 5 | 2 | True |
| 488a444b-76b4-4321-8f4c-33630472566a | intent | praise | complaint | praise | True |
| 6f4dde16-a80f-4c04-a59b-59fd93dd38bc | topic | other | support | other | True |
| bedfe125-68e2-46b1-95c0-42cf41de6707 | severity | 2 | 5 | 2 | True |
| dfd36a89-d276-4d8d-9247-5abba19bf1de | intent | complaint | praise | complaint | True |
| 6e934182-3cd3-49e0-853f-d849c9adb9e3 | topic | other | playback | catalog | True |
| 877ec4e6-993a-4748-9746-7866505d65f1 | severity | 1 | 5 | 1 | True |
| abf176c9-e956-46a0-9e2f-44eab83ceb6d | intent | complaint | request | complaint | True |
| f6c3f99b-75b1-408f-820f-17f5a81a2306 | topic | usability | other | usability | True |
| f3e5ce5d-6c5f-43fe-9087-a9c73af0a0d3 | severity | 1 | 5 | 1 | True |
| b22670fc-29ab-467a-b5b1-078cf0493b48 | intent | complaint | cancellation | complaint | True |
| 3c341f52-2525-4dd0-88b6-8845a8bdc0a4 | topic | billing | other | billing | True |
| 40e97032-ce5a-4dda-8e1e-4836725f725c | severity | 1 | 5 | 1 | True |
| ba19b9ec-e8e0-4504-a4af-235c96433e37 | intent | praise | complaint | praise | True |
| 372b946c-0d3a-43e1-a50b-ddf18b163f04 | topic | other | catalog | other | True |
| 56df638a-17dc-46da-94c4-79aa4202450a | severity | 1 | 5 | 1 | True |
| c41988e0-f76b-4ada-9509-44808b3c3dfc | intent | complaint | praise | complaint | True |
| 7bcfe23b-d545-4491-8546-3012162a1f8c | topic | other | access | other | True |
| 2abcc2cd-47cf-4a77-93d2-400c42ae4198 | severity | 2 | 5 | 2 | True |
| 8bc55766-506d-4899-ad44-0fadd2b12227 | intent | complaint | request | complaint | True |
| a2b83030-02fe-4ac7-8538-0fd75b3ad91e | topic | other | downloads | other | True |
| fac30266-f1c8-44d5-9ab3-1cd9f6d241f8 | severity | 3 | 1 | 3 | True |
| 7fe59ec4-1ff6-4dcd-838f-04845e6485e2 | intent | unclear | praise | unclear | True |
| 1c15adb3-be26-401a-96c2-cf716e35f9e4 | topic | billing | catalog | billing | True |
| 97b558b1-0b30-4384-8aa2-6a40e8334fe2 | severity | 2 | 5 | 2 | True |
| 4328cbfb-a364-4e51-8f2b-0911bfb27834 | intent | complaint | unclear | complaint | True |
| fa068dcc-95ea-43ba-b0e8-24565d16f09c | topic | other | playback | other | True |
| a38bfc0a-dc68-423e-99cf-35b9c2d45634 | severity | 2 | 5 | 2 | True |
| d55a9841-957f-4230-86f3-a044e12e24f5 | intent | praise | cancellation | praise | True |
| 37a7077f-017a-4313-88b9-fa8d794e9249 | topic | billing | downloads | billing | True |
| 3acd46a9-e617-406d-892c-b3de0d349c10 | severity | 3 | 1 | 3 | True |
| ab5fa825-038e-46fd-886f-702769f77772 | intent | praise | unclear | praise | True |
| 06986dcf-f935-4b36-aef4-4226075a08f4 | topic | catalog | support | usability | True |
| 741924f2-4843-4489-aae2-a7e1074b4b80 | severity | 1 | 5 | 1 | True |
| ae3c5427-f3b4-4434-9ef5-2eef2afb2bcf | intent | praise | request | praise | True |
| b9fc90be-33d7-4433-a280-6e6697513f81 | topic | catalog | usability | usability | False |
| c1548d91-4bb9-4c14-9d96-c89a1be9393a | severity | 2 | 5 | 2 | True |
| 5630c138-c8ae-4d9f-b023-975f3c51583d | intent | complaint | unclear | complaint | True |
| 84135b96-54bf-4551-8f43-f83ecf4de87c | topic | usability | playback | usability | True |
| bb9b3fab-ff99-40c5-89a2-a3bb45732854 | severity | 2 | 5 | 2 | True |
| 631fbc79-f1e8-4ccb-aba3-05a1c6424789 | intent | praise | cancellation | praise | True |
| 265ee9ec-6ad8-4184-87aa-492d98a2bae3 | topic | catalog | access | catalog | True |
| 6dd27e3e-92e9-47e6-9c46-5ea2a3bfa6d0 | severity | 3 | 1 | 3 | True |
| 76ed4a62-1e1f-446a-8403-6bb216b21882 | intent | complaint | request | cancellation | True |
| f7866963-73d6-4b6e-b97c-6b91fe65fb2c | topic | other | support | other | True |
| 5e291218-5a22-4b14-b5b0-8f6646f64dd3 | severity | 1 | 5 | 1 | True |
| 71c8a66c-e74c-46a3-94f3-6b31ba0408c2 | intent | request | complaint | request | True |
| 7fc0cb67-6ad4-4da6-8d44-10f45f57a552 | topic | billing | access | billing | True |
| 51da4be1-81e4-490c-9653-f897c673f16b | severity | 1 | 5 | 1 | True |
| 160b6f1a-ee37-4096-b488-918abede1984 | intent | complaint | unclear | complaint | True |
| 29220506-23d8-468c-9915-ec7227b252f2 | topic | billing | downloads | billing | True |
| 290919e2-5e4d-4378-9ba4-c60ec6f644c4 | severity | 2 | 5 | 2 | True |
| 2eefab24-eed1-4235-93f3-93f5bcf3914d | intent | praise | cancellation | praise | True |
| 852d0b01-5e1a-4875-932d-75260d92e6e3 | topic | catalog | support | usability | True |
| 63856d08-b017-4f5c-b436-cc0c6c9c53ef | severity | 1 | 5 | 1 | True |
| 5c6f89ca-48f9-464f-8006-4ea1f1affd10 | intent | praise | unclear | praise | True |
| 9e42f4ee-ccc0-4736-8917-14a9f58e56f9 | topic | other | catalog | other | True |
| 718bbb0b-de5f-43f0-b0c7-f0cb0969c92d | severity | 2 | 5 | 2 | True |
| cf03404c-cd91-402e-93f5-056be4d32b89 | intent | praise | request | praise | True |
| b384f103-714a-42e3-98fc-0bd3d33b4aa6 | topic | support | other | support | True |
| 1752bd0f-20b9-4910-90b8-d77b26861d3c | severity | 3 | 1 | 3 | True |
| 8624f068-edd4-4e5b-94a6-86714c0cce91 | intent | praise | complaint | praise | True |
| 7ba9436d-b9b6-485d-b685-1af9bb57036b | topic | catalog | access | catalog | True |
| 17c8c27e-a19a-45d8-aa2e-04c44509316a | severity | 1 | 5 | 1 | True |
| 18947035-4635-4789-b486-82004e8f8e37 | intent | complaint | praise | complaint | True |
| eebb239a-3564-4ddb-b20d-97262928d3f8 | topic | usability | access | usability | True |
| f8e7ee9b-bf22-4524-b245-65dc2b11abb2 | severity | 2 | 5 | 1 | True |
| 8f8cc4bf-d24b-4bcb-be6a-0af130f957d5 | intent | unclear | cancellation | unclear | True |
| 1526da67-8f0b-4635-a981-94e87c6f7b89 | topic | other | playback | other | True |
| 0c2da7fb-8f6b-42ba-8443-fae4dbf20de3 | severity | 3 | 1 | 3 | True |
| a1ab4924-7598-422a-8597-ca05d0529bc6 | intent | unclear | praise | unclear | True |
| a66ef2d5-f43c-4d35-b33d-77472a55bbd1 | topic | billing | downloads | billing | True |
| c74cc581-1d2a-4397-90a7-93fa84bd6f72 | severity | 3 | 1 | 2 | True |
| 1a0d06d9-a075-4fdd-b809-bffa903a8468 | intent | praise | complaint | praise | True |
| 631873a9-d33e-4a00-b14b-3e3aaf278493 | topic | billing | other | billing | True |
| 5ac62b2f-a4a5-4f5c-a736-1fda95f173cd | severity | 2 | 5 | 2 | True |
| befa5442-8934-49ae-bf00-654bebce4ea5 | intent | complaint | praise | complaint | True |
| 1f1a58e3-a80e-4c7e-aad4-211522129325 | topic | catalog | usability | usability | False |
| c134df2f-8d88-4369-bdf3-ed430d23ccab | severity | 2 | 5 | 2 | True |
| 09a15ed7-c484-4a10-9b48-da2b70ad9922 | intent | praise | unclear | praise | True |
| 1fe9b37a-b20b-4539-9347-7e41176a6058 | topic | other | access | usability | True |
| 42600e40-fad5-48f6-a9b0-bae8221d31e5 | severity | 1 | 5 | 1 | True |
| b194f3d3-4e5a-44e2-b0dd-829b57b833f7 | intent | praise | request | praise | True |
| 649ee7f1-2555-4916-967c-f33aa3d8ddf1 | topic | catalog | access | catalog | True |
| 31273ebb-7157-417d-8b1a-aff541e07a92 | severity | 1 | 5 | 1 | True |
| 1ba6cd98-ca60-4a01-8c21-c6229ab7197d | intent | request | cancellation | request | True |
| 84acb6b0-dd91-4330-944f-2686cbd15ce0 | topic | access | other | access | True |
| 8d55f3c0-57f1-4eee-8ab9-4d648739682d | severity | 1 | 5 | 1 | True |
| cf4d5b1e-87d9-4821-bb3a-101def78fcce | intent | request | unclear | request | True |
| 3ab1dc1e-fdc8-467b-af17-9b137fcf66d8 | topic | billing | access | billing | True |
| c8590c7f-f6a3-4335-b6a6-a15c270a41e7 | severity | 1 | 5 | 1 | True |
| 21646ebe-0274-4fe1-a1ac-698960a3f2f2 | intent | praise | unclear | praise | True |
| 6060fecc-75ff-4a73-916c-60e03ba02043 | topic | billing | downloads | billing | True |
| 88e82f4d-d598-424c-94b1-c11c49ba7311 | severity | 1 | 5 | 2 | True |
| 3ffa4301-d441-4ad4-9f19-cbc792d5313d | intent | praise | request | praise | True |
| fb55b568-afe8-4c28-9ebf-6e6cf2626108 | topic | other | usability | other | True |
| 568a8132-5912-47e7-9cb1-75fd8cece3ac | severity | 2 | 5 | 1 | True |
| 57688d10-361c-4bcd-abb3-674c6bbf72c7 | intent | cancellation | praise | cancellation | True |
| 43db4a13-c5ca-435b-8cf3-e76898c283f9 | topic | other | catalog | other | True |
| f144e5de-e772-46a1-8546-3e07fedb96df | severity | 1 | 5 | 1 | True |
| d93119c6-dc22-46b8-ba54-b8d02c480ae3 | intent | complaint | praise | complaint | True |
| eb20c016-6c74-4bc5-91bf-895c8be3c1e5 | topic | other | access | other | True |
| b734e4da-149f-4e18-8bac-eb4ffe207958 | severity | 2 | 5 | 2 | True |
| 2421580c-7676-49f5-aee5-e9d6d6145613 | intent | praise | unclear | praise | True |
| 4e8161ae-7d0f-446f-b3c7-a353c82bfaf2 | topic | usability | billing | usability | True |
| ede4e0b5-b20d-462f-b263-b82910307783 | severity | 1 | 5 | 1 | True |
| e8954b9d-a72f-46e4-87d6-60d279ef60d2 | intent | request | complaint | complaint | False |
| 0315eeec-0bb2-48e4-9afe-266e8157ba1e | topic | other | support | other | True |
| 01f335df-2b1b-41e2-8ad3-8ac95288d97e | severity | 1 | 5 | 1 | True |
| f8599e18-f368-4199-a8ff-1ea45e62c63a | intent | praise | complaint | praise | True |
| 2e6ae05a-2f39-4d3e-83a2-85f7a364ebb0 | topic | catalog | other | catalog | True |
| e6cd69e2-3af3-4b75-94cd-9c8ce66501ac | severity | 4 | 1 | 4 | True |
| 9208f2b9-c74a-4c81-a150-e1177ea61f12 | intent | complaint | praise | complaint | True |
| 1a206aaa-2693-48ba-ac1d-ada647d49a38 | topic | playback | access | playback | True |
| 0b97fb0b-0f02-44b2-af7a-1a73dc2163ef | severity | 2 | 5 | 2 | True |
| b91866dc-d596-45f5-80e9-500d71f60af3 | intent | praise | unclear | unclear | False |
| 6d654fdd-f3cc-4696-bd16-0342a40ebe77 | topic | other | usability | other | True |
| c2393bb9-9059-4caa-a8f4-434a4528df3a | severity | 2 | 5 | 2 | True |
| b36c5234-39ac-4a40-b049-eabc0a111dcc | intent | complaint | cancellation | complaint | True |
| a3c8b73c-4cb1-43e3-bf84-be289be573cc | topic | other | catalog | other | True |
| a4d17505-9c09-42bf-886c-b80cb940b4b5 | severity | 1 | 5 | 1 | True |
| 26ddacae-a187-45eb-b5ae-1e11b291ab98 | intent | praise | complaint | praise | True |
| 29389fe5-acdc-4f90-bd75-009cb461b1a7 | topic | catalog | billing | other | True |
| 9cb62b3d-05eb-46a2-b4b4-3127ae4ed7af | severity | 1 | 5 | 1 | True |
| 3c05f6ee-9908-41ea-85b8-d831646a9559 | intent | complaint | praise | complaint | True |
| 55f3376b-eccd-42ba-9a69-61e543c8b6c1 | topic | catalog | access | catalog | True |
| 5056ab6b-149b-43af-b4d3-3f72ea715123 | severity | 1 | 5 | 1 | True |
| 02445fdb-784c-4cd8-a140-5845b35be93e | intent | complaint | request | complaint | True |
| 4b013f26-0571-4b27-9f9a-2407fa8d7f0b | topic | usability | access | usability | True |
| 5cc6c1e0-4740-4625-8cdf-f45e5ffac890 | severity | 3 | 1 | 3 | True |
| ebe594c8-a537-41d7-83a8-44f43ae759dd | intent | complaint | cancellation | complaint | True |
| 48e63a90-69ce-4655-a97d-b89e92a24f81 | topic | other | playback | other | True |
| 880ba339-34e5-43c5-a8ff-d51905a4aeaf | severity | 1 | 5 | 1 | True |
| f0c61b06-aaac-455a-8fa8-9987af6fe297 | intent | unclear | request | unclear | True |
| 1beb5b5a-a667-4945-ac05-b85cf554aab7 | topic | playback | access | playback | True |
| 21010400-aa9e-4656-83ac-6c001092091c | severity | 2 | 5 | 1 | True |
| 23430a85-b6e0-406f-b877-0b5bb68c0bd5 | intent | complaint | praise | complaint | True |
| ccadf919-ae3c-498d-99e5-db38fe35fa53 | topic | billing | other | billing | True |
| 359a785c-aebe-4482-8956-8a442f353004 | severity | 1 | 5 | 1 | True |
| 671b04e8-ea90-4afc-89ea-b1e2a24d264a | intent | unclear | cancellation | unclear | True |
| 143e27b2-eb25-4762-bd9a-c91524e8f324 | topic | access | billing | access | True |
| 0fbbb9a2-99bd-44fb-b72c-34071bad379a | severity | 3 | 1 | 2 | True |
| 118a890e-b021-48d0-a395-a173fcdeb65a | intent | praise | request | praise | True |
| 61337d52-79ab-4e25-ae8a-d5d6698771df | topic | other | access | playback | True |
| 0a632e61-4cb5-428d-9a66-8328e3e9602e | severity | 1 | 5 | 1 | True |
| 8e48faa7-5161-409c-a3da-1d4bebf8efff | intent | praise | complaint | praise | True |
| a2e2a211-5061-44ff-a8aa-47e63c5fda90 | topic | usability | billing | usability | True |
| 7ab5071b-acb0-43e5-95bf-ba1259c75d52 | severity | 1 | 5 | 1 | True |
| 36aec49d-675b-4169-a914-f6679ee1c535 | intent | praise | cancellation | praise | True |
| 67de517d-bb45-48f4-848b-407735c7444d | topic | other | support | other | True |
| a7d4837f-a719-4242-a625-7ad6b86467a1 | severity | 3 | 1 | 3 | True |
| 8c7c599d-0606-426c-997c-96a43669aad1 | intent | praise | unclear | praise | True |
| e0d78ad9-440c-4e4c-8c92-0a19c04a3a82 | topic | billing | access | billing | True |
| eb17f422-d777-4684-b05d-2e611cd75aba | severity | 2 | 5 | 2 | True |
| acf8e91e-a230-4e19-9e15-33e146f95b38 | intent | complaint | cancellation | complaint | True |
| c54a8b32-3799-49b0-ae87-a4a0431b4939 | topic | usability | other | usability | True |
| fd2c0602-bef1-4235-90eb-4476c7a4680e | severity | 1 | 5 | 1 | True |
| 7dedccfc-24b7-47ec-a372-3f14202ae11e | intent | complaint | unclear | request | True |
| bab1b0ca-7288-4fcb-a2b7-b6197a5d2c25 | topic | playback | catalog | playback | True |
| 320c597f-116d-4864-9c9b-5b23d18fd1ae | severity | 4 | 1 | 3 | True |
| 594c4ff2-2497-4389-8bff-51150fe386ab | intent | praise | cancellation | unclear | True |
| 55140dd8-3290-48ee-9a21-dfd23479db62 | topic | playback | other | playback | True |
| 0e1f7ed4-f5a2-440d-896e-d490247bf8f2 | severity | 1 | 5 | 2 | True |
| 6ace5d1d-f3b8-495d-853b-b8cdac4f6aef | intent | complaint | request | complaint | True |
| 21050425-d538-4861-bee3-a34cbb5044bc | topic | other | access | other | True |
| 02404778-dc81-4095-8d4d-b245d6606687 | severity | 3 | 1 | 3 | True |
| 5694b7ee-4eae-4787-9e16-58aa789e63a4 | intent | praise | request | praise | True |
| 0ded963b-445d-44ef-b421-bf09d9b395ed | topic | catalog | access | usability | True |
| b9797669-baaa-4f67-a064-6081c312779b | severity | 4 | 1 | 4 | True |
| 99a6c851-54f7-4e84-96e6-b6bb7ab5f9e3 | intent | praise | complaint | praise | True |
| 8a83bacf-cf6b-4054-b153-4b22f8c2258a | topic | playback | usability | catalog | True |
| 8034fd62-752c-4bb7-82b1-e591972ebb8f | severity | 5 | 1 | 5 | True |
| 3c88f934-921e-42bd-bcde-b29364f67bd6 | intent | complaint | praise | complaint | True |
| fb7acdcb-b63d-4bf8-8786-8a1db78e156a | topic | other | playback | other | True |
| b9d08021-739e-4f3e-886a-00bb0f7f50c9 | severity | 1 | 5 | 1 | True |
| 9cfb71fc-8be7-427f-91c0-d9058f9f4c99 | intent | complaint | request | complaint | True |
| 18464fd4-e2fc-4a47-8319-4127dc497135 | topic | playback | access | playback | True |
| 190d9352-12ba-466e-821e-14828d8d86a3 | severity | 1 | 5 | 2 | True |
| a8a81348-7510-43fd-9a71-3d1f0e348101 | intent | praise | request | praise | True |
| a607c9c0-9888-4b47-9328-e221048eb9e0 | topic | usability | downloads | usability | True |
| 388675e4-112f-4f23-b70f-3c29f3a1a883 | severity | 2 | 5 | 2 | True |
| 34a3ef1e-8404-4d6d-9de9-a3f08aa6ed05 | intent | praise | complaint | praise | True |
| c68fba4b-9b9d-446d-9c41-c996a6f948c4 | topic | playback | other | playback | True |
| 7379aeee-0daa-4432-b693-14b8d149e56a | severity | 3 | 1 | 2 | True |
| 68054f2d-e754-4c03-a76a-c71052a2e09b | intent | praise | cancellation | praise | True |
| b0fa1edd-5db7-491b-9cdb-cde8962375f2 | topic | other | access | other | True |
| 5e763f54-48cf-42c4-80e3-d69f183d8512 | severity | 3 | 1 | 3 | True |
| f7bf76d5-c91d-4670-b04b-deede65f0646 | intent | request | praise | complaint | True |
| b7611ca4-0ef6-46de-9aad-cc134e4980e1 | topic | catalog | access | catalog | True |
| e62a9510-1660-40f6-b4ea-abb7fa4b290e | severity | 1 | 5 | 1 | True |
| a4991b74-79c9-4852-9d50-93ce9ba66e2c | intent | complaint | cancellation | complaint | True |
| 0ccd6dfb-2fe4-41c7-b606-6d0beb6814a6 | topic | other | support | other | True |
| 8f64fd78-65c9-4903-a7a9-b1a4e2ed63a8 | severity | 1 | 5 | 1 | True |
| 95305ef2-0d9d-48f4-a3cf-b381430168c3 | intent | complaint | unclear | complaint | True |
| 7dd3df00-8232-4f03-aa91-b2c1dc1b939e | topic | other | playback | other | True |
| 172447d3-3d24-4e46-a87b-5463e8fe483b | severity | 1 | 5 | 1 | True |
| 7a18f7a4-2244-4ca8-8191-849edd1f5d90 | intent | complaint | praise | complaint | True |
| 3ce60b2a-6fa2-43b7-81bb-9aaee748c88c | topic | billing | downloads | billing | True |
| e533f3a6-1443-4db0-9bb7-17942d4d99c7 | severity | 1 | 5 | 1 | True |
| e1a3d78d-b9c0-42cc-9103-1647393aecf1 | intent | praise | unclear | praise | True |
| b21ca808-3a04-48d1-ab18-4240f2f77c43 | topic | catalog | support | catalog | True |
| 242a9fda-2fd8-47bc-a19e-554dd1a5efa7 | severity | 1 | 5 | 2 | True |
| 0135aa3b-7b3e-4325-aa8e-4eeeff911ef5 | intent | unclear | praise | unclear | True |
| 97578051-028f-4315-93d1-dda9c7f0222b | topic | catalog | usability | catalog | True |
| 2b8a3d48-53ae-46d2-9bfd-2832d6fa3249 | severity | 3 | 1 | 2 | True |
| bce6cdcd-e8c8-420c-915b-a5e9bc967fda | intent | praise | complaint | praise | True |
| 96f620f2-d763-4897-a082-ff486a500dff | topic | playback | downloads | usability | True |
| 1e93a262-6cc9-4708-877e-86bb27cb29a8 | severity | 1 | 5 | 1 | True |
| 37b84b2e-2a79-41b0-8da0-39eaca2837c5 | intent | complaint | praise | complaint | True |
| 7731b046-f8b3-424f-9027-af3a1109dfab | topic | catalog | access | other | True |
| 374dc6b9-9ef5-4227-95a8-ee7e9f105cf5 | severity | 3 | 1 | 3 | True |
| bf4a9154-2951-4e0d-bd42-90435084a8cb | intent | complaint | request | complaint | True |
| f0629563-1866-46ce-89ec-d30b457a002d | topic | playback | usability | access | True |
| 1419b685-0275-4548-817a-be77e042e8b2 | severity | 2 | 5 | 1 | True |
| 95f5e005-be56-48ce-8aab-b3cfd98aa01a | intent | complaint | cancellation | complaint | True |
| be1c48c4-46bc-4ddd-ae38-49a970c82d66 | topic | billing | access | billing | True |
| 5f1dd326-96e6-4b35-9b5b-5b8faa105ecb | severity | 1 | 5 | 1 | True |
| 14deda71-0599-4ef5-a733-b80b68628a84 | intent | praise | complaint | praise | True |
| 1b72ced4-e0d7-4d0d-9589-e016c4b02bd7 | topic | other | billing | other | True |
| ac8a00b0-a868-4373-8f76-f28b4d31f6b2 | severity | 4 | 1 | 3 | True |
| 7a441894-6db1-417d-a024-76e63389726f | intent | complaint | praise | complaint | True |
| 306c32d8-a620-4ceb-a5be-99b1187edce5 | topic | other | usability | other | True |
| b528074b-ddd0-4be0-a418-8f1baf7b7904 | severity | 2 | 5 | 2 | True |
| 8ce0bed5-6d83-4b10-8828-b7990bc59f71 | intent | complaint | request | cancellation | True |
| a6eccbda-0dc1-4ff6-b0da-7da999a8f21e | topic | catalog | usability | other | True |
| 35f954c1-da84-42a8-922a-738e14ff443c | severity | 4 | 1 | 4 | True |
| adcfaa9c-0e83-448a-8526-b7711539adaa | intent | praise | request | praise | True |
| 61f2f0d1-65cc-4c66-91da-e1218fabeb4a | topic | usability | playback | usability | True |
| baef6a72-9c54-4e96-8f9a-199ffff43186 | severity | 1 | 5 | 1 | True |
| 319867c6-38ed-4810-84af-b05325422b9a | intent | request | cancellation | request | True |
| c61e57e5-9ea5-4531-a685-5f1fea1ee004 | topic | other | downloads | other | True |
| fbad5aca-569b-41ac-8f49-39d45ed778dd | severity | 1 | 5 | 1 | True |
| b59ef7db-274c-4829-831a-4f8e8c1c9b0c | intent | complaint | praise | complaint | True |
| f3a79c64-32b8-4741-b6ef-a1b927356940 | topic | usability | access | usability | True |
| f23eb928-a12e-4c2d-84a1-37754a671545 | severity | 3 | 1 | 3 | True |
| 9bb4a956-7cab-4a52-b9e0-f4cf4a08def7 | intent | unclear | cancellation | complaint | True |
| 17b6e034-71a5-49f4-8929-93941a598564 | topic | other | playback | other | True |
| 6b41b629-1730-43f1-8fba-9e3119d8d892 | severity | 2 | 5 | 2 | True |
| b8a404a1-6a2d-4de4-b5de-659bb3b5efa6 | intent | complaint | cancellation | complaint | True |
| 0193e7b0-f350-4d40-a69c-9aa80e0b4d9c | topic | downloads | usability | downloads | True |
| 715bc3f6-5cff-4b29-b8d4-c9dd393d2648 | severity | 1 | 5 | 1 | True |
| 56a297b3-2a8f-4c45-ad1e-4fce1ee58a0b | intent | complaint | unclear | complaint | True |
| de6aa304-2a7a-4116-b97b-683068273265 | topic | other | usability | usability | False |
| fd6d286f-fc1b-458c-a479-94c9ebd3e422 | severity | 2 | 5 | 2 | True |
| b00d9c6a-347e-4ea0-b205-b7a70395b0c8 | intent | complaint | praise | complaint | True |
| 34208598-cf86-4129-863a-dc5c2ca0c6ee | topic | other | catalog | other | True |
| f3d6f597-ad1b-4696-b6f9-bd26a5f4bf82 | severity | 2 | 5 | 2 | True |
| f10ca202-4bd2-401a-b603-4550743679ba | intent | praise | unclear | praise | True |
| c73928f0-cd4d-44cf-9987-c40b80190337 | topic | usability | playback | usability | True |
| 6d7ae200-048b-4500-8116-dd975dceae8d | severity | 1 | 5 | 1 | True |
| 7ceb05fe-74fe-4d03-80c9-de2061bd3736 | intent | complaint | cancellation | complaint | True |
| 61e0ddbb-6ec4-4d3a-acd3-41eb5f64afb7 | topic | billing | usability | billing | True |
| 12ed4c61-6bbf-40aa-80b0-5af675a9530c | severity | 3 | 1 | 2 | True |
| 2ed6116f-58c9-4169-8a6a-906c7a194bd8 | intent | unclear | request | unclear | True |
| cc46c895-290d-4aa7-b17b-86923ef47ff1 | topic | catalog | downloads | catalog | True |
| 405b1823-a524-4b8c-b6a5-3eb73e3892af | severity | 1 | 5 | 1 | True |
| 60220938-308e-4fe9-b7af-0685f817815b | intent | unclear | complaint | unclear | True |
| 35f786d6-2386-4743-b4c0-77366abc304d | topic | other | playback | other | True |
| 5b4e200f-58fe-40e2-b344-e9cf588703f9 | severity | 1 | 5 | 1 | True |
| d8e24a64-d928-4fa7-b1b2-db434e236010 | intent | praise | unclear | praise | True |
| 90d9bc1a-b827-4cb5-967d-3a485e1c4f59 | topic | playback | access | playback | True |
| 98827cfe-371f-4ad3-a5e3-5de438cb5552 | severity | 3 | 1 | 3 | True |
| dcd6248a-b73c-447c-8489-4bc86c4233ab | intent | unclear | praise | unclear | True |
| 9d7b273d-56df-43fa-86dd-ae1a9de6b19c | topic | other | usability | other | True |
| 4d3b7d09-80b7-4b34-8265-ae46acc952b5 | severity | 2 | 5 | 2 | True |
| d39b008d-7d46-4d78-8586-0b675b017864 | intent | request | cancellation | complaint | True |
| f555a72f-c9bf-46fe-b791-c05c5d30a793 | topic | usability | support | usability | True |
| 13f4b396-3337-4820-bf43-14970be5e006 | severity | 1 | 5 | 1 | True |
| 510d3ce4-d6ee-4959-adee-ccd286c42ad1 | intent | unclear | complaint | unclear | True |
| f11ceca0-41e3-46b5-8dd7-4a907a57b006 | topic | usability | playback | usability | True |
| ce47994b-bfad-45f0-bb52-2385596a7c96 | severity | 3 | 1 | 3 | True |
| be4483a7-1ff5-45f3-9aa8-a9eac64aa366 | intent | complaint | request | complaint | True |
| fddc5780-8a6d-4db3-b610-f229e9c3f0ea | topic | other | downloads | other | True |
| b9dd3b96-b0b4-4ac2-9543-739e3b8a848c | severity | 1 | 5 | 1 | True |
| 218a9167-255a-42cf-9f86-295260a7baf9 | intent | praise | request | praise | True |
| dc426215-b611-4aac-8e59-60c025bbce14 | topic | billing | catalog | billing | True |
| 1cd5bd79-7ea4-4ae7-9550-f1dc80cbe608 | severity | 3 | 1 | 3 | True |
| 2238e249-3c6f-40d4-aa80-a157c9e56d19 | intent | complaint | unclear | complaint | True |
| ae7ff4cb-bb11-4de4-8fde-fcc82f93e5d8 | topic | billing | access | billing | True |
| 2256a563-73db-48f0-8a89-e879cd27c5e7 | severity | 1 | 5 | 1 | True |
| 3d62bda0-f332-4e74-bac9-5dbe9cb647fe | intent | complaint | praise | complaint | True |
| 312021dd-78b8-4df8-8d67-213cff757ca4 | topic | other | billing | other | True |
| 89939cdb-ff35-4b6f-8203-4065edff83b5 | severity | 2 | 5 | 1 | True |
| d6dfce30-61f1-4b60-9a3e-e81b62ef41b2 | intent | request | praise | request | True |
| 82fd9ba9-ea0c-47be-bf5e-ca715688ba2c | topic | access | playback | access | True |
| 1a072d43-5ba4-4665-9ad4-8582eb1e1dc5 | severity | 3 | 1 | 3 | True |
| ba3fafdf-0d92-460a-825d-c22b10091e26 | intent | complaint | cancellation | complaint | True |
| 8105ad21-b88c-4470-b817-54e01e29d1fc | topic | other | catalog | other | True |
| 0a416ae7-b8e3-45c7-a13f-3b980f27c63a | severity | 2 | 5 | 2 | True |
| cccdfb47-8c95-4b1b-adda-e9d97226fc58 | intent | complaint | unclear | complaint | True |
| 739418da-3781-4103-b927-89047be5bd56 | topic | other | access | other | True |
| 2dd66e1f-064b-4460-b898-d2a782a0cdd8 | severity | 2 | 5 | 3 | True |
| 282e2c78-a7c2-47ad-b0af-1b3a7931a921 | intent | complaint | praise | complaint | True |
| 5511d62a-0d41-4ba8-a903-12e8ffdae9e6 | topic | billing | usability | billing | True |
| 1d7bd71e-5dd7-4e82-b775-2e000c46dc93 | severity | 1 | 5 | 1 | True |
| caa04a59-657c-47f3-8686-6533eb455a78 | intent | praise | unclear | praise | True |
| 458768c8-af6b-4458-b24d-5c00efbbd49d | topic | other | support | other | True |
| 438b5cc9-e135-46db-9c31-1e346aa87c39 | severity | 2 | 5 | 2 | True |
| 49fb5c87-b31f-41ce-be75-40a827e31edf | intent | unclear | praise | complaint | True |
| da12f6f0-bdea-4841-beb9-b4c442e38c46 | topic | billing | access | billing | True |
| 9cead0ab-2166-4355-abfd-c7186fed86d7 | severity | 2 | 5 | 2 | True |
| 57f8cb86-07dc-49fa-9556-f6c278df2ce4 | intent | complaint | unclear | complaint | True |
| 56009b5c-2aee-4f6e-ba33-39d85d746819 | topic | other | billing | other | True |
| 840661ee-3ef7-4e47-b698-f25906bc1903 | severity | 1 | 5 | 1 | True |
| d8fb1790-62fa-4fc5-8c47-add9e3fb70d2 | intent | praise | cancellation | praise | True |
| 1163d87b-708d-45b2-9e36-0ac4f1e60a86 | topic | catalog | support | catalog | True |
| f0d2e2a8-08b5-4f6a-ae04-d5f5c156dbde | severity | 1 | 5 | 1 | True |
| 194e2ea9-0bec-4dbb-958c-f86af67d1ff6 | intent | complaint | request | complaint | True |
| b0535656-9188-4865-b426-42f0530d91f2 | topic | usability | support | usability | True |
| 2def47b9-a1d9-4116-860e-2e1d9c13511b | severity | 1 | 5 | 1 | True |
| d5d8b080-6401-4552-b07e-d82d5f1475b0 | intent | complaint | cancellation | cancellation | False |
| 60d4fa05-aed5-4d01-9ae3-64f852576e8c | topic | billing | support | billing | True |
| 414b72d8-f4fb-4033-aa5e-3f9cd9cfb7ce | severity | 2 | 5 | 2 | True |
| 8e9c8bd1-9716-4e93-af7f-9675a5ec398e | intent | complaint | unclear | unclear | False |
| 809765d0-4b92-421e-ae09-923e221fe10f | topic | other | downloads | other | True |
| 9653756b-3fd1-4284-9a86-7de6d415c073 | severity | 3 | 1 | 3 | True |
| 48ba1ec6-8d5b-4c53-a0be-a801e4ec7797 | intent | praise | cancellation | praise | True |
| 0bda3019-e9ce-4fc6-ad4a-a29027becc6a | topic | usability | access | playback | True |
| 14b17989-8159-40a8-900b-a4e8a2c7414c | severity | 1 | 5 | 1 | True |
| c47f65c1-1a25-4704-9c23-1ae54200d31d | intent | unclear | cancellation | unclear | True |
| c9272c67-6ed8-446b-b8a3-cf8e34f95d0b | topic | other | playback | other | True |
| 295e5793-e19d-4714-bc15-690a5507ad6a | severity | 4 | 1 | 3 | True |
| 2fd5aae0-1c53-410a-98b7-ecab3c66f8bb | intent | complaint | cancellation | complaint | True |
| 920a8799-a336-4609-8427-8a816dced83a | topic | other | billing | other | True |
| 1fe8b029-f38f-4525-a94c-04623c0fd9b2 | severity | 3 | 1 | 2 | True |
| ed56bf2b-4d6b-44d1-85c0-b3585557096e | intent | complaint | unclear | complaint | True |
| 6fa1c101-829d-4f7c-98d5-5387fd03440d | topic | catalog | support | catalog | True |
| 503af18e-a32a-4293-8c66-a6193ae20b20 | severity | 3 | 1 | 3 | True |
| 4e027fdd-8e34-4e5e-85ac-3f9bbb121c76 | intent | complaint | praise | complaint | True |
| 230897b0-e83a-45aa-bce5-26f2a74cf902 | topic | other | catalog | other | True |
| 96ca138b-576c-48df-b93d-69a1ebbe5889 | severity | 1 | 5 | 1 | True |
| d7d928c8-e71d-4512-a8ca-017d6ea10788 | intent | praise | unclear | praise | True |
| 2a39721d-5d49-4d9c-9616-b6b215029386 | topic | catalog | billing | other | True |
| b70fc340-22b6-41ee-ac09-7bc734b2e2fa | severity | 1 | 5 | 1 | True |
| 28cdd6f2-0bbf-4577-89ec-4ab9ff881239 | intent | complaint | cancellation | complaint | True |
| ae658f8c-6ae6-4006-b01e-612043eec24f | topic | other | downloads | other | True |
| c13438b2-e0d2-449b-ae56-9bbe83341937 | severity | 2 | 5 | 2 | True |
| 3eb1fc6e-7b23-46be-9fb4-05a69128db00 | intent | complaint | unclear | complaint | True |
| a268f5a1-6263-4034-8fbf-561e5b8ee698 | topic | billing | catalog | billing | True |
| 5c8074ea-b165-437f-a805-99191a3fc740 | severity | 2 | 5 | 2 | True |
| f53e03a2-8e9b-4b0e-90ae-7c83c4103a83 | intent | complaint | praise | complaint | True |
| 672ce544-5834-4731-bd58-b578868c6ea7 | topic | usability | catalog | usability | True |
| 2be8d574-9204-484c-9359-aeccf36e8db4 | severity | 2 | 5 | 1 | True |
| 71b65bfc-dfcb-41e2-a639-335086064bac | intent | complaint | request | complaint | True |
| b0871cf4-f960-4817-ab4a-892b52f65ad2 | topic | other | billing | other | True |
| 5223d6b7-1adb-452f-9a1a-15fc31a89435 | severity | 3 | 1 | 2 | True |
| ec640e57-7b0d-4c1f-a82f-85590e0446f6 | intent | complaint | cancellation | complaint | True |
| d09b36c7-c34f-4672-a177-bac26ff0bc15 | topic | billing | other | usability | True |
| c557e58d-21e9-4d5e-9931-f84a19c39121 | severity | 1 | 5 | 1 | True |
| 09422650-a3aa-4ace-be18-fc8fecbe1573 | intent | cancellation | praise | cancellation | True |
| a5caa242-5f93-48e7-a737-a16e942b331f | topic | downloads | access | downloads | True |
| 1be6f119-e476-4ca1-9aa4-b9150c85370a | severity | 3 | 1 | 3 | True |
| def4ade4-36e1-492a-96f4-365f3a06c006 | intent | complaint | praise | complaint | True |
| 41b9fa78-d588-4078-9777-c631dff3f7d6 | topic | other | access | other | True |
| 8df7fb51-80d8-4889-9d2c-7cda72435d03 | severity | 2 | 5 | 2 | True |
| d53d5e52-e064-4bdb-adf6-c0ce968225cd | intent | complaint | request | complaint | True |
| d906c582-0430-41f0-8045-dccffdc30faf | topic | billing | usability | billing | True |
| 0d152c6e-fabd-4ed9-bf4d-772face94384 | severity | 2 | 5 | 2 | True |
| d3784c3f-bace-4b73-8032-08195f05086b | intent | complaint | cancellation | complaint | True |
| b521773a-4eb8-471c-a897-5332100e812c | topic | usability | access | usability | True |
| c6f220a4-c42f-4fa1-acab-c408e24ce3f5 | severity | 1 | 5 | 1 | True |
| 2a1cd223-a3b9-4766-9909-6eab6bfebed9 | intent | praise | complaint | praise | True |
| bc991eea-dddf-4ad9-86bf-9cd2f8ee68ef | topic | access | downloads | access | True |
| a0da2841-d8a4-4db6-8e5b-cca429ded9b0 | severity | 1 | 5 | 1 | True |
| 7e0de6c5-c317-44f9-8392-e9f7dff79577 | intent | complaint | praise | complaint | True |
| 6d6504f3-1aa7-49bf-8d8e-6b1c9614d952 | topic | usability | other | usability | True |
| db73957b-fa40-4126-8fac-c404581bebfa | severity | 3 | 1 | 3 | True |
| 8a34dfb3-83f6-471f-9655-91f355dc5125 | intent | complaint | request | complaint | True |
| 26aefdd3-60c9-4413-b584-e5ca36fdf88b | topic | other | usability | other | True |
| 1050efc9-6bc1-44e7-a902-ba7248fd1d20 | severity | 3 | 1 | 2 | True |
| 48814f84-2ab9-48c7-8613-9156f9d987a1 | intent | praise | request | praise | True |
| 834fe23e-a98d-4672-a8be-ddad6309eee6 | topic | other | catalog | other | True |
| 6346d85b-7dc5-436c-8ea1-e0a1517daa6d | severity | 2 | 5 | 2 | True |
| 88c3a4d6-4707-4e81-857d-76b91fa4fd76 | intent | praise | complaint | praise | True |
| 4e26962f-0f7d-413e-bfac-d36320cb44f7 | topic | other | access | usability | True |
| 8d429f06-8b00-4096-a57c-ae4d6c8dadec | severity | 3 | 1 | 3 | True |
| def5de67-fb81-4389-a239-fe997ca5b5a1 | intent | complaint | praise | complaint | True |
| 8a75abc0-7d6e-4686-9e6d-f8c151ae749a | topic | usability | billing | usability | True |
| 46ee7660-f2a3-47d8-b9f6-f34279644475 | severity | 1 | 5 | 1 | True |
| fd3da2e6-1a54-4ab1-90f3-dfb3e63b158e | intent | complaint | request | complaint | True |
| b6fc8894-f371-4674-abf0-93808f0347c6 | topic | access | other | access | True |
| f5b2bbc4-7085-45c5-8b9e-abd157a98d73 | severity | 1 | 5 | 1 | True |
| bc8b7bb3-06fe-4857-adb4-0cdc8d4454b4 | intent | praise | request | praise | True |
| 4ebabb94-4bf5-4caf-8e4a-b40d1050a18f | topic | access | downloads | access | True |
| c4d1559e-bbb2-43c8-9487-31f649634e9b | severity | 2 | 5 | 2 | True |
| 23d40536-b12c-4306-9517-29be80495a26 | intent | complaint | unclear | complaint | True |
| b149eae9-62b0-40e2-b093-0dc6fa17832f | topic | billing | downloads | billing | True |
| 3c1d1754-c941-40bf-b3c7-5340ef99e6bc | severity | 3 | 1 | 3 | True |
| c357d860-e7b4-45c8-b214-367bf97115db | intent | praise | cancellation | praise | True |
| e2c063c9-4861-4deb-bac8-c468666fca42 | topic | catalog | support | usability | True |
| 3918a72f-3122-4ffc-a06b-7e75e904a044 | severity | 4 | 1 | 4 | True |
| f45f4fb4-01f8-4f46-bed1-9d1c828024a4 | intent | complaint | request | complaint | True |
| 04c7a26e-d57f-4a6d-ad23-75f52e8cbfe9 | topic | usability | support | billing | True |
| c6ad1d41-4cf9-4f5e-b67c-22ce399adb5a | severity | 2 | 5 | 2 | True |
| ae0eabb4-271e-44df-bab4-f286eb223d57 | intent | request | complaint | request | True |
| 6c464508-a99b-464d-a04f-851aed8647d4 | topic | other | access | other | True |
| 9cf3ef1e-53ad-46f1-90ee-c4f472ed0516 | severity | 3 | 1 | 2 | True |
| db5708e7-db92-4eb5-991f-2fa23712b6ea | intent | complaint | unclear | unclear | False |
| 370ece33-98bb-4b30-9d42-6fd247ba3335 | topic | usability | billing | usability | True |
| c4d50c58-9316-4e4c-af9c-81e3175f2479 | severity | 2 | 5 | 2 | True |
| 01b923f5-c4e9-4d48-ab12-48405d78b58c | intent | praise | cancellation | praise | True |
| d13ea774-4318-4f99-82bd-b1c115e59d7e | topic | other | support | other | True |
| 6304ab3c-6fdd-45de-94e7-37ee386cd74d | severity | 2 | 5 | 2 | True |
| 1305a930-795b-443d-ac96-d8bf19f78883 | intent | complaint | request | complaint | True |
| ff931ad6-6024-4dcd-8abe-7bc40d5389ad | topic | usability | catalog | usability | True |
| 1b17097d-2e55-4b92-a3ee-95eb4886c661 | severity | 4 | 1 | 4 | True |
| d619a74a-7902-460d-b825-28c30747562a | intent | complaint | cancellation | praise | True |
| 762a4d89-cb3d-432a-87ef-9ef597e4ec25 | topic | other | billing | other | True |
| fa260e19-264e-449e-bfa0-edab622dfcf0 | severity | 2 | 5 | 2 | True |
| 28847d31-6471-4152-969e-f490f97d54fc | intent | praise | complaint | praise | True |
| c5be3bf0-2e52-415e-b7f0-d120927e6758 | topic | other | usability | playback | True |
| b9197940-c704-4cdb-91e2-e77ee07695cd | severity | 2 | 5 | 2 | True |
| 51171873-d6d7-4721-b58f-2499db23e90d | intent | praise | cancellation | praise | True |
| 6beb7958-f7c2-4e9f-a141-304310acff49 | topic | other | catalog | other | True |
| 3eb377c1-f2fe-43b5-b719-8a020fa25258 | severity | 3 | 1 | 3 | True |
| 14e820ba-a3a8-4a7c-b632-72f0fc5a7e2b | intent | complaint | request | complaint | True |
| 723dabe9-02e3-4a0c-b54c-241161ad893e | topic | other | access | other | True |
| b66f56e3-5d37-4ae9-9358-d6bc51c26390 | severity | 1 | 5 | 1 | True |
| 743855e1-083a-4865-b61f-3142d63f060f | intent | praise | request | praise | True |
| 1c1b4447-0d6f-4e12-95f3-84f9c3738a71 | topic | catalog | access | other | True |
| ed5c6423-6af3-444c-84cc-5840be9e1d84 | severity | 1 | 5 | 1 | True |
| 331e1f54-6499-46f7-8292-433030da27c6 | intent | complaint | unclear | complaint | True |
| 18e0f3fa-6b6a-4696-8db4-19e8d74000cc | topic | playback | usability | playback | True |
| 6f7feecb-8a8a-488a-ba8a-0287653d2a3a | severity | 1 | 5 | 1 | True |
| 639ff58d-f2fd-43e3-a848-6e84d0eeb23d | intent | complaint | praise | complaint | True |
| 676a83d2-d81f-4479-948f-c97d7eb8dc24 | topic | other | playback | other | True |
| 208f755f-5554-40b3-8f10-6cc304add37d | severity | 1 | 5 | 1 | True |
| ac9efa61-856d-4a72-803d-41e7f31b1ad5 | intent | complaint | request | cancellation | True |
| a1a8667e-6f74-4357-a361-6d2017525632 | topic | catalog | playback | catalog | True |
| 7aac1980-b773-4179-95e1-dbab3a3edf66 | severity | 2 | 5 | 1 | True |
| ba8ad855-82de-463e-9ae3-ce5ebc6fee4c | intent | praise | request | praise | True |
| dc594c03-5f09-4228-9ef0-6ff5a715033e | topic | other | usability | other | True |
| 0a79b240-d1c2-48dd-b220-0ff20ee4e171 | severity | 1 | 5 | 1 | True |
| 93b5b450-ff4e-449f-9b2c-75a0f378d0a0 | intent | unclear | request | unclear | True |
| 68bc42e5-e28f-49f5-965f-f6ed1e163bf3 | topic | usability | support | usability | True |
| b3607d6a-e9a6-4acf-a584-e022efa37ecf | severity | 4 | 1 | 4 | True |
| d38dabbb-2718-416a-8d6c-1110b276e3b1 | intent | unclear | complaint | unclear | True |
| 3bef4a21-5ce7-4eff-b067-9deb45becce1 | topic | other | access | other | True |
| 4dd9fee9-bcfe-4a0d-bcb8-4470a3257c1e | severity | 1 | 5 | 1 | True |
| 1ee9c29d-f254-4aa0-a613-e92310652653 | intent | complaint | request | complaint | True |
| 03710026-d7b8-4f8e-b54a-2a39ef83efea | topic | catalog | access | catalog | True |
| cdf8ab83-2a97-410c-b80f-7e93324cfc1d | severity | 1 | 5 | 2 | True |
| b7a5593b-d63f-444f-bd44-c622e4f610c9 | intent | praise | request | praise | True |
| 533b3bb8-77dd-4217-ba57-20cebfc8c943 | topic | other | support | other | True |
| 11705670-6b82-4728-9bec-164138ce5a99 | severity | 2 | 5 | 3 | True |
| a77d8f41-a6ea-447f-a56d-48e49e05e19e | intent | praise | complaint | praise | True |
| 5cc499be-2128-44bc-bd66-f680f1dcba69 | topic | other | playback | other | True |
| 65d51f0b-b750-44c1-adbd-3c087602f4de | severity | 2 | 5 | 2 | True |
| aa6cc073-4a75-471d-a312-ebac21028458 | intent | complaint | praise | complaint | True |
| 866ac3bf-cad8-411a-81eb-e3d602981f12 | topic | other | billing | other | True |
| f9f87156-42c9-4a62-8707-28ccd4ab28e4 | severity | 2 | 5 | 2 | True |
| f3023b24-a91a-4814-bfc9-38fc9b2b4718 | intent | complaint | request | cancellation | True |
| cc678f39-94e7-4704-8ccf-9d6d74f28198 | topic | usability | downloads | usability | True |
| edb18d5d-c2b0-4c62-95cd-6e76ffd207dd | severity | 1 | 5 | 1 | True |
| 5b8c80a7-3ca1-4925-887c-97a4ba719a8a | intent | praise | request | praise | True |
| 476d759e-5fd7-4d6b-9736-d31b1262b9c4 | topic | billing | playback | billing | True |
| 5bd648e0-d322-445b-a2f9-c0f404f764b6 | severity | 3 | 1 | 2 | True |
| 2832ba48-e51c-4b1d-ba17-3dc00262cc1a | intent | praise | complaint | praise | True |
| a28d7177-8ecd-4f36-b90c-d1af82e8a724 | topic | usability | playback | usability | True |
| 0047a0a1-9bdc-4a7c-9519-426a187a5959 | severity | 2 | 5 | 3 | True |
| 6d59c594-64d4-418e-bd2e-7bd22d955836 | intent | complaint | praise | complaint | True |
| 91788a09-bf0e-4045-bce4-5b8ed81ad35d | topic | other | downloads | other | True |
| 996a2cc5-34e5-420b-b0a0-f05c0f243e0d | severity | 1 | 5 | 1 | True |
| c78fbdc6-4916-4324-b566-a397611eb72d | intent | unclear | cancellation | unclear | True |
| c7bdb4ac-604f-4212-bb7f-5c2a578f7b8c | topic | other | support | other | True |
| 18abd6dd-ae64-4cc6-917d-482b9d6fad3d | severity | 3 | 1 | 3 | True |
| ac63ef2f-4417-4192-9f35-931585421c30 | intent | complaint | cancellation | complaint | True |
| e3e8d6e0-2350-4673-a471-0c1612437046 | topic | billing | access | usability | True |
| 2a327aab-3c95-478b-a6f8-ed516acca6e3 | severity | 3 | 1 | 2 | True |
| 4055585f-9c86-4f37-a903-58e295bbfba5 | intent | praise | complaint | praise | True |
| 964e0246-27b8-4e4b-8111-58c18657843d | topic | other | billing | other | True |
| 8d466ce9-77c8-4d2e-996c-98345f6882dd | severity | 1 | 5 | 1 | True |
| caf6cb18-a8c3-462b-8e38-c56f6a041829 | intent | complaint | praise | complaint | True |
| 312646a4-9558-4bf1-bd65-1accedac6df9 | topic | other | usability | usability | False |
| 8771df66-f147-4fc4-b0eb-4adc54440fb6 | severity | 3 | 1 | 3 | True |
| 3dfa4aa7-fa4e-40ce-8730-7bf0cdcbfad0 | intent | complaint | request | request | False |
| 585b72f8-3617-43b6-a21b-800e524a6e70 | topic | other | catalog | other | True |
| 1314b05c-a42b-43cb-8d73-306375522742 | severity | 3 | 1 | 2 | True |
| f15a2b7a-7c97-4159-8c7d-a8d5e57880a1 | intent | praise | request | praise | True |
| da3a7fc0-22ed-436c-a924-28fb21820ab7 | topic | catalog | billing | other | True |
| b67267b9-316a-4500-8109-a8a432eb55f2 | severity | 2 | 5 | 2 | True |
| 4da8a4cf-e0e3-49cb-bbb2-0b476d7ed649 | intent | complaint | unclear | complaint | True |
| 1adc752a-b67e-4c91-b88b-b63c9231e04b | topic | billing | usability | billing | True |
| 159238fb-a86c-4de2-80ed-91f454170f96 | severity | 1 | 5 | 1 | True |
| 16b7ae58-0a4e-4cbd-905e-72dbaff16e53 | intent | praise | cancellation | praise | True |
| d7148b0b-ad87-4d45-80ce-de44630454ca | topic | other | support | other | True |
| eb23fac0-9816-4e95-9ecc-f38f514f7bee | severity | 1 | 5 | 1 | True |
| c29ffcdf-0306-4ea9-bb1f-83b646d7f061 | intent | praise | unclear | praise | True |
| 63f14c8d-0aa1-4def-9ffd-3f7b303e45e5 | topic | playback | billing | usability | True |
| 2c877919-8d72-4104-bdf2-ecd72efc2197 | severity | 1 | 5 | 1 | True |
| 61a180ec-95a3-42d4-b890-d892935e34ba | intent | unclear | praise | unclear | True |
| 1a0c247a-7d70-4a30-9e95-f6cc20012c6f | topic | other | billing | other | True |
| 45cc4859-a631-4c94-b459-ed5ad35ed3af | severity | 1 | 5 | 1 | True |
| 3b5d5cfd-f75f-4e91-bd6d-a1180ee58468 | intent | complaint | unclear | complaint | True |
| b290ce78-8a6d-4bdf-a40c-1010d4d3ae85 | topic | playback | catalog | usability | True |
| 1ad8beb4-7bd1-460b-a929-b024bb09d7fa | severity | 3 | 1 | 3 | True |
| a86be349-6426-4fec-b995-d2bf4dcd080a | intent | complaint | praise | complaint | True |
| 130cb788-19bf-4c08-ac98-5f36e0e2ba1f | topic | other | catalog | other | True |
| 33074641-74a3-4c2f-8585-e78b7cb60c24 | severity | 2 | 5 | 2 | True |
| 59c16e27-132f-4327-98de-efe77695c39a | intent | complaint | request | complaint | True |
| 43e0eebd-2307-4357-acdc-c430c429dada | topic | playback | downloads | playback | True |
| f30c43d0-9df7-474f-9dd5-3d01382c9d47 | severity | 3 | 1 | 3 | True |
| cdf6276e-c6fa-4ec2-8890-d891726dd535 | intent | complaint | cancellation | complaint | True |
| fa21db2d-8daf-468b-83ca-7db03f839c2b | topic | other | downloads | other | True |
| 527aa2d5-b181-4617-90e5-c72c56efab03 | severity | 1 | 5 | 1 | True |
| bccf3e01-5c07-4b6f-91b7-0a4fbbbb89ca | intent | praise | complaint | praise | True |
| a8f137a4-2eaa-4192-9da0-b93bcd3ae89c | topic | billing | catalog | billing | True |
| c7349b87-cd7b-4b42-a39a-0c0930cb5f1a | severity | 2 | 5 | 2 | True |
| 700b94c5-3146-44a0-8e38-deac8502ef1f | intent | complaint | praise | complaint | True |
| 1ff7e4b8-9a4a-46b1-9533-66533c529f17 | topic | other | playback | other | True |
| d8913fb3-5e06-44da-b9f3-aa10ca3d76cc | severity | 1 | 5 | 1 | True |
| dbc5815f-cba7-4d02-bd34-3569a3644a33 | intent | complaint | request | complaint | True |
| d26beb68-fae1-4814-8b86-82b9985ed666 | topic | catalog | playback | catalog | True |
| a171a11f-36c0-46e2-bf6d-6de81c3e3249 | severity | 2 | 5 | 2 | True |
| 57c22c6f-81c2-44e2-bfff-6412023e97ea | intent | request | complaint | complaint | False |
| ed3d1d5e-7f14-491f-b0a8-898480a4d75c | topic | usability | downloads | usability | True |
| b8fc7e5d-a8ac-4c79-a405-8c86c3647e88 | severity | 1 | 5 | 1 | True |
| 19c82f14-7448-43c3-8920-2d5f6994133a | intent | praise | complaint | praise | True |
| 354033bc-538d-4899-a412-ec76c6a1207c | topic | usability | support | playback | True |
| e90594a6-003e-43c0-a391-5b6502e86b7b | severity | 1 | 5 | 1 | True |
| 9b904ba7-3b78-4aea-ad23-21e477c7f705 | intent | complaint | praise | complaint | True |
| 43277fda-1699-472f-b62f-647fc2624609 | topic | playback | downloads | usability | True |
| 6989561e-f3cd-4551-87cc-7aaada811b8e | severity | 1 | 5 | 1 | True |
| 758fd733-797c-4c7d-87f0-ecfffba3eb99 | intent | complaint | request | complaint | True |
| 2134b583-9234-44ab-9152-3161077665c5 | topic | other | downloads | other | True |
| 259f91e7-f55c-4e99-ae73-1cf384ca33fa | severity | 1 | 5 | 1 | True |
| bdf377c9-174b-4886-96bc-7489cfcb7923 | intent | praise | request | praise | True |
| 15d191ed-6934-4e9d-b053-51e0871dfba4 | topic | billing | catalog | billing | True |
| 7375afac-d64a-47ce-86c2-4bb6ab31db8f | severity | 1 | 5 | 1 | True |
| 49dbd304-0c86-44aa-9e84-7293dc813a6e | intent | complaint | unclear | complaint | True |
| 8dbb7897-ea47-4115-b06c-8ea5f01bcd8d | topic | playback | billing | playback | True |
| 31b175b8-eba5-4db7-9a08-9a5f40ea37ec | severity | 4 | 1 | 3 | True |
| 52c8d8f4-492b-4fe7-9926-086d0aea0ab8 | intent | praise | cancellation | praise | True |
| 6a98ee7f-af2e-4d1e-b4a2-27536dca19fc | topic | usability | other | playback | True |
| e3e070a1-8468-43d1-bc87-2a50932a43fa | severity | 1 | 5 | 1 | True |
| eccfa79c-6821-4c58-94f0-603c9d37d76a | intent | complaint | request | complaint | True |
| 06146502-b474-418b-beb8-5cca8e20cb25 | topic | billing | other | billing | True |
| c414fd92-aaff-458b-86db-42037fd8f4a6 | severity | 3 | 1 | 3 | True |
| 1860782c-e046-41a7-9676-684692a3385a | intent | complaint | cancellation | complaint | True |
| a38dee31-56fd-4ec0-80cb-83469272ccbd | topic | other | catalog | other | True |
| 18d0b1b9-2d2d-45d4-95da-e685e4df92bc | severity | 1 | 5 | 1 | True |
| 3a9252f6-f004-4c31-ba3c-c544cc877d67 | intent | praise | complaint | praise | True |
| 591c496d-21c6-4f6a-83e0-4455481e5213 | topic | other | access | other | True |
| e5c2735f-e85a-40db-9dd8-db9f7e67253b | severity | 3 | 1 | 3 | True |
| 5dc50cc3-c93a-49c6-b2cf-0199c909df18 | intent | praise | cancellation | praise | True |
| 1682d31f-c1e4-4bc0-af3a-e220c549f202 | topic | other | downloads | other | True |
| b9c6136e-4de5-4a61-8be5-411c29837efa | severity | 2 | 5 | 2 | True |
| b1e4eaac-8d3d-4656-97c7-a16c5f1f38d3 | intent | complaint | request | complaint | True |
| 8a0fe2b4-ede4-48c9-aed9-6d34bc62e805 | topic | usability | access | billing | True |
| d8623953-b14b-4458-9703-48705a5ecbef | severity | 3 | 1 | 2 | True |
| d13e2eba-8f09-42fd-8859-d661f6ff6716 | intent | complaint | cancellation | complaint | True |
| dcd55ef0-3760-459b-ac32-213603d7d8bb | topic | usability | catalog | usability | True |
| d8c1707e-c76b-482e-bd64-ec82caa008d3 | severity | 2 | 5 | 2 | True |
| 46e2f76e-2547-4798-a83b-8ad5a9048cb9 | intent | praise | complaint | praise | True |
| 2a7fc407-2119-40c3-94ff-63ca27090810 | topic | other | billing | other | True |
| a1173780-b16e-4cd3-80ed-fea2e9dbb96a | severity | 3 | 1 | 3 | True |
| 76ceba23-bac1-42d7-91fa-a637f360631a | intent | complaint | praise | complaint | True |
| bbaa16fa-547e-48c5-8d7c-d748e8446c1d | topic | other | usability | other | True |
| 7af2312c-9d55-4beb-857b-1216160d519a | severity | 3 | 1 | 2 | True |
| dd67072f-9e9e-4e58-bb2a-59fc96bd7d24 | intent | complaint | request | unclear | True |
| 19b80977-ed5f-4547-9f71-1ddc6f4b3285 | topic | usability | support | usability | True |
| 1045e27c-c254-41f5-90c3-746cba119273 | severity | 5 | 1 | 4 | True |
| 29cee0c7-fd0a-42a1-b6e3-7da407fe7d11 | intent | praise | request | praise | True |
| 91581ad7-4f4a-4b88-a7f4-a3e04cbc983a | topic | other | access | other | True |
| 4f6bd912-7894-444f-b233-93c0dad3be91 | severity | 2 | 5 | 2 | True |
| 862e3496-1a86-4637-919b-947546b8d852 | intent | complaint | unclear | complaint | True |
| 2013dbe5-4624-4d4a-844c-7334a4b8f4ef | topic | usability | billing | usability | True |
| bdbd63ea-5afe-4701-b413-7ee60a94a575 | severity | 1 | 5 | 1 | True |
| 11acaf62-731b-404b-a7e8-7de87b0b7e96 | intent | complaint | praise | complaint | True |
| a4b5bdcc-b9a6-4205-87da-ce4f15030852 | topic | catalog | downloads | usability | True |
| 206b8667-5858-430f-8d75-1658cab512e3 | severity | 2 | 5 | 2 | True |
| a1509ad1-086a-401c-9152-5bd8d9140d89 | intent | complaint | request | complaint | True |
| d4b93541-436b-4daa-9359-728d1553a127 | topic | billing | access | billing | True |
| 11a0185e-41ba-4a1d-9b73-b8a159961782 | severity | 1 | 5 | 1 | True |
| 2b20ee7f-0b37-4a3e-8db7-0edbee5c88e0 | intent | unclear | praise | unclear | True |
| b7e31052-1a78-4d31-a142-2fa07560107f | topic | catalog | playback | catalog | True |
| ba012651-e56a-41ca-9849-27f56a9f8651 | severity | 3 | 1 | 2 | True |
| eb7d3f29-6df1-484b-8b3c-dc031ff9404b | intent | complaint | unclear | complaint | True |
| 44fe12c4-59b5-4e16-82bc-6bb742b14e40 | topic | billing | other | billing | True |
| ac667649-d8a5-4a6f-9c54-0ed84f9ed069 | severity | 2 | 5 | 2 | True |
| 2b85d3e3-bd28-4dda-b20e-f6eb3037fedb | intent | praise | cancellation | unclear | True |
| 6667bf7c-da15-4664-b652-186d75ba5ed7 | topic | catalog | usability | catalog | True |
| fe81030c-d596-4c67-a736-e9120e420de4 | severity | 1 | 5 | 1 | True |
| e505fbc2-e718-4b34-b464-e47677b52a50 | intent | complaint | request | complaint | True |
| 9a1e2015-4be8-430b-ba17-a16c0f672168 | topic | playback | downloads | playback | True |
| 7c702285-9538-45be-92c4-a7e92144ff32 | severity | 3 | 1 | 3 | True |
| b1bfd2e1-4e2c-451a-badf-4480b987a741 | intent | unclear | praise | unclear | True |
| d31f12fe-0e2b-4dd5-9692-88fc4e855335 | topic | other | downloads | other | True |
| ecaeb4c1-8314-4971-a307-ab35cc3e1b2f | severity | 1 | 5 | 1 | True |
| 19c1b642-74c5-4db1-b0de-2921d97ff8e1 | intent | complaint | unclear | complaint | True |
| d6be76ca-a9ac-4180-aea1-5a6ea87095d4 | topic | billing | catalog | billing | True |
| 885bcec9-9887-4491-9090-0c50144ed7b0 | severity | 3 | 1 | 3 | True |
| 3475302f-9357-4c3a-bd74-8d392e1fd65b | intent | complaint | praise | complaint | True |
| f60dbfb6-6e17-4a7d-9bad-905e5375e54b | topic | usability | catalog | usability | True |
| 631d10ab-9249-4551-bd8c-46ba24b6af31 | severity | 3 | 1 | 3 | True |
| 9b239e89-1a93-452c-a4b2-87abf1879f53 | intent | unclear | cancellation | unclear | True |
| 699c0bb0-8813-402c-870d-4a19dcb30cd5 | topic | other | billing | other | True |
| d78d3992-30fc-46f6-93e1-3c0af2e67c7a | severity | 3 | 1 | 2 | True |
| e73994c0-9f3a-49fc-b48c-8a5d74d3b1ce | intent | complaint | cancellation | complaint | True |
| 11653a1a-660a-4b1e-a2bd-a1f0a1fac100 | topic | other | usability | other | True |
| c7306e98-a26e-4b11-8935-0c3b4ada2edc | severity | 1 | 5 | 1 | True |
| 9e6e2d7c-4be5-49a4-980f-47dfb1c6e8fd | intent | complaint | unclear | complaint | True |
| 079f3b23-f7ad-4c86-b012-12b947fe1b1e | topic | usability | support | usability | True |
| dfdb5010-802d-4fba-9d7b-a602d56818f7 | severity | 1 | 5 | 1 | True |
| 896bf2b9-33e0-488d-8d1c-5b5181ea3ee5 | intent | complaint | praise | complaint | True |
| eb734cf5-486c-463b-b145-be574b30b9dc | topic | catalog | billing | catalog | True |
| 9aa96c64-5872-4ddd-b4e5-41b733f9ce73 | severity | 1 | 5 | 1 | True |
| b07761f1-cbdb-4af4-a7e8-66026bc42fa9 | intent | praise | unclear | praise | True |
| 4c032a90-a37a-4533-909b-0e8506479647 | topic | billing | usability | billing | True |
| 443ee4db-2c7b-4b69-b4f6-2f6b3e83a5c3 | severity | 1 | 5 | 1 | True |
| 2c049ea2-da02-4b56-b62f-d1b682d53027 | intent | complaint | cancellation | complaint | True |
| 2ef295c2-ec33-44b7-bd35-e8a47997da29 | topic | other | support | other | True |
| b9d38ae8-97e6-4a36-ac94-3ceff87e962d | severity | 3 | 1 | 2 | True |
| da5eea59-3b15-4481-9c1e-f4d0a76174a4 | intent | praise | complaint | praise | True |
| 248121a4-5584-4d29-be24-b46507c324e7 | topic | playback | billing | playback | True |
| b423137a-941d-4030-a0d2-00d44f84651b | severity | 2 | 5 | 1 | True |
| 79d26333-7ef4-4117-b6d2-9b972100f435 | intent | complaint | praise | complaint | True |
| aa4018a2-968d-4973-81c3-ad478763ae28 | topic | other | billing | other | True |
| b49863f8-53bb-4153-b1c2-b643612fa89c | severity | 2 | 5 | 2 | True |
| 8582b571-1a18-483a-b257-c5233cdc71c6 | intent | cancellation | complaint | cancellation | True |
| faed1cc9-8ee6-45e5-9e35-07cfdc7042be | topic | other | usability | other | True |
| 5abb3e79-0bfc-4256-bb6d-44b6ba18fabb | severity | 3 | 1 | 3 | True |
| 77096363-2f89-4ba8-b1f8-0f66d04c0502 | intent | praise | request | praise | True |
| 377d1510-a87e-440d-92e4-a9620c3c1781 | topic | playback | other | billing | True |
| 7d71c5b7-2e72-4c28-b0cf-45eba1e9b7f0 | severity | 1 | 5 | 1 | True |
| bb982512-7790-400b-b01a-9c0552fed3cb | intent | complaint | unclear | complaint | True |
| 3274934b-690c-4dde-a8cf-44469afbf29c | topic | playback | downloads | playback | True |
| 7136e887-9a9e-41f8-8add-da85294619a1 | severity | 3 | 1 | 3 | True |
| efcf4169-3676-41a1-81ff-eb90f5d2e8db | intent | request | unclear | request | True |
| d597d519-34b1-43ba-8873-735431506a51 | topic | usability | billing | usability | True |
| 10993646-d552-42ed-80bd-880885fe68c9 | severity | 1 | 5 | 1 | True |
| a559bc83-6ecc-4965-bcd6-d2e53aead164 | intent | request | praise | request | True |
| e86a1f59-e769-49d7-976e-950c0b5abeb4 | topic | catalog | downloads | catalog | True |
| 239ffef7-efe5-4b80-aa7c-fb6ea604e194 | severity | 1 | 5 | 1 | True |
| 43b89d8c-1500-4e01-89d4-81898390a9e9 | intent | praise | request | praise | True |
| 71a70677-94ca-4565-9339-1d9570e78afd | topic | catalog | other | catalog | True |
| c68a4be0-6e41-4e0b-9b91-e55421e1786d | severity | 3 | 1 | 3 | True |
| 407ae24c-81a6-4714-ba8e-250a2fa85ead | intent | complaint | unclear | complaint | True |
| f7002cc4-376f-433d-ac86-c4ac0c3c517f | topic | other | billing | other | True |
| 1101ce90-d863-43f9-b822-68915b211433 | severity | 3 | 1 | 2 | True |
| dc325491-5b42-4730-a3ac-2af2bae515c2 | intent | unclear | complaint | unclear | True |
| 353204b5-dccf-4c42-8e49-a54bbb2bfff0 | topic | other | usability | other | True |
| 0ada4d8e-c5c1-4076-a19e-9e22e0611d63 | severity | 3 | 1 | 3 | True |
| 74e89260-0fe6-43ee-a38f-2f08899b795e | intent | complaint | request | complaint | True |
| 723c39fa-8e2e-4c93-a569-5ebdf6a4cb2b | topic | other | catalog | other | True |
| f060ffb2-8856-4884-b2c4-cf8fcd4a65c3 | severity | 3 | 1 | 3 | True |
| 3d8661a2-f80b-4701-b891-4afd0192b571 | intent | praise | request | praise | True |
| 07625dfa-364f-47e8-8f2a-21e521179aab | topic | usability | playback | usability | True |
| 75dddfca-35d4-4cad-9f5c-45c87f580c0e | severity | 3 | 1 | 3 | True |
| 8157a213-fa8b-420d-a0df-6fb29af8de4a | intent | complaint | unclear | complaint | True |
| 8eca4318-c90b-49e6-95fe-f1c5bd1b4d20 | topic | usability | billing | usability | True |
| 3442424b-c444-4751-be4d-865900d575d3 | severity | 1 | 5 | 1 | True |
| e2538dac-1f51-4bdf-9217-250cfccc4f89 | intent | praise | cancellation | praise | True |
| c4f425f2-f0a6-44b2-842e-1159b603c9bf | topic | other | support | other | True |
| 0ad97750-b480-435f-9dd4-f33483f18138 | severity | 2 | 5 | 1 | True |
| 333bbedd-ff5c-4cb8-9bef-65faa245d935 | intent | complaint | request | complaint | True |
| 0a071e56-3e69-4e29-a9a3-29b351f53917 | topic | other | playback | catalog | True |
| 992f61c8-2f8d-4211-870a-0b50204bc959 | severity | 2 | 5 | 2 | True |
| e0098fd8-80e1-410f-b7ca-cfd9980931a6 | intent | praise | request | praise | True |
| dc1da35a-aca7-414a-a1a5-81fe3651812c | topic | other | billing | other | True |
| 81ae3cc0-a591-4af7-9ffd-4e4f1702049c | severity | 1 | 5 | 1 | True |
| cb8fb7f6-f237-4cb4-b926-bfa97e06cb5f | intent | praise | complaint | praise | True |
| feda411c-a4ab-4fff-92e5-8045d791482c | topic | playback | catalog | playback | True |
| 0d13fb2f-9508-482a-9aa1-4e641016eef2 | severity | 1 | 5 | 2 | True |
| 84754a07-30af-45b2-aaf5-7b2f85b8335d | intent | praise | cancellation | praise | True |
| 5a9f678e-cc4a-46c6-bb23-a5a7978d6fd1 | topic | other | catalog | other | True |
| 8b192585-75ea-46e7-91e4-8ce415c00484 | severity | 2 | 5 | 2 | True |
| ccf6b276-6341-47d6-b999-1805c7ec32e1 | intent | complaint | request | complaint | True |
| 43a05102-a306-4840-a0e7-7cb0c7d8414f | topic | other | access | other | True |
| de9b4b54-ed58-4e23-a6b0-f9d8fa45dd66 | severity | 1 | 5 | 1 | True |
| 4df36f72-27b5-478e-880b-34a3e8b54da3 | intent | praise | request | praise | True |
| 3cb5c17a-71bd-43f0-b817-959f8b7884ca | topic | billing | usability | billing | True |
| 859c42e8-b571-4415-954c-074acea168ac | severity | 2 | 5 | 2 | True |
| 110c7b57-3ea6-481d-911a-92b4fda3654d | intent | complaint | unclear | complaint | True |
| ea937420-b1c3-448a-bc0b-34f4ba63af73 | topic | access | other | access | True |
| 36f96d9d-ab69-4dbd-a39e-1868c716da9e | severity | 1 | 5 | 1 | True |
| 7f61dab4-ad78-43c4-9fb1-c52a676d3184 | intent | praise | cancellation | praise | True |
| c65576e5-3148-4fd7-9e78-d29516163398 | topic | other | playback | other | True |
| 0692c00e-2c16-4087-9a0e-ca0bfcf6dec2 | severity | 1 | 5 | 1 | True |
| e89cc072-b645-4de5-b556-2f609fa245fd | intent | complaint | request | complaint | True |
| 7c227da1-bd46-4540-abf6-82cd4d7ab826 | topic | other | billing | other | True |
| 8e4404cc-ed62-4ed2-91f2-63505f7601b3 | severity | 1 | 5 | 1 | True |
| 9f633930-1368-4239-a182-aeae204ca5b3 | intent | praise | request | praise | True |
| 16acbf30-96f5-4456-bde0-557f1406ba85 | topic | usability | downloads | usability | True |
| dfe32d79-5039-459d-9bfd-fe194e57ee4d | severity | 1 | 5 | 1 | True |
| 978bdf3a-292a-4e3e-8d65-50f051e35c35 | intent | unclear | request | unclear | True |
| aad1e0fc-59bd-4921-9605-aa0d2ea801f4 | topic | other | catalog | other | True |
| a8edce3a-4ba4-4724-b526-bf89baeea6e4 | severity | 2 | 5 | 2 | True |
| 348c7f98-6f14-48d4-84cd-b45cdb5b9ee7 | intent | complaint | praise | complaint | True |
| ce62be88-0fd8-4669-8bb8-a5857f1338cb | topic | usability | playback | usability | True |
| 8a7ffe24-b376-4ee2-8e3a-ce067d26879d | severity | 3 | 1 | 2 | True |
| 6c165826-4bff-4a75-ba15-6e15dec2bbc4 | intent | complaint | request | complaint | True |
| ea5e8cd9-5729-4295-9c4a-eb228ad84e74 | topic | other | downloads | other | True |
| 20819770-27ce-4bee-8cbd-42e4e7f69c6c | severity | 3 | 1 | 2 | True |
| 2afa769a-7d93-4d14-b44c-00f52b27e9ab | intent | praise | request | praise | True |
| dadb163e-a71c-441e-8a8f-b0dfc23279a0 | topic | other | support | other | True |
| 60170db8-a2e8-44ca-9f0a-6e99639f80f2 | severity | 1 | 5 | 1 | True |
| d6430cbb-7e92-466f-b8bd-9efce466ba68 | intent | complaint | unclear | complaint | True |
| a97e4dc9-518a-4d6f-abde-5d98d6bf47b1 | topic | billing | access | billing | True |
| 4442ea94-6691-4514-bcb4-e7a764f5706d | severity | 1 | 5 | 1 | True |
| d32dcc22-26d1-4841-9540-5582f20b7122 | intent | complaint | praise | complaint | True |
| 6ead3bab-9dfb-4568-80b6-e7de506381eb | topic | other | billing | other | True |
| 63e3f48e-6cc4-4615-854a-31b6fb3db062 | severity | 1 | 5 | 1 | True |
| c0b4fd0c-c742-4d95-9223-6f2bca74b024 | intent | praise | unclear | praise | True |
| 0acaee87-9093-4f09-a6b0-ffc80b00b8e0 | topic | usability | downloads | usability | True |
| 74ead357-46d5-42c9-9576-1880a0ec98d5 | severity | 3 | 1 | 3 | True |
| 859bb081-6bce-4cae-8479-0b0b0f84cdb1 | intent | complaint | cancellation | complaint | True |
| a123e8b1-f739-49a0-b1db-fb3a9ec00ac8 | topic | usability | support | usability | True |
| ce6fdbc7-d91f-405f-aada-57d121a14b80 | severity | 1 | 5 | 1 | True |
| 3388b48b-7b4e-4af0-80f7-e61611a0696b | intent | praise | complaint | praise | True |
| 2bbb504e-55f7-4a61-96d8-d9be189a53aa | topic | other | access | other | True |
| 9d305458-dd8d-42fc-8ace-7aef0a98decb | severity | 1 | 5 | 1 | True |
| 3be2da78-505e-42e4-8494-3ccb23faa7ba | intent | praise | cancellation | praise | True |
| ef6fa519-66bb-4a33-ac77-8eceffdea552 | topic | other | downloads | other | True |
| 45ab5070-9906-437c-bd3e-2fff82bb535b | severity | 3 | 1 | 3 | True |
| be193cdc-4393-4436-95d6-3274f554e9e2 | intent | praise | unclear | praise | True |
| 2410d7b8-69d6-4a44-b17b-75f6d0dcedd8 | topic | billing | catalog | billing | True |
| 403595ad-9d56-455b-a004-7c3e84ff4190 | severity | 3 | 1 | 2 | True |
| 0e390246-ddd1-45b3-bdf7-389dd212217f | intent | praise | request | praise | True |
| 17d9a646-b328-48f7-816d-7589b3f090f8 | topic | other | playback | other | True |
| 336fbbba-ef91-48d8-b349-f7f211e05c34 | severity | 3 | 1 | 2 | True |
| 137e3e4f-9d7d-40f0-90b3-785d348be628 | intent | complaint | unclear | complaint | True |
| 715fe799-3aa4-4f79-9431-5c5fd837f955 | topic | other | billing | other | True |
| 0f2e6432-1957-4f75-909c-8268c34332fe | severity | 2 | 5 | 2 | True |
| 1f64b63b-a10f-4c19-8eae-628331bf5357 | intent | complaint | praise | complaint | True |
| 31fe3c7f-3b1b-4273-9135-a1201b3624a2 | topic | other | usability | other | True |
| d229aa98-c4b4-42ba-8f93-101e47c2f969 | severity | 2 | 5 | 2 | True |
| ed41148d-6573-473a-b1d9-a374e492d449 | intent | complaint | request | complaint | True |
| 2d1e02b4-42bb-4959-8e3b-4e22ba9d0127 | topic | other | catalog | other | True |
| 46632653-6434-434d-ac73-4b1a9717411b | severity | 1 | 5 | 1 | True |
| 5d6ba47f-02be-4b99-bb51-0ec800a447cf | intent | praise | request | praise | True |
| 92aad879-6179-478e-b7a5-8dcf52855fe0 | topic | usability | playback | usability | True |
| ce5dcedd-64bb-4133-b89e-271ddfec49b1 | severity | 2 | 5 | 2 | True |
| b250f390-2a15-49d9-84d4-85976ea15dc1 | intent | complaint | unclear | complaint | True |
| 847c72fb-b706-4ac3-9440-e7c08401a433 | topic | billing | usability | billing | True |
| 62948852-571f-4665-8677-60d67bf0325f | severity | 1 | 5 | 1 | True |
| aea67e58-e563-41a6-8561-ea36c30a705d | intent | complaint | praise | complaint | True |
| babb8104-7cd7-47c1-aa81-a79a6534e372 | topic | usability | access | usability | True |
| 3280fb33-8dfe-40fd-873f-8d871d216a23 | severity | 2 | 5 | 2 | True |
| 21313c7f-ee22-4fea-8884-2af156a96f75 | intent | praise | unclear | praise | True |
| 2110773d-b42b-4071-ba0c-574dedc69ab3 | topic | other | playback | other | True |
| 62f6881a-8526-447e-902a-a1a1a863a348 | severity | 2 | 5 | 1 | True |
| 1d32e11e-53dd-4633-a7da-bda8b3a89c17 | intent | complaint | cancellation | praise | True |
| f6255547-5609-4d53-b583-1771f5c077f9 | topic | other | billing | other | True |
| 540c9a43-b6c2-48d8-b45e-3b208b771192 | severity | 1 | 5 | 1 | True |
| a723d2e1-3fa9-40de-b188-2872deeae969 | intent | cancellation | praise | complaint | True |
| e34a86b4-c506-4960-91ca-b96038f57959 | topic | playback | catalog | playback | True |
| 1b3094c7-088b-419d-9076-7ef276c4a9a5 | severity | 4 | 1 | 1 | False |
| 24ddf34b-283b-4fc3-a7ac-770f67c54162 | intent | praise | cancellation | praise | True |
| 41503f01-d3a1-431e-9980-a80f9e880df1 | topic | billing | playback | billing | True |
| 888499e3-3877-4fe9-b6d8-66e3a31d48ca | severity | 1 | 5 | 2 | True |
| 7e770c3e-c4e1-4939-9d24-7b930c8febfb | intent | praise | unclear | praise | True |
| a6e1af17-5cae-4e6b-9ba2-0c8741115c47 | topic | billing | support | billing | True |
| ef3cf69b-d63e-4f89-8d86-69d173b47c25 | severity | 1 | 5 | 1 | True |
| c299c2ff-52d1-44d9-b7ad-b6201dec90ec | intent | praise | request | praise | True |
| 4b225d8d-666d-4163-bbc5-7ec58010d0eb | topic | billing | usability | billing | True |
| 469a689b-adc0-49b1-9ca0-ca2f41fa21a6 | severity | 3 | 1 | 2 | True |
| 3e18a990-1c92-4d02-86b3-77c98c4ffb27 | intent | praise | complaint | praise | True |
| 64a5f464-8480-4450-83fb-f88a1659f189 | topic | downloads | playback | downloads | True |
| 9e2855e2-a66a-40f5-8218-d8cb5911127f | severity | 2 | 5 | 2 | True |
| a44f3ede-7074-4b48-aa45-c06641083faa | intent | complaint | praise | complaint | True |
| 374bc986-df20-4c0a-b158-04c498445c53 | topic | other | playback | other | True |
| 60d502c6-228c-48da-a9c7-4a60bc49b13a | severity | 3 | 1 | 3 | True |
| 0274684d-4415-4499-9d1d-6164330448cf | intent | unclear | cancellation | complaint | True |
| c529c325-22f3-414b-93d9-76711b5cd92d | topic | other | billing | other | True |
| 9df875a1-409d-4bfa-bd6b-a667cd21f9cd | severity | 2 | 5 | 2 | True |
| 4c9dcdf5-b263-4a7f-bcda-d05cd181f402 | intent | praise | request | praise | True |
| 2abe0201-edd9-46b4-880d-ff13cf09ce82 | topic | billing | other | billing | True |
| 3933ba33-aeba-4441-8302-f99ae15529b8 | severity | 2 | 5 | 2 | True |
| 8720c3b8-520e-47d9-bb13-c053833f3132 | intent | praise | complaint | praise | True |
| c6e407ee-56ea-4c63-8fd8-9d26f107fd55 | topic | access | billing | access | True |
| 2e38f1a4-6bb4-46ca-90d8-f7861674a295 | severity | 2 | 5 | 2 | True |
| e1069da6-2cb5-4695-86fe-3d988c8dd6d8 | intent | complaint | praise | complaint | True |
| 9f4d1000-ad55-4851-b1e9-86f2f2cd349c | topic | playback | downloads | playback | True |
| 7a125d91-ef2e-4b3b-8c3c-0d7d536f6ed6 | severity | 1 | 5 | 1 | True |
| d4ddc46b-0270-4db3-a844-faaad08cb1f9 | intent | praise | unclear | praise | True |
| b5991945-072b-4f2e-b59b-cc116706381b | topic | other | downloads | other | True |
| a66b2f26-aa76-45c9-8fd5-b916773c9555 | severity | 3 | 1 | 3 | True |
| d898636a-78ca-47e2-8c8a-9ef9f0f01f92 | intent | complaint | cancellation | complaint | True |
| cb36c41e-b86e-434f-9b82-da442958e5fe | topic | usability | access | usability | True |
| 6198ed29-44d8-45b5-8e2f-42a4de706e68 | severity | 1 | 5 | 1 | True |
| 1c6bd067-8daa-45b2-a5dd-5cb44f1b8a0f | intent | complaint | unclear | complaint | True |
| e94ac333-ba74-4dba-8665-218f5939dd1f | topic | other | playback | other | True |
| 003ac7dd-70e5-45f1-acfa-1c86f9cb1da4 | severity | 2 | 5 | 2 | True |
| bcfe4071-6367-4e50-8824-8a9faa669bca | intent | complaint | praise | complaint | True |
| efc297bf-e7b9-4cd6-87fd-4bb85a4647e6 | topic | downloads | usability | downloads | True |
| 620a94ab-4b8c-4525-bbc9-f47d26fd03da | severity | 1 | 5 | 1 | True |
| 3c0437bd-7b42-4997-9df1-0eaacdef2aab | intent | cancellation | complaint | cancellation | True |
| 92e6337d-c384-4458-b94b-b4f453521cf4 | topic | other | usability | other | True |
| 1c438cd9-eb51-45cf-a627-5740ddbe5d2e | severity | 2 | 5 | 1 | True |
| 2efbca00-c475-430e-ac79-acb195a08bfc | intent | unclear | praise | complaint | True |
| b3f5b499-a8ee-4e00-92dc-5859d2d0bc09 | topic | billing | playback | billing | True |
| 88fd63f4-c82b-478b-a71d-ff3641d693ff | severity | 2 | 5 | 2 | True |
| 7d7adf3e-0fc3-4b21-a83a-7bd3d95be49a | intent | complaint | unclear | complaint | True |
| 423e1c74-f7c8-41d6-9a14-dacb79dfeebf | topic | billing | support | playback | True |
| 893abb4e-be72-4e18-a58d-e6deff62df6a | severity | 1 | 5 | 1 | True |
| 05512fed-2335-4d91-95ed-e3727932ffbc | intent | unclear | complaint | praise | True |
| 751a7648-3f09-490d-bc55-a6eb306ec743 | topic | catalog | access | catalog | True |
| ff60b4aa-576f-4664-afe1-31e7c9e2a6e1 | severity | 1 | 5 | 1 | True |
| f7eba217-ae81-4a68-9387-e811d4130b21 | intent | praise | unclear | praise | True |
| cfe51dc8-e807-4ba9-823b-37d34eb1f44f | topic | other | support | other | True |
| 5d04e246-cc19-4742-a007-418fa5158d5e | severity | 1 | 5 | 1 | True |
| 6348ebfb-be08-4287-9ba2-b0dd9062a94d | intent | praise | request | praise | True |
| 4392575f-14d2-4780-b5a9-a60cfe2a3819 | topic | other | playback | other | True |
| eab53935-913e-4a2d-a746-fae0c5152e23 | severity | 1 | 5 | 1 | True |
| c1b683fc-58cb-470c-b591-e2393748883c | intent | cancellation | praise | complaint | True |
| fc5aad78-d57c-4a77-9df3-a2484138ab07 | topic | billing | downloads | billing | True |
| 35499b64-28f4-4f92-8f54-8dc908d79af7 | severity | 2 | 5 | 2 | True |
| 471c04bf-a248-4364-91af-96c6804e11e3 | intent | complaint | praise | complaint | True |
| a8c5bb1f-b0ec-414e-92cb-b960c71e56e1 | topic | other | usability | catalog | True |
| 5f9ffdf6-bf93-4c18-9684-3665bd211f4e | severity | 1 | 5 | 1 | True |
| 4fe51d78-1fa7-4287-80ae-389907674cb8 | intent | cancellation | complaint | cancellation | True |
| ce99b2de-d098-41db-abb1-ae6fc873caf0 | topic | usability | support | usability | True |
| 2996f586-36c9-425e-82c0-ff6198d43e35 | severity | 1 | 5 | 1 | True |
| 3950e4bd-9304-41ca-aa80-6508167c6504 | intent | complaint | cancellation | complaint | True |
| 84a6d5f4-b025-4ab0-9605-9bd5ccba6e54 | topic | usability | playback | usability | True |
| 899f6d47-c959-417b-8ee5-d56ec85db98f | severity | 3 | 1 | 2 | True |
| 32aa399c-bef2-411f-9d4d-776db0c2c704 | intent | complaint | unclear | complaint | True |
| aa59ba9c-71e0-4e58-97df-8aab4418b885 | topic | usability | billing | usability | True |
| cbbba921-2cbd-49fe-9430-aa11237fc4c1 | severity | 3 | 1 | 2 | True |
| b1a755d2-aa12-4e66-8e0f-b1f5dd61ac3e | intent | complaint | praise | complaint | True |
| 9e24a431-4c68-4f80-a228-ee9520b0910e | topic | billing | catalog | billing | True |
| 04946089-fe3b-4e63-8ff6-ed2ea823c504 | severity | 4 | 1 | 3 | True |
| 786907be-ae76-49b9-af46-b21128d40555 | intent | request | praise | request | True |
| 9ca29dc7-c161-4d44-9dc2-7ae4371167ce | topic | catalog | other | playback | True |
| 03bef169-f026-4b5b-a333-f36c3a21727f | severity | 2 | 5 | 2 | True |
| 0202419e-b19f-49e8-92a0-b19522e3182a | intent | complaint | cancellation | complaint | True |
| a175170e-131c-42c9-8201-a08e6680a764 | topic | billing | downloads | billing | True |
| 63f6f532-9150-48cc-bde4-405f2b8ccffa | severity | 1 | 5 | 1 | True |
| 4fac6488-0b93-4751-8ed3-04579061a6a1 | intent | complaint | unclear | complaint | True |
| da4d4c16-4c0c-415a-8180-8ffb23ffe83a | topic | usability | downloads | usability | True |
| d49763d9-64de-40ff-b767-0e25ea17dd3a | severity | 1 | 5 | 1 | True |
| bb02f179-63b0-4507-854f-f2b96bfc2bef | intent | praise | cancellation | praise | True |
| 354c8a93-827e-475a-8bb8-8f224eef52a2 | topic | access | billing | access | True |
| 356ea0e6-b3ec-45cb-8ee8-822c5c60dce1 | severity | 1 | 5 | 1 | True |
| 92dbd956-708e-4cf6-aab0-842d65ff2a27 | intent | complaint | request | complaint | True |
| 4e16c6a4-65a3-40ab-8b49-2d29c73b08b6 | topic | playback | downloads | playback | True |
| 493fc02c-c666-4017-be26-d05cba1d8855 | severity | 1 | 5 | 1 | True |
| dc7566df-3723-4997-b184-a124cebbdb2b | intent | complaint | cancellation | complaint | True |
| 2a63689b-a516-44ab-b4b4-43e5475c251d | topic | billing | usability | billing | True |
| e979780a-ab57-4fba-a7ec-b44c389f11b2 | severity | 3 | 1 | 3 | True |
| 1848a209-e91d-4d9d-aa39-b3842e2dddc5 | intent | request | cancellation | request | True |
| 9c696098-61f3-4915-b925-99a4839b13a2 | topic | other | support | catalog | True |
| acf8ce78-2fce-4a2a-8517-4a8d29ed959b | severity | 2 | 5 | 2 | True |
| b8a8208a-92c4-4a07-b261-5b18ab076427 | intent | complaint | praise | complaint | True |
| bb39b316-0a0a-4d34-8a57-2d0fb95debd1 | topic | billing | access | billing | True |
| 90c9ff43-8746-4459-9300-59bd18039346 | severity | 3 | 1 | 3 | True |
| 80e838a0-5abb-4453-a4f1-d3ef279e8024 | intent | cancellation | complaint | cancellation | True |
| 7d86960a-7773-457a-b37b-765a42c49d2b | topic | billing | downloads | billing | True |
| 5cae1403-eff9-4098-95f9-18081c73b51f | severity | 3 | 1 | 3 | True |
| 5b761ae4-44b8-417d-96a4-ed339e1b33d6 | intent | complaint | cancellation | complaint | True |
| 09a7560c-3cef-4826-a96e-0843703ac80c | topic | playback | catalog | usability | True |
| e0bb2512-8c18-4bbe-96d8-b02724bc8424 | severity | 1 | 5 | 1 | True |
| f6e5bc23-69c8-4323-a092-dd36e164c206 | intent | complaint | unclear | cancellation | True |
| 4a53c58c-8573-4de2-8a71-83ec6dfe2e51 | topic | billing | playback | billing | True |
| 61f8c46d-2271-41ff-ac27-0927de1470ff | severity | 2 | 5 | 2 | True |
| 6a37f185-46fa-4d1a-8600-8e8e8ec1496f | intent | praise | cancellation | praise | True |
| e0284141-e796-48c9-ba12-0c101d116f3b | topic | billing | support | usability | True |
| 8110c638-5831-4635-a92c-a1d7e90c3606 | severity | 4 | 1 | 3 | True |
| fb29f4da-3dff-48d8-bf43-be24dfe3caad | intent | complaint | request | complaint | True |
| 3e6c1ed9-6ae7-450a-b37a-faee11ce9a7b | topic | other | downloads | catalog | True |
| a4df3e67-1e7f-4b3e-a1ff-1dac7575ebc3 | severity | 1 | 5 | 1 | True |
| 7e35dba1-5211-4bcf-ba29-766112735d91 | intent | unclear | praise | unclear | True |
| c16bbb24-5607-45a1-95fe-04ad623ffbd7 | topic | other | support | other | True |
| f4de03dd-a7a6-419e-94df-8ccd9c4fb7d8 | severity | 3 | 1 | 2 | True |
| 6b383d59-ade1-404f-95fb-31d7e6e9e311 | intent | complaint | unclear | complaint | True |
| 7085e970-4180-4189-bf72-5167205aa471 | topic | catalog | other | catalog | True |
| c697a3c4-988a-4b76-8888-f0e6718ed7a9 | severity | 1 | 5 | 1 | True |
| 7ba10035-5b8f-4a78-b33d-f8f77e151bec | intent | praise | cancellation | praise | True |
| 671ca748-53e3-4be0-8255-1007883b1757 | topic | other | billing | other | True |
| f9e3bb7d-9f25-49c9-83d6-971166a1d562 | severity | 1 | 5 | 1 | True |
| 0104c197-5d63-4a1b-838a-d3780fdcb1dc | intent | praise | unclear | praise | True |
| 25d28152-46bb-4046-8ead-904478fbfa05 | topic | other | usability | other | True |
| 9f46486b-6038-4efe-9984-32f45efe9846 | severity | 2 | 5 | 2 | True |
| 214d2305-2ca1-4327-b98f-f828a0cf100c | intent | unclear | praise | unclear | True |
| 4536e56b-f33a-49cc-93c1-3c97247155d4 | topic | billing | playback | billing | True |
| c6cfcccc-cb27-48f7-81b8-ef450c2d4e4a | severity | 1 | 5 | 1 | True |
| 93781860-53d1-4ecf-8c6d-9d0637e6d268 | intent | complaint | unclear | complaint | True |
| 09cf31cb-e58b-4b67-b586-0f088b9864d6 | topic | catalog | billing | catalog | True |
| a7cae66e-171b-4401-bf45-599fa88ca5ff | severity | 3 | 1 | 3 | True |
| 0b4f75eb-cc28-4fde-9025-f675c26485b7 | intent | complaint | praise | complaint | True |
| 34d950c0-a399-4b20-a3ec-906d1ca015a7 | topic | other | downloads | other | True |
| 646836e0-9d40-44cc-bb3d-ffdbc48e0c5b | severity | 1 | 5 | 1 | True |
| d52a30b7-d1c1-4183-9e11-15fa407e95ab | intent | cancellation | complaint | cancellation | True |
| e8ccac00-e497-4d38-ab43-8c25e69bc6c1 | topic | usability | access | usability | True |
| d30674c6-2cfa-4915-b5e5-109948ac0a53 | severity | 2 | 5 | 1 | True |
| 641ab302-a5f5-4e76-95f0-812e3301a2c9 | intent | complaint | cancellation | unclear | True |
| f13c2268-3610-4098-a12a-38d94f2df694 | topic | playback | billing | playback | True |
| 5f703b2c-3284-409b-b170-3d21828c5175 | severity | 1 | 5 | 1 | True |
| 58604a2b-d0f8-450e-a1e8-90b9855f38b8 | intent | complaint | unclear | complaint | True |
| 32a27ed4-e5ea-425a-9e93-3081d58a591d | topic | usability | other | usability | True |
| 36c33064-9617-4e38-ad76-7175103577e3 | severity | 1 | 5 | 1 | True |
| e67254ee-2041-4aa2-9983-b799f94085e0 | intent | complaint | praise | complaint | True |
| c0557f97-c7c0-4c43-8e5a-421154f62f15 | topic | usability | downloads | usability | True |
| ebba741d-1d46-4287-a86e-b998908b2e1c | severity | 2 | 5 | 2 | True |
| 9d6b35a2-d01a-4761-bb16-ed8f45bb1af7 | intent | cancellation | complaint | cancellation | True |
| d520bd64-4745-46e9-b0a2-713efcdb7e96 | topic | other | catalog | other | True |
| 293d0e43-af90-479b-9505-4d8da2687969 | severity | 1 | 5 | 1 | True |
| ab25c76c-339a-428c-9590-c3ab59af4585 | intent | unclear | praise | unclear | True |
| 714cab07-cbf7-4496-970b-c1e11ca132f2 | topic | other | access | other | True |
| d4eaee30-cce9-455c-90c2-6fe5bf0e5f8f | severity | 3 | 1 | 3 | True |
| 75bccb29-2280-441c-a8c2-42281dbcb7d8 | intent | complaint | unclear | cancellation | True |
| f96006b0-6797-413e-a0a3-151b9bbdf407 | topic | catalog | access | usability | True |
| 2b74b16d-92ba-4313-9399-c2b92bdbdc07 | severity | 2 | 5 | 2 | True |
| 10f553eb-e386-4994-a3bd-ac4850415367 | intent | complaint | praise | cancellation | True |
| 6c134c9c-51cf-4923-b619-3aba564c6012 | topic | other | support | other | True |
| 55592e4c-582e-4da7-9724-50bd3c1a100d | severity | 1 | 5 | 1 | True |
| 1d7764f2-93e6-4ac9-9aa2-0d011d7245d0 | intent | praise | unclear | praise | True |
| 427768de-7737-4a5c-86c4-0f85422d83cc | topic | billing | access | usability | True |
| 75202f94-d19c-4d8d-b168-f8090582b412 | severity | 1 | 5 | 1 | True |
| 60bad486-1712-4729-896c-d9813fe81493 | intent | complaint | cancellation | complaint | True |
| b513f8c5-7836-4efa-8170-913e8a0531c4 | topic | billing | downloads | billing | True |
| 21072c09-b4ac-4445-a20f-b734ae084065 | severity | 2 | 5 | 2 | True |
| 36f74fc9-7825-4662-8e94-c9241892bf8a | intent | cancellation | praise | cancellation | True |
| ab85d4cf-8aae-4f9a-870f-d4a62d1ae87c | topic | playback | catalog | playback | True |
| 0ba29d17-3cae-48ab-b4de-2903f99c854f | severity | 2 | 5 | 2 | True |
| 1d18fbf9-566c-4bff-836a-f42f966aa586 | intent | praise | cancellation | praise | True |
| 8c3fa0f2-becb-4f91-a088-52a7c7105fc3 | topic | billing | playback | billing | True |
| 5a955e0c-7d3c-4e7b-a9ea-d13660a9dbe2 | severity | 3 | 1 | 3 | True |
| 455a16b9-e7fd-45b4-9cfa-553011c2428e | intent | complaint | request | complaint | True |
| fb0e23b6-59a4-44c6-ba36-d027e5c546d0 | topic | usability | playback | usability | True |
| 54a17413-3bf7-4502-a497-fa416df07612 | severity | 2 | 5 | 2 | True |
| d47a188a-bc4b-4577-8e22-13577a9e758b | intent | complaint | cancellation | complaint | True |
| 0f61dbd3-e6c6-42a3-af96-4088215793e0 | topic | other | downloads | other | True |
| 2f67f1bb-292c-4308-a277-58852d4bafb7 | severity | 1 | 5 | 1 | True |
| 5e620d90-a4ea-4314-853c-f6b862db0455 | intent | complaint | unclear | complaint | True |
| 81dc31d0-26cb-4dad-9f89-449d641fd57f | topic | usability | access | downloads | True |
| d5228b72-2db5-4399-959a-8f5d220de378 | severity | 3 | 1 | 2 | True |
| b446c26c-febd-4415-b450-0ead8a37412c | intent | complaint | praise | complaint | True |
| d5a7b30d-6fd8-4346-a378-c57ff2c06095 | topic | usability | catalog | usability | True |
| 7af97887-31df-4613-9ed0-c1e1119647d0 | severity | 2 | 5 | 2 | True |
| a8c7382b-4117-47ca-91a7-751fd663472d | intent | praise | unclear | praise | True |
| d6437e8e-29ea-4220-8735-38d4a69a7c5d | topic | catalog | playback | catalog | True |
| 7efcbbf3-e285-4dec-99a7-8ce549c29e7d | severity | 2 | 5 | 2 | True |
| d752e23a-ff92-45eb-94d1-fa264e53add7 | intent | praise | request | praise | True |
| 1e34b676-160a-4e8c-a0a8-f1975d82d6d4 | topic | other | usability | other | True |
| c17b5290-44fe-4cec-9f3c-955db60c4fc6 | severity | 3 | 1 | 3 | True |
| 1dab4768-84c8-4ad8-9439-ee11958a542e | intent | request | cancellation | request | True |
| cc23cab0-dfe7-45c3-9f93-f2d4bfa45e62 | topic | playback | other | playback | True |
| 02e83ad4-735d-4b28-96fb-219a81053d96 | severity | 1 | 5 | 1 | True |
| 55109027-5ec8-4ca5-b3c3-cc447950e623 | intent | complaint | praise | complaint | True |
| 863a5e06-38f1-4870-ac4c-5c7bae1b480d | topic | other | access | other | True |
| 6a8d1a33-c826-4d3c-b6e4-f96b57a4a919 | severity | 3 | 1 | 3 | True |
| 0530ae8f-e049-4266-8335-2bf538281c84 | intent | complaint | request | complaint | True |
| 4e9cbe01-40f1-46db-b312-9931994603e7 | topic | other | downloads | playback | True |
| d59f09b3-10f9-4205-9008-38e3bd1f97f2 | severity | 1 | 5 | 1 | True |
| d4cbda1e-a62f-4ec9-a445-9a6fd8bcfb65 | intent | complaint | cancellation | complaint | True |
| e9fef42e-4830-4f6f-ac8f-c5fb8d5d3ebc | topic | other | support | other | True |
| 0913fb15-8172-4c31-88d8-465f3df67c14 | severity | 2 | 5 | 2 | True |
| 29464f12-6ce9-441c-8cc5-e807f18c91d9 | intent | complaint | unclear | complaint | True |
| 1016417a-374a-4425-a8cd-1b12026cff5f | topic | usability | catalog | other | True |
| 3b006622-a6e2-4f54-85f9-f3bf6d3fbe09 | severity | 2 | 5 | 2 | True |
| 2140b524-3593-4e65-bb7e-004285ff1568 | intent | complaint | praise | complaint | True |
| 63c6c91c-0992-4812-9091-635e67c4dcf2 | topic | other | billing | other | True |
| c3302d69-a685-4743-ad5b-81eba4556787 | severity | 1 | 5 | 1 | True |
| 857d6259-b4b8-4dd9-bc32-0a24fda4957d | intent | complaint | request | complaint | True |
| 801b7c40-8141-4823-8eff-e05abc256974 | topic | other | usability | other | True |
| 4a7fb559-9945-4b0f-a8f7-daffaa7f3ebc | severity | 1 | 5 | 1 | True |
| 1534d304-d67e-4c4a-8fe8-25426626f1d3 | intent | cancellation | unclear | cancellation | True |
| 29382538-b1bc-4abf-87d6-08d0f42f48e2 | topic | other | catalog | other | True |
| a8caf69a-3d61-468d-9a42-142c002e73cb | severity | 3 | 1 | 3 | True |
| 0ce88bf8-4cf3-4797-b839-6bca00314224 | intent | complaint | unclear | complaint | True |
| 97356634-c52c-4056-9612-4a36688a522a | topic | playback | downloads | playback | True |
| 54b47181-4197-4650-ab4a-1801c0fbefd9 | severity | 2 | 5 | 1 | True |
| 881455d1-21f6-4fb6-97a4-3e8e3ac1ca8e | intent | cancellation | request | cancellation | True |
| cb225e9c-ddc2-4b23-8d0e-d1835d05bf51 | topic | catalog | access | catalog | True |
| e052554e-fa74-4319-ba45-7af0454e75d4 | severity | 3 | 1 | 2 | True |
| 173b5916-07df-4751-8f9f-f2035453f329 | intent | praise | unclear | praise | True |
| cb02ec45-662b-4dcb-aa46-c91ebb3b02a0 | topic | billing | catalog | billing | True |
| 543bd546-884f-4037-a3b7-c6af4c3f4945 | severity | 3 | 1 | 2 | True |
| c5c9ffd5-72e5-4da8-bee4-4a5ff5dcd3f0 | intent | praise | request | praise | True |
| f9a1c6b7-c63c-4eaf-b885-0f8e27d36ee7 | topic | support | usability | support | True |
| d5c17aba-455d-4cef-957a-6ccea159448a | severity | 1 | 5 | 1 | True |
| 67835dbd-10ac-4325-b93e-453d1bd5ec36 | intent | complaint | unclear | complaint | True |
| 05bfd429-d1c2-4fc8-ae7b-d89aa855554b | topic | other | billing | other | True |
| ec11ab85-474c-4629-a3b3-7f4eabe955dc | severity | 1 | 5 | 1 | True |
| 51ed47e3-3426-4114-b312-ef06cdd0b0b8 | intent | praise | cancellation | praise | True |
| baf2e6c8-cd3f-4711-a9aa-6efee256e7da | topic | other | usability | other | True |
| 3677bc48-45de-4c35-85f1-ee3c02409a22 | severity | 2 | 5 | 2 | True |
| 3fc76671-a647-427c-b8e8-71b9120fa1eb | intent | complaint | request | complaint | True |
| df209b8b-17f9-4f2b-b23b-a44bb89d2dae | topic | other | catalog | other | True |
| 1345398e-28e9-4af6-85f6-6dd76d5138d4 | severity | 2 | 5 | 2 | True |
| c6ab0842-06ec-4f30-970f-51fc0ec7df35 | intent | cancellation | unclear | cancellation | True |
| 923a7ffa-0791-4285-813e-47215ecd30bb | topic | billing | support | billing | True |
| b4f9c0d5-a1f1-4343-99d0-d4cbf4809f06 | severity | 1 | 5 | 1 | True |
| f390bcdd-69ef-48bb-8d37-8acf8680506d | intent | praise | complaint | praise | True |
| d3d81ef6-b900-4930-888d-df3fdc7ef1df | topic | playback | support | playback | True |
| 16cd2250-bfcb-4a3e-a4ee-99551a71fa58 | severity | 2 | 5 | 2 | True |
| 40102561-a005-41b8-96cb-a4518627e2a6 | intent | complaint | praise | complaint | True |
| 312943f4-aae1-463c-b747-9bcfeec1ae7d | topic | usability | access | other | True |
| 58627b79-62a1-4eec-83b1-e1344e498ebb | severity | 1 | 5 | 1 | True |
| b479590a-b85f-460f-b296-047cb18f18c9 | intent | praise | unclear | praise | True |
| f9cfc27c-e390-488c-9c68-42b4c8220033 | topic | other | playback | other | True |
| 429dec08-d7f5-4f4a-9998-1c860b04201f | severity | 1 | 5 | 1 | True |
| dec1e683-9d17-4dca-a4d8-7567e351467a | intent | unclear | praise | unclear | True |
| f7c36ebd-1808-4076-a2de-c2a66fcd41fb | topic | other | billing | other | True |
| d05e5b8d-05cb-45d5-bbfb-41022b4d8797 | severity | 3 | 1 | 3 | True |
| c2729354-1efc-46c7-8d45-e44b5b2b59a4 | intent | complaint | unclear | complaint | True |
| f0db7e72-eac3-488f-839e-0df526ee0b72 | topic | other | usability | other | True |
| ee6bf52e-dba1-4bbc-9a1e-d63ef62af77a | severity | 1 | 5 | 1 | True |
| 2c5532ca-b59d-46a8-80ac-b94306511973 | intent | complaint | praise | complaint | True |
| 0e2be044-3e6f-4704-a5a8-b3f36a79aa3e | topic | other | catalog | other | True |
| 7a8f937a-7b1e-455d-9f4a-0b3fc6e45545 | severity | 1 | 5 | 1 | True |
| 43b0af6f-c675-4224-8399-0b805b772472 | intent | complaint | request | cancellation | True |
| e2fce7bc-6d04-43bb-a501-5499b98608bc | topic | other | access | other | True |
| dee4a1b2-fe50-4ba0-bd1a-a61f90c0d8fb | severity | 1 | 5 | 1 | True |
| af6192cd-9d3a-46b0-b74f-4c38595b7e30 | intent | complaint | cancellation | complaint | True |
| 9d150136-f36e-4713-acd3-8f499df4bfde | topic | other | downloads | other | True |
| 284ffc4d-c892-4e6e-866a-034c9ef42ce8 | severity | 1 | 5 | 1 | True |
| 846176c9-e6fe-40d3-a7f8-f04c40c8460e | intent | unclear | request | unclear | True |
| 856aabd6-1a27-4453-a270-e053ebe365a3 | topic | playback | usability | playback | True |
| ed71d7be-8708-408f-bc67-5ffa858144e6 | severity | 1 | 5 | 1 | True |
| 4fc41404-6b80-45d7-a85d-38568574c5d3 | intent | complaint | praise | complaint | True |
| d771f57a-b57d-4521-a0d3-f40ee20c0dbd | topic | catalog | other | other | False |
| 1eee0627-1254-4f7f-9a3b-535d0a60d528 | severity | 3 | 1 | 3 | True |
| d1c1768a-9411-4121-b545-12f27baaae15 | intent | complaint | request | complaint | True |
| f0b6b7cf-f38b-41dc-8eaf-1422a97e5aee | topic | downloads | usability | downloads | True |
| b6335e33-09b1-4c8b-a5c4-fd2710464ee4 | severity | 2 | 5 | 3 | True |
| c0151958-b382-4795-917e-97382bbaf94f | intent | cancellation | unclear | complaint | True |
| 6637c72d-1e76-4f5c-ae90-4ac33e1da507 | topic | usability | downloads | usability | True |
| df94ea11-84c8-417e-a5f8-3e81cfa97394 | severity | 1 | 5 | 1 | True |
| d8e444a2-7f7c-4fea-87e9-c1b9c5a32e7a | intent | praise | complaint | praise | True |
| 8cd601bc-6f01-4dda-82fa-235937f465a5 | topic | other | catalog | other | True |
| e81f307b-1309-4c79-b167-a91e182a165e | severity | 1 | 5 | 1 | True |
| c74754b1-ae4f-4c26-bdf5-454dce647dab | intent | complaint | praise | complaint | True |
| 8a0da6d4-7a23-42ef-b193-cb4587da69b0 | topic | billing | support | billing | True |
| 33c3bd6d-9af5-4587-9d70-e3cf25e78c99 | severity | 2 | 5 | 2 | True |
| 0d54d40e-1ba6-4158-85f7-130dd5be8dd8 | intent | praise | unclear | praise | True |
| 9c75631c-6d57-4925-8f49-bdea0bef56eb | topic | usability | billing | billing | False |
| e550c53b-7a45-42e4-97cb-584a5a02854b | severity | 2 | 5 | 2 | True |
| bc9239c7-a04a-4f94-bf93-bb01146a7167 | intent | unclear | praise | unclear | True |
| e3925c4e-98f6-4125-b01d-de45107fdb61 | topic | access | other | access | True |
| b4f159b0-1df9-44a1-9673-c10dccdf8031 | severity | 2 | 5 | 2 | True |
| 3b6d1b18-007d-450a-ba3b-b87a26b3fdd6 | intent | praise | complaint | praise | True |
| 50b10c28-4fee-4919-a404-fa754b1968ef | topic | downloads | support | downloads | True |
| 3a412e3c-78e4-4704-a6ad-e9620a78f741 | severity | 3 | 1 | 2 | True |
| 41933e8d-303e-4be2-9765-43b72e13e96d | intent | complaint | praise | complaint | True |
| fba94e9b-973e-4696-b352-1d5b2fd6196d | topic | catalog | playback | catalog | True |
| b81f5883-9f85-47d6-bb58-233db2ac6a50 | severity | 1 | 5 | 1 | True |
| b3ee82c1-2149-45ef-9da8-ead03c7a2cc7 | intent | complaint | request | complaint | True |
| c333e4d6-6c0f-4de8-ba4c-a48abf2c83a2 | topic | usability | downloads | usability | True |
| 6c71dcb7-c818-429c-bdca-d2bfff197f11 | severity | 1 | 5 | 2 | True |
| b319e3fe-6353-4c47-8dbe-53e44b6c7515 | intent | complaint | cancellation | complaint | True |
| feeaea74-bf38-4863-87f6-307d90e0b2e8 | topic | other | catalog | other | True |
| 1f391495-7124-44a1-b070-92a7575fa888 | severity | 1 | 5 | 1 | True |
| ab8c6854-09b9-45be-ab01-fed2be9b57d2 | intent | cancellation | praise | cancellation | True |
| 9eaa5b9a-ce06-459f-912e-3181a1d90b08 | topic | other | access | other | True |
| f09e7190-ba70-4a82-95f4-b7e4f61dbcd4 | severity | 1 | 5 | 1 | True |
| f4309366-d0d7-483a-ab44-f44135fe914d | intent | complaint | praise | complaint | True |
| e50cf734-9c5c-41f9-a100-dcd9a89f08e9 | topic | usability | billing | usability | True |
| ae609bbc-3e2d-4bd5-9c2f-f5b922518eee | severity | 2 | 5 | 2 | True |
| 88d33cff-280d-4332-bcad-b38da72e9b72 | intent | complaint | request | complaint | True |
| e9a23292-92cb-438a-96d3-1ce079e9e158 | topic | usability | access | usability | True |
| 3328fe87-2e3d-4140-b15f-a8f1d0cf8adc | severity | 3 | 1 | 2 | True |
| 679b885e-7029-486b-a2ad-0ceb04a028fb | intent | complaint | cancellation | complaint | True |
| f17a545a-98b6-41b6-b05b-3813d573d33e | topic | usability | catalog | usability | True |
| 2c660369-5a0c-4d91-8ae8-c36d5337d40f | severity | 1 | 5 | 1 | True |
| 304a45ea-8d3f-4e39-8359-409da522a8ef | intent | praise | complaint | praise | True |
| af602065-3cc5-427a-a77f-0e5efccf5961 | topic | other | billing | other | True |
| c28fafb7-7cd1-447f-97f0-54b397348661 | severity | 3 | 1 | 2 | True |
| 32d59268-181a-4bbb-bf6d-58f796590f9f | intent | praise | cancellation | praise | True |
| d2b0545c-0cfa-4307-bcd6-0f64f3437f62 | topic | other | usability | other | True |
| d8dbb3a7-d883-4c7f-8a7b-9109490feb25 | severity | 4 | 1 | 4 | True |
| a83646a6-9925-4076-b075-cf803c367c94 | intent | complaint | request | cancellation | True |
| 7a7678fb-f564-4197-b8eb-08153a20561c | topic | catalog | usability | catalog | True |
| 16e34daa-88d3-4d79-bd2c-d23e43255f83 | severity | 1 | 5 | 1 | True |
| d8a2f722-3968-413b-b325-1ccc4be0ef94 | intent | unclear | praise | unclear | True |
| 6465618d-945e-4170-a896-1f341f6fe54e | topic | other | access | other | True |
| 6895dcc0-c3f1-4c1e-9523-e669c2eef58f | severity | 1 | 5 | 1 | True |
| 3b259d38-b9df-4b1d-9a20-c6f884d4fcfa | intent | praise | complaint | praise | True |
| b82ee8e8-dbcd-4bf0-8b6b-9635cdfd6cb6 | topic | other | downloads | other | True |
| 89a49bc5-939a-4e99-8b45-71ae57fc392f | severity | 2 | 5 | 2 | True |
| ee801b76-420b-4817-a845-4ca1f5d2e633 | intent | complaint | praise | complaint | True |
| 02d36000-043d-4aae-b265-c48c9c9401a6 | topic | playback | usability | playback | True |
| eb4bd3c1-b398-4ad7-b456-5c1f4d4db9e7 | severity | 2 | 5 | 1 | True |
| 366cde4e-da1d-4eab-ab9e-01a992c5dac8 | intent | complaint | request | complaint | True |
| e18e7b06-86ab-488e-b9d8-c67de88bde23 | topic | other | playback | catalog | True |
| 0840e6da-7040-4fa1-941f-1886fa596b4a | severity | 1 | 5 | 1 | True |
| 14a576af-057c-4470-8a5d-2b111653d395 | intent | praise | request | praise | True |
| 61713112-f8ee-4743-9a73-0f04596efa4d | topic | other | billing | catalog | True |
| 5fdf3340-742f-45b8-9241-c3225f8ca694 | severity | 1 | 5 | 1 | True |
| 773ba387-6f3e-438e-afb1-284ccfced778 | intent | praise | complaint | praise | True |
| 8367f1e6-4b38-4a8b-8e35-0b1b52c1d818 | topic | other | usability | other | True |
| 6d3b7835-ec8f-4ef2-bfd5-1d177efba7d3 | severity | 1 | 5 | 1 | True |
| 754d5424-bf9b-4ae2-8db2-db7aaf81283d | intent | request | unclear | request | True |
| 384fcbd4-e70d-4309-8a6e-c8c9080d01dc | topic | other | catalog | other | True |
| cfaf9c6c-87c6-4007-ab34-853d2b43596f | severity | 2 | 5 | 2 | True |
| 7ab1063b-e194-4a0f-831f-5ffbf285e358 | intent | praise | unclear | praise | True |
| a0491f0f-8396-4ec8-abf7-d0dc80cce380 | topic | playback | downloads | playback | True |
| ec30f513-78ea-4d5d-bc8b-786855ccc35c | severity | 2 | 5 | 2 | True |
| 7bbb65b1-4ccf-407f-8145-2fbf17930046 | intent | complaint | cancellation | complaint | True |
| fd10e27a-35b1-4359-9dd4-4b9ab66db9f9 | topic | other | downloads | usability | True |
| e256da7e-cdf8-442d-8f6a-6c35ebe1ce5f | severity | 2 | 5 | 2 | True |
| 04821981-3f4c-46df-b615-8f56fbb19cb4 | intent | complaint | unclear | complaint | True |
| 59a6efe6-a03b-41fd-a2f8-e7aa25246ba3 | topic | usability | access | usability | True |
| 33a91039-ba7e-42c2-b334-ceaa450381ca | severity | 1 | 5 | 1 | True |
| 1366116a-d566-41ce-b8a5-fa5ed7169833 | intent | complaint | praise | complaint | True |
| fc0c79c5-04cc-4c46-920f-a8282608006a | topic | playback | billing | playback | True |
| adce6edb-c007-4989-9ecb-30cd10b214bc | severity | 1 | 5 | 1 | True |
| 9d968ea9-8cbf-4907-a125-555d69b7bf52 | intent | complaint | request | complaint | True |
| 6caeda3d-8c2a-4234-bda1-d2b01a048717 | topic | playback | access | playback | True |
| 5f6f3ff6-2d20-49f2-9a5f-52fcfa4301c5 | severity | 2 | 5 | 2 | True |
| f9241b09-568d-46fe-8441-bbf854f36d90 | intent | complaint | cancellation | complaint | True |
| 40ab30bf-451d-49e5-a272-ddd8de3683c0 | topic | billing | other | billing | True |
| a8cb2565-6c39-4b12-bef2-9f09a9538dc4 | severity | 3 | 1 | 3 | True |
| e6b23072-81ce-47b3-98a0-c3b35fa1c9d0 | intent | complaint | unclear | complaint | True |
| 4136adff-b968-4848-94dd-c1cd1a374e95 | topic | usability | support | usability | True |
| a20fc39e-9b17-4d10-92e5-8be21f8e1fbb | severity | 2 | 5 | 2 | True |
| d64db5b1-36e7-4a7b-8429-d0ff0edcfd85 | intent | complaint | praise | complaint | True |
| 33fbb1dd-27e1-4bbf-be63-fe157f80121b | topic | other | access | other | True |
| f6a0d928-fe7c-44ea-a69f-69d6dc2f5fcb | severity | 2 | 5 | 2 | True |
| ebec8417-d50d-4c4b-8511-7151029ddcae | intent | complaint | request | complaint | True |
| b22c108b-f1d7-43a4-ad4b-e082a8e0576d | topic | other | downloads | usability | True |
| 54bd637c-d32c-48a5-aac5-ebef48f0eb67 | severity | 1 | 5 | 1 | True |
| e9438a04-0654-4b40-9549-15c15b73d324 | intent | complaint | cancellation | complaint | True |
| a40615b6-607a-4eb9-b74c-60bd43200eb0 | topic | usability | access | usability | True |
| 22b33b7e-c7c8-4a23-8898-4d1ebc5be581 | severity | 1 | 5 | 1 | True |
| eb256564-d9e6-447e-bf62-63913dec2168 | intent | complaint | unclear | complaint | True |
| 966ecddd-3b71-40fc-b192-5fe5e4cae20f | topic | catalog | other | other | False |
| 56598403-441e-4e75-926a-3471562555d2 | severity | 3 | 1 | 3 | True |
| c56e9ede-470f-4fe7-9eca-c20f599bfb64 | intent | complaint | praise | complaint | True |
| 351cb789-89c4-4ef2-8c34-56ee4d4de335 | topic | other | billing | catalog | True |
| 0a28d564-8c7b-4cd3-b242-e4fd7ef3e99e | severity | 2 | 5 | 1 | True |
| cce7863f-cec8-4f85-ac7c-3accc04b7347 | intent | complaint | request | complaint | True |
| 45444c35-12d7-4ecf-8e65-3a2f2b6f8c7c | topic | other | usability | other | True |
| 2a5a916d-8fde-40a7-99bd-8e74100d1c5c | severity | 3 | 1 | 3 | True |
| fcdb2c55-da48-4414-b458-7c60c4e8a4ec | intent | praise | request | praise | True |
| f1076c32-bc70-49d2-9f7f-0c39b2ede461 | topic | catalog | usability | catalog | True |
| 47520cc8-e597-4169-a0f4-dd17f88ebd77 | severity | 2 | 5 | 2 | True |
| 05b75fd8-3e1b-4977-ab05-45ec86b82324 | intent | unclear | request | complaint | True |
| bc46a215-b042-4ffc-beeb-98e5368b06a9 | topic | playback | downloads | playback | True |
| ae6aef12-8c4b-4c0c-af48-4ddaad2ee487 | severity | 1 | 5 | 1 | True |
| aa113159-0224-4a55-a99e-301dfe5fe81e | intent | praise | cancellation | praise | True |
| eb5e2dff-6049-4931-b3c0-57befa91ac4c | topic | other | downloads | other | True |
| cb751b1d-18bc-41bd-89ec-a82e0564d3d1 | severity | 4 | 1 | 4 | True |
| 44bac516-c153-4d97-8347-4a4475531818 | intent | praise | unclear | praise | True |
| 658dd7dc-ad2d-4a58-b8c5-ea824cf07b90 | topic | other | support | other | True |
| 77f22ac2-fd6f-4d0c-b1c6-06c15b6ac7b7 | severity | 3 | 1 | 3 | True |
| 9e9a4719-810a-44da-931e-dc68d2e72733 | intent | unclear | praise | unclear | True |
| 91c82040-d543-4b6d-ab13-64d5c81c2f03 | topic | other | playback | other | True |
| a20f59e3-bde4-4d87-af0a-5c29e8fe66cc | severity | 3 | 1 | 2 | True |
| b1ddcaac-026b-480e-98c1-9bf3ab6dabc0 | intent | cancellation | praise | complaint | True |
| 980adfcd-bb9f-4013-a717-821cc4c4eef1 | topic | other | billing | other | True |
| d0c2a8a9-ed23-4f7a-832f-294df0e79840 | severity | 1 | 5 | 1 | True |
| 3852751f-f95d-422d-a6de-16748715e4ee | intent | complaint | praise | complaint | True |
| 6cff9dd9-c3c6-4f34-8019-9dd610e2a2f7 | topic | billing | other | usability | True |
| 1dcd61d1-5dd3-4623-833f-42b0ae07fc40 | severity | 3 | 1 | 3 | True |
| 336fc181-26cb-4f9c-bc67-b13a839f6457 | intent | praise | unclear | praise | True |
| edb23206-dcd2-4a9f-9012-3ca438c5bd0f | topic | catalog | usability | catalog | True |
| 6cf2a22b-f7ed-423d-a3d2-cb8a1ac202bd | severity | 1 | 5 | 1 | True |
| 62ec6ea2-ff9d-4f1e-adbb-89676ebf1c5f | intent | request | complaint | request | True |
| caf4593d-ea3b-4a27-bc74-58ca83ea2625 | topic | other | access | other | True |
| d235f3a4-53d4-4ebf-a76f-ab4ac580c622 | severity | 1 | 5 | 1 | True |
| dca03f31-d779-419c-a8c3-049ae869bd9c | intent | cancellation | praise | complaint | True |
| ee5fd2de-46d1-4db5-b200-38d775f031e7 | topic | usability | billing | usability | True |
| aa53bb00-79d8-454c-88e5-4b2d2cf2f87b | severity | 1 | 5 | 1 | True |
| 2d8aabbe-77f8-435d-99f8-2dba71ae6ff3 | intent | complaint | praise | praise | False |
| 83267856-b27f-48d0-a545-9e9598d3917a | topic | billing | catalog | billing | True |
| b6060586-933f-4312-8340-a519bf96280b | severity | 2 | 5 | 2 | True |
| ad0e150a-319f-4d1b-8951-3cd8c99f9db7 | intent | praise | unclear | praise | True |
| db97fed8-09d7-433d-b36e-c59388d54d12 | topic | other | playback | other | True |
| 038ec263-02f2-4e88-a735-372e8d579b4a | severity | 3 | 1 | 2 | True |
| 9ead7206-3151-43b0-aa9d-eafedb5c1077 | intent | complaint | cancellation | complaint | True |
| 58445712-8654-44a2-8aae-8996f1e54c1d | topic | other | billing | other | True |
| 5c7be90d-0975-472e-9926-84264cdf4fce | severity | 1 | 5 | 1 | True |
| 8d45e257-9205-4899-898d-53d02df40d0e | intent | complaint | unclear | complaint | True |
| 92a4d3b7-3007-49a8-9215-ef728e4d3ea8 | topic | other | usability | other | True |
| 48159f8e-546c-417f-9f3f-84329189ddd6 | severity | 1 | 5 | 1 | True |
| cdf3ab11-c5f4-48c1-9885-e76842192776 | intent | praise | cancellation | praise | True |
| 76e7398b-781c-4a15-b1fd-39b8f4fb05b5 | topic | other | catalog | other | True |
| f5effa07-9ca1-4c84-8983-c219e5eea97c | severity | 1 | 5 | 1 | True |
| 7c7f644f-6ca6-4157-84ea-ee5c36c964dd | intent | complaint | request | complaint | True |
| b69f4a4a-a27b-44eb-b8a8-d94887fb1208 | topic | billing | support | billing | True |
| ec4c2062-9160-4226-b487-15978f8d5ab0 | severity | 3 | 1 | 3 | True |
| 2cc049b7-fd32-45de-93ea-3888e319ccab | intent | praise | request | unclear | True |
| 545a9248-9a01-41de-b1cd-d7c5d232d1f8 | topic | catalog | access | catalog | True |
| fc25cff5-aead-4152-8132-25af714bbbe5 | severity | 2 | 5 | 2 | True |
| 35ab105a-5200-487e-9167-a969c45a701a | intent | request | cancellation | request | True |
| d969ce43-515a-478d-b561-04a4beb38771 | topic | other | support | other | True |
| 5152eb0a-7402-4d45-9c34-ca16f9c81448 | severity | 1 | 5 | 1 | True |
| bbf59582-dcfa-452f-8fad-136571f30bf2 | intent | complaint | praise | complaint | True |
| a11082ef-8211-4d51-adc3-47968a4e3991 | topic | other | playback | other | True |
| 6dd5fbe8-9ea3-4dd2-9759-eb8f0877fe48 | severity | 4 | 1 | 4 | True |
| 359b60e2-b009-4517-b198-ba0e73e85800 | intent | complaint | request | complaint | True |
| 985c56d0-5c60-403b-ae2b-1adbb98e5599 | topic | usability | other | usability | True |
| 90eb5bc2-2191-4117-8ab5-ee0f3e3204cc | severity | 2 | 5 | 2 | True |
| 40c7635d-7f4d-41a2-872a-e6b08cedc6d2 | intent | praise | request | praise | True |
| 35e4115a-b5d1-4fcf-b531-66eaa2cd8417 | topic | other | usability | other | True |
| 4796ab83-387a-4f80-8eef-9a516c95931c | severity | 1 | 5 | 1 | True |
| ba8d0562-d8f3-49d4-9202-0e3300753aac | intent | praise | complaint | praise | True |
| 361cedea-ceb5-4d1e-8755-af97c14bf611 | topic | billing | playback | billing | True |
| a4687d04-aaa7-424e-b666-3310c532fce2 | severity | 3 | 1 | 2 | True |
| 60758790-929a-4b6d-a42d-296818fa5625 | intent | complaint | praise | complaint | True |
| 244610bd-d6ff-4029-baeb-ff9deeb4a47e | topic | playback | downloads | downloads | False |
| b668e7b6-2fbd-4703-b25b-4e69db3136af | severity | 2 | 5 | 3 | True |
| fd9b28e4-13ee-423e-97c6-0a3373ad66e1 | intent | complaint | request | complaint | True |
| d4057beb-039e-455d-b1cf-8686ff2bb8ec | topic | other | downloads | other | True |
| 11b7b07d-c5eb-4652-a562-7f54f91fb7d0 | severity | 3 | 1 | 3 | True |
| 34a70e48-724e-4487-bdbb-de492487a8fc | intent | complaint | cancellation | complaint | True |
| de9a15e9-4773-4a0b-8f0a-dd52abf65f13 | topic | other | support | other | True |
| 7672c015-e990-4ea2-8a69-695ba33e7502 | severity | 3 | 1 | 3 | True |
| f1d96685-6eb7-4518-ae02-f51700627bf4 | intent | complaint | unclear | complaint | True |
| 1810e38c-d46e-4480-ab9e-e3a0214b0118 | topic | billing | access | billing | True |
| aca9a32d-76c8-478f-9a8d-cf6fb2cd54f6 | severity | 2 | 5 | 2 | True |
| f83bcf30-5110-42ec-93cb-c22eb316d08a | intent | complaint | praise | complaint | True |
| 00e78f0d-374a-4e20-b1f5-f72ef9fa5980 | topic | other | billing | other | True |
| 39c02d8c-610f-47f5-971b-36bcbfffc14f | severity | 1 | 5 | 1 | True |
| e0f20bea-3af7-4f0a-b2f4-2ac4a597c0c3 | intent | praise | unclear | praise | True |
| 06e036c6-1d92-4939-bdf5-ba4a6936d51e | topic | other | usability | other | True |
| fa3d055e-e762-4ea0-9764-644aa764f840 | severity | 3 | 1 | 3 | True |
| 8f05b7f1-b227-4cbe-b0bc-d0cc73a4a5b7 | intent | complaint | cancellation | complaint | True |
| 8ad41921-3022-49f4-af65-0ebdc8bef8b8 | topic | catalog | usability | catalog | True |
| 57e26cd3-6628-465a-ab0a-f2cf55e7ff8e | severity | 3 | 1 | 3 | True |
| f9a77f16-284f-4a0d-91a3-960b3bdd447f | intent | praise | complaint | praise | True |
| c5e56277-2d0e-414a-92db-8888b6614a8d | topic | other | access | other | True |
| 44a137d8-e01c-4f4b-917b-368916907646 | severity | 3 | 1 | 2 | True |
| 1ec5ae10-e1fe-4294-8f45-16d08714d107 | intent | praise | cancellation | praise | True |
| b337ca92-e56c-4da3-ba5f-37996957dbb9 | topic | other | downloads | other | True |
| 52a3b80f-ecbb-4f7e-9823-086791406f9e | severity | 2 | 5 | 2 | True |
| 0557be93-db50-4d04-b101-a6d4715133c8 | intent | cancellation | complaint | cancellation | True |
| d705ba58-5d02-4d0e-9bdb-dbcfdb69f509 | topic | usability | access | usability | True |
| 48f33252-2422-4894-973a-7c63e588fcda | severity | 2 | 5 | 2 | True |
| 56dd7639-8685-4450-a248-89942d87dafb | intent | complaint | cancellation | complaint | True |
| cd632c49-5b28-4f94-be3e-d0a5d748ded1 | topic | other | playback | other | True |
| fefd68e0-6860-4298-a594-da6530ba45e0 | severity | 1 | 5 | 1 | True |
| bf5d2ca6-6285-4e33-8f61-437a22521012 | intent | complaint | unclear | complaint | True |
| 01511fcc-d78a-4707-9fee-dcde7652d6af | topic | other | billing | other | True |
| fc3b14e3-0e2e-4146-9871-0fc88b14dad5 | severity | 1 | 5 | 1 | True |
| fd02ba77-f733-4629-b938-f739d9e57540 | intent | complaint | praise | complaint | True |
| b629e81f-0f01-4b7a-ab6c-ae2ae9bf65de | topic | other | usability | other | True |
| 3ea6bfb8-4b4a-44c7-b43f-0d920bd01ef4 | severity | 1 | 5 | 1 | True |
| 11278fef-e0e7-4578-9427-903a616adb14 | intent | praise | unclear | praise | True |
| d4ef427a-a0fa-403a-bf92-84e947bbb181 | topic | access | billing | access | True |
| 89ff2d37-63ab-4e04-9c6d-36f57e1fa3c7 | severity | 1 | 5 | 1 | True |
| 3956b8ee-fa65-4195-bab5-2e5055cad63a | intent | unclear | praise | unclear | True |
| 599eaaa5-3bbc-4157-afc6-23e3bac54677 | topic | usability | playback | usability | True |
| e8209cdc-7b28-4b76-9423-c4d192fcc66f | severity | 1 | 5 | 1 | True |
| 47f112f9-eff2-4f06-8956-95b854d944c9 | intent | complaint | unclear | complaint | True |
| f274422c-ced7-4c5b-99c2-a4df9f15a206 | topic | playback | support | playback | True |
| e751c62f-31cb-4375-be52-775959e4b268 | severity | 2 | 5 | 2 | True |
| e383e753-9b2e-482b-bc6c-f15ee8598ee2 | intent | praise | cancellation | praise | True |
| e4b4f7b1-305a-4174-980a-44b71286f3f7 | topic | billing | catalog | billing | True |
| d272d536-6a8c-4da7-86ac-a5458f38e921 | severity | 2 | 5 | 3 | True |
| c226c18c-7fb0-49dc-ae30-1b19d8417fb3 | intent | complaint | request | complaint | True |
| acf6468a-8df3-4b19-8284-c3a6a169f574 | topic | billing | access | billing | True |
| 8f51bcca-d7b3-486b-a45b-f18469ec586a | severity | 2 | 5 | 2 | True |
| 223f1b3c-4770-4687-96b1-77e4586933c6 | intent | complaint | cancellation | complaint | True |
| 48c1a26b-96cf-42fd-9f8c-1ec367a74193 | topic | other | billing | other | True |
| 9e260c4d-06b3-4c8a-af1b-1196c0932db2 | severity | 3 | 1 | 3 | True |
| 0f155caa-1d4b-4c07-ac39-ced60b2e57b4 | intent | praise | complaint | praise | True |
| 86196690-01a7-4ce3-ac86-7aff78f72471 | topic | other | usability | other | True |
| 1aa2b423-8196-4180-b110-b2d90a9a3eb2 | severity | 1 | 5 | 1 | True |
| 08a95031-ae90-400e-9603-acc03c8d86e1 | intent | complaint | praise | complaint | True |
| 7d0c3831-a4e0-4937-82cb-f81044e90ba1 | topic | other | catalog | other | True |
| ddae251b-1513-4e28-9f6c-463fbc493285 | severity | 1 | 5 | 1 | True |
| 43e84259-14e6-4813-b61f-0dee8bb68fcd | intent | praise | unclear | praise | True |
| e379bb56-28ef-45af-8ba9-ec5d29ea3d06 | topic | catalog | billing | usability | True |
| c75074be-f9f6-4a41-b053-99e5ffbb8661 | severity | 3 | 1 | 3 | True |
| a42d6ec7-1734-4beb-88ed-8ac838d6d644 | intent | praise | request | praise | True |
| e01bc03a-d79a-4bd9-be61-bd7bc6902603 | topic | other | downloads | other | True |
| 0ba0db45-4c60-40a4-9634-948b876d7ca8 | severity | 1 | 5 | 1 | True |
| 52a53959-c4c6-4eae-9b0b-1ca8b5680221 | intent | cancellation | praise | cancellation | True |
| 628b6a5d-5f37-41bd-83f1-97969e942371 | topic | access | other | access | True |
| b22e1ffa-30bf-4430-8cc7-60014dcbe9c5 | severity | 2 | 5 | 2 | True |
| 8fe4ee4b-187c-49d7-89bb-182cf30fff63 | intent | complaint | praise | complaint | True |
| 5bfc1fbb-e1ff-45f6-b473-1f99275d640a | topic | other | playback | other | True |
| 8f55611e-bd54-43a1-b3d5-304352528113 | severity | 1 | 5 | 1 | True |
| d9e3ed56-1cdd-4e7c-a2c9-62e01c67fdc5 | intent | complaint | request | complaint | True |
| b915c902-90c1-456a-94f3-7324e58598f2 | topic | other | billing | other | True |
| 74227c7c-120e-43a1-9161-719695720d44 | severity | 3 | 1 | 2 | True |
| 2bbacabf-a3ac-42da-9143-711951ce13bf | intent | complaint | cancellation | complaint | True |
| 6904fe4f-4715-44ec-9460-b09746921559 | topic | catalog | support | playback | True |
| d65ee4d6-5f98-46b1-971b-57eeb73072c3 | severity | 1 | 5 | 1 | True |
| 2d11cea5-2eb0-4359-87de-6df712e52945 | intent | complaint | unclear | complaint | True |
| e478eb33-20ab-4a4f-a53c-5606b2df8694 | topic | billing | playback | usability | True |
| c26331fd-b841-4fe8-91e7-cff9d9d40733 | severity | 1 | 5 | 1 | True |
| 8e7a41a0-78fc-450e-a8a0-621eaba550bd | intent | complaint | praise | unclear | True |
| 65a8654e-65e1-4925-b803-ec442cb52624 | topic | billing | support | billing | True |
| f69e0d8e-540a-45fc-85ac-11723dc41258 | severity | 1 | 5 | 1 | True |
| 5ffb392d-4406-47d5-ba09-7f0ca2da7988 | intent | complaint | request | unclear | True |
| c157b48f-3f97-41ff-bdd8-58b58a94d430 | topic | billing | usability | billing | True |
| 3808b657-597b-4164-bc64-13b9169f9566 | severity | 1 | 5 | 1 | True |
| a534d85c-1e8e-4e77-b19e-99c9ba69c1a5 | intent | complaint | cancellation | complaint | True |
| cf44c2af-eb80-4a22-b348-cf86248fb6db | topic | other | support | other | True |
| bb92cf60-11fd-4786-9f32-76491cc73c87 | severity | 1 | 5 | 1 | True |
| 810a4450-8f9f-4e12-8c27-016ec57ee701 | intent | complaint | unclear | complaint | True |
| 1a1bae74-ce14-45b8-89c2-e71e19b95e44 | topic | billing | access | billing | True |
| 88871074-f96a-46be-b6b2-c9941536577a | severity | 1 | 5 | 1 | True |
| 8fadae5d-761d-46c2-bf32-4b5b558b3867 | intent | praise | cancellation | praise | True |
| cbce9cc9-c5c0-4519-bb0e-16dfadb48d92 | topic | other | billing | other | True |
| 6270c72a-be0a-4a32-a476-756819bb175a | severity | 3 | 1 | 3 | True |
| f6e25150-6569-4f06-9097-ce4409b4a0d0 | intent | complaint | request | cancellation | True |
| 174bd61f-31a2-43a4-8145-582e182f3bad | topic | other | usability | other | True |
| 29cc3d62-cd17-453a-9979-0f8904b30859 | severity | 3 | 1 | 3 | True |
| 46b95d8e-4e5b-4c7c-a2b4-dcf330b1b4a6 | intent | praise | request | praise | True |
| 149e4563-f368-40e6-a498-2c1f1b79e2ed | topic | other | catalog | other | True |
| 77a58642-0323-49c2-a45d-39ee1bb2e319 | severity | 1 | 5 | 1 | True |
| e6837972-f3e2-4656-8743-f1af272d6e40 | intent | complaint | unclear | request | True |
| 25912b56-8576-4824-a3b0-8698ba8d9127 | topic | catalog | billing | catalog | True |
| 9884c4c1-06d9-4e04-8788-b1d9a9745635 | severity | 3 | 1 | 3 | True |
| 5813c49b-8492-41fe-884b-c2e28d025dd9 | intent | praise | cancellation | praise | True |
| 1b2e2a2b-c614-4d6b-90b4-e8ac284c13c6 | topic | usability | billing | usability | True |
| 0e413cb2-12a5-41c8-ac8c-55beff97f1cb | severity | 2 | 5 | 2 | True |
| f478b1fa-a972-4695-8538-1ca9caa78d19 | intent | praise | unclear | praise | True |
| dcbec89b-876a-42e2-b075-17341e952deb | topic | other | support | other | True |
| d2fb0597-3a90-4b77-98ca-468fbd4f0794 | severity | 2 | 5 | 1 | True |
| df9534f8-0af2-4ce6-bfd8-1e69382cb8c1 | intent | praise | request | unclear | True |
| 0ee9fb9c-a59e-4887-a1a0-8a5764f18995 | topic | other | playback | other | True |
| 0d710581-ee32-4aac-acdf-2e24ad581116 | severity | 2 | 5 | 1 | True |
| 1874f9f4-f5ab-4e22-93d6-988f7acaf253 | intent | praise | complaint | praise | True |
| e00cb3e3-c9fc-4d6a-a680-f7ecbaeac4df | topic | billing | downloads | billing | True |
| 1eff6e7b-3bcd-411f-96cb-912cc1155103 | severity | 1 | 5 | 1 | True |
| 073796f1-3a7c-443f-b888-6dc2c6c85231 | intent | praise | cancellation | praise | True |
| 21403926-5c41-41b2-b29e-6c7da62d259f | topic | other | usability | other | True |
| e1acf491-89df-4a48-a4bd-f0b05d40d0ab | severity | 1 | 5 | 1 | True |
| ef6c5fcf-f277-49ce-b1ac-67d3a3786fee | intent | complaint | request | complaint | True |
| 88db8216-b831-4373-a79f-b46a14dd966b | topic | playback | other | usability | True |
| 78d65924-c32e-479f-ba91-1193e794544f | severity | 2 | 5 | 2 | True |
| daff284b-09af-45e9-a154-0cbc02239cf6 | intent | complaint | cancellation | complaint | True |
| 9098307a-7ad3-4f4a-866e-a0ef74b8f9f2 | topic | other | access | other | True |
| fd4af45d-b792-46dc-aab0-5ed86da3c088 | severity | 2 | 5 | 2 | True |
| ec14c0cb-6326-4d90-83f0-90bff16f332f | intent | praise | complaint | praise | True |
| 917c33f3-7d4e-47ad-b114-5a7ab243e797 | topic | other | downloads | other | True |
| c8f8b212-83c4-4811-9c9b-f5a609e724db | severity | 1 | 5 | 1 | True |
| 22c2184b-c70b-4bc8-8691-dc9e229f4288 | intent | praise | cancellation | unclear | True |
| e2aecbeb-7514-41ea-b63f-fccf9b5a4070 | topic | other | support | other | True |
| 1bafb587-cfa5-4437-92c6-75c0929ae606 | severity | 1 | 5 | 1 | True |
| e4006f91-2b7d-4f67-a3a9-28f9e95e9407 | intent | complaint | request | complaint | True |
| f17aad6a-b873-4130-ac5d-24d9effea86e | topic | usability | catalog | usability | True |
| 7ab5509b-caca-434a-8e7f-90224200fde5 | severity | 2 | 5 | 1 | True |
| da15bf06-1e8f-4479-84e5-bfeceb62d572 | intent | complaint | cancellation | complaint | True |
| 1c0165ea-cee7-41d9-a3bb-060543e7cd08 | topic | playback | access | playback | True |
| c17bfeb6-70a0-4a79-9f42-b148396b2b89 | severity | 1 | 5 | 1 | True |
| 67da539c-9c4d-4d3c-9b15-0405d717a182 | intent | complaint | unclear | complaint | True |
| 5d387cb5-d339-41d0-9bc3-6b31ab0b2be6 | topic | other | usability | other | True |
| 9ffb4b5e-0eee-41b4-af3b-836d924dbfd5 | severity | 1 | 5 | 2 | True |
| c1c61104-fd0c-4b04-8fd0-30024d5576ba | intent | complaint | praise | complaint | True |
| 46272d7f-9ec5-4315-ac26-875be328c65b | topic | playback | other | other | False |
| 5a0914d1-d001-483f-8ed2-e18992cf05e4 | severity | 1 | 5 | 1 | True |
| 808eff68-8518-4077-85fb-45a18fc36cdf | intent | complaint | request | complaint | True |
| e482f379-9efb-4747-8f7f-fd8585176bac | topic | playback | downloads | playback | True |
| e06e3b3c-db6c-40c6-bbea-40c5f4b677cf | severity | 4 | 1 | 4 | True |
| de277da1-99a3-4c07-b230-d9caff413a55 | intent | cancellation | unclear | cancellation | True |
| 47e39a56-0a94-4bc7-a0bd-693afedf6337 | topic | billing | usability | billing | True |
| 7d9b55aa-d7ce-4154-a5a5-a68f5f125a6b | severity | 1 | 5 | 1 | True |
| b97cdbdf-fd1c-40a7-a99a-009c18edf272 | intent | cancellation | praise | cancellation | True |
| 99b81e5f-d00e-47f7-85e1-9b081b12a25a | topic | other | support | other | True |
| b0d717f3-e963-4d30-8f11-fbb845599a9b | severity | 1 | 5 | 1 | True |
| 054abedd-ec8a-4c3d-8559-a1915a3a6687 | intent | praise | cancellation | unclear | True |
| 15288da3-ed58-4709-83fb-22ae762f25aa | topic | other | playback | other | True |
| 028a9ba3-674f-4f62-b37f-07c0dde29730 | severity | 2 | 5 | 2 | True |
| c48a9c6c-1088-4747-add1-d228c7348b0f | intent | praise | unclear | praise | True |
| d59f41ba-faa1-4ca6-a624-6a3522db2496 | topic | billing | downloads | billing | True |
| ddddfe43-b60b-498a-a968-70ca490bcedc | severity | 2 | 5 | 2 | True |
| 3ffddabb-c386-453b-86de-cb220112b3de | intent | complaint | cancellation | complaint | True |
| f2d7ee89-8f3a-45bc-ba5d-fbb39927c763 | topic | other | usability | other | True |
| eb085cdf-afe2-4ac5-bf24-6053ea9eceb8 | severity | 2 | 5 | 2 | True |
| 84d1521b-1873-497a-a99d-7f4a591a397d | intent | praise | complaint | praise | True |
| f06d2d0a-5b6d-4900-b9dd-f03bccb1ca37 | topic | billing | playback | billing | True |
| 9fa7a0a1-05cf-46d4-a9e8-619d2d4d5870 | severity | 2 | 5 | 2 | True |
| f6f3d585-cd68-43c9-a2ea-20579a22c3e6 | intent | complaint | praise | complaint | True |
| 5bc05424-a423-4241-95b0-4837cf7b1d39 | topic | other | access | other | True |
| 5846a4d0-ac2e-4fb7-956b-e929439f2064 | severity | 2 | 5 | 2 | True |
| 9ec00065-e0c3-4792-a444-3aa84a1239cb | intent | praise | unclear | praise | True |
| 6739c885-05ac-4fa6-ada2-133f5ab45069 | topic | billing | usability | billing | True |
| bc51846d-b059-4969-8624-580b1ea227ff | severity | 1 | 5 | 1 | True |
| 52032f0b-18f4-4025-8b47-05cebef394fd | intent | praise | request | praise | True |
| 814c82d7-a7ed-4c7c-9d6b-34c705ddb9b8 | topic | other | support | other | True |
| 6b2400b3-cc6a-4f33-98d9-0c102f57a24f | severity | 1 | 5 | 1 | True |
| 69cc330d-4289-41df-88eb-225d4735d4dd | intent | complaint | unclear | complaint | True |
| 25bb0b0d-d285-4607-881e-75ee116afbb2 | topic | other | playback | other | True |
| fedfc3ea-4194-40e4-9661-c9b09fde8920 | severity | 3 | 1 | 3 | True |
| f1f149ef-df82-4f5f-9252-ba5908649e11 | intent | cancellation | request | cancellation | True |
| 79be6a07-75f2-4c70-bbb9-6a378dfb9c72 | topic | catalog | playback | catalog | True |
| 19b75467-0999-455b-b9c2-b8650371f548 | severity | 3 | 1 | 3 | True |
| de9ecb0e-7406-4196-a7f9-d4efddaece9f | intent | praise | unclear | praise | True |
| 951ad752-766d-43cb-882c-059c720144cf | topic | catalog | support | catalog | True |
| 16537579-2ee6-4f7c-8c3c-23faa0f7b1f6 | severity | 1 | 5 | 1 | True |
| d57b90a7-b939-497f-a135-84dbb343dde1 | intent | unclear | praise | unclear | True |
| ae10176c-cb32-4674-877a-9880d7ed6b58 | topic | other | catalog | other | True |
| c45a56d0-2640-4610-ab52-f38856b7d951 | severity | 3 | 1 | 2 | True |
| 2c86ca2e-47b2-4d03-82b9-a54728cb0de0 | intent | complaint | unclear | complaint | True |
| 084442c2-440b-4e9f-8816-a4f375b0ad92 | topic | catalog | billing | catalog | True |
| 7a36db46-62ef-4caf-abcf-d5484a4fc7b5 | severity | 1 | 5 | 1 | True |
| 1de72706-9826-4355-978c-39d63c8d753d | intent | praise | cancellation | praise | True |
| eb6b0fbe-6723-4fdd-8b0e-6c5f52021c49 | topic | catalog | access | catalog | True |
| 9dffb899-32bf-4a1a-bce9-d0f10f7a2708 | severity | 1 | 5 | 1 | True |
| 6871ced2-73e2-46fc-a42c-a65e7bd7f45d | intent | praise | unclear | praise | True |
| 61a4699a-d65a-472c-923c-62c4915e1b29 | topic | playback | usability | playback | True |
| e0a159d0-9cd9-4007-a2a9-206092a1367c | severity | 1 | 5 | 1 | True |
| fb6328bc-e77e-4342-9209-3a01fa01fd2e | intent | praise | request | praise | True |
| f291c945-2e08-4452-a1a5-e274f9ea51e3 | topic | usability | catalog | usability | True |
| 487d1c4e-b51f-429b-a186-d39bdf9b4e23 | severity | 1 | 5 | 1 | True |
| 7dbabd1d-05a6-4118-8140-712aab421162 | intent | cancellation | praise | complaint | True |
| 7575b51b-c351-4f76-b25c-e0f17e40fdd5 | topic | other | billing | other | True |
| 5bfea9bd-c14a-438c-a1b6-40dc463f9824 | severity | 1 | 5 | 1 | True |
| 6ccd45da-4447-473b-b98b-2a84065bf46a | intent | complaint | praise | complaint | True |
| 50df139a-e026-4c5d-8451-4425ce49efe5 | topic | other | usability | other | True |
| 62e456f4-8afa-4f1b-94f4-733dec432743 | severity | 1 | 5 | 1 | True |
| 5d88d895-eaea-41e0-9a7f-ee704d15c074 | intent | complaint | request | complaint | True |
| 8251bbad-8125-4ec6-9e21-08fb77331d2d | topic | other | catalog | other | True |
| ab1eedf5-5f3a-4188-92d8-d4a970051310 | severity | 1 | 5 | 1 | True |
| d3d72c3b-5847-46ea-9ba0-9d5f0a55cc81 | intent | praise | request | praise | True |
| 16cdf694-5ee1-49d0-858d-813f41d22704 | topic | other | access | other | True |
| dc7b35fa-50ea-4a8d-b6f7-9251ee1e8e01 | severity | 1 | 5 | 1 | True |
| 70fe701d-91d4-4cf3-add6-0e66b156125f | intent | complaint | unclear | complaint | True |
| a3faa1ce-d77e-4e72-97cc-98c0dfc93c9d | topic | other | downloads | other | True |
| 14eb257f-7d2a-4245-8c75-99be7011950c | severity | 3 | 1 | 3 | True |
| 0ace0c74-417a-4267-b8e8-eefe8a878ab6 | intent | praise | cancellation | praise | True |
| e5a35ee9-fdb1-4ada-99d6-588cb58d969e | topic | other | support | other | True |
| 1330843b-a4f7-4f15-82b7-298a9e496350 | severity | 1 | 5 | 1 | True |
| 354a2631-ed4e-4dd5-8512-bf7a40145cf7 | intent | cancellation | complaint | cancellation | True |
| 36ed5e00-5bfe-4ae6-8ffd-cba88c2abf1f | topic | other | playback | other | True |
| ae31ea64-6cbe-464e-b93d-a8c4a15e3893 | severity | 1 | 5 | 1 | True |
| bf4f3bd6-02a1-4236-b082-3821386d8278 | intent | complaint | cancellation | complaint | True |
| f6b9ccca-af8b-46a3-b3f5-8237ad780cdc | topic | usability | other | access | True |
| 98438cc0-c588-4d0b-8849-e36320d3d558 | severity | 1 | 5 | 1 | True |
| 900c03f8-9e83-4f9f-b4bb-40cfaae49708 | intent | praise | complaint | praise | True |
| f7a706f2-f754-47cb-bbcc-40cee75bcad6 | topic | catalog | support | catalog | True |
| 70c375ab-8a1f-4ecc-a5bb-ba800cfbfa43 | severity | 1 | 5 | 1 | True |
| 5d6b14db-49a7-45b0-b14f-98a5699a7935 | intent | request | unclear | request | True |
| e87190a9-b584-4053-81ff-36d58b4e0bec | topic | catalog | usability | catalog | True |
| a0885f34-9c7a-440b-9061-374cb93008ff | severity | 1 | 5 | 1 | True |
| 65783cf6-28d1-4923-8017-35e55f8bd3c1 | intent | unclear | cancellation | unclear | True |
| c106504c-31fb-4375-9b6b-1fb25d0bdbbb | topic | catalog | billing | other | True |
| f872e65b-fe06-44a9-9dc5-7fb88aa5de4a | severity | 1 | 5 | 1 | True |
| 88c8d934-d405-42b0-baf7-e52a43a52ca2 | intent | complaint | cancellation | complaint | True |
| 2d9e8f41-7473-41c6-8552-cb440c15ece0 | topic | other | downloads | catalog | True |
| 4dcbadaf-2c3e-4beb-981e-961abb7ffb13 | severity | 2 | 5 | 1 | True |
| 66396807-798f-4470-82ed-13a8103ee17b | intent | praise | complaint | praise | True |
| b0533cf1-3086-4ca2-bde8-67365f0206b6 | topic | other | support | other | True |
| 29c8ca70-a0b9-4afa-8305-773b831947a3 | severity | 4 | 1 | 4 | True |
| 7a10d7f7-06ca-4afa-abb3-a52ef48fb54a | intent | complaint | praise | complaint | True |
| 082c4485-a404-4a39-8460-8c5431b64201 | topic | other | playback | other | True |
| e83ef9c6-6e12-4c2c-a702-21d1bc86e30b | severity | 1 | 5 | 1 | True |
| 79c9fb60-7d1c-4b43-9e5e-11b484760e7c | intent | unclear | cancellation | praise | True |
| 4a797515-8577-4c07-ba42-dd71f14ccd43 | topic | other | billing | other | True |
| ce143420-fe90-47d8-a2db-0798f651b3d1 | severity | 2 | 5 | 1 | True |
| 40efcc20-440c-42d0-9243-2f9f6a0b9e76 | intent | complaint | cancellation | complaint | True |
| 5b52357b-a084-4f22-b6c0-d994d69f2740 | topic | other | usability | other | True |
| e974ab79-1d1f-45c0-bad8-c13b4d2993d8 | severity | 1 | 5 | 1 | True |
| bba1b682-0bbb-4a6d-80e7-3b38c19962b5 | intent | cancellation | praise | cancellation | True |
| a1623586-126c-4684-8c67-b0fbabf831bd | topic | other | catalog | other | True |
| 39bccb5a-460d-4264-97a9-0d8f634a762a | severity | 2 | 5 | 2 | True |
| f0928c87-437a-469b-be6a-db5be70e306d | intent | complaint | praise | complaint | True |
| 3fed61ac-b08c-4399-8fe3-eb6655a3980a | topic | playback | downloads | playback | True |
| 993fe23a-9e57-426c-bbb9-16b95c75d3f4 | severity | 1 | 5 | 1 | True |
| 5d722980-984a-47f9-ae00-1bd56b4cbc4e | intent | cancellation | complaint | complaint | False |
| f5ac0fe7-eeeb-47b9-aba8-fb85fde34cae | topic | other | downloads | playback | True |
| f3aeeedf-1ff7-4e01-89ca-728a265bcd41 | severity | 3 | 1 | 3 | True |
| 6e698db1-4adc-4583-9944-1a82be04c640 | intent | unclear | praise | unclear | True |
| 2a8d4cce-061d-4e07-a1cf-3b7346d78872 | topic | other | support | other | True |
| 3901bc28-2f7a-4a45-a3a4-5e7369067ed4 | severity | 1 | 5 | 1 | True |
| 38df5d68-f226-4305-a012-b045040c9dc5 | intent | complaint | unclear | complaint | True |
| f85b32c7-1962-47d9-8c63-5e50a0fbe697 | topic | usability | catalog | usability | True |
| 0a6f5176-051a-49db-bfe5-32d1421895bf | severity | 3 | 1 | 3 | True |
| d244ddb6-af10-48cb-a270-2613514759aa | intent | complaint | praise | complaint | True |
| 527ba5f0-285e-4a17-839b-4cde29a5947c | topic | billing | downloads | billing | True |
| 3972a2ca-e2a0-4dc2-9fc7-02912557f340 | severity | 2 | 5 | 2 | True |
| 52f4f964-deb7-471c-a9c1-5605204367e9 | intent | praise | unclear | praise | True |
| b84d48bd-297b-4993-a6b3-455d87e8e553 | topic | other | usability | playback | True |
| 627f1447-a24f-4b8b-aa6b-922127f6f316 | severity | 1 | 5 | 1 | True |
| f7c5ca9a-483e-4ab5-845a-8234bc968f20 | intent | complaint | cancellation | complaint | True |
| b8946ad0-438e-4eff-ba22-bdf01f2aa016 | topic | other | catalog | usability | True |
| a620f1aa-5004-4646-99c8-f8af37679ffc | severity | 1 | 5 | 1 | True |
| afb2702f-5c2e-49cb-91af-2d5d78fd6a3f | intent | unclear | request | unclear | True |
| 73382d64-8055-4566-ae9b-258e8b3703f5 | topic | other | access | other | True |
| 62ad5c13-dbe2-4ef6-8141-240bc9f05f7a | severity | 2 | 5 | 1 | True |
| e93f8200-117d-4d23-940a-a0ddf95e6cc2 | intent | cancellation | request | cancellation | True |
| ad2944a0-2a42-4048-b139-a211b7aa657e | topic | other | downloads | other | True |
| 374e85c1-593f-4228-b10b-e88ac235a6db | severity | 3 | 1 | 3 | True |
| fd3004cb-90b6-43fc-8d90-229af72de58a | intent | complaint | request | complaint | True |
| 26713ed2-2197-4652-a47b-366b84e5789d | topic | other | support | other | True |
| 46513e35-d2b3-447f-99d5-3b48231209d5 | severity | 1 | 5 | 1 | True |
| 462dee49-990d-4299-aad8-b272adcaff83 | intent | praise | request | praise | True |
| ad7656be-4681-4462-bcd4-5a8019d00adc | topic | other | playback | other | True |
| e9994b43-bf79-407e-acfc-10187e972bd6 | severity | 4 | 1 | 4 | True |
| 6cf1a4c7-9de9-4a7b-86d1-6ffb4ebff714 | intent | praise | complaint | praise | True |
| 94ebbc86-85a6-477f-a4d4-a94b24b5ca68 | topic | other | billing | other | True |
| b9e76f2f-64da-4f0e-95e5-16e969a9a9e5 | severity | 1 | 5 | 1 | True |
| 460bb018-0c28-4d00-9ec2-298c17a8126d | intent | complaint | praise | complaint | True |
| 6c9f77d6-fd9b-434c-81b0-8bd68d53490a | topic | catalog | support | catalog | True |
| 24001e38-464a-4827-b54c-abe0aada9400 | severity | 1 | 5 | 1 | True |
| 349186bd-27e1-413b-8146-29444d4fb904 | intent | praise | unclear | praise | True |
| 502d6452-5f33-4a8a-8e8e-1d50f282a8c6 | topic | catalog | usability | usability | False |
| 123fd497-b654-4613-8705-614301cdc512 | severity | 1 | 5 | 1 | True |
| f4c619c8-785f-4024-bea5-05501e1c1186 | intent | praise | request | praise | True |
| b4f5d039-db39-4579-b2ab-219efd44f1ba | topic | other | access | other | True |
| b4c00fd9-adaf-40d8-9ec7-15db3bbbe9df | severity | 1 | 5 | 1 | True |
| a1bab63a-a567-44ef-bf1d-1773f738833b | intent | complaint | unclear | complaint | True |
| 4089ef03-a40c-46a3-ab0f-acda73aa33ee | topic | other | downloads | other | True |
| 9848572e-5092-4be6-96e0-80ff65c1e8bf | severity | 3 | 1 | 3 | True |
| 593fcf0c-1434-48f6-aeaa-67fbe2c8901b | intent | complaint | praise | complaint | True |
| e47a0dd7-0d42-4bba-a597-f8c6e2d80674 | topic | playback | usability | playback | True |
| 49930880-2283-41be-b795-4afc0864b099 | severity | 3 | 1 | 2 | True |
| b0b8f4e0-cca1-485d-844c-ff1e458b3dd6 | intent | unclear | cancellation | unclear | True |
| cf29924c-f881-44a5-87cb-b56b58ad7559 | topic | other | playback | downloads | True |
| b4cd1e19-5070-4313-a77c-9664734c6899 | severity | 1 | 5 | 1 | True |
| d0d232e9-de6f-4788-9685-b901a721c240 | intent | unclear | praise | request | True |
| f0001c9f-bb14-4da7-bf57-2f5f71373149 | topic | other | billing | other | True |
| 91f5abeb-ef51-4557-ba30-2a4b5d9a3904 | severity | 2 | 5 | 2 | True |
| 8074d1d8-9378-4ac4-b7da-99441ee1d3f1 | intent | complaint | unclear | complaint | True |
| 66a0df8d-7c4b-4c4d-bbda-41db0d7f3101 | topic | usability | downloads | usability | True |
| f2da86cb-44bc-4419-8f51-65ea9a470ff8 | severity | 3 | 1 | 1 | False |
| bc781356-a714-4b04-9a27-372d3edf1561 | intent | complaint | praise | complaint | True |
| fbdd899f-8fe5-4c37-978a-fe00886ae23c | topic | other | catalog | usability | True |
| 88a8e50e-5c39-472c-8a38-26be08284905 | severity | 2 | 5 | 2 | True |
| c3f40924-c845-4ac1-a767-ccd099b1e1ca | intent | praise | unclear | praise | True |
| 61e0e586-24d8-4d43-870d-b27a6ac6a83a | topic | other | access | other | True |
| 1b447a22-75e4-4e1e-a3b7-c983d56bf88e | severity | 2 | 5 | 1 | True |
| 377d562f-f452-4c24-8971-819d4f956340 | intent | complaint | cancellation | complaint | True |
| b463115b-e967-465f-a153-8bcde5567037 | topic | playback | support | playback | True |
| 4632ac60-ef72-40dd-bf00-53a74d011785 | severity | 3 | 1 | 2 | True |
| 92301dd2-d924-4e7b-85d9-2c9d50cf1360 | intent | request | cancellation | request | True |
| ecefd0fd-4b82-4040-bfd3-38ff3ce8286b | topic | billing | catalog | other | True |
| 9e121b51-ec5b-470c-927f-72b9bef1f4c4 | severity | 3 | 1 | 3 | True |
| a8f3b44a-5b97-4c63-bf77-cac05efe45e8 | intent | praise | cancellation | praise | True |
| 5c61e871-e840-44c7-b336-d6abacfe0ebd | topic | other | playback | other | True |
| 79be5796-8f4a-487e-891b-2533d68f4a2b | severity | 2 | 5 | 2 | True |
| 7e9b477d-f463-4ac2-ad80-09b2a02c167e | intent | complaint | request | complaint | True |
| 65950ee6-e826-4753-aa14-8d407d6307dc | topic | usability | other | usability | True |
| d70d0bf5-4c6a-46f4-b66a-a74cb67973e2 | severity | 1 | 5 | 1 | True |
| 516c1de3-b407-45a7-a4d7-88315e385960 | intent | praise | request | praise | True |
| 4ab9b272-1381-476d-913b-b1711473715e | topic | other | usability | other | True |
| f24bd6d4-6158-4d8b-872a-8b9e1a28711f | severity | 1 | 5 | 1 | True |
| 84399438-7323-4b85-b09d-bd23d33202d8 | intent | complaint | unclear | complaint | True |
| b70b4d29-e5e4-4ee0-8cd7-2016dc0c0f1e | topic | catalog | usability | usability | False |
| 2730eb89-cafe-4478-a70b-6cab7bdcbad7 | severity | 3 | 1 | 3 | True |
| a089d131-e842-4a10-acf1-40ed84e9790a | intent | complaint | praise | complaint | True |
| 42231063-c460-4028-8378-5b165a419cc9 | topic | usability | playback | usability | True |
| 9c3a6f10-bb8b-4b31-bd8c-d2e53eb28bc3 | severity | 3 | 1 | 2 | True |
| b0dd9db7-cbe2-4470-abab-a900d6f189ca | intent | praise | unclear | praise | True |
| b2e79930-fbea-44a4-b75e-bdc3c4bcdde0 | topic | other | downloads | other | True |
| bd1855f8-b0e0-4d96-9907-ccdf875f109c | severity | 1 | 5 | 1 | True |
| 6a55962a-658d-4649-9414-c692c44f30cd | intent | unclear | praise | unclear | True |
| 24719c9e-7518-4c8b-9057-7086697ddb58 | topic | billing | catalog | billing | True |
| 1d999823-6ede-4265-9595-66ca9f5a8f54 | severity | 3 | 1 | 3 | True |
| 9951f3e7-70ca-46d3-bcc3-49671d8fddee | intent | cancellation | praise | cancellation | True |
| a59c54b8-baad-43e6-ab35-56d0b58ea93d | topic | playback | billing | playback | True |
| 1e2230e5-83a9-46c3-8d19-04cc995ca43a | severity | 2 | 5 | 2 | True |
| 311d2a0d-8e08-47ca-a5ae-2800666d4232 | intent | praise | cancellation | praise | True |
| 9982023c-7dfa-4737-8ee1-a259b414d3de | topic | other | billing | other | True |
| f9757f01-0b93-41bb-a1ad-cc3f0a7daa46 | severity | 2 | 5 | 3 | True |
| 10494ffd-1cf0-4d99-af8c-60d4d5624782 | intent | unclear | cancellation | unclear | True |
| e44cb528-6cd5-4393-984a-064d9e2b9fe0 | topic | other | usability | catalog | True |
| 4a3916b6-d78a-4853-a8a6-2e1358c04cd9 | severity | 5 | 1 | 5 | True |
| 280c36db-c655-471a-8cb0-2bb904c97626 | intent | complaint | cancellation | complaint | True |
| e390646f-4597-4b48-a36f-9674c9fb125d | topic | other | catalog | other | True |
| 48596a44-5813-4068-864d-0d3f4309c955 | severity | 1 | 5 | 1 | True |
| 6bf02cc6-e707-40c2-9bd9-5824783b9b10 | intent | request | cancellation | request | True |
| a18556d1-6792-4477-b444-6f322251a6e1 | topic | playback | downloads | playback | True |
| a0042ef6-8513-4e47-89d2-125e8cea3e67 | severity | 2 | 5 | 2 | True |
| 2a5b6ab7-2605-4cf9-9d92-f5cb5cf85904 | intent | cancellation | request | cancellation | True |
| 33a27208-66fe-4da3-ba15-cdcd1afae275 | topic | other | downloads | other | True |
| edb04b04-44a2-44ce-95f5-940bc3550573 | severity | 3 | 1 | 3 | True |
| 3f8859c6-0ea5-4d97-aaf5-8ebd8b4aeedf | intent | praise | unclear | praise | True |
| c2ab2d30-61e1-425f-800f-54bc088fe3b2 | topic | other | support | other | True |
| 09f36334-fcf5-4c03-9774-4811d6ac37df | severity | 3 | 1 | 3 | True |
| f61b77ca-3fd7-40a8-b932-b86c7fd3fe51 | intent | complaint | cancellation | complaint | True |
| 85b426ac-bb9f-464c-b396-f3cf95dccfbe | topic | usability | catalog | usability | True |
| ae3fd8f6-6b7f-40e2-a248-73a8708bea49 | severity | 1 | 5 | 1 | True |
| 8c9f94b9-6385-4dc7-abcf-c5124210ee93 | intent | unclear | request | unclear | True |
| f19fd026-346e-4ad7-86b6-dee18555877d | topic | other | billing | other | True |
| dfc4781c-863c-4a6a-ad4e-a9e6048e8047 | severity | 1 | 5 | 1 | True |
| fc9ab108-eb91-4edb-ab6f-9a12c55ed766 | intent | complaint | praise | complaint | True |
| 6d390539-6adc-4e46-8492-3f2c67930a4f | topic | billing | other | billing | True |
| a5763546-c2b4-4a90-bc3a-a55b2ce2a6c0 | severity | 2 | 5 | 2 | True |
| cd64a9cd-9878-4254-af8c-d26bc73ec84b | intent | complaint | request | complaint | True |
| 8e24e6ac-06f3-455d-af46-b41538419b59 | topic | playback | other | playback | True |
| fa30aa82-2893-4533-83f2-cc395eb149e7 | severity | 3 | 1 | 3 | True |
| 320f782f-c6c5-400a-8ee7-d6a5009b3e25 | intent | complaint | cancellation | complaint | True |
| aea74b33-c891-437c-9fa8-ce33053baa66 | topic | other | access | other | True |
| 21dbefdc-5a2a-4999-866f-a7106971a85d | severity | 1 | 5 | 1 | True |
| 613f0ce3-d355-48ff-9b96-f44d1fd8a7a9 | intent | unclear | request | unclear | True |
| edd4b67a-d874-4d05-bcf3-558f0feb509f | topic | other | downloads | other | True |
| 02cb2115-dd09-4a85-b087-b62e4ea98c67 | severity | 3 | 1 | 3 | True |
| f493a939-0367-4647-8b48-21b744eb81ef | intent | cancellation | request | cancellation | True |
| 4d71a426-6f4b-4295-94b4-cee6c6866829 | topic | playback | usability | usability | False |
| f3bab585-3f13-435a-8f6e-9f5ff3bad434 | severity | 1 | 5 | 1 | True |
| f3b357e0-13b7-40f0-9b51-d15dc7b5f978 | intent | complaint | request | complaint | True |
| b5cc2b79-6065-452a-9f08-0aa3128b1029 | topic | usability | catalog | usability | True |
| ec54c992-243f-4132-9e29-c27911a3cd27 | severity | 1 | 5 | 2 | True |
| 92ba4b29-dce3-4cb5-8098-87a09d7c5b7f | intent | complaint | cancellation | complaint | True |
| d79f68b3-95e4-4202-ab65-7387a1b82d5e | topic | other | billing | other | True |
| 72ff1851-6b9d-4623-8c56-efbe1dc40710 | severity | 2 | 5 | 2 | True |
| 0e8b4ff5-e5b4-4c49-b1dc-31f0479d5124 | intent | praise | complaint | praise | True |
| 403aa955-b37d-4227-9a32-54a9218e470d | topic | other | usability | other | True |
| 8cb41f18-f657-490c-ab37-60cdc6c38419 | severity | 1 | 5 | 1 | True |
| ec3d2850-4d40-4b27-9d9b-d1e919625c9d | intent | complaint | praise | unclear | True |
| 7b29e012-3b37-4dfe-a64a-0f6184892492 | topic | catalog | usability | catalog | True |
| ecf1a082-1039-42ff-9eb5-0fc6869128d6 | severity | 2 | 5 | 2 | True |
| 8be1e808-7dc0-479c-9156-2d13ecdeb509 | intent | praise | unclear | praise | True |
| 79039e7a-6427-40af-91ab-dad66562d8c3 | topic | other | access | other | True |
| 1205d8ac-da85-4d65-bbd8-62aab224f857 | severity | 2 | 5 | 2 | True |
| 0997a75a-f083-4902-83ed-81b15030ca38 | intent | praise | request | praise | True |
| 5d2d2c6a-e872-4a03-8287-d6d53ac8c232 | topic | catalog | access | catalog | True |
| 1499ad78-e80b-40e5-86c4-f090794400c8 | severity | 1 | 5 | 1 | True |
| ff52246d-bc22-4db2-ab4f-1cf8f5f32b4a | intent | complaint | unclear | complaint | True |
| 8142d95f-3a48-45cf-89bc-8cc0af88e5ce | topic | other | support | other | True |
| adf3c6ca-7d47-49f2-8304-17377a95ed9e | severity | 2 | 5 | 2 | True |
| f1831af3-f288-42a1-8a88-36f3169ae2c7 | intent | praise | cancellation | praise | True |
| 34a6be44-15d5-483a-b127-091b8fc1fbf3 | topic | other | playback | other | True |
| d71c690b-ce20-41d7-9f5e-0e986fa1a78b | severity | 2 | 5 | 1 | True |
| 3bad9979-3759-43db-b959-1eb782c73893 | intent | praise | unclear | praise | True |
| 6f6111e8-1148-42ef-bb8b-fead9ecfeb0c | topic | support | catalog | support | True |
| 425fb6fc-1a2a-451f-9c59-bfc8fe72f9bf | severity | 2 | 5 | 2 | True |
| b1f7fac4-a356-4482-abfe-c735e450356a | intent | complaint | cancellation | complaint | True |
| 417836f6-caa7-463a-82b4-ae2c26f69ea1 | topic | billing | other | billing | True |
| 36e4952a-79a0-4886-b681-a2d3c8811b4f | severity | 5 | 1 | 5 | True |
| 55452512-44eb-44e5-9ea1-efa116c5b241 | intent | complaint | unclear | complaint | True |
| da5cd791-316b-4bef-b337-1f822bd9bc89 | topic | billing | playback | billing | True |
| 242906b3-405a-453c-8c30-3b999cf6b430 | severity | 1 | 5 | 1 | True |
| b9662b65-76fb-4c16-b0f1-d24d5f5a509c | intent | unclear | complaint | unclear | True |
| 24d09fb7-2d02-4bda-b42a-3c8c93bb6fd1 | topic | other | access | other | True |
| d121232f-996d-405f-b3ce-cd4e22d197fb | severity | 1 | 5 | 1 | True |
| 4d4a439a-0b00-4aee-a86c-a52f9200e209 | intent | praise | unclear | praise | True |
| 75c3e195-2468-4c28-b3a3-b119edf13867 | topic | other | downloads | other | True |
| e83e8093-7f55-4fa3-88bc-f1b5d1068d42 | severity | 1 | 5 | 1 | True |
| 6083a60d-19e2-4cdb-9c33-5f3f8399a083 | intent | praise | request | praise | True |
| d8996bf8-9140-4b4f-be58-19098eef0aed | topic | catalog | downloads | catalog | True |
| bacc0811-6dd4-4e96-834a-2ad2d415dffd | severity | 1 | 5 | 1 | True |
| 6b3607af-6690-4e31-bc2b-5174419f1084 | intent | cancellation | praise | complaint | True |
| 7ed9149c-dacb-4dcb-b091-7b2c95ff955c | topic | other | playback | other | True |
| a38fe073-7d6a-43f9-98ed-d635e0ce0171 | severity | 2 | 5 | 2 | True |
| 58746d7f-1f24-488e-a2eb-56ee83db0a6f | intent | request | unclear | complaint | True |
| d4ef4933-fe5e-4d78-b34f-61e6fcabed2c | topic | other | billing | other | True |
| 87ad2907-da6e-450f-ab09-541d67909d4e | severity | 2 | 5 | 2 | True |
| a0fbc85e-1252-4ec9-9736-4f511757d96c | intent | complaint | request | complaint | True |
| e2c757d7-5145-4515-84bb-b0730f8cc594 | topic | billing | other | billing | True |
| 90eb0039-ec27-4ae6-97c1-6274ec78520a | severity | 2 | 5 | 2 | True |
| 23806404-fdc5-4093-9a01-90331be3cbe6 | intent | complaint | cancellation | complaint | True |
| 32db3f37-13cb-429a-975e-42c1bf6ecf00 | topic | usability | support | usability | True |
| ea919bc3-5d9c-4c77-aeac-bd6066d6cee9 | severity | 2 | 5 | 3 | True |
| f2c27aee-6cfa-485f-81f0-e5f117ddf69c | intent | complaint | unclear | complaint | True |
| e6fa60d5-cc00-4b78-a714-0076a209fcfd | topic | other | access | downloads | True |
| a09201fa-4875-4df9-83e1-9cb53df838f2 | severity | 1 | 5 | 1 | True |
| 7c7be0a2-5b83-4185-918b-893b644aa9e1 | intent | cancellation | request | cancellation | True |
| 29d6227e-8b38-4832-9891-9ad977edef5e | topic | other | downloads | other | True |
| 34d3834d-d420-4501-9355-b60b8e45b7ad | severity | 1 | 5 | 1 | True |
| c1c3c2a3-8d53-4d09-b7ef-fcbf0bf96102 | intent | complaint | request | complaint | True |

## Disagreements (enricher vs verifier)

- `0047a0a1-9bdc-4a7c-9519-426a187a5959` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "I love the app and its function works smoothly for which they deserve 5 stars but I can't access Spotify podcast in Pakistan, therfore, I am giving 3 stars."
- `004cd387-7d39-4a0d-bc58-9ed4c540b200` enricher billing/complaint/3 vs verifier billing/cancellation/3: "I am very much disappointed with this new feature from this app. Premium for sequence songs, like seriously; why this shuffle system shown app... it's was going smooth and sound unless this feature sh"
- `009aa01e-1786-4dd0-8b62-43f266df47d8` enricher other/unclear/1 vs verifier other/praise/1: "I haven't tried it out yet, But I know it's going to be Good."
- `00ba6706-f74d-47b2-bbef-b5e6115cd655` enricher billing/complaint/2 vs verifier catalog/praise/1: "Love being able to find so many of the tunes I've lost over the years! And love discovering more. Really wish it was a cheaper monthly payment though for premium, it would be much more manageable long"
- `00e79a82-9834-4a83-9d3c-72d11d5c9b2e` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "This is too much u cant even seek okk i shift to other platform where ads dont disturb you every 2 songs i think u got too greedy u say that after 1 set of ads no more disturbance for 30 mins are two "
- `00ea0a93-5b2a-47dc-9d8a-4db499dc8e92` enricher other/praise/1 vs verifier other/unclear/1: "It so fan to a song"
- `00f5e72f-93b2-4b7e-b666-091ca0ce056a` enricher usability/complaint/3 vs verifier usability/complaint/2: "This app was good but now this app is worst because ad ad ad after one song or two songs. Remove ads from this app"
- `01036c2b-70ba-4214-b008-73250998b920` enricher billing/praise/1 vs verifier other/praise/1: "It's the only music app I will actually pay for."
- `0104c197-5d63-4a1b-838a-d3780fdcb1dc` enricher catalog/praise/1 vs verifier other/praise/1: "Good listening music"
- `016b7071-6423-49f6-9882-c45cfa3dcb8a` enricher catalog/complaint/3 vs verifier usability/complaint/2: "I can understand letting podcast creators putting ads in their episodes, but they should NEVER be actual videos. That is not ok. That is so far out beyond ok. It's like watching a YouTube video in 240"
- `01789d39-a70a-4d6d-ba52-eaa4eccb2f30` enricher playback/complaint/4 vs verifier playback/complaint/3: "12/08 update broke playlists. If you stop listening and pickup there later, it plays that one song then gets stuck every single time. You have to go pick another random song somewhere then go back int"
- `01a404bc-bc3e-4485-9461-008fb3034988` enricher other/praise/1 vs verifier playback/praise/1: "Great musics with original sounds"
- `01b923f5-c4e9-4d48-ab12-48405d78b58c` enricher catalog/praise/1 vs verifier other/praise/1: "Spotify offers you the best music you need to enjoy and relax"
- `01f335df-2b1b-41e2-8ad3-8ac95288d97e` enricher other/praise/1 vs verifier other/unclear/1: "IAM out of words ! It's fascinating."
- `02404778-dc81-4095-8d4d-b245d6606687` enricher billing/complaint/3 vs verifier catalog/complaint/3: "Too expensive. Some songs like yesu tiyo to aling alinga by milka omondi was removed from the app without notice"
- `0274684d-4415-4499-9d1d-6164330448cf` enricher other/unclear/1 vs verifier other/complaint/2: "Astagfirullah app"
- `028a9ba3-674f-4f62-b37f-07c0dde29730` enricher support/complaint/2 vs verifier other/complaint/2: "Very bad service after updat"
- `02c18b1f-abdf-440a-a48a-aa1f9ec375c2` enricher usability/cancellation/2 vs verifier usability/complaint/2: "This has become an advertisement app now. Don't install it guys."
- `02d36000-043d-4aae-b265-c48c9c9401a6` enricher playback/complaint/3 vs verifier playback/complaint/4: "It's showing no internet connection while connected to Wi-Fi networks but works fine when connected to mobile data."
- `03710026-d7b8-4f8e-b54a-2a39ef83efea` enricher catalog/complaint/4 vs verifier catalog/complaint/3: "Unable to access the lyrics feature"
- `038ec263-02f2-4e88-a735-372e8d579b4a` enricher usability/complaint/3 vs verifier usability/complaint/2: "Worst app to listen music they always put advertisement in between the song"
- `03a0822c-75cd-4e47-abb7-db988823647b` enricher usability/complaint/3 vs verifier usability/complaint/2: "Hey Spotify, I have another worst idea that you can use: mid song ads 🤯"
- `03d3fd25-1daf-46d5-aa8f-f248a2815d70` enricher usability/complaint/3 vs verifier usability/complaint/2: "I used to enjoy songs but now form 18 th may it started to give me annoyed ads. It's really annoying. Not everyone is rich to buy premium every month. All people deserve to listen to music without fac"
- `03fbd0c3-a72d-460e-8781-ae175318af58` enricher playback/complaint/2 vs verifier usability/complaint/2: "I keep lowering my rate, never raise it. Why replace enhance with smart shuffle? I can't pinpoint what I don't like with smart shuffle, it's just not as good as enhance. Tried it in beta it something "
- `041c2236-529d-4ffa-ba27-772aaa751953` enricher playback/complaint/3 vs verifier usability/complaint/2: "Battery drain is abysmal, home screen is a cluttered disaster of undismissable suggestions."
- `04262e8a-722e-48c3-b429-3a6fa0ab8d47` enricher usability/request/2 vs verifier usability/request/1: "major redesigns needed, please implement rounded UI elements across the application."
- `04472296-8003-45ed-b799-520832a262ea` enricher usability/complaint/2 vs verifier catalog/complaint/2: "Idk man. this is nice but I think I hate is, you can't remove unwanted shows and podcast in your your shows. My dumbass friend put a ASMR anime 18+ ???, And it keeps popping up. There's no way to remo"
- `04821981-3f4c-46df-b615-8f56fbb19cb4` enricher other/complaint/3 vs verifier downloads/complaint/4: "Terrible I cannot see my music"
- `0493c185-977d-4ca8-b144-f005e5c8d824` enricher catalog/request/2 vs verifier catalog/complaint/2: "Quality of Recorded songs is good. Need to better search engine"
- `04946089-fe3b-4e63-8ff6-ed2ea823c504` enricher playback/complaint/4 vs verifier playback/complaint/3: "App keeps crashing/stopping mid songs and keep playing without any sound. Yes I've tried reinstalling. I've tried all the recommendations google had to offer. It happens the most with the new smart sh"
- `04c7a26e-d57f-4a6d-ad23-75f52e8cbfe9` enricher usability/complaint/3 vs verifier billing/complaint/3: "I've paid for premium since 2019, I chose this app because of its ability to work best on the least amount of internet whereas I commonly work in places where you don't have much service. The issue of"
- `04caf4b1-41f7-4ee1-95f6-277efacdc9d2` enricher catalog/praise/1 vs verifier other/praise/1: "Get Best Music experience on Android 1. recommendations 2. Freemium 3. Quality"
- `052d8cd2-88b7-45fe-b1ce-73b86c07ad9d` enricher other/unclear/1 vs verifier other/complaint/2: "i hate this app۔bycott"
- `054abedd-ec8a-4c3d-8559-a1915a3a6687` enricher other/praise/1 vs verifier other/unclear/1: "Salamatof"
- `05512fed-2335-4d91-95ed-e3727932ffbc` enricher other/unclear/1 vs verifier other/praise/1: "Nice but I'm use resso 🙂"
- `056878eb-224f-46cc-9e9f-cd5d7c4544f9` enricher catalog/complaint/3 vs verifier billing/complaint/3: "If you dont have premium, spotify throws random stuff in your playlist, and you dont even get 6 skips per hour, it's like 1 or 2. Really bad."
- `05a04ad1-5036-424b-bb38-c648427a627a` enricher usability/complaint/2 vs verifier other/complaint/2: "ads ads and ads"
- `05b75fd8-3e1b-4977-ab05-45ec86b82324` enricher other/unclear/1 vs verifier other/complaint/2: "Hate this app because it's from sweeden"
- `05bfd429-d1c2-4fc8-ae7b-d89aa855554b` enricher other/cancellation/2 vs verifier other/cancellation/1: "Better options available, bye 😂"
- `05c51218-74c8-4092-aefd-b485d780300e` enricher playback/complaint/3 vs verifier other/complaint/2: "Just improve the bugs like not showing liked songs etc."
- `05dbe465-a887-4026-bcab-f0d8ac7c82be` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "It's reaching new low, everyday for non-premium users. Not gonna use it anymore!"
- `05f43393-19ab-406f-9a9f-7c00271f1f2f` enricher usability/complaint/3 vs verifier usability/complaint/2: "When i choose shuffle option, random songs playing in my playlist even when autoplay is off. I try to use yhe support and the language change. Where i suppose to complain?"
- `061206d3-d0ce-48df-93e7-32a3275104e0` enricher catalog/unclear/1 vs verifier other/unclear/1: "Her 1 song ke bad add"
- `06146502-b474-418b-beb8-5cca8e20cb25` enricher billing/complaint/3 vs verifier billing/cancellation/2: "For so long Spotify was free but then they don't give you skips and you can't listen to the songs you want sorry but this app has gone irritating I don't want to pay for premium"
- `062168fb-cdbf-4c8d-8880-479f0975953c` enricher usability/praise/1 vs verifier other/praise/1: "Best UI 🔥"
- `0643f021-3fb3-4b6f-a866-3ef0ecd68aa0` enricher other/praise/1 vs verifier other/unclear/1: "I am having a fantastic experience, as I just dropped my premium YouTube account to join with my Beloved."
- `064d4d1b-916a-4291-b0b2-2afd7cb784e1` enricher other/complaint/2 vs verifier usability/complaint/2: "New update is not good because due to inability of specific part option"
- `06986dcf-f935-4b36-aef4-4226075a08f4` enricher catalog/complaint/3 vs verifier usability/complaint/2: "Used to be good until a recent update, they added a feature where they will add songs into your playlist. I have to use my free 7 skips per hour to skip through these songs."
- `06b2d887-6ed8-49da-b01e-6b34fb613914` enricher catalog/praise/1 vs verifier other/praise/1: "Nice collections."
- `07564ba1-eb22-4e17-950b-d2aa824deaee` enricher other/request/2 vs verifier other/request/1: "Reverse your decision"
- `07574716-ef33-475d-aac9-839ea6a9eb54` enricher playback/complaint/3 vs verifier playback/complaint/2: "From many days the songs sound is not clear, every song sounds like an echo"
- `07959cdd-7861-4b2f-bb2f-fcfc5787335e` enricher usability/complaint/3 vs verifier usability/complaint/2: "has like all the kusic in the world, but have of your time listening to it will be ads. just use YouTube has less ads."
- `07a84d6b-adf4-44d5-b11e-15598cdd6ef5` enricher usability/cancellation/3 vs verifier usability/complaint/2: "App used to be good. But here recently ads have gotten completely out of control. I don't mind ads, but the ad to music ratio needs to be balanced significantly. "Enjoy the next thirty minutes of ad-f"
- `07f4fccf-dafa-4e94-896f-a81542b95f45` enricher usability/request/1 vs verifier usability/request/2: "Less adds PLEASEEEEEEE"
- `07f84395-3a7b-493b-b223-03049223bd66` enricher billing/complaint/3 vs verifier billing/complaint/4: "it's been days of me trying to buy a premium but it's always failed, i have called the support team many times. i did everything but still something's wrong TT"
- `085f566a-8bf7-4d8d-b18f-e1a0b5f2d582` enricher billing/complaint/3 vs verifier billing/complaint/2: "The hell is wrong with spotify....till ads it was understandable but now pay for listening to the favorite part of the song, is too much. Absolutely the worst update. Making us pay for basic needs."
- `0869d6c4-2079-4bc8-8594-94e6c55bb27b` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too many ads and it lies whenever it says that you can have thirty minutes of uninterrupted listening"
- `08a95031-ae90-400e-9603-acc03c8d86e1` enricher usability/complaint/3 vs verifier usability/complaint/2: "It keeps turning on shuffle, which completely ruins concept albums and carefully curated playlists"
- `08cc2913-dad4-44fc-895a-248dd9cfc746` enricher other/praise/1 vs verifier catalog/praise/1: "I rate this app good I can play so many songs"
- `08db560f-6d82-41b0-8732-c912c55d367c` enricher billing/complaint/2 vs verifier billing/complaint/3: "Auto shuffle has been update and loop after updating it asks premium"
- `08e9781a-09db-4ba9-b5d2-a321ca4e67a3` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too much ads and it keeps deleting songs."
- `08f37dce-0916-4581-915e-12bf97d366d0` enricher catalog/complaint/3 vs verifier playback/complaint/3: "When I'm trying to listen to my music it keeps changing to different music please fix this"
- `0970c545-1307-412a-8514-2e2f0a94de0d` enricher other/praise/1 vs verifier catalog/praise/1: "Very good listening to my favorite music"
- `098627bd-92a5-4482-8df7-5363511377b4` enricher other/unclear/1 vs verifier other/complaint/1: "Just another 1 star cause the other 5 star people forgot to remove theirs lol"
- `09887790-0c91-401f-941f-6e940f931afb` enricher usability/complaint/3 vs verifier usability/complaint/2: "Ad after every track. It means 3min track=1.5-2 min ad."
- `09a631ab-fe58-4f05-96e4-e996f8723bf8` enricher usability/complaint/2 vs verifier usability/complaint/3: "This new layout is TERRIBLE. IMPOSSIBLE to navigate. It's like car mode but all the time."
- `09a7560c-3cef-4826-a96e-0843703ac80c` enricher playback/complaint/3 vs verifier usability/complaint/3: "I have almost 800 songs but if I shuffle play, it only plays the same 30 songs over and over. Then the songs reset every time I close and reopen the app. So ridiculous"
- `09b7c833-d991-4642-b6c2-50f2ad41733f` enricher catalog/complaint/2 vs verifier other/complaint/2: "Está bn pero, cuando comparto las letras me salen muy separas y ya no puedo presumir mi buen gusto musical."
- `09e6c7a3-9637-4b25-a56c-4336ffd59f7f` enricher usability/praise/1 vs verifier other/praise/1: "Great sorce of music entertainment for free. Haven't had a single problem. Not many ads, it's great I love it."
- `09f36334-fcf5-4c03-9774-4811d6ac37df` enricher usability/complaint/3 vs verifier billing/complaint/3: "The worst app ever . This app shows ad before and after playing a song . Let i consider this is ok but whats the problem with skipping a song ? It shows only to buy premium when i play to any song . W"
- `09fc3044-eca4-4a6e-9c58-d6ece59fc8ef` enricher catalog/praise/1 vs verifier other/praise/1: "LITERALLY THE BEST APP EVER CAN FINALLY HEAR SONGS WITHOUT USING YT THANK YOU"
- `09fe20a0-45b2-4003-967f-1e9bea3633f6` enricher other/praise/1 vs verifier usability/praise/1: "Easy to use, stressless"
- `0a071e56-3e69-4e29-a9a3-29b351f53917` enricher other/praise/1 vs verifier catalog/praise/1: "The quality 😍 Spotify playlist has made my life easier!"
- `0a0bb987-7fd3-44e6-914b-5153108213d0` enricher other/complaint/2 vs verifier other/complaint/3: "Used to be a good app until they removed basic features"
- `0a1ddd8b-fc75-4a00-bb62-d761aec939f3` enricher catalog/complaint/2 vs verifier catalog/unclear/1: "4gen and 21st century helps allot but some of us are missing"
- `0a28d564-8c7b-4cd3-b242-e4fd7ef3e99e` enricher other/complaint/2 vs verifier other/complaint/1: "Boo... you know what you did"
- `0a322bb7-065d-4e22-a7cb-ac489ca34f1f` enricher usability/complaint/3 vs verifier usability/complaint/2: "I love Spotify with all my heart but why so many ads, I mean yeah there is Spotify prime but you can't give me ten ads meanwhile I'm trying to listen to my music."
- `0a437183-198d-4cb3-90b7-55a66c6768e6` enricher billing/cancellation/3 vs verifier billing/complaint/3: "This update distroyed the application Spotify removed the basic features. And made it premium should we listen to music freely or are you going to make it premium to Seriously distroing your own costu"
- `0a9a7425-f8be-4478-a60a-007fb58a231e` enricher access/complaint/4 vs verifier access/complaint/5: "Worst experience I'm unable to login with my phone number it says please check your phone number I purchased membership form this application but I can't login with the application what a critical sit"
- `0abb1d34-ffc8-4510-95ba-e0f8eeeb6dad` enricher other/praise/1 vs verifier other/unclear/1: "Wondèrfull app"
- `0ac53936-d660-4990-930b-159ceb593513` enricher playback/complaint/3 vs verifier usability/complaint/2: "It used to be a amazing app and I loved it. But now for some reason everytime I'd try to play one of my playlists it plays one of the songs in it and then a completely random one. I find it really ann"
- `0ad97750-b480-435f-9dd4-f33483f18138` enricher billing/request/2 vs verifier usability/request/1: ""Smart shuffle" does not need to be in the default rotation for the shuffle "button" make it optional or hold the button down or something"
- `0ae0a964-ab54-494b-b483-cfd90140bd25` enricher usability/complaint/2 vs verifier usability/praise/2: "Perfect app But some ads"
- `0b09cf47-1323-4434-952b-226055514dd8` enricher usability/complaint/3 vs verifier usability/complaint/2: "F**king app is this always iam getting ads for every 7to10 mins 😡"
- `0b6910d5-dc3c-4608-97fe-3489d0acf8af` enricher catalog/complaint/3 vs verifier usability/complaint/3: "I used to love the app but just recently I haven't been able to choose specific songs in my playlist I would just have to skip to that song. And every time I search a song and it pulls up I click on i"
- `0b71dd3a-2058-463c-a400-b4176d70b601` enricher usability/complaint/3 vs verifier usability/complaint/2: "On problem lying about 30 minutes of add free music when adds keep on coming after each song"
- `0b7d8ddf-2bf5-4026-91b6-631d6addd6b4` enricher other/complaint/1 vs verifier other/unclear/1: "Kick Pandora in the @$$!"
- `0baa7bab-8baf-41b5-b0ad-25356e15d527` enricher billing/complaint/3 vs verifier billing/complaint/2: "The free version is OK... kinda... hmmmm... It is clear all music companies want you to pay a fee for simple functionality enhancements. OH WELL, you get what you DON'T pay for."
- `0bda3019-e9ce-4fc6-ad4a-a29027becc6a` enricher usability/cancellation/4 vs verifier playback/cancellation/3: "I love this app, but when an ad popped up, the whole app froze and i couldnt open it so i had to uninstall it."
- `0bddc559-6890-4c52-8026-b4a1e1f54169` enricher catalog/complaint/2 vs verifier other/complaint/2: "It's a very bad app for songs😠"
- `0bfab716-7f23-4513-ba35-57de5da79c00` enricher other/complaint/2 vs verifier other/praise/1: "Yeah new update change everything but you have to use older version of this i using old version for long time 😀"
- `0c3d899e-0ef6-4146-acac-c7c830dfffe8` enricher billing/complaint/3 vs verifier billing/complaint/2: "The free version is just to make you buy the premium, showing an ad after every song. It's just annoying using this."
- `0c9685d4-de5d-45c3-ad3e-658f4383411f` enricher other/complaint/2 vs verifier other/cancellation/2: "This app always has some sort of issue. The only reason I don't switch is bc of my extensive Playlist which I can't bother with rebuild on a different platform but im get pretty close at this point"
- `0ce88bf8-4cf3-4797-b839-6bca00314224` enricher playback/complaint/3 vs verifier downloads/complaint/3: "Because you have to pay to use away from wfi"
- `0d1192f5-a23b-4af3-a241-f425ede20820` enricher usability/complaint/3 vs verifier usability/cancellation/3: "I just started using spotify not too long ago because all my friends used it and I wanted to know what it was all about I had a good experience with it until one of the most recent updates where you c"
- `0d13fb2f-9508-482a-9aa1-4e641016eef2` enricher usability/request/1 vs verifier usability/request/2: "Why can't you turn off shuffle or select songs on mobile"
- `0d1609b0-ebf2-423b-8723-1c1933e0bd2a` enricher usability/complaint/3 vs verifier billing/complaint/3: "Too many ads . We even can't rewind a song if we don't have premium very disappointed."
- `0d4c4eec-6942-4d47-b5df-fc7089d38709` enricher billing/cancellation/3 vs verifier other/cancellation/2: "I loved the app but the recent restrictions it has imposed, made it worst. Good bye spotify! Uninstalled. Switched to Wynk music."
- `0d710581-ee32-4aac-acdf-2e24ad581116` enricher downloads/complaint/2 vs verifier catalog/unclear/1: "Bekar hai download Nani hota hai son"
- `0d9eddff-2398-4ab9-8bee-97170f223c07` enricher usability/request/2 vs verifier other/request/1: "It's been great, only issue I have is not being able to see who likes my playlists. And that's really more just me wanting to know than an issue. Update* Would like to be able to make a blend without "
- `0dc45ff2-6ed0-4454-9f09-c74023108e1a` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "I m going to Uninstall this appa bcoz you are restricting listeners buttons aslo"
- `0ddf7fab-3389-4165-a9da-fb5d69b89d8e` enricher downloads/complaint/5 vs verifier downloads/complaint/4: "You app keep deleting my offline downloads....reason why I don't know....I'm paying for your so called premium but it doesn't feel like it"
- `0ded963b-445d-44ef-b421-bf09d9b395ed` enricher catalog/complaint/3 vs verifier usability/cancellation/3: "Paid member since 2013, ABSOLUTELY AWFUL app the last few years. Have no way to see all the recently released podcasts episodes from Web/PC App. UI now looks like they fired their product managers and"
- `0def6977-188d-4fa4-be17-e3b0d86eb2d2` enricher usability/complaint/3 vs verifier usability/cancellation/3: "Believe me or not i have been using this app for music for over 5 years now... if i were to listen any song this app would be it...the recent update just ruined the app u now can't even do basic thing"
- `0dfa7e17-3bdf-40c5-be76-89287e54df40` enricher billing/complaint/3 vs verifier usability/complaint/3: "I can't even rewind the songs now , it's a premium feature?? What the hell bruh Used to like this app It's very bad now How desperate are y'all to get money"
- `0e117fd9-a53c-4db6-b2de-769df815e6e5` enricher catalog/complaint/2 vs verifier catalog/request/1: "Where are dangal movie 's songs!"
- `0e1f7ed4-f5a2-440d-896e-d490247bf8f2` enricher usability/request/1 vs verifier usability/request/2: "Can u pls remove the ads it's so annoying"
- `0e26fff3-736f-4614-b7f2-a0f83443b724` enricher billing/complaint/3 vs verifier usability/complaint/3: "Hey sportify your new update is very bad I am unable to reply the songs and I think this is soo bad You have put many restrictions to non premium users and it is so disgusting 😭 please remove those re"
- `0e42b996-7bc3-4910-a7d1-bd488fb23c64` enricher usability/praise/1 vs verifier other/praise/1: "Love the custom playlists and quality"
- `0ea129b6-50ef-43a4-aa3d-0b2fa8241975` enricher usability/complaint/2 vs verifier catalog/complaint/2: "Adds in regional language is fine....and no need of suggesting other languages....feel irritating"
- `0ebcde6f-5139-4d21-81dd-127177f713d5` enricher billing/complaint/4 vs verifier usability/complaint/3: "Very bad experience!!!! They have changed many things... Now playing songs on Spotify is like headache.... the app which is made for listening music is not able to satisfy customers wish... no songs c"
- `0ef26dc1-e3c7-4c1c-85b5-81efaeb0efc1` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Ewwwwwww i choose spotify over other better apps w more perks coz i like the layout and all .. but imagine asking ussrs to pay for using the most basic features like repeat ? Are you for real ? I don'"
- `0f213d6f-aaea-4636-ada8-7b7f77e14b9a` enricher other/praise/1 vs verifier catalog/praise/1: "Best music online...... It's introduced me too lots of new music.... Couldn't live without Spotify......"
- `0f659a3d-c79f-4264-837e-e79cd1b650e8` enricher usability/complaint/3 vs verifier usability/complaint/2: "I love the app, I use it every day. PLEASE remove the sorting function on both Web and Mobile applications - it's retarded and it doesn't work properly!!! It's keep reorder all my playlists and folder"
- `0fbbb9a2-99bd-44fb-b72c-34071bad379a` enricher playback/complaint/3 vs verifier playback/complaint/2: "Some issues recently. Playlists get stuck."
- `0fc603a5-1542-4b5e-97e6-d50a731c2d51` enricher catalog/praise/1 vs verifier other/praise/1: "Great playlists 👌"
- `100b1414-586a-4222-a59f-1dd483978ae5` enricher catalog/complaint/4 vs verifier playback/complaint/3: "The app is a fault on its own...can't play certain songs...but rather it plays its own songs when you select a particular song...eg I'll try to play Micheal Jackson and it play another artist with a d"
- `1016417a-374a-4425-a8cd-1b12026cff5f` enricher usability/complaint/2 vs verifier other/complaint/2: "Ads only platform"
- `1026642f-b0d9-4636-81b3-7b3b7c0dc54c` enricher catalog/praise/1 vs verifier other/praise/1: "Does exactly what it says on the tin. Great for making playlists to suit all occasions."
- `103a88ce-7592-4dd5-888e-cb42345387f2` enricher support/praise/1 vs verifier other/praise/1: "Great service I love it keep doing what your doing"
- `103cf67a-5e31-4fbf-a68a-239f89375eec` enricher catalog/complaint/2 vs verifier billing/complaint/3: "it's good, but some of the lyrics are missing and the font has changed, so I think I should buy premium. But when it's premium it's the same, like a waste of money :(("
- `104205ca-e739-4bea-b22a-7c275f7bf0fa` enricher billing/praise/1 vs verifier other/praise/1: "Update 27/05/23 - I've been a Premium user now since October '21 and it has been an awesome ride of discovery and rediscovery across the musical spectrum for me! If you have the change, try out Spotif"
- `1045e27c-c254-41f5-90c3-746cba119273` enricher billing/complaint/5 vs verifier billing/complaint/4: "It's changed my premium plan to duo 3 times without me wanting it to"
- `1046a49d-b5a7-47e7-bee7-19951ccc98ab` enricher catalog/complaint/3 vs verifier catalog/request/3: "Hindi lyrics in English had made the app useless. Show lyrics in original language"
- `1050efc9-6bc1-44e7-a902-ba7248fd1d20` enricher other/complaint/3 vs verifier playback/complaint/2: "Spotify runs all the time and recently started taking over my phones audio and playing itself instead of my other running apps."
- `10c8677c-6011-4805-a956-b79fa61a214a` enricher other/praise/1 vs verifier billing/praise/1: "Love it!! Premium is amazinggg. The free version is a little annoying but the premium is definitely worth the money!!!"
- `10f553eb-e386-4994-a3bd-ac4850415367` enricher billing/complaint/3 vs verifier billing/cancellation/3: "Do not install the🚫🚫❌ spotify ❌. Now it is limited to premium version only . After new features we can not access the artist playlist it gives us preview option option to free spotify users now we can"
- `1101ce90-d863-43f9-b822-68915b211433` enricher billing/complaint/3 vs verifier usability/complaint/2: "I love Spotify but when I want to reverse it, it doesn't let me. I recommend if you want to listen to good music. And also, multiple different types of songs, plus there are lyrics to most if they are"
- `11508fa9-1e7a-4b5d-a3aa-40169046dfe5` enricher usability/complaint/3 vs verifier usability/complaint/2: "It's an alright app, can be buggy and I'm getting sick of the smart shuffle. I wish there was a way to not have it as an option plus even when I don't have it on, Spotify keeps adding random songs int"
- `11653a1a-660a-4b1e-a2bd-a1f0a1fac100` enricher other/complaint/2 vs verifier other/unclear/1: "Is this really a song listening app??"
- `11705670-6b82-4728-9bec-164138ce5a99` enricher billing/complaint/2 vs verifier billing/complaint/3: "Idk why you have to pay money for all essential tools like going back to your last song, or repeating the song on mobile, this is why I don't like spotify"
- `1187d87a-0e2d-4a2d-a64f-61456fae67cc` enricher usability/complaint/2 vs verifier other/complaint/2: "Only for advertising"
- `11b7b07d-c5eb-4652-a562-7f54f91fb7d0` enricher billing/cancellation/3 vs verifier billing/complaint/3: "You know . I love listening to podcasts and songs on Spotify . But u canges the things that were there before . We can't even change the order and revind the song for that we have to take premium. It'"
- `11d5094b-ba09-468b-9655-80866efd91fa` enricher billing/complaint/3 vs verifier billing/request/3: "Không thể hủy gói premium hiện tại để chuyển sang gói khác được"
- `11f0ba03-3a8c-4553-9b7f-5a0cee032ad8` enricher billing/complaint/3 vs verifier usability/complaint/2: "It have remove the basic features"
- `121defbd-9765-4a0b-be09-5b7b364ec9d1` enricher catalog/complaint/4 vs verifier usability/complaint/3: "Ads everywhere and the never play what's actually on a play list, it jumps to radio and plays none of your music. Get used to never listening to what you tap on unless you doule out money."
- `124a5839-fd2d-426b-abc0-de0559e82148` enricher usability/cancellation/3 vs verifier usability/complaint/3: "Worst music app After update you can't listen a song on loop And can't forward or backward Don't use this app"
- `1295b29d-d772-42c7-b261-10b3a68b9704` enricher downloads/complaint/2 vs verifier usability/request/2: "Great. Though I wish local on phones was easier to use."
- `12ed4c61-6bbf-40aa-80b0-5af675a9530c` enricher other/complaint/3 vs verifier other/complaint/2: "I'm just sad 0 star isnt an option The new update truly sucks and for me its buggy as well C-C"
- `12f5d0be-9b66-4fbc-ab07-c28768452191` enricher usability/complaint/3 vs verifier usability/complaint/2: "Ads are good but songs intrupting again again 😑"
- `1314b05c-a42b-43cb-8d73-306375522742` enricher billing/complaint/3 vs verifier usability/complaint/2: "Spotify is becoming worst day by day they are literally taking charges of song to repeat 🤬 worst app."
- `13585897-d36a-4eed-b80e-ce714c3b9972` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "This is the reason why I use apple music, everytime I try to listen to my fav songs it keeps shuffling random music that isn't even my taste, Spotify fix your app!! 😕"
- `1366116a-d566-41ce-b8a5-fa5ed7169833` enricher playback/complaint/4 vs verifier playback/complaint/3: "Pause automatically on my s21 ultra all the time. Unusable."
- `137e3e4f-9d7d-40f0-90b3-785d348be628` enricher other/complaint/2 vs verifier catalog/complaint/2: "Fake app copy right songs please don't download"
- `1390163a-f311-4957-802f-acbdde38ebcc` enricher catalog/complaint/3 vs verifier usability/complaint/3: "The new update is very frustrating I can't even view the lyrics also"
- `139f6006-efba-4b40-9ffe-634c48b00f8c` enricher other/complaint/2 vs verifier other/unclear/1: "Just following the trend."
- `13b94f13-59f6-45a2-a89c-70fdc6164015` enricher other/praise/1 vs verifier playback/praise/1: "Excellent I listen to music maybe 6 hours a day the quality is great and I have found so much entertainment I was missing before spotify the only streaming. Service I use"
- `13e0c0b1-461f-43f3-9202-3668e4124dfd` enricher usability/complaint/2 vs verifier usability/complaint/3: "The new interface is bad. They replaced the useful shortcuts from the home screen, with an Instagram style feed, which auto plays. I can't understand how this benefits users."
- `1419b685-0275-4548-817a-be77e042e8b2` enricher other/complaint/2 vs verifier other/unclear/1: "Its west of time"
- `14296838-81fb-4a5e-81e9-779dede786bb` enricher other/complaint/2 vs verifier downloads/complaint/2: "Very very very very bad app don't download if you download then you waste this app your data"
- `145faaac-92d1-4887-a564-ff6e4aa4b306` enricher playback/complaint/4 vs verifier playback/cancellation/3: "The new update (or lack of) with Android 13 is making the listening experience terrible. The music slows down and then speeds up. It cuts off or doesn't play music even if the playlists are downloaded"
- `14706ce6-221d-4e14-8a47-f6823404699f` enricher billing/complaint/3 vs verifier billing/complaint/2: "The day is not far when we have to purchase Premium just to listen songs"
- `1483bd6f-a381-4df6-89b8-bcd44cf0e0a7` enricher other/cancellation/2 vs verifier other/complaint/2: "Disgusting after the update. Switched to another app!"
- `14c6afef-62c5-4536-8a76-ff5d63b9a9a5` enricher other/praise/1 vs verifier billing/praise/1: "Absolutely amazing once you have premium"
- `14db0353-25c0-44dc-bfe0-9bdf3a2cc21b` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Generally a good app for listening to songs and stuff but having a song from other language getting suggested or played on the mix randomly is quite an annoyance and there's no option to block certain"
- `14e820ba-a3a8-4a7c-b632-72f0fc5a7e2b` enricher access/complaint/4 vs verifier access/complaint/3: "Bad experience login problem"
- `14eb257f-7d2a-4245-8c75-99be7011950c` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Was my fav music listening app. Now, it wants me to get premium for every little thing. I don't need Spotify if I have to pay for listening to a particular part or to see the lyrics. It's literally be"
- `14faa546-02cf-4c49-8958-35f9af0a8e0f` enricher catalog/praise/1 vs verifier billing/praise/1: "Better than the other satellite radio station offered. I like that you can customize your music. I have the premium subscription with no advertising great option.-"
- `14ff3e75-e6fc-41e6-9b3f-4d67ff55cd63` enricher downloads/complaint/4 vs verifier usability/complaint/3: "Playlist of liked songs is not opening 😟😟"
- `150f6e1b-34fc-4ba0-8c84-905ab957b758` enricher billing/complaint/2 vs verifier billing/cancellation/3: "I liked this app earlier bt now due to premium policy...it irritates me a lot...so yah don't download this app not worth it now"
- `151ad35c-9942-4452-bd9b-fa7d9094425c` enricher usability/complaint/3 vs verifier usability/complaint/2: "Ufff ...tired off can't tolerate the advertisements"
- `1593aac7-dd7a-4342-9faa-75df9a36bdb5` enricher other/praise/1 vs verifier other/unclear/1: "It's Friday time to dance n party right?"
- `159a6ccb-4545-4d10-b1ed-7d1cb01390bb` enricher usability/complaint/3 vs verifier usability/complaint/2: "One of worst app shows advertisment after every 2songs"
- `163c1297-1599-49c6-9e5e-2fdcbc9f532f` enricher billing/complaint/3 vs verifier usability/complaint/3: "Stripped of all the basic features. I mean I can't even play my playlist in order cant navigate to a specific part of the song!"
- `1682d31f-c1e4-4bc0-af3a-e220c549f202` enricher other/complaint/2 vs verifier other/unclear/1: "Otha Poda Mairu"
- `16be783f-7fe7-4d87-8f5b-7c5f862dd532` enricher catalog/request/2 vs verifier usability/request/2: "Spotify has been good so far with premium, but recently it has started translating the Japanese names of the songs on my playlist to English and Romaji which makes it very difficult to find songs I us"
- `1734d29e-3940-4ba5-a626-5de1166f63d0` enricher usability/complaint/2 vs verifier other/praise/1: "Best app to hear adds ."
- `173a3087-11b1-4627-8ff5-78960d3e420b` enricher billing/request/2 vs verifier billing/complaint/2: "Could be cheaper"
- `1752bd0f-20b9-4910-90b8-d77b26861d3c` enricher usability/complaint/3 vs verifier usability/cancellation/3: "It's really annoying that you can't select a song to play. That you are only allowed to shuffle your liked songs. That wouldn't be so bad if they didn't limit the skips! What's the point of making a l"
- `17d9a646-b328-48f7-816d-7589b3f090f8` enricher other/unclear/1 vs verifier other/praise/1: "Idk Spotify just needed a 5 * review"
- `1810e38c-d46e-4480-ab9e-e3a0214b0118` enricher billing/cancellation/2 vs verifier billing/complaint/2: "You are asking premium for every damn thing you better change it or you are soon gonna lose your fame and hit the rock bottom"
- `183d31b8-62e8-41b2-a634-31adc59d8d75` enricher catalog/praise/1 vs verifier other/praise/1: "Love Spotify there are limitless options for music and I love the old time radio shows"
- `1848a209-e91d-4d9d-aa39-b3842e2dddc5` enricher usability/request/2 vs verifier usability/request/1: "I wish you can use the "custom order" for playlists, like my ocd is so mad at that AND why can we separate the playlists made my other users then just "by you" or "by Spotify""
- `18500efa-d08f-4468-85f9-23851c64b238` enricher catalog/praise/1 vs verifier other/praise/1: "I love this app so far. I am able to listen to podcast and the best music old and current."
- `186a76dd-5890-4dca-a954-cd2e9a6c3be9` enricher other/praise/1 vs verifier downloads/praise/1: "Enjoyable and you can create your own Playlist and download to listen offline.😍😍😍"
- `18837295-4e7a-493a-ae54-9dd3ee08ad6e` enricher billing/request/1 vs verifier downloads/request/1: "CAN SOMEBODY PLEASE, PLEASE, PLEASE, PLEASE THAT KNOWS HOW ADD "FREE, BY U.P.O" ON SPOTIFY?????? And can ya'll please make spotify transferable to a SD card????"
- `18947035-4635-4789-b486-82004e8f8e37` enricher usability/complaint/2 vs verifier usability/complaint/3: "Bhaiya aisa hai baki sb to badhiya hai single ad tk bhi thik tha , lekin ab jo ye ad ka pitara khol de rhe na aur skip bhi nhi kr skte, wo bakwas hai . is mamle me Resso badhiya application hai . kam "
- `18fc416a-cbcb-4d74-afce-09bae8decbe2` enricher catalog/praise/1 vs verifier other/praise/1: "Brilliant selection rarely had issues and well worth the money"
- `190003d3-b78f-4f73-b636-7c96e4386adc` enricher billing/complaint/2 vs verifier catalog/complaint/2: "3 stars on mobile. Best on PC 4 stars As always, PC Master race. You can skip songs listen to anything anytime without premium. Only on pc. If you buy this, buy it on pc. 1 star is gone because they r"
- `190d9352-12ba-466e-821e-14828d8d86a3` enricher other/unclear/1 vs verifier other/complaint/2: "Policing people."
- `19806b13-c358-47f8-a711-866c1153d7d3` enricher catalog/praise/1 vs verifier other/praise/1: "Very good collection of songs"
- `19879b4f-e4d3-4874-b668-897b08e0bfa8` enricher billing/complaint/3 vs verifier billing/complaint/5: "To get premium you need to pay even when you payed for the app."
- `1988442f-820b-45d6-9ff9-848b96f54463` enricher catalog/request/1 vs verifier other/request/1: "Please add hellotone option in this app 🥺"
- `19bd0b41-437a-4837-b6b3-2b5251f9dddc` enricher support/complaint/4 vs verifier access/complaint/4: "Update: after 2 weeks and about a million emails back and forth with a new customer service rep every hour, they told me the problem is my device not not app (the problem is definitely the app, this d"
- `19c1b642-74c5-4db1-b0de-2921d97ff8e1` enricher playback/complaint/3 vs verifier usability/complaint/2: "Pretty good app. Does everything I want in an easy-to-use way that is intuitive to navigate. Can't think of any features to ask for that aren't already available. Edit: just thought of one. The shuffl"
- `19da7278-4720-42f4-ba49-a3a90e7c7415` enricher other/complaint/2 vs verifier other/cancellation/2: "Its terrible, i suggest you use youtube music, at first i thought it was great but once you have it for a while it gets annoying. Also the last few updates have been horrible. I think that not being a"
- `1a08d8f4-a3e1-4236-bc56-9506ff2ecc1e` enricher usability/praise/1 vs verifier catalog/praise/1: "Very easy to use; can find any song you like."
- `1a0d06d9-a075-4fdd-b809-bffa903a8468` enricher usability/praise/1 vs verifier catalog/praise/1: "Nice app for all types of song.Less advertising..Song quality good"
- `1a17fbf1-831c-49d7-9876-f214f8f061fd` enricher usability/praise/1 vs verifier other/praise/1: "New member, but it's great. Fun creating my play lists!"
- `1a3c91bd-f742-4b68-a7cd-345a2f7e580a` enricher billing/complaint/2 vs verifier other/complaint/2: "Begging money all the time"
- `1a4b1750-0433-465a-bf0b-6949c8e66ca0` enricher billing/praise/1 vs verifier other/praise/1: "Really good app for music lovers and its free :) . Worth the money if you love music and get tired of ads!!"
- `1af1ada5-96a9-4592-8801-c9f65b19554c` enricher downloads/complaint/3 vs verifier usability/complaint/3: "Recent upgrades have been annoying. 1. Can't access my liked songs playlist when offline. 2. Removed scroll bar in playlists. 3. Let the search bar be visible by default, I know you can pull down to r"
- `1b3094c7-088b-419d-9076-7ef276c4a9a5` enricher access/complaint/4 vs verifier access/unclear/1: "I'm not logging in 😶🍷"
- `1b447a22-75e4-4e1e-a3b7-c983d56bf88e` enricher other/cancellation/2 vs verifier other/cancellation/1: "Uninstalled successfully as new update was too good and listeners friendly that u know guys.... And I can't handle that much love from Spotify... So, TaTA ByE bye ......"
- `1b72ced4-e0d7-4d0d-9589-e016c4b02bd7` enricher other/praise/1 vs verifier other/unclear/1: "😜👌👌"
- `1ba6d7fe-48f2-4523-91dd-7b1b0fc1805f` enricher other/praise/1 vs verifier other/unclear/1: "Noice..."
- `1c0165ea-cee7-41d9-a3bb-060543e7cd08` enricher playback/complaint/3 vs verifier playback/complaint/2: "video podcasts don't show videos when they are playing and canvas don't show up"
- `1c1b4447-0d6f-4e12-95f3-84f9c3738a71` enricher catalog/praise/1 vs verifier other/praise/1: "it's a great app. I love the fact that it offers different genres of music"
- `1c438cd9-eb51-45cf-a627-5740ddbe5d2e` enricher usability/complaint/2 vs verifier other/praise/1: "The free version has commercials, but so what? Good content and easy to use. The five stars are for the free version; I don't know about the subscriptions."
- `1c532235-c66b-4d6f-aceb-f02146c3b5fe` enricher playback/complaint/3 vs verifier usability/complaint/2: "until they fix the issue where the app opens in the foreground or background when you connect a BT headset i will keep my 1 star. its the most annoying part of this app. otherwise everything is good. "
- `1c6bd067-8daa-45b2-a5dd-5cb44f1b8a0f` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "Very disappointed I cannot download mp3 even with Premium... Shame"
- `1c99659d-4eb4-4139-94b9-07f439a99f55` enricher catalog/praise/1 vs verifier other/praise/1: "Love this app,,,the podcasts,,,dope💯💯"
- `1d14d489-b989-4854-bed6-0564d41e86ef` enricher playback/complaint/3 vs verifier playback/praise/1: "I used to love this app, but the past month it has been a train wreck. I don't know if a update screwed it up or what, but I have no control over it anymore. It keeps pausing/unpausing songs, skipping"
- `1d32e11e-53dd-4633-a7da-bda8b3a89c17` enricher usability/complaint/2 vs verifier other/praise/1: "Ads are annoying but it's a great free service for music fans ,Can purchase ad free at a price"
- `1d999823-6ede-4265-9595-66ca9f5a8f54` enricher billing/complaint/3 vs verifier usability/cancellation/3: "The app was use to be wonderful until the lastest updated come. Literally the app is forcing us to listen to music it want to . I am disappointed with it . this app was used to be my friends because o"
- `1d9a392d-72f5-4d92-abad-480ec9f56ebe` enricher usability/complaint/3 vs verifier usability/complaint/2: "The music quality of this app is great👌 but there was so many interrupted ads between songs without subscription....app promises to listen music for 30 minutes after ads but fails in that🥵"
- `1de72706-9826-4355-978c-39d63c8d753d` enricher usability/praise/1 vs verifier other/praise/1: "Without ads Spotify easily 5 stars"
- `1e11b0d3-9888-45b2-bb6a-789e843796bb` enricher catalog/praise/1 vs verifier other/praise/1: "I love that I can listen to a boat full of music! It's a good medium of music!"
- `1e6f20e2-d032-4867-ba5d-b1819a06715a` enricher billing/complaint/3 vs verifier usability/complaint/2: "Yo believe me I love Spotify and every artist who's music has been put here but without Premium, is the experience really fun? You can't skip like 3 songs without Spotify giving you a 30 second ad ☠️☠"
- `1e90ca41-057e-4c4b-8ace-208794ad19af` enricher other/cancellation/2 vs verifier billing/cancellation/2: "Worst app. Total waste. Uninstalled it. Just a music app with sooooo many restrictions. Better to opt for a simple app for music. Totally waste product."
- `1eb6e337-6db8-4e31-ae33-cd47324f95dc` enricher usability/praise/1 vs verifier other/praise/1: "No addes are their. All type of songs are available. Easy to control."
- `1ed281fc-7181-4660-a355-1d657f9a4073` enricher other/unclear/1 vs verifier other/cancellation/1: "Every Muslim has to completely boycott the brand and app of Sweden because they have disrespected our holy book. The people of Sweden have given us hatred for us in return of our love"
- `1eee0627-1254-4f7f-9a3b-535d0a60d528` enricher billing/cancellation/3 vs verifier playback/cancellation/3: "50/50 on this, I've been using Spotify for years, have paid for many of those years, however the last 6 months or so no matter my device or if I uninstall and reinstall, if my device screen shuts off "
- `1f1a58e3-a80e-4c7e-aad4-211522129325` enricher catalog/complaint/2 vs verifier usability/complaint/2: "they keep adding weird songs I hate to my full playlist and I hate it"
- `1f2ceada-2bb9-4fb5-98df-544f7afb9dac` enricher playback/complaint/3 vs verifier downloads/complaint/3: "My liked songs are not loading at all but other albums are loading"
- `1f391495-7124-44a1-b070-92a7575fa888` enricher catalog/praise/1 vs verifier other/praise/1: "It very nice,, l can get the song l want to,,"
- `1f474875-95f4-41ad-87e3-02ecd3acc3e8` enricher billing/complaint/2 vs verifier billing/unclear/1: "Good if Free"
- `1f64b63b-a10f-4c19-8eae-628331bf5357` enricher usability/complaint/3 vs verifier usability/complaint/2: "Playing ads after every song."
- `1f93610f-c737-4e79-818f-e4db85bab7eb` enricher usability/complaint/3 vs verifier usability/complaint/2: "There was an add about a hard tea with alcohol in it and I would get five adds at a time and watch add would be that same one over and over again and I would the these same five adds every 5 minutes l"
- `1fe189ac-e9d1-4f40-9cf1-2db5d3e80d1b` enricher other/complaint/2 vs verifier usability/complaint/3: "this remove basic feacture"
- `1fe8b029-f38f-4525-a94c-04623c0fd9b2` enricher billing/complaint/3 vs verifier billing/complaint/2: "love the accessibility to your music choice unlike many other platforms buh the restrictions in order to make one use the premium mode is way too much."
- `1fe9b37a-b20b-4539-9347-7e41176a6058` enricher other/praise/1 vs verifier usability/praise/1: "I really love that it's synced across all devices I'm using over the YouTube music"
- `1ffafd76-bbd0-4fac-9fd6-0a8a477c9882` enricher downloads/complaint/3 vs verifier playback/complaint/3: "Constantly crashes and takes a really long time just to show the list of downloads"
- `20325171-5b5d-4a2a-af68-1d08269434b1` enricher usability/complaint/4 vs verifier usability/cancellation/3: "The newest update has made me consider downloading a different music streaming app. Not only are the ads after practically every song, but now you can't even listen to a preview of the songs out of yo"
- `2045d3e3-9df6-4416-94b1-dd0e3cf878a3` enricher other/praise/1 vs verifier catalog/praise/1: "It is a very useful app for all types songs"
- `206b8667-5858-430f-8d75-1658cab512e3` enricher other/cancellation/2 vs verifier other/complaint/2: "You are a swedish brand and as far as o know, everyone from Muslim world would ban you"
- `20819770-27ce-4bee-8cbd-42e4e7f69c6c` enricher catalog/complaint/3 vs verifier usability/complaint/2: "I would give it a five but it always forcefully plays song that I didn't add and that I don't like and it doesn't let you listen with no wifi, but it works with premium? That's a kind of thing that sh"
- `209d7242-bd9d-4ddb-9e97-c9c725aa9a37` enricher usability/unclear/2 vs verifier usability/complaint/2: "What did you do with the CLEAR QUE button?"
- `20dba2f1-f4ae-4ed0-af5b-040b3ef811d3` enricher other/unclear/1 vs verifier other/request/1: "Ya pongan a Julión"
- `21010400-aa9e-4656-83ac-6c001092091c` enricher other/complaint/2 vs verifier other/unclear/1: "Baper mb paisa iman bhikhari amar classor bishale nohe ahun jiman😤"
- `210a417e-a68b-4b64-82b1-521cc959761a` enricher other/unclear/1 vs verifier other/praise/1: "Boom 💥"
- `2162b151-1ff9-4d23-b9c9-782410adcd28` enricher billing/complaint/3 vs verifier billing/complaint/2: "Literally everything needs a subscription a day will come when premium is required to play songs"
- `21863b5f-4096-4def-80db-4d5e9a04a60d` enricher playback/complaint/4 vs verifier playback/complaint/3: "I wish I could rate this app 0 stars. I swear with each update it gets worse. It used to be it only messed up when it wasn't on shuffle, if the app wasn't used for 10 minutes or more and then started "
- `219c5142-ea97-4e07-9741-0b34b2932967` enricher billing/complaint/3 vs verifier usability/complaint/2: "You cant pick a specific song it has to be random and you get bombarded by ads even before the ad free 30 minutes is up UNLESS YOU GET PREMIUM. If youtube musice would let you play it in the backround"
- `21dbefdc-5a2a-4999-866f-a7106971a85d` enricher other/praise/1 vs verifier catalog/praise/1: "Good quality music."
- `21ee5310-78b8-45cf-b88a-65c923159077` enricher billing/complaint/3 vs verifier billing/complaint/2: "In starting it will be good .. after using more... U get tensed with add and restrictions as it says to get premium"
- `220a75c7-9957-4fd7-aeaa-4eb0920bea05` enricher billing/complaint/3 vs verifier usability/complaint/2: "Spotify has destroyed everything now there is no more feelings when you listen to the music. Almost everything has become paid no more choosing which song u want to listen aur change playlists on ur o"
- `22a3e968-97de-4001-9fed-714212c80a7d` enricher other/praise/1 vs verifier catalog/praise/1: "It is so good and has so many grate songs and I have learned so many new songs that I now love!!!!"
- `22c2184b-c70b-4bc8-8691-dc9e229f4288` enricher other/praise/1 vs verifier other/unclear/1: "Nice app otp"
- `22e90755-12a2-40c8-a293-15357ba95a72` enricher playback/complaint/4 vs verifier usability/complaint/3: "This app is beyond garbage. Looking for a song? Sorry thats a Playlist. Click an artist to see their songs or albums? Sorry, only the top 5 songs. The ads are almost every song and when it says you ge"
- `2311dfc2-1201-4127-8614-7fe4642caf88` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Honestly it shouldn't be that hard to not play random songs I've never listened to in my playlist. No, I'm not talking about the "We added" the random songs that come out of nowhere to where you can't"
- `23430a85-b6e0-406f-b877-0b5bb68c0bd5` enricher billing/complaint/2 vs verifier billing/complaint/3: "Spotify just wants money bruh everything is in premium not all most of them please remove: 6 song a day feature and backward lock favourite line And any one seeing this delete Spotify and those who ar"
- `23806404-fdc5-4093-9a01-90331be3cbe6` enricher usability/complaint/3 vs verifier billing/complaint/3: "Ads about removing ads gtfo, Even after paying $12 you are serving adson podcast"
- `23ccf6e0-d9c3-4474-8916-8e671cbb66f2` enricher catalog/praise/1 vs verifier other/praise/1: "Very rich music app."
- `23de3155-1e6a-4c66-81bd-f3db25a637d2` enricher playback/complaint/3 vs verifier playback/complaint/2: "Very bad application, sound quality other song, other features it's very bad👎👎😔😔"
- `240107a0-9d66-410f-aced-f7f9d81f7d2d` enricher usability/complaint/2 vs verifier catalog/praise/1: "Does everything I ask worth the $ The Community capabilites of this app is so huge it is very amazing I really enjoy how Spotify is always upgrading and the amount of music is insane Shuffle play coul"
- `242a9fda-2fd8-47bc-a19e-554dd1a5efa7` enricher other/unclear/1 vs verifier other/complaint/2: "Future is not good"
- `244610bd-d6ff-4029-baeb-ff9deeb4a47e` enricher playback/complaint/3 vs verifier downloads/complaint/3: "Setiap mau update subscription gk bisa pakai data bisanya update subscription kalau pakai wifi, padahal kuota masih banyak dan sinyalnya kenceng"
- `2455d71e-a38b-4062-bda8-440f108a8f0f` enricher usability/complaint/3 vs verifier billing/praise/1: "Awesome other than getting 3-6 consecutive ads without premium"
- `246d2f78-220e-4e68-8d0b-d445ced5d010` enricher billing/complaint/3 vs verifier billing/complaint/2: "Spotify is going worse than ever because of the premium and now they are also asking premium for playing previous song 😡🤬🤬"
- `248121a4-5584-4d29-be24-b46507c324e7` enricher playback/complaint/4 vs verifier playback/complaint/3: "Very very bad , used it for less than 1 hour...it goes off after a few seconds."
- `24b5944d-0aa2-47dc-bcd6-cabf00fd8af3` enricher other/praise/1 vs verifier other/unclear/1: "ॐ नमः शिवाय ॐ"
- `24bf8979-f9ef-435f-b602-3ce15364f62c` enricher catalog/praise/1 vs verifier other/praise/1: "Outside of mixtapes, they are my comfort."
- `24d09fb7-2d02-4bda-b42a-3c8c93bb6fd1` enricher other/praise/1 vs verifier other/unclear/1: "Spotify DEVELOPMENT TEAM "SPOT ON" 😉💯🤘$$!"
- `25361260-0c87-4aa8-9218-6c62ff792280` enricher other/unclear/1 vs verifier other/complaint/2: "Spotify line is better then aoptify"
- `25a04727-c3ca-4706-9061-e81b613264ab` enricher usability/complaint/2 vs verifier usability/request/1: "Always fresh new music being added. My only complaint is the lack of customization for the widget."
- `25d28152-46bb-4046-8ead-904478fbfa05` enricher other/cancellation/2 vs verifier other/complaint/2: "This is the world useless app this bad app I recommend to you not use this app please"
- `25e7b8a8-40ba-4e39-9be4-715187badd2e` enricher catalog/complaint/4 vs verifier catalog/complaint/3: "Most of the songs are not able to play. App show the message " not available" for example bang bang, and tu meri."
- `26263fd4-8542-4d54-83e6-720f19db7476` enricher usability/praise/2 vs verifier billing/praise/2: "Liked songs Playlist is back. Yayy!!! Just love the app. Also pl try n fix on buying subscription it gets stuck."
- `26378cd4-b9c6-4dd6-bcc1-66d8eb600af2` enricher other/request/1 vs verifier usability/complaint/2: "I cant share lyrics in Instagram."
- `26a54045-7a85-4aba-aab5-735baeef57e0` enricher catalog/praise/1 vs verifier other/praise/1: "All song super"
- `26aefdd3-60c9-4413-b584-e5ca36fdf88b` enricher other/unclear/1 vs verifier other/complaint/2: "Use other options"
- `26c9217b-bb60-42de-8bf9-e151dec29ed9` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "New movies songs are not available 😞even old also"
- `271017e6-e451-4966-8ccb-842e4c8ae365` enricher usability/complaint/3 vs verifier usability/cancellation/3: "It was my most favourite music app. But after the latest update I can't even rewind a song which irritates a lot. Even there is no longer loop feature. This really disappoints for many. Atleast let us"
- `27173e8e-560e-4b4e-95c3-81cd807d49c6` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "Two ads back to back not good....uninstalled"
- `2784084e-4e1e-4403-8d67-91b5fdc3723b` enricher usability/complaint/3 vs verifier usability/request/2: "Unreliable updates and changes. Please add useful features like pausing my randomized playlist, switching to another playlist and then jumping back into my randomized playlist without restarting the r"
- `279869d9-4103-418a-914c-0b5cdfbedc7d` enricher usability/complaint/3 vs verifier downloads/complaint/2: "What happened to my liked song playlist?"
- `27bfa8e6-4393-4f56-ba8a-5b3379ef5bd5` enricher catalog/request/2 vs verifier usability/request/2: "Well i have give 4 Star because some of songs are really irritated but we don't get block option to them so make update on it"
- `28124287-e59a-473d-8ad4-cb09ec350cf1` enricher billing/complaint/3 vs verifier other/complaint/2: "It's better of old update version"
- `28270801-e9b5-4b80-9f8a-99fed549f181` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Is not bad, really. I mean, sure, if I wanna listen to stuff on loop via playlist, it will add other things to the mix. Not to mention the lack of a loop button on mobile. But, it's really good, and I"
- `28352ad7-bd2b-4f1e-a2bd-e993fa6f54c6` enricher billing/praise/1 vs verifier catalog/praise/1: "This app is free for song. And also, best for songs."
- `284e27a0-4dce-4af1-934f-970a9aaf76e0` enricher access/request/4 vs verifier access/complaint/4: "I need help I logged out my account. I try to re-login using my phone no. but the otp option is not coming only message in the app that try using another number. I have tried deleting and re installin"
- `28b6bf66-2316-443f-b34a-661456ad4ffc` enricher other/unclear/1 vs verifier other/praise/1: "I'm artist And Spotify 👍"
- `28cdd6f2-0bbf-4577-89ec-4ab9ff881239` enricher catalog/complaint/3 vs verifier usability/complaint/3: "A have a lot of problems with it but the most important is the fact that I can't search up a song and play it on its own without listening the that specific whole album. And if you try selecting the a"
- `28e1a541-37a8-4de9-8eb7-d14fc19c588b` enricher downloads/request/2 vs verifier downloads/unclear/1: "Just make the app download with a fee as well... 🙃🙂"
- `290cb6e1-5b32-4f3c-a5d5-6d3449d37b4f` enricher other/praise/1 vs verifier usability/praise/1: "I like how I can pick my own music"
- `29389fe5-acdc-4f90-bd75-009cb461b1a7` enricher catalog/praise/1 vs verifier other/praise/1: "A home of good music with a great experience."
- `293d0e43-af90-479b-9505-4d8da2687969` enricher other/praise/1 vs verifier other/unclear/1: "Ok it's nice to here"
- `29464f12-6ce9-441c-8cc5-e807f18c91d9` enricher playback/complaint/2 vs verifier usability/complaint/2: "I love it but more skips"
- `295e5793-e19d-4714-bc15-690a5507ad6a` enricher playback/complaint/4 vs verifier playback/cancellation/3: "It stops playing my music when I leave the app. How am I supposed to use it if it doesn't work? I also timed the "30 minutes of ad-free music" it gave me and it lasted TEN MINUTES AND 22 SECONDS BEFOR"
- `29b71334-e583-4c1c-94c9-d4d9e3e25619` enricher usability/complaint/2 vs verifier other/complaint/2: "It's Amazing to listen but, The update, I hate it!"
- `2a07eda5-eb7b-471a-a693-52a65f6b5963` enricher usability/complaint/3 vs verifier playback/complaint/2: "Spotify is a very good app. In the app I can listen to different songs like my choice but one problem is that there are a lot of ads here. 😐And here when I turn on a song and go to another app, the so"
- `2a123213-83f5-4b0f-a3e8-29ddee56569e` enricher other/complaint/2 vs verifier other/unclear/1: "misleading"
- `2a2ffb7f-5bb8-4b56-9d6d-bb7b106ada7c` enricher playback/complaint/3 vs verifier usability/complaint/3: "I'm not able to glide the songs on this app . Unable to rewind my fav part of the song .pls fix the bug spotify."
- `2a327aab-3c95-478b-a6f8-ed516acca6e3` enricher usability/complaint/3 vs verifier other/complaint/2: "TLDR; Since march or april 2023, Spotify embedds TikTok / Youtube reel like Videos, and won't allow deactivating it for our family plan to protect our minors I'm on a family plan and spotify paid sub "
- `2a39721d-5d49-4d9c-9616-b6b215029386` enricher catalog/praise/1 vs verifier other/praise/1: "Just amazing,the whole musical world at your feet!"
- `2aa1c0b5-7962-42ce-b39c-a0a6327d4369` enricher usability/complaint/3 vs verifier usability/complaint/2: "so many ads, I love the shuffle but I can't listen the song while having mental breakdown. :// I'll just give 3 stars"
- `2ab2124c-9e60-4364-9e46-31aa7e9acefc` enricher usability/complaint/3 vs verifier usability/complaint/2: "Dude. The adds are way too loud. You're gunna break my stereo and my hearing. Fix it."
- `2b0d24e3-db9b-4e5f-80f1-f097362675af` enricher other/unclear/1 vs verifier other/praise/1: "Almost have, what I wanted."
- `2b46f268-a624-46fe-a3f4-e17b05937abd` enricher other/complaint/2 vs verifier usability/complaint/3: "Worst app after update can't even use basic functions after update 🤢🤮"
- `2b4aa6f0-04a6-40ae-967b-5fb448fc5810` enricher usability/complaint/2 vs verifier usability/request/2: "New update is absolutely awful, I cannot stress how absolutely gut wrenchingly bad the new UI update is I am begging for it to go back to how it was before l (which was perfect) instead of this endles"
- `2b779deb-c347-4f05-9714-7e2f80c940e3` enricher other/praise/1 vs verifier usability/praise/1: "It is good when ever we want we can select wished songs ❤👍"
- `2b85d3e3-bd28-4dda-b20e-f6eb3037fedb` enricher other/praise/1 vs verifier other/unclear/1: "Strong"
- `2b8a3d48-53ae-46d2-9bfd-2832d6fa3249` enricher downloads/complaint/3 vs verifier downloads/unclear/2: "Nice but free download erutha nalaerukum"
- `2b9372eb-7c02-4a64-bd69-fc65942bd5d0` enricher usability/complaint/3 vs verifier usability/complaint/2: "It's good but there is one problem I don't use premium so the songs on my playlist work on shuffle but sometimes it starts playing songs that aren't in that playlist really appreciate it if you could "
- `2bbb504e-55f7-4a61-96d8-d9be189a53aa` enricher other/complaint/2 vs verifier other/unclear/1: "Farig app r"
- `2bcc101b-4f06-411b-9cb4-96a6bdf7fff7` enricher catalog/complaint/3 vs verifier usability/complaint/3: "What happened to the enhance button on my liked Playlist? It just disappeared I restarted my phone even losing in and out of my account reinstalled the app and its no where to be found"
- `2bcd8503-5c72-416d-8beb-737e86d97b67` enricher other/praise/1 vs verifier usability/complaint/2: "I play harmonica to tunes I get from Spotify. I am happy to get any song anywhere anytime. I get no ads or interruptions during my playing ...unless I get a phone call. If I could ...I would shut the "
- `2be8d574-9204-484c-9359-aeccf36e8db4` enricher access/unclear/2 vs verifier access/unclear/1: "I didn't realize that with Spotify you need to have a login and password for the app"
- `2bf20f19-639d-4c1e-91e2-2406319fd330` enricher billing/complaint/2 vs verifier other/complaint/2: "I don't like this App This app is scammer"
- `2cbd30d1-4c0b-4d35-b70e-097273647722` enricher catalog/praise/1 vs verifier other/praise/1: "I love the podcast"
- `2cc049b7-fd32-45de-93ea-3888e319ccab` enricher other/praise/1 vs verifier other/unclear/1: "Enjoy lesting"
- `2cc52150-4064-41d6-ac1e-bd0e5b21dae9` enricher other/cancellation/2 vs verifier playback/cancellation/3: "The new update sucks, why did they do that? Not being able to play songs according to us is such a big downgrade, they are going to lose several users because of that. I might consider uninstalling th"
- `2d26f4c9-5333-4f38-b557-4730489b60f3` enricher playback/cancellation/4 vs verifier billing/cancellation/3: "After the update we can't play the music we want either we go for premium or it's useless so it's better to uninstall"
- `2d477e7c-588a-4548-ae6d-6ee00d306335` enricher usability/complaint/3 vs verifier usability/complaint/2: "It's chock full of ads, other streaming services are much better in that aspect. Every one to two songs there are two 30 seconds ads."
- `2d65ea48-8483-4d6c-a4ce-d90b05a57e75` enricher billing/request/2 vs verifier billing/request/1: "Pls stop 🛑 the premium pls 🙏🏻🙏🏻🙏🏻🙏🏻 😭😭😭"
- `2d779ace-fd1b-4875-b032-81704e74bbd6` enricher usability/complaint/3 vs verifier usability/complaint/2: "GAVE FOUR BUT PLIZ SPOTIFY PLIZ STOP THIS AD. PLIZ SOMETIME MORETHAN 12 TO 13 ADS. SHOWS UP CONTINIOUSLY PLIZ IT IS TOO MUCH pliz"
- `2d8464a8-3069-4dae-a56a-c2b77633c914` enricher usability/complaint/2 vs verifier usability/complaint/3: "Pushes ads through notifications. There is an out but it's divided into many categories that all have to be individually and manually disabled for both push and email notifications just to not see ads"
- `2d8aabbe-77f8-435d-99f8-2dba71ae6ff3` enricher other/complaint/2 vs verifier other/praise/1: "Aathu!!! sabse gawar update hai ye"
- `2d9e8f41-7473-41c6-8552-cb440c15ece0` enricher other/praise/1 vs verifier catalog/request/1: "great application!!! don't miss to upload."
- `2dcce68b-ff93-44b6-af02-9edbf49507a7` enricher catalog/praise/1 vs verifier other/praise/1: "love listening to the music"
- `2dd66e1f-064b-4460-b898-d2a782a0cdd8` enricher billing/request/2 vs verifier billing/complaint/3: "I didn't like the current Update it's so annoying i want to play my song again again but it showing"want premium " before it don't show this and I want translate songs so i could understand but now it"
- `2def47b9-a1d9-4116-860e-2e1d9c13511b` enricher catalog/praise/1 vs verifier other/praise/1: "Super app of songs 😃😁"
- `2e142ca6-7d94-4cc4-bfe2-f056cde7939c` enricher billing/complaint/2 vs verifier billing/complaint/3: "Every simple thing is in premium new upgrade make this app basically use less"
- `2e37c00b-38b1-4aad-8693-80a697f2f91d` enricher other/unclear/1 vs verifier billing/praise/1: "At this moment I'm satisfied,,But I don't know because I'm still on trial for this app , so I'll reserve my judgement so far 😜😜😜"
- `2e3c48df-b224-428c-8b5e-1fbcb557860e` enricher downloads/complaint/2 vs verifier downloads/complaint/3: "Great catalog, but downloads are proprietary and if you want full features it costs money"
- `2eac5f65-b34a-441e-b94b-b97c6df33f50` enricher billing/complaint/3 vs verifier billing/complaint/4: "After the trial expired, tried to click on musics and was surprised to discover that IT WON'T ALLOW YOU TO LISTEN UNLESS YOU HAVE A SUBSCRIPTION. What's the point of having this installed if I can't l"
- `2edc08f9-7041-4cdb-8bb4-5a91fe0afecc` enricher billing/complaint/3 vs verifier usability/complaint/3: "Really Disappointed by the new feature added by Spotify.Now I can't even play the song in loop and most importantly I can't even play any part of the song by my own"
- `2efbca00-c475-430e-ac79-acb195a08bfc` enricher other/unclear/1 vs verifier other/complaint/2: "Imagine putting the n word into Odetari's Song But odetari dosen't even had that in His Song how About Ayesha Ericota? So many Slurs and racist words But i love her songs tho so Dont cancel Odetari😒😒"
- `2f1964f2-ab07-4397-b9fc-2f50dfe47b23` enricher usability/complaint/3 vs verifier usability/complaint/2: "Adss are too tooo too too too tooo much"
- `2f67f1bb-292c-4308-a277-58852d4bafb7` enricher other/praise/1 vs verifier usability/praise/1: "My music plays good I can shuffle and pick what I want"
- `2f7aea5a-d18c-4b92-9642-2f7ff0de247b` enricher usability/complaint/3 vs verifier usability/complaint/2: "Spotify has been consistently improving their features to their worst possible version, forgetting that the generation they mostly serve grew up hearing music on TV. With more adverstisements than son"
- `3012a3be-cac0-4c7b-9e4f-90a16e3827c5` enricher billing/request/2 vs verifier billing/complaint/2: "Even tho they made shuffle Premium, I still hear a playlist this bad. Bring it back to free please."
- `302cf978-7ad8-4f11-8c01-9c53f5798384` enricher catalog/complaint/2 vs verifier usability/complaint/3: "I'm using this for 6 months now but still unable to use many features like lyrics sharing to Instagram etc"
- `30457e5e-cecf-4329-a161-9ddc53eb8717` enricher catalog/praise/1 vs verifier catalog/complaint/1: "Although Tidal offer you high quality sounds (Hi-Fi) at a low price than Spotify. Spotify has a much better library of music."
- `30b34826-d6da-4b66-b483-872d7bddf39f` enricher usability/complaint/3 vs verifier usability/complaint/2: "too many dream11 ads"
- `30c86d70-a576-416f-a7ea-a3ff7f3fa9b6` enricher other/complaint/3 vs verifier usability/complaint/3: "Horrible, doesn't open links when it should."
- `30dfaa16-dc27-43bc-8d62-c4f9892c77b4` enricher other/cancellation/2 vs verifier billing/cancellation/2: "The recent update really sucks, I've been using app from 3 years but gonna say goodbye sadly, it was a best app not anymore . Really u people are hunger for money this much 🫵🤡. I'm uninstalling Spotif"
- `312646a4-9558-4bf1-bd65-1accedac6df9` enricher other/praise/1 vs verifier usability/praise/1: "Love making a Playlist it's easy and I love music."
- `31273ebb-7157-417d-8b1a-aff541e07a92` enricher catalog/praise/1 vs verifier other/praise/1: "I love this app, I enjoy podcasts and music wherever I go."
- `312943f4-aae1-463c-b747-9bcfeec1ae7d` enricher usability/complaint/2 vs verifier other/praise/1: "Best app but one issue too much of advertisement in Hind"
- `31346e21-72ba-4029-a45e-0473428eb02e` enricher usability/complaint/3 vs verifier playback/complaint/2: "Spotify just played me 8 ads in a row."
- `31423dde-0ff9-4ccd-a2d0-94ff62ed1c7b` enricher catalog/complaint/3 vs verifier playback/complaint/3: "It doesn't even play your full listed of liked songs and play random songs. Then when I press play to the Playlist it doesn't wanna play"
- `3163c474-83b7-40f5-adce-cc0b84883ca5` enricher catalog/complaint/3 vs verifier billing/cancellation/3: "Spotify sticks over the same song again and again. Youtube music seems better at recommendations. Total waste buying premium. I can't listen to many music on the platform. I don't know why I paid for "
- `31b175b8-eba5-4db7-9a08-9a5f40ea37ec` enricher usability/complaint/4 vs verifier usability/complaint/3: "My liked songs folder doesn't open"
- `31ec947a-c2f2-4a89-88bb-df0fcb02ceec` enricher billing/complaint/2 vs verifier billing/complaint/3: "No premium=no entertainment"
- `320c597f-116d-4864-9c9b-5b23d18fd1ae` enricher playback/complaint/4 vs verifier usability/complaint/3: "Very bad app now no skips ,no song playable from liked songs and the app is now like it is controlling us not we . Ery downgraded and no user friendly app"
- `320f782f-c6c5-400a-8ee7-d6a5009b3e25` enricher access/complaint/3 vs verifier catalog/complaint/3: "App interface is not working properly facing problem while searching for songs Spotify team should look at this problem or we have to shift to YouTube music or any other applications"
- `326c7331-5d88-4d8f-a36a-803fb24eac2b` enricher billing/complaint/2 vs verifier billing/complaint/3: "Lyrics are not available without buying premium. Please there are many people who want the lyrics 0lease fix this. 😠😠"
- `32785447-d4e3-4fa0-ad4b-0731022d4094` enricher other/unclear/1 vs verifier other/cancellation/1: "I'm going install wynk now"
- `32937bf8-6fb5-4d1d-8089-f89fb1c6e4da` enricher playback/praise/1 vs verifier other/praise/1: "I fixed the prokblem i had and now Spotify is working perfectly!"
- `32a27ed4-e5ea-425a-9e93-3081d58a591d` enricher usability/complaint/3 vs verifier usability/complaint/2: "I use this app on my ps4 and every time I get an ad it will give me 4 back to back after only listening to a couple songs. I dont know if this is a glitch but it's been going on for so long that I can"
- `32a9051a-1bb5-4ec5-91e1-6a961a86dd40` enricher other/complaint/2 vs verifier other/unclear/1: "pagal hai ye log"
- `32b24ab1-ae40-4d0e-850d-e74c638eb131` enricher usability/complaint/3 vs verifier usability/complaint/2: "After every song I would get about 3-4 ads. Features are very limited, limited skips, shuffle only overall a really bad app. I would reccomend only using the desktop version but ads are really incessa"
- `32c1026e-3da1-4459-b6d3-c81c6240fec1` enricher billing/complaint/3 vs verifier usability/complaint/3: "Did you just display a, "You can skip 6 times in an hour" just now...??? Did Elon Musk buy you out or something, why this insist on the app destruction???"
- `32dca333-67f0-4dc1-aed0-34c7a6a8287d` enricher catalog/praise/1 vs verifier usability/praise/1: "easy to use and lots of song to choose from."
- `32fa293a-f12d-471f-ae8a-4c517880d148` enricher other/praise/1 vs verifier other/unclear/1: "Music yes cool pie"
- `331e1f54-6499-46f7-8292-433030da27c6` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too Many ads.I mean way too many. And i mean it"
- `3328fe87-2e3d-4140-b15f-a8f1d0cf8adc` enricher usability/complaint/3 vs verifier usability/complaint/2: "Worst app nowadays.. Don't have sorting, fast forward nothing please don't use this"
- `336fbbba-ef91-48d8-b349-f7f211e05c34` enricher billing/complaint/3 vs verifier billing/complaint/2: "Spotify free is unusable at this point"
- `3393c703-7ebf-43c9-aa0d-91b2f892dd07` enricher billing/complaint/4 vs verifier access/complaint/4: "Unable to login in with mobile number after paying subscription fee.Total Fraud."
- `339c842e-d872-4d01-a958-d8e9abbee2c0` enricher other/cancellation/2 vs verifier other/complaint/2: "Is the worst and I will never use it again 👎"
- `33fc6d61-990a-461c-862d-ca77124b73fa` enricher billing/complaint/2 vs verifier billing/complaint/3: "There's really no point in getting Spotify if you can't get premium. Idk why they even make this app free. But it is, hands down, the best music app there is."
- `340826fa-a1d4-4d25-bf57-0a06742dc539` enricher other/complaint/2 vs verifier usability/complaint/2: "Each Update seemingly gets worse and worse I shouldn't have to download an APK for an older version just to be able to view full playlists that aren't mine and be able to preview songs even in playlis"
- `3475302f-9357-4c3a-bd74-8d392e1fd65b` enricher billing/complaint/3 vs verifier playback/complaint/2: "Trash, good for nothing, you can't play track of your choice"
- `34d950c0-a399-4b20-a3ec-906d1ca015a7` enricher other/complaint/2 vs verifier other/unclear/1: "They say as time passes progress should be made.These guys disagree"
- `351cb789-89c4-4ef2-8c34-56ee4d4de335` enricher other/praise/1 vs verifier catalog/praise/1: "Best high quality songs"
- `354033bc-538d-4899-a412-ec76c6a1207c` enricher usability/complaint/2 vs verifier playback/complaint/2: "I love it. My only problem is that sometimes when I leave a the app and come back, I can't see the song that was playing"
- `354a2631-ed4e-4dd5-8512-bf7a40145cf7` enricher other/cancellation/2 vs verifier usability/cancellation/2: "Ive been loyal for Spotify for years , but the new update mahes me delete the app, one of the ridiculous update"
- `354cca4f-3fcc-4b93-97a6-a0364cbb53b7` enricher downloads/request/2 vs verifier downloads/complaint/2: "I really like Spotify, but it’s taking up a lot of my mobile data. I'd like it if the downloading was free."
- `356a4de0-a5e1-42ea-b68d-a7c971d2b677` enricher other/cancellation/2 vs verifier other/complaint/2: "Worst updates...still app update are like this....there is no users to use spotify....we will start to use another better apps..."
- `359b60e2-b009-4517-b198-ba0e73e85800` enricher catalog/complaint/4 vs verifier catalog/complaint/3: "Can't listen to the songs I want"
- `35a54c43-611d-4a25-9af3-a62f62ba07f5` enricher catalog/complaint/2 vs verifier usability/request/2: "personally, this app is amazing, but whenever im listening to my playlist it adds songs i never even knew existed and i cant listen to songs from only my playlist and because of this i have to listen "
- `35baaa88-d0ac-4cd5-b225-a7095df45da1` enricher usability/praise/1 vs verifier catalog/praise/1: "Very good has good Playlist"
- `366cde4e-da1d-4eab-ab9e-01a992c5dac8` enricher playback/complaint/3 vs verifier usability/complaint/2: "The shuffle doesn't realize it's playing the same artist twice in a row. And when I'm listening to a podcast and must pause and come back it switches over to the last song instead of the podcast. I pr"
- `3677bc48-45de-4c35-85f1-ee3c02409a22` enricher catalog/complaint/2 vs verifier usability/complaint/2: "It's amazing that they have the worst shuffle play in history, and there are some annoying bugs, but overall a pretty good app"
- `36e67029-de15-4f1e-9335-091245061f75` enricher other/unclear/1 vs verifier catalog/unclear/1: "For Al Quraan"
- `36f74fc9-7825-4662-8e94-c9241892bf8a` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "Too Much ads. Even now you can't listen specific part or music. So I uninstalled Spotify"
- `374bc986-df20-4c0a-b158-04c498445c53` enricher other/complaint/2 vs verifier other/unclear/1: "I Baygoot for this app"
- `374e85c1-593f-4228-b10b-e88ac235a6db` enricher billing/complaint/3 vs verifier usability/complaint/3: "Good but I hate how I can only skip 6 times and can't click onto the song I want to listen to"
- `377d1510-a87e-440d-92e4-a9620c3c1781` enricher playback/cancellation/3 vs verifier billing/cancellation/3: "Still paying for premium. Have 5G now and still constant issues with crashing. Honestly looking to find my music and podcasts elsewhere. Especially since yall wanna put extra ads on my shows (when I p"
- `377d562f-f452-4c24-8971-819d4f956340` enricher playback/complaint/3 vs verifier playback/complaint/4: "All of a sudden, Spotify gets to where music just stops playing and won't continue to play either. I find having to restart the app and continuous same thing ..."
- `37a6e526-b347-4447-ae1f-a96874b79db3` enricher playback/complaint/2 vs verifier other/complaint/2: "Good service, but every update breaks the app a little more."
- `37a7077f-017a-4313-88b9-fa8d794e9249` enricher billing/complaint/3 vs verifier billing/cancellation/3: "Makes absolutely no sense with the latest update.. more like degrade. The basic features are shifted to premium, no repeat or listening to a part of the song. Whosoever came up with the idea... Bad id"
- `380799df-b434-43b4-b088-3f3e2f71fe74` enricher other/request/1 vs verifier usability/request/1: "Spotify is the best ofc. But just one update we all need is that if we could please see, who has liked our public playlist. Thank you! Hope you look into it"
- `38aa7b39-7f24-4153-91cc-ed9ec5801d83` enricher billing/unclear/2 vs verifier billing/complaint/2: "Give money and u good to go 💖"
- `3922f2e5-52e8-4b15-9f70-a234819b8093` enricher other/request/1 vs verifier other/unclear/1: "I have heard that this app os good. I wanna try it anyway."
- `39349ee5-f01d-4d38-855f-61fd32a61f4e` enricher access/complaint/4 vs verifier access/cancellation/4: "I couldn't login the old premium account. That's why I delete the app... Did you wanna help me then help me...... I buy the premium just 2 or 3 days ago... I feel very for this so I unstalled the app."
- `3950e4bd-9304-41ca-aa80-6508167c6504` enricher playback/complaint/3 vs verifier other/complaint/2: "Not compatible with other apps like Amazing Slow Downer anymore. Good job there."
- `395ee789-7a4a-4db9-ae25-634c089f32cd` enricher other/praise/1 vs verifier other/unclear/1: "Was having a issue. But fixed it. Nevermind."
- `396d6639-37bc-41e1-a5db-773c26884f6e` enricher other/complaint/2 vs verifier other/cancellation/2: "The new update just ruined everything, #bringbackoldspotify otherwise there are many other options"
- `396f14ba-4544-47e9-8314-13759cb990c4` enricher other/unclear/2 vs verifier playback/complaint/2: "Connectivity in my house on WiFi devices over laps. Each family members misoc is creeping into others playlist"
- `3974bc98-e26e-4080-a60c-62ec6d0bf812` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "Don't play the songs that I want to"
- `399b9bda-6534-4c33-8280-f4b881dea128` enricher catalog/complaint/3 vs verifier downloads/complaint/3: "Removed liked songs. BOOOOOO"
- `39a0913c-940f-49c5-b45a-419897850f68` enricher playback/complaint/4 vs verifier playback/complaint/3: "Awful network connectivity. A joke really. Stitcher app works just fine on same exact network. The app tells me No Internet Connection, but it should really be saying App Network Failure. Again, other"
- `39d320cd-42c1-4077-aef0-343d0fee8f6e` enricher usability/complaint/2 vs verifier billing/complaint/3: "6 skips per HOUR"
- `3a108d50-046c-4150-b4d2-1b76905eaabe` enricher billing/complaint/3 vs verifier usability/complaint/2: "It's amazing to use I love listening to podcasts on Spotify however I find it kinda dumb to limit skips"
- `3a25971a-f4c6-4459-bdde-8734700807cc` enricher billing/complaint/2 vs verifier billing/complaint/3: "Worst feeling after the update.... It made subscription mandatory"
- `3a3f2e75-7dd5-4455-bcfc-cafaf086dcbd` enricher catalog/cancellation/3 vs verifier downloads/cancellation/3: "Was thinking of switching from Amazon Music to Spotify mostly because of the Local Files functionality (i.e. creating mixed playlists with both Spotify-hosted music & mp3 files ony device). Can't even"
- `3a412e3c-78e4-4704-a6ad-e9620a78f741` enricher usability/complaint/3 vs verifier other/complaint/2: "Slecht. Veel te veel advertenties, en geïnfesteerd met bugs."
- `3a8d3701-a48b-44e2-be9a-7e9b9fdf4172` enricher playback/complaint/4 vs verifier access/complaint/4: "I'm not able to open this app at all! I've been trying since a month."
- `3ab54855-3da4-416d-9df2-8c0de05cf664` enricher billing/complaint/3 vs verifier usability/complaint/3: "It was the best app to listen songs... Until this new update came along. Can't go back to the previous song, can't play it on shuffle. Why should I need to buy premium to just play the previous song ?"
- `3acd46a9-e617-406d-892c-b3de0d349c10` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "Greed just pure greed , was my go to player but now I have no control over my songs anymore they took the most basic features of a music player , imagine you can't play songs in order nor you can jump"
- `3ada93e5-79a9-4c9b-ad90-f92ac8856e5e` enricher usability/praise/1 vs verifier other/praise/1: "Very user friendly!!! Great App!"
- `3b24be6a-bca2-4bbb-a9bd-5935a4f53a6b` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too many ads. It's gotten ridiculous. Even the "30 minutes ad free" isn't always ad free. There's many great qualities about Spotify, it's just a shame it's tainted with ads."
- `3b8a996c-e646-4718-ac61-03727a9a0747` enricher usability/complaint/3 vs verifier usability/complaint/2: "Gandmari app! Founder should be able to know How irriataing add is B/w music! Really sucks!! Preminum dena hai toh app start se pehle do! If you are Indian be equal or.........."
- `3b9bd40d-7f47-42eb-9987-002704f49471` enricher other/unclear/1 vs verifier other/complaint/2: "Ya this app is very extreme"
- `3be8722b-375b-4429-9682-814716cd87df` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Earlier i gave it 5 star but now I'm giving 1 star as he remove one of my favourite features "Add to Queue".This feature is now only for premium membership"
- `3bff8801-0d0f-4c6d-be13-6545dabb4e32` enricher usability/request/1 vs verifier usability/request/2: "pls bring back the option to preview songs before adding them 🙏🙏🙏"
- `3c4732e8-6171-47dc-9bce-b594929b5887` enricher usability/complaint/3 vs verifier usability/cancellation/3: "I can't even choose what song to play in my playlist and songs that aren't in my playlist keep playing randomly and it's getting annoying. You guys really need to change this and let people play whate"
- `3c6c4fdd-dd45-4dd4-a461-c65c1e31afed` enricher playback/praise/1 vs verifier other/praise/1: "crystal clear"
- `3c718bce-c267-46df-bd96-144484634c53` enricher other/praise/1 vs verifier playback/praise/1: "Sound quality is superb, and the app is extremely user friendly. Even the novice device user could figure out there way around the app to enjoy themselves."
- `3c88f934-921e-42bd-bcde-b29364f67bd6` enricher billing/complaint/2 vs verifier billing/complaint/1: "I love spotify. I have payed for this app for many years now. I just read through a bunch of the reviews and people just need to understand that if you want all of the features you have to pay. The fr"
- `3c99bd18-1e46-4b30-a32e-83f67183a068` enricher usability/request/1 vs verifier other/request/1: "Pls bring the ringtone option..we need to set some songs as ringtone.."
- `3c9a742c-991f-4b33-9f6d-68817f53dcf5` enricher usability/request/1 vs verifier usability/complaint/2: "This app has gotten better. But for every few improvements there's a new problem. I wish I could see how many hours my liked "playlist" is."
- `3c9bfaf6-53ac-4848-8a54-35c20d6187ab` enricher access/complaint/4 vs verifier access/complaint/3: "Very bad 😞 It's very difficult to login 😕 I am too much disappointed with this"
- `3cb5c17a-71bd-43f0-b817-959f8b7884ca` enricher billing/complaint/3 vs verifier billing/cancellation/3: "NO WAY, The app is basically -pay to use" now you have to pay to look at the lyrics this is crazy. Never ever gonna use this app again , and dont get me started on the ad frequency which is absolutely"
- `3cb60c19-f172-4a87-9d31-597b4b445180` enricher other/cancellation/2 vs verifier billing/cancellation/3: "My Spotify "premium" account is trash. I suggest you go to pandora or another app service. I've had this account for a long time, glutton for punishment, and I is pretty consistent in how it completel"
- `3ce60b2a-6fa2-43b7-81bb-9aaee748c88c` enricher billing/request/3 vs verifier billing/complaint/3: "Worst song app till now... First you can't listen to a specific part of a song you need to buy premium for this...asap REMOVE this feature."
- `3d62bda0-f332-4e74-bac9-5dbe9cb647fe` enricher access/complaint/4 vs verifier access/complaint/3: "O aplicativo tem me desapontado nos últimos tempos, continua bugando com coisas essenciais e simples como realizar login e manter configurações sincronizadas da conta com meu celular, hoje realizei um"
- `3daa3f98-96fd-40d5-be2c-5ff46f11c893` enricher billing/complaint/3 vs verifier billing/complaint/2: "This app is not developing but decreasing it's own user by making it pay to listen It gained popularity but used for the wrong Not expected and not worthy anymore Waiting for a app which will be bette"
- `3dbfa030-0170-486f-9a3c-d18216219807` enricher billing/complaint/4 vs verifier usability/cancellation/3: "You can't play songs of your choice anymore as much as you want! TF I went to the servh bar to play a song & it says I can't anymore and have to wait for tomorrow. same goes for skip button where I ca"
- `3ded3ea6-afc7-4c06-b855-6f3aae515d19` enricher playback/complaint/4 vs verifier playback/complaint/3: "Whomever wrote this app should have to put their name on it because it is really poorly done. It has issues with merely playing the ads, then after forcing it to do so for awhile, it simply refuses to"
- `3df31979-bb55-4539-97c7-949daa1fbf05` enricher billing/complaint/3 vs verifier billing/complaint/2: "Bro it's not giving basic features for free everything is paid 😔"
- `3dfa4aa7-fa4e-40ce-8730-7bf0cdcbfad0` enricher usability/complaint/2 vs verifier usability/request/2: "Why would you guys remove the shuffle button??"
- `3e107489-aa52-4ade-958d-77a13e9884de` enricher playback/complaint/3 vs verifier playback/complaint/2: "Every time I pause a song it starts the playlist over once that song is complete."
- `3e17475e-2c35-4e13-bb04-c42236d412dd` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "Saalo gareeb smjkr premium option dete ho fire h apun now it's too much I can't even afford premium subscription so I officially deleted it 😊 please delete this premium option otherwise I complaint ag"
- `3e18a990-1c92-4d02-86b3-77c98c4ffb27` enricher catalog/praise/1 vs verifier other/praise/1: "Wow superb I love bts songs soooo much Thx"
- `3e51627a-3468-4253-9a80-ff61d4b15016` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Plays music well, I just absolutely hate the suggestions, they don't work, and are unskipable. (Updated) Got premium and is definitely worth it, though the family plan is better if you have more than "
- `3e6c1ed9-6ae7-450a-b37a-faee11ce9a7b` enricher other/praise/1 vs verifier catalog/praise/1: "It's very good and you are very easy to find a song"
- `3e9a652b-9809-4eb5-bfe5-a85d5422555a` enricher playback/complaint/2 vs verifier usability/complaint/2: "When you pull down the thumbnail of the song is incorrect, terrible bug!"
- `3ea47e18-741b-422b-9a1f-4686c4394804` enricher playback/complaint/3 vs verifier playback/complaint/2: "Very bad quality of sound and frequen ads eritetive"
- `3eb1fc6e-7b23-46be-9fb4-05a69128db00` enricher billing/complaint/3 vs verifier usability/complaint/3: "This is suck, when you play with your playlist, you're not able to listen all you want to play in your playlist, and so many ads. Can't listen properly because of it.!!!!"
- `3ec55d53-d640-4a84-af7b-671861cb0058` enricher catalog/complaint/3 vs verifier downloads/complaint/4: "Great app but now can't even listen to my liked songs Playlist"
- `3f21f932-c673-405e-8da5-948eca9df093` enricher access/complaint/5 vs verifier access/complaint/4: "I was logged in with my number, i got my phone changed and now i codunt able to login in..even I'm paying Spotify on a monthly basis for premium...my money keeps on deducting and i codunt able to logi"
- `3f42bc85-c2fd-47b6-baf5-bdbfcaf237bc` enricher catalog/unclear/1 vs verifier other/unclear/1: "You know why. mohammed assaf"
- `3f540995-d395-4eca-acc6-19f361bd1f1c` enricher support/complaint/2 vs verifier billing/praise/2: "They got the best music but if ya sink ya premium account to ya game console ya can end it and still get ya premium music if yall had better customer services wouldn't have to share a hack ya can't pa"
- `3f685f3f-93e8-42f8-89ad-5661f4e13338` enricher other/praise/1 vs verifier catalog/praise/1: "Umm.. Alright I really love this app it consist of all the songs of the world 🌍🌎 💕💕😘 must download"
- `3fc76671-a647-427c-b8e8-71b9120fa1eb` enricher playback/complaint/3 vs verifier catalog/complaint/3: "To the guys who work on Spotify the new the beatles Revolver video doesn't work could you find out why this is thanks"
- `3fda7bb6-2c3c-4225-a6c5-3c4a7c0855fe` enricher other/praise/1 vs verifier other/unclear/1: "Great app! Any version"
- `3fed61ac-b08c-4399-8fe3-eb6655a3980a` enricher playback/praise/1 vs verifier playback/complaint/2: "Quite pleased. A few lagging and crashes over the past months but they were resolved quickly."
- `3ffab298-a326-43e9-b954-5099885e1eef` enricher billing/cancellation/3 vs verifier other/cancellation/2: "Was it necessary to remove all basic features of the app??..... I am going to switch to jiosaavn"
- `403595ad-9d56-455b-a004-7c3e84ff4190` enricher usability/complaint/3 vs verifier usability/complaint/2: "But one issue I can't choose what song I want it's randomized in a playlist and my other device I can choose what I want to play so why is this happening? But besides that this is a great app and my n"
- `407ae24c-81a6-4714-ba8e-250a2fa85ead` enricher playback/complaint/3 vs verifier usability/complaint/2: "This app sucks. Everytime phone goes off sleep it starts playing. Flip every option in settings to off, still auto plays. And as if that wasn't bad enough it autoplays on my watch too. I wish I could "
- `40aa044d-0e7f-4f4d-b14a-c704b315617e` enricher billing/complaint/2 vs verifier billing/complaint/3: "Not worth it unless you have premium"
- `40e7d555-59e0-47f6-baee-cf9ae965caa8` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Very bad app now with that new update you can't even replay or shuffle your songs like we used to do and they took all of the control from us and forcing us to buy their premium version never gonna co"
- `40ffd17b-0820-4a6b-95cf-c0fec4eb24c9` enricher catalog/praise/1 vs verifier other/praise/1: "I'm in love with the new ai dj"
- `41120c75-8cee-40e3-8fb4-8fc69b3cd2a2` enricher playback/complaint/3 vs verifier usability/complaint/3: "Won't show what's it's playing and how far you are into a song or podcast. Randomly stops when no ones pressed a button even with screen off 😒 🙄"
- `41212a8c-1d64-4e5c-ad6d-3aa8bd15de08` enricher other/praise/1 vs verifier catalog/praise/1: "I like spotify so much coz it eases everything in a way that whatever u want is always available thank you so much .."
- `419e2ada-b8ce-4d5f-900f-dbdeab99556f` enricher catalog/complaint/2 vs verifier usability/complaint/2: "It's a good app, but when im playing my play list's it will randomly play songs based on what I like and I don't like that . If I want to play songs out of my play list I will do it myself"
- `422d8563-afc1-45a7-b8be-46092a54bc0f` enricher usability/praise/1 vs verifier other/praise/1: "Excellent. Highly recommended. No meddlesome ads"
- `423e1c74-f7c8-41d6-9a14-dacb79dfeebf` enricher billing/complaint/3 vs verifier playback/complaint/3: "Very bad app ,khud k man se gaane bhi chalane nhi dete😡😡😡😡😡😡"
- `425fb6fc-1a2a-451f-9c59-bfc8fe72f9bf` enricher billing/complaint/2 vs verifier other/complaint/2: "Greedy fools"
- `426c7e03-0285-42ed-bf97-0b05cca626f3` enricher usability/complaint/3 vs verifier usability/complaint/2: "Nice experience. But it's totally false that we use 30 min uninterrupted music.. Another add is started before 30 min time period..... It's disappointed me......."
- `427768de-7737-4a5c-86c4-0f85422d83cc` enricher billing/complaint/3 vs verifier usability/complaint/3: "The new update is frustrating. Not being able to play the previous song or to the favorite part of the song. Switching to a different now!"
- `4307946a-f231-4f35-b11b-d43beea0f387` enricher catalog/cancellation/4 vs verifier catalog/cancellation/3: "lame! why can't I play the song I want to play..What is the point of using internet.I uninstalled it.."
- `430fc668-1760-43ce-acbf-7848f280aeb1` enricher billing/complaint/3 vs verifier billing/complaint/2: "I hate , it is forcing to take premium ."
- `4324a2f1-0a34-4de4-8af1-dfd018c5ef5d` enricher other/unclear/1 vs verifier other/complaint/2: "Bekar bhag"
- `43277fda-1699-472f-b62f-647fc2624609` enricher playback/complaint/3 vs verifier usability/complaint/3: "Whatever this new update is, is trash. It constantly pauses. Plays different songs than what I put on when I connect to my car. Can't keep the repeat button on when changing albums any more. And the n"
- `43b0af6f-c675-4224-8399-0b805b772472` enricher billing/complaint/3 vs verifier usability/cancellation/3: "Spotify used to be my favourite music app, but now it just sucks so bad. Hate it. Hate all the new updates. Can't skip more than 6 times in a day. Can't choose to play only from my playlists. Can't do"
- `43e64e82-4458-4dc1-aae1-c9fc1fe53e9e` enricher usability/request/1 vs verifier catalog/request/1: "I have been thinking about how to improve the app although it has good benefits How about creating a built-in translator or so, to translate your favorite songs written in a language you don't underst"
- `44033229-a966-49e3-a558-0a95d0978a98` enricher usability/complaint/2 vs verifier usability/praise/1: "It is the best app for Android auto and single listening. Only adds will disturb you if you using free version."
- `443ee4db-2c7b-4b69-b4f6-2f6b3e83a5c3` enricher downloads/praise/1 vs verifier other/praise/1: "Best music app hands down. Yes it helps if your a premium subscriber but lets face it..for the cost of one album a month..you get endless access to so much music and can even download and play it offl"
- `443f4050-d762-4ad1-b7e6-278948f5db64` enricher usability/complaint/2 vs verifier catalog/complaint/2: "The lastest update ruined everything" when is not broken don't fix it" it was working very well there was no need to update anything now when you search a song and play it different song start to play"
- `449952b7-4f11-4824-877e-7f3aeed4839d` enricher playback/complaint/3 vs verifier playback/complaint/2: "I love the selection of music. However, there is always some problem with the app. Most commonly it takes forever to load. Sometimes I have to restart the app several times before I get it to load any"
- `44a137d8-e01c-4f4b-917b-368916907646` enricher usability/complaint/3 vs verifier downloads/complaint/2: "Why the hell you deleting songs from fav?"
- `44adc04a-2d07-46cd-ae68-b205de0211da` enricher other/praise/1 vs verifier playback/praise/1: "I love you Spotify thank you because of you I can listen to music anywhere in good quality and lots of it without you I wouldn't be able to listen to music in my car or when I'm in the woods so you ar"
- `44d3d8a0-f7ca-4fd4-a181-ac04e109760d` enricher playback/complaint/3 vs verifier usability/complaint/3: "It is very nice app . Understands the kind of music I want to listen but from past few days , it's just gone crazy man . Lot of minute problems are appearing while using this app . Sometimes back to 0"
- `450ff889-7c50-40d0-a94f-3f7d4ce1cba4` enricher other/unclear/1 vs verifier other/cancellation/1: "Bycott the spotify"
- `451e1fd3-fb81-406b-8454-a6855cac7475` enricher billing/complaint/3 vs verifier usability/complaint/2: "Everything is cool but some limitations are awkward. Like, skip limit in a day"
- `45915443-0295-4ad2-a35a-dc25a9170823` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "I don't know what happened to Spotify right now. When I want to see the lyric but they can't loud the lyrics. Can you guys please tell me why?"
- `4607d898-3914-4cb8-80a2-224706a95f16` enricher usability/complaint/3 vs verifier usability/complaint/2: "The latest update sucks! Not able to preview songs in playlist anymore."
- `460bb018-0c28-4d00-9ec2-298c17a8126d` enricher usability/complaint/2 vs verifier usability/complaint/3: "I've had it for abt 2 years now, it was great for the first like 1.5 years. From there, it just started becoming REALLY ANNOYING! I'll make a great playlist then at the bottom it'll say "here are song"
- `46272d7f-9ec5-4315-ac26-875be328c65b` enricher playback/complaint/3 vs verifier other/complaint/2: "Spotify is taking Up all my Internet I don't know why but it's to be good and this is that but now it's not good no more like spotify it's mostly taken off my Internet and it says that this day has to"
- `46326e74-b47d-4bde-b860-ef1018549a48` enricher billing/cancellation/3 vs verifier playback/cancellation/4: "worst app, can't play any song with our permission. this is not good you people are making fools, why we should buy premium? we can go on other apps! I'm leaving your app"
- `4632ac60-ef72-40dd-bf00-53a74d011785` enricher billing/complaint/3 vs verifier usability/complaint/2: "Man what happened, we are okay with the ads but too much control for non premium users 🙃"
- `46632653-6434-434d-ac73-4b1a9717411b` enricher other/praise/1 vs verifier catalog/praise/1: "This app is awesome, you get to pick out what you want."
- `469a689b-adc0-49b1-9ca0-ca2f41fa21a6` enricher catalog/complaint/3 vs verifier usability/request/2: "I WANT THE FAMILY PLAYLIST BACK!!! I share my premium acct wit two teenagers, how am I supposed to teach them about the back in the day music and them teach me about new music? Come on, Spotify? You c"
- `46a0f98f-9113-4688-9ef0-2ca28920ffe8` enricher other/praise/1 vs verifier catalog/praise/1: "This is superb and super app " is ke andar bhakti gaane sunke maja hi aa jata hai "," ak bar is ke andar '****shree Hanuman chalisa**** sun ke dekho mere bhai maja hi aa jayega ""
- `471e2b62-db15-4a78-b64a-6ef4b6313b94` enricher usability/praise/1 vs verifier billing/praise/1: "It's really good no ads I haven't got premium but I guess I don't have to"
- `4737b055-12e9-4155-b28a-d1b815c48d3c` enricher playback/complaint/3 vs verifier playback/cancellation/3: "For a company this big this is terrible. It regularly has issue with Bluetooth devices whilst other apps are fine. Makes me consider trying Tidal again."
- `473dfa87-df86-445d-8912-2f43bfdcfb19` enricher usability/complaint/2 vs verifier usability/complaint/3: "You guys are stooping too low. I mean your so desperate that you are giving a person whose using this for free 6 skips per hour seriously step up. Other than that the app is good"
- `474d5dcd-05c6-4225-95f9-48c230810c9c` enricher usability/complaint/3 vs verifier other/complaint/2: "I have a huge disappointment with thus app from the new update its have many change even we don't skip more than 6 song per hour the why this app move with gana or another music apps"
- `47520cc8-e597-4169-a0f4-dd17f88ebd77` enricher other/cancellation/2 vs verifier catalog/cancellation/2: "Mariah Season? Nope. You've just given me another reason not to use Spotify for a while. Well done. Rock 'n' roll on 2023..."
- `476d759e-5fd7-4d6b-9736-d31b1262b9c4` enricher billing/complaint/2 vs verifier billing/request/1: "I have jio sim and they gave me subscription with every recharge. Why I purchase your subscription"
- `47f05ee6-56a5-4c29-8317-0f74673d1ca4` enricher playback/complaint/4 vs verifier usability/complaint/4: "It is not opening and everytime i just got ads😐"
- `47f112f9-eff2-4f06-8956-95b854d944c9` enricher billing/complaint/3 vs verifier billing/complaint/2: "Very bad after update evertingi is premium"
- `48159f8e-546c-417f-9f3f-84329189ddd6` enricher playback/praise/1 vs verifier other/praise/1: "Seamless experience with the right music on the Go. Enjoying every moment with it."
- `482498fa-5346-47f1-897c-f03a41e67101` enricher other/praise/1 vs verifier playback/praise/1: "Very happy with the performance, and variety of music!!!"
- `487d1c4e-b51f-429b-a186-d39bdf9b4e23` enricher catalog/praise/1 vs verifier other/praise/1: "Archetype is my favourite 😍 💕 here thanks 😊 🙏"
- `4881004e-da6e-49a2-96c6-1609547bf77d` enricher billing/complaint/2 vs verifier downloads/praise/1: "Does great for music offline and online. I love that I can download my personal Playlists. As for withdrawing money from my account they could use a better ACH system."
- `48a48022-9af6-4096-9c46-8d90caa14a61` enricher usability/complaint/3 vs verifier usability/complaint/2: "I REALLY LIKE NTHIS APP.BUT I JUST HAVE ONE PROBLEM WITH THE ADS,THEY JUST TOO MUCH ADS MANGIYFUNA LE NGOMA ADS JUST DISAPPOINT ME SO I GIVE THIS APP AHHHH 3 STARS YA THATS ALL I CAN GET FROM THIS APP"
- `48cc4991-62b9-411e-88a8-26731d52545c` enricher billing/cancellation/3 vs verifier billing/cancellation/2: "I hate it.. I hate it... I hate it😠... I don't know what are the developers are thinking... Destroying a perfectly functioning and accomodating app to a hassel and a nuisance. Spotify is for listening"
- `492396a1-ba2e-4437-b150-877123ececa7` enricher usability/complaint/3 vs verifier usability/complaint/2: "Don't use this app more ads"
- `495b2589-7947-4f10-ac56-bc14891732f8` enricher catalog/praise/1 vs verifier other/praise/1: "Very sweet song 😍👍❤️😍😍😍😍"
- `49930880-2283-41be-b795-4afc0864b099` enricher playback/complaint/3 vs verifier usability/complaint/2: "Everytime I pause the music or podcasts I'm listening to for too long, Spotify deletes my queue and switches from whatever playlist I was listening to, to play from my liked songs?!"
- `4996cff3-1233-4b78-982c-ffccb530ba6a` enricher usability/request/2 vs verifier usability/complaint/2: "would be 5 stars if you put the heart back."
- `49af0bc1-744e-48c8-a1fb-3b42dfbfeb93` enricher billing/cancellation/4 vs verifier billing/complaint/3: "This was a best music app, but now it's has been a worst cz of some update they removed all the basics features of the app, idk why they had removed and to do premium and get enjoy ur features, like w"
- `49fb5c87-b31f-41ce-be75-40a827e31edf` enricher other/unclear/1 vs verifier other/complaint/2: "Bal korsa de Spotify"
- `4a2fefe1-3cd8-4ea3-b63a-9f3c871075ed` enricher other/complaint/2 vs verifier other/cancellation/1: "12k aap hai ye Bhai ye Delete karo"
- `4a42dbb0-b992-42fb-a569-6a980a026ba0` enricher usability/complaint/3 vs verifier billing/praise/2: "Very good app but one problem this app show you ads after every 1 song this is the bad think but the app is easy to use and good user interface Keep growing Spotify"
- `4a6c9774-2f97-4990-ba50-c0ce650b2518` enricher playback/complaint/3 vs verifier usability/complaint/3: "SPOTIFY YOUR MUSIC QUALITY IS GOOD BUT YOU HAVE TO MAKE SOME CHANGES FOR EXAMPLE IF I PLAY A SONG THEN UPTO 30 MINUTES SAME SONG WIL PLAY WE CAN'T MOVE TO NEXT IF WE COMPARE TO OTHERS APPS AFTER 30 MI"
- `4a7fb559-9945-4b0f-a8f7-daffaa7f3ebc` enricher billing/praise/1 vs verifier other/praise/1: "I love spotify! We have the family plan and it is amazing."
- `4a9d0708-3a9d-4625-87ea-a3bf412b502e` enricher access/complaint/2 vs verifier downloads/complaint/2: "I like,But I can't install while updating"
- `4ae6e722-09d1-45ef-a914-bd5bd92d6574` enricher catalog/complaint/2 vs verifier other/request/1: "Me ye aap bas BTS ki wajah se download kar rhi hu kiu ki un hone bola h i love you BTS ot7 💜💜💜💜💜😎"
- `4b13be13-3287-4a71-9dd7-8274129c3d78` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Very poor in searching songs"
- `4b72bd95-f0af-4d37-bc52-f27f6e19687c` enricher other/unclear/1 vs verifier other/cancellation/1: "I hate sweden. I love quran. I deleted this app due to burning of our Holy Quran and boycott sweden."
- `4bad2694-145e-4b5e-a70b-f22742f5501c` enricher playback/complaint/3 vs verifier catalog/complaint/3: "It's getting really annoying how it keeps replaying songs from a while ago. It's not what you think either, for me it picks a song it played a while ago (like 4-9 hours ago) and starts playing the exa"
- `4c363266-24e0-46f8-bc39-41e7e07d296a` enricher playback/cancellation/3 vs verifier playback/cancellation/4: "Spotify only plays podcasts or music for a short time before the audio completely stops and can't remember it's place. I have the full paid subscription to this, and experienced this problem for month"
- `4c729ce0-c7e6-4026-b4ec-b44577766d51` enricher usability/complaint/2 vs verifier catalog/request/2: "Please improve the shuffle algorithm. It plays the same set of songs everytime I shuffle play my playlist."
- `4c7304ac-2d31-44d2-8c2b-09d209d68497` enricher downloads/complaint/4 vs verifier playback/complaint/4: "It used to work very well, but now if you have cell data or not it lags, pauses constantly or when there's no cell service even downloaded Playlist won't play. Paying money to listen to intermediate s"
- `4d5ad3c7-fcb3-4a92-8e26-5c4d042e360e` enricher usability/request/1 vs verifier billing/request/1: "Block the ads and make premium free for life time."
- `4d71a426-6f4b-4295-94b4-cee6c6866829` enricher playback/complaint/3 vs verifier usability/complaint/3: "Prefer Spotify over youtube music because of the session play with friends, but it keeps bugging out a lot. YouTube has better randomiser and music suggest. So there's no point in using Spotify over y"
- `4da8a4cf-e0e3-49cb-bbb2-0b476d7ed649` enricher billing/complaint/4 vs verifier access/complaint/4: "Can't upgrade to premium,always can't connect"
- `4dcbadaf-2c3e-4beb-981e-961abb7ffb13` enricher other/cancellation/2 vs verifier other/cancellation/1: "I don't want this app, i prefer jiosavan or something else"
- `4dd9fee9-bcfe-4a0d-bcb8-4470a3257c1e` enricher catalog/request/1 vs verifier other/request/1: "Sonfar i love uaing spotify because there's a lot of choices. But I thought the karaoke feature will be here in the philippines already? Can you please update it so we can enjoy the karaoke?"
- `4de52018-2c6e-4fbc-8bf6-89aa10c41450` enricher playback/complaint/4 vs verifier playback/complaint/3: "Spotify was a good app.After this update I an unable to play the songs that I want to."
- `4de73a80-bd6e-4d51-ba08-00f132c3a038` enricher other/complaint/2 vs verifier access/complaint/4: "This device is not able to use"
- `4e027fdd-8e34-4e5e-85ac-3f9bbb121c76` enricher usability/complaint/2 vs verifier billing/complaint/2: "It's good but no that I expect w After seeing the adds and all"
- `4e16c6a4-65a3-40ab-8b49-2d29c73b08b6` enricher playback/complaint/3 vs verifier playback/complaint/2: "Sometimes the playlist will skip songs and the shuffle isn't on."
- `4e26962f-0f7d-413e-bfac-d36320cb44f7` enricher other/complaint/3 vs verifier usability/complaint/2: "Unusable music player now"
- `4e39bc23-904a-4757-ad61-8185a38a7399` enricher other/praise/1 vs verifier playback/praise/1: "Best music listening app for 🆓 and it's speed is so good 👍"
- `4e804c3b-1561-4296-898b-9471cecbf874` enricher other/praise/1 vs verifier playback/praise/1: "Ver'nice. Like the options for playing audio to various devices and listening share."
- `4e8161ae-7d0f-446f-b3c7-a353c82bfaf2` enricher usability/complaint/3 vs verifier usability/request/2: "i really like this app.its a good app but i hate that you only get 6 skips an hour.i also hate that we can only shuffle our music,we cant listen to the SPECIFIC SONG WE WANT.this is VERY annoying for "
- `4e9cbe01-40f1-46db-b312-9931994603e7` enricher other/complaint/2 vs verifier playback/complaint/2: "Some bugs found , pls do have a check on it"
- `4eb14d7d-bfd7-458d-b5c2-2f6d954ef098` enricher usability/complaint/3 vs verifier billing/complaint/2: "A good app to dive into the endless world of music. Add get annoying and ur forced to upgrade to premium"
- `4eb21ab3-4c23-4a6d-ba5d-d0a8b6f4f4a2` enricher usability/complaint/2 vs verifier billing/complaint/2: "Perfect if you pay for premium , but if you don't the ads can sometimes ruin a moment . Other than that it is a good app to listen to music"
- `4eb361de-ceca-422b-962c-df8657acdd02` enricher usability/complaint/3 vs verifier billing/complaint/2: "The application is quite good .There is a Ocean of music filled with diverse and varieties of genres .The only demerit is the unwanted add which keep on repeating if you don't purchase premium."
- `4ebabb94-4bf5-4caf-8e4a-b40d1050a18f` enricher access/complaint/4 vs verifier access/complaint/3: "I couldn't even link it with my phone"
- `4f6b3e51-fc93-4bad-a1a4-891d8b3c9cab` enricher other/praise/1 vs verifier catalog/praise/1: "A great app for listening to my favorite music from both established artists as well as new prospects."
- `4fb04e75-5ed5-40e1-be56-d100fc6bee6b` enricher downloads/complaint/5 vs verifier downloads/complaint/4: "Nothing works, my playlists, liked songs, and podcasts are gone, I can't listen to any music, and even turning off my internet doesn't let me listen to my downloaded music."
- `4fe51d78-1fa7-4287-80ae-389907674cb8` enricher usability/cancellation/3 vs verifier billing/cancellation/3: "The new update is just dumb. Like I can't even play a specific part of a song? Like seriously? Premium for that? You can't even play it back , shuffle or any stuffs. Like that's the basic thing one ne"
- `502d6452-5f33-4a8a-8e8e-1d50f282a8c6` enricher catalog/praise/1 vs verifier usability/praise/1: "Easy to find the songs I wantand easy to use"
- `506f6980-ddbf-483e-a12f-35e09a937803` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "Worst update everything premium I m very dissapointed I m unstalling this app😡"
- `50a28e08-5027-4a74-b811-4493679f9d2b` enricher other/unclear/2 vs verifier other/complaint/2: "Not good, Not bad either."
- `50b10c28-4fee-4919-a404-fa754b1968ef` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "I lost my data downloading this app and nothing happened it still saying install again"
- `50b591da-c073-46ba-a21a-afddc94c68fd` enricher playback/complaint/3 vs verifier playback/complaint/2: "ok la keren tapi kadang kadang masa dengar lagu lagu tu ter stop sendiri dalam ni semua jenis lagu ada kau nak galau ke nak berhamil duluan ke nak blekping in yor eria semua boleh ko cari je dalam tu"
- `50f02d9f-fb35-4d9c-b89a-0b5198a07d9d` enricher catalog/praise/1 vs verifier other/praise/1: "This is my go to for music of any kind and for my podcasts"
- `510e24ee-ecf2-49b4-ba14-dddf6aa25b8c` enricher playback/complaint/2 vs verifier other/complaint/2: "Buggiest app ever."
- `5156d90a-07cf-4b1d-8b5e-29dfed6a63cf` enricher usability/complaint/3 vs verifier usability/cancellation/2: "Absolute disappointment 😥..I usually listened to music on YouTube but i switched from YouTube cause they started giving 2 ads at a time .Now Spotify doing the same thing,2 annoying ads at the same tim"
- `51610504-d3f3-4f53-98ad-8ee6f7fcce90` enricher usability/complaint/3 vs verifier usability/complaint/2: "What the hell? Only ads after listening 4-5 musics .....are you mocking me? It is SPOTIFY or adofy..."
- `51c0a2a6-3d02-43f5-8790-e2b078cfa5ab` enricher usability/complaint/2 vs verifier usability/request/2: "Ads are annoying go back to the old Spotify! It was way better! Dont change something that was good before!"
- `520944dc-33ef-4082-a276-77992e0d0aa2` enricher other/cancellation/2 vs verifier other/cancellation/1: "Shifting to another platform 🫡 SPKMBK"
- `5223d6b7-1adb-452f-9a1a-15fc31a89435` enricher billing/complaint/3 vs verifier usability/complaint/2: "Ads were fine But not allowing the songs of playlists to play in order."
- `5239907a-e2b4-4788-af7b-c29cd8ee9a79` enricher usability/complaint/3 vs verifier usability/request/3: "Please fix the recent update. I cant find the play navigation bar at the bottom."
- `52a53959-c4c6-4eae-9b0b-1ca8b5680221` enricher billing/cancellation/4 vs verifier billing/cancellation/3: "Hi Spotify! Umm I think you need to add one more premium features for user that you have to buy premium to turn on the app lol 😂 Just straight away uninstalling this app Can buy premium but now it's o"
- `52aa1132-9224-4a97-9416-935ad5545e7b` enricher usability/complaint/3 vs verifier billing/complaint/3: "Why can't you skip songs without premium?! And why does it not let me go back??? And play it again? And ads 😑 and I will play a song and it ends. I want to listen to it aging, but I can't do it back, "
- `540c9a43-b6c2-48d8-b45e-3b208b771192` enricher catalog/praise/1 vs verifier other/praise/1: "Great app lots of music available always works in all areas"
- `540d2733-d2f7-440c-b82a-edd88e5cb2a3` enricher other/praise/1 vs verifier catalog/praise/1: "Since I've been using the premium subscription, I've been completely satisfied with ad-free listening, good sound quality and above all with this "smart Shuffle" feature, the music offered corresponds"
- `543bd546-884f-4037-a3b7-c6af4c3f4945` enricher playback/complaint/3 vs verifier usability/complaint/2: "2 songs 3 ads don't give them money until they improve"
- `543f28a2-cb52-4d14-ba6c-b71248a51f04` enricher catalog/complaint/3 vs verifier usability/complaint/2: "Why can't I bookmark a audiobook!!! Plus it won't let me sync between listening on the web player and the Android app. Audible, at least lets me do that."
- `54a17413-3bf7-4502-a497-fa416df07612` enricher billing/complaint/2 vs verifier other/complaint/2: "So bad that i dont even want to waste my time rating this greedy application."
- `54b47181-4197-4650-ab4a-1801c0fbefd9` enricher other/complaint/2 vs verifier other/cancellation/1: "Spotify is the worst app,from the worst place,an request to play store please lock,block, or remove this app from your platform 🙏 ."
- `5590cda0-dff7-47e6-97ac-ca08852bfcb1` enricher other/complaint/2 vs verifier other/cancellation/2: "The recent updates are totally bad..☹️ I'm requesting you to please make the app like past.. Otherwise people are bound to uninstall it.. So please.. 😞😞😞😞😞😞😞"
- `55b9ab87-cae3-49ae-ae60-d9d988111528` enricher billing/complaint/3 vs verifier downloads/complaint/3: "I like listening to offline but I don't like how punishing it is when you try to listen to music when you dome pay, I've been loyal since 2018 and its been disappointing"
- `55e78c74-5e56-4a79-bc75-2f9a2190f387` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "The thing is that some songs are not available and we can't relist our made playlist by giving songs number like 1,2,3,4,5...etc that's why 2 stars deducted but other wise better than gaana or Amazon "
- `5630c138-c8ae-4d9f-b023-975f3c51583d` enricher billing/complaint/3 vs verifier usability/complaint/3: "All the options of changing song and skipping are removed such a nuisance"
- `565f96aa-449a-4fe6-8519-5daee2cd81ae` enricher other/praise/1 vs verifier billing/praise/1: "Outstanding experience and the price is just incredible for the entire family to enjoy"
- `5663677c-d4d3-4da8-89cf-ff3ba12f84d6` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Does not always play the exact music required"
- `568a8132-5912-47e7-9cb1-75fd8cece3ac` enricher other/complaint/2 vs verifier other/unclear/1: "I hate this aap . I hate Sweden. I love Islam"
- `568fcd9c-a340-4129-b08a-69a7d8415f69` enricher playback/complaint/3 vs verifier usability/complaint/3: "App continually glitches out, not allowing me to add/access my Liked Songs. Have to clear all data, uninstall, reinstall. This is happening multiple times a week now."
- `56df638a-17dc-46da-94c4-79aa4202450a` enricher usability/praise/1 vs verifier other/praise/1: "Easy to use, no problems for now.."
- `56f59df0-3480-4ebc-97ef-3cfa2c44d531` enricher other/praise/1 vs verifier other/unclear/1: "No words for the aap"
- `5705ccbf-52db-4510-aa1b-64b9a67c563c` enricher other/praise/1 vs verifier other/unclear/1: "This app is therapy and stops me from kms and is the only reason I sleep at night"
- `578f6bfd-9c4c-4943-8d63-66dfc8791ae2` enricher playback/complaint/4 vs verifier playback/complaint/3: "I use this app for podcasts mostly, but it keeps stopping on its own. More annoying than that, the screen that pops up to show the actual podcast also to pause and rewind doesn't even come up.... To p"
- `579100b3-6b77-4efb-bca3-4e6f9866ad47` enricher billing/complaint/3 vs verifier billing/cancellation/3: "It WAS a good app, until they made the basic things in the app payable....absolutely dead app now."
- `57b12dcf-c580-4ae9-98b0-234ad1f65cdc` enricher usability/complaint/2 vs verifier usability/complaint/3: "I don't like the recent update that we can play a song once 😮‍💨😤"
- `57c22c6f-81c2-44e2-bfff-6412023e97ea` enricher billing/request/2 vs verifier billing/complaint/2: "I wish you don't charge because kids don't have credit cards"
- `57d115c2-93b2-4c3a-a9c2-9554802ba513` enricher billing/complaint/3 vs verifier billing/cancellation/3: "worsttt after update very limited features in free justt uninstall it"
- `57f2180a-71b3-4059-862c-adc92aa28b6b` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Idk but if I the song I like it become weird .You see I want that song and it became other song ugh!!"
- `5813c49b-8492-41fe-884b-c2e28d025dd9` enricher catalog/praise/1 vs verifier usability/praise/1: "Love the collections."
- `58208f9e-7f19-4861-b5f0-676ef3ab16e2` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "I ended up cancelling my subscription, being frustrated with the last few changes that have been made to the app. Today I woke up to see that hearts are back and the shuffle works normal again(minus t"
- `58627b79-62a1-4eec-83b1-e1344e498ebb` enricher other/praise/1 vs verifier catalog/praise/1: "Music<good music and personalisation=spotify"
- `586cdb20-8657-427b-b685-192460fd6838` enricher usability/complaint/4 vs verifier usability/complaint/3: "Absoulty a trash app,It was not like as it was used to before.You now have listen to songs according to them(spotify) and you can't skip the songs nor go back to previous songs,you can't also play the"
- `58746d7f-1f24-488e-a2eb-56ee83db0a6f` enricher catalog/request/2 vs verifier catalog/complaint/2: "This app helps me to login and it helped me to find song and below it shows lyrics below the song.It is very interesting but some songs hide since and it shows their song clips and I'm giving 4.8 star"
- `587fe0b6-4ecb-4383-aff5-ab24723cf575` enricher other/praise/1 vs verifier usability/praise/1: "My first introduction to using this App was because someone I know was being interviewed on one of the podcasts. I am finding this App reasonably easy to use."
- `58a076a7-213e-4ba6-af8a-ec465742d1a5` enricher playback/complaint/4 vs verifier playback/complaint/3: "Since the update I can't use this on most Bluetooth devices. Also, there's never been easy accessibility to downloaded music. You still have to get on WiFi or data to get the app to show you your down"
- `592a8659-bbda-49ae-9c68-88e7c7e0edea` enricher catalog/complaint/3 vs verifier playback/complaint/3: "This was my favourite..and it is..but it's very irritating nowadays...Now it's not streaming good music even after taking a premium plan of it..Pehle hi thik tha"
- `594c4ff2-2497-4389-8bff-51150fe386ab` enricher catalog/praise/1 vs verifier catalog/unclear/1: "Downloaded this because I wanted to watch Jonathan Gaming's podcast with Mythpat."
- `598db731-b297-431a-ad30-c402f6fa32f2` enricher catalog/complaint/2 vs verifier catalog/praise/1: "It's great with premium and the free version, although they don't have all songs you can think of I like to use it's simple interface and browse new genres"
- `59c01537-5065-4b09-a4db-912300ff4495` enricher billing/cancellation/2 vs verifier other/cancellation/2: "I will not download this app again as long as I have YouTube Music, please stop sending me emails, I have unsubscribed 3 times."
- `59d3ede5-d9a5-4dea-b873-e39091d581fd` enricher catalog/praise/1 vs verifier other/praise/1: "I really enjoyed listening to the podcast"
- `59fd956f-6b9e-4941-b6b7-7c7edfe007c3` enricher other/praise/1 vs verifier other/unclear/1: "Vibe Anu chill Anu peace anu"
- `5a35ea5e-fce4-4096-972c-9b509fef792f` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "Shifting from this app due to New rules and you listen everything through their subscription model"
- `5aa04bd3-9bf2-4c86-8176-2df717390f3a` enricher billing/complaint/3 vs verifier usability/complaint/3: "Worst app , full of limitations Like only 6 skips per hour and u can't play a song that u want"
- `5adc4041-e0c7-481a-9736-50ea4a185632` enricher other/unclear/1 vs verifier access/request/3: "Hi dear friends hope you to be fine I have confront with the problems when I installed this app and my cell phone so could you help me in this problem because I'm eager to install this on my cell phon"
- `5af75251-b5ab-4d17-bde0-fac8d674e897` enricher catalog/praise/1 vs verifier other/praise/1: "Wonderful to have my favourite music at my fingertips"
- `5b0084b1-2455-49dc-ba32-3d130d87f4bc` enricher playback/complaint/4 vs verifier access/complaint/4: "New update is absolute trash. Songs play for 10 seconds then stop. After the update I can't even log into my account now."
- `5b07c0c3-f553-4019-a00b-9a9c546c9caa` enricher catalog/request/1 vs verifier catalog/complaint/2: "Wonderful app I love it and the music on it but would like more veriety of music"
- `5b1d6fd7-5d94-4795-bf17-bedcadadb277` enricher playback/complaint/4 vs verifier playback/complaint/3: "In the beginning, using this app was amazing in the first couple months i had it but then keeps playing certain songs on the list on shuffle. It pauses on its on and crashes after a limited amount of "
- `5b4e200f-58fe-40e2-b344-e9cf588703f9` enricher other/unclear/1 vs verifier other/praise/1: "❤️❤️❤️❤️❤️🤙🏻💔💔💔💔🤎❤️‍🩹❤️‍🩹❤️‍🩹❤️‍🩹❤️‍🩹❤️‍🩹"
- `5b57a101-42fc-4dd6-bf86-de1f8720aa85` enricher other/praise/1 vs verifier catalog/praise/1: "It gives a good combination of music"
- `5b63b645-4154-4ee7-90e8-0e2e5ad2acc0` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "After the last update it started suggesting Bollywood-style Indian music in my curated playlists. There's nothing in my history or location that suggests this fits my profile, let alone a playlist cal"
- `5b69bb12-faa8-46a1-94b8-5638050d24fd` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too many ads , and what's with the lyrics . It's all messed up . You watch an Ad for 30 secs and you get free 30 mins except ads goes for 1 min and after 3 songs another ad pops up. Y'all be drivin it"
- `5b761ae4-44b8-417d-96a4-ed339e1b33d6` enricher playback/complaint/3 vs verifier playback/complaint/2: "Ahh so many glitches , when I play a song jt shows nothing played but music plays"
- `5bb39436-5ee6-41db-ac81-01c3e7dd0f7a` enricher billing/complaint/3 vs verifier usability/complaint/3: "The rrcent update is the worst u cant repeat the songs would not reccomend"
- `5bd648e0-d322-445b-a2f9-c0f404f764b6` enricher usability/complaint/3 vs verifier usability/complaint/2: "Far too keen to play music you haven't asked for. Stop that. Now."
- `5becd61f-50bb-4424-bda6-454a528d748d` enricher billing/complaint/3 vs verifier usability/cancellation/3: "This used to be a really good app but it's just deducting all basic features. I mean "add to queue" option is missing in the new update and it has become so annoying lately. The only way it can be cur"
- `5c1f67d8-8bb2-4974-b848-8c78dfefb816` enricher catalog/complaint/4 vs verifier playback/complaint/3: "Can't even search without the app crashing after the latest update."
- `5c299c2d-5e33-437f-84d9-08542eca8871` enricher usability/complaint/3 vs verifier usability/cancellation/3: "Very bad and irritating experience using this app lately so many ads unnecessarily popping up. shuffle, rewind and repeat these options vanished since the new update makes it difficult to listen to th"
- `5c3c5366-38a8-47a2-99dd-249e45685e16` enricher billing/praise/2 vs verifier billing/complaint/2: "Debería ser gratis pero guapa la app"
- `5c513e2b-4eda-4a05-82ad-0eab320ab791` enricher billing/complaint/2 vs verifier other/complaint/2: "Waste but can't avoid"
- `5c53cc04-d568-4423-9c24-85967b51d239` enricher usability/request/2 vs verifier usability/complaint/2: "Please avoid negative ads just beacuse you want to convert people to premium."
- `5c6f89ca-48f9-464f-8006-4ea1f1affd10` enricher other/praise/1 vs verifier catalog/praise/1: "Music is always available when I need it."
- `5ca01360-2afc-40bf-aa57-5ccc85ba7d69` enricher downloads/request/4 vs verifier downloads/complaint/3: "okok I had it originally as five stars, but it made me realize so. good app, yes. but when I had no internet, I couldn't play my downloaded liked songs. idk it was weird. but also, there should be an "
- `5cbc9acd-8d44-4719-9409-b40ad0db4211` enricher billing/complaint/2 vs verifier billing/complaint/3: "The new update is worst It's like ur are forcing ur customers to buy the premium which is not good"
- `5cc6c1e0-4740-4625-8cdf-f45e5ffac890` enricher billing/complaint/3 vs verifier billing/cancellation/3: "Now the things they are doing to a person to make him buy premium is really getting worse day by day.. earlier lyrics were shown for most of the songs but now "buy premium to access lyrics".. I can't "
- `5ceb9a8a-d715-4c49-b890-96da99cdf570` enricher catalog/praise/1 vs verifier other/praise/1: "This app is amazing super songs and also trending songs in this app super app for music😍"
- `5d00a0fd-b169-4128-bbac-0cd66a69720c` enricher playback/cancellation/4 vs verifier playback/cancellation/3: "Spotify stops after one song every single time I get back in my car, even if it's only stopped for a few minutes. The only way to continue is to open the app and choose a new playlist to start again. "
- `5d387cb5-d339-41d0-9bc3-6b31ab0b2be6` enricher other/unclear/1 vs verifier other/praise/1: "good but😗"
- `5d6b14db-49a7-45b0-b14f-98a5699a7935` enricher downloads/request/1 vs verifier downloads/request/2: "Everything is fine but bring offline song on liked song."
- `5d722980-984a-47f9-ae00-1bd56b4cbc4e` enricher playback/cancellation/3 vs verifier usability/complaint/2: "Spotify kind of sucks it won't let me play any of the songs I saved on my playlist you know a couple of Skis it's kind of annoying so I don't really like this app I think I'ma stick to Pandora because"
- `5d7a3e89-da5a-4af1-9559-d077a7187724` enricher other/unclear/1 vs verifier other/praise/1: "Full support from 🇮🇳 🇮🇳"
- `5db59cbb-0d0c-4f0e-b650-6bf5bcdc6157` enricher billing/complaint/2 vs verifier billing/praise/2: "It is good and more if you pay for it.But you have to pay for it because it has very good benefits and at the same time it is a bit unfair to pay but it is worth it if you enjoy music since it has ver"
- `5e23c05c-cfd9-404e-a329-7342e88f7ca4` enricher other/unclear/1 vs verifier other/cancellation/1: "This is very important news I'm boycott your app"
- `5e34dddb-25fe-4061-a1db-e339d549ed9c` enricher other/praise/1 vs verifier billing/praise/1: "It's overall just pretty good even without premium"
- `5e5e44e7-a326-457b-8573-9978f44a6687` enricher usability/complaint/2 vs verifier usability/request/2: "I like this app most I love this thanks to @team Spotify please fix ads issue getting more ads thanks Team Spotify!"
- `5e620d90-a4ea-4314-853c-f6b862db0455` enricher billing/complaint/2 vs verifier billing/complaint/3: "Always asking for 399 pack n all song is not giving"
- `5eb731f5-5111-4223-9d9d-379fc1ce11d4` enricher usability/complaint/3 vs verifier usability/complaint/2: "Dude why the hell should I pay to listen to music with this app there are so many different apps that guess what free look free don't have to pay for music it's amazing how who knows maybe because it "
- `5f098dae-e170-4eb0-8b57-99a5e12404f1` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "The new home screen/news feed is awfull and unnessessary. Spotify was great at providing easy access to a great range of music and new content through radios and daily lists etc, leave the algorithmic"
- `5f7f950c-cd45-4ae1-9680-19217944a031` enricher playback/complaint/3 vs verifier usability/complaint/3: "'Was' Best app for music but after it got updated in my playlist random music plays on its own the order is no more maintained even after using the queue mode nothing is happening. To much ads keep co"
- `5fb44442-3a4a-4115-88d4-b65d9c5dec02` enricher other/complaint/2 vs verifier other/unclear/1: "Bikod spotify"
- `5fbf862b-11a3-4aa4-9a65-408cddda240c` enricher other/complaint/3 vs verifier downloads/complaint/3: "Doesn't update as a mobile app, old playlists and no downloads. Considering I use this application on other devices I expect across the board for my settibgs to be equal. I create a playlist on my com"
- `5ffb392d-4406-47d5-ba09-7f0ca2da7988` enricher access/complaint/4 vs verifier other/unclear/1: "Ismam all pepole this app suspend"
- `60120410-496f-4e9d-bf22-3acff1165e41` enricher usability/complaint/3 vs verifier usability/complaint/2: "It is not a music streaming app, it is a ad streaming app"
- `602103a3-51d1-4324-b565-87f646c53194` enricher usability/complaint/2 vs verifier usability/cancellation/2: "Its a okay app but there are not enough skips and its been well over an hour and i don't have them replenished and there are too many adds. This app has gone downhill. For everyone that doesn't know w"
- `604277de-8e3e-43ec-b3eb-d926b08f8423` enricher catalog/praise/1 vs verifier other/praise/1: "Mad about Spotify, have never done a search that has not delivered. Made a huge impact on my life, streaming, playlists,Made for you, all services. I love Spotify."
- `6060fecc-75ff-4a73-916c-60e03ba02043` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Worst app you need to pay for nassenecessary things like loop list, you can't forword any songs and the quality of the songs is worse."
- `60d1ecc2-2bd2-4f84-b31a-259b3c1676c4` enricher other/unclear/1 vs verifier other/complaint/2: "Nalla nalla nalla nalla samjhe kya bro ye language bahut bekar app hai"
- `61337d52-79ab-4e25-ae8a-d5d6698771df` enricher other/complaint/2 vs verifier playback/complaint/2: "It takes up so much data and I cannot turn it off just keep playing"
- `617103e5-1ceb-482a-a308-f13c78969fc6` enricher usability/complaint/3 vs verifier usability/complaint/2: "Prefer it over Pandora... For now! Edit:Way too many commercials now... More than Pandora. Lost my #1 spot for sure..."
- `61713112-f8ee-4743-9a73-0f04596efa4d` enricher other/praise/1 vs verifier catalog/praise/1: "👍🏻 Spotify Rocks! They've got all my Faves ♡"
- `627f56e6-ed6f-4824-bf21-717a17274988` enricher billing/complaint/3 vs verifier usability/complaint/3: "It feels like Spotify is forcing me to buy premium. I can't remove the shuffle and the queue option is gone too. I keep getting ads after every 3 songs too."
- `628b6a5d-5f37-41bd-83f1-97969e942371` enricher access/complaint/4 vs verifier access/cancellation/5: "I m unable to login with my correct phone no. It is showing "wrong phone no, try againg ".I have cross checked many a times but found no solution.all my data of that account vanished😢. Now i m just sw"
- `62ad5c13-dbe2-4ef6-8141-240bc9f05f7a` enricher other/complaint/2 vs verifier other/unclear/1: "Me to spotify rating: Jaldi yahan se hato. Utar tohri mai chodein."
- `62f6881a-8526-447e-902a-a1a1a863a348` enricher other/complaint/2 vs verifier other/unclear/1: "Bucky this app"
- `62f69c1d-2fae-4a00-a52a-3f27f70a65be` enricher catalog/praise/1 vs verifier other/praise/1: "It is a really great app for music it contains all the music and creators i like it"
- `63495200-369d-41f0-ad84-3783346019db` enricher playback/complaint/4 vs verifier playback/complaint/3: "Latest update has caused the app to freeze or not load playlists and songs repeatedly, have to close the app sometimes multiple times to get anything up"
- `635fbc9d-7d8d-47ff-b502-40753cdbad3e` enricher catalog/praise/1 vs verifier other/praise/1: "l like the music so much"
- `6392db0d-0451-452a-827b-106fb2fe2009` enricher usability/praise/1 vs verifier other/praise/1: "this app it so very very nice we dont have a advertice"
- `63b19971-dd58-4aa4-9550-e8d8d71f7b26` enricher playback/complaint/4 vs verifier playback/complaint/3: "App just stop working after two days, can't do anything after date"
- `63ca7a03-2c62-4d41-973a-09cda3a006f1` enricher usability/praise/1 vs verifier billing/praise/1: "Awesome. Music verity and now just need ad free"
- `63d89656-0125-4b48-8ca9-280144cfc259` enricher billing/complaint/3 vs verifier billing/request/3: "This used to be the best music app but now the basic features are locked behind premium I really like this app so pls just change it to how it used to me so me and many other users don't shift to anot"
- `63f14c8d-0aa1-4def-9ffd-3f7b303e45e5` enricher playback/complaint/3 vs verifier usability/complaint/2: "Worst I cant listen to a song w/o its playing another song"
- `641ab302-a5f5-4e76-95f0-812e3301a2c9` enricher other/complaint/2 vs verifier other/unclear/1: "I hate spotify. I hate sweeden. We love islam."
- `64335604-9931-489b-8261-1adb3bc98d19` enricher billing/complaint/1 vs verifier billing/complaint/2: "If is free it would be greatest thing that happened in last hundred years"
- `643b0cc1-c5d5-4332-9957-439c0b21ef20` enricher other/complaint/2 vs verifier other/cancellation/2: "This app is using foul, and misleading practices for promotion. Keep away"
- `64a5f464-8480-4450-83fb-f88a1659f189` enricher downloads/complaint/5 vs verifier downloads/cancellation/5: "The ones I downloaded lost the price I paid for and then just disappear!! Scam"
- `64ac1d6b-6ced-40e9-ac98-d816cd1ec7ed` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "The new update is disgusting and so controlling. You just can't play your favorite part of the song, can not play the previous song, can't check the next song, and doesn't play the songs in the proper"
- `64ad7653-2b51-4778-aa20-deead468e1ca` enricher playback/complaint/4 vs verifier access/complaint/4: "Past few days it won't even open!!"
- `6587f338-8f46-4574-9258-b9c5e0342890` enricher catalog/complaint/4 vs verifier playback/complaint/3: "Podcast videos not working"
- `658c6511-91c3-42da-a89e-d3565d5e8789` enricher playback/complaint/3 vs verifier usability/complaint/3: "I like the app. However, I have over 100 songs on my playlist and when I shuffle it and listen, it plays the same 10 over and over. Then goes completely away from my playlist. It would be nice to hear"
- `65b21bbc-3b75-47b0-b1a5-62c675b8c8fb` enricher usability/complaint/3 vs verifier billing/complaint/3: "I can't even play the last song nor can I go back to start of current song and the Playlist is on random like WHY!? I don't have complains for ads or anything but just don't kill the customer base and"
- `65e39bfd-7ec3-474b-a309-6b009b20746f` enricher billing/complaint/2 vs verifier billing/complaint/3: "Why is Spotify saying i am not eligible for a single account plan? Can you explain? I have to pay unnecessary extra money just access your plans, cause the only plans available for me is duo or family"
- `65fd207d-3466-4aeb-a0da-65bf83346858` enricher usability/cancellation/3 vs verifier billing/cancellation/3: "Its was the best app till now but it became worse after it's new updates it ruined all my mood.we cannot jump to a specific part we want to listen. We cannot listen one music again. It become really w"
- `66762fc0-3dcf-41c6-ab24-d953795c26eb` enricher playback/praise/1 vs verifier other/praise/1: "I love this app so much it's bearly glitchy and always has the songs I love! I highly recommended this app and hope you can enjoy as much as me!"
- `66a0df8d-7c4b-4c4d-bbda-41db0d7f3101` enricher usability/complaint/3 vs verifier usability/complaint/2: "I don't mind a few ads. I'm on free, I expect it. I do mind that I get 3 more ads one song after a sponsored ad saying there are 30min ad free. This is constantly the experience now. Your algorithms a"
- `672ce544-5834-4731-bd58-b578868c6ea7` enricher usability/complaint/2 vs verifier usability/request/2: "Why that is no sleep mode feature anymore. Pls rectify this issue. I have been using the apps 5yrs"
- `67465fe0-d64d-4c94-adfb-c18cf5b17558` enricher billing/complaint/4 vs verifier downloads/complaint/3: "U have to pay premium before u can enjoy the music . No downloading at least make the app offline if I have to pay premium"
- `67788933-9b7d-4e82-a7df-cb5b1a95dabd` enricher billing/complaint/3 vs verifier billing/request/2: "Pay 2 use app adding repeat as an premium option"
- `67835dbd-10ac-4325-b93e-453d1bd5ec36` enricher billing/complaint/3 vs verifier billing/complaint/2: "Why do guys need so much money, like tff just basic things have been done premium now shameful."
- `678bc099-9fbd-4986-b3c9-44cb89bdb2a2` enricher usability/complaint/3 vs verifier usability/complaint/2: "Very very very very high advertisement bad app"
- `67ad965d-a86c-4d1b-a20a-a2c46bb98e74` enricher usability/request/2 vs verifier usability/request/1: "Just reduce the advertisement"
- `681a5be0-d272-4537-8b1d-feb97724ccc6` enricher downloads/praise/1 vs verifier other/praise/1: "Very good app. The dj option is awesome a very fun way to hear new music. Being able to download all your favorite songs is a big bonus for those camping trips or places with no cell service. The prem"
- `681aef2e-d8ba-49aa-8960-f36589b98b8b` enricher downloads/praise/1 vs verifier playback/praise/1: "Premium can play music without wifi🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩🤩😯😯😯"
- `6880276e-3dc8-4430-8ee3-2c74097b1eaf` enricher catalog/complaint/3 vs verifier playback/complaint/2: "I would have given 5 stars if the duo Playlist actually worked."
- `688cd6bd-d696-4db2-a8b8-dae533a8c067` enricher usability/complaint/2 vs verifier usability/cancellation/2: "I used to love Spotify, and if they lived up to their original concept and put their profits into paying per stream, I still would, but they instead spend hundreds of millions on getting podcasters on"
- `68cc05cc-b7c1-484b-aa70-5c1cb66d6abb` enricher usability/complaint/2 vs verifier access/request/1: "Could be easier set up"
- `68d86091-8b0a-4c3e-8c04-950ae4eb14bf` enricher catalog/complaint/2 vs verifier other/complaint/2: "Updated two times, still can't see my Spotify wrapped"
- `68e5cda4-386c-48f8-acf8-e0f6e426be82` enricher catalog/praise/1 vs verifier other/praise/1: "I love tgis is free and so many song it's awesome"
- `6904fe4f-4715-44ec-9460-b09746921559` enricher catalog/praise/1 vs verifier playback/praise/1: "Music always there when I need it!"
- `69118058-9209-4479-add2-684ddde152a8` enricher usability/complaint/3 vs verifier usability/cancellation/3: "Spotify is going down day by day. There are hell number of glitches and now you can't even add songs to a queue?! Seriously?!! And now the ads, they have increased so much. Now we can't even rewind so"
- `69231c65-49b0-439c-a4dd-5f108625a5c3` enricher other/cancellation/2 vs verifier other/cancellation/1: "I am switching to another music app"
- `6933c5ff-5266-4fe6-8cf8-42e5eb9e4980` enricher usability/request/2 vs verifier usability/request/1: "Love Spotify glad it comes with my Verizon service! I'm glad they've done video for for podcasts as well! I just need them to make a pop out video feature when putting the application in the backgroun"
- `6973ffd2-6cfc-4492-a073-8857d41268a9` enricher other/request/2 vs verifier other/request/1: "Just a feature i would like if this app comes up with the data ,like it takes a lot of data"
- `6989561e-f3cd-4551-87cc-7aaada811b8e` enricher other/unclear/1 vs verifier other/cancellation/1: "If you want alternative of this app, wynk is an option."
- `69f2a23c-f5e1-4975-98ef-d02264a15606` enricher other/complaint/2 vs verifier other/unclear/1: "Worth off"
- `6a28142c-1e1a-4469-b790-d73933cb7807` enricher usability/complaint/4 vs verifier catalog/complaint/3: "Lyrics have disappeared since the last update and been replaced by 'recently heard ads'. Please fix this! As a hearing impaired user, lyrics are essential."
- `6a283b95-7084-43c3-96df-cc417c2e1119` enricher billing/complaint/2 vs verifier other/complaint/2: "I don't care for it. I have YouTube premium"
- `6a37f185-46fa-4d1a-8600-8e8e8ec1496f` enricher catalog/praise/1 vs verifier other/praise/1: "It's the best app everyone should install. Music play list is endless"
- `6a708772-b03f-4895-8d89-187427bde73a` enricher other/complaint/2 vs verifier other/unclear/1: "go to hell swerdan"
- `6a98ee7f-af2e-4d1e-b4a2-27536dca19fc` enricher usability/cancellation/3 vs verifier playback/complaint/3: "The older update was good. Well now, Spotify doesn't support streamline listening. In the free version, you can't queue up songs, there is constant shuffling disrupting attention, again and again one "
- `6ace5d1d-f3b8-495d-853b-b8cdac4f6aef` enricher playback/complaint/4 vs verifier playback/complaint/3: "When im playing a game(most of time)later on the music stops & takes off & I have to click the play button & when I do it restarts the whole song & when 2 songs pass it does it again & I have to leave"
- `6aebf533-653a-41f0-9755-578ef374cebc` enricher support/praise/1 vs verifier other/praise/1: "Thanks for the help got me back on"
- `6b2714e1-d13a-4689-8255-d5712d2b9bc7` enricher usability/complaint/2 vs verifier usability/complaint/3: "It was my favourite app but now it's very annoying we can't listen to music the way we want it feels like we are getting controlled"
- `6b3607af-6690-4e31-bc2b-5174419f1084` enricher billing/cancellation/3 vs verifier usability/complaint/3: "The latest update just doesnt let me go back to previous songs or skip to the favourite part of the songs , And the app is playing random songs EVEN IN MY LIKED SONGS . I seriouslly feel like i need t"
- `6b383d59-ade1-404f-95fb-31d7e6e9e311` enricher billing/complaint/3 vs verifier billing/complaint/2: "Initially it was good but now it will force to buy primium and not worth in free version"
- `6b68443d-b798-49d7-9855-0b9e9dcd6842` enricher other/complaint/2 vs verifier other/unclear/1: "😤😤☠️"
- `6b716cb2-4c97-4d89-91bc-0dacc6a1cd42` enricher catalog/complaint/3 vs verifier downloads/complaint/2: "I got a premium account i noticing a lot of Songs desapearing literally half of my list they should add like a multi deleting option cause sometimes you can acidently add the same song twice at your l"
- `6b723a94-bd89-4f63-9cf4-8c8a3b72ba62` enricher playback/praise/1 vs verifier usability/praise/1: "I like how you can smoothly move between your devices."
- `6baf0378-bbc2-48c3-badf-db6958c1882e` enricher usability/complaint/2 vs verifier catalog/complaint/2: "Too many political advertisements when the podcasts are on non political topics. Keep your personal opinions and bias to yourselves."
- `6bf02cc6-e707-40c2-9bd9-5824783b9b10` enricher downloads/request/2 vs verifier downloads/request/1: "Good music and good songs but if we can download or save the music we love it for free will be better"
- `6c71dcb7-c818-429c-bdca-d2bfff197f11` enricher other/unclear/1 vs verifier billing/complaint/2: "Hoy Arby Penaflorida magtrabaho ka kasi para may pambili ka ng Premium libre na nga demanding ka pang kupal ka hahaha XD"
- `6ca5fb0f-23fa-44a9-97ae-0f2f91b1b493` enricher billing/complaint/4 vs verifier billing/complaint/3: "All options have been turned premium. No sense of playlists at all now because songs don't play in order. Has turned into the worst app ever. Very disappointed"
- `6ccd45da-4447-473b-b98b-2a84065bf46a` enricher usability/complaint/3 vs verifier other/complaint/2: "Love the functionality of this app. Easy to find podcasts/music. Make playlists, save liked songs to own playlist, etc. However, I'm so SICK of the electric vehicle agenda being pushed on me! If I hav"
- `6cff9dd9-c3c6-4f34-8019-9dd610e2a2f7` enricher billing/complaint/3 vs verifier usability/cancellation/3: "Everything was fine for past few years of me using Spotify until I recently updated... that is.. the new updated version doesn't let's u shuffle the songs the way u want..u can't make your own queue y"
- `6d00c70c-45b3-4318-951a-fd7704451340` enricher other/request/1 vs verifier other/praise/1: "I love Spotify so much send me a VIP because I love your app 389/10"
- `6d06d203-b2f6-4f3e-bb97-396298728da3` enricher other/complaint/1 vs verifier other/unclear/1: "Cannot give 0 so 1"
- `6d112595-882b-481f-bc8a-a945b11086fe` enricher other/praise/1 vs verifier other/unclear/1: "🎧❤️‍🩹"
- `6d295e74-aad5-498c-9c75-dcebeeac1006` enricher usability/complaint/3 vs verifier other/unclear/1: "Song ka app he Kay add's ka khatam hi nahi hoti."
- `6d390539-6adc-4e46-8492-3f2c67930a4f` enricher billing/complaint/3 vs verifier billing/cancellation/3: "The most useless update ever no basic feature and every thing needs premium .I am using it for 1yr but it was good and my favourite app'WAS' did you say the word was?it means that it's not the best mu"
- `6d654fdd-f3cc-4696-bd16-0342a40ebe77` enricher other/praise/1 vs verifier other/unclear/1: "Good. Now don't do anything absurd again. 👍🏼"
- `6daf49b2-b369-4d01-95ea-7d9d2f3ec138` enricher catalog/complaint/3 vs verifier catalog/cancellation/3: "Consistently I've had problems with Spotify. What gives them the right to decide whether or not my location can listen to podcasts. I'd rather steal their info from other libraries than pay for their "
- `6e0d976f-297e-487c-95ec-117f0f770a0f` enricher usability/praise/1 vs verifier other/praise/1: "I had ever seen this different app before. -- This music player played with lyrics and some gif ----- This is the best music player app"
- `6e24c697-f073-4ab9-b8b9-fd9b1ed4504f` enricher downloads/unclear/1 vs verifier downloads/request/1: "Isme offline player la o"
- `6e84ac60-906f-45cd-90e4-cb5b6bde92b0` enricher billing/complaint/2 vs verifier billing/request/2: "Spotify does not recognise my college so apparently I'm not a student. Please fix the Spotify premium student to have a better id system such as student beans as I cannot afford the full membership."
- `6e934182-3cd3-49e0-853f-d849c9adb9e3` enricher other/praise/1 vs verifier catalog/praise/1: "It is the best for BTS armys"
- `6f8b1b0b-d66e-4c76-a521-da91989a2e00` enricher billing/complaint/2 vs verifier billing/complaint/3: "The package that says for students is only for the university where I'm in high school, so having to buy a non-student price and get , a free account is pretty bad.At first I really liked listening to"
- `6f8fcd20-db30-42cb-9f11-88d620157162` enricher usability/complaint/3 vs verifier billing/complaint/2: "Why you made free versions when there are 2-3 long ads after playing just one song"
- `6f95425b-bcb4-4788-88ec-5064bcd877f9` enricher playback/praise/1 vs verifier other/praise/1: "Once I deleted and re-downloaded everything works great"
- `700b94c5-3146-44a0-8e38-deac8502ef1f` enricher billing/complaint/3 vs verifier usability/complaint/3: "2.5 ⭐ (rounded down) On PC, Spotify is fantastic. Able to find songs and enjoy listening to them while doing work or relaxing. Ads on PC are acceptable while considering the Premium option. On Mobile,"
- `70186991-6789-4e43-8124-148550fba2a5` enricher usability/complaint/2 vs verifier usability/request/2: "Why yall change the player format and put the title of the song on top of the album"
- `7067dede-7d5e-4ad8-bb1b-16d0e32f8895` enricher other/praise/1 vs verifier usability/request/1: "Fantastic, Wish you could have unlimited following for artists."
- `707ced2f-8abe-423a-ba16-6218d7b53d66` enricher billing/praise/1 vs verifier other/praise/1: "With premium it's very good music app"
- `708bc543-a7ae-4fec-bfb8-2787825ba295` enricher billing/request/3 vs verifier catalog/request/2: "Hey Spotiy Not everyone can buy PREMIUM so PLEASE bring back lyrics or else 😈😈"
- `709b1d34-0f02-471d-a329-914f24074961` enricher billing/complaint/3 vs verifier usability/complaint/3: "Not a fan of it. Design doesn't look as good as Apple's. 5 skips in the free version is just mean to be brutally honest. When I try to open an album... it doesn't open, instead it opens something wier"
- `70c24b0d-301c-4a2e-a5a9-f5f35110d981` enricher billing/complaint/3 vs verifier playback/complaint/2: "Still a amazing app Im a music lover and it gets glitchy at times recently the app needs improvement though I regularly pay for premium but it got me in duo which I didn't want."
- `70c49ed0-a207-433f-9618-a762abe0fe7a` enricher playback/praise/1 vs verifier other/praise/1: "Love being able to have my music with me everywhere."
- `71080b9f-f95a-47cb-8650-d2b4babb4039` enricher other/complaint/2 vs verifier billing/complaint/2: "I have Been using the app since few years, This app has become from best to worst. Spotify doesn't respect it's loyal users."
- `71215b2b-a91a-4a83-adde-68022e3e3b6e` enricher billing/complaint/4 vs verifier billing/complaint/3: "I hate the new update in it. Now you can't listen to any song on this app without having premium."
- `71252e73-4660-4f0a-921e-1bbfd8f2e8ff` enricher usability/complaint/2 vs verifier other/complaint/2: "i hate the new update."
- `714173ef-3678-4b45-bb9f-bbe677ce9ee3` enricher playback/complaint/4 vs verifier playback/complaint/3: "Please just make it work, I need to switch services specifically because of how bad this app is. Flip 4, crashes, bad downloads, connection errors, smart device errors, songs that stop and skip with p"
- `715e7a71-4f46-4b0e-8d26-6641e1e89fc9` enricher playback/complaint/2 vs verifier playback/complaint/3: "I like it but I gave it 3 stars because everytime I play a song a different song plays. More functional on pc."
- `7167313c-241f-4555-8cd3-18ae5eb5fb52` enricher downloads/complaint/3 vs verifier downloads/request/2: "Spotify is a great app to listen and thay are multiple songs but there is a problem Download playlists. We have to get premium which we pay p/s make download playlist free plan to spoify or makes bett"
- `718bbb0b-de5f-43f0-b0c7-f0cb0969c92d` enricher usability/cancellation/2 vs verifier other/complaint/2: "New update terrible. If I wanted Instagram or tiktok I would use those apps. Spotify was supposed to be for music."
- `71bb5220-71e1-4f6c-8cb3-8577890ee89a` enricher other/praise/1 vs verifier downloads/request/1: "Best app plzzz download"
- `7249e791-ba30-4abc-b8e2-4a56e885ad3a` enricher other/complaint/2 vs verifier other/unclear/1: "How dare you burn our QURAN😡😡"
- `72829629-4d9b-4917-bcc1-05c9aa60686c` enricher usability/request/1 vs verifier usability/request/2: "Please add a dislike option in Spotify app because if you did not like song you should have option to dislike the song , so please add this option Thank you and please reduce the quantity of ads"
- `72865a7e-3317-4a4a-9d42-80650b748664` enricher catalog/praise/1 vs verifier other/praise/1: "Honestly the best decision I ever made in regard to music & podcasts. I run every day and would be lost without Spotify. I use it daily for interesting new podcasts or curated playlists for my runs. ("
- `7296e19f-0401-411d-af60-15878bde507c` enricher playback/praise/1 vs verifier other/praise/1: "Great sound quality and a wide range of music suggestions offered."
- `729c20a9-02ba-4011-98fd-b418fb89e630` enricher billing/cancellation/3 vs verifier playback/complaint/3: "Spotify has become so annoying lately I don't recommend downloading this app at all you can't even listen to songs of your Playlists you can't skip a song you cannot listen to a part of song even you "
- `72a3d84c-baa2-437e-9ecc-e39df67d98f8` enricher other/unclear/1 vs verifier catalog/unclear/1: "Listan a lot of sing"
- `72d47c12-26fd-49c0-a05c-78bc59aae3de` enricher catalog/praise/1 vs verifier other/praise/1: "Every song you can imagine and u can make amazing play list. No commercials."
- `72e985df-53a9-408b-bb4f-dd0c106a7eff` enricher other/complaint/2 vs verifier access/complaint/3: "I love it 🤩🤩 the same time I'm trying to make my own song but it won't let me even though I putting in my own Spotify password I am starting to hate this fix this now 😡🤬🖕🏻"
- `7366eb18-8f71-4975-9cc1-53efc79a6cb8` enricher other/cancellation/2 vs verifier other/complaint/2: "Updation k bad ab iski rating giregi. Or most of the people app ko uninstall krege. We're not satisfied with this updates."
- `7379aeee-0daa-4432-b693-14b8d149e56a` enricher usability/complaint/3 vs verifier usability/complaint/2: "They will say you are going to get the next 30 minutes of music without any advertisement or interruptions yet viola and you barely had listened to two songs and there creeps in two 30 seconds adverti"
- `73f1a35f-7b89-4e60-b528-ea0b8d298067` enricher usability/cancellation/3 vs verifier usability/complaint/2: "This is way out of line. Ur ads R too much ! I feel lyk unistalling it now. If yall reading dis (spotify) plz despite da absurd amount of ads fr those non-premium customers, atleast make it according "
- `74227c7c-120e-43a1-9161-719695720d44` enricher billing/complaint/3 vs verifier billing/complaint/2: "Thay are making everything premium."
- `74a32ff2-8850-474b-b9d6-af92041eaa97` enricher other/unclear/2 vs verifier other/unclear/1: "Literally!!! 😒😒"
- `74aa8615-95b6-412c-af31-12b29d73b661` enricher other/cancellation/2 vs verifier other/complaint/2: "Duck this app ,"
- `74c9bb31-b0be-48b0-9892-2fa8934df4c3` enricher catalog/praise/1 vs verifier other/praise/1: "Great music choices great listening old &news music 🎼 Hank you Spotify😊"
- `74e89260-0fe6-43ee-a38f-2f08899b795e` enricher playback/complaint/3 vs verifier usability/complaint/3: "Very bad experience nowadays can't listen to the part of the song worst update ever👎👎👎"
- `7515744b-6b14-47c6-ba8c-c25e00ddc41b` enricher playback/complaint/3 vs verifier playback/complaint/4: "The malfunctioing of the app is completely annoying. Recent updates have been that the app just can play one or just two songs, and then just stops and I can't play nothing else"
- `752320d6-291a-4dc7-85e5-68a7a47468b5` enricher billing/complaint/4 vs verifier downloads/complaint/4: "I paid for Spotify Premium a few months back, but it won't let me play or download FULL songs. I CAN ONLY PREVIEW songs... I uninstalled, re-installed but the issue still remains."
- `75285c79-6841-4691-86f3-437bc09c28a7` enricher playback/praise/1 vs verifier other/praise/1: "Amazing.. Best for sound!!!"
- `758fd733-797c-4c7d-87f0-ecfffba3eb99` enricher billing/complaint/3 vs verifier billing/complaint/2: "Seriously??? You can see the lyrics on premium??? What kind of update is this??"
- `75a88a59-66c3-42c7-8a49-2239715e683a` enricher usability/complaint/3 vs verifier usability/complaint/2: "Why I cant repeat the song? When the song end, randomly song are played 😤"
- `75bccb29-2280-441c-a8c2-42281dbcb7d8` enricher billing/complaint/3 vs verifier billing/cancellation/3: "Eh it was good the first week and that's it. After one week of making an account I noticed that you need premium to about anything to control what music you want or else it will choose for you If I ma"
- `75dca6d9-ac67-4412-96f6-b842a100c1c0` enricher billing/complaint/3 vs verifier billing/complaint/2: "Worst app only after money."
- `75f1696a-ffd4-432b-9d7d-2c98e129eda1` enricher other/complaint/2 vs verifier other/unclear/1: "I'm too lazy to write everything out but do better."
- `76698770-61e0-4322-8024-0d92d169b5e5` enricher playback/complaint/3 vs verifier other/complaint/2: "Very poor quality"
- `76a49c52-41f8-43ef-abce-970a6dce1824` enricher billing/complaint/2 vs verifier other/complaint/2: "Beakar hai paisa mangte hai har baat pe"
- `76a9fbd9-5351-442a-816e-e292d3d4a199` enricher catalog/praise/1 vs verifier other/praise/1: "Wonderful collection of music. Enjoy anytime, anywhere."
- `76ceba23-bac1-42d7-91fa-a637f360631a` enricher catalog/complaint/3 vs verifier access/complaint/3: "What is the point of making playlist if you're just gonna put songs that I didn't even want?? Sometimes it signs me out whenever I accidentally remove it from the recent apps and it will failed if I t"
- `76cfa29b-e3b0-46bb-a7aa-7872aee511ed` enricher other/complaint/2 vs verifier other/cancellation/1: "I love this application but ,this application of sweden and they did unprofesion and very bad things burning of Quran so i am buycoting this application.."
- `76e89d46-8484-4466-85cf-3d1b751327dc` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "It has been long time since I used Spotify but the recent update of Spotify is really make me uninstall this app. Without premium I was listened one song repeatedly. But now neither we can change the "
- `76ed4a62-1e1f-446a-8403-6bb216b21882` enricher usability/complaint/3 vs verifier billing/cancellation/3: "I am starting to hate this app update by update. Now it is just becoming pay to listen type of app. First they make ads appear frequently after every 2 songs or so and then they increase the number of"
- `77020249-b252-42c9-8217-bbb22a6d94e9` enricher usability/complaint/3 vs verifier usability/complaint/2: "Ads issue to much"
- `77073e6c-b323-40d8-aa40-a47e57c846fd` enricher usability/complaint/3 vs verifier usability/request/2: "In new update there is no scroll bar to move the song , and rewind, previous track option disabled pls vring it back."
- `7731b046-f8b3-424f-9027-af3a1109dfab` enricher catalog/praise/1 vs verifier other/praise/1: "Great app for planning song"
- `77853cc4-35c0-46c4-bd57-69968c1c1b11` enricher playback/complaint/3 vs verifier playback/complaint/4: "It keeps crashing on my divice"
- `77afcd48-db06-4fdf-a101-ca54ee7e3138` enricher usability/complaint/3 vs verifier billing/complaint/2: "very ads, need only money"
- `78077e72-ebd2-4965-9b68-ae53e7509d3e` enricher playback/complaint/3 vs verifier playback/cancellation/3: "Earlier it was amazing... music sound everything was just great 👍 But now from last 2 weeks....saare songs 1-2 min ke ho gaye hai..why? My playlist contains all my favourite song...jo mai daily basis "
- `781807fa-1dab-4915-9a59-e871aba935e7` enricher other/praise/1 vs verifier other/unclear/1: "I've had Spotify for years and I love the app not perfect but what is"
- `783ac4dc-adb3-40c4-a127-9aef67bed69d` enricher billing/complaint/3 vs verifier billing/complaint/2: "This app has became pay to play."
- `7865a05f-6e3f-4710-a9a5-b12e20eb98f6` enricher catalog/complaint/3 vs verifier billing/complaint/2: "Now premium??!!!! I used to love Spotify when it had every song .. and lyrics as well ... Now upgrade to premium..I hate it"
- `78c7e210-3a22-46ab-b397-898204bef8f1` enricher playback/complaint/4 vs verifier playback/cancellation/3: "Spotify app is completely broken on android, playlists stop playing and switch to a radio station at random times and the control bar for music disappears after not using the app for a few minutes. On"
- `78d65924-c32e-479f-ba91-1193e794544f` enricher other/complaint/2 vs verifier usability/complaint/2: "This app was top notch but after every update they remove basic features. This latest update is the final nail in the coffin."
- `78d9954c-5f6d-4193-88dd-e2a57d9d5b9b` enricher other/praise/1 vs verifier playback/praise/1: "Spotify has Amazon and YouTube music beat by a zillion miles. The sound is seconded to none. Keep up the good work. YOU ROCK!!!"
- `79694b14-5b24-4f66-a5cc-bafc421c12b0` enricher usability/cancellation/3 vs verifier usability/complaint/2: "This is useless application, advertisements keep coming again and again and we can't even skip, they are forcing you to get membership, please stop this app"
- `7989ebe0-14ed-4d9b-8016-3acc6a1ce2e7` enricher playback/complaint/4 vs verifier catalog/complaint/3: "I have been experiencing this issue that whenever I open Spotify and even try to start my search for a song or podcast it show me network error. I don't know why it is happening but one thing is clear"
- `799a19f8-bf67-4643-98ea-22d216488ad2` enricher catalog/praise/1 vs verifier other/praise/1: "I love this app. I haven't been on this app or on the podcast my homie RADIO and Shaggy do called THE PALCAST."
- `79c9fb60-7d1c-4b43-9e5e-11b484760e7c` enricher other/unclear/1 vs verifier other/praise/1: "My music!!!!!!"
- `79db2613-34ac-4749-9ce2-4d34c8ff43f3` enricher usability/complaint/3 vs verifier usability/complaint/2: "I am new user of this app. But why too many advertisements are played. Almost after one or two song you play ads. It is irritating. Let people listen music. Provide your service with ease and comfort."
- `79ddb624-5b43-4f8e-a75c-503262bbd63c` enricher usability/cancellation/2 vs verifier usability/complaint/2: "Using the app since 4 years. The recent update just took it to a whole new level of awful. I never thought a music app will try to copy a social media app but here we are. God awful. I don't wanna see"
- `7a0599fb-879c-4292-8d5b-661010dc07d5` enricher catalog/praise/1 vs verifier other/praise/1: "The best music app it has my play list"
- `7a18f7a4-2244-4ca8-8191-849edd1f5d90` enricher access/complaint/2 vs verifier access/complaint/3: "It was great but then I randomly got logged out by Spotify idk if I was hacked but im rlly sad TAT 😭😭😭😭"
- `7a36db46-62ef-4caf-abcf-d5484a4fc7b5` enricher other/praise/1 vs verifier other/unclear/1: "Let's have a best experience"
- `7a87bd98-b864-4525-8e7c-21f0003411c1` enricher billing/praise/1 vs verifier downloads/praise/1: "I have used this app for years and premium is great. You can download songs or a whole playlist easy if you want when going on roadtrips, no ads with premium, there is a "Car Mode" in settings that yo"
- `7a8fcc05-c436-4f57-940b-c9c6cf35c11d` enricher billing/request/1 vs verifier other/unclear/1: "Primium primium lo abhi rating rating karo 😆😆"
- `7a9bff6a-b81e-4c10-b90a-ef7841637a63` enricher billing/complaint/4 vs verifier billing/cancellation/4: "Worked great, sub ran out wont let me cancel and won't let me update the payment details, makes the app unusable and broken just won't let me into it, can't turn my account into free service and I can"
- `7aac1980-b773-4179-95e1-dbab3a3edf66` enricher other/complaint/2 vs verifier other/unclear/1: "u know, fix everything or else ure just gonna keep loosing."
- `7ab5509b-caca-434a-8e7f-90224200fde5` enricher other/complaint/2 vs verifier other/unclear/1: "Tra$hcvcndy"
- `7ab8cfdb-9928-4dfb-9f03-c795e0c1afec` enricher other/praise/1 vs verifier catalog/praise/1: "This app is all you need , from music to Pod casts"
- `7af2312c-9d55-4beb-857b-1216160d519a` enricher usability/complaint/3 vs verifier usability/complaint/2: "To many adds and random music still turns up when I've turned play recommend songs off"
- `7bcfe23b-d545-4491-8546-3012162a1f8c` enricher other/complaint/2 vs verifier other/cancellation/2: "Think of a better marketing strategy. The current one is gonna make you loose all of it.. Signing off.. From heart to hate."
- `7c702285-9538-45be-92c4-a7e92144ff32` enricher catalog/cancellation/3 vs verifier usability/cancellation/3: "This is the most useless app I can't play the song I want to when I play a song it plays another song I don't want that to happen like who told you to play songs on your own the app should play the so"
- `7c8ea931-d775-46a1-a954-35fa81a94dbf` enricher usability/complaint/2 vs verifier downloads/complaint/2: "Great on the go option Needs to be more user friendly tho in downloading to ones playlist"
- `7c9ccbf9-975f-49f1-9597-128fa37125fe` enricher usability/complaint/2 vs verifier usability/request/2: "Overall the app is good, I'm just wondering why you guys removed the function to pause and skip songs outside the app it was a pretty simple and easy feature that allowed me to switch music without be"
- `7ca8a59d-fc62-4946-a8c0-f0f4c5b2494b` enricher other/cancellation/3 vs verifier usability/cancellation/2: "This doesn't even deserve 1 star after new update. This update making me soo angry and leads to write a bad review on my favourite app( Spotify). How can you guys just remove option of " added to queu"
- `7ceaf85f-b746-43e3-8f47-e0f5d19415ff` enricher support/complaint/3 vs verifier access/request/2: "Im trying to get my account info for spotify i hope some one can provide me with a num i can reach them at my searching is not working"
- `7cee483e-63d3-4a1d-afe8-217cf974203c` enricher other/unclear/1 vs verifier other/cancellation/1: "Hate this app.Bycott sewdin application👎👎👎👎👎"
- `7d31ebbc-5e20-428f-a6b8-fea762c6665c` enricher catalog/cancellation/3 vs verifier usability/cancellation/3: "it doesn't play what I want. everytime I choose a specific song, it shuffles and play a different song. I'm uninstalling it!"
- `7d5dbe68-0af1-4863-8b37-7a0ea16bfe93` enricher usability/complaint/3 vs verifier catalog/cancellation/3: "It's ad is always disturbing me.....to apply for premium....and it's not showing the lyrics also..it's telling that take the premium for lyrics.....I don't like that.....so I'm downloading Resso NOW.."
- `7d5e739d-8cae-4adc-b932-7db9cf635205` enricher catalog/complaint/3 vs verifier catalog/request/3: "It's good for listening music everything is ok. my phone is format also Spotify, so that I installed again it doesn't show lyrics why. I don't know what the problem,I tried so much times. Suggestion: "
- `7dbabd1d-05a6-4118-8140-712aab421162` enricher billing/cancellation/3 vs verifier usability/complaint/3: "Don't you think Spotify you are being such a money sucker at first we wete not able shuffle it's ok then you are able to skip for 6 times per hour and next you also limited the replaying of the songs "
- `7dedccfc-24b7-47ec-a372-3f14202ae11e` enricher usability/complaint/3 vs verifier usability/request/2: "The new homescreen is so bad, autoplays music even after you turn the audio off next time you open the app and scroll it will blast at full force. And it's not even music that I like!? Why do Spotify "
- `7e41090d-7a98-421a-b884-c2ff9f75f763` enricher usability/complaint/3 vs verifier usability/complaint/2: "Love this app although sometimes when I turn on shuffle it feels like radio only playing the most popular song I have a rarely playing newly added songs. Also it seems stuck on a 3 hour loop which is "
- `7e66dcbf-e4a7-4b42-b72f-6356932ec3bd` enricher other/complaint/2 vs verifier usability/complaint/3: "poor anf bad quality my joystick doesnt work"
- `7e84c02c-a28b-483f-a5c6-bf4052bdbbfb` enricher other/unclear/1 vs verifier other/praise/1: "Live this"
- `7e9b477d-f463-4ac2-ad80-09b2a02c167e` enricher downloads/complaint/4 vs verifier playback/complaint/4: "Totally unreliable. Arrived at a party, internet is non existent here, app refuses to play downloaded list for some reason. App is updated. Why I pay for this?"
- `7f01745d-6876-4caa-957a-9438e42f7f2c` enricher usability/complaint/3 vs verifier usability/cancellation/3: "Recent update sucks. Can't arrange my playlist. Uninstalled successfully"
- `7f61dab4-ad78-43c4-9fb1-c52a676d3184` enricher catalog/praise/1 vs verifier other/praise/1: "Love this song 🎵"
- `7f732cf9-ba49-4d0b-8029-a2bb97a20c9d` enricher usability/complaint/3 vs verifier usability/cancellation/3: "Worst app ever... doesn't let u go to previous song..stopped queue for songs...ads are like afer every other song. Idk why this is so liked. Seems like spotify needs money for evtg..cant even let peop"
- `7f86c836-577f-4256-b428-5383a351f8f0` enricher downloads/unclear/1 vs verifier other/unclear/1: "Set to Offline"
- `7fcd5950-fb6e-4596-bd65-2d25be69d11a` enricher catalog/praise/1 vs verifier other/praise/1: "Always great music and choices! Any genres, it's there for you!"
- `803b705a-779b-4b8d-8267-838093c1332c` enricher support/praise/1 vs verifier other/praise/1: "I had some issues when I started but it has all been solved and I'm enjoying sweet melodies"
- `8041fd9d-6193-4de3-a042-df01b423c1fe` enricher playback/complaint/4 vs verifier playback/cancellation/4: "The second longest relationship I've ever had is w/ Spotify, but the app hasn't worked in at least 3 weeks. I can't recommend something that doesn't work, which cost money. The second star is only bec"
- `80482015-31dd-464d-b650-ab82507973c5` enricher playback/praise/1 vs verifier other/praise/1: "I can listen to good music anytime, anywhere thanks to spotify!"
- `8074d1d8-9378-4ac4-b7da-99441ee1d3f1` enricher usability/complaint/2 vs verifier other/complaint/2: "I hate being nagged to rate things"
- `807e1a23-155b-4d38-8e96-2b2175a19903` enricher usability/complaint/3 vs verifier usability/complaint/2: "Is your new update removing the option to switch between card or phone storage?? Also, its so annyoing to have to press the loop button for every song i play. This update is garbage. The app still tak"
- `808eff68-8518-4077-85fb-45a18fc36cdf` enricher billing/complaint/3 vs verifier usability/complaint/3: "The most enjoyed music app is now considered dumb!!! Like whyyyyy this update ????? Soo good it was but now can't listen to song of our choice!!! Can't play it in the order I need then what's the poin"
- `80e838a0-5abb-4453-a4f1-d3ef279e8024` enricher other/cancellation/1 vs verifier other/cancellation/2: "I'm not use this app because of this country disrespect to our Qur'en!!!"
- `8110c638-5831-4635-a92c-a1d7e90c3606` enricher catalog/complaint/4 vs verifier catalog/complaint/3: "I loved this app but idk why all hit songs are unavailable this is very irritating my friend uninstalled the app due to this problem pls fix this becoz I got addicted to this app only"
- `81206543-3478-4133-a7d2-482280063406` enricher playback/complaint/3 vs verifier usability/complaint/2: "Android version isnt as usable as windows. ?? Problems stopping. Likes to run non stop. More adds -3 stars. Store your songs and skip this!"
- `81dc31d0-26cb-4dad-9f89-449d641fd57f` enricher usability/complaint/2 vs verifier downloads/request/1: "It's good 👍👍👍 but please bring back the delete option"
- `8296fa13-e092-4acb-8d8f-684150759776` enricher access/complaint/5 vs verifier access/complaint/4: "Someone is using my Spotify account from another country fix this problem please. I am unable to listen to my playlist"
- `829ec271-2d90-4551-95e4-f101fd9591de` enricher billing/complaint/3 vs verifier usability/complaint/3: "can't play songs or playlists on loop anymore, can't turn off shuffle. I think they messed up real bad with this update."
- `82b0ca3d-14bb-4803-9b1b-60eab5ba986e` enricher usability/complaint/3 vs verifier usability/complaint/2: "Ads 😑😑😑😑😑😑😑😑😑😑😑😑😐😑😑😑😑😑😑😑😑😑😑😑😑😑😑😑😑😑😑"
- `82defc09-711b-4dff-8ca5-384e112cd8b9` enricher playback/request/2 vs verifier usability/request/1: "It should allow us to browse any song and should allow us to play any song on our watch Speaker Not through Bluetooth device"
- `8306f9e0-d724-4f73-99e7-94c4f0b9809d` enricher usability/request/2 vs verifier catalog/request/1: "Please fix the lyrics back to normal"
- `833bb852-9847-4d0f-94e1-f12bf770ca81` enricher playback/complaint/3 vs verifier playback/complaint/2: "Update ke baad bht si problems a rahi hain click kisi or song pe karta hoon or play koi or song ho jata ha fix this issue"
- `834a0ae5-e8c5-49df-8136-35cc0c7dd6f5` enricher support/cancellation/3 vs verifier usability/cancellation/3: "Any time I connected to my car with sync the spotify app would open. None of the "solutions" I found online were even close to my menu options, and spotify's support was of no help even after talking "
- `83904150-4a72-4d1c-bab2-4d6f0ba79bdf` enricher catalog/praise/1 vs verifier other/praise/1: "The best music app ever! I receive updates on my favourite artists and it creates Playlist for me based on my the kind of music I love and also recommends hot new artists! I love love love it!"
- `83afc6c9-b577-48a6-98df-d9c6f4aac989` enricher other/unclear/1 vs verifier other/unclear/2: "bsdk kuran ko nahi jalate to 5 rating milti"
- `83bf81da-2481-423b-afd3-dbcd24a5faa3` enricher billing/complaint/2 vs verifier other/unclear/1: "Spotify is always like...... MAI GAREEB HU🥺🥺"
- `840661ee-3ef7-4e47-b698-f25906bc1903` enricher other/praise/1 vs verifier playback/praise/1: "Good to have music at the touch of your fingers all are good , sounds are fantastic"
- `84090917-7506-4a8a-bde2-599b6835c654` enricher billing/complaint/3 vs verifier billing/cancellation/3: "The new update is worst. We can't reach to a certain time of a song while listening it. Basically it forces us to purchase the premium subscription. Better to delete this app."
- `8443b4c1-9c55-4318-9b0a-06ad2a4ed20f` enricher usability/complaint/2 vs verifier playback/complaint/2: "Given the amount of artists I've selected the songs repeat way too much"
- `847e7a29-d997-45a0-8481-1a21723929cc` enricher other/unclear/1 vs verifier other/praise/1: "Jab se astronot vala inta achaha"
- `84a6d5f4-b025-4ab0-9605-9bd5ccba6e54` enricher usability/complaint/3 vs verifier usability/complaint/2: "They've ruined the enhanced playlist feature by forcing you to listen to it in shuffle"
- `852d0b01-5e1a-4875-932d-75260d92e6e3` enricher catalog/praise/1 vs verifier usability/praise/1: "good apps, easy to use and best music explorer 👍👍👏"
- `856aabd6-1a27-4453-a270-e053ebe365a3` enricher playback/complaint/4 vs verifier playback/complaint/3: "Not able to play on s22 ultra, can't play search results songs"
- `85953b16-6fa4-434d-a009-c830c3105368` enricher usability/complaint/3 vs verifier usability/complaint/2: "1/17/23 update: what is going on???! Every few days in past few months, something changes/disappears: Song Preview (now back, but you have to tap "and more"), then ability to Preview songs in my saved"
- `861b2386-b354-4be2-87e5-296a3c513128` enricher billing/complaint/3 vs verifier usability/complaint/3: "Honestly, the adds? The Spotify just want money now, I even have a limit to pick a song? It doesn't even let me play my own playlist. There just adding random songs, 1 star, If I could give a 0, then "
- `8677a17d-dd24-414c-961a-4d56238acc59` enricher usability/complaint/3 vs verifier usability/complaint/2: "It is excellent back...but now a days ads are too annoying 🙄! In middle of the song the ad start to play.can you please stop the ads to play between songs"
- `86c1f9cf-03b6-4652-988b-88f0b283c5a5` enricher usability/complaint/4 vs verifier access/complaint/4: "I do not recommend app to any one because every song that I listened to it has like 5 million ads that I had to listened and is very annoying and when I updated this app my account was there I have lo"
- `86f62d1d-f02a-4299-bbfd-a19f840b55b1` enricher playback/complaint/4 vs verifier playback/cancellation/3: "The app has gone completely downhill in the past few weeks. It started with only being able to play continuously with the screen turned on, which was annoying (I like to listen to music while falling "
- `870e56f8-a989-4444-bf55-402b0d700006` enricher catalog/praise/1 vs verifier other/praise/1: "Great selection of music genre"
- `872bbb40-7783-40fe-868d-2a191037d41a` enricher catalog/praise/1 vs verifier other/praise/1: "Finds all of my music.in the middle of it all"
- `874a30f0-a8f2-485d-a5ff-59c467e113bc` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "From this update what is that why we need premium now let we stop using it"
- `8771df66-f147-4fc4-b0eb-4adc54440fb6` enricher usability/complaint/3 vs verifier billing/complaint/3: "Money hungry only 6 skips per hour"
- `877f111e-3078-47a1-ad62-87030b68e98f` enricher support/praise/1 vs verifier usability/praise/1: "Excellent service and easy to use"
- `87818fe9-18f3-4791-af25-d4830333b888` enricher other/complaint/2 vs verifier other/unclear/1: "do Kaudi ka sada hua hai Bahut jyada Bura lagta"
- `8855f0c5-751b-409c-9de3-393d3ea5c8b5` enricher other/unclear/1 vs verifier other/request/1: "Isko download matt karna"
- `885bcec9-9887-4491-9090-0c50144ed7b0` enricher billing/complaint/3 vs verifier billing/cancellation/3: "I like Spotify the only thing I do not like is that if you don't have the premium version you're not allowed to skip six songs and have to wait like whole hour which is absolutely ridiculous and you a"
- `8874f370-a88a-452a-b85a-ffd21a0c971f` enricher usability/complaint/3 vs verifier usability/complaint/2: "¡Ojo, que no te engañen! Pagarás la suscripción para tener MENOS anuncios, NO para que te los QUITEN: los podcats cortan la emisión para meter anuncios de los patrocinadores y luego seguir."
- `888499e3-3877-4fe9-b6d8-66e3a31d48ca` enricher usability/praise/1 vs verifier usability/complaint/2: "Buy Spotify premium and its amazing, otherwise ads will annoy the hell out of you"
- `88871074-f96a-46be-b6b2-c9941536577a` enricher other/praise/1 vs verifier playback/praise/1: "Fixed bugs. Seamless & efforless okay across multiple devices. Can even select Spotify to play as my alarm clock. Can play on Roku TV, PlayStation, & control the music played across multiple devices. "
- `88a0a603-2308-48c7-8c20-763a0957b215` enricher other/praise/1 vs verifier catalog/praise/1: "I find 95% of things I'm looking for. Solid service for music streaming."
- `88bad8da-0d73-4285-b030-e66d5bc28843` enricher catalog/complaint/1 vs verifier catalog/complaint/2: "Don't have all the songs I desire. Otherwise, I enjoy Spotify"
- `88ccb860-3652-4372-8855-d516a7b25839` enricher playback/complaint/3 vs verifier catalog/complaint/3: "The big problem that you can't listen at the song you want"
- `88db8216-b831-4373-a79f-b46a14dd966b` enricher playback/complaint/3 vs verifier usability/cancellation/3: "when i open the song i want suddenly change to another song, i have uninstalled and downloaded many times but it's still the same please"
- `88e82f4d-d598-424c-94b1-c11c49ba7311` enricher playback/praise/1 vs verifier catalog/complaint/2: "Buena calidad de audio, en contenido solo agregaría más opciones de audio libros"
- `891a85ae-0ad9-4b90-8c67-00d79f8f0feb` enricher other/unclear/2 vs verifier catalog/praise/1: "The app is so best because the best song is on it"
- `896bf2b9-33e0-488d-8d1c-5b5181ea3ee5` enricher other/complaint/2 vs verifier catalog/complaint/2: "Artificial intelligence feature was worse than I thought"
- `89939cdb-ff35-4b6f-8203-4065edff83b5` enricher usability/praise/2 vs verifier usability/praise/1: "There are a lot of ads but hey its free. Aside from the ads I absolutely love this app. I like all diff types of music and this app has many options. I can listen to whatever I feel like at the moment"
- `899f6d47-c959-417b-8ee5-d56ec85db98f` enricher billing/complaint/3 vs verifier usability/complaint/2: "Worst app ever. How greedy can you be to not let us have any control over the songs without paying you? We're listening to ads with few songs sometimes by mistake."
- `89a49bc5-939a-4e99-8b45-71ae57fc392f` enricher other/complaint/2 vs verifier other/cancellation/2: "discusting music app don't install time wasted/money"
- `89b9d212-9e40-4a1d-9bc3-d1660441ec30` enricher billing/complaint/3 vs verifier billing/complaint/2: "Really useless if you do not pay, you must listen to the songs that you do not like!"
- `8a0bf103-104b-47a3-8d09-89580d5ebd39` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Spotify is great on the PC besides the ads. I expected the app to be as good. But it isn't. If you want to listen to a specific song, you can't without it being randomly shuffled in with songs you don"
- `8a0fe2b4-ede4-48c9-aed9-6d34bc62e805` enricher usability/complaint/3 vs verifier billing/complaint/3: "Another problem!! First I got problems like ad after every single song!! Now I'm getting 2-3 ads after every 2-3 songs!! I cannot get premium due to some problem!! Not every one is rich! That's why I "
- `8a2790f0-9e00-4a3d-9630-832b89693e78` enricher usability/complaint/3 vs verifier billing/complaint/3: "I purchased premium but still ads are coming. Please see this conflict"
- `8a75abc0-7d6e-4686-9e6d-f8c151ae749a` enricher usability/request/2 vs verifier usability/request/1: "Wish that you guys would update ur widget. It dated"
- `8a7ffe24-b376-4ee2-8e3a-ce067d26879d` enricher playback/complaint/3 vs verifier playback/complaint/2: "It makes songs while playing roblox"
- `8a80444a-2517-41b8-aa30-4559e98dd485` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "The app works pretty much as you'd expect--missing some functionality but at the expense of convenience. And yeah it's bad they don't pay their creators hardly anything. But do you know what's crimina"
- `8a83bacf-cf6b-4054-b153-4b22f8c2258a` enricher playback/complaint/3 vs verifier catalog/complaint/2: "The continue playing function is broken, it just loops the playlist you had on. All the reccommended features don't work, after 10 years it still has no clue about my listening desires. Randomly selec"
- `8a9d5f55-34af-4104-be96-c053ad5dc16a` enricher usability/complaint/2 vs verifier usability/request/2: "Yeah...... It's absolutely wonderful music app to use, but too many ads in between the songs. I hope this feedback will seen by Spotify. Please reduce the ads❤️"
- `8ac53809-f2e0-4d94-bd9e-6aaa3b7eead6` enricher playback/complaint/2 vs verifier usability/complaint/2: "Updates have worst play settings"
- `8ad41921-3022-49f4-af65-0ebdc8bef8b8` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "What I searched for is different from what is playing 😒"
- `8aff78ef-2aaf-44e7-af77-077e456cc367` enricher playback/complaint/3 vs verifier catalog/complaint/2: "I click on a song, and it plays a different song from the same artist. The name on the main page is the same, but the name on the scrolldown screen is different. I did some research, and what I can se"
- `8b2782df-d709-4fee-a8e6-98473d0918fc` enricher catalog/praise/1 vs verifier other/praise/1: "Great options for music"
- `8b624aaf-ece8-4450-a638-315ad4181259` enricher billing/complaint/2 vs verifier billing/praise/1: "Excellent if a little expensive"
- `8b66aa1b-3567-4bd7-9d5b-be686c060801` enricher other/praise/1 vs verifier playback/praise/1: "Clear, crisp music is food for the spirit."
- `8b783e01-7a4b-47d3-ba7b-9508430871f7` enricher usability/complaint/3 vs verifier usability/complaint/2: "After two to three songs there is always an ad."
- `8b951807-110d-4e80-8635-1fdb3e4127dd` enricher billing/complaint/2 vs verifier billing/complaint/3: "I have spotify student. Which means I pay $4.99/month. Recently for TWO days I didn't have enough in my account. After that I had plenty yet spotify still insists that they can't process my payment wi"
- `8baf8f3f-bfad-45ce-93c9-dfbf9092f4ac` enricher playback/praise/1 vs verifier other/praise/1: "App start working thanks"
- `8be1e808-7dc0-479c-9156-2d13ecdeb509` enricher catalog/praise/1 vs verifier other/praise/1: "I love this app because we can hear songs without premium and just love this app and all the songs of my favorite group is tgere hopes u keep this .. and keep adding more feature... Love you and Prupl"
- `8be20f51-2d76-4d6e-bf08-230c9a5a35c8` enricher playback/praise/1 vs verifier other/praise/1: "Nice app & good and running songs"
- `8c0e9938-48c2-4ef4-a494-946ce59cdfaf` enricher other/complaint/2 vs verifier other/cancellation/2: "This app is killing itself! Only a matter of time before someone comes along and finishes wiping it out by being better, it wouldn't be hard. You used to be so good Spotify, now you suck unbelievably "
- `8c3fa0f2-becb-4f91-a088-52a7c7105fc3` enricher billing/cancellation/3 vs verifier billing/complaint/3: "This is just worst update of Spotify. I can't play the songs I choose more than the limit then why would I use this app. This is terrible. That shuffle option is more frustrating, it says I have to ge"
- `8ce0bed5-6d83-4b10-8828-b7990bc59f71` enricher other/complaint/2 vs verifier other/cancellation/2: "Horrible app on play store remove this app"
- `8cf8258f-7483-40aa-8e02-342afeee0ec2` enricher other/complaint/3 vs verifier playback/complaint/3: "Spotify was my go-to application for music, but after the last update, it's not working. Such a shame, didn't expect this from Spotify"
- `8d466ce9-77c8-4d2e-996c-98345f6882dd` enricher other/praise/1 vs verifier catalog/praise/1: "Great app and great playlist of all songs. Love it."
- `8d79747d-30b7-4772-8c14-79d72ad4cc89` enricher other/complaint/2 vs verifier billing/complaint/2: "Total FRAUD!!!"
- `8da85a46-9621-4831-8b4c-52d6040eb788` enricher other/praise/1 vs verifier other/complaint/2: "Is really good just has some announcements"
- `8db2e85b-7b09-4260-8006-0e7b7ab13be2` enricher billing/request/1 vs verifier billing/complaint/2: "Stop Premium! !"
- `8db9be2f-f97e-491a-8bf1-fe53e8a958eb` enricher playback/complaint/3 vs verifier catalog/complaint/3: "I cant understand why when i press a song it plays a different song,you guys need to fix it,its bad"
- `8e06c434-3a22-490a-ae65-66068fe21d09` enricher usability/request/2 vs verifier usability/complaint/2: "Love the app. Something happened to the sleep timer setting for me. Very frustrating because I used to use that every night. Would appreciate having that added back."
- `8e39bb56-039e-4d68-a7fd-d19ea3f747c8` enricher billing/complaint/3 vs verifier billing/cancellation/3: "Spotify was great until they stopped letting the free users go to the previous song, listen an album in the order and not even letting them to toggle the song bar. I know you need to provide additiona"
- `8e7a41a0-78fc-450e-a8a0-621eaba550bd` enricher other/complaint/2 vs verifier other/unclear/1: "Can't rate any lower"
- `8e9c8bd1-9716-4e93-af7f-9675a5ec398e` enricher other/complaint/2 vs verifier other/unclear/1: "Don't Update"
- `8ec3fe3c-fa55-4238-9a82-82f714b9a5b0` enricher other/praise/1 vs verifier usability/praise/1: "I've recently switched my review to 5 stars. They fixed so many issues and I love how they even added an equalizer and the ability to boost the volume. Thank you so much for making such a great music "
- `8ed002be-9ac0-4a40-9301-90dda88401d3` enricher billing/complaint/2 vs verifier billing/complaint/3: "This app is pay to play music"
- `8f41ea09-81d7-431e-9df7-b583361c2063` enricher other/complaint/3 vs verifier playback/complaint/3: "Wish I could rate this junk lower. Garbage app, pauses, fails to load sometimes, full of ads, freezes, limited revenue for artists, trashy interface etc."
- `8f424b7c-ffaf-488f-845a-33ad6f700e8f` enricher usability/complaint/2 vs verifier usability/complaint/3: "I love Spotify but now all we have is 6 skips and I can't choose my songs and see my playlist no more I like all the new updates but I wanna see my songs and playlists again and I wanna loop them agai"
- `8f51bcca-d7b3-486b-a45b-f18469ec586a` enricher other/cancellation/2 vs verifier other/complaint/2: "Need to stop all updates!!"
- `8f55611e-bd54-43a1-b3d5-304352528113` enricher catalog/praise/1 vs verifier other/unclear/1: "Won me over with two words. Stray. Kids."
- `8fc9a390-71cc-4bbd-9a17-cb16b53afeb3` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "The new update sucks and I'm not able to queue any songs or play back the songs i played . The app forces to listen songs on suffel. all the features are available only for premium users why should th"
- `8fdec18a-bbef-4847-bc79-b42e48080c43` enricher catalog/request/1 vs verifier other/request/1: "When we indian are getting the karaoke mode?!"
- `900c03f8-9e83-4f9f-b4bb-40cfaae49708` enricher catalog/praise/1 vs verifier other/praise/1: "I like this, I am a BTS ARMY 💜 I love Kpop idols songs"
- `90103dd3-4a58-4544-a09e-e4590b870e2b` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "Recently...under the name of premium now I can't even choose the song I like to listen.....this is the worst I have experienced on Spotify...😡plz solve this issues asap......I'm literally at verge of "
- `9075edd1-fac2-4b33-a614-456ed8dbd267` enricher billing/complaint/3 vs verifier billing/complaint/2: "Wrost with lastest update just promoting premium"
- `90aebbdb-8cb8-4c0c-ba65-c2752d95a5cf` enricher usability/praise/1 vs verifier other/praise/1: "I love the music options and how you can turn of your phone while listening to music"
- `90c9ff43-8746-4459-9300-59bd18039346` enricher usability/complaint/3 vs verifier usability/cancellation/3: "New UI is horrible. I tried it for about a month and it makes the app almost unusable. I finally just rolled back to the old update."
- `90d9bc1a-b827-4cb5-967d-3a485e1c4f59` enricher playback/complaint/3 vs verifier playback/complaint/2: "Buffering is disgusting"
- `90e3e8b8-0f53-432a-bd5b-a7f0108b4b5a` enricher usability/complaint/3 vs verifier usability/complaint/2: "paying for premium and there's mad ads all throughout podcast."
- `90ea61a5-4400-4abd-b97f-f8121d67683f` enricher usability/complaint/3 vs verifier usability/complaint/2: "This app is very good but there is one problem advertisement.There is a lot of ads music is playing nonstop there is no variety of songs in playlists"
- `90ebfb01-e36e-4453-b172-b5acf920a4fb` enricher usability/complaint/3 vs verifier usability/complaint/2: "2-3 years back Spotify had least or negligible ads now for every song they are advertising ads,Unable to listen songs properly."
- `9144733e-1202-4d19-8197-478a4b246090` enricher catalog/praise/1 vs verifier other/praise/1: "Good playlists, shorts and the quality gets even better with premium."
- `915ad6ad-81be-41c6-8954-bf68dfc85595` enricher other/praise/1 vs verifier other/request/1: "Listen to my favorite music"
- `917c33f3-7d4e-47ad-b114-5a7ab243e797` enricher other/praise/1 vs verifier other/unclear/1: "Music on the SPOTify !"
- `9195a32a-b91f-4c6c-8d01-67791b0aad36` enricher other/praise/1 vs verifier other/unclear/1: "Its my World as a teenager!!"
- `91d5aa0a-8317-4070-825f-2218e4c99546` enricher other/praise/1 vs verifier catalog/praise/1: "Ots an excellent channel to listen to.old melodies"
- `91ee178f-62d0-4de4-8568-c5252e28b013` enricher usability/complaint/2 vs verifier other/complaint/2: "Old one is better than updated one"
- `9208f2b9-c74a-4c81-a150-e1177ea61f12` enricher usability/complaint/3 vs verifier usability/complaint/2: "Missing sleep timer all of the sudden, so many changes with smart playlists too, now it's smart shuffle? Just stick to something please"
- `9212fd80-cf97-48aa-9f80-be3916178264` enricher playback/complaint/4 vs verifier playback/complaint/3: "Absolutely dreadful experience trying to connect to my Smart TV. Spotify sound will not go through the TV despite all of apps and YouTube working perfectly well. May have to go back to the free versio"
- `92301dd2-d924-4e7b-85d9-2c9d50cf1360` enricher catalog/request/1 vs verifier usability/request/1: "please fix 2x speed for podcast"
- `92868ac9-6210-4494-8dd7-f709541d4729` enricher usability/complaint/3 vs verifier billing/complaint/3: "Ads torture only to those who were premium subscribers once. Free users who never tried premium are somewhat safe. Edit: Seems like ads torture isn't enough to make people buy premium subscription. No"
- `92aad879-6179-478e-b7a5-8dcf52855fe0` enricher usability/complaint/2 vs verifier usability/praise/1: "It has been with me for all my years all the way to 18 years old and I still prefer it dispute the ads"
- `93781860-53d1-4ecf-8c6d-9d0637e6d268` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "A good application, but the bad thing about it is that when I set a song that I want to listen to in a playlist that is not specific, a second song that is not available is played, and this makes me v"
- `93842c76-c0fe-4da8-a56c-2cf712477098` enricher billing/complaint/3 vs verifier billing/complaint/2: "Love the app but the one thing I don't like is that on a computer you dont need premium to choose a specific song or put your playlist on and off shuffle"
- `93b5b450-ff4e-449f-9b2c-75a0f378d0a0` enricher billing/unclear/2 vs verifier billing/unclear/1: "Ok thank you I will update my account & give Spotify 1 more chance I still have a few days left before I need to update my account with a new card number"
- `944164ed-80ab-4322-bf52-6772bcbb5c54` enricher usability/complaint/2 vs verifier usability/complaint/3: "I hate the new format for spotify. We used to be able to go onto our liked songs which were downloaded songs and play everything for that artist. Now when we hit liked songs it brings up individual al"
- `94649be9-4f99-498b-8bdb-f36f94f9fe73` enricher other/complaint/3 vs verifier usability/complaint/2: "i gave it 4 stars the first time i used it but I'll have to reduce 2 types for obvious reasons. I installed the original bcs i thought it could function better than the Spotify Lite but after one nigh"
- `946ec73d-7f5a-4c95-958b-178e19c08032` enricher other/unclear/1 vs verifier other/complaint/2: "Boy coot😡😡😡"
- `94ab6394-899e-4188-85af-97bde9980f3e` enricher usability/complaint/3 vs verifier usability/complaint/2: "I haven't even listen to one song and it shows advertisement. It's crazy"
- `94bd955b-cfa6-4975-a951-9df19a09f6ea` enricher other/complaint/2 vs verifier playback/praise/1: "Love the app but needs improved performance"
- `94c2fa9e-6beb-4f82-a3f1-4c45c9429ae6` enricher playback/praise/1 vs verifier other/unclear/1: "That bass is devil 😈"
- `94ebbc86-85a6-477f-a4d4-a94b24b5ca68` enricher other/complaint/3 vs verifier other/complaint/2: "App becoming useless since update"
- `95326197-6dfd-4e23-884d-c85903e11dee` enricher catalog/complaint/4 vs verifier downloads/complaint/4: "Songs are no longer playable by themselves. You only get an excerpt of it. The albums I had in my library are mixed up with all the wrong songs so vadically albums do not exist anymore. Spotify is a l"
- `9537236e-c76a-4629-b582-287485661578` enricher catalog/praise/2 vs verifier catalog/complaint/2: "Much better algorithms these days. Used to have zero variety. Music is the spice of life. Dont bore me with what Ive already heard 5 times."
- `954b0ac6-6121-439d-b04f-b2b3a5e12881` enricher other/praise/1 vs verifier downloads/praise/1: "Perfect app, nice download list"
- `95502086-d697-4c02-b868-0a0c3dea322d` enricher billing/praise/1 vs verifier catalog/praise/1: "Listen,Spotify is a great app, I've been using it for over 3 years,the people on here say 'it plays random songs not from my playlist' usually that is with a normal subscribtion. I highly recommend ge"
- `9576f7a9-6067-4d7c-98e8-4a9e05e9f770` enricher playback/complaint/3 vs verifier playback/complaint/2: "I'm fairly sure something broke in the last update. Something I do a lot is play music through my Bluetooth headphones and then put my headphones away as I need to hear something else. However, where "
- `95d026c8-38d4-4417-bf64-0cdc797b6895` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Spotify goes through ups and downs. One of the downs is the Discover. There is hardly any suggestions compared to what there used to be a few weeks ago. What happened to all the good suggestions?"
- `95d94595-2154-42f5-9a26-5bd886d9227b` enricher catalog/praise/1 vs verifier other/praise/1: "I love different playlist"
- `95f5e005-be56-48ce-8aab-b3cfd98aa01a` enricher usability/complaint/3 vs verifier usability/complaint/2: "This is the 3rd time I've given Spotify a 1 star rating. Every other has been deleted. If you like listening to ads this is the app for you. If you like music or podcasts look elsewhere. EDIT While th"
- `966ecddd-3b71-40fc-b192-5fe5e4cae20f` enricher catalog/praise/1 vs verifier other/praise/1: "Best app for listening adda"
- `96e9161c-5f95-417f-ad6f-997ce7d097ec` enricher playback/request/1 vs verifier billing/request/1: "Add a loop feature for non-premium and I'll give five stars"
- `96f620f2-d763-4897-a082-ff486a500dff` enricher playback/complaint/3 vs verifier usability/complaint/3: "I Can't Even Skip Song. The Update Is Very Badd"
- `97194478-6671-47f8-bc78-7874a90e7026` enricher billing/complaint/3 vs verifier billing/complaint/2: "Latest update made it worse. Pushing for premium. Lost it's credibility."
- `97a9a2cf-9760-4b94-b5cc-947eac97df08` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "Shittiest update ever, you can't listen to album in order, you can't choose songs to play. Spotify has become greedy. I'm uninstalling."
- `97b558b1-0b30-4384-8aa2-6a40e8334fe2` enricher usability/request/2 vs verifier usability/complaint/2: "Was nice if u reduce the length of the ad"
- `97c0b42c-3c3c-4468-9c9b-82a4fb920a51` enricher usability/request/2 vs verifier usability/complaint/2: "1 star only coz shuffle is not random it feel like I'm getting same track all time please atleast add option for fully randomly shuffle in settings"
- `980a1909-f498-433e-a1a5-065830aea377` enricher billing/complaint/3 vs verifier usability/complaint/3: "Was the best app for music ..but now it is the worst app.i can't go back to previous song,can't shuffle, seek is not working.everything just shifted to premium"
- `985c56d0-5c60-403b-ae2b-1adbb98e5599` enricher usability/complaint/3 vs verifier usability/complaint/2: "It's the same 4 ads over and over. Much more frequent than they advertise."
- `98602147-1377-458d-b685-781b322b51ce` enricher billing/complaint/3 vs verifier billing/cancellation/3: "The update where premium is required just to play your favourite song or if you want to repeat a song is really frustrating and very disappointed with the app . At first it was only ads that were so a"
- `9867eb57-e030-406f-a92b-9c7b5fb8e615` enricher playback/complaint/4 vs verifier playback/complaint/3: "This app was very slow and it cant install music or this app use internet to play th music.i recomemded dont install this app👎👎👎👎"
- `98795e79-1992-482d-80e0-69d2e809107f` enricher other/complaint/2 vs verifier catalog/complaint/2: "How much yg has paid you to change the results over night ??? Shame on you"
- `98827cfe-371f-4ad3-a5e3-5de438cb5552` enricher billing/complaint/3 vs verifier billing/cancellation/3: "I used to love this app and it's recommendations but lately it's been all a money game and since the most basic features like scrubbing around the song's timeline and shuffle play has become a part of"
- `9884c4c1-06d9-4e04-8788-b1d9a9745635` enricher usability/complaint/3 vs verifier playback/complaint/3: "It wont play all the songs in my playlist"
- `98955bae-8449-42e3-9571-253c986fe96f` enricher usability/complaint/3 vs verifier usability/complaint/2: "It is really good. I've been using Spotify for over 10 years. However, I have become very disappointed with the shuffle function. Although I have a couple hundred songs in some of my play lists, Spoti"
- `9951f3e7-70ca-46d3-bcc3-49671d8fddee` enricher billing/cancellation/3 vs verifier billing/cancellation/2: "Unless spotify resets its update...i will not be using this app...spotify has become now money centric completely. Not thinking about larger percentage of people using this app."
- `997d7bca-721f-40ab-b082-306bdb108a19` enricher other/praise/1 vs verifier catalog/praise/1: "Great selection of laughter I've ever seen."
- `99a71c4a-7523-4fa4-b142-4535b3eb6c0e` enricher usability/cancellation/3 vs verifier billing/cancellation/3: "Idk it's just waste of your data... Everything is under the premium and the premium is also crashed so yeah and ofc too many as in too many ads plus you cannot replay any part of the song I am uninsta"
- `9a4148a4-3ab1-406b-93b7-06b40eb4179b` enricher other/praise/1 vs verifier other/complaint/2: "Love this app very much just some complications at times."
- `9a687a61-e96a-4492-80e0-4eff037636b0` enricher usability/praise/1 vs verifier billing/praise/1: "No interruption from ads but a decent price as well as their bundles for family it's really good I recommend you to listen to music from here"
- `9a7c9fab-2af7-4724-8aed-357762819482` enricher other/praise/1 vs verifier billing/praise/1: "Worth my money"
- `9a86534c-eb3e-4fca-b02b-4c2d39ea8791` enricher downloads/complaint/5 vs verifier downloads/complaint/3: "Simple to navigate and an endless supply of content however 9nce you 0ay for the service and start downloading content you can't play "offline content" if your subscription terminates due to a delinqu"
- `9a8d7339-8c96-41c1-ac39-b69b4f39fd51` enricher billing/complaint/2 vs verifier billing/complaint/3: "I give it 1.0 star. first thay tell us you will get Premium free yet thay ask bank staff. What if you are 12 year olds."
- `9b41e1ca-6be3-487a-8d30-bd0fbe930a47` enricher usability/complaint/2 vs verifier usability/complaint/3: "The last update is really bad. Home screen is useless."
- `9b6e551f-2913-48d9-a7ca-4621eff9e094` enricher playback/complaint/3 vs verifier playback/complaint/2: "Keeps opening whenever I connect headphones."
- `9bb4a956-7cab-4a52-b9e0-f4cf4a08def7` enricher other/unclear/1 vs verifier downloads/complaint/2: "If you till did not downloaded the app you are unlucky"
- `9bba0661-e160-4272-a7e1-6d7942889db3` enricher other/request/2 vs verifier usability/complaint/2: "Same as everyone!! Atleast bring back loop option!"
- `9bcc48fa-4057-42de-8156-c6877df26cea` enricher other/praise/1 vs verifier usability/praise/1: "Amazing app been using it for year's its really useful for music! Needs hz adjuster but has everything plus more have been a Spotify member 6years maybe more 2010 in the app store on iPod 3rd generati"
- `9bd272eb-fd82-4b23-8e1c-90159bf059f9` enricher other/unclear/1 vs verifier downloads/complaint/2: "Ill ratr iy only if i download songs cos am not use ioo it"
- `9c3a6f10-bb8b-4b31-bd8c-d2e53eb28bc3` enricher billing/complaint/3 vs verifier billing/complaint/2: "Music forward, backward, repeat, there are the simple part of a application. But here why we need to pay for all. Nonsense"
- `9c696098-61f3-4915-b925-99a4839b13a2` enricher other/praise/1 vs verifier catalog/praise/1: "Spotify keeps me sane. I love that I can easily access my favourite lists and it is so easy to search for new music. The Daily recommendations are fantastic."
- `9c75631c-6d57-4925-8f49-bdea0bef56eb` enricher usability/complaint/3 vs verifier billing/complaint/3: "One of my fav apps. I am using Spotify for a long period now ,but now we can't even hear the songs in the order we need, also not able to forward or reverse the playing song. Now this app is all about"
- `9ca29dc7-c161-4d44-9dc2-7ae4371167ce` enricher catalog/complaint/3 vs verifier playback/complaint/3: "Some songs that are available but not playable and when clicked on its album the song apperas to be light in colour please fix it No solution till now"
- `9cead0ab-2166-4355-abfd-c7186fed86d7` enricher support/complaint/2 vs verifier other/complaint/2: "Yo. Your mobile service sucks the chrome off a hubcap. Fix your junk, you clown salesmen."
- `9cf3ef1e-53ad-46f1-90ee-c4f472ed0516` enricher catalog/complaint/3 vs verifier usability/complaint/2: "Stop throwing some random garbage in my suffle list already packed with more than a dozen tracks."
- `9d1fe65a-65b3-4a5b-9d17-156b26193e42` enricher catalog/praise/1 vs verifier other/praise/1: "Girls got me listening to this app. Was easy to understand ad use, I now have so many song list and listening to song I haven't heard since I was a kid. Enjoying it so very much, thank u!!!!"
- `9d6b35a2-d01a-4761-bb16-ed8f45bb1af7` enricher billing/cancellation/4 vs verifier billing/cancellation/3: "I hate this app now a days because only for some reasons where we cant replay the music or we cant play what we like again Whenever I click on the part which I like it always ask to do premium pleas f"
- `9d968ea9-8cbf-4907-a125-555d69b7bf52` enricher playback/complaint/4 vs verifier playback/complaint/3: "The latest update is annoying, especially when it freezes it won't work until you uninstall and install again.. but for how long"
- `9e0ca167-46a2-4c01-92b2-17e046ee1d40` enricher other/cancellation/1 vs verifier other/unclear/1: "I boycut all swedone app because swedone government allowed permission burnkuran"
- `9e121b51-ec5b-470c-927f-72b9bef1f4c4` enricher usability/complaint/3 vs verifier billing/complaint/3: "Worstttt app with worst update nd full of adds , will u give premium for free then y so adds worst music app"
- `9e260c4d-06b3-4c8a-af1b-1196c0932db2` enricher usability/complaint/3 vs verifier playback/complaint/3: "UI glitches sometimes. The screen will get stuck and show the same thing even when I switch the song. Also app totally crashed when trying to move from internal to external storage, so I had to reinst"
- `9fc80950-da25-4322-84ab-dbde1ea92280` enricher support/praise/1 vs verifier other/praise/1: "Magnifico servicio."
- `9fcb6a32-e387-4994-b0ba-558af26ad338` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "I understand commercials, but playing 5 commercials every 5 minutes of ridiculous. Uninstalled. Slacker has been my fav music app so far for listening to the latest hits."
- `9ffb4b5e-0eee-41b4-af3b-836d924dbfd5` enricher other/unclear/1 vs verifier other/complaint/2: "Freedom of speech discriminated! An dammi Filastini."
- `a0c09c8a-92ee-45bd-ab96-99223066a0fb` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "This app is great, amazing but for some reason it took out the lyrics for every song. My brother said check if there was any updates but the last update was a few days ago I even logged into another a"
- `a1173780-b16e-4cd3-80ed-fea2e9dbb96a` enricher usability/complaint/3 vs verifier playback/complaint/3: "Not satisfied...so many Ads and I don't know it only works on mobile data and not on wifi ??"
- `a1498233-4250-491e-8e4e-45ae9a44b893` enricher billing/complaint/4 vs verifier billing/complaint/5: "I BOUGHT SPOTIFY PREMIUM MINI BUT IT DOESN'T WORK IT JUST SAYS I STILL HAVE A FREE ACCOUNT WASTE OF MONEY"
- `a194a0dd-8615-4da6-b8fb-d6fb1ecdec90` enricher other/praise/1 vs verifier catalog/praise/1: "Greatest music at all times"
- `a1c77e66-8129-4f5c-ae12-af76b1a12b41` enricher billing/cancellation/2 vs verifier billing/cancellation/3: "This app is big waste of money first, get amazon music it has free download. Not to mention it is terrible scam for artists. There ads are extra annoying to make me buy premium like as if i want to. P"
- `a20f59e3-bde4-4d87-af0a-5c29e8fe66cc` enricher usability/complaint/3 vs verifier usability/complaint/2: "The new home screen sucks so much, I no longer have easy access to new music or a wide range of new releases. I don't even want to scroll down to find them because I don't want to be harassed by a bun"
- `a242f778-aa89-499e-b12a-f2cac8b7130d` enricher playback/praise/2 vs verifier playback/complaint/2: "The app can be very laggy or glitchy but all in all great sounds music"
- `a2b83030-02fe-4ac7-8538-0fd75b3ad91e` enricher other/praise/1 vs verifier other/unclear/1: "No words to put. My best buddy 🦋❤"
- `a2ddf632-54da-4a57-bb8d-e210ca149823` enricher billing/complaint/3 vs verifier billing/complaint/2: "To do anything, we need premium. Developers do not care about good service. They only care about earning money"
- `a2e2a211-5061-44ff-a8aa-47e63c5fda90` enricher usability/complaint/3 vs verifier usability/complaint/2: "Ads are so much disturbing after every single song"
- `a2efb5f8-42f2-4d26-b157-55ad7056e0c2` enricher downloads/request/2 vs verifier downloads/request/1: "Please let us save unlimited offline songs, as a Music lover I highly recommend to lift the 10,000 song limit in the library. We want to enjoy streaming songs and play it offline infinitely. Hoping fo"
- `a3039220-4db5-47ae-9950-7a535006795a` enricher usability/request/2 vs verifier usability/request/1: "Wish I could remove a song from a playlist while it's up vs having to find it in my playlist to remove it... We can add to a playlist while on the song screen, why not remove?"
- `a3205281-c783-4c3a-9149-31c754b3ede6` enricher catalog/request/1 vs verifier usability/request/1: "Excelente aplicación de música, la utilizo en todo momento... Sería excelente que pusiera el karaoke ingles -Español 💯👍..."
- `a3440d2c-5066-4e9f-9adc-75287a14d522` enricher other/complaint/2 vs verifier other/unclear/1: "😂😂🤬🤬"
- `a3454e6c-8988-456e-a0bc-405224c08976` enricher usability/cancellation/3 vs verifier usability/complaint/2: "My experience has been awful every time I put on a song ut gives me the wrong song even though I don't need and update add the adds here are just to many of them I had 5 adds in a ROW!I just insist th"
- `a38fe073-7d6a-43f9-98ed-d635e0ce0171` enricher other/complaint/2 vs verifier usability/complaint/2: "Ajeeb h na gane agye kr skty na pechy aur na apni marzi sy kuch kr skty."
- `a3c9b3ec-dc44-4833-a113-a76789b6037f` enricher other/praise/1 vs verifier downloads/praise/1: "This is my go to for music. I have the premium version which lows me to listen to music without wifi by downloading. It helps me get through my day"
- `a3e42af3-28f6-4c37-92fd-8f1787016435` enricher other/praise/2 vs verifier other/complaint/2: "Great service, useless widget"
- `a40615b6-607a-4eb9-b74c-60bd43200eb0` enricher usability/complaint/3 vs verifier usability/complaint/2: "Fun for listening to the music but the adds are so annoying. You don't even get the "watch this ad to get 30 minutes of ad free listening" anymore. I get to listen to 3 songs and then it plays like 5 "
- `a44cbd64-7b98-4650-869e-60eb96950708` enricher catalog/praise/1 vs verifier other/praise/1: ", very good app with all the tunes you could wish for"
- `a4687d04-aaa7-424e-b666-3310c532fce2` enricher billing/complaint/3 vs verifier billing/complaint/2: "The worsttt music app. U need premium to do anything"
- `a49dd912-8178-4042-9fd7-60aa3184d595` enricher catalog/praise/1 vs verifier other/praise/1: "I love the music made for me.❤️❤️❤️❤️❤️"
- `a4ab7fcc-3e51-461d-a2aa-620bc8f6df3a` enricher playback/complaint/2 vs verifier usability/complaint/2: "Turns itself on randomly it's so annoying!!!!!! 6am ! Please fix!"
- `a4b5bdcc-b9a6-4205-87da-ce4f15030852` enricher catalog/complaint/2 vs verifier usability/request/2: "please stop addding song that are not in my playlist. Its so annoying to listen to a song not on your playlist when you want to listen to YOUR playlist not what Spotify wants. I wish there was a optio"
- `a5553bbf-27c6-45d4-ac0a-7934b0a53b40` enricher catalog/complaint/3 vs verifier usability/complaint/3: "Basically useless and they kept playing recommended songs in my playlist instead of the actual songs I put in and in which it had became impossible to skip after a few times."
- `a559bc83-6ecc-4965-bcd6-d2e53aead164` enricher billing/request/2 vs verifier billing/request/1: "May I know the reason for the price hike?"
- `a597af1f-e08e-43b9-9641-e30446a33631` enricher playback/complaint/4 vs verifier playback/complaint/3: "Everything time an in podcast advert (ie one spliced in by the podcast creater rather than a spotify add) ends, Spotify stops playing and only way to resume is use the 15second skip. Yes I've tried cl"
- `a60e365d-4fbe-4fce-a1a4-985715965e90` enricher other/complaint/2 vs verifier other/cancellation/2: "Worst app ever,instead you use yt music"
- `a60ecb3f-c01a-4669-b864-c5813c9be7b7` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "It's good but I don't like it because when I listen to music it just shows an another one for example I tryed listening to kerosene but it puted an another song please fix it so we can hear the origin"
- `a669aaba-1281-4cd9-aa4d-602c78b0d00a` enricher playback/complaint/3 vs verifier usability/complaint/2: "Literally hate new update why I can't adjust the song to my favourite part😞"
- `a67e36c6-d12b-4d4b-a34b-08ebfe0d0ec3` enricher usability/cancellation/2 vs verifier usability/cancellation/3: "As a premium customer of 5+ years, the re-design of the home screen is an abomination Why keep paying for premium when content I did not select, essentially unavoidable ads, are forced every time I op"
- `a6d134af-3a10-4e0f-a150-31c966025d08` enricher usability/complaint/2 vs verifier billing/complaint/2: "Repeat option removed from mix section."
- `a6e1af17-5cae-4e6b-9ba2-0c8741115c47` enricher billing/complaint/2 vs verifier billing/unclear/1: "It's worst after premium options 😔"
- `a6eb9bc2-0338-4b01-8e59-206baa4d8658` enricher usability/complaint/2 vs verifier usability/unclear/1: "Ads Kami kra"
- `a6eccbda-0dc1-4ff6-b0da-7da999a8f21e` enricher catalog/praise/1 vs verifier other/praise/1: "Great song"
- `a723d2e1-3fa9-40de-b188-2872deeae969` enricher other/cancellation/1 vs verifier other/complaint/2: "We don't need you...there's a lot of options available in the market. 👍👍"
- `a73cbea8-c7fc-431c-8f46-6b053492e8c1` enricher playback/cancellation/3 vs verifier playback/cancellation/4: "100% of the time I connect to Bluetooth or directly via USB, the first song doesn't play. I have to disconnect and then start the Playlist over. Sometimes it decides to stop playing while I'm driving."
- `a7ac7d78-d182-4211-b486-3fa26561a551` enricher billing/request/2 vs verifier billing/complaint/2: "I found Spotify got 2.7 stars on the Play Store, compelling me to write a review. I'm a Premium user. For me, Spotify blows its competitors out of the water. It meets my needs reasonably well. I feel "
- `a7b29ac5-c812-4b30-abcd-d9cba8c19542` enricher billing/complaint/3 vs verifier usability/complaint/3: "What's with the new update?? I can't even play songs on repeat or shuffle. It's worse"
- `a83646a6-9925-4076-b075-cf803c367c94` enricher playback/complaint/4 vs verifier other/cancellation/2: "I had it for a bit but then it just stoped working and I had to delete it"
- `a83b9531-95a4-4881-b3ff-e2098f29ac50` enricher access/request/3 vs verifier access/complaint/4: "Hey Spotify team. It's been a month and still nothing has changed. I would really like to use my old number and change my email address. Pls send me an OTP rather than sending me "check your number an"
- `a8466556-2d55-41b5-8226-81bc02099bf7` enricher access/complaint/4 vs verifier access/cancellation/4: "Please don't download spotify.I didn't even get a chance to make an account.I am never downloading it ever again Sorry."
- `a86be349-6426-4fec-b995-d2bf4dcd080a` enricher catalog/complaint/3 vs verifier usability/complaint/3: "I use spotify on all my devices. Many songs don't ha e lyrics and some which do, I can't see the lyrics on my android TV. It is a very good feature which is recently missing. I think this issue must b"
- `a8773260-fcfc-477b-9052-de5414e7bdee` enricher billing/complaint/3 vs verifier usability/complaint/3: "I don't know what the creaters think about this I think they only want earn money from this app I am saying this because of the recent update even I can't even forward ⏩ and backward the song freely"
- `a8c5bb1f-b0ec-414e-92cb-b960c71e56e1` enricher other/praise/1 vs verifier catalog/praise/1: "I really enjoy using Spotify, I have discovered new music from my genre and new artists. Excited for hi-fi sound quality in the near future."
- `a8e00d9b-074a-42fc-9647-7fed9ba6b3a9` enricher billing/complaint/2 vs verifier billing/complaint/3: "You've block all features for normal users"
- `a8ed8a61-a035-4a6c-818e-1bf61f855cf9` enricher billing/complaint/3 vs verifier other/complaint/3: "1, or worse, i would rate it a Zero. I have been using spotify for the past 3 years now, and the update has never been worse. It does not even have common features of a proper music streaming app anym"
- `a8f137a4-2eaa-4192-9da0-b93bcd3ae89c` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Without premium you can't go to the previous dong you can't even skip through the song without premium you are also limited on your skips you have ads that say you now get 30 minutes of ad free music "
- `a91be625-c858-4fbc-8c2f-6b9ce878687f` enricher usability/complaint/3 vs verifier usability/request/2: "I love this app besides there is a add after every song please fix this"
- `a9251d90-4607-4425-8aac-0a30972096ea` enricher catalog/complaint/2 vs verifier other/unclear/1: "Gaddar Dangal movie ka gana hata kya ukhad loge jit toh wrestler ki hi hogi"
- `a9443687-26b1-4fad-84cb-86c6103bbf4f` enricher billing/complaint/3 vs verifier billing/cancellation/3: "Even the basic requirements for hearing song like moving the pointer to fav line of a song is made premium... Songs are always on shuffle... we can't go back to previous song... Going to uninstall..."
- `a995df8e-bdf4-4245-8ce5-4a79fee79327` enricher other/unclear/1 vs verifier other/complaint/2: "Fuc....."
- `aa4018a2-968d-4973-81c3-ad478763ae28` enricher other/unclear/1 vs verifier other/praise/1: "Love Islam and holy quran ❤️❤️❤️❤️❤️"
- `ab2d4c7a-3fe5-4a0a-aafd-7b1f17e358e6` enricher usability/complaint/3 vs verifier usability/complaint/2: "The shuffle option is remove which deteoriate the experience"
- `ab2ee509-a037-460a-9fac-12077bc8b818` enricher billing/complaint/2 vs verifier usability/complaint/3: "False advertising- "30 minutes ad-free" There are ads every two or three songs, so the claim at the beginning that I can listen for 30 minutes without advertising is false. I timed how long between ad"
- `ab5205a4-eace-4a98-acbf-4cfd4ac79c80` enricher usability/complaint/3 vs verifier usability/complaint/2: "Best app for listening songs But ads are terrible every songs ends a advertisement starts What the hell is this ads At a limit ads are good but after every song is not good after 3 to 4 songs ads will"
- `ab85d4cf-8aae-4f9a-870f-d4a62d1ae87c` enricher playback/complaint/3 vs verifier playback/complaint/2: "Has anyone else have this app just start playing random songs thru the media player all by itself, even when not on the app? This has just recently started happening even when I'm watching youtube (mu"
- `ab8c6854-09b9-45be-ab01-fed2be9b57d2` enricher billing/cancellation/4 vs verifier billing/cancellation/3: "This app has started capitalism like apple where a user has to pay them to even skip through, shuffle or playback the songs, worst update ever in time... stopping to use it immediately"
- `abb27fbb-8925-41af-ae18-b647549b6a59` enricher billing/complaint/3 vs verifier billing/complaint/2: "Designed to make the listening very annoying inorder to get you to pay for adds free."
- `abf62e1f-2303-4f13-b9e0-70d3767df04b` enricher catalog/request/1 vs verifier downloads/request/1: "please give us recently played songs and allow us to safe them as playlist. thanks"
- `ac034031-6d4d-490d-ad66-7a96b3e61701` enricher playback/complaint/4 vs verifier playback/cancellation/3: "The app keeps quitting in the middle of songs. I want it to play continuously in the car or whatever, but it will play 2 or 3 songs then just stop, a lot of the time it will be in the middle of a song"
- `ac2e1e8d-1a8c-466d-b146-178d41ef6d0b` enricher usability/complaint/3 vs verifier other/complaint/2: "look. it was better then NOW when I downloaded it it was cool it didnt have many ads but now its JUST SO ANNOYING it has so many ads. when I was trying to download it IT LITERALLY SAID I HAD TO DELETE"
- `ac430205-a4d5-4fc3-8c57-93fd2d0887d4` enricher usability/complaint/3 vs verifier other/complaint/2: "Can't stop playing the music I dont wanna listen to. And it still sucks"
- `ac63ef2f-4417-4192-9f35-931585421c30` enricher other/complaint/1 vs verifier other/complaint/2: "Don't have time for constant updates....the version I have works just fine."
- `ac6aee57-7d4d-477c-91fb-c08ec30403f3` enricher playback/complaint/3 vs verifier playback/complaint/2: "Simply app is ok but it keeps stopping for no reason"
- `ac8a00b0-a868-4373-8f76-f28b4d31f6b2` enricher usability/complaint/4 vs verifier downloads/complaint/3: "Liked songs won't load"
- `ac9efa61-856d-4a72-803d-41e7f31b1ad5` enricher usability/complaint/4 vs verifier billing/cancellation/3: "The new updates made it impossible to work with this app,I can't turn off shuffle nor can I skip any part,I can't go back to previous song. Literally nothing is available without premium,if you just w"
- `acbb8b1e-e9cd-42dc-b1b6-bcd1e17e4e26` enricher playback/complaint/3 vs verifier usability/complaint/2: "This app is great but I'm having some issues lately when using my mobile device as a remote control when i played music on my laptop. Sometime the phone don't find my laptop or the music controller do"
- `acbbc140-0040-4d63-9d1c-ae604c0645d3` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "The new UI is absolutely terrible, it autoplays unwanted videos on my phone speaker while I stream to my room speaker. Remove this garbage or I am moving to a different music app. I have spotify for m"
- `acf8ce78-2fce-4a2a-8517-4a8d29ed959b` enricher catalog/complaint/2 vs verifier other/complaint/2: "Racist platform ,promoting political agendas Disgusting 🤮"
- `acf8e91e-a230-4e19-9e15-33e146f95b38` enricher usability/complaint/2 vs verifier other/complaint/2: "Too many addd"
- `ad1b0b3a-8820-412a-bfac-d66067fe46a6` enricher usability/complaint/2 vs verifier usability/request/1: "Shuffle mode doesn't actually shuffle randomly, it's based on an algorithm. Make it random like it should be."
- `ad33c661-3768-4224-bb2c-381989a1cf9a` enricher billing/complaint/2 vs verifier other/complaint/2: "Company became very much focused on Money"
- `ad662ca1-4ca6-4e38-b344-93c198664406` enricher catalog/praise/1 vs verifier other/praise/1: "This is best platfrom of songs"
- `ad7b3e82-47f2-4dc9-a256-17cb32a7ccd1` enricher billing/complaint/3 vs verifier usability/complaint/3: "The update is honestly WAAY too restricting.The forced shuffle feature on every user that isnt on premium is just...so unappreciatedable to the point where its clear that,the only target is money. But"
- `adad98dc-97b4-49c5-a8d8-30aecdf7b8fd` enricher catalog/praise/1 vs verifier other/praise/1: "Great app I love that you can play eny song you want!!!"
- `adae2fcc-e11b-4641-b8ba-69643a0d1638` enricher usability/complaint/3 vs verifier usability/complaint/2: "Still no fix for the missing scroll bar in "Liked Songs" for us Android users. It's very annoying trying to manually scroll for a song in the car before the light changes. Edit: You guys brought back "
- `adf18270-7916-4c68-a0aa-8b6b75bd26e6` enricher catalog/praise/1 vs verifier other/praise/1: "Always able to find good music"
- `adf3c6ca-7d47-49f2-8304-17377a95ed9e` enricher catalog/request/2 vs verifier usability/request/2: "Can y'all give us the option to enable or disable smart shuffle it's annoying when I'm listening to a playlist I created then this random song start playing. It's highly frustrating"
- `adfda3e5-b630-497e-9212-3ed0abe80372` enricher other/cancellation/2 vs verifier billing/cancellation/3: "Spotify latest update is a very bad move they have stopped all the basic features required by a user . Sorry but now I have to switch."
- `ae0b3f4d-2e67-4c0c-ab24-974b7bfd5bb1` enricher usability/complaint/3 vs verifier usability/complaint/2: "Play 1 -2 song and then play advertise every time."
- `ae609bbc-3e2d-4bd5-9c2f-f5b922518eee` enricher billing/cancellation/2 vs verifier other/cancellation/2: "Spotify think he is only one music app for Indians that's why he change his T&C for free user's.......Buddy I am going to uninstall you now Bye Bye."
- `ae76704c-4e92-4f55-9e0f-70cca1499d3d` enricher billing/complaint/4 vs verifier billing/complaint/3: "the skips are limited per day, lyrics aren't visible, one can't choose the songs they want to listen to on their own until an unless one buys the Spotify Premium.. this is direct exploitation of the u"
- `ae7ff4cb-bb11-4de4-8fde-fcc82f93e5d8` enricher billing/complaint/2 vs verifier billing/complaint/3: "This app is only for premium users. Don't download it if you don't want to buy premium subscription. It is literally the worst app for free user."
- `af1384b7-b77d-4437-ad8f-0530053fb79d` enricher other/complaint/4 vs verifier playback/complaint/3: "This app is so bad in so many ways. From the lack of discoverability to the regular interruptions and inability to connect to the internet even when on wifi or with a full signal, Spotify makes listen"
- `af4aa3fe-ea70-4dd1-bdff-da5b384a6040` enricher other/praise/1 vs verifier playback/praise/1: "Spotify is my one of the most favorite song app we was listen very much songs clearly and very awsome app"
- `af686678-da91-4ae2-a976-0757aae73699` enricher other/complaint/2 vs verifier playback/complaint/2: "Very buggy"
- `af8d06ca-e683-4048-b5f9-d87e61610635` enricher billing/praise/1 vs verifier other/praise/1: "Spotify, not only has lots of new and old music, but, it's the ability to have more control over your playlist. I.e. Pandora offers a premium package that says you get certain perks for paying. But in"
- `af8f55b1-7a8c-4566-95cd-9cde3170a9e4` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Bring back blend radio. The DJ feature is garbage. The plus sign change was unnecessary."
- `afe9a020-6dd5-41c2-b3ed-3f3e93503bc6` enricher other/praise/1 vs verifier catalog/praise/1: "I can't believe I have not tried spotify until now. This is a great music app. I will continue using this app for years to come. I also found a song that the other music streamers cannot locate or are"
- `b0533cf1-3086-4ca2-bde8-67365f0206b6` enricher other/unclear/1 vs verifier other/praise/1: "My holy book quran"
- `b0535656-9188-4865-b426-42f0530d91f2` enricher usability/complaint/3 vs verifier usability/complaint/2: "So much adds gadho mar jao or wo sufful ka button on karke rakha hai uski wajese kuch bhi bajj jata hai pasand nhi isiliye change Kiya to add aa jata hai. ham gana age piche bhi nhi kar skte. Overall "
- `b0591db9-c097-4362-9b68-41cf84aa02b9` enricher playback/complaint/3 vs verifier downloads/complaint/3: "I have used my Spotify on numerous devices over the years. That being said, Spotify has always been a challenge to play music and podcasts in areas with less than great cell service. Web pages and You"
- `b06275fd-a7f9-4522-bdc2-086a780dcddc` enricher usability/complaint/3 vs verifier usability/complaint/2: "It was my fav app until the last update. I HATE IT. It literally changed the basic options like, Playing songs in order,repeating songs. l dont understand why?!! . PLEASE RESTORE THE OLD OPTIONS"
- `b0c4fc8c-a60c-4863-a12a-2fc8a8a90e63` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "dear Spotify bug playlist others no showing fix it"
- `b0da28dc-4a0d-479c-8148-4a43603f0023` enricher playback/complaint/3 vs verifier playback/cancellation/2: "Actually, when I used this, I was shocked. There are many weaknesses here. The song I play does not play. When I watch it with YouTube Music, it lags far behind. I am bored.Now i uninstall this 🤮🤮🤮"
- `b103c39c-9ba2-411a-a48a-957dc20f43d6` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "Look spotify is good in all but once it comes ro remixes like sped up or like a song x another. YOU GUYS TAKE IT DOWN like I'm enjoying someone's remix they make. And you take it down like don't do th"
- `b1621bf2-fbdd-48ed-b434-f7504b1539c1` enricher usability/complaint/2 vs verifier billing/complaint/2: "Even Shuffle u greedy"
- `b1645172-6297-47cb-92ca-ff7834d1d0cf` enricher downloads/request/1 vs verifier downloads/unclear/1: "Is spotify not offline app??"
- `b18b8e92-740d-47c0-bf5e-eb226bd0c480` enricher usability/complaint/3 vs verifier usability/complaint/2: "Very rubish too much ad even I can't listen music"
- `b1ad3a73-ffad-4658-9c33-0c5944375f8f` enricher usability/complaint/4 vs verifier billing/complaint/3: "At first the app was working well but now it won't let me in my Playlist and when I try to find an individual song it just plays something else random that I didn't ask for and when i try to go to my "
- `b1b7f7e4-83b9-4fd5-9a2d-b0aebad16012` enricher billing/request/2 vs verifier billing/complaint/2: "It's had some bugs since I started but it's definitely living up to the standard I desired for music. I wish they'd go down in the prices."
- `b1ddcaac-026b-480e-98c1-9bf3ab6dabc0` enricher billing/cancellation/3 vs verifier billing/complaint/3: "Was the best app for streaming music. Now you can't repeat your favorite song without premium. So long."
- `b1df1b2c-ab48-44b8-8956-6b73b344eb30` enricher billing/cancellation/3 vs verifier billing/complaint/3: "I am changing my 5 star rating to 1 as they reduced there features inspite of giving us for what to get premium it's so disgusting tbh 🙄 soon they're looseing one user for shure"
- `b22c108b-f1d7-43a4-ad4b-e082a8e0576d` enricher other/request/1 vs verifier usability/request/1: "Call me crazy but I need Spotify connect to play on multiple devices not just 1. I want to blast my music on at least 3 devices. I need the speed up function like vlc player has to make the songs play"
- `b290ce78-8a6d-4bdf-a40c-1010d4d3ae85` enricher playback/complaint/3 vs verifier usability/complaint/3: "App has been buggy for months. Play bar keeps disappearing and the app has to be restarted to get it to reappear. It also randomly pauses audio sometimes."
- `b2966c8c-4e0a-4ccc-ac09-2a48abe38b5a` enricher catalog/praise/1 vs verifier downloads/praise/1: "I download all my music onto this app, and get to listen to artists I would never normally consider"
- `b2e79930-fbea-44a4-b75e-bdc3c4bcdde0` enricher other/praise/1 vs verifier other/unclear/1: "So..nice"
- `b319e3fe-6353-4c47-8dbe-53e44b6c7515` enricher playback/complaint/4 vs verifier playback/complaint/3: "Not sure if it was a new update, but every podcast I listen to freezes at 5 minutes and 46 seconds on the dot. I can go back and it plays fine, but once it reaches that mark, it will not play past it."
- `b36c5234-39ac-4a40-b049-eabc0a111dcc` enricher billing/complaint/3 vs verifier usability/complaint/2: "Bad really very bad. No skip, no repeat , no lyrics."
- `b3b0adcf-71ee-4636-81c7-8ea3070d971d` enricher playback/complaint/3 vs verifier playback/cancellation/3: "I love Spotify, been using ot for years. Recently i got a new phone. Spotify worked fine but now while im listening to music or podcasts. The sound stops but its still playing. I haven't found a way t"
- `b3db5165-d61a-45fa-a37e-e7e371fe80cf` enricher usability/complaint/3 vs verifier billing/complaint/3: "Too many ads, can't listen to specific parts of music, can't play songs on loop, removed lyrics of almost every song available on spotify. Made all the free features paid. Idk why Spotify is behaving "
- `b403868e-07f5-48b8-ba15-d7d434b1cc83` enricher catalog/praise/1 vs verifier other/praise/1: "Khub sundor eai app sob song available is really khub sundor app"
- `b423137a-941d-4030-a0d2-00d44f84651b` enricher other/complaint/2 vs verifier other/unclear/1: "Below 1 rating is possible"
- `b446c26c-febd-4415-b450-0ead8a37412c` enricher access/complaint/3 vs verifier usability/complaint/3: "It's normally perfect and besides the add I've literally never had a problem with it but for the past 3 days it won't let me click on an album it just go to a black screen for example I tried to click"
- `b4f159b0-1df9-44a1-9673-c10dccdf8031` enricher other/complaint/2 vs verifier usability/complaint/2: "It sucks and it's not user friendly whatsoever"
- `b528074b-ddd0-4be0-a418-8f1baf7b7904` enricher other/request/2 vs verifier other/complaint/2: "It have to make improvements for androids device"
- `b55c5f0a-58f9-4ca6-91f9-407910f261f7` enricher playback/praise/1 vs verifier other/praise/1: "It's a great app to use with headphones!"
- `b57300f3-8d7d-43f5-b964-88ebcc8736ce` enricher billing/complaint/3 vs verifier usability/cancellation/3: "I hope this app fixes itself because I am really not happy with the results. In the free plan, you get SIX skips an hour. Which means you have to sit through songs you hate or dont want to here at the"
- `b574daec-4134-4a88-84ed-a56da3f8f16e` enricher other/complaint/2 vs verifier playback/complaint/2: "Ano na spotify? grabe sa bagal ang response ng app ninyo. ginagastusan ng premium pero di naman ramdam ang pagka premium. jusko"
- `b59ef7db-274c-4829-831a-4f8e8c1c9b0c` enricher other/complaint/2 vs verifier billing/complaint/2: "Money hungry douchbags"
- `b5cc2b79-6065-452a-9f08-0aa3128b1029` enricher usability/complaint/3 vs verifier usability/complaint/2: "To agresive on the commercials to stop using the free app"
- `b6080cef-48c3-4aa0-961c-1b52b9a4acbd` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "It cant put the music i want"
- `b609650a-bbfb-475c-8044-6ef171062665` enricher billing/complaint/3 vs verifier usability/complaint/3: "The most horrible app I have seen the latest version is the horrible version I have ever seen it doesn't allow us to like to move forward or backward the song specially the Android and the non premium"
- `b622d6a9-cc40-4a59-914c-a1ba5dc7568a` enricher billing/request/2 vs verifier billing/complaint/3: "The app takes a lot of money I will recommend that they should go back to free mode without ads .if not they'll lose a lot of customers"
- `b6335e33-09b1-4c8b-a5c4-fd2710464ee4` enricher billing/complaint/2 vs verifier billing/complaint/3: "Nowadays Spotify has become demanding in everything and has started asking for subscription. Even in song play."
- `b64e49f6-5fa6-4710-bdb4-78c1dbd44843` enricher usability/complaint/2 vs verifier catalog/complaint/2: "Annoying interface, navigation and suggested songs are not relevant"
- `b6541780-82d9-42e0-ab2b-37524cf697e4` enricher catalog/complaint/3 vs verifier usability/complaint/3: "App is terrible constantly changes from your playlist to songs recommend for you. Struggles to go from wifi to 4g even with downloaded playlist. Is very frustrating to use. Also shuffle plays the same"
- `b668e7b6-2fbd-4703-b25b-4e69db3136af` enricher other/cancellation/2 vs verifier playback/cancellation/3: "It Used to be one of my essential apps. Now uninstalling after their new decisions."
- `b66f56e3-5d37-4ae9-9358-d6bc51c26390` enricher catalog/praise/1 vs verifier other/praise/1: "This is an amazing appnto listen music the recommendations are on the top and exactly what you want . I love this app hats of to team Spotify."
- `b69f4a4a-a27b-44eb-b8a8-d94887fb1208` enricher billing/complaint/2 vs verifier billing/complaint/3: "Everything needs premium"
- `b70b4d29-e5e4-4ee0-8cd7-2016dc0c0f1e` enricher catalog/request/1 vs verifier usability/request/1: "add some option that can look the lyrics"
- `b7319582-a13a-48eb-b438-9d08b661d6c5` enricher billing/complaint/3 vs verifier usability/complaint/2: "Ye koi tareeka hai bheekh mangne ka.... Between the song ads pop up , even this is not enough now they said that we have to buy premium to listen our favorite part of song...."
- `b80b1844-8681-4a65-8c0c-0c125a36b7f0` enricher access/complaint/4 vs verifier access/complaint/3: "1 becuase thie gqme is so annoying and it won't let me on the normal spotify"
- `b81f5883-9f85-47d6-bb58-233db2ac6a50` enricher catalog/praise/1 vs verifier other/praise/1: "my favourite song"
- `b82ee8e8-dbcd-4bf0-8b6b-9635cdfd6cb6` enricher other/complaint/2 vs verifier other/complaint/1: "I hate spotify and swezland , l love Quran"
- `b8384cd7-39f0-474f-9047-cdc0beb119d1` enricher other/cancellation/2 vs verifier other/cancellation/1: "Hope the bad things happen to your company just like Disney and Marvel. You do your thing (not caring about fans,customers) we do our things ( shift to your competition or start the great pirate era)"
- `b84d48bd-297b-4993-a6b3-455d87e8e553` enricher other/complaint/2 vs verifier playback/complaint/2: "Quality is very poor"
- `b8946ad0-438e-4eff-ba22-bdf01f2aa016` enricher other/praise/1 vs verifier usability/praise/1: "Really like it. Quite intuitive."
- `b91866dc-d596-45f5-80e9-500d71f60af3` enricher other/praise/1 vs verifier other/unclear/1: "wanderful😁😂🤣"
- `b9d38ae8-97e6-4a36-ac94-3ceff87e962d` enricher billing/complaint/3 vs verifier billing/complaint/2: "first you put loads of ads and now you also limit the features available to free users wow talk about greedy kys"
- `b9e76f2f-64da-4f0e-95e5-16e969a9a9e5` enricher other/praise/1 vs verifier other/unclear/1: "Love ly like"
- `b9fc90be-33d7-4433-a280-6e6697513f81` enricher catalog/complaint/3 vs verifier usability/complaint/2: "Pretty decent, the random song feature sucks doesn't play your whole play list and a lot of repeats."
- `ba012651-e56a-41ca-9849-27f56a9f8651` enricher catalog/complaint/3 vs verifier usability/request/2: "I'm sick and tired of having unwanted suggested songs autoplay and shuffle in whenever I try to play a playlist, and being unable to skip them if I've used up the amount of skips given per hour. I can"
- `ba5faaf3-6cfb-45a8-948a-ae138e02f661` enricher billing/complaint/1 vs verifier billing/praise/1: "I love my Spotify. I love music from classical for Bubble baths ! I listen to Liberace to Rock and Roll for bangin' your head ! Thanks Quiet Riot !!! There's music for every mood ! For everyone ! It's"
- `ba9c0f42-e438-40b5-8ce2-0a01d39572de` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "I can't seem to listen to my local file music anymore it's greyed out. I've tried reinstalling and it didn't work."
- `babb8104-7cd7-47c1-aa81-a79a6534e372` enricher usability/complaint/2 vs verifier usability/praise/1: "Lots of lovely musics...with few adds only"
- `bad6feba-20d5-4892-85ab-fb8651db000f` enricher usability/complaint/3 vs verifier usability/complaint/2: "First this app was so good then there is more advertisement than music played"
- `bae12f5b-7129-4166-aace-c7bf8d533776` enricher playback/praise/1 vs verifier catalog/praise/1: "superb app!! Great music quality, and you can find all the songs of whatever language or type it is. It also doesnt matter how old is it. I would recommend it to all who are music lovers."
- `bb00f210-7a90-4695-b4cd-37f278fb50ef` enricher other/unclear/1 vs verifier other/cancellation/1: "Boycott #Sweden #Boycott #Spotify Uninstalled 🔥"
- `bb079cbf-cac1-4a02-8739-d934e0e24fa9` enricher other/praise/1 vs verifier catalog/praise/1: "Best for music hands down"
- `bb8eb5b2-063d-482d-984d-bc55014b9842` enricher billing/complaint/2 vs verifier usability/complaint/2: "Always adds always adds what if are not able to afford premium"
- `bb8ec184-0099-4fc3-8f33-08cd34fd9198` enricher usability/complaint/3 vs verifier playback/complaint/3: "It's unbelievable how bad this app manages to be. Horrific design, especially for podcasts, barely functional search, and huge numbers of app-breaking bugs which you can read about in other reviews."
- `bb92cf60-11fd-4786-9f32-76491cc73c87` enricher catalog/praise/1 vs verifier other/praise/1: "I always listen to songs from spoify.... this app is very good and recommended 👏🏻👏🏻"
- `bba1b682-0bbb-4a6d-80e7-3b38c19962b5` enricher other/cancellation/2 vs verifier other/cancellation/3: "Horrible app after the newest update would not recommend!!! Downloading a different app and deleting Spotify immediately!!"
- `bbc97f8e-8c4a-46dc-916a-ab23373973be` enricher playback/complaint/2 vs verifier playback/cancellation/4: "Was fun while it lasted, can't listen on browelsers. Anyway off it goes."
- `bbce3afe-11c0-42a7-ad43-32ebc92ab531` enricher usability/complaint/2 vs verifier usability/request/2: "Can't remove it from drop down menu like other apps."
- `bbefb7a0-1d24-4568-bbe4-fc838792923b` enricher catalog/complaint/4 vs verifier catalog/complaint/3: "disgusting. added #genre stuff related to shorts. now whenever i search a song i see pornographic content."
- `bc781356-a714-4b04-9a27-372d3edf1561` enricher billing/complaint/2 vs verifier usability/complaint/2: "the best music and podcast app I've ever used, though the ads are unbearable"
- `bcc0e0ab-c7e3-4f11-9a39-0f613ebd5aa6` enricher playback/complaint/2 vs verifier catalog/complaint/2: "Sometimes the app will say it's playing one song, but ends up playing another. I find it quite annoying when I'm looking for one song in particular. I usually end up just playing the album it's on to "
- `bcd0c807-2059-406f-a69c-e5068c1364f7` enricher usability/complaint/2 vs verifier other/complaint/2: "The old Spotify was better than the new update."
- `bce646bc-4164-4b06-898b-91474f826b56` enricher billing/complaint/2 vs verifier usability/complaint/2: "This app has much restrictions. I just get on YouTube and create a Playlist much better and it's free"
- `bd0c23d5-2cbd-4c2d-baff-c59d1f037512` enricher billing/complaint/3 vs verifier billing/complaint/2: "I love using spotify but I did not love how I got switch to the duo plan when I only have one accouct"
- `bd7cda6b-2f5b-46f7-87ba-8f00aa89fb26` enricher playback/complaint/3 vs verifier playback/complaint/2: "Lagging"
- `bda18a7b-f29b-4d73-907c-741108ccc474` enricher other/unclear/1 vs verifier other/cancellation/1: "I boycott this sweden app....bcz of"
- `bdd83b32-a1d6-434a-9344-0b572fca254a` enricher other/complaint/2 vs verifier other/unclear/1: "Bekar ha bhaiya, main to Tut Gaya"
- `be193cdc-4393-4436-95d6-3274f554e9e2` enricher catalog/praise/1 vs verifier other/praise/1: "I love spotify. I've been using it since 2023. I have the paid subscription and I love playing music to boost my mood and have dance parties with my kids. They have the best Playlists and great sugges"
- `be1c48c4-46bc-4ddd-ae38-49a970c82d66` enricher billing/complaint/3 vs verifier billing/complaint/2: "Edit: they patched spotify to encourage users to buy premium, otherwise free version is pandora clone. Premium is worth it tho."
- `be4781b2-9d2e-4e10-8233-b945a924e249` enricher catalog/praise/1 vs verifier other/praise/1: "The cycle of artist is very well done"
- `be64e311-0c5c-454c-bf4e-716868b20c9b` enricher catalog/complaint/3 vs verifier playback/complaint/3: "It wont load my liked songs at all on mobile. I have to play them through my laptop :("
- `be8c8d07-97d5-4c82-956f-2454f6132f5b` enricher playback/complaint/4 vs verifier usability/complaint/3: "This app is terrible. I downloaded it on my phone and when I try to play one song it plays something completely different and when I make a playlist it wont even allow me to move the songs around in t"
- `beac4fb3-afa8-4a3d-a31e-be686fdc299d` enricher usability/complaint/3 vs verifier usability/complaint/2: "By far the best app for listening to music but since I refuse to pay for premium the ads are so fricking annoying, I've had three 30 seconds ads listened to two songs and had three more. No this hasn'"
- `bec07907-d981-4d54-951c-a40ce88a5342` enricher downloads/complaint/2 vs verifier billing/complaint/2: "It is a stupid app don't download this please🙏🙏because if u want to download a song we have to pay money for this , this app is there for only listening songs , if u want to edit a video compalsary u "
- `bef6fe06-4149-4e98-9b12-565ac65ae693` enricher billing/praise/1 vs verifier other/praise/1: "I'm very pleased using Spotify, it's good value for money."
- `befa5442-8934-49ae-bf00-654bebce4ea5` enricher downloads/complaint/4 vs verifier downloads/complaint/2: "Amazing amazing app. Although y'all need to work on your offline mode, why do I need an internet connection to initiate my downloaded content😊🍻????"
- `bf028d42-f249-470d-9716-78b69aee203c` enricher other/unclear/1 vs verifier billing/unclear/1: "Idk but iambroke so yeah"
- `bf4c242c-1dfd-4c02-898f-795f5aa70ca9` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Can't find some songs i can find on other apps"
- `bf4f3bd6-02a1-4236-b082-3821386d8278` enricher usability/complaint/2 vs verifier other/complaint/2: "Advertise so boring"
- `bf5d2ca6-6285-4e33-8f61-437a22521012` enricher other/complaint/2 vs verifier billing/complaint/2: "being too greedy"
- `bf634c6c-7dc1-45f0-ac5c-9e0f9a1c8f64` enricher playback/complaint/3 vs verifier playback/complaint/2: "Was Great on every other phone, but when I got the Galaxy flip 3 it would pause the music or make it skip when I heard the phone was closed or the screen was off"
- `bf915f07-869c-44e0-b710-9983d4be6213` enricher billing/complaint/3 vs verifier usability/complaint/3: "Made a liked songs playlists of more than 145 songs and music and now you have restricted all the features that I cannot play the songs in order, can't play a specific part of the song, listen to anno"
- `bfc2929e-d73e-4fbe-b75d-c9e6067845bd` enricher billing/complaint/2 vs verifier billing/praise/1: "I absolutely love this app, it has gotten a little pricey but it's worth it."
- `c0080abc-6db7-42e3-a2bf-3e3061998757` enricher billing/complaint/3 vs verifier usability/complaint/3: "Pathetic app update. Why coerce users with ridiculous methods like keeping shuffle mode on and unable listen/go to previous track."
- `c0151958-b382-4795-917e-97382bbaf94f` enricher usability/cancellation/3 vs verifier usability/complaint/3: "Absolutely disappointed with the latest Spotify update! The loop button and the previous song button have been mercilessly disabled, making it impossible to enjoy my music the way I want to. But that'"
- `c03b42e5-a655-4443-a2a9-e6b666fb033d` enricher usability/cancellation/3 vs verifier usability/complaint/3: "Spotify was the best some time before it started coercing the users to buy premium. Like who likes that you play a playlist and after the first song (approax. 2 min) there are 2 ads and after this, so"
- `c0557f97-c7c0-4c43-8e5a-421154f62f15` enricher usability/cancellation/4 vs verifier usability/cancellation/3: "One of the best apps for listening to music, or rather, it was. It's the past now. Spotify is no longer the best music app. With the new damn updates, the devs did a very good job on disappointing us."
- `c0ab14ca-9c8d-4430-b2c1-ffde048b19cf` enricher catalog/cancellation/4 vs verifier usability/cancellation/3: "I have been using this app for years. But since it's last updation, I'm not able to play the song of my choice, single tracks are unavailable. Every song I search comes in a playlist. I don't know wha"
- `c106504c-31fb-4375-9b6b-1fb25d0bdbbb` enricher catalog/complaint/3 vs verifier other/complaint/2: "Horrible. ¿Quien quiere una app que no regpeta los verdaderos numeros? Y ni hablar de que uno paga premium para que se reflejen los numeros tal cual, una horrible experiencia."
- `c13438b2-e0d2-449b-ae56-9bbe83341937` enricher other/complaint/2 vs verifier other/cancellation/2: "😡😡😡😡😡 ban Karo is app ko please 🙏🙏 bhut Bakar app hai bhai log install mat karana"
- `c17b5290-44fe-4cec-9f3c-955db60c4fc6` enricher billing/complaint/3 vs verifier billing/cancellation/3: "This app used to be one of the best music apps. USED TO BE. but now it is fully totally completely forcing people (it's only users) to pay for using it. Like why everyone should pay for it. The app ca"
- `c17bfeb6-70a0-4a79-9f42-b148396b2b89` enricher catalog/praise/1 vs verifier other/praise/1: "All your Favorite songs and albums in one place."
- `c19a64e1-7176-4e22-9681-f566a422c2b9` enricher downloads/praise/1 vs verifier other/praise/1: "Nice, 👍worth to download"
- `c1b17567-471d-4adb-834b-c16c44d0fd49` enricher usability/complaint/3 vs verifier usability/request/2: "It was perfect back then but after update it doesn't showing lyrics, instead of that it showing abt the artists.Pls change it to lyrics back."
- `c1b683fc-58cb-470c-b591-e2393748883c` enricher catalog/cancellation/3 vs verifier catalog/complaint/3: "Spotify just disappointed me yet again. Many songs which I like aren't available and even while leaving, 'Biggest' was not available on the playlist which appears after subscription cancellation. LoL."
- `c219843b-66a4-4967-bffb-ad4310f09530` enricher support/complaint/2 vs verifier other/praise/1: "They still haven't smoothed out the podcast experience 100% but I have faith in them. Great company overall."
- `c226c18c-7fb0-49dc-ae30-1b19d8417fb3` enricher usability/complaint/3 vs verifier usability/complaint/2: "The app says 30 mins of interrupted listening and then interuptes me after every song"
- `c25708b2-55f9-4f1e-bb42-21dbbeea536b` enricher catalog/request/1 vs verifier billing/request/1: "Hello Spotify! You added translate lyrics feature and video with audio in your updated version but I can not see that in my Spotify , I'm asking you for your help with this new amazing features, hope "
- `c28fafb7-7cd1-447f-97f0-54b397348661` enricher billing/complaint/3 vs verifier billing/complaint/2: "They are turning free features into primium features just so that people will left with no choice but to switch on to the primium version which was once available for free. Just how pathetic Spotify h"
- `c2d8d99f-46fb-4cb1-ab20-07b0cb4689d3` enricher other/unclear/1 vs verifier other/cancellation/1: "😠😠😠😠😠😠😠😠😠Bycott spotify"
- `c324ce57-f5bb-493f-a1d3-541bffbce199` enricher billing/complaint/4 vs verifier usability/complaint/3: "Very wrost update...I can't choose any song to play..and not able to use song trackline they saying if you hav to choose song go premium..it literally like F.M Radio.. very bad update..."
- `c325e5a9-b6c9-49be-b09e-7fcfca0d87ef` enricher catalog/complaint/2 vs verifier usability/complaint/2: "The lyrics background colors are awful, wish there was an option to change it to pure black. I miss high quality option a lot."
- `c3302d69-a685-4743-ad5b-81eba4556787` enricher other/unclear/1 vs verifier other/praise/1: "🙏💓💓🔥"
- `c3322fc8-2aa2-4fda-b79c-2c6a19152e42` enricher catalog/complaint/2 vs verifier other/complaint/2: "The experience listening to music is great, but the experience listening to podcasts is pretty bad."
- `c333e4d6-6c0f-4de8-ba4c-a48abf2c83a2` enricher usability/complaint/2 vs verifier usability/request/1: "Why can't I sort my freaking playlists by artist anymore?"
- `c355dd2f-9d8c-4955-bdeb-e4615803a05a` enricher billing/complaint/3 vs verifier billing/complaint/2: "What's the point for spotify premium, it gets annoying paying 11 bucks every month, like let me pick a song I want and not make me shuffle"
- `c41988e0-f76b-4ada-9509-44808b3c3dfc` enricher billing/complaint/3 vs verifier billing/complaint/2: "Why we need to buy subscription for just playing our own playlist or playing song on loop? It's seems like u guys are begging for money."
- `c448872a-b492-47f9-af2d-c1d201b435fa` enricher other/praise/1 vs verifier playback/praise/1: "Highest music app streaming without hassles wherever and whenever offline buddy"
- `c4548e6b-59d6-4736-be64-cb1f137f010e` enricher catalog/request/2 vs verifier catalog/complaint/2: "Not sure what happened, all of a sudden a lot of Chinese songs titles changed to some poor English translation. Making it extremely difficult to use and find songs from list etc. I understand English "
- `c45a56d0-2640-4610-ab52-f38856b7d951` enricher billing/complaint/3 vs verifier billing/complaint/2: "You guys have made a really great app.. I really love it and I've gotten premium a couple times. However I feel not being able to play the first song you want in free mode kinda defeats the whole purp"
- `c4671833-7bc0-4c19-80eb-e5cbf085cef1` enricher other/praise/1 vs verifier other/unclear/1: "McDonald's of music 😜"
- `c49d35a7-2c9f-4d46-979c-cca62f54afe0` enricher billing/cancellation/2 vs verifier other/cancellation/1: "Terrible to try an CANCEL"
- `c4d1559e-bbb2-43c8-9487-31f649634e9b` enricher billing/cancellation/2 vs verifier billing/complaint/2: "I enjoyed it. Now I don't. Even ads were fine with me. But... You guys- stop putting premium on literally everything. You guys are just shooing away your users."
- `c4efa911-8aad-4842-a048-3b234c63c5f3` enricher usability/complaint/2 vs verifier usability/complaint/3: "This app seems really desparate for money. On the free plan, there is a WE ADDED section on the created playlists. This adds more songs on playlists that I already made. This is an infuriating tactic "
- `c522c6d0-2d8e-450c-870f-1e8bce76cc6b` enricher usability/praise/1 vs verifier other/praise/1: "User friendly. Amazing!"
- `c529c325-22f3-414b-93d9-76711b5cd92d` enricher other/praise/1 vs verifier other/complaint/2: "Bets music app. ....no compatibility 💜"
- `c56d3189-f1d3-4dcc-ab78-06369bc5666e` enricher usability/complaint/3 vs verifier downloads/complaint/3: "I'm not able to access my liked songs"
- `c56e9ede-470f-4fe7-9eca-c20f599bfb64` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "It's good at what it does, but if you're not paying, the app's song recommendations are bad."
- `c59138e0-9fee-4337-ac33-a6c223127088` enricher other/complaint/3 vs verifier other/complaint/2: "New updates made this app useless"
- `c5be3bf0-2e52-415e-b7f0-d120927e6758` enricher other/unclear/1 vs verifier playback/unclear/1: "Battery saver"
- `c5f74d66-893a-427e-8acf-24c9347ef217` enricher other/unclear/1 vs verifier catalog/complaint/3: "fitur bagiin lirik ke sg ilang"
- `c653586d-19e4-45a9-a525-8ab0b7a5b5a3` enricher billing/praise/1 vs verifier other/praise/1: "Fantastic app add free love you Spotify"
- `c657c8ee-d6d8-4913-9ada-afe7ca1c71b7` enricher other/praise/1 vs verifier playback/praise/1: "Only way to play music through my phone!"
- `c65e3925-3157-4e28-8b38-d30c9ecd1395` enricher access/complaint/4 vs verifier playback/complaint/4: "Spotify doesn't work for users in East Africa. I have a premium plan but it doesn't play any song or let me search for songs. It used to work before but now it doesn't"
- `c6e407ee-56ea-4c63-8fd8-9d26f107fd55` enricher access/cancellation/4 vs verifier access/complaint/4: "Can't even log in anymore, the app is completely useless at this point."
- `c71352e6-4774-46c8-8b05-d5a308534cdd` enricher playback/complaint/3 vs verifier usability/complaint/2: "Constantly autoplays despite it being turned off. Utter trash."
- `c7289f29-6f58-4e29-b8a9-c9d3e16041bb` enricher catalog/complaint/3 vs verifier usability/complaint/3: "It doesn't let u play songs u like and they play different songs"
- `c7371cf0-437a-40e1-a6cf-bfb8dc1bf444` enricher downloads/complaint/5 vs verifier other/complaint/4: "Just lost all my playlists"
- `c74754b1-ae4f-4c26-bdf5-454dce647dab` enricher playback/complaint/3 vs verifier usability/complaint/3: "Whenever i try to play a song it shuffles and play another song which i don't want to listen it's really hard to listen song beacuse of it.Plz fix it."
- `c74cc581-1d2a-4397-90a7-93fa84bd6f72` enricher playback/complaint/3 vs verifier playback/complaint/2: "It's a great app overall but it sometimes crashes"
- `c75cdd63-3174-4d39-bc0f-50d136e31c89` enricher support/complaint/3 vs verifier support/complaint/2: "Getting bombed with email and ads spam even on the premium service, also lack of real human support is frustrating from a company as large as spotify."
- `c7952368-49b7-4745-9768-7501fbeea905` enricher playback/complaint/3 vs verifier playback/complaint/2: "I have switched from pandora to Spotify I love it just 1 issue is that my liked songs are playing like 5 seconds of the songs and I don't know why if anyone can tell me why that would be awesome!"
- `c7b34ab3-5a29-4458-8233-537958c8a644` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Trash! This music app is so hard to use! Songs that i want to play doesn't show up instead other annoying songs show up!"
- `c7bdb4ac-604f-4212-bb7f-5c2a578f7b8c` enricher other/complaint/2 vs verifier other/cancellation/1: "Do not install this app"
- `c7bff642-dc4e-4058-ad37-4d1c253ade23` enricher billing/complaint/3 vs verifier usability/cancellation/3: "After the recent update they ruined all the fun and amazement Spotify is our first preference to listen music because of its playlists and music but now after update we cannot skip to our desired poin"
- `c7de67f9-4af7-4f27-a08a-e5a96ba8a13f` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "It do not show lyrics any more it's annoying please fix it🤦🏻‍♀️"
- `c831741d-60cc-44fb-8658-d243c7ccfde4` enricher other/complaint/2 vs verifier other/unclear/1: "Beekar update..."
- `c83af5b2-c508-40df-8843-f3f71f801364` enricher other/praise/1 vs verifier other/unclear/1: "Moslam ♥️"
- `c88667d3-8831-447b-a42d-e785e8094cc1` enricher billing/complaint/3 vs verifier billing/cancellation/3: "I don't know what's happening to this app. Before few week i was enjoying the quality of the app and the new update just made me annoyed. I even couldn't select the song i love. It made me even more a"
- `c8867ec1-7050-48af-a28e-6590214cb393` enricher catalog/request/1 vs verifier other/request/1: "Its a great app with lots of artist and podcasts but i have some ideas to updates: make the option to block podcasts and videos podcats and another option is to delete history of what i heard like the"
- `c8b8940d-99d1-404f-81e4-56ac9191e2e8` enricher other/complaint/2 vs verifier other/cancellation/1: "Hate this application👎, I love islam"
- `c8ccb0b2-42b2-42eb-b25b-d84262aebd57` enricher catalog/praise/1 vs verifier other/praise/1: "The wide range of options are outstanding!"
- `c9272c67-6ed8-446b-b8a3-cf8e34f95d0b` enricher other/praise/1 vs verifier other/unclear/1: "It,s is cool and the best way to"
- `c9c5501f-5c24-4b7b-b1f3-d42c363b37bd` enricher playback/complaint/2 vs verifier usability/complaint/2: "If I play a playlist, I want to hear that playlist, not songs based on the playlist."
- `c9e2cb79-d617-479a-bc64-137589d2ba56` enricher other/complaint/2 vs verifier usability/complaint/3: "Hate the new updates I can't play my favourite songs anymore"
- `ca59b541-bf18-4bc6-b5e7-f37df2a29d5f` enricher usability/complaint/3 vs verifier access/complaint/4: "Spotify is great but it won't let me open my like songs for some reason for my Android weird that's never happened???🤔"
- `cae66fcf-1111-4e6f-9c2d-b0c318797924` enricher catalog/praise/1 vs verifier other/praise/1: "It is good for songs"
- `caf6cb18-a8c3-462b-8e38-c56f6a041829` enricher downloads/complaint/4 vs verifier playback/complaint/3: "It's a good app it has all the death metal I listen to. My only problem is why the hell do have to go offline to listen to downloaded music. And I have a 5g phone and it always says I'm offline unless"
- `cb35ce46-903c-4840-8bd8-ca512ea62389` enricher other/praise/1 vs verifier playback/praise/1: "One of the best audio apps in the game"
- `cb36c41e-b86e-434f-9b82-da442958e5fe` enricher usability/complaint/3 vs verifier usability/complaint/2: "I can say that this is one of the best song aap I ever tried. I can say they have a very good collection of songs but nowadays this aap is showing very very much annoying ad's. I literally threw away "
- `cb77d6f5-e0bf-4c7c-9a71-3ff832f9896e` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too much ads, after every taps there's ads, before the next song plays there's ads..Ads are everywhere"
- `cba17a1f-d9f2-4c7a-a673-9df9febf02b9` enricher billing/request/2 vs verifier billing/unclear/1: "Some option paid."
- `cbbba921-2cbd-49fe-9430-aa11237fc4c1` enricher usability/complaint/3 vs verifier usability/complaint/2: "Adverts start in the middle of the song now? Wow fantastic!"
- `cbfc2948-95ac-469c-a96b-c21a962798e6` enricher usability/complaint/2 vs verifier usability/cancellation/2: "What on earth have you done?! I dont want to watch video clips. I just want to be able to find my music. Roll this update back please or I'll be looking elsewhere for a music app if this stays"
- `cc678f39-94e7-4704-8ccf-9d6d74f28198` enricher usability/complaint/2 vs verifier usability/request/2: "BRING BACK OLD SONGS VIEW FORMAT IN PLAYLISTS ON SPOTIFY FREE, the new viewing mode doesnt allow me to preview songs or add songs from one playlist to another among tons of other lost features."
- `ccb7eaa0-3ca0-4c28-8402-093c9975c0d1` enricher other/praise/1 vs verifier playback/praise/1: "Iam lil peep and theis app is not working well for me and my wife I love it"
- `cd2a8146-6ff9-416f-8b6a-c74fca1c60de` enricher other/unclear/1 vs verifier downloads/unclear/1: "This only download fo mc slaat🐍"
- `cd475ac0-324a-4845-834b-43fbb034e5d7` enricher billing/request/2 vs verifier other/request/1: "Spotify bring back regular features,"
- `cd632c49-5b28-4f94-be3e-d0a5d748ded1` enricher other/request/2 vs verifier other/request/1: "Please make it like it was earlier"
- `cd64a9cd-9878-4254-af8c-d26bc73ec84b` enricher billing/complaint/3 vs verifier usability/complaint/3: "Earlier it was the best but now I don't know why they turned on shuffle songs automatically and it can only be changed by getting premium"
- `cd7a9952-43ac-4476-9f19-f0824b178454` enricher playback/complaint/4 vs verifier playback/complaint/3: "Got hang or sometimes not opening"
- `cd810400-ddb9-4271-83ad-30dbacefd028` enricher catalog/request/1 vs verifier other/request/1: "DJ AI lacking female version. Would be nice to have a female voice for DJ."
- `cdac6ddd-979f-440f-8f0f-5e05280d92a5` enricher usability/complaint/3 vs verifier usability/complaint/2: "Not just are they following this awfull trend of worstening 'even more easy to find your stuff' interfaces that hide almost everything. There's adds in premium version, even though spotify states ther"
- `cdb83af0-0e8b-41d0-9410-8cf0428e1699` enricher usability/complaint/3 vs verifier usability/complaint/2: "Sometimes there is an ad that says i would get 30 mins of ad-less music and then less than 30 mins later (literally 10mins later) there is another ad. It's also really annoying when there's like 3 ads"
- `cdbc7615-7c2e-444c-8566-fefc40ae0690` enricher other/complaint/2 vs verifier other/unclear/1: "Bhot bura"
- `cdd53354-70ca-4160-878d-ce9b68170902` enricher usability/complaint/2 vs verifier usability/unclear/1: "Irrigatingv advertisement"
- `cdd9f2ea-0d02-44ca-8534-c1bfae329056` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Love the app brilliant use it everyday, only problem I have noticed recently is that most of the lyrics won't load other than that amazing app"
- `cdf6276e-c6fa-4ec2-8890-d891726dd535` enricher playback/complaint/3 vs verifier playback/complaint/2: "The app won't stop automatically start playing the last song when ever I open it or connect to a new Bluetooth device. I removed all background permissions and so forth but had no change in the apps b"
- `cdf8ab83-2a97-410c-b80f-7e93324cfc1d` enricher other/unclear/1 vs verifier other/complaint/2: "👎👎👎👎sewden app my foot"
- `ce143420-fe90-47d8-a2db-0798f651b3d1` enricher other/complaint/2 vs verifier other/cancellation/1: "I'm Muslim dislike app"
- `ce472d44-e405-4fd1-8289-0e25008c931d` enricher playback/complaint/2 vs verifier playback/request/1: "Spotify is a top quality service. The only thing it's missing is a high quality codec for better sound quality."
- `ce47994b-bfad-45f0-bb52-2385596a7c96` enricher billing/complaint/3 vs verifier usability/complaint/3: "The shuffle because of update I can't even listen my playlist because it just play another song that can match "vibe" because I don't have premium to stop shuffle. I really used to like this app"
- `ce592455-858e-454f-a1c9-242dfdf65fd0` enricher catalog/praise/1 vs verifier other/praise/1: "Nice Bast Song ❤️❤️🥰"
- `ce70f488-2129-472d-9afd-a9f0601c439f` enricher access/request/4 vs verifier access/complaint/4: "I've been using spotify for sometime now and i've had no issues, i changed my phone recently and i can't login....it's either telling me that i'm offline or somehing went wrong...i. Really need help."
- `ce99b2de-d098-41db-abb1-ae6fc873caf0` enricher usability/complaint/4 vs verifier usability/complaint/3: "The Playing Now screen has completely disappeared from my app. I have no way to pause, rewind, or skip anything I'm listening too. Needs serious update. 07/12/22 Update: After several rounds of uninst"
- `ced2c425-3125-47ef-9232-d7eb61bf79cd` enricher other/complaint/4 vs verifier other/complaint/2: "Tha app is not working"
- `cee181bb-05e5-4f31-8333-d14d11306fb5` enricher billing/complaint/3 vs verifier billing/complaint/2: "current update is very disappointed... that updates main thing everyone subscribe the premium... i dont know y all app do this continously... its very bad... really disappointing... we earing songs wi"
- `cf29924c-f881-44a5-87cb-b56b58ad7559` enricher other/praise/1 vs verifier downloads/praise/1: "Fantastic app. Many options are easy to use and can be used offline."
- `cf44c2af-eb80-4a22-b348-cf86248fb6db` enricher other/complaint/2 vs verifier other/unclear/1: "Don't install the application They don't understand anyone's difficulties, they don't believe in the people of Pulpar."
- `cf4d5b1e-87d9-4821-bb3a-101def78fcce` enricher usability/request/1 vs verifier catalog/request/1: "Suggestions can be more easier accessed as a never-ending list rather than 8by8songs"
- `cf59511e-3dbc-49e4-8127-e57eed0cf1b9` enricher other/cancellation/2 vs verifier other/cancellation/1: "Its Haram that's why uninstalling."
- `cfaf9c6c-87c6-4007-ab34-853d2b43596f` enricher other/complaint/2 vs verifier playback/complaint/2: "Very bad music system poor"
- `d09b36c7-c34f-4672-a177-bac26ff0bc15` enricher billing/complaint/3 vs verifier usability/cancellation/3: "spotify is on it's way to become the worst streaming platform. what should the basic features of a music app are only accessible for premium. there's not much you can do on the app anymore."
- `d09b97fd-e97d-4bde-8aba-69804dd5c4bd` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "Very bad the new update made the app a paid one uninstalling cant pick our songs there is only shuffle play I'll go for other apps like wynk and gaana this app from my favourite app it changed to the "
- `d0b83072-33bd-447c-9dca-e444fa0da4b1` enricher other/praise/1 vs verifier playback/praise/1: "I can hear music now"
- `d0c2a8a9-ed23-4f7a-832f-294df0e79840` enricher other/praise/1 vs verifier other/unclear/1: "You can listen to music 🎵🎵😀🎵🎵😀🎵🎵😀"
- `d0d232e9-de6f-4788-9685-b901a721c240` enricher other/unclear/1 vs verifier usability/request/1: "Add should be low"
- `d121232f-996d-405f-b3ce-cd4e22d197fb` enricher billing/praise/1 vs verifier other/praise/1: "An app to just get lost in the music. Spotify Premium is definitely worth it - I use this app daily with no problems at all! Highly recommend to try"
- `d13d1729-8077-499e-988a-4f35ef956aac` enricher usability/request/2 vs verifier billing/request/2: "Too much ads and we dont want your subscription, make it free 😔"
- `d13ea774-4318-4f99-82bd-b1c115e59d7e` enricher other/cancellation/2 vs verifier other/cancellation/1: "I no longer use Spotify"
- `d155cb08-4546-4508-8aa9-065fe35b5194` enricher catalog/request/2 vs verifier catalog/complaint/2: "Bring back playlist song previews!! I don't understand why this feature was removed but not having it makes making playlists extremely difficult. It has genuinely reduced how much i use the app becaus"
- `d1cfe231-4339-4663-8972-e7c06cf6a8f4` enricher playback/cancellation/3 vs verifier other/cancellation/2: "Uninstalled due to android auto issue"
- `d1d117e3-c16d-4833-9583-e73dd64acda0` enricher other/praise/1 vs verifier usability/praise/1: "Excellent choices, easy to use."
- `d2722daa-453d-444c-b8ee-24987776f99f` enricher usability/complaint/3 vs verifier usability/complaint/2: "Great music app. More enjoyable with spotify premium so theres no ads, but I feel like there could be less ads when you don't have premium. When you do an online mix, I think it's fine with ads to be "
- `d272d536-6a8c-4da7-86ac-a5458f38e921` enricher billing/complaint/2 vs verifier billing/complaint/3: "They're seemingly trying to engineer this app to be the worst possible experience for non premium users but it is still the best music streaming service"
- `d2e89b34-b40c-4d62-ae3a-16299de3dd64` enricher other/request/1 vs verifier usability/request/1: "These app should have.. Sleep timer"
- `d2f2f760-f77a-4025-90ad-afd36dbe584e` enricher other/praise/1 vs verifier other/unclear/1: "Good a"
- `d2f6b32b-6d45-4fc3-b057-64910598bd7b` enricher usability/complaint/3 vs verifier usability/complaint/2: "I don't know why the hell app is have so much of adss !!!!!! It's spoils the mood which is created once really .... Yesh ..... After 5 to 7 min the ads goes on nd it really sucks !!!!!!! ....."
- `d2fb0597-3a90-4b77-98ca-468fbd4f0794` enricher other/complaint/2 vs verifier other/unclear/1: "Bhagwan maff nahi karega kabhi yaad rakhna Spotify walo"
- `d30674c6-2cfa-4915-b5e5-109948ac0a53` enricher usability/complaint/2 vs verifier usability/praise/1: "It's nice having mumusic to stream for free. The ads are a bit annoying but it's a small price to pay. Plus if you have premium you don't have to deal with ads."
- `d32dcc22-26d1-4841-9540-5582f20b7122` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "Downloads don't stay downloaded"
- `d3378144-589d-4f3c-8a9c-52746b68e9e2` enricher billing/complaint/3 vs verifier billing/complaint/2: "Well can I listen to music on my xbox series X without the shuffle but when I wanna use a mobile version I have to pay For premium to remove shuffle"
- `d33a4b0c-40d1-4bee-a868-1db975fcc7c1` enricher usability/complaint/3 vs verifier usability/complaint/2: "30 minute of no ads didn't work, literally a 4 min song and I got an ad right after it"
- `d3651218-4f19-4e33-afeb-2d4212c1e670` enricher other/praise/1 vs verifier other/unclear/1: "#1 music 🎸and podcast🎙️ application 💥 for when you get the need 👙 for some time out.💡"
- `d39b008d-7d46-4d78-8586-0b675b017864` enricher billing/request/3 vs verifier billing/complaint/3: "Why does everything have to be premium I would request the company to minimize the premium cause if I want to listen to a certain part of song they tell to buy premium and when i want to listen to som"
- `d3d2e3bc-3ed9-466f-a8c7-5aab45f29bf5` enricher playback/praise/2 vs verifier playback/complaint/2: "Slightly laggy but nonetheless,still my favorite music app"
- `d3d81ef6-b900-4930-888d-df3fdc7ef1df` enricher playback/complaint/4 vs verifier playback/complaint/3: "I live this app, but since the last update, it randomly stops playing after the first sing in a playlist. I've tried everything. Uninstalling/ reinstalling, clearing the cache and everything else I've"
- `d3fc4fa5-5fc2-4c9c-820f-c90a56c53255` enricher usability/complaint/3 vs verifier usability/complaint/2: "Can't skip the song and forward few seconds"
- `d40a6c99-40a4-48f3-ad0f-296b557acec4` enricher billing/complaint/2 vs verifier usability/request/1: "I'm paying for this app. I don't want any suggestions on my saved play list like Pandora."
- `d42943c7-58cd-4518-b9b6-dd002e3ec960` enricher usability/complaint/2 vs verifier billing/praise/1: "It's an awesome app to use for streaming music. I'm on the free plan and when I upgrade I'd add the 5th ⭐"
- `d4519010-d200-4aca-ba79-5b080bad3833` enricher catalog/complaint/2 vs verifier other/complaint/2: "Man there is no canvas option available, three stars due to that reason"
- `d457dba5-0b9f-4c17-b6c8-9ffa6aefb52b` enricher usability/praise/1 vs verifier catalog/praise/1: "Easy to navigate app. They have had every song I looked up."
- `d46b472c-dcb4-4633-8865-1f07715d9ca4` enricher other/complaint/2 vs verifier other/unclear/1: "I hate this app and swedan ,I love you islam"
- `d47a188a-bc4b-4577-8e22-13577a9e758b` enricher usability/complaint/3 vs verifier usability/complaint/2: "There is too many ads, I understand that the company wants to make money but 4 ads for every 2 songs is way too much And everytime you look at the lyrics theres another ad. Its also annoying to put so"
- `d49763d9-64de-40ff-b767-0e25ea17dd3a` enricher support/praise/1 vs verifier access/praise/1: "I really love this app and I really love support services thanks to team that I got my account back few days ago unfortunately I deleted my Spotify and some kind of technical or login issue in my phon"
- `d4b150e6-1ad9-4226-a73e-f0aafcbfc9d9` enricher catalog/request/1 vs verifier other/request/1: "Nice app. It would be great if it would be possible to see the music lyrics in the TV when I cast using the Google Chromecast for example."
- `d4cbda1e-a62f-4ec9-a445-9a6fd8bcfb65` enricher access/complaint/3 vs verifier billing/complaint/3: "Korea version doesn't work after 1 week. 7 day trial only"
- `d5228b72-2db5-4399-959a-8f5d220de378` enricher usability/complaint/3 vs verifier usability/complaint/2: "Random podcast I don't care about pop up interrupting the music. Pointless to pay for premium as these cannot be skipped via the car stereo as you normally skip the songs"
- `d54da0b8-d5ce-434f-bd68-9e5bc783e062` enricher usability/complaint/3 vs verifier catalog/complaint/3: "Spotify, this app would be a 5 or 4 if u never made this annoying update. First of all, when i type in a song i want, most the time it just starts playing random songs from a playlist that the song i "
- `d5583d07-d0f6-493a-8527-f521e2cfd254` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "There used to be one or two ads in between songs, now there's 5 or 6 in between and no more 30 min ad free music. Used to love Spotify not any more."
- `d570af41-7514-4a8f-94da-e27f248db6ab` enricher catalog/praise/1 vs verifier other/praise/1: "I enjoyed the music"
- `d5827513-f110-459c-ad33-e0af6dd742ba` enricher usability/complaint/2 vs verifier usability/request/1: "Good, but missing a feature. Can't edit playlist descriptions on mobile."
- `d5a7b30d-6fd8-4346-a378-c57ff2c06095` enricher usability/cancellation/3 vs verifier usability/complaint/3: "Just advertisments... Lots of advertisements.. After every song.. I mean common.. The people who have or could have subscription will take it.. But who could not.. Don't download.. You are going to re"
- `d5d8b080-6401-4552-b07e-d82d5f1475b0` enricher other/complaint/2 vs verifier other/cancellation/2: "The new update is worst... Spotify has showed their true face, now see how they go down. I am going to shift to Jio Saavan."
- `d60a7675-db91-4e7a-baee-b7d2f7e97936` enricher catalog/praise/1 vs verifier other/praise/1: "Knows my musical tastes better than me. Lol."
- `d619a74a-7902-460d-b825-28c30747562a` enricher other/complaint/3 vs verifier other/praise/1: "The "SPOTIFY APP" is for listening high quality Audio from different artists you like..Its also user friendly for everybody...Students or Adults also can listen many podcasts which they like to listen"
- `d6284e21-db16-4bfa-9e91-97ef48eb8dcd` enricher usability/complaint/3 vs verifier usability/complaint/2: "Its good to listen to music on there because of all the special stuff they do. As a person who don't have preimium at the moment I don't understand why there giveing 5 ads when they used to only give "
- `d6420cdc-cda5-4d79-8a57-cf5c70008c09` enricher downloads/praise/1 vs verifier other/praise/1: "A great app that has 99.9 percent of the music from all over the world. The best part is the reasonable price and reliability especially since you can download songs for when you're offline. I highly "
- `d6430cbb-7e92-466f-b8bd-9efce466ba68` enricher other/complaint/2 vs verifier playback/complaint/2: "Pretty bad on moblie w that its on ps4 tho"
- `d6437e8e-29ea-4220-8735-38d4a69a7c5d` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Why thunivu movie tamil songs(ajith) not available in application. What your people doing. Very worst app. Only Partiality app and promotion for money only."
- `d6591c11-34ad-495c-b8ec-9d96413b9016` enricher catalog/praise/1 vs verifier downloads/praise/1: "This Spotify app is wholesome if you're looking for something to listen then this app is for you you can download from podcasts to video game music"
- `d69f1528-389d-4056-b268-cd897c1d5f7a` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Latest release punjabi songs of saukan saukne movie and some other movies is still not available in the app."
- `d6db6c4c-15e7-47ec-aff9-8586dbff6c78` enricher usability/complaint/3 vs verifier usability/complaint/2: "More ads than Pandora. 4 ads in a row, 1 song, 4 more ads..."
- `d70b297d-9cf0-4004-b2e7-a9d8701dfbe6` enricher usability/complaint/3 vs verifier billing/complaint/2: "Premium options are not good. There are more ads than music . Became worst app"
- `d70d0bf5-4c6a-46f4-b66a-a74cb67973e2` enricher playback/praise/1 vs verifier other/praise/1: "It's great 😃👍 for me to listen in the background thank you for the app without it I would have been paying for other music apps and thank you"
- `d71c690b-ce20-41d7-9f5e-0e986fa1a78b` enricher other/complaint/2 vs verifier other/praise/1: "Good really good the song doesn't give me a good idea to get"
- `d752e23a-ff92-45eb-94d1-fa264e53add7` enricher catalog/praise/1 vs verifier other/praise/1: "New user but happy one Gr8t to get playlist 5****"
- `d752ebc6-a139-486b-9d41-bc8e399c0aa2` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "ɴᴏ ᴅᴏᴡɴʟᴏᴀᴅ"
- `d771f57a-b57d-4521-a0d3-f40ee20c0dbd` enricher catalog/praise/1 vs verifier other/praise/1: "Amazing app I listened Twice 'I can't stop me' it was amazing and I saw the lyrics Thank you"
- `d787fac1-0210-4c17-b741-a7b7580cd061` enricher playback/cancellation/4 vs verifier playback/cancellation/3: "I used to love this app. It was the only place I got my podcasts and music but recently it either stops whenever it wants to or it won't stop without me uninstalling it. It also starts to play a playl"
- `d78c963c-70c9-4141-96aa-79a793eb8e12` enricher catalog/praise/1 vs verifier other/praise/1: "Very nice music 🎶🎼 App in the the world 🌍"
- `d78d3992-30fc-46f6-93e1-3c0af2e67c7a` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Can't find shin megami tensei 4 ost B2 . Only cover song appeared"
- `d7c5b421-c4df-44b6-aab3-97724e2651b8` enricher usability/request/1 vs verifier billing/request/1: "If I buy premium, would the app interface rotate too if I rotate my screen? Now, 2023, you can. Not sure about the free user."
- `d7d928c8-e71d-4512-a8ca-017d6ea10788` enricher usability/praise/2 vs verifier other/praise/1: "I LOVE this app! It is so much fun to use! There is many good songs on here and many different artists which is amazing. I totally recommend the payed version because I don't even experience any adds!"
- `d8035051-85af-4ee1-9274-6773d1156924` enricher usability/request/1 vs verifier catalog/request/1: "Please make this app show the lyrics"
- `d84a82e7-2ea9-4aee-9adf-b5e2b7ae656c` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "Waste app worst experience with ads....I am deleting it....🤝"
- `d8623953-b14b-4458-9703-48705a5ecbef` enricher usability/complaint/3 vs verifier usability/complaint/2: "Eveything is nice except you can hear some songs in between the adds."
- `d898636a-78ca-47e2-8c8a-9ef9f0f01f92` enricher catalog/complaint/3 vs verifier billing/complaint/3: "Very good app.All songs which I want to listen can be found 😄. Problem is to many adds. In a recent update, it is made that the lyrics are made for premium users only. Very sad thing while is used to "
- `d8996bf8-9140-4b4f-be58-19098eef0aed` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "First time I rated this app was almost 10 years ago, and more recently, 7 years ago ... 5-stars both times. It pains me to not return the same review today. Though I still primarily listen to Spotify,"
- `d8af15df-1963-4ad6-9d0f-5efc962401f9` enricher other/praise/1 vs verifier other/unclear/1: "Legit this app is EGSTREEMLY PENG"
- `d8c992d3-342a-4f61-b865-255c6a70e2a2` enricher usability/complaint/3 vs verifier usability/complaint/2: "Dear sweet baby jesus for all that is holy fix whatever is causing the damn app to "unlike" songs I have liked. It is absolutely doing my head in."
- `d8dbb3a7-d883-4c7f-8a7b-9109490feb25` enricher playback/complaint/4 vs verifier access/complaint/4: "I got a new phone and now it stays stuck at the opening logo. It's been like this for a week."
- `d906c582-0430-41f0-8045-dccffdc30faf` enricher billing/complaint/2 vs verifier billing/complaint/3: "Because of new update Spotify only want premium 😞😞"
- `d93119c6-dc22-46b8-ba54-b8d02c480ae3` enricher usability/complaint/3 vs verifier usability/complaint/2: "God! It's the worst! Why is it so hard to make it to where I can play whatever I want without it being on shuffle, it's not just playlists, it's normal songs too. It's the dumbest thing I've ever seen"
- `d953ab66-ad26-4093-a857-f6033d53b41b` enricher other/unclear/2 vs verifier other/unclear/1: "APOLOGIZE TO LISA!!!!"
- `d98ab80b-8691-40cf-b62f-cf1d1c537f9b` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "i unable to find zee music company song"
- `da0d1ae1-c4bd-4e02-a57c-e269d9c7fa2a` enricher usability/complaint/3 vs verifier usability/complaint/2: "Every time I skip a song/ pick a song that's not on the playlist that I'm playing it plays an ad"
- `da3a7fc0-22ed-436c-a924-28fb21820ab7` enricher catalog/praise/1 vs verifier other/praise/1: "I love spotify it Always has my music"
- `da5cd791-316b-4bef-b337-1f822bd9bc89` enricher billing/complaint/4 vs verifier billing/complaint/3: "Can't even play song we love to listen they have charged premium to listen songs... Worst experience now they will decide which song should we listen..."
- `dabaf5e4-6809-46f4-9263-e9a192e45c91` enricher catalog/complaint/3 vs verifier usability/complaint/2: "Playing suggested songs during a album when I don't have the option on. Never had this problem before. I would click on the album and it'll always play the songs in that album not songs that aren't ev"
- `db5708e7-db92-4eb5-991f-2fa23712b6ea` enricher billing/complaint/2 vs verifier other/unclear/1: "Only prime use"
- `db73957b-fa40-4126-8fac-c404581bebfa` enricher playback/complaint/3 vs verifier usability/complaint/3: "在播放我的最愛的清單音樂常常跳出去，沒辦法聽清單上所有的音樂，常常跳到沒聽過的音樂，很困擾"
- `db7adf64-a6ca-4b61-b655-032f8a192e1e` enricher usability/praise/1 vs verifier other/praise/1: "It's amazing i get to listen to music for free without having an ad every 2 seconds im thanful for this app thank god."
- `db823cbc-996f-4942-ab3c-0607d907e302` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too many ads very annoying, Ads is running from 1 min"
- `dc0f0e2b-5301-45d2-848a-826d768971ee` enricher usability/complaint/3 vs verifier usability/complaint/2: "Too many adds. Also adds random music that i dont like on my perfectly planned playlist, and it doesnt let me delte it"
- `dc407cba-03c9-4d5f-be9c-b881effffb14` enricher catalog/request/2 vs verifier usability/request/2: "Overall design and user experience is great. However, I have a 1000 song Playlist but seem to be hearing similar songs all the time even when it is shuffled on different days. Spotify clearly has an a"
- `dc426215-b611-4aac-8e59-60c025bbce14` enricher billing/complaint/4 vs verifier billing/complaint/3: "cant pay with momo, always redirect to google play screen even when my phone has momo already installed"
- `dc55b2cd-5fae-4f88-9a37-c395b5d7c3e8` enricher usability/complaint/3 vs verifier usability/complaint/2: "Meine on repeat Playlist aktualisiert sich nicht kann mir dabei jemand helfen? Danke Sonst eine Super App"
- `dca03f31-d779-419c-a8c3-049ae869bd9c` enricher usability/cancellation/3 vs verifier usability/complaint/2: "Ads make me wanna throw away my phone and the lyrics won't show up now. Already switched to another app. L Spotify"
- `dcc2d541-46bb-4c55-84ed-c662483b47ba` enricher downloads/praise/1 vs verifier other/praise/1: "I bought a new phone and somehow my music didn't download the voice but with Spotify I got my music back"
- `dccdb5b3-d99c-4875-9400-ebcff0215ae0` enricher usability/request/2 vs verifier usability/complaint/2: "Hey y'all this new home screen UI is so awful. Can you at least give us an option of UI in the app."
- `dcfcc810-0969-404e-b6bc-4a0fec80c255` enricher usability/complaint/3 vs verifier usability/complaint/2: "You can't choose song all song always random not like before"
- `dd34491b-2346-4493-9f74-f934db8ee1c3` enricher other/praise/1 vs verifier usability/praise/1: "This app is satisfying my mind I'm enjoying my playlist 😁....... ☺️ thankyou for suggesting this app for me 🤍 please avoid add 😅 ..... Thanks ☺️"
- `dd53a3e8-3f07-4d1f-9f77-476b2a7729e0` enricher other/complaint/2 vs verifier playback/complaint/3: "they took their servers down right when a certain someone made a comeback bro its so obvious and annoying, Spotify alwyzs does this fix your damn app or I swear I'm suing"
- `dd67072f-9e9e-4e58-bb2a-59fc96bd7d24` enricher other/complaint/2 vs verifier other/unclear/1: "Best to worst..."
- `dd762df5-b090-4d14-8580-539c550124a5` enricher catalog/complaint/2 vs verifier catalog/complaint/3: "Listening to the songs and else is alright but most lyrics keep on saying "couldn't load" whatsoever is so exaggerating"
- `dd857562-8257-4312-96da-201b86028da6` enricher catalog/complaint/3 vs verifier usability/complaint/3: "Problems i have with Spotify currently: 1: I have 1000+ songs in my "liked" playlist but only 50 get repeated constantly when on shuffle 2: the most recent update brought back enhanced to "liked" play"
- `dd8f9c4f-10ba-4024-b222-debbf8e9b05e` enricher catalog/request/1 vs verifier catalog/praise/1: "Almost every single and album is seen here. Spotify also personalises some playlists of mine! I would also love if Spotify would recommend more songs to me."
- `dd9ba46f-662b-43d7-95fe-87629177f267` enricher billing/complaint/2 vs verifier billing/complaint/3: "Worst update ever . Everything is gone to premium"
- `ddc00aa1-a75f-4389-b8ca-43908860390d` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Don't like Spotify adding random tracks to my lists"
- `ddd12dfd-b375-482f-83ac-930e575863da` enricher other/praise/1 vs verifier other/complaint/2: "Like it but could be better"
- `de2c26fe-ab5b-422e-acf0-a7b0762ad738` enricher billing/complaint/3 vs verifier billing/complaint/2: "The tricks of not playing the said song and adding the option as *want to listen to you fav song so go to PREMIUM* like what the hell man.Not satisfied"
- `de6aa304-2a7a-4116-b97b-683068273265` enricher other/request/2 vs verifier usability/request/1: "Please find a way to restore delete account Playlist"
- `de6e8632-67c0-4b0f-8b90-f74262c85b22` enricher usability/praise/1 vs verifier other/praise/1: "I enjoy the ease of using the app to listen to my favorite music"
- `de7e10da-9efa-41fe-b41e-7cda8fe98ec7` enricher other/complaint/2 vs verifier usability/complaint/2: "I am having a good time listening at this app but things not good lately. Why spotify made songs harder just to listen music? This is disappointing!"
- `dea04fb5-bdbe-473b-a00a-391f8a764819` enricher billing/complaint/3 vs verifier playback/complaint/3: "It's annoying bro I wanna play my song and it's playing others songs 🚶‍♂️ so annoying"
- `dea64e18-9c0c-4531-8c78-deef0d18d44f` enricher usability/complaint/4 vs verifier usability/complaint/3: "It has been SUPER BUGGY. I can't search music in my own Playlist. Can't click on anything. Also, you should put the "hide from Playlist" button away from the "add to Playlist" button. Did you guys fir"
- `decd414c-e51a-4440-9525-f3e7c9e5d291` enricher playback/complaint/4 vs verifier downloads/complaint/4: "Why do my tracks randomly skip to the next one in queue when my phone is locked? This has been happening for like 2 weeks and my boyfriend has experiencing the same thing. Also, when I have no interne"
- `dee4a1b2-fe50-4ba0-bd1a-a61f90c0d8fb` enricher other/praise/1 vs verifier catalog/praise/1: "Great choice and variety"
- `def3b110-ca80-4298-9118-114c84e4d187` enricher playback/complaint/4 vs verifier playback/complaint/3: "I've reviewed Spotify very well infact I gave the app 5 star too but seems like it's all in vain, the app everytime hangs and turn off whenever it wants I'm too fed up with this app now"
- `def5de67-fb81-4389-a239-fe997ca5b5a1` enricher usability/complaint/4 vs verifier usability/complaint/3: "a total downfall. unskippable multi minute long ads, forced shuffle mode, no playback control. its not a music app anymore, its a radio that plays songs and you can't control anything. did I mention t"
- `df6ad4e2-c10f-4b9a-9dc2-953d41e13d29` enricher billing/praise/2 vs verifier usability/praise/1: "It is nice because if you dont have premium you can still have 6 skips until a hour later"
- `df77019a-06a7-4e58-8a75-5b92f4b680b6` enricher usability/praise/1 vs verifier other/praise/1: "U should download Spotify now interruptions nothing I love it no problems at all I recommend it."
- `df9534f8-0af2-4ce6-bfd8-1e69382cb8c1` enricher other/praise/1 vs verifier other/unclear/1: "Supop"
- `dfb5f792-9180-466d-8d8d-371e1c264ceb` enricher catalog/praise/1 vs verifier other/praise/1: "Perfect application for all the music i like"
- `dfbd4af7-2132-40a1-bac8-6766a5e4bb89` enricher other/complaint/2 vs verifier catalog/request/2: "where's da fookin lyrics"
- `dfdb5010-802d-4fba-9d7b-a602d56818f7` enricher catalog/praise/1 vs verifier other/praise/1: "It is best for ear music ,tuns and play list song"
- `e00cb3e3-c9fc-4d6a-a680-f7ecbaeac4df` enricher billing/complaint/3 vs verifier billing/request/1: "It should let you listen to the song you like WITHOUT PREMIUM."
- `e0284141-e796-48c9-ba12-0c101d116f3b` enricher billing/complaint/3 vs verifier usability/complaint/3: "Update: Do NOT pay for Premium! It still plays ads!! Such a Scam!! ___________________ App Very intrusive, App start playing songs as soon as I closed other other apps or seat in the car orconnects to"
- `e044f755-af64-412a-aea5-f9b2c2a178c9` enricher playback/complaint/2 vs verifier billing/complaint/3: "I've been a Spotify user for like 4 years, and I've been using the premium account for less than a year, but I didn't have the Canvas feature. Even my friends who aren't premium members can see canvas"
- `e052554e-fa74-4319-ba45-7af0454e75d4` enricher usability/complaint/3 vs verifier usability/complaint/2: "Still my favorite music app. Edit- sure would be nice if it would actually shuffle my ENTIRE playlist instead of selecting 50 songs or so and repeating those. I've got WAY more songs than that, and it"
- `e06e3b3c-db6c-40c6-bbea-40c5f4b677cf` enricher playback/complaint/4 vs verifier access/complaint/4: "I can't open my app what us wrong with the app???"
- `e0d3e2e2-6de1-44f0-81be-9a61419d3558` enricher other/complaint/3 vs verifier usability/complaint/3: "Bloody hell, the pairing to other devices suck like cant even connect to the ps5. Their steps dont even work."
- `e0d87882-9a82-4691-8646-ef6350e11d5c` enricher playback/complaint/3 vs verifier billing/complaint/2: "You guys are very slow after buying a premium plan also"
- `e0e10eec-9f3d-4bde-813e-bc9e8c2a6a84` enricher catalog/complaint/3 vs verifier downloads/complaint/3: "Deletes songs every so often"
- `e1069da6-2cb5-4695-86fe-3d988c8dd6d8` enricher billing/complaint/3 vs verifier billing/complaint/2: "Trash I mean u need premium to repeat the song 🐷🐷🐷🐷🐷🐷 Trash app"
- `e13d7b53-568a-403c-992f-0039abafd87b` enricher other/unclear/1 vs verifier other/praise/1: "Good for gaming hahahaha"
- `e17cb1bc-af5e-4524-8200-d791cc95506d` enricher catalog/praise/1 vs verifier other/praise/1: "Great library for your favorite music 🎶"
- `e185dee8-90ed-4954-a637-d888b066d4b1` enricher playback/complaint/4 vs verifier playback/complaint/3: "The app had had the bug of stopping songs half way through since like 2021. Still hasn't been fixed I personally have tried all the recommended steps to fix it and it still happens don't pay for premi"
- `e18e7b06-86ab-488e-b9d8-c67de88bde23` enricher other/cancellation/2 vs verifier catalog/cancellation/2: "They are blocking Christian artists who are standing for their rights and not paying artists. If they are removing certain artists for standing up for what they believe but allowing rappers to stay on"
- `e1d8c31d-7e48-423e-b007-28887a3c394e` enricher catalog/praise/1 vs verifier other/praise/1: "ang ganda ng mga kanta"
- `e223fac8-7e9c-465e-880c-0299be08ad17` enricher usability/complaint/3 vs verifier usability/complaint/2: "I love this app, but it would be nice if there wasn't ads every half hour, or that we could only have six skips an hour. It's getting a little ridiculous."
- `e2538dac-1f51-4bdf-9217-250cfccc4f89` enricher catalog/praise/1 vs verifier other/praise/1: "Available music of my choice, constant and without ads thanks Dr"
- `e2799101-30c4-4400-b923-466849575525` enricher other/unclear/1 vs verifier other/praise/1: "Quran power"
- `e2c063c9-4861-4deb-bac8-c468666fca42` enricher catalog/complaint/3 vs verifier usability/complaint/2: "O ponen la letra de las canciones ya o quemo todo. Qué es esto ahora. No le pongo 0 estrellas porque no sé como se hace porque vamos que rabia."
- `e2c757d7-5145-4515-84bb-b0730f8cc594` enricher billing/complaint/2 vs verifier billing/praise/2: "This is very awesome app but just has one flaw that the pricing are too much for Indian users with that much price I can buy 3 year ganna subscriptions for 1 year of spotify subscription but the money"
- `e2e59961-37a8-40d4-ab48-6f5949c0c283` enricher other/unclear/1 vs verifier other/complaint/2: "discord is better"
- `e321d40b-4a2b-4bc6-bf82-2c34ca59b63b` enricher downloads/complaint/3 vs verifier downloads/complaint/4: "When using the app in a place with no reception/WiFi like a plane or the underground my liked songs list does not load, it instead shows a spinner forever. I routinely have to force stop the app, then"
- `e323dd32-fd86-405f-b1f1-965ab58e5a8a` enricher billing/complaint/3 vs verifier other/complaint/2: "Bhen ke lodo ek gana sirf ek gana Bina add ke chala do na Are har koi amir ka choda nahi hota ha ok Jo tumhari membership le le 🤬"
- `e34b1b27-09a7-4357-a0bf-9b2e7c612d9d` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Stop adding songs to playlists 😭😭😭😭"
- `e34ff728-d964-4857-8586-06f1b02ee399` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "Great, just don't i can't download the music otherwise no complains"
- `e36cc761-ee14-4d82-b461-989ee4723fbb` enricher billing/complaint/2 vs verifier billing/complaint/3: "Had a 160 hour playlist before I got a free trial of premium, wasn't able to afford to pay for premium, so my playlist got cut down to 32 hours and I'm not a happy camper."
- `e379bb56-28ef-45af-8ba9-ec5d29ea3d06` enricher catalog/complaint/2 vs verifier usability/complaint/2: "Music shuffle is terrible, unlike last time"
- `e3cd380b-a8fb-4299-9d4a-b36a2533d4d9` enricher usability/praise/1 vs verifier other/praise/1: "Woooooh,I like the app it's flexible and easy to use.....you listen to nice music"
- `e3d85377-419c-4fbe-a930-9d0f37fd6e70` enricher usability/praise/2 vs verifier usability/praise/1: "I use the unpaid spotify... And i get 6 skips an hour... The adds are few and keeps a nice record of your music and also suggests nice music according to what you've been listening to"
- `e3e8d6e0-2350-4673-a471-0c1612437046` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "Very bad it has changed first it used be advertised which was understandable but know we can't play the songs we want and can't skip the songs too it is so annoying it's like you are forcing to buy th"
- `e3f9f210-2df8-449b-af96-c828c53889e0` enricher other/unclear/1 vs verifier other/complaint/2: "Tatting appp"
- `e41cc90d-c232-498c-b8dd-ab026d3257f9` enricher access/complaint/4 vs verifier playback/complaint/4: "I can't play it with my wifi connection. Baaaad"
- `e433b512-375b-421b-8830-efd3c7bcdafe` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Waise toh yeh app thik hai par bohot se aise gaane hain jo isme nhi hai"
- `e44cb528-6cd5-4393-984a-064d9e2b9fe0` enricher other/praise/1 vs verifier catalog/praise/1: "👍 🦸‍♂️ best musics💯💯💯💯"
- `e478eb33-20ab-4a4f-a53c-5606b2df8694` enricher billing/complaint/2 vs verifier usability/complaint/2: "Wish I could skip more. 😒 Otherwise, pretty decent app"
- `e48f3290-beb8-44b5-acbd-baddd8e34550` enricher playback/complaint/2 vs verifier usability/complaint/2: "I tried many many time to play my fav song.. but it change to another song😠 its make me more stress😠"
- `e4b31305-92b9-46e7-9f03-e803d7ede11d` enricher other/cancellation/2 vs verifier billing/complaint/3: "Because of Recent Updates The App Became Worse Than Before only restriction they didn't do is it should play the song after exiting the app became worst app time to look for alternatives"
- `e4b4f7b1-305a-4174-980a-44b71286f3f7` enricher billing/complaint/2 vs verifier billing/complaint/3: "app is garbage. don't bother without premium. with premium though, a good experience. is what i would say if they werent constantly advertising spotify duo to me. seriously i pay $10 a month for NO AD"
- `e50cf734-9c5c-41f9-a100-dcd9a89f08e9` enricher usability/complaint/3 vs verifier usability/cancellation/2: "I love Spotify but like why is there a listening history now??You also can't even delete it😭 also after like one song 2 freaking ads will play, like it tells you "30 mins of free listening time" then "
- `e53a6c27-a3a0-477b-9485-3cd666e8b416` enricher playback/complaint/4 vs verifier playback/complaint/3: "I honestly wish I could give Spotify a better review than 1 star, but the amount of crashes and general misbehaving of the app prevents me from doing so. I can only list a cpl since I'm limited to 500"
- `e5da4d9b-3f47-408f-9a61-e18057a81b00` enricher other/praise/1 vs verifier billing/complaint/2: "Not all the Indians butt hurt that Spotify isn't free anymore and randomly giving it 1 star rating. Grow up people. Its the best music app out there especially if you are into foreign artists."
- `e5fee5d5-0d8d-4c70-bd52-71ffb2160da4` enricher downloads/complaint/2 vs verifier other/praise/1: "Love it as always, I don't know how to download music for my ringtone this is the best music app I've ever want anymore. Thank you!!!!!!"
- `e6057e23-81b0-49f4-ad72-38f36fa1abef` enricher billing/praise/1 vs verifier downloads/praise/1: "I love this app! Inexpensive and all my fav music, downloads super fast too!!"
- `e62fa232-ecde-4b1e-9da1-ddb0b65e349e` enricher usability/complaint/3 vs verifier usability/complaint/2: "Nice songs recommendations I find lots of new songs but the quality of ads is wrost. Weird ads asking to buy premium plan in hindi language. You want to show ads it's okay but dont show nonsense ads l"
- `e651c7d4-8991-406e-b6d4-fddf979a2b5f` enricher playback/complaint/4 vs verifier playback/complaint/3: "New update is completely buggy. Songs don't play, queue list stops playing. Forward buttons don't work"
- `e65461b6-cc7f-4a82-9ad6-529d4d5ef3a5` enricher billing/request/2 vs verifier usability/request/2: "Why the basic features are removed?????pls add"
- `e6837972-f3e2-4656-8743-f1af272d6e40` enricher billing/complaint/3 vs verifier usability/request/2: "Spotify remains a good music streaming choice but here are some issues you should note about Spotify if you are from Africa. 1: They have refused to give us the Canva feature till date. 2: Their sound"
- `e6aa51fb-8943-47dd-8676-d104b8ba2409` enricher billing/cancellation/3 vs verifier usability/cancellation/2: "Complete hating this app now and uninstalling it permanently, repeat shuffle automatically is on as we need to have premium account to remove it , secondly so many ads as if we are here only to listen"
- `e6d68922-5d62-4cf7-a201-88110d1770d7` enricher support/praise/1 vs verifier playback/praise/1: "Great music service, the audio is high quality and the app is easy to use. Also very quick and friendly support."
- `e6ee90e9-9c2d-4407-99a4-f51204364aa0` enricher playback/complaint/2 vs verifier other/complaint/2: "It amazing but there is a bug that meed fixing"
- `e6fa60d5-cc00-4b78-a714-0076a209fcfd` enricher other/unclear/1 vs verifier downloads/unclear/1: "It's pretty fun and convenient Downloading podcasts and music: you can- at least on the premium edition- download songs and podcasts although, from what I've seen, they do not turn into files on your "
- `e6fae4c6-e283-42e2-b588-397f412961a6` enricher usability/complaint/3 vs verifier usability/complaint/2: "It is a great music app, it has very good music, but it has adds and it hasn't been 30 minutes yet, and it constantly asks you "buy premium so there are no adds. Well I don't want to spotify, leave me"
- `e71e28ea-87a1-44bb-b898-ff87153b8e77` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "App is good to risen songs. But fail to download song"
- `e73994c0-9f3a-49fc-b48c-8a5d74d3b1ce` enricher usability/complaint/3 vs verifier usability/complaint/2: "Currently having issues with the autoplay setting. I have it switched on but it's not working."
- `e751c62f-31cb-4375-be52-775959e4b268` enricher usability/complaint/2 vs verifier other/complaint/2: "recent update completely ruined the app and mood"
- `e7756b1b-301a-4047-a99b-f5d20ffc960e` enricher other/complaint/2 vs verifier playback/complaint/2: "Bekar aap h install mt Krna bugs hi bugs h"
- `e775ffe5-2847-4487-8287-9ea282a1a921` enricher billing/unclear/1 vs verifier billing/complaint/2: "Exuberant utill didnt appeal for subscription 😅"
- `e7a18bb0-d85a-4582-b442-492436f65f2a` enricher other/cancellation/2 vs verifier other/cancellation/1: "Delete 😡🤬"
- `e7ec08ad-ba62-475e-8b78-f48f10909433` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "Horrible developments. Last year Wrapped worked just fine, NOW it's giving the fast skipping slide bug of 2021 for me. The Your Top Songs 2022 is filled with songs I never listened to and specifically"
- `e7fa32fd-34ce-4f50-a0c2-7147cb08d1eb` enricher usability/complaint/2 vs verifier usability/cancellation/2: "New UI update is terrible. My Spotify just updated to the new version and I absolutely hate it!! Doesn't feel user friendly at all and takes so much more time to find what I want. Please go back to th"
- `e83e8093-7f55-4fa3-88bc-f1b5d1068d42` enricher other/praise/1 vs verifier catalog/praise/1: "Best music provider out there"
- `e87190a9-b584-4053-81ff-36d58b4e0bec` enricher catalog/request/2 vs verifier catalog/request/1: "Would be good if Spotify suggested similar tracks or tracks I may like based on what I'm watching and play videos. Similar to how YouTube works. I do enjoy Spotify but it could be better."
- `e87f4fef-26ba-4b02-a694-19202bdf0639` enricher catalog/praise/1 vs verifier other/praise/1: "The number of online songs I listen to till now, but no Spotify app can match this app: Really amezing unbelievable..no words about this app.. enjoy"
- `e8954b9d-a72f-46e4-87d6-60d279ef60d2` enricher billing/request/3 vs verifier billing/complaint/3: "It's all premium now , I want to go back"
- `e89cc072-b645-4de5-b556-2f609fa245fd` enricher usability/complaint/3 vs verifier usability/complaint/2: "Can not back to the previous song and when try to back the latest song is play, bad experience."
- `e8d3ccb9-da53-42c3-847a-ab403511040a` enricher other/praise/1 vs verifier catalog/praise/1: "This is the best songs app. Everyone should have this masterpiece"
- `e8d508e7-6209-44cb-a343-861558f33fc3` enricher catalog/complaint/3 vs verifier billing/complaint/3: "I love this app but because of the premium I hate this app the most we can't read lyrics the function is off. About the network my wifi is very High but still it's showing no connection available. The"
- `e90594a6-003e-43c0-a391-5b6502e86b7b` enricher usability/praise/1 vs verifier playback/praise/1: "I love the spotify app a lot and how the lyrics run smoothly No troubles😍😍😍😍"
- `e91b4949-d462-4dd6-bb76-c9b22c2b1053` enricher usability/complaint/2 vs verifier billing/complaint/2: "Loved except ads"
- `e965cbd3-6cca-44de-bd8d-999cd559eb84` enricher playback/request/2 vs verifier downloads/complaint/2: "I love it I just wish you can listen to music without wifi But all tho it's an amazing app"
- `e98f040f-e88b-47db-8225-e0a62a8fa988` enricher usability/request/1 vs verifier other/complaint/2: "Nice selection just wish it had a longer timer"
- `e9a8714a-f248-469a-afb1-186705159f41` enricher other/praise/1 vs verifier other/unclear/1: "for music"
- `ea6bb037-dd27-4d1f-9b98-fafbaf14a5d7` enricher other/praise/1 vs verifier other/unclear/1: "entertainment 100%"
- `ea919bc3-5d9c-4c77-aeac-bd6066d6cee9` enricher usability/complaint/2 vs verifier usability/complaint/3: "We get it spotify you need revenue. But don't play 1 minute 30 seconds worth of ads every time i change the song or after every second song! And why can I play my music in order without premium? Pleas"
- `eabfb530-a075-4742-8853-2f37033a7359` enricher playback/complaint/4 vs verifier playback/praise/2: "The app keeps crashing, unable to play music at all. They have responded promptly and fixed it"
- `eb1f02c5-317e-4aea-b0d4-622cfdbfd9a4` enricher playback/complaint/3 vs verifier playback/cancellation/3: "Nord n10 5g app skips on higher quality devices like my pioneer car stereo will cancel my subscription if it continues."
- `eb4bd3c1-b398-4ad7-b456-5c1f4d4db9e7` enricher usability/request/2 vs verifier usability/request/1: "Wish it would hold screen giving name of song longer and make changing albums/tracks easier."
- `eb7d3f29-6df1-484b-8b3c-dc031ff9404b` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "I have no idea why my Spotify does not show the lyrics. It used to show them but something happened I suppose and now I can't see the lyrics and it's bothering me as I can't read the lyrics and sing a"
- `eb9aeb5c-89bf-4d79-8acd-86f4aec53488` enricher catalog/complaint/3 vs verifier billing/complaint/3: "can't listen to previews anymore"
- `eb9ed6b5-8248-42af-bea4-4179913b277f` enricher usability/cancellation/2 vs verifier usability/cancellation/3: "Worst UI update ever. The last thing I want my music player to be is TikTok. U use TikTok to kill a couple mins of spare time glancing at random vids, who the hell has a moment and thinks "I want to l"
- `ebe17108-1f54-4877-8bd6-d3f6003ba78f` enricher catalog/cancellation/3 vs verifier billing/complaint/3: "Its getting worsen day by day , only adds are there , manytime it happens that , songs are removed from Spotify , and now its irritating. Edit :- worst app ever , now u can't even listen music accordi"
- `ebe594c8-a537-41d7-83a8-44f43ae759dd` enricher catalog/complaint/3 vs verifier usability/complaint/2: "Never updating this piece of junk ever again.I HATE the new search! Instead of instantly finding the song I'm searching for, it suggests results, which u have to click on to get the the real results(s"
- `ec30f513-78ea-4d5d-bc8b-786855ccc35c` enricher other/complaint/2 vs verifier billing/complaint/2: "The more Installs the mor the Spotify is getting worst... Don't even think Spotify premium is coming like this 😕"
- `ec3d2850-4d40-4b27-9d9b-d1e919625c9d` enricher other/complaint/2 vs verifier other/unclear/1: "Get good."
- `ec3f0893-d105-4157-bda1-06b2abd9a017` enricher other/praise/1 vs verifier other/unclear/1: "udh balik kok, lofff uuu😘😻😍💟😠"
- `ec4c2062-9160-4226-b487-15978f8d5ab0` enricher billing/complaint/3 vs verifier usability/cancellation/3: "LET ME JUST PLAY MY MUSIC WHEN I WANT IT, there's no reason why I have to get premium just to repeat a song A BASIC FEATURE ON OTHER APPS it's ridiculous. Not to mention the fact I can't even click on"
- `ec54c992-243f-4132-9e29-c27911a3cd27` enricher other/unclear/1 vs verifier other/complaint/2: "So I'll write my review about your recent update in the language that used to be our love language.. Spotify! “Cause baby, now we got bad blood You know it used to be mad love So take a look what you'"
- `ec640e57-7b0d-4c1f-a82f-85590e0446f6` enricher other/complaint/3 vs verifier playback/complaint/3: "Last update sucks. It was working amagingly, but when i updated it started to show application error.😑😑 i really loved this one.😓"
- `ecc3e249-6569-4d4c-adc3-5092f9873833` enricher billing/complaint/3 vs verifier billing/complaint/2: "Very shameful every system has been changed to ensure to go for premium charges . Now this app became not useful at all"
- `ecee9ed4-a18a-4562-b073-bc820639ba2b` enricher other/complaint/3 vs verifier usability/complaint/2: "New updates are really frustrating. Basic features are removed. Really the worst update ."
- `ecefd0fd-4b82-4040-bfd3-38ff3ce8286b` enricher billing/praise/1 vs verifier other/praise/1: "Spotify is a great deal 🤝🤝🤝"
- `ed1bf93d-e52d-4287-89ce-1d111836d97e` enricher usability/praise/1 vs verifier other/praise/1: "I love this app It's very easy to use and the best for listening of music"
- `ed1ef04f-2eac-4c0d-ae50-8c05762f7400` enricher access/complaint/3 vs verifier playback/complaint/4: "app is not working . Always shows that no internet connection besides of working internet normally"
- `ed2d0600-5b5f-4d49-86dd-41ad285b72d1` enricher billing/cancellation/3 vs verifier usability/cancellation/3: "This app was an amazing app with good quality music, good song choices, great playlist and all. But after the current updation,this app has been ruining my musical experience. There is no place for no"
- `ed41148d-6573-473a-b1d9-a374e492d449` enricher usability/complaint/3 vs verifier usability/complaint/2: "More ads are coming Song to song ads are coming Waste app"
- `ed5c6423-6af3-444c-84cc-5840be9e1d84` enricher other/praise/1 vs verifier playback/praise/1: "Sound Was execlent ♥️"
- `ed64ca6e-7197-4f03-90a5-e545d73d476f` enricher playback/complaint/4 vs verifier playback/complaint/3: "Always crashing and not working right,ose my controls so I can't rewind fast forward or pause"
- `edd4b67a-d874-4d05-bcf3-558f0feb509f` enricher other/unclear/1 vs verifier other/praise/1: "SUPER...."
- `ee6bf52e-dba1-4bbc-9a1e-d63ef62af77a` enricher catalog/praise/1 vs verifier other/praise/1: "i love spotify music and podcasts"
- `ee721a07-0c50-4e93-81e0-c4295d925abc` enricher usability/complaint/2 vs verifier downloads/complaint/2: "Dropping my rating down to 2 stars because the app works, but the most recent update made it harder to switch to offline. I just want to be able to quickly change to offline when I know I won't be nea"
- `ee9a0ac0-e299-42c8-9ee9-90ffbe9b7c9c` enricher catalog/complaint/3 vs verifier catalog/request/2: "Liriknya gk muncul krnaoa yah? kemarin" ada, kok skrng gk ada:(. Tolong dibenerin"
- `eef71ff7-e7a6-4d22-8dab-08ff48475337` enricher other/praise/1 vs verifier other/unclear/1: "Supper se uppar..👍"
- `eeffe125-4c74-42f0-be69-45f615883b5c` enricher other/unclear/1 vs verifier downloads/complaint/4: "This app is offine"
- `ef01b9c4-f3dc-4e13-ae69-ec8409c1b3b6` enricher other/unclear/1 vs verifier other/cancellation/1: "Boyscott sweden"
- `efb39daa-19f2-4184-b3e6-c201b134f8bb` enricher playback/complaint/3 vs verifier playback/complaint/2: "I love Spotify. I use the free version and it still works great. But, it randomally stops playing, and when I press play again it restarts the song again. Very annoying. Nothing I do fixes it."
- `efc297bf-e7b9-4cd6-87fd-4bb85a4647e6` enricher downloads/unclear/1 vs verifier downloads/praise/1: "I no longer download I just Spotify.. thanks to spotify"
- `efcf4169-3676-41a1-81ff-eb90f5d2e8db` enricher other/request/1 vs verifier usability/request/1: "Bhosdwalon thoda chhota add b bna skte ho"
- `f009d84d-d39c-4141-a99f-7f89f96688d2` enricher other/unclear/1 vs verifier other/praise/1: "I love my religion I love my quran"
- `f00c8679-c9ac-4e9b-8cab-b401fc05a1b4` enricher other/unclear/1 vs verifier other/complaint/2: "Amazing awful experience of love music"
- `f0629563-1866-46ce-89ec-d30b457a002d` enricher playback/complaint/4 vs verifier access/complaint/4: "I can't open the app it always offline even if i have a internet connection"
- `f0700501-0b34-48d1-a989-de2d916cf92f` enricher usability/complaint/3 vs verifier usability/cancellation/2: "This app is more concentrating on ADs rather playing a music...even if you here saying listen music without 30 min interruption still after 5 min you will listen a shirt AD... Why should I purchase yo"
- `f0942c46-3290-4815-a17e-16bf979ed378` enricher other/cancellation/2 vs verifier other/cancellation/1: "I'm not using Spotify while it publicly supports hateful speech and behavior of artist by promoting their music no matter who that artist is."
- `f09e7190-ba70-4a82-95f4-b7e4f61dbcd4` enricher other/unclear/1 vs verifier other/cancellation/1: "All Sweden app boycott, useless app"
- `f10e7cd7-023f-49b4-adec-2be901f7d466` enricher other/cancellation/2 vs verifier other/complaint/2: "remove this it is a virus"
- `f15a73f4-6800-4fc4-90e5-e91f7d58dcc5` enricher catalog/praise/1 vs verifier other/praise/1: "Super picks"
- `f17aad6a-b873-4130-ac5d-24d9effea86e` enricher usability/complaint/3 vs verifier usability/complaint/2: "I can't fathom how anyone at Spotify thought it was a good idea to remove the feature that lets you preview songs while creating playlists. Then there's the matter of audio quality which is a level be"
- `f19ad3ae-68a6-483e-bb79-8ed8423bbfb2` enricher access/complaint/4 vs verifier access/request/4: "Hey! Am having problem in logging in with my phone number from past few weeks can you please help me."
- `f1abd13b-2391-4b04-8109-efa7f3cfed0b` enricher playback/complaint/4 vs verifier playback/complaint/3: "Continously pauses songs and podcasts randomly. When in Offline mode, it still requires connection to WiFi or data to start the app and access even downloaded content. Promises "30 minutes ad-free lis"
- `f1b42679-6dd6-4525-963b-14054c6cad24` enricher catalog/praise/1 vs verifier other/praise/1: "Listen to it everyday ..... almost nothing that i van't find!"
- `f1d6e1d3-9241-4e1e-9fbc-0a4619c9a3a5` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "Nightmare of an app! Can someone tell me why it takes 20mins to download just one song! Ice reinstalled it 4 times now and still no improvement"
- `f24bd6d4-6158-4d8b-872a-8b9e1a28711f` enricher usability/praise/1 vs verifier other/praise/1: "No adds works well"
- `f258dcff-1985-4453-a93c-ecadcf355c8c` enricher billing/complaint/2 vs verifier billing/complaint/3: "Too much ads don't tell me about premium that's stupid think about it cause we're using our data to access your app and then we still have to pay premium while you're still making money out the data w"
- `f2c27aee-6cfa-485f-81f0-e5f117ddf69c` enricher catalog/complaint/3 vs verifier catalog/complaint/2: "But for some songs the lyrics are not coming I need the lyrics This app is soo good 💯 but only the lyrics are not coming"
- `f2da86cb-44bc-4419-8f51-65ea9a470ff8` enricher playback/complaint/3 vs verifier playback/praise/1: "Love the musical choices, but doesn't play in the cooler."
- `f2ee4586-9667-40cb-bde0-dcdb0bf63619` enricher usability/complaint/3 vs verifier usability/complaint/2: "It has way to many adds i actually wanna kms because of it"
- `f3023b24-a91a-4814-bfc9-38fc9b2b4718` enricher access/complaint/3 vs verifier billing/cancellation/3: "Sheer is bad!! I shared my student Id issued in 2020 for 3 years degree and it rejected my profile saying it's old or expired. How is it possible it's still valid for 1 year. Pathetic app. Not going t"
- `f3797e3e-1b88-4934-8b81-340ab4bebd17` enricher other/complaint/2 vs verifier other/unclear/1: "you'll end up here, and sticking here anyway - go ahead and save the time and discouragement of trying the competition - there's no comparison"
- `f3bab585-3f13-435a-8f6e-9f5ff3bad434` enricher downloads/praise/1 vs verifier billing/praise/1: "I've used Premium Spotify for over 10 years and love it. I'm able to put together any playlist and have it downloaded and available anytime. Great music selection, I've only found a handful of songs t"
- `f3e5ce5d-6c5f-43fe-9087-a9c73af0a0d3` enricher other/praise/1 vs verifier playback/praise/1: "Very nice and Beautiful to listen.Sound Very clear."
- `f40c22f5-95df-4543-b363-ef6036ffd773` enricher usability/complaint/2 vs verifier usability/request/2: "Re-add feature to like all songs on album. You tried plus a year ago why no love Spotify? New releases screen useless recently. Where's the new albums from this week? Not albums from 10 years ago. Add"
- `f416ced7-23a4-4ac6-9b3f-c02b5593dcbc` enricher billing/complaint/3 vs verifier billing/complaint/2: "Worst app . Forceing to buy premium subscription"
- `f4309366-d0d7-483a-ab44-f44135fe914d` enricher usability/complaint/3 vs verifier usability/complaint/2: "Every disappointed app 😮‍💨. 1 song 2 ads 🥲 and sometimes ads starts while playing music 😅"
- `f43b5e71-50fb-4085-8987-aab7623a6b1d` enricher playback/complaint/3 vs verifier downloads/complaint/3: "Glitches more often than not now. I've downloaded my songs a good 7 times now and still have to every once in a while. The app is okay if you can find what you're looking for and they don't change the"
- `f45f4fb4-01f8-4f46-bed1-9d1c828024a4` enricher billing/complaint/3 vs verifier other/complaint/2: "It's becoming the worst app to listen our fav songs 😡."
- `f4723684-de07-4592-a62f-fdad162630ff` enricher usability/complaint/3 vs verifier usability/complaint/2: "This has all the music I like but like the amount of adds tho and I can't skip like for what bc it's playing songs that aren't on my Playlist and I can't switch back I'm not wasting my money just to f"
- `f478b1fa-a972-4695-8538-1ca9caa78d19` enricher playback/praise/1 vs verifier usability/praise/2: "I overall love the app but when i play a song somthong else plays but its amazing i reccomnd the app it might have some misshaps but trust me this app is way better than any other music app😄😄😄😄😄😄😄😄😄😄😄"
- `f4790cda-8662-46fb-b634-2895684692b9` enricher other/complaint/2 vs verifier other/unclear/1: "🤮🤮🤧🤮🤧"
- `f479aec5-8c65-43fb-ae88-dd4bfd98c451` enricher usability/complaint/3 vs verifier usability/complaint/2: "Free version; went from same ad over and over to multiples ads after almost every song. May just listen to the radio. At least I'll hear local/relevant ads rather than the generic ones"
- `f493a939-0367-4647-8b48-21b744eb81ef` enricher catalog/cancellation/2 vs verifier usability/cancellation/2: "I paid for Premium to get rid of ads and to stop Spotify from "adding songs you may like." So here I am, 3 months into premium and Spotify is STILL adding songs to my playlists! This is absolutely mad"
- `f4de03dd-a7a6-419e-94df-8ccd9c4fb7d8` enricher playback/complaint/3 vs verifier other/complaint/2: "It is not working properly"
- `f4e120d3-77bb-4404-a9f6-28e493410df9` enricher other/complaint/2 vs verifier other/cancellation/2: "Worst update ever!!! I'll better buy youtube music premium rather than this garbage👎"
- `f5027e10-a188-447f-9eb7-6e35fb30be4c` enricher catalog/praise/1 vs verifier other/praise/1: "All song one palytfrom nice service I injuy morning to night।"
- `f5396679-5633-449f-ab37-ad31a877fa91` enricher catalog/praise/1 vs verifier catalog/complaint/2: "I loved there songs but it doesn't have every song still missing some but still I like it 🌺💞💐"
- `f53e03a2-8e9b-4b0e-90ae-7c83c4103a83` enricher other/complaint/3 vs verifier playback/complaint/3: "Not working in my s21 fe by last 4 months"
- `f5526555-4441-427f-a359-79301e6d5a97` enricher billing/complaint/3 vs verifier usability/complaint/2: "Before it was very better but now it is so bad because there premium we can't listen one song again we can also not listen one song repeated it is now very bad"
- `f555a72f-c9bf-46fe-b791-c05c5d30a793` enricher usability/praise/1 vs verifier usability/praise/2: "Okay. I love this app. Much better than Musi!! U guys just dont know how to use this app, ads aren't much of a problem. If u dont know why spotify ads songs for u in ur playlist, you have to add at le"
- `f56832d4-ddc6-4619-baa8-570cb7519ccc` enricher usability/praise/1 vs verifier other/praise/1: "It's an amazing app, super easy to use I love it❤️"
- `f5ac0fe7-eeeb-47b9-aba8-fb85fde34cae` enricher other/praise/1 vs verifier playback/praise/1: "Works easily, good sound quality, reasonable cost."
- `f5b1e3c7-2346-4013-a466-c075781efdb6` enricher billing/complaint/3 vs verifier billing/complaint/2: "why are you making common features premium? using this app for songs is very irritating now just because you want premium for every small features."
- `f5bfa35a-e9b6-421d-9e28-4debb61c15df` enricher playback/complaint/3 vs verifier usability/complaint/3: "The latest update make it worse as I cannot even play the song that I like and it keep preventing me from skipping. When I tried to continue from the song I stop it went on to the next song instead of"
- `f6205cb1-d22e-4158-ad06-cdd0dde60957` enricher playback/complaint/3 vs verifier usability/complaint/3: "Notification podcast buttons work backwards, Android auto only works every other day. Service is alright, Android app is bad."
- `f67f6aad-fc1b-4b45-88d5-6006c5f75898` enricher usability/complaint/2 vs verifier catalog/complaint/2: "It's really good but 'you have filters on which may set results to hide' I've tried different ways to get rid of if but it doesn't go before it happened again on my first account then I looked for how"
- `f6a0d928-fe7c-44ea-a69f-69d6dc2f5fcb` enricher billing/complaint/2 vs verifier other/complaint/2: "Money hungry cash grab trash"
- `f6a8723b-00b6-4b22-8b51-ca47b6d4da10` enricher usability/cancellation/4 vs verifier usability/complaint/3: "I use Spotify for years but after this update i can't even make a playlist or turn off shuffle i use another app to play music now Am gonna be honest this UPDATE SUCKS it only shows perium and paid st"
- `f6aa856b-2957-47ca-a9f0-d07b07ce4959` enricher usability/complaint/3 vs verifier usability/complaint/2: "This app is stressing me out keeps putting songs into my playlist and i don't know how to stop the song from playing its really annoying and since im new to the app its just way to hard"
- `f6b9ccca-af8b-46a3-b3f5-8237ad780cdc` enricher usability/complaint/2 vs verifier access/praise/2: "I personally enjoy using spotify it's really easy and I get tons of recommendations I do have to say for a few months I had a problem I don't know if it's common though II couldn't look or play my lik"
- `f6c3f99b-75b1-408f-820f-17f5a81a2306` enricher usability/complaint/3 vs verifier usability/complaint/2: "Good app for advertisement ,not Good for hearing songs"
- `f6e25150-6569-4f06-9097-ce4409b4a0d0` enricher playback/complaint/3 vs verifier usability/cancellation/3: "What's happening to Spotify? I'm playing an album, I have to pause it for a minute. I go back to the app & it just jumps & plays something (random) else? Never had this issue. Currently a premium fami"
- `f6e5bc23-69c8-4323-a092-dd36e164c206` enricher usability/complaint/2 vs verifier usability/cancellation/2: "Very selfish app. Too many ads so the Spotify corp can earn money and it waste our time . Never install this app. It always beg you to switch to premium. God will never forgive to this greedy app."
- `f6edebf0-5344-4fcc-920b-03e58c812bb3` enricher catalog/praise/1 vs verifier other/praise/1: "It's easy and simple entertainment app. It provides all kind of music.try it my fallowers"
- `f6f3d585-cd68-43c9-a2ea-20579a22c3e6` enricher billing/complaint/3 vs verifier billing/complaint/2: "To all the Indians, use jiotunes, it's much better than this, and also Spotify is charging you for seeking the music (dragging forward or backward)."
- `f73dbd2b-5cdb-4b60-9100-073b705aa437` enricher other/complaint/2 vs verifier other/complaint/1: "Why U Do That Spotify!?"
- `f7700ca0-81c2-40b3-85b6-7de2685fa3a3` enricher catalog/request/2 vs verifier playback/complaint/3: "SPOTIFY LOAD THE LYRICS"
- `f77a2fc7-4170-44c7-8744-fa1fcd296d03` enricher billing/complaint/2 vs verifier usability/complaint/2: "Good but it is bad that u only get 6 skips a hour"
- `f7bf76d5-c91d-4670-b04b-deede65f0646` enricher usability/request/2 vs verifier usability/complaint/2: "I've got the premium and it's almost perfect. The thing that I don't like the most is that every song added to the queue disappears after being played once. It's frustrating, you can at least give the"
- `f80122a8-b5ce-4b5e-9c7d-1924efdc7b8e` enricher usability/complaint/3 vs verifier usability/complaint/2: "Not a great user experience. Video ads during podcasts...huge thumbs down. "Smart shuffle" aka enhanced playlists will ruin your listening experience."
- `f80a55e5-3551-49f8-80ce-77bd2ecc2c4a` enricher catalog/complaint/4 vs verifier catalog/complaint/3: "Spotify was a nice app,now I can't listen to any song and make new accounts all the time for example I want to put a katy Parry song and it gives me another song,pls fix it and also I can't listen to "
- `f80cbbfd-98bb-4f8a-b8b3-8aecf0a75f3e` enricher billing/cancellation/3 vs verifier usability/cancellation/2: "I don't usually post reviews but now I couldn't stop myseIf from doing. If there was an option to rate 0 I would've done that..Very frustrating..no unlimited skips,can't seek,no repeat, unlimited ads."
- `f83eccef-d5fb-4673-8a71-bd31f66bbbe7` enricher usability/complaint/3 vs verifier usability/complaint/2: "Just the worse the amount of adds is getting annoying day by day"
- `f85b32c7-1962-47d9-8c63-5e50a0fbe697` enricher usability/request/2 vs verifier usability/request/1: "Reduce advertisement"
- `f8d0c5d7-77b7-4fbf-8702-8b8af049f950` enricher catalog/complaint/2 vs verifier other/complaint/2: "I didn't get my 2022 wrapped so 1 star"
- `f8e7ee9b-bf22-4524-b245-65dc2b11abb2` enricher other/complaint/2 vs verifier other/complaint/1: "I hate this app and sawedan I love islam 🕋"
- `f9054b47-033f-4f4d-b46a-a2af828825a6` enricher other/praise/1 vs verifier billing/praise/1: "I fully recommend this app is the best app that I've ever use Spotify as Mum I don't really think that YouTube music is that and go check out on Spotify Spotify music or man it's the best it gives you"
- `f96006b0-6797-413e-a0a3-151b9bbdf407` enricher catalog/complaint/2 vs verifier usability/complaint/3: "Forced recommended songs in my personal playlists. I have shuffle and their dumb "special shuffle" off but at the end it still plays random music not even similar to my playlists vibe. Dumb"
- `f9757f01-0b93-41bb-a1ad-cc3f0a7daa46` enricher usability/complaint/2 vs verifier usability/request/3: "I don't like what you all did with the playlist. I want to see what I have on there, or if I want to listen to one song in particular, I can't on that playlist. If you could revert this change, I will"
- `f9f1df97-f767-4b96-a0ac-81b09fdf62df` enricher other/unclear/1 vs verifier other/praise/1: "Honestly, Lit."
- `fa3d055e-e762-4ea0-9764-644aa764f840` enricher billing/complaint/3 vs verifier usability/cancellation/3: "At last it is showing its true colours . I can't even skip to my favourite part. Ads are negligible but can't turn off auto shuffle and can't go to previous song . This is too much and I'm going to un"
- `fad6471c-9149-4252-a259-403ebb6fee6b` enricher usability/complaint/2 vs verifier usability/praise/1: "If you like music like me you should download Spotify I always love Spotify but they always have an adds :( I like it anyways"
- `faec75fe-47f8-4c7a-8892-afe6b7bb0984` enricher usability/cancellation/3 vs verifier billing/cancellation/4: "Firstly, i want to say that it has got too many adds. Nearly after 2 songs ,an ad comes . Purchasing premium is not always affordable for me . It is not able to play some songs that are available on i"
- `fb29f4da-3dff-48d8-bf43-be24dfe3caad` enricher other/complaint/2 vs verifier playback/complaint/2: "Great quality sound. Many problems with app."
- `fb7acdcb-b63d-4bf8-8786-8a1db78e156a` enricher other/unclear/1 vs verifier other/praise/1: "Hmmm.... MUSIC"
- `fb8717d6-39e5-4266-988d-52c9f3c467e9` enricher playback/complaint/3 vs verifier playback/cancellation/3: "Videos don't play only audio on podcast when connected to radio....if they drop rogan I'm out....only reason I got spotify was rogan"
- `fba94e9b-973e-4696-b352-1d5b2fd6196d` enricher catalog/complaint/4 vs verifier catalog/cancellation/3: "I really loved this app for so long.But lately this appo became just waste of time and data.I am not able to search songs.What they shows in title is not the song what is played.Can't skip the songs a"
- `fbbb1ca4-9a54-43b6-abe0-0da83ab5e7fa` enricher billing/complaint/2 vs verifier usability/complaint/2: "You want money by disabling shuffle but this would result in the opposite and you'll lose even ad revenue since ppl will simply delete and use another alternative app I wonder who tf comes up with suc"
- `fbdd899f-8fe5-4c37-978a-fe00886ae23c` enricher other/request/1 vs verifier usability/request/1: "Where the option to clear the history"
- `fc0c79c5-04cc-4c46-920f-a8282608006a` enricher playback/complaint/4 vs verifier playback/complaint/3: "Same issue everyone else has had throughout the years. Songs quit playing after 9 seconds. All app and device settings are optimal and uninstall - reinstall of app didn't work"
- `fc2b5d6b-3aba-4928-bc1c-0585ff44f34f` enricher usability/complaint/2 vs verifier usability/praise/1: "Epic app, not a fan of the ads tho"
- `fc3b14e3-0e2e-4146-9871-0fc88b14dad5` enricher catalog/praise/1 vs verifier other/praise/1: "I love the music 🎶💖"
- `fc4d65d1-e93c-4f99-b011-f52091284557` enricher usability/praise/1 vs verifier other/praise/1: "I love Spotify. easy to use, awesome song collection, My playlists across all my devices."
- `fc567fb3-9ee1-41bc-9c83-ff2d6db25480` enricher usability/request/2 vs verifier usability/complaint/2: "I hate the new update. Liking an album should automatically add all it's songs to my liked songs instead of making me go through and like each song individually"
- `fc84b14d-9cda-45d9-b9ab-ce1993e7b087` enricher catalog/praise/1 vs verifier other/praise/1: "Spotify is my fave app when it comes to listening music! I love their every update and their suggested playlist for me. Keep it up!"
- `fc9ab108-eb91-4edb-ab6f-9a12c55ed766` enricher downloads/complaint/4 vs verifier downloads/complaint/3: "i've been reading reviews and others also have a problem with the music not playing when it's not in your playlist. i tried downloading songs but it won't work. it takes too long and it's weird becaus"
- `fcb06c1e-8d05-43ec-8150-1edb71b1731f` enricher usability/cancellation/3 vs verifier usability/cancellation/2: "Removing the queue feature is the worst thing you could have done. Uninstalling right now."
- `fcc61b1d-7afd-48e3-9451-24456dea54e1` enricher downloads/complaint/2 vs verifier billing/complaint/2: "It's pretty great, don't get me wrong. But the thing that had been irritating me is how we need to be a premium to download playlists. I don't mind the other things that only premium account can do, b"
- `fcd209ee-6f0b-4e45-b865-bc9d75f7b127` enricher catalog/cancellation/2 vs verifier catalog/cancellation/3: ""Dammi Falastini" song was removed from Spotify and labeled as anti semitic. This is a pro-palestine song supporting a nation that continue to be massacred for years, and the lyrics contain nothing an"
- `fcdb2c55-da48-4414-b458-7c60c4e8a4ec` enricher playback/praise/1 vs verifier other/praise/1: "Awesome quality..."
- `fd10e27a-35b1-4359-9dd4-4b9ab66db9f9` enricher other/cancellation/2 vs verifier usability/cancellation/2: "I hate the new update with them adding songs to your own playlist and honestly I used to love spotify but now its a big no to liking it!I'm going to Uninstall it. Okay I Uninstalled it!"
- `fd3004cb-90b6-43fc-8d90-229af72de58a` enricher playback/complaint/3 vs verifier usability/complaint/3: "I've subscribed to Spotify for YEARS. Great app, love my music, etc etc. Recently, however, this app has gained a mind of its own. It will turn off the shuffle and play recommended songs even if I jus"
- `fd9789e9-4f54-4c0f-830a-fca0f5d87f5e` enricher billing/complaint/3 vs verifier billing/complaint/2: "Done such a cheap thing Every action needs premium such a cheap way Spotify"
- `fd9b0f82-bcee-46d6-9288-06c93d3f5040` enricher usability/complaint/3 vs verifier usability/complaint/2: "I love this app but every time there is ad why and once I think to take spotify premium but then there are so many ad i will not take premium please solve this problem every one song there is ad..."
- `fdfa793b-c471-4d33-9c4e-1cf79c102c8c` enricher usability/complaint/3 vs verifier usability/complaint/2: "Great app for listening music, wish it had all my fav songs, but its still good, but it keeps playing my songs with shuffle, and pissing me off so please just remove that option completely it's annoyi"
- `fe883ac9-15f2-4730-ac1f-072be351b763` enricher billing/request/2 vs verifier usability/request/1: "Wonderful, I wish the they could extend the skips to 10 at least and the ads maybe play 2 ads in an hour"
- `fedfc3ea-4194-40e4-9661-c9b09fde8920` enricher billing/complaint/3 vs verifier usability/complaint/3: "The new updates are so stupid... You can't skip to a particular part of the song and u can only skip songs for few times...yes exactly ab apni psnd ka gana bhi nhi sun skte"
- `fee59173-851b-47f4-bc10-d78b4172aedf` enricher catalog/complaint/2 vs verifier usability/complaint/3: "Theres no canvas option for me on this app and ive uninstalled reinstalled... cleared cache... prayed to the gods.... Please help and a friend of mine has canvas. Please resolve this as I'm a premium "
- `feeaea74-bf38-4863-87f6-307d90e0b2e8` enricher other/complaint/3 vs verifier other/complaint/2: "Worst app in the playstore. App is not working properly"
- `ff36edeb-09ba-4fcf-988e-80bb3e3dcf9d` enricher usability/complaint/3 vs verifier usability/complaint/2: "I pay for this why do I have to listen to so many bloody adds!?"
- `ff52246d-bc22-4db2-ab4f-1cf8f5f32b4a` enricher playback/complaint/3 vs verifier usability/complaint/2: "I'd like to say I like. I do when it works but it keeps swapping devices randomly and without me agreeing. Doesn't matter if I'm on WiFi or data amd it connects to devices I've never even seen"
- `ff9ab816-9d98-4e47-add7-bbd80d9e2c37` enricher usability/complaint/4 vs verifier usability/complaint/3: "Hi spotify since last 1 month I can listen my favorite music and skip every single song very easily now a days after last update spotify I can't skip any song I can't select any song this is terrible "
- `fffc8389-5d62-4f7b-853f-ef366ecd17ec` enricher other/complaint/3 vs verifier usability/complaint/3: "New links don't work. Since the new short link it does not work on my android phone when people share with me"
