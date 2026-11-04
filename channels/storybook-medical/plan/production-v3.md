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

1. **Storyboard sheet (free).** Every shot: the narration line and its key word, what we see (composition, who
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
