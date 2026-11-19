"""HC002-S1 shot 1 looks (user 2026-11-18): free, local, from the paid cut-outs (cutouts_hc002s1.py).
  iron-lit/   the bar with a SUNLIT top edge (light from the pale sky above) in two states: "rod" and "glint" (a star on
              the edge). Switching states on the bar's own keys makes the glint ride the bar exactly.
  gage-s1-sil/, hat-sil/   a TRUE silhouette against the bright smoke, with a warm rim light on the top and sides. The
              white shirt stays a shade lighter than the trousers, so his look (shirt, braces, hat) still reads.
  gage-s1-black/   (story-craft Rule 0b, user 2026-11-19) PURE black inside the warm rim: no face, no shirt shade, so the bar
              can burst out of the top of his head with nothing to see but a black shape, a flash and the bar.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/looks_hc002s1.py [--black-only]
"""
import json
import shutil
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

S = Path(__file__).resolve().parents[5] / "projects/hc002-s1/assets/images/sprites"


def shifted(a: np.ndarray, dy: int, dx: int = 0) -> np.ndarray:
    """a moved by (dy, dx), zeros where it comes in from outside."""
    out = np.zeros_like(a)
    h, w = a.shape
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    out[yd, xd] = a[ys, xs]
    return out


def rim(alpha: np.ndarray, top: int, side: int) -> np.ndarray:
    """0..1 band just inside the edge that faces the light: the top edge (pixels whose neighbour `top` px above is
    transparent) at full strength, the left/right edges at half."""
    a = alpha / 255.0
    band = np.clip(a - shifted(a, top), 0, 1)
    sides = np.clip(a - shifted(a, 0, side), 0, 1) + np.clip(a - shifted(a, 0, -side), 0, 1)
    return np.clip(band + 0.5 * sides, 0, 1)


def copy_meta(src: Path, dst: Path, frames: dict, canvas=None):
    m = json.load(open(src / "sprites.json"))
    m["source"] = f"{m['source']} + looks_hc002s1.py"
    m["frames"] = frames
    if canvas:
        m["canvas"] = canvas
    json.dump(m, open(dst / "sprites.json", "w"), indent=1)


def silhouette(name: str, out: str, flat: bool = False):
    src, dst = S / name, S / out
    shutil.rmtree(dst, ignore_errors=True)
    dst.mkdir(parents=True)
    m = json.load(open(src / "sprites.json"))
    for files in m["frames"].values():
        for f in files:
            a = np.array(Image.open(src / f).convert("RGBA")).astype(np.float32)
            lum = (0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]) / 255
            l2 = lum ** 2                                   # mid-tones (the face) go dark, the white shirt stays a shade up
            dark = np.stack([8 + 24 * l2, 9 + 26 * l2, 13 + 29 * l2], axis=-1)        # shirt ~29, face ~18, trousers ~9: no features
            if flat:                                        # Rule 0b: one black shape, nothing inside it
                dark = np.broadcast_to(np.array([8, 9, 12], np.float32), dark.shape)
            r = rim(a[..., 3], 7, 4)
            r = np.array(Image.fromarray((r * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))) / 255
            warm = np.array([250, 230, 190], np.float32)
            rgb = dark * (1 - 0.95 * r[..., None]) + warm * 0.95 * r[..., None]
            Image.fromarray(np.dstack([rgb, a[..., 3]]).clip(0, 255).astype(np.uint8), "RGBA").save(dst / f)
    copy_meta(src, dst, m["frames"])
    print(out, "ok")


def lit_iron():
    src, dst = S / "iron", S / "iron-lit"
    shutil.rmtree(dst, ignore_errors=True)
    dst.mkdir(parents=True)
    rod = np.array(Image.open(src / "rod-0.png").convert("RGBA")).astype(np.float32)
    PAD = 90                                               # room above / below for the glint's rays (anchor stays centred)
    rod = np.pad(rod, ((PAD, PAD), (0, 0), (0, 0)))
    r = rim(rod[..., 3], 7, 0)
    r = np.array(Image.fromarray((r * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5))) / 255
    sun = np.array([255, 238, 196], np.float32)
    rgb = rod[..., :3] * (1 - 0.9 * r[..., None]) + sun * 0.9 * r[..., None]
    lit = Image.fromarray(np.dstack([rgb, rod[..., 3]]).clip(0, 255).astype(np.uint8), "RGBA")
    lit.save(dst / "rod-0.png")
    # the glint: a four-point star with a soft glow on the lit edge, 68 % along the bar (toward the point)
    a = rod[..., 3]
    cols = np.nonzero(a.max(axis=0) > 128)[0]
    gx = int(cols.min() + 0.68 * (cols.max() - cols.min()))
    gy = int(np.nonzero(a[:, gx] > 128)[0].min()) + 3
    star = Image.new("RGBA", lit.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(star)
    for rad, alpha in ((46, 70), (30, 120), (16, 200)):
        d.ellipse([gx - rad, gy - rad, gx + rad, gy + rad], fill=(255, 240, 200, alpha))
    star = star.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(star)
    L, w = 88, 7
    d.polygon([(gx, gy - L), (gx + w, gy), (gx, gy + L), (gx - w, gy)], fill=(255, 253, 245, 255))
    d.polygon([(gx - L * 1.5, gy), (gx, gy - w), (gx + L * 1.5, gy), (gx, gy + w)], fill=(255, 253, 245, 255))
    g = lit.copy()
    g.alpha_composite(star)
    g.save(dst / "glint-0.png")
    copy_meta(src, dst, {"rod": ["rod-0.png"], "glint": ["glint-0.png"]}, [lit.width, lit.height])
    print("iron-lit ok", lit.size, "glint at", gx, gy)


if __name__ == "__main__":
    import sys
    if "--black-only" in sys.argv:
        silhouette("gage-s1", "gage-s1-black", flat=True)
        raise SystemExit
    lit_iron()
    silhouette("gage-s1", "gage-s1-sil")
    silhouette("hat", "hat-sil")
    silhouette("gage-s1", "gage-s1-black", flat=True)
