# Production v3: length, motion without the AI look, and a storyboard that matches the final

Written 2026-11-04 from the user's notes after HC001. Applies from HCS01 Forssmann on. Older rules still hold
(memory: edit-review-rules-hc001, editing-standard-long, effects-on-exact-object).

## 1. Length

| Format | Target | Hard limit | Why |
|---|---|---|---|
| **Short** | **40–50 s** | 55 s | A Short is judged by "viewed vs swiped away" and % watched. Every second over 50 needs a reason. HC001 S2 (59.6 s) and S3 (57.3 s) ran long. |
| **Long video** | **8–10 min** | 12 min | 8:00+ allows mid-roll ads once monetized. Longer only if the story truly has more turns; never padding. |

- **Monetization route:** YouTube Partner Program needs 1,000 subscribers + **4,000 public watch hours from long
  videos** in 12 months, *or* 10 M Shorts views in 90 days. Shorts views don't count as watch hours, so the long
  videos carry the watch-hour route and the Shorts bring the subscribers.
- **Watch hours = views × minutes watched.** A 9-minute video watched 40% = 3.6 min per view. A 15-minute video
  watched 20% gives less and tells YouTube viewers left. Length helps only while retention holds.
- **SEO:** length is not a ranking factor; satisfaction and watch time are.
- **How we keep a long video from feeling long:**
  - The hook sets one question in the first 30 s, and every chapter must move it forward.
  - Cut any line that repeats what the picture already shows or what was said before.
  - A turn (new fact, reversal, reveal) at least every 60–90 s.
  - The script's reading length is checked *before* narration: about 2.4 words per second after the speed-up.
- **Fresh eyes:** you have watched HC001 too often to judge its pace. From now on, YouTube Studio's
  retention graph judges it: on Nov 15 we'll see exactly where viewers left and cut the same kind of moment in HC002.

## 2. Motion: what makes each shot move

Every shot in the storyboard names its motion method, cheapest and most controllable first:

| Code | Method | Cost | Control |
|---|---|---|---|
| **CAM** | Camera move on the still (push, pan, tilt, rack to the subject) | free | full |
| **FX** | Our effects on measured masks: highlight one person, depth blur, a cut-out part that swings or slides (keys, a letter, a hand), glow, stamp, line drawing itself, colour fade | free | full |
| **ACT** | Layered animation (plan/layered-animation.md, user 2026-11-16): character and prop animation on the still: cut-out layers of the figure and props, animated in Remotion — breathing, trembling hands, a blink, a head turn, a shudder, sweat running; flame flicker, liquid slosh, a swinging door, a needle sliding. The face/body of the still already shows the exact feeling; ACT makes it live. **Every shot goes through the `layered-shot` skill** (`.claude/skills/layered-shot/SKILL.md`): layer plan → sheet / plate prompts (approval) → cut-outs → keyframes → 3 s preview → approval. `episode.py build` fails a CAM-only story shot unless it is marked `breath` | free (pieces ~$0.07 each) | full |
| **2.5D** | Depth parallax: a depth map of the painting turns it into layers, so a camera move shows real depth (foreground slides past the background) | free (local depth model) | full |
| **3D** | Three.js inside the same Remotion render (diagrams, a rotating object, a route through a body) | free | full |
| **CLIP** | AI video clip (Kling, image-to-video, start frame + end frame) | $0.28–0.49 each try | partial |

**AI clip rules** (a clip is the last choice, not the default):
1. Only when the motion *is* the story beat and CAM/FX/2.5D/3D can't tell it.
2. Only simple motion: one subject, one action, a clear destination. No hands handling objects, no talking
   faces, no crowds, nothing moving by itself.
3. A written clip spec before spending: start frame, end frame (when used), the one action, camera, what must
   NOT happen. You approve each spec.
4. Decided **after** the rough cut (§3), when we can see the still already doesn't work.
5. **One retry at most.** If the second try fails, the shot stays a still with CAM/FX.
6. Budget: a Short 0–2 clips, a long video at most ~6.

## 3. The storyboard: from a sketch to a rough cut

HC001's animatic was text cards over simple shapes, so it didn't show what the video would be. Images are cheap
($0.15) and only clips are expensive, so the new order makes the storyboard almost the final film:

0. **Period research (free; user, 2026-11-14).** Before the storyboard: real portraits of every main character and
   period images of each set, costume, prop and script (Wikimedia Commons, Wellcome, museums; licence noted), saved to
   `projects/<id>/refs/` and listed in `editorial/episodes/<ID>/references.md`. No portrait from the lifetime: follow the
   image the audience's culture knows. Check every set for anachronisms; show disputed events in a way that fits every
   account. The real photos become the likeness references for the cast sheets.
0b. **Approval page (user, 2026-11-14: "keep this setting to get the approval before generation").** Every episode has
   one claude.ai Artifact page, built by `scripts/storyboard_page.py`: per shot the pre-viz sketch, narration line and
   shot design; the real references beside the cast; later the image prompts and the images. The user approves each
   gate on it (storyboard + pre-viz → prompts → images) by shot number. Nothing is generated between gates.
1. **Storyboard sheet (free).** Decoupage first (L28, user review 2026-11-06): every shot is a designed shot with
   its **size** (ELS/LS/MS/MCU/CU/ECU/insert/OTS), **angle**, **lens**, the **action of its own line** and the
   **emotion on the faces**. Since 2026-11-16 (story-craft.md Rule 0): every shot is written as a director's
   breakdown: the moment, the action in progress (a verb), the feeling and how face and body show it, the camera
   move that delivers it, the ACT animation of character and props, the sound. A shot whose only motion is CAM
   (zoom/pan) is refused by review unless it is a deliberate breath between beats. Every shot also names its **level**
   (HERO / ALIVE / BREATH, plan/layered-animation.md §7) and its tricks; HERO shots get a free motion pre-viz on stand-ins. One image per idea in the narration. A set that comes back changes size and angle
   (long → medium → close, reverse angle), or the line gets its own place and light. The prompts then use
   `framing()`, and the lint stops a SHOT-less frame or the same set at the same size twice in a row. Every shot: the narration line and its key word, what we see (composition, who
   is where, what the eye should land on), the motion code and exactly what moves, on-screen text and *where*
   it sits (never on a face), SFX tied to a visible action, and the target length. You approve it.
2. **Image prompts** (lint + prompt_kit), then you approve them.
3. **Images** (~$0.15 each), then you approve them, with regenerations as needed.
4. **Narration** with the new voice (~$0.10 for a Short).
5. **Rough cut = the storyboard video:** the real images, real narration, real camera moves, FX, 3D, captions,
   stamps and music, rendered by the same Remotion compositions as the final. Clip candidates play as stills
   with a "CLIP?" label. **You review this, not a sketch.**
6. **Clip decisions:** only the shots that still feel dead get a clip spec (§2). Then the final.

## 4. 3D: where Three.js and Blender help

**No new renderer is needed.** Remotion stays: `@remotion/three` puts a Three.js scene inside the same
composition, frame-exact, with the same captions, SFX and camera system. Blender (installed:
`.runtime/blender/blender-4.5.10`) is for the rare shot Three.js can't make well; it renders a PNG sequence that
Remotion plays as a layer.

The look must stay storybook: flat/toon shading, an ink outline, our palette and a paper-grain overlay, so a 3D
element reads as part of the painting and never as a video game.

| Use | Example | Tool |
|---|---|---|
| **2.5D parallax** on our paintings | the Forssmann corridor: a slow pull back where the walls slide past (replaces a "walking" AI clip) | depth map + Three.js mesh |
| **Inside-the-body routes** | the catheter line travelling elbow → shoulder → heart; Gage's rod path through the skull | Three.js line + toon anatomy |
| **Objects that turn** | the 1956 medal, Beaumont's watch, a vial | Three.js (textured with our own painted image) |
| **Maps and globes** | routes across a turning globe (Persia → Europe for Avicenna's book) | Three.js |
| **Hero physical shots** (rare) | liquid in a glass, cloth, smoke | Blender |

**First test (free):** the Forssmann catheter route and the medal, before any other 3D use is planned.
