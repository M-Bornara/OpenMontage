"""Cold open C1 and C4 as Tier A (Mahdi 2026-11-25): a still + comic-kit effects, NO generation, no spend.
  C1 (3 s)  beat-1 still (the iron tip at the drill hole): slow push, a tiny spark burst + TCK! + RGB split + zoom punch on the strike, metal clank
  C4 (4 s)  beat-5 still (Gage down, two men running): slow push, drifting dust particles, ringing ears + wind + running steps
    python channels/storybook-medical/scripts/fx_tiera.py   -> projects/fx-demo/renders/cold-c1-spark.mp4, cold-c4-aftermath.mp4"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fx_demo as d  # noqa: E402

K = d.L / "assets/images/keyframes"
if __name__ == "__main__":
    d.main("cold-c1-spark", [("c1", 0.0, 3.0, K / "cold-b1-tip-v1.png", {"type": "push", "from": 1.02, "to": 1.16})],
           [{"preset": "zoom_punch", "at": 1.3, "dur": 0.3, "amount": 0.06},
            {"preset": "comic_burst", "at": 1.32, "dur": 0.5, "x": 68, "y": 49, "w": 14, "h": 20, "color": "#FFE066", "rot": -8, "points": 9},
            {"preset": "onomatopoeia", "at": 1.34, "dur": 0.6, "text": "TCK!", "x": 60, "y": 30, "size": 120, "rot": -9, "color": "#FFFFFF"},
            {"preset": "rgb_split", "at": 1.32, "dur": 0.35, "px": 9},
            {"preset": "screen_shake", "at": 1.32, "dur": 0.3, "strength": 6}], 3.0,
           [{"name": "metal-clank", "at": 1.3, "gain_db": -12.0}, {"name": "riser-drone", "at": 0.1, "gain_db": -24.0, "dur": 1.2}], auto_sfx=False)
    d.main("cold-c4-aftermath", [("c4", 0.0, 4.0, K / "cold-b5-dust-v1.png", {"type": "push", "from": 1.02, "to": 1.14, "cx": 0.5, "cy": 0.62})],
           [{"preset": "dust", "at": 0.0, "dur": 4.0, "count": 90, "x": 50, "y": 55, "w": 100, "h": 80, "size": 9, "drift": 55}], 4.0,
           [{"name": "ear-ring", "at": 0.0, "gain_db": -22.0, "dur": 2.5}, {"name": "desert-wind", "at": 0.0, "gain_db": -20.0, "dur": 4.0},
            {"name": "running-footsteps", "at": 0.6, "gain_db": -20.0, "dur": 2.2}])
