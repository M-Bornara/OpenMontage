"""HCS05 al-Razi: writes projects/hcs05-al-razi/episode.json (title, narration, references, keyframes) from
storyboard-v1.md v1.1 (approved with its pre-viz 2026-11-14), with the prompt_kit blocks, then lints every prompt.
Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS05-al-razi/build_hcs05.py
Then (after the user approves the prompts on the storyboard page):
    episode.py refs hcs05-al-razi --batch   ->   episode.py keyframes hcs05-al-razi --batch
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (FULL_BLEED, NO_PEOPLE, NO_TEXT, ONE_EACH, PERIOD, SAFE_FRAMING, camera, cast, framing,  # noqa: E402
                        glasses_gag, lint_all, matt_beat, real_writing, set_block)

PID = "hcs05-al-razi"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

NARRATION = """[curious] Eleven hundred years ago, a doctor refused to treat some of his patients. On purpose.
Al-Razi was a Persian physician from Rey, near today's Tehran.
For the first signs of meningitis, the treatment was bloodletting.
Al-Razi wasn't sure it worked.
So he bled one group of patients… and deliberately left another group alone.
Then he watched what happened to both.
The bled group did better, he wrote, in his giant medical encyclopedia. So he kept the treatment.
[mischievously] He was wrong. Bloodletting doesn't help meningitis.
[curious] Some call it the first clinical trial. Not quite. But comparing two groups is how we test every medicine today."""

# ── people: the look Iranians know (1956 portrait, Wellcome S0001954, CC BY 4.0: credit in CREDITS) ─────────────────
RAZI = ("AL-RAZI (about 50; a white turban wrapped high and full, a full thick black beard, thick dark eyebrows, calm "
        "thoughtful eyes often looking down, olive skin; a long sand-coloured outer robe with a gold-embroidered collar "
        "band, over a blue tunic)")
ASSISTANT = "a young hospital assistant (20s, short dark beard, a plain brown robe and a small brown cap)"
PATIENT = ("a feverish young man (about 20) lying on a low bed under a woven wool blanket, a damp white cloth on his "
           "forehead, one hand at the back of his stiff neck, eyes half closed")
MOTHER = "his mother (40s, a dark headscarf, worried, sitting on the floor cushion beside the bed)"

# ── sets (period references: references.md) ─────────────────────────────────────────────────────────────────────
NOT_LATER = ("No blue or turquoise tiles, no glass windows, no chairs, no desks, no printed or bound modern books, no "
             "metal lanterns: this is about 900 AD.")
WARD = set_block("The hospital ward (bimaristan) in Rey", "about 900 AD",
                 "a long hall of warm baked brick laid in woven geometric patterns, round brick arches, carved plaster "
                 "panels, wooden lattice windows, small clay oil lamps in wall niches, low wooden beds with woven wool "
                 "blankets in two rows, a long plain cloth curtain hung down the middle of the hall")
REY = set_block("The city of Rey, near today's Tehran", "about 900 AD, at dusk",
                "a walled city of mud brick and baked brick, flat roofs and a few plain brick domes, a citadel on a "
                "rocky hill, poplar trees, and far behind, the white snow cone of Mount Damavand in the Alborz mountains")
ROOM = set_block("Al-Razi's room at night", "about 900 AD",
                 "a carpet and cushions on the floor, a clay oil lamp, a brass inkwell and reed pens, piles of loose "
                 "paper notebooks tied with cord; plain plastered walls")
MUSEUM = set_block("A museum gallery today", "present day",
                   "dim gallery, white walls, one glass display case lit from above")
LAB = set_block("A modern laboratory today", "present day", "a clean white lab bench, soft daylight")
SCRIPT = ("Any writing is rows of small brown-black ink strokes in an angular Arabic-style hand of the 900s, too small "
          "and soft to read; no words, no numbers, no headings.")

STYLE_PLATE = f"{HC1}/plate-study.png"
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"

REFERENCES = {
    "sheet-razi": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/razi_1956.jpg"],
        roles="Reference 1 shows our character model-sheet layout and painting style only (not this person). Reference 2 "
              "is the well-known Iranian portrait of al-Razi: paint THIS face, turban, beard and clothes in our storybook "
              "style (ignore the writing on it; do not put the portrait itself on the sheet). ",
        prompt=f"Clean character model sheet on plain bone-white paper: {RAZI}. Front view, three-quarter view, profile "
               "view, back view, a seated cross-legged view, plus three head close-ups (doubtful, frowning; calm, a "
               "knowing half-smile; watchful). Same scale in every view. No text, labels or watermark."),
    "plate-ward": dict(aspect="9:16", refs=[STYLE_PLATE, "proj:refs/samanid_mausoleum.jpg"],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. "
              "Reference 2 is a 10th-century building used ONLY for the brick patterns and arches. ",
        prompt=f"{WARD} Vertical frame down the middle of the hall, the two rows of beds and the curtain receding. "
               f"EMPTY location plate: no people. {NOT_LATER} {PERIOD} {NO_TEXT}"),
}

Z = "ref:sheet-razi"
WARD_LOOK = ("Reference 1 is the ward plate, for the painting style, brick, light and beds ONLY: do NOT copy its "
             "composition or camera angle. ")
RAZI_ROLE = "Reference 2 is AL-RAZI (same face, turban, beard and robe). "
# the ward is seen five times (pre-viz map-ward.png): beds of group A on the west side, group B on the east side, the
# curtain down the middle, the entrance and al-Razi's place at the south end
WARD_MAP = ("GEOGRAPHY: two rows of four beds run north-south; group A on the west side, group B on the east side, a cloth "
            "curtain hangs down the middle between them; the entrance is at the south end.")

KEYFRAMES = {
    "s1a": dict(aspect="9:16", refs=["ref:plate-ward", Z], roles=WARD_LOOK + RAZI_ROLE,
        prompt=f"{WARD} {WARD_MAP} {framing('MS', 'eye level', '35 mm', 'al-Razi stops his assistant from treating a patient, on purpose', 'calm authority, the assistant puzzled')} "
               f"{camera('in the aisle by the curtain, mid-ward', 'south, toward the entrance', 'the arched entrance at the south end with pale daylight in the doorway, the curtain on the left')} "
               f"{cast(RAZI + ', standing between two beds, his open palm raised to stop', ASSISTANT + ', carrying a small brass bowl toward a bed, stopped mid-step')} "
               f"Patients lie under blankets in the beds, faces turned away. {NOT_LATER} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s1b": dict(aspect="9:16", resolution="4K", refs=["kf:s1a", Z],
        roles="Reference 1 is an earlier shot of this film, for the painting style and lamplight ONLY. " + RAZI_ROLE,
        prompt=f"{WARD} {framing('CU', 'eye level', '85 mm, shallow focus', 'he did it on purpose', 'calm, one eyebrow slightly raised, a knowing half-smile')} "
               f"{camera('close in front of him', 'al-Razi', 'soft warm brick and a lamp niche, out of focus')} "
               f"{cast(RAZI + ', head and shoulders, the face in the upper half of the frame')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2": dict(aspect="9:16", resolution="4K", refs=["ref:plate-ward", "proj:refs/samanid_mausoleum.jpg"],
        roles=WARD_LOOK + "Reference 2 is a 10th-century building used ONLY for its brick patterns and dome. ",
        prompt=f"{REY} {framing('ELS', 'high angle from a hillside', '24 mm', 'his city, eleven hundred years ago', 'warm, ancient, peaceful')} "
               f"{camera('on a hillside south of the city', 'north, over the city', 'the city roofs and domes, the citadel hill, and Damavand far away on the right')} "
               f"{NOT_LATER} {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3": dict(aspect="9:16", refs=["ref:plate-ward"], roles=WARD_LOOK,
        prompt=f"{WARD} {WARD_MAP} {framing('MS', 'eye level, beside the bed', '35 mm', 'the first signs of meningitis, and the usual treatment waiting', 'worry, fever')} "
               f"{camera('in the aisle beside bed A3', 'west, at the bed', 'the brick wall with a lattice window and a lamp niche')} "
               f"{cast(PATIENT, MOTHER)} On a low wooden side table: a small brass bowl and a slim lancet laid on a "
               f"folded white cloth. No cut, no blood. {NOT_LATER} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4": dict(aspect="9:16", refs=["ref:plate-ward", Z], roles=WARD_LOOK + RAZI_ROLE,
        prompt=f"{ROOM} {framing('MCU', 'eye level, low', '50 mm', 'al-Razi doubts the treatment', 'frowning, the pen paused')} "
               f"{camera('on the carpet in front of him', 'al-Razi', 'a plain plastered wall with the lamp glow, piles of notebooks')} "
               f"{cast(RAZI + ', sitting cross-legged on a cushion on the carpet, a sheet of paper resting on his raised knee, a reed pen paused above it')} "
               f"A brass inkwell on the carpet beside him. {SCRIPT} {NOT_LATER} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5": dict(aspect="9:16", refs=["ref:plate-ward"], roles=WARD_LOOK,
        prompt=f"{WARD} {WARD_MAP} {framing('ELS', 'top-down, straight down from high above', '24 mm', 'two groups: one bled, one left alone', 'a clear, deliberate pattern')} "
               f"{camera('high above the curtain', 'straight down', 'the two rows of beds and the curtain between them')} "
               "The curtain runs down the centre of the frame. LEFT row (group A): four patients in bed, each with a "
               "small brass bowl on the floor beside the bed and a white bandage on one forearm. RIGHT row (group B): "
               "four patients in the same beds with nothing beside them. Patients lie still under blankets, faces "
               f"turned away. No blood. {NOT_LATER} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6": dict(aspect="9:16", refs=["ref:plate-ward", Z, "kit:matt-sheet.jpg"],
        roles=WARD_LOOK + RAZI_ROLE + "Reference 3 is MATT: copy his face, amber round spectacles, teal scarf and amber "
              "notebook only; his clothes are described below. ",
        prompt=f"{WARD} {WARD_MAP} {framing('MS', 'low angle', '35 mm', 'he watches what happens to both groups', 'patient, watchful, night')} "
               f"{camera('low at the south end of the ward', 'north, up the aisle', 'the two rows of beds running away, the curtain in the middle, lamps in the niches')} "
               f"{cast(RAZI + ', sitting on a floor cushion at the end of the aisle, a paper notebook on his knee, looking down both rows')} "
               f"{matt_beat('a plain 10th-century Persian student robe and a small cap', 'standing just behind al-Razi holding up a small clay oil lamp, wide-eyed')} "
               f"{SCRIPT} {NOT_LATER} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7a": dict(aspect="9:16", refs=["ref:plate-ward", Z, "kit:glasses-sheet.jpg"],
        roles=WARD_LOOK + "Reference 2 is AL-RAZI (his hand and sleeve only). Reference 3 shows Matt's amber spectacles. ",
        prompt=f"{ROOM} {framing('INSERT', 'top-down over the carpet', '50 mm', 'he writes down his result in his notes', 'focus, conviction')} "
               f"{camera('above his knee', 'straight down', 'the carpet and the notebooks')} "
               "His hand (sand sleeve, blue cuff) writes with a reed pen on a paper notebook; around it, tall piles of "
               f"his paper notebooks tied with cord. {SCRIPT} {glasses_gag('folded on top of one pile of notebooks')} "
               f"{FULL_BLEED} {NOT_LATER} {SAFE_FRAMING} {PERIOD}"),
    "s7b": dict(aspect="9:16", refs=["ref:plate-ward"], roles=WARD_LOOK,
        prompt=f"{WARD} {WARD_MAP} {framing('CU', 'eye level', '50 mm', 'he keeps the treatment', 'calm, routine, a dawn light')} "
               f"{camera('beside a group B bed', 'east, at the bedside', 'the brick wall with a lattice window full of dawn light')} "
               "Only a hand in a brown sleeve setting a small brass bowl and a slim lancet down on a folded white cloth "
               f"beside a bed. No cut, no blood. {NOT_LATER} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8": dict(aspect="9:16", refs=["ref:plate-ward"], roles=WARD_LOOK,
        prompt=f"{set_block('A forgotten storeroom shelf', 'centuries later', 'dusty wooden shelf, cobwebs, dim grey light')} "
               f"{framing('CU', 'high angle', '50 mm', 'the treatment did not work', 'abandoned, faintly comic')} "
               f"{camera('above the shelf', 'down at the bowl', 'the dusty shelf and a plain wall')} "
               "The same small brass bowl turned upside down, dull and dusty, a rusty lancet beside it. "
               f"{NO_PEOPLE} {SAFE_FRAMING} {NO_TEXT}"),
    "s9a": dict(aspect="9:16", refs=["ref:plate-ward"], roles=WARD_LOOK,
        prompt=f"{MUSEUM} {framing('LS', 'eye level', '35 mm', 'some call it the first clinical trial', 'curiosity, a question mark')} "
               f"{camera('in the gallery behind the visitor', 'the display case', 'the dim white gallery wall')} "
               f"{cast('a museum visitor in a dark coat, seen from behind on the left, looking into the case')} "
               "In the glass case: an old open manuscript with brown pages. Below it, a small white museum card. "
               f"{real_writing('The first clinical trial?', 'on the museum card')} {SAFE_FRAMING}"),
    "s9b": dict(aspect="9:16", refs=["ref:plate-ward"], roles=WARD_LOOK,
        prompt=f"{LAB} {framing('MS', 'eye level', '35 mm', 'comparing two groups is how every medicine is tested today', 'clear, modern, hopeful')} "
               f"{camera('in front of the bench', 'the bench', 'a plain pale lab wall')} "
               "Two neat rows of small white medicine bottles on the bench, one row behind the other, echoing two rows "
               "of beds; each bottle has a plain white label with no lettering (the A and B are added in the edit). "
               f"{NO_PEOPLE} {SAFE_FRAMING}"),
}


# -- v2 references (user, 2026-11-14: "make sure duplications are not happening"): L38 + L39 --------------------------
# The ward plate goes only to ward shots (L39); his room, Rey, the shelf, the museum and the lab take the al-Razi sheet
# or the HC001 study plate as STYLE only. s1a now faces south (entrance) so it can't repeat s6 (north, up the aisle).
OUTSIDE = "Reference 1 is a people-free room from another film, for the painting style ONLY: never paint its room. "
SHEETS = {"Z": "AL-RAZI (same face, turban, beard and robe)",
          "MATT": "MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; his clothes are "
                  "described below",
          "GL": "Matt's amber spectacles (the hidden gag)"}
REFS = {"Z": Z, "MATT": "kit:matt-sheet.jpg", "GL": "kit:glasses-sheet.jpg"}
KF_LOOK = "Reference 1 is an earlier shot of this film, for the painting style and lamplight ONLY. "
V2 = {
    "s1a": ("ward", [("ref:plate-ward", WARD_LOOK)], ["Z"]),
    "s1b": ("ward", [("kf:s1a", KF_LOOK)], ["Z"]),
    "s2": ("rey", [(STYLE_PLATE, OUTSIDE)], []),
    "s3": ("ward", [("ref:plate-ward", WARD_LOOK)], []),
    "s4": ("room", [], ["Z"]),
    "s5": ("ward", [("ref:plate-ward", WARD_LOOK)], []),
    "s6": ("ward", [("ref:plate-ward", WARD_LOOK)], ["Z", "MATT"]),
    "s7a": ("room", [], ["Z", "GL"]),
    "s7b": ("ward", [("ref:plate-ward", WARD_LOOK)], []),
    "s8": ("shelf", [(STYLE_PLATE, OUTSIDE)], []),
    "s9a": ("museum", [(STYLE_PLATE, OUTSIDE)], []),
    "s9b": ("lab", [(STYLE_PLATE, OUTSIDE)], []),
}
for name, (set_id, firsts, sheets) in V2.items():
    k = KEYFRAMES[name]
    k.update(refs=[r for r, _ in firsts] + [REFS[x] for x in sheets], set=set_id,
             roles="".join(role for _, role in firsts)
             + "".join(f"Reference {len(firsts) + j + 1} is {SHEETS[x]}. " for j, x in enumerate(sheets)))
    if sheets:
        k["prompt"] += " " + ONE_EACH


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="The Doctor Who Refused to Treat Half His Patients", format="short", dual_format=False,
              image_resolution="2K", loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s7a: Matt's spectacles on a pile of al-Razi's notebooks",
              theme={"culture": "persia", "font": "lalezar"},
              previz_approved="2026-11-14: storyboard v1.1 + pre-viz approved by the user on the storyboard page "
                              "(claude.ai/artifact/Dy34MeUVzxbLtEMi4ujsJC): 'now i can say we go for next'")
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
