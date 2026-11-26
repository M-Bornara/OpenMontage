# Layered animation: we animate, we don't generate clips (user, 2026-11-16)

Goal: every story shot is a small multi-layer animation built by us, like After Effects: a background plate, cut-out
actors and props that move on top, 3D objects as layers, and sound on the moves. AI makes the *pieces* (stills);
the motion is ours (Remotion, Three.js, Blender). AI video clips become the rare exception.

Example (Finlay): plate = the hand on the table, no mosquito · sprite sheet = the same mosquito flying (2 wing
frames) and landed · the mosquito flies in on a curved path, wings flapping, its shadow growing on the skin, slows,
lands with a tiny bounce, wings fold (state swap), buzz SFX fades to silence on landing.

## 1. The layer plan (part of every storyboard shot, decided by us)
For each shot the storyboard lists, before any prompt:
| Layer | What | Static or moving | Source |
|---|---|---|---|
| BG | the plate WITHOUT anything that will move (empty chair, hand without the mosquito) | static (+ Life: drift, flicker) | generated plate, or the still with the object removed (inpaint / clean plate, fx_prep) |
| MG | characters: same character in the poses this shot needs (cast-sheet style, one image) | moving: pose swaps + ACT (breath, tremble, blink, head turn) | generated pose sheet → cut-outs |
| ACTORS | moving objects (mosquito, letter, needle, cup, door) in their states (flying/landed, open/closed) | moving: path + states | generated sprite sheet on a flat background → cut-outs |
| 3D | objects that must turn or catch light (medal, heart, catheter route, coin, bottle) | moving | Three.js toon (Three3D.tsx), Blender for hero physics |
| FG | foreground for depth (lamp edge, curtain, smoke) | slow parallax | cut from the plate or generated |
| FX/TEXT | glow, highlight, hook card, CASE chip, captions | — | Fx.tsx, ShortFx.tsx |
Rule: decide per shot what stays painted in the background and what is a separate moving layer. A thing that moves
is never painted into the plate.

## 2. Making the pieces (prompts, all stills)
- **Sprite sheets**: one image per actor with every state side by side, same design, on a flat plain background
  (cuts cleanly), e.g. "mosquito, side view, 4 states: wings up / wings down / landing legs out / landed, wings
  folded". Like our cast sheets. ~$0.15 per sheet.
- **Pose sheets** for characters: the same person in 2–4 poses of this shot (reach, flinch, look up), matching the
  plate's light and angle.
- **Plates** generated empty of the moving things; or a clean plate made from the existing still (fx_prep).
- Light, angle and scale of sprites must match the plate: the prompt names the plate's light direction and camera.
- Cut-outs: rembg / colour key (scripts/fx_prep.py), saved as PNG with alpha, checked in magenta over the plate.

## 3. The motion (Remotion, free)
A reusable `<Actor>` layer: keyframed path (bezier, ease), state machine (loop "fly" frames at N fps, then "land",
"idle"), procedural life (wobble noise, flap, bob, breathing), rotation following the path, squash/settle on
contact, contact shadow on the plate, depth (scale + blur by z), occlusion (in front of / behind a named layer
mask), motion blur, and SFX cues fired from keyframes (buzz while flying, tap on landing). Characters use the same
layer with pose swaps + ACT. 3D objects render as a layer via Three3D (toon look, light matched to the plate).
Shots are described in the episode's edit_<ep>.py as data (layers + keyframes), not hand-coded per shot.

## 4. Review
For each layered shot: a 3-frame contact sheet (start, middle, end) + a 3 s preview MP4 before the full cut. Lint:
a story shot with no moving layer (only CAM zoom/pan) is refused unless marked "breath".

## 4b. Built (2026-11-16) — the workflow is the `layered-shot` skill (`.claude/skills/layered-shot/SKILL.md`)
- Motion: `remotion/Stage.tsx` `<Actor>`, `<ActorShadow>`, `<LayerStack>` (wired into `StorybookShort` ShotLayer via
  `shot.layers`); 3D layers: `Three3D.tsx` `LAYER_SCENES` (medal).
- Data + sound + lint: `scripts/layers.py` (`build_layers`, `sfx_cues` → the mix, `lint_motion` in `episode.py build`).
- Pieces: `prompt_kit.sprite_sheet()`, `pose_sheet()`, `empty_plate()`, `KEY_BG` (lint L43); cut-outs
  `fx_prep.sheet()` (key + unmix, aligned frames, `sprites.json`, magenta + onion-skin `check.png`).
- Review: `scripts/layer_review.py` (3 s preview with sound + start/middle/end sheet); the approval page shows it
  (`storyboard_page.py` `layered_block`).
- Pilot: HCS07 s3 mosquito (`edit_hcs07.py` MOSQUITO, `layers_s3.py` free stand-ins, `build_hcs07.py` paid prompts).

## 5. Cost and limits
Pieces: ~$0.15 per sheet/plate (often 2–3 per shot instead of 1). Motion: $0. Clips (Kling) only when a layer
animation can't tell the beat (fluids, crowds, complex hand work), approved per shot as before.

## 6. The trick library: any 2D After Effects trick (user, 2026-11-16)
The goal is the whole After Effects 2D toolkit, not one mosquito. Each trick becomes a named preset in
`remotion-composer/src/tricks/` that a shot can call by name in edit_<ep>.py. Before building, check which ones
Puppet.tsx, Life.tsx, Fx.tsx and Three3D.tsx already do; reuse those, build the rest.

| # | AE trick | Story use | How we do it in Remotion |
|---|---|---|---|
| 1 | Keyframes + graph editor easing | every move feels weighted | `interpolate` + `Easing.bezier` presets (ease-in, ease-out, snap) |
| 2 | Motion path + auto-orient | mosquito flies in, leaf falls, ball rolls | `<Actor path>` bezier, rotate along path |
| 3 | Anticipation, overshoot, squash & stretch | a jump, a landing, a slam | `spring()` + scale on contact |
| 4 | Parenting / null objects | hand moves with arm, hat with head | nested transforms with pivot points |
| 5 | Puppet pin tool | head tilts, hand trembles, chest breathes, arm reaches | character cut into parts (rig sheet) on pivots; small bends with a mesh warp |
| 6 | Wiggle expression | nervous hands, fever shake, candle | `@remotion/noise` on position/rotation |
| 7 | Loop expression | wing flap, breathing, clock tick | frame modulo cycles |
| 8 | Frame swap / sprite sheet | blink, mouth open, wing states, door open | state image swap per frame range |
| 9 | Animating on 2s / time remap / hold | hand-drawn feel, freeze on the shock moment | frame quantize; hold frames |
| 10 | Masks + track mattes | reveal, wipe, figure behind a door, x-ray view | `clipPath` / `mask-image`, animated |
| 11 | Trim paths (draw-on lines) | map route, blood path, a signature, a crack | SVG `strokeDashoffset` |
| 12 | 2.5D camera on 2D layers | depth when the camera moves | parallax by layer depth; push, pan, dolly |
| 13 | Camera shake, rack focus | impact, panic, shifting attention | wrapper with noise shake; animated blur by layer |
| 14 | Motion blur, echo trails | fast swat, fall, whip | directional blur + ghost copies |
| 15 | Turbulent displace | heat haze, fever, water, smoke, dizziness | SVG `feTurbulence` + `feDisplacementMap` |
| 16 | Particles | dust, rain, snow, sparks, flies, blood drops (no gore) | particle component with seeds |
| 17 | Light: glow, rays, flicker | candle, lamp, sunrise, surgical light | animated gradients + glow filter |
| 18 | Colour change over time | cold to warm, calm to danger | animated grade on the whole shot |
| 19 | Moving shadows | contact shadow, a shadow entering before the person | shadow layer tied to the actor |
| 20 | Liquid fill / drip | glass filling, ink spreading | mask grows along a shape |
| 21 | Text animators | typewriter date, per-letter pop | split text, staggered |
| 22 | Card flip / pseudo-3D turn | letter turns over, coin flips | `rotateY` with perspective |
| 23 | Cartoon accents | speed lines, impact flash, smear frame | overlay presets |
| 24 | Transitions | match cut, whip pan, shape wipe, ink-bleed reveal | transition presets between shots |
| 25 | Lip sync (later) | a character speaks | mouth shapes from the voice track; only after 1–24 work |

### What this changes in image generation
- Characters that need puppet moves are generated as a **rig sheet**: head, torso, upper arm, forearm, hand,
  legs as separate parts on a flat background, same light, plus 2–3 expression heads. Big pose changes still use
  pose sheets.
- Objects that change state get a **state sheet** (closed / open, still / flying, full / empty).
- Backgrounds are generated **empty** of anything that will move.

### Rule
Every story beat uses at least one trick from 2–11 or 15–20 (an action), not only camera moves (12–13).
The storyboard names the tricks per shot, e.g. `mosquito: path(2) + flap loop(7) + land squash(3) + shadow(19)`.

## 7. How we use it: the plan (approved by the user 2026-11-16)

### Scope
| Video | Layered animation | Why |
|---|---|---|
| Packaging v2 re-renders (golden eye, Onesimus, Snow, Semmelweis) | none new; free Life tricks on the existing images only | due within days; only the opening changes |
| HCS07 Finlay (Dec 3) | s3 mosquito with the real pieces (plate + sheet, $0.13) | the heart of the Short |
| HCS05 al-Razi (Dec 7) | one free HERO: 7a, the reed pen moves and the writing draws itself on | no new image needed (draw-on + one cut-out) |
| The Nov 29 Short and every later one, HC002 Gage when un-parked | fully layered, planned from the storyboard | the first Short designed this way from the start |

### Three levels per shot (named in the storyboard)
- **HERO** (2–3 per Short: hook, turn, climax): empty plate + sprite/pose/rig sheet, path, states, shadow, sound.
  ≈$0.13 per shot (2 pieces, Batch).
- **ALIVE** (most shots, free): something in the picture moves, made from the image itself: breath, blink, flicker,
  smoke, sway, a cut-out hand that trembles (Life.tsx presets + free cut-outs).
- **BREATH** (max 1–2 per Short): CAM only, a deliberate rest (`breath=True`; the build lint allows it).
Each storyboard row names its level and its tricks, e.g. `HERO · mosquito: path + flap + land + shadow · buzz → silence`.

### Steps per episode
1. Story beats (story-doctor): mark the 2–3 HERO beats.
2. Storyboard: level + tricks + layer plan per shot → user OK.
3. **Motion pre-viz (free):** every HERO shot moves on stand-ins on the approval page; the user approves the motion
   and the piece prompts together (this gate replaces the sketch pre-viz and the prompt gate for HERO shots).
4. Images: stills + the empty plates and sheets for HERO shots.
5. Rough cut with the real motion → user review.
Cost: ≈+$0.30–0.40 per Short (3 HERO shots); images stay ≈$1–1.50.

### Build next, only when a storyboard needs it (validate before automating)
1. **Character rig**: rig sheet (head, torso, upper arm, forearm, hand on a flat background) → parts on pivots in
   `<Actor>`: head turn, reach, flinch, blink. First user: al-Razi 1a (raised palm) style shots.
2. **Free cut-out from an existing still**: one command (object out + plate inpaint), generalising `layers_s3.py`,
   so ALIVE shots cost $0.
3. **Draw-on writing / lines** (al-Razi 7a), then liquid fill, card flip, heat haze as stories call for them.
