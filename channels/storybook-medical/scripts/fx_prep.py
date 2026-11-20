"""Cut-outs for the Shorts' masked effects (free, local). Coordinates are fractions of the 9:16 FRAME (as the renderer
shows it), so they match the numbers measured on the gridded contact sheets; they are mapped back to the source still
here, and episode.py build crops the mask / plate exactly like the still (fit_frame), so they line up.

    cut(image, name, box, how="rembg"|"color", hinge=None)
      -> <keyframes>/fx/<stem>-<name>.mask.png   white, alpha = the part that moves
      -> <keyframes>/fx/<stem>-<name>.clean.png  the still with that part painted out (cv2 inpaint), shown under
                                                  the moving copy so a wag / shake never reveals a ghost

    python channels/storybook-medical/scripts/fx_prep.py <image> <name> <x0> <y0> <x1> <y1> [--how color] [--check]

    sheet(image, names) -> sprite / pose sheet cut into aligned RGBA frames + sprites.json + check.png (magenta)
    python channels/storybook-medical/scripts/fx_prep.py sheet <sheet.png> fly-0 fly-1 land-0 rest-0 [--out DIR]
"""
from __future__ import annotations

import argparse
import json
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
    if how == "poly":            # exactly the traced outline (a thin tool: rembg grabs the person or the rock behind it)
        if not poly:
            raise ValueError("how='poly' needs a poly outline")
        a = np.full((crop.height, crop.width), 255, np.uint8)
    elif how == "bright":          # a lit surface without the dark ink on it (a watch's LCD face around its digits)
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


# ── sprite / pose sheets → aligned cut-outs (plan/layered-animation.md §2; user 2026-11-16) ────────────────────────────
def _key_alpha(rgb: np.ndarray, key: np.ndarray, lo: float = 38, hi: float = 110) -> tuple[np.ndarray, np.ndarray]:
    """Soft chroma key against a flat background colour, with the background UNMIXED from semi-transparent pixels
    (observed = a*fg + (1-a)*key  ->  fg = (observed - (1-a)*key) / a): a mosquito's smoky wings keep their own grey,
    not a green tint."""
    d = np.sqrt(((rgb.astype(np.float32) - key) ** 2).sum(axis=2))
    a = np.clip((d - lo) / (hi - lo), 0, 1)
    fg = (rgb.astype(np.float32) - (1 - a[..., None]) * key) / np.maximum(a[..., None], 1e-3)
    return np.clip(fg, 0, 255).astype(np.uint8), a


def _despill_edge(rgba: np.ndarray, key: np.ndarray, band: int = 5) -> np.ndarray:
    """The key colour that survives in the opaque ink line next to the background (a dark outline reads as fully
    opaque, so the unmixing leaves its green cast: a dark-green line round Gage's fingers). Within `band` px of the
    transparent area, the key's dominant channel is clamped to the larger of the other two. Only the edge band, so a
    green object's own colour inside the figure is kept."""
    import cv2
    k = int(np.argmax(key))
    edge = cv2.dilate((rgba[..., 3] < 128).astype(np.uint8), np.ones((2 * band + 1,) * 2, np.uint8)).astype(bool)
    out = rgba.copy()
    others = np.delete(out[..., :3], k, axis=2).max(axis=2)
    ch = out[..., k]
    fix = edge & (ch > others)
    ch[fix] = others[fix]
    return out


def sheet(image: str, names: list[str], out_dir: str | None = None, how: str = "key", align: str = "phase",
          pad: int = 24, anchor=(0.5, 0.5), min_area: float = 0.002) -> Path:
    """Cut a sprite sheet (one object, its states side by side on a flat background) or a pose sheet into frames.

    names: one per figure in reading order (rows top to bottom, left to right), "<state>-<n>", e.g.
           ["fly-0", "fly-1", "land-0", "rest-0"]. Writes <out>/<name>.png (RGBA, all on ONE canvas size so the actor's
           width means the same thing in every state), <out>/sprites.json for layers.py, and <out>/check.png: every
           frame over magenta (holes and halos show at once) plus the sheet's alpha.
    how:   "key"   = flat-colour key, the colour measured on the sheet's border (prompt_kit KEY_BG asks for green);
           "rembg" = the background model, for sheets that came back on a busy background.
    align: "phase" = every frame's alpha aligned to the sheet's FIRST frame by phase correlation (the solid body
           dominates, so wings / legs changing don't make it jump between states); "center" = bounding-box centres;
           "bottom" = bounding-box feet (characters standing).
    anchor: (ax, ay) fractions of the canvas, or "solid" = the centroid of the first frame's fully opaque core (an
           insect's body, not its legs or wings): the point that rides the actor's path and that it turns around."""
    import cv2
    src = Path(image)
    im = np.array(Image.open(src).convert("RGB"))
    H, W = im.shape[:2]
    border = np.concatenate([im[:8].reshape(-1, 3), im[-8:].reshape(-1, 3), im[:, :8].reshape(-1, 3), im[:, -8:].reshape(-1, 3)])
    key = np.median(border, axis=0).astype(np.float32)
    if how == "rembg":
        from masks import _session
        from rembg import remove
        a = np.array(remove(Image.fromarray(im), session=_session()).getchannel("A")).astype(np.float32) / 255
        fg = im
    else:
        fg, a = _key_alpha(im, key)
    # find the figures: the alpha, closed hard enough that thin legs and wings join their body
    solid = (a > 0.25).astype(np.uint8)
    joined = cv2.dilate(solid, np.ones((max(9, W // 90),) * 2, np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(joined)
    blobs = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > min_area * W * H]
    if len(blobs) != len(names):
        raise SystemExit(f"{src.name}: found {len(blobs)} figures, expected {len(names)} ({names}); check the sheet "
                         f"(figures touching? a busy background? try how='rembg')")
    # reading order: figures whose vertical spans overlap share a row (long legs move a figure's top edge, so rounding
    # the top put figures of one row into different rows); rows top to bottom, then left to right
    rows: list[list[int]] = []
    for i in sorted(blobs, key=lambda i: stats[i, cv2.CC_STAT_TOP]):
        top, bot = stats[i, cv2.CC_STAT_TOP], stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT]
        if rows and top < max(stats[j, cv2.CC_STAT_TOP] + stats[j, cv2.CC_STAT_HEIGHT] for j in rows[-1]) \
                and bot > min(stats[j, cv2.CC_STAT_TOP] for j in rows[-1]):
            rows[-1].append(i)
        else:
            rows.append([i])
    blobs = [i for r in rows for i in sorted(r, key=lambda i: stats[i, cv2.CC_STAT_LEFT])]
    cuts = []
    for i in blobs:
        x, y, w, h = stats[i, :4]
        keep = (lab[y:y + h, x:x + w] == i)
        alpha = (a[y:y + h, x:x + w] * keep * 255).astype(np.uint8)
        ys, xs = np.nonzero(alpha > 8)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        rgba = np.dstack([fg[y:y + h, x:x + w][y0:y1, x0:x1], alpha[y0:y1, x0:x1]])
        cuts.append(rgba)
    cuts = [_despill_edge(c, key) for c in cuts]
    cw = max(c.shape[1] for c in cuts) + 2 * pad
    ch = max(c.shape[0] for c in cuts) + 2 * pad
    out = Path(out_dir) if out_dir else src.parent / src.stem
    out.mkdir(parents=True, exist_ok=True)
    frames: dict[str, list[str]] = {}
    ref = None
    placed = []
    # work on a canvas with a wide margin M: the phase shift moves a frame towards the first one, and a raised arm then
    # slid off a canvas sized for the unshifted cut-outs (HC002-S1 2a, user 2026-11-20: "the fingers of gage is cut out")
    Mg = max(cw, ch) // 2
    for name, c in zip(names, cuts):
        canvas = np.zeros((ch + 2 * Mg, cw + 2 * Mg, 4), np.uint8)
        h, w = c.shape[:2]
        ox, oy = (cw - w) // 2, (ch - h) // 2 if align != "bottom" else ch - pad - h
        canvas[Mg + oy:Mg + oy + h, Mg + ox:Mg + ox + w] = c
        if align == "phase":
            core = cv2.erode((canvas[..., 3] > 240).astype(np.float32), np.ones((3, 3), np.uint8))   # the solid body
            if ref is None:
                ref = core
            else:
                (dx, dy), _ = cv2.phaseCorrelate(ref, core)
                M = np.float32([[1, 0, -dx], [0, 1, -dy]])
                canvas = cv2.warpAffine(canvas, M, canvas.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        placed.append(canvas)
    # grow the canvas SYMMETRICALLY only as far as a shifted frame overflows it (+ pad): its centre stays the same
    # body point, and sheets that never overflowed come out exactly as before
    ys, xs = np.nonzero(np.max([p[..., 3] for p in placed], axis=0) > 8)
    over_x = int(max(0, Mg - xs.min(), xs.max() + 1 - (Mg + cw)))
    over_y = int(max(0, Mg - ys.min(), ys.max() + 1 - (Mg + ch)))
    ex = over_x + pad if over_x else 0
    ey = over_y + pad if over_y else 0
    if ex or ey:
        print(f"  {src.name}: a shifted frame overflowed the canvas by {over_x},{over_y} px: canvas grown")
    placed = [p[Mg - ey:Mg + ch + ey, Mg - ex:Mg + cw + ex] for p in placed]
    cw, ch = cw + 2 * ex, ch + 2 * ey
    for name, canvas in zip(names, placed):
        Image.fromarray(canvas, "RGBA").save(out / f"{name}.png")
        frames.setdefault(name.rsplit("-", 1)[0], []).append(f"{name}.png")
    if anchor == "solid":
        core = cv2.erode((placed[0][..., 3] > 240).astype(np.uint8), np.ones((5, 5), np.uint8))
        ys, xs = np.nonzero(core)
        anchor = (round(xs.mean() / cw, 4), round(ys.mean() / ch, 4))
    meta = {"source": src.name, "canvas": [cw, ch], "anchor": list(anchor), "key": [int(v) for v in key], "frames": frames}
    json.dump(meta, open(out / "sprites.json", "w"), indent=1)
    # the check image: each frame over magenta, labelled; below, the sheet's alpha at the same width
    # last tile = ONION SKIN: every frame at 1/n over each other, with the anchor cross: a body that jumps between
    # states shows as a double outline here
    tile = 260
    row = Image.new("RGB", (tile * (len(placed) + 1), tile + 26), (255, 0, 255))
    d = ImageDraw.Draw(row)
    for j, (name, c) in enumerate(zip(names, placed)):
        im_c = Image.fromarray(c, "RGBA")
        im_c.thumbnail((tile - 10, tile - 10))
        row.paste(im_c, (j * tile + (tile - im_c.width) // 2, 26 + (tile - im_c.height) // 2), im_c)
        d.text((j * tile + 8, 6), name, fill=(255, 255, 255))
    onion = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    for c in placed:
        layer = Image.fromarray(c, "RGBA")
        layer.putalpha(Image.fromarray((c[..., 3] / len(placed) * 1.6).clip(0, 255).astype(np.uint8)))
        onion.alpha_composite(layer)
    od = ImageDraw.Draw(onion)
    axp, ayp = anchor[0] * cw, anchor[1] * ch
    od.line([(axp - 14, ayp), (axp + 14, ayp)], fill=(255, 255, 0, 255), width=2)
    od.line([(axp, ayp - 14), (axp, ayp + 14)], fill=(255, 255, 0, 255), width=2)
    onion.thumbnail((tile - 10, tile - 10))
    j = len(placed)
    row.paste(onion, (j * tile + (tile - onion.width) // 2, 26 + (tile - onion.height) // 2), onion)
    d.text((j * tile + 8, 6), "onion skin + anchor", fill=(255, 255, 255))
    am = Image.fromarray((a * 255).astype(np.uint8)).convert("RGB")
    am = am.resize((row.width, round(am.height * row.width / am.width)))
    check = Image.new("RGB", (row.width, row.height + am.height), (0, 0, 0))
    check.paste(row, (0, 0)); check.paste(am, (0, row.height))
    check.save(out / "check.png")
    print(f"{src.name}: {len(names)} frames {sorted(frames)} on a {cw}x{ch} canvas -> {out} (look at check.png)")
    return out / "sprites.json"


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "sheet":
        sp = argparse.ArgumentParser()
        sp.add_argument("cmd"); sp.add_argument("image"); sp.add_argument("names", nargs="+")
        sp.add_argument("--out"); sp.add_argument("--how", default="key", choices=("key", "rembg"))
        sp.add_argument("--align", default="phase", choices=("phase", "center", "bottom"))
        s = sp.parse_args()
        sheet(s.image, s.names, s.out, s.how, s.align)
        raise SystemExit
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
