"""HCS01 Forssmann: writes projects/hcs01-forssmann/episode.json (title, narration v3, references, keyframes) from
storyboard-v3.md, with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS01-forssmann/build_hcs01.py
Then:  episode.py refs hcs01-forssmann   ->   episode.py keyframes hcs01-forssmann
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (FULL_BLEED, NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, WAVY_WRITING, cast, glasses_gag,  # noqa: E402
                        lint_all, real_writing, set_block)

PID = "hcs01-forssmann"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

NARRATION = """[excited] In 1929, a young doctor pushed a tube through his own arm… all the way into his own heart.
Werner Forssmann, a trainee surgeon in Germany, wanted to reach a living heart through a vein…
His boss said no… Far too dangerous.
The nurse with the supplies agreed to help… if he tried it on HER.
[mischievously] He tricked her… He numbed his own arm instead…
He slid the catheter in… Sixty-five centimeters.
Then he walked to the X-ray room, the tube still in his arm.
[curious] The picture showed the tip… inside his heart… He was fine.
His reward? His new boss in Berlin fired him.
Twenty-seven years later, the world caught up… Nobel Prize.
[serious] But in 1932, he had joined the Nazi Party."""

# ── people (one look each, storyboard-v3 "Sets and cast") ───────────────────────────────────────────────────
FORSSMANN = ("WERNER FORSSMANN (25, lean, dark hair slicked straight back, clean-shaven, narrow face, dark eyes, a keen "
             "restless look; white surgical coat over a white shirt and dark tie)")
SCHNEIDER = ("DR. SCHNEIDER, the chief surgeon (about 55, heavy-set, grey hair, a thick grey moustache, heavy eyebrows, dark three-piece suit under an open white coat)")
DITZEN = ("NURSE GERDA DITZEN (about 30, kind round face, light-brown hair pinned up under a starched white nurse's cap, "
          "a pale grey-blue dress with a white apron and white collar, a ring of large iron keys at her belt)")
SLEEVE = "his LEFT shirt and coat sleeve rolled up above the elbow"

# ── sets ─────────────────────────────────────────────────────────────────────────────────────────────────────
OR = set_block("The operating room of the Auguste-Viktoria hospital, Eberswalde, Germany", "1929",
               "pale green-white tiled walls, white enamel and nickel-steel fittings, a tall frosted window, a tall "
               "glass-fronted supply cabinet, a narrow steel operating table with a white sheet, one amber lamp hanging "
               "low; cool green-white light with one warm pool of amber under the lamp")
WARD = set_block("A doctors' room in the same hospital, Eberswalde", "1929",
                 "green-white tiled lower walls, cream plaster above, a tall window with white muslin, an oak desk, "
                 "a large framed anatomy wall chart of a human arm and chest; soft morning light")
OFFICE = set_block("The chief surgeon's office, Eberswalde", "1929",
                   "dark oak panelling, a heavy oak desk, a crank wall telephone, glass-fronted bookcases of medical "
                   "books, a small skull used as a paperweight; warm brown lamplight, the only room in the film that is "
                   "dark and wooden")
CORRIDOR = set_block("The long hospital corridor, Eberswalde", "1929",
                     "a very long straight corridor, cream tiles with a green band, a row of white globe lamps receding "
                     "to a vanishing point, doors on both sides, a polished floor reflecting the lamps; cool and quiet")
XRAY = set_block("The X-ray room, Eberswalde", "1929",
                 "dim blue light, a tall wooden-cabinet X-ray apparatus with a glowing glass tube and thick cables, a "
                 "glowing wall lightbox; the only blue room in the film")

STYLE_PLATE = f"{HC1}/plate-study.png"           # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only

REFERENCES = {
    # ── cast sheets ──
    "sheet-forssmann": dict(aspect="16:9", refs=[SHEET_LAYOUT],
        roles="Reference 1 shows our character model-sheet layout and painting style only (not this person). ",
        prompt=f"Clean character model sheet on plain bone-white paper: {FORSSMANN}, Germany, 1929. Front view, "
               "three-quarter view, profile view, back view, plus three head close-ups (determined, sly half-smile, "
               "relieved). Same scale in every view. No text, labels or watermark."),
    "sheet-schneider": dict(aspect="16:9", refs=[SHEET_LAYOUT],
        roles="Reference 1 shows our character model-sheet layout and painting style only (not this person). ",
        prompt=f"Clean character model sheet on plain bone-white paper: {SCHNEIDER}, Germany, 1929. Front view, "
               "three-quarter view, profile view, plus three head close-ups (stern, saying no, impatient). Same scale in "
               "every view. No text, labels or watermark."),
    "sheet-ditzen": dict(aspect="16:9", refs=[SHEET_LAYOUT],
        roles="Reference 1 shows our character model-sheet layout and painting style only (not this person). ",
        prompt=f"Clean character model sheet on plain bone-white paper: {DITZEN}, Germany, 1929. Front view, "
               "three-quarter view, profile view, back view, plus three head close-ups (eyebrows raised pointing at "
               "herself, eyes closed waiting, surprised). Same scale in every view. No text, labels or watermark."),
    # ── set plates (people-free, vertical) ──
    "plate-or": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{OR} Vertical frame of the room from the door: the operating table in the middle distance, the "
               "supply cabinet on the left, the lamp above. EMPTY location plate: no people. Three clear depth layers. "
               f"{PERIOD} {NO_TEXT}"),
    "plate-corridor": dict(aspect="9:16", refs=["ref:plate-or"],
        roles="Reference 1 is the same hospital (match its tiles, colours and painting style). ",
        prompt=f"{CORRIDOR} Perfectly centred, symmetric one-point perspective down the corridor. EMPTY location "
               f"plate: no people. {PERIOD} {NO_TEXT}"),
    "plate-xray": dict(aspect="9:16", refs=["ref:plate-or"],
        roles="Reference 1 is the same hospital (match its painting style; this room is blue, not green). ",
        prompt=f"{XRAY} Vertical frame: the apparatus on the left, the glowing lightbox on the right wall at chest "
               f"height, empty. EMPTY location plate: no people. {PERIOD} {NO_TEXT}"),
}

F = "ref:sheet-forssmann"
KEYFRAMES = {
    "s1a": dict(aspect="9:16", refs=["ref:plate-or"],
        roles="Reference 1 is this operating room (style and colours). ",
        prompt=f"{OR} Extreme close-up: a long coiled red-brown rubber catheter tube lying in loose loops in a steel "
               "kidney-shaped tray on the white sheet, one open end pointing toward the camera, lit by the single amber "
               "lamp; the tiles soft and out of focus behind. The coil fills the lower two thirds of the frame; the top "
               f"third is calm out-of-focus tiles. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD}"),
    "s1b": dict(aspect="9:16", refs=["ref:plate-or"],
        roles="Reference 1 is for the painting style and palette only (never its room). ",
        prompt="SET: an anatomy plate in an old illustrated medical book, Germany, 1920s. A storybook anatomy plate on warm cream paper, like a page from an old illustrated medical book "
               "painted in our style: a man seen from the front FROM THE TOP OF THE HEAD DOWN TO THE WAIST ONLY "
               "(cropped at the waist, nothing below), drawn as a simple ink outline with a soft cream wash, both arms "
               "hanging slightly away from the body. Inside, drawn in soft colour: ONE blue vein, ONLY in the arm on the "
               "VIEWER'S RIGHT (his LEFT arm), running up the inner arm from the elbow crease, over the shoulder, under "
               "the collarbone and down into the top of the heart; the heart painted in muted warm red, slightly to the "
               "VIEWER'S RIGHT of the chest centre. The arm on the viewer's left has no vein. Nothing else inside the body. The figure is centred and fills the middle 70% "
               "of the frame; plain cream paper around it. No face details (a simple blank oval head). "
               f"{FULL_BLEED} {SAFE_FRAMING} {NO_TEXT}"),
    "s2": dict(aspect="9:16", refs=["ref:plate-or", F, "kit:glasses-sheet.jpg"],
        roles="Reference 1 is the hospital style. Reference 2 is WERNER FORSSMANN (same face, hair, white coat). "
              "Reference 3 shows Matt's amber spectacles. ",
        prompt=f"{WARD} Wide vertical frame. {cast(FORSSMANN + ', standing in the left third of the frame, three-quarter view, gazing up at the anatomy chart, one hand on his chin')} "
               "The large anatomy wall chart hangs on the right wall: a human arm and chest with one vein in blue "
               "running from the elbow to the heart, painted simply. The top 20% of the frame is calm cream wall. "
               f"{glasses_gag('folded on the windowsill next to a potted geranium')} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3": dict(aspect="9:16", refs=["ref:plate-or", "ref:sheet-schneider"],
        roles="Reference 1 is the hospital painting style (this office is dark oak, not tiles). Reference 2 is DR. "
              "SCHNEIDER (same face, moustache, suit). ",
        prompt=f"{OFFICE} Medium close-up from a LOW angle, so he looms: {cast(SCHNEIDER + ', seated behind the desk, leaning forward, one flat hand pressed on the desk, a firm stern look straight at the viewer')} "
               "The crank telephone on the wall behind him, the skull paperweight on the desk. The top 20% of the frame "
               f"is dark calm panelling. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4": dict(aspect="9:16", refs=["ref:plate-or", "ref:sheet-ditzen"],
        roles="Reference 1 is this operating room. Reference 2 is NURSE GERDA DITZEN (same face, cap, dress). ",
        prompt=f"{OR} Medium shot: {cast(DITZEN + ', standing in front of the glass supply cabinet, holding up her ring of large iron keys in her right hand at shoulder height, pointing at her own chest with her left index finger, eyebrows raised, a bold half-smile')} "
               "The keys hang clearly separated from her hand against the cabinet glass. Her head is in the upper half "
               f"of the frame; the bottom 20% is plain floor and table edge. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5": dict(aspect="9:16", refs=["ref:plate-or", F, "ref:sheet-ditzen"],
        roles="Reference 1 is this operating room. Reference 2 is WERNER FORSSMANN. Reference 3 is NURSE GERDA DITZEN. ",
        prompt=f"{OR} Side view, comedy two-shot. {cast(DITZEN + ', lying on her back on the operating table in the lower half of the frame, fully dressed, eyes closed, hands folded, patiently waiting', FORSSMANN + ', standing behind the head of the table in the right half of the frame, turned AWAY from her, ' + SLEEVE + ', holding out his bare LEFT forearm (the arm with the rolled sleeve) and dabbing it with a cotton swab held in his RIGHT hand, glancing back at her with a sly look')} "
               f"The top 20% of the frame is calm tiled wall. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2: v1 was only his face, so the line "he slid the catheter in" had no action (user review of the storybook)
    "s6a": dict(aspect="9:16", resolution="4K", refs=["ref:plate-or", F],
        roles="Reference 1 is this operating room. Reference 2 is WERNER FORSSMANN (same face, hair, white coat). ",
        prompt=f"{OR} Close-up from over his right shoulder, looking down at the action: {cast(FORSSMANN)} He sits at "
               "the operating table; his bare LEFT forearm (the arm with the rolled-up sleeve) rests on the white sheet, "
               "palm up. With his RIGHT hand he is feeding a thin red-brown rubber tube into the crook of his left elbow; "
               "the point where it enters is completely hidden under a small square of white gauze pressed by his "
               "fingers. A long loop of the tube trails back from his hand into the steel tray. His face is in partial "
               "profile in the upper third of the frame, eyes on his arm, intensely focused, one bead of sweat. Warm "
               "amber lamp light. NO blood, NO needle, NO visible skin opening. The arm and hands fill the centre of the "
               f"frame. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6b": dict(aspect="9:16", refs=["ref:plate-or"],
        roles="Reference 1 is this operating room (style and colours). ",
        prompt=f"{OR} Extreme close-up on the white sheet: a thin red-brown rubber catheter tube (one plain single tube with simple rounded "
               "ends, NO fork, NO Y-branch) laid straight beside "
               "a long brass measuring rule, running diagonally from the lower left to the upper right; the rule has "
               "fine engraved tick marks only, with NO numbers. No skin, no needle, no blood. The middle 30% of the "
               f"frame height is the plainest part of the sheet. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7": dict(aspect="9:16", refs=["ref:plate-corridor", F],
        roles="Reference 1 is this corridor (same tiles, lamps, perspective). Reference 2 is WERNER FORSSMANN. ",
        prompt=f"{CORRIDOR} Perfectly centred symmetric frame down the corridor. {cast(FORSSMANN + ', small in the middle distance at the centre, walking toward the camera with purpose, ' + SLEEVE + ', a thin rubber tube taped along his inner left forearm with white tape, his right hand steadying it')} "
               f"The top 25% of the frame is the receding ceiling and lamps. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8a": dict(aspect="9:16", refs=["ref:plate-xray"],
        roles="Reference 1 is this X-ray room (blue light). ",
        prompt=f"{XRAY} Close-up of the glowing wall lightbox filling the frame, an X-ray film clipped to it: a "
               "human chest seen from the front in soft grey-blue, the ribs, the spine, and the shadow of the heart "
               "slightly to the viewer's right of centre; the patient's left shoulder and upper arm at the VIEWER'S "
               "RIGHT edge of the film. No tube or line on the film. The film fills the middle 70% of the frame. "
               f"{NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2: v1 showed the tube on his right arm (user review); v2 did too, so s8b.png is the MIRRORED s8b.orig.png (L25)
    "s8b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-xray", F],
        roles="Reference 1 is this X-ray room. Reference 2 is WERNER FORSSMANN (same face). ",
        prompt=f"{XRAY} Medium shot: {cast(FORSSMANN + ', standing beside the glowing lightbox on the right, ' + SLEEVE + ', the thin tube still taped to his inner left forearm, looking at the film with a small relieved half-smile, lit cool blue from the lightbox')} "
               "He faces the camera, so his LEFT arm (rolled sleeve, taped tube) is on the VIEWER'S RIGHT side of the "
               "image; his RIGHT arm, on the viewer's left, has its sleeve down and no tube. "
               f"The bottom 20% of the frame is the dark floor and apparatus base. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9": dict(aspect="9:16", refs=["ref:plate-or", F],
        roles="Reference 1 is the hospital painting style. Reference 2 is WERNER FORSSMANN (his coat). ",
        prompt="SET: a plain wooden desk in a hospital office, Berlin, 1929, grey daylight. Extreme close-up from "
               "above: a single typed letter on official paper lying on the desk, a dark wax seal at its foot; at the "
               "right edge of the frame his hand (only the hand and white coat sleeve) pulls a dark overcoat from the "
               "back of a chair. The letter fills the centre. "
               f"{real_writing('Charité · Berlin', 'as a small printed letterhead at the top')} {WAVY_WRITING} "
               f"No greeting line. {SAFE_FRAMING} {PERIOD}"),
    "s10a": dict(aspect="9:16", refs=["ref:plate-or"],
        roles="Reference 1 is for the painting style only. ",
        prompt="SET: a café table, Germany, 1956, warm golden morning light, muted colours. Close-up from above: a "
               f"folded 1956 newspaper lying on the table next to a coffee cup. {real_writing('NOBEL PRIZE', 'as the big headline across the top of the front page')} "
               f"A blurred photograph block under the headline. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD}"),
    "s10b": dict(aspect="1:1", refs=["ref:plate-or"],
        roles="Reference 1 is for the painting style only. ",
        prompt="Front view, perfectly flat and centred: the face of a round gold medal, painted in our storybook "
               "style, a laurel wreath around the rim and a small torch in the centre, warm gold with soft highlights. "
               "The circle fills 90% of the frame on a plain dark-red background. Generic design, not any real medal. "
               f"{FULL_BLEED} {NO_PEOPLE} {NO_TEXT}"),
    "s11": dict(aspect="9:16", refs=["ref:plate-or", F],
        roles="Reference 1 is the hospital painting style. Reference 2 is WERNER FORSSMANN (same face; now in a dark "
              "suit, a few years older). ",
        prompt="SET: a plain dark-green studio backdrop, Germany, 1932, soft side light. Head-and-shoulders portrait "
               f"of {FORSSMANN.replace('white surgical coat over a white shirt and dark tie', 'dark suit, white shirt and dark tie')}, "
               "28 here, a serious neutral expression, looking just past the camera. His head is in the upper half; "
               f"his suit and the painted backdrop continue all the way to the bottom edge (no flat band, no empty strip). {cast('FORSSMANN')} No badges, pins, symbols or "
               f"uniforms of any kind. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}

# ── cover (plan/thumbnail-craft.md: movie poster, text band at the bottom, publish.cover.textY 1240) ─────────
COVERS = {
    "cover": dict(aspect="9:16", refs=["ref:plate-xray", F],
        roles="Reference 1 is the X-ray room (style and blue light). Reference 2 is WERNER FORSSMANN (same face, hair, coat). ",
        prompt=f"{XRAY} MOVIE-POSTER COVER ART for a vertical short film, 9:16. The hero fills 55-70% of the frame "
               f"height, bold and clear. {cast(FORSSMANN + ', front and centre, waist up, facing the viewer, ' + SLEEVE + ', holding his bare LEFT forearm up across his chest; a thin red-brown rubber catheter tube enters the inner LEFT elbow under a small square of white gauze and loops up over his shoulder; he looks straight at the viewer with a daring, slightly mad half-smile')} "
               "He faces the camera, so his LEFT arm (rolled sleeve, the tube) is on the VIEWER'S RIGHT side of the "
               "image; his RIGHT arm has its sleeve down and no tube. Behind his shoulder the glowing lightbox shows a "
               "pale X-ray of a chest with the faint shadow of the heart. One strong warm amber key light on his face "
               "and the tube against the cool blue room, teal-charcoal falloff at the edges. His face stays between 15% "
               "and 55% of the frame height. The bottom 30% of the frame is the same room continuing, darker and out "
               "of focus, with nothing in it. NO blood, NO wound. NO panel, NO border, NO split screen; no lettering "
               f"anywhere (the title is added later). {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}

# s1b and s9 were fixed locally after generation (plan/prompt-lessons.md L25, L26, L24): the arm-side vein and the
# letter's lorem ipsum. Originals: keyframes/s1b.orig.png, s9.orig.png. Don't regenerate them without redoing the fix.


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="He Pushed a Tube Into His Own Heart", format="short", dual_format=False, image_resolution="2K",
              references=REFERENCES, keyframes=KEYFRAMES, covers=COVERS)
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES, **COVERS})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
