"""HCS07 s3, the layered-animation pilot (user 2026-11-16): Finlay's raised hand; a mosquito flies in, wings flapping,
its shadow growing on the skin, lands with a small bounce, folds its wings; the buzz stops on landing.

Pieces (plan/layered-animation.md §1):
  BG     the s3 still WITHOUT the mosquito         paid: empty_plate() (refs: kf:s3)        free stand-in: cv2 inpaint
  MASK   the hand (the shadow falls only on skin)  free: fx_prep.cut(rembg) on the plate
  ACTOR  the mosquito: fly x2, land, rest           paid: sprite_sheet() on green            free stand-in: drawn below
  LIFE   the lamp flame breathes                    free: Life.Glow

    python channels/storybook-medical/editorial/episodes/HCS07-finlay/layers_s3.py [--free]
(default) builds the paid pieces into plates/s3-empty.png + sprites/mosquito/; --free builds the stand-ins: the preview shows the MOTION; the real pieces
replace them after the prompts are approved (build_hcs07.py REFERENCES "plate-s3-empty", "sprite-mosquito").
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import fx_prep  # noqa: E402

P = REPO / "projects/hcs07-finlay"
IMG = P / "assets/images"
S3 = IMG / "keyframes/s3.png"
MOSQ_BOX = (0.625, 0.532, 0.705, 0.585)            # the painted mosquito on the back of the hand (frame fractions)
# its outline (legs, wing tip, antenna), measured on s3-mosquito.check.png: without it the colour key also took the
# shaded skin in the box's top-left corner and the inpaint smeared it
MOSQ_POLY = [(0.6348, 0.5494), (0.6641, 0.5377), (0.6979, 0.5450), (0.6979, 0.5677), (0.6706, 0.5831), (0.6283, 0.5776),
             (0.6328, 0.5604)]
HAND_BOX = (0.545, 0.500, 0.815, 0.665)            # the raised fist + cuff
NAMES = ["fly-0", "fly-1", "land-0", "rest-0"]
GREEN = (0, 177, 64)


# the hand's upper-left ink outline next to the mosquito (frame fractions, measured on review crops): the hole crosses it
EDGE = [(0.6874, 0.5183), (0.5800, 0.5859)]


def _two_side_inpaint(img: np.ndarray, hole: np.ndarray, edge=EDGE, ink_w: int = 7) -> np.ndarray:
    """The mosquito's legs touch the hand's ink outline: one inpaint smears wall, outline and skin together. Instead
    fill each side of the outline only from its own side, then redraw the ink line through the hole."""
    import cv2
    H, W = img.shape[:2]
    ch = W * 16 / 9
    top = (H - ch) / 2
    (x0, y0), (x1, y1) = [(x * W, top + y * ch) for x, y in edge]
    yy, xx = np.mgrid[:H, :W]
    side = (xx - x0) * (y1 - y0) - (yy - y0) * (x1 - x0) > 0
    near = cv2.dilate(hole, np.ones((61, 61), np.uint8)) > 0
    h = hole > 0
    out = img.copy()
    for s in (side, ~side):
        filled = cv2.inpaint(img, ((h | (near & ~s)) * 255).astype(np.uint8), 7, cv2.INPAINT_TELEA)
        out[h & s] = filled[h & s]
    # the ink colour: the darkest pixels along the outline just outside the hole
    band = np.zeros((H, W), np.uint8)
    cv2.line(band, (int(x0), int(y0)), (int(x1), int(y1)), 255, ink_w * 3)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sel = (band > 0) & ~near & (gray < 70)
    ink = np.median(img[sel], axis=0) if sel.any() else np.array([20, 20, 24])
    line = out.copy()
    cv2.line(line, (int(x0), int(y0)), (int(x1), int(y1)), ink.tolist(), ink_w, cv2.LINE_AA)
    zone = cv2.dilate(hole, np.ones((5, 5), np.uint8)) > 0
    out[zone] = line[zone]
    return out


def plate_free() -> Path:
    """Stand-in plate: s3 with the mosquito painted out locally (colour-keyed mask, two-side inpaint across the hand's
    outline). The paid empty_plate() repaints it properly."""
    import cv2
    mask, _ = fx_prep.cut(str(S3), "mosquito", MOSQ_BOX, how="color", grow=3, check=True, poly=MOSQ_POLY)
    a = np.array(Image.open(mask).getchannel("A"))
    hole = ((cv2.dilate(a, np.ones((9, 9), np.uint8)) > 20) * 255).astype(np.uint8)
    img = cv2.cvtColor(np.array(Image.open(S3).convert("RGB")), cv2.COLOR_RGB2BGR)
    out = IMG / "plates"
    out.mkdir(exist_ok=True)
    dst = out / "s3-empty.free.png"
    Image.fromarray(cv2.cvtColor(_two_side_inpaint(img, hole), cv2.COLOR_BGR2RGB)).save(dst)
    return dst


def hand_mask(plate: Path) -> Path:
    mask, _ = fx_prep.cut(str(plate), "hand", HAND_BOX, how="rembg", grow=2, check=True)
    return mask


def _mosquito(state: str, S: int = 4) -> Image.Image:
    """A top-down Aedes-style mosquito, head to the RIGHT (the actor turns it along its path), drawn 4x and reduced."""
    W, H = 560 * S, 440 * S
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wing = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d, dw = ImageDraw.Draw(im), ImageDraw.Draw(wing)
    cx, cy = 300 * S, 220 * S
    ink, white = (22, 20, 22, 255), (236, 232, 222, 255)

    def leg(x0, y0, pts, w=4):
        q = [(x0 * S, y0 * S)] + [(x * S, y * S) for x, y in pts]
        d.line(q, fill=ink, width=w * S, joint="curve")
        for (xa, ya), (xb, yb) in zip(q[1:], q[2:]):          # white bands on the lower legs
            for f in (0.35, 0.7):
                x, y = xa + (xb - xa) * f, ya + (yb - ya) * f
                d.ellipse((x - 3 * S, y - 3 * S, x + 3 * S, y + 3 * S), fill=white)

    def wing_ell(ang, length, width):
        a = np.radians(ang)
        bx, by = cx - 18 * S, cy
        tip = (bx + np.cos(a) * length * S, by + np.sin(a) * length * S)
        mid = ((bx + tip[0]) / 2, (by + tip[1]) / 2)
        poly = []
        for k in range(48):
            th = 2 * np.pi * k / 48
            u, v = np.cos(th) * length / 2 * S, np.sin(th) * width / 2 * S
            poly.append((mid[0] + u * np.cos(a) - v * np.sin(a), mid[1] + u * np.sin(a) + v * np.cos(a)))
        dw.polygon(poly, fill=(150, 160, 170, 105), outline=(30, 30, 34, 230), width=2 * S)
        dw.line([(bx, by), tip], fill=(40, 40, 46, 160), width=S)

    # legs: (side) front / middle / hind, by state
    if state.startswith("fly"):       # tucked and trailing back in flight
        legs = [((300, 208), [(250, 250), (170, 268)]), ((300, 232), [(250, 190), (170, 172)]),
                ((290, 210), [(230, 256), (150, 282)]), ((290, 230), [(230, 184), (150, 158)]),
                ((280, 212), [(220, 262), (130, 296)]), ((280, 228), [(220, 178), (130, 144)])]
    elif state.startswith("land"):    # reaching forward and wide for the skin
        legs = [((305, 210), [(360, 150), (430, 110)]), ((305, 230), [(360, 290), (430, 330)]),
                ((292, 208), [(300, 120), (300, 60)]), ((292, 232), [(300, 320), (300, 380)]),
                ((280, 210), [(220, 140), (150, 100)]), ((280, 230), [(220, 300), (150, 340)])]
    else:                             # standing on the skin: legs splayed
        legs = [((305, 210), [(350, 160), (410, 140)]), ((305, 230), [(350, 280), (410, 300)]),
                ((292, 208), [(290, 140), (275, 90)]), ((292, 232), [(290, 300), (275, 350)]),
                ((280, 210), [(230, 160), (160, 130)]), ((280, 230), [(230, 280), (160, 310)])]
    for (x0, y0), pts in legs:
        leg(x0, y0, pts)
    # wings
    if state == "fly-0":              # wings down: long, spread wide
        wing_ell(-118, 175, 46); wing_ell(118, 175, 46)
    elif state == "fly-1":            # wings up: foreshortened
        wing_ell(-150, 95, 40); wing_ell(150, 95, 40)
    elif state == "land-0":           # half open
        wing_ell(-150, 165, 40); wing_ell(150, 165, 40)
    else:                             # folded back over the abdomen
        wing_ell(-174, 170, 34); wing_ell(174, 170, 34)
    # body: abdomen (banded), thorax (lyre mark), head, proboscis, antennae
    d.ellipse(((cx - 175 * S), cy - 17 * S, cx - 30 * S, cy + 17 * S), fill=ink)
    for k in range(5):
        x = cx - (60 + 22 * k) * S
        d.arc((x - 6 * S, cy - 17 * S, x + 6 * S, cy + 17 * S), 270, 90, fill=white, width=3 * S)
    d.ellipse((cx - 45 * S, cy - 25 * S, cx + 18 * S, cy + 25 * S), fill=ink)
    d.arc((cx - 34 * S, cy - 16 * S, cx + 6 * S, cy + 4 * S), 190, 350, fill=white, width=3 * S)
    d.arc((cx - 34 * S, cy - 4 * S, cx + 6 * S, cy + 16 * S), 10, 170, fill=white, width=3 * S)
    d.ellipse((cx + 10 * S, cy - 14 * S, cx + 38 * S, cy + 14 * S), fill=ink)
    d.line([(cx + 36 * S, cy), (cx + 112 * S, cy - 4 * S)], fill=ink, width=4 * S)
    d.line([(cx + 34 * S, cy - 6 * S), (cx + 80 * S, cy - 34 * S)], fill=ink, width=2 * S)
    d.line([(cx + 34 * S, cy + 6 * S), (cx + 80 * S, cy + 34 * S)], fill=ink, width=2 * S)
    im = Image.alpha_composite(wing, im) if state != "rest-0" else Image.alpha_composite(im, wing)
    return im.resize((W // S, H // S), Image.LANCZOS)


def sheet_free() -> Path:
    """Stand-in sprite sheet, laid out like the paid one will be (four states in a row on chroma-key green), then cut by
    the same fx_prep.sheet() the real sheet will go through."""
    cells = [_mosquito(n) for n in NAMES]
    W = sum(c.width for c in cells) + 80 * (len(cells) + 1)
    sh = Image.new("RGBA", (W, cells[0].height + 160), GREEN + (255,))
    x = 80
    for c in cells:
        sh.alpha_composite(c, (x, 80))
        x += c.width + 80
    out = IMG / "sprites"
    out.mkdir(exist_ok=True)
    f = out / "mosquito-sheet.free.png"
    sh.convert("RGB").save(f)
    return fx_prep.sheet(str(f), NAMES, str(out / "mosquito-free"), how="key", align="phase", anchor="solid")


# ---- the paid pieces (generated 2026-11-16, $0.134) --------------------------------------------------------------
# The sheet came back with 2 top-down frames (wings spread, wings folded) and 2 SIDE views, head pointing UP. The plate
# looks straight down at the hand, so only the top-down frames are used; the wing beat and the fold are made from the
# spread frame by turning each wing about its root (measured on the cut frame, 709x679 canvas).
REF = P / "assets/images/refs"
WING_L = [(322, 238), (285, 232), (250, 224), (200, 212), (150, 196), (30, 198), (14, 242), (50, 296), (150, 322), (250, 310), (322, 270)]   # top edge follows the wing: the front leg runs just above it
WING_R = [(710 - x, y) for x, y in WING_L]                       # mirror (body axis x = 355)
ROOT_L, ROOT_R = (318, 247), (392, 247)
BODY_ANCHOR = (355, 330)          # thorax/abdomen centre on the cut frame: lands on the painted spot


def _poly_mask(size, poly) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return m


def _turn(layer: Image.Image, pivot, deg: float, scale: float) -> Image.Image:
    """Rotate (counter-clockwise on screen for deg > 0) and scale an RGBA layer about a pivot."""
    import math
    a = math.radians(deg)
    c, s_ = math.cos(a) / scale, math.sin(a) / scale
    px, py = pivot
    # inverse map: source = R(-a)/scale * (dest - pivot) + pivot  (y down)
    m = (c, -s_, px - c * px + s_ * py, s_, c, py - s_ * px - c * py)
    return layer.transform(layer.size, Image.AFFINE, m, resample=Image.BICUBIC)


def _swept(spread: Image.Image, deg: float, scale: float) -> Image.Image:
    """The spread frame with both wings swept back toward the tail by deg."""
    body = spread.copy()
    out = Image.new("RGBA", spread.size, (0, 0, 0, 0))
    wings = []
    for poly, root, sign in ((WING_L, ROOT_L, 1), (WING_R, ROOT_R, -1)):
        m = _poly_mask(spread.size, poly)
        w = Image.new("RGBA", spread.size, (0, 0, 0, 0))
        w.paste(spread, (0, 0), m)
        a = np.array(body)
        a[..., 3] = np.where(np.array(m) > 0, 0, a[..., 3])
        body = Image.fromarray(a)
        wings.append(_turn(w, root, sign * deg, scale))
    for w in wings:                # wings under the body, like the folded frame
        out.alpha_composite(w)
    out.alpha_composite(body)
    return out


def pieces_paid() -> tuple[Path, Path, Path]:
    """plates/s3-empty.png + its hand mask + sprites/mosquito/ (fly x2, land x2, rest; head pointing RIGHT)."""
    plate = IMG / "plates/s3-empty.png"
    shutil.copy(REF / "plate-s3-empty.png", plate)
    mask = hand_mask(plate)
    cut = IMG / "sprites/mosquito-cut"
    fx_prep.sheet(str(REF / "sprite-mosquito.png"), ["top-spread", "side-a", "side-b", "top-folded"], str(cut),
                  how="key", align="phase")
    spread = Image.open(cut / "top-spread.png").convert("RGBA")
    folded = Image.open(cut / "top-folded.png").convert("RGBA")
    frames = {"fly": [spread, _swept(spread, 45, 0.9)],
              "land": [_swept(spread, 20, 0.97), _swept(spread, 58, 0.88)],
              "rest": [folded]}
    out = IMG / "sprites/mosquito"
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    names = {}
    for st, ims in frames.items():
        names[st] = []
        for j, im in enumerate(ims):
            f = f"{st}-{j}.png"
            im.rotate(-90, expand=True, resample=Image.BICUBIC).save(out / f)   # head up -> head right
            names[st].append(f)
    W, H = spread.size
    ax, ay = BODY_ANCHOR[0] / W, BODY_ANCHOR[1] / H
    meta = {"source": "sprite-mosquito.png (top-down frames; wing poses made by layers_s3.pieces_paid)",
            "canvas": [H, W], "anchor": [round(1 - ay, 4), round(ax, 4)], "frames": names}
    (out / "sprites.json").write_text(json.dumps(meta, indent=1))
    # check: every frame over magenta + onion skin with the anchor
    tiles = [Image.open(out / f) for st in names for f in names[st]]
    tw, th = tiles[0].size
    chk = Image.new("RGBA", (tw * (len(tiles) + 1), th), (255, 0, 255, 255))
    for i, t in enumerate(tiles):
        chk.alpha_composite(t, (i * tw, 0))
        ImageDraw.Draw(chk).text((i * tw + 6, 4), [f for st in names for f in names[st]][i], fill="white")
    on = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    for t in tiles:
        on = Image.blend(on, t, 0.5) if on.getbbox() else t.copy()
    chk.alpha_composite(on, (len(tiles) * tw, 0))
    cx, cy = len(tiles) * tw + meta["anchor"][0] * tw, meta["anchor"][1] * th
    ImageDraw.Draw(chk).line([(cx - 12, cy), (cx + 12, cy)], fill="yellow", width=2)
    ImageDraw.Draw(chk).line([(cx, cy - 12), (cx, cy + 12)], fill="yellow", width=2)
    chk.convert("RGB").save(out / "check.png")
    return plate, mask, out / "sprites.json"


if __name__ == "__main__":
    if "--free" in sys.argv:
        plate = plate_free()
        mask = hand_mask(plate)
        sprites = sheet_free()
    else:
        plate, mask, sprites = pieces_paid()
    meta = json.load(open(sprites))
    print("plate", plate, "\nmask ", mask, "\nsprites", sprites, meta["canvas"], meta["frames"])
