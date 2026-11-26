"""HC002-L rows 21 and 30: free bandage paint fix on S1's 16:9 s10 and s12 (user 2026-11-23, the open fix from Nov 19).

Same fix as s9 (paint_bandage_s9_16x9.py) and the 9:16 stills: the patch stays over his LEFT eye (right of the picture), the
band that runs flat across BOTH brows is painted OUT over his RIGHT brow and forehead (left of the picture: skin + eyebrow
show). Pixel coordinates measured on an 8x grid of the 2752x1536 stills. Pillow + numpy, 4x supersampled.

    python .../paint_bandage_s10_s12_16x9.py [--preview DIR]

The originals stay as s10.orig.png / s12.orig.png (made on the first run); the fix always starts from them.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[5]
KF = REPO / "projects/hc002-s1/assets/images/keyframes16x9"
Z = 4

CFG = {
    # s10: Gage on the piazza. Patch diagonal starts at about (1456, 584); the flat band left of x=1458 is removed.
    "s10": dict(box=(1410, 540, 1520, 640),
                skin_sample=(1448, 610, 1466, 626),            # lit cheek, beside the nose
                skin_poly=[(1436, 565), (1446, 562), (1458, 564), (1459, 584), (1452, 586), (1443, 588), (1436, 587)],
                brow=[(1441, 590), (1446, 588.5), (1452, 588.5), (1457, 590)], brow_w=1.6,
                shade=[(1458, 565), (1459, 585)]),
    # s12: Gage far down the street (face ~40 px). The flat band left of x=1080 is removed, the patch end stays on the right.
    "s12": dict(box=(1040, 430, 1120, 500),
                skin_sample=(1066, 482, 1080, 492),
                skin_poly=[(1064, 452), (1074, 450), (1081, 452), (1081, 476), (1070, 478), (1064, 474)],
                brow=[(1064, 468), (1068, 466.5), (1074, 466.5), (1079, 468)], brow_w=1.2,
                shade=[(1081, 452), (1081, 476)]),
}


def fix(name: str, preview: Path | None):
    c = CFG[name]
    dst, src = KF / f"{name}.png", KF / f"{name}.orig.png"
    if not src.exists():
        src.write_bytes(dst.read_bytes())
    im = Image.open(src).convert("RGB")
    x0, y0, x1, y1 = c["box"]
    crop = im.crop(c["box"])
    w, h = crop.size
    big = crop.resize((w * Z, h * Z), Image.LANCZOS)
    arr = np.asarray(big).astype(np.float32)
    sx0, sy0, sx1, sy1 = c["skin_sample"]
    reg = np.asarray(im.crop(c["skin_sample"])).reshape(-1, 3).astype(np.float32)
    ok = (reg[:, 0] > 120) & (reg[:, 0] - reg[:, 2] > 25)
    skin = np.percentile(reg[ok], 60, axis=0) if ok.sum() > 10 else reg.mean(0)
    m = Image.new("L", (w * Z, h * Z), 0)
    ImageDraw.Draw(m).polygon([((x - x0) * Z, (y - y0) * Z) for x, y in c["skin_poly"]], fill=255)
    # only the BAND (light, low colour) and its dark ink outline are replaced: hair, skin and the head outline stay
    lum = arr.mean(-1)
    sat = arr.max(-1) - arr.min(-1)
    like = (((lum > 150) & (sat < 70)) | (lum < 55)).astype(np.uint8) * 255
    like = np.asarray(Image.fromarray(like).filter(ImageFilter.MaxFilter(Z + 1)).filter(ImageFilter.GaussianBlur(Z * 0.3))).astype(np.float32) / 255
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(Z * 0.6))).astype(np.float32) / 255
    m = (m * like)[..., None]
    # a faint forehead shading: a touch darker toward the hair, lighter below
    yy = np.linspace(0, 1, h * Z)[:, None, None]
    tone = skin[None, None, :] * (0.93 + 0.08 * yy)
    arr = arr * (1 - m) + tone * m
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out, "RGBA")
    d.line([((x - x0) * Z, (y - y0) * Z) for x, y in c["brow"]], fill=(58, 38, 28, 255), width=int(c["brow_w"] * Z), joint="curve")
    d.line([((x - x0) * Z, (y - y0) * Z) for x, y in c["shade"]], fill=(70, 50, 40, 90), width=int(0.8 * Z))
    small = out.resize((w, h), Image.LANCZOS)
    full = im.copy()
    full.paste(small, (x0, y0))
    full.save(dst)
    if preview:
        preview.mkdir(parents=True, exist_ok=True)
        s = 6
        sheet = Image.new("RGB", (w * s * 2 + 10, h * s), "white")
        sheet.paste(crop.resize((w * s, h * s), Image.LANCZOS), (0, 0))
        sheet.paste(small.resize((w * s, h * s), Image.LANCZOS), (w * s + 10, 0))
        sheet.save(preview / f"{name}-bandage-before-after.png")
    print("wrote", dst)


if __name__ == "__main__":
    pv = Path(sys.argv[sys.argv.index("--preview") + 1]) if "--preview" in sys.argv else None
    for n in CFG:
        fix(n, pv)
