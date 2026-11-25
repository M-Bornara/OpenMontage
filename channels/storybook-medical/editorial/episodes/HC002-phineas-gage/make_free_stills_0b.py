"""HC002-L 2026-11-25 free steps (no AI spend).

36b = tight crop of 36a's monster drawing.
36c = cruder, higher-contrast ink version of row 7's page (threshold + rough lines + sepia grade).
55  = paint-fix of the shut lid and mouth on row55-portrait-v3 (v3 kept untouched) -> v4-paint.

Run from the repo root:  python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/make_free_stills_0b.py
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter

K = "projects/hc002-l/assets/images/keyframes16x9/"
W, H = 2752, 1536


def make_36b():
    im = Image.open(K + "row36a-oldbook-v1.png").convert("RGB")
    # drawing sits at about x 700-1100, y 320-560 in a 1376-wide preview -> x2 for full res
    cx, cy, w = 1810, 890, 1000
    h = int(w * 9 / 16)
    box = (cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2)
    out = im.crop(box).resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 90, 3))
    out.save(K + "row36b-textbook-v2crop.png")


def make_36c():
    src = cv2.imread(K + "row7-monster-v1.png")
    g = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    g = cv2.GaussianBlur(g, (0, 0), 3)
    # local threshold keeps the ink lines, drops the page colour
    ink = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 14)
    rng = np.random.default_rng(7)
    # rough lines: warp the ink with low-frequency noise, then break edges with grain
    dx = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 14) * 90
    dy = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 14) * 90
    xs, ys = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    ink = cv2.remap(ink, xs + dx, ys + dy, cv2.INTER_LINEAR, borderValue=255)
    grain = cv2.GaussianBlur(rng.standard_normal((H, W)).astype(np.float32), (0, 0), 1.6)
    ink = np.where((ink.astype(np.float32) + grain * 220) > 128, 255, 0).astype(np.uint8)
    ink = cv2.medianBlur(ink, 3)
    # sepia grade: ink = deep brown, page = warm paper with a soft vignette
    paper = np.array([196, 222, 238], np.float32)  # BGR warm cream
    dark = np.array([22, 38, 58], np.float32)  # BGR dark sepia
    t = (ink.astype(np.float32) / 255.0)[..., None]
    out = dark * (1 - t) + paper * t
    vy, vx = np.mgrid[0:H, 0:W]
    vig = 1 - 0.35 * (((vx - W / 2) / (W / 2)) ** 2 + ((vy - H / 2) / (H / 2)) ** 2)
    out = np.clip(out * vig[..., None], 0, 255).astype(np.uint8)
    cv2.imwrite(K + "row36c-paperback-v2ink.png", out)


def make_55():
    im = cv2.imread(K + "row55-portrait-v3.png")
    # eye + cheek bulge (full res box derived from a 4x zoom of x1200-1560, y380-640)
    eye = np.zeros((H, W), np.uint8)
    cv2.ellipse(eye, (1437, 539), (36, 18), 0, 0, 360, 255, -1)
    # mouth ends (the corners curl up) and the line itself
    mouth = np.zeros((H, W), np.uint8)
    cv2.rectangle(mouth, (1332, 614), (1432, 632), 255, -1)
    # keep the eyebrow and nose-side shadow out of the eye mask
    brow = np.zeros((H, W), np.uint8)
    cv2.rectangle(brow, (1380, 470), (1480, 521), 255, -1)
    eye[brow > 0] = 0
    mask = cv2.bitwise_or(eye, mouth)
    sm = cv2.inpaint(im, mask, 3, cv2.INPAINT_TELEA)
    sm = cv2.GaussianBlur(sm, (0, 0), 1.2)
    out = im.copy()
    soft = cv2.GaussianBlur(mask, (0, 0), 3).astype(np.float32)[..., None] / 255.0
    out = (im * (1 - soft) + sm * soft).astype(np.uint8)
    line = (30, 38, 62)  # BGR, matches the outline ink
    # shut lid: flat, slightly sunken at the outer end (no lash curl, no upward flick)
    pts = np.array([[1403, 531], [1423, 531], [1443, 532], [1463, 534]], np.int32)
    cv2.polylines(out, [pts], False, line, 2, cv2.LINE_AA)
    # faint lower edge so the lid reads as a closed, slightly hollow lid
    pts2 = np.array([[1408, 546], [1435, 549], [1462, 549]], np.int32)
    cv2.polylines(out, [pts2], False, (92, 110, 150), 1, cv2.LINE_AA)
    # level mouth, corners neither up nor down
    cv2.polylines(out, [np.array([[1352, 623], [1378, 624], [1406, 624]], np.int32)], False, (52, 66, 118), 2, cv2.LINE_AA)
    out = cv2.addWeighted(out, 0.6, cv2.GaussianBlur(out, (0, 0), 0.8), 0.4, 0)
    cv2.imwrite(K + "row55-portrait-v4paint.png", out)


if __name__ == "__main__":
    make_36b()
    make_36c()
    make_55()
    print("ok")
