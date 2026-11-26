"""HC002-L Gage long: row 49 (the six-horse coach, the long's own HERO) on REAL art (user 2026-11-22: "cast + HERO pieces
first, show me, then the rest"). Free: no paid call. The three cold-open HERO rows (2, 4, 5) reuse S1's approved keys
and sprites on the new 16:9 plates; they are re-timed in the long's edit and shown there.

The compositor is HC003-S1's (hero_real_hc003s1: plate + keyed actors + camera keys) switched to a 16:9 frame, plus a
looping state (the horses' 3-frame trot) and turning wheels. Positions measured on plate-r49 (the road at ~0.62).
Out: projects/hc002-l/review/hero/49-real.mp4 + 49-real-sheet.jpg (start / "six horses" / end), pieces.jpg

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/hero_real_hc002l.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/editorial/episodes/HC003-dancing-plague"))
import hero_real_hc003s1 as hr  # noqa: E402

P = REPO / "projects/hc002-l"
hr.P, hr.OUT = P, P / "review/hero"
hr.W, hr.H, hr.OW, hr.OH = 3840, 2160, 960, 540
hr.WORDS = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
hr.NARR = P / "assets/audio/narration.wav"
W, H = hr.W, hr.H


def despill(im: Image.Image) -> Image.Image:
    """The keyed trot dust came back green-tinted (half-transparent green between the legs): pixels where green clearly
    beats red and blue are dropped, and the remaining green spill is pulled down to the red/blue mean."""
    a = np.array(im).astype(np.int16)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    spill = g > np.maximum(r, b) + 18
    a[spill, 3] = 0
    g2 = np.minimum(g, (r + b) // 2 + 10)
    a[..., 1] = np.where(a[..., 3] > 0, g2, g)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), "RGBA")


def frames_of(name: str, height: float, anchor: str = "bottom", every: bool = False, mirror: bool = False):
    """Like hr.load_piece; `every` keeps EVERY frame of every state as its own state ("trot0", "trot1", ...)."""
    d = P / "assets/images/sprites" / name
    meta = json.load(open(d / "sprites.json", encoding="utf-8"))
    frames = {}
    for s, fs in meta["frames"].items():
        for i, f in enumerate(fs if every else fs[:1]):
            frames[f"{s}{i}" if every else s] = Image.open(d / f).convert("RGBA")
    frames = {s: despill(im) for s, im in frames.items()}
    first = next(iter(frames))
    bb = frames[first].getbbox()
    k = height * H / (bb[3] - bb[1])
    frames = {s: im.convert("RGBa").resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS).convert("RGBA")
              for s, im in frames.items()}
    a = np.array(frames[first].getchannel("A")) > 128
    ys, xs = np.nonzero(a)
    anc = {"bottom": ((xs.min() + xs.max()) / 2, ys.max()), "center": ((xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2)}[anchor]
    return frames, (anc[0] / frames[first].width, anc[1] / frames[first].height), {}


def row49():
    t0 = hr.word_t("for", 237.0)                      # "For about seven years, he drove a coach…"
    six, sant = hr.word_t("six", t0), hr.word_t("santiago", t0)
    win = (t0 - 0.05, hr.word_t("six", sant) - 0.05)  # to the cut before row 50 ("Six horses.")
    end, s = win[1] - win[0], sant - win[0]
    road = 0.70                                        # the wheels' contact line on the road (measured on plate-r49)
    team = frames_of("horses-r49", 0.22, "bottom", every=True)
    body = frames_of("coach-r49", 0.33, "bottom")
    body = ({"body": body[0]["body"]}, body[1], {})
    wheel = frames_of("coach-r49", 0.165, "center")
    wheel = ({"wheel": wheel[0]["wheel"]}, wheel[1], {})
    gage = frames_of("gage-r49", 0.23, "bottom")
    bw = body[0]["body"].getbbox()
    bwf = (bw[2] - bw[0]) / W                          # the coach body's width (frame fractions)
    # the whole rig drifts left with the trot, then lets the camera go at "Santiago" (it passes out to the left)
    def x_at(x0):
        return [{"t": 0.0, "x": x0}, {"t": s, "x": x0 - 0.16, "ease": "linear"}, {"t": end, "x": x0 - 0.75, "ease": "in"}]
    cx = 0.80                                          # the coach body's centre at the start
    spin_per_frac = W / (math.pi * 0.165 * H) * 360     # rolling: degrees per frame-width travelled
    def wheel_keys(off):
        ks = x_at(cx + off)
        for k in ks:
            k["y"] = road - 0.083
            k["rot"] = (k["x"] - (cx + off)) * spin_per_frac
        ks[0]["state"] = "wheel"
        return ks
    trot = [{"t": round(i / 10, 2), "state": f"trot{i % 3}"} for i in range(int(end * 10) + 1)]
    team_keys = [dict(k, y=road) for k in x_at(cx - bwf / 2 - 0.15)] + trot
    team_keys.sort(key=lambda k: k["t"])
    gage_keys = [dict(k, y=road - 0.143) for k in x_at(cx - bwf * 0.36)]
    gage_keys[0]["state"] = "steady"
    gage_keys.insert(1, {"t": six - win[0], "state": "urge"})
    bounce = lambda ks: [dict(k, y=road - 0.044) for k in ks]  # noqa: E731
    body_keys = bounce(x_at(cx))
    body_keys[0]["state"] = "body"
    return {"name": "49", "win": win, "plate": P / "assets/images/refs/plate-r49.png", "hero_at": six - win[0],
            "actors": [{"id": "team", "hero": True, "piece": team, "keys": team_keys},
                       {"id": "wheel-back", "piece": wheel, "keys": wheel_keys(+bwf * 0.30)},
                       {"id": "coach", "hero": True, "piece": body, "keys": body_keys},
                       {"id": "wheel-front", "piece": wheel, "keys": wheel_keys(-bwf * 0.28)},
                       {"id": "gage", "piece": gage, "keys": gage_keys, "xfade": 0.12}],
            "cam": [{"t": 0.0, "scale": 1.0, "x": 0, "y": 0}, {"t": end, "scale": 1.04, "x": 2, "y": 0, "ease": "inout"}]}


PIECES = ["sheet-harlow", "sheet-gage-chile", "plate-r2", "plate-r4", "plate-r5", "plate-r49", "sprite-coach-r49",
          "sprite-horses-r49", "pose-gage-r49"]

if __name__ == "__main__":
    print(hr.pieces_sheet(PIECES))
    print(hr.render(row49()))
