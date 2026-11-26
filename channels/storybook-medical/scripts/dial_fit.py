"""Fit a painted watch dial (perspective = an affine circle) to its 12 hour marks, so drawn hands point exactly at the
painted marks and their tips trace the painted ring. Rule L5 (prompt_kit): watches are generated WITHOUT hands; Clock.tsx
draws them. `fit(path, centre_guess, radius_guess, stem)` -> dict(x, y, marks) in SOURCE pixels: (x, y) = the centre pin, marks =
the 12 hour marks' centres from 12 o'clock clockwise. 12 o'clock is the mark under the STEM (where the crown and chain
bow attach): a painted dial has no numerals and is drawn tilted, so "the top mark" is not 12 (user review 2026-10-26:
every time read one hour early) (painted dials are never a perfect ellipse around the pin, so Clock.tsx
interpolates between the MEASURED marks; a mark the detector misses is filled from an affine fit of the others).
`python dial_fit.py IMAGE cx cy R stemx stemy OUT.jpg` draws hands at 12/3/6/9 o'clock over the image as a check."""
import math
import sys

import cv2
import numpy as np


def fit(path, cx, cy, R, stem):
    im = cv2.imread(str(path))
    x0, y0 = cx - R, cy - R
    hsv = cv2.cvtColor(im[y0:cy + R, x0:cx + R], cv2.COLOR_BGR2HSV)
    cream = ((hsv[..., 2] > 170) & (hsv[..., 1] < 90)).astype(np.float32)
    dark = ((hsv[..., 2] < 110) & (cv2.blur(cream, (61, 61)) > 0.55)).astype(np.uint8)
    n, _, st, cen = cv2.connectedComponentsWithStats(dark)
    blobs = sorted(((st[i, 4], cen[i][0] + x0, cen[i][1] + y0) for i in range(1, n)), reverse=True)
    # the pin = the blob nearest the guessed centre (any size); the hour marks = the big blobs
    pin = min((b for b in blobs if b[0] > 80), key=lambda b: math.hypot(b[1] - cx, b[2] - cy))
    marks = [b for b in blobs if b[0] > blobs[0][0] * 0.3 and b is not pin]
    px, py = pin[1], pin[2]
    rows, rhs, used, found = [], [], set(), {}
    for _, mx, my in marks:
        ang = math.degrees(math.atan2(mx - px, -(my - py))) % 360          # clockwise from up
        k = round(ang / 30) % 12
        if k in used:
            continue
        used.add(k)
        found[k] = (mx, my)
        s, c = math.sin(math.radians(k * 30)), math.cos(math.radians(k * 30))
        rows.append([s, c, 1]); rhs.append([mx, my])                      # m = s*e + c*n + centre   (n points to 12)
    sol, *_ = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)
    (ex, ey), (nx, ny), (ox, oy) = sol
    mk = lambda k: found.get(k) or (ox + math.sin(math.radians(k * 30)) * ex + math.cos(math.radians(k * 30)) * nx,
                                    oy + math.sin(math.radians(k * 30)) * ey + math.cos(math.radians(k * 30)) * ny)
    # renumber so the mark nearest the stem's direction (seen from the pin) is 12
    sa = math.atan2(stem[0] - px, -(stem[1] - py))
    off = min(range(12), key=lambda k: abs(math.remainder(math.atan2(mk(k)[0] - px, -(mk(k)[1] - py)) - sa, 2 * math.pi)))
    full = [mk((k + off) % 12) for k in range(12)]
    return dict(x=px, y=py, marks=[(float(a), float(b)) for a, b in full], measured=len(found), shift=off)


def point(d, hours, rho):
    """Same maths as Clock.tsx: a periodic Catmull-Rom through the 12 marks, then a fraction rho of the way pin -> mark."""
    m = d["marks"]
    h = hours % 12
    i = int(h)
    t = h - i
    p0, p1, p2, p3 = (m[(i + j) % 12] for j in (-1, 0, 1, 2))
    q = [0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t * t
                + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t ** 3) for a in (0, 1)]
    return d["x"] + rho * (q[0] - d["x"]), d["y"] + rho * (q[1] - d["y"])


if __name__ == "__main__":
    path, cx, cy, R, sx, sy, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
    d = fit(path, cx, cy, R, (sx, sy))
    print(round(d["x"], 1), round(d["y"], 1), "measured", d["measured"], "12 = old mark", d["shift"], [tuple(round(v) for v in m) for m in d["marks"]])
    im = cv2.imread(path)
    for h, col in ((0, (0, 0, 255)), (3, (0, 200, 0)), (6, (255, 0, 0)), (9, (0, 200, 255))):
        p = point(d, h, 1.0)
        cv2.line(im, (round(d["x"]), round(d["y"])), (round(p[0]), round(p[1])), col, 6)
    for k in range(60):
        p = point(d, k / 5, 1.0)
        cv2.circle(im, (round(p[0]), round(p[1])), 5, (255, 0, 255), -1)
    cv2.imwrite(out, cv2.resize(im[cy - R:cy + R, cx - R:cx + R], (800, 800)))
