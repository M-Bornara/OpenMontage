"""HCS10 Pettenkofer: free HERO motion pre-viz on stand-in PIECES (user 2026-11-20: storyboard approved with 4 fixes;
"then the free HERO pre-viz on real pieces, with scale lines (L51) in every hand close-up"). No paid call.

For each HERO shot (1, 4, 6, 7) this draws the pieces the paid sheets will replace, with the SAME names, states and
anchors (plan/layered-animation.md §7 step 3), sized in centimetres from the storyboard's L51 scale table:
    plates/s<n>-empty.free.png         the set without what moves
    sprites/free/<name>/sprites.json   the moving piece in its states (the fx_prep.sheet format)
and renders a preview with the keys in the edit's format (t, x, y = the anchor in frame fractions, state, ease):
    projects/hcs10-pettenkofer/review/hero/<shot>-preview.mp4    (540x960, a click on each key word)
    projects/hcs10-pettenkofer/review/hero/<shot>-sheet.jpg      start / key / end frames
Overlays: the estimated word under the frame (narration not recorded yet: times from the storyboard's ≈s), the HERO
1/3 box on the moving piece at its key (layered-shot HERO size rule), the Shorts safe zone, the hook card band (shot 1)
and a 10 cm scale ruler on the hand close-ups (L51). The keys move into edit_hcs10.py once the narration exists
(c.at("word") replaces the estimates).

    python channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/hero_previz_hcs10.py [1 4 6 7]
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[5]
P = REPO / "projects/hcs10-pettenkofer"
IMG, OUT = P / "assets/images", P / "review/hero"
W, H, FPS, OW, OH = 1080, 1920, 30, 540, 960

INK, SKIN, SKIN2 = (30, 28, 30), (214, 172, 146), (190, 148, 122)
WHITE_HAIR, COAT, SHIRT, WOOD = (232, 230, 224), (34, 32, 36), (226, 222, 212), (120, 84, 56)
GLASS, LIQ, AMBER = (196, 222, 230), (220, 236, 238), (232, 163, 61)


def _font(size: int):
    for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


# ── piece helpers ─────────────────────────────────────────────────────────────────────────────────────────────────
def _grad(im, top, bottom, y0=0.0, y1=1.0):
    d = ImageDraw.Draw(im)
    a, b = int(y0 * im.height), int(y1 * im.height)
    for y in range(a, b):
        t = (y - a) / max(1, b - a)
        d.line([(0, y), (im.width, y)], fill=tuple(int(p + (q - p) * t) for p, q in zip(top, bottom)) + (255,))


def _glow(im, box, col, blur, alpha):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse(box, fill=(*col, alpha))
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))


def _label(im, text):
    ImageDraw.Draw(im).text((24, im.height - 50), "STAND-IN · " + text, fill=(255, 255, 255, 190), font=_font(26))


def _save(im, rel):
    p = IMG / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    im.save(p)
    return p


def _sheet(name, frames: dict, anchor, note):
    """Frames on one canvas + sprites.json (the format fx_prep.sheet writes for the paid sheets)."""
    out = IMG / "sprites/free" / name          # the real cut-outs take sprites/<name> (the edit's path)
    out.mkdir(parents=True, exist_ok=True)
    spec = {"source": f"STAND-IN ({note}); the paid sheet replaces it with the same states",
            "canvas": list(next(iter(frames.values())).size), "anchor": list(anchor), "frames": {}}
    for state, im in frames.items():
        im.save(out / f"{state}-0.png")
        spec["frames"][state] = [f"{state}-0.png"]
    (out / "sprites.json").write_text(json.dumps(spec, indent=1), encoding="utf-8")
    return {s: im for s, im in frames.items()}, anchor


def _small_glass(d, cx, top, cm, liquid=True):
    """The small culture glass: 7 cm tall, 5 cm across, ~1 cm of liquid (C14)."""
    w, h = 5 * cm, 7 * cm
    d.rounded_rectangle([cx - w / 2, top, cx + w / 2, top + h], int(cm * 0.6), fill=(*GLASS, 150), outline=(90, 110, 120, 255), width=max(2, int(cm * 0.15)))
    if liquid:
        d.rectangle([cx - w / 2 + cm * 0.3, top + h - 1.3 * cm, cx + w / 2 - cm * 0.3, top + h - 0.3 * cm], fill=(*LIQ, 220))
    d.line([(cx - w / 2 + cm * 0.6, top + cm * 0.5), (cx - w / 2 + cm * 0.6, top + h - cm)], fill=(255, 255, 255, 200), width=max(2, int(cm * 0.25)))


def _face_front(d, cx, cy, cm):
    """Pettenkofer, 1892, front: white hair brushed back, broad full white beard, heavy brows (Lenbach / c.1898)."""
    d.ellipse([cx - 9.5 * cm, cy - 13 * cm, cx + 9.5 * cm, cy + 2 * cm], fill=(*WHITE_HAIR, 255))                 # hair mass
    d.ellipse([cx - 7.5 * cm, cy - 10 * cm, cx + 7.5 * cm, cy + 10 * cm], fill=(*SKIN, 255), outline=(*INK, 255), width=int(cm * 0.25))
    d.chord([cx - 7.5 * cm, cy - 12 * cm, cx + 7.5 * cm, cy - 3 * cm], 180, 360, fill=(*WHITE_HAIR, 255))           # brushed-back top
    d.polygon([(cx - 7.8 * cm, cy + 1 * cm), (cx + 7.8 * cm, cy + 1 * cm), (cx + 6 * cm, cy + 12 * cm),
               (cx, cy + 15 * cm), (cx - 6 * cm, cy + 12 * cm)], fill=(*WHITE_HAIR, 255))                           # full beard
    d.ellipse([cx - 4 * cm, cy + 1.6 * cm, cx + 4 * cm, cy + 4.2 * cm], fill=(240, 238, 232, 255))                  # moustache
    for ex in (cx - 3.2 * cm, cx + 3.2 * cm):
        d.line([(ex - 1.8 * cm, cy - 3.2 * cm), (ex + 1.8 * cm, cy - 3.0 * cm)], fill=(150, 146, 140, 255), width=int(cm * 0.7))  # brows
        d.ellipse([ex - 0.6 * cm, cy - 2.2 * cm, ex + 0.6 * cm, cy - 1.2 * cm], fill=(*INK, 255))
    d.line([(cx, cy - 2 * cm), (cx - 0.6 * cm, cy + 1 * cm)], fill=(*SKIN2, 255), width=int(cm * 0.4))              # nose


def _hand(d, wx, wy, ang, cm, col=SKIN, state="open", cuff=COAT, fore=12):
    """A man's hand (19 cm from wrist to fingertip, 8.5 cm palm width), from the wrist at (wx, wy) pointing at ang
    (degrees, 0 = right). States: open (flat / reaching), stopped (fingers spread, upright), grip, palm (raised, facing us)."""
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    P_ = lambda a, b: (wx + ca * a * cm - sa * b * cm, wy + sa * a * cm + ca * b * cm)  # noqa: E731  (a along, b across)
    d.polygon([P_(-fore, -4.5), P_(0.5, -4.5), P_(0.5, 4.5), P_(-fore, 4.5)], fill=(*cuff, 255))                    # sleeve / forearm
    d.polygon([P_(0, -1.5), P_(0.8, -1.5), P_(0.8, 1.5), P_(0, 1.5)], fill=(*SHIRT, 255))                           # shirt cuff
    if state == "grip":
        d.polygon([P_(0, -4.3), P_(8.6, -4.6), P_(9.6, -2), P_(9.6, 2), P_(8.6, 4.6), P_(0, 4.3)], fill=(*col, 255),
                  outline=(*INK, 255), width=int(cm * 0.2))                                                       # the fist, from above
        for k in range(4):                                                                                            # white knuckles over the edge
            b = -3.2 + k * 2.15
            d.ellipse([P_(8.2, b)[0] - cm, P_(8.2, b)[1] - cm, P_(8.2, b)[0] + cm, P_(8.2, b)[1] + cm], fill=(236, 214, 200, 255), outline=(*INK, 255))
        for k in range(3):                                                                                            # tendons up
            b = -2.2 + k * 2.2
            d.line([P_(1, b), P_(7, b)], fill=(170, 128, 104, 255), width=int(cm * 0.3))
        return
    if state == "clutch":                                                                                            # fingers curl, clutching
        d.polygon([P_(0, -4.3), P_(8.8, -4.7), P_(8.8, 4.7), P_(0, 4.3)], fill=(*col, 255), outline=(*INK, 255), width=int(cm * 0.2))
        for k in range(4):                                                                                            # curled fingers: short, bent down
            b = -3.4 + k * 2.25
            d.polygon([P_(8.4, b - 1), P_(12.0, b - 0.9), P_(12.6, b), P_(12.0, b + 0.9), P_(8.4, b + 1)],
                      fill=(*col, 255), outline=(*INK, 255))                                               # along the hand
            kx, ky_ = P_(8.8, b)
            d.ellipse([kx - 0.9 * cm, ky_ - 0.9 * cm, kx + 0.9 * cm, ky_ + 0.9 * cm], fill=(240, 222, 210, 255), outline=(*INK, 255))  # white knuckle
        for k in range(3):
            b = -2.2 + k * 2.2
            d.line([P_(1, b), P_(7.6, b)], fill=(170, 128, 104, 255), width=int(cm * 0.3))                           # tendons up
        d.line([P_(2, -4.2), P_(7.5, -5.6)], fill=(*col, 255), width=int(cm * 2.0))                                   # thumb pressed in
        return
    d.polygon([P_(0.5, -4.2), P_(9.5, -4.4), P_(9.5, 4.4), P_(0.5, 4.2)], fill=(*col, 255), outline=(*INK, 255))    # palm
    spread = {"open": 0.6, "stopped": 1.6, "palm": 1.0}[state]
    for k, ln in enumerate((7.5, 8.6, 8.2, 6.6)):                                                                     # four fingers
        b = (-3.3 + k * 2.2) * (1 + (spread - 1) * 0.3)
        a0 = (9.2, b)
        tip = (9.2 + ln, b * (1 + 0.12 * spread))
        d.line([P_(*a0), P_(*tip)], fill=(*col, 255), width=int(cm * 1.7))
        d.ellipse([P_(*tip)[0] - 0.85 * cm, P_(*tip)[1] - 0.85 * cm, P_(*tip)[0] + 0.85 * cm, P_(*tip)[1] + 0.85 * cm], fill=(*col, 255))
    d.line([P_(2, -4.2), P_(6.5, -8.5 if state != "open" else -6.5)], fill=(*col, 255), width=int(cm * 2.0))      # thumb


# ── shot 1: hand + small glass rising; the student's hand stops short on "drink" ──────────────────────────────────────
CM1 = 0.42 * W / 15          # his face ≈ 15 cm wide fills 0.42 of the frame width


def shot1():
    im = Image.new("RGBA", (W, H))
    _grad(im, (40, 30, 24), (24, 18, 16))
    for x in (0.62, 0.72, 0.82):                                                                                       # flask shapes, soft
        ImageDraw.Draw(im).ellipse([x * W, 0.2 * H, (x + 0.06) * W, 0.26 * H], fill=(70, 60, 52, 255))
    _glow(im, [0.02 * W, 0.08 * H, 0.32 * W, 0.24 * H], AMBER, 60, 170)                                                 # the gas lamp
    im = im.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(im)
    cx, cy = 0.5 * W, 0.52 * H
    d.polygon([(0.04 * W, H), (0.1 * W, 0.7 * H), (0.32 * W, 0.62 * H), (0.68 * W, 0.62 * H), (0.9 * W, 0.7 * H), (0.96 * W, H)], fill=(*COAT, 255))
    d.polygon([(0.42 * W, 0.62 * H), (0.58 * W, 0.62 * H), (0.5 * W, 0.76 * H)], fill=(*SHIRT, 255))
    _face_front(d, cx, cy, CM1)
    _label(im, "s1 empty plate: his face, NO glass, NO hand")
    plate = _save(im, "plates/s1-empty.free.png")

    cv = Image.new("RGBA", (int(12 * CM1), int(26 * CM1)), (0, 0, 0, 0))     # his hand + small glass
    g = ImageDraw.Draw(cv)
    gx, top = cv.width * 0.5, cv.height * 0.03
    g.polygon([(gx - 4.5 * CM1, cv.height), (gx - 3.5 * CM1, top + 9 * CM1), (gx + 3.5 * CM1, top + 9 * CM1),
               (gx + 4.5 * CM1, cv.height)], fill=(*COAT, 255))                              # sleeve
    g.rectangle([gx - 3.6 * CM1, top + 8.6 * CM1, gx + 3.6 * CM1, top + 9.6 * CM1], fill=(*SHIRT, 255))   # cuff
    g.rounded_rectangle([gx - 4.2 * CM1, top + 2.2 * CM1, gx + 4.0 * CM1, top + 9.2 * CM1], int(CM1 * 2),
                        fill=(206, 166, 140, 255), outline=(*INK, 255))                     # palm behind the glass
    _small_glass(g, gx, top, CM1)
    for k in range(3):                                                                      # fingers round the front
        y = top + (2.6 + k * 1.5) * CM1
        g.rounded_rectangle([gx - 3.2 * CM1, y, gx + 2.0 * CM1, y + 1.35 * CM1], int(CM1 * 0.6),
                            fill=(206, 166, 140, 255), outline=(*INK, 255))
    g.rounded_rectangle([gx + 1.6 * CM1, top + 2.0 * CM1, gx + 3.0 * CM1, top + 5.6 * CM1], int(CM1 * 0.6),
                        fill=(214, 172, 146, 255), outline=(*INK, 255))                     # thumb
    hg = _sheet("hand-glass-s1", {"hold": cv}, (0.5, 0.03), "his right hand holding the small glass, one state")

    st = {}
    for state in ("reaching", "stopped"):
        c = Image.new("RGBA", (int(34 * CM1), int(16 * CM1)), (0, 0, 0, 0))
        _hand(ImageDraw.Draw(c), c.width * 0.98, c.height * 0.55, 180 + (8 if state == "reaching" else -4), CM1,
              col=(222, 184, 158), state="open" if state == "reaching" else "stopped", cuff=(60, 56, 70), fore=14)
        st[state] = c
    tip = min(im_.getbbox()[0] for im_ in st.values()) / st["reaching"].width           # anchor = the fingertips
    sh = _sheet("student-hand-s1", st, (tip, 0.55), "the blond student's right hand: reaching / stopped short")
    return {
        "name": "1", "dur": 4.4, "plate": plate, "cm": CM1, "card": (0.0, 2.5),
        "words": [(0.0, "Munich"), (0.5, "1892"), (1.2, "a"), (1.4, "seventy-three-year-old"), (2.3, "professor"),
                  (2.8, "is about"), (3.15, "to"), (3.3, "DRINK"), (3.7, "CHOLERA")],
        "clicks": [3.3, 3.7],
        "cam": [{"t": 0, "scale": 1.0, "x": 0, "y": 0}, {"t": 3.7, "scale": 1.08, "x": 0, "y": -1.5, "ease": "out"}],
        "actors": [
            {"id": "hand-glass", "piece": hg, "keys": [{"t": 0, "x": 0.43, "y": 0.80, "state": "hold"},
                                                       {"t": 3.7, "x": 0.47, "y": 0.575, "ease": "inout"}], "hero": True},
            {"id": "student-hand", "piece": sh, "xfade": 0.08,
             "keys": [{"t": 0, "x": 1.02, "y": 0.80, "state": "reaching"}, {"t": 1.1, "x": 0.80, "y": 0.77, "ease": "out"},
                      {"t": 3.3, "x": 0.64, "y": 0.73, "state": "stopped", "ease": "inout"}]},
        ],
        "hero_at": 3.7,
    }


# ── shot 4: the refusal; MS + push in; ONE swap to the raised palm on "no" ─────────────────────────────────────────────
CM4 = 0.12 * H / 23          # his head ≈ 23 cm tall fills 0.12 of the frame height (MS, waist up)


def shot4():
    im = Image.new("RGBA", (W, H))
    _grad(im, (150, 132, 108), (110, 92, 72), 0, 0.66)
    d = ImageDraw.Draw(im)
    for i in range(3):                                                                                                  # glass-fronted cabinets of jars
        x0 = 0.28 + i * 0.24
        d.rectangle([x0 * W, 0.08 * H, (x0 + 0.2) * W, 0.6 * H], fill=(96, 70, 50, 255), outline=(60, 44, 32, 255), width=6)
        for r in range(5):
            for c in range(3):
                d.ellipse([(x0 + 0.025 + c * 0.06) * W, (0.12 + r * 0.095) * H, (x0 + 0.065 + c * 0.06) * W, (0.17 + r * 0.095) * H], fill=(160, 170, 150, 255))
    d.rectangle([0, 0, 0.14 * W, 0.66 * H], fill=(236, 232, 214, 255))                                                  # the window light, left edge
    mx, my = 0.86 * W, 0.42 * H                                                                                        # MATT at the back, by the cabinets
    d.ellipse([mx - 28, my - 34, mx + 28, my + 34], fill=(*SKIN, 255))
    d.rectangle([mx - 50, my + 34, mx + 50, my + 200], fill=(46, 44, 50, 255))
    d.line([(mx - 30, my + 40), (mx + 30, my + 40)], fill=(40, 140, 140, 255), width=12)                               # teal scarf
    for gx in (mx - 13, mx + 13):
        d.ellipse([gx - 11, my - 10, gx + 11, my + 8], outline=(*AMBER, 255), width=4)                                  # amber spectacles
    d.rectangle([mx + 20, my + 90, mx + 60, my + 140], fill=(*AMBER, 255))                                              # notebook
    d.polygon([(0, 0.66 * H), (W, 0.64 * H), (W, 0.74 * H), (0, 0.76 * H)], fill=(*WOOD, 255))                          # the bench top
    d.rectangle([0, 0.75 * H, W, H], fill=(70, 50, 36, 255))
    _small_glass(d, 0.80 * W, 0.645 * H - 7 * CM4, CM4)
    _label(im, "s4 empty plate: bench, cabinets, Matt; NO Pettenkofer")
    plate = _save(im, "plates/s4-empty.free.png")
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0))                                                                       # two students' backs (FG layer)
    f = ImageDraw.Draw(fg)
    f.ellipse([-0.22 * W, 0.70 * H, 0.36 * W, 1.18 * H], fill=(40, 38, 46, 255))
    f.ellipse([0.02 * W, 0.62 * H, 0.22 * W, 0.74 * H], fill=(200, 170, 110, 255))                                     # the blond one's head
    f.ellipse([0.70 * W, 0.72 * H, 1.25 * W, 1.18 * H], fill=(30, 30, 36, 255))
    f.ellipse([0.80 * W, 0.64 * H, 0.98 * W, 0.75 * H], fill=(52, 38, 30, 255))

    poses = {}
    for state in ("hands", "palm"):
        c = Image.new("RGBA", (int(80 * CM4), int(78 * CM4)), (0, 0, 0, 0))
        g = ImageDraw.Draw(c)
        cx, base = c.width * 0.5, c.height
        g.polygon([(cx - 24 * CM4, base), (cx - 22 * CM4, base - 48 * CM4), (cx + 22 * CM4, base - 48 * CM4), (cx + 24 * CM4, base)], fill=(*COAT, 255))
        g.polygon([(cx - 5 * CM4, base - 48 * CM4), (cx + 5 * CM4, base - 48 * CM4), (cx, base - 30 * CM4)], fill=(*SHIRT, 255))
        _face_front(g, cx, base - 62 * CM4, CM4)
        _hand(g, cx + 18 * CM4, base - 8 * CM4, 100, CM4, state="open", fore=26)                                        # his left hand stays on the bench
        if state == "hands":
            _hand(g, cx - 18 * CM4, base - 8 * CM4, 80, CM4, state="open", fore=26)
        else:
            _hand(g, cx - 26 * CM4, base - 28 * CM4, -95, CM4, state="palm", fore=22)                                   # palm up at chest height, toward them
        poses[state] = c
    pz = _sheet("pettenkofer-s4", poses, (0.5, 1.0), "MS behind the bench: hands on the bench / palm raised")
    return {
        "name": "4", "dur": 3.6, "plate": plate, "fg": fg, "cm": CM4,
        "words": [(0.0, "his"), (0.2, "students"), (0.7, "offered"), (1.0, "to go"), (1.3, "first,"), (1.75, "he wrote."),
                  (2.5, "he"), (2.7, "said"), (3.0, "NO")],
        "clicks": [3.0],
        "cam": [{"t": 0, "scale": 1.0, "x": 0, "y": 0}, {"t": 3.0, "scale": 1.18, "x": 0, "y": 3, "ease": "inout"}],
        "focus": [(0.0, 0.0), (1.5, 1.0)],         # rack focus FG students -> him
        "actors": [{"id": "pettenkofer", "piece": pz, "xfade": 0.08, "hero": True,
                    "keys": [{"t": 0, "x": 0.50, "y": 0.665, "state": "hands"}, {"t": 3.0, "x": 0.50, "y": 0.665, "state": "palm"}]}],
        "glint": (0.86, 0.42, 3.2),
        "hero_at": 3.1,
    }


# ── shot 6: the gulp; profile against the window; ONE swap on "gulp", the window swells on "purest water" ─────────────
CM6 = 0.28 * H / 23


def shot6():
    im = Image.new("RGBA", (W, H))
    _grad(im, (214, 220, 222), (186, 194, 198))
    d = ImageDraw.Draw(im)
    for x in (0.0, 0.33, 0.66, 0.99):                                                                                 # leaded window mullions
        d.line([(x * W, 0), (x * W, H)], fill=(80, 84, 86, 255), width=16)
    for y in (0.0, 0.25, 0.5, 0.75):
        d.line([(0, y * H), (W, y * H)], fill=(80, 84, 86, 255), width=12)
    d.rectangle([0.88 * W, 0, W, H], fill=(140, 120, 96, 255))                                                         # curtain edge
    for x in (0.93, 0.99):
        _glow(im, [(x - 0.06) * W, 0.45 * H, (x + 0.06) * W, 0.9 * H], (50, 46, 50), 30, 230)                           # two students, soft
    _label(im, "s6 empty plate: window, students soft; NO Pettenkofer")
    plate = _save(im, "plates/s6-empty.free.png")

    poses = {}
    for state in ("lips", "back"):
        c = Image.new("RGBA", (int(60 * CM6), int(58 * CM6)), (0, 0, 0, 0))
        g = ImageDraw.Draw(c)
        cx, base = c.width * 0.42, c.height
        g.polygon([(cx - 24 * CM6, base), (cx - 16 * CM6, base - 20 * CM6), (cx + 12 * CM6, base - 22 * CM6), (cx + 20 * CM6, base)], fill=(*COAT, 255))
        tilt = 0 if state == "lips" else -28
        head = Image.new("RGBA", (int(34 * CM6), int(34 * CM6)), (0, 0, 0, 0))
        hd = ImageDraw.Draw(head)
        hx, hy = head.width * 0.45, head.height * 0.5
        hd.ellipse([hx - 9 * CM6, hy - 12 * CM6, hx + 9 * CM6, hy + 11 * CM6], fill=(*WHITE_HAIR, 255))                  # hair, back of head
        hd.ellipse([hx - 6 * CM6, hy - 10 * CM6, hx + 9 * CM6, hy + 10 * CM6], fill=(*SKIN, 255), outline=(*INK, 255), width=4)
        hd.polygon([(hx + 9 * CM6, hy - 2 * CM6), (hx + 12 * CM6, hy + 2 * CM6), (hx + 8.5 * CM6, hy + 3 * CM6)], fill=(*SKIN, 255))   # nose
        hd.polygon([(hx - 2 * CM6, hy + 3 * CM6), (hx + 9.5 * CM6, hy + 4 * CM6), (hx + 6 * CM6, hy + 15 * CM6), (hx - 4 * CM6, hy + 11 * CM6)], fill=(*WHITE_HAIR, 255))  # beard
        hd.line([(hx + 3 * CM6, hy - 4 * CM6), (hx + 7 * CM6, hy - 4.2 * CM6)], fill=(150, 146, 140, 255), width=10)      # brow
        hd.ellipse([hx + 4.6 * CM6, hy - 3 * CM6, hx + 5.8 * CM6, hy - 1.8 * CM6], fill=(*INK, 255))
        gl = Image.new("RGBA", (int(18 * CM6), int(18 * CM6)), (0, 0, 0, 0))     # rim at the centre
        gd = ImageDraw.Draw(gl)
        _small_glass(gd, gl.width * 0.5, gl.height * 0.5, CM6, liquid=(state == "lips"))
        for k in range(3):
            y = gl.height * 0.5 + (2.4 + k * 1.5) * CM6
            gd.rounded_rectangle([gl.width * 0.5 - 3 * CM6, y, gl.width * 0.5 + 2.6 * CM6, y + 1.3 * CM6], 8,
                                 fill=(206, 166, 140, 255), outline=(*INK, 255))
        gl = gl.rotate(80 if state == "lips" else 92, resample=Image.BICUBIC)               # bottom out, then up
        mx_, my_ = hx + 8.6 * CM6, hy + 3.4 * CM6                                           # the mouth
        head.alpha_composite(gl, (int(mx_ - gl.width / 2), int(my_ - gl.height / 2)))
        head = head.rotate(-tilt, center=(hx, hy + 8 * CM6), resample=Image.BICUBIC)
        c.alpha_composite(head, (int(cx - hx), int(base - 20 * CM6 - head.height * 0.82)))
        poses[state] = c
    pz = _sheet("pettenkofer-s6", poses, (0.42, 1.0), "profile: the small glass at his lips / head back, drinking")
    return {
        "name": "6", "dur": 3.6, "plate": plate, "cm": CM6,
        "words": [(0.1, "one"), (0.4, "GULP"), (1.2, "like"), (1.4, "the"), (1.55, "PUREST"), (1.95, "WATER"), (2.5, "he wrote")],
        "clicks": [0.4, 1.55],
        "cam": [{"t": 0, "scale": 1.0, "x": 0, "y": 0}, {"t": 3.6, "scale": 1.02, "x": 0, "y": 0}],
        "swell": (1.55, 0.6, 0.35),
        "actors": [{"id": "pettenkofer", "piece": pz, "xfade": 0.08, "hero": True,
                    "keys": [{"t": 0, "x": 0.40, "y": 1.0, "state": "lips"}, {"t": 0.4, "x": 0.40, "y": 1.0, "state": "back"}]}],
        "hero_at": 1.0,
    }


# ── shot 7: the cramps; high angle on the desk; the hand flat -> ONE swap to the grip on "cramps"; colour drains ───────
CM7 = W / 30                 # the frame shows ≈ 45 cm of desk across


def shot7():
    im = Image.new("RGBA", (W, H))
    _grad(im, (150, 108, 70), (120, 84, 54), 0, 0.90)
    d = ImageDraw.Draw(im)
    for k in range(9):
        d.line([(0, (0.05 + k * 0.075) * H), (W, (0.07 + k * 0.075) * H)], fill=(130, 92, 60, 255), width=3)            # wood grain
    d.rectangle([0, 0.90 * H, W, 0.92 * H], fill=(90, 62, 40, 255))                                                     # the desk edge (4 cm)
    d.rectangle([0, 0.92 * H, W, H], fill=(28, 24, 22, 255))                                                            # floor in shadow
    px, py = 0.30 * W, -0.02 * H                                                                                         # papers 21 x 34 cm
    d.polygon([(px, py), (px + 21 * CM7, py + 1 * CM7), (px + 20 * CM7, py + 35 * CM7), (px - 1 * CM7, py + 34 * CM7)], fill=(234, 226, 204, 255))
    for k in range(12):
        y = py + (3 + k * 2.4) * CM7
        d.line([(px + 2 * CM7 + (k % 2) * 6, y), (px + 18 * CM7, y + 0.4 * CM7)], fill=(120, 116, 110, 255), width=4)     # wavy, unreadable
    ix, iy = 0.12 * W, 0.12 * H
    d.ellipse([ix - 3 * CM7, iy - 3 * CM7, ix + 3 * CM7, iy + 3 * CM7], fill=(30, 30, 34, 255))                          # inkwell 6 cm
    gx, gy = 0.86 * W, 0.50 * H
    d.ellipse([gx - 2.5 * CM7, gy - 2.5 * CM7, gx + 2.5 * CM7, gy + 2.5 * CM7], fill=(*GLASS, 200), outline=(90, 110, 120, 255), width=5)   # empty small glass, from above
    _glow(im, [-0.3 * W, -0.2 * H, 0.6 * W, 0.4 * H], (220, 224, 226), 120, 90)                                          # grey light, top left
    _label(im, "s7 empty plate: desk top, papers, glass; NO hand")
    plate = _save(im, "plates/s7-empty.free.png")

    poses = {}
    for state in ("flat", "clutch"):
        c = Image.new("RGBA", (int(30 * CM7), int(40 * CM7)), (0, 0, 0, 0))     # wrist pinned at (0.25, 0.55)
        g = ImageDraw.Draw(c)
        wx, wy, ca, sa = c.width * 0.25, c.height * 0.55, math.cos(math.radians(-35)), math.sin(math.radians(-35))
        P_ = lambda a, b: (wx + ca * a * CM7 - sa * b * CM7, wy + sa * a * CM7 + ca * b * CM7)  # noqa: E731
        if state == "flat":                                                                     # the loose top sheet, flat (21 cm wide)
            g.polygon([P_(-1, -9), P_(21, -9), P_(21, 8.5), P_(-1, 8.5)], fill=(238, 230, 208, 255), outline=(160, 150, 130, 255))
            for k in range(6):
                g.line([P_(1.5 + k * 3.4, -7.5), P_(1.5 + k * 3.4, 7)], fill=(120, 116, 110, 255), width=3)                 # wavy lines, unreadable
        else:                                                                                   # the same sheet bunched into his fingers
            g.polygon([P_(3, -9), P_(9, -12), P_(15, -10), P_(17, -4), P_(18, 3), P_(15, 9.5), P_(9, 11), P_(3, 8.5), P_(5, 0)],
                      fill=(226, 218, 196, 255), outline=(140, 130, 112, 255))
            for a_, b_, a2, b2 in ((9, -11, 11, -5), (14, -9, 12, -3), (16.5, -1, 12.5, 0), (15, 8, 12, 3), (8, 10, 10.5, 4),
                                   (4, 6, 8, 2), (5, -6, 8.5, -2), (16, 4, 13.5, 1.5)):
                g.line([P_(a_, b_), P_(a2, b2)], fill=(150, 140, 120, 255), width=4)                  # creases toward the fist
        _hand(g, wx, wy, -35, CM7, col=(206, 166, 140) if state == "flat" else (198, 160, 140),
              state="open" if state == "flat" else "clutch", fore=30)
        poses[state] = c
    hz = _sheet("hand-s7", poses, (0.25, 0.55),
                "his old hand flat on a loose sheet / the fingers curled, clutching and crumpling the sheet, knuckles white (wrist fixed)")
    return {
        "name": "7", "dur": 4.2, "plate": plate, "cm": CM7,
        "words": [(0.0, "(pause)"), (1.0, "two"), (1.25, "days"), (1.55, "later…"), (2.6, "the"), (2.8, "CRAMPS"), (3.3, "began")],
        "clicks": [], "crumple": [2.8],
        "cam": [{"t": 0, "scale": 1.0, "x": 0, "y": 0}, {"t": 4.2, "scale": 1.1, "x": 0, "y": -2}],
        "drain": [(0.0, 1.0), (2.8, 0.75), (4.2, 0.25)],   # saturation over time: warm lab -> grey-green
        # his forearm comes in from the bottom-left over the near edge; the hand lies flat on a loose sheet, then on
        # "cramps" ONE swap: the fingers curl and clutch the sheet, crumpling it, knuckles white; hold (user 2026-11-20:
        # not a fist, which reads as anger); the wrist does not move; a paper crumple on "cramps"
        "actors": [{"id": "hand", "piece": hz, "xfade": 0.10, "hero": True,
                    "keys": [{"t": 0, "x": 0.20, "y": 0.80, "state": "flat"}, {"t": 2.8, "x": 0.20, "y": 0.80, "state": "clutch"}]}],
        "hero_at": 3.2,
    }


# ── renderer ──────────────────────────────────────────────────────────────────────────────────────────────────────────
EASE = {"linear": lambda u: u, "inout": lambda u: u * u * (3 - 2 * u), "out": lambda u: 1 - (1 - u) ** 2,
        "in": lambda u: u * u}


def _interp(keys, t, field, default=0.0):
    ks = [k for k in keys if field in k]
    if not ks:
        return default
    if t <= ks[0]["t"]:
        return ks[0][field]
    for a, b in zip(ks, ks[1:]):
        if t <= b["t"]:
            u = (t - a["t"]) / max(1e-6, b["t"] - a["t"])
            return a[field] + (b[field] - a[field]) * EASE[b.get("ease", "linear")](u)
    return ks[-1][field]


def _state(keys, t):
    cur, since, prev = None, 0.0, None
    for k in keys:
        if "state" in k and k["t"] <= t:
            if cur is not None and k["state"] != cur:
                prev = cur
            cur, since = k["state"], k["t"]
    return cur, since, prev


def _world(shot, t):
    im = Image.open(shot["plate"]).convert("RGBA")
    if "swell" in shot:                                                                     # the window brightens, not him
        t0, d_, amt = shot["swell"]
        im = Image.blend(im, Image.new("RGBA", im.size, (255, 252, 240, 255)), amt * min(1, max(0, (t - t0) / d_)) * 0.6)
    if "drain" in shot:
        ts = [a for a, _ in shot["drain"]]
        vs = [b for _, b in shot["drain"]]
        sat = vs[-1] if t >= ts[-1] else next(vs[i] + (vs[i + 1] - vs[i]) * (t - ts[i]) / (ts[i + 1] - ts[i]) for i in range(len(ts) - 1) if t < ts[i + 1])
    focus = None
    if "focus" in shot:
        (a, fa), (b, fb) = shot["focus"]
        focus = fa + (fb - fa) * min(1, max(0, (t - a) / (b - a)))
    boxes = []
    for a in shot["actors"]:
        frames, anchor = a["piece"]
        st, since, prev = _state(a["keys"], t)
        spr = frames[st]
        xf = a.get("xfade", 0)
        if prev and xf and t - since < xf:
            spr = Image.blend(frames[prev], spr, (t - since) / xf)
        if focus is not None:
            spr = spr.filter(ImageFilter.GaussianBlur(6 * (1 - focus)))
        x, y = _interp(a["keys"], t, "x") * W, _interp(a["keys"], t, "y") * H
        ox, oy = int(x - anchor[0] * spr.width), int(y - anchor[1] * spr.height)
        im.alpha_composite(spr, (ox, oy)) if 0 <= ox and 0 <= oy and ox + spr.width <= W and oy + spr.height <= H else _paste(im, spr, ox, oy)
        if a.get("hero"):
            bb = spr.getbbox()
            if bb:
                boxes.append((ox + bb[0], oy + bb[1], ox + bb[2], oy + bb[3]))
    if "fg" in shot:
        im.alpha_composite(shot["fg"].filter(ImageFilter.GaussianBlur(2 + 14 * (focus or 0))))
    if "drain" in shot:
        rgb = ImageEnhance.Color(im.convert("RGB")).enhance(sat)
        tint = Image.new("RGB", im.size, (150, 166, 150))
        im = Image.blend(rgb, tint, 0.18 * (1 - sat)).convert("RGBA")
    return im, boxes


def _paste(im, spr, ox, oy):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    lay.paste(spr, (ox, oy), spr)
    im.alpha_composite(lay)


def _camera(im, cam, t, boxes):
    s, tx, ty = _interp(cam, t, "scale", 1.0), _interp(cam, t, "x") * W / 100, _interp(cam, t, "y") * H / 100
    cx, cy = W / 2, H / 2
    x0, y0 = cx + (0 - cx - tx) / s, cy + (0 - cy - ty) / s
    x1, y1 = cx + (W - cx - tx) / s, cy + (H - cy - ty) / s
    out = im.crop((int(x0), int(y0), int(x1), int(y1))).resize((OW, OH), Image.LANCZOS)
    k = OW / (x1 - x0)
    return out, [((b[0] - x0) * k, (b[1] - y0) * k, (b[2] - x0) * k, (b[3] - y0) * k) for b in boxes], s


def _overlay(fr, shot, t, boxes, s):
    d = ImageDraw.Draw(fr, "RGBA")
    f, fb = _font(17), _font(24)
    ky = lambda y: y * OH / H  # noqa: E731
    for y in (288, 1248):                                                                                               # safe zone
        for x in range(0, OW, 14):
            d.line([(x, ky(y)), (x + 7, ky(y))], fill=(255, 255, 255, 150), width=1)
    if shot.get("card") and shot["card"][0] <= t < shot["card"][1]:
        d.rectangle([20, ky(360), OW - 20, ky(610)], fill=(232, 163, 61, 90), outline=(232, 163, 61, 220), width=2)
        d.text((OW / 2, ky(485)), "HOOK CARD A (0–2.5 s)", fill=(255, 255, 255, 230), font=fb, anchor="mm")
    near = abs(t - shot["hero_at"]) < 0.5 or t >= shot["hero_at"]
    for b in boxes:                                                                                                     # HERO 1/3 rule
        bw, bh = (min(b[2], OW) - max(b[0], 0)) / OW, (min(b[3], OH) - max(b[1], 0)) / OH
        ok = max(bw, bh) >= 1 / 3
        col = (80, 220, 120, 230) if ok else (240, 70, 60, 230)
        if near:
            d.rectangle(b, outline=col, width=2)
            d.text((max(6, b[0] + 4), max(4, b[1] + 4)), f"HERO {max(bw, bh):.2f} of frame {'≥' if ok else '<'} 1/3",
                   fill=col, font=f)
    cm = shot["cm"] * s * OW / W                                                                                        # L51 scale ruler: 10 cm
    d.rectangle([OW - 24 - 10 * cm, OH - 118, OW - 24, OH - 110], fill=(255, 255, 255, 220))
    d.text((OW - 24, OH - 126), "10 cm (hand = 19 cm)", fill=(255, 255, 255, 230), font=f, anchor="rb")
    word = next((w for a, w in reversed(shot["words"]) if a <= t), "")
    d.rectangle([0, OH - 70, OW, OH], fill=(0, 0, 0, 170))
    d.text((14, OH - 60), f"shot {shot['name']}  t={t:4.2f}s  (word times estimated)", fill=(200, 200, 200, 255), font=f)
    d.text((14, OH - 36), word, fill=(255, 210, 120, 255) if word.isupper() else (255, 255, 255, 255), font=fb)
    if "glint" in shot and shot["glint"][2] <= t < shot["glint"][2] + 0.35:
        gx, gy = shot["glint"][0] * OW, shot["glint"][1] * OH
        for a in range(0, 180, 45):
            r = 16 if a % 90 == 0 else 8
            d.line([(gx - r * math.cos(math.radians(a)), gy - r * math.sin(math.radians(a))),
                    (gx + r * math.cos(math.radians(a)), gy + r * math.sin(math.radians(a)))], fill=(255, 240, 200, 255), width=2)
    return fr


def render(shot):
    OUT.mkdir(parents=True, exist_ok=True)
    mp4 = OUT / f"{shot['name']}-preview.mp4"
    n = round(shot["dur"] * FPS)
    srcs = [f"sine=f=1320:d=0.06,adelay={int(c * 1000)}|{int(c * 1000)}" for c in shot["clicks"]]
    srcs += [f"anoisesrc=d=0.45:c=pink:a=0.9,highpass=f=1800,tremolo=f=28:d=0.95,afade=t=in:d=0.03,afade=t=out:st=0.2:d=0.25,"
             f"adelay={int(c * 1000)}|{int(c * 1000)}" for c in shot.get("crumple", [])]
    clicks = "".join(f"{x},apad=whole_dur={shot['dur']}[c{i}];" for i, x in enumerate(srcs))
    mix = "".join(f"[c{i}]" for i in range(len(srcs))) + f"amix=inputs={len(srcs)}:normalize=0,volume=0.5[a]"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
           "-filter_complex", clicks + mix, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "22",
           "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    keep = {0: None, round(shot["hero_at"] * FPS): None, n - 1: None}
    for i in range(n):
        t = i / FPS
        world, boxes = _world(shot, t)
        fr, sb, s = _camera(world, shot["cam"], t, boxes)
        fr = _overlay(fr.convert("RGB"), shot, t, sb, s)
        proc.stdin.write(fr.tobytes())
        if i in keep:
            keep[i] = fr.copy()
    proc.stdin.close()
    proc.wait()
    sheet = Image.new("RGB", (OW * 3 + 20, OH), "white")
    for j, fr in enumerate(keep.values()):
        sheet.paste(fr, (j * (OW + 10), 0))
    sheet.save(OUT / f"{shot['name']}-sheet.jpg", quality=86)
    return mp4


SHOTS = {"1": shot1, "4": shot4, "6": shot6, "7": shot7}

if __name__ == "__main__":
    for k in (sys.argv[1:] or list(SHOTS)):
        print(render(SHOTS[k]()))
