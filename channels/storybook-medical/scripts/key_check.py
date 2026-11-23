"""Chroma-key PRE-FLIGHT: pick the key colour BEFORE a sprite / pose sheet is generated (user 2026-11-22).

Why: fx_prep.sheet() keys against the flat background with soft thresholds (alpha ramps from distance 38 to 110 in RGB).
Anything in the drawing that sits within 110 of the key comes out partly or fully see-through. HC003-S1: the green key
(#00B140) ate Troffea's blue dress and the wagon's dark teal-brown interior (a half-invisible rider, cobbles showing
through the wagon). The colours are known BEFORE generation (model sheets, the plate it goes into, the style palette), so
measure them first and ask the sheet for the key that stays furthest from them.

    python channels/storybook-medical/scripts/key_check.py <image or #hex> [<image or #hex> ...]
    e.g. key_check.py projects/hc003-s1/assets/images/refs/sheet-troffea.png projects/hc003-s1/assets/images/refs/plate-s10.png "#1F4E5A"

Images: a model sheet / plate / reference. Pixels like the border (paper, flat background) are skipped. Exit code 1 when
even the best key is risky (> RISK share), so a script can stop. Free, runs offline.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

LO, HI = 38.0, 110.0           # fx_prep._key_alpha thresholds: below LO the pixel is removed, LO..HI it turns see-through
RISK = 0.01                    # more than 1 % of the drawing's pixels inside HI of the key = pick another key
KEYS = {                       # name: (rgb, wording for the sheet prompt; prompt_kit.KEY_BGS)
    "green": (0, 177, 64),
    "magenta": (255, 0, 255),
    "blue": (0, 71, 187),
    "orange": (255, 120, 0),
}


def _hex(s: str) -> np.ndarray:
    s = s.lstrip("#")
    return np.array([[int(s[i:i + 2], 16) for i in (0, 2, 4)]], dtype=np.float32)


def sample(src: str, n: int = 60000) -> np.ndarray:
    """Subject pixels of an image (or one pixel of a hex colour), as float RGB rows."""
    if src.startswith("#"):
        return _hex(src)
    im = np.array(Image.open(src).convert("RGB"))
    H, W = im.shape[:2]
    border = np.concatenate([im[:8].reshape(-1, 3), im[-8:].reshape(-1, 3), im[:, :8].reshape(-1, 3), im[:, -8:].reshape(-1, 3)])
    bg = np.median(border, axis=0)
    px = im.reshape(-1, 3).astype(np.float32)
    flat_border = float(np.sqrt(((border.astype(np.float32) - bg) ** 2).sum(1)).mean()) < 20   # a flat sheet background
    if flat_border:
        px = px[np.sqrt(((px - bg) ** 2).sum(1)) > 40]
    rng = np.random.default_rng(1)
    return px[rng.choice(len(px), min(n, len(px)), replace=False)] if len(px) else px


def score(px: np.ndarray, key: tuple[int, int, int]) -> dict:
    d = np.sqrt(((px - np.array(key, dtype=np.float32)) ** 2).sum(1))
    return {"lost": float((d < LO).mean()), "leaky": float(((d >= LO) & (d < HI)).mean()), "min": float(d.min())}


def worst_colours(px: np.ndarray, key, k: int = 3) -> list[str]:
    d = np.sqrt(((px - np.array(key, dtype=np.float32)) ** 2).sum(1))
    near = px[d < HI]
    if not len(near):
        return []
    q = (near // 32 * 32 + 16).astype(int)
    vals, cnt = np.unique(q, axis=0, return_counts=True)
    return [f"#{v[0]:02X}{v[1]:02X}{v[2]:02X} ({c / len(px):.1%})" for v, c in sorted(zip(vals, cnt), key=lambda t: -t[1])[:k]]


def check(sources: list[str]) -> tuple[str, dict]:
    px = np.concatenate([sample(s) for s in sources])
    res = {name: score(px, rgb) for name, rgb in KEYS.items()}
    best = min(res, key=lambda n: res[n]["lost"] + res[n]["leaky"])
    return best, {"px": px, "res": res}


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    best, info = check(argv)
    px, res = info["px"], info["res"]
    print(f"{len(px)} sampled drawing pixels from {len(argv)} source(s)\n")
    print(f"{'key':8} {'rgb':14} {'removed':>8} {'see-through':>12}  {'nearest colour':>14}   colours at risk")
    for name, rgb in KEYS.items():
        r = res[name]
        mark = "  <- best" if name == best else ""
        print(f"{name:8} {str(rgb):14} {r['lost']:8.1%} {r['leaky']:12.1%} {r['min']:14.0f}   "
              f"{', '.join(worst_colours(px, rgb)) or '-'}{mark}")
    r = res[best]
    risky = r["lost"] + r["leaky"] > RISK
    print(f"\nUse key={best!r} for these sheets (prompt_kit.sprite_sheet(..., key='{best}'))."
          + ("  WARNING: even the best key puts more than 1 % of the drawing at risk: key the sheet by hand or use how='rembg'." if risky else ""))
    return 1 if risky else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
