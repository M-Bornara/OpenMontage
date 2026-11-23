# HC002-L · motion budget v1 (2026-11-23, decided with Mahdi)

Why: rigid cut-out puppets fail when parts depend on each other (wheel on axle, rope on horse, driver on box, team of horses). Effort grows with dependencies, not shots. A long cannot carry that.

## Tiers
| Tier | What moves | Use in the long |
|---|---|---|
| A (default) | camera push/pan, 2-3 parallax layers, grade, light, particles, document draw-ons, hard cut or dissolve between two stills | nearly every shot |
| B | ONE free-standing sprite or overlay, ONE simple action, no attached parts (a head-turn swap, a stamp, a line drawing on, a letter sliding) | a few shots |
| C | full compositor (keys, sprites, sound) | max 1-2 hero moments; Shorts |
| D (AI clip) | image-to-video from OUR approved still, 4-6 s, for coupled or organic motion | max 3-5 in the long, wide or back-of-head shots only; test one first |


Never animate as sprites: wheels, horses or any animal, ropes/reins, crowds, hinged things (doors, lids, page stacks), anything attached to anything else. Show the cause or the result instead (dust plume, hoofbeat sound, push to a still hoof). 

Rules: (1) tier is set at storyboard time, per shot. (2) A shot that fails review twice drops one tier. (3) Anything with a coupling is Tier A or a still-cut. (4) New C needs Mahdi's yes and a cost.

## Row changes (from long-storyboard-v1)
| Row | Was | Now | Change |
|---|---|---|---|
| 49 coach + six horses | HERO layered | A, plus ONE optional test | Still of the coach on the road, parallax road/hills, dust layer, camera pan, hoofbeat + wheel sound. Test ONE image-to-video clip ($0.49, stated in storyboard) as an upgrade; if it flashes or the driver/horses/ropes come apart, keep the A version. No wheel, horse or rein sprites. |
| 65 evening coach | reuse 49 | A | grade of row 49's still |
| 2 glance | HERO reuse (sprites on plate) | B, as two-still cut | Still 1 men look up; hard cut to still 2 head turned, on "glances". No re-seating of S1 sprites. |
| 5 lies then lifts | HERO reuse (sprites) | B, as two-still cut | cut lie -> up on elbow on "talking"; dust layer. |
| 4 silhouette + bar | HERO reuse | C (keep) | the one approved hero moment; S1 v3 pieces on a new 16:9 plate. Pieces have no attached parts. Needs 16:9 re-measure (open item). |
| 54 case opens (lid sprite) | lid sprite | A | closed-case still, cut/dissolve to open-case still with a click. +1 still. |
| 46 stable doors swing | hinged doors | A | dissolve to the closed-doors still (wider). |
| 36 pages flip through stack | page hinges | A | 3 quick hard cuts of 3 book stills, each cruder, on the beat. |
| 38 slips flutter | many sprites | A | push in + dust only. |
| 39 stamps peel off | peel | B | fade out instead of peel. |
| 45 horse nods, brushed | animal | A | still + slow push + snort/hooves sound. |
| 48 flags/gulls | animated | A | slow pan; gulls in sound only. |
| 24-25 candle out, dawn | light | A | grade crossfade on one still, no relight sprites. |
| all other ALIVE rows | camera/grade/particles/draw-ons | unchanged (A or B) | 17 stamp/draw-on rows stay B. |

Result: C = 1 (row 4), B = a handful, everything else A. Row 49 gets one upgrade test. Cost: Claude Code recomputes the ledger estimate from this table before any spend.

## Tier D · AI image-to-video clips (Mahdi open to it, 2026-11-23)
Good for: wheels, horses, reins, water, smoke, fabric, crowds from behind. Targets in the long: row 49 (coach), 19 (ox cart), 45 (horse), 65 (evening coach), 48 (harbour), 26 (leaves).
**Default model (Mahdi, 2026-11-23): gemini-omni-1.2-flash via fal (live $0.0273/s, 720p; fal endpoint google/gemini-omni-flash/v1.2/image-to-video; tool gemini_omni_fal, model_version "v1.2"). Fallback: Kling v2.1 pro ($0.098/s). One take per model, then Tier A.** The Omni row in cost-ledger.csv (row49-coach-omni-v1, $0.14) is an ESTIMATE from the live rate, not fal's billed amount: true it up against fal's usage page. Omni has no audio-off option (the clip carries synthesized audio: mute it in the edit).

Rules: start frame = our approved still (style match); 4-6 s; wide or back views only, no faces in motion; cut away before drift; put our grain/grade over it so it matches the stills; max 2 takes per shot, then fall back to Tier A (two-round rule); cost said and approved first.
Pass checklist (row 49 test): six horses stay six; reins stay attached; wheels roll the right way; driver stays on the box and below the horses' line; no flashing or style drift; no new objects.
Open: platform disclosure rules for AI-generated video (YouTube, TikTok, Instagram, Facebook) must be looked up with sources before the long is uploaded.

## Tier D result · row 49 test (2026-11-23)
Start frame row49-coach-v2-flip.png (six horses, 3 pairs, flipped to lead right). Model: Kling v2.1 pro on fal, $0.49 (live fal price $0.098/s), one take, 5 s, 1920x1080, 24 fps.
Checks: six horses stay six YES; reins attached YES; driver stays on the box YES; no flashing (brightness step max 1.5) YES; no new objects YES; mild sky/sea drift (no style change); wheel direction: judged by Mahdi watching the clip: looks good.
Decision: row 49 upgrade accepted. Omni 1.2 Flash was then tested on the same frame ($0.14 est., 720p): six horses, reins, driver all held; Mahdi chose Omni as the default, Kling as the fallback. Clips are large (26.7 MB / 5 s): recompress before the edit.
