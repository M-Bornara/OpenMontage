"""HC002-S1 shot 2a as a tight MCU (user 2026-11-19): s2a and s2b came back with the set plate's camera (same cliff, kegs,
planks), so 2a -> 2b read as a jump cut with the crew popping in. Free fix: 2a becomes a tight MCU on Gage (the camera
keys in edit_hc002s1.py) with the cliff SOFT behind him, so the cut is close -> wide.

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/mcu2a_hc002s1.py [--cut]

Gage (with his bar) is cut with rembg (fx_prep.cut, "gage" box), the plate behind him is inpainted and blurred (a long
lens: sigma 6 px of the 1536 still = ~12 px on screen at the x2.8 zoom), and the sharp Gage is laid back on top:
keyframes/s2a-dof.png. The arm wag is re-cut from that still (alive_hc002s1.py's s2a arm outline), so the patch behind
the moving forearm is soft too.
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import fx_prep  # noqa: E402

KF = REPO / "projects/hc002-s1/assets/images/keyframes"
GAGE_BOX = (0.20, 0.22, 0.66, 0.80)
ARM = ((0.50, 0.28, 0.63, 0.405),
       [(0.525, 0.398), (0.567, 0.398), (0.577, 0.35), (0.612, 0.31), (0.607, 0.284), (0.568, 0.29), (0.552, 0.33),
        (0.523, 0.375)])
SIGMA = 6

if "--cut" in sys.argv or not (KF / "fx/s2a-gage.mask.png").exists():
    fx_prep.cut(str(KF / "s2a.png"), "gage", GAGE_BOX, how="rembg", grow=1, check=True)

im = cv2.imread(str(KF / "s2a.png")).astype(np.float32)
a = np.array(Image.open(KF / "fx/s2a-gage.mask.png").getchannel("A")).astype(np.float32) / 255
hole = cv2.dilate(((a > 0.08) * 255).astype(np.uint8), np.ones((15, 15), np.uint8))
plate = cv2.inpaint(im.astype(np.uint8), hole, 15, cv2.INPAINT_TELEA).astype(np.float32)
soft = cv2.GaussianBlur(plate, (0, 0), SIGMA)
# a choked matte for the sharp layer (no hard keyed edge against the blur)
m = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 1.2)[..., None]
out = soft * (1 - m) + im * m
cv2.imwrite(str(KF / "s2a-dof.png"), np.clip(out, 0, 255).astype(np.uint8))
print("keyframes/s2a-dof.png")
# user 2026-11-19: no arm wave cut out of the still (the cut was not clean; L53). And continuity: in the 2b wide Gage
# raises his RIGHT hand (screen left), so the MCU is mirrored to match (the soft cliff and his clothes read the same).
cv2.imwrite(str(KF / "s2a-dof-mirror.png"), np.clip(out, 0, 255).astype(np.uint8)[:, ::-1])
print("keyframes/s2a-dof-mirror.png")
# user 2026-11-20 (ALIVE v2): Gage is a generated pose-sheet figure; this is his background, the soft cliff with him gone
# (inpainted, then blurred: the blur hides the fill), mirrored like the MCU.
cv2.imwrite(str(KF / "s2a-soft-mirror.png"), np.clip(soft, 0, 255).astype(np.uint8)[:, ::-1])
print("keyframes/s2a-soft-mirror.png")
