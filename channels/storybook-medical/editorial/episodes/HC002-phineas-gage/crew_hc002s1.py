"""HC002-S1 shot 1 v3 (user 2026-11-19: "the crew ducks"): the two crewmen cut out of plate-s1 as sprites, and a clean
plate without them, so they can flinch while the camera pulls out. Free (local rembg masks + cv2 inpaint).

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/crew_hc002s1.py

Masks: fx_prep.cut(plate-s1, "crew-l" / "crew-r", rembg) -> refs/fx/plate-s1-crew-*.mask.png (already cut; re-run with
--cut). Writes sprites/crew-l, sprites/crew-r (stand-0.png + sprites.json, anchor = the feet) and refs/plate-s1-nocrew.png,
and prints each actor's w / x / y (frame fractions) so the sprite at rest sits exactly on the painted man.
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "channels/storybook-medical/scripts"))
P = ROOT / "projects/hc002-s1/assets/images"
PLATE = P / "refs/plate-s1.png"
BOXES = {"crew-l": (0.0, 0.565, 0.235, 0.935), "crew-r": (0.765, 0.56, 1.0, 0.92)}

if "--cut" in sys.argv:
    import fx_prep
    for name, box in BOXES.items():
        fx_prep.cut(str(PLATE), name, box, how="rembg", check=True)

im = np.array(Image.open(PLATE).convert("RGB"))
H, W = im.shape[:2]
top = (H - W * 16 / 9) * 0.5            # fit_frame crops the 9:16 window from the middle (focus 0.5)
hole = np.zeros((H, W), np.uint8)
out = {}
for name in BOXES:
    a = np.array(Image.open(P / f"refs/fx/plate-s1-{name}.mask.png").getchannel("A"))
    ys, xs = np.nonzero(a > 8)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([im[y0:y1, x0:x1], a[y0:y1, x0:x1]])
    # the feet: the mean x of the solid pixels in the bottom 4 % of the cut, at its bottom edge
    solid = a[y0:y1, x0:x1] > 128
    low = solid[int(0.96 * (y1 - y0)):]
    fx_ = (np.nonzero(low)[1].mean() if low.any() else (x1 - x0) / 2) / (x1 - x0)
    d = P / f"sprites/{name}"
    d.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba).save(d / "stand-0.png")
    json.dump({"source": "plate-s1 + crew_hc002s1.py", "canvas": [int(x1 - x0), int(y1 - y0)], "anchor": [round(fx_, 4), 1.0],
               "frames": {"stand": ["stand-0.png"]}}, open(d / "sprites.json", "w"), indent=1)
    out[name] = {"w": round((x1 - x0) / W, 4), "x": round((x0 + fx_ * (x1 - x0)) / W, 4),
                 "y": round((y1 - top) / (W * 16 / 9), 4), "anchor": [round(fx_, 4), 1.0]}
    hole |= ((a > 20) * 255).astype(np.uint8)
hole = cv2.dilate(hole, np.ones((11, 11), np.uint8))
clean = cv2.inpaint(cv2.cvtColor(im, cv2.COLOR_RGB2BGR), hole, 9, cv2.INPAINT_TELEA)
Image.fromarray(cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)).save(P / "refs/plate-s1-nocrew.png")
json.dump(out, open(P / "sprites/crew.json", "w"), indent=1)
print(json.dumps(out, indent=1))
