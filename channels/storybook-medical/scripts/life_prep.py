"""Free prep for living stills (Life.tsx): region masks (sky, water, fire...), subject cut-outs and a background plate with
the subject painted out (OpenCV inpaint), so a subject can move (parallax, sway, bob) without revealing a hole.

    from life_prep import plate, region, subject, clean_plate
Coordinates are percent of the image. All outputs are PNG/JPG in the Remotion public/img folder.
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from masks import subject_mask

MASK_W = 1920


def plate(src: str, out: str, width: int = 2880) -> str:
    """The still itself, at a resolution above the output, so zooms and pans stay sharp and smooth."""
    im = Image.open(src).convert("RGB")
    im.resize((width, round(im.height * width / im.width)), Image.LANCZOS).save(out, quality=93)
    return out


def _save_alpha(a: np.ndarray, out: str) -> str:
    m = Image.new("RGBA", (a.shape[1], a.shape[0]), (255, 255, 255, 0))
    m.putalpha(Image.fromarray(a))
    m.save(out)
    return out


def region(src: str, out: str, poly: list[tuple[float, float]], feather: float = 1.2,
           brighter_than: int | None = None, darker_than: int | None = None, minus: list[str] = ()) -> str:
    """A soft region mask from a polygon, optionally keeping only pixels brighter/darker than a lightness value (sky vs
    treeline, water vs dock posts), minus other masks (e.g. the canoe inside the water)."""
    im = Image.open(src).convert("RGB")
    im = im.resize((MASK_W, round(im.height * MASK_W / im.width)), Image.LANCZOS)
    W, H = im.size
    poly_img = Image.new("L", (W, H), 0)
    ImageDraw.Draw(poly_img).polygon([(x / 100 * W, y / 100 * H) for x, y in poly], fill=255)
    a = np.array(poly_img).astype(np.float32)
    L = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2LAB)[:, :, 0].astype(np.float32)
    if brighter_than is not None:
        a *= np.clip((L - brighter_than) / 18 + 0.5, 0, 1)
    if darker_than is not None:
        a *= np.clip((darker_than - L) / 18 + 0.5, 0, 1)
    a = cv2.morphologyEx(a, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    for m in minus:
        sub = np.array(Image.open(m).getchannel("A").resize((W, H))).astype(np.float32)
        sub = cv2.dilate(sub, np.ones((15, 15), np.uint8))
        a *= 1 - sub / 255
    k = max(3, int(feather / 100 * W) | 1)
    a = cv2.GaussianBlur(a, (k, k), 0)
    return _save_alpha(np.clip(a, 0, 255).astype(np.uint8), out)


def subject(src: str, out: str, box: tuple[float, float, float, float]) -> str:
    return subject_mask(src, out, box, width=MASK_W, grow=2)


def clean_plate(src: str, masks: list[str], out: str, width: int = 2880, grow: int = 18) -> str:
    """The background with the subjects painted out (Telea inpaint on a grown mask). Good enough for the few pixels
    a subject moves (parallax / sway); never shown on its own."""
    im = Image.open(src).convert("RGB")
    im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    W, H = im.size
    hole = np.zeros((H, W), np.uint8)
    for m in masks:
        a = np.array(Image.open(m).getchannel("A").resize((W, H)))
        hole = np.maximum(hole, (a > 20).astype(np.uint8) * 255)
    hole = cv2.dilate(hole, np.ones((grow * 2 + 1, grow * 2 + 1), np.uint8))
    # inpaint at half size (much faster, the fill is soft anyway), then paste the fill back at full size
    small = cv2.resize(np.array(im), (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    hs = cv2.resize(hole, (W // 2, H // 2), interpolation=cv2.INTER_NEAREST)
    filled = cv2.inpaint(cv2.cvtColor(small, cv2.COLOR_RGB2BGR), hs, 9, cv2.INPAINT_TELEA)
    filled = cv2.cvtColor(cv2.resize(filled, (W, H), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB)
    soft = cv2.GaussianBlur(hole.astype(np.float32), (31, 31), 0)[:, :, None] / 255
    res = np.array(im) * (1 - soft) + filled * soft
    Image.fromarray(res.astype(np.uint8)).filter(ImageFilter.SMOOTH).save(out, quality=92)
    return out

