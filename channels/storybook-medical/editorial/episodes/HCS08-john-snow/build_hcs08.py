"""HCS08 John Snow: writes projects/hcs08-john-snow/episode.json (title, narration, references, keyframes) from
storyboard-v1.md (script v2), with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS08-john-snow/build_hcs08.py
Then:  episode.py refs hcs08-john-snow --batch   ->   episode.py keyframes hcs08-john-snow --batch
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, WAVY_WRITING, camera, cast, framing, glasses_gag,  # noqa: E402
                        lint_all, matt_beat, set_block)

PID = "hcs08-john-snow"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

# script v2 (storyboard-v1.md): three small trims of the approved v1, facts unchanged
NARRATION = """[curious] In 1854, a doctor stopped a deadly outbreak… by taking the handle off a water pump.
London, Soho. Cholera killed about five hundred people in ten days.
Most doctors blamed bad air.
John Snow blamed the water. He went door to door, listing every death.
They clustered around one pump… on Broad Street.
The brewery next door had no cases. The workers drank beer.
A widow miles away died too. She liked the taste of Broad Street water… and had it brought to her.
On the eighth of September, they took the handle off.
[mischievously] The twist? The outbreak was already fading. Snow admitted it himself.
[curious] But his map of those deaths… is how we still hunt diseases today."""

# ── people ────────────────────────────────────────────────────────────────────────────────────────────────────────
SNOW = ("JOHN SNOW, the doctor (41, clean-shaven, dark brown hair swept back and thinning at the temples, a lean serious "
        "searching face; a black frock coat, a dark waistcoat, a white shirt with a black cravat)")
WIDOW = "an elderly widow (70s, a kind lined face, a black silk dress, a white lace cap)"

# ── the pump: one object in every shot it appears in ─────────────────────────────────────────────────────────────
PUMP = ("the Broad Street pump: a tall black cast-iron street pump about as high as a man, a fluted column with a "
        "rounded cap and a short spout, a long curved iron handle, standing on a low stone base at the edge of the "
        "pavement with a small stone trough under the spout. ORIENTATION (fixed in every shot): the spout and trough "
        "face OUT over the road, toward Broad Street (south); the long curved handle sticks out on the pump's WEST side, "
        "along the pavement, where a person standing on the pavement works it")

# ── sets ──────────────────────────────────────────────────────────────────────────────────────────────────────────
ROOFS = set_block("Soho, London, seen from above", "late summer 1854",
                  "soot-dark brick terraces packed tight, slate roofs, rows of chimney pots smoking, a church spire; a "
                  "thick brown-grey fog lying in the streets, a pale sun")
STREET = set_block("Broad Street, Soho", "September 1854",
                   "narrow street of soot-dark four-storey brick houses with shops below, gas lamps, cobbles, wooden "
                   "shutters; brown-grey haze, flat light")
BREWERY = set_block("The cellar of the Broad Street brewery", "1854",
                    "brick vaults, rows of huge oak barrels, a wooden trestle table, warm oil-lamp light, golden and "
                    "cosy, a world away from the sick street")
HAMPSTEAD = set_block("Hampstead, on a green hill north of London", "1854",
                      "a quiet detached Georgian brick house with a white door and a small garden, green trees, clean "
                      "air; far away on the horizon the brown smoke of London")
PARLOUR = set_block("The widow's parlour in Hampstead", "1854",
                    "a small comfortable Victorian sitting room, floral wallpaper, a lace-covered table, a window with "
                    "soft daylight")
STUDY = set_block("John Snow's study at night", "1854-1855",
                  "a cluttered desk, a brass oil lamp with a warm glow, stacks of papers and books, a window with night "
                  "outside")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only
SHEET = "Reference 1 shows our character model-sheet layout and painting style only (not this person). "

REFERENCES = {
    "sheet-snow": dict(aspect="16:9", refs=[SHEET_LAYOUT], roles=SHEET,
        prompt=f"Clean character model sheet on plain bone-white paper: {SNOW}, London, 1854. Front view, "
               "three-quarter view, profile view, back view, plus three head close-ups (studying something closely, "
               "quietly determined, a small honest smile). Same scale in every view. No text, labels or watermark."),
    "plate-broad-street": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free room plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{STREET} Vertical frame looking down the street, with {PUMP} on the left pavement in the near middle "
               "ground, clearly seen. EMPTY location plate: no people. Three clear depth layers. "
               f"{PERIOD} {NO_TEXT}"),
}

S = "ref:sheet-snow"
STYLE = "Reference 1 is the Broad Street plate, for the painting style, palette and the pump's exact design ONLY: do NOT copy its composition or camera angle. "
LOOK = ("Reference 1 is the Broad Street plate, for the painting style and palette ONLY: do NOT copy its composition, "
        "camera position or angle; this is a different view. ")

# ── the set map (L36, user 2026-11-09): one fixed geography; every street shot says where the camera stands, which
# way it faces and exactly what is behind. Drawn in review/previz-street.png before any image is paid for. ──────────
MAP = ("GEOGRAPHY: Broad Street runs west to east; Cambridge Street crosses it north to south. The pump stands at the kerb "
       "on the NORTH-WEST corner of that crossroads, in front of the corner house (a soot-dark brick house with a shuttered "
       "ground-floor shop and a gas lamp on a bracket). The brewery is on the north side of Broad Street, just east of the "
       "crossroads.")
# v3 street shots: the plate (one fixed camera view) is no longer a reference; style comes from the rooftop shot s1a,
# the pump's design from a crop of the plate that shows only the pump
STREET_LOOK = ("Reference 1 is an earlier shot of this film, for the painting style, palette and fog colour ONLY: do NOT "
               "copy its composition or camera position. ")
PUMP_REF = "proj:assets/images/refs/prop-pump.png"
PUMP_ROLE = "Reference 2 shows the pump's exact design ONLY (ignore the street behind it). "

KEYFRAMES = {
    "s1a": dict(aspect="9:16", refs=["ref:plate-broad-street"],
        roles=STYLE,
        prompt=f"{ROOFS} {framing('ELS', 'high angle over the rooftops', '24 mm', 'a deadly outbreak hangs over a crowded city', 'ominous, hushed')} "
               f"{camera('on a high rooftop west of Soho', 'east over the rooftops', 'chimney pots and slate roofs in rows, a church spire, a narrow street far below lost in fog')} "
               "Chimney pots and roofs fill the foreground; one narrow street below, empty, lost in fog. The top 20% "
               f"is hazy brown sky. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user): v1 was the plate again with a bigger pump
    "s1b": dict(aspect="9:16", resolution="4K", refs=["kf:s1a", PUMP_REF],
        roles=STREET_LOOK + PUMP_ROLE,
        prompt=f"{STREET} {MAP} {framing('CU', 'very low angle, looking up', '50 mm', 'the pump at the heart of the story stands silent', 'mysterious, heavy')} "
               f"{camera('low in the road at the kerb, close to the pump', 'north, straight at the corner house', 'the flat brick front of the corner house: one tall shuttered ground-floor shop window and an iron gas-lamp bracket, with fog and pale sky above the roofline; no street receding, no other houses', 'the pump stands in the centre, filling the frame from the stone trough at the bottom to its rounded cap near the top; its spout and trough face us, and the long curved handle is on the LEFT of the column (its west side, along the pavement)')} "
               f"{PUMP}. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user): v1 and v2 still read as the plate's street
    "s2": dict(aspect="9:16", refs=["kf:s1a"],
        roles=STREET_LOOK,
        prompt=f"{STREET} {MAP} {framing('LS', 'eye level, straight-on and flat to the house fronts', '35 mm', 'cholera has emptied the street', 'grief, silence')} "
               f"{camera('on the north pavement of Broad Street, west of the crossroads, back to the houses behind', 'south, square-on to the houses across the street', 'three narrow front doors side by side across the whole frame, each with stone steps and a black crepe mourning bow; closed shutters on every window above; no street receding into the distance, no sky except a strip at the top', 'the pump is NOT in view')} "
               f"{cast('a woman in a black mourning dress and shawl, sitting on the steps of the middle door, head bowed, hands in her lap')} "
               f"No bodies, no sick people. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user): v1 put the doctors in front of the plate's street and pump
    "s3": dict(aspect="9:16", refs=["kf:s1a"],
        roles=STREET_LOOK,
        prompt=f"{STREET} {framing('MS', 'eye level', '50 mm, shallow focus', 'the doctors of the day blame foul air', 'disgust, self-importance')} "
               f"{camera('in the middle of Cambridge Street, north of the crossroads', 'south, into thick fog', 'a soft out-of-focus wall of brown-green fog, one gas lamp glowing through it on the left and the faint dark outline of a church spire; no houses in focus, no street receding', 'the pump is NOT in view')} "
               f"{cast('a portly Victorian physician in a top hat and grey frock coat pressing a white handkerchief to his nose', 'a thin Victorian physician in a top hat and black coat holding a small posy of flowers to his nose')} "
               "A faint sickly green fog curls around their legs and shoulders. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4a": dict(aspect="9:16", resolution="4K", refs=["ref:plate-broad-street", S],
        roles=STYLE + "Reference 2 is JOHN SNOW (same face, hair and clothes). ",
        prompt=f"{STUDY} {framing('CU', 'eye level', '85 mm, shallow focus', 'Snow suspects the water, not the air', 'sharp curiosity, one eyebrow down')} "
               f"{camera('beside the desk', 'the window', 'the tall window with the town outside, the lamp and papers on the desk')} "
               f"{cast(SNOW + ', head and shoulders, holding a clear glass of slightly cloudy water up between his face and the window, studying it')} "
               f"Daylight from the window behind the glass. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user): v1 stood on the plate's street with the pump in the wrong place (far down the middle of the road)
    "s4b": dict(aspect="9:16", refs=["kf:s1a", S],
        roles=STREET_LOOK + "Reference 2 is JOHN SNOW (same face, hair and clothes). ",
        prompt=f"{STREET} {MAP} {framing('OTS', 'eye level, from inside the house', '28 mm', 'Snow goes door to door, counting the dead', 'patient, methodical, sad')} "
               f"{camera('inside the dark narrow hallway of a house on Cambridge Street, behind the woman who opens the door', 'west, out through the open front door', 'the bright doorway framed by the dark hallway walls; through it only the soot-dark brick fronts of the houses across Cambridge Street, soft and out of focus in the haze', 'the pump is NOT in view')} "
               f"{cast('a tired woman in a plain dress and apron, seen from behind at the left edge: her shoulder, her hair in a bun and her hand on the door', SNOW + ', standing on the front step in the doorway facing her, a small notebook open, pencil in hand, listening gently')} "
               f"A black crepe bow hangs on the outside of the open door. {WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 image kept (user OK): camera line added for L36 only
    "s5": dict(aspect="9:16", refs=["ref:plate-broad-street"],
        roles=STYLE,
        prompt=f"{STREET} {MAP} {framing('ELS', 'high angle from a rooftop, about 45 degrees down', '24 mm', 'the deaths cluster around one pump', 'a pattern revealed')} "
               f"{camera('on a rooftop at the south-east corner of the crossroads', 'north-west, down onto the crossroads', 'the four streets meeting, the corner houses with black crepe bows on their doors')} "
               f"A crossroads of four streets: {PUMP} small at the north-west corner. On the house fronts all "
               "around it, many front doors carry black crepe mourning bows ON THE DOORS, most near the pump, fewer "
               "and fewer further down each street. The cobbles are empty and clean. "
               f"{NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6": dict(aspect="9:16", refs=["ref:plate-broad-street", "kit:matt-sheet.jpg"],
        roles=STYLE + "Reference 2 is MATT: copy his face, amber round spectacles, teal scarf and amber notebook only; "
              "his clothes are described below. ",
        prompt=f"{BREWERY} {framing('MS', 'eye level', '35 mm', 'the brewery workers stay healthy: they drink beer, not pump water', 'cheerful, hearty')} "
               f"{camera('at the end of the trestle table', 'along the table toward the back vault', 'rows of huge oak barrels under a brick vault, a lamp on the wall')} "
               "CROWD: exactly three brewery workers in shirtsleeves, leather aprons and caps, laughing and raising "
               "pewter tankards of beer at the trestle table; nobody else except Matt. "
               f"{matt_beat('a brown Victorian jacket and flat cap', 'leaning on a barrel at the side holding a tankard, writing in his notebook')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7a": dict(aspect="9:16", refs=["ref:plate-broad-street"],
        roles=STYLE,
        prompt=f"{HAMPSTEAD} {framing('LS', 'eye level', '35 mm', 'far from Soho, death has reached one quiet house', 'still, sad, puzzling')} "
               f"{camera('on the lane below the house', 'north, up the green hill', 'the house on the hill, trees, and far away on the right horizon the brown smoke of London')} "
               "The house in the centre: one upstairs window shuttered, a black mourning wreath on the white door. "
               f"{NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7b": dict(aspect="9:16", refs=["ref:plate-broad-street"],
        roles=STYLE,
        prompt=f"{PARLOUR} {framing('MS', 'eye level', '50 mm', 'she drinks the Broad Street water she loves, brought all the way to her', 'innocent pleasure, quietly ominous')} "
               f"{camera('just inside the parlour door', 'the window', 'the window with soft daylight, floral wallpaper, the lace-covered table')} "
               f"{cast(WIDOW + ', sitting in an armchair in the centre, smiling as she raises a glass of water', 'a carter in a cap and work coat setting a big brown stoneware water jug on the lace table beside her')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user): v1 was the plate's street again, and the workman looked like he was hammering the handle
    "s8": dict(aspect="9:16", refs=["kf:s1a", PUMP_REF, S, "kit:glasses-sheet.jpg"],
        roles=STREET_LOOK + PUMP_ROLE + "Reference 3 is JOHN SNOW. Reference 4 shows Matt's amber spectacles. ",
        prompt=f"{STREET} {MAP} {framing('MS', 'low angle', '28 mm', 'the parish takes the handle off the pump', 'a decisive, quiet moment')} "
               f"{camera('low on the south-east corner of the crossroads', 'north-west, across the crossroads at the pump', 'the open crossroads behind the pump: the corner house with its shuttered shop, Broad Street leading away to the left and Cambridge Street leading away to the right, black crepe bows on several doors', 'the pump stands close in the left third of the frame, the same pump as the crossroads seen from above; its spout and trough face the road toward the lower left, and the empty handle pivot is on the LEFT side of the column (its west side), where the handle was')} "
               f"{PUMP}. "
               f"{cast('a workman in shirtsleeves and a cap, on the pavement just right of the pump, walking toward the right carrying the long curved iron handle in both hands, already detached, a large spanner sticking out of his back pocket', SNOW + ', standing a little behind on the right, watching intently', 'a parish official in a top hat beside Snow, arms folded')} "
               "Nobody hammers or strikes anything: the handle has been unbolted and is being carried off. "
               f"{glasses_gag('folded on the edge of the small stone trough under the spout')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 image kept (user OK): camera line added for L36 only
    "s9a": dict(aspect="9:16", refs=["ref:plate-broad-street"],
        roles=LOOK,
        prompt=f"{STREET} {framing('LS', 'high angle, from a first-floor window looking down across the street at the houses opposite', '35 mm', 'the outbreak was already fading on its own', 'relief, life returning')} "
               f"{camera('at a first-floor window on the south side of Broad Street', 'north and down', 'the sunlit house fronts opposite, a doorstep and the pavement below')} "
               "Bright golden morning sun, the fog gone, clear sky light on the brick. Shutters are open; one door still "
               "has a black mourning bow. "
               f"{cast('a small child sitting on a doorstep below', 'a woman opening the shutters of a window opposite', 'a man walking past with a basket of bread')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9b": dict(aspect="9:16", refs=["ref:plate-broad-street", S],
        roles=STYLE + "Reference 2 is JOHN SNOW. ",
        prompt=f"{STUDY} {framing('MCU', 'eye level', '50 mm', 'Snow writes, honestly, that the outbreak was already fading', 'a small rueful honest smile')} "
               f"{camera('across the desk from him', 'Snow at his desk', 'bookshelves, the lamp and the dark night window behind him')} "
               f"{cast(SNOW + ', at the desk writing in a large bound book with a pen, looking up for a moment')} "
               f"{WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s10": dict(aspect="9:16", resolution="4K", refs=["ref:plate-broad-street", S],
        roles=STYLE + "Reference 2 is JOHN SNOW (his hand and cuff only). ",
        prompt=f"{STUDY} {framing('INSERT', 'top-down, looking straight down at the desk', '50 mm', 'the map that founded epidemiology', 'discovery')} "
               f"{camera('above the desk', 'straight down', 'the map on the desk top')} "
               "A large hand-drawn street map on cream paper fills the frame: thin ink lines for the streets, no names; "
               "small black bars stacked along the streets like little towers, tallest and thickest around one small "
               "pump symbol in the centre and thinning out further away. Snow's hand with a pen at the lower edge, his "
               f"black cuff. The lamp's warm glow. {WAVY_WRITING} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}


# v5 (user, 2026-11-10: "s8 looks like wrong direction for pump"): v3 put the pump on the CAMERA's corner, with the
# corner house across the street behind it; on the map the pump stands in front of the corner house. (A v4 edit of v3
# fixed the leftover handle curl and the spanner but not the corner.) New camera: in the road just in front of the pump.
KEYFRAMES["s8"] = dict(aspect="9:16", refs=["kf:s1a", PUMP_REF, S, "kit:glasses-sheet.jpg"],
    roles=STREET_LOOK + PUMP_ROLE + "Reference 3 is JOHN SNOW. Reference 4 shows Matt's amber spectacles. ",
    prompt=f"{STREET} {MAP} {framing('MS', 'low angle', '28 mm', 'the parish takes the handle off the pump', 'a decisive, quiet moment')} "
           f"{camera('in the road a few steps south-east of the pump, low', 'north-west, at the pump and the corner house right behind it', 'the corner of the corner house directly behind the pump: its corner edge in the middle of the frame, its Broad Street front turning away on the left and its Cambridge Street front turning away on the right, a shuttered shop on the ground floor; beyond the corner, Broad Street disappears into fog on the far left and Cambridge Street on the far right, black crepe bows on two doors', 'the pump stands on the pavement right against the corner house, a little left of centre, NOT on the near side of any street')} "
           f"{PUMP}. Seen from here its spout and stone trough face the camera and the road; on the LEFT side of the column "
           "there is only a small empty iron pivot where the handle was fixed. "
           f"{cast('a workman in shirtsleeves and a cap, on the pavement just right of the pump, walking toward the right carrying the long curved black iron pump handle in both hands across his body, a large spanner tucked in his back pocket', SNOW + ', standing on the pavement on the right by the house wall, watching intently', 'a parish official in a top hat beside Snow, arms folded')} "
           "Nobody hammers or strikes anything: the handle has been unbolted and is being carried off. "
           f"{glasses_gag('folded on the edge of the small stone trough under the spout')} "
           f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}")

# v6: v5 got the corner right (pump against the corner house) but drew the handle still attached, on the RIGHT, same side
# as the spout. EDIT v5 to the approved plan (L33): handle detached and carried, empty pivot on the LEFT.
KEYFRAMES["s8"] = dict(aspect="9:16", refs=["proj:assets/images/keyframes/s8.v5.keep.png", PUMP_REF],
    roles="Reference 1 is the finished image to EDIT. Reference 2 shows the pump's exact design ONLY (handle on the "
          "opposite side of the column from the spout). ",
    prompt="EDIT this exact image; change only the pump handle and the workman's hands. The long curved iron handle is "
           "NO LONGER attached to the pump: remove it from the pump completely. On the LEFT side of the pump column, near "
           "the top, opposite the spout, there is only a small empty iron pivot bracket. The workman, in the same place "
           "and the same walking pose, now holds the detached long curved black iron handle in both hands across his "
           "body, carrying it away to the right; it touches nothing. The spout stays on the right side of the column. "
           "Everything else stays identical: the pump column, cap, spout, trough and its place on the corner kerb, the "
           "corner house, the street, Snow and the official, the folded amber spectacles on the trough, the light, the "
           "colours, the framing, the painting style. "
           f"SHOT: unchanged medium shot. {camera('in the road a few steps south-east of the pump, low', 'north-west, at the pump and the corner house right behind it', 'unchanged from reference 1')} "
           "FRAMING: unchanged; every story-relevant person, object and action sits inside the central 70% of the frame. "
           "CAMEO: none needed in this shot.")

def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="The Doctor Who Stopped a Plague by Breaking a Pump", format="short", dual_format=False,
              image_resolution="2K", loop=True, tail_seconds=1.0, references=REFERENCES, keyframes=KEYFRAMES,
              glasses="s8: Matt's spectacles on the pump's stone trough",
              theme={"culture": "victorian-london", "font": "montserrat"})
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
