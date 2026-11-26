# HC003-S1 · on-screen text (storyboard v1) · fact gate 2026-11-21 · 7 PASS

| # | field | text | claim ID(s) | verdict |
|---|---|---|---|---|
| 1 | hook card | She couldn't stop dancing. | C03 C16 C21 | PASS (accepted wording) |
| 2 | name tag | Frau Troffea · Strasbourg, July 1518 | C01 C02 | PASS |
| 3 | stamp, shot 5 | DAY 2 | C16 | PASS |
| 4 | stamp, shot 7 | DAY 3 | C17 | PASS |
| 5 | stamp, shot 9 | 30+ | C04 | PASS |
| 6 | stamp, shot 10 | TO SAVERNE | C18 | PASS |
| 7 | counter, shot 13 | 400* + "*one chronicle" | C19 (C05) | PASS |

Conditions from the gate (keep at the edit): the name tag and "30+" show ATTRIBUTED facts without attribution on screen;
they pass because narration line 3 ("the chronicles say") comes before them, so that line must not move after shot 9.
The "*one chronicle" footnote must stay readable on the 400 counter (C05 is DISPUTED). At the build these texts go
through onscreen_text.py (fact-gate/onscreen-tags.json) as for every Short.
