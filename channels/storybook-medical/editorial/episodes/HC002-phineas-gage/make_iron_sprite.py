"""HC002-L 2026-11-25 (free): the rigid iron SPRITE for the HIT shot, cut (never redrawn) from the approved 1:34 iron of row 13.
iron-ref.png itself is a noisy, low-resolution crop of the real iron photograph (no clean edge to cut), so the sprite is cut from
row13-iron-v3redraw.png: the same rod the viewer already saw in row 13 (thickness = length / 34, straight body, the last quarter tapers to a point
at the RIGHT, the left end blunt and flat). The cut is the rod's own geometry (redraw_row13_rod.py: X0 156, tip 2640, centre row 763) with the
background and the shadow left out. Output: assets/images/sprites/iron-hit-sprite.png (RGBA, the tip at the right).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/make_iron_sprite.py     (from the repo root)"""
import cv2
import numpy as np

P = "projects/hc002-l/assets/images/"
im = cv2.imread(P + "keyframes16x9/row13-iron-v3redraw.png")
X0, X1 = 156, 2640
L = X1 - X0
T = int(round(L / 34))                 # 73 px thick
YC = 763
XT = X1 - L // 4                       # the taper starts a quarter from the tip
half = T / 2
SS = 4                                 # supersample the mask for a clean antialiased edge
pad = 6
w, h = L + 2 * pad, T + 2 * pad
big = np.zeros((h * SS, w * SS), np.uint8)
pts = np.array([[pad, pad + 1], [XT - X0 + pad, pad + 1], [L + pad, pad + half], [XT - X0 + pad, pad + T - 1], [pad, pad + T - 1]], np.float32) * SS
cv2.fillPoly(big, [pts.astype(np.int32)], 255)
alpha = cv2.resize(big, (w, h), interpolation=cv2.INTER_AREA)
alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8))                       # 1 px in: no rock fringe on the ink outline
crop = im[int(YC - half) - pad:int(YC - half) - pad + h, X0 - pad:X0 - pad + w]
out = np.dstack([crop, alpha])
cv2.imwrite(P + "sprites/iron-hit-sprite.png", out)
print(out.shape, "thickness", T, "length", L, "ratio 1:%.1f" % (L / T))
