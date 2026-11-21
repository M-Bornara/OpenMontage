"""HCS10 Pettenkofer, rough cut 1 (2026-11-20; user: "go ahead with the 9 story stills and the edit"): writes the
timeline into projects/hcs10-pettenkofer/episode.json from Liam's REAL narration (artifacts/word_timestamps.json).

HERO shots 1 / 4 / 6 / 7 are the APPROVED real-art previews (hero_real_hcs10.py, page v6) ported as they are: the same
paid pieces, the same fitted sizes and anchors, the same keys warped onto Liam's words; the HERO shots start exactly at
the preview windows, so every key lands where it was approved. The other shots are ALIVE moves from storyboard-v1.md
(light, particles, camera; nothing cut out of a still moves, L53); shot 12 is the BREATH. Shot 8 is the free Meyers
c.1885 plate (the LEFT tube only) laid on aged paper here.
Also, once (idempotent): the caption spellings (user OK 2026-11-20), plate-s1 without the paper edge, the hand-s7 sprite
with the faint lines faded, the shot-8 document.
    python channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/edit_hcs10.py
    python channels/storybook-medical/scripts/episode.py sfx hcs10-pettenkofer
    python channels/storybook-medical/scripts/episode.py build hcs10-pettenkofer
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(HERE))
import hero_real_hcs10 as hr  # noqa: E402

PID = "hcs10-pettenkofer"
P = REPO / "projects" / PID
KF = f"projects/{PID}/assets/images/keyframes/"
REFS = P / "assets/images/refs"
SPRD = P / "assets/images/sprites"
TOP, MID, LOW = 360, 660, 1030
# rough cut 1 text sheet (2026-11-20): captions moved off faces and off the HERO actions (s1 mouth + glass, s4 his face,
# s6 his eyes, s7 the clutching hand; s2/s5a/s10/s12 people and the glass); the HAMBURG stamp dropped (the caption says it)
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())  # noqa: E731

# ── 1. caption spellings (Whisper: "Pettenkoffer", "73 -year -old", "8 ,600"); the raw transcript is kept once ─────────
WT = P / "artifacts/word_timestamps.json"
RAW = P / "artifacts/word_timestamps.raw.json"
if not RAW.exists():
    shutil.copy(WT, RAW)
raw = json.load(open(RAW, encoding="utf-8"))
words, i = [], 0
while i < len(raw):
    w = dict(raw[i])
    if w["word"] == "73" and i + 2 < len(raw) and raw[i + 1]["word"] == "-year":
        w.update(word="73-year-old", end=raw[i + 2]["end"]); i += 3
    elif w["word"] == "8" and i + 1 < len(raw) and raw[i + 1]["word"].startswith(",600"):
        w.update(word="8,600", end=raw[i + 1]["end"]); i += 2
    else:
        w["word"] = w["word"].replace("Pettenkoffer", "Pettenkofer"); i += 1
    words.append(w)
json.dump(words, open(WT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ── 2. the shots: (name, its first words, caption zone); HERO shots start at their approved preview windows ─────────────
PLAN = [("1", "munich 1892", TOP), ("2", "cholera had", TOP), ("3a", "robert koch", TOP), ("3b", "max von", TOP),
        ("4", "his students", LOW), ("5a", "baking soda", TOP), ("5b", "then germs", TOP), ("6", "one gulp", TOP),
        ("7", "two days", 600), ("8", "for a", LOW), ("9", "but it", TOP), ("10", "his critics", TOP),
        ("11", "the baking", TOP), ("12", "he survived", TOP)]
HERO = {n: hr.SHOT[n]["win"][0] for n in hr.SHOT}           # {"1": 0.0, "4": 15.6, "6": 24.85, "7": 28.3}
toks = [norm(w["word"]) for w in words]
first, starts, k = {}, {}, 0
for name, lead_words, _cap in PLAN:
    want = lead_words.split()
    k = next(j for j in range(k, len(toks)) if toks[j:j + len(want)] == want)
    first[name] = k
    starts[name] = HERO.get(name, round(max(words[k - 1]["end"] + 0.1 if k else 0.0, words[k]["start"] - 0.3), 2))
    k += 1
names = [p[0] for p in PLAN]
END_ALL = round(words[-1]["end"] + 1.2, 2)                   # the held last frame (the end line sits on it)
dur = {n: round((starts[names[j + 1]] if j + 1 < len(names) else END_ALL) - starts[n], 2) for j, n in enumerate(names)}


def w(word: str, shot: str) -> float:
    """Start of `word` inside `shot`, relative to the shot start."""
    j0 = first[shot]
    j1 = first[names[names.index(shot) + 1]] if shot != names[-1] else len(words)
    for j in range(j0, j1):
        if toks[j] == norm(word):
            return round(words[j]["start"] - starts[shot], 2)
    raise SystemExit(f"{word!r} not in shot {shot}")


def cam(t, s, fx, fy, sx=0.5, sy=0.5, **kw):
    """Camera key: frame point (fx, fy) shown at screen point (sx, sy) at zoom s."""
    return {"t": round(t, 3), "scale": s, "x": round((sx - 0.5 - (fx - 0.5) * s) * 100, 2),
            "y": round((sy - 0.5 - (fy - 0.5) * s) * 100, 2), **kw}


# ── 3. one-time assets (free) ────────────────────────────────────────────────────────────────────────────────────────────
S1_CLEAN = REFS / "plate-s1-clean.png"
if not S1_CLEAN.exists():
    hr._no_paper_s1(Image.open(REFS / "plate-s1.png").convert("RGBA")).save(S1_CLEAN)
SOFT = SPRD / "hand-s7-soft"
if not SOFT.exists():
    SOFT.mkdir()
    meta = json.load(open(SPRD / "hand-s7/sprites.json", encoding="utf-8"))
    hr._soften_writing(Image.open(SPRD / "hand-s7/flat-0.png").convert("RGBA"), hr.SOFTEN[("hand-s7", "flat")]).save(SOFT / "flat-0.png")
    shutil.copy(SPRD / "hand-s7/clutch-0.png", SOFT / "clutch-0.png")
    json.dump(meta, open(SOFT / "sprites.json", "w", encoding="utf-8"), indent=1)
# shot 8: the LEFT tube of the Meyers plate (514 x 588 scan; x 18-162) 1700 px tall on warm aged paper
M_X0, M_X1, M_H, M_TOP = 18, 162, 1700, 110
MK = M_H / 588
M_LEFT = (1080 - round((M_X1 - M_X0) * MK)) // 2
S8 = P / "assets/images/keyframes/s8.png"
if not S8.exists():
    rng = np.random.default_rng(8)
    yy, xx = np.mgrid[0:1920, 0:1080]
    vign = 1 - 0.22 * (((xx - 540) / 540) ** 2 + ((yy - 960) / 960) ** 2)
    paper = np.dstack([232 * vign, 214 * vign, 178 * vign]) + rng.normal(0, 5, (1920, 1080, 1))
    tube = Image.open(REPO / f"projects/{PID}/refs/meyers_cholera_bacilli_1885.png").convert("L").crop((M_X0, 0, M_X1, 588))
    tube = np.array(tube.resize((round(tube.width * MK), M_H), Image.LANCZOS), dtype=float) / 255
    ink = np.array([46, 34, 24], dtype=float)
    reg = paper[M_TOP:M_TOP + M_H, M_LEFT:M_LEFT + tube.shape[1]]
    paper[M_TOP:M_TOP + M_H, M_LEFT:M_LEFT + tube.shape[1]] = reg * tube[..., None] + ink * (1 - tube[..., None])
    Image.fromarray(np.clip(paper, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(S8)
M = lambda x, y: (round((M_LEFT + (x - M_X0) * MK) / 1080, 4), round((M_TOP + y * MK) / 1920, 4))  # noqa: E731

# rough cut 1 review (user 2026-11-20): "shots 1 + 6: the liquid reads yellow-green (poison); grade it clear, slightly warm".
# s1's liquid was painted yellow-green; s6's glass kept the green of the key background through its transparency. Inside
# the glass box only, yellow..cyan pixels lose most of their colour and take a warm hue. Originals kept as *.orig.png.
GLASS = {"hand-glass-s1": {"hold-0": (250, 560, 560, 980), "tilt-0": None},
         "pettenkofer-s6": {"lips-0": (800, 450, 1010, 730), "back-0": (640, 180, 930, 420)}}


def _clear_glass(im: Image.Image, box) -> Image.Image:
    import cv2
    a = np.array(im.convert("RGBA"))
    rgb = np.ascontiguousarray(a[..., :3])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    m = np.zeros(hsv.shape[:2], bool)
    x0, y0, x1, y1 = box
    m[y0:y1, x0:x1] = True
    m &= (hsv[..., 0] >= 22) & (hsv[..., 0] <= 95) & (hsv[..., 1] > 18) & (a[..., 3] > 0)
    hsv[..., 0] = np.where(m, 18, hsv[..., 0])                     # warm
    hsv[..., 1] = np.where(m, hsv[..., 1] * 0.22, hsv[..., 1])     # nearly clear
    out = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB)
    return Image.fromarray(np.dstack([out, a[..., 3]]), "RGBA")


for spr, frames in GLASS.items():
    for fr, box in frames.items():
        src, orig = SPRD / spr / f"{fr}.png", SPRD / spr / f"{fr}.orig.png"
        if box is None or not src.exists():
            continue
        if not orig.exists():
            shutil.copy(src, orig)
        _clear_glass(Image.open(orig), box).save(src)


# ── 4. HERO shots: the approved real-art previews, ported (hero_real_hcs10.build) ───────────────────────────────────────
SPRITES = {"hand-glass": "hand-glass-s1", "student-hand": "student-hand-s1", "hand": "hand-s7-soft"}


def hero(n: str) -> dict:
    shot, _spec = hr.build(n)
    actors = []
    for a in shot["actors"]:
        frames, anchor = a["piece"]
        piece = hr.PIECE[(n, a["id"])]
        spr = SPRITES.get(a["id"], piece) if n != "4" and n != "6" else piece
        act = {"id": a["id"], "sprites": f"proj:assets/images/sprites/{spr}/sprites.json",
               "w": round(next(iter(frames.values())).width / 1080, 4), "anchor": [round(float(anchor[0]), 4), round(float(anchor[1]), 4)],
               "face": "fixed", "xfade": a.get("xfade", 0.08), "depth": {"blur": 0}, "motionBlur": False,
               "keys": [{kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in key.items()} for key in a["keys"]]}
        actors.append(act)
    motion = {"type": "keys", "keys": [{kk: (round(v, 3) if isinstance(v, float) else v) for kk, v in c.items()} for c in shot["cam"]]}
    return {"actors": actors, "motion": motion, "shot": shot}


H1, H4, H6, H7 = hero("1"), hero("4"), hero("6"), hero("7")
# s4: the rack focus of the preview (students -> him by ~1.5 s) as depth blur: z 0.97 -> 1.0 (a 3 % growth under the push)
FOCUS4 = H4["shot"]["focus"][-1][0]
for a in H4["actors"]:
    a["depth"] = {"focus": 1.0, "blur": 140}
    a["keys"][0]["z"] = 0.97
    a["keys"].insert(1, {"t": round(FOCUS4, 2), "x": a["keys"][0]["x"], "y": a["keys"][0]["y"], "z": 1.0, "ease": "out"})
    a["keys"][-1]["z"] = 1.0
G4 = H4["shot"]["glint"]
SW6 = H6["shot"]["swell"]
CRUMPLE = H7["shot"]["crumple"][0]

# ── 5. key words (relative to their shots) ────────────────────────────────────────────────────────────────────────────
CHOLERA1 = w("cholera", "1")
K8600 = w("8600", "2")
GERM3, WATER3 = w("germ", "3a"), w("water", "3a")
ALONE = w("alone", "3b")
NO4 = w("no", "4")
ACID = w("acid", "5a")
TEASPOON = w("teaspoon", "5b")
GULP = w("gulp", "6")
SWARMED = w("swarmed", "8")
VICTORY = w("victory", "9")
MILD = w("mild", "10")
HELPED = w("helped", "11")
BUT12 = w("but", "12")

# ── 6. the ALIVE shots (storyboard tricks; positions measured on the stills, frame fractions) ────────────────────────────
ALIVE = {
    # 2: Hamburg, a slow crane down the street; river fog drifts across it
    "2": dict(motion={"type": "keys", "keys": [cam(0.0, 1.14, 0.5, 0.42), cam(dur["2"], 1.08, 0.5, 0.52, ease="inOut")]},
              fx=[{"kind": "particles", "style": "haze", "x": 0.15, "y": 0.52, "tx": 0.85, "ty": 0.48, "spread": 0.18,
                   "every": 0.35, "life": 4.0, "size": 320, "color": "205,210,214", "opacity": 0.28}]),
    # 3a: window light glows through the flask; a glint crosses his spectacles on "water"
    "3a": dict(motion={"type": "push", "from": 1.02, "to": 1.08, "x": 0, "y": 0.5},
               fx=[{"kind": "glow", "x": 0.74, "y": 0.35, "r": 0.11, "at": 0.0, "dur": 0.9, "strength": 0.4, "color": "225,242,255"},
                   # on his near (left) lens, not the temple arm (user 2026-11-20: rough cut 1 put it beside the rim)
                   {"kind": "glint", "x": 0.421, "y": 0.381, "at": round(WATER3, 2), "size": 26},
                   {"kind": "particles", "style": "haze", "x": 0.06, "y": 0.3, "tx": 0.3, "ty": 0.42, "spread": 0.1,      # dust motes
                    "every": 0.4, "life": 3.0, "size": 110, "color": "236,246,252", "opacity": 0.16}]),
    # 3b: dust in the window shafts; push up the low angle
    "3b": dict(motion={"type": "push", "from": 1.02, "to": 1.09, "x": 0, "y": 1.0},
               fx=[{"kind": "particles", "style": "haze", "x": 0.5, "y": 0.08, "tx": 0.5, "ty": 0.3, "spread": 0.22,
                    "every": 0.3, "life": 3.0, "size": 180, "color": "240,226,190", "opacity": 0.22}]),
    # 5a: white grains fall from the spoon into the water, then a soft white cloud (NO bubbles, NO fizz)
    "5a": dict(motion={"type": "push", "from": 1.03, "to": 1.1, "x": 0, "y": 0},
               fx=[{"kind": "particles", "style": "grains", "x": 0.56, "y": 0.44, "tx": 0.5, "ty": 0.49, "spread": 0.01,
                    "every": 0.05, "life": 0.4, "size": 6, "color": "246,244,236", "from": 0.1, "to": round(ACID, 2)},
                   {"kind": "glow", "x": 0.48, "y": 0.5, "r": 0.09, "at": round(ACID - 0.6, 2), "dur": 1.0, "strength": 0.28,
                    "color": "244,244,238"}]),
    # 5b: the thin clear stream from the flask lip into the small glass
    "5b": dict(motion={"type": "push", "from": 1.02, "to": 1.07, "x": 0, "y": -0.5},
               fx=[{"kind": "particles", "style": "grains", "x": 0.52, "y": 0.51, "tx": 0.51, "ty": 0.69, "spread": 0.004,
                    "every": 0.03, "life": 0.35, "size": 4, "color": "222,236,242", "from": 0.0, "to": round(TEASPOON + 0.4, 2)}]),
    # 8: the Meyers tube: a slow tilt down; a band of light runs down the culture line and the bubble glows on "swarmed"
    "8": dict(source=KF + "s8.png", motion={"type": "keys", "keys": [cam(0.0, 1.3, 0.5, 0.36), cam(dur["8"], 1.3, 0.5, 0.56, ease="inOut")]},
              fx=[{"kind": "travel", "points": [list(M(88, 252)), list(M(84, 395))], "at": round(SWARMED - 0.2, 2), "dur": 0.9,
                   "colors": ["rgba(255,240,205,1)", "rgba(255,206,130,1)"], "width": 8},
                  {"kind": "glow", "x": M(88, 252)[0], "y": M(88, 252)[1], "r": 0.07, "at": round(SWARMED, 2), "dur": 0.3,
                   "strength": 0.6, "color": "255,214,150"}]),
    # 9: morning sun comes up through the window at the left; dust in the light
    "9": dict(motion={"type": "push", "from": 1.02, "to": 1.08, "x": 0, "y": 0},
              fx=[{"kind": "glow", "x": 0.06, "y": 0.36, "r": 0.42, "at": 0.0, "dur": round(VICTORY, 2), "strength": 0.38, "color": "255,212,140"},
                  {"kind": "particles", "style": "haze", "x": 0.1, "y": 0.4, "tx": 0.45, "ty": 0.62, "spread": 0.12,
                   "every": 0.4, "life": 3.0, "size": 200, "color": "250,226,170", "opacity": 0.2}]),
    # 10: the gas lamp flickers; push toward the tapping finger, landing on "mild case"
    # v2 still (critics re-cast): the lamp hangs at the top centre (0.5, 0.15), the bald critic's finger taps at (0.35, 0.64)
    "10": dict(motion={"type": "keys", "keys": [cam(0.0, 1.02, 0.5, 0.5), cam(round(MILD, 2), 1.28, 0.36, 0.6, ease="inOut"),
                                                cam(dur["10"], 1.3, 0.36, 0.6, ease="linear")]},
               fx=[{"kind": "glow", "x": 0.5, "y": 0.15, "r": 0.16, "at": 0.0, "dur": 0.5, "strength": 0.35, "color": "255,196,110"},
                   {"kind": "particles", "style": "haze", "x": 0.5, "y": 0.19, "tx": 0.47, "ty": 0.03, "spread": 0.03,  # lamp heat / smoke
                    "every": 0.45, "life": 3.2, "size": 150, "color": "222,204,172", "opacity": 0.14}]),
    # 11: a cold green tint creeps into the water (no bubbles); the amber lamp stays warm
    "11": dict(motion={"type": "push", "from": 1.03, "to": 1.1, "x": 0, "y": 0},
               fx=[{"kind": "tint", "at": round(HELPED - 0.3, 2), "dur": 1.4, "from": "rgba(70,150,100,0)", "to": "rgba(70,150,100,0.42)"},
                   {"kind": "glow", "x": 0.79, "y": 0.24, "r": 0.1, "at": 0.0, "dur": 0.6, "strength": 0.25, "color": "255,190,110"},
                   {"kind": "particles", "style": "haze", "x": 0.51, "y": 0.6, "tx": 0.5, "ty": 0.48, "spread": 0.05,   # the cloud turns
                    "every": 0.5, "life": 3.0, "size": 120, "color": "242,242,236", "opacity": 0.16}]),
    # 12: BREATH: the lamp glow breathes, the colour drains on "but not the argument"
    "12": dict(motion={"type": "push", "from": 1.0, "to": 1.03, "x": 0, "y": 0}, breath=True,
               grey={"from": round(BUT12, 2), "to": round(dur["12"] - 0.4, 2)},
               fx=[{"kind": "glow", "x": 0.49, "y": 0.3, "r": 0.12, "at": 0.0, "dur": 1.2, "strength": 0.3, "color": "255,196,110"}]),
}

# ── 7. assemble ─────────────────────────────────────────────────────────────────────────────────────────────────────────
shots = []
for j, (name, _lw, cap) in enumerate(PLAN):
    s = {"id": f"s{j + 1:02d}", "start": starts[name], "end": round(starts[name] + dur[name], 2), "source": KF + f"s{name}.png",
         "motion": {"type": "push", "from": 1.02, "to": 1.06, "x": 0, "y": 0}, "captionY": cap, "breath": False}
    if name in ALIVE:
        s.update(ALIVE[name])
    if name == "1":
        s.update(source=str(S1_CLEAN.relative_to(REPO)).replace("\\", "/"), motion=H1["motion"],
                 layers={"bg": "proj:assets/images/refs/plate-s1-clean.png", "actors": H1["actors"]})
    if name == "4":
        s.update(source=f"projects/{PID}/assets/images/refs/plate-s4.png", motion=H4["motion"],
                 fx=[{"kind": "glint", "x": G4[0], "y": G4[1], "at": round(G4[2], 2), "size": 26}],
                 layers={"bg": "proj:assets/images/refs/plate-s4.png", "actors": H4["actors"]})
    if name == "6":
        s.update(source=f"projects/{PID}/assets/images/refs/plate-s6.png", motion=H6["motion"],
                 fx=[{"kind": "glow", "x": 0.22, "y": 0.4, "r": 0.5, "at": round(SW6[0], 2), "dur": SW6[1], "strength": 0.3,
                      "color": "255,252,240"}],
                 layers={"bg": "proj:assets/images/refs/plate-s6.png", "actors": H6["actors"]})
    if name == "7":
        s.update(source=f"projects/{PID}/assets/images/refs/plate-s7.png", motion=H7["motion"],
                 grey={"from": round(CRUMPLE - 0.1, 2), "to": round(dur["7"], 2)},
                 layers={"bg": "proj:assets/images/refs/plate-s7.png", "actors": H7["actors"]})
    shots.append(s)

A = lambda shot, t: round(starts[shot] + t, 2)  # noqa: E731
# rough cut 1 review (user 2026-11-20): a stamp only adds what the narration doesn't say (place, date, name tag), never the
# spoken words (stamp_lint.py, run by the build): "≈ 8,600", "LESS THAN A TEASPOON", "2 DAYS LATER" and the "purest water"
# quote are gone; "1 WEEK" stays because it lands before Liam says "week". MUNICH moved off his hair to the dark wall at the
# upper left (x 43-477, above his head top at y ~690).
overlays = [
    {"kind": "stamp", "start": 2.6, "end": round(starts["2"] - 0.1, 2), "text": "MUNICH · 1892", "y": 600, "x": 260, "size": 44},
    {"kind": "nameTag", "start": A("3a", 0.15), "end": round(starts["3b"] - 0.15, 2), "text": "Robert Koch", "sub": "Berlin", "y": 1060},
    {"kind": "nameTag", "start": A("3b", 0.15), "end": round(starts["4"] - 0.15, 2), "text": "Max von Pettenkofer", "sub": "Munich, 73", "y": 1060},
    {"kind": "stamp", "start": A("8", 0.15), "end": round(starts["9"] - 0.1, 2), "text": "1 WEEK", "y": TOP},
]

S_ = lambda name, t, **kw: {"name": name, "at": round(t, 2), **kw}  # noqa: E731
SFX = [
    S_("watch-ticking", 0.0, gain_db=-16, dur=round(CHOLERA1, 2), fade_out=0.05),          # the tick stops on "cholera"
    S_("cello-low", CHOLERA1, gain_db=-14, dur=2.0, fade_out=0.8, query="cello low note"),
    S_("gulls-water", A("2", 0.0), gain_db=-22, dur=3.6, fade_out=0.8),
    S_("horse-carriage", A("2", 0.6), gain_db=-24, dur=2.5, fade_out=0.8),
    S_("glass-clink", A("3a", 0.3), gain_db=-20),
    S_("door-knock", A("3b", ALONE), gain_db=-14, dur=0.4, fade_out=0.1),                 # one knock on the lectern
    S_("footsteps-hall", A("4", 0.1), gain_db=-20, dur=1.6, fade_out=0.4),
    S_("chair-scrape", A("4", 1.2), gain_db=-22),
    S_("glass-clink", A("5a", 0.3), gain_db=-22),
    S_("water-pour", A("5b", 0.1), gain_db=-24, dur=round(TEASPOON + 0.4, 2), fade_out=0.3),
    # swallow.mp3 (Freesound 'sip.wav', CC0) is a sip then the swallow, which peaks at 2.9 s: start at 2.6 s, peak on "gulp"
    S_("swallow", A("6", GULP - 0.3), gain_db=-14, dur=0.8, fade_out=0.2, query="swallow gulp", **{"in": 2.6}),
    S_("watch-ticking", A("7", 0.0), gain_db=-20, dur=round(CRUMPLE, 2), fade_out=0.1),   # the clock in the silence
    S_("paper-crumple", A("7", CRUMPLE), gain_db=-10, dur=0.9, fade_out=0.2, query="paper crumple"),
    S_("cello-low", A("7", CRUMPLE), gain_db=-12, dur=2.4, fade_out=1.0, query="cello low note"),
    S_("machine-hum", A("8", 0.0), gain_db=-26, dur=round(dur["8"], 2), fade_out=0.5),
    S_("tick-click", A("8", 0.05), gain_db=-18),
    S_("birdsong", A("9", 0.0), gain_db=-24, dur=round(dur["9"], 2), fade_out=0.6),
    S_("quill-writing", A("9", 0.4), gain_db=-20, dur=2.2, fade_out=0.4),
    S_("paper-slide", A("10", 0.1), gain_db=-18),
    S_("crowd-murmur", A("10", 0.3), gain_db=-28, dur=2.0, fade_out=0.6),
    S_("watch-ticking", A("12", 0.3), gain_db=-20, dur=round(dur["12"] - 0.3, 2), fade_out=0.8),
]

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"format": "short", "loop": True, "tail_seconds": 1.0, "motion_lint": "fail",
           "storyboard": "channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/storyboard-v1.md",
           "previz": "rough cut 1 (real narration)", "shots": shots, "overlays": overlays, "sfx": SFX,
           "music": {**ep.get("music", {}), "lufs": -22,
                     "prompts": {"m1": {"sections": 3, "prompt": (
                         "Purely instrumental, no voice, no choir, no singing. Late-Romantic German chamber music, Munich "
                         "1890s: a solo cello and a piano in a minor key over a soft ticking pulse like a pocket watch; "
                         "warm and stubborn at first, tense in the middle, then hollow and quiet; a lonely cello line at "
                         "the close. No modern drums, no synths, no Hollywood orchestra.")}},
                     "selected": ep.get("music", {}).get("selected") or "m1",
                     # storyboard row 7: music out before the pause, silence through "cramps" (clock, crumple, cello note)
                     "gaps": [{"from": round(starts["7"] - 0.2, 2), "to": round(starts["7"] + CRUMPLE + 1.6, 2),
                               "fade_out": 0.4, "fade_in": 0.8}]},
           "packaging": {"version": 2, "case": 12, "hook": {"card": "He drank *cholera*. / On purpose.", "anchor": "top"}}})
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(shots)} shots, {len(words)} words, {END_ALL} s; starts {starts}")
