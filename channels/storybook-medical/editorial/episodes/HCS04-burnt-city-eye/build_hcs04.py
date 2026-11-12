"""HCS04 golden eye: writes projects/hcs04-burnt-city-eye/episode.json (title, narration, references, keyframes) from
storyboard-v1.md, with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS04-burnt-city-eye/build_hcs04.py
Then:  episode.py refs hcs04-burnt-city-eye   ->   episode.py keyframes hcs04-burnt-city-eye
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, cast, framing, glasses_gag, lint_all,  # noqa: E402
                        matt_beat, set_block)

PID = "hcs04-burnt-city-eye"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

NARRATION = """[curious] Five thousand years ago, a woman in Iran was buried with a golden eye.
The Burnt City, around 2900 BC. She died in her late twenties.
Her eye was a half-ball of tar paste… covered in a thin layer of gold.
Drawn on it: an iris… and fine gold lines, like rays of light.
Two tiny holes held it in place with a thread.
Under a microscope, her eye socket showed the marks… she had worn it for years.
[mischievously] Was she a priestess? A queen? Nobody knows. That part is a legend.
[curious] Some archaeologists say it wasn't an eye at all… but an eyepatch.
Either way, five thousand years ago… someone made her a golden eye."""

# ── people (no likeness exists; never from a modern reconstruction) ──────────────────────────────────────────────
WOMAN = ("THE WOMAN of the Burnt City (about 28, slim, warm olive-brown skin, long dark hair in one thick braid down her "
         "back, a calm proud face, a plain undyed cream wool dress with a woven belt, a necklace of small carnelian and "
         "lapis stone beads). Her LEFT eye is the golden eye: a smooth gold half-ball with a painted iris and fine "
         "radiating lines, held by a very fine gold thread that runs from its sides back around her head")
EYE = ("the golden eye: a small half-ball about 2.5 cm across, a black tar core under a thin skin of gold; its WHOLE "
       "front surface is gold (no white, no cream, it must not look like a real eyeball or a modern glass eye); on its "
       "front a circle for the iris at the centre and very fine thin gold lines radiating out from it like the rays of "
       "a sun; two tiny holes on opposite sides of its rim")

# ── sets ──────────────────────────────────────────────────────────────────────────────────────────────────────────
CITY = set_block("Shahr-e Sukhteh, the Burnt City, on a desert terrace in Sistan, south-east Iran", "about 2900 BC",
                 "flat-roofed sun-dried mud-brick houses in warm ochre, narrow lanes, reed mats, clay jars, a canal of "
                 "the Helmand delta with reeds, a vast flat desert plain to the horizon; dry golden dusk light")
GRAVE = set_block("A family grave at the edge of the Burnt City cemetery at night", "about 2900 BC",
                  "a rectangular pit in pale desert earth, two small clay oil lamps, a dark starry sky; only lamplight")
HOUSE = set_block("The doorway of a mud-brick house in the Burnt City, morning", "about 2900 BC",
                  "a low wooden lintel, smooth ochre plaster walls, a woven reed curtain pushed aside, soft cool morning "
                  "light from the lane")
TEMPLE = set_block("Mud-brick temple steps of the Burnt City, as a legend", "about 2900 BC",
                   "broad steps of ochre mud brick, a red-gold sunset sky, a golden haze, painted like an old woven "
                   "tapestry with a soft patterned border at the edges")
WORKSHOP = set_block("A craftsman's workshop in the Burnt City by lamplight", "about 2900 BC",
                     "a low mud-brick room, a work mat on the floor, small stone and bone tools, a pot of black tar, "
                     "thin gold leaf, one clay oil lamp; deep warm shadows")
DIG = set_block("An archaeological excavation at Shahr-e Sukhteh at sunset", "2006",
                "a neat square trench cut into pale dusty earth, string grid lines, a soft paint brush; low red-gold "
                "sunlight raking across the ground")
FIELDLAB = set_block("The dig's field lab, a canvas tent beside the trenches", "2006",
                     "folding tables, plastic trays of clay potsherds, round dig sieves, a clip-on work lamp, blue "
                     "nitrile gloves; warm lamp light against the blue dusk outside the tent flap")
NIGHTLAB = set_block("A university research lab at night", "2006",
                     "a dark room, one desk lamp, a grey stereo microscope, shelves of labelled boxes in shadow; cool "
                     "blue with a single warm pool of light")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "

REFERENCES = {
    "sheet-woman": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {WOMAN}. Bronze Age Iran, 2900 BC. Front view, "
               "her LEFT profile (the golden-eye side), three-quarter view, back view (the braid and the thread around "
               "her head), plus three head close-ups (calm, a small smile, proud). Same scale in every view. No text, "
               "labels or watermark."),
    # v2 (L30): v1 used the room plate as reference and came back as a log cabin with giant foggy domes
    "prop-eye": dict(aspect="16:9", refs=[SHEET_LAYOUT],
        roles="Reference 1 shows our model-sheet layout and painting style only (not its subject). ",
        prompt=f"Clean prop model sheet on plain bone-white paper: {EYE}. Four views at the same scale: straight front "
               "(the iris circle and rays), side view (the half-ball profile and one tiny hole), three-quarter view, and "
               "the back (flat, black tar). Each view small, about 15% of the sheet height, on plain bone-white paper with a soft "
               "contact shadow; no room, no furniture, no background scene. Painted in our storybook style, gold catching warm light. "
               "No text, labels or watermark."),
    "plate-city": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{CITY} Vertical frame from a rooftop: lanes of flat mud-brick roofs stepping down to the canal, the "
               "desert plain beyond. EMPTY location plate: no people. Three clear depth layers. "
               f"{PERIOD} {NO_TEXT}"),
}

W = "ref:sheet-woman"
E = "ref:prop-eye"
STYLE = "Reference 1 is the Burnt City plate, for the painting style and palette only. "
KEYFRAMES = {
    "s1": dict(aspect="9:16", refs=["ref:plate-city", E],
        roles=STYLE + "Reference 2 is THE GOLDEN EYE prop (same shape, iris circle and rays). ",
        prompt=f"{DIG} {framing('ECU', 'top-down, looking straight into the trench', 'macro 100 mm', 'a brush has just swept the dust off a golden eye lying in the earth of a grave', 'a breathless discovery')} "
               f"{EYE}, lying half-buried in pale dusty earth in the centre of the frame, its gold face up and catching "
               "the low red sunlight; a soft paint brush rests beside it, a little dust still in the air. No bones "
               f"visible. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", refs=["ref:plate-city"],
        roles=STYLE,
        prompt=f"{CITY} {framing('ELS', 'high angle', '24 mm', 'the city settles down for the evening', 'peaceful, ancient')} "
               "Rows of flat mud-brick roofs in the foreground and middle distance, thin cooking smoke rising, the canal "
               "glinting, tiny figures and two donkeys walking home along a lane, the desert plain to the horizon. The "
               f"top 20% is calm dusk sky. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2b": dict(aspect="9:16", refs=["ref:plate-city"],
        roles=STYLE,
        prompt=f"{GRAVE} {framing('MS', 'eye level, from the end of the grave', '50 mm', 'her family lays a bronze mirror beside her in the grave', 'quiet grief')} "
               f"{cast('an older woman in a dark wool shawl, kneeling on the left edge of the grave', 'a young man in a cream wool tunic, kneeling on the right, gently lowering a round bronze hand mirror into the grave', extra='In the pit lies a body under one loosely draped plain cream shroud, lying on its side with knees slightly drawn up, seen only as a soft cloth shape; NOT bandaged, NOT wrapped in strips, nothing like an Egyptian mummy; no face, no skin, no bones.')} "
               f"Their faces are lit from below by the two oil lamps. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2: v1 drew the eye cream like a ping-pong eyeball (from the prop sheet); reference 2 is now the gold eye of s1
    "s3": dict(aspect="9:16", resolution="4K", refs=["ref:plate-city", "kf:s1", "kit:glasses-sheet.jpg"],
        roles=STYLE + "Reference 2 shows THE GOLDEN EYE (copy its all-gold surface, ignore the trench). Reference 3 shows Matt's amber spectacles. ",
        prompt=f"{FIELDLAB} {framing('INSERT', 'side angle, low over the table', 'macro, very shallow focus', 'an archaeologist holds the golden eye under the lamp to study what it is made of', 'wonder')} "
               f"{EYE}, resting in the cupped palm of one blue-gloved hand (only the hand and wrist in frame), in the "
               "centre of the frame; a small chip at the lower edge of the rim shows the black tar inside under the gold. "
               "Behind, softly out of focus: trays of potsherds and a round dig sieve. "
               f"{glasses_gag('hanging by one arm from the rim of the dig sieve in the blurred background')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user): v2 came out as a flat gold medallion, unlike s1/s3; reference 2 is now the eye in the palm (s3)
    "s4": dict(aspect="9:16", resolution="4K", refs=["ref:plate-city", "kf:s3", "kf:s1"],
        roles=STYLE + "References 2 and 3 show THE GOLDEN EYE: draw exactly this object (same domed shape, same "
              "engraved almond eye outline, same iris circle, same gold), ignore the hand, lab and trench. ",
        prompt="SET: a plain dark velvet cloth under a single warm lamp, 2006. "
               f"{framing('ECU', 'straight on', 'macro', 'we look straight into the golden eye and see what was drawn on it', 'mesmerising')} "
               "The same small domed gold half-ball as references 2 and 3, seen from the front and a little above so its "
               "rounded dome is clear (NOT a flat disc, NOT a coin or medallion), filling the middle 60% of the frame on "
               "the dark cloth: the engraved almond-shaped eye outline, the iris circle at its centre, and fine thin "
               "lines radiating from the iris like rays, crisp and clear. Soft gold highlights on the curve of the "
               f"dome, a little black tar visible at the rim. {NO_PEOPLE} {SAFE_FRAMING} {NO_TEXT}"),
    # v3: v2 still looped a second strand under the ear (the model draws a loop for 'two holes'); now one straight
    # headband line. v2 (user, rough cut 1): both strands left the eye on the same side and one ran down her cheek; the holes are on
    # opposite sides of the eye, so in profile only the OUTER hole shows and one thread runs back over the ear
    "s5": dict(aspect="9:16", resolution="4K", refs=["ref:plate-city", W, "kf:s4"],
        roles=STYLE + "Reference 2 is THE WOMAN (same face, braid, dress, necklace). Reference 3 is THE GOLDEN EYE "
              "(copy its all-gold domed surface and engraved eye exactly). ",
        prompt=f"{HOUSE} {framing('MCU', 'her LEFT profile, eye level', '85 mm, shallow focus', 'she stands in her doorway wearing the golden eye, held by its fine thread', 'calm, at ease, a small private smile')} "
               f"{cast(WOMAN + ', seen in LEFT profile facing the left side of the frame, so the golden eye in her LEFT eye socket faces the camera')} "
               "The golden eye sits in her eye socket like a real eye would, all gold. It is held by ONE very fine "
               "gold thread worn like a thin headband: from the side of the eye it runs in ONE single straight line, "
               "level, back across her temple above the ear to the back of her head, where it disappears under her hair. "
               "Exactly one straight gold line on this side of her head: NO loop, NO second strand, nothing below the "
               "ear, nothing on the cheek or jaw. The golden eye sits in the upper-middle of the frame, catching the "
               "morning light. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # NOTE: this second "s5" key overrides the generated-from-scratch s5 above (kept for the record).
    # v4 (edit, not a new picture): v2 and v3 both drew a LOOP (a second strand under the ear) however it was asked;
    # so the good v2 frame is edited instead: remove only the lower strand
    "s5": dict(aspect="9:16", resolution="4K", refs=["proj:assets/images/keyframes/s5.v2-loop.keep.png"],
        roles="Reference 1 is the finished image to EDIT. ",
        prompt="EDIT this exact image; change only one thing. Two thin gold threads leave the golden eye toward the back "
               "of her head: an upper one that runs straight back above her ear, and a lower one that curves down below "
               "her ear and loops back. REMOVE the lower curved thread completely and paint her skin, ear and hair "
               "there as if it was never there. Keep the upper straight thread. Everything else stays identical: her "
               "face, the golden eye, the pose, the light, the colours, the framing, the painting style. "
               "SHOT: unchanged medium close-up. FRAMING: unchanged; every story-relevant person, object and action "
               "sits inside the central 70% of the frame. CAMEO: none needed in this shot."),
    "s6a": dict(aspect="9:16", refs=["ref:plate-city"],
        roles=STYLE,
        prompt=f"{NIGHTLAB} {framing('OTS', 'over the right shoulder of the researcher', '35 mm', 'a scientist bends to the microscope to examine the bone of her eye socket', 'focused, hushed')} "
               f"{cast('a researcher in a grey sweater (40s, dark hair, seen from behind and in partial profile), bending to the eyepieces of a grey stereo microscope')} "
               "Under the microscope lens: a small irregular curved fragment of pale skull bone, the size of a coin, on a black tray, clean like stone (NOT a cartoon dog-bone shape). The lamp makes the "
               f"only warm light. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user, rough cut 1): v1 showed a groove on what looked like a long leg bone, not an eye socket
    "s6b": dict(aspect="9:16", refs=["ref:plate-city", "kf:s4"],
        roles="Reference 1 is for the painting style and palette only. Reference 2 shows the size and round shape of "
              "the golden eye (do NOT draw the eye itself). ",
        prompt="SET: the view down a microscope, storybook painting, 2006. "
               f"{framing('ECU', 'straight down the eyepiece', 'microscope view', 'the bone of her eye socket shows a round worn mark where the golden eye rested for years', 'a quiet revelation, not gory')} "
               "A large round field of view fills almost the whole frame, black around the circle. Inside it: the "
               "curved RIM of a human eye socket (the orbit) in clean pale ivory bone, smooth and dry like weathered "
               "stone, clearly the edge of an eye socket, seen close; on the inner wall of the socket, a faint round "
               "polished imprint the size and curve of the half-ball eye, as if something round rested there for years. "
               f"Only bone, no skin, no blood, nothing gory; a museum specimen. {NO_PEOPLE} {SAFE_FRAMING} {NO_TEXT}"),
    # NOTE: overrides the s6b above. v3 (user, rough cut 2: "the circle inside the socket looks like an eyeball"): edit
    # the v2 frame so the imprint is a faint worn hollow, not a drawn ring
    "s6b": dict(aspect="9:16", refs=["proj:assets/images/keyframes/s6b.v2-ring.png"],
        roles="Reference 1 is the finished image to EDIT. ",
        prompt="EDIT this exact image; change only one thing. Inside the eye socket there is a crisp drawn circle that "
               "looks like an eyeball outline. Replace it with a FAINT worn hollow: a soft, slightly smoother and "
               "slightly lighter patch of bone on the socket's inner wall, with NO outline, no ring, no circle line, as "
               "if something round had rested and rubbed there for years. Keep everything else identical: the skull, "
               "the round microscope view, the black surround, the colours, the painting style. "
               "SHOT: unchanged extreme close-up. FRAMING: unchanged; every story-relevant person, object and action "
               "sits inside the central 70% of the frame. NO PEOPLE."),
    "s7": dict(aspect="9:16", refs=["ref:plate-city", W, "kit:matt-sheet.jpg"],
        roles=STYLE + "Reference 2 is THE WOMAN (same face, braid, golden left eye). Reference 3 is MATT: copy his face, "
              "amber round spectacles, teal scarf and amber notebook only; his clothes are described below. ",
        prompt=f"{TEMPLE} {framing('LS', 'low angle up the steps', '35 mm', 'the legend: she stands on the temple steps like a priestess-queen', 'grand, mythical, a little too perfect, like a story told around a fire')} "
               f"{cast(WOMAN + ', in a long deep-blue robe and a thin gold headband, standing tall at the top of the steps in the upper-middle of the frame, her golden left eye glowing', 'a crowd of about eight townspeople in cream and ochre wool at the foot of the steps, seen from behind, raising their hands toward her', extra=matt_beat('a plain Bronze Age undyed wool robe and a rope belt', 'at the far left edge of the crowd, not raising his hands, writing in his notebook with a sceptical tilt of the head'))} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8": dict(aspect="9:16", refs=["ref:plate-city", E],
        roles=STYLE + "Reference 2 is THE GOLDEN EYE prop. ",
        prompt=f"{FIELDLAB} {framing('MS', 'reverse angle, from the tent flap looking in, eye level', '35 mm', 'one archaeologist tries the golden eye on over her own eye like a patch to make her point', 'playful and comic; her colleague is unconvinced')} "
               f"{cast('a woman archaeologist (30s, sun hat pushed back, dusty khaki shirt) on the left, holding the golden eye up over her right eye like an eyepatch, eyebrows raised, half-grinning', 'a man archaeologist (50s, grey beard, dusty blue shirt) on the right, arms folded, one eyebrow up, not convinced')} "
               "Between them a folding table with trays of potsherds and the clip-on lamp. The blue dusk is behind "
               f"them, outside the tent. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9": dict(aspect="9:16", resolution="4K", refs=["ref:plate-city", W, E],
        roles=STYLE + "Reference 2 is THE WOMAN. Reference 3 is THE GOLDEN EYE. ",
        prompt=f"{WORKSHOP} {framing('CU', 'slightly high angle', '85 mm, shallow focus', 'a craftsman presses gold leaf onto the small black half-ball to make her eye', 'patient, careful, tender')} "
               f"{cast('a craftsman (50s, grey-streaked beard, ochre tunic), seen as his two weathered hands in the lower-middle of the frame pressing a sheet of thin gold leaf onto a small black tar half-ball with a smooth bone tool', WOMAN +', sitting just behind him, soft and out of focus in the upper part of the frame, her head turned so her LEFT side faces away from us; she waits', extra='She appears ONCE only: there is exactly one woman in the picture, no second copy of her.')} "
               f"The half-ball is half covered in gold, half still black. Warm lamplight. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="The 5,000-Year-Old Golden Eye", format="short", dual_format=False, image_resolution="2K",
              loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s3: Matt's spectacles hang from the dig sieve behind the gloved hand")
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
