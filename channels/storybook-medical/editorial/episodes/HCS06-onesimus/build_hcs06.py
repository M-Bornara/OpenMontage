"""HCS06 Onesimus: writes projects/hcs06-onesimus/episode.json (title, narration, references, keyframes) from
storyboard-v1.md (script v2), with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS06-onesimus/build_hcs06.py
Then:  episode.py refs hcs06-onesimus   ->   episode.py keyframes hcs06-onesimus
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, WAVY_WRITING, cast, framing, glasses_gag,  # noqa: E402
                        lint_all, matt_beat, set_block)

PID = "hcs06-onesimus"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

# script v2 (storyboard-v1.md): two trims for length, "for centuries" in place of the unsourced "two hundred years"
NARRATION = """[serious] In 1721, smallpox hit Boston. The idea that saved lives came from a man who wasn't free.
His name was Onesimus. He was enslaved in the house of the minister Cotton Mather.
He had told Mather how West Africans beat smallpox… a tiny cut, a little matter from a sick person… then protection for life.
Only one doctor would try it: Zabdiel Boylston.
He started with his own six-year-old son.
[serious] The town was furious. Someone threw a grenade through Mather's window. The fuse went out.
The note said: "Cotton Mather, you dog… I'll inoculate you with this."
About one in seven who caught it died. Of Boylston's patients… about one in forty.
[curious] The idea came from Onesimus. For centuries, almost nobody said his name."""

# ── people (no likenesses exist: illustrated stand-ins; Onesimus with dignity, never in chains) ─────────────────────
ONESIMUS = ("ONESIMUS (30s, a West African man, dark brown skin, close-cropped black hair, a strong calm intelligent face, "
            "upright posture; a plain cream linen shirt, a dark brown wool waistcoat, dark breeches)")
MATHER = ("COTTON MATHER, the minister (late 50s, heavy-lidded scholarly eyes, a full white powdered wig, a black clerical "
          "coat with two small white preaching bands at the collar, black knee breeches and stockings)")
BOYLSTON = ("ZABDIEL BOYLSTON, the doctor (early 40s, his own brown hair tied back, clean-shaven, a determined kind face; "
            "a plain brown wool coat, a white cravat)")
TOMMY = "his son TOMMY (6, small, fair tousled hair, a white linen nightshirt)"

# ── sets ──────────────────────────────────────────────────────────────────────────────────────────────────────────
HARBOUR = set_block("Boston harbour from the hill", "1721",
                    "steep-roofed wooden houses and a few brick ones, white church steeples, long wooden wharves, tall "
                    "sailing ships at anchor; a cold grey dawn over grey-green water")
STUDY = set_block("Cotton Mather's study in his Boston house", "about 1716",
                  "dark wood panelling, floor-to-ceiling shelves crammed with leather books, a heavy desk with a quill, "
                  "inkwell and papers, a small-paned window with warm daylight")
KITCHEN = set_block("A small back room of a Boston house at dawn", "about 1716",
                    "bare plank walls, one small-paned window glowing with cold dawn light, everything else in shadow")
VILLAGE = set_block("A West African village, as a remembered story", "about 1700",
                    "round houses of red earth with thatched roofs, a packed red-earth yard, a big shade tree, warm "
                    "afternoon sun; painted softer and warmer like a memory; full-bleed to every edge, no border, no frame (the vignette is added in the edit)")
COFFEE = set_block("A Boston coffee house where the town's physicians meet", "1721",
                   "low beamed ceiling, smoky air, long wooden tables with pewter mugs and clay pipes, a fire, grey "
                   "light from leaded windows")
BEDROOM = set_block("The Boylstons' bedroom at night", "June 1721",
                    "a simple wooden bed with a patchwork quilt, whitewashed walls, one candle on a stool; warm small "
                    "pool of light, deep shadow around")
STREET = set_block("A narrow Boston street outside Mather's house", "1721",
                   "packed earth and cobbles, overhanging wooden houses, a painted plank front door with an iron latch (no doorknob), overcast daylight")
NIGHTROOM = set_block("An upstairs room in Mather's house at 3 a.m.", "November 1721",
                      "wide wooden floorboards, a small-paned window smashed in, cold blue moonlight falling across the "
                      "floor, deep shadow")
GRAVEYARD = set_block("A Boston burying ground in winter", "1721",
                      "slate headstones leaning in rows, bare black trees, a low stone wall, flat grey winter light, a "
                      "thin snow")
SICKROOM = set_block("A warm room in Boylston's house where inoculated patients recover", "1721",
                     "whitewashed walls, three simple beds, a fire in the hearth, golden afternoon light through a window")
PORTRAIT = set_block("A plain room with a window, Boston, morning", "1720s",
                     "a plain warm plaster wall, a small-paned window with golden morning light")

# Mather's diary (Nov 1721): a "granado" thrown through the window, the fuse knocked out, a paper tied to it
GRENADE = ("a 1721 hand grenade (a 'granado'): a rough dull cast-iron ball the size of a large apple, pitted and "
           "uneven, with a short wooden fuse plug in its top; the burnt-out fuse is a short blackened stub, its tip "
           "a dying dark-red ember with one thin curl of grey smoke; no cartoon bomb shape, no bright spark, no flame")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "

REFERENCES = {
    "sheet-onesimus": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {ONESIMUS}, Boston, about 1716. Front view, "
               "three-quarter view, profile view, back view, plus three head close-ups (calm and dignified, explaining "
               "with quiet confidence, a hint of a smile). Same scale in every view. No chains, no shackles. No text, "
               "labels or watermark."),
    "sheet-mather": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {MATHER}, Boston, 1721. Front view, "
               "three-quarter view, profile view, plus three head close-ups (astonished, pleading, stern). Same scale "
               "in every view. No text, labels or watermark."),
    "sheet-boylstons": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {BOYLSTON}, and {TOMMY}, Boston, 1721. Each "
               "in front view, three-quarter view and profile view at the same scale, plus head close-ups (the father "
               "worried, the father resolute; the boy brave, the boy laughing). No text, labels or watermark."),
    "plate-boston": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{STREET} Vertical frame looking down the street: overhanging wooden houses on both sides, a church "
               f"steeple at the end. EMPTY location plate: no people. Three clear depth layers. {PERIOD} {NO_TEXT}"),
}

O, MA, B = "ref:sheet-onesimus", "ref:sheet-mather", "ref:sheet-boylstons"
STYLE = "Reference 1 is the Boston plate, for the painting style and palette only. "
KEYFRAMES = {
    "s1a": dict(aspect="9:16", refs=["ref:plate-boston"],
        roles=STYLE,
        prompt=f"{HARBOUR} {framing('ELS', 'high angle from the hill', '24 mm', 'a plague ship has brought smallpox and the town is afraid', 'cold, ominous')} "
               "Rooftops in the foreground, the harbour beyond; one ship at the wharf flies a plain yellow quarantine "
               "flag; a few tiny figures in the lane below hurry away from it. The top 20% is grey dawn sky. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s1b": dict(aspect="9:16", refs=["ref:plate-boston", O],
        roles=STYLE + "Reference 2 is ONESIMUS (same build, hair and clothes). ",
        prompt=f"{KITCHEN} {framing('MCU', 'eye level', '85 mm, backlit', 'a man stands at the window, holding a knowledge nobody has asked him for', 'still, thoughtful, quietly strong')} "
               f"{cast(ONESIMUS + ', standing at the window in three-quarter view, half in silhouette against the dawn light, his face mostly in shadow with only a rim of light on his cheek and brow')} "
               f"No chains. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2": dict(aspect="9:16", refs=["ref:plate-boston", O, MA, "kit:glasses-sheet.jpg"],
        roles=STYLE + "Reference 2 is ONESIMUS. Reference 3 is COTTON MATHER. Reference 4 shows Matt's amber spectacles. ",
        prompt=f"{STUDY} {framing('MS', 'eye level', '35 mm', 'Onesimus stands in the doorway as Mather turns from his desk toward him', 'Onesimus upright and composed; Mather curious')} "
               f"{cast(ONESIMUS + ', standing tall in the open doorway on the right, in the light', MATHER + ', seated at his book-crowded desk on the left, turning in his chair toward him')} "
               f"{glasses_gag('folded on the desk beside the quill and inkwell')} {WAVY_WRITING} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3a": dict(aspect="9:16", refs=["ref:plate-boston", O, MA],
        roles=STYLE + "Reference 2 is ONESIMUS. Reference 3 is COTTON MATHER. ",
        prompt=f"{STUDY} {framing('OTS', 'over the shoulder of Mather, toward Onesimus', '50 mm', 'Onesimus explains how his people beat smallpox; here he is the teacher', 'Onesimus sure and calm, one hand open; Mather astonished, his quill put down')} "
               f"{cast(MATHER + ', seen from behind at the left edge: the back of his white wig and one black shoulder, out of focus', ONESIMUS + ', facing the camera in the centre, standing by the bookshelves, one hand open as he explains')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-boston"],
        roles=STYLE,
        prompt=f"{VILLAGE} {framing('INSERT', 'close side angle', 'macro, shallow focus', 'a healer makes a tiny scratch on a forearm to protect it from smallpox', 'careful, calm')} "
               f"{cast('a village healer, seen only as an older dark-skinned hand holding a small iron blade', 'a young person, seen only as a dark-skinned forearm resting on a woven mat', extra='The blade makes a tiny shallow scratch on the forearm, at most one small dot of red; beside it on the mat a short cotton thread with a little pale matter on it.')} "
               f"Nothing gory. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3c": dict(aspect="9:16", refs=["ref:plate-boston"],
        roles=STYLE,
        prompt=f"{VILLAGE} {framing('LS', 'eye level', '35 mm', 'the protected children run and play, healthy', 'joyful, safe')} "
               f"{cast('four children aged about 5 to 10, running and laughing across the yard under the big tree', 'an older healer woman in an indigo wrap, sitting in the shade of her doorway, smiling as she watches')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4": dict(aspect="9:16", refs=["ref:plate-boston", MA, B],
        roles=STYLE + "Reference 2 is COTTON MATHER. Reference 3 shows ZABDIEL BOYLSTON (the man, not the boy). ",
        prompt=f"{COFFEE} {framing('LS', 'low angle', '28 mm', 'the physicians refuse Mather, and one doctor stands up to say yes', 'scorn from the many, resolve from the one')} "
               f"{cast(MATHER + ', standing in the centre holding out an open hand, pleading', 'four wigged physicians in grey and black coats at the long table, turning their backs, one sneering over his shoulder', BOYLSTON + ', standing up from a side table on the right, resolute, one hand on the table')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5": dict(aspect="9:16", resolution="4K", refs=["ref:plate-boston", B],
        roles=STYLE + "Reference 2 is ZABDIEL BOYLSTON and his son TOMMY. ",
        prompt=f"{BEDROOM} {framing('MS', 'low, at the boy height', '50 mm', 'the doctor prepares to inoculate his own little son first', 'the boy is brave, biting his lip; the father is tender and afraid')} "
               f"{cast(TOMMY + ', sitting on the edge of the bed in the centre, his left sleeve rolled up, chin up', BOYLSTON + ', kneeling in front of him on the left, one hand gently holding the small arm, looking into his face')} "
               f"No blade visible. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user): v1 drew the door standing alone in the middle of the crowd
    "s6a": dict(aspect="9:16", refs=["ref:plate-boston", "kit:matt-sheet.jpg"],
        roles=STYLE + "Reference 2 is MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; "
              "his clothes are described below. ",
        prompt=f"{STREET} {framing('LS', 'eye level', '28 mm', 'the town turns on Mather: an angry crowd at his door', 'fury, fists raised')} "
               f"The front of Mather's two-storey wooden house fills the background across the whole frame, its plank front door with an iron latch set into the house wall on the right, closed. " f"CROWD: exactly six angry Boston townspeople in 1720s coats, caps and bonnets, in the street in the foreground and middle ground, facing the house, fists raised toward its door, one waving a printed pamphlet; nobody else except Matt. " f"{matt_beat('a brown 1720s frock coat and a black tricorn hat', 'at the left edge of the crowd, the only calm one, writing in his notebook')} "
               f"The pamphlet shows only blocks of tiny grey lines. {WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-boston"],
        roles=STYLE,
        prompt=f"{NIGHTROOM} {framing('MS', 'floor level', '24 mm', 'a grenade has been thrown through the window and lies on the floor; its fuse is dying', 'cold dread, held breath')} "
               f"{GRENADE}, lying on the floorboards in the centre among shards of broken window glass glinting in the "
               "moonlight; a folded paper note is tied around it with a string. The smashed window behind. It is NOT "
               "exploding and NOT sparking: the danger is over, only silence and that last curl of smoke. "
               f"{NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user): v1 s6b was a cartoon bomb with a fizzing spark, s7 a plain metal ball; now one consistent 1721 granado
    "s7": dict(aspect="9:16", resolution="4K", refs=["ref:plate-boston", "kf:s6b"],
        roles=STYLE + "Reference 2 is the grenade and note of the previous shot: the SAME object. ",
        prompt="SET: the same floor in Mather's house, close, by candlelight, November 1721. "
               f"{framing('INSERT', 'high angle, looking down', '50 mm', 'a threatening note is tied to the iron ball', 'menace')} "
               f"The SAME grenade as reference 2 ({GRENADE}), close: the paper note tied around it with string is half "
               "unfolded toward us in the centre; a candle at the upper edge throws warm light. "
               f"{WAVY_WRITING} {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8a": dict(aspect="9:16", refs=["ref:plate-boston"],
        roles=STYLE,
        prompt=f"{GRAVEYARD} {framing('LS', 'high angle', '35 mm', 'the town buries its smallpox dead', 'heavy grief')} "
               "CROWD: exactly three mourners in black cloaks, small in the middle distance, heads bowed beside a row of fresh earth graves; nobody else. "
               f"The headstones show no carving, only plain slate. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8b": dict(aspect="9:16", refs=["ref:plate-boston", B],
        roles=STYLE + "Reference 2 is ZABDIEL BOYLSTON and his son TOMMY. ",
        prompt=f"{SICKROOM} {framing('MS', 'eye level', '50 mm', 'the inoculated patients have come through, alive and getting well', 'relief and warmth')} "
               f"{cast(TOMMY + ', sitting up in the nearest bed in the centre, laughing', BOYLSTON + ', sitting on the bed beside him, smiling with relief, a hand on his shoulder', 'a young woman in a linen cap by the window, smiling, recovering', extra='At most two or three small faint marks on the boy, nothing more.')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9": dict(aspect="9:16", resolution="4K", refs=["ref:plate-boston", O],
        roles=STYLE + "Reference 2 is ONESIMUS (same face). ",
        prompt=f"{PORTRAIT} {framing('CU', 'slightly low angle', '85 mm, shallow focus', 'we finally see the face of the man the story forgot', 'quiet dignity, the hint of a smile, looking straight at the viewer')} "
               f"{cast(ONESIMUS + ', head and shoulders, lit warm by the window light, looking straight into the camera')} "
               f"The lower 25% is the calm plain wall and his waistcoat, for his name. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="The Enslaved Man Who Saved Boston", format="short", dual_format=False, image_resolution="2K",
              loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s2: Matt's spectacles on Mather's desk by the quill")
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
