"""HC002-S1 shot 8 (user 2026-11-18): "the lying -> propped change jumps in size and position, so it reads as a cut.
Match the propped pose's scale and place to the lying body so the shoulder rises from where it lay (add an in-between
'shoulder lifting' state if a free one exists)." Free, local; run after cutouts_hc002s1.py.
  - scale: the propped drawing came back bigger; scale it so his head (the grey hair) matches the lying head's size;
  - place: pin it at the waist (the straight cut at the left edge, the trouser band's centre);
  - lift-0: the in-between, the "fingers" frame tipped up around the waist, so the shoulder starts to rise in place.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/match_s8.py
"""
import json
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

S = Path(__file__).resolve().parents[5] / "projects/hc002-s1/assets/images/sprites/gage-s8"
LIFT_DEG = float(sys.argv[1]) if len(sys.argv) > 1 else 14


def rgba(name):
    return np.array(Image.open(S / name).convert("RGBA"))


def hair_box(a):
    """Bounding box of the largest grey (low saturation, mid tone) region: his dusty hair."""
    rgb = a[..., :3].astype(int)
    lum = rgb.mean(2)
    grey = (np.abs(rgb[..., 0] - rgb[..., 2]) < 28) & (np.abs(rgb[..., 0] - rgb[..., 1]) < 28) & (lum > 60) & (lum < 175) \
        & (a[..., 3] > 200)
    grey = cv2.morphologyEx(grey.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(grey)
    i = 1 + int(np.argmax(st[1:, 4]))
    x, y, w, h, area = st[i]
    return x, y, w, h, area


def waist(a):
    """The waist cut: the leftmost opaque columns; returns (x of the cut, centre y of the trouser band)."""
    cols = np.nonzero((a[..., 3] > 200).any(axis=0))[0]
    x0 = cols.min()
    band = np.nonzero(a[:, x0:x0 + 12, 3].max(axis=1) > 200)[0]
    return x0, (band.min() + band.max()) / 2


for f in ("prop-0.png",):
    if not (S / "prop-0.unmatched.png").exists():
        shutil.copy(S / f, S / "prop-0.unmatched.png")
lie, fing, prop = rgba("lie-0.png"), rgba("fingers-0.png"), rgba("prop-0.unmatched.png")
H, W = lie.shape[:2]
hl, hp = hair_box(lie), hair_box(prop)
scale = float(np.sqrt(hl[4] / hp[4]))
print(f"hair area lie {hl[4]} prop {hp[4]} -> scale {scale:.3f}")
small = cv2.resize(prop, (round(prop.shape[1] * scale), round(prop.shape[0] * scale)), interpolation=cv2.INTER_AREA)
(lx, ly), (px, py) = waist(lie), waist(small)
dx, dy = lx - px, ly - py
M = np.float32([[1, 0, dx], [0, 1, dy]])
matched = cv2.warpAffine(small, M, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
Image.fromarray(matched, "RGBA").save(S / "prop-0.png")
print(f"prop pinned at the waist: shift {dx:.0f}, {dy:.0f}")

# in-between: the fingers frame tipped up around the waist (negative = counter-clockwise: the head end rises)
R = cv2.getRotationMatrix2D((float(lx), float(ly)), LIFT_DEG, 1.0)
lift = cv2.warpAffine(fing, R, (W, H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
Image.fromarray(lift, "RGBA").save(S / "lift-0.png")

m = json.load(open(S / "sprites.json"))
m["frames"] = {"lie": ["lie-0.png"], "fingers": ["fingers-0.png"], "lift": ["lift-0.png"], "prop": ["prop-0.png"]}
m["source"] = "pose-gage-s8.png + match_s8.py (prop scaled to the lying head and pinned at the waist; lift = tipped fingers)"
json.dump(m, open(S / "sprites.json", "w"), indent=1)

# onion check: lie, lift, prop over each other
on = np.zeros((H, W, 3), np.float32) + [255, 0, 255]
for fr, col in ((lie, (0, 255, 255)), (lift, (255, 255, 0)), (matched, (255, 255, 255))):
    a = fr[..., 3:4] / 255.0 * 0.45
    on = on * (1 - a) + fr[..., :3] * a
Image.fromarray(on.clip(0, 255).astype(np.uint8)).save(S / "match-check.png")
print("ok")
