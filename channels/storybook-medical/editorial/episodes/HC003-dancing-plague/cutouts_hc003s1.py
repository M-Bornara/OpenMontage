"""HC003-S1: the two cut-outs fx_prep.sheet can't do alone (free, 2026-11-22).

1. pose-s10: drawing 2 (Troffea seated between the two city men) keys as ONE figure (their ground shadows touch). It is
   cut with drawing 1, then split by the empty columns between the bodies (above the feet), into the states
   "seated" (all three), "troffea" (her alone) and "men" (the two men), all on the same canvas, so she can leave on the
   wagon from exactly where she sat while the men stay.
2. sprite-coif-s4 came back with the Troffea sheet printed under it as faint ghosts (L45 again). Only near-opaque,
   far-from-green pixels are kept and, in each coif's box, only the largest piece: the coif, not the ghosts.
    python channels/storybook-medical/editorial/episodes/HC003-dancing-plague/cutouts_hc003s1.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import fx_prep  # noqa: E402

P = REPO / "projects/hc003-s1/assets/images"


def split_seated():
    out = P / "sprites/group-s10"
    tmp = P / "sprites/_tmp-s10"
    fx_prep.sheet(str(P / "refs/pose-s10.png"), ["lifted-0", "seated-0"], str(tmp), align="bottom")
    meta = json.load(open(tmp / "sprites.json", encoding="utf-8"))
    seated = np.array(Image.open(tmp / meta["frames"]["seated"][0]).convert("RGBA"))
    a = seated[..., 3] > 128
    ys, xs = np.nonzero(a)
    y0, y1 = ys.min(), ys.max()
    body = a[y0: y0 + int(0.80 * (y1 - y0))]            # above the feet and their shadows
    cols = body.any(axis=0)
    runs, on, start = [], False, 0
    for x, c in enumerate(cols):
        if c and not on:
            on, start = True, x
        elif not c and on:
            on = False
            runs.append((start, x))
    if on:
        runs.append((start, len(cols)))
    runs = [r for r in runs if r[1] - r[0] > 30]
    if len(runs) == 3:
        mid = runs[1]
        cut = ((runs[0][1] + mid[0]) // 2, (mid[1] + runs[2][0]) // 2)   # split in the middle of each gap
    else:   # 2026-11-22: her hands rest almost against the men's sleeves (no empty column): measured on _grid.jpg
        cut = (385, 782)
    her, men = seated.copy(), seated.copy()
    her[:, :cut[0], 3] = 0
    her[:, cut[1]:, 3] = 0
    men[:, cut[0]:cut[1], 3] = 0
    out.mkdir(parents=True, exist_ok=True)
    Image.open(tmp / meta["frames"]["lifted"][0]).save(out / "lifted-0.png")
    Image.fromarray(seated).save(out / "seated-0.png")
    Image.fromarray(her).save(out / "troffea-0.png")
    Image.fromarray(men).save(out / "men-0.png")
    json.dump({**{k: v for k, v in meta.items() if k != "frames"},
               "frames": {"lifted": ["lifted-0.png"], "seated": ["seated-0.png"], "troffea": ["troffea-0.png"], "men": ["men-0.png"]}},
              open(out / "sprites.json", "w", encoding="utf-8"), indent=1)
    print("group-s10:", runs, "split at", cut)
    solidify_group()
    solidify_wagon()
    warm_interior()
    solid_core_all()


def solidify_group(key=(4, 174, 82), far=75):
    """The chroma key (lo 38 / hi 110 from the green) lets a mid-blue dress through at 70-85 % alpha: Troffea looked half
    visible on the wagon (user 2026-11-22). Any pixel that is not clearly key-green (distance > `far`) and has any alpha
    becomes fully opaque; the soft edge (near-green, anti-aliased) keeps its alpha. Idempotent, free."""
    out = P / "sprites/group-s10"
    for st in ("lifted", "seated", "troffea", "men"):
        f = out / f"{st}-0.png"
        im = np.array(Image.open(f).convert("RGBA"))
        dist = np.sqrt(((im[..., :3].astype(int) - np.array(key)) ** 2).sum(-1))
        a = im[..., 3]
        lift = (a > 5) & (a < 255) & (dist > far)
        im[..., 3] = np.where(lift, 255, a)
        Image.fromarray(im).save(f)
        print("solidify", st, int(lift.sum()), "px lifted to opaque")


def solidify_wagon(key=(4, 174, 82), far=75, shadow_from=0.78):
    """The wagon's dark covered opening (where Troffea sits) came out of the key semi-transparent: the cobbles showed through
    BEHIND her (user 2026-11-22, "invisible areas"). Above `shadow_from` of the sprite's height every non-green pixel
    with alpha becomes opaque; below it is the ground shadow, which must stay soft. Idempotent, free."""
    f = P / "sprites/wagon-s10/body-0.png"
    im = np.array(Image.open(f).convert("RGBA"))
    ys, xs = np.nonzero(im[..., 3] > 5)
    y0, y1 = ys.min(), ys.max()
    dist = np.sqrt(((im[..., :3].astype(int) - np.array(key)) ** 2).sum(-1))
    a = im[..., 3]
    zone = np.zeros(a.shape, bool)
    zone[: y0 + int(shadow_from * (y1 - y0))] = True
    lift = zone & (a > 5) & (a < 255) & (dist > far)
    im[..., 3] = np.where(lift, 255, a)
    Image.fromarray(im).save(f)
    print("solidify wagon body", int(lift.sum()), "px lifted to opaque")


def warm_interior(tint=(214, 170, 120), keep_ink=30):
    """Contrast, not alpha (user 2026-11-23, "the woman is still invisible"): Troffea's dark blue dress sat in front of the
    wagon's dark teal covered opening, so she read as part of the shadow. The opening's dark pixels become warm lit canvas
    (the sun comes through the cover): the original texture's brightness is kept, the ink line stays. Derived from
    body-0.orig.png (the keyed, solidified sprite), so it can be run again."""
    import shutil
    f = P / "sprites/wagon-s10/body-0.png"
    orig = f.with_name("body-0.orig.png")
    if not orig.exists():
        shutil.copy(f, orig)
    im = np.array(Image.open(orig).convert("RGBA")).astype(np.float32)
    a = im[..., 3]
    ys, xs = np.nonzero(a > 5)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    zone = np.zeros(a.shape, bool)
    zone[y0 + int(0.08 * (y1 - y0)): y0 + int(0.62 * (y1 - y0)), x0 + int(0.70 * (x1 - x0)): x1 + 1] = True   # the opening
    lum = im[..., :3].mean(axis=2)
    r, g, bl = im[..., 0], im[..., 1], im[..., 2]
    cool = (bl > r + 6) | (g > r + 10)                    # the pale teal patch left in the opening is cool, canvas is warm
    m = zone & (a > 200) & (lum > keep_ink) & ((lum < 105) | cool)
    k = (0.55 + 0.6 * lum / 255.0)[..., None]
    new = np.clip(np.array(tint, np.float32)[None, None, :] * k, 0, 255)
    w = np.where(cool, 1.0, np.clip((105 - lum) / 40.0, 0, 1))[..., None] * m[..., None]
    im[..., :3] = im[..., :3] * (1 - w) + new * w
    Image.fromarray(im.round().astype(np.uint8)).save(f)
    print("warm interior", int(m.sum()), "px")


def solid_core_all(depth=7):
    """Troffea's two dancer sprites (shot 1, shot 4) keyed with see-through blue dress / skirt (green key vs blue-teal).
    Everything more than `depth` px inside the outline that has any alpha becomes opaque; the soft edge keeps its alpha;
    real gaps (alpha ~ 0) stay open. Idempotent, free (user 2026-11-22: shot 1 'a bit invisible')."""
    import cv2
    for d in ("troffea-s1", "troffea-s4"):
        meta = json.load(open(P / "sprites" / d / "sprites.json", encoding="utf-8"))
        for st, fs in meta["frames"].items():
            f = P / "sprites" / d / fs[0]
            im = np.array(Image.open(f).convert("RGBA"))
            a = im[..., 3]
            dist = cv2.distanceTransform((a > 5).astype(np.uint8), cv2.DIST_L2, 5)
            lift = (a > 5) & (a < 255) & (dist > depth)
            im[..., 3] = np.where(lift, 255, a)
            Image.fromarray(im).save(f)
            print("solid core", d, st, int(lift.sum()), "px")


def clean_coif():
    import cv2
    im = np.array(Image.open(P / "refs/sprite-coif-s4.png").convert("RGB")).astype(np.int32)
    H, W = im.shape[:2]
    key = np.median(np.concatenate([im[:8].reshape(-1, 3), im[:, :8].reshape(-1, 3)]), axis=0)
    dist = np.sqrt(((im - key) ** 2).sum(-1))
    solid = (dist > 150).astype(np.uint8)                # the coif (white / lavender) is far from green; ghosts are not
    solid = cv2.morphologyEx(solid, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(solid)
    out = P / "sprites/coif-s4"
    out.mkdir(parents=True, exist_ok=True)
    frames = {}
    for state, (x0, x1) in (("falling", (0.0, 0.5)), ("rest", (0.5, 1.0))):
        best = max((i for i in range(1, n) if x0 * W <= stats[i, 0] + stats[i, 2] / 2 < x1 * W), key=lambda i: stats[i, 4])
        m = (lab == best).astype(np.uint8)
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
        alpha = cv2.GaussianBlur(m * 255, (3, 3), 0)
        x, y, w, h = cv2.boundingRect(m)
        rgba = np.dstack([im.astype(np.uint8), alpha])[y:y + h, x:x + w]
        canvas = np.zeros((max(h, 1) + 48, max(w, 1) + 48, 4), np.uint8)
        canvas[24:24 + h, 24:24 + w] = rgba
        Image.fromarray(canvas).save(out / f"{state}-0.png")
        frames[state] = [f"{state}-0.png"]
        print("coif", state, (x, y, w, h))
    json.dump({"frames": frames}, open(out / "sprites.json", "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    split_seated()
    clean_coif()
