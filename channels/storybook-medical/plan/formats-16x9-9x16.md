# Sharing work between 16:9 (long) and 9:16 (Shorts)

Status: **proposal, to be tested on HC001 before adoption.** It replaces the earlier blanket
"`dual_format`: every keyframe generated twice".

## The problem
- A frame composed for 16:9 spreads sideways. A frame composed for 9:16 stacks vertically.
- Cropping one into the other usually gives a cramped, centred shot.
- Generating everything twice doubles image cost and doubles drift: the same moment looks slightly
  different in each format.

## What is shared for free (always)
- Research, fact logs, character sheets, location plates and the style anchor. These are made once per
  story universe.
- Maps, dates, documents, letters, contracts, counters and diagrams. These are built in Remotion as layouts,
  so they reflow to either format at no cost.
- The music library, the SFX library, the colour and caption system.

## Shots: four types, each with its own rule
| Type | Examples | Rule | Cost per shot |
|---|---|---|---|
| **1. Inserts & close-ups** | hands, objects, faces, the pocket watch, the iron bar, the contract | Generate **once at 1:1, 2K**. A 2048² square holds a full-quality 16:9 frame (2048×1152) **and** a full-quality 9:16 frame (1152×2048). Both formats are sharp, and neither looks cropped, because a close-up has no "sides" to lose. | $0.12 instead of 2 × $0.08 |
| **2. Wide master + vertical windows** | establishing shots, a room with two people, a street with a crowd | Generate **once at 16:9, 4K** (~5500×3070). Compose on **thirds, not the centre**: each subject must read on its own inside a vertical slice. The Short then uses **windows**: the left subject, the right subject (a shot/reverse-shot from one image), or a slow **pan** across the scene. A pan in a vertical video is a deliberate move, not an awkward crop. | $0.16 → 1 wide + 2–3 vertical shots |
| **3. Tall-only shots** | falling through ice, the iron flying upward, a figure against the sky, letters stacking up | **Native 9:16**, Short only. Height is the point of the shot, so the long video uses a different shot. | $0.08 |
| **4. Wide-only shots** | landscapes, maps of journeys, crowd panoramas for chapter openings | **Native 16:9**, long only (or a pan in the Short, as in type 2) | $0.08–0.16 |

**Video clips** (H3 or Kling, about $0.16–0.28 each) can't be cropped: a 16:9 clip cropped to 9:16 drops to
around 600 px wide. So clips are generated **once, in the format where that moment matters most**. The
other format uses the still with a camera move. A clip is generated in both formats only for the single key
action of a story (e.g. the string being pulled out).

## Composition rules for shared masters (go into prompts)
- "Wide cinematic composition; main subject on the left third, secondary on the right third; each subject
  complete and readable within a vertical strip; generous headroom; no key detail at the extreme left or
  right edge."
- Never place the only point of interest dead centre unless the shot is meant to be symmetrical.
- Review each master twice on the contact sheet: once as a 16:9 frame, once with its 9:16 windows drawn on.

## What this saves (HC001 example)
| | Every keyframe twice (old plan) | Shared plan |
|---|---|---|
| Long: ~50 shots | 50 × $0.16 = $8.00 | ~30 masters × $0.16 + ~20 inserts × $0.12 = $7.20 |
| 3 Shorts: ~60 shots | (already included above as duplicates) + ~60 more × $0.08 = $4.80 | ~35 come free as windows/inserts; ~25 tall-only × $0.08 = $2.00 |
| Rerolls (~20%) | ≈ $2.60 | ≈ $1.80 |
| **Images total** | **≈ $15.40** | **≈ $11.00** (≈ 30% less) |

The money saved is modest because images are already cheap. The bigger wins are:
1. **Consistency:** the same moment looks identical in the long video and the Short.
2. **Fewer images to review and reroll.**
3. **More shots per image** (reverse shots and punch-ins come from one master), which keeps Shorts fast
   without more generations.

## Optional: free local upscaling
The repo already has `tools/enhancement/upscale.py` (Real-ESRGAN, including an **anime/illustration
model**). It isn't installed yet. Installing it (free, runs on your NVIDIA GPU) would let us generate
masters at **2K ($0.12) instead of 4K ($0.16)** and upscale windows locally. The test below would show
whether that's good enough.

## Test before adopting (~$0.60, needs approval)
Two HC001 shots: the Beaumont + Alexis two-shot as a wide 4K master, and the pocket-watch insert as a 1:1 2K.
Render each as a 16:9 frame and as 9:16 windows (left, right, pan), next to the native 9:16 pilot frames.
You judge whether the windows look designed or cropped.
