"""Visual storyboard page (user, 2026-11-14: "I cannot see the formatted md file ... more visuals before generation").

Reads each episode's storyboard .md (script block, shot table, sets/cast table, cost), puts the free pre-viz frame next
to every shot and the reference photos (portraits, period places) next to the cast, and writes one HTML page plus an
img/ folder, ready to publish as an Artifact. Run from the repo root:

    python channels/storybook-medical/scripts/storyboard_page.py <out_dir> <episode-key> [<episode-key> ...]

Episode keys are in EPISODES below; add a new episode there (storyboard, previz dir, refs with credits).
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

import storyboard_lint

REPO = Path(__file__).resolve().parents[3]
EP = REPO / "channels/storybook-medical/editorial/episodes"

EPISODES = {
    "hcs07": {
        "lint_0b": "warn",   # storyboard approved before Rule 0b (2026-11-19)
        "anchor": "finlay", "short": "Finlay", "slot": "Thu Dec 3 · 15:00 ET = 14:00 Alberta",
        "storyboard": EP / "HCS07-finlay/storyboard-v2.md", "story": EP / "HCS07-finlay/story-v2.md", "project": REPO / "projects/hcs07-finlay",
        "previz": REPO / "projects/hcs07-finlay/review/previz", "maps": ["map-academy.png"],
        "refs_dir": REPO / "projects/hcs07-finlay/refs",
        "refs": [
            ("finlay.jpg", "Carlos Finlay", "Moustache into side whiskers, shaved chin, round spectacles.", "Photo, c. 1900s · Wikimedia Commons · public domain"),
            ("reed.jpg", "Walter Reed", "Moustache, dark-blue US Army uniform with shoulder cords.", "Photo, 1890s · Wikimedia Commons · public domain"),
            ("lazear.jpg", "Jesse Lazear", "Full trimmed beard, centre-parted hair.", "Photo, before 1900 · Wikimedia Commons · public domain"),
            ("havana_harbor_1860.jpg", "Havana harbour", "Morro Castle and lighthouse, busy harbour (shot 2a).", "Photo, c. 1860 · Wikimedia Commons · public domain"),
            ("havana_street_1880s.jpg", "A Havana house front", "Lime plaster, iron window grille (shot 2b).", "Photo, 1870s–80s · Wikimedia Commons · public domain"),
            ("academy_building.jpg", "The Academy building today", "Stone and scale only; the street front is a later remodel.", "Photo, 2026 · Wikimedia Commons · CC BY-SA 4.0"),
        ],
    },
    "hcs05": {
        "lint_0b": "warn",   # storyboard approved before Rule 0b (2026-11-19)
        "anchor": "al-razi", "short": "al-Razi", "slot": "Mon Dec 7 · 15:00 ET = 14:00 Alberta",
        "storyboard": EP / "HCS05-al-razi/storyboard-v2.md", "story": EP / "HCS05-al-razi/story-v2.md", "project": REPO / "projects/hcs05-al-razi",
        "previz": REPO / "projects/hcs05-al-razi/review/previz", "maps": ["map-ward.png"],
        "refs_dir": REPO / "projects/hcs05-al-razi/refs",
        "refs": [
            ("razi_1956.jpg", "Al-Razi, the look we follow", "White turban, full black beard, sand robe with a gold collar over a blue tunic.", "Painting for the 5th Iranian Medical Congress, 1956 · Wellcome Collection S0001954 · CC BY 4.0"),
            ("razi_behzad.jpg", "Al-Razi by Hossein Behzad", "For comparison only: old, white beard, an alchemist's flask.", "Miniature, 20th c. · Wikimedia Commons · public domain"),
            ("samanid_mausoleum.jpg", "Brick of his century", "Patterned baked brick and a plain dome: Rey and the ward.", "Samanid Mausoleum, Bukhara, c. 914–943 · Wikimedia Commons · public domain"),
            ("nain_stucco.jpg", "Carved stucco", "Wall decoration for the ward.", "Jameh Mosque of Nain, 10th c. · Wikimedia Commons · CC BY-SA 2.0"),
            ("quran_folio_950.jpg", "Handwriting of his time", "Angular cursive on paper: the look of his notebook pages (shot 7a).", "Quran folio, 950–1000 · The Met via Wikimedia Commons · public domain"),
        ],
    },
    "hcs10": {
        "anchor": "pettenkofer", "short": "Pettenkofer", "slot": "CASE 12 · Tue Dec 1 · 15:00 ET = 14:00 Alberta · ready by Fri Nov 27",
        "storyboard": EP / "HCS10-pettenkofer/storyboard-v1.md",   # story-v1 is approved; the v2-revision block does not apply
        "project": REPO / "projects/hcs10-pettenkofer", "previz": REPO / "projects/hcs10-pettenkofer/review/previz",
        "maps": ["map-lab.png"], "refs_dir": REPO / "projects/hcs10-pettenkofer/refs",
        "refs": [
            ("pettenkofer_lenbach_1890s.png", "Max von Pettenkofer, 1890s (Lenbach)", "The portrait nearest 1892: white hair brushed back, full white beard. The face we follow.", "Franz von Lenbach, 1890s · Wikimedia Commons · public domain"),
            ("pettenkofer_c1898.jpg", "Pettenkofer, c. 1898", "A photo six years later: hair, whiskers, the old sunken face.", "Photo, c. 1898 · Wikimedia Commons · public domain"),
            ("pettenkofer_1883.jpg", "Pettenkofer, 1883", "Nine years earlier, for comparison.", "Popular Science Monthly vol. 23, 1883 · Wikimedia Commons · public domain"),
            ("koch_1890.jpg", "Robert Koch, December 1890", "Dark full beard, receding hairline, rimless spectacles (shot 3a).", "Engraving, Uusi Kuvalehti, 1 Dec 1890 · Wikimedia Commons · public domain"),
            ("hamburg_water_1892.jpg", "Hamburg 1892: the emergency water supply", "Water carts and queues in the epidemic (shot 2).", "Pincerno, 1892 · Wikimedia Commons · public domain"),
            ("hamburg_disinfection_1892.gif", "Hamburg 1892: disinfection squad", "Period street, clothes and carts (shot 2).", "1892 · Wikimedia Commons · public domain"),
            ("meyers_cholera_bacilli_1885.png", "Cholera culture in gelatin, Meyers lexicon c. 1885", "Shot 8 uses only the LEFT tube (Koch's cholera bacillus, day 2); the middle and right tubes are other germs.", "Meyers Konversations-Lexikon, 4th ed., c. 1885 · Wikimedia Commons · public domain"),
        ],
        "extra": [EP / "HCS10-pettenkofer/backgrounds-v1.md"],
        "hero_previz": [("1", "Shot 1 · the hook: his hand brings the small glass to his lips; the student's hand reaches in and stops short on \"drink\""),
                        ("4", "Shot 4 · the refusal: MS, push in 1.0 → 1.18; ONE swap to the raised palm on \"no\"; rack focus; Matt's glint"),
                        ("6", "Shot 6 · the gulp: the small glass at his lips; ONE swap, head back, on \"gulp\"; the window swells on \"purest water\""),
                        ("7", "Shot 7 · the cramps: ≈ 30 cm of desk; flat hand on a sheet → ONE swap: the fingers clutch and crumple it on \"cramps\" (your fix); the colour drains")],
        "hero_real": [("1", "Shot 1 · NEW plate (v2): his head lower, the hook card clears his hair and forehead (hair top 0.36, card 0.19–0.32); the glass reaches his lip on \"drink\", the student's hand reaches in and stops short (0.38 of the frame). Free fix: the paper edge at the bottom right painted out"),
                      ("4", "Shot 4 · NEW plate (v2): a true over-the-shoulder, two backs big in the lower corners, Matt small at the back right (0.19 of the height, ? glint after \"no\"); no crop needed: the palm comes up on \"no\" at 0.51 of the frame"),
                      ("6", "Shot 6 · unchanged (approved): head back on \"gulp\", the window brightens on \"purest water\" (0.86 of the frame)"),
                      ("7", "Shot 7 · NEW sheet (v2): the sheet stays full size and spread; on \"cramps\" the fingers clutch, creases only under them, the sleeve does not move; crumple sound; colour drains. Free fix: the faint lines on the flat sheet faded (the clutched one is blank)")],
        "hero_pieces": REPO / "projects/hcs10-pettenkofer/review/hero/pieces.jpg",
        "page_title": "Pettenkofer Storyboard",
        "status": "package re-checked by the fact gate (41 PASS): title is now 'The Professor Who Drank Cholera at 73', 12 caption/description fixes (HCS10 $1.64) · waiting for your OK, then you upload Tue Dec 1",
    },
    "hc003s1": {
        "anchor": "dancing-s1", "short": "Dancing S1", "slot": "CASE 14 · Sat Dec 5 · 15:00 ET = 14:00 Alberta · ready by Tue Dec 1",
        "storyboard": EP / "HC003-dancing-plague/s1-storyboard-v1.md",   # s1-story-v3 approved 2026-11-21
        "project": REPO / "projects/hc003-s1", "previz": REPO / "projects/hc003-s1/review/previz",
        "maps": ["map-lane.png"], "refs_dir": REPO / "projects/hc003-s1/refs",
        "refs": [
            ("hondius_dancing_pilgrims_1642.jpg", "The dancing pilgrims (Hondius 1642, after Bruegel 1564)", "The image people know of the dancing mania: how the dancers move, the helpers holding them.", "Engraving, 1642 · Wikimedia Commons · public domain"),
            ("durer_nuremberg_woman_dance_1500.jpg", "Nuremberg woman dressed for a dance (Dürer 1500)", "Gown, coif and shoes of the period: Troffea's sheet.", "Watercolour, 1500, Albertina · Wikimedia Commons · public domain"),
            ("durer_dancing_peasants_1514.jpg", "The dancing peasant couple (Dürer 1514)", "A dance pose and dress of 1514.", "Engraving, 1514 · Wikimedia Commons · public domain"),
            ("gersdorff_feldbuch_1517.jpg", "Gersdorff, Feldbuch der Wundarznei (Strasbourg 1517)", "A Strasbourg medical book of the year before: shot 12a.", "Woodcut, 1517 · Wikimedia Commons · public domain"),
            ("merian_strasbourg_1644.jpg", "Strasbourg (Merian 1644)", "The city and the cathedral spire over the roofs.", "Engraving, 1644 · Wikimedia Commons · public domain"),
            ("strasbourg_kammerzell.jpg", "Maison Kammerzell, Strasbourg", "Half-timbered fronts with overhanging storeys: the lane.", "Photo · Wikimedia Commons"),
        ],
        "extra": [EP / "HC003-dancing-plague/s1-refs.md", EP / "HC003-dancing-plague/s1-backgrounds-v1.md",
                  EP / "HC003-dancing-plague/fact-gate/2026-11-21-script-s1-v3.md"],
        "page_title": "Dancing Plague S1 Storyboard",
        "status": "HERO shots on real art (11 pieces, $0.74) · waiting for your OK, then the story stills",
        "hero_pieces": REPO / "projects/hc003-s1/review/hero/pieces.jpg",
        "hero_real": [
            ("1", "Shot 1 · the hook (frame 1): Troffea mid-turn in the lane from frame 0, the shutter swings open above, the camera pushes in; ONE swap to the other turn on \"dance\"; hook card A in the bottom band (0–2.5 s). Liam's real timing"),
            ("4", "Shot 4 · the collapse (Rule 0b): her pure black silhouette against the dusk lane; a hard cut to the fallen pose on \"collapsed\" and her coif drops into the foreground (the coif appears only here, your fix for shot 14). The coif sheet came back with ghosts of her sheet (L45): cut free, no re-roll"),
            ("10", "Shot 10 · the wagon: the two city men lift her onto the tail of the wagon; ONE swap to seated on \"wagon\"; on \"shrine\" the wagon rolls out to the left with her on it (wheels turning), the men stay behind"),
        ],
    },
    "hc002l": {
        "aspect": "16:9",   # long = 1920x1080: every preview video / still on this page is 16:9 (user 2026-11-22: it rendered in short mode)
        "anchor": "gage-long", "short": "Gage long", "slot": "HC002-L · Sun Dec 13 · 11:00 ET = 10:00 Alberta · ready by Wed Dec 9",
        "storyboard": EP / "HC002-phineas-gage/long-storyboard-v2.md",   # v1 + motion budget v1 (tiers A/B/C/D, Mahdi 2026-11-23)
        "project": REPO / "projects/hc002-l", "previz": REPO / "projects/hc002-l/review/previz", "maps": [],
        "refs_dir": REPO / "projects/hc002-s1/refs",
        "refs": [
            ("harlow_skull_1868_full.png", "Harlow 1868, the skull engraving", "Row 17: the bar's path draws itself on it; the only place the path is shown.", "Harlow 1868, fig. 2 · Internet Archive scan · public domain"),
            ("gage_miller.jpg", "Phineas Gage, second portrait (likeness only)", "Rows 55 and 67 are re-illustrated from the portraits, never the photos themselves.", "Photograph, 1850s · Wikimedia Commons · public domain"),
            ("cavendish_cut.jpg", "The rock cut at Cavendish today", "The cut's rock walls (cold open, row 32).", "Photo, 2009 · Wikimedia Commons · CC BY-SA 3.0"),
        ],
        "extra": [EP / "HC002-phineas-gage/long-motion-tiers-v1.md", EP / "HC002-phineas-gage/long-refs.md", EP / "HC002-phineas-gage/long-backgrounds-v1.md",
                  EP / "HC002-phineas-gage/fact-gate/2026-11-21-long-script.md",
                  EP / "HC002-phineas-gage/fact-gate/2026-11-21-long-onscreen.md"],
        "page_title": "Gage Long Storyboard",
        "status": "storyboard v2: motion budget (A/B/C/D) · cost shown · waiting for your OK, nothing generated",
        "hero_pieces": REPO / "projects/hc002-l/review/hero/pieces.jpg",
        "h1": "Gage long: storyboard v2, with the motion budget",
        "lede": ("Your motion budget is applied (Tier A camera / parallax / grade for nearly every row, B for one simple overlay or a two-still swap, C for row 4 only, "
                 "D for AI clips with row 49 as the single test). Rows 2, 5 and 49 lose their sprite plans. Nothing is generated. Tap any picture to enlarge it."),
        "ask": ("<p><b>Cost (not spent):</b> 50 stills, 1 already paid (the pit plate for row 2) = 49 × $0.067 = <b>$3.28</b>; music ≈ $0.06; thumbnails ≈ $0.21; row 49's still $0.067 "
                "(the approved test, made first) = <b>≈ $3.62</b>. Spent so far on the long: $0.67. Optional apart: the row-49 clip ≈ $0.49 (the other Tier D rows 19, 45, 65, 48, 26 are not planned; all six would be $2.94).</p>"
                "<p><b>Held until your yes:</b> the 49 stills, the row-49 clip, and the Dancing stills.</p>"),
        "clip_tests": {
            "title": "Tier D tests: row 49 (two models, same frame), then rows 19 and 45 (Omni 1.2 Flash)",
            "legend": "Same still, same motion text, 5 s each, one take each. Nothing else was generated. Check: six horses stay six, reins attached, wheels roll the right way, driver stays on the box, no flashing or drift, no new objects. Audio is muted here.",
            "still": REPO / "projects/hc002-l/assets/images/keyframes16x9/row49-coach-v2-flip.png",
            "still_note": "row49-coach-v2-flip.png: the approved still ($0.067), mirrored so the team leads right.",
            "clips": [
                {"label": "A · Kling v2.1 pro (fal)", "src": REPO / "projects/hc002-l/assets/video/row49-coach-kling-v1-web.mp4",
                 "note": "$0.49 · 1920×1080 · 24 fps source, 10.9 MB after recompress (original 26.7 MB)."},
                {"label": "B · Gemini Omni 1.2 Flash (fal, 720p)", "src": REPO / "projects/hc002-l/assets/video/row49-coach-omni-v1-web.mp4",
                 "note": "≈ $0.14 (fal $0.0273/s) · 1280×720 · 24 fps source, 3.2 MB muted copy (original 5.7 MB with synthesized audio)."},
                {"label": "C · Row 19 ox cart · Omni 1.2 Flash · PASS (test only)", "src": REPO / "projects/hc002-l/assets/video/row19-oxcart-omni-v1-web.mp4",
                 "note": "Start frame s9-flip.png (rough paint fix, accepted for the test). ≈ $0.14 ESTIMATE · 720p, 5 s. Six people and two oxen stay the same, yoke and harness attached, cart drifts about 4% of the frame width left to right, light dust, camera locked (background moves under 3 px), no flashing. Wheel spin direction not confirmed by eye. Passing clip also made as 1080p 30 fps (frame blend + grain)."},
                {"label": "D · Row 45 stable · Omni 1.2 Flash · FAIL (breath)", "src": REPO / "projects/hc002-l/assets/video/row45-stable-omni-v1-web.mp4",
                 "note": "Start frame row45-stable-v2.png. ≈ $0.14 ESTIMATE · 720p, 5 s. One man, one horse, brush stays in his hand, rope stays attached, horse nods once. But the small breath is drawn as hard white scratch marks drifting off the nostrils: a new object, so not upscaled."},
                {"label": "E · Row 45 retake · minimal motion text · FAIL (second brush) → Tier A", "src": REPO / "projects/hc002-l/assets/video/row45-stable-omni-v2-web.mp4",
                 "note": "Same start frame, ≈ $0.14 ESTIMATE · 720p, 5 s. Nostrils and mouth are clean and the horse nods once, but from about 0.8 s to 1.3 s a SECOND brush appears in his rope hand and the lead rope hangs free before it returns. Fails no new objects, brush in hand and rope attached. No more retakes: row 45 goes to Tier A (still + slow push + sound). Not upscaled."},
                {"label": "F · Row 48 harbour · Omni 1.2 Flash · FAIL (new gulls)", "src": REPO / "projects/hc002-l/assets/video/row48-harbour-omni-v1-web.mp4",
                 "note": "2026-11-25. Start frame row48-valparaiso-v1.png. Prompt exactly: 'Ships sway gently and the water ripples. Locked camera. No cuts.' ≈ $0.14 ESTIMATE (live fal price checked $0.0273/s) · 720p, 5 s. Ships, coaches and houses hold, the camera is locked, no flashing (brightness step max 0.26) and no style drift. But seven SEAGULLS fly across the sky from the first second: they are not in the still and the prompt did not mention them, so it fails 'no new objects'. Not upscaled."},
                {"label": "G · Row 26 farmhouse · Omni 1.2 Flash · FAIL (face changes, drifting leaves)", "src": REPO / "projects/hc002-l/assets/video/row26-farmhouse-omni-v1-web.mp4",
                 "note": "2026-11-25. Start frame row26-farmhouse-v1.png. Prompt exactly: 'Gage walks slowly forward a few steps. Locked camera. No cuts.' ≈ $0.14 ESTIMATE · 720p, 5 s. One man throughout, hands empty, door, shovel, wood pile and lantern unchanged, camera locked, no flashing (step max 0.29). But his face is redrawn as he walks toward the camera (squint at the start, both eyes wide open at the end, more shading), which breaks the shut-left-eye rule, and a few leaves drift down that were not moving in the still (a leaf crosses the open door). Fails 'style drift' and 'no new objects'. Not upscaled."},
            ],
            "images": [
                {"id": "upscale", "src": REPO / "projects/hc002-l/review/omni-tests/upscale-compare.jpg",
                 "label": "Free test: Omni 720p upscaled to 1080p and 2160p, next to a normal still of the long (s2b)",
                 "note": "Lanczos + light unsharp + light grain. Top: the full frames. Bottom: 100% detail on the 2160 grid. Seen whole, the 1080p version holds; at 100% the Omni upscale is clearly softer than a still (soft ink lines, no fine face detail), and the grain adds weight (1080p 21 MB, 2160p 66 MB for 5 s at CRF 16). Different scenes: this compares sharpness, not content."},
                {"id": "fps", "src": REPO / "projects/hc002-l/review/omni-tests/fps-ghost-check.jpg",
                 "label": "Free test: 24 → 30 fps, three ways (same frame, crop at 160%)",
                 "note": "Judder = unevenness of the background step per frame (source 24 fps: 0.06). Frame repeat 0.26 (every 5th frame is a copy), frame blend (ffmpeg framerate) 0.04 = smoothest, motion interpolation (minterpolate) 0.19 and it dropped 2 frames. No ghosting visible on the blend at this frame."},
            ]},
        "batch1": {
            "title": "Batch 1 · ten story stills (waiting for your OK)",
            "legend": "Rows 2, 11, 23, 26, 29, 41, 52, 53, 55, 58. Actual cost $0.67 (10 × $0.067, Gemini Batch). Rows 2 and 11 are BEFORE the accident, so he has both eyes open and no scar (S1's 1848 sheet); the others use the Chile sheet (left eye shut). Each card says what passed and what did not. Batch 2 not started.",
            "items": [
                {"name": "row2-glance-v1", "title": "Row 2 · MCU, he glances over his shoulder (1848, before the accident)",
                 "report": "Likeness: thick dark hair yes, clean-shaven yes, about 25 yes, both eyes open yes (correct, it is before the accident), no scar yes. People 1. Hands and iron not in view. Rock wall, drill hole, autumn hills as written. No text, nothing modern. PASS."},
                {"name": "row11-keg-v1", "title": "Row 11 · MCU, he lifts the powder keg onto his shoulder (before the accident)",
                 "report": "Likeness: dark hair, clean-shaven, both eyes open, no scar. People 3 (Gage, a red-haired freckled youth, a dark-moustached man in a flat cap). Scale: the keg is about forearm length (about 40 cm), plain wood with hoops, no lettering. Drift: his hat came out as a rounded bowler, not the wide-brimmed felt of the sheet. No text. PASS with the hat drift."},
                {"name": "row23-harlow-v1", "title": "Row 23 · Harlow rolls up his cuffs by the lamp",
                 "report": "Harlow (sheet-harlow): dark-brown hair, short trimmed dark beard, about 29, no spectacles, frock coat hung on the chair. People 1. Open black bag with instruments, lamp, medicine bottles on a shelf, as written. No text. PASS."},
                {"name": "row26-farmhouse-v1", "title": "Row 26 · WS, thinner, out of the farmhouse into the late-autumn yard (Tier D start frame candidate)",
                 "report": "Likeness: thick dark hair, clean-shaven, no bandage, no hat, thinner. Left eye: NOT clear (both eyes narrowed in a squint); the scar is not visible. People 1, hands EMPTY (fine for Tier D under L73). He stands beside the open door, not stepping out of it. Extras: a shovel against the wall, a wall lantern (period). No text. PASS on the scene, UNCLEAR on the shut eye."},
                {"name": "row29-doorway-v1", "title": "Row 29 · MS, Gage argues in a doorway",
                 "report": "Likeness: dark hair, clean-shaven, about 28. The shut eye is his RIGHT eye (wrong side: the Chile sheet's close-ups draw it that way) and the faint scar lines sit on his right forehead. The mirrored copy fixes both. People 2 (the second: a bald man with grey side-whiskers, palm raised). No blows. No text. FAIL as drawn, PASS mirrored."},
                {"name": "row41-boston-v1", "title": "Row 41 · Boston lecture room, with the Matt cameo",
                 "report": "People 5 as asked: Gage; a white-haired doctor with long side whiskers; a bald clean-shaven doctor with arms folded; a young dark-haired doctor, no spectacles; MATT at the back right with amber round glasses, teal scarf and amber notebook. Gage: dark hair, clean-shaven, but both lids look lowered, not a clean left-eye-only closure. SCALE FAIL: the iron on the table is a short club with a knob (about 45 cm), not a 109 cm thin rod. Blackboard blank, no text. FAIL on the iron and the eyes: a re-roll candidate."},
                {"name": "row52-innyard-v1", "title": "Row 52 · MS, the inn yard, he hands a bag down",
                 "report": "Likeness: older and thinner, dark hair, clean-shaven. The shut eye is his RIGHT (wrong side). The mirrored copy fixes it. People 1 plus a passenger arm only (no face). Bag about 55 cm. Coach side, adobe wall, gate as written. No text. FAIL as drawn, PASS mirrored."},
                {"name": "row53-innhearth-v1", "title": "Row 53 · MS, he tells a story at the inn table",
                 "report": "Likeness: older and thinner, dark hair, clean-shaven, profile. The shut eye is the near one, his RIGHT (wrong side). The mirrored copy fixes it. People 4 (Gage and three distinct children: braids girl, fair-haired boy, small boy with a missing tooth). Hands open and empty. Fire, jug, beams as written. No text. FAIL as drawn, PASS mirrored."},
                {"name": "row55-portrait-v1", "title": "Row 55 · the re-illustrated portrait in its case (likeness test)",
                 "report": "Painted in our style, not a copy of the photo: dark hair, clean-shaven, about 30, LEFT eye shut and right eye open (the one face that came out on the right side). People 1. The iron is a long smooth rod with a point, upright, longer than his torso. Open leather case with a brass oval mat on dark wood. Drift: the wood and leather look a little photographic. No text. PASS."},
                {"name": "row58-deck-v1", "title": "Row 58 · MS, the ship deck, health failing",
                 "report": "FAIL on the face: his skin came out sickly green-grey, a bright red scar mark sits on his RIGHT forehead (it reads as a wound, against 'no wound, no blood'), and the shut eye is his RIGHT. Mirroring fixes the side but not the skin or the red mark. The rest is right: People 1, the carpet bag and a cloth-wrapped bundle about 1 m long, grey-green sea, no land, no text. Re-roll candidate."},
            ],
            "images": [
                {"id": "s10s12", "src": REPO / "projects/hc002-l/review/s10-s12-bandage-attempt.jpg",
                 "label": "Free fix, rows 21 and 30: S1's 16:9 s10 and s12 brow paint (before left, after right)",
                 "note": "NOT CLEAN. The band is gone over his right brow, but the repaint leaves a flat skin patch on the forehead (s10) and a smeared face (s12, where he is tiny). So the originals are back in place and the attempts are kept as s10.fix-attempt.png and s12.fix-attempt.png. Proposal: a re-roll of s10 and s12 as new 16:9 stills with the bandage over the left eye only, $0.067 each (not started)."},
            ]},
        "batch2": {
            "title": "Re-rolls of 2026-11-24 · rows 41, 55, 58 and S1's s10 / s12 (one take each, waiting for your OK)",
            "legend": "Actual cost $0.335 (5 × $0.067, Gemini Batch); hc002-l total $2.99. Free first: sheet-gage-chile-v2 (the panels whose shut eye was on the wrong side are mirrored; the two bottom heads were already right, so they stay). New stills use v2. Result: s10 and s12 pass, row 41 passes once mirrored (free copy), rows 55 and 58 do NOT pass: no further take without your yes and a cost.",
            "items": [
                {"name": "row41-boston-v2", "title": "Row 41 · Boston lecture room, re-roll (iron, young doctor)",
                 "report": "Fixed: the young doctor is a thin man with RED-BROWN hair and ginger side whiskers, nothing like Gage (dark hair, square jaw). The three doctors are distinct (white-haired with long whiskers; bald and clean-shaven, arms folded; the young ginger one), no spectacles on any. MATT sits in the back row with amber round glasses, teal scarf and an amber notebook. Gage stands by the table, hand beside the iron on the table. No text on the blackboard. Iron: now long (it spans most of the table) with a point, but the blunt end has a flared head (a small knob) and it is thicker than 3 cm: PARTIAL. Eyes as drawn: his RIGHT eye (picture-left) is shut and the left one is lowered but open: wrong side again. The mirrored copy has the LEFT eye shut and the right one looking down: use the mirrored copy."},
                {"name": "row58-deck-v2", "title": "Row 58 · MS, the ship deck, re-roll (skin, scar)",
                 "report": "Fixed: normal healthy skin, no green; older and thinner; the shut eye is his LEFT (the near eye, squeezed shut); one person; carpet bag and a cloth-wrapped bundle about 1 m long; no text. NOT fixed: the scar is a thin RED line on his RIGHT forehead (above the open eye), not a faint pale line on the left. FAIL on the scar (side and colour). Mirroring does not help (it would move the shut eye to the wrong side too)."},
                {"name": "row55-portrait-v2", "title": "Row 55 · the portrait in its case, re-roll (not a wink)",
                 "report": "Left lid shut (picture-right), right eye open, scar on his left forehead, our painted style, one person. NOT fixed: it still reads as a WINK: the shut lid is squeezed with the brow lowered and the head tilted, with a faint smirk. The iron is upright and long with a point, but its blunt end has a flared lip. FAIL on the expression."},
                {"name": "row21-s10-v2", "title": "Row 21 · S1 s10, new 16:9 (bandage over the left eye only)",
                 "report": "PASS. Same scene and cast (hotel piazza, Gage waving, Dr Williams from behind with the bag, Matt on the post, carriage). The bandage wraps the crown and passes diagonally over his LEFT eye (picture-right); his RIGHT eye and eyebrow are bare skin. Nothing over the right brow. Compare the heads below."},
                {"name": "row30-s12-v2", "title": "Row 30 · S1 s12, new 16:9 (bandage over the left eye only)",
                 "report": "PASS at the size he is shown (about 40 px): same street, doorway, whispering friends. A diagonal bandage over the crown and one eye, no flat band across both brows. His face is soft, as in the original."},
            ],
            "images": [
                {"id": "sheet", "src": REPO / "projects/hc002-l/review/sheet-chile-v1-v2.jpg",
                 "label": "Free: sheet-gage-chile (left) and sheet-gage-chile-v2 (right)",
                 "note": "In v1 the shut eye was on picture-left (his right) in the three full-body views and the top-right head. v2 mirrors those panels, so in every view his LEFT eye is the shut one. The two bottom heads were already right and are untouched; the top-left bust has both lids lowered and is untouched. The first attempt (mirroring all four heads) broke the two bottom heads; caught by comparing before and after."},
                {"id": "heads", "src": REPO / "projects/hc002-l/review/s10-s12-bandage-reroll-heads.jpg",
                 "label": "Heads at 6-8×: s10 new, s10 old, s12 new, s12 old",
                 "note": "Old: a flat band across both brows. New: the bandage crosses diagonally over his left eye only."},
            ]},
        "batch3": {
            "title": "Batch 2a · row 55 v3, the row-58 scar paint-out and 22 new stills (waiting for your OK)",
            "legend": "Actual cost $1.541 (23 × $0.067, one Gemini Batch; the cap was $1.60); hc002-l total $4.53. Free: the red scar on row 58 painted out, and iron-ref.png (the rod cut from the Wilgus daguerreotype, no face) used as the iron's SHAPE reference next to the written description. Result of the 22: 18 pass, 2 partial (rows 60 and 64), 2 fail (36b and 36c: the drawing came back as a rock-cut sketch, not the head). Lint was clean for all 23 and the build's view check found no copied backgrounds. Batch 2b not started.",
            "items": [
                {"name": "row58-deck-v3", "title": "Row 58 · the ship deck with the red scar painted out (free)",
                 "report": "The thin red scar line is gone from the forehead, nothing painted in its place. At film scale it is clean; at 4× a very faint vertical smoothing and a small notch in the eyebrow (where the line crossed it) can be seen. Everything else is untouched (v2 is kept as row58-deck-v2.orig.png). A correction to my last report: the scar was above the SHUT eye, i.e. on his LEFT forehead, which is the correct side; only its red colour was the problem."},
                {"name": "row55-portrait-v3", "title": "Row 55 · the portrait, re-roll with the Wilgus pose and expression",
                 "report": "Painted in our style, not the photograph (no grey, no grain, no copied mat). Head straight, shoulders level, brows level, mouth closed and level, one person, a faint pale scar high on the left forehead; the left lid (picture-right) is shut and the right eye is open and looks at the viewer. The iron is upright, long, thin and of even thickness with a plain flat top: no flared head this time (the shape came from iron-ref.png). Remaining flaw: the shut lid is still drawn with a lash curve and a lifted cheek, and the mouth corners rise a very little, so beside the photograph's flat, sunken lid it can still read as a mild wink. BORDERLINE: your call."},
                {"name": "row5a-lying-v1", "title": "Row 5 · still 1 · WS low, he lies in the settling dust (face turned away)",
                 "report": "People 1: dark hair, white shirt and dark braces from S1's 1848 sheet (not the Chile v2 sheet: its hat, scarf and jacket are Chilean, wrong at the rock cut). He lies on his back on grey rubble with his face turned up and away: only an ear, jaw and a sliver of cheek, no features. No blood, no injury mark, no bandage, no hat. Dust and smoke, light shafts from the right, rock wall behind. No text, nothing modern. PASS."},
                {"name": "row5b-elbow-v1", "title": "Row 5 · still 2 · MS, he pushes up on one arm (a closer size, another camera)",
                 "report": "People 1, same clothes and hair. He props himself up on one arm with his BACK to the camera and his face turned away toward the smoke. A close grey rock wall, a split drill steel and a broken plank on the rubble: a different camera and background from still 1. No blood, no text. PASS."},
                {"name": "row6-textbook-v1", "title": "Row 6 · INSERT, a hand turns a textbook page to a small head diagram",
                 "report": "One adult hand and a shirt cuff only, no face. The diagram is a plain engraved head in profile with nothing inside it (Rule 0b). Scale line L51 was used: the page is about a hand and a half wide, the diagram about thumb-sized, and it reads right against the hand. The printed text is soft wavy lines, no readable words (they look more like handwriting than print). Modern textbook on purpose. PASS."},
                {"name": "row7-monster-v1", "title": "Row 7 · CU, the crude 'monster' cartoon on the page",
                 "report": "A crude black pen cartoon of a snarling man with one bold line across his head, as approved in storyboard v2; it reads as a cartoon, not a realistic wound. No hands, no real person, wavy lines for the text, page corners in shadow. A closer size and a different background from row 6. PASS."},
                {"name": "row8-farm-v1", "title": "Row 8 · WS, a boy from behind carries a bucket across a New Hampshire farmyard",
                 "report": "People 1: a small boy in a straw hat and patched shirt seen only from behind, a wooden bucket in both hands. Grey clapboard farmhouse, barn, stone wall, rolling green hills, summer light, as written. No railroad or rock. No text. PASS."},
                {"name": "row24-sickroom-v1", "title": "Row 24 · WS, the sickroom at night",
                 "report": "People 1 in view: a woman in a dark dress and white cap, seen from behind, wringing a cloth over a basin. The bed holds only the shape under a patchwork quilt (no head, no hair, no face) as Rule 0b asks. A low candle, deep blue night in the small window, a sloped ceiling with beams. No door, no doctor, no text, nothing modern. PASS."},
                {"name": "row25-candle-v1", "title": "Row 25 · CU, the candle against the window going from night to dawn",
                 "report": "A low candle on a wooden bedside table, the small window behind it with a sky between deep blue and grey dawn. No bed, no person, no hand, no text. A closer size and another camera than row 24. PASS."},
                {"name": "row28-desk-v1", "title": "Row 28 · MS, Harlow writes in his case book by lamplight",
                 "report": "Harlow from sheet-harlow: dark-brown hair, short trimmed dark beard, no spectacles, shirtsleeves and waistcoat, writing with a quill; looks about 35 rather than 29. People 1. The case book shows wavy lines only. An ink pot, a dark bookcase of leather books, no window. Small drift: the lamp is a wall oil lamp beside him, not on the desk. PASS."},
                {"name": "row31-gate-v1", "title": "Row 31 · MS, the contractor shuts his ledger and shakes his head at the gate",
                 "report": "People 1 plus a hand: a stout, clean-shaven contractor in a tall black hat and overcoat holds a closed ledger, frowning, his breath steaming; at the lower right only a hand and a white sleeve (no face, no body). Split-rail gate, plank site shed, snow and haze beyond, no rim of the cut. Drift: the hand grips the top rail rather than dropping off it. No text. PASS."},
                {"name": "row36a-oldbook-v1", "title": "Row 36 · 1 of 3 · an old leather book with the neat drawing",
                 "report": "A heavy old leather-bound book open on a dark oak desk under a brass desk lamp; on its page a careful pen drawing of a man's head with one line across it. No person, no hands, wavy lines for the text, no readable words. Modern desk lamp on purpose (it is 'present day'). PASS."},
                {"name": "row36b-textbook-v1", "title": "Row 36 · 2 of 3 · a classroom textbook (the drawing is WRONG)",
                 "report": "FAIL: the book on the classroom desk is right, but the page shows a red pen sketch of a rock cut and trees, NOT the redrawn head. The prompt said only 'the same drawing' and the model invented one; the drawing has to be spelled out again in each prompt."},
                {"name": "row36c-paperback-v1", "title": "Row 36 · 3 of 3 · a paperback on a worn table (the drawing is WRONG)",
                 "report": "FAIL: the same fault: the page shows a pencil sketch of a rock cut, not the crude head scrawl; it is also a hardback, not a cheap cracked-spine paperback. The table and the pile of books are right."},
                {"name": "row37-reports-v1", "title": "Row 37 · CU, hands untie the ribbon on old reports (Macmillan: hands only)",
                 "report": "Two adult hands in plain cuffs, no face, no body. A bundle of old yellowed reports (wavy lines, no words) tied with a dark ribbon on green baize, a brass lamp's pool of light and dust motes. Scale line L51 used: the bundle is about two hands wide. No text. PASS."},
                {"name": "row38-slips-v1", "title": "Row 38 · INSERT, a thick book bristling with paper slips",
                 "report": "A thick book on the baize, paper slips fanned out of it, each slip with a small head drawing, the later ones darker; dust puffs, the lamp's foot, dark panelling. No hands, no faces beyond the drawings, wavy lines for text. Another camera and background from row 37. PASS."},
                {"name": "row46-stabledoors-v1", "title": "Row 46 · WS, the stable doors shut, the yard empty",
                 "report": "Row 45's place at a wider size from another camera: two tall closed plank doors with a heavy bar across them, an empty packed-earth yard with a few wisps of straw, a trough, a pale sky. No horse, no person, no open doorway. No text. PASS."},
                {"name": "row48-valparaiso-v1", "title": "Row 48 · ELS high, Valparaiso bay and a coach yard",
                 "report": "Built from the real period lithograph (ships, pale hills, houses) and the real coach photograph (coach shape): a bay with tall sailing ships, whitewashed houses climbing dry hills, and a row of seven new dark-red coaches in the foreground yard. No people. No text, nothing modern. A Tier D candidate (the doc's note). PASS."},
                {"name": "row54a-caseclosed-v1", "title": "Row 54 · 1 of 2 · MS, the closed case on the table",
                 "report": "A closed brown leather case with a brass clasp on a dark wooden table, a pale plaster wall soft behind, window light from the left. No person, no hands. Note: with nothing beside it, it reads as a small box or briefcase, larger than a real daguerreotype case. PASS with that note."},
                {"name": "row54b-caseopen-v1", "title": "Row 54 · 2 of 2 · CU, the case open, nothing visible on the plate",
                 "report": "The case open with a plum velvet lid and a dark mirror-like plate in a gilt mat; no picture visible, as asked. A closer size and another camera than 54a. No hands, no text. PASS."},
                {"name": "row59-field-v1", "title": "Row 59 · LS, the hoe left standing in the furrow",
                 "report": "A long-handled hoe stands in a furrow in a dry golden field, the grass bending in the wind, low brown hills and a wide pale sky. No person, no building (Rule 0b: framing). A thin blue line at the lower right looks like a furrow shadow. No text. PASS."},
                {"name": "row60-porch-v1", "title": "Row 60 · LS, the empty chair on the porch and the iron against the post",
                 "report": "An empty wooden chair on a porch at evening, the iron leaning against the post, golden light. The iron is thin, straight and round with an even thickness, no knob or flared end, about a hip high against the chair (the right proportions), and its top is pointed. FLAW: its LOWER end is pointed too; the iron should be blunt at one end. No person, no body. PARTIAL."},
                {"name": "row61-letter-v1", "title": "Row 61 · MS, Harlow, older and grey, reads a letter by the window",
                 "report": "Harlow from sheet-harlow's older head: grey-streaked hair and a full grey beard, dark frock coat, no spectacles; he reads a letter held in both hands beside a lace-curtained window in grey daylight, an inkwell with a quill, a writing desk. People 1. Looks about 55 rather than 48. The letter is wavy lines only. No text. PASS."},
                {"name": "row64-lecture-v1", "title": "Row 64 · LS, a lecturer points at the skull drawing; the listeners lean in",
                 "report": "A gaunt lecturer with a long moustache and a black frock coat points a wooden pointer at a plain chalk skull outline on the blackboard (no bar in it). Gaslight, arched windows, curved benches. Three casting cards were given (a young nodding man, a heavy man with grey whiskers and folded arms, a thin bald man leaning in) and they are there, but about five or six other faces show in profile or shadow, more than the card limit. The pointer touches the eye socket and cheek, not the forehead. PARTIAL."},
            ],
            "images": [
                {"id": "scar", "src": REPO / "projects/hc002-l/review/row58-scar-paintout-before-after.png",
                 "label": "Free: row 58, before (left) and after (right) the scar paint-out",
                 "note": "Colour-targeted: only the scar's own reddish pixels (a score of how much redder than the skin around), then a small inpaint along its path; the eyebrow's black is excluded. 242 pixels changed in the first pass and about 260 in the second."},
                {"id": "ironref", "src": REPO / "projects/hc002-l/review/iron-ref-view.png",
                 "label": "Free: iron-ref.png, the SHAPE reference for the iron",
                 "note": "Cut from gage_wilgus.jpg along the rod's own axis: only the two stretches with no hand on them, no face, on a flat grey. It is low-resolution and soft (a daguerreotype), so it carries the rod's proportion (long, thin, round, even, no knob) but not the point, which stays in the written description. Used for rows 55 v3 and 60."},
                {"id": "faces", "src": REPO / "projects/hc002-l/review/row55-v3-face-vs-wilgus.jpg",
                 "label": "Row 55 v3 face (left) against the Wilgus face (right), at 3×",
                 "note": "The photograph's closed lid is flat and sunken with no creases. Ours is smoother than v2 but is still drawn with a lash curve and a lifted cheek."},
            ]},
        "batch4": {
            "title": "2026-11-25 · rows 36b, 36c, 55 (free) and row 13, the iron on its own ($0.067)",
            "legend": "Actual cost $0.067 (one still, Gemini Batch); hc002-l total $4.60. Free: 36b is a tight crop of 36a's drawing, 36c is a cruder, higher-contrast ink version of row 7's page, row 55 has its shut lid and mouth paint-fixed (v3 kept). Paid: row 13, the iron alone on a flat rock. Rows 54a, 31, 28 and 61 are accepted as they are. Held: rows 60 and 64 re-rolls, the other 11 stills of batch 2b, all clips, the Dancing stills.",
            "items": [
                {"name": "row36b-textbook-v2crop", "title": "Row 36b · the textbook's head drawing (free: a crop of 36a)",
                 "report": "A 1000 px wide crop of 36a's open-book drawing (an older man's snarling head with the bold line across it), scaled to the 2752 x 1536 frame with light sharpening. It is a crop of an existing image, so it is soft at 100% (about 2.75x enlargement), fine at film scale. One drawing, the same one as 36a, no text. PASS."},
                {"name": "row36c-paperback-v2ink", "title": "Row 36c · the paperback's cruder cartoon (free: row 7's page, as rough ink)",
                 "report": "Made from row 7's cartoon head: local threshold, warped and broken lines for a rougher hand, then a sepia ink on warm paper with a soft vignette (no colour from the original). It reads as the same monster head drawn more crudely and with more contrast; the page's wavy text lines are kept as scratchy marks. No readable text. PASS."},
                {"name": "row55-portrait-v4paint", "title": "Row 55 · v3 with the shut lid and mouth paint-fixed (free; v3 kept)",
                 "report": "Lid: the lash curve and the lifted cheek under the shut left eye were painted out and one flat, slightly sunken lid line put in; mouth: the corner curl painted out and one level line drawn. Does it still read as a wink? No longer a squeeze or a lash flick, so it reads as a shut lid; but the retouch is visible at 4x (a ruled lid line, and the mouth shows a faint double line) and the brow still slightly lifts on that side. At film scale it is acceptable; a clean fix would need a re-roll, not more painting."},
                {"name": "row13-iron-v1", "title": "Row 13 · the tamping iron alone on a flat rock, side view (paid, one take)",
                 "report": "Pointed at ONE end only: YES (the right end; the left is not pointed). Blunt and cut flat at the other end: YES (flat-cut face, a very slightly softened corner, no collar or knob). Straight: YES, perfectly horizontal. No text, no inscription, no hand, no person: YES. It fills the width (about 6% to 96%). Where it differs from the real iron: it is thicker than 1 1/4 in (about 1:21 thick to length, the real one is about 1:34), and its taper is short (about the last 10% of the length, not the last foot, which is a quarter). The rock ledge and morning light came out as asked."},
            ],
            "images": [
                {"id": "lid", "src": REPO / "projects/hc002-l/review/row55_lid_before_after.png",
                 "label": "Free: row 55, v3 (left) and the paint-fixed v4 (right), face at 4x",
                 "note": "Left: the shut lid has a lash curve that flicks up at the outer end, a lifted cheek bulge and a curled mouth. Right: one flat lid line, the cheek smoothed, a level mouth."},
                {"id": "ironref2", "src": REPO / "projects/hc002-l/refs/iron-ref-v2.png",
                 "label": "iron-ref-v2.png, cut from row 13: the iron reference for every later iron shot",
                 "note": "The rod strip cut from row 13 (it passed the four checks). Note its two differences from the real iron: a little thick, and a short taper. The written description stays with it."},
            ]},
        "batch5": {
            "title": "2026-11-25 (second approval, cap $1.00) · row 13 / 60 / 64 re-rolls and the batch 2b stills, one per row",
            "legend": "Actual cost $0.938 (14 × $0.067, one Gemini Batch); hc002-l total $5.54. Lint was clean for all 14; the build's view check found no copied backgrounds. New standing iron wording (a slender javelin-like rod, 34 times longer than thick, ONE end tapering over its last quarter, the other blunt and flat) is in every new iron shot, with iron-ref-v2.png as the shape reference. Mahdi's '11 stills' were 11 ROWS: rows 12 (four inserts) and 43 (two stills) need more, so I made ONE still per row (12a, 43a); the other four (12b, 12c, 12d, 43b) would cost $0.268 more and are not made. Result: 5 pass, 5 partial, 4 fail (row 13 v2, row 60 v2, row 27, row 62). No second take of anything.",
            "items": [
                {"name": "row13-iron-v2", "title": "Row 13 · the iron alone on a rock, re-roll with the new wording (FAIL: keep v1)",
                 "report": "Pointed at one end only: YES (the right end). Blunt and flat at the other end: YES (a flat cut seen as an ellipse, no collar). Straight: YES. No text: YES. But the thickness-to-length ratio is about 1:20 (a rod about 118 px thick over about 2400 px of length), where the target is 1:34: it is NOT slender, no better than v1 (about 1:21). Taper: the upper edge starts to narrow at about 84% of the length, so the taper is about the last 16% (v1 was about 10%), where the target is a quarter. Per your rule it fails again, so v1 stays as the row-13 still and nothing more is made. iron-ref-v2.png (cut from v1) is unchanged."},
                {"name": "row60-porch-v2", "title": "Row 60 · the porch chair at evening with the iron leaning by it (FAIL on the iron)",
                 "report": "No person, no hands: YES. Evening light, porch, post, an empty ladder-back chair: as written. The iron leans against the post and is thin (about a broom handle), straight, with its pointed end UP, as asked, but the point is drawn as a spearhead (it widens like a leaf before the tip) and the blunt end on the boards is a small FLARED FOOT, like a plate: it breaks 'blunt, cut flat, no flare'. People 0. No text. FAIL on the iron; the scene is right."},
                {"name": "row64-lecture-v2", "title": "Row 64 · the lecturer points at the skull's forehead (PARTIAL: more than three faces)",
                 "report": "Pointer: its tip rests on the front of the skull outline at the forehead, above the eye socket (v1 had it at the eye socket). A gaunt lecturer with a long grey moustache and a black frock coat; the three casting cards are there (young man in the front row nodding; heavy man with grey mutton-chop whiskers, arms folded; thin bald man leaning forward). But two more audience faces show in the lower corners (a bearded man in profile at the left and a man's cheek at the right) and a bald crown at the bottom edge: five audience faces, not three. Skull outline only, no bar in it, no text on the board. Gaslight, arched windows, curved benches. PARTIAL."},
                {"name": "row12a-drill-v1", "title": "Row 12 · still 1 of 4 · ECU, a hammer drives the hand drill into the rock",
                 "report": "Two gloved hands (one holds the drill, one swings a short iron hammer) in a rolled shirt sleeve: no face, no body. Scale line L51 held: the drill is a plain iron rod about a thumb thick, the hammer head about fist-size, chips jumping from the grey layered rock. One more hand than I asked for (I asked for one), which reads naturally. No text. PASS. (Inserts b, c and d, 1.5 s each, are not made.)"},
                {"name": "row15-endofcut-v1", "title": "Row 15 · the cut seen along its length, Gage on the ledge, two crewmen call from the pit",
                 "report": "People 3, as asked: Gage small on the ledge at the left in a low dark felt hat, white shirt and dark braces, both eyes open (before the accident; S1's 1848 sheet, not Chile v2, whose shut eye is wrong here), the iron held upright; two crewmen in the pit (a grey-bearded driller, an arm raised, mouth open; a heavy moustached man with cupped hands). The iron is a thin straight pole about chin height; its ends are too small to judge. The cut runs away between two layered walls to autumn hills. No text, nothing modern. PASS."},
                {"name": "row20-stairs-v1", "title": "Row 20 · low angle up the inn stairs, bandaged Gage climbs",
                 "report": "People 1 plus a crewman's hand at his elbow (hand and sleeve only). The white bandage wraps the crown and crosses his LEFT eye (picture-right); his RIGHT eye is open and its brow is bare skin. Dark hair, clean-shaven, white shirt and dark braces. No blood. A steep wooden staircase on a white clapboard wall, a lit window at the top, a dusk sky. No text. PASS."},
                {"name": "row27-profile-v1", "title": "Row 27 · CU, Gage in profile, grey light (FAIL: scar on the wrong side)",
                 "report": "A three-quarter profile facing RIGHT; the near eye is open and the far eye is drawn shut (his LEFT: correct). Grey wall, white shirt, calm. But a clear pale SCAR sits high on the near (right) forehead: the left forehead is the scarred one, and the shot is meant to show the unhurt side. FAIL on the scar. Mirroring would also flip the shut eye to the wrong side. A free paint-out of the scar is possible (as for row 58) if you want it."},
                {"name": "row32-rim-v1", "title": "Row 32 · Gage alone on the rim of the cut at dusk",
                 "report": "People 1: Gage from behind in a dark jacket, hands empty, his head turned a little; far below, tiny working figures and one lamp, no faces. Orange sky, rim in the foreground. Drift: the cut reads as a big round quarry pit, not a narrow railroad cut, and he is larger in the frame than 'small'. No text. PASS with that drift."},
                {"name": "row42-barnum-v1", "title": "Row 42 · Barnum's hall, Gage beside the iron on a stand, a boy staring up (PARTIAL: face)",
                 "report": "People: Gage, a boy in a cap, and a few soft visitors from behind in the far hall. Gaslight, glass cases, painted banners showing only a lion and ships (no lettering). The iron lies on two brackets on a waist-high table: a long thin pole, about 1:40, pointed at the right with a taper over about the last fifth, blunt and flat at the left: good. Face: he smiles with both lids lowered as he looks down at the boy, so the shut left eye cannot be read, and the pale scar sits on the picture-left forehead (his RIGHT). The boy looks up at Gage, not at the iron. PARTIAL."},
                {"name": "row43a-shelf-v1", "title": "Row 43 · still 1 of 2 · the iron on a museum shelf with a handwritten card (PARTIAL)",
                 "report": "No people. A glass-fronted wooden cabinet shelf with soft jars behind; the iron lies along the shelf pointed to the right with a folded card propped in front of it, written in soft wavy lines (some red), unreadable. The rod is about 1:25 and looks like a pencil, with a short taper over about the last 12%; the card hides part of it. No text. PARTIAL on the iron. (Still 2, the empty shelf and the lifting hand, is not made.)"},
                {"name": "row44-bedside-v1", "title": "Row 44 · the iron by the bed, a coat on a hook, morning light (PARTIAL)",
                 "report": "No people. A plain bedroom, a narrow bed with a patchwork quilt, a coat on a wall hook, morning light through a muslin curtain, as written. The iron is thin and straight and leans upright at the FOOT of the bed (I asked for the head); its pointed top is a small leaf-shaped spearhead. Quiet, right mood. No text. PARTIAL on the iron."},
                {"name": "row50-reins-v1", "title": "Row 50 · CU, his gloved hands on the reins (PARTIAL)",
                 "report": "Scale line L51 used (each rein a thumb-wide flat strap). Two weathered gloved hands hold a fan of leather reins, steady; behind them the coach window. But about seven or eight straps show, not six; the passengers behind the glass show faces (three men in top hats), not only hat tops; and a man's jacket and knees show, not only the hands; a thin black frame line runs along the top and left edges. No text. PARTIAL."},
                {"name": "row62-doorstep-v1", "title": "Row 62 · a closed box and the wrapped iron handed across a doorstep (FAIL on the iron)",
                 "report": "Hands only, no faces: a woman's hands in dark sleeves hold out a plain closed wooden box and a bundle to a man's open hands in a dark coat cuff, on a worn stone step before a plain wooden door. Closed box about right (two hands wide), nothing inside shown. But the bundle came out as a short fat sack tied with string at both ends, about half the length of the box's depth, not a slender 109 cm pole wrapped in sacking. FAIL on the wrapped iron."},
                {"name": "row63-case-v1", "title": "Row 63 · the museum case at night, the light rises on the iron",
                 "report": "No people. A glass case on a dark cabinet in a dark gallery, a warm pool of light on a plum velvet floor, the iron lying along it, pointed at the right and flat at the left, a thin pole about 1:38 (near the 1:34 target), the taper over about the last tenth. A pale rounded soft shape at the bottom-right edge reads as the skull (it looks like a moon or an egg: soft, no detail, Rule 0b). No label, no text. PASS."},
            ],
            "images": [
                {"id": "iron13", "src": REPO / "projects/hc002-l/review/iron13-v1-v2.jpg",
                 "label": "Row 13: v1 (top) and the re-roll v2 (bottom), the rod strips",
                 "note": "Both are about 1:20 (a stout bar, not a javelin); v2 has a slightly longer taper, v1 a cleaner flat end. v2 is no nearer the target, so per your rule v1 stays."},
            ]},
        "batch6": {
            "title": "2026-11-25 (third approval, cap $0.55) · free redraws and paint-outs, row 12 b / c / d, and the two Tier D clips",
            "legend": "Spent: three stills $0.201 (actual, Gemini Batch) + two clips about $0.273 (ESTIMATE: live fal price $0.0273/s checked, 2 × 5 s; true up on fal's usage page) = about $0.47 of the $0.55 cap. hc002-l is at $5.74 actual plus the two clip estimates. Free: row 13 procedural redraw (1:34), the scar painted out of rows 27 and 42, the Chile sheet checked and repainted as v3, row 43b made from 43a. Clips: both FAILED the checklist (they are in the clip-test block above, F and G), so neither was upscaled. Held: all other clips, the Dancing stills, any more stills. No second take.",
            "items": [
                {"name": "row13-iron-v3redraw", "title": "Row 13 · the iron redrawn at 1:34 on v1 (free; v1 kept)",
                 "report": "Cut out the old rod and its shadow, filled the rock behind with a gradient plus grain, and redrew the rod at the same length: 73 px thick over 2484 px long = exactly 1:34.0, straight, the other end blunt and cut flat (the old cap reused), tapering in a smooth cone over its last 621 px = 25% of the length to a point. Every column of the new rod is the OLD rod's own shading column squeezed to the new thickness; the outline is the old ink colour. One end pointed, the other blunt and flat: YES. Straight: YES. No text: YES. At film scale it does NOT look fake: a slender javelin-like rod on the rock. At 100% the patch of rock where the old rod was is a little smoother than the painted rock around it, and the new shadow is a softer, airbrushed band. Recommendation: use it as the row-13 still; v1 stays as the original."},
                {"name": "row27-profile-v2paint", "title": "Row 27 · the scar painted off the right forehead (free; original kept)",
                 "report": "The pale scar on the near (right) forehead is gone, nothing put in its place; the shut far eye (his left) is untouched. A tiny faint speck remains near the end of the brow at 3×; clean at film scale."},
                {"name": "row42-barnum-v2paint", "title": "Row 42 · the scar painted off the right forehead (free; original kept)",
                 "report": "The scar line at the picture-left hairline is gone, nothing put in its place. A small soft notch shows in the hairline at 6×; clean at film scale. His lowered lids are accepted as they are."},
                {"name": "row43b-shelf-v1paint", "title": "Row 43 · still 2 · the empty shelf, the same label (free, from 43a)",
                 "report": "The iron is painted out of 43a (the rod behind the card and its shadow, including the tip at the right) and the shelf wood and jars filled in; the handwritten card is untouched. No new generation. A faint grey smudge is left behind the card's right edge; otherwise a clean empty shelf."},
                {"name": "row12b-pour-v1", "title": "Row 12 · insert b · powder poured from a flask into the hole",
                 "report": "One hand in a worn work glove and a rolled shirt cuff, no face. A small iron flask tips its spout over a black drill hole in flat grey rock and a thin dark stream runs into the hole. Scale line L51 held for the flask (about a hand and a half long) and the stream (a pencil-thin thread); the hole is drawn a bit wider than 5 cm (about a third of the flask's length). No text. PASS."},
                {"name": "row12c-fuse-v1", "title": "Row 12 · insert c · a fuse laid in the hole",
                 "report": "The tips of two fingers (bare, not gloved) lay a thin pale cord into a round black hole; the cord trails back across the rock in a long curve. The cord is thin (under a centimetre), the hole about two fingers wide. A soft grey rock wall behind. A different size (CU) and camera from b. No text. PASS."},
                {"name": "row12d-tamp-v1", "title": "Row 12 · insert d · the iron tamps the powder (small in the scene)",
                 "report": "One man, kneeling on a rock ledge, seen from behind and above (a low-crowned dark felt hat, white shirt, dark braces); his face is not visible. Both hands on the iron, which stands upright in the drill hole: a thin straight pole, about 1:30, a little taller than his chest, the pointed end UP and the blunt end in the hole. Taper short (about the last tenth), but small in the frame as asked. Layered rock wall and a strip of sky. No blood, no text. PASS."},
            ],
            "images": [
                {"id": "chile", "src": REPO / "projects/hc002-l/review/chile_v2_v3_scar.png",
                 "label": "Free: sheet-gage-chile v2 (top) and v3 (bottom), the two views with a scar problem",
                 "note": "Checked all four head views of v2. Top-left bust: a faint scar on his RIGHT forehead (wrong), removed in v3 and a faint pale one added on his LEFT. Top-right head: two lines, a wrong-side one on the right (removed) and the left one (kept). Bottom-left head: scar on his left (right already). Bottom-right head: no scar (left alone). So my guess that mirroring moved the scar was only half right: the top-left bust was never mirrored and still had it on the right. v2 is kept; v3 is the file for later Gage shots."},
                {"id": "r13", "src": REPO / "projects/hc002-l/review/row13_before_after.jpg",
                 "label": "Row 13: v1 (top) and the 1:34 redraw (bottom)",
                 "note": "Same rock, same light; only the rod and its shadow are new."},
                {"id": "r27", "src": REPO / "projects/hc002-l/review/row27_scar_before_after.jpg",
                 "label": "Row 27: before (left) and after the scar paint-out (right)",
                 "note": "Colour and path targeted, as for row 58."},
                {"id": "r42", "src": REPO / "projects/hc002-l/review/row42_scar_zoom.jpg",
                 "label": "Row 42: before (left) and after the scar paint-out (right), at 6×",
                 "note": "The scar is gone; a small soft notch in the hairline shows only at this zoom."},
            ]},
        "review_report": [REPO / "projects/hc002-l/review/cold_open_report.json", REPO / "projects/hc002-l/review/fx_report.json", REPO / "projects/hc002-l/review/review_report.json"],
        "preview_cut": {
            "src": REPO / "projects/hc002-l/renders/preview.mp4",
            "title": "FIRST FULL CUT of the long · 1080p preview, no music (waiting for your OK)",
            "legend": "6 min 15 s (re-rendered 2026-11-25 with the review fixes below), 1920×1080, 30 fps, -14 LUFS, rendered through the pipeline (size check passed 1920×1080; its own final review found nothing). All 66 rows in order on Liam's recorded narration; the chapter cards, title (after the sting), stamps, name tags and quote cards start on their key words; rows 49 (Kling) and 19 (Omni) are the two passing clips, frame-blended to 30 fps; row 65 is a free evening grade of the row-49 clip (mirrored, 1.25× crop); each clip plays at its own speed and length and the rest of its row is a tight Tier A still; rows 45, 48 and 26 are Tier A stills; row 13 is the 1:34 redraw; row 55 is v4paint; the Gage stills use the Chile v3 sheet. The sound is Liam plus 70 FREE placeholder effects from the channel library (not tuned); there is NO music. Shown here in nine chapter segments (a page file must stay under 15 MB); the full 1080p file is projects/hc002-l/renders/preview.mp4.",
            "labels": ["Cold open · sting · title", "1 · The Foreman", "2 · What Happened", "3 · No Longer Gage", "4 · The Myth", "5 · The Evidence",
                       "6 · The Other Side of the World", "7 · The Ending", "8 · Why It Matters · end screen"],
            "notes": [
                "COLD OPEN, rebuilt (0:00-0:22), the narration audio is NOT changed; only the pictures move. Pour still (0-5.95 s, slow push, powder hiss on 'powder') -> tip still on 'with a bar of iron' (5.95 s) -> the row-2 glance (plate from 7.2 s, 0.5 s before the voice so it is not a 0.1 s flash; the glance still from 'glances' 7.8 s) -> C1 spark (9.82 s) -> C2 blast (11.76 s) -> C3 rod (14.30 s) -> C4 aftermath (15.50 s) -> the dazed still with the blood painted to soot (19.98 s, on 'talking') -> row 6 (21.6 s).",
                "Where the timing had to give: C1 was built for 3.0 s but is shown 1.94 s (9.82-11.76 s): the TCK! spark lands on 'spark' (11.12 s) and the blast has to land on 'shoots' (12.06 s), so its 1.1 s of calm after the spark is dropped. C2 (Omni, 4.0 s) plays 2.54 s (11.76-14.30 s): its blast starts 0.30 s into the clip, so the clip starts 0.30 s before 'shoots'; it stops where the rod comes 'out the top of his skull' (C3 at 14.30 s), before Gage stands up at about 3.4 s. C3 is the first 1.2 s only (the rod turns into a cross after 1.3 s). C4 (Tier A) is stretched to the narration, 4.5 s, because a still can be: the clips themselves are never stretched, frozen or sped up. Nothing in the narration was cut or moved.",
                "C2 has an impact frame (3 frames), a comic burst over the blast and a hand-lettered BOOM!, with a shake; the burst covers the ledge where the violence would be (rule 0b). C1 has the small spark burst, TCK!, a short RGB split and a clank. Sound is free-library placeholders, untuned.",
                "CALLBACKS (C3's first 1.2 s again at natural speed, with a 2-frame impact flash and a halftone grade): row 17 at 90.16 s on 'came out through the top of his head' (amber), row 40 at 198.0 s in the pause before 'did Phineas Gage really...' (cyan-magenta), row 67 at 348.6 s on 'And the iron that went through his head?' (mono). Row 17's engraving continues its push after the callback.",
                "New stills in the cut: row 9 hilltop (from 37.7 s, replaces the S1 quarry crop), the title background (32.5 s, replaces the S1 quarry), row 43b empty shelf (replaces the painted-out v1), row 1 pour and row 5 soot copy. The older row-4 picture (empty plate, flash) is gone.",
                "Row 17 (84.9 s): the narration walks the iron's path (cheekbone, eye, top of the head); the picture is Harlow's engraving held still, with no path drawn on, and the amber callback on the last line. Chapter card 2 is hard to read over its white page.",
                "Row 25 (123.4 s): 'it looked like the iron might win': the candle still has no night-to-dawn grade yet.",
                "Row 33 (165.7 s): 'many versions end': a dissolve to the row-6 textbook page, not a freeze and sepia of row 32.",
                "Rows 39 and 40: the four stamps do not fade out and the drawing does not tear; row 40 is a push on the cropped drawing of 36b.",
                "Row 47 (231.9 s): the map now holds 5.0 s (3.6 s of ship ambience added after 'He went to Chile.'); the route is a schematic dashed sea route round Cape Horn, not a sourced one, marked as such, with its label moved off the captions. Every row after it is 3.6 s later than in the first cut.",
                "Row 56 (275.7 s): the monster drawing does not slide in beside the portrait; the portrait holds and the word 'exploded' appears as a card.",
                "Row 57 (282.5 s): 12.4 s on one split still (grey doorway left, coach right); the left does not grey and the right does not warm, so it is the longest hold in the cut.",
                "Quote cards sit in the middle of the frame and cover faces in rows 11, 22 and 29 (and the stamps on row 35 sit on the cartoon face): the card position is fixed in the component.",
                "Long single-picture stretches (tempo): row 13 (10.3 s), row 29 (8.0 s), row 53 (7.7 s), row 17 (7.0 s), row 52 (7.0 s), row 59 (6.9 s), row 39 (6.8 s), row 56 (6.8 s).",
                "Clips: rows 19, 49 and 65 play at their own speed and length (5.0, 5.07, 5.07 s) and then cut to a tight still of the same scene (about 1 s); no frozen frame. Proposals are in the review block below.",
                "Pictures you already accepted with flaws show as they are: row 44 (spearhead tip, foot of the bed), row 50 (seven reins, passenger faces), row 60 (flared foot), row 62 (the bundle is a short sack), row 64 (five faces), row 36b (a soft crop).",
            ],
            "gaps": [
                "Tier A layers: every still has only a camera push, pull or slide (the motion lint lists all 83 shots as camera-only); the parallax, dust, flicker, candle and grade layers the storyboard promised are not built.",
                "Row 13's measure line and glint, row 17's amber path, row 25's night-to-dawn grade, row 40's tear, the stamp fades of row 39.",
                "Sound: the placeholders are one-shot library files placed on the rows; no tuning, no music. The end screen is the generic brand end screen.",
                "4K master: the stills are 2752 px wide, so the final 3840 px render is soft (the pipeline warns); this preview is 1080p.",
            ],
        },
        "hero_real": [],   # v2 (2026-11-23): no HERO sprite plans for rows 2, 5, 49; row 4 stays C (S1 pieces)
    },
    "hc002s1": {
        "anchor": "gage-s1", "short": "Gage S1", "slot": "CASE 11 · Sun Nov 29 · 15:00 ET = 14:00 Alberta · ready by Wed Nov 25",
        "storyboard": EP / "HC002-phineas-gage/s1-storyboard-v1.md", "story": EP / "HC002-phineas-gage/s1-story-v2.md",
        "project": REPO / "projects/hc002-s1", "previz": REPO / "projects/hc002-s1/review/previz", "maps": [],
        "refs_dir": REPO / "projects/hc002-s1/refs",
        "refs": [
            ("gage_wilgus.jpg", "Phineas Gage (likeness only)", "Square face, clean-shaven, dark hair. Taken years after the accident: used for his face, never shown (it belongs to the long video's twist).", "Daguerreotype, 1850s · Wilgus collection via Wikimedia Commons · CC BY-SA 3.0"),
            ("gage_miller.jpg", "Phineas Gage, second portrait (likeness only)", "The same face from a second angle; not shown in S1.", "Photograph, 1850s · Wikimedia Commons · public domain"),
            ("tamping_iron.jpg", "The tamping iron", "Smooth, round, pointed at one end: not a crowbar (shots 1, 3, 5, 7, 11).", "Harlow 1868 · Wikimedia Commons · public domain"),
            ("harlow_skull_1868.jpg", "Harlow's skull drawing, 1868", "Shot 6: the bar's path draws itself on this engraving; no flesh anywhere.", "Harlow 1868, fig. 1 · Wikimedia Commons · public domain"),
            ("bigelow_1850_side.png", "Bigelow 1850, side view", "The path through the skull as the doctors drew it in 1850.", "Am J Med Sci 1850 · Wikimedia Commons · public domain"),
            ("cavendish_cut.jpg", "The rock cut at Cavendish today", "Grey rock walls of the cut (presumed site): the set of shots 1–5 and 8.", "Photo, 2009 · Wikimedia Commons · CC BY-SA 3.0"),
            ("ox_carts_1850s.jpg", "Ox carts, 1850s", "Wooden carts and oxen of the period (shot 9).", "Photo, 1850s, St. Anthony, Minnesota · DPLA via Wikimedia Commons · public domain"),
        ],
        "extra": [EP / "HC002-phineas-gage/script-long-v1.md", EP / "HCS10-pettenkofer/story-v1.md", EP / "HCS11-hilliard/story-v1.md",
                  EP / "HCS13-koepcke/story-v1.md", EP / "HCS12-ffirth/story-v1.md"],
        "page_title": "Slate Scripts for Approval",
        "status": "Gage S1 HERO shots, round 2 (closer, per your notes) · waiting for your OK",
        "layered_title": "Gage S1: the three HERO shots, closer (your notes of Nov 18)",
        "layered_lede": ("Your rule from now on: in a HERO shot the moving subject fills at least 1/3 of the frame (the build now checks it). "
                         "All three shots are reworked to it. Next to each preview: what happens in plain words, what changed, then every "
                         "piece the shot uses with the picture that came back and its full prompt, exactly as sent. The timing is still a "
                         "SCRATCH timeline (no narration yet; every key is tied to a word, so the real narration re-times it), and there "
                         "is no sound yet."),
        "hero": {
            "s01": {"label": "Shot 1 · the blast", "pieces": ["plate-s1", "pose-gage-s1", "sprite-iron", "sprite-hat"],
                    "desc": ("Low on the floor of the rock cut, looking up, with the hook card on top. The charge goes off: dust bursts up, "
                             "the picture shakes, two of his men duck. The iron bar shoots up out of the dust <b>above</b> him (never across "
                             "his head) and comes toward us: it grows from 0.6 to 0.93 of the frame width, with a sunlit top edge, a trail "
                             "behind it while it is fast, and a glint that runs along it twice (once as it hangs, once on “skull”). It stays "
                             "in the frame to the cut. Gage is a true silhouette with a warm rim of light: his hat, shirt and braces read "
                             "as shapes, his face does not. He is thrown backward toward the camera, tipping back as his hat spins away, "
                             "and drops out of the bottom of the frame."
                             "<br><b>Changed:</b> the bar 2–3× bigger and closer (it was 0.34 wide), lit edge + glint + trail, visible until "
                             "“skull”; Gage a true silhouette instead of a dimmed lit figure; a big, clear fall backward."),
                    "notes": {"plate-s1": "v1, unchanged.",
                              "pose-gage-s1": "v2. Made into a silhouette locally (no new image): the white shirt kept a shade lighter, a warm rim on the edges.",
                              "sprite-iron": "v1. The sunlit edge and the glint are added locally (no new image).",
                              "sprite-hat": "v2, as a silhouette (locally)."}},
            "s05": {"label": "Shot 4 · the look", "pieces": ["plate-s4", "pose-gage-s4"],
                    "desc": ("It opens wide, from the pit behind two of his men, with Gage up on the ledge holding the tamping iron in the "
                             "drill hole. The camera pushes in on him through the shot and lands at a medium shot (3.6×) just before the "
                             "word “shoulder”, when he turns his head over his right shoulder toward his men: the turn now fills the "
                             "frame.<br><b>Changed:</b> the push in, ending at MS (he grows from 0.24 to about 0.86 of the frame height). "
                             "The background softens as it is enlarged; he stays sharp."),
                    "notes": {"plate-s4": "v1, unchanged.", "pose-gage-s4": "v2, unchanged."}},
            "s09": {"label": "Shot 8 · he spoke", "pieces": ["plate-s8", "pose-gage-s8"],
                    "desc": ("No music. Ground level, on the rock floor: the smoke settles in your shafts of light. Gage lies across the "
                             "foreground, his open hand large at the lower left, his head turned away (only the back of his head). In "
                             "the silence his fingers curl; on the word “spoke” he pushes himself up on his elbow, his shoulder rising "
                             "toward us. No face, no blood.<br><b>Changed:</b> the plate remade as planned (ground-level, close), and a new "
                             "close pose sheet to match it, because the full-body side view could not fill the foreground without going soft."),
                    "notes": {"plate-s8": ("v4. v3 painted a man's hand into the empty plate, because my prompt named the hand that is "
                                           "added later (new lesson L47), and it copied the old wide camera. v4 takes only a detail of "
                                           "the old plate (the rock, the smoke and your light shafts). Two kegs came back labelled "
                                           "“BLASTING POWDER”: the lettering is painted out locally, and the set description now asks "
                                           "for unmarked kegs."),
                              "pose-gage-s8": ("v4, close, no sheet reference. The propped-up drawing came back facing the other way, "
                                               "so it is mirrored and lined up at the waist. Dark flecks in his hair that read like "
                                               "wounds are painted out locally.")}},
        },
        "story_kicker": "Story doctor · story v2 · 2026-11-18 · for approval",
        "v1_label": "v1 (S1 script, Oct 18)",
        "script_heading": "Script v2 (for approval; not recorded yet)",
        "h1": "Gage S1: the three HERO shots, closer",
        "lede": "Round 4 for Gage S1 (CASE 11, Sun Nov 29). Your notes on the three HERO shots are in: everything moving is now at least a third of the frame (the build checks it from now on); shot 1's bar is bigger, closer and lit, and Gage is a true silhouette thrown backward; shot 4 pushes in to MS for the head turn; shot 8 has its ground-level plate with his hand and shoulder in the foreground. Hilliard and Koepcke scripts: approved. Further down, “Reference images made first” shows the character sheets and the set plate with their prompts, and the story stills keep their sketches and prompts (not made yet). Tap any picture to enlarge it.",
        "ask": "<p><b>Gage S1, the three HERO shots:</b> OK them, or tell me what to change. After your OK I make the story stills you approved: the 9 stills with their 16:9 versions for the long, ≈ $1.21 on Gemini Batch, plus the bandaged-Gage sheet redo (+$0.07). After that come narration (≈ $0.07) and music (≈ $0.13) on fal ($20.97 balance).</p><p><b>Spent this round:</b> $0.20 for 3 images. Shot 8 needed both a new plate and a matching close pose sheet: you estimated ~$0.07 for the plate alone, and the full-body cut-outs would have gone soft at that size. One more plate try was needed after v3 painted a hand in. Everything else (the lit bar, the glint, the trail, the silhouettes, the push) was done locally for free. Gage S1 total so far: $1.54 for 23 images.</p>",
    },
}


def inline(md: str) -> str:
    t = html.escape(md.strip())
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def table(lines: list[str], start_pat: str) -> list[list[str]]:
    """Rows of the first markdown table whose header line matches start_pat, plus every later table with the very same
    header line (a long video's storyboard has one shot table per chapter, 2026-11-21)."""
    rows, on, head = [], False, None
    for ln in lines:
        if not on and ln.startswith("|") and (re.search(start_pat, ln) if head is None else ln == head):
            on, head = True, head or ln
            continue
        if on:
            if not ln.startswith("|"):
                on = False
                continue
            if re.match(r"^\|[-\s|]+\|$", ln):
                continue
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows


def parse(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").split(" · ")[0]
    m = re.search(r"```\n(.*?)```", text, re.S)
    script = m.group(1).strip().splitlines() if m else []
    shots = table(lines, r"^\| # \|")
    cast = table(lines, r"^\| Who / where \|")
    notes, cur = [], None  # bold-led paragraphs (Care, Period, Theme...), joined across wrapped lines
    for ln in lines:
        if ln.startswith("**") and not ln.startswith("**Total"):
            if cur:
                notes.append(cur)
            cur = ln
        elif cur and ln.strip() and not ln.startswith(("|", "#", "```")):
            cur += " " + ln.strip()
        else:
            if cur:
                notes.append(cur)
            cur = None
    if cur:
        notes.append(cur)
    notes = [n for n in notes if not n.startswith(("**Loop", "**Decoupage"))][:7]
    cost = re.search(r"\*\*Total ≈ (\$[\d.]+)\.\*\*", text)
    timed = re.search(r"^\| # \| t \|", text, re.M)   # long storyboards give start times, not durations
    secs = (max((float(r[1]) for r in shots if re.match(r"^[\d.]+$", r[1])), default=0.0) if timed else
            sum(float(r[1]) for r in shots if re.match(r"^[\d.]+$", r[1])))
    return {"title": title, "script": script, "shots": shots, "cast": cast, "notes": notes,
            "cost": cost.group(1) if cost else "", "secs": secs}


def tension_svg(beats: list[tuple[str, int, int]], v1_label: str = "v1 (rough cut 1)") -> str:
    """v1 vs v2 tension per beat (editorial rating 0-10). Two series: legend + direct labels; native hover titles."""
    W, H, L, R, T, B = 640, 250, 34, 44, 14, 46
    n = len(beats)
    x = lambda i: L + (W - L - R) * (i / max(1, n - 1))  # noqa: E731
    y = lambda v: T + (H - T - B) * (1 - v / 10)  # noqa: E731
    grid = "".join(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="g"/>'
                   f'<text x="{L - 8}" y="{y(v) + 4:.1f}" class="ax" text-anchor="end">{v}</text>' for v in (0, 5, 10))
    ticks = "".join(f'<text x="{x(i):.1f}" y="{H - B + 18}" class="ax" text-anchor="middle">{html.escape(b[0])}</text>'
                    for i, b in enumerate(beats))
    out = []
    for key, idx, label in (("v1", 1, v1_label), ("v2", 2, "v2 (proposed)")):
        pts = " ".join(f"{x(i):.1f},{y(b[idx]):.1f}" for i, b in enumerate(beats))
        dots = "".join(f'<circle cx="{x(i):.1f}" cy="{y(b[idx]):.1f}" r="4.5" class="d {key}"><title>{label} · {html.escape(b[0])}: '
                       f'{b[idx]}/10</title></circle>' for i, b in enumerate(beats))
        last = beats[-1][idx]
        out.append(f'<polyline points="{pts}" class="l {key}"/>{dots}'
                   f'<text x="{x(n - 1) + 8:.1f}" y="{y(last) + 4:.1f}" class="lab">{key}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" class="tension" role="img" aria-label="Tension per beat, v1 versus v2">{grid}{ticks}'
            f'{"".join(out)}</svg>')


def story_block(k: str, e: dict, img: Path) -> str:
    """Round 2 (user 2026-11-15, 'the rhythm is flat'): story-v2.md from the story-doctor skill, for approval."""
    f = e.get("story")
    if not f or not f.exists():
        return ""
    lines = f.read_text(encoding="utf-8").splitlines()
    def para(prefix: str) -> str:  # a paragraph that wraps over several md lines
        out = None
        for ln in lines:
            if out is None and ln.startswith(prefix):
                out = ln
            elif out is not None:
                if not ln.strip() or ln.startswith(("|", "#", "- ")):
                    break
                out += " " + ln.strip()
        return out or ""
    why = para("Why:")
    spine = [ln[2:] for ln in lines if ln.startswith("- **")]
    beats = table(lines, r"^\| Beat \| Line")
    shots = table(lines, r"^\| # \| Beat")
    rhythm = table(lines, r"^\| Beat \| Cuts")
    score = table(lines, r"^\| \| Hook")
    cost = next((ln for ln in lines if "**≈ $" in ln), "")
    changed = para("**Changed from v1")
    kf_dir = e["project"] / "assets/images/keyframes"
    pts, rows = [], []
    for b in beats:
        m = re.match(r"(\d+)\s*→\s*(\d+)", b[3])
        name = b[0].split()[0]
        if m:
            pts.append((name, int(m.group(1)), int(m.group(2))))
        tags = re.match(r"^((?:\[[^\]]+\]\s*)*)(.*)$", b[1])
        tg = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in re.findall(r"\[[^\]]+\]", tags.group(1)))
        body = re.sub(r"\[(pause|beat)\]", r'<span class="tag">[\1]</span>', inline(tags.group(2)))
        rows.append(f'<tr><td><span class="beat">{html.escape(b[0])}</span></td><td>{tg}{body}</td>'
                    f'<td class="tn">{html.escape(b[3])}</td></tr>')
    # merge repeated beat names so the chart has one point per beat (the highest v2 inside it)
    merged: dict[str, tuple[str, int, int]] = {}
    for nme, a, b2 in pts:
        merged[nme] = (nme, max(a, merged.get(nme, (0, 0, 0))[1]), max(b2, merged.get(nme, (0, 0, 0))[2]))
    cards = []
    for r in shots:
        n, beat, act, status = (r + [""] * 4)[:4]
        sid = n.split(",")[0].strip().strip("~")  # "9a, 9b" / "~~5~~, ~~9a~~": the first shot's picture
        st = re.search(r"\*\*(KEEP|REDO|NEW|DROP)\*\*|^(KEEP|DROP)", status)
        kind = (st.group(1) or st.group(2)) if st else "KEEP"
        kf = kf_dir / f"s{sid}.png"
        pic = (f'<img src="img/{shrink(kf, img / f"{k}-v2-{sid}", 600)}" alt="Current image, shot {html.escape(sid)}" loading="lazy">'
               if kf.exists() and not sid.startswith("N") else '<div class="newpic">new image</div>')
        cards.append(f'<article class="v2 {kind.lower()}">{pic}<div><div class="head"><span class="num">{html.escape(n.replace("~", ""))}</span>'
                     f'<span class="st {kind.lower()}">{kind}</span><span class="size">{inline(beat)}</span></div>'
                     f'<p>{inline(act)}</p><p class="muted">{inline(status)}</p></div></article>')
    rh = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rhythm)
    sc = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in score)
    return f"""
  <div class="block story"><div class="kicker">{html.escape(e.get("story_kicker", "Round 2 · story v2 · approved 2026-11-15"))}</div>
  <p class="lede">{inline(why.removeprefix('Why: '))}</p>
  <h3>The tension curve (editorial rating per beat)</h3>
  <div class="chart"><div class="key"><span><i class="sw v1"></i>{html.escape(e.get("v1_label", "v1, rough cut 1"))}</span><span><i class="sw v2"></i>v2, proposed</span></div>
  {tension_svg(list(merged.values()), e.get("v1_label", "v1 (rough cut 1)"))}</div>
  <h3>Spine</h3><ul class="spine">{''.join(f'<li>{inline(s)}</li>' for s in spine)}</ul>
  <h3>Script v2, beat by beat</h3><div class="cast"><table><tr><th>Beat</th><th>Line (Liam)</th><th>Tension v1 → v2</th></tr>{''.join(rows)}</table></div>
  <div class="notes"><p>{inline(changed)}</p></div>
  <h3>Shots: keep, fix, redo, new (every shot has an action)</h3><div class="v2grid">{''.join(cards)}</div>
  <h3>Rhythm map (the edit plan)</h3><div class="cast"><table><tr><th>Beat</th><th>Cuts</th><th>Camera</th><th>Music</th><th>Hero sound</th></tr>{rh}</table></div>
  <h3>Score</h3><div class="cast"><table><tr><th></th><th>Hook</th><th>Stakes</th><th>Turns</th><th>Climax</th><th>Payoff</th><th>Action</th><th>Rhythm</th><th>Avg</th></tr>{sc}</table></div>
  <p class="meta">{inline(cost)}</p></div>"""


PROMPT_KEYS = r"(SET:|GEOGRAPHY:|SHOT:|CAMERA:|BACKGROUND \(exactly this, nothing else\):|CAST:|CROWD:|FRAMING:|Hidden detail|Small background cameo of MATT)"


def prompt_html(spec: dict) -> str:
    """One image spec -> readable blocks: which references go in, then the prompt split at its labelled parts."""
    parts = re.split(PROMPT_KEYS, spec.get("prompt", ""))
    out, cur = [], parts[0].strip()
    if cur:
        out.append(cur)
    for i in range(1, len(parts), 2):
        out.append(parts[i] + parts[i + 1])
    refs = ", ".join(r.split(":", 1)[-1].split("/")[-1] for r in spec.get("refs", []))
    meta = f"{spec.get('aspect', '9:16')} · {spec.get('resolution', '2K')} · references: {refs or 'none'}"
    roles = f'<p class="roles">{inline(spec["roles"])}</p>' if spec.get("roles") else ""
    return (f'<details class="prompt"><summary>Image prompt</summary><p class="pmeta">{html.escape(meta)}</p>{roles}'
            + "".join(f"<p>{inline(x)}</p>" for x in out) + "</details>")


def sent_prompt(spec: dict) -> str:
    """The prompt EXACTLY as episode.py sends it (style lock + roles + prompt + aspect + tail + style prefix)."""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import episode as epi
        return (epi.LOCK + spec.get("roles", "") + " " + spec["prompt"] + f" Aspect {spec.get('aspect', '9:16')}."
                + epi.TAIL + " " + epi.style_prefix())
    except Exception:
        return spec.get("roles", "") + " " + spec.get("prompt", "")


def hero_pieces(k: str, sid: str, hero: dict, ep: dict, p: Path, img: Path) -> str:
    """Per HERO shot (user 2026-11-18): each paid piece it uses = the picture that came back + its full prompt."""
    refs = ep.get("references", {})
    out = []
    for rn in hero.get("pieces", []):
        spec = refs.get(rn)
        if not spec:
            continue
        f = p / "assets/images/refs" / f"{rn}.png"
        pic = (f'<img src="img/{shrink(f, img / f"{k}-{sid}-{rn}", 1100)}" alt="{html.escape(rn)}, as generated" loading="lazy">'
               if f.exists() else '<p class="st new">not made yet</p>')
        names = ", ".join(r.split(":", 1)[-1].split("/")[-1] for r in spec.get("refs", []))
        out.append(f'<article class="piece"><figure>{pic}<figcaption><b>{html.escape(rn)}</b>'
                   f'<span>{html.escape(hero.get("notes", {}).get(rn, ""))}</span></figcaption></figure>'
                   f'<details class="prompt" open><summary>Full prompt, exactly as sent</summary>'
                   f'<p class="pmeta">{html.escape(spec.get("aspect", "9:16"))} · {html.escape(spec.get("resolution", ep.get("image_resolution", "2K")))}'
                   f' · references in: {html.escape(names or "none")}</p>'
                   f'<p class="full">{html.escape(sent_prompt(spec))}</p></details></article>')
    return f'<div class="pieces">{"".join(out)}</div>' if out else ""


def md_section(f: Path) -> str:
    """A markdown file (headings, paragraphs, bullet lists, tables) as one page block: the long script on the S1 page."""
    out, para, tbl, lst = [], [], [], []
    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>"); para.clear()
        if lst:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + "</ul>"); lst.clear()
        if tbl:
            rows = [r for r in tbl if not re.match(r"^\|[-\s|]+\|$", r)]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
            out.append(f'<div class="cast"><table><tr>{head}</tr>{body}</table></div>'); tbl.clear()
    lines = f.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ")
    for ln in lines[1:]:
        if ln.startswith("|"):
            if para or lst:
                flush()
            tbl.append(ln); continue
        if tbl:
            flush()
        if ln.startswith("#"):
            flush(); out.append(f"<h3>{inline(ln.lstrip('# '))}</h3>")
        elif re.match(r"^\s*- ", ln):
            if para:
                flush()
            lst.append(ln.strip()[2:])
        elif re.match(r"^\s{2,}\S", ln) and lst:
            lst[-1] += " " + ln.strip()
        elif not ln.strip() or ln.strip() == "---":
            flush()
        else:
            if lst:
                flush()
            para.append(ln.strip())
    flush()
    return f'<div class="block mdsec"><div class="kicker">for approval</div><h2>{inline(title)}</h2>{"".join(out)}</div>'


def episode_json(e: dict) -> dict:
    import json
    f = e.get("project") and e["project"] / "episode.json"
    return json.load(open(f, encoding="utf-8")) if f and f.exists() else {}


def image_cost(ep: dict) -> tuple[int, float]:
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import google_images as g
    except Exception:
        return 0, 0.0
    n, tot = 0, 0.0
    for sec in ("references", "keyframes"):
        for spec in ep.get(sec, {}).values():
            n += 1
            tot += g.price(spec.get("model", "gemini-3-pro-image"), spec.get("resolution", ep.get("image_resolution", "2K")), True)
    return n, tot


def web_preview(render: Path, dst: Path) -> bool:
    """A light copy of the rough cut for the page (an Artifact file must stay under 15 MB): 540x960 for a Short,
    960x540 for a long. The size follows the SOURCE orientation (user 2026-11-23: the Gage long coach rendered 16:9 but
    this scale squashed it to 540x960, so the page looked like short mode)."""
    import subprocess
    if not render.exists():
        return False
    if not dst.exists() or dst.stat().st_mtime < render.stat().st_mtime:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dims = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                               "-of", "csv=p=0", str(render)], capture_output=True, text=True, check=True).stdout.strip().split(",")
        w, h = int(dims[0]), int(dims[1])
        size = "scale=960:540" if w > h else "scale=540:960"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(render), "-vf", size, "-c:v", "libx264",
                        "-preset", "slow", "-crf", "26", "-maxrate", "1500k", "-bufsize", "3000k", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(dst)], check=True)
    return True


def clip_tests_block(k: str, e: dict, out: Path, img: Path) -> str:
    """Tier D test clips side by side (user 2026-11-23): the start still + one labelled clip per provider, with price and file size."""
    tests = e.get("clip_tests")
    if not tests:
        return ""
    p, figs = e.get("project"), []
    st = tests.get("still")
    if st and Path(st).exists():
        figs.append(f'<figure><img src="img/{shrink(Path(st), img / f"{k}-clip-start", 1300)}" alt="Start frame for both clips" loading="lazy">'
                    f'<figcaption><b>Start frame (both clips)</b><span>{html.escape(tests.get("still_note", ""))}</span></figcaption></figure>')
    for i, c in enumerate(tests["clips"]):
        dst = out / "video" / f"{p.name}-row49-clip-{i}.mp4"
        if not web_preview(Path(c["src"]), dst):
            continue
        figs.append(f'<figure><video class="cut" controls playsinline loop preload="metadata" src="video/{dst.name}"></video>'
                    f'<figcaption><b>{html.escape(c["label"])}</b><span>{html.escape(c["note"])}</span></figcaption></figure>')
    for c in tests.get("images", []):
        if Path(c["src"]).exists():
            figs.append(f'<figure class="wide2"><img src="img/{shrink(Path(c["src"]), img / (k + "-" + c["id"]), 2000)}" alt="{html.escape(c["label"])}" loading="lazy">'
                        f'<figcaption><b>{html.escape(c["label"])}</b><span>{html.escape(c["note"])}</span></figcaption></figure>')
    return ('<div class="block"><h3>' + html.escape(tests["title"]) + '</h3><p class="legend">' + html.escape(tests["legend"]) + '</p>'
            '<div class="refs cliptests">' + "".join(figs) + '</div></div>')


def preview_block(k: str, e: dict, out: Path) -> str:
    """The first full cut of the long (user 2026-11-25): the 1080p preview split at the chapter starts into web segments (an Artifact
    file must stay under 15 MB), the picture/narration notes, and what is not built yet."""
    pv = e.get("preview_cut")
    if not pv or not Path(pv["src"]).exists():
        return ""
    import subprocess
    src, p = Path(pv["src"]), e["project"]
    chap = json.load(open(p / "artifacts/chapters.json", encoding="utf-8"))
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(src)],
                                 capture_output=True, text=True, check=True).stdout.strip())
    starts = [0.0] + [c["start"] for c in chap[1:]]
    ends = starts[1:] + [total]
    figs = []
    for i, (a, b) in enumerate(zip(starts, ends)):
        dst = out / "video" / f"{p.name}-cut-{i}.mp4"
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            dst.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.2f}", "-to", f"{b:.2f}", "-i", str(src), "-vf", "scale=960:540",
                            "-c:v", "libx264", "-preset", "slow", "-crf", "29", "-maxrate", "850k", "-bufsize", "1700k", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(dst)], check=True)
        mb = dst.stat().st_size / 1e6
        if mb > 14.5:
            raise SystemExit(f"{dst.name} is {mb:.1f} MB: over the Artifact file limit")
        label = pv["labels"][i]
        figs.append(f'<figure><video class="cut" controls playsinline preload="metadata" src="video/{dst.name}"></video>'
                    f'<figcaption><b>{html.escape(label)}</b><span>{a:.0f}s to {b:.0f}s · {mb:.1f} MB</span></figcaption></figure>')
    notes = "".join(f"<li>{html.escape(n)}</li>" for n in pv["notes"])
    gaps = "".join(f"<li>{html.escape(n)}</li>" for n in pv["gaps"])
    return ('<div class="block"><h3>' + html.escape(pv["title"]) + '</h3><p class="legend">' + html.escape(pv["legend"]) + '</p>'
            '<div class="refs cliptests">' + "".join(figs) + '</div>'
            '<p class="legend"><b>Rows where the narration and the picture disagree, or the picture is not what the storyboard asked for:</b></p><ul class="legend">'
            + notes + '</ul><p class="legend"><b>Not built into this cut (it is a preview):</b></p><ul class="legend">' + gaps + '</ul></div>')


def review_block(k: str, e: dict, out: Path, img: Path) -> str:
    """Review fixes (user 2026-11-25): a report file with titled sections; each has paragraphs, bullet lists, a table and labelled images
    (the cut audit contact sheets, the background-check result, the caption highlight, the map, the clip-length list, the reuse list)."""
    specs = e.get("review_report")
    if not specs:
        return ""
    return "".join(_review_one(k, e, Path(sp), out, img) for sp in (specs if isinstance(specs, list) else [specs]) if Path(sp).exists())


def _review_one(k: str, e: dict, spec: Path, out: Path, img: Path) -> str:
    rep = json.load(open(spec, encoding="utf-8"))
    parts = [f'<div class="block"><h3>{html.escape(rep["title"])}</h3><p class="legend">{html.escape(rep.get("legend", ""))}</p>']
    for n, sec in enumerate(rep["sections"]):
        parts.append(f'<h4>{html.escape(sec["heading"])}</h4>')
        for para in sec.get("paras", []):
            parts.append(f'<p class="legend">{html.escape(para)}</p>')
        if sec.get("bullets"):
            parts.append('<ul class="legend">' + "".join(f"<li>{html.escape(b)}</li>" for b in sec["bullets"]) + "</ul>")
        if sec.get("table"):
            t = sec["table"]
            parts.append('<div style="overflow-x:auto"><table class="legend" style="border-collapse:collapse;font-size:13px"><tr>'
                         + "".join(f'<th style="text-align:left;padding:3px 10px;border-bottom:1px solid var(--line)">{html.escape(h)}</th>' for h in t["head"]) + "</tr>"
                         + "".join("<tr>" + "".join(f'<td style="padding:3px 10px;vertical-align:top;border-bottom:1px solid var(--line)">{html.escape(str(c))}</td>' for c in r) + "</tr>"
                                   for r in t["rows"]) + "</table></div>")
        figs = []
        for j, v in enumerate(sec.get("videos", [])):
            dst = out / "video" / f"{spec.stem}-{n}-{j}.mp4"
            if Path(v["src"]).exists() and web_preview(Path(v["src"]), dst):
                figs.append(f'<figure class="wide2"><video class="cut" controls playsinline loop preload="metadata" src="video/{dst.name}"></video>'
                            f'<figcaption><b>{html.escape(v["label"])}</b><span>{html.escape(v.get("note", ""))}</span></figcaption></figure>')
        for j, im in enumerate(sec.get("images", [])):
            if not Path(im["src"]).exists():
                continue
            figs.append(f'<figure class="wide2"><img src="img/{shrink(Path(im["src"]), img / f"{k}-{spec.stem}-{n}-{j}", im.get("edge", 2000))}" alt="{html.escape(im["label"])}" loading="lazy">'
                        f'<figcaption><b>{html.escape(im["label"])}</b><span>{html.escape(im.get("note", ""))}</span></figcaption></figure>')
        if figs:
            parts.append('<div class="refs cliptests">' + "".join(figs) + "</div>")
    parts.append("</div>")
    return "".join(parts)


def batch1_block(k: str, e: dict, ep: dict, out: Path, img: Path) -> str:
    """Gage long, story stills batch 1 (user 2026-11-23): each still with its check report, a mirrored copy where the closed eye is on
    the wrong side, the prompt, and the free S1 brow-fix attempts."""
    kf = e["project"] / "assets/images/keyframes16x9"
    blocks = []
    for bk, tag in (("batch1", "b1"), ("batch2", "b2"), ("batch3", "b3"), ("batch4", "b4"), ("batch5", "b5"), ("batch6", "b6")):   # batch4 = 2026-11-25: free crops + row 13; batch2 = the 2026-11-24 re-rolls, batch3 = row 55 v3 + batch 2a
        b = e.get(bk)
        if not b:
            continue
        figs = []
        for it in b["items"]:
            src = kf / f'{it["name"]}.png'
            if not src.exists():
                continue
            pics = f'<img src="img/{shrink(src, img / (k + "-" + tag + "-" + it["name"]), 1500)}" alt="{html.escape(it["title"])}" loading="lazy">'
            flip = kf / f'{it["name"]}-flip.png'
            if flip.exists():
                pics += (f'<img src="img/{shrink(flip, img / (k + "-" + tag + "-" + it["name"] + "-flip"), 1500)}" alt="Mirrored copy" loading="lazy">'
                         '<small>the same still mirrored: the shut eye is now his LEFT (use this one)</small>')
            spec = ep.get("keyframes", {}).get(it["name"])
            figs.append(f'<figure class="wide2"><div class="pics">{pics}</div><figcaption><b>{html.escape(it["title"])}</b>'
                        f'<span>{html.escape(it["report"])}</span>{prompt_html(spec) if spec else ""}</figcaption></figure>')
        for c in b.get("images", []):
            if Path(c["src"]).exists():
                figs.append(f'<figure class="wide2"><img src="img/{shrink(Path(c["src"]), img / (k + "-" + tag + "-" + c["id"]), 2000)}" alt="{html.escape(c["label"])}" loading="lazy">'
                            f'<figcaption><b>{html.escape(c["label"])}</b><span>{html.escape(c["note"])}</span></figcaption></figure>')
        blocks.append('<div class="block"><h3>' + html.escape(b["title"]) + '</h3><p class="legend">' + html.escape(b["legend"]) + '</p>'
                      '<div class="refs cliptests">' + "".join(figs) + '</div></div>')
    return "".join(blocks)


def hero_block(k: str, e: dict, out: Path, img: Path) -> str:
    """Free HERO motion pre-viz on stand-in pieces (hero_previz_<ep>.py, before narration exists): per shot the preview
    (a click marks each key word) and its start / key / end sheet."""
    p, arts, real = e.get("project"), [], []
    for sid, cap in e.get("hero_real", []):
        rev = p / "review/hero"
        if not web_preview(rev / f"{sid}-real.mp4", out / "video" / f"{p.name}-hero-{sid}-real.mp4"):
            continue
        sheet = rev / f"{sid}-real-sheet.jpg"
        sh = (f'<img class="wide" src="img/{shrink(sheet, img / f"{k}-hero-{sid}-real-sheet", 1500)}" alt="Start, key and end '
              f'frames of shot {sid} on the real pieces" loading="lazy">') if sheet.exists() else ""
        real.append(f'<article class="hero"><h4>{html.escape(cap)}</h4><video class="cut" controls playsinline loop '
                    f'preload="metadata" src="video/{p.name}-hero-{sid}-real.mp4"></video>{sh}</article>')
    if real:
        pcs = e.get("hero_pieces")
        pimg = (f'<img class="wide" src="img/{shrink(pcs, img / f"{k}-hero-pieces", 1800)}" alt="The paid pieces: cast sheets, '
                f'sprite and pose sheets, plates" loading="lazy">') if pcs and pcs.exists() else ""
        real = ['<div class="block"><h3>HERO shots on the REAL pieces (the recorded narration, real word times)</h3><p class="legend">'
                'The approved motion, unchanged, on the paid pieces: every key moved from the estimated word to the word Liam '
                'says; the sound is the narration. Green box = the moving piece at its key (≥ 1/3); dashed lines = the safe zone.'
                '</p>' + pimg] + real + ["</div>"]
    for sid, cap in e.get("hero_previz", []):
        rev = p / "review/hero"
        if not web_preview(rev / f"{sid}-preview.mp4", out / "video" / f"{p.name}-hero-{sid}.mp4"):
            continue
        sheet = rev / f"{sid}-sheet.jpg"
        sh = (f'<img class="wide" src="img/{shrink(sheet, img / f"{k}-hero-{sid}-sheet", 1500)}" alt="Start, key and end '
              f'frames of shot {sid}" loading="lazy">') if sheet.exists() else ""
        arts.append(f'<article class="hero"><h4>{html.escape(cap)}</h4><video class="cut" controls playsinline loop '
                    f'preload="metadata" src="video/{p.name}-hero-{sid}.mp4"></video>{sh}</article>')
    if not arts:
        return "".join(real)
    return "".join(real) + ('<div class="block"><h3>HERO motion pre-viz (free stand-in pieces, word times estimated)</h3><p class="legend">'
            'Drawn stand-ins with the same names, states and sizes as the paid pieces (cm, L51). Green box = the moving piece at its key '
            '(≥ 1/3 of the frame); dashed lines = the Shorts safe zone; a click marks each key word. Nothing paid.</p>'
            + "".join(arts) + "</div>")


def layered_block(k: str, e: dict, ep: dict, out: Path, img: Path) -> str:
    """Layered shots (user 2026-11-16, .claude/skills/layered-shot): per shot the 3 s preview with sound, the contact
    sheet, the layer plan, the free stand-in pieces and the prompts of the paid pieces (waiting for the user's OK)."""
    sys.path.insert(0, str(Path(__file__).parent))
    import layers
    p = e.get("project")
    if not p:
        return ""
    arts = []
    for s in ep.get("shots", []):
        if not s.get("layers"):
            continue
        sid = s["id"]
        rev = p / "review/layers"
        vid = ""
        if web_preview(rev / f"{sid}-preview.mp4", out / "video" / f"{p.name}-{sid}-layers.mp4"):
            vid = (f'<video class="cut" controls playsinline loop preload="metadata" '
                   f'src="video/{p.name}-{sid}-layers.mp4"></video>')
        sheet = ""
        if (rev / f"{sid}-sheet.jpg").exists():
            sheet = (f'<img class="wide" src="img/{shrink(rev / f"{sid}-sheet.jpg", img / f"{k}-{sid}-layersheet", 1500)}" '
                     f'alt="Start, middle and end frames of the layered shot" loading="lazy">')
        plan = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>"
                       for a, b, c in layers.layer_plan(s))
        stand = []
        bg = (s["layers"].get("bg") or "")
        if bg:
            f = Path(p / bg.split(":", 1)[-1]) if bg.startswith("proj:") else Path(bg)
            if f.exists():
                cap = ('<b>Plate (free stand-in)</b><span>' + html.escape(f.name) + ': ' + html.escape(e.get("plate_note",
                       "the mosquito painted out locally. The paid plate repaints it cleanly.")) + '</span>') if ".free" in f.name else (
                      '<b>Plate (real, $0.067)</b><span>The same painting repainted without the mosquito; it lines up with '
                      'the still within 1.5 px, so the landing spot holds.</span>')
                stand.append(f'<figure><img src="img/{shrink(f, img / f"{k}-{sid}-plate", 900)}" alt="Plate without the mosquito" loading="lazy">'
                             f'<figcaption>{cap}</figcaption></figure>')
        for a in s["layers"].get("actors", []):
            sp = a.get("sprites", "")
            f = (p / sp.split(":", 1)[-1]).parent / "check.png" if sp.startswith("proj:") else None
            if f and f.exists():
                chk_name = f"{k}-{sid}-{a['id']}-check"
                stand.append(f'<figure><img src="img/{shrink(f, img / chk_name, 1300)}" alt="Cut-outs over magenta" loading="lazy">'
                             + (f'<figcaption><b>{html.escape(a["id"])}: cut-outs (free stand-in)</b><span>Every state over '
                                f'magenta, and the onion skin: one body outline means it doesn’t jump when the wings fold.</span>'
                                if "free" in sp else
                                f'<figcaption><b>{html.escape(a["id"])}: real cut-outs ($0.067 sheet)</b><span>Wing beat (2 frames), '
                                f'the fold (2 frames), at rest. The sheet gave 2 top-down frames and 2 side views; the side views '
                                f'don’t match a camera looking down at the hand, so the beat and the fold are made from the '
                                f'top-down frame by turning each wing at its root.</span>')
                             + '</figcaption></figure>')
        hero = e.get("hero", {}).get(sid)
        if hero:   # user 2026-11-18: the shot in plain words + every piece's picture and full prompt beside the preview
            arts.append(f'<article class="layered"><div class="head"><span class="num">{html.escape(hero.get("label", sid))}</span>'
                        f'<span class="chip">{s["end"] - s["start"]:.1f} s</span><span class="size">{html.escape(sid)} · layered · real pieces</span></div>'
                        f'<div class="lgrid">{vid}<div class="cast"><p class="desc">{hero["desc"]}</p>'
                        f'<details><summary>Layers and motion</summary><table><tr><th>Layer</th><th>What</th><th>Motion</th></tr>{plan}</table></details></div></div>'
                        f'{sheet}{hero_pieces(k, sid, hero, ep, p, img)}</article>')
            continue
        arts.append(f'<article class="layered"><div class="head"><span class="num">{html.escape(Path(str(s["source"])).stem)}</span>'
                    f'<span class="chip">{s["end"] - s["start"]:.1f} s</span><span class="size">{html.escape(sid)} · layered</span></div>'
                    f'<div class="lgrid">{vid}<div class="cast"><table><tr><th>Layer</th><th>What</th><th>Motion</th></tr>{plan}</table></div></div>'
                    f'{sheet}<div class="refs">{"".join(stand)}</div></article>')
    if not arts:
        return ""
    pieces = []
    tot = 0.0
    try:
        import google_images as g
    except Exception:
        g = None
    for rn, spec in ep.get("references", {}).items():
        if "for cut-out animation" not in spec.get("prompt", "").lower():
            continue
        made = (p / "assets/images/refs" / f"{rn}.png").exists()
        usd = g.price(spec.get("model", "gemini-3-pro-image"), spec.get("resolution", ep.get("image_resolution", "2K")), True) if g else 0
        tot += 0 if made else usd
        pieces.append(f'<article><b>{html.escape(rn)}</b><span class="st {"" if made else "new"}">'
                      f'{"made" if made else f"waiting for your OK · ${usd:.3f}"}</span>'
                      f'{prompt_html(spec).replace("<details", "<details open", 1)}</article>')
    if e.get("hero") and e.get("layered_lede"):   # prompts already sit beside each shot
        return (f'<div class="block"><h3>{html.escape(e.get("layered_title", "Layered shots"))}</h3>'
                f'<p class="lede">{e["layered_lede"].replace("{tot}", f"{tot:.2f}")}</p>{"".join(arts)}</div>')
    if tot == 0 and pieces and not e.get("layered_lede"):
        return (f'<div class="block"><h3>Layered shots: our own animation (pilot)</h3>'
                f'<p class="lede">The preview now runs on the <b>real pieces</b> (made 2026-11-16, $0.134): the plate without the '
                f'mosquito and the cut-out mosquito, warmed to the lamp’s light. Same motion you approved.</p>'
                f'{"".join(arts)}'
                f'<details><summary>The two prompts</summary><div class="refgen">{"".join(pieces)}</div></details></div>')
    if e.get("layered_lede"):
        return (f'<div class="block"><h3>{html.escape(e.get("layered_title", "Layered shots"))}</h3>'
                f'<p class="lede">{e["layered_lede"].replace("{tot}", f"{tot:.2f}")}</p>{"".join(arts)}'
                f'<h3>The paid pieces (prompts)</h3><div class="refgen">{"".join(pieces)}</div></div>')
    return (f'<div class="block"><h3>Layered shots: our own animation (pilot)</h3>'
            f'<p class="lede">The preview runs on free stand-ins: the plate with the mosquito painted out on this machine, '
            f'and a drawn mosquito. It shows the MOTION: the path, the landing on “suspect”, the wings folding, the shadow on the skin, '
            f'the buzz stopping. The paid pieces below replace the stand-ins (Gemini Batch, <b>${tot:.2f}</b> together).</p>'
            f'{"".join(arts)}'
            f'<h3>The two paid pieces (prompts)</h3><div class="refgen">{"".join(pieces)}</div></div>')


def shrink(src: Path, dst: Path, edge: int = 900):
    im = Image.open(src).convert("RGB")
    im.thumbnail((edge, edge))
    im.save(dst.with_suffix(".jpg"), quality=82)
    return dst.with_suffix(".jpg").name


CSS = """
:root{--bg:#f3eee3;--surface:#fbf8f1;--ink:#22262a;--muted:#5d625f;--line:#d9cfbd;--amber:#b8740f;--amber-soft:#f4dfb6;--teal:#1f4e5a;--teal-soft:#d5e4e4;--s1:#2f6fc0;--s2:#c07a12;
--display:'Montserrat',system-ui,sans-serif;--body:'Inter',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1a1d20;--surface:#23282c;--ink:#efe6d2;--muted:#a9a99f;--line:#3a4044;--amber:#e8a33d;--amber-soft:#4a3a1e;--teal:#8cc0c4;--teal-soft:#1f3a40;--s1:#4a86d0;--s2:#b9781a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1a1d20;--surface:#23282c;--ink:#efe6d2;--muted:#a9a99f;--line:#3a4044;--amber:#e8a33d;--amber-soft:#4a3a1e;--teal:#8cc0c4;--teal-soft:#1f3a40;--s1:#4a86d0;--s2:#b9781a;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.55}
.wrap{max-width:1180px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.01em;text-wrap:balance;margin:0}
h1{font-size:clamp(26px,4vw,38px)} h2{font-size:clamp(22px,3vw,30px)} h3{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}
.kicker{font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber)}
.lede{color:var(--muted);max-width:68ch;margin:10px 0 0}
nav{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 8px}
nav a{font-family:var(--display);font-weight:700;font-size:13px;padding:8px 14px;border-radius:999px;background:var(--surface);border:1px solid var(--line);color:var(--ink);text-decoration:none}
nav a:hover,nav a:focus-visible{border-color:var(--amber);outline:none}
section.ep{margin-top:44px;padding-top:12px;border-top:3px solid var(--ink)}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 0 0;color:var(--muted);font-size:14px;font-variant-numeric:tabular-nums}
.meta b{color:var(--ink)}
.block{margin-top:28px;display:grid;gap:12px;grid-template-columns:minmax(0,1fr)}
.notes{background:var(--teal-soft);border-radius:10px;padding:14px 18px;display:grid;gap:8px;font-size:14px}
.notes p{margin:0}
.script{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:6px;font-size:15px}
.script p{margin:0}.tag{font-family:var(--mono);font-size:12px;color:var(--teal);margin-right:6px}
.refs{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
figure img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top;display:block;cursor:zoom-in;background:var(--line)}
figcaption{padding:10px 12px;display:grid;gap:4px;font-size:13px;min-width:0}
figcaption b{font-family:var(--display);font-size:14px}
.credit{color:var(--muted);font-size:11.5px}
.cast{overflow-x:auto}
.cast table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:560px}
.cast td,.cast th{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
.cast th{font-family:var(--display);font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.maps{display:flex;flex-wrap:wrap;gap:14px}.maps img{max-width:min(420px,100%);border-radius:10px;border:1px solid var(--line);cursor:zoom-in}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,520px),1fr));gap:16px}
.shot{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;grid-template-columns:150px 1fr;gap:14px;align-items:start}
.shot img{width:150px;aspect-ratio:9/16;border-radius:6px;display:block;cursor:zoom-in;border:1px solid var(--line)}
.shot .info{min-width:0;display:grid;gap:8px}
.head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.num{font-family:var(--display);font-weight:800;font-size:22px}
.chip{font-family:var(--mono);font-size:12px;background:var(--amber-soft);color:var(--ink);padding:2px 8px;border-radius:999px;font-variant-numeric:tabular-nums}
.size{font-family:var(--mono);font-size:12px;color:var(--teal)}
.line{font-size:15.5px;margin:0}.line strong{color:var(--amber)}
.shot dl{margin:0;display:grid;grid-template-columns:62px 1fr;gap:4px 10px;font-size:13.5px}
.shot dt{font-family:var(--display);font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding-top:2px}
.shot dd{margin:0;min-width:0}
.legend{font-size:13px;color:var(--muted)}
.legend span{display:inline-block;width:26px;height:10px;background:var(--amber-soft);border:1px solid var(--amber);vertical-align:middle;margin-right:6px;border-radius:2px}
.ask{margin-top:48px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px;display:grid;gap:6px}
.ask p{margin:0}
details.prompt{border-top:1px dashed var(--line);padding-top:8px;font-size:13px}
details.prompt summary{cursor:pointer;font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--teal)}
details.prompt p{margin:6px 0 0;overflow-wrap:anywhere}.pmeta{font-family:var(--mono);font-size:11.5px;color:var(--muted)}
.roles{color:var(--muted);font-style:italic}
.pics{display:grid;gap:6px;justify-items:start}.pics small{font-family:var(--mono);font-size:11px;color:var(--muted)}
.refgen{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:14px}
.refgen article{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:grid;gap:6px;min-width:0}
.refgen b{font-family:var(--display)}
video.cut{width:min(360px,100%);aspect-ratio:9/16;border-radius:12px;background:#000;display:block}
.ar16 video.cut{width:min(760px,100%);aspect-ratio:16/9}
.cliptests{grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr))}.cliptests figure img{aspect-ratio:16/9;object-fit:cover}.cliptests figure.wide2{grid-column:1/-1}.cliptests figure.wide2 img{aspect-ratio:auto;object-fit:contain}.cliptests video.cut{width:100%}.cliptests .pics{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:8px}.cliptests .pics img{width:100%;height:auto;aspect-ratio:16/9;object-fit:contain}.cliptests .pics small{grid-column:1/-1}
.ar16 .shot{grid-template-columns:300px 1fr}.ar16 .shot img{width:300px;aspect-ratio:16/9}
.ar16 .v2grid article{grid-template-columns:150px 1fr}.ar16 .v2grid img,.ar16 .newpic{width:150px;aspect-ratio:16/9}
.story{background:var(--surface);border:2px solid var(--amber);border-radius:14px;padding:18px 20px}
.story h3{margin-top:10px}
.chart{display:grid;gap:6px}.key{display:flex;gap:16px;font-size:13px;color:var(--muted)}
.sw{display:inline-block;width:18px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}
.sw.v1{background:var(--s1)}.sw.v2{background:var(--s2)}
svg.tension{width:100%;max-width:680px;height:auto}
svg.tension .g{stroke:var(--line);stroke-width:1}svg.tension .ax{fill:var(--muted);font:11px var(--mono)}
svg.tension .l{fill:none;stroke-width:2;stroke-linejoin:round}svg.tension .l.v1{stroke:var(--s1)}svg.tension .l.v2{stroke:var(--s2)}
svg.tension .d{stroke:var(--surface);stroke-width:2}svg.tension .d.v1{fill:var(--s1)}svg.tension .d.v2{fill:var(--s2)}
svg.tension .lab{fill:var(--ink);font:700 12px var(--display)}
.spine{margin:0;padding-left:18px;display:grid;gap:3px;font-size:14px}
.beat{font-family:var(--mono);font-size:12px;white-space:nowrap}.tn{font-family:var(--mono);white-space:nowrap}
.v2grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:12px}
.v2grid article{display:grid;grid-template-columns:84px 1fr;gap:12px;border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--bg);font-size:13.5px}
.v2grid article p{margin:4px 0 0}.v2grid .muted{color:var(--muted);font-size:12.5px}
.v2grid img,.newpic{width:84px;aspect-ratio:9/16;border-radius:6px;object-fit:cover;cursor:zoom-in}
.newpic{display:grid;place-items:center;border:2px dashed var(--amber);color:var(--amber);font:700 11px var(--display);text-align:center}
.v2grid article.drop{opacity:.55}
.st{font:700 11px var(--display);letter-spacing:.06em;padding:2px 8px;border-radius:999px;background:var(--line)}
.st.redo,.st.new{background:var(--amber-soft);color:var(--ink)}
.layered{background:var(--surface);border:2px solid var(--teal);border-radius:14px;padding:14px;display:grid;gap:14px;margin-top:12px}
.layered .desc{margin:0 0 10px;font-size:1.02rem;line-height:1.5}.pieces{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:14px}.piece{background:var(--bg);border-radius:10px;padding:10px;display:grid;gap:8px;align-content:start}.piece figure{margin:0}.piece img{width:100%;height:auto;border-radius:6px;cursor:zoom-in}.piece figcaption{display:grid;gap:2px;margin-top:6px}.piece .full{white-space:pre-wrap;font-size:.84rem;line-height:1.45;overflow-wrap:anywhere}
.lgrid{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:16px;align-items:start}
img.wide{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);cursor:zoom-in}
.layered figure img{aspect-ratio:auto;object-fit:contain;background:var(--bg)}
.layered .refs{grid-template-columns:minmax(0,220px) minmax(0,1fr)}
.refgen .st{justify-self:start}
@media (max-width:640px){.layered .refs{grid-template-columns:minmax(0,1fr)}}
@media (max-width:640px){.lgrid{grid-template-columns:minmax(0,1fr)}}
#lb{position:fixed;inset:0;background:rgba(10,12,14,.88);display:flex;align-items:center;justify-content:center;padding:24px;z-index:20;cursor:zoom-out}
#lb[hidden]{display:none}
#lb img{max-width:100%;max-height:100%;border-radius:6px}
@media (max-width:560px){.shot{grid-template-columns:110px 1fr}.shot img{width:110px}.shot dl{grid-template-columns:1fr}.shot dt{padding-top:6px}}
@media (prefers-reduced-motion:no-preference){nav a{transition:border-color .15s}}
"""


def build(out: Path, keys: list[str]) -> Path:
    img = out / "img"
    img.mkdir(parents=True, exist_ok=True)
    eps = [(k, EPISODES[k], parse(EPISODES[k]["storyboard"])) for k in keys]
    # L50 (story-craft Rule 0b, 2026-11-19): every violent row names its softening tool (`0b: ...`). Storyboards made
    # before the rule carry "lint_0b": "warn".
    for k in keys:
        issues = storyboard_lint.lint_file(EPISODES[k]["storyboard"])
        for m in issues:
            print(("WARN " if EPISODES[k].get("lint_0b") == "warn" else "") + m)
        if issues and EPISODES[k].get("lint_0b") != "warn":
            raise SystemExit(f"{k}: {len(issues)} violent row(s) without a Rule 0b softening tool (L50)")
    nav = "".join(f'<a href="#{e["anchor"]}">{html.escape(p["title"].split(" — ")[0])} · {e["short"]}</a>' for k, e, p in eps)
    body = []
    stages = []
    pilots: list[str] = []
    for k, e, p in eps:
        ep = episode_json(e)
        kf_dir = e.get("project", Path("-")) / "assets/images/keyframes"
        ref_dir = e.get("project", Path("-")) / "assets/images/refs"
        has_imgs = any((kf_dir / f"{n}.png").exists() for n in ep.get("keyframes", {}))
        stage = ("images · waiting for your OK" if has_imgs else
                 "image prompts · waiting for your OK" if ep.get("previz_approved") and ep.get("keyframes") else
                 "storyboard + pre-viz · waiting for your OK")
        stages.append(stage)
        n_img, img_usd = image_cost(ep)
        vid = ""
        if e.get("project") and web_preview(e["project"] / "renders/final.mp4", out / "video" / f"{e['project'].name}.mp4"):
            vid = (f'<div class="block"><h3>Rough cut (watch with sound)</h3><video class="cut" controls playsinline '
                   f'preload="metadata" src="video/{e["project"].name}.mp4"></video></div>')
            if not e.get("story"):
                stage = "rough cut · waiting for your OK"
                stages[-1] = stage
        story = story_block(k, e, img)
        layered = preview_block(k, e, out) + review_block(k, e, out, img) + layered_block(k, e, ep, out, img) + hero_block(k, e, out, img) + clip_tests_block(k, e, out, img) + batch1_block(k, e, ep, out, img)
        if layered:
            pilots.append(e["short"])
        if story:
            stage = stages[-1] = ("rough cut 2 · waiting for your OK" if all((kf_dir / f"{n}.png").exists() for n in ep.get("keyframes", {}))
                                  else "v2 sketches + prompts · waiting for your OK")
        if layered:
            stage = stages[-1] = "layered pilot · real pieces · waiting for your OK"
        if e.get("status"):
            stage = stages[-1] = e["status"]
        # reference images to make (cast sheets, set plates) with their prompts
        refgen = []
        for rn, spec in ep.get("references", {}).items():
            done = ref_dir / f"{rn}.png"
            pic = ""
            if done.exists():
                pic = f'<img src="img/{shrink(done, img / f"{k}-gen-{rn}", 1100)}" alt="{html.escape(rn)}" loading="lazy">'
            refgen.append(f'<article><b>{html.escape(rn)}</b>{pic}{prompt_html(spec).replace("<details", "<details open", 0)}</article>')
        # script
        sc = []
        for ln in p["script"]:
            m = re.match(r"^\[(\w+)\]\s*(.*)$", ln)
            sc.append(f'<p><span class="tag">[{m.group(1)}]</span>{inline(m.group(2))}</p>' if m else f"<p>{inline(ln)}</p>")
        # refs
        figs = []
        for fn, name, note, credit in e["refs"]:
            src = e["refs_dir"] / fn
            if not src.exists():
                continue
            local = shrink(src, img / f"{k}-ref-{Path(fn).stem}")
            figs.append(f'<figure><img src="img/{local}" alt="{html.escape(name)}" loading="lazy">'
                        f'<figcaption><b>{html.escape(name)}</b><span>{html.escape(note)}</span>'
                        f'<span class="credit">{html.escape(credit)}</span></figcaption></figure>')
        maps = []
        for mp in e["maps"]:
            if (e["previz"] / mp).exists():
                local = shrink(e["previz"] / mp, img / f"{k}-{Path(mp).stem}", 1100)
                maps.append(f'<img src="img/{local}" alt="Set map: camera positions" loading="lazy">')
        cast = "".join(f"<tr><td>{inline(r[0])}</td><td>{inline(r[1])}</td><td>{inline(r[2])}</td></tr>"
                       for r in p["cast"] if len(r) >= 3)
        cards = []
        for r in p["shots"]:
            if len(r) < 8:
                continue
            n, s, line, size, see, fx, txt, sfx = r[:8]
            fr = e["previz"] / f"{n}.png"
            pics = []
            if fr.exists():
                shutil.copy(fr, img / f"{k}-{n}.png")
                pics.append(f'<img src="img/{k}-{n}.png" alt="Pre-viz sketch, shot {html.escape(n)}" loading="lazy"><small>sketch</small>')
            kf = kf_dir / f"s{n}.png"
            redo = "**REDO**" in see
            if kf.exists():
                pics.append(f'<img src="img/{shrink(kf, img / f"{k}-kf-{n}", 900)}" alt="Image, shot {html.escape(n)}" loading="lazy">'
                            f'<small>{"rough cut 1 image: being REDONE" if redo else "image"}</small>')
            elif "**NEW**" in see:
                pics.append('<small>new image: after your OK</small>')
            pic = f'<div class="pics">{"".join(pics)}</div>'
            spec = ep.get("keyframes", {}).get(f"s{n}")
            ptxt = prompt_html(spec) if spec else ""
            cards.append(
                f'<article class="shot">{pic}<div class="info"><div class="head"><span class="num">{html.escape(n)}</span>'
                f'<span class="chip">{html.escape(s)} s</span><span class="size">{inline(size)}</span></div>'
                f'<p class="line">“{inline(line)}”</p><dl><dt>We see</dt><dd>{inline(see)}</dd>'
                f'<dt>Motion</dt><dd>{inline(fx)}</dd><dt>Text</dt><dd>{inline(txt)}</dd>'
                f'<dt>Sound</dt><dd>{inline(sfx)}</dd></dl>{ptxt}</div></article>')
        notes = "".join(f"<p>{inline(n)}</p>" for n in p["notes"])
        body.append(f"""
<section class="ep{" ar16" if e.get("aspect") == "16:9" else ""}" id="{e['anchor']}">
  <div class="kicker">{html.escape(k.upper())} · {html.escape(e['slot'])}</div>
  <h2>{html.escape(p['title'].split(' — ', 1)[-1])}</h2>
  <div class="meta"><span><b>{len(cards)}</b> shots</span><span>≈ <b>{p['secs']:.0f} s</b> of pictures</span>
  <span>{f"images <b>{n_img}</b> · <b>${img_usd:.2f}</b> (Gemini Batch) + narration and music ≈ <b>$0.13</b>" if n_img else f"estimate <b>{html.escape(p['cost'])}</b>"}</span>
  <span>status <b>{html.escape(stage)}</b></span></div>
  {layered}
  {story}
  {vid}
  <div class="block"><h3>Notes and period rules</h3><div class="notes">{notes}</div></div>
  <div class="block"><h3>{html.escape(e.get("script_heading", "Script v2 (approved, recorded)"))}</h3><div class="script">{''.join(sc)}</div></div>
  <div class="block"><h3>People and places: the real pictures we follow</h3><div class="refs">{''.join(figs)}</div></div>
  <div class="block"><h3>Cast and sets</h3><div class="cast"><table><tr><th>Who / where</th><th>Look</th><th>Shots</th></tr>{cast}</table></div></div>
  <div class="block"><h3>Set map (where each camera stands)</h3><div class="maps">{''.join(maps)}</div></div>
  {f'<div class="block"><h3>Reference images made first (cast sheets and empty sets)</h3><div class="refgen">{"".join(refgen)}</div></div>' if refgen else ''}
  <div class="block"><h3>Shots</h3><p class="legend"><span></span>orange band = where the on-screen text sits · dotted lines = the Shorts safe zone</p>
  <div class="shots">{''.join(cards)}</div></div>
  {"".join(md_section(f) for f in e.get("extra", []))}
</section>""")
    first = eps[0][1]
    if first.get("h1"):
        h1, lede, ask = first["h1"], first["lede"], first["ask"]
    elif pilots:
        h1 = "Layered animation pilot: Finlay’s mosquito"
        lede = ("Our own animation instead of AI clips: the painting becomes layers (a clean plate, a mosquito cut out in four "
                "states, a shadow, the lamp’s glow) and we move them with keyframes, like After Effects. Watch the 3 s preview "
                "with sound at the top of Finlay. Both Shorts’ storyboards stay below for reference. Tap any picture to enlarge it.")
        ask = ("<p><b>The real mosquito</b> (the preview at the top of Finlay): the same motion you approved, now with the "
               "real plate and the real mosquito. Check the wing beat in flight, the landing on “suspect”, the wings folding "
               "and that it sits on the skin, not on top of the picture.</p>"
               "<p>After your OK: the full Finlay render, the text check, and a new short.mp4 in the package.</p>")
    else:
        h1 = "Next two Shorts: rough cut 2"
        lede = ("Round 2 (after your rough-cut review): each Short now starts with the proposed story v2, its tension curve against rough cut 1, and which shots stay, get fixed, are redone or are new. Below it: rough cut 1 and the approved v1 storyboard for reference. Each shot shows a rough sketch of the framing (people as silhouettes, where the text goes), the narration line it covers, and what the painting will show. The real portraits and period pictures set how people and places look. Tap any picture to enlarge it.")
        ask = ("<p>Rough cut 2 is at the top of each Short (watch with sound): story v2, the 11 new images, the silent climaxes. Tell me by time or shot number what to change, or say it is ready for covers and publish packages. Reply in chat with the shot numbers you want changed (for example \"al-Razi 6: Matt holds the lamp higher\"), or say both are OK. The order is always: storyboard and sketches, then the image prompts (open \"Image prompt\" under any shot), then the images. Nothing is paid for until you approve the step before it.</p>")
    page = f"""<title>{html.escape(first.get("page_title", "Finlay and al-Razi Storyboards"))}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400&family=Montserrat:wght@700;800&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <div class="kicker">Oddly Matt · approval page · {html.escape(first.get("status") or "layered pilot · real pieces · waiting for your OK" if first.get("status") or pilots else (stages[0] if len(set(stages)) == 1 else ", ".join(stages)))}</div>
  <h1>{html.escape(h1)}</h1>
  <p class="lede">{html.escape(lede)}</p>
  <nav>{nav}</nav>
  {''.join(body)}
  <div class="ask"><h3>What I need from you</h3>{ask}</div>
</div>
<div id="lb" hidden><img alt=""></div>
<script>
const lb=document.getElementById('lb'),lbi=lb.querySelector('img');
document.addEventListener('click',e=>{{const t=e.target;if(t.tagName==='IMG'&&t.closest('figure,.shot,.maps,.v2grid,.layered,.piece')){{lbi.src=t.src;lbi.alt=t.alt;lb.hidden=false}}else if(t.closest('#lb')){{lb.hidden=true}}}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.hidden=true}});
</script>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    return out / "index.html"


if __name__ == "__main__":
    print(build(Path(sys.argv[1]), sys.argv[2:] or ["hcs07", "hcs05"]))
