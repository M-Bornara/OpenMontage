"""HC002-S1 ALIVE v2 (user 2026-11-20, "do the few generate to make it better"; L53: nothing cut out of a still moves).

The moving people of shots 2a, 2b, 10 and 12 are GENERATED pose sheets (build_hc002s1.py pose-*), cut on their green key
(fx_prep.sheet) into sprites/<name>/; the plates are the approved stills without them (plate-s*-empty). This script:
  1. aligns each empty plate to its approved still (ORB + RANSAC similarity), so the camera keys measured on the still
     stay valid even if the plate came back a little shifted or scaled -> keyframes/s<shot>-empty.png
  2. cuts each pose sheet -> sprites/<name>/ (+ check.png)
  3. places the figure exactly where the painted person stood: the sheet's pose that matches the still is matched to
     the still (ORB inside the figure's alpha; the person's rembg outline + bottom-centre as the fallback) and prints the
     actor's w / x / y for edit_hc002s1.py (ALIVE2 below is read by the edit).
Writes keyframes/alive2.json. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/alive2_hc002s1.py [--check]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import fx_prep  # noqa: E402

P = REPO / "projects/hc002-s1/assets/images"
KF, REFS, SPR = P / "keyframes", P / "refs", P / "sprites"

PLATES = {"plate-s2b-empty": "s2b", "plate-s10-empty": "s10", "plate-s12-empty": "s12"}
# sheet -> sprite dir, frame names (reading order), the still it goes into, the frame that matches the still's pose, and
# the person's box on the still (fractions x0, y0, x1, y1) for the match and the fallback
SHEETS = {
    # came back with his LEFT arm up (as in the unmirrored still): flipped, so the reading order is in, out, up
    "pose-gage-s2a": dict(out="gage-s2a", names=["in-0", "out-0", "up-0"], still="s2a-dof-mirror.png", match="up",
                          box=(0.30, 0.28, 0.82, 1.0), flip=True),
    "pose-crew-s2b": dict(out="driller-s2b", names=["raise-0", "strike-0"], still="s2b.png", match=None,
                          box=(0.56, 0.58, 0.82, 0.90)),
    "pose-gage-s10": dict(out="gage-s10", names=["rest-0", "hand-0", "wave-0"], still="s10.png", match="hand",
                          box=(0.42, 0.35, 0.66, 0.60)),
    "pose-friend-s12": dict(out="friend-s12", names=["up-0", "lean-0"], still="s12.png", match="lean",
                            box=(0.32, 0.27, 0.63, 0.99), skip=True),   # v1 (9:16) repainted the scene; user 2026-11-20: no re-roll, 12 stays a held beat
}


def grey(a: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(a, cv2.COLOR_RGB2GRAY)


def similarity(a: np.ndarray, b: np.ndarray, ma=None, mb=None, n=6000):
    """(M 2x3 a->b, inliers) by ORB + ratio test + RANSAC similarity, or (None, 0)."""
    orb = cv2.ORB_create(n, scaleFactor=1.2, nlevels=10)
    ka, da = orb.detectAndCompute(a, ma)
    kb, db = orb.detectAndCompute(b, mb)
    if da is None or db is None:
        return None, 0
    good = [p[0] for p in cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(da, db, k=2)
            if len(p) == 2 and p[0].distance < 0.75 * p[1].distance]
    if len(good) < 12:
        return None, 0
    pa = np.float32([ka[g.queryIdx].pt for g in good])
    pb = np.float32([kb[g.trainIdx].pt for g in good])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=5.0)
    return (M, int(inl.sum())) if M is not None else (None, 0)


def align_plates():
    for ref, shot in PLATES.items():
        src = REFS / f"{ref}.png"
        if not src.exists():
            print(f"  {ref}: not generated yet")
            continue
        still = np.array(Image.open(KF / f"{shot}.png").convert("RGB"))
        plate = np.array(Image.open(src).convert("RGB").resize((still.shape[1], still.shape[0]), Image.LANCZOS))
        M, n = similarity(grey(plate), grey(still))
        k = float(np.hypot(M[0, 0], M[1, 0])) if M is not None else 1.0
        print(f"  {ref} -> {shot}: {n} inliers, scale {k:.3f}, shift {M[0, 2]:.1f},{M[1, 2]:.1f} px" if M is not None
              else f"  {ref}: no match, used as is")
        out = plate if M is None else cv2.warpAffine(plate, M, (still.shape[1], still.shape[0]), flags=cv2.INTER_LANCZOS4,
                                                     borderMode=cv2.BORDER_REPLICATE)
        Image.fromarray(out).save(KF / f"{shot}-empty.png")


def person_box(still: np.ndarray, box) -> tuple[int, int, int, int]:
    """The painted person's bbox in the still (rembg on the box crop, largest component)."""
    from masks import _session
    from rembg import remove
    H, W = still.shape[:2]
    x0, y0, x1, y1 = int(box[0] * W), int(box[1] * H), int(box[2] * W), int(box[3] * H)
    a = np.array(remove(Image.fromarray(still[y0:y1, x0:x1]), session=_session()).getchannel("A")) > 128
    n, lab, st, _ = cv2.connectedComponentsWithStats(a.astype(np.uint8))
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h = st[i, :4]
    return x0 + x, y0 + y, w, h


def place(name: str, spec: dict) -> dict | None:
    sheet = REFS / f"{name}.png"
    if not sheet.exists() or spec.get("skip"):
        print(f"  {name}: not generated yet / skipped")
        return None
    if spec.get("flip"):
        flipped = REFS / f"{name}-flip.png"
        Image.open(sheet).transpose(Image.FLIP_LEFT_RIGHT).save(flipped)
        sheet = flipped
    d = SPR / spec["out"]
    fx_prep.sheet(str(sheet), spec["names"], str(d), align="phase")
    meta = json.load(open(d / "sprites.json"))
    cw, ch = meta["canvas"]
    ax, ay = meta.get("anchor", [0.5, 0.5])
    still = np.array(Image.open(KF / spec["still"]).convert("RGB"))
    H, W = still.shape[:2]
    fh = W * 16 / 9
    oy = (H - fh) / 2                                    # episode.fit_frame crops the still's height to 9:16
    frame = spec["match"] or spec["names"][0].split("-")[0]
    spr = np.array(Image.open(d / f"{frame}-0.png").convert("RGBA"))
    alpha = spr[..., 3]
    rgb = spr[..., :3].copy()
    rgb[alpha < 128] = 0
    bx = spec["box"]
    mb = np.zeros((H, W), np.uint8)
    mb[int(bx[1] * H):int(bx[3] * H), int(bx[0] * W):int(bx[2] * W)] = 255
    M, n = (None, 0)
    if spec["match"]:
        M, n = similarity(grey(rgb), grey(still), (alpha > 128).astype(np.uint8) * 255, mb)
    k = float(np.hypot(M[0, 0], M[1, 0])) if M is not None else 0
    how = f"ORB {n} inliers"
    if M is None or n < 25 or not 0.2 < k < 5:
        # fallback: the person's outline in the still; same height, bottom-centre on bottom-centre
        px, py, pw, ph = person_box(still, bx)
        ys, xs = np.nonzero(alpha > 128)
        sh, sx0, sx1, sy1 = ys.max() - ys.min(), xs.min(), xs.max(), ys.max()
        k = ph / sh
        tx = px + pw / 2 - (sx0 + sx1) / 2 * k
        ty = py + ph - sy1 * k
        M = np.float32([[k, 0, tx], [0, k, ty]])
        how = f"outline fallback (ORB {n})"
    X, Y = M @ np.float32([ax * cw, ay * ch, 1])
    out = {"sprites": f"proj:assets/images/sprites/{spec['out']}/sprites.json", "w": round(cw * k / W, 4),
           "x": round(float(X) / W, 4), "y": round((float(Y) - oy) / fh, 4)}
    print(f"  {name}: {how}, scale {k:.3f} -> w {out['w']}, x {out['x']}, y {out['y']}")
    return out


def check_sheet(res: dict):
    """The matched pose over its plate next to the approved still: the figure must sit where the painted one stood."""
    tiles = []
    for name, spec in SHEETS.items():
        r = res.get(name)
        if not r:
            continue
        shot = spec["still"].split(".")[0].replace("-dof-mirror", "")
        still = Image.open(KF / spec["still"]).convert("RGB")
        plate_p = KF / ("s2a-soft-mirror.png" if shot == "s2a" else f"{shot}-empty.png")
        plate = Image.open(plate_p).convert("RGB").resize(still.size)
        meta = json.load(open(SPR / spec["out"] / "sprites.json"))
        cw, ch = meta["canvas"]
        ax, ay = meta.get("anchor", [0.5, 0.5])
        W, H = still.size
        fh = W * 16 / 9
        oy = (H - fh) / 2
        frame = spec["match"] or spec["names"][0].split("-")[0]
        spr = Image.open(SPR / spec["out"] / f"{frame}-0.png").convert("RGBA")
        w = r["w"] * W
        h = w * ch / cw
        spr = spr.resize((round(w), round(h)), Image.LANCZOS)
        comp = plate.copy()
        comp.paste(spr, (round(r["x"] * W - ax * w), round(r["y"] * fh + oy - ay * h)), spr)
        tiles += [still, comp]
    if not tiles:
        return
    tw = 380
    th = round(tw * tiles[0].height / tiles[0].width)
    sheet = Image.new("RGB", (tw * len(tiles), th), "white")
    for i, t in enumerate(tiles):
        sheet.paste(t.resize((tw, th)), (i * tw, 0))
    out = REPO / "projects/hc002-s1/review/layers/alive2-place.jpg"
    sheet.save(out, quality=86)
    print(out)


if __name__ == "__main__":
    align_plates()
    res = {n: r for n, s in SHEETS.items() if (r := place(n, s))}
    json.dump(res, open(KF / "alive2.json", "w"), indent=1)
    check_sheet(res)
