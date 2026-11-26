# Hook cards v2.1: proposals (2026-11-17) · change C006 v2.1

**Status (2026-11-17, end of day):** all six cards APPROVED; Onesimus = card A "a **GRENADE** through / the window.
Why?" (the user's pick). Change after the first preview (user): the whole card is on screen on frame 0, no word
pop-in; the amber word brightens over 0–0.4 s. **Golden eye:** rendered, text check 0 collisions, copied to
deliverables/short.mp4 (44.7 s); "in Iran" re-cut with no gap (the user heard a hole at the first join).
**Onesimus, Snow, Semmelweis, Finlay, al-Razi:** 4 s preview + sheet in projects/<id>/review/hook/, approved 2026-11-17 (Onesimus framing kept for the window) -> full renders.

| Short | Collapse | Captions from | Frame 1 as built |
|---|---|---|---|
| Golden eye | 2.01 s (held to "was") | "was buried with a golden eye" | s1 (as before) |
| Onesimus | 2.50 s (no pause in the line) | "Boston." (from 2.5 s: a word still spoken after the card is captioned from then), then "The idea…" | s6b CU 1.15→1.42, ember + smoke, fire sound |
| Snow | 2.50 s | "a deadly outbreak…" | s7b CU 1.45→1.65 on the widow drinking, glint on the glass, glass clink; captions TOP. The cut-off hand on the jug (left edge) stays: removing it needs a 219 px pan, the zoom allows 119 |
| Semmelweis | 2.27 s (held to "doctors") | "doctors to wash their hands" | s1a, zoom 1.22→1.28 (1.10 showed a black band) |
| Finlay | 2.35 s (the pause) | "then spent 19 years…" | s1c, push-in starts at frame 0 and lands on "yellow fever"; lamp flicker + dust |
| al-Razi | 2.47 s (held to "refused") | "refused to treat…" | s5a MS 1.18→1.30, curtain ripple, lamp flicker, cloth rustle; s1a from "refused" |

Timing rule (packaging_v2.hook_until): the spoken hook's end if ≤ 2.5 s; else the last pause (≥ 0.1 s) between
1.8 and 2.5 s; else 2.5 s. An episode can pin it to a word (`until` in edit_<ep>.py).

Rules (packaging-v2-spec.md §1, v2.1): 4–8 words · max 2 lines · 1 amber word · no spoiler · every word in the
claims log (research.md "Facts") · nothing OVERSTATEMENT/DISPUTED stated as fact · box ≤ 15% of 1920 = 288 px.
Card: complete on frame 0 (amber word brightens 0–0.4 s), holds to the end of the spoken hook (max 2.5 s), collapse into the CASE chip.

**Fit check.** Two lines in the 751 px inner width allow ~15 characters per line at 72 px, ~17 at 65 px.
Two lines at 65–73 px make a box of 190–210 px (10–11% of the height), under the 15% cap. The spec's example
("About 500 dead in 10 days. / One doctor blames this pump.", 11 words) breaks its own 8-word rule. The Snow options
below replace it.

**Collapse time.** Every spoken hook is longer than 2.5 s (3.6–6.4 s), so each card collapses partway through
the sentence, on a word boundary. Captions start with the next word.

## Summary (in posting order)

| # | Short (posts) | Card pick (amber word in CAPS) | Frame 1 (reused, no new image) | Card position · covers the action? | Continuity (first 3 shots) |
|---|---|---|---|---|---|
| 07 | Golden eye (Sat Nov 21; ready-by **today**) | she wore **GOLD** / in her eye socket | s1: the brush sweeping dust off the eye (as now) | top, y 360–551 · no (the eye sits at ~y 940) | OK |
| 08 | Onesimus (Mon Nov 23) | a **GRENADE** for / a smallpox idea | **change:** s6b, tighter: the grenade on the floor among the glass, fuse burning | top, y 360–566 · no (the fuse is at ~y 745; the card covers the window) | v2.0 opened on s7, which comes back at the same size at ~30 s: fixed |
| 09 | Snow (Wed Nov 25) | 500+ dead. / was it the **WATER**? | **change:** s7b, tighter: the widow drinking Broad Street water | bottom, y 1057–1248 · no (her face and glass are in the upper half) | **v2.0 bug:** handle off in shot 1, on in shot 2; s8 back to its beat only |
| 10 | Semmelweis (Fri Nov 27) | doctors' **HANDS** / killing mothers? | s1a: him washing while the doctors glare (as now) | bottom, y 1048–1248 · no (the hands are at ~y 880) | OK |
| 11 | Finlay (Thu Dec 3) | a tiny suspect. / **19** years of doubt. | s1c: the mosquito on the arm by the lamp (as now) | top, y 360–542 · no (the mosquito is at ~y 1150–1400) | OK; frame 1 has no motion yet (the planned mosquito layer is the fix) |
| 12 | al-Razi (Mon Dec 7) | one group bled. / one left **ALONE**. | **change:** s5a, tighter: al-Razi drawing the curtain that splits the ward | top, y 360–570 · no (his head and hand are at ~y 900–1000) | OK; s1a (the ward conversation) moves to shot 2 |

---

## 07 · Golden eye (HCS04)
Spoken hook: "5,000 years ago, a woman in Iran was buried with a golden eye." (ends 4.35 s). The card collapses
at 2.5 s, and captions start on "was buried…".
**Ending (don't give it):** eye or eyepatch? DISPUTED. So the card never calls it "an eye".

| | Card (line 1 / line 2) | Words | Longest line | Claims |
|---|---|---|---|---|
| A ★ | SHE WORE **GOLD** / IN HER EYE SOCKET | 7 | 17 ch (~65 px) | gold layer VERIFIED (S2); left eye socket VERIFIED (S3); worn for years VERIFIED (S1) |
| B | 5,000 YEARS AGO / SHE WORE **GOLD** | 6 | 15 ch (~72 px) | c. 2900–2800 BC ≈ 4,900 yrs (the approved script rounds to 5,000); worn VERIFIED |
| C | WORN FOR **YEARS** / IN HER EYE SOCKET | 7 | 17 ch | imprint = worn a long time VERIFIED (S1); socket VERIFIED |

**Pick A:** it states the strange fact (gold, in a living woman's eye socket) and gives no answer. "Golden eye"
takes one side of the dispute, and A avoids it. Over the brush shot the viewer sees a gold eye-like thing and
asks the question themselves.
**Frame 1:** s1 as now (a fast camera start, sand dust off the brush, a glint). The eye is at screen y ≈ 940, and
the card ends at y ≈ 551.
**Continuity:** s1 (2006 dig) → s2a (the city, 2900 BC, "The Burnt City") → s2b (the burial at night). The
narration names the time jump, so there's no problem.

## 08 · Onesimus (HCS06)
Spoken hook: "In 1721, smallpox hit Boston. The idea that saved lives came from a man who wasn't free." (ends
6.43 s). The card collapses at 2.5 s, and captions start on "The idea…" (3.31 s).
**Ending (don't give it):** "for centuries, almost nobody said his name".

| | Card | Words | Longest line | Claims |
|---|---|---|---|---|
| A ★ | A **GRENADE** FOR / A SMALLPOX IDEA | 6 | 15 ch (~72 px) | grenade through Mather's window VERIFIED (diary); the note ties it to inoculation VERIFIED |
| B | IT SAVED LIVES. / HE WASN'T **FREE**. | 6 | 15 ch | the approved hook line; Onesimus enslaved VERIFIED (S2, S3) |
| C | BEAT SMALLPOX / WITH A **CUT**? | 5 | 13 ch (~84 px) | West African inoculation: a cut + matter VERIFIED (P2 via S1, S2); frame would be s3b |

**Pick A:** "why would anyone throw a grenade over a medical idea?" is the strongest open question. It is true
and gives nothing away. Note: the grenade hit **Mather's** house, so the card says nothing about Onesimus that
could read as "they bombed him". B is the premise, but it is softer and its image (the man at the window) is static.
**Frame 1, a change:** s6b (the grenade among broken glass), framed tighter on the ball. Spark + smoke on the fuse
(the fx built for v2.0), fire sound. v2.0 used s7 (the note on the ball). s7 comes back at its own beat (~30 s)
at the same size, which repeats the image (L28). s6b at a closer size than its later full shot is not a repeat.
**Continuity:** s6b-CU (night, Nov 1721) → s1a harbour (dawn, on "Boston") → s1b Onesimus at the window. It's a
flash-forward and then back. The grenade returns at its beat, so the opening pays off. OK.

## 09 · Snow (HCS08)
Spoken hook: "In 1854, a doctor stopped a deadly outbreak… by taking the handle off a water pump." (ends 5.71 s;
the spoken line is the myth the twist corrects). The card collapses at 2.5 s, and captions start on "a deadly
outbreak…".
**Ending (don't give it):** the handle comes off, and the twist: the outbreak was already fading (OVERSTATEMENT).
So no handle and no "stopped" on the card.

| | Card | Words | Longest line | Claims |
|---|---|---|---|---|
| A ★ | 500+ DEAD. / WAS IT THE **WATER**? | 6 | 17 ch (~65 px) | "upwards of five hundred fatal attacks" in ten days VERIFIED (P1); Snow suspected the water VERIFIED (P1, S1); a question, not a claim |
| B | 500+ **DEAD** / IN 10 DAYS | 5 | 10 ch (~98 px) | VERIFIED (P1). Pure stakes, no question |
| C | BAD AIR? / OR THE **WATER**? | 5 | 13 ch (~84 px) | most doctors blamed miasma VERIFIED (S1); Snow the water VERIFIED; frame would be s3 (the doctors in green fog) |

**Pick A:** the number gives the danger, and the question gives the case to follow. With the picture under it, a
woman drinking a glass of water, the viewer feels the danger before it is explained. It isn't a spoiler: "the
water" is said at ~10 s, while the payoff is the handle and the twist.
**Frame 1, a change:** s7b (the widow takes a glass of Broad Street water), framed tighter on the glass at her lips,
with a slow camera start and a water sound. She is in danger and doesn't know it. The card goes at the **bottom**,
because her face and the glass sit in the upper half.
**Continuity, the v2.0 bug:** v2.0 opened on s8, with the handle already taken off. The next shot, s1b, showed the
pump with the handle on, and the removal is the payoff. Fix: s8 appears **only** at its beat ("On the eighth of
September…", near the end), as in v1. New order: s7b-CU → s1b (the pump with its handle, on "handle… water pump")
→ s2 (the street in mourning). The widow comes back at her beat (~25 s) at full size, so the opening pays off.
Also: no existing shot shows people drawing water at the Broad Street pump, which would be a stronger frame 1.
s7b is the closest we have. A new shot would be paid (≈$0.07) and isn't needed.

## 10 · Semmelweis (HCS09)
Spoken hook: "In 1847, a doctor told other doctors to wash their hands. They hated him for it." (ends 5.59 s). The
card collapses at 2.2 s (after "other"), and captions start on "doctors to wash their hands".
**Ending (don't give it):** he lost his job and died in an asylum; the Semmelweis reflex. "Nobody listened" is
an OVERSTATEMENT. Don't use "they all" or "nobody".

| | Card | Words | Longest line | Claims |
|---|---|---|---|---|
| A ★ | DOCTORS' **HANDS** / KILLING MOTHERS? | 4 | 16 ch (~69 px) | cadaverous particles on the doctors' hands, deaths fell after washing VERIFIED (S1); a question |
| B | HE SAID: **WASH** / YOUR HANDS. | 5 | 13 ch (~84 px) | VERIFIED (S1) |
| C | WASH YOUR HANDS? / MANY **REFUSED**. | 5 | 16 ch | "many doctors rejected" VERIFIED, but "refused" can read as "refused to wash" (his students did wash): risky |

**Pick A:** it states the horror as a question and makes you watch the hands on screen. It isn't the ending:
the hook already says "wash their hands", and the story is what it cost him. B is the safe, plain version.
**Frame 1:** s1a as now (framed up, drops from his hands, a washing sound). The card stays at the **bottom**: a top
card would sit on the doctors' faces (at ~y 520 in this framing).
**Continuity:** s1a → s1b (the professor's scorn) → s2a (the corridor that splits in two). OK.

## 11 · Finlay (HCS07)
Spoken hook: "He found what spreads yellow fever, then spent 19 years trying to make anyone believe him." (ends
4.95 s). The card collapses at 2.3 s, and captions start on "then spent 19 years…".
**Ending (don't give it):** "Finlay had been right all along" and Reed's credit. So the card doesn't say he was
right, and "nobody believed" is out (it was "almost nobody").

| | Card | Words | Longest line | Claims |
|---|---|---|---|---|
| A ★ | A TINY SUSPECT. / **19** YEARS OF DOUBT. | 7 | 18 ch (~61 px) | mosquito theory, 14 Aug 1881 VERIFIED (P1); disbelief, accepted only in 1900 VERIFIED (S1, S2) |
| B | WHAT SPREADS / YELLOW **FEVER**? | 4 | 13 ch (~84 px) | "nobody knew how it spread" VERIFIED (S1); a question |
| C | ALMOST NOBODY / **BELIEVED** HIM. | 4 | 13 ch | VERIFIED (S1, the script's own wording) |

**Pick A:** "suspect" over the mosquito on bare skin makes the insect the culprit, without saying he was proven
right, and 19 is the cost. B is the cleanest question if you want fewer words.
**Frame 1:** s1c as now. **Missing:** nothing moves in frame 1 yet. The planned mosquito retrofit fixes this
(the approved plan reuses the s3 mosquito across s1c / s3 / s5b / s8a): a small walk or a wing flick from frame 0,
plus the lamp flicker. Until then, a fast camera start + the lamp glow (free).
**Continuity:** s1c (the mosquito on the arm, night) → s5 (Finlay's hands at the larva jars) → s2a (Havana harbour,
"Havana, 1881"). OK.

## 12 · al-Razi (HCS05)
Spoken hook: "1,100 years ago, a doctor refused to treat some of his patients. On purpose." (ends 5.47 s). The
card collapses at 2.4 s, and captions start on "refused to treat…".
**Ending (don't give it):** "He was wrong. Bloodletting doesn't help meningitis", and "first clinical trial" is an
OVERSTATEMENT. "Half his patients" is not in the claims (only "two groups"), so it can't go on the card.

| | Card | Words | Longest line | Claims |
|---|---|---|---|---|
| A ★ | ONE GROUP BLED. / ONE LEFT **ALONE**. | 6 | 15 ch (~68 px Lalezar) | bled one group, "intentionally" left another unbled VERIFIED (P1) |
| B | WHAT IF THE CURE / DOES **NOTHING**? | 7 | 16 ch | his doubt VERIFIED (P1: he wanted to reach a conclusion); a question |
| C | HE DIDN'T TREAT / SOME. ON **PURPOSE**. | 6 | 16 ch | the approved hook says "refused to treat"; strictly he left them *unbled*, so "treat" is a stretch |

**Pick A:** it describes the experiment itself in six plain words, exactly as P1 says. B points at the ending
("does nothing" is close to the answer), and C stretches the claim.
**Frame 1, a change:** s5a (al-Razi drawing the curtain that splits the ward), tighter, with the curtain swinging
(an ALIVE trick, free) and lamp flicker. The card goes at the top over the vault. v2 spec: the ward conversation
(s1a) was the anti-model for frame 1.
**Continuity:** s5a-MS (the curtain) → s1a (he stops the bowl on "refused to treat", now shot 2) → s1b (his
portrait). s5a comes back at full size at "So he split his patients in two", a different size, so not a repeat. OK.
Font: the card follows the episode theme font (Lalezar), as the captions do.

---

## After the OK (step 2, not started)
1. `hook_card:` in each publish.md.
2. HookCard: pop in (~0.6 s stagger), hold to min(hook end, 2.5 s), collapse into the CASE chip, box ≤ 15%, with
   the position per episode as above.
3. text_check: fail if a card is over 8 words, over 2 lines or over 15% of the height, or doesn't match `hook_card:`.
4. Openings: Onesimus s6b-CU, Snow s7b-CU (s8 only at its beat), al-Razi s5a-MS; golden eye / Semmelweis /
   Finlay keep frame 1.
5. Per Short, in posting order (golden eye first): a contact sheet (0, 0.5, 1.5, 3 s) + a 4 s preview → your OK →
   the full render → the text sheet.
