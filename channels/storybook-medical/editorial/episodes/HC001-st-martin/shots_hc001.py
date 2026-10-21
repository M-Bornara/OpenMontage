"""HC001 v2 shot stills: one prompt per generated picture of the beat sheet (beats.json), built from
  the beat's ACTION (written here, action first) · its shot size · its SET (sets_hc001.py: look + location plate)
  · the right-age cast sheets · prompt_kit blocks (framing, period, red rule, writing, body side, glasses, Matt).
Writes episode.json "keyframes" entries named s<beat> (s0.05 …; first/last frames of a first+last clip are s<beat>a / s<beat>b).
Run from the repo root: python channels/storybook-medical/editorial/episodes/HC001-st-martin/shots_hc001.py [--write] [--batch N]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
sys.path.insert(0, str(HERE))
import prompt_kit as K  # noqa: E402
from sets_hc001 import SETS, SET_OF  # noqa: E402

P = Path("projects/hc001-window-into-his-stomach/episode.json")
W = "projects/window-into-the-stomach/assets/images/"
E2 = "projects/human-test-tube/assets/images/refs/"

# ── location plates per set (reference 1: the place; also the style reference, since it has no people) ──
PLATE = {"MAC_SHORE": "ref:plate-harbor", "MAC_FORT": "ref:plate-harbor", "MAC_STORE": "ref:plate-store16",
         "MAC_HOSP": "ref:plate-machosp", "NIAGARA": "ref:plate-niagara", "PLATTS": "ref:plate-platts", "CABIN": "ref:plate-cabin",
         "WASH_DEPT": "ref:plate-washington", "WASH_ROOMS": "ref:plate-washrooms", "FARM": "ref:plate-farm",
         "STTHOMAS": "ref:plate-churchyard16", "LAKE": "projects/_fxlab/remotion/public/img/M21-lake.jpg"}
STYLE_ONLY = "ref:plate-harbor"

# ── cast: who → (reference sheet, role text, description in the CAST line) ──
def alexis(year):
    if year < 1826:
        return (W + "sheet-alexis.png", "ALEXIS at about 18",
                "ALEXIS (young French-Canadian voyageur, about 18: his sheet's face and dark hair, red knitted tuque, loose linen shirt, woven arrow sash)")
    if year < 1846:
        return ("ref:sheet-alexis-1830s", "ALEXIS at about 30",
                "ALEXIS at about 30 (his 1830s sheet: weathered, short stubble, red tuque, brown wool waistcoat, arrow sash)")
    return (W + "sheet-alexis-old.png", "OLD ALEXIS",
            "OLD ALEXIS (his later-life sheet: white hair and beard, red tuque, brown waistcoat, sash)")


def beaumont(year):
    if year < 1830:
        return (W + "sheet-beaumont.png", "DR. BEAUMONT in 1822–25",
                "DR. WILLIAM BEAUMONT (his sheet: dark-blue 1820s US Army surgeon's coat, brass buttons, brass watch chain always visible)")
    if year < 1840:
        return ("ref:sheet-beaumont-1833", "DR. BEAUMONT in 1833",
                "DR. BEAUMONT aged 48 (his 1833 sheet: heavier, greying temples, the dark-blue army surgeon's coat, brass watch chain)")
    return ("ref:sheet-beaumont-1850s", "DR. BEAUMONT around 1850",
            "DR. BEAUMONT aged 65 (his 1850s sheet: white-grey hair, civilian black frock coat, brass watch chain)")


T22, TSC, TLY, T80 = "ref:troupe-mackinac-1822", "ref:troupe-scholars-clergy", "ref:troupe-later-years", "ref:troupe-1880"
TROUPE = {  # key: (sheet, position in the line-up, description)
    "f1": (T22, "LEFT", "a young stocky voyageur, round cheerful face, brown wool cap, faded blue shirt, green sash"),
    "f2": (T22, "SECOND", "a tall lanky voyageur, drooping black moustache, blue wool cap, striped shirt"),
    "voy": (T22, "THIRD", "an older grey-bearded voyageur in a leather cap and buckskin jacket"),
    "clerk": (T22, "RIGHT", "the thin clean-shaven store clerk in a waistcoat and long canvas apron"),
    "p1": (TSC, "LEFT", "a fat, completely bald professor with grey mutton-chop whiskers and a black tailcoat"),
    "p2": (TSC, "SECOND (the thin white-haired man)", "a very thin, tall professor with long white hair and a dark-green frock coat"),
    "priest": (TSC, "RIGHT", "an elderly parish priest in a black cassock with a plain cross"),
    "sol1": (TLY, "LEFT", "a tall fair young infantry private in a light-blue fatigue jacket"),
    "sol2": (TLY, "SECOND", "a stout red-cheeked corporal with dark side-whiskers, same light-blue jacket"),
    "israel": (TLY, "THIRD", "Beaumont's son Israel, about 20, slim, brown riding coat, tall boots"),
    "merchant": (TLY, "RIGHT", "a portly fur merchant in a grey top hat and a fur-collared greatcoat"),
    "dig1": (T80, "LEFT", "a lean farmer in a straw hat and braces"),
    "dig2": (T80, "SECOND", "a broad young farmer with curly hair and a work smock"),
    "son80": (T80, "THIRD", "Alexis's grown son, about 45, full dark beard, black Sunday coat, hat in hand"),
    "dau80": (T80, "RIGHT", "Alexis's grown daughter, about 40, black bonnet, dark mourning dress"),
}
WIFE = (E2 + "sheet-young-family.png", "his WIFE (the woman on this sheet)",
        "ALEXIS'S WIFE (her sheet: dark hair in a bun, grey wool shawl, patched brown dress)")
KIDS = (E2 + "sheet-young-family.png", "his WIFE and their small child (this sheet)", "")
MATT = ("kit:matt-eras.jpg", "MATT (use only his 1820s voyageur outfit: teal scarf, amber notebook, hat brim low)", "")
OSLER = ("ref:sheet-osler", "DR. WILLIAM OSLER in 1880",
         "DR. WILLIAM OSLER (his sheet: about 30, slim, dark moustache, dark frock coat, watch chain)")
GLASSES = "kit:glasses-sheet.jpg"

SIZE = {"ECU": "Extreme close-up.", "CU": "Close-up.", "MCU": "Medium close-up (head and shoulders).", "MS": "Medium shot (waist up).",
        "WS": "Wide shot: full figures in their setting.", "EWS": "Extreme wide establishing shot.", "FILE": "Medium shot."}
PORT = ("a small, clean, healed, brass-rimmed round opening in the skin of his LEFT side, like a neat illustrated porthole with "
        "soft warm shadow inside (NO blood, NO wound, NO organs)")
HANDS_B = "only DR. BEAUMONT'S HANDS and forearms are in frame (dark-blue cuff with a brass button)"

# ── the shots: id → (action, cast keys, options) ── cast keys: A, B, wife, kids, matt, osler, troupe keys, "hands"
#    options: people_free · writing (WAVY) · porthole · wound · glasses '<where>' · matt '<beat>' · aspect
S = {}


def shot(id, action, cast=(), **o):
    S[id] = dict(action=action, cast=list(cast), **o)


# 0 · hook (Fort Niagara, 1825)
shot("0.01", "Beaumont's hands tie a thin cream-white silk string tightly around a small cube of raw beef on the table; his open "
     "brass pocket watch lies beside it. Concentrated, careful hands.", ["hands"], watch=True, clip=True)
shot("0.02a", "The small cube of beef hangs on its taut cream-white string just ABOVE the opening in Alexis's side; Beaumont's "
     "fingers pinch the string at the top of the frame. Alexis's shirt is pulled up, his skin calm.", ["hands", "A"], porthole=True)
shot("0.02b", "SAME FRAME as reference 1 (the first frame), only one change: the beef is now INSIDE the opening, gone from view, and "
     "the cream-white string runs taut from Beaumont's fingers at the top of the frame down into the opening.", ["hands", "A"],
     porthole=True, first="s0.02a")
shot("0.05", "Beaumont holds the cream-white string up to the window light: half of the beef is dissolved away, ragged and smaller. "
     "Behind it, soft and slightly out of focus, Beaumont's wide astonished eyes.", ["B"])
shot("0.06", "Alexis has just stood up from the chair and walks toward the open door on the right with a big armful of firewood, "
     "tucking his shirt in, perfectly at ease; Beaumont sits at the table on the left with his notebook up, watching him go.",
     ["A", "B"], writing=True, clip=True)
shot("0.07", "Beaumont alone at the table, his notebook in hand, staring at the doorway Alexis has just left by; lamplight on his "
     "face, a half-smile of disbelief.", ["B"], writing=True)
# 1 · the case (Mackinac 1822)
shot("1.01", "Dawn over Mackinac Island: the whitewashed fort with wooden blockhouses on its bluff, birchbark canoes pulled up on the "
     "pebble beach, grey log warehouses, smoke from chimneys, mist lying on the water. Calm sky in the upper centre for a title.",
     [], people_free=True)
shot("1.03", "A brigade of four large birchbark freight canoes paddles in toward the beach, voyageurs in wool caps and sashes "
     "stroking in rhythm, spray flashing off the blades, fur bales in the canoes. In the LAST canoe on the left, small: MATT, "
     "writing in his amber notebook instead of paddling.", ["f1", "f2", "voy", "matt"], matt="writing in his notebook instead of paddling", crowd="about twelve voyageurs across the four canoes, all different, none in a red tuque",
     clip=True)
shot("1.04", "Three voyageurs in one canoe pull their paddles together in a hard stroke, water spraying off the blades, faces "
     "straining and grinning.", ["f1", "f2", "voy"])
shot("1.05", "Alexis laughs on the dock with his two friends, all three sharing a loaf of bread, morning light, canoes behind them. "
     "Alexis in the right third.", ["A", "f1", "f2"])
shot("1.05b", "Alexis heaves a heavy fur bale up onto the dock with both arms, muscles straining; more bales behind him, marked only "
     "with a simple painted shape (no lettering).", ["A"])
shot("1.06", "Inside the crowded fur-company store: by the counter the clerk fumbles a long musket, its muzzle swinging carelessly "
     "toward the room; voyageurs crowd the shelves; Alexis stands in the left foreground, turning his head toward the noise. "
     "Dust in the light from the door.", ["A", "clerk", "f1", "voy"], crowd="about eight men in the store; the named ones are clearly placed, the rest generic")
shot("1.08", "A spilled powder horn and a scatter of grey duck-shot pellets on the store's floorboards, a wisp of gun smoke curling "
     "above them.", [], people_free=True)
shot("1.10", "Beaumont runs up the steep dirt path from the white fort, his medical bag in hand, coat flapping, urgent.", ["B"], clip=True)
shot("1.11", "Beaumont bursts in through the bright store doorway, light flaring behind him; the men inside turn and step back "
     "to make way.", ["B", "f1", "f2", "clerk"], crowd="Beaumont plus about six men inside")
shot("1.12", "Beaumont kneels on the floor over Alexis, who lies on his back, shirt torn (no injury visible from this angle); "
     "close to the camera on the right, MATT holds a lantern high so the doctor can see, its warm light on Beaumont's intense face.",
     ["B", "A", "matt"], matt_bold="MATT is clearly visible in this shot (his bold moment): close to camera on the right, holding the lantern high, face lit, worried")
shot("1.13", "Over Beaumont's shoulder: Alexis's torn, scorched shirt pulled aside, and on his LEFT side below the ribs a fresh "
     "gunshot wound, painted with restraint: a dark ragged opening, powder burns around it, a little blood, no gore, no organs.",
     ["B", "A"], wound=True)
shot("1.14", "The store gone silent: the men stand with their hats in their hands, heads bowed; Alexis lies on the floor covered "
     "with a grey wool blanket up to his chest, eyes closed.", ["A", "f1", "f2", "voy", "clerk"], crowd="exactly 5 people")
shot("1.15a", "Close on Alexis's face as he lies on the floorboards, pale, EYES CLOSED, lips parted, red tuque fallen beside his head.", ["A"])
shot("1.15b", "SAME FRAME as reference 1 (the first frame), only one change: Alexis's EYES ARE NOW WIDE OPEN in shock.", ["A"], first="s1.15a")
shot("1.16", "Beaumont's face in lantern light, changing from worry to sharp curiosity, eyes narrowing as he thinks.", ["B"])
# 2 · what happened next (Mackinac post hospital)
shot("2.01", "Alexis lies bandaged in the iron army cot, pale, eyes closed, a candle on the stool; through the small window the "
     "straits at dusk.", ["A"])
shot("2.02", "Alexis, propped up in bed, tries a spoonful of broth and chokes; Beaumont, on the left, leans in holding a basin, "
     "worried. Tasteful: no vomit shown.", ["A", "B"], clip=True)
shot("2.03", "Beaumont's worried face as he carefully unwinds a clean white bandage, eyes down on his work.", ["B"])
shot("2.04", "Morning sun floods the whitewashed sickroom; Alexis sits up in bed eating porridge from a wooden bowl, colour back "
     "in his face.", ["A"])
shot("2.05", "Beaumont, on the left, changes the dressing at Alexis's side (only clean white linen visible); Alexis sits on the "
     "cot on the right, patient; through the window the first snow falls.", ["B", "A"])
shot("2.07", "Beaumont's hand lifts a curved surgical needle threaded with silk from a tray, candlelight glinting on it.", ["hands"])
shot("2.08", "Low angle: Alexis, sitting up in bed, pushes the tray with the needle away with one hand, jaw set, eyes hard: no.", ["A"])
shot("2.09", "Alexis sits by the small window looking out at the straits, his face unreadable, the light cool.", ["A"])
shot("2.10", "1820s surgical tools laid out on a cloth in candlelight: a bone saw, knives, a probe; no anaesthetic anywhere, "
     "the steel cold and grim.", [], people_free=True)
shot("2.13", "Beaumont at his desk at home slowly looks up from his papers, the idea landing on his face, firelight warm on him.",
     ["B"], writing=True)
# 3 · the science
shot("3.02", "Two rival professors glare at each other across a lecture table: the fat bald one on the left, arms folded, and the "
     "thin white-haired one on the right, pointing a long finger; students' benches rise behind them.", ["p1", "p2"])
shot("3.05", "A closed wooden door at night with warm lamplight glowing in the gap beneath it.", [], people_free=True)
shot("3.06", "The white fort on its bluff above the straits, seen from the water; a tiny figure of Beaumont stands on the wall walk "
     "looking out.", ["B"])
# 4 · the experiments (Fort Niagara 1825)
shot("4.03", "Six small pieces of food tied along a cream-white silk string laid across the table, spaced apart and clearly "
     "different: a dark spiced beef cube, a pale fat salt-pork piece, a red raw-beef cube, a grey boiled-beef cube, a crust of "
     "stale bread, a green curl of raw cabbage. Each has a small blank paper tag.", [], people_free=True)
shot("4.05", "The same six pieces on the cream-white string, pulled up after two hours: four are gone (just the empty loops of "
     "string), the others half-dissolved and ragged.", [], people_free=True)
shot("4.06", "Alexis sits up on the army cot looking unwell, one hand pressed on his belly, grimacing.", ["A"])
shot("4.07a", "Beaumont's fingers hold a small white pill just above the opening in Alexis's side.", ["hands", "A"], porthole=True)
shot("4.07b", "SAME FRAME as reference 1 (the first frame), only one change: the pill is gone, dropped inside; Beaumont's "
     "fingers open and empty.", ["hands", "A"], porthole=True, first="s4.07a")
shot("4.08", "Comedy hold: Beaumont sits writing happily in his notebook, humming to himself, the room perfectly still around him.",
     ["B"], writing=True)
shot("4.10", "Beaumont, on the left, arranges glass vials of amber liquid, each with a small piece of meat, in a wooden rack by "
     "the warm iron stove; the rack sits well inside the frame.", ["B"], glasses="folded on the shelf above the stove")
shot("4.11", "A wooden rack of glass vials of amber liquid with small pieces of meat inside, warm beside the iron stove, steam "
     "curling.", [], people_free=True)
shot("4.12", "One glass vial of amber liquid with a cube of meat in it, by the stove, the meat whole and firm.", [], people_free=True)
shot("4.12b", "SAME FRAME as reference 1, only one change: the meat cube has softened and shrunk to a small ragged shred, the "
     "liquid a little cloudy.", [], people_free=True, first="s4.12")
shot("4.15", "Alexis, on the right, sits on the cot with a mortified face, eyes wide, looking down at his own side; only Beaumont's "
     "shoulder and ear lean into the left edge of the frame (we never see what he does).", ["A", "B"])
shot("4.17", "Beaumont's sour face, lips pursed, as if he has tasted something bitter.", ["B"])
shot("4.18", "Alexis stands with his arms folded, glaring at the rack of vials, angry and impatient.", ["A"])
shot("4.19", "Alexis stands in the left third staring at the open front door and the bright road beyond.", ["A"])
shot("4.21", "Beaumont looks up sharply from his notes at the table.", ["B"], writing=True)
shot("4.22", "Alexis's empty Windsor chair by the open front door, the door still swinging, bright road outside, nobody there.",
     [], people_free=True)
# 5 · the human experiment
shot("5.02", "Beaumont writes furiously at the table, quill pressing hard, face angry.", ["B"], writing=True)
shot("5.03", "Alexis and his bride stand at the door of a small fieldstone country church, shy and happy, spring light.", ["A", "wife"])
shot("5.05", "Alexis paddles in the stern of a big freight canoe with other voyageurs on a grey northern river, spruce on the banks.",
     ["A", "f1", "voy"], crowd="Alexis plus five or six voyageurs in the big canoe")
shot("5.08", "Alexis splits firewood in the fort yard with an axe, a pile of logs beside him.", ["A"], clip=True)
shot("5.09", "Alexis carries a heavy sack across the stockade yard, bent under it; on the left Beaumont reads his notes, not looking up.",
     ["A", "B"], writing=True)
shot("5.11b", "Alexis paddles hard at dusk, jaw set, one hand pressed against his side between strokes, the lake behind him.", ["A"])
shot("5.13", "Alexis stands at the door of his house, a small defiant smile.", ["A"])
shot("5.14", "A Washington government corridor: white columns, plaster walls, two clerks in the distance carrying papers.",
     [], extras="exactly two small distant clerks in dark coats, faces not detailed")
shot("5.15", "Alexis stands in an ill-fitting army uniform, the sleeves too long over his hands, looking down at himself, unsure.",
     ["A"])
shot("5.16", "Extreme close-up of a contract on the mahogany desk: an official-looking page in neat ink lines with a wax seal; a "
     "candle beside it.", [], people_free=True, writing=True)
shot("5.19", "Beaumont's hand holds out a quill pen toward the viewer across the desk.", ["hands"])
shot("5.21", "Two soldiers laugh loudly in the barracks, slapping their knees; Alexis sits on a bunk on the left, not laughing.",
     ["A", "sol1", "sol2"])
shot("5.21b", "Close on Alexis's face, not laughing, eyes down, while blurred soldiers laugh behind him.", ["A"],
     extras="the soldiers behind are blurred shapes only")
shot("5.22", "Extreme close-up of a folded letter held in a hand, an X mark at the bottom where a signature would be.", [],
     extras="only one hand in frame", writing=True)
shot("5.23", "Alexis's wife stands at the door of their house with her arms folded, firm and unafraid, looking straight ahead.",
     ["wife"])
shot("5.24", "Alexis walks away along the country road from his house, small in the frame, not looking back.", ["A"])
shot("5.25", "Beaumont, older, sits alone at his desk in his study with a fresh blank sheet of paper, a candle, tired.", ["B"])
# 6 · what they learned
shot("6.03", "A committee table in an oak-panelled room: a leather purse of gold coins spilling onto green baize, papers beside it.",
     [], people_free=True, writing=True)
shot("6.05", "Beaumont's son Israel rides a horse along a country road toward a distant farm.", ["israel"])
shot("6.06", "Old Alexis stands at his farm fence, shaking his head slowly, firm.", ["A"])
# 7 · case file photos
shot("7.03", "A portly fur merchant counts a stack of pelts on the store counter.", ["merchant"])
shot("7.05", "Beaumont half in shadow at his table, lamplight on one side of his face, unreadable.", ["B"])
# 8 · the last word
shot("8.02", "Osler writes at his desk under a gaslight, a brass microscope and journals beside him.", ["osler"], writing=True)
shot("8.03", "A museum shelf of labelled specimen jars behind glass, and in the middle one EMPTY jar.", [], people_free=True, writing=True)
shot("8.04", "A folded letter set down unopened on a plank farmhouse table, closed shutters behind.", [], people_free=True, writing=True)
shot("8.05", "The parish priest stands at the church door in summer light, hands folded.", ["priest"])
shot("8.06", "A shuttered farmhouse room in summer heat: a closed plain wooden coffin on trestles, candles burning, a crucifix "
     "on the wall.", [], people_free=True)
shot("8.09", "Close on a fresh grave mound with wildflowers on it, and a red knitted tuque hung on the wooden fence post beside it.",
     [], people_free=True)
shot("8.10", "Alexis's grown son and daughter stand at the fresh grave at sunset, heads bowed, the son holding his hat.",
     ["son80", "dau80"])
# 9 · why it matters
shot("9.03", "A red knitted tuque hanging on a nail by a farmhouse door, evening light.", [], people_free=True)
shot("9.04", "Silhouette of a 1920s doctor in a white coat holding a long thin rubber tube, backlit in a tiled hospital corridor.",
     [], extras="exactly one person, a dark silhouette with no face detail")
# props (sprites on plain backgrounds, composited over the lake plate)
shot("prop-canoe-family", "A birchbark canoe seen from the side: Alexis paddling in the stern, his wife and two small children "
     "sitting in the middle. Isolated on a plain flat light-grey background, no water, no shadow.", ["A", "wife", "kids"], sprite=True, crowd="exactly 4 people")
shot("prop-canoe-solo", "A birchbark canoe seen from the side with Alexis alone paddling in the stern. Isolated on a plain flat "
     "light-grey background, no water, no shadow.", ["A"], sprite=True)

BEAT = {"0.02a": "0.02", "0.02b": "0.02", "1.15a": "1.15", "1.15b": "1.15", "4.07a": "4.07", "4.07b": "4.07", "4.12b": "4.12",
        "prop-canoe-family": "5.11", "prop-canoe-solo": "9.02"}
BATCHES = [("0.", "1."), ("2.", "3.", "4."), ("5.",), ("6.", "7.", "8.", "9.", "prop")]


def build(sid, beats):
    s = S[sid]
    bid = BEAT.get(sid, sid)
    b = beats[bid]
    set_id = SET_OF.get(bid)
    st = SETS[set_id]
    year = int(re.search(r"\d{4}", st["year"]).group())
    refs, roles, who = [], [], []
    plate = PLATE.get(set_id)
    if s.get("first"):
        refs.append("kf:" + s["first"])
    if s.get("sprite"):
        refs.append(STYLE_ONLY)
        roles.append("is a STYLE reference only (painting style): never copy its place")
    elif plate:
        refs.append(plate)
        roles.append("is the LOCATION: this exact place (layout, materials, light); compose the shot inside it from the camera "
                     "angle the shot needs. It is also the style reference")
    else:
        refs.append(STYLE_ONLY)
        roles.append("is a STYLE reference only (painting style): never copy its place")
    if s.get("first"):
        roles.insert(0, "is the FIRST FRAME of this moment: keep everything identical except the change described")
    for c in s["cast"]:
        if c == "A":
            ref, role, desc = alexis(year)
        elif c == "B":
            ref, role, desc = beaumont(year)
        elif c == "hands":
            ref, role, desc = beaumont(year)[0], "DR. BEAUMONT (hands and cuffs only)", HANDS_B
        elif c == "wife":
            ref, role, desc = WIFE
        elif c == "kids":
            ref, role, desc = KIDS[0], KIDS[1], "two small children (a boy of about four and a toddler) like the child on the family sheet"
            if ref in refs:
                who.append(desc)
                continue
        elif c == "matt":
            ref, role, desc = MATT[0], MATT[1], "MATT (1820s voyageur outfit, teal scarf, amber notebook)"
        elif c == "osler":
            ref, role, desc = OSLER
        else:
            sheet, pos, desc = TROUPE[c]
            ref, role = sheet, f"a line-up of stock characters: use ONLY the {pos} person (the one described as '{desc}')"
            if ref in refs:  # two people from the same line-up: one reference, both positions named
                i = refs.index(ref)
                roles[i] += f"; and the {pos} person ('{desc}')"
                who.append(desc)
                continue
        if ref not in refs:
            refs.append(ref)
            roles.append(f"is {role}")
        who.append(desc)
    if s.get("glasses"):
        refs.append(GLASSES)
        roles.append("is Matt's amber spectacles (the hidden-glasses joke)")
    role_txt = " ".join(f"Reference {i + 1} {r}." for i, r in enumerate(roles))
    parts = [SIZE.get(b["shot"], "") if not s.get("sprite") else "Side view, full object.", s["action"]]
    if s.get("people_free"):
        parts.append(K.NO_PEOPLE.split(" Reference 1")[0])
    elif s.get("crowd"):
        parts.append(f"CAST: {s['crowd']}. The named people: " + "; ".join(who) + ". Nobody resembles another named person.")
    elif who:
        parts.append(K.cast(*who, extra=s.get("extras", "")))
    elif s.get("extras"):
        parts.append(f"CAST: {s['extras']}. Nobody else in the frame.")
    if s.get("porthole"):
        parts.append(f"On ALEXIS's body: {PORT}. " + K.body_mark("Alexis", "the opening", side="LEFT"))
    if s.get("wound"):
        parts.append(K.body_mark("Alexis", "the wound", side="LEFT"))
    if s.get("watch"):
        parts.append(f"The pocket watch: {K.NO_HANDS}.")
    if s.get("writing"):
        parts.append(K.WAVY_WRITING)
    if s.get("glasses"):
        parts.append(K.glasses_gag(s["glasses"]))
    if s.get("matt_bold"):
        parts.append(s["matt_bold"] + ".")
    if s.get("matt"):
        parts.append(K.matt_beat("his 1820s voyageur outfit", s["matt"]))
    if not s.get("sprite"):
        parts.append(K.set_block(st["name"], st["year"], st["look"]))
    parts.append(K.SAFE_FRAMING)
    parts += [K.PERIOD, K.RED_RULE, "No lettering, signs or labels anywhere."]
    return {"aspect": "16:9", "resolution": "4K", "refs": refs, "roles": role_txt, "prompt": " ".join(p for p in parts if p),
            "beat": bid}


if __name__ == "__main__":
    beats = {b["id"]: b for b in json.load(open("projects/hc001-window-into-his-stomach/artifacts/beats.json", encoding="utf-8"))["beats"]}
    specs = {(sid if sid.startswith("prop") else "s" + sid): build(sid, beats) for sid in S}
    issues = K.lint_all(specs)
    print(len(specs), "shots ·", "lint:", issues or "clean")
    if "--show" in sys.argv:
        for n, v in specs.items():
            print(f"\n## {n}  refs={v['refs']}\n{v['roles']}\n{v['prompt']}")
    if "--write" in sys.argv:
        ep = json.load(open(P, encoding="utf-8"))
        ep["keyframes"].update(specs)
        json.dump(ep, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("written ->", P)
    for i, pre in enumerate(BATCHES):
        names = [n for n in specs if n.lstrip("s").startswith(pre) or n.startswith(pre)]
        print(f"batch {i + 1}: {len(names)} ·", " ".join(names))
