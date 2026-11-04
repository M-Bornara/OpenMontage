"""HC001 keyframe prompts (shot-plan.md section A-D). Writes them into the production project's episode.json.
Run from the repo root: python channels/storybook-medical/editorial/episodes/HC001-st-martin/keyframes_hc001.py"""
import json
from pathlib import Path

P = Path("projects/hc001-window-into-his-stomach/episode.json")
W = "projects/window-into-the-stomach/assets/images/"          # pilot sheets/plates
E2 = "projects/human-test-tube/assets/images/refs/"             # ep-2 sheets/plates
STYLE = "kit:style-anchor.jpg"
A, AO, B, FAM, OSL = W + "sheet-alexis.png", W + "sheet-alexis-old.png", W + "sheet-beaumont.png", E2 + "sheet-young-family.png", "ref:sheet-osler"

ALEX = "ALEXIS (young French-Canadian voyageur: same face and dark hair as his sheet, red knitted tuque, loose linen shirt, woven arrow sash)"
ALEX40 = "ALEXIS in his forties (same face as his young sheet, a little weathered, short beard, red tuque, farmer's waistcoat)"
ALEXOLD = "OLD ALEXIS (same face as his later-life sheet: white hair and beard, red tuque, brown waistcoat, sash)"
BEAU = "DR. WILLIAM BEAUMONT (same face and hair as his sheet, dark-blue 1820s army surgeon's coat with a brass watch chain always visible)"
BEAU_CIV = "DR. WILLIAM BEAUMONT, older (same face as his sheet, greying, civilian black frock coat, brass watch chain)"
PORT = ("a small, clean, brass-rimmed round porthole set in the skin of his LEFT side, like a neat illustrated window with soft warm "
        "shadow inside (NO blood, NO wound, NO organs)")
M = ("Wide cinematic 16:9 frame composed on thirds: each person complete and readable inside their own vertical third, generous "
     "headroom, three depth layers (foreground, midground, background), no key detail at the extreme left or right edge.")
I = ("Square frame, close-up: the subject fills the centre 60% of the frame with even margins on every side, so it can be framed "
     "both wide and tall.")
T = ("Vertical 9:16 frame: faces and key objects stay out of the bottom 22% and the right 12% (phone interface), and out of the top 10%.")
RULES = ("Beaumont is always on the LEFT, Alexis on the RIGHT. Alexis's red tuque is the only saturated red in the frame; the silk string "
         "is cream-white; glass vials hold amber liquid. 1820s frontier: nothing modern. Warm amber key light, teal shadows.")
GLASSES = ("Hidden detail: a small pair of round wire spectacles with amber-tinted lenses (exactly as in the glasses reference) resting "
           "{where}, small, at the edge of the frame, easy to miss.")


def roles(*names):
    return ("Reference 1 is the style anchor (style only). " +
            " ".join(f"Reference {i + 2} is {n}." for i, n in enumerate(names)))


def m(refs, role_names, prompt, res="4K"):
    return {"aspect": "16:9", "resolution": res, "refs": [STYLE] + refs, "roles": roles(*role_names),
            "prompt": f"{M} {prompt} {RULES}"}


def ins(refs, role_names, prompt):
    return {"aspect": "1:1", "resolution": "2K", "refs": [STYLE] + refs, "roles": roles(*role_names), "prompt": f"{I} {prompt} {RULES}"}


def tall(refs, role_names, prompt):
    return {"aspect": "9:16", "resolution": "2K", "refs": [STYLE] + refs, "roles": roles(*role_names), "prompt": f"{T} {prompt} {RULES}"}


KF = {
    # ── masters (4K) ──
    "M02": m([A, B, "ref:plate-study"], ["ALEXIS", "BEAUMONT", "the study room"],
             f"Fort Mackinac 1825, daylight. RIGHT THIRD: {ALEX} has just stood up and walks toward the open door on the right carrying a big "
             f"armful of firewood, tucking his shirt down. LEFT THIRD: {BEAU} sits at the table with his notebook open, watching him go with "
             "fascination, pocket watch open on the table."),
    "M03": m(["ref:plate-harbor"], ["the Mackinac harbour plate"],
             "Extreme wide shot of Mackinac Island at dawn, June 1822, recomposed from the harbour plate with life added: smoke from "
             "chimneys, a few tiny figures on the dock, gulls, mist on the lake; Fort Mackinac on the bluff drawn as whitewashed stone walls "
             "with wooden blockhouses (not a castle). Leave the sky in the upper-centre calm for a title."),
    "M04": m(["ref:plate-harbor", A, "kit:matt-eras.jpg"], ["the harbour plate", "ALEXIS", "MATT (use only the 1820s voyageur outfit, teal scarf, amber notebook)"],
             "Wide shot: a brigade of four large birch-bark freight canoes arriving at the Mackinac dock in morning light, voyageurs in red "
             "tuques and woven sashes paddling in rhythm, spray, fur bales in the canoes; Alexis paddling in the lead canoe (right third). "
             "Cameo, very small, far back in the LAST canoe on the left: MATT in his 1820s voyageur outfit with the teal scarf, writing in a "
             "small amber notebook instead of paddling, face half under his hat brim. He must not draw attention.",),
    "M05": m([A, "ref:plate-harbor"], ["ALEXIS", "the harbour"],
             f"Medium shot on the dock: {ALEX} laughing with two fellow voyageurs (generic, no red hats on them: brown and blue caps), "
             "sharing bread, canoes behind them, morning light. Alexis in the right third, friends left and centre."),
    "M07": m([B, "ref:plate-harbor"], ["BEAUMONT", "the island and fort"],
             f"{BEAU} running down a steep dirt path from the white fort on the bluff toward the village below, medical bag in hand, coat "
             "flapping, urgent. He is in the left third, the path curving to the right, the village roofs and lake in the background."),
    "M08": m([B, A, "ref:plate-store16"], ["BEAUMONT", "ALEXIS (only as a shape under a blanket)", "the store interior"],
             f"Inside the fur-company store, moments after an accident: {BEAU} kneels on the floor in the left third beside a man lying "
             "under a grey wool blanket (only the blanket shape and a red tuque on the floor are visible, no injury shown), lantern light "
             "on Beaumont's face, intense concentration. In the background, silent voyageurs and a clerk stand holding their hats, a "
             "musket leaning against the counter with a wisp of smoke. No blood anywhere."),
    "M09": m([A, "ref:plate-sickroom16"], ["ALEXIS", "the sickroom"],
             f"The sickroom at night, 1822: {ALEX} (without the tuque, it hangs on the bedpost) lies in the bed in the right third, "
             "pale, bandages wrapped around his chest under the quilt, eyes closed, a candle on the table, the window on the left dark "
             "blue. Calm, quiet, alive."),
    "M10": m([A, B, "ref:plate-sickroom16"], ["ALEXIS", "BEAUMONT", "the sickroom"],
             f"Same sickroom by day: {BEAU} in the left third carefully changing the bandage at Alexis's side (only clean white linen "
             "visible), a basin and folded cloths on the table; Alexis sitting up in bed in the right third; through the window on the "
             "left, autumn leaves falling (the seasons are passing)."),
    "M11": m([A, B, "ref:plate-sickroom16"], ["ALEXIS", "BEAUMONT", "the sickroom"],
             f"Low camera angle. {BEAU} in the left third holds a small tray with a curved needle and thread toward the bed. {ALEX}, "
             "sitting up in bed in the right third, turns his head firmly away and raises a hand: a clear, calm NO. Low angle gives Alexis "
             "dignity and power. Candle light."),
    "M12": m([B, "ref:plate-study"], ["BEAUMONT", "the study"],
             f"Night, the study: {BEAU} alone at his desk in the left third, oil lamp, an open notebook, slowly looking up from his "
             "writing with the expression of a man who has just realised something enormous. The door on the right with light under it. "
             "Deep teal shadows, half his face in shadow."),
    "M13": m(["ref:plate-study"], ["the study (style of the room only)"],
             "Comedy tableau, 1820s: two elderly physicians in powdered-wig-era coats sit at opposite ends of a long table piled with "
             "medical books, glaring at each other across it, one with a tiny model millstone, the other with a wilted pear on a plate. "
             "Deadpan, symmetrical-ish, each man in his own third."),
    "M14": m(["ref:plate-harbor", B], ["the island and fort", "BEAUMONT (tiny)"],
             "Extreme wide shot of Fort Mackinac on its limestone bluff above the lake: whitewashed stone walls and wooden blockhouses, "
             "a flag, the village far below. A tiny figure of Beaumont stands on the wall walk in the left third looking out. Afternoon "
             "light, huge sky."),
    "M15": m([A, B, E2 + "plate-fort-yard.png"], ["ALEXIS", "BEAUMONT", "the fort yard"],
             f"The back yard of the officer's log house inside the fort, late afternoon: {ALEX} splits kindling on a chopping block in "
             f"the right third, axe raised; {BEAU} watches from the open doorway in the left third, notebook in hand. Woodpile, chickens."),
    "M16": m([A, B, "ref:plate-study"], ["ALEXIS", "BEAUMONT", "the study"],
             f"Deadpan comedy frame, the study by day: {BEAU} at the desk in the left third writing happily and quickly in his notebook, "
             f"pleased with himself; in the right third, {ALEX} sits on a stool looking pale and unwell, hand pressed to his side, "
             "staring at the doctor. The room is perfectly still, a clock on the wall."),
    "M17": m(["ref:plate-study", "kit:glasses-sheet.jpg"], ["the study", "Matt's spectacles (exact design)"],
             "Close-medium shot of the study's corner: a small cast-iron stove glowing, beside it a wooden rack of six glass vials filled "
             "with AMBER liquid, each with a small cube of meat inside, a faint warm steam. A shelf above the rack with jars and a folded "
             "cloth. " + GLASSES.format(where="folded on the shelf above the rack, half behind a jar")),
    "M18": m([A, B, "ref:plate-study"], ["ALEXIS", "BEAUMONT", "the study"],
             f"The study: in the right third, {ALEX} stands with arms folded, glaring with impatience at the rack of amber vials by the "
             f"stove; in the left third, {BEAU} writes the word in his notebook without looking up. Comic tension, still frame."),
    "M19": m(["ref:plate-study", A], ["the study", "ALEXIS (only his tuque)"],
             "The study, empty: a wooden chair beside the open door, the door swinging slightly, daylight and the lake outside; on the "
             "chair, nothing. On the floor, a few wood chips. Beaumont's notebook open on the desk in the left foreground. Absence."),
    "M20": m([FAM, A], ["the young family (wife and two small children)", "ALEXIS"],
             f"Warm summer evening in Lower Canada, 1828: {ALEX} with his wife and two small children outside a small log cabin, the "
             "wife holding a baby, a toddler at Alexis's knee, a freight canoe pulled up by the river behind. Happy, warm, ordinary life. "
             "Alexis right third, wife centre-left."),
    "M21": m([FAM, A], ["the family", "ALEXIS"],
             "Extreme wide shot: a single birch-bark canoe very small on a vast river under a huge sky, travelling from RIGHT to LEFT, "
             "Alexis paddling at the stern, his wife and two children in the middle with bundles, a kettle and a cradle. Forested shores, "
             "cool travel blues, the canoe in the right third heading left."),
    "M22": m([A], ["ALEXIS"],
             f"A quiet French-Canadian village street in summer 1832 during a cholera epidemic: shutters closed, an empty cart, a "
             f"lantern still burning in daylight; {ALEX} stands in his own doorway in the right third, watchful, alive. Sombre, no bodies."),
    "M23": m([A, "ref:plate-washington"], ["ALEXIS", "the Washington corridor"],
             f"The War Department corridor, Washington, 1833: {ALEX} (no tuque here, it sticks out of his pocket) stands in an "
             "ill-fitting army sergeant's uniform that is slightly too big, looking down at himself, a little out of place; clerks pass "
             "in the background. He stands in the right third."),
    "M24": m([A, B, "ref:plate-washington"], ["ALEXIS", "BEAUMONT (civilian clothes)", "the corridor office"],
             f"A small office off the corridor, 1833: on the desk a contract (lines of illegible handwriting, no signature); {BEAU_CIV} "
             f"in the left third slides a quill pen across the desk toward {ALEX} (right third, in his sergeant's uniform), who looks at "
             "the paper he cannot read, uncertain."),
    "M25": m([A, "ref:plate-washington"], ["ALEXIS", "the corridor"],
             f"Washington barracks room, 1833: in the background, three soldiers laughing and pointing (at nothing graphic; just mocking "
             f"laughter); in the foreground right third, {ALEX} in his uniform, not laughing, looking straight ahead, quietly dignified."),
    "M26": m([FAM, A, "ref:plate-farm"], ["the family (the wife)", "ALEXIS", "the Quebec farm"],
             f"Golden low evening light at a log cabin in Lower Canada, 1834: Alexis's wife stands in the open doorway in the left third, "
             f"arms folded, calm and decided; behind her inside the warm cabin, {ALEX} sits by the fire with a child on his knee. Home."),
    "M27": m([B, "ref:plate-study"], ["BEAUMONT (older)", "the study style"],
             f"A St. Louis study in the 1840s: {BEAU_CIV}, greyer now, alone at a desk in the left third under a lamp, a fresh sheet of "
             "paper and a quill in front of him, a few sealed letters stacked at his elbow, rain on the window. Persistent, lonely."),
    "M28": m([A, "ref:plate-farm"], ["ALEXIS (in his forties)", "the farm"],
             f"The farm near Berthier, 1846: a young man on horseback (Beaumont's son, generic rider, dark coat) has stopped on the dirt "
             f"road in the left third; {ALEX40} stands behind his fence in the right third, shaking his head kindly but firmly. Hens, hay."),
    "M29": m([B], ["BEAUMONT (only his empty chair)"],
             "St. Louis at night, 1853: a dark wet cobbled street, gas-lamp glow, one lit upstairs window in the left third; through it, "
             "an empty desk chair and a cold lamp. Quiet, final. No people."),
    "M30": m([AO, "ref:plate-farm"], ["OLD ALEXIS", "the farm"],
             f"Sunset on the farm: {ALEXOLD} sits on the porch step of his log house in the right third, hands on his knees, looking at "
             "the river below. Long golden light, peaceful."),
    "M31": m(["ref:plate-farm"], ["the farm"],
             "The same log farmhouse at dusk, June 1880: deep blue sky, one window glowing warm, the rest dark, mist rising from the "
             "river. The house in the right third. Still, quiet."),
    "M32": m([OSL], ["DR. WILLIAM OSLER"],
             "Montreal, 1880: Dr. William Osler (same face, hair and moustache as his sheet, frock coat) writes a letter at a desk by a "
             "tall window in the left third, books and a microscope behind him, lamp light; thoughtful, professional curiosity."),
    "M33": m(["ref:plate-churchyard16"], ["the churchyard"],
             "The parish churchyard on a hot June afternoon, 1880: two farmers in shirtsleeves dig a deep grave beside the fence (only "
             "their shoulders and shovels above ground level, a high mound of earth), heat haze, the white church in the left third, a "
             "tall shovel leaning on the fence. Respectful, no coffin, no body."),
    "M34": m(["ref:plate-churchyard16", AO], ["the churchyard", "OLD ALEXIS (only his red tuque)"],
             "The same churchyard at evening: a fresh closed grave with wildflowers laid on it, a simple wooden cross, and a red knitted "
             "tuque hung on the fence post beside it. Golden light, peaceful, the church in the left third."),
    "M35": m([A], ["ALEXIS"],
             f"Sunrise on a wide calm river: {ALEX} paddles a birch-bark canoe from LEFT to RIGHT toward the rising sun, a small figure "
             "in the left third, mist, golden reflections, a long way still to go. Hopeful, free."),
    # ── inserts (1:1, 2K) ──
    "I01": ins([B], ["BEAUMONT (only his hands and cuffs)"],
               "Extreme close-up: a doctor's hands in dark-blue cuffs tie a cream-white silk thread around a small cube of raw beef on a "
               "wooden table; an open brass pocket watch lies beside it."),
    "I02": ins([A], ["ALEXIS (only his side and shirt)"],
               f"Extreme close-up of {PORT}, the linen shirt lifted at its edge; a small cube of beef on a cream-white silk string is being "
               "lowered toward the porthole from above. Clean, gentle, illustrated."),
    "I03b": ins(["kf:I03a"], ["THE SAME pocket watch (identical design, table and lighting)"],
                "The identical open brass pocket watch on the same table, now with the hands at exactly ONE o'clock. Everything else identical."),
    "I03c": ins(["kf:I03a"], ["THE SAME pocket watch (identical design, table and lighting)"],
                "The identical open brass pocket watch on the same table, now with the hands at exactly TWO o'clock. Everything else identical."),
    "I04": ins([B], ["BEAUMONT (only his hand and cuff)"],
               "A doctor's hand lifts a cream-white silk string out of frame; tied along it hang six small food pieces, the cabbage leaf "
               "and the bread visibly half dissolved, the meats softened. Clean and appetising-neutral, no slime."),
    "I05": ins([B], ["BEAUMONT (only his hand and cuff)"],
               "The same cream-white silk string lifted up, now almost bare: only two small shrunken pieces of meat remain tied to it, "
               "the empty loops where the others were. Deadpan."),
    "I06": ins([], [],
               "Extreme close-up of an 1820s flintlock musket lock: the hammer snapping down, a bright spark leaping from the frizzen, a "
               "puff of white powder smoke. Dark background, warm spark light."),
    "I07": ins([], [],
               "Extreme close-up: a small metal tray on a bedside table with a curved surgical needle, a coil of linen thread and folded "
               "cloths, a candle flame reflected in the needle. Cool teal shadows."),
    "I08": ins([], [],
               "Six food items laid out in a neat 3-by-2 grid on plain bone-white paper, each item separate in its own cell with space "
               "around it, each tied with a short cream-white silk string with a small BLANK paper tag: spiced braised beef, raw salted "
               "fat pork, raw salted lean beef, boiled salted beef, a piece of stale bread, a slice of raw cabbage. Clean, flat, even light."),
    "I09": ins([A], ["ALEXIS (only his side)"],
               f"Close-up of {PORT}; a small round white medicine pill falls toward it from above, a tiny motion trail. Clean diagram feel."),
    "I10": ins([], [],
               "Extreme close-up of a glass vial filled with clear amber liquid, kept warm by a stove glow behind; inside, a small cube of "
               "meat with softened, dissolving edges and a few fine particles floating. Scientific, clean."),
    "I11": ins([B], ["BEAUMONT (only his hand)"],
               "An open handwritten notebook from 1825 on a desk: pages of dense ILLEGIBLE scribble-handwriting (no readable words), "
               "small neat sketches of a stomach and a tiny pocket watch in the margins, a quill resting across it, lamp light."),
    "I12": ins([], [],
               "A long wooden shelf packed with dozens of matching worn leather notebooks, some lying flat, ink bottles and a candle at "
               "one end; the shelf runs from left to right through the frame. No lettering on the spines."),
    "I13": ins([], [],
               "An 1833 contract on a desk: a single sheet with lines of ILLEGIBLE copperplate scribble (no readable words), a red wax "
               "seal is NOT allowed (use a brown wax seal), NO signature or mark at the bottom, a quill and inkwell beside it."),
    "I14": ins([], [],
               "A leather purse spilling gold and silver coins on a polished committee table in London, 1840, beside a closed ledger and "
               "a quill. NO spectacles anywhere (they are reserved for the hidden-glasses game). Warm candlelight."),
    "I17": ins([A], ["ALEXIS (only his red tuque)"],
               "A red knitted voyageur tuque hanging on an iron nail beside a weathered wooden cabin door, evening light across the "
               "grain of the wood. Simple, quiet."),
    "I18": ins([], [],
               "A dark silhouette of a young 1920s doctor in a white coat seen from behind in a hospital corridor, holding up a long, "
               "thin rubber tube coiled in one hand, backlit by a single cold window. Mysterious, no face visible."),
    "I19": ins([], [],
               "Clean educational illustration on soft bone background: a round brass porthole ring set in pastel skin-toned surface; a "
               "soft pastel-pink fold of lining slides halfway across the opening from one side like a little lid. Gentle, cute, "
               "diagrammatic, NO blood, NO organs."),
    "I20": ins([], [],
               "Close-up of two round millstones grinding grain into flour, a little cloud of flour dust, wooden frame, warm light."),
    "I21": ins([], [],
               "A single pear on a plate going soft and wrinkled, slightly brown, comic but not disgusting (no flies, no mould), plain "
               "background."),
    "I22": ins([W + "plate-stomach.png"], ["the clean pastel stomach-interior style (match it)"],
               "Clean pastel educational view inside a stomach, like the reference: soft pink folds, a glowing pool of AMBER gastric "
               "juice at the bottom in which a small cube of food is dissolving with tiny bubbles. Gentle, NO blood."),
    # ── tall-only (9:16) for the Shorts ──
    "T1": tall([A, "ref:plate-store16"], ["ALEXIS (only his silhouette)", "the store"],
               "Low angle, the store doorway backlit by bright lake light: the silhouette of a young voyageur in a tuque falling backward, "
               "a cloud of grey powder smoke curling across the frame. Silhouette only, no wound, no detail of injury."),
    "T2a": tall([A, "ref:plate-sickroom16"], ["ALEXIS", "the sickroom"],
                f"Close-up of {ALEX}'s face on the pillow, eyes CLOSED, pale, candle light from the side, the bandage just visible at "
                "the shoulder. Teal shadows. Face in the upper-middle of the frame."),
    "T2b": tall(["kf:T2a"], ["THE SAME frame (identical face, pillow, framing)"],
                "The identical close-up, but his eyes are now OPEN and the light has warmed to amber, a hint of life returning. "
                "Everything else identical."),
    "T3": tall([AO, "kit:glasses-sheet.jpg"], ["OLD ALEXIS", "Matt's spectacles (exact design)"],
               "Extreme wide vertical frame: from the top of a wooden fort palisade looking down at a wide river at sunset, a tiny "
               "birch-bark canoe paddled by old Alexis (red tuque) far below. " +
               GLASSES.format(where="on top of one sharpened palisade post in the upper foreground")),
    "T4": tall([B, "ref:plate-study", "kit:glasses-sheet.jpg"], ["BEAUMONT", "the study", "Matt's spectacles (exact design)"],
               f"Deadpan comedy frame: {BEAU} writing happily and fast in his notebook at the desk under the window, the room still. " +
               GLASSES.format(where="on the windowsill behind him")),
    "T5": tall([A], ["ALEXIS"],
               f"A dirt road through fields, 1825: {ALEX} walks away from the camera, moving left-to-right across the frame toward the "
               "horizon with a bundle on his shoulder; behind him on the left, a log officer's house with an open door. Cool morning."),
    "T6": tall([A, "ref:plate-farm", "kit:glasses-sheet.jpg"], ["ALEXIS (in his forties)", "the farm", "Matt's spectacles (exact design)"],
               f"Sunset at the farm: {ALEX40} at his fence turns away and walks back toward his house; far down the road, a tiny rider "
               "on horseback leaving. " + GLASSES.format(where="hanging by one arm from the top rail of the fence in the foreground")),
}

ep = json.load(open(P, encoding="utf-8"))
ep["keyframes"].update(KF)
json.dump(ep, open(P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(len(ep["keyframes"]), "keyframes in episode.json;", len(KF), "written now")
