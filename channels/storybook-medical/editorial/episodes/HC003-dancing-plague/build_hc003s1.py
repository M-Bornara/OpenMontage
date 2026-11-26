"""HC003-S1 Dancing Plague: writes projects/hc003-s1/episode.json (title, narration, references, keyframes) from the
approved script v3 (s1-story-v3.md: ending A, hook card A, title 1, theme rhine-1518 pending the listen; fact gate 21
PASS) and storyboard v1 + backgrounds v1 (APPROVED 2026-11-22 with one fix: shot 14 without the coif), then lints every
image prompt. The narration is read from the script block of s1-story-v3.md, so what Liam reads is exactly what the
gate passed.
Order (as Gage / Pettenkofer; user 2026-11-22): narration (done) -> the 2 cast sheets -> the 3 HERO shots' pieces,
shown on real art -> only then the story stills (KEYFRAMES, added after the HERO shots are approved).
    python channels/storybook-medical/editorial/episodes/HC003-dancing-plague/build_hc003s1.py
    python channels/storybook-medical/scripts/episode.py refs hc003-s1 sheet-troffea sheet-townsfolk --batch
    python channels/storybook-medical/scripts/episode.py refs hc003-s1 <HERO_PIECES> --batch
Root-cause rule (L40 / L47b / L55): NO set plate and NO keyframe is ever a reference; each plate's background is written
out from s1-backgrounds-v1.md (camera()) and its references are only period images (architecture) or the people in it.
Sheets are 16:9 (L54); plates 9:16.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (EMPTY_HANDS, KEY_BG, FULL_BLEED, NO_TEXT, ONE_EACH, PERIOD, REF_IDENTITY_ONLY, SAFE_FRAMING,  # noqa: E402
                        camera, framing, lint_all, lint_lookalikes, pose_sheet, set_block, sprite_sheet)

PID = "hc003-s1"
P = REPO / "projects" / PID
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"          # HC001 model sheet: layout + style only (a sheet, not a scene)
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "


def narration() -> str:
    md = (HERE / "s1-story-v3.md").read_text(encoding="utf-8")
    block = re.search(r"```\n(\[intense\] Strasbourg.*?)\n```", md, re.S).group(1)
    assert "four hundred people had joined the dancing" in block and "others started dancing too" in block
    return block.strip()


def sizes(items: dict) -> str:
    """A SCALE line for pieces that must stay EMPTY of hands (scale() names a hand as its ruler, and a hand named in an
    empty plate gets painted in, L47): sizes in inches / cm only."""
    return "SCALE (true sizes, keep these proportions): " + "; ".join(f"{k} {v}" for k, v in items.items()) + "."


# ── people (storyboard "Sets and cast"; no portrait of Troffea exists: dress after Dürer 1500 / Hondius 1642) ────────
TROFFEA = ("FRAU TROFFEA, a townswoman of Strasbourg in July 1518 (about 30, slim, a plain kind oval face, tired grey eyes, "
           "a few freckles; her hair completely covered by a white linen coif that wraps the head and ties under the chin, "
           "its two long ends hanging down her back; an ankle-length mid-blue wool gown with a fitted bodice laced at the "
           "front and long sleeves, a pale undyed linen apron, worn brown leather shoes; no jewellery, nothing red)")
TOWNSFOLK = [
    "her HUSBAND, a craftsman of about 35, short dark-brown hair, clean-shaven, a worried face, a plain brown wool doublet, dark hose, no cap",
    "a CITY MAN, tall, about 40, a short trimmed black beard, a flat black cap, the city's livery: a knee-length tunic split dark-red and white",
    "a second CITY MAN, broad and bald, about 50, clean-shaven, a heavy jaw, the same dark-red and white livery tunic, no cap",
    "a PRETZEL SELLER, a thin freckled youth of about 18, sandy hair, a linen shirt and a grey jerkin, a wooden tray of pretzels on a strap",
    "an OLD WOMAN of about 70, a deeply lined face, a dark-brown hood over her head and shoulders",
    "an APPRENTICE of about 14, round-faced, a green felt cap, a leather apron",
    "a NUN of about 50, a round calm face, a black veil over a white wimple, a black habit",
    "a stout BURGHER of about 55, a short grey beard, a flat black velvet cap, a dark gown with a wide fur collar",
]
T, TF = "ref:sheet-troffea", "ref:sheet-townsfolk"
T_ROLE = "Reference 1 is FRAU TROFFEA's model sheet (face, coif, gown, build). "

REFERENCES = {
    "sheet-troffea": dict(aspect="16:9",
        refs=[SHEET_LAYOUT, "proj:refs/durer_nuremberg_woman_dance_1500.jpg", "proj:refs/hondius_dancing_pilgrims_1642.jpg"],
        roles=(SHEET + "Reference 2 is Albrecht Dürer's 1500 drawing of a townswoman of the Upper Rhine dressed for a dance: take "
               "the SHAPES of her dress from it (the long gown, the fitted bodice, the white linen head covering, the shoes) as a "
               "plainer EVERYDAY version, painted in our storybook style, never as a drawing or a copy. Reference 3 is an "
               "engraving of the dancing pilgrims of the 1500s: period dress and the way the dancers move only; not its people, "
               "faces or layout. "),
        prompt=(f"Clean character model sheet on plain bone-white paper: {TROFFEA}. Front view, three-quarter view, profile "
                "view facing RIGHT and back view, all full length from the coif to the shoes, plus three head close-ups (calm "
                "and far away, eyes half closed; exhausted, eyes down; turning, the coif ends swinging). Same scale in every "
                "view. A woman of a free imperial city on the Rhine in 1518, period-true. No text, labels or watermark.")),
    "sheet-townsfolk": dict(aspect="16:9",
        refs=[SHEET_LAYOUT, "proj:refs/durer_dancing_peasants_1514.jpg", "proj:refs/durer_bagpiper_1514.jpg"],
        roles=(SHEET + "References 2 and 3 are Albrecht Dürer's 1514 engravings of townspeople and a musician: period dress "
               "(doublets, hose, caps, gowns) only, painted in our storybook style; not their faces, poses or layout. "),
        prompt=("Clean character model sheet (a line-up) on plain bone-white paper: eight different people of Strasbourg in "
                "1518, in TWO rows of four, each waist up, front view: "
                + "; ".join(f"({i}) {c}" for i, c in enumerate(TOWNSFOLK, 1)) + ". Each has a clearly different face, age, "
                "build, hair and expression; no look-alikes, no twins, nobody in a blue gown with a white linen coif (that "
                "is the heroine's look), and nobody wears eyeglasses. No text, labels or watermark.")),
}

# ── HERO pieces (layered-shot: the plate is empty of what moves; the sheets hold exactly the states the keys use) ─────
LANE = set_block("a narrow cobbled lane in Strasbourg", "July 1518",
                 "tall half-timbered houses close on both sides with dark oak beams, ochre and cream plaster, overhanging "
                 "upper storeys and steep tiled roofs, wooden shutters, a stone gutter down the middle of the cobbles; the "
                 "single tall spire of the cathedral rising over the roofs to the north")
SQUARE = set_block("the small square at the south end of the same lane", "July 1518",
                   "cobbles, the arched stone gate of the city wall, half-timbered house corners at the edges")
S1_LIGHT = "hard midday summer sun from the upper RIGHT, short shadows to the lower left"
S4_LIGHT = "dusk: she is lit from BEHIND by the last purple-orange sky at the end of the lane (backlit, almost a silhouette), a faint warm rim on her right side from a lit doorway"
S10_LIGHT = "bright midday summer sun from the upper LEFT, short shadows to the lower right"

REFERENCES.update({
    # shot 1 (frame 1, hook card A in the band 0.51-0.65): the lane, the spire; NO Troffea, NO shutter (its sprite)
    "plate-s1": dict(aspect="9:16",
        refs=["proj:refs/strasbourg_kammerzell.jpg", "proj:refs/merian_strasbourg_1644.jpg"],
        roles=("Reference 1 is a photo of a real Strasbourg half-timbered house: the architecture only (beams, overhanging "
               "storeys, windows), painted in our storybook style, never traced and never this exact house. Reference 2 is "
               "a 1644 view of Strasbourg: the cathedral's single spire and the roofs only. "),
        prompt=(f"{LANE} "
                f"{framing('MS', 'eye level, slightly low', '35 mm', 'the middle of the lane where a woman will dance alone (she is added later)', 'strange, quiet, hot midday')} "
                f"{camera('in the middle of the lane, a few steps back', 'north up the lane', 'half-timbered house fronts close on both sides with overhanging upper storeys, the cathedral spire small and pale in the gap between the roofs, hard midday sun', 'the square and the gate are NOT in view')} "
                "High on the LEFT wall, at about 0.22-0.32 of the frame height, an EMPTY dark window opening with NO shutter "
                "(a shutter is added there later). The middle of the lane is EMPTY cobbles from about 0.25 to 0.95 of the "
                "frame height: a woman about 0.7 of the frame height tall is added there later. EMPTY LOCATION PLATE: no "
                "people, no figures, no hands anywhere. "
                f"{sizes({'the lane': 'about 11 ft (3.5 m) wide', 'the window opening': 'about 2 x 3 ft (60 x 90 cm)', 'a cobblestone': 'about 5 x 6 in (12 x 15 cm)'})} "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "pose-troffea-s1": dict(aspect="16:9", refs=[T], roles=T_ROLE,
        prompt=pose_sheet(TROFFEA,
                          ["mid-turn to her LEFT, both arms half raised and bent at the elbows, palms open, the blue skirt "
                           "flaring out to the LEFT, the coif ends swinging left, her face calm and far away, eyes half closed. "
                           + EMPTY_HANDS.replace("His", "Her"),
                           "EXACTLY the same woman, face and costume; ONE change: mid-turn the other way, to her RIGHT, the "
                           "arms swung over to the right, the skirt flaring out to the RIGHT, the coif ends swinging right. "
                           + EMPTY_HANDS.replace("His", "Her")],
                          "s1: alone in the middle of a sunny cobbled lane", S1_LIGHT,
                          "from the front, eye level, slightly low, 35 mm", "the whole figure from the coif to the shoes")),
    "sprite-shutter-s1": dict(aspect="16:9", refs=[], roles="",
        prompt=sprite_sheet("wooden window shutter of a half-timbered house (vertical oak planks with two iron strap hinges "
                            "on its LEFT edge, weathered grey-brown)",
                            ["closed, flat, seen from below at a steep upward angle",
                             "EXACTLY the same shutter swung open on its left hinges about 70 degrees toward the viewer, seen "
                             "from the same low angle, its planks in perspective"],
                            "s1: high on a house wall over a sunny lane", S1_LIGHT,
                            "from the lane below, looking steeply up at a window high on the left wall",
                            sizes({"the shutter": "about 2 x 3 ft (60 x 90 cm)"}))),
    # shot 4 (the collapse, dusk, low from the cobbles): NO Troffea, NO coif (both are pieces)
    "plate-s4": dict(aspect="9:16", refs=["proj:refs/strasbourg_kammerzell.jpg"],
        roles=("Reference 1 is a photo of a real Strasbourg half-timbered house: the architecture only, painted in our "
               "storybook style as dark dusk silhouettes, never traced. "),
        prompt=(f"{LANE} "
                f"{framing('MLS', 'low angle, the camera just above the cobbles', '28 mm', 'the far middle of the lane at dusk where a dancing woman will turn and fall (she is added later)', 'exhausted, ominous, quiet')} "
                f"{camera('low on the cobbles at the north end of the lane', 'south-south-west down the lane', 'the lane narrowing away to a purple-orange dusk sky at its south end, the house fronts black silhouettes with two warm lit windows, an open doorway on the right spilling lamplight', 'the spire is behind the camera and NOT in view')} "
                "The cobbles in the far middle of the lane, from about 0.3 to 0.75 of the frame height, are EMPTY (a figure "
                "about half the frame height tall is added there later), and the near cobbles in the lower LEFT foreground "
                "are EMPTY (a small piece of white cloth lands there later). EMPTY LOCATION PLATE: no people, no figures, "
                f"no hands, no shadows of people. "
                f"{sizes({'the lane': 'about 11 ft (3.5 m) wide', 'a cobblestone': 'about 5 x 6 in (12 x 15 cm)', 'the doorway': 'about 3 x 6 ft (90 x 185 cm)'})} "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # L45b: no model-sheet reference for a lying pose (it prints ghosts); she is turned into a flat black silhouette in code
    "pose-troffea-s4": dict(aspect="16:9", refs=[], roles="",
        prompt=pose_sheet(TROFFEA,
                          ["still dancing, turning, both arms out, the skirt flaring, on her feet, seen from the front-side",
                           "EXACTLY the same woman and gown; ONE change: fallen on the ground, lying on her side with her "
                           "knees drawn up and one arm stretched out, exhausted; her white coif has come OFF (it is NOT in "
                           "this drawing): her dark-brown hair in a loose plait"],
                          "s4: in a lane at dusk, seen from low on the cobbles", S4_LIGHT,
                          "from low on the ground, a little below her, 28 mm", "the whole figure")),
    "sprite-coif-s4": dict(aspect="16:9", refs=[T], roles=T_ROLE + "Only her white linen COIF (head covering) is drawn here. ",
        prompt=sprite_sheet("white linen coif (a woman's head covering of 1518 with two long tie ends), empty, nobody wearing it",
                            ["falling through the air at its FULL size, open and softly billowing, the two ties trailing above it",
                             "EXACTLY the same coif at the SAME full size come to rest, lying open and nearly flat with a few soft folds, seen from low and almost side-on"],
                            "s4: big in the foreground of a dusk lane, low on the cobbles",
                            "cool purple dusk light all round, a faint warm rim from a lit doorway at the RIGHT",
                            "from low, just above the ground, close",
                            sizes({"the coif": "about 10 in (25 cm) across, its ties about 16 in (40 cm) long"}))),
    # shot 10 (the wagon): the square and the gate; NO wagon, NO people (pieces)
    "plate-s10": dict(aspect="9:16", refs=["proj:refs/merian_strasbourg_1644.jpg"],
        roles=("Reference 1 is a 1644 view of Strasbourg: the city wall and its arched stone gates only, painted in our "
               "storybook style, never copied. "),
        prompt=(f"{SQUARE} "
                f"{framing('MLS', 'eye level', '35 mm', 'the place by the city gate where a wagon will wait to take a dancing woman away (all added later)', 'sad, frightened, final')} "
                f"{camera('at the south end of the lane, at the edge of the small square', 'south toward the city gate', 'the small cobbled square and, behind it in the middle distance, the arched stone gate of the city wall with its heavy timber doors open, a strip of summer sky above; half-timbered house corners at the left and right edges', 'the lane behind the camera and the spire are NOT in view')} "
                "The cobbles of the square from about 0.45 to 0.95 of the frame height are EMPTY across the whole width (a "
                "covered wagon and three people are added there later). EMPTY LOCATION PLATE: no people, no wagon, no "
                "horses, no figures, no hands anywhere. "
                f"{sizes({'the gate arch': 'about 13 ft (4 m) high', 'a cobblestone': 'about 5 x 6 in (12 x 15 cm)'})} "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # a pose sheet of a GROUP (pose_sheet() is one person): the same three people in the shot's two poses
    "pose-s10": dict(aspect="16:9", refs=[T, TF],
        roles=(T_ROLE + "Reference 2 is the townsfolk line-up: use ONLY the two CITY MEN (numbers 2 and 3, the dark-red and "
               "white livery). "),
        prompt=("POSE SHEET for cut-out animation: the SAME group of three people drawn twice in ONE row from left to right, "
                "each group separate with wide empty space around it: FRAU TROFFEA between the two city men (the tall one with "
                "the short black beard on her LEFT, the broad bald one on her RIGHT). (1) the two men each hold her gently with "
                "one hand under her arm, lifting her a little as if onto a wagon's tail; her arms still raised and swaying to "
                "a beat nobody hears, her face far away. (2) EXACTLY the same three people; ONE change: she now SITS on an "
                "invisible ledge at hip height (the wagon is NOT drawn: her legs hang down, her hands rest beside her), still "
                "swaying, and the two men have stepped back half a pace, letting go. Each drawing shows the whole figures, the "
                "identical size, costumes, faces and proportions, seen from the same camera: from the front-side, eye level, "
                f"35 mm. LIGHT: as in the shot (s10: a sunny square by the city gate): {S10_LIGHT}. Only these three people, "
                f"no wagon, no horses, no ground. Ink outline and painting style of our film. {REF_IDENTITY_ONLY} {KEY_BG} "
                f"{FULL_BLEED} {NO_TEXT}")),
    "sprite-wagon-s10": dict(aspect="16:9", refs=[], roles="",
        prompt=sprite_sheet("covered farm wagon of 1518 (a long wooden bed with a hooped off-white canvas cover, its tail-board "
                            "let down at the RIGHT end; the shafts point out to the LEFT, with NO horses drawn)",
                            ["the wagon BODY alone, WITHOUT its wheels, side view facing LEFT",
                             "ONE large spoked wooden wagon wheel with an iron rim, seen exactly side-on, alone"],
                            "s10: in a sunny cobbled square by a city gate", S10_LIGHT,
                            "from the side, eye level, 35 mm",
                            sizes({"the wagon bed": "about 10 ft (3 m) long", "the wheel": "about 4 ft (1.2 m) across"}))),
})

HERO_PIECES = ["plate-s1", "pose-troffea-s1", "sprite-shutter-s1", "plate-s4", "pose-troffea-s4", "sprite-coif-s4",
               "plate-s10", "pose-s10", "sprite-wagon-s10"]
KEYFRAMES: dict = {}          # the story stills: written after the HERO shots are approved on real art

# L61: the lead's signature look; no extra may carry it (checked here and by episode.py before any paid call)
SIGNATURES = {"Troffea": [r"blue (?:wool )?gown", r"white linen coif"]}


def main():
    from lib.checkpoint import init_project
    if not (P / "project.json").exists():
        init_project(PID, title="The Woman Who Couldn't Stop Dancing", pipeline_type="animated-explainer")
    import episode
    episode.step_init(PID)
    for d in ("assets/audio", "artifacts", "refs"):
        (P / d).mkdir(parents=True, exist_ok=True)
    f = P / "episode.json"
    ep = json.load(open(f, encoding="utf-8")) if f.exists() else {}
    ep.update(title="The Woman Who Couldn't Stop Dancing", playbook="storybook-medical", format="short",
              dual_format=False, image_resolution="2K", loop=True, tail_seconds=1.0,
              references=REFERENCES, keyframes=KEYFRAMES,
              theme={"culture": "rhine-1518", "font": "montserrat"}, motion_lint="fail",
              glasses="s7: Matt at an upper window, the ? glint on his spectacles (Matt cameo, L29)",
              storyboard="2026-11-22: s1-storyboard-v1.md + s1-backgrounds-v1.md APPROVED (fix: shot 14 without the coif)",
              previz_approved="2026-11-22: user approved the storyboard + free pre-viz; HERO pieces on real art next")
    ep.setdefault("narration", {"punch_words": []})
    ep["narration"]["v3_text"] = narration()
    ep["signatures"] = SIGNATURES
    json.dump(ep, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES}, require_matt=False)
    for n, v in lint_lookalikes({k: v for k, v in REFERENCES.items() if k not in ("sheet-troffea", "sprite-coif-s4", "pose-troffea-s1", "pose-troffea-s4", "pose-s10")}, SIGNATURES).items():
        issues.setdefault(n, []).extend(v)
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {f}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
