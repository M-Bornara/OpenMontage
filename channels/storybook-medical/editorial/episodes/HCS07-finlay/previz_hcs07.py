"""HCS07 Finlay free pre-viz (no paid call): one blocking frame per shot (with the text zone) and the Academy hall set
map. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS07-finlay/previz_hcs07.py
-> projects/hcs07-finlay/review/previz/<shot>.png + map-academy.png
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from previz import draw_map, render_frames  # noqa: E402

OUT = REPO / "projects/hcs07-finlay/review/previz"
INK, SKY, SEA = (30, 30, 34), (196, 214, 222), (92, 140, 160)
LIME, OCHRE, BLUEW, STONE = (226, 216, 190), (206, 170, 110), (150, 180, 196), (176, 166, 146)
COAT, WOOD, AMBER, NIGHT = (36, 34, 38), (120, 84, 54), (232, 163, 61), (40, 44, 58)
TENT, PALM, GLASS = (236, 232, 220), (60, 110, 70), (190, 214, 210)

SHOTS = [
    {"name": "1a", "zone": "TOP", "text": "19 YEARS", "shapes": [
        ("rect", 0, 0, 1, 1, (84, 72, 62)),
        ("rect", 0, .35, 1, .5, COAT), ("rect", .05, .4, .95, .46, (58, 54, 58), "crossed arms 1"),
        ("rect", 0, .55, 1, .7, COAT), ("rect", .05, .6, .95, .66, (58, 54, 58), "crossed arms 2"),
        ("rect", 0, .75, 1, .9, COAT), ("rect", .05, .8, .95, .86, (58, 54, 58), "crossed arms 3"),
        ("line", .3, .52, .5, .56, (212, 175, 55), 3), ("text", .5, .97, "faces cropped above frame")]},
    {"name": "1b", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (240, 230, 200), (200, 186, 150)),
        ("ellipse", .25, .2, .45, .3, (150, 130, 110)), ("ellipse", .55, .2, .75, .3, (150, 130, 110)),
        ("text", .5, .14, "Finlay's eyes + round spectacles, soft focus"),
        ("rect", .28, .32, .72, .82, GLASS, "glass jar"), ("rect", .26, .3, .74, .34, (140, 140, 140)),
        ("line", .44, .55, .56, .55, INK, 3), ("ellipse", .48, .53, .52, .57, INK), ("text", .5, .62, "mosquito")]},
    {"name": "2a", "zone": "TOP", "text": "HAVANA · 1881", "shapes": [
        ("grad", SKY, (230, 230, 220)), ("rect", 0, .38, 1, .62, SEA),
        ("poly", [(.55, .38), (.95, .3), (1, .38)], STONE), ("rect", .82, .18, .86, .32, LIME, ""),
        ("text", .82, .14, "Morro + lighthouse"),
        ("poly", [(.15, .5), (.3, .5), (.27, .54), (.18, .54)], WOOD), ("line", .22, .38, .22, .5, INK, 2),
        ("rect", .22, .38, .27, .41, (230, 200, 40)), ("text", .24, .34, "ship: yellow quarantine flag"),
        ("rect", 0, .62, 1, 1, OCHRE), ("rect", .05, .66, .3, .8, LIME), ("rect", .35, .7, .6, .86, BLUEW),
        ("rect", .65, .66, .95, .82, LIME), ("text", .5, .93, "flat lime-washed roofs, slow push in")]},
    {"name": "2b", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", SKY, (240, 236, 220)),
        ("poly", [(0, .1), (.4, .3), (.4, .8), (0, 1)], OCHRE), ("poly", [(1, .1), (.6, .3), (.6, .8), (1, 1)], BLUEW),
        ("rect", .05, .35, .17, .6, (90, 70, 56), "shut"), ("ellipse", .09, .37, .13, .41, INK),
        ("text", .11, .3, "crepe bow"), ("rect", .82, .38, .94, .55, (70, 70, 74)), ("text", .88, .58, "iron grille"),
        ("rect", .2, .6, .36, .72, COAT, "carriage"),
        ("fig", .7, .9, .28, {}, "crossing away"), ("fig", .77, .92, .26, {}),
        ("text", .5, .2, "street goes away; no sick people shown")]},
    {"name": "3", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, NIGHT), ("ellipse", .7, .1, 1.1, .5, (120, 100, 60)), ("text", .82, .2, "lamp"),
        ("fig", .45, 1.2, 1.05, {"col": COAT}, "Finlay 1881 (MCU)"),
        ("rect", 0, .78, 1, 1, WOOD), ("ellipse", .35, .7, .6, .78, (226, 196, 170)),
        ("ellipse", .45, .7, .5, .74, INK), ("text", .48, .68, "mosquito on his hand")]},
    {"name": "4a", "zone": "TOP", "text": "ACADEMY OF SCIENCES", "shapes": [
        ("rect", 0, 0, 1, 1, STONE), ("poly", [(.05, .1), (.25, .1), (.25, .55), (.05, .55)], (210, 202, 182)),
        ("poly", [(.4, .1), (.6, .1), (.6, .55), (.4, .55)], (210, 202, 182)),
        ("poly", [(.75, .1), (.95, .1), (.95, .55), (.75, .55)], (210, 202, 182)),
        ("text", .5, .06, "convent arches, tall shuttered windows"),
        ("rect", .44, .6, .56, .72, WOOD, "lectern"), ("fig", .5, .74, .2, {}, "Finlay"),
        ("rect", 0, .8, 1, .86, WOOD), ("rect", 0, .9, 1, .96, WOOD), ("text", .5, .99, "benches (backs of heads)")]},
    {"name": "4b", "zone": "TOP", "text": "caption (above the faces)", "shapes": [
        ("rect", 0, 0, 1, 1, STONE),
        ("fig", .15, .55, .26, {"col": COAT}), ("fig", .35, .55, .26, {"col": COAT}), ("fig", .55, .55, .26, {"col": COAT}),
        ("fig", .75, .55, .26, {"col": COAT}), ("rect", 0, .55, 1, .6, WOOD),
        ("fig", .25, .95, .42, {"col": COAT}, "arms crossed"), ("fig", .5, .95, .42, {"col": COAT}, "hand fan"),
        ("fig", .8, .98, .5, {"col": (90, 60, 110)}, "MATT leans in"), ("rect", 0, .9, 1, .96, WOOD)]},
    {"name": "5", "zone": "TOP", "text": "1881 → 1900 counter", "shapes": [
        ("rect", 0, 0, 1, 1, (210, 196, 166)), ("rect", .62, .05, .98, .55, (240, 236, 220), "window"),
        ("rect", 0, .2, .55, .23, WOOD), ("rect", 0, .4, .55, .43, WOOD),
        ("rect", .05, .12, .14, .2, GLASS), ("rect", .2, .12, .29, .2, GLASS), ("rect", .35, .12, .44, .2, GLASS),
        ("rect", .05, .32, .14, .4, GLASS), ("rect", .2, .32, .29, .4, GLASS), ("text", .27, .47, "jars: larvae, gauze tops"),
        ("ellipse", .3, .62, .5, .7, (226, 196, 170)), ("rect", .34, .52, .46, .64, GLASS, "jar"),
        ("text", .4, .74, "his hands lift a jar to the light"),
        ("ellipse", .08, .5, .2, .54, AMBER), ("text", .14, .58, "MATT'S GLASSES")]},
    {"name": "6a", "zone": "TOP", "text": "1900 · WALTER REED", "shapes": [
        ("grad", SKY, (236, 230, 200)), ("line", .1, .1, .12, .5, PALM, 5), ("ellipse", .02, .05, .22, .15, PALM),
        ("line", .9, .08, .88, .5, PALM, 5), ("ellipse", .78, .02, .98, .12, PALM),
        ("poly", [(.15, .5), (.25, .38), (.35, .5)], TENT), ("poly", [(.4, .48), (.5, .36), (.6, .48)], TENT),
        ("poly", [(.65, .5), (.75, .38), (.85, .5)], TENT), ("line", .5, .2, .5, .36, INK, 2),
        ("rect", .5, .2, .57, .24, (180, 40, 50)), ("rect", 0, .5, 1, 1, (196, 178, 130)),
        ("fig", .5, .98, .55, {"col": (40, 46, 70)}, "Reed (front)"), ("fig", .3, .85, .38, {"col": (40, 46, 70)}),
        ("fig", .7, .85, .38, {"col": (40, 46, 70)}), ("text", .5, .4, "low angle: they walk toward us")]},
    {"name": "6b", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, WOOD), ("rect", 0, .25, .55, .4, (240, 236, 220), "Finlay's white cuff"),
        ("ellipse", .45, .26, .62, .4, (226, 196, 170)), ("rect", .55, .3, .75, .34, GLASS), ("text", .65, .27, "glass tube of eggs"),
        ("ellipse", .68, .28, .85, .42, (226, 196, 170)), ("rect", .8, .25, 1, .42, (40, 46, 70), "army sleeve"),
        ("text", .5, .7, "top-down over the table")]},
    {"name": "7a", "zone": "TOP", "text": "JESSE LAZEAR", "shapes": [
        ("rect", 0, 0, 1, 1, (224, 220, 206)), ("rect", 0, .6, 1, 1, (200, 196, 182)),
        ("fig", .4, 1.15, .95, {"col": (60, 60, 64)}, "Lazear (beard), MCU"),
        ("rect", .45, .62, 1, .7, (226, 196, 170), "patient's forearm only"),
        ("rect", .6, .5, .66, .63, GLASS), ("text", .63, .46, "test tube on the arm"),
        ("ellipse", .3, .66, .42, .74, (226, 196, 170)), ("ellipse", .34, .67, .38, .7, INK),
        ("text", .36, .8, "a stray mosquito lands on HIS hand")]},
    {"name": "7b", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, (120, 104, 80)), ("poly", [(0, 0), (.5, .1), (1, 0)], TENT),
        ("rect", .62, .1, .98, .5, (150, 120, 90)), ("line", .8, .15, .8, .45, PALM, 4), ("text", .8, .08, "flap open: palms, dusk"),
        ("rect", .1, .6, .7, .7, (210, 204, 186), "empty cot"), ("rect", .35, .55, .55, .6, (80, 90, 70), "folded uniform + cap"),
        ("rect", .8, .55, .84, .65, (240, 230, 200)), ("ellipse", .79, .5, .85, .55, AMBER), ("text", .82, .72, "candle")]},
    {"name": "8a", "zone": "MID", "text": "DOCUMENTED", "shapes": [
        ("grad", (240, 180, 80), (190, 110, 40)), ("line", .2, .5, .8, .5, INK, 8),
        ("poly", [(.45, .5), (.3, .3), (.5, .45)], (60, 50, 40)), ("poly", [(.55, .5), (.7, .3), (.5, .45)], (60, 50, 40)),
        ("line", .35, .5, .2, .7, INK, 3), ("line", .5, .5, .5, .75, INK, 3), ("line", .65, .5, .8, .7, INK, 3),
        ("text", .5, .85, "macro silhouette, wings lit")]},
    {"name": "8b", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, (200, 186, 160)), ("rect", .45, .05, .98, .5, SKY, "window: Havana roofs"),
        ("fig", .32, 1.0, .75, {"col": (220, 214, 196)}, "Finlay 1900, linen suit"),
        ("rect", .4, .5, .55, .58, (250, 246, 236), "letter")]},
    {"name": "9a", "zone": "LOW", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, (70, 50, 50)), ("poly", [(0, .1), (.5, .2), (1, .1)], (180, 40, 50)),
        ("text", .5, .07, "bunting"), ("fig", .5, .7, .55, {"col": (40, 46, 70)}, "Reed on stage (low angle)"),
        ("rect", 0, .7, 1, 1, WOOD), ("ellipse", .05, .2, .25, .35, (255, 255, 230)), ("text", .15, .4, "flash"),
        ("fig", .15, 1.05, .35, {}, "photographer"), ("fig", .85, 1.05, .35, {})]},
    {"name": "9b", "zone": "TOP", "text": "caption", "shapes": [
        ("rect", 0, 0, 1, 1, WOOD), ("rect", .1, .1, .9, .9, (246, 240, 224)),
        ("line", .18, .3, .8, .3, (120, 120, 120), 2), ("line", .18, .38, .8, .38, (120, 120, 120), 2),
        ("line", .18, .46, .8, .46, (120, 120, 120), 2), ("text", .45, .53, "... the theory of Dr. Finlay ..."),
        ("line", .3, .57, .62, .57, (180, 40, 50), 3), ("line", .62, .58, .85, .75, INK, 6), ("text", .8, .8, "Reed's pen")]},
]

ACADEMY = {
    "title": "Academy hall · north up",
    "blocks": [(0, 0, 1000, 120, "tall shuttered windows", (210, 202, 182)),
               (380, 160, 620, 280, "LECTERN", (150, 110, 70)),
               (100, 420, 900, 500, "bench row 1", (170, 130, 90)), (100, 560, 900, 640, "bench row 2", (170, 130, 90)),
               (100, 700, 900, 780, "bench row 3", (170, 130, 90))],
    "landmarks": [(500, 220, "Finlay"), (820, 450, "Matt (row 1, right)")],
    "cameras": [("1a", 300, 360, 180, 30, "CU arms, row 1"), ("4a", 500, 930, 0, 50, "LS from the back"),
                ("4b", 500, 300, 180, 60, "reverse from the lectern")],
}


# -- story v2 (approved 2026-11-15): new + redone shots; the redo names replace their v1 sketches ----------------------
V2_SHOTS = [
    {"name": "1c", "zone": "TOP", "text": "caption (above the mosquito)", "shapes": [
        ("grad", (90, 60, 30), (240, 170, 70)), ("ellipse", .55, .1, .95, .45, (255, 210, 120)), ("text", .75, .5, "lamp glow, blurred"),
        ("poly", [(0, .72), (1, .62), (1, .9), (0, 1)], (200, 150, 110)), ("text", .5, .88, "forearm"),
        ("ellipse", .4, .48, .6, .58, INK), ("line", .42, .56, .32, .66, INK, 2), ("line", .58, .56, .68, .64, INK, 2),
        ("line", .45, .5, .3, .4, (240, 240, 240), 2), ("line", .55, .5, .7, .4, (240, 240, 240), 2),
        ("text", .5, .45, "mosquito lands, backlit")]},
    {"name": "2c", "zone": "TOP", "text": "caption (on the wall, above the door)", "shapes": [
        ("rect", 0, 0, 1, 1, OCHRE), ("rect", .3, .25, .7, .8, WOOD, "door"), ("ellipse", .45, .2, .55, .27, INK),
        ("text", .5, .17, "black bow"), ("fig", .5, .8, .45, {"col": INK}, "woman, hand to mouth"),
        ("poly", [(.05, .62), (.65, .55), (.67, .62), (.07, .7)], (150, 110, 70)), ("text", .35, .53, "plain coffin"),
        ("fig", .62, 1.0, .5, {"col": (90, 60, 40)}, "big bald man, front"), ("fig", .1, 1.0, .5, {"col": (220, 210, 180)}, "young man, back"),
        ("rect", .78, .7, 1, .9, WOOD, "cart"), ("fig", .9, .72, .28, {"col": (200, 200, 190), "sitting": True}, "old driver")]},
    {"name": "4b", "zone": "TOP", "text": "caption (on the wall, above the faces)", "shapes": [
        ("rect", 0, 0, 1, 1, LIME), ("rect", .35, .1, .65, .45, WOOD, "arched door (south wall)"),
        ("rect", 0, .5, 1, .62, (60, 58, 62), "back rows: dim, out of focus"),
        ("fig", .18, 1.0, .5, {"col": COAT, "sitting": True}, "1 old bald, shakes head"),
        ("fig", .4, 1.0, .5, {"col": COAT, "sitting": True}, "2 young, smirk"),
        ("fig", .62, 1.0, .52, {"col": COAT, "sitting": True}, "3 heavy, turns away"),
        ("fig", .85, 1.0, .5, {"col": (226, 210, 170), "sitting": True}, "MATT, writing")]},
    {"name": "5b", "zone": "LOW", "text": "caption (on the jars)", "shapes": [
        ("rect", 0, 0, 1, 1, (140, 110, 80)), ("rect", .75, .05, .98, .55, (250, 240, 210), "window"),
        ("rect", 0, .55, 1, .6, WOOD), ("rect", 0, .75, 1, .8, WOOD),
        ("rect", .05, .45, .13, .55, GLASS), ("rect", .2, .45, .28, .55, GLASS), ("rect", .35, .45, .43, .55, GLASS),
        ("rect", .5, .45, .58, .55, GLASS), ("rect", .65, .45, .73, .55, GLASS), ("text", .4, .42, "row of larvae jars"),
        ("fig", .32, .98, .7, {"col": (60, 58, 62)}, "Finlay 1881, sleeves rolled"), ("ellipse", .4, .34, .5, .42, (170, 100, 60)),
        ("text", .55, .3, "pitcher pours")]},
    {"name": "6a", "zone": "LOW", "text": "caption (on the quay stones)", "shapes": [
        ("rect", 0, 0, 1, .45, SKY), ("rect", 0, .35, 1, .5, SEA), ("rect", 0, .5, 1, 1, STONE),
        ("rect", .55, .25, .95, .45, (60, 60, 60), "steam launch"), ("rect", .8, .1, .84, .25, (40, 40, 40)),
        ("fig", .3, .95, .7, {"col": (40, 50, 90)}, "REED steps ashore"), ("fig", .52, .95, .62, {"col": (150, 130, 90)}, "stocky bald, khaki"),
        ("fig", .7, .95, .6, {"col": (240, 236, 220)}, "young Cuban, white suit"), ("fig", .9, .95, .66, {"col": (80, 60, 50)}, "dockworker + crate"),
        ("rect", .84, .3, .98, .38, WOOD)]},
]
SHOTS = [s for s in SHOTS if s["name"] not in {x["name"] for x in V2_SHOTS} | {"1a", "2b"}] + V2_SHOTS
ACADEMY["cameras"] = [c for c in ACADEMY["cameras"] if c[0] != "1a"]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    render_frames(OUT, SHOTS)
    draw_map(ACADEMY, 900).save(OUT / "map-academy.png")
    print(OUT)
