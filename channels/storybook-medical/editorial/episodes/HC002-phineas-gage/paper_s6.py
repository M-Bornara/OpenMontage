"""HC002-S1 shot 6 (FREE, storyboard v1): Harlow's 1868 engraving of the skull, printed on aged paper, for both formats.

Source: Fig. 2 of the plate in Harlow 1868 (public domain), cropped from the Internet Archive scan of the NLM copy
(archive.org/details/66210360R.nlm.nih.gov, page image 0024, box 881,473-1482,1280, levels stretched so the scan paper
reads white) -> refs/harlow_skull_1868_full.png (601 x 807). The Commons file "Phineas gage - 1868 skull diagram.jpg" is
only 165 px (its original IS that size), kept as harlow_skull_1868.jpg. The edit's path points are ENGRAVING fractions
measured on the full plate and mapped through the placement below.

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/paper_s6.py
Writes assets/images/keyframes/s6.png (1536 x 2752), keyframes16x9/s6.png (2752 x 1536) and s6_layout.json.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

P = Path("projects/hc002-s1")
REFS = P / "refs"
OUT = P / "assets/images"
# 9:16: the engraving's top at 22 % of the frame, 66 % of the frame tall (under the TOP caption at y 288, the entry
# point under the cheekbone at ~y 1259 of 1920); 16:9: centred, 88 % of the height
LAYOUT = {"9x16": {"size": (1536, 2752), "top": 0.22, "h": 0.66}, "16x9": {"size": (2752, 1536), "top": 0.06, "h": 0.88}}


def source() -> tuple[Image.Image, str]:
    for name in ("harlow_skull_1868_full.jpg", "harlow_skull_1868_full.png", "harlow_skull_1868_full.tif",
                 "harlow_skull_1868.jpg"):
        if (REFS / name).exists():
            return Image.open(REFS / name).convert("L"), name
    raise SystemExit("no Harlow engraving in refs/")


def paper(size: tuple[int, int], seed: int = 11) -> np.ndarray:
    """Aged paper: warm cream, soft mottling, faint fibres, darker edges (deterministic)."""
    W, H = size
    rng = np.random.default_rng(seed)
    base = np.array([234, 222, 194], np.float32)
    mott = Image.fromarray((rng.random((H // 24, W // 24)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
    mott = np.asarray(mott.filter(ImageFilter.GaussianBlur(40)), np.float32) / 255 - 0.5
    grain = np.asarray(Image.fromarray((rng.random((H, W)) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)),
                       np.float32) / 255 - 0.5
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
    vig = np.clip((r - 0.65) / 0.75, 0, 1) ** 1.6
    img = base[None, None, :] * (1 + 0.07 * mott[..., None] + 0.035 * grain[..., None])
    img = img * (1 - 0.32 * vig[..., None]) + np.array([-6, -10, -22], np.float32) * vig[..., None]
    return np.clip(img, 0, 255)


def compose(fmt: str, eng: Image.Image) -> tuple[Image.Image, dict]:
    L = LAYOUT[fmt]
    W, H = L["size"]
    h = round(L["h"] * H)
    w = round(h * eng.width / eng.height)
    e = eng.resize((w, h), Image.LANCZOS)
    if eng.width < 600:   # the 165 px stand-in: soften the upscale so the jpeg blocks don't read as pixels
        e = e.filter(ImageFilter.GaussianBlur(1.2))
    ink = np.asarray(e, np.float32) / 255            # 1 = paper, 0 = ink
    ink = np.clip((ink - 0.12) / 0.8, 0, 1)          # the white of the scan becomes the paper, not a grey box
    x0, y0 = (W - w) // 2, round(L["top"] * H)
    img = paper((W, H))
    reg = img[y0:y0 + h, x0:x0 + w]
    color = np.array([46, 34, 26], np.float32)        # warm brown-black printing ink
    img[y0:y0 + h, x0:x0 + w] = reg * ink[..., None] + color * (1 - ink[..., None]) * 0.9 + reg * (1 - ink[..., None]) * 0.1
    lay = {"x0": x0 / W, "y0": y0 / H, "w": w / W, "h": h / H}
    return Image.fromarray(img.astype(np.uint8)), lay


def main():
    eng, name = source()
    out = {"source": name, "source_px": list(eng.size)}
    for fmt, folder in (("9x16", "keyframes"), ("16x9", "keyframes16x9")):
        im, lay = compose(fmt, eng)
        im.save(OUT / folder / "s6.png")
        out[fmt] = lay
    json.dump(out, open(OUT / "keyframes/s6_layout.json", "w"), indent=1)
    print(f"s6 from {name} {eng.size}: {out['9x16']}")


if __name__ == "__main__":
    main()
