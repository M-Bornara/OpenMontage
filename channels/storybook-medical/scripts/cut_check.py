"""Cut check L52 (user 2026-11-19, Gage S1 2a -> 2b): two consecutive shots must not share the same camera at the same
size. Both 2a and 2b came back with the set plate's camera (same cliff, kegs, planks), so the cut read as a JUMP CUT with
the crew popping in.

For every cut (shot A -> shot B):
  1. SAME CAMERA? ORB features on the two source stills (the clean plate of a layered shot, the frame either side of the
     cut for a clip; never the rendered frame, whose captions would match themselves), ratio test, then a RANSAC
     similarity fit (scale + rotation + shift). Many inliers = the two pictures are the same view of the same set.
  2. SAME SIZE AND PLACE? The fit maps still A into still B (scale k). With each shot's camera at the cut (A at its end,
     B at its start: zoom s and the window centre), the on-screen size ratio is r = k * sB / sA, and the overlap is the
     IoU of A's window mapped into B with B's window.
  A cut FAILS when the cameras match, 1/1.5 < r < 1.5 and the windows overlap (IoU > 0.3): a jump cut. A same-camera
  cut that changes size a lot (close -> wide, r = 0.37 for Gage 2a -> 2b after the fix) is a real cut and only noted.
  Opt-out: the shot B's storyboard row (or the shot itself, "cut": ...) says "same-camera cut intended".

    python channels/storybook-medical/scripts/cut_check.py <project-id> [...]     # exit 1 on any L52
`episode.py build` runs it after the motion lint (episodes may carry "cut_lint": "warn").
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[3]
EP = REPO / "channels/storybook-medical/editorial/episodes"
MIN_INLIERS, MIN_FRAC = 40, 0.25
SIZE_JUMP, IOU_JUMP = 1.5, 0.3
INTENDED = "same-camera cut intended"


def resolve(pid: str, ref: str) -> Path:
    if ref.startswith("proj:"):
        return REPO / "projects" / pid / ref[5:]
    p = Path(ref)
    return p if p.is_absolute() else REPO / ref


def picture(pid: str, shot: dict, at_end: bool):
    """The shot's source picture (grey, 9:16 middle crop, 640 px tall) and its pixel aspect."""
    src = resolve(pid, (shot.get("layers") or {}).get("bg") or shot.get("source", ""))
    if not src.exists():
        return None
    if src.suffix.lower() in (".mp4", ".mov", ".webm"):
        cap = cv2.VideoCapture(str(src))
        n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, n - 2) if at_end else 0)
        ok, im = cap.read()
        cap.release()
        if not ok:
            return None
    else:
        im = cv2.imread(str(src))
        if im is None:
            return None
    H, W = im.shape[:2]
    fh = min(H, round(W * 16 / 9))
    fw = min(W, round(fh * 9 / 16))
    y0, x0 = (H - fh) // 2, (W - fw) // 2
    im = im[y0:y0 + fh, x0:x0 + fw]
    return cv2.cvtColor(cv2.resize(im, (360 * 2, 640 * 2)), cv2.COLOR_BGR2GRAY)


def camera(shot: dict, t: float) -> tuple[float, float, float]:
    """(zoom, window centre x, y) in frame fractions at t seconds into the shot."""
    m, dur = shot.get("motion") or {}, max(1e-6, shot["end"] - shot["start"])
    u = min(1.0, max(0.0, t / dur))
    typ = m.get("type")
    if typ == "keys" and m.get("keys"):
        ks = m["keys"]
        k = ks[0] if t <= ks[0]["t"] else ks[-1]
        for p, q in zip(ks, ks[1:]):
            if p["t"] <= t <= q["t"]:
                f = (t - p["t"]) / max(1e-6, q["t"] - p["t"])
                k = {c: p.get(c, 0) + (q.get(c, 0) - p.get(c, 0)) * f for c in ("scale", "x", "y")}
                break
        s = k["scale"]
        return s, 0.5 - k.get("x", 0) / 100 / s, 0.5 - k.get("y", 0) / 100 / s
    if typ in ("push", "pull"):
        a = m.get("from", 1.04 if typ == "push" else 1.18)
        b = m.get("to", 1.18 if typ == "push" else 1.04)
        s = a + (b - a) * u
        return s, 0.5 - m.get("x", 0) * u / 100 / s, 0.5 - m.get("y", 0) * u / 100 / s
    if typ == "slide":
        s = m.get("scale", 1.1)
        x = m.get("from", 0) + (m.get("to", 0) - m.get("from", 0)) * u
        return s, 0.5 - x / 100 / s, 0.5
    return m.get("scale", 1.04), 0.5, 0.5


def match(a: np.ndarray, b: np.ndarray):
    """(inliers, fraction, 2x3 similarity A -> B) or None."""
    orb = cv2.ORB_create(3000, scaleFactor=1.2, nlevels=10)
    ka, da = orb.detectAndCompute(a, None)
    kb, db = orb.detectAndCompute(b, None)
    if da is None or db is None or len(ka) < 20 or len(kb) < 20:
        return None
    good = []
    for pair in cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2):
        if len(pair) == 2 and pair[0].distance < 0.75 * pair[1].distance:
            good.append(pair[0])
    if len(good) < 12:
        return None
    pa = np.float32([ka[g.queryIdx].pt for g in good])
    pb = np.float32([kb[g.trainIdx].pt for g in good])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=6.0)
    if M is None:
        return None
    n = int(inl.sum())
    return n, n / len(good), M


def window(s: float, cx: float, cy: float, w: int, h: int) -> np.ndarray:
    hw, hh = 0.5 / s, 0.5 / s
    return np.float32([[(cx - hw) * w, (cy - hh) * h], [(cx + hw) * w, (cy - hh) * h],
                       [(cx + hw) * w, (cy + hh) * h], [(cx - hw) * w, (cy + hh) * h]])


def iou(p: np.ndarray, q: np.ndarray) -> float:
    inter, _ = cv2.intersectConvexConvex(p, q)
    union = cv2.contourArea(p) + cv2.contourArea(q) - inter
    return float(inter / union) if union > 0 else 0.0


def intended(pid: str, ep: dict, shot: dict) -> bool:
    if INTENDED in str(shot.get("cut", "")).lower():
        return True
    sb = ep.get("storyboard")
    if not sb or not resolve(pid, sb).exists():
        return False
    name = str(shot.get("previz") or shot["id"]).lower().lstrip("s0") or "0"
    for line in resolve(pid, sb).read_text(encoding="utf-8").splitlines():
        cells = [c.strip().strip("*").lower() for c in line.strip().strip("|").split("|")]
        if line.lstrip().startswith("|") and cells and cells[0] == name and INTENDED in line.lower():
            return True
    return False


def check(pid: str, ep: dict | None = None, verbose: bool = True) -> list[str]:
    ep = ep or json.load(open(REPO / "projects" / pid / "episode.json", encoding="utf-8"))
    shots, out = ep["shots"], []
    for A, B in zip(shots, shots[1:]):
        a, b = picture(pid, A, True), picture(pid, B, False)
        if a is None or b is None:
            continue
        m = match(a, b)
        tag = f"{pid} {A['id']}->{B['id']} ({A.get('previz', '')}->{B.get('previz', '')}, cut at {B['start']:.2f} s)"
        if not m or m[0] < MIN_INLIERS or m[1] < MIN_FRAC:
            continue
        n, frac, M = m
        k = float(np.hypot(M[0, 0], M[1, 0]))
        sA, ax, ay = camera(A, A["end"] - A["start"])
        sB, bx, by = camera(B, 0.0)
        r = k * sB / sA
        h, w = a.shape
        wa = cv2.transform(window(sA, ax, ay, w, h)[None], M)[0]
        ov = iou(np.float32(wa), window(sB, bx, by, w, h))
        what = f"same camera ({n} inliers, {frac:.0%}), on-screen size x{r:.2f}, overlap {ov:.2f}"
        if 1 / SIZE_JUMP < r < SIZE_JUMP and ov > IOU_JUMP:
            if intended(pid, ep, B):
                verbose and print(f"  ok (intended) {tag}: {what}")
                continue
            out.append(f"L52: {tag}: {what}: a jump cut. Reframe one side (close <-> wide, x1.5+ size change, or a "
                       f"different part of the set), regenerate one still without the set plate as a reference (L47), "
                       f"or write '{INTENDED}' in the storyboard row")
        elif verbose:
            print(f"  note {tag}: {what}: a real size change, not a jump")
    return out


if __name__ == "__main__":
    bad = []
    for pid in sys.argv[1:]:
        found = check(pid)
        print(f"{pid}: {len(found)} L52")
        for f in found:
            print("  " + f)
        bad += found
    sys.exit(1 if bad else 0)
