"""HC002-L row 19: free bandage paint fix on S1's 16:9 s9 still (user 2026-11-23, the open fix from Nov 19).

The band runs flat across BOTH brows and reads as a blindfold. Same fix as the 9:16 stills (paint_bandage_hc002s1.py):
the patch stays over his LEFT eye (right of the picture), the band is painted OUT over his RIGHT brow and forehead (left of
the picture: skin + eyebrow show), and a narrow wrap runs from the patch over the crown (claims C04: in under the left
cheekbone, out through the top of the head). Pixel coordinates measured on a 4x grid of the 2752x1536 still.

    python .../paint_bandage_s9_16x9.py [--preview DIR]

The original stays as s9.orig.png (made on the first run); the fix always starts from it.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[5]
KF = REPO / "projects/hc002-s1/assets/images/keyframes16x9"
Z = 4
BX, BY = 1380, 520          # origin of the measuring grid (zoom 4x: zoom (zx, zy) -> px (BX + zx/4, BY + zy/4))


def zp(pts):
    return [(BX + x / 4, BY + y / 4) for x, y in pts]


# band pixels LEFT of this line (picture left = his right brow) are painted out
CUT_LINE = zp([(566, 296), (604, 400)])
BOX = zp([(484, 290), (610, 450)])                          # where the band is looked for
SKIN_PTS = zp([(486, 318), (520, 308), (556, 312), (580, 350), (600, 392), (560, 392), (520, 384), (487, 386)])
BROW = zp([(489, 377), (505, 371), (525, 369), (546, 372)])    # his right eyebrow (picture left), drawn back
WRAP_C = zp([(606, 304), (614, 228)])                        # centre line: foot on the patch -> over the crown
WRAP_W = (22 / 4, 16 / 4)
HAIR = zp([(540, 232), (566, 214), (620, 210), (664, 236), (684, 296), (640, 312), (566, 312)])   # clip: head


def mask(pts, size, ox, oy):
    m = Image.new("L", (size[0] * Z, size[1] * Z), 0)
    ImageDraw.Draw(m).polygon([((x - ox) * Z, (y - oy) * Z) for x, y in pts], fill=255)
    return m


def run(preview: Path | None = None):
    src, dst = KF / "s9.orig.png", KF / "s9.png"
    if not src.exists():
        (KF / "s9.orig.png").write_bytes(dst.read_bytes())
    im = Image.open(src).convert("RGB")
    x0, y0, x1, y1 = 1380, 520, 1680, 760
    crop = im.crop((x0, y0, x1, y1))
    w, h = crop.size
    big = crop.resize((w * Z, h * Z), Image.LANCZOS)
    arr = np.asarray(big).astype(np.float32)

    # skin tone: a cheek sample (zoom ~ (520, 470) -> beside his nose)
    reg = np.asarray(im.crop((1500, 620, 1545, 650))).reshape(-1, 3).astype(np.float32)   # lit face, nose to cheek
    ok = (reg[:, 0] > 190) & (reg[:, 1] > 130) & (reg[:, 1] < 200) & (reg[:, 2] > 90) & (reg[:, 0] - reg[:, 2] > 40)
    cheek = np.percentile(reg[ok], 70, axis=0) if ok.sum() > 20 else reg.mean(0)
    shade = cheek * 0.88
    skin_m = np.asarray(mask(SKIN_PTS, (w, h), x0, y0).filter(ImageFilter.GaussianBlur(1.6 * Z / 2))).astype(np.float32) / 255
    # only paint where the band is (light, low colour): keep the hair, cloth, skin that are not band
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    lum = (r + g + b) / 3
    sat = arr.max(-1) - arr.min(-1)
    band = ((lum > 175) & (sat < 60)).astype(np.float32)
    band = np.asarray(Image.fromarray((band * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.0))).astype(np.float32) / 255
    # left of the cut line only
    (lx0, ly0), (lx1, ly1) = CUT_LINE
    ys, xs = np.mgrid[0:h * Z, 0:w * Z]
    px, py = xs / Z + x0, ys / Z + y0
    side = ((px - lx0) * (ly1 - ly0) - (py - ly0) * (lx1 - lx0)) > 0     # one side of the line
    if not bool(side[int((605 - y0) * Z), int((1510 - x0) * Z)]):   # (1510, 605) = his forehead, picture-left of the cut: must be the painted side
        side = ~side
    paint = np.clip(skin_m * band * side, 0, 1)[..., None]
    # a soft shadow under the new band edge: darker skin along the cut line
    dist = np.abs((px - lx0) * (ly1 - ly0) - (py - ly0) * (lx1 - lx0)) / np.hypot(lx1 - lx0, ly1 - ly0)
    skin_col = cheek[None, None, :] * (1 - 0.12 * np.clip(1 - dist / 5, 0, 1))[..., None] + 0 * arr
    arr = arr * (1 - paint) + skin_col * paint
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    d = ImageDraw.Draw(out, "RGBA")
    ink = (48, 32, 26, 255)
    # eyebrow
    d.line([((x - x0) * Z, (y - y0) * Z) for x, y in BROW], fill=(58, 38, 28, 255), width=int(2.2 * Z), joint="curve")
    # narrow wrap over the crown, clipped to the head
    (fx, fy), (tx, ty) = WRAP_C
    n = 14
    L, R = [], []
    for i in range(n + 1):
        t = i / n
        cx, cy = fx + (tx - fx) * t - 1.5 * 4 * t * (1 - t), fy + (ty - fy) * t
        half = (WRAP_W[0] + (WRAP_W[1] - WRAP_W[0]) * t) / 2
        dx, dy = tx - fx, ty - fy
        ln = np.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        L.append((cx + nx * half, cy + ny * half)); R.append((cx - nx * half, cy - ny * half))
    poly = L + R[::-1]
    wrap = Image.new("RGBA", out.size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wrap)
    wd.polygon([((x - x0) * Z, (y - y0) * Z) for x, y in poly], fill=(238, 232, 216, 255))
    wd.line([((x - x0) * Z, (y - y0) * Z) for x, y in L + [L[0]]][:-1], fill=ink, width=int(0.9 * Z))
    wd.line([((x - x0) * Z, (y - y0) * Z) for x, y in R], fill=ink, width=int(0.9 * Z))
    clip = mask(HAIR, (w, h), x0, y0)
    wrap.putalpha(Image.fromarray(np.minimum(np.asarray(wrap.split()[3]), np.asarray(clip))))
    out = Image.alpha_composite(out.convert("RGBA"), wrap).convert("RGB")

    small = out.resize((w, h), Image.LANCZOS)
    full = im.copy()
    full.paste(small, (x0, y0))
    full.save(dst)
    if preview:
        preview.mkdir(parents=True, exist_ok=True)
        before = crop.resize((w * 3, h * 3), Image.LANCZOS)
        after = small.resize((w * 3, h * 3), Image.LANCZOS)
        sheet = Image.new("RGB", (w * 6 + 10, h * 3), "white")
        sheet.paste(before, (0, 0)); sheet.paste(after, (w * 3 + 10, 0))
        sheet.save(preview / "s9-bandage-before-after.png")
    print("wrote", dst)


if __name__ == "__main__":
    run(Path(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None)
