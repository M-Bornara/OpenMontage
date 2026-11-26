"""HC002-L 2026-11-25 (free): row 43 still 2 = row 43a with the iron painted out (an empty shelf, the same label). No generation.
The rod is masked (not the card in front of it), the shelf wood and jars behind are inpainted, fine grain added. Run from the repo root."""
import cv2
import numpy as np

K = "projects/hc002-l/assets/images/keyframes16x9/"
im = cv2.imread(K + "row43a-shelf-v1.png")
H, W = im.shape[:2]
S, OX, OY = 2350 / 1600, 400, 620          # the 1600-wide crop of x 400..2750, y 620..1100 used to measure the polygons


def pts(p):
    return np.array([[OX + x * S, OY + y * S] for x, y in p], np.int32)


rod = pts([(60, 80), (400, 128), (745, 152), (1190, 198), (1470, 282), (1508, 298), (1520, 346), (1190, 300), (745, 246), (340, 216), (50, 176)])
card = pts([(430, 78), (748, 102), (768, 160), (748, 206), (692, 264), (682, 288), (343, 243)])
m = np.zeros((H, W), np.uint8)
cv2.fillPoly(m, [rod], 255)
c = np.zeros((H, W), np.uint8)
cv2.fillPoly(c, [card], 255)
m[c > 0] = 0
m = cv2.dilate(m, np.ones((5, 5), np.uint8), iterations=2)
m[c > 0] = 0
out = cv2.inpaint(im, m, 14, cv2.INPAINT_TELEA)
rng = np.random.default_rng(5)
g = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 1.3)[..., None] * 4.0
soft = cv2.GaussianBlur(m, (0, 0), 4).astype(np.float32)[..., None] / 255.0
out = np.clip(out.astype(np.float32) + g * soft, 0, 255).astype(np.uint8)
res = (im * (1 - soft) + out * soft).astype(np.uint8)
# second pass: the rod's tip shadow at the right, and the dark wedge left behind the card
m2 = np.zeros((H, W), np.uint8)
cv2.fillPoly(m2, [np.array([(2300, 935), (2670, 980), (2670, 1095), (2300, 1070)], np.int32)], 255)
cv2.fillPoly(m2, [np.array([(1410, 835), (1580, 835), (1580, 955), (1410, 955)], np.int32)], 255)
m2[c > 0] = 0
m2 = cv2.dilate(m2, np.ones((5, 5), np.uint8), iterations=1)
res2 = cv2.inpaint(res, m2, 14, cv2.INPAINT_TELEA)
soft2 = cv2.GaussianBlur(m2, (0, 0), 4).astype(np.float32)[..., None] / 255.0
res = np.clip(res.astype(np.float32) * (1 - soft2) + (res2.astype(np.float32) + g * soft2) * soft2, 0, 255).astype(np.uint8)
cv2.imwrite(K + "row43b-shelf-v1paint.png", res)
print("mask px", int((m > 0).sum()))
