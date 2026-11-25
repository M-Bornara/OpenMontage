"""Timeline-wide background similarity check (review 2026-11-25, HC002-L rows 10 -> 11).

cut_check.py (L52) only looks at CONSECUTIVE shots and only at cameras that match as the same photograph. Rows 10 and 11 were two
different stills of the same set (same cliff, same kegs, same planks) and read as a jump cut, and nothing else compared shots that
are a few seconds apart. This check compares EVERY pair of shots whose visible moments are within 6 s of each other:

  1. Each shot is the picture the viewer sees at the moment nearest the other one: the shot's source (a still, or a clip's first /
     last frame), cut to the camera window (zoom and centre from the motion) at the shot's start or end, downscaled to 320 x 180
     and turned to grey.
  2. SAME STILL: both shots use one file. They only differ by their camera, so it is geometry: the windows overlap (IoU > 0.3)
     and their zoom is within x1.5 of each other = the same crop used twice = FAIL. A different crop (x1.5 or more, or little overlap) passes.
  3. DIFFERENT STILLS: (a) ORB features + RANSAC similarity (as cut_check) = same camera on the same set, FAIL when the on-screen
     size is within x1.5 and the windows overlap; (b) edge structure on a grid of tiles (Sobel on the blurred frames, a zero-mean
     correlation per tile): the share of tiles with edges in BOTH frames that correlate above TILE_CORR. People occupy a minority of
     the tiles, so a redrawn set with new people still scores high = FAIL at TILE_SHARE or more.
Opt-out: the later shot says "same-camera cut intended" in its "cut" field (as L52).

    python channels/storybook-medical/scripts/bg_similarity.py <project-id> [...]     # exit 1 on any pair
`episode.py build` runs it after cut_check; the regression test is test_bg_similarity.py (rows 10 and 11 must fail).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cut_check  # noqa: E402

REPO = cut_check.REPO
WITHIN = 6.0                     # seconds between the end of the earlier shot and the start of the later one
W, H = 320, 180
TILES = (8, 4)                   # columns, rows
TILE_CORR, TILE_SHARE, MIN_EDGE = 0.55, 0.42, 6.0
SIZE_JUMP, IOU_JUMP = 1.5, 0.3
SKIP = ("brand:",)


def source(pid: str, shot: dict) -> Path | None:
    ref = (shot.get("layers") or {}).get("bg") or shot.get("source", "")
    if not ref or ref.startswith(SKIP):
        return None
    p = cut_check.resolve(pid, ref)
    return p if p.exists() else None


def full_frame(path: Path, at_end: bool) -> np.ndarray | None:
    if path.suffix.lower() in (".mp4", ".mov", ".webm"):
        cap = cv2.VideoCapture(str(path))
        n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, n - 2) if at_end else 0)
        ok, im = cap.read()
        cap.release()
        return im if ok else None
    return cv2.imread(str(path))


def view(im: np.ndarray, s: float, cx: float, cy: float) -> np.ndarray:
    """The camera window (zoom s, centre cx cy in frame fractions) of a 16:9 picture, 320 x 180 grey."""
    h, w = im.shape[:2]
    fh = min(h, round(w * 9 / 16))
    fw = min(w, round(fh * 16 / 9))
    im = im[(h - fh) // 2:(h - fh) // 2 + fh, (w - fw) // 2:(w - fw) // 2 + fw]
    im = cv2.resize(im, (W * 3, H * 3), interpolation=cv2.INTER_AREA)
    x0, y0 = int(round((cx - 0.5 / s) * W * 3)), int(round((cy - 0.5 / s) * H * 3))
    ww, hh = int(round(W * 3 / s)), int(round(H * 3 / s))
    x0, y0 = max(0, min(W * 3 - ww, x0)), max(0, min(H * 3 - hh, y0))
    return cv2.cvtColor(cv2.resize(im[y0:y0 + hh, x0:x0 + ww], (W, H), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)


def edges(g: np.ndarray) -> np.ndarray:
    g = cv2.GaussianBlur(g, (0, 0), 1.6).astype(np.float32)
    return cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))


def tile_share(a: np.ndarray, b: np.ndarray) -> float:
    """Share of the tiles with edges in both frames whose edge structure correlates above TILE_CORR."""
    ea, eb = edges(a), edges(b)
    tw, th = W // TILES[0], H // TILES[1]
    valid = hit = 0
    for j in range(TILES[1]):
        for i in range(TILES[0]):
            ta, tb = ea[j * th:(j + 1) * th, i * tw:(i + 1) * tw], eb[j * th:(j + 1) * th, i * tw:(i + 1) * tw]
            if ta.mean() < MIN_EDGE or tb.mean() < MIN_EDGE:
                continue
            valid += 1
            za, zb = ta - ta.mean(), tb - tb.mean()
            d = float(np.sqrt((za * za).sum() * (zb * zb).sum()))
            if d > 1e-6 and float((za * zb).sum()) / d > TILE_CORR:
                hit += 1
    return hit / valid if valid else 0.0


def window(s: float, cx: float, cy: float) -> np.ndarray:
    return cut_check.window(s, cx, cy, W, H)


def compare(pid: str, A: dict, B: dict) -> tuple[bool, str] | None:
    """(is a match, what) for the earlier shot A and the later shot B, or None when a picture is missing."""
    pa, pb = source(pid, A), source(pid, B)
    if pa is None or pb is None:
        return None
    sA, ax, ay = cut_check.camera(A, A["end"] - A["start"])
    sB, bx, by = cut_check.camera(B, 0.0)
    if pa == pb and pa.suffix.lower() not in (".mp4", ".mov", ".webm"):
        r = sB / sA
        ov = cut_check.iou(np.float32(window(sA, ax, ay)), np.float32(window(sB, bx, by)))
        return (1 / SIZE_JUMP < r < SIZE_JUMP and ov > IOU_JUMP,
                f"the same still, zoom x{sA:.2f} -> x{sB:.2f} (x{r:.2f}), windows overlap {ov:.2f}")
    fa, fb = full_frame(pa, True), full_frame(pb, False)
    if fa is None or fb is None:
        return None
    ga, gb = view(fa, sA, ax, ay), view(fb, sB, bx, by)
    m = cut_check.match(cv2.resize(ga, (W * 2, H * 2)), cv2.resize(gb, (W * 2, H * 2)))
    if m and m[0] >= cut_check.MIN_INLIERS and m[1] >= cut_check.MIN_FRAC:
        # the views are already cut to each shot's camera, so the fitted scale IS the on-screen size ratio and the mapped frame is the overlap
        k = float(np.hypot(m[2][0, 0], m[2][1, 0]))
        full = np.float32([[0, 0], [W * 2, 0], [W * 2, H * 2], [0, H * 2]])
        ov = cut_check.iou(np.float32(cv2.transform(full[None], m[2])[0]), full)
        what = f"same camera on the same set ({m[0]} feature inliers, {m[1]:.0%}), on-screen size x{k:.2f}, overlap {ov:.2f}"
        return (1 / SIZE_JUMP < k < SIZE_JUMP and ov > IOU_JUMP), what
    share = tile_share(ga, gb)
    return share >= TILE_SHARE, f"edge structure matches in {share:.0%} of the tiles"


def check(pid: str, ep: dict | None = None, verbose: bool = False) -> list[str]:
    ep = ep or json.load(open(REPO / "projects" / pid / "episode.json", encoding="utf-8"))
    shots = [s for s in ep["shots"] if source(pid, s) is not None]
    out = []
    for i, A in enumerate(shots):
        for B in shots[i + 1:]:
            if B["start"] - A["end"] > WITHIN:
                break
            res = compare(pid, A, B)
            if res is None:
                continue
            bad, what = res
            tag = f"{A['id']} ({A['start']:.1f}-{A['end']:.1f} s) / {B['id']} ({B['start']:.1f}-{B['end']:.1f} s)"
            if verbose:
                print(f"  {'MATCH' if bad else 'ok   '} {tag}: {what}")
            if bad and cut_check.INTENDED not in str(B.get("cut", "")).lower():
                out.append(f"BG: {tag}: {what}. The same background within {WITHIN:.0f} s reads as a jump cut: reframe one "
                           f"(x1.5 or more), pick a different still, or write '{cut_check.INTENDED}' in the shot's cut field")
    return out


if __name__ == "__main__":
    bad = []
    for pid in [a for a in sys.argv[1:] if not a.startswith("-")]:
        found = check(pid, verbose="-v" in sys.argv)
        print(f"{pid}: {len(found)} similar pair(s)")
        for f in found:
            print("  " + f)
        bad += found
    sys.exit(1 if bad else 0)
