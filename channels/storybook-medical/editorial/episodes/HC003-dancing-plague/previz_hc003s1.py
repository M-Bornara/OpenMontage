"""HC003-S1 Dancing Plague free pre-viz, stage 1 (no paid call; s1-storyboard-v1.md, 2026-11-21).

One blocking sketch per shot -> projects/hc003-s1/review/previz/<shot>.png and the lane map with every camera
(map-lane.png): the lane is in 10 shots, so the map shows that no two consecutive lane shots share a camera (L52).
The approval page (storyboard_page.py hc003s1) shows them beside each row. Stage 2: drawn stand-in pieces for the three
HERO shots (turn / collapse / wagon) and a motion preview on them (hero_previz_hc003s1.py).

    python channels/storybook-medical/editorial/episodes/HC003-dancing-plague/previz_hc003s1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from previz import draw_map, render_frames  # noqa: E402

OUT = REPO / "projects/hc003-s1/review/previz"
INK, SKY, DUSK, DAWN = (30, 30, 34), (196, 210, 222), (92, 70, 120), (150, 170, 200)
TIMBER, PLASTER, COBBLE, GOLD = (92, 62, 40), (222, 204, 168), (128, 120, 108), (236, 190, 110)
BLUE, COIF, SKIN, WOOD = (60, 90, 150), (244, 242, 236), (214, 176, 150), (130, 92, 58)
GREY, PAPER, RED = (128, 132, 128), (226, 214, 186), (170, 50, 40)


def lane(sky=SKY, ground=COBBLE):
    """Half-timbered walls on both sides narrowing to the roof gap, cobbles below."""
    return [("grad", sky, ground),
            ("poly", [(0, 0), (0.3, 0.12), (0.34, 0.62), (0, 0.8)], PLASTER),
            ("poly", [(1, 0), (0.7, 0.12), (0.66, 0.62), (1, 0.8)], PLASTER),
            ("line", 0.1, 0.05, 0.12, 0.72, TIMBER, 5), ("line", 0.9, 0.05, 0.88, 0.72, TIMBER, 5),
            ("line", 0.0, 0.4, 0.33, 0.36, TIMBER, 4), ("line", 1.0, 0.4, 0.67, 0.36, TIMBER, 4),
            ("poly", [(0, 0.8), (0.34, 0.62), (0.66, 0.62), (1, 0.8), (1, 1), (0, 1)], ground)]


SHOTS = [
    {"name": "1", "zone": "LOW", "text": "HOOK CARD A BOTTOM (0-2.5 s)", "shapes": lane() + [
        ("line", 0.5, 0.06, 0.5, 0.16, INK, 3), ("text", 0.5, 0.03, "spire in the roof gap"),
        ("rect", 0.08, 0.2, 0.2, 0.32, WOOD, "shutter swings"),
        ("ellipse", 0.42, 0.2, 0.58, 0.3, COIF), ("ellipse", 0.44, 0.24, 0.56, 0.32, SKIN),
        ("poly", [(0.44, 0.32), (0.56, 0.32), (0.8, 0.86), (0.2, 0.86)], BLUE),
        ("line", 0.45, 0.36, 0.3, 0.28, SKIN, 7), ("line", 0.55, 0.36, 0.7, 0.26, SKIN, 7),
        ("text", 0.5, 0.6, "Troffea MS ~0.7 height, mid-turn"), ("text", 0.5, 0.92, "card over hem + cobbles")]},
    {"name": "2", "zone": "MID", "text": "caption", "shapes": [
        ("grad", (150, 140, 128), COBBLE), ("rect", 0.0, 0.0, 1.0, 0.3, (110, 96, 80)),
        ("poly", [(0.1, 0.55), (0.9, 0.5), (0.9, 0.62), (0.1, 0.66)], BLUE, "hem"),
        ("ellipse", 0.2, 0.7, 0.48, 0.8, WOOD, "shoe ~24 cm"), ("ellipse", 0.52, 0.66, 0.8, 0.76, WOOD),
        ("rect", 0.0, 0.86, 1.0, 0.9, (90, 86, 80), "gutter"), ("text", 0.5, 0.95, "slide with the steps; dust")]},
    {"name": "3", "zone": "LOW", "text": "name tag TOP · caption LOW", "shapes": [
        ("grad", (200, 170, 120), (150, 120, 90)), ("rect", 0.7, 0.2, 0.86, 0.7, (60, 110, 70), "green door"),
        ("ellipse", 0.2, 0.2, 0.8, 0.5, COIF), ("ellipse", 0.26, 0.28, 0.74, 0.72, SKIN),
        ("rect", 0.14, 0.7, 0.86, 1.0, BLUE), ("text", 0.5, 0.5, "eyes far away; turns through frame")]},
    {"name": "4", "zone": "LOW", "text": "caption", "shapes": lane(DUSK, (50, 44, 60)) + [
        ("rect", 0.7, 0.5, 0.78, 0.68, GOLD, "lit door"),
        ("fig", 0.5, 0.7, 0.5, {}, "her silhouette ~0.5 h"), ("ellipse", 0.06, 0.84, 0.34, 0.96, COIF),
        ("text", 0.2, 0.8, "coif falls (FG)"), ("text", 0.5, 0.1, "dusk; on 'collapsed' -> fallen")]},
    {"name": "5", "zone": "MID", "text": "stamp DAY 2 TOP", "shapes": [
        ("grad", GOLD, (150, 120, 80)), ("rect", 0.8, 0.5, 1.0, 1.0, (160, 150, 130), "doorstep"),
        ("ellipse", 0.22, 0.62, 0.5, 0.74, WOOD, "shoe, laces strained"), ("ellipse", 0.5, 0.66, 0.76, 0.78, WOOD),
        ("poly", [(0.18, 0.5), (0.8, 0.46), (0.8, 0.58), (0.18, 0.62)], BLUE, "hem"),
        ("text", 0.5, 0.92, "tilt up; cold -> gold")]},
    {"name": "6", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (230, 214, 170), (170, 150, 120)), ("rect", 0.0, 0.0, 0.16, 1.0, (40, 30, 24)),
        ("rect", 0.0, 0.0, 1.0, 0.06, (40, 30, 24)), ("ellipse", -0.2, 0.5, 0.42, 1.2, (90, 60, 40), "husband's back"),
        ("line", 0.3, 0.62, 0.52, 0.52, SKIN, 10), ("fig", 0.7, 0.78, 0.5, {}, "she turns away"),
        ("text", 0.5, 0.94, "rack focus hand -> her")]},
    {"name": "7", "zone": "LOW", "text": "stamp DAY 3 TOP", "shapes": lane() + [
        ("fig", 0.5, 0.74, 0.14, {}, "Troffea"), ("fig", 0.2, 0.86, 0.34, {}), ("fig", 0.28, 0.82, 0.28, {}),
        ("fig", 0.8, 0.86, 0.34, {}), ("fig", 0.72, 0.82, 0.28, {}), ("fig", 0.36, 0.78, 0.2, {}),
        ("rect", 0.74, 0.18, 0.86, 0.28, (240, 230, 200), "MATT"), ("text", 0.5, 0.95, "5 faces max; the rest backs")]},
    {"name": "8", "zone": "MID", "text": "caption · Dutch tilt", "shapes": [
        ("grad", (150, 140, 128), COBBLE), ("rect", 0.1, 0.0, 0.2, 0.7, (70, 60, 50)), ("rect", 0.3, 0.0, 0.42, 0.7, (90, 60, 40)),
        ("rect", 0.7, 0.0, 0.84, 0.68, BLUE), ("ellipse", 0.3, 0.68, 0.58, 0.78, (50, 40, 34), "buckled shoe taps"),
        ("text", 0.5, 0.9, "tilt 0 -> 8 deg")]},
    {"name": "9", "zone": "LOW", "text": "stamp 30+ MID", "shapes": [
        ("grad", DUSK, (60, 50, 70)), ("rect", 0.0, 0.0, 0.12, 1.0, (50, 40, 50)), ("rect", 0.88, 0.0, 1.0, 1.0, (50, 40, 50)),
        ("ellipse", 0.4, 0.4, 0.6, 0.5, (110, 110, 120), "fountain"),
        *[("ellipse", x, y, x + 0.05, y + 0.03, INK) for x, y in
          [(0.2, 0.2), (0.3, 0.3), (0.5, 0.25), (0.7, 0.3), (0.25, 0.6), (0.45, 0.65), (0.65, 0.58), (0.75, 0.7),
           (0.35, 0.8), (0.55, 0.85), (0.2, 0.75), (0.8, 0.5)]],
        ("text", 0.5, 0.95, "from a roof; no faces")]},
    {"name": "10", "zone": "LOW", "text": "stamp TO SAVERNE TOP", "shapes": [
        ("grad", SKY, COBBLE), ("poly", [(0.3, 0.1), (0.7, 0.1), (0.7, 0.5), (0.3, 0.5)], (150, 140, 120)),
        ("ellipse", 0.38, 0.18, 0.62, 0.5, (90, 90, 96), "gate"),
        ("rect", 0.15, 0.5, 0.8, 0.68, WOOD, "wagon ~0.6 w"), ("ellipse", 0.2, 0.62, 0.36, 0.78, (60, 44, 30)),
        ("ellipse", 0.58, 0.62, 0.74, 0.78, (60, 44, 30)),
        ("fig", 0.62, 0.92, 0.45, {}, "two men lift her (0.45 h)"), ("fig", 0.5, 0.92, 0.42, {}), ("fig", 0.74, 0.92, 0.44, {}),
        ("text", 0.5, 0.06, "on 'shrine' the wagon rolls out L")]},
    {"name": "11", "zone": "LOW", "text": "caption · SILENT hold", "shapes": lane((170, 172, 176), (110, 108, 104)) + [
        ("line", 0.5, 0.06, 0.5, 0.16, INK, 3), ("line", 0.4, 1.0, 0.47, 0.64, (90, 84, 76), 3),
        ("line", 0.6, 1.0, 0.53, 0.64, (90, 84, 76), 3), ("text", 0.5, 0.92, "wheel tracks; wagon gone"),
        ("fig", 0.42, 0.7, 0.14, {}), ("fig", 0.5, 0.68, 0.12, {}), ("fig", 0.58, 0.71, 0.14, {}), ("fig", 0.46, 0.66, 0.1, {})]},
    {"name": "12a", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (60, 44, 30), (30, 22, 16)), ("rect", 0.12, 0.14, 0.88, 0.86, PAPER, "folio page ~28x40 cm"),
        ("rect", 0.3, 0.26, 0.7, 0.5, (150, 130, 100), "woodcut"), ("line", 0.9, 0.9, 0.56, 0.56, SKIN, 14),
        ("text", 0.6, 0.94, "finger taps the page")]},
    {"name": "12b", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", SKY, (180, 160, 120)), ("rect", 0.0, 0.6, 1.0, 0.72, WOOD, "stage boards"),
        ("fig", 0.3, 0.6, 0.42, {}, "carpenter"), ("fig", 0.7, 0.6, 0.38, {}, "carpenter"),
        ("line", 0.34, 0.3, 0.42, 0.22, INK, 5), ("text", 0.5, 0.9, "hammers; sawdust")]},
    {"name": "12c", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (180, 140, 90), (120, 90, 60)), ("ellipse", 0.2, 0.36, 0.8, 0.86, (220, 200, 160), "frame drum ~45 cm"),
        ("line", 0.9, 0.2, 0.56, 0.5, WOOD, 8), ("fig", 0.8, 0.5, 0.3, {}, "shawm"), ("text", 0.5, 0.94, "stick strikes")]},
    {"name": "13", "zone": "LOW", "text": "counter 400* MID", "shapes": [
        ("grad", (170, 160, 140), (150, 140, 120)), ("rect", 0.4, 0.42, 0.6, 0.54, WOOD, "stage"),
        ("poly", [(0.0, 0.2), (1.0, 0.7), (1.0, 0.76), (0.0, 0.26)], (120, 110, 100)),
        *[("ellipse", 0.05 + (i % 9) * 0.1, 0.1 + (i // 9) * 0.1, 0.08 + (i % 9) * 0.1, 0.12 + (i // 9) * 0.1, INK)
          for i in range(81) if not (3 <= i % 9 <= 5 and 3 <= i // 9 <= 4)],
        ("text", 0.5, 0.96, "top-down; spire shadow; pull out")]},
    {"name": "14", "zone": "LOW", "text": "caption · END LINE", "shapes": lane(DAWN, (110, 110, 120)) + [
        ("rect", 0.08, 0.2, 0.22, 0.32, WOOD, "shutter open"), ("ellipse", 0.3, 0.84, 0.62, 0.96, COIF, "her coif"),
        ("text", 0.5, 0.1, "empty; blue -> gold; pull out")]},
]

LANE = {
    "title": "The lane: 11 cameras (spire N, gate S)",
    "blocks": [(150, 60, 420, 820, "west houses", (196, 170, 130)), (580, 60, 850, 820, "east houses (hers at the doorstep)", (196, 170, 130)),
               (150, 840, 850, 990, "square + city gate (wagon)", (214, 208, 196)),
               (580, 500, 620, 560, "", (244, 238, 226))],
    "streets": [(420, 40, 580, 840, "cobbles")],
    "landmarks": [(500, 10, "spire (far, over the roofs)"), (600, 530, "her door")],
    "cameras": [
        ("1", 500, 420, 0, 40, "MS, facing N"), ("2", 470, 480, 90, 20, "ECU ground, E"),
        ("3", 530, 360, 225, 14, "MCU, SW"), ("4", 500, 150, 200, 50, "MWS low, dusk"),
        ("5", 560, 600, 0, 30, "CU ground, N"), ("6", 600, 530, 270, 40, "OTS from her door, W"),
        ("7", 500, 90, 180, 40, "WS from the N end, crowd"), ("8", 520, 580, 0, 20, "ECU feet, N"),
        ("10", 500, 860, 180, 40, "MWS at the S end, the gate"), ("11", 500, 800, 0, 40, "WS from the S end, N"),
        ("14", 470, 130, 180, 45, "WS low, dawn, S"),
    ],
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(len(render_frames(OUT, SHOTS)), "sketches")
    draw_map(LANE, 900).save(OUT / "map-lane.png")
    from PIL import Image   # row 12 is three quick inserts: one strip for the page (12a | 12b | 12c)
    parts = [Image.open(OUT / f"12{x}.png").convert("RGB") for x in "abc"]
    strip = Image.new("RGB", (sum(i.width for i in parts), parts[0].height), "white")
    for k, im in enumerate(parts):
        strip.paste(im, (k * parts[0].width, 0))
    strip.save(OUT / "12.png")
    print(OUT)
