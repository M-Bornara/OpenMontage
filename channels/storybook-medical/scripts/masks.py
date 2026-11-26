"""Subject masks for focus effects (free, local rembg). Give a box around ONE person/object (percent of the image);
rembg cuts out the main subject inside that box, and the result is written as a full-frame mask PNG (white, alpha = subject)
that Remotion uses for outline glows, colour isolation, rack focus and shine sweeps.

    python masks.py <image> <out.png> <x0> <y0> <x1> <y1> [--width 1920] [--grow 2]
"""
from __future__ import annotations

import argparse

from PIL import Image, ImageFilter


_S = None


def _session():
    # BiRefNet (MIT licence). Not rembg's default bria-rmbg: its weights are non-commercial (CC BY-NC).
    global _S
    if _S is None:
        from rembg import new_session
        _S = new_session("birefnet-general")
    return _S


def subject_mask(image: str, out: str, box: tuple[float, float, float, float], width: int = 1920, grow: int = 2,
                 pad: float = 0.3) -> str:
    """The box is a HINT, not a crop edge: rembg runs on the box grown by `pad` (of its size) on every side, and only the
    shapes that reach into the box are kept. A subject that pokes out of the box (a pointing hand, a blanket) stays whole,
    and the mask never has a straight edge where the box was (user review 2026-10-24: 'rectangular, in the wrong place')."""
    import numpy as np
    from rembg import remove

    im = Image.open(image).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    W, H = im.size
    x0, y0, x1, y1 = (round(v / 100 * s) for v, s in zip(box, (W, H, W, H)))
    px, py = round((x1 - x0) * pad), round((y1 - y0) * pad)
    X0, Y0, X1, Y1 = max(0, x0 - px), max(0, y0 - py), min(W, x1 + px), min(H, y1 + py)
    alpha = remove(im.crop((X0, Y0, X1, Y1)), session=_session()).getchannel("A")
    a = np.array(alpha)
    try:
        import cv2
        n, lab = cv2.connectedComponents((a > 40).astype(np.uint8), connectivity=8)
        inner = lab[y0 - Y0:y1 - Y0, x0 - X0:x1 - X0]
        keep = [k for k in range(1, n) if (inner == k).sum() > 0.03 * inner.size]
        a = np.where(np.isin(lab, keep), a, 0).astype(np.uint8)
    except ImportError:
        pass
    full = Image.new("L", (W, H), 0)
    full.paste(Image.fromarray(a), (X0, Y0))
    if grow:
        full = full.filter(ImageFilter.MaxFilter(grow * 2 + 1)).filter(ImageFilter.GaussianBlur(grow))
    mask = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    mask.putalpha(full)
    mask.save(out)
    cover = sum(full.histogram()[i] * i for i in range(256)) / 255 / (W * H) * 100
    print(f"mask -> {out} ({cover:.1f}% of frame)")
    return out


def polygon_mask(image: str, out: str, pts: list[tuple[float, float]], width: int = 1920, feather: int = 5) -> str:
    """A subject the cut-out models can't separate (a person lying under a blanket behind a barrel): its outline MEASURED
    on a coordinate grid as a polygon in % of the frame, feathered so the edge is soft."""
    im = Image.open(image)
    W, H = width, round(im.height * width / im.width)
    from PIL import ImageDraw
    a = Image.new("L", (W, H), 0)
    ImageDraw.Draw(a).polygon([(x / 100 * W, y / 100 * H) for x, y in pts], fill=255)
    a = a.filter(ImageFilter.GaussianBlur(feather))
    mask = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    mask.putalpha(a)
    mask.save(out)
    print(f"polygon mask -> {out}")
    return out


def whole_mask(image: str, out: str, box: tuple[float, float, float, float], width: int = 1920, grow: int = 2,
               limit: list[tuple[float, float]] | None = None) -> str:
    """Cut-out on the WHOLE picture (people standing in a group separate best this way), keeping only the shapes that
    reach into the box. `limit`: a measured polygon (% of the frame) the subject lies inside, to split it from people it
    touches (friends sharing a loaf of bread come out as one shape)."""
    import cv2
    import numpy as np
    from rembg import remove
    im = Image.open(image).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    W, H = im.size
    a = np.array(remove(im, session=_session()).getchannel("A"))
    x0, y0, x1, y1 = (round(v / 100 * s) for v, s in zip(box, (W, H, W, H)))
    n, lab = cv2.connectedComponents((a > 40).astype(np.uint8), connectivity=8)
    inner = lab[y0:y1, x0:x1]
    keep = [k for k in range(1, n) if (inner == k).sum() > 0.03 * inner.size]
    a = np.where(np.isin(lab, keep), a, 0).astype(np.uint8)
    full = Image.fromarray(a)
    if grow:
        full = full.filter(ImageFilter.MaxFilter(grow * 2 + 1)).filter(ImageFilter.GaussianBlur(grow))
    if limit:
        from PIL import ImageChops, ImageDraw
        reg = Image.new("L", (W, H), 0)
        ImageDraw.Draw(reg).polygon([(x / 100 * W, y / 100 * H) for x, y in limit], fill=255)
        full = ImageChops.multiply(full, reg.filter(ImageFilter.GaussianBlur(3)))
    mask = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    mask.putalpha(full)
    mask.save(out)
    print(f"whole-picture mask -> {out}")
    return out


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("image")
    a.add_argument("out")
    a.add_argument("box", nargs=4, type=float)
    a.add_argument("--width", type=int, default=1920)
    a.add_argument("--grow", type=int, default=2)
    o = a.parse_args()
    subject_mask(o.image, o.out, tuple(o.box), o.width, o.grow)


def canoe_water(src: str, sink: float = 0.14, refl_len: float = 0.4) -> dict:
    """A canoe sprite drawn in 3/4 view has a TILTED keel (HC001: ~9.5°), so a flat waterline sank one end and lifted the
    other out of the water (user review 2026-10-26). From the measured keel (the hull's lowest opaque pixel per column,
    fitted on its middle 40 %), writes next to the sprite:
      <name>-water.png  the canoe's mask: opaque above the waterline (parallel to the keel, `sink` of the sprite height
                        above it), fading out just below it; the bow and stern curve up out of the water by themselves
      <name>-refl.png   its reflection: every column mirrored straight down about its own waterline point (the way a
                        reflection on still water works), fading with depth; same width, (1 + refl_len) × the height
    Returns {"wmid": the waterline at mid-hull as a fraction of the sprite height, "E": the reflection's height factor}."""
    import cv2
    import numpy as np
    im = np.array(Image.open(src).convert("RGBA"))
    H, W = im.shape[:2]
    a = im[..., 3] > 128
    cols = np.where(a.any(0))[0]
    x0, x1 = cols[0], cols[-1]
    bot = np.array([np.max(np.nonzero(a[:, x])[0]) if a[:, x].any() else 0 for x in range(W)])
    mid = [x for x in cols if x0 + 0.3 * (x1 - x0) <= x <= x0 + 0.7 * (x1 - x0)]
    k, b = np.polyfit(mid, bot[mid], 1)
    yw = k * np.arange(W) + b - sink * H                              # the waterline per column (px)
    yy = np.arange(H)[:, None]
    d = (yy - yw[None, :]) / H                                        # below the line > 0
    m = np.interp(d, [-0.02, 0.01, 0.04], [1.0, 0.25, 0.0])
    out = np.dstack([np.full((H, W), 0, np.uint8)] * 3 + [(m * 255).astype(np.uint8)])
    from pathlib import Path
    base = Path(src).with_suffix("")
    Image.fromarray(out, "RGBA").save(f"{base}-water.png")
    E = 1 + refl_len
    RH = round(H * E)
    ry = np.arange(RH, dtype=np.float32)[:, None].repeat(W, 1)
    src_y = (2 * yw[None, :] - ry).astype(np.float32)                 # mirror about the column's waterline
    src_x = np.arange(W, dtype=np.float32)[None, :].repeat(RH, 0)
    refl = cv2.remap(im, src_x, src_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    depth = (ry - yw[None, :]) / H
    fade = np.interp(depth, [0, 0.02, 0.28], [0, 1, 0]) * (ry >= yw[None, :])   # close under the hull only
    refl[..., 3] = (refl[..., 3] * fade).astype(np.uint8)
    Image.fromarray(refl, "RGBA").save(f"{base}-refl.png")
    return {"wmid": float(yw[W // 2] / H), "E": E}
