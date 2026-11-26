"""HCS09 shot 1b as a close-up with the corridor SOFT behind the professor (user 2026-11-20, L52): s1b and s2a share the
corridor's camera, so 1b -> 2a read as a jump cut (the professor vanishes from the same hall). Free fix, as Gage S1 2a:
1b becomes a CU on his face (the push in edit_hcs09.py) and the hall behind him is inpainted + blurred, so the cut reads
close -> wide.

    python channels/storybook-medical/editorial/episodes/HCS09-semmelweis/dof1b_hcs09.py [--cut]

Writes keyframes/s1b-dof.png (the professor sharp, the corridor at sigma 7 px of the 1536-wide still).
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import fx_prep  # noqa: E402

KF = REPO / "projects/hcs09-semmelweis/assets/images/keyframes"
PROF_BOX = (0.18, 0.12, 1.0, 1.0)
SIGMA = 7

if "--cut" in sys.argv or not (KF / "fx/s1b-prof.mask.png").exists():
    fx_prep.cut(str(KF / "s1b.png"), "prof", PROF_BOX, how="rembg", grow=1, check=True)

im = cv2.imread(str(KF / "s1b.png")).astype(np.float32)
a = np.array(Image.open(KF / "fx/s1b-prof.mask.png").getchannel("A")).astype(np.float32) / 255
hole = cv2.dilate(((a > 0.08) * 255).astype(np.uint8), np.ones((15, 15), np.uint8))
plate = cv2.inpaint(im.astype(np.uint8), hole, 15, cv2.INPAINT_TELEA).astype(np.float32)
soft = cv2.GaussianBlur(plate, (0, 0), SIGMA)
m = cv2.GaussianBlur(cv2.erode(a, np.ones((3, 3), np.uint8)), (0, 0), 1.2)[..., None]
out = soft * (1 - m) + im * m
cv2.imwrite(str(KF / "s1b-dof.png"), np.clip(out, 0, 255).astype(np.uint8))
print("keyframes/s1b-dof.png")
