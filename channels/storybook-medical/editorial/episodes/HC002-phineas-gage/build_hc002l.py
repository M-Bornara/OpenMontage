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
                        camera, cast, framing, lint_all, pose_sheet, set_block, sprite_sheet)

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
