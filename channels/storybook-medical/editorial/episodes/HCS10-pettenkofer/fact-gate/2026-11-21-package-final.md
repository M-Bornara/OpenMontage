# Fact gate, HCS10 package, FINAL (round 3, 2026-11-21): 41 PASS, 0 STRONGER THAN CLAIM, 0 NO CLAIM

Independent `fact-gate` sub-agent, input = claims.csv + fact-gate/package.md only. Rounds: r1 (12 flags, see
2026-11-21-package-r1.md), r2 (0 flags + 2 optional clarity notes, applied), r3 (0 flags).

| # | field | sentence | claim ID(s) | verdict |
|---|---|---|---|---|
| 1 | youtube.title | The Professor Who Drank Cholera at 73 | C46 C01 C02 | PASS (r1: title 1 stated a motive) |
| 2 | description | Munich, 7 October 1892. | C01 | PASS |
| 3 | description | Max von Pettenkofer, 73, drank a fresh culture of cholera germs in front of witnesses. | C01 C02 C08 C09 | PASS |
| 4 | description | That year, cholera killed about 8,600 people in Hamburg. | C06 | PASS (r1: "had just killed") |
| 5 | description | Robert Koch blamed a germ carried in the drinking water. | C05 | PASS |
| 6 | description | Pettenkofer believed the germ alone was not enough: the soil and the ground water had to be right too. | C04 | PASS |
| 7 | description | Some of his students offered to take the risk in place of their old teacher. | C18 | PASS |
| 8 | description | He refused. | C18 | PASS |
| 9 | description | First he drank a little bicarbonate of soda, to neutralise his stomach acid. | C12 | PASS |
| 10 | description | Then one cubic centimetre of a broth culture made in Munich from Georg Gaffky's cultures of the Hamburg outbreak (Gaffky was Koch's former assistant). | C14 C09 C10 | PASS (r2 note: Gaffky didn't make the broth) |
| 11 | description | He wrote that it tasted like the purest water. | C17 | PASS |
| 12 | description | Two days later came stomach cramps and diarrhoea, for about a week, and the lab found his gut swarming with cholera germs. | C19 C20 | PASS |
| 13 | description | But he took no medicine, felt otherwise well, and declared victory. | C19 C25 | PASS (r1: "never turned dangerous") |
| 14 | description | His critics said he had simply had a mild case of cholera, and most experts now think so too. | C26 C30 | PASS |
| 15 | description | Ten days after him, his pupil Rudolf Emmerich repeated the drink and got much sicker, but survived. | C22 | PASS |
| 16 | description | And the irony: modern studies show that neutralising stomach acid makes cholera far easier to catch. | C33 | PASS |
| 17 | description | The soda made his experiment more dangerous, not less. | C33 | PASS |
| 18 | description | He lost the argument about the water. | C36 | PASS |
| 19 | description | But his clean-water and sewer work did help Munich. | C36 | PASS |
| 20 | description | This is a history story, not medical advice. | NF | PASS |
| 21 | description | Never try anything like this. | NF | PASS |
| 22 | description | Another man who drank a culture of bacteria to test his own theory: "The Doctor Who Drank Bacteria" (linked above). | C45 | PASS (r1: "another doctor ... his own germs") |
| 23 | pinned comment | Who was braver: Pettenkofer or Marshall? 🧪 (Did you spot Matt's glasses? 👓) | NF | PASS |
| 24 | hook_card | He drank *cholera*. / On purpose. | C01 C12 C18 C28 | PASS (r1: tag C01 alone) |
| 25 | tiktok | A 73-year-old professor drank cholera on purpose. | C01 C02 C46 C12 C18 C28 | PASS |
| 26 | tiktok | Munich, 1892. | C01 | PASS |
| 27 | tiktok | His rival blamed a germ in the water. | C05 | PASS (r1: "He wanted to prove his rival wrong.") |
| 28 | tiktok | He said the germ alone wasn't enough. | C04 | PASS |
| 29 | tiktok | Two days later, the cramps began. | C19 | PASS |
| 31 | instagram | 1892: a 73-year-old professor drank cholera in front of witnesses. | C01 C02 C46 C08 | PASS (r1: "to win an argument") |
| 32 | instagram | Max von Pettenkofer said the germ alone wasn't enough. | C04 | PASS |
| 33 | instagram | He survived the bet… but not the argument. | C19 C22 C26 C36 | PASS |
| 34 | instagram | (Source: British Medical Journal, 1892.) | C37 | PASS (advisory: the BMJ gives his age as 74; the caption says 73 per C02) |
| 36 | facebook | In 1892 a Munich professor, Max von Pettenkofer, 73, drank a culture of cholera germs in front of witnesses. | C01 C02 C46 C08 | PASS (r1: "famous") |
| 37 | facebook | That year, cholera killed about 8,600 people in Hamburg, and his rival Robert Koch blamed a germ in the water. | C06 C05 | PASS |
| 38 | facebook | Pettenkofer believed the germ alone wasn't enough. | C04 | PASS (r1: "was sure") |
| 39 | facebook | He was sick for about a week, and survived. | C19 C22 | PASS (r1: "for a week ... declared victory") |
| 40 | facebook | His critics said: that was cholera, just a mild case. | C26 | PASS |
| 30, 35, 41 | first comments ×3 | the challenge (as 23) | NF | PASS |

Gate advisories (all PASS): C18 is ATTRIBUTED but its notes approve the unattributed "His students offered ... He
refused"; "On purpose" rests on C12 (VERIFIED) + C18, C28 is extra.
