"""Regression test for highlight_check.measure on synthetic frames: a full-height marker passes, the OLD half-height strip must FAIL."""
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import highlight_check as h  # noqa: E402


def frame(marker_top, marker_bot):
    im = np.zeros((2160, 3840, 3), np.uint8)
    im[:] = (204, 230, 241)                                                  # paper (BGR)
    cv2.rectangle(im, (1500, marker_top), (1900, marker_bot), (115, 188, 235), -1)   # amber marker (BGR of 235, 188, 115)
    cv2.putText(im, "iron will", (1520, 1085), cv2.FONT_HERSHEY_SIMPLEX, 3.2, (30, 36, 43), 8)   # ink, about 100 px tall
    return im


ok = True
with tempfile.TemporaryDirectory() as d:
    for name, (a, b), want in (("full-height marker (155 px)", (960, 1115), True), ("OLD half-height strip (lower 45 %)", (1049, 1115), False)):
        cv2.imwrite(str(Path(d) / "f.png"), frame(a, b))
        got, msg = h.measure(Path(d) / "f.png", Path(d))
        print(("PASS" if got == want else "FAIL"), name, "->", "passed" if got else "flagged", "|", msg)
        ok &= got == want
sys.exit(0 if ok else 1)
