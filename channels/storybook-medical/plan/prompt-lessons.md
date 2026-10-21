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
| L13 | Cover text band ignored (a hand drawn through it, S2) or faked as a blurred strip with a hard seam (S1) | The band alone isn't a layout | `poster_layout(text_band, head_at, entries)`: say where the head is and where hands enter (from the side, not through the band) | prompt block · review |
| L14 | The opening drawn on the character's RIGHT when he faces the camera (HC001 thumbnail A, S1, S2 covers) | "His left" is ambiguous to the model when he faces us | `body_mark(..., facing_camera=True)` adds "his LEFT side = the viewer's RIGHT side"; mirror as a free fix | prompt block · review |
| L15 | "Illegible copperplate" came back as readable **"Lorem ipsum… Contract… signature"**, twice (HC001 I13; seen in the S3 render) | "Illegible" still invites letters | `WAVY_WRITING`: rows of wavy ink lines with no letters and no heading, slightly out of focus; lint L8 requires it for writing props. **Even then the first line can still say "Lorem ipsum" (third try), so the free post-fix is to blur only the written block (PIL Gaussian ~7 px with a soft mask)** | lint L8 · prompt block · post-fix |
| L16 | Pages, books and contracts keep coming back with lorem ipsum (HC001 I11, I13; seen by the user at 3:27, 5:11, 7:18) | The model needs *something* to write and fills the page with placeholder Latin | `real_writing(text)`: give the page its **real words**, a short period-true heading or quote from the script and sources (under ~8 words, e.g. "Experiments, 1825"), spelled exactly; every other line is wavy ink lines; "never Latin or placeholder text". Lint L8 accepts this or WAVY_WRITING. The blur post-fix stays as a backup | lint L8 · prompt block |
| L17 | The story's subject sits at the frame edge (HC001 M17: the vials touch the bottom edge), so the camera can't zoom, pan or focus on it (user, focus reel) | Nothing in the prompt asked for room around the subject | `SAFE_FRAMING`: every story-relevant person, object and action inside the central 70%, with room for the camera | lint L17 · prompt block |
| L18 | The brass-porthole look was used for the moment of the shooting (HC001 1.13), but in June 1822 it was a fresh gunshot wound; the opening only healed into the 'window' later (user, animatic v1) | The brand symbol was applied to every stomach shot regardless of the timeline | The porthole look is only for the HEALED opening (winter 1822–23 on). At the injury: a restrained painted wound (torn, scorched shirt, dark opening, powder burns, a little blood, no gore). Story-time check per beat | beat sheet note · review |
| L19 | One log-cabin office everywhere: Mackinac 1822, Niagara 1825, Washington 1833, St. Louis, even Osler's office in 1880 (HC001 v1 M01 M11 M13 M17 M18 M27; user, animatic v2) | No place or year in the prompts, so the model fell back on its default room | `sets_<ep>.py` (place + year + look per set) and `set_block()` in every story prompt; the builder never lets a set change be a plain cut | lint L19 · beats.py |
| L20 | A first+last-frame pair came back at two different shot sizes (HC001 1.15a wide, 1.15b close-up), so the clip would become a zoom | The two frames were generated separately and "close on his face" lost to the plate's wide room | Generate the better-framed frame first, then derive the other one from it ("SAME FRAME as reference 1, only one change") | shots_*.py `first=` · review |
| L21 | The injured man stood up holding his own shirt open (HC001 1.13 v1) | "Over the doctor's shoulder: the wound" never said what Alexis's BODY was doing | Injury and illness shots state the posture explicitly (lying on his back, unconscious) plus a "NOT standing" guard | review · shot prompts |
| L22 | A prop sprite copied the model-sheet layout: four extra Alexis heads above the canoe (HC001 prop-canoe-solo v1) | A sheet as the only identity reference plus "plain background" reads as "make a sheet" | Derive a second sprite from an approved one ("SAME IMAGE, only X changes"); never send a sprite with only a sheet | review · shots_*.py `first=` |
| L23 | Widening a square close-up changed its meaning: the body porthole became a ship's porthole in a wall, the string shot gained a wrongly dressed Alexis (HC001 wI19, wI01, $0.24 unused) | "Extend the scene" invents a scene when the square image has an abstract or tight background | Prefer a zoom into an existing 16:9 shot of the same subject; widen only close-ups with a clear, real setting | review |
| L24 | Readable words still appear on paper and wall frames ("Contract", "Dear Mama", "Dr. William Osler") despite WAVY_WRITING (HC001 5.16, 5.22, 8.02) | The model writes headings and certificates by habit | Free fix: inpaint the word + soften the page (life_prep-style mask); real words go in as Remotion overlays | review (every document shot) |
| E3 | Dissolves flickered in the animatic: the film dissolve adds light ('plus-lighter'), and the transition was drawn over the shots beneath it, so the brightness doubled (user: the graveyard) | A transition layer that isn't isolated blends with what's under it | Every transition renders on an opaque, isolated stage. Beats on the same image are ONE continuous camera move, never restarted | code (Transitions.tsx, Animatic.tsx) |
| E4 | After every transition the incoming shot repeated about 1 s (user, animatic v2) | The incoming shot ran on the transition's clock, half a transition ahead of its own sequence | The incoming shot holds its first frame until the cut point, then runs on its own clock (`InShot`) | Animatic.tsx |
| E5 | Only 2 of the hook's flash-forwards played, each for too long (user: "random cuts") | Inserting the new hook line also stretched the beat that ends where it is inserted | Beats that start before the insert keep their end | Animatic.tsx |

## Clip lessons (Kling v2.1 standard, image-to-video)
| # | Symptom (where seen) | Cause | Fix | Enforced in |
|---|---|---|---|---|
| K1 | After the action, the character does it again (a second axe chop: HC001 C5; Veo did the same in the sh06 test) | 5 s is longer than one action; the model fills the time | Write **ONE action, then everything holds still until the end** (`CLIP_HOLD`); trim with `"use": [start, end]` | `prompt_kit.CLIP_HOLD` · `use` trims |
| K2 | The moving object doesn't reach its target (the beef never reaches the porthole: C1) | Image-to-video can't hit a precise spot | Animate the *motion*, then cut to a close-up of the result (C1 → I02) | shot plan |
| K3 | Camera creeps in or the subject drifts against the brief (C4 drifts right, C8 pushes in) | The model adds motion | Choose clips whose story survives small drift; mirror the source if direction matters | review |

## Narration lessons (ElevenLabs v3, Liam)
| # | Symptom (where seen) | Cause | Fix | Enforced in |
|---|---|---|---|---|
| N1 | 20 % of sentences run into the next (< 0.3 s of silence), even with a line break after each one (HC001: 29 of 147) | v3 treats line breaks as soft; fast, excited delivery | A `[pause]` tag after each sentence: HC001 ch6 went from 5 tight to 0 (min 0.32 s, median 0.80 s), and the tag is not spoken. It costs about 16 % more length, so the owner judges the pace | `narrate` spacing check · owner listen |
| K5 | Kling v2.1 standard faded the people OUT of the room in the last second (HC001 v2.02 at 3.8 s, v5.08 at 3.1 s), despite CLIP_HOLD | The model "finishes" a short action by emptying the scene | Review every clip to its last frame; record the usable window (`use`) and cut before it. The first+last-frame clips (pro) never did this | review · clip `use` |

## Edit and music lessons
| # | Symptom | Cause | Fix | Enforced in |
|---|---|---|---|---|
| E1 | An edit anchor doesn't match ("two hours", "realised", "That one's") | The transcriber writes digits, US spellings and its own contractions | Anchor each shot on nearby plain words, never on numbers or spellings | `edit_*.py` (the builder stops if a phrase isn't found) |
| E2 | "Eight, ten months" read as a hesitation, captions "8, 10" | A comma between numbers | Write it as the source does ("eight or ten months") | script review |
| M1 | Short music tracks (~43 s) would loop 12 times under a 9-min video | MiniMax picks its own length | `"sections": 8–10` for longer tracks; 4 cues following the story's acts, crossfaded (`music.cues`) | `episode.py music` / `mix` |
| M2 | The vocal check fires on "." | The transcriber returns punctuation on instrumentals | Vocals = at least one real word | `episode.py music` |

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
