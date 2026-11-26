"""HC002-S1 shot 3 (user 2026-11-19): "the pour must end before the bar arrives: slide the hand + flask out to the right as
the bar slides into the hole". Free, local: the hand + flask cut out of the (keg-free) s3 still as a sprite, and a clean
plate without them (and without the painted powder stream hanging in the air under the nozzle).

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/hand_hc002s1.py [--check]

Mask: fx_prep.cut(s3.orig.png, "hand", (0.44, 0.07, 1.0, 0.53), rembg) -> keyframes/fx/s3.orig-hand.mask.png (cut once;
the hand does not touch the keg, so the mask fits s3.png too). Writes sprites/hand3 (stand-0.png + sprites.json, anchor =
the centre) and keyframes/s3-nohand.png, and prints the actor's w / x / y (frame fractions) so the sprite at rest sits
exactly on the painted hand.

The hole behind the arm is big (12 % of the still): cv2 Telea smears it into wedges. Instead: a push-pull fill (the
surrounding colours, smoothly interpolated), the painting's own brush grain (high-pass of the wall left of the hole, the ink
lines left out), and the block cracks that run INTO the hole redrawn as continuations in the ink's colour. The stream is a
row fill (the ledge's brush bands run sideways, as with the keg).
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / "projects/hc002-s1/assets/images"
STILL = P / "keyframes/s3.png"
MASK = P / "keyframes/fx/s3.orig-hand.mask.png"
# the painted grains falling from the nozzle to the rim of the hole (they stay in the air once the flask has gone)
STREAM = [(684, 1395), (745, 1395), (732, 1500), (730, 1560), (718, 1611), (628, 1611), (630, 1540), (652, 1460)]
# cracks / block edges that run into the hole, continued (source px; measured where they enter and leave the arm)
CRACKS = [
    [(955, 528), (1150, 615), (1330, 696)],                    # the lower block's top edge, on toward the right-hand crack
    [(1288, 272), (1420, 298), (1536, 316)],                   # the ledge line above, on under the sleeve
    [(708, 1198), (850, 1252), (1000, 1318)],                  # the back edge of the ledge, under the hand
]
INK_W = 7


def pushpull(img: np.ndarray, known: np.ndarray) -> np.ndarray:
    """Fill the unknown pixels with a smooth interpolation of the known ones (mask-weighted pyramid down, then up)."""
    H, W = known.shape
    if min(H, W) <= 4:
        w = known.sum()
        return np.broadcast_to((img * known[..., None]).sum((0, 1)) / max(w, 1e-6), img.shape).copy()
    h2, w2 = max(1, H // 2), max(1, W // 2)
    num = cv2.resize(img * known[..., None], (w2, h2), interpolation=cv2.INTER_AREA)
    den = cv2.resize(known, (w2, h2), interpolation=cv2.INTER_AREA)
    small = num / np.maximum(den, 1e-6)[..., None]
    filled = pushpull(small, np.clip(den * 4, 0, 1))
    up = cv2.resize(filled, (W, H), interpolation=cv2.INTER_LINEAR)
    return img * known[..., None] + up * (1 - known[..., None])


def row_fill(f32, gray, hole):
    out = f32.copy()
    ys = np.nonzero(hole.any(1))[0]
    W = f32.shape[1]
    for y in ys:
        xr = np.nonzero(hole[y])[0]
        l0, r0 = xr.min(), xr.max()

        def strip(a_, b_):
            px = f32[y, max(0, a_):min(W, b_)]
            ok = gray[y, max(0, a_):min(W, b_)] > 75
            return np.median(px[ok], 0) if ok.sum() > 3 else np.median(px, 0)
        L, R = strip(l0 - 26, l0 - 2), strip(r0 + 3, r0 + 27)
        u = ((np.arange(l0, r0 + 1) - l0) / max(1, r0 - l0))[:, None]
        out[y, l0:r0 + 1] = L * (1 - u) + R * u
    return cv2.GaussianBlur(out, (0, 0), sigmaX=3, sigmaY=10)


def main():
    im = cv2.imread(str(STILL))
    H, W = im.shape[:2]
    f32 = im.astype(np.float32)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    a = np.array(Image.open(MASK).getchannel("A"))

    # ── the sprite: the hand + flask with its soft matte
    ys, xs = np.nonzero(a > 8)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([cv2.cvtColor(im, cv2.COLOR_BGR2RGB)[y0:y1, x0:x1], a[y0:y1, x0:x1]])
    d = P / "sprites/hand3"
    d.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba).save(d / "stand-0.png")
    json.dump({"source": "s3.png + hand_hc002s1.py", "canvas": [int(x1 - x0), int(y1 - y0)], "anchor": [0.5, 0.5],
               "frames": {"stand": ["stand-0.png"]}}, open(d / "sprites.json", "w"), indent=1)
    FH = W * 16 / 9                       # the 9:16 window, cropped from the middle of the 1536 x 2752 still
    top = (H - FH) / 2
    rest = {"w": round((x1 - x0) / W, 4), "x": round((x0 + x1) / 2 / W, 4), "y": round(((y0 + y1) / 2 - top) / FH, 4)}

    # ── the clean plate
    arm = cv2.dilate(((a > 20) * 255).astype(np.uint8), np.ones((11, 11), np.uint8))
    stream = np.zeros((H, W), np.uint8)
    cv2.fillPoly(stream, [np.array(STREAM, np.int32)], 255)
    out = f32.copy()
    # 1. the arm: push-pull from everything round it (the ink lines left out of the known pixels, so they don't bleed in)
    ink = cv2.dilate(((gray < 70) * 255).astype(np.uint8), np.ones((5, 5), np.uint8))
    known = ((arm == 0) & (ink == 0)).astype(np.float32)
    pp = pushpull(f32, known)
    pp = cv2.GaussianBlur(pp, (0, 0), 6)
    out[arm > 0] = pp[arm > 0]
    # 2. the stream: row fill
    rf = row_fill(out, gray, stream > 0)
    out[stream > 0] = rf[stream > 0]
    # 3. paint texture, made (a mirrored tile of the wall's own grain showed as kaleidoscope ghosts): broad vertical
    # strokes (the wall faces are painted in long up-down strokes) + a fine grain along the brush direction
    rng = np.random.default_rng(11)
    broad = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=16, sigmaY=70)
    broad /= broad.std() + 1e-6
    fine = rng.normal(0, 1, (H, W)).astype(np.float32)
    k = np.zeros((41, 41), np.float32); k[20, :] = 1 / 41
    fine = cv2.filter2D(fine, -1, cv2.warpAffine(k, cv2.getRotationMatrix2D((20, 20), 20, 1), (41, 41)))
    fine = cv2.GaussianBlur(fine, (0, 0), 1.0)
    fine /= fine.std() + 1e-6
    tex = (broad * 3.5 + fine * 3)[..., None]
    hole = ((arm > 0) | (stream > 0)).astype(np.uint8) * 255
    soft = cv2.GaussianBlur(hole, (0, 0), 4).astype(np.float32)[..., None] / 255
    out = out + tex * soft
    out = f32 * (1 - soft) + out * soft
    # 4. the cracks, in the ink's own colour (the darkest pixels on the crack beside the arm)
    probe = im[300:420, 920:960].reshape(-1, 3)
    inkc = probe[np.argsort(probe.sum(1))[:20]].mean(0)
    lines = np.zeros((H, W), np.float32)
    rng2 = np.random.default_rng(5)
    for c in CRACKS:                 # a hand-drawn stroke: resampled every ~12 px with a small wobble, tapered at both ends
        pts = []
        for (ax, ay), (bx, by) in zip(c, c[1:]):
            n = max(2, int(np.hypot(bx - ax, by - ay) / 12))
            pts += [(ax + (bx - ax) * i / n, ay + (by - ay) * i / n) for i in range(n)]
        pts.append(c[-1])
        wob = np.cumsum(rng2.normal(0, 0.8, len(pts)))
        wob -= np.linspace(wob[0], wob[-1], len(pts))
        for i in range(len(pts) - 1):
            u = i / (len(pts) - 1)
            wd = max(2, round(INK_W * min(1, 4 * u, 4 * (1 - u)) * rng2.uniform(0.8, 1.05)))
            p0 = (int(pts[i][0]), int(pts[i][1] + wob[i])); p1 = (int(pts[i + 1][0]), int(pts[i + 1][1] + wob[i + 1]))
            seg = np.zeros((H, W), np.uint8)
            cv2.line(seg, p0, p1, 255, wd, cv2.LINE_AA)
            lines = np.maximum(lines, seg.astype(np.float32) * rng2.uniform(0.82, 0.95))
    lines = cv2.GaussianBlur(lines, (0, 0), 0.9)[..., None] / 255
    out = out * (1 - lines) + inkc * lines
    out = np.clip(out, 0, 255).astype(np.uint8)
    cv2.imwrite(str(P / "keyframes/s3-nohand.png"), out)
    print(json.dumps(rest), "-> sprites/hand3, keyframes/s3-nohand.png")
    if "--check" in sys.argv:
        c = np.hstack([im[0:1700, 560:1536], out[0:1700, 560:1536]])
        cv2.imwrite(str(P / "keyframes/s3-nohand.check.jpg"), cv2.resize(c, (c.shape[1] // 2, c.shape[0] // 2)))


if __name__ == "__main__":
    main()
