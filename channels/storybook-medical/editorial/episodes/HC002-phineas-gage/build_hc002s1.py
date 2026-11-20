"""HC002-S1 Gage: the image prompts (story v2 + storyboard v1, approved 2026-11-18; HERO pre-viz on stand-ins) into
projects/hc002-s1/episode.json "references" + "keyframes", then the prompt lint. Nothing is generated here.
Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/build_hc002s1.py
After the user approves the motion pre-viz AND these prompts on the approval page:
    episode.py refs hc002-s1 --batch          (sheets + set plate first: everything else takes them as references)
    episode.py refs hc002-s1 plate-s1 plate-s4 plate-s8 --batch, then the sprite / pose sheets (they take the plates)
    episode.py keyframes hc002-s1 --batch
    then fx_prep.py sheet ... -> assets/images/sprites/<name>/ (same names as the stand-ins), point edit_hc002s1.py at them.

Teaser rule: nothing after 1849 (no Chile, no portrait, no later life). Care: never the bar in a head, never a wound;
Gage is a silhouette in shot 1 and faces away in shot 8; after the accident a cloth bandage covers his left eye and crown.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (EMPTY_HANDS, FULL_BLEED, empty_plate, NO_TEXT, ONE_EACH, PERIOD, SAFE_FRAMING, camera, cast, crowd, framing, scale,  # noqa: E402
                        glasses_gag, lint_all, matt_beat, pose_sheet, set_block, sprite_sheet)

PID = "hc002-s1"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"
STYLE_PLATE = f"{HC1}/plate-study.png"           # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"          # HC001 model sheet: layout + style only

NARRATION = """[intense] In 1848, an iron bar shot straight through a man's skull.
[curious] Phineas Gage. Twenty-five. Railroad foreman. The best his bosses had.
His job: pack blasting powder into the rock with an iron bar. Thirteen pounds.
[quiet] His men caught his eye. He looked over his shoulder…
[fast] …and the iron struck the rock. A spark.
The bar went in under his cheekbone, behind his eye… and out the top of his head.
It landed about eighty feet away.
[pause] [whispers] Within minutes… he spoke.
[curious] He rode to his hotel sitting up in an ox cart.
The doctor remembered the greeting: "Doctor, here is business enough for you."
[warm] He survived. He even kept the iron. [pause] [whispers] But his friends said… he was "no longer Gage.\""""

# ── people ──────────────────────────────────────────────────────────────────────────────────────────────────────────
GAGE = ("PHINEAS GAGE in September 1848 (25; a strong, square-jawed young face, clean-shaven, thick dark hair, both eyes "
        "open and unhurt; a white work shirt with the sleeves rolled up, dark braces, dark wool trousers, work boots, a "
        "soft, wide-brimmed, low flat-crowned dark felt hat (a slouch hat of 1848: NOT a bowler or derby, NOT a top hat))")
GAGE_NOHAT = GAGE.split(", a soft, wide-brimmed")[0] + "; NO hat)"   # shots 1 and 8: the hat is its own sprite / gone
GAGE_AFTER = ("PHINEAS GAGE after the accident, 1848 (the same young man, 25, no hat: a clean white cloth bandage wrapped "
              "over the CROWN of his head and down diagonally over his own LEFT eye (L48: in a front view that is on the RIGHT "
              "side of the picture), so the top of his head and his left eye are covered; his right eye open; no blood, no wound visible anywhere; calm; the same white shirt and dark "
              "braces, and a short dark wool work jacket over them (NOT a long frock coat))")
TAMPING_IRON = ("tamping iron of 1848: a smooth, perfectly straight, round iron rod, about 3 ft 7 in long and thick as a "
                "thumb, dark grey with a dull sheen, tapering to a POINT at one end and blunt at the other (NOT a crowbar: "
                "no hook, no claw, no bend; NOT a drill or auger: no handle, no grip, no crossbar, no screw tip)")
CREW = [
    "a grey-bearded older driller in his fifties, broad and weathered, a battered straw hat",
    "a red-haired, freckled youth of about seventeen, thin, no hat",
    "a heavy, dark-moustached man in his thirties with a round face and a flat cap",
]

# ── sets (references: the photo of the cut, period ox carts) ─────────────────────────────────────────────────────────
CUT = set_block("The railroad rock cut near Cavendish, Vermont", "13 September 1848",
                "a fresh cut through grey schist rock with raw, layered walls and a rough ledge; drill holes; small wooden "
                "kegs of blasting powder (plain wood, no lettering); stacked rails and timber; wooded hills in early autumn colour beyond")
ROAD = set_block("A dirt road through fields near Cavendish, Vermont", "September 1848",
                 "a rutted dirt road between stubble fields and stone walls, maples just turning, a clapboard village ahead")
HOTEL = set_block("The front of a village hotel in Cavendish, Vermont", "September 1848",
                  "a two-storey white clapboard hotel with a covered wooden piazza (porch) along its front, wooden chairs, "
                  "a hitching rail, a dirt street")
ROOM = set_block("A plain rented room in a Vermont village", "1849", "bare plank walls, a narrow doorway, daylight")
STREET = set_block("A village street in Vermont", "1849", "clapboard houses, a doorway on a dirt street, grey daylight")

SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "
PHOTO = ("Reference 2 is a period photograph of the real Phineas Gage taken YEARS AFTER the accident (his left eye closed, "
         "holding his iron): paint THIS face (head shape, jaw, hair, brow, nose) in our storybook style, YOUNGER (25) and "
         "with BOTH EYES OPEN AND UNHURT, never as a photo, and do not copy the iron or the photograph's pose. ")
MATT = "kit:matt-sheet.jpg"
G, GA, CREW_REF, CUTP = "ref:sheet-gage-1848", "ref:sheet-gage-after", "ref:sheet-crew", "ref:plate-cut"
CUT_LOOK = ("Reference 1 is the rock cut's set plate, for the painting style, rock, light and palette ONLY: do NOT copy its "
            "composition or camera position. ")
STYLE_ONLY = ("Reference 1 is a people-free room plate from another film, for the painting style ONLY: never its room, "
              "composition or camera. ")
NOT_HERE = "{who} is NOT in this picture (he is animated in later as a separate cut-out): leave the place where he stands empty."

REFERENCES = {
    "sheet-gage-1848": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/gage_miller.jpg"], roles=SHEET + PHOTO,
        prompt=(f"Clean character model sheet on plain bone-white paper: {GAGE}. Front view, three-quarter view, profile "
                "view, back view, plus three head close-ups (confident, giving an order; concentrating, looking down; "
                "turning his head over his shoulder). Same scale in every view. No text, labels or watermark.")),
    # v2 (2026-11-18): v1's bandage missed the crown, one close-up showed both eyes, and he wore a frock coat. Reference 1 is
    # now the approved 1848 sheet (same face as the shots already made), with its layout.
    "sheet-gage-after": dict(aspect="16:9", refs=[G], roles=("Reference 1 is the model sheet of PHINEAS GAGE before the "
                             "accident: the same man, face, hair, build and layout; here he wears no hat and has the bandage. "),
        prompt=(f"Clean character model sheet on plain bone-white paper: {GAGE_AFTER}. Front view, three-quarter view, "
                "profile view from his RIGHT side, back view, plus two head close-ups (calm, a dry half smile; tired). "
                "In EVERY view and both close-ups the bandage covers the crown and his LEFT eye exactly the same way. "
                "Same scale in every view. No text, labels or watermark.")),
    "sheet-crew": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=("Clean character model sheet (a line-up) on plain bone-white paper: three different railroad workmen of 1848, standing "
                "side by side, full figure, front view: " + "; ".join(f"({i}) {c}" for i, c in enumerate(CREW, 1)) +
                ". Shirts with rolled sleeves, braces, wool trousers, boots. Each has a clearly different face, age, build "
                "and hair; no look-alikes. No text, labels or watermark.")),
    "plate-cut": dict(aspect="9:16", refs=[STYLE_PLATE, "proj:refs/cavendish_cut.jpg"],
        roles=(STYLE_ONLY + "Reference 2 is a modern photograph of the real cut, used ONLY for the rock: grey layered "
               "schist walls; ignore the modern trees, rails and road. "),
        prompt=(f"{CUT} Vertical frame along the floor of the cut toward the open end, rock walls rising on both sides. "
                f"EMPTY LOCATION PLATE: no people. Three clear depth layers. {PERIOD} {NO_TEXT}")),
}

# ── HERO pieces (layered: the plate is empty of what moves; the sheets hold exactly the poses the keys use) ──────────
REFERENCES.update({
    "plate-s1": dict(aspect="9:16", refs=[CUTP], roles=CUT_LOOK, set="cut",
        prompt=(f"{CUT} {framing('LS', 'very low angle from the floor of the cut', '24 mm', 'a blast has just gone off: grey-brown smoke and dust billow up from a drill hole low in the frame', 'violent, sudden')} "
                f"{camera('on the floor of the cut, low, near the blast hole', 'up and along the cut toward a pale September sky', 'the two rock walls rising on the left and right and the pale sky between them filling the upper half')} "
                "Two crewmen duck at the far left and right edges, arms over their heads, seen from behind. The upper half "
                "of the frame is open pale sky (the iron bar and the hook card are added there later). "
                + NOT_HERE.format(who="Phineas Gage") + " No iron bar, no hat in the air. "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "plate-s4": dict(aspect="9:16", refs=[CUTP, CREW_REF], roles=CUT_LOOK + "Reference 2 is the crew (only the two backs). ",
        set="cut", prompt=(
            f"{CUT} {framing('OTS', 'eye level', '50 mm, shallow focus', 'two of his men in the pit look up toward the ledge', 'a normal working moment, about to go wrong')} "
            f"{camera('in the pit behind two crewmen', 'up toward the rock ledge', 'the ledge with a drill hole and a powder keg on it, the wooded hills and sky behind')} "
            "Two crewmen in the foreground, seen from behind (backs, hats and shoulders, soft focus), at the left and right "
            "edges. On the ledge in the middle distance: the drill hole, a small keg, nothing else. "
            + NOT_HERE.format(who="Phineas Gage") + f" {ONE_EACH} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # v4 (user 2026-11-18: "remake the plate as planned: ground-level MS, his hand + shoulder large in the foreground, face
    # turned away; the light shafts are good: keep them"). v3 painted a man's hand (the prompt named it, L47) and copied the
    # v2 plate's wide camera (it was the whole reference): v4 takes only a DETAIL crop of v2 (rock, smoke, light shafts).
    # no framing() here: its 'waist up' / 'faces' wording invites a person into an empty plate (L47)
    "plate-s8": dict(aspect="9:16", refs=["proj:refs/s8_light_detail.png"],
        roles=("Reference 1 is a small DETAIL of our rock cut: copy ONLY its painting style, the grey layered rock, the "
               "settling smoke and the slanting shafts of daylight. It is not a camera or a composition. "), set="cut",
        prompt=(f"{CUT} SHOT: ground-level view, the camera lies ON the rock floor, 35 mm, shallow focus; stunned silence after a blast. "
                f"{camera('on the rock floor itself, the lens a few inches above the ground', 'along the floor toward the foot of the rock wall', 'the foot of a grey layered rock wall a few yards away, settling smoke, shafts of daylight from the upper LEFT')} "
                "The rock floor is seen almost edge-on: big out-of-focus pebbles and grit right at the bottom edge, the bare "
                "floor rising in steep perspective through the whole lower half of the frame to the foot of a grey layered rock "
                "wall a few yards away, which fills the upper half; settling grey smoke drifts over the floor, and shafts of "
                "daylight slant down through it from the upper LEFT. The near foreground is bare, clear rock floor. "
                "EMPTY LOCATION PLATE: no people, no hands, no bodies, no clothes, no tools anywhere. No blood. "
                f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "sprite-iron": dict(aspect="16:9", refs=[SHEET_LAYOUT],
        roles="Reference 1 is our model-sheet layout and painting style ONLY: do not copy the person on it. ",
        prompt=sprite_sheet(TAMPING_IRON, ["lying straight and level, side view, the POINT to the RIGHT",
                                           "the same, a little foreshortened as if turning toward the viewer"],
                            "s1: a blast in a rock cut under a pale sky", "soft daylight from the upper LEFT",
                            "from the side, level", "Each rod is about four fifths of the picture's width.")),
    "sprite-hat": dict(aspect="16:9", refs=[SHEET_LAYOUT],   # v2: not the Gage sheet (v1 printed it underneath, L45)
        roles="Reference 1 is our model-sheet layout and painting style ONLY: do not copy the person on it. ",
        prompt=sprite_sheet("soft, wide-brimmed, low flat-crowned dark felt slouch hat of 1848 (NOT a bowler or derby)", ["seen from the side", "seen from below, tumbling"],
                            "s1: a blast in a rock cut under a pale sky", "soft daylight from the upper LEFT",
                            "from the side and below")),
    "pose-gage-s1": dict(aspect="16:9", refs=[G],
        roles="Reference 1 is PHINEAS GAGE (his build and clothes only: this shot shows him as a dark silhouette). ",
        prompt=pose_sheet(GAGE_NOHAT,
                          ["standing braced over a drill hole, legs apart, leaning forward, at the moment of the blast. "
                           + EMPTY_HANDS + " His hands are low in front of him",
                           "thrown backward by the blast, arms flung up, back arched. " + EMPTY_HANDS],
                          "s1: a blast in a rock cut, the sky behind him", "strong back light from the pale sky: he is "
                          "almost a dark silhouette against it, a thin light rim on his edges", "from low in front, the "
                          "whole figure, feet at the bottom of each drawing")),
    "pose-gage-s4": dict(aspect="16:9", refs=[G],
        roles="Reference 1 is PHINEAS GAGE (face, hair, clothes). ",
        prompt=pose_sheet(GAGE, [f"standing three-quarter to the viewer's left, both hands resting on the top (blunt) end of the "
                                 f"{TAMPING_IRON}, which stands upright, point down, at his feet; his eyes down on it",
                                 "EXACTLY the same stance, body angle, hands and iron as drawing (1); ONLY his head turns over "
                                 "his RIGHT shoulder toward the viewer, eyes on his men"],
                          "s4: the ledge seen from the pit", "daylight from the upper LEFT",
                          "from slightly below, a little to his right", "from the knees up")),
    # v4 (2026-11-18): close, for the ground-level MS plate: his right shoulder and hand LARGE in the foreground. No sheet
    # reference (L45b); the face is never seen.
    "pose-gage-s8": dict(aspect="16:9", refs=[], roles="",
        prompt=pose_sheet(GAGE_NOHAT[:-1] + ", his hair grey with dust)",
                          ["lying on his back on the ground, still: his right shoulder and upper arm nearest to the viewer, "
                           "his right hand lying open, palm up, closest of all; beyond the shoulder his head is turned AWAY "
                           "from the viewer, so only the back of his head and his dusty hair show, never his face or profile",
                           "EXACTLY the same, only the fingers of his right hand curling",
                           "the same man pushing up on his right elbow: the shoulder rising toward the viewer, his head lifting, "
                           "still turned away"],
                          "s8: the rock floor in settling smoke, camera on the ground",
                          "soft grey daylight from the upper LEFT through smoke",
                          "from ground level at his right side, close to his right shoulder; his face is never seen; no blood, no wound",
                          "his head, shoulders, chest and right arm with the hand, the body cut off straight at the waist, "
                          "the same size in all three")),
})

# ── ALIVE pieces v2 (user 2026-11-20: "do the few generate to make it better"; L53: nothing cut out of a still moves) ──
# Each moving person is GENERATED on green (a pose sheet with exactly the poses the keys swap between) and each plate
# is the approved still WITHOUT that person (empty_plate). 2a needs no plate: its soft cliff (mcu2a_hc002s1.py) is
# already empty. Reference 1 = the approved shot, for identity, size and light only.
SHOT_ID = ("Reference 1 is the approved shot this person is animated into: copy {who} EXACTLY (face, hair, hat, clothes, "
           "build, painting style and light) but NOTHING else of the picture: not its background, not the other people, "
           "not its frame. ")
REFERENCES.update({
    # 2a "Phineas Gage. Twenty-five. Railroad foreman.": a wave (pose 1 -> 2 -> 1 -> 3 -> 1) on the mirrored MCU.
    "pose-gage-s2a": dict(aspect="16:9", refs=["kf:s2a-dof-mirror"], roles=SHOT_ID.format(who="PHINEAS GAGE (the man)"),
        prompt=pose_sheet(GAGE, ["his RIGHT arm raised high (on the LEFT side of each drawing), elbow bent, the open palm "
                                 "toward the viewer, fingers together; his left arm down at his side; looking up and off to "
                                 "the left, confident",
                                 "EXACTLY the same as drawing (1); ONLY the raised forearm and hand tilt outward, away from "
                                 "his head (the first half of a wave)",
                                 "EXACTLY the same as drawing (1); ONLY the raised forearm and hand tilt inward, toward his "
                                 "hat (the other half of the wave)"],
                          "2a: a medium close-up below a sunlit rock cut, the cliff soft behind him",
                          "warm morning daylight as in reference 1", "from slightly below, straight on, as in reference 1",
                          "from the top of his hat down to his belt, the raised hand included")),
    # 2b "The best his bosses had.": the moustached driller (lower right) swings his sledge: up, strike, up, strike.
    "plate-s2b-empty": dict(aspect="9:16", refs=["kf:s2b"], roles="",
        prompt=empty_plate("the high wide view of the rock cut with Gage on the ledge, the contractor, and the crew below",
                           "the heavy dark-moustached driller in the flat cap with the sledgehammer, lower right",
                           "the grey rock floor of the cut and the stacked timber and rails behind where he stood")),
    "pose-crew-s2b": dict(aspect="16:9", refs=["kf:s2b"],
        roles=SHOT_ID.format(who="the heavy dark-moustached driller in the flat cap (lower right)"),
        prompt=pose_sheet(CREW[2] + ", a white work shirt with rolled sleeves, dark braces, dark wool trousers, boots",
                          ["the sledgehammer raised high over his RIGHT shoulder, both hands on the long handle, about to swing",
                           "the sledgehammer swung down: its head at the ground in front of his feet, arms straight, "
                           "knees bent, the strike"],
                          "2b: a rock cut seen from high on the hillside", "soft daylight from the upper LEFT",
                          "from high above and a little in front, as in reference 1",
                          "the whole figure with the whole hammer, feet at the bottom of each drawing")),
    # 10 "Doctor, here is business enough for you.": Gage, seated, raises his hand in greeting (pose 1 -> 2 <-> 3).
    "plate-s10-empty": dict(aspect="9:16", refs=["kf:s10"], roles="",
        prompt=empty_plate("the hotel piazza seen from the street behind the doctor, with Matt leaning on the post",
                           "the bandaged young man sitting in the wooden chair on the piazza",
                           "the same empty wooden chair, the white clapboard wall and the window behind it")),
    "pose-gage-s10": dict(aspect="16:9", refs=["kf:s10", GA],
        roles=SHOT_ID.format(who="PHINEAS GAGE (the bandaged man in the chair)") + "Reference 2 is his model sheet (identity only). ",
        prompt=pose_sheet(GAGE_AFTER, ["sitting at ease, legs crossed, both hands resting on his knee, calm",
                                       "EXACTLY the same; ONLY his RIGHT hand raised beside his head in greeting, the open palm toward the viewer",
                                       "EXACTLY the same as drawing (2); ONLY the raised hand tilted a little outward (a small wave)"],
                          "10: a hotel piazza in late daylight", "warm late daylight from the LEFT",
                          "from the street, slightly below, three-quarter toward the viewer's left, as in reference 1",
                          "the whole seated figure (the chair is NOT drawn: he sits on nothing), the same size in all three")),
    # 12 "But his friends said… he was no longer Gage.": the bearded friend leans in to whisper on "said".
    "plate-s12-empty": dict(aspect="9:16", refs=["kf:s12"], roles="",
        prompt=empty_plate("two friends in a doorway, the street with Phineas Gage walking away behind them",
                           "the lanky bearded friend in the cap (left of centre, in front)",
                           "the stout friend in the brown waistcoat, whole and unchanged, the dark figures in the doorway "
                           "behind, the door frame and the street")),
    "pose-friend-s12": dict(aspect="9:16", refs=["kf:s12"],
        roles=SHOT_ID.format(who="the lanky bearded friend in the cap (left of centre)"),
        prompt=pose_sheet("a lanky man of about thirty with a short brown beard, a flat cap and a worn olive work jacket",
                          ["standing upright, turned three-quarter to the right, hands down, glancing back over his "
                           "shoulder toward the viewer, uneasy",
                           "leaning in to the right, his head tilted, his left hand cupped beside his mouth as if "
                           "whispering into a friend's ear, eyes sliding sideways"],
                          "12: a doorway on a grey village street", "soft grey daylight from the LEFT",
                          "eye level, as in reference 1", "from the cap down to the knees, the same size in both")),
})

# ── the story stills ─────────────────────────────────────────────────────────────────────────────────────────────────
ONE = ONE_EACH
KEYFRAMES = {
    "s2a": dict(aspect="9:16", refs=[CUTP, G], set="cut",
        roles=CUT_LOOK + "Reference 2 is PHINEAS GAGE (face, hair, clothes). ",
        prompt=(f"{CUT} {framing('MS', 'low angle', '35 mm', 'the foreman signals his crew, one arm raised, the iron bar in his other hand', 'confident, in charge, morning energy')} "
                f"{camera('below the ledge', 'up at him', 'the rock wall and early autumn trees against a bright morning sky')} "
                f"{cast(GAGE)} {ONE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s2b": dict(aspect="9:16", refs=[CUTP, G, CREW_REF], set="cut",
        roles=CUT_LOOK + "Reference 2 is PHINEAS GAGE. Reference 3 is the crew (three different men). ",
        prompt=(f"{CUT} {framing('LS', 'high angle from the hillside', '28 mm', 'the crew swing sledgehammers on drills in the cut below while Gage on the rim waves them on', 'busy, proud work')} "
                f"{camera('on the wooded hillside above the cut', 'down into it', 'the raw cut through the autumn hills, stacked rails beside it')} "
                + crowd("the cut below", CREW + ["a contractor of 1848 in a top hat and frock coat with mutton-chop whiskers, "
                        "a ledger under his arm, standing on the bank and nodding toward Gage"]) +
                f" Phineas Gage stands small on the rim. {ONE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s3": dict(aspect="9:16", refs=[CUTP], set="cut", roles=CUT_LOOK,
        # user 2026-11-19 (scale, L51): v1 had a toy-sized keg beside the hand and a hole too small for it; the keg was
        # painted out (keg_out_hc002s1.py). If s3 is ever regenerated, this prompt states every size against the hand.
        prompt=(f"{CUT} {framing('INSERT', 'three-quarter top view', '50 mm', 'a hand tips a fist-sized powder flask over a drill hole in the rock, black grains pouring in', 'careful, routine, dangerous')} "
                f"{camera('just above the drill hole', 'down at it', 'grey rock around the hole, no keg or barrel anywhere near the hand')} "
                + scale({"the powder flask": "about the size of his fist (a pear-shaped leather-and-brass flask)",
                         "the drill hole": "about 2 in (5 cm) across, a little wider than two fingers side by side",
                         "any powder keg": "about twice the hand's height (none in this picture)"}) +
                " Only one hand and cuff are in the picture, no person. No iron bar in the picture (it is animated in later). "
                f"{FULL_BLEED} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s5": dict(aspect="9:16", refs=[CUTP], set="cut", roles=CUT_LOOK,
        prompt=(f"{CUT} {framing('ECU', 'low', '100 mm macro', 'the lip of a drill hole in grey rock, dark powder grains around it, waiting', 'the second before disaster')} "
                f"{camera('at the rock surface', 'along it to the hole', 'out-of-focus rock and dust')} "
                "No iron bar, no hand, no spark in the picture (they are animated in later). "
                f"{FULL_BLEED} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s7": dict(aspect="9:16", refs=[STYLE_PLATE], roles=STYLE_ONLY,
        prompt=(f"{CUT.replace('The railroad rock cut', 'The grassy slope beyond the rock cut')} "
                f"{framing('LS', 'eye level', '35 mm', 'far down a grassy slope two crewmen start running toward the camera', 'alarm')} "
                f"{camera('on the grassy slope', 'back toward the cut', 'grass, a stone wall and the mouth of the cut far behind, small')} "
                "The middle ground is open grass (an iron bar lands there, animated later). "
                + crowd("far away on the slope", CREW[:2]) + f" {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s9": dict(aspect="9:16", refs=[STYLE_PLATE, GA, CREW_REF, "proj:refs/ox_carts_1850s.jpg"],
        roles=(STYLE_ONLY + "Reference 2 is PHINEAS GAGE after the accident (bandage over the LEFT eye). Reference 3 is "
               "the crew. Reference 4 is a period photograph used ONLY for the cart and oxen. "),
        prompt=(f"{ROAD} {framing('LS', 'eye level', '35 mm', 'two oxen pull a wooden cart left to right; Gage sits UPRIGHT in it, a cloth pressed to his bandaged head; his men walk beside it', 'stunned, strangely calm')} "
                f"{camera('at the side of the road', 'across it', 'stubble fields, a stone wall and maples')} "
                + crowd("walking beside the cart", CREW[:2]) + f" {ONE} No blood. {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s10": dict(aspect="9:16", refs=[STYLE_PLATE, GA, MATT],
        roles=(STYLE_ONLY + "Reference 2 is PHINEAS GAGE after the accident. Reference 3 is MATT: copy his face, amber "
               "round spectacles, teal scarf and amber notebook only; his clothes are of 1848. "),
        prompt=(f"{HOTEL} {framing('MS', 'eye level', '35 mm', 'Gage, sitting calmly in a wooden chair on the piazza, legs crossed, raises one hand in greeting to a doctor stepping down from his carriage', 'deadpan, absurdly calm')} "
                f"{camera('in the street behind the doctor', 'toward the piazza', 'the white clapboard hotel front and its piazza')} "
                f"{cast(GAGE_AFTER, 'DR. EDWARD WILLIAMS, seen only from behind in the foreground: tall hat, dark coat, a leather medical bag', 'MATT')} "
                f"{matt_beat('a brown waistcoat and a low felt hat of 1848', 'leaning on the piazza post behind Gage, pencil frozen over his notebook, jaw dropped')} "
                f"{ONE} No blood. {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    # v2 (2026-11-18): v1 drew TWO crossing rods, and its 16:9 version copied the HC001 study (shelves, lamp, quill, test
    # tubes) from the style plate: the Gage sheet is now the style + sleeve reference, the room is spelled out bare.
    "s11": dict(aspect="9:16", refs=[G], roles=("Reference 1 is PHINEAS GAGE: copy ONLY the painting style and his white "
                                               "shirt sleeve, rolled up; only his hand and forearm are in this picture. "),
        prompt=(f"{ROOM} {framing('CU', 'eye level', '85 mm', f'a young man’s hand grips the {TAMPING_IRON} leaning in the corner by a doorway', 'quiet, possessive')} "
                f"{camera('close to the door frame', 'into the corner', 'bare plank wall in soft daylight')} "
                + scale({"the iron rod": "1 1/4 in (3 cm) thick, about two fingers wide, so the fist closes round it with "
                                         "the fingertips just meeting the thumb"}) +
                " Exactly ONE iron rod in the whole picture. The room is bare: plank walls and a plank floor only; no "
                "furniture, no shelves, no books, no bottles, no lamp, no stove. "
                f"Only the hand and its rolled white shirt sleeve are in the picture, no face. {ONE_EACH} "
                f"{glasses_gag('hanging by one arm from a nail on the plank wall above the iron')} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
    "s12": dict(aspect="9:16", refs=[STYLE_PLATE, GA],
        roles=STYLE_ONLY + "Reference 2 is PHINEAS GAGE after the accident (small, out of focus). ",
        prompt=(f"{STREET} {framing('MS', 'eye level', '50 mm', 'two friends whisper in a doorway and one glances back over his shoulder at the street', 'uneasy, unsure of him')} "
                f"{camera('just outside the doorway', 'past the two friends into the street', 'the dirt street where Phineas Gage, small and out of focus, walks away')} "
                + crowd("in the doorway", ["a lanky man of about thirty with a short brown beard and a cap",
                                           "a stout clean-shaven man of about forty-five in a waistcoat"]) +
                f" {ONE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}")),
}


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(image_resolution="2K", references=REFERENCES, keyframes=KEYFRAMES,
              previz_approved=("2026-11-18: user approved the HERO shots v6 (1 as is; 4 + 8 with fixes) and said go "
                               "ahead with the 9 story stills + 16:9 and the bandaged-Gage sheet redo"),
              glasses="s11: Matt's spectacles hanging from a nail above the iron",
              theme={"culture": "new-england-1840s (proposed)", "font": "montserrat"},
              storyboard="2026-11-18: s1-storyboard-v1.md; HERO pre-viz on stand-ins (previz_hc002s1.py, edit_hc002s1.py)")
    ep["narration"]["v3_text"] = NARRATION
    # theme new-england-1840s (approved 2026-11-18): fiddle, banjo drone, low drum; 2 candidates, no vocals
    ep["music"] = {**ep.get("music", {}), "lufs": ep.get("music", {}).get("lufs", -22),
                   "selected": "m2", "prompts": {   # m2 46.1 s covers the Short; m1 is 37.2 s
        "m1": {"sections": 2, "prompt": ("Instrumental, rural Vermont 1848: a solo fiddle playing a slow, haunting old-time air "
               "in a minor key over a low open-string banjo drone and a soft frame drum like a distant heartbeat; tense and "
               "curious, a stunned hush in the middle, then a quiet, wondering close. No vocals, no modern drums, no synths.")},
        "m2": {"sections": 2, "prompt": ("Instrumental, New England 1840s old-time music: clawhammer banjo picking a tense, "
               "repeating figure, a fiddle answering with long mournful notes, a low bass drum on every other bar; builds "
               "unease, then a hushed, eerie ending. No vocals, no synths, no modern drums.")}}}
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
