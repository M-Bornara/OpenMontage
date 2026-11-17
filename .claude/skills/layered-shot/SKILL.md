---
name: layered-shot
description: Oddly Matt / The Human Casebook layered animation (After Effects style, our own motion instead of AI clips). Use for EVERY new story shot from storyboard to render, when a shot "only zooms", when the motion lint fails, or when the user asks for a thing to move in a shot (an insect flies in, a letter slides, a hand flinches, a medal turns). Walks the shot through layer plan → sheet / plate prompts (approval) → cut-outs → keyframes → 3 s preview → approval.
---

# Layered shot (channel: storybook-medical)

AI paints the **pieces** (stills); **we** animate them. A thing that moves is never painted into the plate.
Read first: `channels/storybook-medical/plan/layered-animation.md` (the method), `plan/story-craft.md` Rule 0 (every
beat is an action with a feeling) and `plan/production-v3.md` §2 (motion codes) and §3 (the gates).

Pilot and worked example: HCS07 s3, the mosquito (`editorial/episodes/HCS07-finlay/edit_hcs07.py` MOSQUITO,
`layers_s3.py`, `build_hcs07.py` "plate-s3-empty" / "sprite-mosquito").

## The tools

| Step | Tool | Cost |
|---|---|---|
| Plan | storyboard row + the layer table below | free |
| Prompts | `prompt_kit.empty_plate()`, `sprite_sheet()`, `pose_sheet()`, `KEY_BG` (lint L43) | free |
| Pieces | `episode.py refs <pid> <names> --batch` (after approval) | ~$0.07 each (Batch 2K) |
| Cut-outs | `fx_prep.py sheet <sheet.png> fly-0 fly-1 land-0 rest-0 --out …` → frames + `sprites.json` + `check.png` | free |
| Masks | `fx_prep.cut(plate, name, box, how="rembg", poly=…)` → `fx/<plate>-<name>.mask.png` | free |
| Motion | `layers={…}` on the shot in `edit_<ep>.py` → `remotion/Stage.tsx` `<Actor>` / `<LayerStack>` | free |
| Sound | an actor key's `"sfx": {"name", "until": "contact", "fade_out"}` → `scripts/layers.py` → the mix | free |
| Review | `layer_review.py <pid> <shot> [--build]` → `review/layers/<shot>-preview.mp4` + `-sheet.jpg` | free |
| Lint | `episode.py build` fails a story shot with only CAM motion unless `breath=True` | free |

## 1. Layer plan (with the storyboard, before any prompt)

**First pick the shot's level** (plan/layered-animation.md §7), and write it in the storyboard row with the tricks:
- **HERO** (2–3 per Short: hook, turn, climax): new pieces (empty plate + sheet), path, states, shadow, sound; free
  motion pre-viz on stand-ins before the pieces are paid. ≈$0.13.
- **ALIVE** (most shots): free; moves made from the image itself (Life.tsx presets, a free cut-out). No new pieces.
- **BREATH** (max 1–2 per Short): CAM only, `breath=True`.
Re-renders of finished Shorts get no new HERO shots, only free ALIVE tricks.

**Then write the shot's motion plan BEFORE any image prompt** (user, 2026-11-16: Finlay was painted before the
animation existed, so he can't react to the mosquito). Per shot: start pose → end pose for every character and actor,
what moves and when (on which word), the reaction (who looks, flinches, freezes), the sound. The images are then made
FOR those poses: the plate empty of what moves, a pose sheet with exactly the start / end / reaction poses, a sprite
sheet with exactly the states the keys need (each sheet with the character's or object's reference image, so the views
stay consistent: the mosquito sheet drifted into side views without one). Never paint first and animate what the
still allows.

**Frame 1 rule (packaging v2, plan/packaging-v2-spec.md):** the Short's first shot shows the danger or the strange act
ALREADY HAPPENING and something moves from frame 0 (an actor, a spark, dust, a fast camera start; never a slow
push-in or an establishing shot). The hook card sits on it from frame 0, so its layout leaves the card's band free
(top y 360+ or bottom up to 1248). Usually the hook shot is one of the 2–3 HERO shots.


For each shot, one row per layer. Decide what stays painted and what moves:

| Layer | What | Moves how | Piece |
|---|---|---|---|
| BG | the plate WITHOUT anything that moves | static, + `glows` on its real lights | `empty_plate()` from the approved still, or a new plate |
| MG | characters: the poses this shot needs | pose swaps (`xfade`) + `breath` | `pose_sheet()` (2–4 poses, same light / camera) |
| ACTORS | moving objects in their states | keyframed path + state machine | `sprite_sheet()` (one object, N states) |
| 3D | things that turn or catch light | `kind: "3d"`, a scene from `Three3D.tsx LAYER_SCENES` | none (built in code) |
| FG | depth: lamp edge, curtain, smoke | `parallax` > 1, blur | cut from the plate |

Write the beat first (story-craft Rule 0): the moment, the action (a verb), the feeling, the camera, the sound. The
layers exist to perform that beat. One idea per shot: one actor doing one thing well beats five things moving.

## 2. Prompts → approval (nothing is paid before the user's OK)

- Sheets: `sprite_sheet(obj, states, plate, light, angle, scale)`. Every state the keys need, same design / size /
  angle, on `KEY_BG` (flat chroma-key green), lit like the plate (name the side the light comes from). Draw the object
  facing RIGHT (top-down) or in the direction it will travel; the actor turns it along the path.
- Characters: `pose_sheet(person, poses, plate, light, angle, crop)` with the character's sheet as reference.
- Plates: `empty_plate(frame, remove, behind)` with the approved still as reference (`kf:<shot>`).
- Put them in the episode's build script (REFERENCES), run it (lint must be clean), and show them on the episode's
  approval page with the free preview (step 4). Tell the user the cost.
- Free stand-ins first: a plate with the object inpainted out (`fx_prep.cut(..., how="color", poly=…)`; across an ink
  outline, inpaint each side from its own side as in `layers_s3.py`) and a drawn sheet, so the MOTION is approved
  before any spend.

## 3. Cut-outs

`fx_prep.sheet()` keys the flat background (and unmixes it from smoky, semi-transparent parts), finds the figures in
reading order, puts every frame on ONE canvas, aligns them to the first frame's solid body (phase correlation) and
writes `check.png`. Look at it every time:
- every frame over magenta: no green fringe, no holes, nothing cut off;
- the onion-skin tile: ONE body outline (a double outline = the body jumps when the state changes), the yellow cross on
  the point that should ride the path (`anchor="solid"` = the body's centre).

## 4. Keyframes (data in `edit_<ep>.py`, never per-shot code)

Units: x, y = fractions of the 9:16 FRAME (measure on the still: the same numbers as fx); t = seconds in the shot;
z = depth (1 = on the surface / in focus; >1 nearer the camera: bigger, blurred). Times come from the narration
(`c.at("word")`): land / hit on the word, or just before it so the sound stops into a beat of silence.

```python
ACTOR = {"id": "mosquito", "sprites": "proj:assets/images/sprites/mosquito/sprites.json", "w": 0.09, "face": "path",
         "states": {"fly": {"fps": 50}, "land": {"fps": 6, "loop": False, "then": "rest"}, "rest": {}}, "xfade": 0.08,
         "wobble": {"amp": 0.006, "hz": 2.4, "rot": 12}, "depth": {"focus": 1, "blur": 4},
         "shadow": {"light": [-0.28, 0.07], "opacity": 0.6, "fade": 0.6, "clip": "hand"},
         "keys": [{"t": 0.1, "x": 1.08, "y": 0.37, "z": 1.7, "state": "fly",
                   "sfx": {"name": "mosquito-buzz", "until": "contact", "fade_in": 0.3, "fade_out": 0.12}},
                  {"t": 0.77, "x": 0.91, "y": 0.43, "z": 1.5}, {"t": 1.89, "x": 0.69, "y": 0.50, "z": 1.08, "stop": True},
                  {"t": 2.33, "x": 0.662, "y": 0.553, "z": 1, "state": "land", "contact": {"squash": 0.14, "lift": 0.07}}]}
c.shot(t, KF + "s3.png", push(...), layers={"bg": PLATE, "masks": {"hand": MASK}, "glows": [...], "actors": [ACTOR]})
```

Key options: `ease` (arriving segment), `out` / `in` bezier handles, `stop` (hover), `contact` (squash, bounce, lift),
`state`, `rot` (with `face: "keys"`), `sfx`. Actor options: `wobble` / `bob` / `flap` (flight), `breath` (characters),
`xfade` (pose swaps), `shadow` (`light` = offset per unit of height, `clip` = the surface mask), `depth`, `behind`
(occluded by a named mask), `motionBlur`, `parallax`, `from` / `to`.
Rules that came out of the pilot:
- route the path across a bright part of the plate (a dark speck vanishes over dark brass);
- start off frame or from behind something; never pop in;
- the contact key is where the painted object was (the plate and the story agree);
- the shadow needs a real offset (`light` ~0.2–0.3 for a close lamp) or it hides under the actor;
- keep text clear of the path (name tags and captions sit above every layer).

## 5. Preview → approval

`python channels/storybook-medical/scripts/layer_review.py <pid> <shot> --build` (build + mix + 3 s render + sheet).
Watch it with sound. Check: the actor reads at phone size, the path, the landing on the word, the shadow, the sound
stopping on contact, no text on the action. Put the preview and the sheet on the approval page; only after the
user's OK: generate the paid pieces (step 2), cut them (step 3), swap the stand-in paths in the edit, re-run the
preview, then the full render (text_check runs after it).

## 6. Lint and logs

- `episode.py build` runs `layers.lint_motion`: CAM-only story shots fail; a deliberate pause is `breath=True`.
  Episodes cut before 2026-11-16 carry `"motion_lint": "warn"`.
- Every paid piece is logged by `episode.py` in `cost-ledger.csv` and the episode's `cost_log.json`; report the cost
  before and after (memory: report-ai-costs).
- A failed piece (wrong light, merged figures, a recomposed plate) becomes a prompt_kit rule + lint + regression test
  (memory: prompt-lessons-loop).
