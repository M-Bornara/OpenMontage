# Image prompt lessons (living log)

Every generation round teaches us something. A lesson only counts once it's **enforced**:
- as a building block in [`scripts/prompt_kit.py`](../scripts/prompt_kit.py) that the next episode's prompts use; **and**
- where possible, as a **lint rule** that stops `refs` / `keyframes` / `thumbs` / `covers` *before* any money is spent.

`--lint-ok` overrides the lint, but only after reading the finding.

**After every image review (G3), do this:**
1. Add each new failure to the table below: symptom → cause → fix → where it's enforced.
2. Add the block or lint rule to `prompt_kit.py`.
3. Run `python channels/storybook-medical/scripts/test_prompt_lint.py`. It checks that the lint still catches the
   recorded failures, so a lesson can't quietly stop working.

## Lessons
| # | Symptom (where seen) | Cause | Fix | Enforced in |
|---|---|---|---|---|
| L1 | Alexis / a red-tuque man pasted into empty scenes, close-ups and other people's scenes (HC001: 19 of 61) | The kit style anchor *is* the pilot's red-tuque voyageur; the model copies its content, not just its style | Shots without that character use a **people-free episode plate** as reference 1 | lint L1 · `NO_PEOPLE` |
| L2 | Same, in scenes where he does belong but a second copy appears | No instruction that reference 1 is style only | `ANCHOR_NOTE` whenever the anchor is used | lint L2 |
| L3 | Square close-ups drawn as a framed card with a white margin (HC001: 5) | "Square frame" reads as a card | `FULL_BLEED` on every square | lint L3 |
| L4 | Thumbnail text side painted as a flat panel with a hard seam (HC001 thumbs A, C) | "Plain/empty background for text" | `TEXT_SIDE`: the same scene continues, darker and out of focus | lint L4 |
| L5 | Clock hands never exact (12:00 → 11:58, 2:00 → 1:50) | The image model can't do precise hand angles | `NO_HANDS`; Remotion draws exact, animated hands | lint L5 |
| L6 | The opening on the wrong person (the doctor) or the wrong side / place (shoulder, chest, right side) (HC001 thumb A, I02, I09) | Two bodies in frame, and left/right is ambiguous to the model | `body_mark(person, what, side, where)`; check the side after generation; **mirror** if wrong (free) | lint L6 · review |
| L7 | Extra people: a duplicate Alexis in bed, an officer with a vial, onlookers (HC001 M10, M25) | No cast list | `cast(...)`: "exactly N people… nobody else" | lint L7 (partial) · review |
| L8 | Writing on props: river names on the map (misspelled), "Contract", a signature-like scribble, a modern US map on a wall (HC001 refs, I13) | Props invite text | `NO_TEXT`; frame away from what can't be fixed | lint L8 |
| L9 | Red vials and a dark-red string (HC001 I03a test, study plate) | Default colours | `RED_RULE` | prompt block |
| L10 | Fort Mackinac drawn castle-like; modern state borders on the map | The model's generic "fort" / "map" | `PERIOD` + an exact description ("whitewashed stone walls, wooden blockhouses") | prompt block · review |
| L11 | Reading spectacles in a London scene would confuse the spot-the-glasses game | A generic prop | Only Matt's amber spectacles, only where planned | lint L11 |
| L12 | Matt's glasses placed in dull spots (a shelf, a rail); Matt only once in a long video | No gag written into the plan | `glasses_gag(...)` and `matt_beat(...)`, written in the shot plan as a joke; 4–6 Matt beats per long video | `brand-signature.md` · shot-plan column |

## Things that worked first time (keep doing them)
- **Chaining from the episode's character sheets:** likeness held in every image (HC001).
- **Thirds composition for wide masters:** the 9:16 windows read as designed shots.
- **Recomposing a pilot plate into 16:9** with "this same room": continuity kept.
- **One end-of-stage re-roll batch** with all lessons applied: HC001 26/26 usable.
- **Batch size doesn't matter for quality.** Each request in a Gemini batch is independent (no shared memory).
  Batches are grouped **by category** (wide images / close-ups / tall / covers) only to make review easier.

## Open (no code fix possible, review catches it)
- An extra person in a scene that has a valid cast (HC001 M25), or people added around a grave (M34).
- Mirror-fixes when the side is wrong.
