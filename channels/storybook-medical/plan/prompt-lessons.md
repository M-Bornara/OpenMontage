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
| L24 | Readable words still appear on paper and wall frames ("Contract", "Dear Mama", "Dr. William Osler") despite WAVY_WRITING (HC001 5.16, 5.22, 8.02; HCS01 s9: a full lorem-ipsum letter even with real_writing + WAVY_WRITING, twice) | The model writes headings and certificates by habit | Free fix: inpaint the word + soften the page (life_prep-style mask); real words go in as Remotion overlays | review (every document shot) |
| L25 | A left/right detail inside one figure lands on the wrong side: the vein in his RIGHT arm though the prompt said "his LEFT arm, on the VIEWER'S RIGHT", 3 tries (HCS01 s1b) | The model mirrors anatomy by habit; side words are weak against a symmetric figure | Generate it, then fix locally for free: inpaint the wrong side's paint (mask by colour, keep the ink line) | review |
| L26 | An "edit this image, change only X" pass made it worse (veins in both arms) or changed nothing (the lorem letter), $0.27 (HCS01 s1b, s9) | Image edits through the same model re-imagine the frame instead of editing it | For a small local change use a free local fix (inpaint + redraw), not a paid edit pass | review |
| L27 | The generated Short cover put the tube on the wrong arm, looped it round his neck like a stethoscope, and drew the empty bottom 30% as a flat band with a hard seam, $0.13 (HCS01) | A poster prompt repeats the hardest asks of the story (side, prop, empty band) in one frame | First check the approved 4K keyframes: if one already shows the hook action with a calm band for the title, use it as the cover (free). Generate only when none does | review |
| L28 | Decoupage (user review, HCS02/HCS03 rough cuts): the same lab/valley in most shots; s5 and s6 the same valley with only the centre moved; one thermometer held over three ideas; a smiling Marshall on "time to treat himself"; the presenter behind his audience, a giant kookaburra; a blank watch on "forty minutes"; a plain diagram as the payoff. 16 shots redone, $1.12 | Prompts named a set and a subject, not a shot: no size, angle, lens, action or emotion, so the model fell back on one wide view of the set | Every keyframe gets `framing(size, angle, lens, action, mood)`; one image per idea in the line; a repeated set changes size and angle; payoffs show the result in a life; numbers the line names are in the picture | `prompt_kit.framing` + lint L28 (SHOT line; same set + same size back to back) · test_prompt_lint · storyboard review |
| L30 | HCS04 prop-eye sheet came back as a log-cabin room (the HC001 style plate) with four giant foggy half-domes in it, $0.07 | A room plate as the only reference: the model copies its contents, not just its style, even with "style only" | Model and prop sheets take a plain-paper model sheet (sheet-osler) as reference for layout + style | `prompt_kit.lint` L30 · test_prompt_lint |
| L31 | HCS06 s3b: "a soft vignette at the edges" (memory look) came back as a card with a painted white paper border; fixed free by a 6% crop of the 4K image | The model reads "vignette" as a framed illustration | The image stays full-bleed (FULL_BLEED); the vignette is an edit effect | `prompt_kit.lint` L31 · test_prompt_lint |
| L32 | HCS06 s6a (user): the angry crowd stood around a door with no house; s6b drew a cartoon bomb with a fizzing spark on "the fuse went out" and s7 a plain ball, so the grenade changed between shots; HCS04 s4 drew the eye as a flat medallion unlike s1/s3. 4 redos, $0.43 | cast('six townspeople') printed "exactly 1 person: six…"; the prop was described separately per shot; s4 referenced the trench frame only | Crowds get a CROWD line, not cast(); a prop seen in several shots gets ONE description constant (GRENADE, EYE) and the later shot takes the earlier frame as reference (kf:) | `prompt_kit.lint` L32 · test_prompt_lint |
| L33 | HCS04 s5 (user, rough cut 1): "two holes held it with a thread" was drawn as a LOOP from one side (a strand down the cheek, then under the ear); two fresh prompts ("one straight line, no loop") still drew the loop, $0.24; hand inpainting smeared the skin | The model reads two holes + thread as a loop; a negative instruction doesn't undo a strong visual prior | When one detail fails twice on an otherwise good frame, EDIT that frame (reference = the frame, prompt = "change only X, keep everything else identical"): fixed first try, $0.12 | review |
| L34 | HCS08 s2 + s9a (2026-11-09): the Broad Street plate was given as "for the painting style, palette and the pump's exact design" and both shots came back as near-copies of the plate (same camera, same fog), so "the street in mourning" and "the street days later in sun" were one picture twice; s1b/s3 also leaned on it | A reference role without "only" reads as "reproduce this image" | Plate roles say "ONLY: do NOT copy its composition or camera angle; this is a different view" (the `LOOK` role in build_hcs08.py); regenerated v2 at a new angle / high angle in sun, first try, $0.13. Lint L34 + test | lint |
| L35 | HCS09 s4a (2026-11-09): a macro INSERT (scalpel at the autopsy) came back as a framed picture-in-picture card with a border | Close-up inserts invite a "detail panel" layout | Add FULL_BLEED to every macro insert; regenerated v2 full-bleed, first try, $0.12. Lint L35 + test | lint |
| L36 | HCS08 s1b, s2, s3, s4b, s8 (user, 2026-11-09): five shots on Broad Street, different sizes, all with the plate's street behind them; s4b put the pump in the middle of the road, s8 looked like hammering. L28 only compared NEIGHBOURING shots by SIZE LABEL, and framing() said "a new angle" without saying which; the plate (one fixed camera view) won over the words. The user had to catch it after paying | No set geography and no camera direction in the prompt; review missed 3 of 5 | A set MAP (MAP block: where the pump, corner house, brewery are) + `camera(position, facing, exact background, landmark)` on every shot of a repeated set; the plate is no longer a reference for street shots (style from s1a, pump design from a crop of the plate: refs/prop-pump.png). **Free pre-viz before any spend** (`scripts/previz.py`: set map with camera cones + blocking frames, now vs planned) for the user to approve. Lint L36 (any two shots on one set, not only neighbours, need distinct camera lines) + test | lint + previz |
| L37 | User, 2026-11-09, after the Snow pre-viz: "do this for every single shot analysis we do from now, high restrictions on rules"; also the pump handle must face the right way | Camera mapping was only planned for repeated sets; props with a front/back had no fixed orientation | HARD: every story shot has camera() (lint L37 + test); `episode.py keyframes` stops at the PREVIZ GATE until episode.json has "previz_approved" (after the user's OK). Props get a fixed ORIENTATION in their description (pump: spout + trough to the road, handle on its west side) and each shot says where those parts appear from its camera | lint + gate |
| L38 | HCS08 s8 v3 (user, 2026-11-10: "wrong direction for pump"): camera on the SE corner facing NW, prompt said the pump stands "close in the left third"; the model put the pump on the camera's own corner, with the corner house it belongs to across the street | A frame position ("close, left third") is not a place in the set; the model satisfies it by moving the landmark | A landmark's place is stated in SET terms in the camera line ("on the pavement right against the corner house, NOT on the near side of any street"), and the camera moves to get the frame size, not the landmark. Pre-viz cone must end ON the landmark's map position | previz |
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
| L29 | 2026-11-07 | HCS02/HCS03: no Matt in any Short (user: "I thought we included him") | One Matt cameo in a new shot of every video, Shorts included: `matt_beat()`; lint L29 flags a video without one (`require_matt=False` only for images made before the rule) | test_prompt_lint.py L29 |

## L38 · L39 (user, 2026-11-14, HCS07 Finlay / HCS05 al-Razi, before generation): "since you are using a reference image make sure duplications are not happening"
- **L38:** a model sheet shows several views of ONE person; a shot that takes a sheet carries `ONE_EACH` (each person appears once, take only face/hair/clothes). One sheet per age: a sheet with Finlay 1881 + 1900 could put both in a shot.
- **L39:** a set plate is a reference only for shots on its own set: story shots that use `ref:plate-<set>` declare `"set": "<set>"`. Other sets take the character sheets, or a style-only plate from outside the film.
- Found while writing them: wording that contains "model sheet" makes the lint treat a shot as a sheet and skip its shot checks; `ONE_EACH` says "character references" instead.

## L40 · L41 + look-alikes (HCS07 Finlay first images, 2026-11-14)
- **L40:** s4b (reverse angle) took s4a as a reference and came back as s4a again with Matt added. An earlier keyframe copies its camera: use one only for a closer shot of the same view (`"kf_same_view": true`); otherwise the set plate or an outside style plate.
- **L41:** s1a "their faces are above the frame" came back as three headless bodies. Never write faces/heads out of frame; put heads in, or show only hands/objects.
- **Look-alikes:** s6a's second officer and s9a's photographer got Reed's face (same uniform / same era, moustache). `ONE_EACH` now adds "everyone else has a clearly different face, hair and age"; give extras a distinguishing trait (clean-shaven, grey-haired, bowler hat).
- **Batch resume:** a lost connection while polling left a paid batch running (HCS05). `episode.py ... --batch --resume` collects it from artifacts/batch_jobs.json instead of paying twice.

## Round 2 (HCS05 / HCS07 images, 2026-11-14)
- **Extras duplicated without any sheet:** HCS05 s3 `cast(PATIENT, MOTHER)` ("exactly 2 people") came back with two
  mothers. A count alone isn't enough when the set has room for more: say WHERE each person is and "nobody behind / no
  second woman".
- **Period lamps:** the model's default oil lamp has a glass chimney (1800s). Ancient and medieval sets name the lamp:
  "a small open clay dish lamp with a spout and a bare flame, NO glass chimney" (HCS05 `NOT_LATER`).
- **Unbound notebooks:** "paper notebooks" came back as leather-bound books; write "unbound stacks of folded sheets,
  no covers, tied with cord".
- **A pose that won't change:** Lazear (HCS07 s7a) held the tube at his face twice. Fix the geometry, not the verb:
  "standing upright, the tube at arm's length, far below his face, at mattress height".

## L42 + rough cut 1 review (user, 2026-11-15)
- **Cloned crowds (HCS07 s1a, s4b, s6a):** "all doctors look the same, soldiers look the same". The CROWD line was one
  shared description ("about twelve bearded academics in black frock coats"), so the model drew one face twelve
  times. Fix: `prompt_kit.crowd(where, [≤5 casting cards])`, each card different in age, build, hair, beard and
  expression; everyone else from behind or in shadow. Lint **L42** flags a CROWD line without cards. Test added.
- **Top-down rooms break (HCS05 s5):** the floor was seen from above but the walls, lattice windows, wall niches and
  curtain were painted as front elevations, so the room looks folded open. Use eye-level one-point perspective
  for rooms full of furniture; keep top-down for tabletop inserts.
- **Impossible geometry (HCS05 s7b):** a bed ran through a wall and walls stacked inside each other. Close-ups
  with a plain, soft background are safer than a detailed room behind a prop.
- **FX measured off-target (HCS05 s3 lancet, s7a glasses):** the effects layer shares the camera transform (correct);
  the error was the measurement (glasses at y 0.235, glint placed at 0.20). Measure on a crop with a fine grid and
  check the rendered frame at the effect's exact time.
- **Story, not just images:** the cut felt flat because the scripts were lists of facts and the shots were poses.
  New step before every script approval: `.claude/skills/story-doctor/SKILL.md` (spine, beats, tension curve,
  action shots, rhythm map, score) → `story-v2.md` → approval page.

## L44 · L45 · L45b · L46 (HC002-S1 Gage, first HERO pieces, 2026-11-18)
- **L44:** plate-cut came back with a row of colour swatches labelled with hex codes (the style prefix lists the palette as
  hex), and plate-s8 copied them from it. `NO_TEXT` and episode.py `TAIL` now forbid swatches / palette chips.
- **L45:** a sprite / pose sheet with a character MODEL SHEET as reference printed that sheet underneath as ghosts (hat sprite,
  lying poses). `REF_IDENTITY_ONLY` is now in `sprite_sheet()` / `pose_sheet()`; lint L45 checks it. An object sprite (the hat)
  takes no character sheet at all: describe it in words.
- **L45b:** even with `REF_IDENTITY_ONLY`, a LYING pose sheet ghosted the standing sheet again. A pose far from the sheet's
  standing views, whose face isn't seen: no sheet reference (lint L45b).
- **L46:** "both hands on a bar (no bar drawn)" came back with a T-handled tool, "hands on the tamping iron" as a D-handled
  auger. Use `EMPTY_HANDS` when the prop is its own sprite; otherwise give the prop's full description with what it is NOT.
- Also: "low-crowned felt hat" became a bowler (London, 1849): name the period hat ("slouch hat of 1848, NOT a bowler").
- Cut-outs: `cutouts_hc002s1.py` `solidify()` keeps the largest piece and makes the inside opaque WITHOUT filling holes
  (filling put the key green back between the iron and his leg); colours close to the key (the hat's teal) use rembg.

## L47 + HERO size (HC002-S1 Gage HERO round 2, 2026-11-18)
- **HERO rule (user):** the moving subject fills at least 1/3 of the frame in a HERO shot (phone). Plates are designed at
  that scale (MS / CU, the subject large in the foreground); small gestures get a push-in to MS on the beat word.
  `layers.lint_hero_size` checks it at `episode.py build`.
- **L47:** an empty plate whose prompt named what is added later ("a man's shoulder and hand are added there later,
  large") came back with a man's hand painted in. Describe only the empty place. Also: `framing()` in an empty plate says
  "waist up" / "faces": write a plain SHOT line instead.
- A whole earlier plate as reference copied its wide camera again (L40 for plates): pass a DETAIL crop of it (rock, smoke,
  light) instead (`refs/s8_light_detail.png`).
- "kegs of blasting powder" came back with readable "BLASTING POWDER" labels: prop descriptions that name contents need
  "plain, no lettering". Painted out locally (rebuild the band from the wood above / below; inpaint smears it).
- Building prompt/lint code through a shell heredoc turned `\b` into a real backspace (two lint rules silently dead).
  Write such edits with a file, then grep for control characters.
- **L48 (HC002-S1 sheet-gage-after v2, 2026-11-18):** "a bandage over his LEFT eye" came back over his RIGHT eye in every
  view (the model took the viewer's left). Say "his own LEFT eye (in a front view, on the RIGHT side of the picture)".
  Fixed for free by mirroring the whole model sheet (only button side and profile side change).
- **L49 (HC002-S1 s11, 2026-11-18):** a hand-only keyframe that took the character sheet (for the sleeve) came back fine at
  9:16, but its 16:9 recompose (which gets the same references) painted the WHOLE person standing in the doorway with
  an over-long arm. A hand-only / object-only still: no character sheet; or redo the 16:9 from the 9:16 frame alone
  (`wide_s11.py`). v1 had also copied the HC001 study (shelves, lamp, quill, test tubes) from the style plate into the
  16:9: spell a bare room out ("no furniture, no shelves, no lamp") and keep other films' rooms out of the references.
- Text on set signs: "CAVENDISH HOTEL" came back readable despite NO_TEXT (a hotel invites a sign). Flat boards are
  painted out locally (`fix_s10_sign.py`: the board's letter holes inpainted).

## L47b + L51 + L52 (HC002-S1 Gage, user 2026-11-19)
- **L47b:** s2a and s2b both took the rock cut's set plate as Reference 1 with "do NOT copy its composition or camera
  position" in the roles, and both came back with the plate's camera (same cliff, kegs, planks): 2a -> 2b read as a jump
  cut with the crew popping in. A full set plate always carries its camera; the words don't hold it back. Lint L47b:
  a `ref:plate-*` / `plate-*.png` reference fails unless the file is a cropped detail (name with `detail` / `crop`), the
  spec is an empty plate, or the prompt says `prompt_kit.SAME_CAMERA`. For a new angle: no plate (style in words or a
  detail crop).
- **L51:** a hand close-up came back with a toy keg and a bar thinner than a finger: `prompt_kit.scale()` states every
  object's size next to the hand.
- **L52 (edit, not prompt):** `scripts/cut_check.py`, run by `episode.py build`: ORB + a RANSAC similarity fit on the two
  stills either side of every cut; same camera at a similar size (x0.67-1.5) over the same part of the set fails, unless
  the storyboard row says "same-camera cut intended". Free fix for Gage: 2a reframed as a tight MCU on a soft-background
  still (mcu2a_hc002s1.py), size ratio x0.37 = close -> wide.

## L53: no animated pieces cut out of a still (HC002-S1 Gage, user 2026-11-19)
- **Failure:** the 2a arm wave, the 2b hammer swings and the 0:43 head + hand lean (shot 12) were pieces cut out of the
  still (`wag` / `nudge` over an inpainted plate). The edges and the filled holes showed: "do not just grab a piece of
  picture and keep animating it". Also: 2a raised his LEFT hand, the 2b wide his RIGHT.
- **Rule:** anything that moves is a separately generated prop / actor sprite (layered-shot skill), or the shot holds
  still (camera + haze). A cut-out fx (`wag`, `shake`, `nudge`) passes only with `"cut": "approved"` after the user saw
  the cut and called it perfect.
- **Lint:** `layers.lint_cutouts`, run by `episode.py build` (fails; `"cutout_lint": "warn"` for old cuts).
- **Continuity:** the same character raises the same hand across a cut (2a mirrored to match 2b).

## L54: sprite / pose sheets are always 16:9 (HC002-S1 pose-friend-s12, 2026-11-20)
- **Failure:** the one 9:16 pose sheet of the ALIVE v2 batch (the whispering friend, with the approved shot s12 as
  reference) came back as shot 12 repainted: the street, the other man half-keyed into green, Gage's ghost where the
  friend's head should be. The three 16:9 sheets of the same batch, each with its shot as reference, came back clean.
- **Rule + lint:** `lint()` L54 fails any sprite / pose sheet whose aspect isn't 16:9 (test in test_prompt_lint.py).
- Also seen: "his RIGHT arm raised (on the LEFT of each drawing)" came back with the left arm up (the reference still
  had it that way): a free horizontal flip fixed it (alive2_hc002s1.py `flip`).


## L55 + L56 + L40 widened: the same background again and again (user 2026-11-20, audit of all episodes)
- **User:** "make sure the backgrounds are not going to be similar again ... find out where the problem is".
- **Not thin prompts.** `view_check.py` on every project: 28 stills in 9 episodes are the SAME picture as the set plate
  they were given (ORB 133–1858 matching points). HCS05 s5a / s5b / s6 had long camera() lines facing west, south and
  north and all three came back as plate-ward.png with a person painted in. The image model treats a full scene among
  the references as the picture to EDIT; "style only" / "do not copy its camera" / camera() lose every time.
- **Why it kept coming back:** every episode passed its set plate (or another keyframe, HCS08 kf:s1a x5) as Reference 1
  on every shot; the kit's own L1 / L39 / L40 messages recommended "a people-free plate" / "the set plate" as the fix;
  L36/L37 added more words against the picture; L40 only fired with a declared "set"; --lint-ok waved findings
  through; and nothing compared the images until the edit (cut_check L52), after the spend and the user's review.
  Thin settings made it worse where they existed (HCS09 s1b: "SET: the hospital, a corridor." and no camera line).
- **Rules:** L40 now fires on any kf: reference (unless kf_same_view); L55 every story frame has its own set_block()
  and a camera() BACKGROUND of >= 8 words; L55b no two story frames share a BACKGROUND; L1/L39/L40 messages point to
  a cropped detail or no scene at all. `episode.py`: L36/L37/L39/L40/L47b/L55 are a hard gate (--lint-ok does not
  skip them; --legacy only) and the sequence rules compare a re-roll with the whole episode. **L56** `view_check.py`
  runs the moment keyframes come back: any still that matches its scene reference or another keyframe (>= 120 ORB
  inliers; a shared prop / face scores 47–77) is shown to the user before the edit.
- **Per episode:** a `backgrounds-v1.md` sheet (one written background per shot, from the set map, neighbours checked)
  goes on the approval page with the storyboard (HCS10 first).
- **Refined (user 2026-11-20):** "no two shots share the same background" must still allow returning to a place on
  purpose from a different camera. L55b now fails only BACK-TO-BACK shots with the same BACKGROUND, or a later shot with
  the same camera (position + facing) and background; L36 compares position too. view_check L56: a copied reference or a
  back-to-back same view fails; a same view later in the film is a note. Already-packaged Shorts: only back-to-back
  jump cuts get fixed, free fixes only (reframe / crop / reorder); a paid re-roll needs the user's OK.

## L57 + L58 + L59 (HCS10 Pettenkofer HERO pieces, 2026-11-20)

- **L57 · "handwriting" in a sheet's subject brings real letters back.** pose-hand-s7 said "a loose sheet of paper
  covered in faint wavy handwriting" and came back reading "Lorem ipsum dolor sit am…", although WAVY_WRITING was in
  the prompt. In a sheet, say "faint grey wavy lines, no letters" and nothing else about writing. Lint L57. (Free fix
  used on v1: hero_real_hcs10._soften_writing inpaints the ink strokes inside the paper and blends 25 % back.)
- **L58 · a state that changes a prop's shape keeps the prop's full size.** "The fingers curl and clutch the paper,
  crumpling it" came back as a small paper ball in a fist: the flat 21 cm sheet vanished between the drawings, so the
  swap pops. Say: the sheet still at its full size, mostly spread, only the part under the fingers dragged into creases.
  Lint L58. Also: "EXACTLY the same forearm and wrist" was not enough (the wrist moved); name every part that stays
  (forearm, sleeve, cuff, wrist) and "not moved or turned".
- **L59 · an empty plate + a Matt cameo: Matt fills the empty place.** plate-s4 asked for "the empty space behind the
  bench in the centre, where the professor will stand" and painted Matt there. Say where Matt is AND "away from the
  empty place". Lint L59.
- **Not lintable, noted:** plate-s4 "OTS, students in the foreground at the edges" came back as a wide shot with the
  students walking full-figure in the middle ground: give the foreground backs a size ("filling the lower corners up
  to 0.35 of the frame height"). plate-s1 "the top of his hair at about one third of the frame height" came back at
  0.17: ask for a lower number and say the upper third is only wall ("nothing of him in it").
Tests: test_prompt_lint.py (the v1 prompts fail, the v2 prompts pass).

## L58b + L60 + the cut-out edge (HCS10 Pettenkofer re-rolls, 2026-11-20)

- **L58b**: the v2 hand sheet said "never a ball" in the pose text but its SCALE line still said "crumpled, a ball of about
  4 in". The size line is read as a fact and wins. A crumpling prop gets its size as still spread ("still 8 in wide when
  clutched, only the strip under the fingers creases"). Lint: `L58` also fails on "a ball" outside "never a ball".
- **L60**: plate-s4 v1 asked for a CLOSE over-the-shoulder AND carried SAFE_FRAMING ("everything inside the central 70%,
  room to zoom"); it came back wide with the students small in the middle. An OTS plate uses `OTS_FRAMING` (only the
  subject in the central 70%, the foreground backs big and cut by the edges). v2 with it: a true OTS first time.
- **Cut-out edges (fx_prep, not a prompt)**: the unmixing divides by a small alpha, so the soft outer edge of a cream sheet
  came out PINK (173, 74, 77 at alpha 194) and alpha-0 pixels kept stray magenta/cyan that a straight resize bleeds in.
  `fx_prep._bleed_edges` (every sheet cut now): alpha-0 pixels and magenta-shifted soft pixels take the nearest solid
  colour. `sheet(..., fill_holes=True)` for an object lying on paper: the fingers' grey-green shadows keyed as holes.
  Preview resizes are premultiplied (RGBa) as a browser does.

## L61 + L11 pince-nez + the stamp rule (HCS10 rough cut 1 review, user 2026-11-20)

- **L61**: the critics (s10 v1) came back as "a white beard and pince-nez" (= Pettenkofer + glasses) and "a full dark
  beard" (= Koch). Extras never carry a lead's signature look. Each build declares `SIGNATURES` (lead -> regexes, stored
  in episode.json "signatures"); `prompt_kit.lint_lookalikes` checks every crowd() card, in the build and before any paid
  keyframe run. v2 cards (bald / grey side-whiskers / moustache only, "none wears eyeglasses") came back right first time.
- **L11** now catches pince-nez, monocle and eyeglasses, not only "spectacles" (a negated "none wears eyeglasses" passes).
  L11b: a real person's documented spectacles via `real_spectacles()` (Koch).
- **Stamps** (not a prompt): a stamp adds a place, date or name, never the spoken words; a repeat may stay only if it lands
  before the words. `scripts/stamp_lint.py`, run by `episode.py build`.
- **L29** (Matt cameo) now also sees a HERO background in "references" (shot 4's plate), not only keyframes.
- **Tool**: a transparent glass on a chroma-key sheet keeps the key's green (s6's mint glass); grade the glass box after
  the cut (edit_hcs10.py `_clear_glass`). A pose pair cut with whole-body alignment can still jump at the swap when the
  arm changes: align on the head + collar (s4's palm drawing was 48 px off).
