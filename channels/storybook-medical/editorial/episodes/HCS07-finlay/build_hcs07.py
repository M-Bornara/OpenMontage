"""HCS07 Finlay: writes projects/hcs07-finlay/episode.json (title, narration, references, keyframes) from
storyboard-v1.md v1.1 (approved with its pre-viz 2026-11-14), with the prompt_kit blocks, then lints every prompt.
Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS07-finlay/build_hcs07.py
Then (after the user approves the prompts on the storyboard page):
    episode.py refs hcs07-finlay --batch   ->   episode.py keyframes hcs07-finlay --batch
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (FULL_BLEED, NO_PEOPLE, NO_TEXT, ONE_EACH, PERIOD, SAFE_FRAMING, WAVY_WRITING, camera, cast,  # noqa: E402
                        framing, glasses_gag, lint_all, matt_beat, real_writing, set_block)

PID = "hcs07-finlay"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

NARRATION = """[curious] For nineteen years, almost nobody believed the man who solved yellow fever.
Havana, 1881. Yellow fever was killing thousands, and nobody knew how it spread.
Doctor Carlos Finlay had an idea… a mosquito.
He told the Academy of Sciences. The reaction: disbelief.
For nineteen years he kept breeding mosquitoes and testing his idea.
In 1900, a US Army team led by Walter Reed came to Cuba… and finally tested it. With Finlay's mosquitoes.
[serious] One of the team, Jesse Lazear, was bitten… and died of yellow fever.
The mosquito was the carrier. Finlay had been right all along.
[curious] Reed got most of the fame. But Reed himself gave the credit… to Finlay."""

# ── people (from the real photos in projects/hcs07-finlay/refs, references.md) ───────────────────────────────────
EYEGLASSES = "small oval wire-rimmed eyeglasses with CLEAR glass (clear, NOT amber, not tinted)"
FINLAY81 = ("CARLOS FINLAY in 1881 (47; bald on top with dark-grey hair at the sides, a thick dark-grey moustache that runs "
            f"into full side whiskers, a clean-shaven chin, {EYEGLASSES}, a kind, intent face; black frock coat, white "
            "shirt, dark bow tie)")
FINLAY00 = ("CARLOS FINLAY in 1900 (66; the same face older: bald on top, a white moustache running into white side "
            f"whiskers, a clean-shaven chin, {EYEGLASSES}; a light cream linen suit, a dark polka-dot bow tie)")
REED = ("WALTER REED (49; a neat dark moustache, short side-parted dark hair, a lean serious face; a US Army officer's "
        "dark-blue uniform of 1900 with a high standing collar, braided gold shoulder cords and brass buttons)")
LAZEAR = ("JESSE LAZEAR (34; centre-parted dark hair, a full, neatly trimmed dark beard and moustache, a calm focused face; "
          "white shirt with the sleeves rolled up, a dark waistcoat)")

# ── sets (period photos: references.md) ───────────────────────────────────────────────────────────────────────────
HARBOUR = set_block("Havana harbour seen from the roofs of the old city", "1881",
                    "flat lime-washed rooftops in the foreground; across the deep blue-green harbour mouth, the stone "
                    "Morro Castle and its lighthouse on a rocky point; sailing ships and one steamer at anchor; bright "
                    "tropical afternoon light")
STREET = set_block("A narrow street in Old Havana", "1881",
                   "two-storey houses with thick lime-plastered walls in faded ochre, pale blue and cream, tall wooden "
                   "doors, iron window grilles, wooden shutters, flat roofs, worn cobbles; hard sun and deep shade")
STUDY = set_block("Finlay's study at night, Havana", "1881",
                  "dark wooden desk, a brass oil lamp with a warm glow, books and papers, a tall shuttered window")
ACADEMY = set_block("The hall of the Royal Academy of Medical, Physical and Natural Sciences of Havana, in the old San "
                    "Agustin convent", "14 August 1881",
                    "thick whitewashed stone walls, round stone arches, tall windows with wooden shutters half open to "
                    "bright daylight, rows of plain wooden benches facing a wooden lectern; no ceiling fans, no electric "
                    "light")
LAB = set_block("Finlay's home laboratory, Havana", "1880s-1890s",
                "wooden shelves of glass jars with gauze tops, holding water and mosquito larvae; a brass microscope, "
                "notebooks, a tall window with sunlight")
CAMP = set_block("A US Army camp of white tents near Havana", "summer 1900",
                 "rows of white canvas army tents, tall royal palms, reddish earth, a flagpole with the US flag of 1900, "
                 "bright sun")
WARD = set_block("Las Animas hospital ward, Havana", "August 1900",
                 "a long whitewashed ward, iron beds with white sheets, tall shuttered windows open to the light")
TENT = set_block("Inside an army tent", "September 1900, at dusk",
                 "canvas walls glowing orange in the last light, a folding camp cot, a wooden crate as a table, the tent "
                 "flap open to royal palms against a dusk sky")
STAGE = set_block("A banquet hall in the United States", "1901",
                  "a small raised stage hung with red, white and blue bunting, gas lamps, an audience in evening dress")
REED_DESK = set_block("Walter Reed's desk", "1900-1901", "dark wood desk top, an inkwell, a handwritten report on paper")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "
PHOTO = ("Reference 2 is a period photograph of the real person: paint THIS face (likeness: head shape, hair, whiskers, "
         "eyes, nose) in our storybook style, not as a photo; do not put the photograph itself on the sheet. ")


def sheet(person: str, extra: str) -> str:
    return (f"Clean character model sheet on plain bone-white paper: {person}. Front view, three-quarter view, profile "
            f"view, back view, plus three head close-ups ({extra}). Same scale in every view. No text, labels or watermark.")


REFERENCES = {
    # two sheets, one age each (L38: one sheet with both ages could put two Finlays in a shot)
    "sheet-finlay-1881": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/finlay.jpg"],
        roles=SHEET + PHOTO + "The photo shows him older (about 1900): paint him at 47, hair and whiskers dark grey. ",
        prompt=sheet(FINLAY81, "intent, studying something closely; patient, a little hurt; quietly certain")),
    "sheet-finlay-1900": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/finlay.jpg"], roles=SHEET + PHOTO,
        prompt=sheet(FINLAY00, "a small quiet smile; reading; kind")),
    "sheet-reed": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/reed.jpg"], roles=SHEET + PHOTO,
        prompt=sheet(REED, "serious, listening; determined; a modest half smile")),
    "sheet-lazear": dict(aspect="16:9", refs=[SHEET_LAYOUT, "proj:refs/lazear.jpg"], roles=SHEET + PHOTO,
        prompt=sheet(LAZEAR, "focused at work; calm; tired")),
    "plate-street": dict(aspect="9:16", refs=[STYLE_PLATE, "proj:refs/havana_street_1880s.jpg"],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. "
              "Reference 2 is a period photograph used ONLY for the house details (lime plaster, iron window grille, "
              "door); ignore the people in it. ",
        prompt=f"{STREET} Vertical frame looking down the narrow street, houses on both sides. EMPTY location plate: no "
               f"people. Three clear depth layers. {PERIOD} {NO_TEXT}"),
    "plate-academy": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{ACADEMY} Vertical frame from the back of the hall toward the lectern under the tall windows. EMPTY "
               f"location plate: no people. {PERIOD} {NO_TEXT}"),
}

F = F81 = "ref:sheet-finlay-1881"
F00, R, L = "ref:sheet-finlay-1900", "ref:sheet-reed", "ref:sheet-lazear"
STYLE_ONLY = ("Reference 1 is the {n} plate, for the painting style and palette ONLY: do NOT copy its composition or "
              "camera angle. ")
HALL_LOOK = ("Reference 1 is an earlier shot of this hall, for the painting style, stone, light and benches ONLY: do NOT "
             "copy its composition or camera position. ")
# the Academy hall is the one set seen three times (pre-viz map-academy.png): lectern at the north end under the windows,
# benches in rows facing it, Matt at the east end of row 1
HALL_MAP = ("GEOGRAPHY: the lectern stands at the north end of the hall under the tall shuttered windows; rows of benches "
            "face it from the south.")
CROSSED = ("CROWD: about twelve bearded Spanish-Cuban academics in black frock coats on the benches, most with their arms "
           "crossed, sceptical.")
CROWD_BACKS = ("CROWD: about twelve academics in black frock coats on the benches, seen only from behind (backs of heads "
               "and shoulders).")

KEYFRAMES = {
    "s1a": dict(aspect="9:16", refs=["kf:s4a"], roles=HALL_LOOK,
        prompt=f"{ACADEMY} {HALL_MAP} {framing('MCU', 'slightly low angle', '50 mm', 'the doubters: arms crossed against a new idea', 'stubborn, closed, one eyebrow raised')} "
               f"{camera('in the front bench row, close, looking along it', 'west, along the row', 'the next seated men in the row, out of focus, and a stone arch')} "
               "Three seated bearded academics side by side, chest up, each with his WHOLE head and face in the frame: "
               "stern faces, arms firmly crossed over black frock coats, one gold watch chain. Every person has a head. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s1b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-academy", F],
        roles=STYLE_ONLY.format(n="Academy") + "Reference 2 is CARLOS FINLAY (same face, whiskers, clear eyeglasses). ",
        prompt=f"{STUDY} {framing('CU', 'eye level', '100 mm, very shallow focus', 'the man who solved yellow fever, looking at the culprit', 'quiet certainty')} "
               f"{camera('across the desk, very close to the jar', 'Finlay', 'dark study and the lamp glow, soft')} "
               "A small clear glass jar held up to the light fills the centre of the frame; inside it, ONE mosquito, a "
               "crisp dark silhouette with white-banded legs. Behind the glass, out of focus, the eyes and clear "
               f"eyeglasses of {FINLAY81}. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", resolution="4K", refs=["ref:plate-street", "proj:refs/havana_harbor_1860.jpg"],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is a period photograph used ONLY for the shape of "
              "Morro Castle, its lighthouse and the harbour mouth. ",
        prompt=f"{HARBOUR} {framing('ELS', 'high angle over the rooftops', '24 mm', 'a busy tropical port where a deadly fever comes and goes', 'bright, beautiful, uneasy')} "
               f"{camera('on a high rooftop in the old city', 'north-east, across the harbour mouth', 'flat roofs below, the harbour mouth, Morro Castle and the lighthouse on the far point, sky')} "
               "Among the ships at anchor, one sailing ship flies a small plain yellow flag at its masthead (the "
               f"quarantine flag). {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2b": dict(aspect="9:16", refs=["ref:plate-street"], roles=STYLE_ONLY.format(n="Havana street"),
        prompt=f"{STREET} {framing('LS', 'eye level', '35 mm', 'fear in the street: nobody knows how the fever spreads', 'hushed, wary')} "
               f"{camera('in the street, at the corner', 'down the narrow street', 'the street narrowing away in sun and shade')} "
               "On the left, one house with closed shutters and a black mourning bow on its tall door; a doctor's small "
               "black two-wheeled carriage with a horse waits outside it. "
               f"{cast('a woman in a long pale dress and a shawl walking away on the far right, keeping her distance', 'a man in a straw hat crossing to the far side')} "
               f"No sick people, no bodies. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3": dict(aspect="9:16", refs=["ref:plate-academy", F],
        roles=STYLE_ONLY.format(n="Academy") + "Reference 2 is CARLOS FINLAY (1881 version: dark-grey whiskers). ",
        prompt=f"{STUDY} {framing('MCU', 'eye level', '50 mm', 'Finlay has his idea: the mosquito', 'still, fascinated, holding his breath')} "
               f"{camera('across the desk', 'Finlay', 'the dark shuttered window and bookshelves, lamp glow on the right')} "
               f"{cast(FINLAY81 + ', at his desk, holding perfectly still, studying a mosquito that has landed on the back of his own raised hand')} "
               f"The mosquito is a small sharp dark silhouette; no bite, no blood. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4a": dict(aspect="9:16", refs=["ref:plate-academy", F],
        roles=STYLE_ONLY.format(n="Academy") + "Reference 2 is CARLOS FINLAY (1881). ",
        prompt=f"{ACADEMY} {HALL_MAP} {framing('LS', 'eye level', '28 mm', 'Finlay presents his mosquito theory to the Academy', 'formal, tense')} "
               f"{camera('at the back of the hall behind the last bench', 'north, toward the lectern', 'the lectern under the tall shuttered windows and the stone arches, rows of benches with the backs of heads')} "
               f"{cast(FINLAY81 + ', small in the frame at the lectern, papers in hand, speaking')} "
               f"{CROWD_BACKS} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4b": dict(aspect="9:16", refs=["kf:s4a", "kit:matt-sheet.jpg"],
        roles=HALL_LOOK + "Reference 2 is MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; "
              "his clothes are described below. ",
        prompt=f"{ACADEMY} {HALL_MAP} {framing('MS', 'eye level, the reverse angle from the lectern', '35 mm', 'the Academy does not believe him', 'disbelief: crossed arms, one raised eyebrow, a bored hand fan')} "
               f"{camera('at the lectern, where Finlay stands', 'south, at the audience', 'the seated audience FACING the camera, and behind them the hall\'s south wall: plain whitewashed stone with one tall arched wooden door; NO windows and NO lectern anywhere in view')} "
               f"{CROSSED} One raises an eyebrow; one fans himself slowly with a paper hand fan. "
               f"{matt_beat('a cream linen jacket and a straw boater of 1881', 'at the right end of the front bench, the only one leaning forward, eagerly writing in his notebook')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5": dict(aspect="9:16", refs=["ref:plate-academy", F, "kit:glasses-sheet.jpg"],
        roles=STYLE_ONLY.format(n="Academy") + "Reference 2 is CARLOS FINLAY (his hands and cuffs). Reference 3 shows "
              "Matt's amber spectacles. ",
        prompt=f"{LAB} {framing('MS', 'eye level', '35 mm', 'nineteen years of breeding mosquitoes and testing', 'patient, stubborn devotion')} "
               f"{camera('beside the shelves', 'the window', 'the shelves of jars on the left and the bright tall window on the right')} "
               "Finlay's hands (black sleeves, white cuffs) lift one gauze-topped jar of larvae toward the window light; "
               f"only his hands and cuffs are in the picture, no person. {glasses_gag('folded on the shelf beside the larvae jars')} "
               f"{WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6a": dict(aspect="9:16", refs=["ref:plate-street", R],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is WALTER REED (same face, moustache, uniform). ",
        prompt=f"{CAMP} {framing('ELS', 'low angle', '24 mm', 'the US Army commission arrives to test the idea', 'purposeful, official')} "
               f"{camera('low on the camp path', 'down the path between the tents', 'rows of white tents, royal palms, the flagpole')} "
               f"{cast(REED + ', in front, walking toward the camera', 'an older army officer, clean-shaven, grey-haired, in the same uniform without shoulder cords', 'an army doctor in a white jacket', 'an army doctor in shirtsleeves')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6b": dict(aspect="9:16", refs=["ref:plate-street", F, R],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is CARLOS FINLAY in 1900 (his hand and cuff). "
              "Reference 3 is WALTER REED (his uniform sleeve). ",
        prompt=f"{framing('INSERT', 'top-down over a table', '50 mm', 'Finlay hands over his mosquitoes', 'trust, a quiet handover')} "
               f"{camera('above a wooden table', 'straight down', 'the plain wooden table top')} "
               "From the left, an old man's hand with a cream linen cuff (Finlay, 1900) passes a small corked glass tube "
               "holding tiny dark mosquito eggs on a strip of paper to a hand from the right in a dark-blue army sleeve "
               f"with a brass button (Reed). {FULL_BLEED} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7a": dict(aspect="9:16", refs=["ref:plate-street", L],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is JESSE LAZEAR (same face, full beard). ",
        prompt=f"{WARD} {framing('MCU', 'eye level', '50 mm', 'at work feeding a lab mosquito, Lazear is bitten by a stray one', 'absorbed in his work, unaware')} "
               f"{camera('beside the bed', 'Lazear across the bed', 'the whitewashed ward wall and a tall shuttered window behind him')} "
               f"{cast(LAZEAR + ', bending over the bed, both hands low: he presses the open mouth of a small upside-down glass test tube flat against the patient’s bare forearm on the sheet, a lab mosquito inside the tube; his eyes are on the tube', 'the patient, seen ONLY as one bare forearm resting on the white sheet')} "
               "A second mosquito, a small dark silhouette, has landed on the back of Lazear's own hand; he has not "
               f"noticed. No blood, no sick face. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7b": dict(aspect="9:16", refs=["ref:plate-street"], roles=STYLE_ONLY.format(n="Havana street"),
        prompt=f"{TENT} {framing('LS', 'eye level', '35 mm', 'Lazear has died of yellow fever', 'grief, silence')} "
               f"{camera('inside the tent by the entrance', 'the empty cot and the open flap', 'canvas wall, the open flap with royal palms against the dusk sky')} "
               "An empty folding cot with a folded dark-blue army jacket and a field cap laid on it; a single candle "
               f"burning on the crate. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8a": dict(aspect="9:16", resolution="4K", refs=["ref:plate-street"], roles=STYLE_ONLY.format(n="Havana street"),
        prompt=f"{framing('ECU', 'eye level', 'macro', 'the carrier, finally proved', 'striking, almost beautiful')} "
               f"{camera('very close to the insect', 'the mosquito side-on', 'a plain warm amber glow, nothing else')} "
               "ONE yellow-fever mosquito (Aedes aegypti) side-on in the centre: a dark body with a white lyre-shaped mark "
               "on its back, white-banded legs, delicate wings lit from behind, drawn as a crisp storybook silhouette. "
               f"{FULL_BLEED} {NO_PEOPLE} {SAFE_FRAMING} {NO_TEXT}"),
    "s8b": dict(aspect="9:16", refs=["ref:plate-street", F],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is CARLOS FINLAY (1900 version: white whiskers, linen suit). ",
        prompt=f"{STUDY.replace('at night', 'by day').replace('1881', '1900')} {framing('MS', 'eye level', '50 mm', 'Finlay was right all along', 'a small quiet smile, vindicated but modest')} "
               f"{camera('inside the room, beside the desk', 'Finlay at the open window', 'the open window with bright Havana rooftops behind him')} "
               f"{cast(FINLAY00 + ', standing at the window, reading a letter, a small quiet smile')} "
               f"{WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9a": dict(aspect="9:16", refs=["ref:plate-street", R],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is WALTER REED. ",
        prompt=f"{STAGE} {framing('MS', 'low angle', '35 mm', 'Reed is celebrated', 'applause, bright flashes')} "
               f"{camera('below the stage among the audience', 'up at Reed', 'the bunting and the gas lamps of the hall')} "
               f"{cast(REED + ', on the stage, accepting applause with a modest nod', 'a young clean-shaven photographer in a bowler hat at the left, with a box camera on a tripod and a flash pan raised and flashing')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9b": dict(aspect="9:16", refs=["ref:plate-street", R],
        roles=STYLE_ONLY.format(n="Havana street") + "Reference 2 is WALTER REED (his uniform sleeve and hand only). ",
        prompt=f"{REED_DESK} {framing('INSERT', 'top-down over the desk', '50 mm', 'Reed gives the credit to Finlay', 'fairness, a quiet correction')} "
               f"{camera('above the desk', 'straight down', 'the report on the desk top')} "
               "A handwritten report on cream paper fills the frame. Reed's hand in a dark-blue sleeve underlines one "
               f"name with a pen. {real_writing('Dr. Carlos J. Finlay', 'in the middle of the page, underlined')} The rest of the "
               "page is nearly blank: only four soft wavy grey lines with NO letters above and below the name, no heading, "
               "no signature, no other words. "
               f"{FULL_BLEED} {SAFE_FRAMING} {PERIOD}"),
}


# -- v2 references (user, 2026-11-14: "make sure duplications are not happening"): L38 + L39 --------------------------
# A set plate goes only to shots on its own set (L39); shots elsewhere take the character sheets (painted in our style)
# or the HC001 study plate as STYLE only (not from this film, so its room can't be mistaken for one of ours). Each shot
# with a sheet says every person appears once (L38). Finlay has one sheet per age.
OUTSIDE = "Reference 1 is a people-free room from another film, for the painting style ONLY: never paint its room. "
SHEETS = {"F81": "CARLOS FINLAY in 1881 (dark-grey whiskers, clear eyeglasses)",
          "F00": "CARLOS FINLAY in 1900 (white whiskers, clear eyeglasses, linen suit)",
          "R": "WALTER REED", "L": "JESSE LAZEAR",
          "MATT": "MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; his clothes are "
                  "described below",
          "GL": "Matt's amber spectacles (the hidden gag)"}
REFS = {"F81": F81, "F00": F00, "R": R, "L": L, "MATT": "kit:matt-sheet.jpg", "GL": "kit:glasses-sheet.jpg"}
HARBOUR_PHOTO = ("Reference 2 is a period photograph used ONLY for the shape of Morro Castle, its lighthouse and the "
                 "harbour mouth; paint it, never copy the photo. ")
V2 = {  # shot: (set, leading refs with their roles, sheet keys)
    "s1a": ("academy", [("ref:plate-academy", STYLE_ONLY.format(n="Academy"))], []),
    "s1b": ("study", [], ["F81"]),
    "s2a": ("harbour", [(STYLE_PLATE, OUTSIDE), ("proj:refs/havana_harbor_1860.jpg", HARBOUR_PHOTO)], []),
    "s2b": ("street", [("ref:plate-street", STYLE_ONLY.format(n="Havana street"))], []),
    "s3": ("study", [], ["F81"]),
    "s4a": ("academy", [("ref:plate-academy", "Reference 1 is the empty Academy hall: this is that hall, seen from the back. ")], ["F81"]),
    "s4b": ("academy", [(STYLE_PLATE, OUTSIDE)], ["MATT"]),  # v3: kf:s4a made it a copy of s4a
    "s5": ("lab", [], ["F81", "GL"]),
    "s6a": ("camp", [], ["R"]),
    "s6b": ("table", [], ["F00", "R"]),
    "s7a": ("ward", [], ["L"]),
    "s7b": ("tent", [(STYLE_PLATE, OUTSIDE)], []),
    "s8a": ("macro", [(STYLE_PLATE, OUTSIDE)], []),
    "s8b": ("study", [], ["F00"]),
    "s9a": ("stage", [], ["R"]),
    "s9b": ("desk", [], ["R"]),
}
for name, (set_id, firsts, sheets) in V2.items():
    k = KEYFRAMES[name]
    k.update(refs=[r for r, _ in firsts] + [REFS[x] for x in sheets], set=set_id,
             roles="".join(role for _, role in firsts)
             + "".join(f"Reference {len(firsts) + j + 1} is {SHEETS[x]}. " for j, x in enumerate(sheets)))
    if sheets:
        k["prompt"] += " " + ONE_EACH


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="Nobody Believed Him About the Mosquito", format="short", dual_format=False,
              image_resolution="2K", loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s5: Matt's spectacles on the shelf beside the larvae jars",
              theme={"culture": "caribbean-colonial", "font": "montserrat"},
              previz_approved="2026-11-14: storyboard v1.1 + pre-viz approved by the user on the storyboard page "
                              "(claude.ai/artifact/Dy34MeUVzxbLtEMi4ujsJC): 'now i can say we go for next'")
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
