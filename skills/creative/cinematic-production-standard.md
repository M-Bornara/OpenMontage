# Cinematic Production Standard (all OpenMontage projects)

**Applies to every narrated or story-driven video, whatever the story, channel or pipeline.** Written 2026-10-20 from the
first full review of a long-form episode (HC001, 34 notes) and the follow-up test reels. The agent decides *where, how and
when* each technique is used; this file sets the bar and the rules for deciding.

The reference implementation lives in `channels/storybook-medical/` (Remotion `Fx.tsx`, `Life.tsx`, `Transitions.tsx`,
`LabReels.tsx`; scripts `masks.py`, `life_prep.py`, `lab.py`, `prompt_kit.py`). Reuse it, and move it into a shared
library when a second project needs it.

---

## 1 · Plan everything before spending: beat sheet → animatic → approval

No paid image, clip, voice or music call runs before the user has **seen** the film planned as an animatic.

1. **Beat sheet (decoupage).** Derive it from the narration, one row per beat, every 3–4 s in tense parts and 5–6 s
   in calm ones. Columns:
   - key word (the beat is anchored to it);
   - what we SEE (action verb first);
   - shot size and angle;
   - **set** (place + year, from a set list where each set has its own look: materials, palette, light);
   - cast (each person by their reference);
   - subject box (where the subject sits in the frame);
   - camera move and its **target**;
   - **source type**: still, living still (which life layers), separate sprite props, clip, or first+last-frame clip;
   - the transition in, and why;
   - focus effect / motion graphic / overlay;
   - SFX;
   - mood 1–5;
   - match-cut partner, if any.
2. **Animatic (wireframe storyboard, free).** Rendered in Remotion from the beat sheet, with:
   - the real narration (or a draft TTS) and temp music;
   - each beat as a wireframe card: subject boxes at their planned positions, labels, shot size, a camera-move arrow
     and target;
   - the **real** transitions, focus effects, overlays, motion graphics and captions applied.
   The user watches the whole film's rhythm, sync and structure before anything is generated. Problems found here
   (a missing action, a still that is too long, a flat section, a repeated image, a weak hook) cost nothing to fix.
3. **Approval gates.** Every paid step is approved separately: beat sheet / animatic, cast, prompts per batch,
   images, clips, narration, music, rough cut, fine cut, thumbnails, publish. Estimate the cost before each paid call,
   report the actual cost after.

## 2 · Images

- **Lead with the action.** `[who] is [doing what] to [what], [visible emotion]`, then shot size and angle, then the
  setting last. Every action the narrator names is shown.
- **Native aspect only.** A 16:9 video uses 16:9 images. A 9:16 / Short may crop a window out of a 16:9 image when the
  crop holds the action. No square crops. Close-ups are generated as close-ups, never made by zooming a crop.
- **Safe framing.** Story subjects sit inside the central 70% of the frame, so the camera can zoom, pan and focus on
  them.
- **Distinct sets.** Every story image names its set (place + year) and carries that set's own look in the prompt.
  Different places and years never share one generic room (in HC001 v1 one log-cabin office stood in for five
  places across 58 years). A set may return only when the story returns to that place.
- **Distinct cast.** Every recurring person has a reference sheet. Extras come from a reusable troupe library. Nobody
  may resemble a main character.
- **Writing.** Give pages their real words (a short, period-true heading or quote); every other line is wavy ink
  lines. Never accept placeholder or Latin text. A blur post-fix is the backup.
- **Layered generation (planned in the animatic).** Anything that should move (birds, a canoe with its passengers,
  chickens, a swinging sign) is generated as a **separate prop** on a plain background and composited over an
  **empty plate**. Then it animates cleanly. Never cut a mover out of a busy painting: the cut-out edge shows.
- **Match cuts are designed, not found.** Both images are planned with the shape at the same size and position.
- Keep a lint for every prompt lesson, enforced before any paid call (see `prompt_kit.py`).

## 3 · Motion: clips vs living stills

- **Living-still overlays can be used freely:** particles (dust motes, sparks, embers), light glows (lamp, fire,
  window), light rays, rain, fog, falling leaves, light shifts. They're add-ons, so there's nothing to cut out.
- **Animating part of a still** (sway, bob, breathe, parallax, sky drift, water ripple) only when the moving part sits
  on a **clean, light, simple background**, or when it was generated as a separate prop. If the cut-out edge would be
  visible, don't use it.
- **Clips** are for real actions (a shot fired, food thrown up, an axe swing). One action, then stillness.
- **First + last frame clips** (Kling v2.1 pro/master `tail_image_url`, about 2× the standard price, plus one image for the
  end frame) are for actions that must END in a specific state (food pulled out of the porthole, a door closing).
  The end frame pins the motion, which removes repeated actions and missed targets. Plan them in the beat sheet.
- A clip that ends before its slot is followed by a **different** image, never a still of its own frame.

## 4 · Camera

- Every push and pan is centred on the **target** the narration names (person, object, action). Never the chair, the
  wall or the floor.
- Smooth only: a sine in-out ease, slow speeds (≤ ~0.03 scale/s for calm shots), with the source above the output
  resolution (≥ 1.5×). No jitter, flicker or lurch. Check this with a frame-difference scan.
- Shake only on a big hit. Snap zoom only on a sudden action, rarely.

## 5 · Sync

- Each beat is anchored to its **key word**, not to the first word of the sentence. The picture arrives about 6 frames
  before the word.
- A clip's action peak lands on its word.
- No image repeats within 60 s, unless it's a deliberate callback. No still holds over ~7 s.

## 6 · Focus effects (when the narration points at something)

| Effect | Use |
|---|---|
| Target push-in / motivated pan | the default camera language |
| Spotlight (dim + desaturate) | "this person / this object" in a busy scene |
| Colour isolation | rare, high-meaning moments |
| Character pulse (soft white tint, thin rim, sweep) | a name is said |
| Amber glow | other emphasis (objects, the brand) |
| Rack focus | attention moves between two people |
| **Shine sweep** | objects that matter (vials, a contract, a coin): use it a lot |
| **Hand-drawn ink circle / underline / arrow + handwritten note** | modern, on trend: use often, with the narrator's or host's voice |
| Loupe / magnifier | only when the source resolution holds up (no pixelation) |
| Ping | spotting small things ("find the glasses / find Matt") |
| Freeze-frame callout | a main character's first appearance |
| Glint | a hidden easter egg, timed during another highlight so it's easy to miss |

At most one highlight about every 20 s.

## 7 · Transitions (choosing them is part of the art)

| Kind | Use |
|---|---|
| Hard cut on action | within a scene, on movement (most cuts) |
| Smooth (filmic) dissolve | time passes in the same place |
| Dip to black / to parchment | a death, a chapter end, entering a document |
| Ink bleed | a scene change in an illustrated / painted style |
| Push-through (porthole / window / keyhole) | into a detail, inside a body, into a flashback |
| Match cut (planned pair) | linking two shapes, eras or people |
| Whip pan | energy, travel, "meanwhile" |
| Light leak | flash-forwards, memory |
| Passer-by / foreground wipe | a figure or object crosses the lens |
| Fog roll | a long time passing outdoors |
| Zoom-through | arrivals, the pace of the hook |
| **AI-style (v2):** morph, element-by-element / depth peel (the scene leaves layer by layer and the next one builds in), luma dissolve | showpiece moments, about 1–3 per video |

**A change of set is never a plain cut** (the beat builder enforces it): years passing → film dissolve, or a dip
when the mood is lowest; a few months → light dissolve; the same time in another place → ink bleed, or a whip when
the energy is high. Hard cuts stay inside a set, or are marked as deliberate ("cut!", e.g. cutting on an action that
carries across a doorway).

**No page turns.** They read as a jump and look cheap: a chapter card fades in softly (light dissolve) or hard-cuts.

**Same set, new subject, both wide or medium = a jump cut.** The background barely changes, so the subject seems to
pop in. Dissolve, change the shot size, or cover the beat with a different picture (the beat builder warns about it).

**Two shots of the same picture** (a callback, a frame that returns from a section) are joined by a dissolve or by
nothing, never by a dip or a chapter-style transition: those read as a glitch.

**Ambient light sits on its source.** A lamp glow goes on the lamp, dust motes and rays in the window light. A glow on
a person is a focus effect and must be planned in that beat's fx.

**The hook has its own sound.** Faster music than the story, cut off on the intro sting; the story's music starts
after the sting. Every cluster of fast cuts gets sound design: a riser into it, a whoosh and a hit on each cut.

**The hook never spoils the ending.** Flash-forwards tease the conflict (the shot, the refusal, the experiment, the
contract), never the death or the final twist.

Structure changes (hook → story, story → a myth / fact section, back to the story, the ending) get a **bigger** change:
a different look (frame or border, texture, colour), a change of rhythm and music, and a signature transition.

## 8 · Structure and rhythm

- **Hook (0–30 s):** the strangest true image and line in under 3 s, then who/when, then the twist, then a trailer of
  4–6 flash-forwards on music hits, then an open loop answered only at the end.
- **Re-hook** each chapter with a small open loop, and break the pattern every 45–60 s.
- **Mood curve:** cut pace, music (drops to silence, hits on key words) and narration delivery follow planned peaks
  and valleys.

## 9 · Review like a senior director and film editor

Before showing any cut, check:
- every named action is visible;
- every camera move hits its target;
- no edge-cropped subjects;
- no copies of faces;
- no placeholder text;
- no repeats;
- no long dead stills;
- cuts land on the key words;
- every transition's choice is justified;
- the hook grabs;
- every section change is unmistakable;
- the rhythm has peaks and valleys;
- motion is smooth (frame-difference scan);
- audio: music under the narration, SFX subtle, -14 LUFS;
- music covers every section (no cue shorter than its section; the render script refuses);
- every sound effect has its picture on the same frame (a stamp thud when the stamp lands, never from the notes alone);
- every mask follows its subject's outline (overlay sheet checked; a measured polygon when cut-out models fail);
- a name card that introduces one person in a group highlights that person;
- props on water sit in it (hull below the waterline, contact shadow, ripples, reflection, facing the way they move);
- a map zooms slowly onto the named place and highlights it; a route shows where it starts and where it ends;
- text over a bright picture has its own dark plate.

## 10 · Lessons loop

Every failure becomes a recorded lesson, plus a prompt block or edit rule, plus a lint or regression test, so it can't
repeat (example: `channels/storybook-medical/plan/prompt-lessons.md`).
