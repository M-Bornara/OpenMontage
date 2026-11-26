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

## Tier D results, rows 19 and 45 (2026-11-23, Omni 1.2 Flash, ~$0.137 each, estimates)
Row 19 ox cart: PASS (counts, yoke, no flashing, no new objects); cart travels ~4% of the frame width in 5 s, camera locked; wheel direction to be judged by eye. Row 45 stable: FAIL on "no new objects" (breath drawn as white scratch marks), caused by our motion text. Retake with minimal motion text (L73) once, same model.
Row 45 retake (minimal text, no breath, ~$0.137 est., 5 s, 720p): FAIL again. Nostrils and mouth are clean (no scribbles), horse nods once, but from about 0.8 s to 1.3 s a SECOND brush appears in his other hand (the rope hand), the lead rope hangs free for a moment, then the rope is back in his hand. Fails "no new objects", "brush stays in his hand" and "rope attached". Decision (Mahdi): no more retakes; row 45 goes to Tier A (still + slow push + snort/hooves sound). Two takes spent, ~$0.27 + 2 stills $0.13.

## Tier D results, rows 48 and 26 (2026-11-24, Omni 1.2 Flash, ~$0.137 each, estimates) and the FINAL TALLY (Mahdi, 2026-11-25)
Row 48 harbour (prompt: "Ships sway gently and the water ripples. Locked camera. No cuts."): FAIL on "no new objects": the model added about seven seagulls that are in neither the still nor the prompt (the empty sky is filled). Ships, coaches, houses held; camera locked; no flashing (max brightness step 0.26).
Row 26 farmhouse (prompt: "Gage walks slowly forward a few steps. Locked camera. No cuts."): FAIL on style drift and new objects: Gage's face was REDRAWN as he walked toward the camera (a squint at the start, both eyes wide open at the end, more shading), which breaks the shut-left-eye rule, and a few leaves drifted down that were not moving in the still. Counts, hands, props and the locked camera held; no flashing (max step 0.29).
**Final Tier D tally (decided with Mahdi, 2026-11-25):**
| Row | Result | Used as |
|---|---|---|
| 49 coach | Kling v2.1 pro PASS (Omni 1.2 also held) | the clip (Kling, 5 s) |
| 19 ox cart | Omni 1.2 Flash PASS | the clip (frame-blended to 30 fps) |
| 45 stable | FAIL twice (breath scratches; a second brush) | Tier A: still + slow push + hooves and a snort in the sound |
| 48 harbour | FAIL (gulls added) | Tier A: still + slow pan + gulls and flags in the SOUND only |
| 26 farmhouse | FAIL (face redrawn, leaves) | Tier A: still + slow push + wind in the sound |
| 65 evening coach | not generated | a free evening GRADE of the row-49 clip (a wider crop) |
Causes, for the rule: wide shots with a locked sky and no moving faces are the safe Tier D candidates (rows 49, 19). An empty sky gets gulls; a face that walks toward the camera is re-rendered; a hand with a tool gets a second tool. No Tier D clip in the long is ever used unchecked; the failed clips are kept on disk and not used. Total Tier D spend on the long: about $1.33 (Kling $0.49 + six Omni takes at ~$0.14 = $0.84, the Omni figures are estimates).
