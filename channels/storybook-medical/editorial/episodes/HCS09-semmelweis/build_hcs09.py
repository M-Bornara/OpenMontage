"""HCS09 Semmelweis: writes projects/hcs09-semmelweis/episode.json (title, narration, references, keyframes) from
storyboard-v1.md (script v2), with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS09-semmelweis/build_hcs09.py
Then:  episode.py refs hcs09-semmelweis --batch   ->   episode.py keyframes hcs09-semmelweis --batch
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (FULL_BLEED, NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, WAVY_WRITING, cast, framing, glasses_gag,  # noqa: E402
                        lint_all, matt_beat, set_block)

PID = "hcs09-semmelweis"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

# script v2 (storyboard-v1.md): trims for length; Kolletschka "was cut" (by a student's scalpel), not "cut his finger"
NARRATION = """[curious] In 1847, a doctor told other doctors to wash their hands. They hated him for it.
Vienna had two maternity wards. In the doctors' ward, about one mother in ten died of fever.
In the midwives' ward… far fewer. Women begged not to go to the doctors.
Ignaz Semmelweis's friend was cut at an autopsy… and died of the same fever.
The doctors went straight from the dead… to the mothers.
So Semmelweis made them wash in chlorine. Deaths fell to about one in a hundred.
[serious] But many doctors refused to believe their hands could kill. He lost his job.
In 1865, he died in an asylum… of an infected wound.
[curious] Today, rejecting new evidence has a name… the Semmelweis reflex."""

# ── people ────────────────────────────────────────────────────────────────────────────────────────────────────────
SEMMELWEIS = ("IGNAZ SEMMELWEIS, the doctor (29, Hungarian, a broad round face, dark brown hair already thinning at the "
              "temples, a thick dark moustache and short side whiskers, intense dark eyes; a black frock coat, a white "
              "shirt, a black cravat)")
PROFESSOR = ("the senior professor (60s, grey side whiskers, thin grey hair combed flat, a high stiff white collar and "
             "black cravat, a dark frock coat, cold heavy-lidded eyes)")
DOCTORS = "frock-coated Viennese doctors of the 1840s with side whiskers"

# ── sets ──────────────────────────────────────────────────────────────────────────────────────────────────────────
HOSPITAL = "the Vienna General Hospital maternity clinics, 1847"
CORRIDOR = set_block("A long vaulted corridor in the Vienna General Hospital", "1847",
                     "whitewashed walls, a stone floor, tall arched windows; at its far end the corridor splits into "
                     "two tall wooden double doors side by side")
WARD1 = set_block("The First Clinic, the doctors' maternity ward", "1847",
                  "a long whitewashed ward, two rows of iron beds with white linen, tall windows; cold, sickly pale "
                  "green light")
WARD2 = set_block("The Second Clinic, the midwives' maternity ward", "1847",
                  "a long whitewashed ward, iron beds with white linen and wool blankets; warm candle-gold light, calm")
AUTOPSY = set_block("The hospital's autopsy room", "1847",
                    "a grey stone slab table, a white sheet, steel instruments on a tray, cold grey light")
WASHROOM = set_block("A row of wash basins at the entrance of the First Clinic", "1847",
                     "white porcelain basins on a long wooden stand against a whitewashed wall, jugs, a window with "
                     "clean morning light")
LECTURE = set_block("A medical society lecture room in Vienna", "1848",
                    "tiered wooden benches, dark panelling, tall windows, a lectern at the front, grey daylight")
GATE = set_block("The gate of the Vienna General Hospital", "winter 1849",
                 "a tall stone archway with iron gates, a cobbled street, snow falling, grey dusk")
ASYLUM = set_block("A corridor in an asylum near Vienna", "1865",
                   "a long bare corridor, peeling pale walls, one small barred window, cold blue light, an open door at "
                   "the far end")
PORTRAIT = set_block("A plain room with a window, Vienna", "1847",
                     "a plain warm plaster wall, soft window light from one side")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "

REFERENCES = {
    "sheet-semmelweis": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {SEMMELWEIS}, Vienna, 1847. Front view, "
               "three-quarter view, profile view, back view, plus three head close-ups (urgent and insisting, "
               "grieving, tired and steady). Same scale in every view. No text, labels or watermark."),
    "plate-clinic": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{CORRIDOR} Vertical frame, one-point perspective down the corridor to the two doors. EMPTY location "
               f"plate: no people. Three clear depth layers. {PERIOD} {NO_TEXT}"),
}

SM = "ref:sheet-semmelweis"
STYLE = "Reference 1 is the hospital plate, for the painting style and palette only. "
KEYFRAMES = {
    "s1a": dict(aspect="9:16", refs=["ref:plate-clinic", SM],
        roles=STYLE + "Reference 2 is IGNAZ SEMMELWEIS (same face, hair and clothes). ",
        prompt=f"{WASHROOM} {framing('MS', 'eye level', '35 mm', 'a young doctor tells his colleagues to wash their hands', 'urgent conviction against cold disbelief')} "
               f"{cast(SEMMELWEIS + ', in the centre with his sleeves rolled up, holding his wet hands out over a basin toward the others', 'CROWD: exactly three ' + DOCTORS + ' on the right, frowning, arms folded')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s1b": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"SET: {HOSPITAL}, a corridor. {framing('CU', 'low angle', '85 mm, shallow focus', 'the establishment despises the idea', 'cold scorn')} "
               f"{cast(PROFESSOR + ', head and shoulders, arms folded, looking down his nose at the camera')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE + "Keep the plate's corridor and two doors. ",
        prompt=f"{CORRIDOR} {framing('ELS', 'eye level, perfectly symmetrical', '24 mm', 'two wards side by side with two different fates', 'foreboding')} "
               "The left door glows with cold pale green light from inside; the right door glows with warm candle-gold "
               f"light. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2b": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"{WARD1} {framing('LS', 'high angle', '35 mm', 'in the doctors ward, mothers are dying of fever', 'grief, cold dread')} "
               "Rows of beds recede; at the back two beds have their white sheets drawn up over still shapes, small "
               f"and far away. {cast('a nun in a black habit and white wimple, praying beside one of the far beds')} "
               f"No faces of the dead, nothing graphic. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3a": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"{WARD2} {framing('MS', 'eye level', '50 mm', 'in the midwives ward, mothers survive', 'warm relief, tenderness')} "
               f"{cast('a young mother sitting up in bed, smiling and reaching out', 'a midwife in a grey dress and white apron and cap, handing her a swaddled newborn baby')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3b": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"SET: {HOSPITAL}, the doorway of the First Clinic, its cold green light spilling out. "
               f"{framing('MS', 'from behind the woman', '35 mm', 'a woman begs not to be taken into the doctors ward', 'desperation')} "
               f"{cast('a heavily pregnant young woman in a plain dress and a brown shawl, seen from behind, on her knees on the stone floor, hands clasped, pleading', 'a nurse in a grey dress and white cap standing in the doorway, troubled')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4a": dict(aspect="9:16", resolution="4K", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"{AUTOPSY} {framing('INSERT', 'close side angle', 'macro, shallow focus', 'a student scalpel slips and cuts a doctor finger during an autopsy', 'a sharp sudden shock')} "
               f"{cast('an older doctor, seen only as his left hand and black coat cuff resting on the edge of the white sheet', 'a student, seen only as a young hand holding a small steel scalpel that has just slipped')} "
               "One thin short line of red on the doctor's fingertip, nothing more. Only the white sheet, never a body. "
               f"{FULL_BLEED} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4b": dict(aspect="9:16", refs=["ref:plate-clinic", SM],
        roles=STYLE + "Reference 2 is IGNAZ SEMMELWEIS. ",
        prompt=f"SET: {HOSPITAL}, a small bare sickroom with one window. {framing('MS', 'eye level', '50 mm', 'his friend has died of the same fever as the mothers', 'grief turning into a terrible question')} "
               f"{cast(SEMMELWEIS + ', standing alone beside an empty stripped iron bed, his hat in his hand, staring at it')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"SET: {HOSPITAL}, a doorway between the grey autopsy room and the cold green ward. "
               f"{framing('LS', 'eye level', '28 mm', 'doctors go straight from the dead to the mothers without washing', 'careless confidence, unseen danger')} "
               f"{cast('a doctor in a dark frock coat striding through the doorway into the ward, his bare unwashed hands swinging by his sides', 'CROWD: exactly three young medical students following him, talking')} "
               "Behind them the grey autopsy room with a white sheet on the slab; ahead the beds of the ward. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6a": dict(aspect="9:16", refs=["ref:plate-clinic", SM, "kit:matt-sheet.jpg"],
        roles=STYLE + "Reference 2 is IGNAZ SEMMELWEIS. Reference 3 is MATT: copy his face, amber round spectacles, "
              "teal scarf and amber notebook only; his clothes are described below. ",
        prompt=f"{WASHROOM} {framing('MS', 'eye level', '35 mm', 'every student must scrub in chlorine water before entering', 'discipline, a new rule')} "
               "CROWD: exactly three medical students in shirtsleeves at the basins, scrubbing their hands hard; nobody "
               "else except Semmelweis and Matt. "
               f"{cast(SEMMELWEIS + ', standing behind them on the right, arms folded, watching every hand')} "
               f"{matt_beat('shirtsleeves and a dark 1840s waistcoat like the students', 'at the end of the row on the left, sniffing his wet hands and pulling a face')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-clinic", "kit:glasses-sheet.jpg"],
        roles=STYLE + "Reference 2 shows Matt's amber spectacles. ",
        prompt=f"{WASHROOM} {framing('INSERT', 'high angle, looking down', '50 mm', 'washing in chlorine saves the mothers', 'clean, hopeful')} "
               f"{cast('a doctor, seen only as two hands and rolled white sleeves, scrubbing in a white porcelain basin of pale cloudy chlorine water')} "
               f"{glasses_gag('folded on the wide rim of the basin')} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7a": dict(aspect="9:16", refs=["ref:plate-clinic", SM],
        roles=STYLE + "Reference 2 is IGNAZ SEMMELWEIS. ",
        prompt=f"{LECTURE} {framing('LS', 'low angle from the front', '28 mm', 'the doctors refuse to believe their own hands could kill', 'mockery and isolation')} "
               f"CROWD: exactly six {DOCTORS} on the benches, some turning away, one laughing behind his hand; nobody else. "
               f"{cast(SEMMELWEIS + ', standing alone at the lectern in the foreground, seen from the side, his hand on a sheaf of papers')} "
               f"{WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7b": dict(aspect="9:16", refs=["ref:plate-clinic", SM],
        roles=STYLE + "Reference 2 is IGNAZ SEMMELWEIS. ",
        prompt=f"{GATE} {framing('LS', 'eye level', '35 mm', 'his post ends; he leaves the hospital', 'lonely, defeated')} "
               f"{cast(SEMMELWEIS + ', in a dark overcoat and hat, walking out under the archway toward us carrying a small wooden box, snow on his shoulders')} "
               f"A gatekeeper's lantern behind him. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8": dict(aspect="9:16", refs=["ref:plate-clinic"],
        roles=STYLE,
        prompt=f"{ASYLUM} {framing('LS', 'eye level, one-point perspective', '24 mm', 'he died here, alone and forgotten', 'bleak, quiet')} "
               f"{NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9": dict(aspect="9:16", resolution="4K", refs=["ref:plate-clinic", SM],
        roles=STYLE + "Reference 2 is IGNAZ SEMMELWEIS (same face). ",
        prompt=f"{PORTRAIT} {framing('CU', 'slightly low angle', '85 mm, shallow focus', 'the man who was right, looking at us', 'tired, steady, unbowed')} "
               f"{cast(SEMMELWEIS + ', head and shoulders, lit warm from the window, looking straight into the camera')} "
               f"The lower 30% is his dark coat and the calm plain wall, for text. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="The Doctor They Hated for Saying Wash Your Hands", format="short", dual_format=False,
              image_resolution="2K", loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s6b: Matt's spectacles on the chlorine basin's rim",
              theme={"culture": "vienna-1840s", "font": "montserrat"})
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
