"""HC002-L 2026-11-25 (free): paint the scar off the RIGHT forehead (picture-left) of rows 27 and 42; no replacement; originals kept.
Same method as row 58: a thin corridor along the measured scar path AND the pixels that differ from their surroundings, then a small inpaint."""
import cv2
import numpy as np

K = "projects/hc002-l/assets/images/keyframes16x9/"


def fix(src, dst, pts, width, thr):
    im = cv2.imread(K + src)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dev = np.abs(g - cv2.GaussianBlur(g, (0, 0), 10))
    corridor = np.zeros(g.shape, np.uint8)
    cv2.polylines(corridor, [np.array(pts, np.int32)], False, 255, width)
    m = cv2.bitwise_and(corridor, (dev > thr).astype(np.uint8) * 255)
    m = cv2.dilate(m, np.ones((3, 3), np.uint8), iterations=2)
    out = cv2.inpaint(im, m, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(K + dst, out)
    print(dst, "pixels", int((m > 0).sum()))


fix("row27-profile-v1.png", "row27-profile-v2paint.png", [(1290, 335), (1245, 400), (1210, 460), (1185, 530)], 34, 5)
fix("row42-barnum-v1.png", "row42-barnum-v2paint.png", [(1190, 293), (1185, 308), (1181, 322), (1180, 334)], 15, 9)
