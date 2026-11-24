"""HC002-L row 58 (user 2026-11-24): paint out the RED scar line on the forehead of row58-deck-v2.orig.png, no replacement scar.
Free (OpenCV inpaint). The scar is the only reddish pixels there: score = (r-g) - (g-b) (scar ~ +48, skin ~ +8), plus the dark
remainder of the stroke along its own path; the eyebrow's black (y >= 276, lum < 60) is excluded. Output: row58-deck-v3.png.
    python .../paint_out_row58_scar.py
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KF = Path(__file__).resolve().parents[5] / "projects/hc002-l/assets/images/keyframes16x9"
PATH = [(1236, 233), (1239, 247), (1242, 256), (1240, 262), (1237, 269), (1240, 275), (1245, 282), (1248, 288)]
BOX = (1215, 225, 1265, 300)

im = Image.open(KF / "row58-deck-v2.orig.png").convert("RGB")
a = np.asarray(im).astype(int)
score = (a[..., 0] - a[..., 1]) - (a[..., 1] - a[..., 2])
lum = a.mean(-1)
red = (score > 22) & (a[..., 0] > 110)
box = np.zeros(red.shape, bool)
box[BOX[1]:BOX[3], BOX[0]:BOX[2]] = True
pm = Image.new("L", im.size, 0)
ImageDraw.Draw(pm).line(PATH, fill=255, width=9, joint="curve")
path = np.asarray(pm) > 0
loc = cv2.blur(lum.astype(np.float32), (15, 15))
brow = (lum < 60) & (np.arange(im.height)[:, None] >= 276)
mask = (red & box) | (path & (((score > 15) & (a[..., 0] > 110)) | ((loc - lum) > 14)) & ~brow)
mask = np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(3)))
out = cv2.inpaint(np.asarray(im)[..., ::-1].copy(), mask, 4, cv2.INPAINT_TELEA)[..., ::-1]
Image.fromarray(out).save(KF / "row58-deck-v3.png")
print("painted", int((mask > 0).sum()), "px ->", KF / "row58-deck-v3.png")
