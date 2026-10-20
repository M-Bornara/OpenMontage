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


def subject_mask(image: str, out: str, box: tuple[float, float, float, float], width: int = 1920, grow: int = 2) -> str:
    from rembg import remove

    im = Image.open(image).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    W, H = im.size
    x0, y0, x1, y1 = (round(v / 100 * s) for v, s in zip(box, (W, H, W, H)))
    alpha = remove(im.crop((x0, y0, x1, y1)), session=_session()).getchannel("A")
    full = Image.new("L", (W, H), 0)
    full.paste(alpha, (x0, y0))
    if grow:
        full = full.filter(ImageFilter.MaxFilter(grow * 2 + 1)).filter(ImageFilter.GaussianBlur(grow))
    mask = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    mask.putalpha(full)
    mask.save(out)
    cover = sum(full.histogram()[i] * i for i in range(256)) / 255 / (W * H) * 100
    print(f"mask -> {out} ({cover:.1f}% of frame)")
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
