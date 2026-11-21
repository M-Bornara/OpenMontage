# Fact gate, HC002-S1 package, FINAL (round 3, 2026-11-21): 40 PASS, 0 STRONGER THAN CLAIM, 0 NO CLAIM

Independent `fact-gate` sub-agent, input = claims.csv + fact-gate/package-s1.md only. Rounds: r1 (3 flags), r2 (2 flags).

| # | field | sentence | claim ID(s) | verdict |
|---|---|---|---|---|
| 1 | youtube.title | He Took an Iron Bar Through the Skull… and Spoke | C04 C05 | PASS |
| 2 | description | Near Cavendish, Vermont, 13 September 1848. | C01 | PASS |
| 3 | description | Phineas Gage, 25, was a railroad construction foreman, and his employers thought him the most efficient and capable foreman they had. | C01 C18 | PASS |
| 4 | description | His job: pack blasting powder into holes in the rock with a smooth iron tamping bar, 3 ft 7 in long and 13¼ lb (1.1 m, 6 kg). | C23 C02 | PASS |
| 5 | description | His men caught his attention, he looked over his shoulder, and the iron struck a spark on the rock. | C03 | PASS |
| 6 | description | The powder exploded. | C03 | PASS |
| 7 | description | The bar went in under his left cheekbone, passed behind his left eye and came out through the top of his head. | C04 | PASS |
| 8 | description | It landed about 80 feet (24 m) away. | C04 | PASS (r1: was 25 m) |
| 9 | description | Within minutes he spoke. | C05 | PASS |
| 10 | description | He rode to his hotel sitting up in an ox cart, and Dr Williams later remembered his greeting: "Doctor, here is business enough for you." | C05 C06 | PASS (r1: "Edward" dropped) |
| 11 | description | He survived, and he kept the iron. | C32 C07 | PASS |
| 12 | description | But his friends said he was "no longer Gage". | C08 | PASS |
| 13 | description | What that really meant is a longer story. | NF | PASS |
| 14 | description | This is a history story, not medical advice. | NF | PASS |
| 15 | description | More true medical stories: "The Man With a Window Into His Stomach" (linked above). | NF | PASS |
| 16–18 | pinned comment | "No longer Gage." / What do you think changed in him? / Your guess 👇 (And did you spot Matt's glasses? 👓) | C08 / NF / NF | PASS |
| 19 | hook_card | An iron bar / through his *skull*. | C04 | PASS |
| 20 | tiktok | Phineas Gage, 1848: a 13¼-pound iron bar went through his head. | C01 C02 C04 | PASS (r2: was 13-pound) |
| 21 | tiktok | Minutes later, he spoke. | C05 | PASS |
| 22 | tiktok | His friends said he was "no longer Gage." | C08 | PASS |
| 26 | instagram | 1848, Vermont: a 13¼-pound iron bar went through Phineas Gage's head. | C01 C02 C04 | PASS (r2: was 13-pound) |
| 27 | instagram | Minutes later, he spoke. | C05 | PASS |
| 28 | instagram | He rode to his hotel sitting up in an ox cart, and he kept the iron. | C05 C07 | PASS |
| 29 | instagram | Source: Dr John Harlow's 1868 report. | C30 | PASS |
| 33 | facebook | In 1848, a blast on a Vermont railroad sent an iron bar through a foreman's head. | C01 C03 C04 | PASS |
| 34 | facebook | Minutes later, he was talking. | C05 | PASS |
| 35 | facebook | Phineas Gage rode to his hotel sitting up in an ox cart, and Dr Williams later remembered his greeting: "Doctor, here is business enough for you." | C05 C06 | PASS (r1: attribution added) |
| 36 | facebook | He survived and kept the iron. | C32 C07 | PASS |
| 37 | facebook | But his friends said he was "no longer Gage." | C08 | PASS |
| 23–25, 30–32, 38–40 | first comments ×3 | the challenge (as 16–18) | C08 / NF / NF | PASS |

Gate notes: C23 is tier C with "CHECK Harlow p.4 wording" still in its notes (VERIFIED, so it passes). Not gated (on-screen
text in the render): shot 7 stamp "≈ 80 ft (25 m)" (edit_hc002s1.py) has the r1 rounding; needs a free re-render to fix.
