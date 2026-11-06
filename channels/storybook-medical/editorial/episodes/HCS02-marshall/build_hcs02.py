"""HCS02 Marshall: writes projects/hcs02-marshall/episode.json (title, narration, references, keyframes) from
storyboard-v1.md, with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS02-marshall/build_hcs02.py
Then:  episode.py refs hcs02-marshall   ->   episode.py keyframes hcs02-marshall
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (FULL_BLEED, NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, cast, glasses_gag, lint_all,  # noqa: E402
                        set_block)

PID = "hcs02-marshall"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

NARRATION = """[excited] In 1984, a doctor drank a broth of live bacteria… On purpose.
Barry Marshall, a young doctor in Perth, Australia, and pathologist Robin Warren had found spiral bacteria living in inflamed stomachs.
Back then, most doctors blamed ulcers on stress.
Marshall said… bacteria. Almost nobody believed him.
[curious] The bacteria wouldn't infect his lab pigs… So he tested the only subject left… himself.
Within days, he was vomiting… His breath was awful.
On day ten, a biopsy showed the bacteria… and an inflamed stomach.
[mischievously] His wife suggested it was time to treat himself.
Twenty-one years later, Marshall and Warren won the Nobel Prize… and most ulcers became curable."""

# ── people (living people: illustrated stand-ins, no likeness from photos; storyboard-v1 "Sets and cast") ──────
MARSHALL = ("BARRY MARSHALL (32, lean, short dark-brown hair, clean-shaven, friendly open face, a cheeky confident "
            "grin; an open-collar pale-blue shirt under a white lab coat, a small plain hospital ID badge with no writing)")
WARREN = ("ROBIN WARREN, the pathologist (late 40s, greying hair, a short grey beard, calm thoughtful face, half-moon "
          "glasses on a cord, a white lab coat over a brown knitted tie)")
ADRIENNE = ("ADRIENNE MARSHALL, his wife (early 30s, shoulder-length wavy light-brown hair, a soft green cardigan over "
            "a cream blouse, a wry knowing look)")

# ── sets ─────────────────────────────────────────────────────────────────────────────────────────────────────
LAB = set_block("A hospital research lab, Fremantle, Perth, Western Australia", "1984",
                "cream-painted brick walls, white laminate benches, glass culture dishes, a Bunsen burner, a beige "
                "microscope, a tall louvre window with bright Australian sunlight striping the bench, a gum tree "
                "outside; warm sunny light")
HOSPITAL = set_block("The front of a hospital in Perth, Western Australia", "1984",
                     "a low cream-brick 1970s hospital building, a covered entrance, tall palm trees, a deep blue sky, "
                     "hard bright sunshine and short shadows")
LECTURE = set_block("A hospital lecture room in Perth", "1984",
                    "tiered wooden seats, beige walls, a slide projector beam, a wooden lectern, a window with a gum "
                    "tree branch outside; flat afternoon light, a little stuffy")
OFFICE = set_block("A 1980s city office, Perth", "1984",
                   "a cluttered desk with a beige push-button telephone, a full glass ashtray, stacks of folders, "
                   "venetian blinds with harsh striped light")
KITCHEN = set_block("The Marshalls' home kitchen, Perth", "1984",
                    "1980s orange-and-brown tiles, a laminate table, a fridge, warm evening lamp light")
STOCKHOLM = set_block("A grand concert hall stage, Stockholm, Sweden", "2005",
                      "deep blue velvet curtains, a wide stage, warm golden spotlights, rows of flowers along the edge "
                      "of the stage")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "

REFERENCES = {
    "sheet-marshall": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {MARSHALL}, Australia, 1984. Front view, "
               "three-quarter view, profile view, back view, plus three head close-ups (cheeky grin, queasy and green, "
               "sheepish). Same scale in every view. No text, labels or watermark."),
    "sheet-warren": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {WARREN}, Australia, 1984. Front view, "
               "three-quarter view, profile view, plus three head close-ups (peering into a microscope, quietly "
               "pleased, thoughtful). Same scale in every view. No text, labels or watermark."),
    "sheet-adrienne": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {ADRIENNE}, Australia, 1984. Front view, "
               "three-quarter view, profile view, plus three head close-ups (one eyebrow raised, arms folded and "
               "unimpressed, a small smile). Same scale in every view. No text, labels or watermark."),
    "plate-lab": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{LAB} Vertical frame from the doorway: the bench in the middle distance with the microscope and "
               "culture dishes, the louvre window on the right. EMPTY location plate: no people. Three clear depth "
               f"layers. {PERIOD} {NO_TEXT}"),
}

M = "ref:sheet-marshall"
LABREF = "Reference 1 is the lab (style, colours and sunlight). "
KEYFRAMES = {
    "s1": dict(aspect="9:16", refs=["ref:plate-lab", M],
        roles=LABREF + "Reference 2 is BARRY MARSHALL (same face, hair, shirt and coat). ",
        prompt=f"{LAB} Medium close-up from a LOW angle, looking up at him: {cast(MARSHALL + ', raising a tall glass laboratory beaker of cloudy amber-brown broth in his right hand like a toast, a cheeky grin, looking at the beaker')} "
               "The beaker is in the upper-middle of the frame, catching the sunlight; his face just below and beside "
               f"it. The top 15% is calm cream wall. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", refs=["ref:plate-lab", M, "kit:glasses-sheet.jpg"],
        roles="Reference 1 is for the painting style only. Reference 2 is BARRY MARSHALL. Reference 3 shows Matt's "
              "amber spectacles. ",
        prompt=f"{HOSPITAL} Wide vertical frame. {cast(MARSHALL + ', small in the middle distance, walking toward the entrance carrying a brown briefcase')} "
               "Palm trees in the foreground on the left and right edges, the building behind. The top 20% is deep "
               f"blue sky. {glasses_gag('folded on the reception counter, visible through the glass entrance doors')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2b": dict(aspect="9:16", refs=["ref:plate-lab", "ref:sheet-warren"],
        roles=LABREF + "Reference 2 is ROBIN WARREN (same face, beard, glasses, coat). ",
        prompt=f"{LAB} {cast(WARREN + ', in the lower third of the frame, seated at the microscope, eye to the eyepiece')} "
               "Filling the upper half of the frame, a large round storybook 'microscope view' circle with a soft dark "
               "edge, floating above him like a thought: inside it, pink stomach lining with about eight separate "
               "S-shaped spiral bacteria, each a little curly rod with a few thin tails, painted in teal, well spaced "
               f"and not overlapping. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles="Reference 1 is for the painting style only (never its room). ",
        prompt=f"{OFFICE} Medium shot: {cast('a frazzled businessman (50s, loosened tie, rolled sleeves, sweaty brow) at the desk, clutching his stomach with both hands, grimacing')} "
               "A jagged red zigzag line is drawn over his tummy like a cartoon ache. The phone on the desk is "
               f"ringing, slightly lifted off its cradle. The top 20% is the striped blinds. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4": dict(aspect="9:16", refs=["ref:plate-lab", M],
        roles="Reference 1 is for the painting style only. Reference 2 is BARRY MARSHALL. ",
        prompt=f"{LECTURE} Wide vertical frame from the side of the room: {cast(MARSHALL + ' at the lectern in the upper left, pointing eagerly at a big projected drawing of a teal spiral bacterium on the wall', extra='Below him, three rows of older doctors in grey suits sit with arms crossed and doubtful faces; one yawns widely.')} "
               "On the windowsill on the right a kookaburra (brown and cream bird, big beak) sits with its beak wide "
               f"open, as if laughing. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5a": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles="Reference 1 is the lab (style and colours). ",
        prompt="SET: a clean animal-research pen beside the hospital lab, Perth, 1984, cream walls, fresh straw, "
               "bright window light. Medium shot: one healthy, happy pink piglet with a curly tail eating from a steel "
               "bowl, ears up, totally fine. The piglet fills the middle of the frame, its curly tail clear against "
               f"the cream wall. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-lab", M],
        roles=LABREF + "Reference 2 is BARRY MARSHALL (same face). ",
        prompt=f"{LAB} Close-up: {cast(MARSHALL + ', holding the beaker of cloudy amber-brown broth at chest height, looking straight at the viewer with his eyebrows raised, a reckless half-smile')} "
               f"His eyes are at about 35% of the frame height; the beaker in the lower middle. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6": dict(aspect="9:16", refs=["ref:plate-lab", M],
        roles=LABREF + "Reference 2 is BARRY MARSHALL (same hair and coat). ",
        prompt=f"{LAB} Comedy medium shot. {cast(MARSHALL + ', seen from behind and a little to the side, hunched over a steel lab sink, one hand on his stomach, his skin with a sickly pale green tint', 'a young female lab colleague in a white coat in the doorway on the right, leaning far away from him, fanning a hand in front of her nose, eyes squeezed shut')} "
               f"Nothing visible inside the sink. The top 20% is calm wall. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles="Reference 1 is the lab (style and colours). ",
        prompt=f"{LAB} Extreme close-up: a glass microscope slide on the microscope stage under a warm lamp; above it "
               "a large round 'microscope view' circle fills the upper half of the frame: inflamed deep-red stomach "
               "lining, swollen and sore-looking, crowded with the same teal S-shaped spiral bacteria. Storybook style, "
               f"not a photograph, nothing gory. The middle 30% of the frame height is plain. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8": dict(aspect="9:16", refs=["ref:plate-lab", M, "ref:sheet-adrienne"],
        roles="Reference 1 is for the painting style only. Reference 2 is BARRY MARSHALL. Reference 3 is ADRIENNE "
              "MARSHALL. ",
        prompt=f"{KITCHEN} Comedy two-shot. {cast(ADRIENNE + ', standing in the doorway in the upper right, arms folded, one eyebrow raised, holding up a small brown pill bottle in one hand', MARSHALL + ', seated at the kitchen table in the lower left, looking up at her sheepishly, no green tint')} "
               "The pill bottle is clear against the wall behind it. The top 15% is calm wall. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9a": dict(aspect="9:16", refs=["ref:plate-lab", M, "ref:sheet-warren"],
        roles="Reference 1 is for the painting style only. Reference 2 is BARRY MARSHALL, 21 years older (greying "
              "hair, dark suit). Reference 3 is ROBIN WARREN, 21 years older (white hair and beard, dark suit). ",
        prompt=f"{STOCKHOLM} Wide vertical frame from the back of the hall. {cast('BARRY MARSHALL at 54 (greying hair, dark suit and white bow tie)', 'ROBIN WARREN at 68 (white hair and beard, dark suit and white bow tie)', extra='They stand side by side in the middle of the stage, taking a bow, small in frame; the audience is only soft dark shapes of heads in the foreground.')} "
               f"No medal design, no logo, no banner. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9b": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles="Reference 1 is for the painting style and palette only. ",
        prompt="SET: a storybook anatomy drawing on warm cream paper, 1980s. A simple stomach shape drawn as a soft "
               "ink outline, centred and filling the middle 60% of the frame, its inside painted sore red with five "
               "small teal S-shaped spiral bacteria. Nothing else; plain cream paper around it. "
               f"{FULL_BLEED} {NO_PEOPLE} {SAFE_FRAMING} {NO_TEXT}"),
}

# The FX layers need their objects as clean cut-outs: s2b spirals, s5a tail, s8 pill bottle (masks.py after generation).


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="The Doctor Who Drank Bacteria", format="short", dual_format=False, image_resolution="2K",
              references=REFERENCES, keyframes=KEYFRAMES)
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
