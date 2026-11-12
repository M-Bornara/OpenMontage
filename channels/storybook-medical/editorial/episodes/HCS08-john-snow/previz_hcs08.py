"""HCS08 free pre-viz (no paid call): the Broad Street set map with every street camera, and planned blocking frames for
the five v3 shots next to the rejected v1 images. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS08-john-snow/previz_hcs08.py
-> projects/hcs08-john-snow/review/previz-street.jpg
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from previz import render  # noqa: E402

PROJ = REPO / "projects/hcs08-john-snow"
HOUSE, CORNER, BREW, INK = (176, 150, 128), (140, 105, 85), (214, 170, 90), (30, 30, 34)
BRICK, DARK, FOG_T, FOG_B = (110, 78, 62), (42, 36, 34), (196, 190, 174), (150, 142, 126)

MAP = {
    "title": "Broad Street set map (north up) · camera = dot, view = cone",
    "streets": [(0, 430, 1000, 570, "BROAD STREET"), (430, 0, 570, 1000, "CAMBRIDGE STREET")],
    "blocks": [(0, 0, 430, 430, "houses", HOUSE), (570, 0, 1000, 430, "houses", HOUSE),
               (0, 570, 430, 1000, "houses", HOUSE), (570, 570, 1000, 1000, "houses", HOUSE),
               (280, 290, 430, 430, "corner house (shuttered shop)", CORNER),
               (620, 280, 900, 430, "BREWERY", BREW)],
    "landmarks": [(405, 452, "PUMP (handle on its west side, spout to the road)")],
    "cameras": [
        ("v1", 110, 452, 90, 40, "v1: every old street shot looked from here", True),
        ("1b", 395, 530, 0, 44, "s1b"),
        ("2", 200, 445, 180, 50, "s2"),
        ("3", 500, 120, 180, 40, "s3"),
        ("4b", 650, 270, 270, 40, "s4b"),
        ("5", 690, 690, 315, 60, "s5 (kept)"),
        ("8", 500, 520, 315, 60, "s8"),
        ("9a", 790, 600, 0, 50, "s9a (kept)"),
    ],
}

SHOTS = [
    {"name": "s1b", "camera": "CU, very low, facing NORTH at the corner house. Behind the pump: only the flat brick front "
                              "of the corner house (shuttered shop, gas lamp) and fog. No street going away. Spout + trough face us, handle on the LEFT (west, along the pavement).",
     "shapes": [("grad", FOG_T, FOG_B), ("rect", 0, .12, 1, .9, BRICK, "corner house front"),
                ("rect", .58, .32, .94, .74, (72, 60, 55), "shutters"),
                ("line", .03, .3, .2, .3, INK, 5), ("ellipse", .14, .26, .23, .37, (240, 200, 120)),
                ("rect", 0, .9, 1, 1, (125, 118, 108)), ("pump", .5, .97, .86, "left"),
                ("text", .5, .05, "fog / pale sky")]},
    {"name": "s2", "camera": "LS, eye level, FLAT-ON, facing SOUTH at the houses across Broad Street (west end). Three "
                             "doors with mourning bows fill the frame, widow on the middle steps. Pump NOT in view.",
     "shapes": [("grad", FOG_T, FOG_B), ("rect", 0, .05, 1, .8, BRICK),
                ("rect", .08, .12, .26, .3, (72, 60, 55)), ("rect", .41, .12, .59, .3, (72, 60, 55)),
                ("rect", .74, .12, .92, .3, (72, 60, 55)),
                ("rect", .07, .42, .27, .78, DARK), ("rect", .40, .42, .60, .78, DARK), ("rect", .73, .42, .93, .78, DARK),
                ("ellipse", .14, .44, .2, .48, (0, 0, 0)), ("ellipse", .47, .44, .53, .48, (0, 0, 0)),
                ("ellipse", .8, .44, .86, .48, (0, 0, 0)),
                ("rect", .05, .78, .29, .82, (120, 115, 108)), ("rect", .38, .78, .62, .82, (120, 115, 108)),
                ("rect", .71, .78, .95, .82, (120, 115, 108)), ("rect", 0, .82, 1, 1, (135, 128, 118)),
                ("fig", .5, .86, .32, {"sitting": True}, "widow in black"),
                ("text", .5, .94, "pump NOT in view")]},
    {"name": "s3", "camera": "MS, eye level, in Cambridge Street facing SOUTH into thick fog. Behind the doctors: only "
                             "fog, one gas lamp glow, a faint spire. No houses in focus, no pump.",
     "shapes": [("grad", (160, 170, 145), (112, 118, 98)), ("ellipse", .03, .22, .25, .44, (232, 214, 150)),
                ("poly", [(.62, .04), (.67, .32), (.57, .32)], (128, 134, 118)),
                ("fig", .3, 1.02, .8, {"hat": True}, "doctor + handkerchief"),
                ("fig", .72, 1.02, .84, {"hat": True}, "doctor + posy"),
                ("text", .5, .5, "green fog")]},
    {"name": "s4b", "camera": "OTS from INSIDE the hallway, facing WEST out of the open door. Woman's back in the "
                              "foreground, Snow on the step with his notebook, the houses across Cambridge Street "
                              "blurred. Pump NOT in view.",
     "shapes": [("rect", 0, 0, 1, 1, (48, 40, 36)), ("rect", .3, .1, .84, .82, (186, 172, 152), "houses across, blurred"),
                ("rect", .3, .82, .84, .86, (120, 115, 108)),
                ("fig", .6, .84, .62, {}, "Snow + notebook"),
                ("fig", .1, 1.2, 1.1, {"col": (18, 16, 15)}, "woman (back)")]},
    {"name": "s8", "camera": "v5 PLAN. MS, low, standing in the road a few steps from the pump, facing NORTH-WEST. The pump "
                             "stands in FRONT of the corner house; the house's corner edge is right behind it, Broad Street "
                             "going away on the left, Cambridge Street on the right. Spout + trough face the road (toward "
                             "us); empty handle pivot on the pump's west side (left); the workman walks right carrying the "
                             "handle; Snow + official on the right pavement; glasses on the trough.",
     "shapes": [("grad", FOG_T, FOG_B),
                ("poly", [(.18, .16), (.5, .26), (.5, .74), (.18, .7)], BRICK),
                ("poly", [(.5, .26), (.82, .16), (.82, .7), (.5, .74)], (128, 92, 72)),
                ("text", .34, .3, "corner house (Broad St side)"), ("text", .66, .3, "(Cambridge St side)"),
                ("poly", [(0, .62), (.18, .7), (.18, .76), (0, .8)], (150, 142, 128)),
                ("poly", [(.82, .7), (1, .62), (1, .8), (.82, .76)], (150, 142, 128)),
                ("text", .1, .58, "Broad St"), ("text", .91, .58, "Cambridge St"),
                ("rect", 0, .76, 1, 1, (140, 132, 120)),
                ("pump", .42, .9, .6, "none"), ("rect", .44, .82, .54, .9, (110, 110, 110)),
                ("ellipse", .47, .81, .51, .83, (230, 170, 40)),
                ("fig", .66, .97, .44, {}, "workman + handle"), ("line", .56, .72, .78, .69, INK, 6),
                ("fig", .84, .86, .32, {}, "Snow"), ("fig", .94, .86, .33, {"hat": True}, "official")]},
]

if __name__ == "__main__":
    out = render(PROJ / "review/previz-street.jpg", MAP, SHOTS, PROJ / "assets/images/keyframes")
    print(out)
