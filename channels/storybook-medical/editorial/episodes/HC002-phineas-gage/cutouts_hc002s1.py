"""HC002-S1 Gage: the paid sprite / pose sheets (2026-11-18) -> cut-outs with the SAME names and states as the drawn
stand-ins, so the approved keys in edit_hc002s1.py play on the real pieces unchanged. Free, local.
The stand-ins move to review/previz/sprites-free/ (kept for comparison).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/cutouts_hc002s1.py
then look at every assets/images/sprites/<name>/check.png (magenta: holes and halos; onion skin: one outline).
"""
import json

import cv2
import numpy as np
from PIL import Image
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from fx_prep import sheet  # noqa: E402

P = REPO / "projects/hc002-s1/assets/images"
FREE = REPO / "projects/hc002-s1/review/previz/sprites-free"
PAD = 24

# sheet -> (sprite folder, frame names in reading order, align, anchor: "feet" = bottom centre, else (ax, ay))
CUTS = {
    "sprite-iron": ("iron", ["rod-0", "turn-0"], "center", (0.5, 0.5)),
    "sprite-hat": ("hat", ["side-0", "tumble-0"], "center", (0.5, 0.5), "rembg"),   # teal underside ~ key green
    "pose-gage-s1": ("gage-s1", ["stand-0", "thrown-0"], "bottom", "feet"),
    "pose-gage-s4": ("gage-s4", ["down-0", "turn-0"], "bottom", "feet"),
    "pose-gage-s8": ("gage-s8", ["lie-0", "fingers-0", "prop-0"], "bottom", "feet", "rembg"),  # teal shirt shadows ~ key green   # v4 (close, ground level); prop mirrored below
}



def solidify(png: Path):
    """Keep the largest piece (a drill hole drawn at a foot is not him) and make its inside fully opaque: a colour
    close to the key (the hat's teal underside) is otherwise half-keyed and shows the plate through."""
    a = np.array(Image.open(png).convert("RGBA"))
    m = (a[..., 3] > 60).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 2:
        big = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        a[..., 3] = np.where(cv2.dilate((lab == big).astype(np.uint8), np.ones((5, 5), np.uint8)) > 0, a[..., 3], 0)
        m = (lab == big).astype(np.uint8)
    # NOT hole-filled: the gaps between an arm and the body, or the iron and a leg, are real background
    inside = cv2.erode(m, np.ones((5, 5), np.uint8)) > 0
    a[..., 3] = np.where(inside, 255, a[..., 3])
    Image.fromarray(a, "RGBA").save(png)


for src, (name, frames, align, anchor, *how) in CUTS.items():
    img = P / "refs" / f"{src}.png"
    if not img.exists():
        print(f"{src}: not generated yet, skipped")
        continue
    out = P / "sprites" / name
    meta = json.load(open(out / "sprites.json")) if (out / "sprites.json").exists() else {}
    if str(meta.get("source", "")).startswith("STAND-IN"):
        FREE.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(FREE / name, ignore_errors=True)
        shutil.move(str(out), str(FREE / name))
    try:
        sj = sheet(str(img), frames, str(out), (how or ["key"])[0], align, pad=PAD,
                   anchor=(0.5, 0.5) if anchor == "feet" else anchor)
    except SystemExit as e:   # a figure count mismatch: the background model instead of the colour key
        print(e, "-> retry with rembg")
        sj = sheet(str(img), frames, str(out), "rembg", align, pad=PAD, anchor=(0.5, 0.5) if anchor == "feet" else anchor)
    if anchor == "feet":      # the feet sit PAD px above the canvas bottom (align="bottom")
        m = json.load(open(sj))
        m["anchor"] = [0.5, round((m["canvas"][1] - PAD) / m["canvas"][1], 4)]
        json.dump(m, open(sj, "w"), indent=1)
    for f in frames:
        solidify(out / f"{f}.png")

# v4 shot 8: the "prop" drawing came back facing the other way (waist on the right). Mirror it and line it up with "lie"
# at the waist (the straight cut, left edge of the body) and the floor line (bottom), so the swap never flips him.
s8 = P / "sprites/gage-s8"
if (s8 / "prop-0.png").exists() and json.load(open(s8 / "sprites.json"))["source"].startswith("pose-gage-s8"):
    def box(im):
        a = np.array(im)[..., 3] > 60
        ys, xs = np.nonzero(a)
        return xs.min(), ys.max()
    lie = Image.open(s8 / "lie-0.png")
    prop = Image.open(s8 / "prop-0.png").transpose(Image.FLIP_LEFT_RIGHT)
    (lx, lb), (px, pb) = box(lie), box(prop)
    canvas = Image.new("RGBA", prop.size, (0, 0, 0, 0))
    canvas.alpha_composite(prop, (int(lx - px), int(lb - pb)))
    canvas.save(s8 / "prop-0.png")
    print("gage-s8: prop mirrored and aligned to lie at the waist and the floor")


def despeckle_hair(png: Path):
    """Care (no wound): the "dust" on his head came back as dark brown flecks that read like wounds near the crown.
    Small compact dark blobs inside the grey hair are repainted from their surroundings (cv2 inpaint); long ink lines
    and hair strands (elongated) are kept."""
    im = np.array(Image.open(png).convert("RGBA"))
    rgb, a = im[..., :3].copy(), im[..., 3]
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    med = cv2.medianBlur(rgb, 21)
    mhsv = cv2.cvtColor(med, cv2.COLOR_RGB2HSV)
    hair = (mhsv[..., 1] < 70) & (mhsv[..., 2] > 70) & (mhsv[..., 2] < 190) & (a > 200)     # grey, mid-tone = dusty hair
    darker = (med.astype(int).sum(2) - rgb.astype(int).sum(2)) > 75
    warm = (hsv[..., 0] < 25) & (hsv[..., 1] > 60)                                            # brown / reddish
    cand = (hair & darker & ((hsv[..., 2] < 95) | warm)).astype(np.uint8)          # dark grey-black or brown flecks
    n, lab, st, _ = cv2.connectedComponentsWithStats(cand)
    mask = np.zeros_like(cand)
    for i in range(1, n):
        w, h, area = st[i, 2], st[i, 3], st[i, 4]
        if 4 <= area <= 900 and max(w, h) <= 3.5 * max(1, min(w, h)):
            mask[lab == i] = 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    rgb = cv2.inpaint(rgb, mask, 6, cv2.INPAINT_TELEA)
    # green spill from the key on the hair edges: green never rises above red and blue in this figure
    r_, g_, b_ = (rgb[..., i].astype(int) for i in range(3))
    rgb[..., 1] = np.minimum(g_, np.maximum(r_, b_) + 6).astype(np.uint8)
    Image.fromarray(np.dstack([rgb, a]), "RGBA").save(png)
    return int((mask > 0).sum())


for f in ("lie-0", "fingers-0", "prop-0"):
    if (s8 / f"{f}.png").exists():
        print(f, "despeckled px:", despeckle_hair(s8 / f"{f}.png"))
