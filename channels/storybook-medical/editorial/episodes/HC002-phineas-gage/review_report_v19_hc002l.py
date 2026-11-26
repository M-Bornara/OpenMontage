"""HC002-L review of preview v19 (Mahdi 2026-11-25) -> projects/hc002-l/review/v19_report.json, shown first on the approval page (storyboard_page.review_block).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/review_report_v19_hc002l.py      (from the repo root)"""
import json
from pathlib import Path

B = "E:/Projects/OpenMontage/projects/"
R = B + "hc002-l/review/"
F = B + "fx-demo/renders/"
clip_map = json.load(open("projects/hc002-l/review/clip_map.json", encoding="utf-8"))

sections = [
    {"heading": "Not run: the generation in the pasted block",
     "paras": ["Your message says 'No spend in this prompt' and 'HOLD: any generation'; the pasted block inside it approves $1.25 for four Omni clips and four stills. I followed your own words: NOTHING was generated and nothing was spent. The four clip slots are built and waiting (item 8), the prompts and prices are below, and the whole thing runs the moment you say go."]},

    {"heading": "1 · Quote-card highlight: the marker is now the full line height (2x crop, viewed)",
     "paras": ["CAUSE: the quote card's marker (the 'iron will' phrase) was `linear-gradient(transparent 55%, amber 55%)` on an inline span, which paints only the LOWER 45% of the text. Last round I fixed the caption marker but never touched the card, so it stayed half height. FIX: the marker is now a solid amber box, an inline-block at the card text's own line height (1.35 x 54 px) with a little padding, in StorybookLong.tsx.",
              "CHECK (the crop below is a 2x render, 3840 x 2160, of the real frame at 48.9 s, viewed): the box runs from above the dots and ascenders of 'iron will' to below the baseline. Measured: marker 155 px tall against a 146 px line and 97 px of glyph ink, covering the ink at both ends. The caption marker at the bottom of the same frame (the word 'AS') is full height too. File: E:\\Projects\\OpenMontage\\projects\\hc002-l\\review\\highlight_check\\quote_card_2x.png",
              "REGRESSION: scripts/highlight_check.py renders this frame at 2x on every long render, measures the marker and fails the render if it does not cover the full text height; test_highlight_check.py proves it flags the OLD half-height strip (negative control) and passes the new one."],
     "images": [{"src": R + "highlight_check/quote_card_2x.png", "label": "2x crop of the quote card: the marker behind 'iron will' now covers the full line height", "edge": 1700},
                {"src": R + "highlight_check/frame_small.jpg", "label": "The whole frame (marker on the card, caption marker below)", "edge": 1500}]},

    {"heading": "2 · Existing-clip map: every shot, its picture, and any clip of the same scene",
     "paras": ["93 shots. CLIPS IN THE CUT, all at natural speed and length: row 19 ox cart (Omni), row 49 coach (Kling), row 65 (a graded crop of the Kling clip), C2 blast, and the C2 footage again under the HIT layers.",
              "WHERE A CLIP OF THE SAME SCENE EXISTS BUT IS NOT USED (all three flagged or close to your two times; each failed its check in the Tier D tests and was kept on disk, as decided with you on 2026-11-25): ~2:09 = row 26 farmhouse: row26-farmhouse-omni-v1 (5.0 s), FAIL, his face is redrawn as he walks toward the camera (it breaks the shut-eye rule) and leaves are added. ~3:45 = row 45 stable: row45-stable-omni-v1, FAIL, white breath scribbles about 2-3.5 s; row45-stable-omni-v2, FAIL, a second brush appears 0.5-1.3 s. Row 48 harbour (3:57): row48-harbour-omni-v1, FAIL, about seven gulls added to the sky. The frames are below.",
              "WHICH DO NOT MATCH AT ALL: the HC002-S1 Short layered clips (s01 to s13) are all 9:16 (1080 x 1920) with their captions burned in, so they cannot stand in for the 16:9 stills of rows 10, 16 and 22 (their scenes). The row-49 Omni clip also passes and is held as the alternate.",
              "MY PROPOSAL: keep the stills for rows 26 and 45 unless YOU accept the flaws. If you want movement at ~3:45, row45-stable-omni-v1 is the best candidate: the first ~1.8 s is clean (the man brushes, the horse stands); the scribbles come at ~2-3.5 s. If you want it, I use the clip at natural speed and cut to the still at 1.8 s. For row 26 I would not use it: the face redraw breaks a hard rule. Nothing was changed in the cut for these: your call.",
              "Full table below (also projects/hc002-l/review/clip_map.csv)."],
     "images": [{"src": R + "clipmap/failed_clips_sheet.jpg", "label": "The flagged clips, frames at 0 / 1.5 / 3 / 4.9 s. Rows: row 26 farmhouse, row 45 v1, row 45 v2 (0 / 0.8 / 1.1 / 4.9 s), row 48 harbour", "edge": 1900},
                {"src": R + "clipmap/s1_previews_sheet.jpg", "label": "The HC002-S1 Short layered clips: 9:16 with burned-in captions (s02, s05, s09, s11, s01, s13)", "edge": 1900}],
     "table": clip_map},

    {"heading": "3 · ~1:20: row 16, still S1 s5 (the empty rock plate)",
     "paras": ["Row 16 (1:18.6 to 1:24.9), shot r16, picture S1 s5 = HC002-S1's shot 5, the empty rock cut with the drill hole (16:9 copy keyframes16x9/s5.png), a push from 1.30 to 1.55, a small hit at 2.2 s and the quote card 'struck fire upon the rock'. At 1:20 the narration is 'He looked over his shoulder. The iron came down...': the picture has no man and no iron in it. The frame is in the first image below (left, top row).",
              "FREE PROPOSAL (not applied, you said no regeneration yet): the new cold-open pieces fit this line. 'He looked over his shoulder' = the row-2 glance still in a different crop; 'The iron came down and struck fire upon the rock' = the tip still in the tight Tier A crop with the spark (the stand-in the cold open already uses), a small hit on 'struck'. It repeats the cold open's pictures at different crops (a callback); say yes and I put it in."],
     "images": [{"src": R + "clipmap/flagged_frames.jpg", "label": "Preview v19 at 1:20 (r16), 1:34 (r18), 2:09 (r26), 3:45 (r45), 5:41 (r65d) and 5:42.5 (r66a)", "edge": 1900}]},

    {"heading": "4 · ~1:34 'he spoke': the long shot is shortened, then the dazed soot still (done)",
     "paras": ["Row 18 now holds the lying/elbow still 3.3 s (1:31.9 to 1:35.2) and cuts to the row-5 dazed still with the blood painted to soot at 1:35.2, on 'spoke', and holds it to row 19 (1.6 s). Frame below."],
     "images": [{"src": R + "hitcheck/r18b.png", "label": "r18b at 1:35.6, 'he spoke'", "edge": 1500}]},

    {"heading": "5 · ~5:41: rows 65 and 66; the face is back, the horse-leg still has a free proposal",
     "paras": ["WHICH ROWS: row 65 (5:35.6 to 5:41.2, 'Macmillan argues...', the graded crop of the Kling clip for its natural 5.07 s, then r65d, a 0.5 s tight still of the horses' legs) and row 66 (from 5:41.2, 'The man in those photographs isn't a monster', r66a). The v19 r66a was a 2.1x crop on the portrait's HAND, which cut his face off.",
              "DONE: r66a is now the framed portrait WITH his face (a 1.7x to 1.8x crop centred on the face and shoulders; row 67's wide shot of the same still is 1.0x to 1.12x, so they do not repeat). Frame below.",
              "THE HORSE-LEG STILL (r65d, 0.5 s) IS ONLY A FILLER between the clip's end and the voice. FREE OPTION (proposed, not applied): drop r65d and dissolve from the coach clip straight into the portrait at 5:40.7, half a second before the voice starts, the dissolve the script already asks for ('the portrait and the coach driver dissolve into each other'). Alternatives: a tight crop of the driver from the row-49 clip's first frame (free), or the same dissolve but ending on the reins still (row 50). I recommend the dissolve."],
     "images": [{"src": R + "hitcheck/r66a.png", "label": "r66a at 5:42.4: the framed portrait with his face", "edge": 1500}]},

    {"heading": "6 and 7 · The HIT shot (free), and the three callbacks are now it; C3 is retired",
     "paras": ["BUILD: base = the C2 explosion clip at NATURAL speed from 0.45 s (never slowed), in a 2.2x crop on the ledge. On top: an impact frame (3 frames), an orange-ink comic burst with an ink splash that FOLLOWS the man's head the whole time (he sinks down and left as the blast throws him: I tracked him off a gridded sheet of the footage), and the rigid iron SPRITE rising out of the head. Sprite and burst run on a remapped clock at 40% for 0.5 s (the footage under them does not); shake, whoosh, boom and thud. 1.3 s; in the callbacks 0.2 s of Gage down follows, 1.5 s in all; in the cold open the next shot IS Gage down (C4).",
              "THE SPRITE: you named iron-ref.png, but that file is a noisy, low-resolution crop of the real iron photograph with no clean edge to cut. I cut the sprite from the approved 1:34 iron of row 13 (row13-iron-v3redraw.png: thickness = length / 34, the last quarter tapering to a point), by the rod's own geometry, antialiased, never redrawn: the same rod the viewer saw in row 13. It is drawn about 4x life size next to the figure so that it reads (at true size it would be 90 px).",
              "RULE 0b: the bar is never shown inside a head: the burst covers the head and jaw the whole time, the bar is visible only below the jaw and above the burst. For the headroom (the man stands at the top edge of the footage) the footage is shifted down 14% and a sky layer above it takes the footage's own top-edge colour.",
              "ROUGH SPOTS: the sky extension is a soft flat band at the top; the splash is flat orange (it does not change with the halftone grade, which is deliberate: the grade shows on the picture, the burst is the accent); the sprite is enlarged.",
              "CALLBACKS: row 17 at 1:30.4 (amber, ending on row 18), row 40 at 3:18.0 (cyan-magenta, in the pause before 'did Phineas Gage really...'), row 67 at 5:48.6 (mono). Each is 1.5 s: the HIT then 0.2 s of Gage down, then the row's picture. The cold open uses the HIT where C3 was (14.30 s). C3 is no longer in the cut."],
     "videos": [{"src": F + "hit-cold-open.mp4", "label": "The HIT shot as in the cold open (1.3 s, no grade)"},
                {"src": F + "hit-callback-amber.mp4", "label": "Callback, row 17: amber (1.5 s with Gage down)"},
                {"src": F + "hit-callback-cyan_magenta.mp4", "label": "Callback, row 40: cyan-magenta"},
                {"src": F + "hit-callback-mono.mp4", "label": "Callback, row 67: mono"}],
     "images": [{"src": F + "hit_final_sheet.jpg", "label": "The HIT shot, frames from 0 to 1.28 s: impact frame, burst on the head, the bar rising out of it, the burst fading", "edge": 1900},
                {"src": R + "hitcheck/sheet.jpg", "label": "In the real long (single frames, no render): cold open x3, bar close-up with glint, then callbacks 17 / 40 / 67, 'he spoke', the portrait", "edge": 1900}]},

    {"heading": "8 · The cold open is ready for four Omni clips (not generated)",
     "paras": ["Slots, built into the edit (each is a clip if its file exists, otherwise the still stand-in shown now): pour 0-3.0 s | tamp 3.0-5.95 s | the bar close-up 5.95-7.2 s (always a still: slow push and a glint on the bar, built) | glance 7.2-9.8 s | spark 9.82-11.76 s. A clip plays from its first frame at natural speed and is TRIMMED to its slot, never stretched, sped up or frozen (the build refuses a clip shorter than its slot). Then C2 blast at 11.76 s, the HIT at 14.30 s, C4 (Gage down) at 15.6 s, the dazed soot still at 20.0 s.",
              "WHEN YOU SAY GO (not run): four Omni 1.2 Flash clips, 720p, 3 s, one take each = 12 s x $0.0819 = $0.983 (fal's page, 720p; 360p would be $0.33). One-line motion texts (L73), background named (L55), nothing else: POUR (start frame cold-r1-pour): 'Flat grey layered schist rock. A gloved hand tips a small iron flask and a thin stream of black powder runs into the drill hole. Locked camera.' TAMP (cold-b1-tip): 'Flat grey layered schist rock. The iron bar's pointed tip presses into the drill hole and rests. Locked camera.' GLANCE (row-2 glance still): 'Autumn hills and a grey rock wall. The man turns his head to look over his shoulder. Locked camera.' SPARK: 'Flat grey layered schist rock. The iron's tip scrapes the rock and one spark jumps. Locked camera.' I would start the spark clip from cold-b1-tip, not cold-b2-ledge or cold-b3-rod: those two show no bar striking stone, so a strike would have to be invented. Four more stills (1:42 sitting up, 4:06 carriage, two angry Gage variants) at about $0.067 each = $0.268; total $1.25, the figure in the pasted block.",
              "RISKS I KNOW FROM THE TIER D TESTS: a hand with a tool gets a second tool (the pour clip), a face that moves is redrawn (the glance clip), an empty sky gets extras. Any failed first take: I stop and report; a retake needs your yes and a cost."]},

    {"heading": "9 · Checks",
     "paras": ["Build (no render): background check 0 similar pairs, L52 jump-cut check 0, no clip would freeze, the four background regression tests pass; the highlight regression passes on the real frame and flags the old half-height marker on the synthetic one.",
              "CUT AUDIT: NOT RUN. It measures the rendered file, and you said not to re-render until the clips exist. The preview below is still the v19 render and shows none of today's changes (the HIT, row 18, the face portrait, the callbacks): the in-context frames above are single-frame renders. The audit runs on the next render."]},
]
json.dump({"title": "REVIEW OF PREVIEW v19 · done, proposed, and what is waiting (waiting for your OK)",
           "legend": "Nothing generated and nothing spent in this round. The preview video further down is STILL the v19 render: it does not include the changes listed here. Next render: after the four clips exist (or on your word).",
           "sections": sections}, open("projects/hc002-l/review/v19_report.json", "w", encoding="utf-8"), indent=1)
print("v19_report.json", len(sections), "sections")
