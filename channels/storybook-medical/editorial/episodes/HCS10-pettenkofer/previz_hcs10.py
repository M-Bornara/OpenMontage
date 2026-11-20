"""HCS10 Pettenkofer free pre-viz, stage 1 (no paid call; storyboard-v1.md, 2026-11-20).

One blocking sketch per shot -> projects/hcs10-pettenkofer/review/previz/<shot>.png and the lab's set map with every
camera (map-lab.png): the lab is in 9 shots, so the map shows that no two consecutive lab shots share a camera (L52).
The approval page (storyboard_page.py hcs10) shows them beside each row. Stage 2, after the storyboard OK: drawn
stand-in pieces for the four HERO shots (glass, hand, pose sheets) and a motion preview on them.

    python channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/previz_hcs10.py
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from previz import draw_map, render_frames  # noqa: E402

OUT = REPO / "projects/hcs10-pettenkofer/review/previz"
INK, WALL, DARK, LAMP = (30, 30, 34), (92, 70, 52), (52, 40, 32), (232, 163, 61)
WIN, COAT, SKIN, GLASS = (176, 190, 196), (36, 34, 38), (214, 176, 150), (200, 226, 232)
GREY, STREET, PAPER, WOOD = (128, 132, 128), (110, 112, 110), (226, 214, 186), (120, 84, 56)
WHITE = (236, 232, 222)

SHOTS = [
    {"name": "1", "zone": "TOP", "text": "HOOK CARD A (0-2.5 s)", "shapes": [
        ("grad", DARK, WALL), ("ellipse", 0.62, 0.3, 1.0, 0.62, LAMP),
        ("ellipse", 0.2, 0.36, 0.72, 0.7, SKIN), ("rect", 0.12, 0.66, 0.84, 1.0, COAT),
        ("rect", 0.36, 0.6, 0.5, 0.78, GLASS, "glass"), ("poly", [(1.0, 0.62), (0.7, 0.66), (0.7, 0.72), (1.0, 0.74)], SKIN),
        ("text", 0.47, 0.48, "his face + glass ~1/2 of frame"), ("text", 0.82, 0.8, "student's hand reaches in"),
        ("text", 0.43, 0.88, "glass rises to his lips")]},
    {"name": "2", "zone": "MID", "text": "stamp ≈ 8,600 · HAMBURG 1892", "shapes": [
        ("grad", (170, 174, 176), STREET), ("poly", [(0, 0.2), (0.28, 0.3), (0.3, 1), (0, 1)], (90, 86, 84)),
        ("poly", [(1, 0.2), (0.72, 0.3), (0.7, 1), (1, 1)], (90, 86, 84)), ("line", 0.5, 0.06, 0.5, 0.3, INK, 2),
        ("rect", 0.4, 0.55, 0.62, 0.66, WOOD, "water cart"), ("fig", 0.36, 0.72, 0.1, {}), ("fig", 0.3, 0.74, 0.1, {}),
        ("fig", 0.25, 0.76, 0.1, {}, "queue"), ("text", 0.5, 0.2, "masts + the Elbe in haze"),
        ("text", 0.5, 0.9, "fog drifts; empty street")]},
    {"name": "3a", "zone": "TOP", "text": "caption · name tag Koch", "shapes": [
        ("grad", (150, 140, 120), (80, 70, 60)), ("rect", 0.0, 0.0, 0.22, 0.6, WIN),
        ("ellipse", 0.3, 0.3, 0.74, 0.62, SKIN), ("rect", 0.24, 0.6, 0.86, 1.0, COAT),
        ("ellipse", 0.38, 0.5, 0.64, 0.66, (190, 190, 190)), ("rect", 0.14, 0.34, 0.26, 0.5, GLASS, "flask"),
        ("text", 0.52, 0.72, "Koch: grey beard, spectacles")]},
    {"name": "3b", "zone": "TOP", "text": "caption · name tag Pettenkofer, 73", "shapes": [
        ("grad", (120, 100, 80), (70, 56, 44)), ("poly", [(0, 0.42), (1, 0.3), (1, 0.4), (0, 0.52)], WOOD),
        ("poly", [(0, 0.55), (1, 0.43), (1, 0.53), (0, 0.65)], WOOD), ("fig", 0.5, 1.02, 0.68, {}, "Pettenkofer, finger up"),
        ("rect", 0.32, 0.72, 0.68, 1.0, WOOD, "lectern"), ("line", 0.62, 0.4, 0.66, 0.3, SKIN, 6),
        ("text", 0.5, 0.2, "low angle, empty benches behind")]},
    {"name": "4", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", WALL, DARK), ("rect", 0.0, 0.1, 0.16, 0.6, WIN), ("rect", 0.2, 0.62, 0.9, 0.7, WOOD, "bench"),
        ("fig", 0.55, 0.66, 0.36, {}, "Pettenkofer: palm up on 'no'"), ("rect", 0.5, 0.58, 0.54, 0.62, GLASS),
        ("fig", 0.86, 0.5, 0.16, {}, "MATT"), ("ellipse", -0.15, 0.62, 0.38, 1.12, COAT),
        ("ellipse", 0.62, 0.66, 1.15, 1.15, COAT), ("text", 0.5, 0.94, "two students' backs (soft)")]},
    {"name": "5a", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", WOOD, (100, 70, 48)), ("ellipse", 0.28, 0.36, 0.72, 0.6, GLASS),
        ("line", 0.62, 0.3, 0.86, 0.12, (180, 180, 180), 10), ("rect", 0.08, 0.66, 0.3, 0.8, (200, 200, 200), "soda tin"),
        ("text", 0.5, 0.48, "top-down: powder falls in"), ("ellipse", 0.78, 0.8, 1.05, 1.05, (150, 120, 60))]},
    {"name": "5b", "zone": "MID", "text": "stamp LESS THAN A TEASPOON", "shapes": [
        ("grad", (110, 100, 90), (60, 50, 44)), ("rect", 0.3, 0.52, 0.7, 0.98, GLASS, "glass (side, macro)"),
        ("poly", [(0.62, 0.18), (0.86, 0.26), (0.62, 0.42), (0.5, 0.36)], GLASS), ("line", 0.54, 0.4, 0.5, 0.56, WHITE, 3),
        ("text", 0.72, 0.14, "culture flask tips")]},
    {"name": "6", "zone": "LOW", "text": "caption · quote stamp MID", "shapes": [
        ("grad", WIN, (140, 150, 156)), ("ellipse", 0.3, 0.2, 0.7, 0.56, SKIN), ("rect", 0.22, 0.54, 0.84, 1.0, COAT),
        ("rect", 0.64, 0.3, 0.76, 0.46, GLASS, "glass"), ("text", 0.5, 0.62, "profile against the window"),
        ("text", 0.5, 0.12, "on 'gulp': head back")]},
    {"name": "7", "zone": "LOW", "text": "caption · stamp 2 DAYS LATER TOP", "shapes": [
        ("grad", (120, 128, 120), (80, 88, 82)), ("poly", [(0, 0.3), (1, 0.24), (1, 1), (0, 1)], (110, 96, 80)),
        ("rect", 0.1, 0.36, 0.5, 0.56, PAPER, "papers"), ("rect", 0.66, 0.3, 0.78, 0.44, GLASS),
        ("poly", [(0.3, 0.62), (0.7, 0.58), (0.74, 0.7), (0.32, 0.74)], SKIN), ("text", 0.52, 0.8, "his hand grips the edge"),
        ("text", 0.5, 0.15, "high angle; face out of frame; colour drains")]},
    {"name": "8", "zone": "LOW", "text": "caption · stamp 1 WEEK TOP", "shapes": [
        ("grad", PAPER, (200, 186, 156)), ("ellipse", 0.14, 0.3, 0.86, 0.7, (240, 236, 220)),
        ("text", 0.5, 0.5, "Meyers plate c.1885: comma bacilli"), ("text", 0.5, 0.78, "a lens slides over it")]},
    {"name": "9", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", (210, 196, 160), WALL), ("rect", 0.0, 0.08, 0.14, 0.7, (240, 226, 190)), ("rect", 0.34, 0.04, 0.92, 0.62, WOOD, "bookcase"),
        ("rect", 0.1, 0.66, 0.9, 0.76, WOOD, "desk"), ("fig", 0.58, 0.8, 0.5, {"sitting": True}, "writing, a faint smile"),
        ("rect", 0.2, 0.6, 0.26, 0.66, GLASS), ("text", 0.5, 0.92, "morning sun rises")]},
    {"name": "10", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (110, 96, 80), (60, 50, 42)), ("poly", [(0, 0.3), (1, 0.3), (1, 0.38), (0, 0.38)], WOOD),
        ("poly", [(0, 0.5), (1, 0.5), (1, 0.58), (0, 0.58)], WOOD), *[("fig", 0.1 + 0.16 * i, 0.5, 0.12, {}) for i in range(6)],
        ("fig", 0.5, 0.74, 0.22, {}, "a critic stands, points"), ("text", 0.5, 0.15, "high angle from the back rows")]},
    {"name": "11", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", (70, 52, 40), (40, 30, 24)), ("ellipse", 0.62, 0.12, 0.8, 0.26, LAMP), ("rect", 0.26, 0.3, 0.74, 0.96, GLASS, "glass (side, macro)"),
        ("ellipse", 0.4, 0.5, 0.44, 0.54, WHITE), ("ellipse", 0.55, 0.62, 0.59, 0.66, WHITE),
        ("ellipse", 0.47, 0.72, 0.5, 0.75, WHITE), ("text", 0.5, 0.2, "dark room + lamp behind; bubbles; green tint")]},
    {"name": "12", "zone": "LOW", "text": "caption · END LINE", "shapes": [
        ("grad", (70, 60, 56), (40, 34, 32)), ("rect", 0.0, 0.1, 0.2, 0.56, (90, 100, 110)),
        ("rect", 0.3, 0.58, 0.78, 0.64, WOOD, "far bench"), ("ellipse", 0.6, 0.36, 0.76, 0.5, LAMP),
        ("fig", 0.52, 0.64, 0.22, {}, "alone, ~1/4 height"), ("text", 0.5, 0.86, "dusk; hold")]},
]

LAB = {
    "title": "The Munich lab (top view): 9 shots, 9 cameras",
    "blocks": [(0, 0, 40, 1000, "", (176, 190, 196)), (40, 0, 1000, 30, "", (120, 100, 80)),
               (80, 150, 270, 330, "", (196, 170, 130)),
               (330, 400, 720, 520, "", (196, 170, 130)), (780, 120, 960, 260, "shelves", (170, 150, 120)),
               (860, 820, 1000, 960, "door", (150, 130, 110)),
               (80, 345, 300, 385, "his desk: 6, 7, 9, 11, 12", (244, 238, 226))],
    "landmarks": [(560, 450, "bench: shots 1, 4, 5a, 5b"), (175, 240, ""), (20, 560, "tall windows")],
    # his desk: shots 6, 7, 9, 11, 12 (label below the block)
    "cameras": [
        ("1", 500, 640, 0, 28, "CU, 85 mm"), ("4", 600, 820, 345, 50, "OTS over 2 students"),
        ("5a", 470, 560, 0, 20, "top-down over the glass"), ("5b", 760, 460, 270, 18, "side macro"),
        ("6", 430, 240, 270, 26, "profile, window behind"), ("7", 300, 120, 225, 40, "high angle on the hand"),
        ("9", 470, 380, 315, 44, "MS, the bookcase corner"), ("11", 300, 280, 90, 14, "side macro, into the room"),
        ("12", 900, 700, 300, 50, "WS from the door, dusk"),
    ],
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(len(render_frames(OUT, SHOTS)), "sketches")
    draw_map(LAB, 900).save(OUT / "map-lab.png")
    print(OUT)
