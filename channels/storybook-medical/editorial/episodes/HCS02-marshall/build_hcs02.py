"""HCS02 Marshall: writes projects/hcs02-marshall/episode.json (title, narration, references, keyframes) from
storyboard-v2.md, with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS02-marshall/build_hcs02.py
Then:  episode.py refs hcs02-marshall   ->   episode.py keyframes hcs02-marshall
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, cast, framing, glasses_gag, lint_all,  # noqa: E402
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

# ── people (living people: illustrated stand-ins, no likeness from photos; storyboard "Sets and cast") ──────────
MARSHALL = ("BARRY MARSHALL (32, lean, short dark-brown hair, clean-shaven, friendly open face, a cheeky confident "
            "grin; an open-collar pale-blue shirt under a white lab coat, a small plain hospital ID badge with no writing)")
WARREN = ("ROBIN WARREN, the pathologist (late 40s, greying hair, a short grey beard, calm thoughtful face, half-moon "
          "glasses on a cord, a white lab coat over a brown knitted tie)")
ADRIENNE = ("ADRIENNE MARSHALL, his wife (early 30s, shoulder-length wavy light-brown hair, a soft green cardigan over "
            "a cream blouse, a wry knowing look)")

# ── sets: v2 gives most lines their own place (user review: "the lab background is in every shot") ───────────────
LAB = set_block("A hospital research lab, Fremantle, Perth, Western Australia", "1984",
                "cream-painted brick walls, white laminate benches, glass culture dishes, a Bunsen burner, a beige "
                "microscope, a tall louvre window with bright Australian sunlight striping the bench, a gum tree "
                "outside; warm sunny light")
LAB_NIGHT = set_block("The same Fremantle research lab, late at night", "1984",
                      "the bench and culture dishes lit only by one desk lamp, a black louvre window, long shadows; "
                      "secretive and quiet")
HOSPITAL = set_block("The front of a hospital in Perth, Western Australia", "1984",
                     "a low cream-brick 1970s hospital building, a covered entrance, tall palm trees, a deep blue sky, "
                     "hard bright sunshine and short shadows")
PATHOLOGY = set_block("Robin Warren's pathology room at night, Royal Perth Hospital", "1984",
                      "a small dark room, grey-green walls, racks of glass slides, one hooded microscope lamp making a "
                      "single warm pool of light; everything else in deep shadow")
LECTURE = set_block("A tiered medical lecture theatre in Perth", "1984",
                    "steep curved rows of dark wooden benches, a slide projector beam cutting through dusty air, a "
                    "pull-down screen, a wooden lectern at the bottom, a high side window; dim, the only dark room in "
                    "the film")
OFFICE = set_block("A 1980s city office, Perth", "1984",
                   "a cluttered desk with a beige push-button telephone, a full glass ashtray, stacks of folders, "
                   "venetian blinds with harsh striped light")
CORRIDOR = set_block("A Fremantle Hospital staff corridor", "1984",
                     "green linoleum floor, pale-yellow walls, a row of plastic chairs, a water fountain, harsh flat "
                     "fluorescent light")
KITCHEN = set_block("The Marshalls' home kitchen, Perth", "1984",
                    "1980s orange-and-brown tiles, a laminate table, a fridge, warm evening lamp light")
STOCKHOLM = set_block("A grand concert hall stage, Stockholm, Sweden", "2005",
                      "deep blue velvet curtains, a wide stage, warm golden spotlights, rows of flowers along the edge "
                      "of the stage")
CLINIC = set_block("A family doctor's consulting room", "2005",
                   "a modern desk, a computer monitor, a blood-pressure cuff on the wall, a window with soft daylight, "
                   "calm blue and white")

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
STYLE = "Reference 1 is for the painting style only (never its room). "
KEYFRAMES = {
    # v1 kept (s1, s2a, s3, s5a, s9a): SHOT lines added afterwards, images unchanged
    "s1": dict(aspect="9:16", refs=["ref:plate-lab", M],
        roles="Reference 1 is the lab (style, colours and sunlight). Reference 2 is BARRY MARSHALL (same face, hair, "
              "shirt and coat). ",
        prompt=f"{LAB} {framing('MS', 'low angle looking up', '35 mm', 'he raises a beaker of cloudy broth like a toast', 'cheeky, daring')} "
               f"{cast(MARSHALL + ', raising a tall glass laboratory beaker of cloudy amber-brown broth in his right hand like a toast, a cheeky grin, looking at the beaker')} "
               "The beaker is in the upper-middle of the frame, catching the sunlight; his face just below and beside "
               f"it. The top 15% is calm cream wall. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", refs=["ref:plate-lab", M, "kit:glasses-sheet.jpg"],
        roles=STYLE + "Reference 2 is BARRY MARSHALL. Reference 3 shows Matt's amber spectacles. ",
        prompt=f"{HOSPITAL} {framing('LS', 'eye level', '28 mm', 'a young doctor arrives at work')} "
               f"{cast(MARSHALL + ', small in the middle distance, walking toward the entrance carrying a brown briefcase')} "
               "Palm trees in the foreground on the left and right edges, the building behind. The top 20% is deep "
               f"blue sky. {glasses_gag('folded on the reception counter, visible through the glass entrance doors')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1 was the same sunny lab again; now a dark pathology room, his face lit by the lamp
    "s2b": dict(aspect="9:16", refs=["ref:plate-lab", "ref:sheet-warren"],
        roles=STYLE + "Reference 2 is ROBIN WARREN (same face, beard, glasses, coat). ",
        prompt=f"{PATHOLOGY} {framing('MCU', 'side angle, slightly low', '50 mm, shallow focus', 'he discovers something strange under the microscope', 'quiet astonishment, eyebrows up')} "
               f"{cast(WARREN + ', in profile in the lower half of the frame, leaning back from the microscope eyepiece, his face lit warm by the lamp')} "
               "Above him, filling the upper 45% of the frame, a round storybook 'microscope view' circle glowing like "
               "a lantern in the dark: pink stomach lining with about eight separate teal S-shaped spiral bacteria "
               f"with thin tails, well spaced. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles=STYLE,
        prompt=f"{OFFICE} {framing('MS', 'eye level', '35 mm', 'a stressed businessman clutches his aching stomach', 'pain and stress')} "
               f"{cast('a frazzled businessman (50s, loosened tie, rolled sleeves, sweaty brow) at the desk, clutching his stomach with both hands, grimacing')} "
               "A jagged red zigzag line is drawn over his tummy like a cartoon ache. The phone on the desk is "
               f"ringing, slightly lifted off its cradle. The top 20% is the striped blinds. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1 put him BEHIND the audience and the kookaburra was huge. Reverse angle from the back rows.
    "s4": dict(aspect="9:16", refs=["ref:plate-lab", M],
        roles=STYLE + "Reference 2 is BARRY MARSHALL. ",
        prompt=f"{LECTURE} {framing('LS', 'high angle from the back of the top row, looking down the tiers', '28 mm', 'he argues his idea to a room that does not believe him', 'he is eager; the audience is cold and doubtful')} "
               f"{cast(MARSHALL + ', far below at the lectern in the lower-middle of the frame, FACING the audience and the camera, one arm pointing up at a projected drawing of a teal spiral bacterium on the screen behind him', extra='In the foreground, seen FROM BEHIND, the backs of the heads and grey-suited shoulders of about eight older doctors in the top rows, arms folded; one leans his head on his hand, bored. Nobody faces the camera except Marshall.')} "
               "On the high side window ledge at the right, a SMALL kookaburra at true bird size (smaller than a "
               f"person's head), beak open as if laughing. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5a": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles="Reference 1 is the lab (style and colours). ",
        prompt="SET: a clean animal-research pen beside the hospital lab, Perth, 1984, cream walls, fresh straw, "
               f"bright window light. {framing('MS', 'low angle at pig height', '35 mm', 'the pig eats happily, perfectly healthy', 'cheerful')} "
               "One healthy, happy pink piglet with a curly tail eating from a steel bowl, ears up, totally fine. The "
               f"piglet fills the middle of the frame, its curly tail clear against the cream wall. {NO_PEOPLE} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1 was a smiling medium shot in the sunny lab; now a close-up at night, the decision
    "s5b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-lab", M],
        roles=STYLE + "Reference 2 is BARRY MARSHALL (same face). ",
        prompt=f"{LAB_NIGHT} {framing('CU', 'slightly low angle', '85 mm, very shallow focus', 'he lifts the beaker of broth toward his lips, about to drink', 'serious and determined, a flicker of nerves, no smile')} "
               f"{cast(MARSHALL + ', his face filling the upper half of the frame, lit from below by the desk lamp, the beaker of cloudy amber-brown broth raised close to his chin in the lower half, his eyes looking straight at the viewer')} "
               f"The background is dark and out of focus. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1 was the lab again; now a corridor, him sick on a chair, colleagues giving him a wide berth
    "s6": dict(aspect="9:16", refs=["ref:plate-lab", M],
        roles=STYLE + "Reference 2 is BARRY MARSHALL (same face and coat). ",
        prompt=f"{CORRIDOR} {framing('MLS', 'eye level, the corridor running away from the camera', '35 mm', 'he is sick and his breath drives people away', 'he is miserable and queasy; the colleagues are comically disgusted')} "
               f"{cast(MARSHALL + ', slumped on a plastic chair in the left foreground, pale with a sickly green tint, sweaty, one hand on his stomach, an empty steel kidney dish on his knees', 'a nurse in a white uniform', 'a young doctor in a white coat', extra='The nurse and the young doctor hurry past on the far right side of the corridor, leaning away from him, both pinching their noses; a faint green haze drifts from him toward them.')} "
               f"Nothing inside the dish. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1 showed the lab and microscope again; now the view itself fills the frame
    "s7": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles="Reference 1 is for the painting style and palette only. ",
        prompt="SET: the view down a microscope, storybook painting, 1984. "
               f"{framing('ECU', 'straight down the eyepiece', 'microscope view', 'the biopsy proves the bacteria have inflamed his stomach', 'alarming but not gory')} "
               "A large round field of view fills almost the whole frame, black around the circle: swollen, sore "
               "deep-red stomach lining in soft folds, crowded with teal S-shaped spiral bacteria with thin tails. "
               f"Storybook style, not a photograph, nothing gory. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1 had him smiling; he is sick, she is the one in charge
    "s8": dict(aspect="9:16", refs=["ref:plate-lab", M, "ref:sheet-adrienne"],
        roles=STYLE + "Reference 2 is BARRY MARSHALL. Reference 3 is ADRIENNE MARSHALL. ",
        prompt=f"{KITCHEN} {framing('MS', 'low angle across the kitchen table', '35 mm', 'his wife tells him it is time to take the pills', 'he is pale, sweaty and sorry for himself; she is firm and wry, one eyebrow up')} "
               f"{cast(MARSHALL + ', slumped at the kitchen table in the lower foreground, pale and clammy, a slight green tint, head propped on one hand, the other hand on his stomach, an untouched plate of dinner in front of him', ADRIENNE + ', standing behind him in the doorway in the upper right, arms folded, holding up a small brown pill bottle')} "
               f"The pill bottle is clear against the wall behind it. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9a": dict(aspect="9:16", refs=["ref:plate-lab", M, "ref:sheet-warren"],
        roles=STYLE + "Reference 2 is BARRY MARSHALL, 21 years older (greying hair, dark suit). Reference 3 is ROBIN "
              "WARREN, 21 years older (white hair and beard, dark suit). ",
        prompt=f"{STOCKHOLM} {framing('LS', 'from the back of the hall', '35 mm', 'the two of them bow as Nobel laureates', 'triumph')} "
               f"{cast('BARRY MARSHALL at 54 (greying hair, dark suit and white bow tie)', 'ROBIN WARREN at 68 (white hair and beard, dark suit and white bow tie)', extra='They stand side by side in the middle of the stage, taking a bow, small in frame; the audience is only soft dark shapes of heads in the foreground.')} "
               f"No medal design, no logo, no banner. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review: "not smart"): v1 was a plain stomach diagram; now the payoff in a real life, a patient cured
    "s9b": dict(aspect="9:16", refs=["ref:plate-lab"],
        roles=STYLE,
        prompt=f"{CLINIC} {framing('MCU', 'eye level, over the shoulder of the doctor', '50 mm', 'a patient with an ulcer is handed a simple course of pills and knows he will be fine', 'relief, a grateful smile')} "
               f"{cast('a middle-aged man in a plain blue sweater (the patient), facing the camera, one hand resting on his stomach, smiling with relief', 'a woman doctor in a white coat, seen from behind over her shoulder on the left, handing him a small plain white pill box')} "
               f"The pill box and his smile are in the centre. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
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
