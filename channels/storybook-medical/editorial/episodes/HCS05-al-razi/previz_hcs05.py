"""HCS05 al-Razi free pre-viz (no paid call): one blocking frame per shot (with the text zone) and the ward set map.
Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS05-al-razi/previz_hcs05.py
-> projects/hcs05-al-razi/review/previz/<shot>.png + map-ward.png
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from previz import draw_map, render_frames  # noqa: E402

OUT = REPO / "projects/hcs05-al-razi/review/previz"
INK, BRICK, BRICK_D, STUCCO = (30, 30, 34), (186, 150, 106), (140, 104, 70), (226, 212, 186)
LAMP, NIGHT, BED, CLOTH = (240, 190, 90), (54, 44, 40), (150, 110, 80), (236, 228, 210)
BRASS, ROBE, TUNIC, TURBAN = (196, 150, 60), (214, 190, 140), (90, 120, 170), (240, 238, 230)
PAPER, SKY_D, MODERN = (236, 224, 196), (120, 100, 130), (226, 230, 232)

RAZI = {"col": (150, 132, 100)}

SHOTS = [
    {"name": "1a", "zone": "TOP", "text": "c. 900 AD", "shapes": [
        ("rect", 0, 0, 1, 1, (120, 92, 66)), ("poly", [(.1, .05), (.3, .05), (.3, .4), (.1, .4)], BRICK_D),
        ("poly", [(.7, .05), (.9, .05), (.9, .4), (.7, .4)], BRICK_D), ("text", .5, .07, "brick arches, oil lamps"),
        ("rect", 0, .7, .3, .8, BED, "bed"), ("rect", .7, .7, 1, .8, BED, "bed"),
        ("fig", .5, .9, .6, RAZI, "al-Razi, palm raised"), ("line", .58, .5, .7, .44, INK, 6),
        ("fig", .82, .9, .5, {"col": (110, 80, 60)}, "assistant + bowl"), ("ellipse", .72, .55, .84, .6, BRASS)]},
    {"name": "1b", "zone": "LOW", "text": "caption (on the robe, below the beard)", "shapes": [
        ("rect", 0, 0, 1, 1, (90, 70, 54)), ("ellipse", .25, .02, .75, .18, TURBAN), ("text", .5, .04, "white turban"),
        ("ellipse", .3, .12, .7, .38, (200, 160, 120)), ("poly", [(.32, .3), (.68, .3), (.6, .48), (.4, .48)], (30, 26, 24)),
        ("text", .5, .44, "full black beard, knowing look"), ("rect", .1, .48, .9, 1, ROBE), ("rect", .4, .48, .6, 1, TUNIC)]},
    {"name": "2", "zone": "TOP", "text": "REY · al-RAZI", "shapes": [
        ("grad", SKY_D, (230, 170, 120)), ("poly", [(.55, .3), (.75, .12), (.95, .3)], (240, 240, 245)),
        ("text", .75, .08, "Damavand, far"), ("poly", [(0, .45), (.25, .3), (.45, .45)], (150, 120, 90)),
        ("rect", .12, .28, .3, .36, BRICK_D, "citadel"), ("rect", 0, .45, 1, 1, BRICK),
        ("ellipse", .2, .5, .36, .62, BRICK_D), ("rect", .2, .56, .36, .7, BRICK_D),
        ("ellipse", .6, .55, .72, .64, BRICK_D), ("rect", .6, .6, .72, .72, BRICK_D),
        ("text", .5, .8, "patterned brick, plain domes, NO blue tiles"), ("line", .7, .38, .7, .45, (255, 255, 255), 2),
        ("text", .82, .42, "TODAY'S TEHRAN")]},
    {"name": "3", "zone": "TOP", "text": "caption (above the patient)", "shapes": [
        ("rect", 0, 0, 1, 1, (130, 100, 72)), ("rect", 0, .55, .75, .7, BED), ("rect", .05, .5, .7, .58, (180, 150, 120), "young man, fever"),
        ("rect", .08, .47, .22, .52, CLOTH), ("text", .15, .43, "damp cloth"),
        ("fig", .55, .55, .42, {"col": (60, 50, 60), "sitting": True}, "mother"),
        ("rect", .78, .6, 1, .9, (110, 80, 56), "side table"), ("ellipse", .8, .56, .95, .62, BRASS),
        ("line", .82, .64, .96, .64, (200, 200, 200), 2), ("text", .88, .7, "bowl + lancet on cloth")]},
    {"name": "4", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, NIGHT), ("ellipse", .65, .15, .85, .3, LAMP), ("text", .75, .34, "oil lamp"),
        ("fig", .42, .95, .7, {"col": (150, 132, 100), "sitting": True}, "al-Razi, cross-legged"),
        ("rect", .45, .62, .62, .66, PAPER), ("text", .55, .7, "paper on his knee, reed pen paused"),
        ("rect", 0, .9, 1, 1, (120, 40, 40)), ("text", .5, .95, "carpet + cushion (no desk, no chair)"),
        ("rect", .05, .78, .2, .9, PAPER), ("rect", .07, .72, .18, .78, PAPER), ("text", .12, .66, "notebooks"),
        ("ellipse", .75, .84, .82, .88, INK), ("text", .78, .8, "inkwell")]},
    {"name": "5", "zone": "MID", "text": "GROUP A · GROUP B", "shapes": [
        ("rect", 0, 0, 1, 1, (160, 130, 96)), ("rect", .48, 0, .52, 1, (180, 60, 50)), ("text", .5, .03, "curtain"),
        ("rect", .08, .08, .4, .2, BED), ("rect", .08, .3, .4, .42, BED), ("rect", .08, .52, .4, .64, BED),
        ("rect", .08, .74, .4, .86, BED),
        ("ellipse", .4, .1, .46, .14, BRASS), ("ellipse", .4, .32, .46, .36, BRASS),
        ("ellipse", .4, .54, .46, .58, BRASS), ("ellipse", .4, .76, .46, .8, BRASS),
        ("rect", .6, .08, .92, .2, BED), ("rect", .6, .3, .92, .42, BED), ("rect", .6, .52, .92, .64, BED),
        ("rect", .6, .74, .92, .86, BED), ("text", .24, .95, "bowls + bandaged arms"), ("text", .76, .95, "nothing")]},
    {"name": "6", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, NIGHT), ("poly", [(.5, .3), (0, .6), (0, .72)], (110, 84, 60)),
        ("poly", [(.5, .3), (1, .6), (1, .72)], (110, 84, 60)), ("text", .5, .26, "two rows run away from us"),
        ("fig", .4, .98, .55, {"col": (150, 132, 100), "sitting": True}, "al-Razi on a cushion"),
        ("fig", .72, 1.0, .62, {"col": (90, 60, 110)}, "MATT: student + lamp"),
        ("ellipse", .76, .42, .84, .48, LAMP)]},
    {"name": "7a", "zone": "TOP", "text": "KITAB AL-HAWI", "shapes": [
        ("rect", 0, 0, 1, 1, (120, 40, 40)), ("rect", .18, .25, .82, .75, PAPER),
        ("line", .25, .35, .75, .35, INK, 2), ("line", .25, .42, .75, .42, INK, 2), ("line", .25, .49, .75, .49, INK, 2),
        ("text", .5, .58, "angular cursive of the 900s, on paper"),
        ("ellipse", .55, .6, .75, .72, (200, 160, 120)), ("line", .6, .62, .5, .5, (100, 70, 40), 4), ("text", .68, .76, "hand + reed pen"),
        ("rect", 0, .78, .3, 1, PAPER), ("rect", .02, .72, .28, .78, PAPER), ("text", .15, .68, "piles of notebooks"),
        ("ellipse", .07, .8, .23, .86, (232, 163, 61)), ("text", .15, .9, "MATT'S GLASSES")]},
    {"name": "7b", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (240, 210, 160), (190, 150, 110)), ("rect", 0, .65, 1, 1, CLOTH),
        ("ellipse", .25, .5, .7, .7, BRASS), ("line", .65, .72, .95, .7, (200, 200, 200), 4),
        ("text", .5, .4, "dawn: bowl set down by a new bed"), ("ellipse", .15, .52, .3, .56, (200, 160, 120)), ("text", .2, .48, "hand")]},
    {"name": "8", "zone": "MID", "text": "WRONG", "shapes": [
        ("rect", 0, 0, 1, 1, (120, 116, 110)), ("rect", 0, .6, 1, .64, (90, 80, 70), ""),
        ("text", .5, .67, "shelf (grey: colour drained)"),
        ("ellipse", .25, .46, .7, .62, (150, 130, 90)), ("text", .47, .43, "bowl upside down, dusty"),
        ("line", .72, .59, .92, .58, (130, 90, 60), 3), ("text", .85, .54, "rusty lancet")]},
    {"name": "9a", "zone": "MID", "text": "OVERSTATEMENT", "shapes": [
        ("rect", 0, 0, 1, 1, (60, 60, 66)), ("rect", .2, .45, .8, .7, (190, 214, 220), "glass case"),
        ("rect", .3, .52, .7, .64, PAPER, "later manuscript copy"), ("rect", .55, .72, .82, .78, (250, 250, 250)),
        ("text", .68, .82, "card: THE FIRST CLINICAL TRIAL?"), ("fig", .12, .98, .52, {"col": (40, 40, 44)}, "visitor")]},
    {"name": "9b", "zone": "TOP", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, MODERN), ("rect", 0, .65, 1, 1, (200, 206, 210)),
        ("rect", .1, .45, .18, .62, (250, 250, 250), "A"), ("rect", .25, .45, .33, .62, (250, 250, 250), "A"),
        ("rect", .4, .45, .48, .62, (250, 250, 250), "A"),
        ("rect", .1, .7, .18, .87, (250, 250, 250), "B"), ("rect", .25, .7, .33, .87, (250, 250, 250), "B"),
        ("rect", .4, .7, .48, .87, (250, 250, 250), "B"), ("text", .7, .66, "two rows = the two rows of beds")]},
]

WARD = {
    "title": "The ward · north up",
    "blocks": [(100, 80, 460, 900, "", (186, 150, 106)), (540, 80, 900, 900, "", (186, 150, 106)),
               (130, 120, 330, 220, "bed A1", (150, 110, 80)), (130, 320, 330, 420, "bed A2", (150, 110, 80)),
               (130, 520, 330, 620, "bed A3 (shot 3)", (150, 110, 80)), (130, 720, 330, 820, "bed A4", (150, 110, 80)),
               (670, 120, 870, 220, "bed B1", (150, 110, 80)), (670, 320, 870, 420, "bed B2", (150, 110, 80)),
               (670, 520, 870, 620, "bed B3", (150, 110, 80)), (670, 720, 870, 820, "bed B4", (150, 110, 80)),
               (480, 80, 520, 900, "", (180, 60, 50))],
    "landmarks": [(500, 940, "end of ward: al-Razi + Matt (shot 6)")],
    "cameras": [("1a", 500, 650, 180, 50, "MS, facing the entrance"), ("3", 420, 560, 270, 50, "MS at bed A3"),
                ("5", 500, 480, 0, 20, "top-down over the curtain"), ("6", 500, 990, 0, 60, "low, from the end"),
                ("7b", 620, 330, 90, 40, "CU at a B bed")],
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    render_frames(OUT, SHOTS)
    draw_map(WARD, 900).save(OUT / "map-ward.png")
    print(OUT)
