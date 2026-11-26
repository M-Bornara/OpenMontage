"""HC002-L 2026-11-25 (free): sheet-gage-chile-v3.png = v2 with the scar moved onto his LEFT forehead (picture-right).
v2 had a faint scar line on the picture-LEFT forehead (his right) in the top-left bust and the top-right head (the top-right head also has
the right one on picture-right). Here the wrong-side line is inpainted away, and in the bust a faint pale scar is added on the picture-right
forehead (a mirrored copy of the removed line's mask). v2 is kept. Run from the repo root.
"""
import cv2
import numpy as np

D = "projects/hc002-l/assets/images/refs/"
im = cv2.imread(D + "sheet-gage-chile-v2.png")


def line_mask(box, thr=7):
    x0, y0, x1, y1 = box
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    loc = g - cv2.GaussianBlur(g, (0, 0), 7)
    m = np.zeros(g.shape, np.uint8)
    m[y0:y1, x0:x1] = (loc[y0:y1, x0:x1] < -thr).astype(np.uint8) * 255
    return m


def clean(box, thr=7):
    m = line_mask(box, thr)
    return cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)


out = im.copy()


def path_mask(pts, width, box, thr=4):
    """The scar line only: a thin corridor along the measured path AND the pixels darker than their surroundings."""
    corridor = np.zeros(im.shape[:2], np.uint8)
    cv2.polylines(corridor, [np.array(pts, np.int32)], False, 255, width)
    m = cv2.bitwise_and(corridor, line_mask(box, thr))
    return cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=1)


# A: top-left bust (centre x 1988): remove the picture-left line, add a pale one at the mirrored place
CXA = 1988
mA = path_mask([(1957, 148), (1953, 168), (1950, 190)], 11, (1925, 138, 1990, 215))
# B: top-right head: remove the picture-left line only (the picture-right one stays)
mB = path_mask([(2438, 196), (2430, 220), (2421, 247)], 11, (2410, 175, 2465, 262))
for m in (mA, mB):
    out = cv2.inpaint(out, m, 3, cv2.INPAINT_TELEA)
flip = np.zeros(im.shape[:2], np.uint8)
ys, xs = np.nonzero(mA)
nx = 2 * CXA - xs
flip[ys, nx] = 255
flip = cv2.GaussianBlur(flip, (0, 0), 1.0).astype(np.float32) / 255.0
out = np.clip(out.astype(np.float32) + flip[..., None] * 40.0, 0, 255).astype(np.uint8)
cv2.imwrite(D + "sheet-gage-chile-v3.png", out)
print("A px", int((mA > 0).sum()), "B px", int((mB > 0).sum()))
