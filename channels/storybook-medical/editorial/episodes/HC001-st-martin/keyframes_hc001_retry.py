"""HC001 re-roll batch (one batch at the end, lessons from the first review applied to every prompt).
Lessons: (1) the style anchor shows the pilot's red-tuque voyageur, so the model inserts him: object/empty shots use a
people-free plate as the style reference and say NO PEOPLE; (2) square prompts drew framed borders: full-bleed;
(3) the porthole drifted to the shoulder/chest: anchor it to the lower LEFT abdomen; (4) clock hands are unreliable:
the watch is drawn without hands and Remotion animates them."""
import json
from pathlib import Path

P = Path("projects/hc001-window-into-his-stomach/episode.json")
ep = json.load(open(P, encoding="utf-8"))
KF = ep["keyframes"]

STYLE_ROOM = "ref:plate-study"          # people-free style reference (our own plate)
NOPEOPLE = ("NO PEOPLE anywhere in the frame: no figures, no faces, no hands unless stated. "
            "Reference 1 is a STYLE reference only: copy its painting style, never its contents.")
ANCHOR_NOTE = ("Reference 1 is a STYLE reference only: copy its painting style; do NOT copy or include the man in it, "
               "and no red tuque unless this prompt asks for Alexis.")
FULL = "Full-bleed image to every edge: no border, no frame, no white margin, no vignette card."
PORT = ("a small, clean, brass-rimmed round porthole set in the skin of the LOWER LEFT side of his abdomen, just below the ribs, "
        "like a neat illustrated window with soft warm shadow inside (NO blood, NO wound, NO organs)")
RULES = ("1820s frontier, nothing modern. The silk string is cream-white; glass vials hold amber liquid; no saturated red except "
         "Alexis's tuque when he is in the shot. Warm amber key light, teal shadows. No text, letters or watermark.")


def obj(prompt, refs=None, aspect="1:1", res="2K", extra_roles=""):
    return {"aspect": aspect, "resolution": res, "refs": [STYLE_ROOM] + (refs or []),
            "roles": "Reference 1 is a people-free room plate used for STYLE only. " + extra_roles,
            "prompt": f"{prompt} {NOPEOPLE} {FULL if aspect == '1:1' else ''} {RULES}"}


def fix_people(name, add):
    """Keep the original composition prompt, add the anchor warning and an explicit cast list."""
    k = KF[name]
    k["refs"] = [STYLE_ROOM if r == "kit:style-anchor.jpg" else r for r in k["refs"]]
    k["roles"] = ANCHOR_NOTE + " " + k["roles"].replace("Reference 1 is the style anchor (style only). ", "")
    k["prompt"] = k["prompt"] + " " + add


# ── wide masters ──
KF["M03"] = obj("Extreme wide shot of Mackinac Island at dawn, June 1822, from the water: the harbour plate's shingle beach, dock "
                "and log warehouses small in the lower third, chimney smoke, gulls, mist on the lake; Fort Mackinac on the bluff as "
                "whitewashed stone walls with wooden blockhouses (not a castle). The upper-centre sky is calm and empty for a title.",
                ["ref:plate-harbor"], aspect="16:9", res="4K", extra_roles="Reference 2 is the harbour plate (match its place).")
fix_people("M10", "CAST: exactly TWO people. Beaumont standing at the bedside and Alexis SITTING UP in the bed under the quilt with "
                  "his shirt open at the side for the dressing. There is NO third person and nobody lying under a sheet.")
KF["M13"]["refs"] = [STYLE_ROOM]
KF["M13"]["roles"] = "Reference 1 is a people-free room plate used for STYLE only."
KF["M13"]["prompt"] += (" CAST: exactly two elderly physicians in grey wigs and dark 1820s coats. NO tuques, no hats, no red "
                        "clothing, no young men.")
KF["M14"] = obj("Extreme wide shot of Fort Mackinac on its limestone bluff above the lake: whitewashed stone walls and wooden "
                "blockhouses, a flag, the village far below. On the wall walk in the left third, ONE tiny figure of an army surgeon "
                "in a dark-blue coat looking out. Afternoon light, huge sky.",
                ["ref:plate-harbor"], aspect="16:9", res="4K", extra_roles="Reference 2 is the island and fort.")
KF["M14"]["prompt"] = KF["M14"]["prompt"].replace("NO PEOPLE anywhere in the frame: no figures, no faces, no hands unless stated.",
                                                  "Only the ONE tiny surgeon figure; nobody else.")
KF["M17"] = obj("Close-medium shot of a corner of the study: a small cast-iron stove glowing, beside it a wooden rack of six glass "
                "vials filled with AMBER liquid, each with a small cube of meat inside, faint warm steam. A wooden shelf above the "
                "rack with stoneware jars and a folded cloth. Hidden detail: a small pair of round wire spectacles with amber-tinted "
                "lenses (exactly as in the glasses reference) folded on the shelf, half behind a jar, easy to miss.",
                ["kit:glasses-sheet.jpg"], aspect="16:9", res="4K", extra_roles="Reference 2 shows the spectacles' exact design.")
fix_people("M25", "CAST: Alexis in the right foreground, and in the background ONLY three ordinary soldiers in plain 1830s army "
                  "uniforms laughing among themselves. NO officer, nobody holding a bottle or vial, no doctor.")
KF["M29"] = obj("St. Louis at night, 1853: a dark wet cobbled street, a street-lamp glow, one lit upstairs window in the left third; "
                "through it, an empty desk chair and a cold lamp. Quiet, final.", aspect="16:9", res="4K")
KF["M31"] = obj("The log farmhouse from the farm plate at dusk, June 1880: deep blue sky, one window glowing warm, the rest dark, "
                "mist rising from the river, the house in the right third. Still.",
                ["ref:plate-farm"], aspect="16:9", res="4K", extra_roles="Reference 2 is the farm (same house).")
fix_people("M32", "CAST: ONLY Dr. Osler, alone in the room. Nobody else, no young man, no red tuque.")
KF["M32"]["refs"] = [STYLE_ROOM] + [r for r in KF["M32"]["refs"] if r != "kit:style-anchor.jpg"]
KF["M32"]["roles"] = "Reference 1 is a people-free room plate used for STYLE only. Reference 2 is DR. WILLIAM OSLER."
KF["M33"] = obj("The parish churchyard on a hot June afternoon, 1880: two farmers in plain shirtsleeves and straw hats (NO red, NO "
                "tuques) dig a deep grave beside the fence; only their shoulders and shovels show above a high mound of earth; "
                "heat haze, the white church in the left third, a tall shovel leaning on the fence. Respectful: no coffin, no body.",
                ["ref:plate-churchyard16"], aspect="16:9", res="4K", extra_roles="Reference 2 is the churchyard.")
KF["M33"]["prompt"] = KF["M33"]["prompt"].replace("NO PEOPLE anywhere in the frame: no figures, no faces, no hands unless stated.",
                                                  "Only the two diggers.")
KF["M34"] = obj("The same churchyard at evening: a fresh closed grave covered with wildflowers, a simple wooden cross, and a red "
                "knitted tuque hung on the fence post beside it. Golden light, peaceful, the church in the left third.",
                ["ref:plate-churchyard16"], aspect="16:9", res="4K", extra_roles="Reference 2 is the churchyard.")
KF["M34"]["prompt"] = KF["M34"]["prompt"].replace("no saturated red except Alexis's tuque when he is in the shot",
                                                  "the red tuque on the fence post is the only saturated red")

# ── inserts ──
KF["I02"] = {"aspect": "1:1", "resolution": "2K", "refs": [STYLE_ROOM, "projects/window-into-the-stomach/assets/images/sheet-alexis.png"],
             "roles": "Reference 1 is a people-free room plate (STYLE only). Reference 2 is ALEXIS (skin tone, linen shirt only).",
             "prompt": f"Extreme close-up of a young man's torso, framed from just below the chest to the hip, seen from the front: his "
                       f"linen shirt is lifted with one hand, showing {PORT}. From the top of the frame a small cube of beef on a "
                       f"cream-white silk string is being lowered toward the porthole. No face in frame. {FULL} {RULES}"}
KF["I03a"] = obj("Extreme close-up, square: an open brass pocket watch lying on a worn wooden table, the watch face has the 12 numerals "
                 "as simple marks but NO HANDS AT ALL (the clock hands will be added later), a centre pin only. Its chain trails off "
                 "frame. A coiled cream-white silk string beside it. The watch fills the centre 60% with even margins.")
KF["I05"] = obj("Extreme close-up: a hand in a dark-blue coat cuff lifts a cream-white silk string up through the frame; it is almost "
                "bare, only two small shrunken pieces of meat still tied to it and empty loops where the others were. Deadpan.")
KF["I05"]["prompt"] = KF["I05"]["prompt"].replace("no hands unless stated", "only the one hand stated")
KF["I06"] = obj("Extreme close-up of an 1820s flintlock musket lock on a wooden stock: the hammer snapping down, a bright spark "
                "leaping from the frizzen, a puff of white powder smoke. Dark background, warm spark light.")
KF["I08"] = {"aspect": "1:1", "resolution": "2K", "refs": [],
             "roles": "",
             "prompt": "Six food items laid out in a neat 3-by-2 grid on plain flat bone-white paper, each item alone in its own cell "
                       "with generous empty space around it, each tied with a short cream-white silk string and a small BLANK paper "
                       "tag: spiced braised beef, raw salted fat pork, raw salted lean beef, boiled salted beef, a piece of stale "
                       "bread, a slice of raw cabbage. NOTHING else on the paper: no bottles, no vials, no props. Even soft light, "
                       f"storybook gouache style with inked outlines. {FULL} No text."}
KF["I09"] = {"aspect": "1:1", "resolution": "2K", "refs": [STYLE_ROOM],
             "roles": "Reference 1 is a people-free room plate (STYLE only).",
             "prompt": f"Close-up of a young man's torso from below the chest to the hip, front view, shirt lifted, showing {PORT}; "
                       f"a small round white medicine pill falls toward it from above with a tiny motion trail. No face in frame. "
                       f"{FULL} {RULES}"}
KF["I10"] = obj("Extreme close-up of a glass vial of clear amber liquid on a wooden rack, a warm stove glow behind; inside, a small "
                "cube of meat with softened, dissolving edges and a few fine particles floating. Scientific, clean.")
KF["I11"] = obj("An open handwritten notebook from 1825 lying on a desk, seen from above at an angle: pages of dense ILLEGIBLE "
                "scribble-handwriting (no readable words), small neat sketches of a stomach and a pocket watch in the margins, a "
                "quill resting across it, lamp light.")
KF["I12"] = obj("A long wooden shelf packed with dozens of matching worn leather notebooks, some lying flat, an ink bottle and a "
                "candle at one end; the shelf runs left to right through the frame. No lettering on the spines.")
KF["I13"] = obj("An 1833 contract lying on a desk: a single sheet with lines of ILLEGIBLE copperplate scribble (no readable words), a "
                "brown wax seal, NO signature or mark at the bottom, a quill and inkwell beside it.")
KF["I14"] = obj("A leather purse spilling gold and silver coins on a polished committee table in London, 1840, beside a closed "
                "ledger and a quill. Warm candlelight.")
KF["I17"] = obj("A red knitted voyageur tuque hanging on an iron nail beside a weathered wooden cabin door, evening light across the "
                "grain of the wood. Simple and quiet.")
KF["I17"]["prompt"] = KF["I17"]["prompt"].replace("no saturated red except Alexis's tuque when he is in the shot",
                                                  "the tuque is the only saturated red")
KF["I19"] = {"aspect": "1:1", "resolution": "2K", "refs": [],
             "roles": "",
             "prompt": "Clean educational diagram in storybook gouache style on a soft bone-white background: a round brass porthole "
                       "ring set in a flat patch of pastel skin-toned surface, seen straight on; a soft pastel-pink fold of lining slides "
                       "halfway across the opening from one side like a little lid. Gentle and diagrammatic, NO blood, NO organs, "
                       f"no people, no hands. {FULL} No text."}
KF["I20"] = obj("Close-up of two round millstones grinding grain into flour, a little cloud of flour dust, wooden frame, warm light.")
KF["I22"] = {"aspect": "1:1", "resolution": "2K", "refs": ["projects/window-into-the-stomach/assets/images/plate-stomach.png"],
             "roles": "Reference 1 is the clean pastel stomach-interior style (match it).",
             "prompt": "Clean pastel educational view inside a stomach, like the reference: soft pink folds, a glowing pool of AMBER "
                       "gastric juice at the bottom in which a small cube of food is dissolving with tiny bubbles. NO people, NO hands, "
                       f"no string, NO blood. {FULL} No text."}

# the two extra watch images are no longer needed (Remotion draws the hands)
for k in ("I03b", "I03c"):
    KF.pop(k, None)

json.dump(ep, open(P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
RETRY = ["M03", "M10", "M13", "M14", "M17", "M25", "M29", "M31", "M32", "M33", "M34",
         "I02", "I03a", "I05", "I06", "I08", "I09", "I10", "I11", "I12", "I13", "I14", "I17", "I19", "I20", "I22"]
print(" ".join(RETRY))
