"""HCS10 Pettenkofer: writes projects/hcs10-pettenkofer/episode.json (title, narration, references, keyframes) from
storyboard-v1.md (APPROVED 2026-11-20 with 4 fixes) and backgrounds-v1.md, with the prompt_kit blocks, then lints
every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/build_hcs10.py
Order (user 2026-11-20, "same as Gage"): narration -> the 2 cast sheets -> the 4 HERO shots' pieces, shown on real art
-> only then the 9 story stills (KEYFRAMES, added after the HERO pieces are approved).
    episode.py narrate hcs10-pettenkofer
    episode.py refs hcs10-pettenkofer sheet-pettenkofer sheet-students --batch
    episode.py refs hcs10-pettenkofer <the 9 HERO pieces> --batch

Every story frame here follows the 2026-11-20 root-cause rule (L47b / L40 / L55): NO set plate and NO other keyframe is
ever a reference; each frame's background is written out (camera() from backgrounds-v1.md) and its references are only
the people in it. Every hand close-up carries a scale() line (L51) with the storyboard's true sizes, the same sizes the
free pre-viz (hero_previz_hcs10.py) was drawn to. Sheets are 16:9 (L54).
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (EMPTY_HANDS, FULL_BLEED, NO_TEXT, ONE_EACH, PERIOD, SAFE_FRAMING, WAVY_WRITING, camera, cast,  # noqa: E402
                        framing, lint_all, matt_beat, pose_sheet, scale, set_block, sprite_sheet)

PID = "hcs10-pettenkofer"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"          # HC001 model sheet: layout + style only (a sheet, not a scene)
MATT = "kit:matt-sheet.jpg"

# script approved 2026-11-18 (storyboard-v1.md "Script"), word for word
NARRATION = """[intense] Munich, 1892. A seventy-three-year-old professor is about to drink cholera.
[serious] Cholera had just killed about eight thousand six hundred people in Hamburg.
Robert Koch blamed a germ in the water. Max von Pettenkofer said: the germ alone isn't enough.
[quiet] His students offered to go first, he wrote. He said no.
Baking soda first, to calm his stomach acid. Then germs from Hamburg. Less than a teaspoon.
One gulp. "Like the purest water," he wrote.
[pause] [whispers] Two days later… the cramps began.
For a week. His gut swarmed with cholera germs.
[curious] But it never turned deadly. He declared victory.
His critics: that was cholera. Just a mild case.
The baking soda? It helped the germs. [pause] He survived the bet… but not the argument."""

# ── people (storyboard "Sets and cast"; faces from the refs the user saved 2026-11-20) ───────────────────────────────
PETTENKOFER = ("MAX VON PETTENKOFER, the professor (73, old and frail but upright; white hair brushed straight back from a "
               "high forehead, a broad full white beard and white moustache, heavy grey-white brows, deep-set tired eyes, "
               "a long straight nose; a dark frock coat, a dark waistcoat, a white shirt with a high collar, a dark tie)")
STUDENTS = ["a tall young man of about 22 with fair blond hair parted at the side and no beard, a long thin face",
            "a young man of about 25 with dark wavy hair and a dark moustache, a square jaw",
            "a short, round-faced young man of about 20 with light brown cropped hair and round cheeks, no beard"]
STUDENT_DRESS = "dark 1890s three-piece suits, white shirts with stiff collars, dark ties"
P, ST = "ref:sheet-pettenkofer", "ref:sheet-students"
P_ROLE = "Reference 1 is MAX VON PETTENKOFER's model sheet (face, hair, beard, build, clothes). "

# ── sets (one look each, L19; the lab appears in 9 shots, each from its own camera: backgrounds-v1.md) ───────────────
LAB = set_block("Max von Pettenkofer's hygiene laboratory in Munich", "October 1892",
                "long wooden benches of dark oak, a brass microscope, glass flasks, beakers and stoppered jars, "
                "glass-fronted cabinets along the north wall, tall leaded windows on the west wall, brass gas lamps; "
                "amber lamplight against grey autumn daylight")
DESK = set_block("Pettenkofer's own writing desk in the corner of his Munich laboratory", "October 1892",
                 "a heavy dark oak desk top, worn and scratched, loose folio papers covered in handwriting, a glass inkwell; "
                 "cold grey daylight")

SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "
PORTRAITS = ("References 2 and 3 are portraits of the real Max von Pettenkofer in the 1890s (a painting by Lenbach and a "
             "photograph of about 1898): paint THIS face (head shape, high forehead, white hair brushed back, the broad full "
             "white beard, heavy brows, deep-set eyes, nose) in our storybook style, aged 73, never as a photograph, and do "
             "not copy the portraits' poses, frames or backgrounds. ")


def sizes(items: dict) -> str:
    """A SCALE line for a plate that must stay EMPTY of hands: scale() names "an adult man's hand" as its ruler, and a
    hand named in an empty plate gets painted in (L47); so sizes here are in inches / cm only."""
    return "SCALE (true sizes, keep these proportions): " + "; ".join(f"{k} {v}" for k, v in items.items()) + "."


NOT_HERE = "{who} is NOT in this picture (he is animated in later as a separate cut-out): leave the place where he stands empty."

REFERENCES = {
    "sheet-pettenkofer": dict(aspect="16:9",
        refs=[SHEET_LAYOUT, "proj:refs/pettenkofer_lenbach_1890s.png", "proj:refs/pettenkofer_c1898.jpg"],
        roles=SHEET + PORTRAITS,
        prompt=(f"Clean character model sheet on plain bone-white paper: {PETTENKOFER}. Front view, three-quarter view, "
                "profile view facing RIGHT, back view, all from the waist up, plus three head close-ups (calm and certain; "
                "looking down at something small in his hand; head tipped back, eyes half closed). Same scale in every "
                "view. His hands are old, with thin skin and visible veins. No text, labels or watermark.")),
    "sheet-students": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=("Clean character model sheet (a line-up) on plain bone-white paper: three different university students "
                "of 1892 in Munich, standing side by side, waist up, front view: "
                + "; ".join(f"({i}) {c}" for i, c in enumerate(STUDENTS, 1)) + f". All in {STUDENT_DRESS}. Below each, a "
                "small back view of the same student (head and shoulders from behind). Each has a clearly different face, "
                "age, build and hair; no look-alikes. No text, labels or watermark.")),
}

# ── HERO pieces (layered-shot: the plate is empty of what moves; the sheets hold exactly the states the keys use, the
#    same names and states as the approved stand-ins in assets/images/sprites/) ─────────────────────────────────────
S1_LIGHT = "warm amber gas lamplight from high on the LEFT, the right side of things in deep warm shadow"
S4_LIGHT = "cool grey daylight from a tall window at the LEFT, soft shadows to the right"
S6_LIGHT = "pale grey daylight from the tall window in FRONT of him (the right of the picture), his profile lit, a soft rim"
S7_LIGHT = "cold grey daylight from the upper LEFT, soft shadows down and to the right"

REFERENCES.update({
    # shot 1 (frame 1, hook card A over the wall above his head): his face, NO glass, NO hands
    "plate-s1": dict(aspect="9:16", refs=[P], roles=P_ROLE,
        prompt=(f"{LAB} "
                f"{framing('CU', 'eye level, slightly low', '85 mm, shallow focus', 'the old professor looks down, calm and steady, at something small just below his chin (it is added later)', 'calm, certain, unafraid')} "
                f"{camera('at the south side of the bench, close to him', 'north', 'the dark north wall far behind him, out of focus: one amber gas-lamp glow high on the left, dim shapes of glass flasks on a shelf, deep brown shadow', 'no windows, no daylight, no benches in view')} "
                f"{cast(PETTENKOFER)} His head and shoulders fill the frame: his face is about 0.42 of the frame width, "
                "his face centred left to right; the centre of his face at about 0.55 of the frame height and the TOP "
                "of his white hair LOW, at about 0.35 of the frame height: the whole upper third of the frame is only the "
                "dark, calm wall and the lamp glow, with nothing of him in it (a title is placed there later). His mouth is just visible under the white moustache, lips closed. NO glass, NO cup and NO hands "
                "anywhere in the picture, and nothing held or lying in front of him; his arms are down out of frame. "
                f"{sizes({'his face': 'about 6 in (15 cm) wide'})} {ONE_EACH} {PERIOD} {NO_TEXT}")),
    "sprite-hand-glass-s1": dict(aspect="16:9", refs=[P], roles=P_ROLE + "Only his HAND and coat sleeve are drawn here. ",
        prompt=sprite_sheet("old man's RIGHT hand holding a small drinking glass, the hand and the dark frock-coat sleeve "
                            "with a white shirt cuff at the bottom, the wrist upright, the glass held in front of the "
                            "fingers at the top, a little clear liquid in its bottom",
                            ["the glass held upright, seen from the front, the fingers wrapped round it and the thumb on the side",
                             "EXACTLY the same hand and glass, tipped a little toward the viewer's LEFT"],
                            "s1: a close-up of his face by amber lamplight", S1_LIGHT, "from the front, at face height",
                            scale({"the small glass": "about 2 3/4 in (7 cm) tall and 2 in (5 cm) across, smaller than the hand",
                                   "the liquid": "only about 1/2 in (1 cm) deep, clear, nothing in it",
                                   "the hand": "old and thin-skinned, with visible veins"}))),
    "sprite-student-hand-s1": dict(aspect="16:9", refs=[ST], roles="Reference 1 is the students (student 1, the tall blond one: his sleeve and hand only). ",
        prompt=sprite_sheet("young man's RIGHT hand and forearm in a dark 1890s suit sleeve with a white shirt cuff, coming "
                            "in from the RIGHT, the fingers pointing LEFT",
                            ["reaching out, the fingers open and stretched toward the left",
                             "stopped short: EXACTLY the same hand and sleeve, the fingers spread and lifted a little, hesitating"],
                            "s1: a close-up of the old professor's face by amber lamplight", S1_LIGHT,
                            "from the front, at face height, the forearm level",
                            scale({"the hand": "a young man's hand, about 7 1/2 in (19 cm) from wrist to fingertip",
                                   "the sleeve": "about 3 1/2 in (9 cm) wide"}))),
    # shot 4 (OTS, MS, push in to "no"): the bench, Matt, two students' backs; NO Pettenkofer
    "plate-s4": dict(aspect="9:16", refs=[ST, MATT],
        roles="Reference 1 is the students (only two BACKS: students 2 and 3 from behind). Reference 2 is MATT (the small cameo). ",
        prompt=(f"{LAB} "
                f"{framing('OTS', 'eye level', '50 mm, shallow focus', 'two of his students in the foreground step toward the empty place behind the bench, as if to volunteer', 'urgent, loyal')} "
                f"{camera('at the south end of the long bench, behind two students', 'north-north-west', 'the long dark oak bench across the frame with a small glass on it, behind it the tall glass-fronted cabinets of stoppered jars along the north wall; the window light comes in from the left edge', 'the window itself and his desk are NOT in view')} "
                "CLOSE over-the-shoulder framing: two students in the foreground, seen from BEHIND only, so close to the "
                "camera that their backs, shoulders and the backs of their heads are LARGE and soft, filling the lower left "
                "and lower right corners up to about 0.35 of the frame height; just beyond them, the bench top at about "
                "two thirds of the frame height, a small empty glass on it right of centre, and the empty space behind "
                "the bench in the centre of the frame, where the professor will stand. "
                + NOT_HERE.format(who="Max von Pettenkofer") + " "
                + matt_beat("an 1890s student's dark suit", "small, at the far right edge by the cabinets at the back, away from the "
                           "empty place in the centre, writing in his amber notebook")
                + f" {cast('the two students seen from behind', 'MATT, small, at the back')} {ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "pose-pettenkofer-s4": dict(aspect="16:9", refs=[P], roles=P_ROLE,
        prompt=pose_sheet(PETTENKOFER,
                          ["standing square to the viewer behind a bench (the bench is NOT drawn: the drawing ends in a "
                           "straight line at his waist), both hands resting flat at waist height, his eyes on someone in "
                           "front of him, calm. " + EMPTY_HANDS,
                           "EXACTLY the same stance, face and left hand as drawing (1); ONLY his RIGHT hand comes up to "
                           "chest height, the palm open toward the viewer, calm and firm: a quiet 'no'. " + EMPTY_HANDS],
                          "s4: over two students' shoulders in his laboratory", S4_LIGHT,
                          "from the front, eye level, 50 mm", "from the waist up")),
    # shot 6 (the gulp): profile against the window; NO Pettenkofer
    "plate-s6": dict(aspect="9:16", refs=[ST], roles="Reference 1 is the students (two of them, as soft dark blurs only). ",
        prompt=(f"{LAB} "
                f"{framing('MCU', 'eye level, profile view', '85 mm, very shallow focus', 'the place by the tall window where the old professor will stand in profile and drink', 'still, quiet, held breath')} "
                f"{camera('beside the tall window, close', 'west into the window', 'the tall leaded window filling the background, small rectangular panes of pale grey sky between dark lead lines, a thin curtain edge at the right; two students as soft dark blurs at the far right edge', 'the bench, the shelves and the lamps are NOT in view')} "
                "The left half and the lower part of the frame are open window light, an empty place by the window. "
                + NOT_HERE.format(who="Max von Pettenkofer")
                + f" {cast('the two students, out of focus, at the far right edge')} {ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "pose-pettenkofer-s6": dict(aspect="16:9", refs=[P], roles=P_ROLE,
        prompt=pose_sheet(PETTENKOFER,
                          ["in profile facing RIGHT, his RIGHT hand holding a small glass to his lips, the glass level, his "
                           "eyes open and calm on it",
                           "EXACTLY the same, ONE change: his head tipped back and the glass tipped up, drinking it down, "
                           "his eyes half closed"],
                          "s6: in profile against a tall bright window", S6_LIGHT, "from the side, eye level, 85 mm",
                          "the head and shoulders, the hand and glass at his mouth")
               + " " + scale({"the small glass": "about 2 3/4 in (7 cm) tall, half hidden by his fingers",
                              "the liquid": "clear, a little in the bottom, nothing in it"})),
    # shot 7 (the cramps): the desk top from above; NO hand, NO loose sheet (the sheet under his hand is in the pose sheet)
    "plate-s7": dict(aspect="9:16", refs=[], roles="",
        prompt=(f"{DESK} "
                f"{framing('CU', 'high angle, looking straight down onto the desk top', '50 mm', 'a desk top in the grey light, after the drinking: the small glass stands empty', 'cold, still, foreboding')} "
                f"{camera('above the desk, looking straight down', 'down onto the desk top', 'the dark oak desk top only, filling the frame: a stack of folio papers with handwriting at the top, a glass inkwell at the upper left, the small empty glass at the right; the near edge of the desk and dark floor in a thin band at the bottom', 'no wall, no window and no floor except the thin band at the bottom')} "
                "The lower left of the desk top is bare, empty wood (a hand and a loose sheet are added there later). "
                "EMPTY LOCATION PLATE: no people, no hands, no arms. "
                f"{WAVY_WRITING} "
                f"{sizes({'the frame': 'about 12 in (30 cm) of desk across', 'the small glass': 'about 2 in (5 cm) across from above', 'the inkwell': 'about 2 1/2 in (6 cm) across', 'the papers': 'folio sheets about 8 x 13 in (21 x 34 cm)', 'the desk edge': 'about 1 1/2 in (4 cm) thick'})} "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # no sheet reference (L45b: a standing model sheet prints as ghosts under a lying / flat pose); the hand in words
    "pose-hand-s7": dict(aspect="16:9", refs=[], roles="",
        prompt=pose_sheet("the old professor's RIGHT hand and forearm (dark frock-coat sleeve, white shirt cuff), seen "
                          "straight from above, the forearm coming in from the LOWER RIGHT corner of each drawing, with a loose "
                          "sheet of paper with faint grey wavy lines (no letters) under the hand",
                          ["the hand lying flat and still on the flat sheet of paper",
                           "the forearm, sleeve, cuff and wrist EXACTLY where they are in drawing (1), not moved or "
                           "turned; ONE change: the fingers curl and clutch the paper, the knuckles white, tendons standing "
                           "up on the back of the hand (in pain, not anger: NOT a punching fist). The sheet is still at its "
                           "full size, still mostly spread flat on the desk exactly where it was; only its part under the "
                           "fingers is dragged into the palm in deep creases radiating from the fingers (never a ball)"],
                          "s7: a desk top seen from above in cold light", S7_LIGHT, "from straight above, 50 mm",
                          "only the hand, wrist and forearm with the paper under it; no face, no body")
               + f" {WAVY_WRITING} "
               + scale({"the loose sheet": "about 8 in (21 cm) wide when flat; crumpled, a ball of about 4 in (10 cm) in his hand",
                        "the hand": "old and thin-skinned, about 7 1/2 in (19 cm) from wrist to fingertip"})),
})

# v2 prompts (2026-11-20, after the first real pieces): pose-hand-s7 (L57 Lorem ipsum, L58 the sheet became a ball,
# the wrist moved), plate-s4 (came back wide, Matt in the empty place, L59), plate-s1 (hair top at 0.17, under the card).
# Re-rolls only after the user's OK ($0.067 each); the v1 images are what the real-art preview uses.
REROLL_V2 = ["pose-hand-s7", "plate-s4", "plate-s1"]

HERO_PIECES = ["plate-s1", "sprite-hand-glass-s1", "sprite-student-hand-s1", "plate-s4", "pose-pettenkofer-s4",
               "plate-s6", "pose-pettenkofer-s6", "plate-s7", "pose-hand-s7"]

# the 9 story stills (2, 3a, 3b, 5a, 5b, 9, 10, 11, 12) are added after the HERO pieces are approved on real art
KEYFRAMES = {}


def main():
    from lib.checkpoint import init_project
    p = REPO / "projects" / PID / "episode.json"
    if not (REPO / "projects" / PID / "project.json").exists():
        init_project(PID, title="He Drank Cholera to Prove His Rival Wrong", pipeline_type="animated-explainer")
    sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
    import episode
    episode.step_init(PID)
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="He Drank Cholera to Prove His Rival Wrong", format="short", dual_format=False,
              image_resolution="2K", loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s4: Matt's own glasses get the ? glint after 'no' (Matt cameo, L29)",
              theme={"culture": "munich-1890s", "font": "montserrat"}, motion_lint="fail",
              storyboard="2026-11-20: storyboard-v1.md + backgrounds-v1.md APPROVED with 4 fixes",
              previz_approved=("2026-11-20: user approved the HERO motion pre-viz of shots 1, 4, 6; shot 7 changed to the "
                               "fingers clutching and crumpling a loose sheet (not a fist, not the edge grip)"))
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
