"""HC002-S1 Gage free pre-viz (no paid call; storyboard s1-storyboard-v1.md, approved 2026-11-18 for the HERO pre-viz).

1. one blocking sketch per shot -> projects/hc002-s1/review/previz/<shot>.png (the approval page shows them);
2. drawn STAND-IN pieces for the three HERO shots (plan/layered-animation.md §7 step 3: the motion is approved on
   stand-ins, then the paid pieces replace them with the same names and keys):
     shot 1  plates/s1-empty.free.png       the rock cut, sky, smoke; no Gage, no bar
             sprites/iron/                  the tamping iron (one state, point to the RIGHT; the actor spins it)
             sprites/gage-s1/               Gage as a silhouette: stand / thrown (pivot at the boots)
             sprites/hat/                   his hat
     shot 4  plates/s4-empty.free.png       the pit seen over two crewmen's shoulders; no Gage
             sprites/gage-s4/               Gage, bar in both hands: down (eyes on the bar) / turn (over his shoulder)
     shot 8  plates/s8-empty.free.png       the rock floor in settling smoke; no Gage
             sprites/gage-s8/               Gage from behind his right shoulder: lie / fingers / prop (on the elbow)
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/previz_hc002s1.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from previz import render_frames  # noqa: E402

P = REPO / "projects/hc002-s1"
IMG = P / "assets/images"
W, H = 1080, 1920
INK, SKY, ROCK, DIRT = (30, 30, 34), (214, 208, 192), (96, 96, 100), (150, 128, 100)
HILL, AUT, SMOKE, SKIN = (120, 112, 80), (184, 120, 60), (170, 164, 152), (214, 170, 140)
SHIRT, COAT, IRON, AMBER = (230, 226, 214), (60, 52, 48), (44, 44, 48), (232, 163, 61)

# ── 1. blocking sketches (frame fractions; zones = where the caption / card sits) ────────────────────────────────────
SHOTS = [
    {"name": "1", "zone": "TOP", "text": "HOOK CARD (A)", "shapes": [
        ("grad", SKY, (200, 190, 170)), ("poly", [(0, 0.3), (0.2, 0.4), (0.26, 1), (0, 1)], ROCK),
        ("poly", [(1, 0.28), (0.8, 0.42), (0.76, 1), (1, 1)], ROCK), ("ellipse", 0.1, 0.62, 0.7, 0.95, SMOKE),
        ("line", 0.42, 0.52, 0.68, 0.38, IRON, 7), ("fig", 0.3, 0.88, 0.22, {}, "Gage thrown back"),
        ("text", 0.6, 0.47, "the bar spins up; slow motion at the top")]},
    {"name": "2a", "zone": "TOP", "text": "caption · stamp VERMONT", "shapes": [
        ("grad", SKY, AUT), ("poly", [(0, 0.62), (1, 0.55), (1, 1), (0, 1)], ROCK),
        ("fig", 0.5, 0.9, 0.5, {"hat": True}, "Gage, arm up (low angle)"), ("line", 0.62, 0.55, 0.7, 0.4, INK, 4),
        ("text", 0.5, 0.52, "name tag y 1000")]},
    {"name": "2b", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (200, 196, 176), AUT), ("poly", [(0.25, 0.35), (0.75, 0.35), (0.62, 1), (0.38, 1)], ROCK),
        ("fig", 0.36, 0.62, 0.07, {}), ("fig", 0.46, 0.66, 0.07, {}), ("fig", 0.56, 0.62, 0.07, {}),
        ("fig", 0.5, 0.36, 0.06, {"hat": True}, "Gage on the rim"), ("fig", 0.86, 0.5, 0.1, {"hat": True}, "contractor")]},
    {"name": "3", "zone": "TOP", "text": "caption · stamp MID 3 ft 7 in", "shapes": [
        ("grad", (120, 116, 110), (80, 78, 76)), ("ellipse", 0.42, 0.6, 0.58, 0.66, INK),
        ("poly", [(0.6, 0.28), (0.72, 0.3), (0.56, 0.58), (0.5, 0.56)], (110, 90, 70)),
        ("line", 0.62, 0.92, 0.82, 0.3, IRON, 9), ("text", 0.5, 0.75, "powder pours; the bar slides in")]},
    {"name": "4", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", SKY, HILL), ("poly", [(0, 0.66), (1, 0.6), (1, 1), (0, 1)], ROCK),
        ("fig", 0.6, 0.72, 0.42, {"hat": True}, "Gage turns his head"), ("line", 0.58, 0.45, 0.58, 0.74, IRON, 6),
        ("ellipse", -0.1, 0.72, 0.4, 1.1, (40, 38, 40)), ("ellipse", 0.65, 0.76, 1.15, 1.12, (40, 38, 40)),
        ("text", 0.5, 0.94, "two crewmen's backs (soft)")]},
    {"name": "5", "zone": "TOP", "text": "caption · FLASH", "shapes": [
        ("grad", (110, 104, 98), (70, 66, 62)), ("line", 0.5, 0.0, 0.5, 0.6, IRON, 16),
        ("ellipse", 0.38, 0.56, 0.62, 0.66, (255, 230, 150)), ("text", 0.5, 0.75, "one spark, white flash")]},
    {"name": "6", "zone": "LOW", "text": "caption", "shapes": [
        ("grad", (236, 226, 200), (220, 206, 176)), ("ellipse", 0.2, 0.25, 0.8, 0.62, (200, 190, 168)),
        ("line", 0.36, 0.56, 0.6, 0.18, AMBER, 5), ("text", 0.5, 0.7, "Harlow 1868 engraving; the path draws on")]},
    {"name": "7", "zone": "TOP", "text": "caption · stamp 80 ft", "shapes": [
        ("grad", SKY, (150, 150, 100)), ("poly", [(0, 0.5), (1, 0.45), (1, 1), (0, 1)], (130, 140, 90)),
        ("line", 0.55, 0.62, 0.6, 0.78, IRON, 6), ("fig", 0.2, 0.62, 0.06, {}), ("fig", 0.28, 0.6, 0.06, {}),
        ("text", 0.6, 0.85, "the bar lands point-first, dust puff")]},
    {"name": "8", "zone": "LOW", "text": "caption on 'he spoke'", "shapes": [
        ("grad", SMOKE, (110, 104, 98)), ("poly", [(0, 0.66), (1, 0.62), (1, 1), (0, 1)], ROCK),
        ("rect", 0.2, 0.6, 0.78, 0.66, INK, "Gage lying, face away"), ("text", 0.5, 0.4, "music SILENT; he pushes up")]},
    {"name": "9", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", SKY, (160, 150, 110)), ("rect", 0, 0.66, 1, 0.74, DIRT),
        ("rect", 0.4, 0.55, 0.72, 0.66, (120, 90, 60), "ox cart"), ("fig", 0.55, 0.58, 0.12, {}, "Gage upright"),
        ("rect", 0.12, 0.56, 0.36, 0.68, (90, 70, 50), "oxen"), ("fig", 0.8, 0.72, 0.14, {"hat": True})]},
    {"name": "10", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", (220, 214, 200), (190, 180, 160)), ("rect", 0, 0.3, 1, 0.75, (226, 220, 206), "hotel piazza"),
        ("fig", 0.62, 0.72, 0.3, {"sitting": True}, "Gage, hand up"), ("fig", 0.18, 0.98, 0.5, {"hat": True}, "doctor (back)"),
        ("fig", 0.88, 0.7, 0.24, {"hat": True}, "Matt")]},
    {"name": "11", "zone": "TOP", "text": "caption", "shapes": [
        ("grad", (90, 80, 70), (60, 54, 48)), ("line", 0.4, 0.2, 0.6, 0.95, IRON, 16),
        ("ellipse", 0.42, 0.5, 0.66, 0.64, SKIN), ("text", 0.5, 0.75, "the hand closes on the iron")]},
    {"name": "12", "zone": "LOW", "text": "caption · end line", "shapes": [
        ("grad", (170, 168, 164), (130, 128, 124)), ("rect", 0.0, 0.2, 0.42, 1, (110, 100, 90), "doorway"),
        ("fig", 0.2, 0.9, 0.5, {"hat": True}), ("fig", 0.34, 0.92, 0.48, {}), ("fig", 0.75, 0.66, 0.14, {}, "Gage (soft)")]},
]


# ── 2. stand-in pieces ─────────────────────────────────────────────────────────────────────────────────────────────────
def _grad(im: Image.Image, top, bottom, y0=0.0, y1=1.0):
    d = ImageDraw.Draw(im)
    a, b = int(y0 * im.height), int(y1 * im.height)
    for y in range(a, b):
        t = (y - a) / max(1, b - a)
        d.line([(0, y), (im.width, y)], fill=tuple(int(p + (q - p) * t) for p, q in zip(top, bottom)))


def _blob(im: Image.Image, boxes, col, blur=40, alpha=200):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for x0, y0, x1, y1 in boxes:
        d.ellipse([x0 * W, y0 * H, x1 * W, y1 * H], fill=(*col, alpha))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def _label(im: Image.Image, text: str):
    ImageDraw.Draw(im).text((24, H - 60), "STAND-IN · " + text, fill=(255, 255, 255, 200))


def plate_s1() -> Path:
    im = Image.new("RGBA", (W, H))
    _grad(im, (226, 222, 210), (206, 196, 176))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0.26 * H), (0.22 * W, 0.42 * H), (0.27 * W, H), (0, H)], fill=(*ROCK, 255))       # left wall
    d.polygon([(W, 0.24 * H), (0.8 * W, 0.44 * H), (0.75 * W, H), (W, H)], fill=(*ROCK, 255))        # right wall
    d.polygon([(0, 0.86 * H), (W, 0.84 * H), (W, H), (0, H)], fill=(*DIRT, 255))                      # floor
    for x0, y0, x1, y1 in [(0.02, 0.5, 0.12, 0.52), (0.85, 0.55, 0.97, 0.57)]:                           # strata lines
        d.line([(x0 * W, y0 * H), (x1 * W, y1 * H)], fill=(70, 70, 74, 255), width=4)
    _blob(im, [(0.05, 0.66, 0.6, 0.96), (0.25, 0.6, 0.75, 0.9), (0.4, 0.72, 0.95, 1.0)], SMOKE, 60, 230)
    for x, y in [(0.08, 0.92), (0.92, 0.9)]:                                                              # two crewmen ducking
        d.ellipse([(x - 0.03) * W, (y - 0.06) * H, (x + 0.03) * W, (y - 0.03) * H], fill=(40, 38, 40, 255))
        d.rounded_rectangle([(x - 0.05) * W, (y - 0.035) * H, (x + 0.05) * W, (y + 0.03) * H], 30, fill=(40, 38, 40, 255))
    _label(im, "s1 empty plate (no Gage, no bar)")
    return _save(im, "plates/s1-empty.free.png")


def plate_s4() -> Path:
    im = Image.new("RGBA", (W, H))
    _grad(im, (222, 218, 204), (190, 176, 140), 0, 0.5)
    _grad(im, (150, 130, 90), (120, 112, 80), 0.5, 1)
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0.48 * H), (0.4 * W, 0.4 * H), (W, 0.46 * H), (W, 0.62 * H), (0, 0.66 * H)], fill=(*HILL, 255))
    d.polygon([(0.25 * W, 0.7 * H), (W, 0.66 * H), (W, H), (0.25 * W, H)], fill=(*ROCK, 255))            # the ledge he stands on
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f = ImageDraw.Draw(fg)
    f.ellipse([-0.18 * W, 0.74 * H, 0.38 * W, 1.12 * H], fill=(42, 38, 38, 255))                         # crewman 1 (back)
    f.ellipse([0.0 * W, 0.68 * H, 0.2 * W, 0.78 * H], fill=(36, 32, 32, 255))                             # his hat
    f.ellipse([0.7 * W, 0.8 * H, 1.2 * W, 1.12 * H], fill=(48, 44, 42, 255))                              # crewman 2 (back)
    f.ellipse([0.82 * W, 0.74 * H, 1.0 * W, 0.83 * H], fill=(36, 32, 32, 255))
    im.alpha_composite(fg.filter(ImageFilter.GaussianBlur(14)))                                            # soft foreground
    _label(im, "s4 empty plate (no Gage)")
    return _save(im, "plates/s4-empty.free.png")


def plate_s8() -> Path:
    im = Image.new("RGBA", (W, H))
    _grad(im, (180, 174, 162), (130, 124, 116), 0, 0.62)
    _grad(im, (112, 108, 104), (84, 80, 78), 0.62, 1)
    _blob(im, [(-0.2, 0.15, 0.7, 0.6), (0.3, 0.25, 1.2, 0.7), (0.0, 0.5, 1.0, 0.75)], (196, 190, 178), 80, 170)
    d = ImageDraw.Draw(im)
    for x, y, r in [(0.15, 0.8, 0.03), (0.82, 0.74, 0.02), (0.6, 0.9, 0.025)]:                              # stones
        d.ellipse([(x - r) * W, (y - r / 2) * H, (x + r) * W, (y + r / 2) * H], fill=(70, 68, 66, 255))
    _label(im, "s8 empty plate (no Gage)")
    return _save(im, "plates/s8-empty.free.png")


def _save(im: Image.Image, rel: str) -> Path:
    p = IMG / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p)
    return p


def _sheet(name: str, frames: dict[str, list[Image.Image]], anchor: tuple[float, float], note: str) -> Path:
    """Frames on one canvas size + sprites.json (the same format fx_prep.sheet writes for the paid sheets)."""
    out = IMG / "sprites" / name
    out.mkdir(parents=True, exist_ok=True)
    first = next(iter(frames.values()))[0]
    spec = {"source": f"STAND-IN ({note}); the paid sheet replaces it with the same states", "canvas": list(first.size),
            "anchor": list(anchor), "frames": {}}
    for state, ims in frames.items():
        spec["frames"][state] = []
        for i, im in enumerate(ims):
            fn = f"{state}-{i}.png"
            im.save(out / fn)
            spec["frames"][state].append(fn)
    (out / "sprites.json").write_text(json.dumps(spec, indent=1), encoding="utf-8")
    return out / "sprites.json"


def iron() -> Path:
    S = 3
    im = Image.new("RGBA", (900 * S, 70 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([20 * S, 22 * S, 760 * S, 48 * S], 12 * S, fill=(*IRON, 255))                       # the shaft
    d.polygon([(760 * S, 22 * S), (880 * S, 35 * S), (760 * S, 48 * S)], fill=(*IRON, 255))                 # the point
    d.line([(40 * S, 28 * S), (840 * S, 34 * S)], fill=(120, 120, 126, 255), width=3 * S)                   # highlight
    return _sheet("iron", {"rod": [im.resize((900, 70), Image.LANCZOS)]}, (0.5, 0.5), "a drawn bar")


def _person(d, S, x, y, h, lean=0.0, arms="down", hat=True, col=(28, 26, 28, 255)):
    """A silhouette standing at (x, y) (feet), height h, leaning back by `lean` (fraction of h at the head)."""
    import math
    hx = x - lean * h
    head = h * 0.12
    d.ellipse([(hx - head * 0.45) * S, (y - h) * S, (hx + head * 0.45) * S, (y - h + head) * S], fill=col)
    sh = (hx, y - h + head * 1.1)
    hip = (x - lean * h * 0.4, y - h * 0.45)
    d.line([(sh[0] * S, sh[1] * S), (hip[0] * S, hip[1] * S)], fill=col, width=int(h * 0.2 * S), joint="curve")
    for dx in (-0.05, 0.05):
        d.line([((hip[0] + dx * h * 0.6) * S, hip[1] * S), ((x + dx * h) * S, y * S)], fill=col, width=int(h * 0.07 * S))
    if arms == "up":                                    # flung up and back
        for ang in (-130, -60):
            a = math.radians(ang)
            d.line([(sh[0] * S, sh[1] * S), ((sh[0] + math.cos(a) * h * 0.27) * S, (sh[1] + math.sin(a) * h * 0.27) * S)],
                   fill=col, width=int(h * 0.055 * S))
    else:
        for dx in (-0.08, 0.08):
            d.line([(sh[0] * S, sh[1] * S), ((sh[0] + dx * h) * S, (sh[1] + h * 0.33) * S)], fill=col, width=int(h * 0.055 * S))
    if hat:
        d.rectangle([(hx - head * 0.5) * S, (y - h - head * 0.55) * S, (hx + head * 0.5) * S, (y - h + head * 0.2) * S], fill=col)
        d.rectangle([(hx - head * 0.85) * S, (y - h + head * 0.1) * S, (hx + head * 0.85) * S, (y - h + head * 0.25) * S], fill=col)


def gage_s1() -> Path:
    S, cw, ch = 3, 420, 900
    frames = {}
    for state, lean, arms in (("stand", 0.0, "down"), ("thrown", 0.18, "up")):
        im = Image.new("RGBA", (cw * S, ch * S), (0, 0, 0, 0))
        _person(ImageDraw.Draw(im), S, cw / 2, ch - 20, 780, lean=lean, arms=arms, hat=state == "stand")
        frames[state] = [im.resize((cw, ch), Image.LANCZOS)]
    return _sheet("gage-s1", frames, (0.5, 0.978), "drawn silhouettes")


def hat() -> Path:
    S = 3
    im = Image.new("RGBA", (200 * S, 110 * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([55 * S, 10 * S, 145 * S, 80 * S], 20 * S, fill=(40, 34, 30, 255))
    d.ellipse([10 * S, 66 * S, 190 * S, 100 * S], fill=(40, 34, 30, 255))
    return _sheet("hat", {"hat": [im.resize((200, 110), Image.LANCZOS)]}, (0.5, 0.6), "a drawn hat")


def gage_s4() -> Path:
    """Medium shot, seen from behind-left over the crew: torso, arms down to the bar in the hole, head down / turned."""
    S, cw, ch = 3, 620, 1000
    frames = {}
    for state in ("down", "turn"):
        im = Image.new("RGBA", (cw * S, ch * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([200 * S, 300 * S, 430 * S, 720 * S], 60 * S, fill=(*SHIRT, 255), outline=(*INK, 255), width=5 * S)
        d.line([(230 * S, 330 * S), (300 * S, 720 * S)], fill=(80, 60, 40, 255), width=14 * S)               # braces
        d.line([(400 * S, 330 * S), (340 * S, 720 * S)], fill=(80, 60, 40, 255), width=14 * S)
        d.rectangle([215 * S, 700 * S, 415 * S, ch * S], fill=(*COAT, 255))                                  # trousers
        d.line([(330 * S, 360 * S), (330 * S, ch * S)], fill=(*IRON, 255), width=22 * S)                     # the bar
        for x in (245, 395):                                                                                  # arms to the bar
            d.line([(x * S, 360 * S), (330 * S, 600 * S)], fill=(*SHIRT, 255), width=46 * S)
            d.ellipse([300 * S, 570 * S, 360 * S, 630 * S], fill=(*SKIN, 255))
        hx, hy = (300, 245) if state == "down" else (270, 205)
        d.ellipse([(hx - 70) * S, (hy - 85) * S, (hx + 70) * S, (hy + 85) * S], fill=(*SKIN, 255), outline=(*INK, 255), width=5 * S)
        if state == "turn":                                                                                   # face toward camera
            for ex in (hx - 30, hx + 22):
                d.ellipse([(ex - 9) * S, (hy - 15) * S, (ex + 9) * S, (hy + 3) * S], fill=(*INK, 255))
            d.line([((hx - 20) * S, (hy + 45) * S), ((hx + 18) * S, (hy + 45) * S)], fill=(*INK, 255), width=5 * S)
        else:                                                                                                 # looking down at the hole
            d.line([((hx - 40) * S, (hy + 20) * S), ((hx + 10) * S, (hy + 30) * S)], fill=(*INK, 255), width=5 * S)
        d.rectangle([(hx - 75) * S, (hy - 120) * S, (hx + 75) * S, (hy - 55) * S], fill=(46, 40, 36, 255))   # hat
        d.rectangle([(hx - 110) * S, (hy - 62) * S, (hx + 110) * S, (hy - 45) * S], fill=(46, 40, 36, 255))
        frames[state] = [im.resize((cw, ch), Image.LANCZOS)]
    return _sheet("gage-s4", frames, (0.53, 0.99), "drawn poses")


def gage_s8() -> Path:
    """From behind his right shoulder, on the ground: lie (still) / fingers (the hand moves) / prop (up on the elbow)."""
    S, cw, ch = 3, 1000, 560
    frames = {}
    for state in ("lie", "fingers", "prop"):
        im = Image.new("RGBA", (cw * S, ch * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        lift = {"lie": 0, "fingers": 0, "prop": 150}[state]
        d.rounded_rectangle([420 * S, 380 * S, 960 * S, 520 * S], 60 * S, fill=(*COAT, 255))                 # legs
        d.polygon([(180 * S, (420 - lift) * S), (470 * S, (370 - lift * 0.4) * S), (470 * S, 520 * S), (150 * S, 520 * S)],
                  fill=(*SHIRT, 255), outline=(*INK, 255))                                                    # torso
        d.ellipse([60 * S, (330 - lift) * S, 230 * S, (480 - lift) * S], fill=(120, 110, 100, 255), outline=(*INK, 255), width=5 * S)  # dusty hair, face away
        if state == "prop":
            d.line([(230 * S, 400 * S), (200 * S, 520 * S)], fill=(*SHIRT, 255), width=50 * S)               # the elbow down
        hand = {"lie": [(560, 470), (620, 500)], "fingers": [(560, 455), (630, 470)], "prop": [(540, 440), (600, 470)]}[state]
        d.line([(470 * S, 440 * S), (hand[0][0] * S, hand[0][1] * S)], fill=(*SHIRT, 255), width=40 * S)
        d.line([(hand[0][0] * S, hand[0][1] * S), (hand[1][0] * S, hand[1][1] * S)], fill=(*SKIN, 255), width=30 * S)
        frames[state] = [im.resize((cw, ch), Image.LANCZOS)]
    return _sheet("gage-s8", frames, (0.5, 0.93), "drawn poses")


if __name__ == "__main__":
    print(len(render_frames(P / "review/previz", SHOTS)), "sketches")
    for f in (plate_s1, plate_s4, plate_s8, iron, gage_s1, hat, gage_s4, gage_s8):
        print(f())
