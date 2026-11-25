"""Separate checks (Mahdi 2026-11-25) of screen_shake, rgb_split and the mono palette, plus the retuned cyan_magenta and the overscanned whip_pan.
    python channels/storybook-medical/scripts/fx_check.py   -> projects/fx-demo/renders/fx-check.mp4 (9 s)"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fx_demo as d  # noqa: E402

S1, L = d.S1, d.L
SH = [("c1", 0.0, 2.0, S1 / "s5.png", {"type": "static"}),                   # screen_shake alone
      ("c2", 2.0, 4.0, S1 / "s2b.png", {"type": "static"}),                  # rgb_split alone
      ("c3", 4.0, 6.0, S1 / "s2b.png", {"type": "static"}),                  # mono
      ("c4", 6.0, 8.0, S1 / "s5.png", {"type": "static"}),                   # cyan_magenta
      ("c5", 8.0, 10.0, L / "assets/images/refs/plate-r4.png", {"type": "static"})]  # whip pan lands here
FX = [{"preset": "screen_shake", "at": 0.5, "dur": 0.8, "strength": 22},
      {"preset": "rgb_split", "at": 2.4, "dur": 0.9, "px": 18},
      {"preset": "halftone_flashback", "at": 4.0, "dur": 2.0, "palette": "mono", "dot": 9},
      {"preset": "halftone_flashback", "at": 6.0, "dur": 2.0, "palette": "cyan_magenta", "dot": 9},
      {"preset": "whip_pan", "at": 7.7, "dur": 0.6, "dir": 1}]
if __name__ == "__main__":
    d.main("fx-check", SH, FX, 10.0, [])
