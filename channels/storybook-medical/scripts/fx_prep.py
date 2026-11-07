"""Cut-outs for the Shorts' masked effects (free, local). Coordinates are fractions of the 9:16 FRAME (as the renderer
shows it), so they match the numbers measured on the gridded contact sheets; they are mapped back to the source still
here, and episode.py build crops the mask / plate exactly like the still (fit_frame), so they line up.

    cut(image, name, box, how="rembg"|"color", hinge=None)
      -> <keyframes>/fx/<stem>-<name>.mask.png   white, alpha = the part that moves
      -> <keyframes>/fx/<stem>-<name>.clean.png  the still with that part painted out (cv2 inpaint), shown under
                                                  the moving copy so a wag / shake never reveals a ghost

    python channels/storybook-medical/scripts/fx_prep.py <image> <name> <x0> <y0> <x1> <y1> [--how color] [--check]
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def frame_box(im: Image.Image, box, focus: float = 0.5):
    """Frame fractions (9:16 window, as fit_frame crops it) -> source pixel box."""
    W, H = im.size
    ch = W * 16 / 9
    top = (H - ch) * focus if H > ch else 0
    x0, y0, x1, y1 = box
    return round(x0 * W), round(top + y0 * ch), round(x1 * W), round(top + y1 * ch)


def _rembg(crop: Image.Image) -> np.ndarray:
    from masks import _session
    from rembg import remove
    return np.array(remove(crop, session=_session()).getchannel("A"))


def _color(crop: Image.Image) -> np.ndarray:
    """Ink-and-colour subject on a flat wall: everything that is far from the crop's median (the wall) colour."""
    import cv2
    a = np.array(crop).astype(np.int16)
    wall = np.median(a.reshape(-1, 3), axis=0)
    far = (np.abs(a - wall).sum(axis=2) > 70).astype(np.uint8)
    far = cv2.morphologyEx(far, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab = cv2.connectedComponents(far)
    if n > 1:
        big = 1 + int(np.argmax([(lab == k).sum() for k in range(1, n)]))
        far = (lab == big).astype(np.uint8)
    # fill the loops of a curly tail / the space inside a hand
    # (padded by one pixel, so a corner the subject fences off against the box edge still counts as outside)
    h, w = far.shape
    flood = np.pad(far, 1) * 255
    cv2.floodFill(flood, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 128)
    far = np.where(flood[1:-1, 1:-1] == 0, 1, far)
    return far * 255


def cut(image: str, name: str, box, how: str = "rembg", grow: int = 3, focus: float = 0.5, check: bool = False, poly=None):
    """poly: optional outline [(x, y), ...] in frame fractions; the cut is clipped to it (keeps only that object
    when rembg also grabs what touches it, e.g. the phone's cradle and the binders behind the handset)."""
    import cv2
    src = Path(image)
    im = Image.open(src).convert("RGB")
    X0, Y0, X1, Y1 = frame_box(im, box, focus)
    crop = im.crop((X0, Y0, X1, Y1))
    if how == "bright":          # a lit surface without the dark ink on it (a watch's LCD face around its digits)
        a = ((np.array(crop.convert("L")) > 110) * 255).astype(np.uint8)
    else:
        a = _rembg(crop) if how == "rembg" else _color(crop)
    full = np.zeros((im.height, im.width), np.uint8)
    full[Y0:Y1, X0:X1] = a
    if poly:
        clip = Image.new("L", im.size, 0)
        pts = [frame_box(im, (x, y, x, y), focus)[:2] for x, y in poly]
        ImageDraw.Draw(clip).polygon(pts, fill=255)
        full = np.minimum(full, np.array(clip.filter(ImageFilter.GaussianBlur(2))))
    m = Image.fromarray(full)
    m = (m.filter(ImageFilter.MaxFilter(grow * 2 + 1)) if grow else m).filter(ImageFilter.GaussianBlur(1.5))
    out = src.parent / "fx"
    out.mkdir(exist_ok=True)
    mask = Image.new("RGBA", im.size, (255, 255, 255, 0))
    mask.putalpha(m)
    mp = out / f"{src.stem}-{name}.mask.png"
    mask.save(mp)
    hole = (np.array(m.filter(ImageFilter.MaxFilter(9))) > 20).astype(np.uint8) * 255
    clean = cv2.inpaint(cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR), hole, 9, cv2.INPAINT_TELEA)
    cp = out / f"{src.stem}-{name}.clean.png"
    Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).save(cp)
    cover = (np.array(m) > 128).mean() * 100
    print(f"{mp.name}: {cover:.2f}% of the still; plate -> {cp.name}")
    if check:   # the mask in magenta over the still, cropped round the box, for a visual check
        pad = 80
        c = im.copy()
        tint = Image.new("RGB", im.size, (255, 0, 255))
        c = Image.composite(Image.blend(c, tint, 0.55), c, m)
        ImageDraw.Draw(c).rectangle((X0, Y0, X1, Y1), outline=(255, 255, 0), width=3)
        c.crop((max(0, X0 - pad), max(0, Y0 - pad), min(im.width, X1 + pad), min(im.height, Y1 + pad))).save(out / f"{src.stem}-{name}.check.png")
    return mp, cp


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("image"); ap.add_argument("name")
    ap.add_argument("box", nargs=4, type=float)
    ap.add_argument("--how", default="rembg", choices=("rembg", "color", "bright"))
    ap.add_argument("--grow", type=int, default=3)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--poly", help="x,y x,y ... outline in frame fractions")
    a = ap.parse_args()
    poly = [tuple(map(float, q.split(","))) for q in a.poly.split()] if a.poly else None
    cut(a.image, a.name, a.box, a.how, a.grow, check=a.check, poly=poly)
