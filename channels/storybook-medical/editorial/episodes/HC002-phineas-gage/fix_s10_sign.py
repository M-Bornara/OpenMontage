"""HC002-S1 s10 (both formats): the hotel came back with a readable "CAVENDISH HOTEL" sign (NO_TEXT). The board is a flat
cream panel: find it as the largest cream region in the search box, treat the letters as holes in it, and inpaint only
those holes from the board around them. The originals stay as <name>.lettered.png. Free, local.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/fix_s10_sign.py
"""
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

P = Path(__file__).resolve().parents[5] / "projects/hc002-s1/assets/images"
# image -> search box (fractions of the image)
JOBS = {P / "keyframes/s10.png": (0.25, 0.18, 0.80, 0.36), P / "keyframes16x9/s10.png": (0.33, 0.0, 0.70, 0.22)}
out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else None

for f, (bx0, by0, bx1, by1) in JOBS.items():
    keep = f.with_name(f.stem + ".lettered.png")
    if not keep.exists():
        shutil.copy(f, keep)
    im = np.array(Image.open(keep).convert("RGB"))
    H, W = im.shape[:2]
    x0, y0, x1, y1 = int(bx0 * W), int(by0 * H), int(bx1 * W), int(by1 * H)
    sub = im[y0:y1, x0:x1].astype(int)
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    cream = ((r + g + b) / 3 > 165) & (r >= g) & (g >= b) & (r - b > 25) & (r - b < 110)
    cream = cv2.morphologyEx(cream.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(cream)
    k = 1 + int(np.argmax(st[1:, 4]))
    board = (lab == k).astype(np.uint8)
    # the letters: holes inside the board (fill from outside, what stays unreached and is not board = holes)
    h, w = board.shape
    flood = np.pad(board, 1) * 255
    cv2.floodFill(flood, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 128)
    holes = ((flood[1:-1, 1:-1] == 0)).astype(np.uint8)
    holes = cv2.dilate(holes, np.ones((9, 9), np.uint8))   # 9: the letters' soft edges too
    mask = np.zeros((H, W), np.uint8)
    mask[y0:y1, x0:x1] = holes * 255
    fixed = cv2.inpaint(im, mask, 7, cv2.INPAINT_TELEA)
    Image.fromarray(fixed).save(f)
    bx, by, bw, bh = st[k, :4]
    print(f.parent.name, f.name, "board", (x0 + bx, y0 + by, bw, bh), "letter px", int(holes.sum()))
    if out_dir:
        pad = 40
        c = Image.fromarray(fixed[max(0, y0 + by - pad):y0 + by + bh + pad, max(0, x0 + bx - pad):x0 + bx + bw + pad])
        c.save(out_dir / f"s10_{f.parent.name}.png")
