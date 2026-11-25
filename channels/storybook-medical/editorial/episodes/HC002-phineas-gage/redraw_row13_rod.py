"""HC002-L 2026-11-25 (free): row 13, procedural redraw of the iron at 1:34 on row13-iron-v1.png (v1 kept).
1. cut the old rod (and its blue shadow) out and fill the rock behind it (a per-column gradient between the rock above and below, plus grain);
2. redraw the rod: the SAME length, thickness = length / 34, a straight body, tapering in a straight cone over its LAST QUARTER to a point,
   the other end blunt and cut flat; every column re-uses the OLD rod's own column (its shading strip) squeezed to the new thickness, the left
   cap is the old cap, and the ink outline is the old ink colour;
3. a new, narrower soft shadow under it.
Run from the repo root.  Output: row13-iron-v3redraw.png"""
import cv2
import numpy as np

K = "projects/hc002-l/assets/images/keyframes16x9/"
im = cv2.imread(K + "row13-iron-v1.png")
H, W = im.shape[:2]
X0, X1 = 156, 2640                  # old rod: left cap edge, tip
YT, YB = 700, 826                   # old rod: top and bottom outline rows (body)
L = X1 - X0
T0 = int(round(L / 34))             # new thickness 1:34
YC = (YT + YB) // 2
XT = X1 - L // 4                    # the taper starts one quarter from the tip
OLD_BODY_END = 2300

# 1. fill the rock where the old rod and its shadow were
out = im.copy().astype(np.float32)
y_a, y_b = 690, 884
x_a, x_b = X0 - 22, X1 + 54
top = im[y_a - 10:y_a, x_a:x_b].astype(np.float32).mean(axis=0)
bot = im[y_b:y_b + 10, x_a:x_b].astype(np.float32).mean(axis=0)
top = cv2.GaussianBlur(top[None], (0, 0), 6)[0]
bot = cv2.GaussianBlur(bot[None], (0, 0), 6)[0]
t = np.linspace(0, 1, y_b - y_a, dtype=np.float32)[:, None, None]
fill = top[None] * (1 - t) + bot[None] * t
rng = np.random.default_rng(3)
gn = lambda sg: cv2.GaussianBlur(rng.standard_normal((y_b - y_a, x_b - x_a)).astype(np.float32), (0, 0), sg)
grain = (gn(1.4) * 3.0 + gn(30) * 30.0)[..., None]   # fine grain + a little coarse mottling
out[y_a:y_b, x_a:x_b] = fill + grain
# feather the patch into its surroundings
mask = np.zeros((H, W), np.float32)
mask[y_a:y_b, x_a:x_b] = 1
mask = cv2.GaussianBlur(mask, (0, 0), 7)[..., None]
filled = (im.astype(np.float32) * (1 - mask) + out * mask)

def thickness(x):
    return T0 if x <= XT else max(1.0, T0 * (X1 - x) / (X1 - XT))


xs_ = np.arange(W)
prof = np.array([thickness(x) for x in xs_], np.float32)
prof = cv2.GaussianBlur(prof[None], (0, 0), 70)[0]      # round the kink where the taper starts
prof = np.where(xs_ > X1 - 40, np.array([thickness(x) for x in xs_], np.float32), prof)   # the tip itself stays sharp
prof[:XT - 300] = T0

# 2. a soft, narrow shadow under the new rod (before the rod itself)
sh = np.zeros((H, W), np.float32)
bottom_y = YC + T0 // 2
for x in range(X0 + 6, X1 + 12):
    thick = max(2, thickness(x))
    yb = int(YC + thick / 2)
    sh[yb:yb + int(0.42 * T0), x] = 1
sh = cv2.GaussianBlur(sh, (0, 0), 5)
sh[:, :X0 - 10] = 0
shadow_col = np.array([70, 62, 52], np.float32)      # BGR: a cool dark brown-grey, as the old shadow
filled = filled * (1 - 0.48 * sh[..., None]) + shadow_col * 0.48 * sh[..., None]

# 3. the rod: each column is the old rod's own column squeezed to the new thickness
res = filled.copy()
for x in range(X0, X1 + 1):
    th = float(prof[x])
    th_i = max(1, int(round(th)))
    ox = x if x < 300 else int(300 + (x - 300) * (OLD_BODY_END - 300) / (XT - 300)) if x <= XT else OLD_BODY_END
    ox = min(ox, W - 1)
    col = im[YT:YB + 1, ox:ox + 1]                         # old rod strip at that x
    new = cv2.resize(col, (1, th_i), interpolation=cv2.INTER_AREA).astype(np.float32)
    y0 = int(round(YC - th_i / 2))
    res[y0:y0 + th_i, x] = new[:, 0]
# ink outline (the old ink colour), top and bottom edges + the tip
ink = tuple(int(v) for v in np.median(im[YB - 1:YB + 1, 800:2200].reshape(-1, 3), axis=0))
ink = tuple(min(v, 70) for v in ink)
res8 = np.clip(res, 0, 255).astype(np.uint8)
top_pts = [(x, int(round(YC - prof[x] / 2))) for x in range(X0 + 8, X1 + 1, 6)] + [(X1, YC)]
bot_pts = [(x, int(round(YC + prof[x] / 2))) for x in range(X0 + 8, X1 + 1, 6)] + [(X1, YC)]
for pts in (top_pts, bot_pts):
    cv2.polylines(res8, [np.array(pts, np.int32)], False, ink, 4, cv2.LINE_AA)
# soften the pasted columns a touch so the strip reads painted, not stamped
blur = cv2.GaussianBlur(res8, (0, 0), 0.9)
band = np.zeros((H, W), np.float32)
band[YC - T0:YC + T0, X0 - 4:X1 + 8] = 1
band = cv2.GaussianBlur(band, (0, 0), 3)[..., None]
final = (res8 * (1 - 0.5 * band) + blur * 0.5 * band).astype(np.uint8)
cv2.imwrite(K + "row13-iron-v3redraw.png", final)
print("L", L, "T0", T0, "ratio 1:%.1f" % (L / T0), "taper", X1 - XT, "px =", round((X1 - XT) / L * 100), "% of length")
