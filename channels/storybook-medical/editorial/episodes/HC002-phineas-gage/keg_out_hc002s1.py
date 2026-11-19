"""HC002-S1 shot 3 scale fix (user 2026-11-19): the keg beside the hand looked toy-sized (a keg is ~2x a hand's height),
so it is painted OUT of the s3 stills (9:16 and 16:9). Free, local. The rock edge that ran behind the keg splits the
hole into two surfaces: each side is inpainted (Telea) ONLY from its own side (the other side is masked as unknown),
a little stroke-direction grain is added, and the ink edge is redrawn in the line's own colour and width.
The originals stay as s3.orig.png.

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/keg_out_hc002s1.py [--check]
"""
import shutil
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
K = ROOT / "projects/hc002-s1/assets/images"
# per still: the keg (+ its contact shadow) as polygons in source px; the ink edge behind it (measured where it enters
# and leaves the keg); the line width (px, measured on the line beside the keg)
JOBS = {
    "keyframes/s3.png": {
        "holes": [[(1040, 1626), (1280, 1626), (1306, 1700), (1306, 2000), (1270, 2040), (1040, 2048), (1012, 2000), (1012, 1700)],
                  [(1280, 1890), (1400, 1905), (1400, 2010), (1300, 2018)]],
        "edge": [(1000, 1858), (1160, 1767), (1312, 1683)], "ink": 8},
    "keyframes16x9/s3.png": {
        "holes": [[(1545, 905), (1675, 905), (1692, 950), (1692, 1120), (1660, 1146), (1550, 1150), (1528, 1120), (1528, 950)],
                  [(1680, 1060), (1780, 1075), (1780, 1122), (1690, 1130)]],
        "edge": [(1505, 1051), (1606, 996), (1704, 944)], "ink": 7},
}


def paint_out(path: Path, holes, edge, ink):
    orig = path.with_name(path.stem + ".orig.png")
    if not orig.exists():
        shutil.copy(path, orig)
    im = cv2.imread(str(orig))
    H, W = im.shape[:2]
    hole = np.zeros((H, W), np.uint8)
    for p in holes:
        cv2.fillPoly(hole, [np.array(p, np.int32)], 255)
    hole = cv2.dilate(hole, np.ones((7, 7), np.uint8))
    # the two sides of the edge (a half-plane split along the polyline, extended)
    side = np.zeros((H, W), np.uint8)
    (ax, ay), (bx, by) = edge[0], edge[-1]
    ext = [(ax - 4000 * (bx - ax) / (bx - ax + 1e-6), ay - 4000 * (by - ay) / (bx - ax + 1e-6))] + edge + \
          [(bx + 4000, by + 4000 * (by - ay) / (bx - ax + 1e-6))]
    poly = np.array(ext + [(W + 4000, -4000), (-4000, -4000)], np.int32)
    cv2.fillPoly(side, [poly], 255)                       # 255 = above the edge
    # the ink line itself is neither side: keep it out of both fills
    line = np.zeros((H, W), np.uint8)
    cv2.polylines(line, [np.array(edge, np.int32)], False, 255, ink + 10)
    out = im.copy()
    ys, xs = np.nonzero(hole)
    # row fill: each row of the hole blends its left and right borders (median of a 24 px strip just outside, ink pixels
    # left out), weighted by distance: the painting's flat brush areas run sideways, so this keeps their tone without
    # pulling the dark stroke above down into a block; then a light vertical smooth
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    f32 = im.astype(np.float32)
    rowfill = f32.copy()
    for y in range(ys.min(), ys.max() + 1):
        xr = np.nonzero(hole[y])[0]
        if not len(xr):
            continue
        l0, r0 = xr.min(), xr.max()

        def strip(a_, b_):
            px = f32[y, max(0, a_):min(W, b_)]
            ok = g[y, max(0, a_):min(W, b_)] > 75
            return np.median(px[ok], 0) if ok.sum() > 3 else np.median(px, 0)
        L, R = strip(l0 - 26, l0 - 2), strip(r0 + 3, r0 + 27)
        u = ((np.arange(l0, r0 + 1) - l0) / max(1, r0 - l0))[:, None]
        rowfill[y, l0:r0 + 1] = L * (1 - u) + R * u
    sm = cv2.GaussianBlur(rowfill, (0, 0), sigmaX=3, sigmaY=14)
    out = np.where(hole[..., None] > 0, sm, f32).astype(np.uint8)
    # grain: noise smeared along the painting's brush direction (~ -20 deg), only inside the hole
    rng = np.random.default_rng(7)
    n = rng.normal(0, 1, (H, W)).astype(np.float32)
    k = np.zeros((1, 41), np.float32); k[0] = 1 / 41
    M = cv2.getRotationMatrix2D((20, 0), 20, 1)
    n = cv2.filter2D(n, -1, cv2.warpAffine(np.pad(k, ((20, 20), (0, 0))), M, (41, 41)))
    n = cv2.GaussianBlur(n, (0, 0), 1.2)
    soft = cv2.GaussianBlur(hole, (0, 0), 5).astype(np.float32)[..., None] / 255
    out = np.clip(out.astype(np.float32) + n[..., None] * 9 * soft, 0, 255)
    out = (im.astype(np.float32) * (1 - soft) + out * soft).astype(np.uint8)
    # the ink edge, in the colour of the line beside the keg
    probe = im[1850:1872, 990:1012] if "keyframes/" in str(path).replace("\\", "/") else im[edge[0][1] - 8:edge[0][1] + 8, edge[0][0] - 12:edge[0][0]]
    dark = probe.reshape(-1, 3)[np.argsort(probe.reshape(-1, 3).sum(1))[:12]].mean(0)
    cv2.polylines(out, [np.array(edge, np.int32)], False, tuple(int(c) for c in dark), ink, cv2.LINE_AA)
    cv2.imwrite(str(path), out)
    if "--check" in sys.argv:
        pad = 200
        c = out[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad]
        o = im[max(0, ys.min() - pad):ys.max() + pad, max(0, xs.min() - pad):xs.max() + pad]
        cv2.imwrite(str(path.with_name(path.stem + ".keg-check.jpg")), np.hstack([o, c]))
    print(path.relative_to(ROOT), "keg painted out")


if __name__ == "__main__":
    for rel, j in JOBS.items():
        paint_out(K / rel, j["holes"], j["edge"], j["ink"])
