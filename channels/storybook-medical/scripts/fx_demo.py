"""Comic effects prototype (Mahdi 2026-11-25): a 13.6 s cold-open demo from EXISTING stills and the existing row-19 clip only (nothing generated, no spend).
    0.0-3.0   the strike plate (S1 s5): line boil, a small "TCK!" on the spark, a zoom punch before the hit
    3.0-5.6   the empty cut plate (row 4), under: impact frame (3 frames, starburst, halftone, speed lines), screen shake + RGB split,
              a comic burst over the masked area and a hand-lettered BOOM!
    5.3-5.9   panel wipe (the cut is under it at 5.6)
    5.6-8.6   flashback: the crew in the quarry (S1 s2b), amber halftone, line boil
    8.3-8.9   whip pan with motion blur (the cut is at 8.6)
    8.6-13.6  flashback: the ox cart (the row-19 clip at its own speed and length, 5.0 s), cyan-magenta plates off register
Sound hooks (whoosh / impact / bass hit) come from the free channel library through comic_fx.sfx_for.
    python channels/storybook-medical/scripts/fx_demo.py            -> projects/fx-demo/renders/comic-demo.mp4 (1080p)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import comic_fx  # noqa: E402
import episode  # noqa: E402

REPO, KIT = episode.REPO, episode.KIT
P = REPO / "projects/fx-demo"
L = REPO / "projects/hc002-l"
S1 = REPO / "projects/hc002-s1/assets/images/keyframes16x9"
CLIP = L / "assets/video/row19-oxcart-omni-v1-1080p30.mp4"
END = 13.6

SHOTS = [  # id, start, end, source, motion
    ("d1", 0.0, 3.0, S1 / "s5.png", {"type": "push", "from": 1.04, "to": 1.14}),
    ("d2", 3.0, 5.6, L / "assets/images/refs/plate-r4.png", {"type": "pull", "from": 1.16, "to": 1.05}),
    ("d3", 5.6, 8.6, S1 / "s2b.png", {"type": "push", "from": 1.05, "to": 1.15}),
    ("d4", 8.6, END, CLIP, {"type": "static"}),
]
FX = [
    {"preset": "line_boil", "at": 0.0, "dur": 5.6, "fps": 8, "amount": 6},
    {"preset": "onomatopoeia", "at": 2.3, "dur": 0.6, "text": "TCK!", "x": 55, "y": 36, "size": 130, "rot": -10, "color": "#FFFFFF"},
    {"preset": "zoom_punch", "at": 2.8, "dur": 0.3, "amount": 0.08},
    {"preset": "impact_frame", "at": 3.0, "frames": 3, "x": 50, "y": 48},
    {"preset": "comic_burst", "at": 3.1, "dur": 2.2, "x": 50, "y": 50, "w": 46, "h": 62, "color": "#FFC43D", "rot": -6},
    {"preset": "onomatopoeia", "at": 3.1, "dur": 2.2, "text": "BOOM!", "x": 50, "y": 50, "size": 340, "rot": -7, "color": "#E2352B"},
    {"preset": "panel_wipe", "at": 5.3, "dur": 0.6, "dir": "diag"},
    {"preset": "halftone_flashback", "at": 5.6, "dur": 3.0, "palette": "amber", "dot": 9},
    {"preset": "line_boil", "at": 5.6, "dur": 8.0, "fps": 6, "amount": 5},
    {"preset": "whip_pan", "at": 8.3, "dur": 0.6, "dir": 1},
    {"preset": "halftone_flashback", "at": 8.6, "dur": 5.0, "palette": "cyan_magenta", "dot": 9},
]


def main(name: str = "comic-demo", shots_in=None, fx_in=None, end_in=None, extra_cues=None) -> Path:
    shots_in = shots_in or SHOTS; fx = fx_in or FX; end = end_in or END
    rem = P / "remotion"
    if rem.exists():
        shutil.rmtree(rem)
    shutil.copytree(KIT / "remotion", rem)
    (rem / "public/img").mkdir(parents=True, exist_ok=True)
    (rem / "public/vid").mkdir(parents=True, exist_ok=True)
    shots = []
    for sid, a, b, src, motion in shots_in:
        if src.suffix == ".mp4":
            shutil.copy(src, rem / f"public/vid/{sid}.mp4")
            kind, rel = "video", f"vid/{sid}.mp4"
        else:
            episode.fit_frame(src, rem / f"public/img/{sid}.jpg", (3840, 2160))
            kind, rel = "image", f"img/{sid}.jpg"
        shots.append({"id": sid, "src": rel, "kind": kind, "start": a, "end": b, "inPoint": 0, "motion": motion, "transitionIn": "cut", "darken": 0})
    props = {"totalSeconds": end, "shots": shots, "overlays": [], "words": [], "captions": False, "fx": fx}
    json.dump(props, open(rem / "props.json", "w", encoding="utf-8"))
    composer = REPO / "remotion-composer"
    entry = episode.tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    out = P / "renders"
    out.mkdir(parents=True, exist_ok=True)
    silent = out / f"{name}-silent.mp4"
    subprocess.run(["npx", "remotion", "render", str(entry), "StorybookLong", str(silent), f"--props={(rem / 'props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", "--log=error"], cwd=composer, check=True, shell=sys.platform == "win32")
    # sound: the hooks from the events + a few free library cues on the scene (spark, riser, cart)
    cues = comic_fx.sfx_for(fx) + (extra_cues if extra_cues is not None else [{"name": "riser-drone", "at": 0.3, "gain_db": -22.0, "dur": 2.7}, {"name": "metal-clank", "at": 2.32, "gain_db": -16.0},
                                    {"name": "horse-carriage", "at": 8.6, "gain_db": -24.0, "dur": 5.0}])
    lib = KIT / "library/sfx"
    ins, chains = [], []
    for i, c in enumerate(cues):
        ins += ["-i", str(lib / f"{c['name']}.mp3")]
        d = c.get("dur")
        trim = f"atrim=0:{d}," if d else ""
        chains.append(f"[{i}:a]{trim}asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume={c['gain_db']}dB,"
                      f"adelay={int(c['at'] * 1000)}|{int(c['at'] * 1000)}[a{i}]")
    mix = "".join(f"[a{i}]" for i in range(len(cues)))
    final = out / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), *ins, "-filter_complex",
                    ";".join(chains) + f";{mix}amix=inputs={len(cues)}:normalize=0,atrim=0:{end},loudnorm=I=-14:TP=-1.5[m]",
                    "-map", "0:v", "-map", "[m]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(final)], check=True)
    print(final, f"{episode.duration(final):.2f}s", "cues:", [(c["name"], c["at"]) for c in cues])
    return final


if __name__ == "__main__":
    main()
