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
    "pose-gage-s8": ("gage-s8", ["lie-0", "fingers-0", "spare-0", "prop-0"], "bottom", "feet"),   # v3 came back 2x2; spare unused
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
