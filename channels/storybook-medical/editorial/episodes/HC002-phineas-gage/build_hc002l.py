"""HC002-L Gage long: projects/hc002-l/episode.json from the approved, fact-gated script (script-long-v1.md; user
2026-11-21: changed lines approved, record the narration) and the approved storyboard (long-storyboard-v1.md +
long-backgrounds-v1.md; user 2026-11-22: images approved, usual order: cast + HERO pieces first, shown, then the rest).
The narration chapters are read straight from the script table, so what Liam reads is exactly what the gate passed
(fact-gate/2026-11-21-long-script.md):
  - one chapter per "## N · ..." section, one script row per line, the row's `[tag]`s kept as ElevenLabs v3 tags;
  - struck-through rows (~~...~~, e.g. row 51) are skipped;
  - gap_after: 3.3 s after the cold open (sting 1.8 s + title), 1.2 s between chapters (as HC001-L).
Images (16:9 film): root-cause rule L40 / L55: NO set plate and NO keyframe is ever a reference; S1's plates are not
passed either (they were made before the rule): only the real cut photo (rock) and S1's small light detail (style).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/build_hc002l.py [--print]
    python channels/storybook-medical/scripts/episode.py narrate hc002-l                       (done 2026-11-21)
    python channels/storybook-medical/scripts/episode.py refs hc002-l sheet-harlow sheet-gage-chile --batch
    python channels/storybook-medical/scripts/episode.py refs hc002-l <HERO_PIECES> --batch
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (EMPTY_HANDS, FULL_BLEED, KEY_BG, NO_TEXT, ONE_EACH, PERIOD, REF_IDENTITY_ONLY, SAFE_FRAMING, OTS_FRAMING,  # noqa: E402
                        WAVY_WRITING, camera, cast, crowd, framing, lint_all, matt_beat, pose_sheet, scale, set_block, sprite_sheet)

PID = "hc002-l"
P = REPO / "projects" / PID
S1 = "projects/hc002-s1/assets/images/refs"
SHEET_LAYOUT = "projects/hc001-window-into-his-stomach/assets/images/refs/sheet-osler.png"
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "


def chapters() -> list[dict]:
    out, cur = [], None
    for line in (HERE / "script-long-v1.md").read_text(encoding="utf-8").splitlines():
        h = re.match(r"## (\d+) · (.+?) \(", line)
        if h:
            cur = {"id": f"ch{h.group(1)}", "title": h.group(2).strip(), "rows": []}
            out.append(cur)
            continue
        if line.startswith("## "):
            cur = None
            continue
        m = re.match(r"\| (\d+) \| (.*?) \| .* \| [^|]* \|\s*$", line)
        if cur is None or not m or "~~" in m.group(2):
            continue
        text = re.sub(r"`(\[[^\]]+\])`", r"\1", m.group(2)).strip()
        cur["rows"].append((int(m.group(1)), text))
    return out


def sizes(items: dict) -> str:
    """SCALE line for pieces that must stay EMPTY of hands (L47): sizes only, no hand as the ruler."""
    return "SCALE (true sizes, keep these proportions): " + "; ".join(f"{k} {v}" for k, v in items.items()) + "."


# ── people ──────────────────────────────────────────────────────────────────────────────────────────────────────────
HARLOW = ("DR JOHN MARTYN HARLOW, the country doctor of Cavendish (29 in 1848: a long oval face, a high forehead, dark-brown "
          "hair brushed back, a short neatly trimmed dark-brown beard and moustache, kind deep-set eyes; a dark frock coat, a "
          "dark waistcoat, a white shirt with a high collar and a black neck-cloth)")
GAGE_CHILE = ("PHINEAS GAGE in Chile in the 1850s (about 30: the same strong square-jawed face, clean-shaven, thick dark hair; "
              "his LEFT eye closed for good, lid shut and a little sunken (L48: in a front view that is on the RIGHT side of the "
              "picture), a faint pale scar high on the left side of his forehead under the hair; no bandage, no wound, no "
              "blood; calm)")
G1848, GCH, HARLOW_REF = f"{S1}/sheet-gage-1848.png", "ref:sheet-gage-chile", "ref:sheet-harlow"
STYLE_DETAIL = "projects/hc002-s1/refs/s8_light_detail.png"
STYLE_ROLE = ("Reference 1 is a small painted DETAIL of our film (grey rock, settling smoke, slanting light): copy ONLY its "
              "painting style, ink line and palette; it is not a camera, a composition or a place. ")

REFERENCES = {
    "sheet-harlow": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/harlow_john_martyn.jpg"],
        roles=(SHEET + "Reference 2 is an engraved portrait of the real Dr John Martyn Harlow in OLD age (grey hair, full grey "
               "beard): paint THIS face (the long oval face, high forehead, nose, deep-set eyes, the beard's shape) in our "
               "storybook style, YOUNGER, as he was at 29 in 1848, with dark-brown hair and a SHORT trimmed dark beard; "
               "never as an engraving, and do not copy its pose or frame. "),
        prompt=(f"Clean character model sheet on plain bone-white paper: {HARLOW}. Front view, three-quarter view, profile "
                "view facing RIGHT, back view, all from the waist up, plus three head close-ups (calm, rolling up his shirt "
                "cuffs; writing, looking down; older at 48 in 1867, the beard and hair streaked with grey). Same scale in "
                "every view. Clearly NOT Phineas Gage (Gage is clean-shaven). No text, labels or watermark.")),
    "sheet-gage-chile": dict(aspect="16:9", refs=[G1848, "projects/hc002-s1/refs/gage_miller.jpg"],
        roles=("Reference 1 is the approved model sheet of PHINEAS GAGE in 1848: the same man, face, hair, build and layout; "
               "here he is a few years older and his left eye is closed for good. Reference 2 is a period photograph of the "
               "real Phineas Gage in the 1850s: his face as it was then (the closed left eye, the hair), painted in our "
               "storybook style, never as a photograph, and do not copy its pose or the iron. "),
        prompt=(f"Clean character model sheet on plain bone-white paper: {GAGE_CHILE}. Two outfits: (A) as a coach driver in "
                "Chile: a short dark wool jacket over a white shirt, a cotton scarf loose at the neck against the dust, a "
                "broad-brimmed low felt hat, dark trousers, boots; (B) dressed up for a portrait: a dark frock coat, a "
                "waistcoat, a white shirt with a dark cravat, no hat. Outfit A in front view, three-quarter view and profile "
                "facing LEFT, full figure; outfit B in front view, waist up; plus two head close-ups (steady, eyes on the "
                "road; a small smile). In EVERY view his LEFT eye is closed and the right eye open. Same scale in every view. "
                "No text, labels or watermark.")),
}

# ── HERO pieces (16:9) ───────────────────────────────────────────────────────────────────────────────────────────────
CUT = set_block("The railroad rock cut near Cavendish, Vermont", "13 September 1848",
                "a fresh cut through grey schist rock with raw, layered walls and a rough ledge; drill holes; small wooden "
                "kegs of blasting powder (plain wood, no lettering); wooded hills in early autumn colour beyond")
CUT_PHOTO = ("Reference 2 is a modern photograph of the real cut, used ONLY for the rock: grey layered schist walls; ignore "
             "the modern trees, rails and road. ")
CREW_REF = f"{S1}/sheet-crew.png"
ROAD = set_block("a mountain coach road between Valparaíso and Santiago, Chile", "the 1850s",
                 "a dusty pale road cut along a dry mountain slope, the coastal range in hazy layers behind, cactus, thorny "
                 "scrub and boulders, hard bright sun")
R49_LIGHT = "hard midday sun from the upper RIGHT, short shadows to the lower left, a warm dusty haze"

REFERENCES.update({
    # row 2 (S1 shot 4 in 16:9): OTS from the pit; NO Gage (S1's head-turn pose sprites go on it)
    "plate-r2": dict(aspect="16:9", refs=[STYLE_DETAIL, "projects/hc002-s1/refs/cavendish_cut.jpg", CREW_REF],
        roles=STYLE_ROLE + CUT_PHOTO + "Reference 3 is the crew line-up: only TWO of them, seen from BEHIND (the grey-bearded driller and the heavy dark-moustached man). ",
        prompt=(f"{CUT} {framing('OTS', 'eye level, looking up a little', '50 mm, shallow focus', 'two of his men in the pit look up toward the ledge where their foreman will stand (he is added later)', 'a normal working moment, about to go wrong')} "
                f"{camera('in the pit behind two crewmen', 'up toward the rock ledge', 'the rock ledge above with a drill hole and one small plain wooden keg on it, the grey layered rock wall behind it, wooded autumn hills and a pale sky at the top', 'nobody on the ledge')} "
                "WIDE 16:9 frame: two crewmen in the foreground seen from BEHIND only (backs, hats and shoulders, large and "
                "soft), cut by the lower LEFT and lower RIGHT edges; the ledge across the middle of the frame with an EMPTY "
                "place in its centre where the foreman will stand (added later). Phineas Gage is NOT in this picture. "
                f"{ONE_EACH} {OTS_FRAMING} {PERIOD} {NO_TEXT}")),
    # row 4 (S1 shot 1 v3 in 16:9): the blast from the cut floor; NO Gage, NO iron, NO hat (S1's sprites go on it)
    "plate-r4": dict(aspect="16:9", refs=[STYLE_DETAIL, "projects/hc002-s1/refs/cavendish_cut.jpg"],
        roles=STYLE_ROLE + CUT_PHOTO,
        prompt=(f"{CUT} {framing('LS', 'very low angle from the floor of the cut', '24 mm', 'a blast has just gone off: grey-brown smoke and dust billow up from a drill hole low in the frame', 'violent, sudden')} "
                f"{camera('on the floor of the cut, low, near the blast hole', 'up and along the cut toward a pale September sky', 'the two layered rock walls rising at the left and right edges and the pale sky between them filling the upper half')} "
                "WIDE 16:9 frame: the walls frame the left and right thirds; the middle third is open: smoke billowing low, "
                "pale sky above it (a black figure, an iron bar and a hat are added there later). EMPTY LOCATION PLATE: no "
                "people, no figures, no iron bar, no hat, no hands. "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # row 5 / 18 (S1 shot 8 in 16:9): ground level, settling smoke; NO Gage (S1's lie -> lift pieces go on it)
    "plate-r5": dict(aspect="16:9", refs=[STYLE_DETAIL],
        roles=STYLE_ROLE,
        prompt=(f"{CUT} SHOT: ground-level view, the camera lies ON the rock floor, 35 mm, shallow focus; stunned silence after a blast. "
                f"{camera('on the rock floor itself, the lens a few inches above the ground', 'along the floor toward the foot of the rock wall', 'the foot of a grey layered rock wall a few yards away across the whole width, settling smoke, shafts of daylight from the upper LEFT')} "
                "WIDE 16:9 frame: the rock floor seen almost edge-on, big out-of-focus pebbles and grit at the bottom edge, the "
                "bare floor rising in steep perspective to the foot of the wall, which fills the upper half; settling grey "
                "smoke drifts over the floor, daylight shafts slant through it. The middle of the floor is bare and clear (a "
                "man is added there later). EMPTY LOCATION PLATE: no people, no hands, no bodies, no clothes, no tools. No blood. "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # row 49 (the long's own HERO): the mountain road; NO coach, NO horses (pieces)
    "plate-r49": dict(aspect="16:9", refs=["proj:refs/valparaiso_1850s.jpg"],
        roles=("Reference 1 is a period view of Valparaíso (1830): the dry coastal hills and their colours only, painted in "
               "our storybook style; never copied. "),
        prompt=(f"{ROAD} {framing('LS', 'eye level, from the roadside', '35 mm', 'the empty mountain road where a six-horse coach will pass (added later)', 'open, bright, free')} "
                f"{camera('at the roadside on the downhill side', 'across the road toward the slope', 'the pale dusty road running level across the whole width of the frame at about 0.62 of the height, the dry slope with cactus and boulders rising behind it, the coastal range in hazy blue layers at the top', 'no sea, no town')} "
                "The road across the frame is EMPTY over its whole width (a coach and six horses are added there later, about "
                "half the frame width long). EMPTY LOCATION PLATE: no people, no coach, no horses, no animals. "
                f"{sizes({'the road': 'about 16 ft (5 m) wide', 'a boulder': 'about 3 ft (1 m)'})} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "sprite-coach-r49": dict(aspect="16:9", refs=["proj:refs/concord_coach.jpg"],
        roles=("Reference 1 is a photograph of an 1852 Concord stagecoach: its SHAPE only (the rounded body, the driver's box, "
               "the leather thoroughbraces, the roof rail), painted in our storybook style, dusty and well used; never its "
               "lettering or the museum around it. "),
        prompt=sprite_sheet("1850s Concord stagecoach, dusty dark-red body with faded yellow trim (no lettering), an empty driver's "
                            "box at the front, the coach facing LEFT",
                            ["the coach BODY alone WITHOUT its wheels, side view facing LEFT, the driver's box EMPTY, luggage "
                             "under a tarpaulin on the roof, passengers' hats faintly seen through the side windows",
                             "ONE large spoked wooden coach wheel with an iron rim, seen exactly side-on, alone"],
                            "row 49: a dusty mountain road in hard sun", R49_LIGHT, "from the side, eye level, 35 mm",
                            sizes({"the coach body": "about 10 ft (3 m) long", "the wheel": "about 5 ft (1.5 m) across"}))),
    "sprite-horses-r49": dict(aspect="16:9", refs=[],
        roles="",
        prompt=sprite_sheet("team of SIX horses in harness, three pairs one behind the other, all bay and brown, trotting to the LEFT "
                            "(seen from the side, the near horse of each pair in front), the reins and traces running back to the "
                            "RIGHT edge where the coach will be",
                            ["the whole team mid-trot, the front legs of the near horses lifted",
                             "EXACTLY the same team, the next step of the trot, the other legs lifted",
                             "EXACTLY the same team, the third step of the trot"],
                            "row 49: a dusty mountain road in hard sun", R49_LIGHT, "from the side, eye level, 35 mm",
                            sizes({"each horse": "about 5 ft 3 in (1.6 m) at the shoulder", "the team": "about 33 ft (10 m) long"}))),
    "pose-gage-r49": dict(aspect="16:9", refs=[GCH],
        roles="Reference 1 is PHINEAS GAGE's 1850s model sheet: outfit A (the coach driver). ",
        prompt=pose_sheet(GAGE_CHILE + ", in outfit A, the coach driver",
                          ["seated on a driver's box (the box is NOT drawn: he sits on nothing, his boots on an invisible "
                           "footboard), holding six reins in both hands, raised to his chest, steady, eyes on the road ahead to the LEFT",
                           "EXACTLY the same; ONE change: he leans forward a little and lifts the reins, urging the horses on"],
                          "row 49: driving a coach along a sunny mountain road", R49_LIGHT,
                          "from the side, eye level, 35 mm, his profile facing LEFT", "the whole figure, seated")),
})

# plate-r2 re-roll (user 2026-11-23, one generation, $0.067): the first plate had haze in the pit before the blast. The
# style reference's "settling smoke" is dropped from this plate's roles and the prompt says it outright. Own name: the
# approved-in-use plate-r2.png is not overwritten; the user sees this one before it replaces anything.
_r2 = REFERENCES["plate-r2"]
REFERENCES["plate-r2-v2"] = {**_r2,
    "roles": _r2["roles"].replace("settling smoke, ", ""),
    "prompt": _r2["prompt"] + " Clear still air, no smoke, no haze, no mist, nothing smoking."}
assert "smoke" not in REFERENCES["plate-r2-v2"]["roles"].replace("no smoke", "")

HERO_PIECES = ["plate-r2", "plate-r4", "plate-r5", "plate-r49", "sprite-coach-r49", "sprite-horses-r49", "pose-gage-r49"]
KEYFRAMES: dict = {}          # the ~40 story stills: written after the HERO shots are approved on real art
# Row 49 coach test still (user 2026-11-23, Tier A + the single Tier D test): ONE still of the coach and six horses.
# L55: the background is WRITTEN (long-backgrounds-v1.md row 49), no set plate / keyframe is a reference: the Gage sheet
# is for the person, concord_coach.jpg for the coach's shape only. The coach faces RIGHT (the clip trots left to right).
KEYFRAMES["row49-coach-v1"] = dict(aspect="16:9", refs=["ref:sheet-gage-chile", "proj:refs/concord_coach.jpg"],
    roles=("Reference 1 is PHINEAS GAGE's 1850s model sheet: outfit A (the coach driver): take only his face, hair, build and clothes "
           "(do NOT copy its layout or other views). Reference 2 is a photograph of an 1852 Concord stagecoach: its SHAPE only (the "
           "rounded body, the driver's box, the leather thoroughbraces, the roof rail), painted in our storybook style, dusty and well "
           "used; never its lettering or the museum around it. "),
    prompt=(f"{ROAD.replace('hard bright sun', 'soft neutral late-afternoon light')} {framing('LS', 'eye level, from the roadside, side view', '35 mm', 'a Concord stagecoach pulled by SIX horses trots along the mountain road to the RIGHT, dust rising behind it; PHINEAS GAGE sits on the driver box holding the reins', 'open, steady, free')} "
            f"{camera('at the roadside on the downhill side', 'across the road toward the slope', 'a dusty pale road running level across the frame, the dry slope with cactus, thorny scrub and boulders behind it, the coastal range in hazy layers at the top; no sea, no town')} "
            "WIDE 16:9 frame: the coach and its team run across the frame, together at least ONE THIRD of the frame width, the coach "
            "facing RIGHT. EXACTLY SIX horses in three pairs, all bay and brown: each horse shows all four legs, its head and its ears, "
            "clearly separate from its neighbours (no merged bodies, no extra or missing horse). The reins are visibly drawn running from "
            "his hands to the horses. Gage is seated on the driver's box, small in the frame (a wide shot: no close-up, his face tiny), "
            "his head BELOW the line of the horses' backs; "
            "A trail of pale dust behind the coach. "
            "LIGHT: even, neutral late-afternoon light, soft shadows, no strong colour cast. "
            + sizes({"the road": "about 16 ft (5 m) wide", "the coach body": "about 10 ft (3 m) long", "a wheel": "about 5 ft (1.5 m) across",
                     "each horse": "about 5 ft 3 in (1.6 m) at the shoulder", "the team": "about 33 ft (10 m) long"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No modern objects. {NO_TEXT}"))
# row49-coach-v2 (user 2026-11-23, ONE re-roll): v1 came back with 4 horses, a left-leading team, the sea. v2: THREE pairs in a
# staggered line receding into the distance; a distant sea is allowed; no "head below the horses' line" rule (a real box sits
# above); NO direction in the prompt: the image is mirrored afterwards (row49-coach-v2-flip.png) so the team leads RIGHT.
KEYFRAMES["row49-coach-v2"] = dict(aspect="16:9", refs=["ref:sheet-gage-chile", "proj:refs/concord_coach.jpg"],
    roles=KEYFRAMES["row49-coach-v1"]["roles"],
    prompt=(f"{ROAD.replace('hard bright sun', 'soft neutral evening light')} {framing('LS', 'eye level, from the roadside, side view', '35 mm', 'a Concord stagecoach pulled by SIX horses trots along the mountain road, dust rising behind it; PHINEAS GAGE sits on the driver box holding the reins', 'open, steady, free')} "
            f"{camera('at the roadside on the downhill side', 'across the road toward the slope', 'a dusty pale road along the dry slope with cactus, thorny scrub and boulders, the coastal range in hazy layers behind, a distant strip of sea far below is allowed; no town')} "
            "WIDE 16:9 frame: the team and coach run across the frame, together at least ONE THIRD of the frame width. THE TEAM IS THREE "
            "PAIRS OF HORSES, SIX HORSES IN ALL (count them: 1, 2, 3, 4, 5, 6), all bay and brown, harnessed in a staggered line "
            "that recedes into the distance, the pairs one behind the other; every horse's head is visible and every pair's legs are "
            "visible, each horse clearly separate from its neighbours (no merged bodies, no extra or missing horse); all trotting the same "
            "way, the coach BEHIND them. The reins are visibly drawn running from his hands to the team. Gage sits on the Concord coach's "
            "driver box, small in the frame (a wide shot: no close-up, his face tiny). A trail of pale dust behind the coach. "
            "LIGHT: even, neutral evening light, soft shadows, no strong colour cast. "
            + sizes({"the road": "about 16 ft (5 m) wide", "the coach body": "about 10 ft (3 m) long", "a wheel": "about 5 ft (1.5 m) across",
                     "each horse": "about 5 ft 3 in (1.6 m) at the shoulder", "the team": "about 33 ft (10 m) long"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No modern objects. {NO_TEXT}"))
# row 45 start still for the Tier D test (user 2026-11-23): ONE man, ONE horse, a livery stable in Hanover, N.H. (1850s).
# L55: the background is written here (long-backgrounds-v1.md row 45); the Gage sheet is for the person only.
KEYFRAMES["row45-stable-v1"] = dict(aspect="16:9", refs=["ref:sheet-gage-chile"],
    roles=("Reference 1 is PHINEAS GAGE's 1850s model sheet: take only his face, hair and build (older, thinner, clean-shaven, his left "
           "eye closed); do NOT copy its layout, its other views or its outfits. "),
    prompt=(f"{set_block('a livery stable in Hanover, New Hampshire', 'the 1850s', 'a weathered grey-brown plank stable with a wide open double door, straw on a packed-earth yard, a wooden water trough, soft overcast morning light')} "
            f"{framing('MLS', 'eye level, from the yard, a little to the side', '35 mm', 'PHINEAS GAGE stands beside a bay horse he has just led out of the stable door; with a stiff-bristled grooming brush held in his right hand he brushes the neck of the horse, the lead rope loose over his other arm', 'calm, patient, at ease')} "
            f"{camera('in the yard', 'the open stable door with the man and the horse in front of it', 'the plank wall and the open dark doorway of the stable behind them, straw on the ground, a wooden trough at the right edge; nothing else')} "
            "WIDE-ish 16:9 frame: exactly ONE man and exactly ONE horse and nobody else. The horse is seen from the side, its whole head, "
            "ears and neck clearly visible, all four legs on the ground; the man stands at its shoulder, small in the frame (his face small, "
            "not a close-up), the grooming brush clearly in his hand against the horse's neck. He wears a plain work shirt, a waistcoat, "
            "trousers and boots, no hat. No second horse, no extra people, no animals in the doorway. "
            + sizes({"the horse": "about 5 ft 3 in (1.6 m) at the shoulder", "the stable door": "about 8 ft (2.4 m) high", "the brush": "about 9 in (23 cm) long"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No modern objects. {NO_TEXT}"))

# v2 (user 2026-11-23, ONE re-roll): v1 gave a grey-haired older stranger with both eyes open, dark moody light.
KEYFRAMES["row45-stable-v2"] = dict(aspect="16:9", refs=["ref:sheet-gage-chile"],
    roles=("Reference 1 is PHINEAS GAGE's 1850s model sheet (the Chile/Hanover look, clean-shaven): take ONLY his face, hair and clothes "
           "from it; do NOT copy its layout, its other views or its poses. He is about 28, thick DARK brown hair, clean-shaven, strong square "
           "jaw, his LEFT eye shut (a sunken, closed lid), a faint pale scar high on the left forehead. NOT grey-haired, NOT older, no beard. "),
    prompt=(f"{set_block('a livery stable in Hanover, New Hampshire', 'the 1850s', 'a weathered grey-brown plank stable with a wide open double door, straw on a packed-earth yard, a wooden water trough, soft even overcast morning light, bright and open, not dark, not moody')} "
            f"{framing('MLS', 'eye level, from the yard, a little to the side', '35 mm', 'PHINEAS GAGE, about 28, stands in three-quarter profile beside a bay horse he has just led out of the stable door; with a stiff-bristled grooming brush held in his raised right hand he brushes the neck of the horse, the lead rope loose over his other arm', 'calm, patient, at ease')} "
            f"{camera('in the yard', 'the open stable door with the man and the horse in front of it', 'the plank wall and the open doorway of the stable behind them, straw on the ground, a wooden trough at the right edge; nothing else')} "
            "WIDE-ish 16:9 frame: the man and the horse together fill only the middle third of the frame width. Exactly ONE man and exactly ONE "
            "horse and nobody else. The horse is seen from the side, its whole head, ears, neck and front legs clearly visible; the man stands "
            "at its shoulder, small in the frame, his face small and in three-quarter or profile view, thick dark hair, clean-shaven, strong "
            "square jaw, his LEFT eye closed, a faint pale scar high on his left forehead; the stiff grooming brush clearly in his raised hand "
            "against the horse's neck. He wears a plain work shirt, a waistcoat, trousers and boots, no hat. No second horse, no extra people, "
            "no animals in the doorway. "
            + sizes({"the horse": "about 5 ft 3 in (1.6 m) at the shoulder", "the stable door": "about 8 ft (2.4 m) high", "the brush": "about 9 in (23 cm) long"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No modern objects. {NO_TEXT}"))

# ── BATCH 1 (user 2026-11-23, Mahdi approved: rows 2, 11, 23, 26, 29, 41, 52, 53, 55, 58; ten stills, ~$0.67) ──────────────
# L55: every background is WRITTEN (long-backgrounds-v1.md), no set plate / keyframe is a reference; the sheets are for the
# person only (face, hair, clothes). Face wording from row45-stable-v2. TIMELINE: rows 2 and 11 are BEFORE the accident
# (13 Sep 1848): both eyes open, no scar, so they use S1's 1848 sheet; rows 26, 29, 41, 52, 53, 55, 58 are after it: the
# Chile sheet, LEFT eye closed (L48), scar. Rows 52, 53, 58: older and thinner.
FACE_ONLY = ("take ONLY his face, hair and clothes from it; do NOT copy its layout, its other views or its poses. ")
GAGE_28 = ("PHINEAS GAGE, about 28: thick DARK hair, clean-shaven, a strong square jaw, his LEFT eye closed (a sunken, shut lid; L48: "
           "in a front view that is on the RIGHT side of the picture, in a profile facing right it is the far eye), a faint pale scar "
           "high on the left side of his forehead under the hair; NOT grey-haired, NOT older, no beard; no bandage, no wound, no blood")
GAGE_OLDER = ("PHINEAS GAGE, about 32: the same face but older and thinner (hollower cheeks, leaner build), thick DARK hair, "
              "clean-shaven, a strong square jaw, his LEFT eye closed (a sunken, shut lid; L48: in a front view that is on the RIGHT "
              "side of the picture), a faint pale scar high on the left side of his forehead under the hair; NOT grey-haired, no "
              "beard; no bandage, no wound, no blood")
GAGE_1848 = ("PHINEAS GAGE, 25, on 13 September 1848 BEFORE the accident: thick DARK hair, clean-shaven, a strong square jaw, BOTH "
             "eyes open, no scar, no bandage, no wound")
R_CHILE = "Reference 1 is PHINEAS GAGE's 1850s model sheet (the Chile / Hanover look, clean-shaven): " + FACE_ONLY
R_1848 = "Reference 1 is PHINEAS GAGE's 1848 model sheet (before the accident, both eyes open): " + FACE_ONLY
B1 = {}

B1["row2-glance-v1"] = dict(aspect="16:9", refs=[G1848], roles=R_1848,
    prompt=(f"{CUT} {framing('MCU', 'eye level, from in front of him on the ledge, a little to his left', '50 mm, shallow focus', 'PHINEAS GAGE stands on the rock ledge and turns his head to look back over his own shoulder toward his men calling from below; his hands and the iron are not in the picture', 'alert, just distracted, about to go wrong')} "
            f"{camera('on the ledge in front of him', 'at his face', 'the grey layered schist wall behind his head with one drill hole, wooded hills in early autumn colour soft at the far edge, a pale sky above', 'no iron bar, no powder, no other person in view')} "
            f"{cast(GAGE_1848 + ', in his low-crowned dark felt hat, a white shirt and dark braces, chest up, his face a medium-size part of the frame (not tiny, not huge)')} "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No blood. {NO_TEXT}"))

B1["row11-keg-v1"] = dict(aspect="16:9", refs=[G1848], roles=R_1848 + "The two crewmen are NOT from the reference. ",
    prompt=(f"{set_block('the powder store beside the Cavendish rock cut', 'summer 1848', 'a rough plank powder shed with kegs stacked inside, soft overcast daylight')} "
            f"{framing('MCU', 'eye level', '50 mm', 'PHINEAS GAGE lifts a small wooden powder keg onto his right shoulder without effort, a calm easy half-smile; two crewmen behind him grin', 'easy strength, good humour')} "
            f"{camera('in front of the shed door', 'at Gage and the shed wall', 'a wooden shed wall of rough boards with kegs stacked behind them, the two crewmen soft behind his shoulders')} "
            f"{cast(GAGE_1848 + ', in the low-crowned dark felt hat, white shirt with sleeves rolled, dark braces, chest up, the keg on his shoulder', 'a red-haired freckled youth of about seventeen, thin, no hat, grinning, soft, behind his left side', 'a heavy dark-moustached man in his thirties with a round face and a flat cap, grinning, soft, behind his right side')} "
            + scale({"the powder keg": "plain wood, no lettering, about 40 cm (16 in) tall and 30 cm (12 in) across, as tall as his forearm and hand together, on his shoulder"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No blood. {NO_TEXT}"))

B1["row23-harlow-v1"] = dict(aspect="16:9", refs=[HARLOW_REF],
    roles="Reference 1 is DR JOHN MARTYN HARLOW's model sheet (29 in 1848): take ONLY his face, hair, short beard and clothes from it; do NOT copy its layout, its other views or its poses. ",
    prompt=(f"{set_block('the country doctor Harlow room in Cavendish, Vermont', 'September 1848', 'a plain plaster room, a shelf of medicine bottles, an oil lamp, warm lamplight against a dim room')} "
            f"{framing('MS', 'eye level', '50 mm', 'DR HARLOW rolls up his shirt cuffs beside the lamp, his black medical bag open on the table, ready for a hard case', 'calm, focused, kind')} "
            f"{camera('across the table from him', 'at him', 'a plain plaster wall, a shelf of medicine bottles above his shoulder, the oil lamp warm pool on the table with the open black bag', 'no window in view')} "
            f"{cast(HARLOW + ', waist up, in shirtsleeves and waistcoat (the frock coat hung on the chair), no spectacles')} "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

B1["row26-farmhouse-v1"] = dict(aspect="16:9", refs=[GCH], roles=R_CHILE,
    prompt=(f"{set_block('a farmhouse yard in Lebanon, New Hampshire', 'late November 1848', 'a weathered clapboard farmhouse door opening onto a yard of bare trees, fallen brown leaves, a wood pile, thin cold light')} "
            f"{framing('LS', 'eye level', '35 mm', 'PHINEAS GAGE, thinner and slow, steps out of the farmhouse door into the yard and squints at the low sun; his hands hang EMPTY at his sides', 'weak, careful, alive')} "
            f"{camera('in the yard, facing the farmhouse door', 'toward the door', 'the farmhouse door and a strip of its clapboard wall, a yard of bare late-autumn trees, fallen leaves, a wood pile, low sun from the left', 'no sickroom, no bed')} "
            f"{cast(GAGE_28 + ', thinner than before, no bandage, no hat, a short dark wool jacket over a white shirt, small in the frame (a wide shot, his face small), full figure, hands empty')} "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No blood. {NO_TEXT}"))

B1["row29-doorway-v1"] = dict(aspect="16:9", refs=[GCH], roles=R_CHILE + "The other man is NOT from the reference. ",
    prompt=(f"{set_block('a plain village doorway in New England', 'winter 1848-49', 'a dark plank door and frame, a room beyond in cold grey light, muted colours')} "
            f"{framing('MS', 'eye level', '35 mm', 'PHINEAS GAGE argues in a doorway, mouth open mid-sentence, one hand slicing the air, while an older man steps back from him with a raised palm; an argument only: no blows, no raised fists', 'fitful, irreverent, impatient of restraint')} "
            f"{camera('in the room facing the doorway', 'at the door', 'a dark plank door and its frame, a room beyond in grey light', 'no street, no sky')} "
            f"{cast(GAGE_28 + ', in a white shirt, dark braces and a waistcoat, no hat, in the doorway, waist up, hands EMPTY', 'a stout bald man in his fifties with grey side-whiskers and a brown coat, no spectacles, stepping back, his palm raised')} "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No blood. {NO_TEXT}"))

B1["row41-boston-v1"] = dict(aspect="16:9", refs=[GCH, "kit:matt-sheet.jpg"],
    roles=R_CHILE + "Reference 2 is MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; his clothes are of 1849. ",
    prompt=(f"{set_block('a small lecture room of the Boston Society for Medical Improvement', '1849', 'a small raked room, curved wooden benches, a demonstration table, a tall window with cold winter light, a blackboard')} "
            f"{framing('LS', 'eye level, from the side benches', '35 mm', 'PHINEAS GAGE stands by the demonstration table with the tamping iron laid on it, resting one hand beside it; three doctors lean forward to look at him', 'serious, curious, a little theatre')} "
            f"{camera('on the side benches of the lecture room', 'across the room toward the table and the tall window', 'the curved wooden benches, the demonstration table, a tall window with winter light, a blackboard with no writing', 'no museum cases, no skull drawing')} "
            f"{cast(GAGE_28 + ', in a dark frock coat and waistcoat with a white shirt, no hat, small in the frame, his face small, the closed left eye visible', 'a white-haired doctor of sixty with long side whiskers, no spectacles, leaning forward', 'a bald clean-shaven doctor of fifty, no spectacles, arms folded', 'a young dark-haired doctor of about twenty-five, clean-shaven, no spectacles', 'MATT')} "
            f"{matt_beat('a dark frock coat and a brown waistcoat of 1849', 'on the back row of the benches at the far side, writing in his amber notebook with the amber round spectacles on his nose')} "
            + sizes({"the tamping iron lying on the table": "about 3 ft 7 in (109 cm) long and 1 1/4 in (3.2 cm) thick, smooth and round, tapering to a point", "the table": "about 3 ft (90 cm) high"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No blood. {NO_TEXT}"))

B1["row52-innyard-v1"] = dict(aspect="16:9", refs=[GCH], roles=R_CHILE + "Outfit A (the coach driver) is his clothes here. ",
    prompt=(f"{set_block('the yard of a coaching inn on the Valparaiso to Santiago road, Chile', 'the 1850s', 'a whitewashed adobe inn wall with a wooden gate, dusty ground, the side of a dark-red coach, warm afternoon light')} "
            f"{framing('MS', 'eye level', '50 mm', 'PHINEAS GAGE, standing by the coach, hands a leather travel bag down to a passenger, a small kind smile', 'warm, steady, a little proud')} "
            f"{camera('in the inn yard beside the coach', 'at Gage and the inn wall', 'a whitewashed adobe inn wall, the side of the coach at his back, a passenger arm reaching up from the lower right edge for the bag', 'no road, no mountains')} "
            f"{cast(GAGE_OLDER + ', as a coach driver: a short dark wool jacket over a white shirt, a cotton scarf loose at the neck, a broad-brimmed low felt hat, waist up, three-quarter view so both the shut left eye and the open right eye show')} "
            "The passenger is only an arm in a sleeve and a hand at the lower right edge (no face, no body, no second person). "
            + sizes({"the leather travel bag": "about 22 in (55 cm) long, held by its handle in one hand"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

B1["row53-innhearth-v1"] = dict(aspect="16:9", refs=[GCH], roles=R_CHILE + "The children are NOT from the reference. ",
    prompt=(f"{set_block('the common room of a coaching inn in Chile', 'the 1850s', 'a low whitewashed room with dark beams, a wooden table by a stone fireplace, a clay jug, warm firelight')} "
            f"{framing('MS', 'eye level', '35 mm', 'PHINEAS GAGE sits at the inn table telling a story with both open hands, children leaning in wide-eyed', 'warm, playful, spellbound listeners')} "
            f"{camera('across the table from him', 'at him and the fire', 'an inn table by a stone fireplace, a clay jug on the table, the children faces leaning in on both sides, warm light', 'no yard, no coach')} "
            f"{cast(GAGE_OLDER + ', in shirtsleeves and a waistcoat, no hat, at the table, both hands open and empty in the air as he tells a story, waist up, three-quarter view so both eyes show', 'a girl of about eight with two dark braids, wide-eyed', 'a boy of about ten with messy fair hair, grinning', 'a small boy of about five with a round face and a missing front tooth, mouth open')} "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

B1["row55-portrait-v1"] = dict(aspect="16:9", refs=[GCH],
    roles=R_CHILE + "Outfit B (the portrait outfit) is his clothes here. This is a NEW painting in our storybook style, never a photograph or a copy of one. ",
    prompt=(f"{set_block('a dark wood table in a quiet room', 'the 1850s', 'a dark wood table top, soft side light from the left, nothing else')} "
            f"{framing('MCU', 'eye level, from above the table, looking at the portrait', '50 mm', 'an open dark leather daguerreotype case lies on the table; in its oval gilt mat is a painted portrait of PHINEAS GAGE standing in a dark frock coat, a waistcoat and a dark cravat, no hat, holding his tamping iron upright in his right hand at his side', 'proud, steady, serious')} "
            f"{camera('above the table', 'down at the open case', 'the dark wood table top around the open leather case, nothing else', 'no hands, no room')} "
            f"{cast(GAGE_28 + ', shown only INSIDE the oval portrait, waist up, his LEFT eye shut, the right eye open')} "
            "The portrait fills about 60% of the frame width. The tamping iron in the portrait is a smooth, perfectly straight, round iron rod about 3 ft 7 in (109 cm) long, "
            "tapering over its last foot to a point, held upright beside him, its full length visible and clearly longer than his torso. "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

B1["row58-deck-v1"] = dict(aspect="16:9", refs=[GCH], roles=R_CHILE,
    prompt=(f"{set_block('the deck of a sailing ship bound from Valparaiso to San Francisco', '1859', 'a worn wooden deck and rail, rigging and canvas, a grey-green sea and a pale grey sky, steady cold light')} "
            f"{framing('MS', 'eye level', '35 mm', 'PHINEAS GAGE stands at the ship rail, one hand on it, coat buttoned, looking out to sea, his health failing; beside him lean a carpet bag and a long bundle wrapped in cloth', 'tired, quiet, far away')} "
            f"{camera('on the deck beside him', 'at him and the sea', 'the wooden rail, rigging lines, a grey-green sea and pale sky', 'no land in view')} "
            f"{cast(GAGE_OLDER + ', thinner and tired, in a dark wool coat buttoned to the neck, a low felt hat, waist up, three-quarter view so both eyes show')} "
            + sizes({"the cloth-wrapped bundle (the tamping iron)": "about 3 ft 7 in (109 cm) long and slim, leaning against the rail", "the carpet bag": "about 20 in (50 cm) wide"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

KEYFRAMES.update(B1)

# ── BATCH 1 RE-ROLLS (user 2026-11-24, Mahdi approved: rows 41, 58, 55 and S1's 16:9 s10 / s12 for rows 21 and 30; one take each,
# $0.067 each, ~$0.34 with the free steps) ─────────────────────────────────────────────────────────────────────────────────────
# FREE (done): sheet-gage-chile-v2.png = the panels whose SHUT eye was on the wrong side mirrored (the three full-body views and the
# top-right head; the two bottom heads already shut his LEFT eye, so they stay): every NEW spec uses GCH2. The first ten (B1) were
# made with the v1 sheet and stay recorded as such. Rows 29, 52, 53: the mirrored copies (-flip.png) are the ones used.
GCH2 = "ref:sheet-gage-chile-v2"
USE_MIRRORED = ["row29-doorway-v1-flip", "row52-innyard-v1-flip", "row53-innhearth-v1-flip"]
R_CHILE2 = ("Reference 1 is PHINEAS GAGE's 1850s model sheet (clean-shaven; in EVERY view his LEFT eye is the shut one, on the RIGHT "
            "side of the picture in a front view): " + FACE_ONLY + "Do NOT copy the sheet's smiles or winks. ")
# L75 (this re-roll): ONE description of the iron, used by every shot that shows it (the Warren museum photo in refs/ is of his SKULL,
# not the rod, so there is NO photo reference for the iron: its shape is written).
IRON_ROD = ("a smooth, perfectly round iron rod, 3 ft 7 in (109 cm) long and 1 1/4 in (3.2 cm) thick, dull dark grey, tapering over its "
            "last foot to a point and plain and blunt at the other end; no knob, no handle, no pommel, no crossbar, no hook, no bend")
B2 = {}

B2["row41-boston-v2"] = dict(aspect="16:9", refs=[GCH2, "kit:matt-sheet.jpg"],
    roles=R_CHILE2 + "Reference 2 is MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; his clothes are of 1849. ",
    prompt=(f"{set_block('a small lecture room of the Boston Society for Medical Improvement', '1849', 'a small raked room, curved wooden benches, a demonstration table, a tall window with cold winter light, a blackboard')} "
            f"{framing('LS', 'eye level, from the side benches', '35 mm', 'PHINEAS GAGE stands by the demonstration table with his tamping iron laid lengthwise ON the table beside his resting hand; three doctors lean forward to look at him', 'serious, curious, a little theatre')} "
            f"{camera('on the side benches of the lecture room', 'across the room toward the table and the tall window', 'the curved wooden benches, the demonstration table, a tall window with winter light, a blackboard with no writing', 'no museum cases, no skull drawing')} "
            f"{cast(GAGE_28 + ', in a dark frock coat and waistcoat with a white shirt, no hat, standing three-quarter toward the doctors so his shut LEFT eye (picture-right) and open right eye both show, his face small but his shut left lid clear', 'a white-haired doctor of sixty with long white side whiskers, no spectacles, leaning forward', 'a bald clean-shaven doctor of fifty, no spectacles, arms folded', 'a thin young doctor of about twenty-five with RED-BROWN hair and GINGER side whiskers, a narrow pale freckled face and a soft chin, no spectacles, clearly NOT like Gage (no dark hair, no square jaw)', 'MATT')} "
            f"{matt_beat('a dark frock coat and a brown waistcoat of 1849', 'in the BACK row of the benches at the far side, writing in his amber notebook with the amber round spectacles on his nose')} "
            f"The tamping iron is {IRON_ROD}. "
            + sizes({"the tamping iron lying on the table": "109 cm long, it lies along the table top and spans almost the whole table's length, much longer than a man's forearm, as thin as a broom handle",
                     "the table": "about 3 ft (90 cm) high and 4 ft (120 cm) long"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} No blood. {NO_TEXT}"))

B2["row58-deck-v2"] = dict(aspect="16:9", refs=[GCH2], roles=R_CHILE2,
    prompt=(f"{set_block('the deck of a sailing ship bound from Valparaiso to San Francisco', '1859', 'a worn wooden deck and rail, rigging and canvas, a grey-green sea and a pale grey sky, steady cold light')} "
            f"{framing('MS', 'eye level', '35 mm', 'PHINEAS GAGE stands at the ship rail, one hand on it, coat buttoned, looking out to sea, quiet and tired; beside him lean a carpet bag and a long bundle wrapped in cloth', 'tired, quiet, far away')} "
            f"{camera('on the deck beside him', 'at him and the sea', 'the wooden rail, rigging lines, a grey-green sea and pale sky', 'no land in view')} "
            f"{cast(GAGE_OLDER + ', thinner and older, in a dark wool coat buttoned to the neck, a low felt hat, waist up, facing the camera turned a little toward the left of the picture so both eyes show: his shut LEFT eye is on the RIGHT side of the picture')} "
            "SKIN AND SCAR: his skin is a normal, healthy, warm natural skin tone, exactly like the reference (NOT green, NOT grey, NOT pale-sick); "
            "the scar is one faint, thin, PALE line high on his LEFT forehead (picture-right), lighter than the skin, NOT red, no blood, no wound. "
            "The cold sea light does not tint his face. "
            + sizes({"the cloth-wrapped bundle (the tamping iron)": "109 cm (3 ft 7 in) long and slim, leaning against the rail", "the carpet bag": "about 20 in (50 cm) wide"}) + " "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

B2["row55-portrait-v2"] = dict(aspect="16:9", refs=[GCH2],
    roles=R_CHILE2 + "Outfit B (the portrait outfit) is his clothes here. This is a NEW painting in our storybook style, never a photograph or a copy of one. ",
    prompt=(f"{set_block('a dark wood table in a quiet room', 'the 1850s', 'a dark wood table top, soft side light from the left, nothing else')} "
            f"{framing('MCU', 'eye level, from above the table, looking at the portrait', '50 mm', 'an open dark leather daguerreotype case lies on the table; in its oval gilt mat is a painted portrait of PHINEAS GAGE standing in a dark frock coat, a waistcoat and a dark cravat, no hat, holding his tamping iron upright in his right hand at his side', 'proud, steady, serious')} "
            f"{camera('above the table', 'down at the open case', 'the dark wood table top around the open leather case, nothing else', 'no hands, no room')} "
            f"{cast(GAGE_28 + ', shown only INSIDE the oval portrait, waist up')} "
            "EXPRESSION: calm and neutral, lips closed and level, NO smile, NO smirk, cheeks relaxed. His LEFT eyelid (picture-right) is shut for good: "
            "smooth, flat and slightly sunken, the way an old injury leaves it, NOT a wink (no squeeze, no lifted cheek, no creases fanning out); "
            "his RIGHT eye (picture-left) is open and looks steadily at the viewer. "
            f"The portrait fills about 60% of the frame width. The tamping iron in the portrait is {IRON_ROD}, held upright beside him, its full length visible and clearly longer than his torso. "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))

# rows 21 and 30: S1's 16:9 s10 / s12 came back with the bandage as a flat band across BOTH brows. These are EDITS of those frames
# (the same scene and cast are the point, so the frame is the reference and SAME_CAMERA says so): only Gage's head changes.
S1_16 = "projects/hc002-s1/assets/images/keyframes16x9"
S1_GA = "projects/hc002-s1/assets/images/refs/sheet-gage-after.png"
BANDAGE_FIX = ("Reference 1 is the approved film frame: keep EVERYTHING in it exactly the same (the place, the camera, every person and "
               "object, the light, the colours, the composition) EXCEPT the bandage on PHINEAS GAGE's head. Reference 2 is Gage's bandaged "
               "model sheet. His bandage wraps over the CROWN of his head and passes diagonally down over his LEFT eye ONLY (on the RIGHT "
               "side of the picture); it does NOT cross his right brow or his forehead on the left side of the picture: his RIGHT eye, his "
               "right eyebrow and the skin and hair above them are bare and visible. ")
B2["row21-s10-v2"] = dict(aspect="16:9", refs=[f"{S1_16}/s10.orig.png", S1_GA],
    roles=BANDAGE_FIX + "Same camera as the set plate (intended). ",
    prompt=("Edit the approved frame: Gage on the hotel piazza in Cavendish, Vermont, September 1848 raises one hand in greeting to Dr Williams "
            "stepping down from his carriage; Matt leans on the piazza post. Change ONLY Gage's bandage as described; everything else "
            "stays pixel-for-pixel the same. Exactly ONE bandage, over his left eye (picture-right) only. No blood. " + NO_TEXT))
B2["row30-s12-v2"] = dict(aspect="16:9", refs=[f"{S1_16}/s12.orig.png", S1_GA],
    roles=BANDAGE_FIX + "Same camera as the set plate (intended). ",
    prompt=("Edit the approved frame: two friends whisper in a doorway on a village street in Vermont, 1849, and Phineas Gage walks away far "
            "down the dirt street, small and a little out of focus. Change ONLY Gage's bandage as described (at this distance a small white "
            "wrap over the crown and ONE eye, on the picture-right side of his face only); everything else stays pixel-for-pixel the same. "
            "No blood. " + NO_TEXT))

KEYFRAMES.update(B2)

# ── 2026-11-24 (user): row 55 v3 + BATCH 2a (22 stills, cap $1.60 in all) ──────────────────────────────────────────────────────
# iron-ref.png (free): the rod cut out of gage_wilgus.jpg along its axis, only the two hand-free stretches, no face, on grey. It is
# the SHAPE reference for every shot where the iron appears, together with the words (IRON_ROD2 adds: no collar / flare / cap, which
# v2 of rows 41 and 55 both came back with).
IRON_REF = "proj:refs/iron-ref.png"
WILGUS = "proj:refs/gage_wilgus.jpg"
IRON_ROD2 = (IRON_ROD + "; the blunt end is simply cut off flat at the same thickness as the rod: no collar, no flare, no cap, no ring")
IRON_ROLE = ("Reference 3 is ONLY the SHAPE of the iron: a long, straight, perfectly round rod of one even thickness along its whole length "
             "(thin, about as thick as a thumb and a half), no knob, no flared end; ignore its grey background and its blur. ")

B2["row55-portrait-v3"] = dict(aspect="16:9", refs=[GCH2, WILGUS, IRON_REF],
    roles=(R_CHILE2 + "Outfit B (the portrait outfit) is his clothes here. Reference 2 is a period photograph of the real Phineas Gage: take "
           "ONLY his POSE and his EXPRESSION from it (facing the camera straight on, head straight, brows level, calm and confident, "
           "the left lid shut, the right eye open, the iron held upright in front of him), and re-illustrate it as a NEW painting in our "
           "storybook style with our colours and ink line: never the photograph itself, no black-and-white, no grain, no gilt frame "
           "copied. " + IRON_ROLE),
    prompt=(f"{set_block('a dark wood table in a quiet room', 'the 1850s', 'a dark wood table top, soft side light from the left, nothing else')} "
            f"{framing('MCU', 'eye level, from above the table, looking at the portrait', '50 mm', 'an open dark leather daguerreotype case lies on the table; in its oval gilt mat is a painted portrait of PHINEAS GAGE seen straight on, in a dark frock coat, a waistcoat and a dark cravat, no hat, holding his tamping iron upright in front of him with his right hand', 'calm, confident, steady')} "
            f"{camera('above the table', 'down at the open case', 'the dark wood table top around the open leather case, nothing else', 'no hands, no room')} "
            f"{cast(GAGE_28 + ', shown only INSIDE the oval portrait, waist up')} "
            "EXPRESSION AND POSE: head STRAIGHT (not tilted), shoulders level, both brows LEVEL at the same height, mouth closed and level, NO smile and NO smirk, "
            "calm and confident. His LEFT eyelid (picture-right) is shut for good: a smooth, flat, closed lid, slightly sunken, with NO creases, NO squeezing, "
            "no lifted cheek, so it does NOT read as a wink; his RIGHT eye (picture-left) is open and looks straight at the viewer. "
            f"The portrait fills about 60% of the frame width. The tamping iron is {IRON_ROD2}, held upright, its full length visible and clearly longer than his torso. "
            f"{ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))
KEYFRAMES.update({"row55-portrait-v3": B2["row55-portrait-v3"]})

# ── BATCH 2a ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────
# L55: every background is WRITTEN (long-backgrounds-v1.md) and goes in word for word; the only references are the sheets (face,
# hair, clothes), a SMALL style detail (painting style only) and real period photographs used for ONE named thing each.
# Gage: the only Gage appearances in 2a are row 5 (his face turned AWAY, 13 Sep 1848: clothes + hair from S1's 1848 sheet, because the
# Chile sheet's hat, scarf and jacket are Chilean and wrong at the rock cut) and row 31 (a hand and a sleeve, no face), so v2 is not needed.
B3 = {}
NOBODY = "CAST: no people in the frame (nobody, no figures, no faces, no hands)."
STYLE_REFS = [STYLE_DETAIL]
HARLOW_OLD = ("DR JOHN MARTYN HARLOW at 48 in 1867: the same long oval face and high forehead, deep-set kind eyes, the hair and his full beard "
              "now streaked with grey (grey-brown, not white); a dark frock coat, a dark waistcoat, a white shirt with a high collar and a black "
              "neck-cloth")


def S(name, sz, ang, lens, action, mood, sname, year, look, pos, facing, bg, lm, people, refs=None, roles="", extra="", size_line=""):
    """One batch-2a still: the lines every story still needs, in the order of the shots already made."""
    refs = refs if refs is not None else STYLE_REFS
    roles = roles or (STYLE_ROLE if refs == STYLE_REFS else "")
    sheet = any("sheet" in r for r in refs)
    B3[name] = dict(aspect="16:9", refs=refs, roles=roles,
        prompt=(f"{set_block(sname, year, look)} {framing(sz, ang, lens, action, mood)} {camera(pos, facing, bg, lm)} {people} "
                + (extra + " " if extra else "") + (size_line + " " if size_line else "")
                + (f"{ONE_EACH} " if sheet else "") + f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"))


# row 5 ×2 (hard cut on "talking"): the cut floor after the blast; his face turned away; no blood (Rule 0b: smoke + framing)
G5 = ("PHINEAS GAGE, 25, thick DARK hair, in a white shirt and dark braces covered in grey dust, no hat; his FACE is turned AWAY from the camera "
      "(we see the back of his head, his neck and one shoulder only); no blood, no injury mark and no bandage visible anywhere")
R5 = ("Reference 1 is PHINEAS GAGE's 1848 model sheet: take ONLY his hair and his clothes (white shirt, dark braces) from it; his face is turned "
      "away in this picture; do NOT copy its layout, its other views or its poses. ")
S("row5a-lying-v1", "LS", "low, from the rubble floor", "28 mm",
  "PHINEAS GAGE lies on his side on the grey rubble in the settling dust, his face turned away from the camera, one arm out; a faint drift of smoke across him",
  "stunned stillness, the quiet after the blast", "the floor of the Cavendish rock cut just after the blast", "13 September 1848",
  "grey broken rock and rubble, drifting smoke and settling dust, pale light slanting through the dust from the right",
  "low on the rubble floor of the cut, ten paces from him", "along the floor toward him and the foot of the rock wall",
  "settling dust and drifting smoke over a floor of grey rubble, the foot of a layered rock wall faint behind him, shafts of pale light from the right",
  "no sky, no rim of the cut, no kegs, no other person",
  cast(G5), refs=[G1848], roles=R5)
S("row5b-elbow-v1", "MS", "from beside him at ground level", "35 mm",
  "PHINEAS GAGE pushes himself up on one elbow in the dust, his head lifting, his face still turned away from the camera toward the smoke",
  "dazed, alive", "the floor of the Cavendish rock cut just after the blast", "13 September 1848",
  "grey broken rock and rubble, drifting smoke and settling dust, pale light slanting through the dust from the right",
  "right beside him at ground level, a body-length from his shoulder", "across him toward a close rock wall",
  "a close wall of grey layered schist streaked with dust, a split iron drill steel and a broken plank lying in the rubble in front of it",
  "no sky, no wide view of the cut, no other person",
  cast(G5), refs=[G1848], roles=R5)

# rows 6, 7: the modern textbook (modern on purpose: it is the "story you've heard")
BOOK = ("a modern textbook: white matte pages, the printed text drawn ONLY as rows of soft grey wavy lines with no lettering, words or numbers")
S("row6-textbook-v1", "INSERT", "directly above, looking straight down", "50 mm",
  "a hand turns a page of an open textbook toward a small engraved diagram of a plain head in profile (an outline only, nothing inside it)",
  "studious, ordinary", "a modern textbook spread", "present day",
  f"{BOOK}; a small engraved head-in-profile diagram in the left margin; the shadowed gutter between the pages",
  "directly above the open book", "straight down at the spread",
  "a white matte page spread with a small engraved head diagram in the left margin and grey blurred text columns on both pages, the shadowed gutter in the middle",
  "no room, no desk edge",
  "CAST: no faces; only ONE adult hand and a plain shirt cuff entering at the lower right corner of the page.",
  extra=WAVY_WRITING,
  size_line=scale({"the open textbook": "each page about 24 cm (9 1/2 in) wide, a page as wide as a hand and a half", "the head diagram": "about 5 cm (2 in) tall, smaller than a thumb"}))
S("row7-monster-v1", "CU", "directly above, closer, a little to the right", "85 mm",
  "the same textbook page, closer: a crude cartoon scrawl of a snarling man with a single bold line across his head, and the page edges shadowing darker",
  "lurid, sensational", "a modern textbook spread", "present day",
  f"{BOOK}; a crude black pen cartoon of a snarling man with one bold line across his head",
  "directly above the right-hand page, closer than before", "straight down at the cartoon",
  "the crude cartoon drawing on a white page with a margin of grey wavy lines, the page corners falling into shadow",
  "no hand, no room",
  "CAST: no people in the frame (a drawing of a cartoon man is on the page; no real person, no hands).")

# row 8: the birth farm
S("row8-farm-v1", "LS", "eye level", "35 mm",
  "a small boy, seen only from behind, carries a wooden bucket across a farmyard toward a barn; the grass moves in a light breeze",
  "quiet, rural, a beginning", "a hill farm in Grafton County, New Hampshire", "summer, about 1823",
  "rolling green hills, a grey clapboard farmhouse and barn, a stone wall, warm summer sunlight",
  "in the farmyard at the edge of the field", "north across the yard toward the barn and the hills",
  "rolling green hills, a grey clapboard farmhouse and a barn, a stone wall along the yard, a wide summer sky",
  "no railroad, no rock cut, no road",
  cast("a boy of about eight, seen only from BEHIND, in a patched shirt, short trousers and a straw hat, carrying a wooden bucket in both hands"))

# rows 24, 25: the sickroom (Rule 0b: the patient is only a shape; the cloth and the candle carry it)
S("row24-sickroom-v1", "LS", "eye level, from the corner", "35 mm",
  "a woman wrings out a cloth over a basin on the washstand; beside her the bed holds only the shape of a body under a quilt; a candle burns low on the washstand",
  "tense, hushed", "a narrow sickroom under the roof of a Vermont inn", "September 1848, night",
  "a whitewashed plaster room, a sloped ceiling, a washstand with a basin, a bed, one candle, deep blue night in a small window",
  "in the corner of the room by the door", "across the room toward the washstand and the bed",
  "a narrow whitewashed room under a sloped ceiling, a washstand with a white basin, a bed under a quilt, a small window of deep blue night",
  "no door in view, no doctor",
  cast("a woman of about forty seen only from BEHIND at the washstand, in a dark dress and a white cap, wringing a cloth",
       extra="The bed holds only the SHAPE of a body under a quilt: no head, no face, no hair, no hand visible; it is not a person in view."))
S("row25-candle-v1", "CU", "low, at candle height", "85 mm",
  "a candle burned low on a wooden bedside table; behind it the small window shows the sky between deep blue night and grey dawn",
  "the hinge of the night, a held breath", "the same sickroom, close on the bedside table", "September 1848, before dawn",
  "a low candle, a wooden table, a small window with the sky at the edge of dawn",
  "close to the bedside table at candle height", "past the candle toward the small window",
  "the stub of a candle with a soft flame on a plain wooden table, the small window behind it with a sky going from deep blue to grey dawn",
  "no bed, no person, no hand",
  "CAST: no people in the frame (nobody, no hands).")

# row 28: Harlow writes (sheet-harlow)
HR = ("Reference 1 is DR JOHN MARTYN HARLOW's model sheet: take ONLY his face, hair, short beard and clothes from it; do NOT copy its layout, "
      "its other views or its poses. ")
S("row28-desk-v1", "MS", "eye level, over the desk", "50 mm",
  "DR HARLOW writes in a case book by lamplight, the quill moving across the page, his eyes on the page; his patient's case, noted day by day",
  "patient, watchful, attentive", "Dr Harlow's desk in Cavendish, Vermont", "autumn 1848",
  "a dark wooden desk, a case book open under an oil lamp, an ink pot, a dark bookcase, warm lamplight",
  "across the desk from him", "at him and the open case book",
  "the desk top with an open case book, an ink pot and the oil lamp, a dark bookcase of leather books behind him",
  "no window",
  cast(HARLOW + ', in shirtsleeves and a waistcoat, no spectacles, writing with a quill'),
  refs=[HARLOW_REF], roles=HR, extra=WAVY_WRITING)

# row 31: the contractor at the gate
S("row31-gate-v1", "MS", "eye level", "35 mm",
  "a contractor at a site gate closes his ledger with a snap and shakes his head slowly; at the lower right edge a man's hand slips down off the gate's top rail",
  "regretful, firm; a door closing", "the gate of a railroad contractors' work site, Vermont", "winter 1849",
  "a wooden gate in a split-rail fence, a plank site shed with a ledger table behind, the cut far behind in winter haze",
  "at the gate, facing the contractor", "at him and the gate",
  "a wooden gate in a split-rail fence, a plank site shed with a ledger table behind, the railroad cut far away in winter haze",
  "no rim of the cut, no close rock",
  cast("a stout, clean-shaven contractor of about fifty in a dark frock coat, a tall black hat and a heavy overcoat, a thick ledger in his hands",
       extra="At the lower right edge ONLY a man's hand and wrist in a worn white shirt sleeve slide down off the gate's top rail: no face, no body, no other person."),
  extra="The ledger's pages show only rows of soft grey wavy lines, no figures or lettering. " + WAVY_WRITING + "")

# row 36 ×3: the drawing, each copy cruder (modern book objects on purpose)
DRAW = "a pen drawing of a snarling man's head with one bold line across it"
S("row36a-oldbook-v1", "INSERT", "from the side, at table height", "50 mm",
  f"a heavy old leather-bound book lies open on a dark oak desk under a brass lamp; on its page {DRAW}, careful and neat",
  "authoritative, old", "an old library desk", "present day",
  "a dark oak desk, a brass lamp's warm pool, leather books on a shelf, the open book",
  "at the side of the desk at table height", "along the desk at the open book",
  "a dark oak desk with a brass lamp's warm pool and a shelf of leather books soft behind the open book",
  "no hand, no person",
  "CAST: no people in the frame (nobody, no hands).", extra=WAVY_WRITING)
S("row36b-textbook-v1", "INSERT", "from above and to the left, at an angle", "50 mm",
  f"a glossy textbook propped open on a pale classroom desk; on its page the same drawing, redrawn rougher and heavier",
  "official, a little careless", "a school classroom desk", "present day",
  "a pale classroom desk, a window of grey daylight, the propped-open textbook",
  "above and to the left of the desk", "down at the propped textbook",
  "a pale wooden classroom desk with a window of grey daylight and a blackboard edge soft behind the propped-open textbook",
  "no hand, no person",
  "CAST: no people in the frame (nobody, no hands).", extra=WAVY_WRITING)
S("row36c-paperback-v1", "INSERT", "flat top-down", "35 mm",
  "a cheap paperback with a cracked spine lies open on a worn table; on its page the drawing again, now a crude scrawl",
  "sensational, careless", "a worn kitchen table", "present day",
  "a worn wooden table, a pile of other paperbacks, a desk lamp",
  "directly above the table", "straight down at the open paperback",
  "a worn wooden table top with a pile of other battered paperbacks and the base of a desk lamp at the edge",
  "no hand, no person",
  "CAST: no people in the frame (nobody, no hands).", extra=WAVY_WRITING)

# rows 37, 38: the reading room (Macmillan is a living person: hands only, never a face)
S("row37-reports-v1", "CU", "directly above", "50 mm",
  "two hands untie a ribbon round a bundle of old reports on a green baize table; dust drifts in the lamp light",
  "patient, reverent", "a reading room table", "present day",
  "a green baize table top, a bundle of old yellowed reports tied with a ribbon, a brass lamp's pool of light",
  "directly above the table", "straight down at the bundle",
  "a green baize table top with a bundle of old yellowed reports tied with a dark ribbon in a brass lamp's pool of light",
  "no faces, no body",
  "CAST: no faces and no bodies; only TWO adult hands in plain shirt cuffs (a living scholar: never a face).",
  extra=WAVY_WRITING,
  size_line=scale({"the bundle of reports": "about 30 cm (12 in) long and 8 cm (3 in) thick, the width of two hands", "the ribbon": "about 1.5 cm wide"}))
S("row38-slips-v1", "INSERT", "from the side, low, at table level", "50 mm",
  "a thick book lands open on the baize with a soft thump, paper slips sticking out of its pages like feathers; on each slip a tiny drawing of the same crude head, each darker than the last",
  "weighty, damning", "the same reading room table", "present day",
  "a green baize table, the brass lamp, a thick open book bristling with paper slips",
  "at the table edge, low", "along the table at the book",
  "a green baize table edge, the foot of a brass lamp and a thick open book bristling with paper slips, the dark room behind",
  "no hands, no faces",
  "CAST: no people in the frame (nobody, no hands).", extra=WAVY_WRITING)

# row 46: the shut stable (row 45's set, wider, another camera)
S("row46-stabledoors-v1", "LS", "eye level, from far across the yard", "28 mm",
  "the tall plank stable doors are shut and barred, the yard in front of them empty; a few wisps of straw stir on the ground",
  "empty, a closing, a decision made", "a livery stable in Hanover, New Hampshire", "1852",
  "a weathered grey-brown plank stable, packed earth and straw, a wooden water trough, flat grey overcast light",
  "far across the yard near the gate, a little to the right of the doors", "at the shut double doors and the roof line",
  "two tall closed plank doors with a heavy wooden bar across them, the empty packed-earth yard in front with a few wisps of straw, a pale grey sky above the roof",
  "no horse, no person, no open doorway",
  "CAST: no people in the frame (nobody, no horse, no animal).")

# row 48: Valparaiso (a real period lithograph for the bay, a real coach photograph for the coaches)
S("row48-valparaiso-v1", "ELS", "high, from the hillside above the town", "24 mm",
  "Valparaiso bay with sailing ships at anchor, the town of houses climbing the dry hills; in the foreground a coach yard where new coaches stand in a row",
  "a new beginning, a wide horizon", "the harbour of Valparaiso, Chile", "1852",
  "a bay of grey-green water with tall sailing ships, whitewashed houses climbing pale dry hills, a dirt coach yard with new coaches in the foreground, bright afternoon sun",
  "high on the hillside above the coach yard", "down and out over the yard, the town and the bay",
  "a dirt coach yard with a row of new dark-red coaches in the foreground, below it the town climbing pale dry hills to a bay of tall sailing ships",
  "no mountain road, no close people",
  "CAST: no people in the frame (the coaches stand unattended; no figures).",
  refs=[STYLE_DETAIL, "proj:refs/valparaiso_1850s.jpg", "proj:refs/concord_coach.jpg"],
  roles=(STYLE_ROLE + "Reference 2 is a period lithograph of Valparaiso bay, used ONLY for the shapes of the ships, the pale hills and the houses; "
         "ignore its framing and composition. Reference 3 is a period photograph used ONLY for the shape of the coaches. "))

# row 54 ×2: the case, closed then open (the picture inside not seen yet)
S("row54a-caseclosed-v1", "MS", "eye level, at table height", "50 mm",
  "a closed brown leather daguerreotype case stands on a dark wooden table, its little brass clasp catching the light",
  "waiting, a held breath", "a quiet room with a dark table", "undated",
  "a dark wooden table and a pale plaster wall, soft window light from the left",
  "at the end of the table at table height", "along the table at the closed case",
  "a closed brown leather daguerreotype case standing on a dark wooden table, a pale plaster wall softly out of focus behind it",
  "no hands, no person, no open case",
  "CAST: no people in the frame (nobody, no hands).")
S("row54b-caseopen-v1", "CU", "above and in front, tilted down", "85 mm",
  "the same leather case now lies open on the table, its velvet-lined lid raised; the plate inside is a dark mirror-like surface in shadow, nothing visible on it yet",
  "a revelation about to happen", "a quiet room with a dark table", "undated",
  "a dark wooden table, an open leather case with a velvet lid, soft window light from the left",
  "above and in front of the case, close", "down and across at the open case",
  "an open brown leather case with a plum velvet lid and a dark mirror-like plate in a gilt mat, the dark wood grain of the table around it",
  "no hands, no person, no picture visible on the plate",
  "CAST: no people in the frame (nobody, no hands).")

# rows 59, 60: California, then the porch with the iron (Rule 0b: framing, no body)
S("row59-field-v1", "LS", "eye level", "35 mm",
  "a long-handled hoe stands upright in a furrow, left where it was dropped; the dry grass of the field bends in the wind",
  "empty, unsettling quiet", "a farm field near Santa Clara, California", "February 1860",
  "a dry golden field, a long dark furrow, low brown hills, a wide pale sky, a steady wind",
  "at the edge of the field in the furrow line", "along the furrow toward the hoe and the low hills",
  "a dry golden field with one long dark furrow running away, low brown hills behind and a wide pale windy sky",
  "no building, no person",
  "CAST: no people in the frame (nobody, no animal).")
S("row60-porch-v1", "LS", "eye level", "35 mm",
  "an empty wooden chair on a porch at evening; the tamping iron leans against the porch post beside it, its point up",
  "still, an ending", "a farmhouse porch in California", "May 1860, evening",
  "a worn wooden porch floor and a railing, a whitewashed wall, a golden evening sky, crickets",
  "on the porch steps, low", "along the porch at the chair and the post",
  "a worn wooden porch floor and railing, a whitewashed wall with a post, a golden evening sky beyond the rail",
  "no person, no body",
  "CAST: no people in the frame (nobody, no body, no hands).",
  refs=[STYLE_DETAIL, IRON_REF], roles=STYLE_ROLE + "Reference 2 is ONLY the SHAPE of the iron: a long, straight, perfectly round rod of one even thickness, no knob, no flared end; ignore its grey background and its blur. ",
  extra=f"The iron is {IRON_ROD2}.",
  size_line=sizes({"the tamping iron leaning on the post": "109 cm long, thin as a broom handle, taller than the seat of the chair is high (the chair seat about 45 cm), reaching up to a man's hip",
                   "the chair": "a plain wooden chair, seat about 45 cm high"}))

# row 61: Harlow, older and grey (the older head of sheet-harlow)
S("row61-letter-v1", "MS", "eye level, from the side", "50 mm",
  "DR HARLOW, older and grey, reads a letter by a window in the grey daylight, the page held in both hands, a quiet, weighing look",
  "thoughtful, a last request", "Dr Harlow's study, Woburn, Massachusetts", "1867",
  "a window with a lace curtain and grey daylight, a writing desk with an inkwell, a dark wood floor",
  "at the side of the desk by the window", "at him and the window",
  "a tall window with a lace curtain and grey daylight beside a writing desk with an inkwell and a dark wood floor",
  "no 1848 room, no lamp",
  cast(HARLOW_OLD + ', waist up, reading the letter, no spectacles'),
  refs=[HARLOW_REF],
  roles=("Reference 1 is DR JOHN MARTYN HARLOW's model sheet: take his face from it, and for his hair and beard use its OLDER head close-up (48 "
         "in 1867, grey-streaked); do NOT copy its layout, its other views or its poses. "),
  extra=WAVY_WRITING)

# row 64: the lecture (casting cards; the rest from behind)
S("row64-lecture-v1", "LS", "eye level, from the back of the room", "28 mm",
  "a lecturer points his wooden pointer at the FRONT part of a plain skull outline on the blackboard while the listeners lean in and some nod",
  "attentive, a lesson landing", "a medical college lecture theatre", "the 1870s",
  "a raked lecture theatre, curved wooden benches, tall windows, a blackboard with a drawn skull outline in side view, gaslight",
  "at the back of the raked theatre", "down the room toward the blackboard",
  "rows of curved wooden benches full of listeners seen from behind, a blackboard at the front with a plain skull outline in side view, tall arched windows either side",
  "no bar drawn in the skull, no Boston room",
  cast("a tall gaunt lecturer of about fifty in a black frock coat with a long grey moustache and no beard, pointing with a wooden pointer",
       extra=crowd("the listeners on the benches", ["a young man in the front row, clean-shaven, nodding", "a heavy man with grey mutton-chop whiskers, arms folded", "a thin man with a high bald head, leaning forward"])))

KEYFRAMES.update(B3)

# ── 2026-11-25 (user): row 13, ONE still ($0.067): the iron alone, a candidate for iron-ref-v2.png ─────────────────────────────
B4 = {}
B4["row13-iron-v1"] = dict(aspect="16:9", refs=[STYLE_DETAIL, IRON_REF],
    roles=(STYLE_ROLE + "Reference 2 is ONLY the PROPORTION and straightness of the iron: a long, straight, perfectly round rod of one even "
           "thickness along its whole length, pointed at ONE end only; ignore its grey background and its blur. "),
    prompt=(f"{set_block('a flat grey rock ledge in the open air', 'September 1848', 'a flat grey rock surface, clear low morning light from the left, a soft pale sky blur behind, nothing else')} "
            f"{framing('MS', 'dead level with the rock, a pure side view', '50 mm', 'the tamping iron lies alone on a flat rock, perfectly horizontal, its full length filling the width of the frame from the left edge to the right edge', 'quiet, plain, a small heavy object')} "
            f"{camera('beside the rock at its own height, square on to the iron', 'straight at the side of the iron', 'a flat grey rock surface and a soft pale morning sky blur behind', 'no person, no hand, no other object')} "
            f"{NOBODY} The iron is {IRON_ROD2}. Draw it as ONE straight rod with the POINTED end at the RIGHT and the BLUNT, flat-cut end at the LEFT: "
            "the thickness stays the same along the whole rod until the last foot at the right, where it narrows smoothly to a point; the LEFT end is cut flat and is NOT pointed, "
            "NOT rounded, NOT flared. A smooth dull dark-grey surface with a soft highlight along the top; no inscription, no marks and no writing anywhere on it. "
            + sizes({"the tamping iron": "109 cm long and 3.2 cm thick, as thin as a broom handle, lying on a flat rock ledge"})
            + f" {SAFE_FRAMING} {PERIOD} {NO_TEXT}"))
KEYFRAMES.update(B4)


def main():
    chs = chapters()
    assert [c["id"] for c in chs] == [f"ch{i}" for i in range(9)], [c["id"] for c in chs]
    rows = [n for c in chs for n, _ in c["rows"]]
    assert rows == [n for n in range(1, 68) if n != 51], "script rows missing or out of order"
    narr = [{"id": c["id"], "title": c["title"], "v3_text": "\n".join(t for _, t in c["rows"]),
             "gap_after": 3.3 if c["id"] == "ch0" else 1.2} for c in chs]
    if "--print" in sys.argv:
        for c in narr:
            print(f"== {c['id']} {c['title']} ({len(c['v3_text'])} chars)\n{c['v3_text']}\n")
        print(sum(len(c["v3_text"]) for c in narr), "characters")
        return
    for d in ("assets/audio", "artifacts", "refs"):
        (P / d).mkdir(parents=True, exist_ok=True)
    f = P / "episode.json"
    ep = json.load(open(f, encoding="utf-8")) if f.exists() else {}
    ep.update({"title": "Phineas Gage: The Story Everyone Gets Wrong (HC002-L)", "playbook": "storybook-medical",
               "format": "long", "theme": {"culture": "new-england-1840s", "font": "montserrat"},
               "image_resolution": "2K", "dual_format": False, "references": REFERENCES, "keyframes": KEYFRAMES,
               "use_mirrored": USE_MIRRORED,   # user 2026-11-24: these mirrored copies are the stills used (originals kept)
               "storyboard": "2026-11-22: long-storyboard-v1.md + long-backgrounds-v1.md; images approved (user 2026-11-22)",
               "previz_approved": "2026-11-22: user approved the long's images (~$3.50) once its refs were in; cast + HERO first"})
    ep.setdefault("narration", {})
    if not ep["narration"].get("chapters"):
        ep["narration"]["chapters"] = narr
    ep["narration"].setdefault("punch_words", [])
    json.dump(ep, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES}, require_matt=False)
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{f}: {len(narr)} chapters, {len(REFERENCES)} references ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
