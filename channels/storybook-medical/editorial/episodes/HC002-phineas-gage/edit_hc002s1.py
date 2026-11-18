"""HC002-S1 Gage, PRE-VIZ cut (2026-11-18): the storyboard (s1-storyboard-v1.md) on a SCRATCH timeline, so the three
HERO shots can be keyframed and previewed before anything is paid.

SCRATCH, replaced later: there is no narration yet (it waits for the image OK and the C33/C22/C24/C28 checks), so this
writes a silent narration.wav and word timings spread evenly over each shot's storyboard length. Every key below is
written RELATIVE to a word (w("shoulder")), so the real narration re-times the motion by re-running this script.
Shots 1, 4, 8 = HERO on the REAL paid pieces (2026-11-18: plates refs/plate-s1/s4/s8.png, cut-outs from the pose and
sprite sheets by cutouts_hc002s1.py; the stand-ins are in review/previz/sprites-free/); the others show their blocking
sketch (breath). Positions are measured on the plates (frame fractions).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/edit_hc002s1.py
    python channels/storybook-medical/scripts/episode.py build hc002-s1
    python channels/storybook-medical/scripts/layer_review.py hc002-s1 s01 --from 0 --seconds 3
"""
import json
import re
import subprocess
from pathlib import Path

PID = "hc002-s1"
P = Path("projects") / PID
PV = f"projects/{PID}/review/previz/"
SPR = f"proj:assets/images/sprites/"
TOP, MID, LOW = 360, 660, 1030
TOP4 = 288   # shot 4: Gage's head on the ledge starts at y ~0.24 (460 px): the caption sits above it (safe zone >= 288)
PLATE = f"projects/{PID}/assets/images/refs/"
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())  # noqa: E731

# (shot, storyboard seconds, narration, caption zone, words start after, words end before)
PLAN = [
    ("1", 3.0, "In 1848, an iron bar shot straight through a man's skull.", LOW, 0.15, 0.25),
    ("2a", 2.6, "Phineas Gage. Twenty-five. Railroad foreman.", TOP, 0.1, 0.2),
    ("2b", 2.6, "The best his bosses had.", LOW, 0.3, 0.6),
    ("3", 3.2, "His job: pack blasting powder into the rock with an iron bar. Thirteen pounds.", TOP, 0.1, 0.2),
    ("4", 3.0, "His men caught his eye. He looked over his shoulder…", TOP4, 0.1, 0.35),
    ("5", 1.6, "…and the iron struck the rock. A spark.", TOP, 0.05, 0.1),
    ("6", 3.8, "The bar went in under his cheekbone, behind his eye… and out the top of his head.", LOW, 0.15, 0.3),
    ("7", 2.0, "It landed about eighty feet away.", TOP, 0.2, 0.3),
    ("8", 5.0, "Within minutes… he spoke.", TOP, 2.2, 1.2),     # TOP: LOW sat on his head once he props up          # music silent: 2.2 s of nothing first
    ("9", 3.4, "He rode to his hotel sitting up in an ox cart.", TOP, 0.2, 0.3),
    ("10", 5.0, "The doctor remembered the greeting: \"Doctor, here is business enough for you.\"", TOP, 0.15, 0.3),
    ("11", 2.8, "He survived. He even kept the iron.", TOP, 0.15, 0.35),
    ("12", 4.6, "But his friends said… he was \"no longer Gage.\"", LOW, 0.4, 1.2),
]

# ── the scratch timeline ───────────────────────────────────────────────────────────────────────────────────────────────
words, starts, t = [], {}, 0.0
for name, secs, line, *_rest in PLAN:
    a, b = t + _rest[1], t + secs - _rest[2]
    toks = line.split()
    wt = [len(norm(x)) + 2 for x in toks]
    k = (b - a) / sum(wt)
    x = a
    for tok, wgt in zip(toks, wt):
        words.append({"word": tok, "start": round(x, 3), "end": round(x + wgt * k - 0.04, 3), "shot": name})
        x += wgt * k
    starts[name] = round(t, 2)
    t += secs
TOTAL_NARR = round(t, 2)
(P / "artifacts").mkdir(parents=True, exist_ok=True)
json.dump([{k: v for k, v in w_.items() if k != "shot"} for w_ in words],
          open(P / "artifacts/word_timestamps.json", "w", encoding="utf-8"), indent=1)
(P / "assets/audio").mkdir(parents=True, exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{TOTAL_NARR}",
                "-c:a", "pcm_s16le", str(P / "assets/audio/narration.wav")], check=True)


def w(phrase: str, shot: str, word: int = 0) -> float:
    """Start of `phrase` (inside `shot`) in seconds RELATIVE to the shot start."""
    want = [norm(x) for x in phrase.split()]
    ws = [x for x in words if x["shot"] == shot]
    toks = [norm(x["word"]) for x in ws]
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            return round(ws[i + word]["start"] - starts[shot], 2)
    raise SystemExit(f"{phrase!r} not in shot {shot}")


# ── HERO 1: the bar in the air (hook card on top, y 360-~610: the bar stays below y 0.36 while the card is up) ───────
# plate-s1: the blast hole at (0.47, 0.68), the two ducking crewmen at x 0.22-0.37 and 0.62-0.73; Gage stands between
# them in the foreground (feet just below the frame at 1.065, head top ~0.66, raised hands below ~0.60: the LOW caption
# at 0.54 stays above them), darkened to a back-lit silhouette.
IRON = {"id": "iron", "sprites": SPR + "iron/sprites.json", "w": 0.34, "face": "keys",
        "motionBlur": {"samples": 10, "shutter": 0.6},
        "keys": [{"t": 0.0, "x": 0.54, "y": 0.45, "rot": -72},                        # already ABOVE his hat (care: never across his head)
                 {"t": 0.45, "x": 0.55, "y": 0.44, "rot": -20, "ease": "out"},        # fast, then...
                 {"t": 2.4, "x": 0.60, "y": 0.43, "rot": 330},                        # ...hangs, one slow turn (time remap)
                 {"t": 3.0, "x": 1.2, "y": 0.05, "rot": 560, "ease": "in"}]}          # card gone: out top-right
GAGE1 = {"id": "gage", "sprites": SPR + "gage-s1/sprites.json", "w": 0.48, "face": "keys", "xfade": 0.08,
         "grade": "brightness(0.15) saturate(0.5)",            # back-lit by the pale sky: a silhouette (storyboard, care)
         "states": {"stand": {}, "thrown": {}},
         "keys": [{"t": 0.0, "x": 0.50, "y": 1.065, "rot": -3, "state": "stand"},
                  {"t": 0.1, "x": 0.50, "y": 1.065, "rot": -6, "state": "thrown"},
                  {"t": 0.8, "x": 0.48, "y": 1.07, "rot": -13, "ease": "out"},
                  {"t": 3.0, "x": 0.475, "y": 1.07, "rot": -15}]}
HAT = {"id": "hat", "sprites": SPR + "hat/sprites.json", "w": 0.13, "face": "keys",
       "grade": "brightness(0.55) saturate(0.7)", "states": {"side": {}, "tumble": {}},
       "keys": [{"t": 0.0, "x": 0.53, "y": 0.655, "rot": 0, "state": "side"},
                {"t": 0.25, "x": 0.47, "y": 0.58, "rot": -60, "state": "tumble"},
                {"t": 1.3, "x": 0.27, "y": 0.42, "rot": -220, "ease": "out"},
                {"t": 3.0, "x": 0.12, "y": 0.47, "rot": -300}]}
DUST1 = {"kind": "particles", "style": "haze", "x": 0.47, "y": 0.70, "tx": 0.5, "ty": 0.5, "spread": 0.12, "every": 0.12,
         "life": 2.6, "size": 220, "color": "196,186,166", "opacity": 0.45, "from": 0, "to": 3}

# ── HERO 4: the look over the shoulder (on "shoulder") ─────────────────────────────────────────────────────────────────
TURN = w("shoulder", "4")
# plate-s4: the drill hole on the ledge at (0.485, 0.506), between the two crewmen's backs: the iron's tip stands in it
# (the rod is centred on the canvas, its tip at the feet line); Gage about 0.27 of the frame tall.
GAGE4 = {"id": "gage", "sprites": SPR + "gage-s4/sprites.json", "w": 0.152, "face": "fixed", "xfade": 0.2,
         "grade": "sepia(0.12)", "breath": {"amp": 0.008, "period": 3.0, "states": ["down", "turn"]},
         "keys": [{"t": 0.0, "x": 0.487, "y": 0.512, "state": "down"}, {"t": TURN, "x": 0.487, "y": 0.512, "state": "turn"}]}

# ── HERO 8: the climax, in silence (fingers move, then up on the elbow on "spoke") ──────────────────────────────────────
SPOKE = w("spoke", "8")
# plate-s8: the clear floor in the lower middle (x 0.25-0.75, y 0.66-0.86); his head to the right, away from us.
GAGE8 = {"id": "gage", "sprites": SPR + "gage-s8/sprites.json", "w": 0.62, "face": "fixed", "xfade": 0.25,
         "grade": "brightness(0.88) sepia(0.18)", "breath": {"amp": 0.012, "period": 2.6, "states": ["lie", "fingers", "prop"]},
         "keys": [{"t": 0.0, "x": 0.49, "y": 0.80, "state": "lie"}, {"t": 1.6, "x": 0.49, "y": 0.80, "state": "fingers"},
                  {"t": SPOKE, "x": 0.49, "y": 0.80, "state": "prop"}]}
SMOKE8 = {"kind": "particles", "style": "haze", "x": 0.5, "y": 0.45, "tx": 0.5, "ty": 0.62, "spread": 0.3, "every": 0.3,
          "life": 3.5, "size": 260, "color": "200,194,182", "opacity": 0.3, "from": 0, "to": 5}

# ── the shots ──────────────────────────────────────────────────────────────────────────────────────────────────────────
SKETCH = {"push": {"type": "push", "from": 1.02, "to": 1.08, "x": 0, "y": 0}}
shots = []
for i, (name, secs, line, cap, *_r) in enumerate(PLAN):
    s = {"id": f"s{i + 1:02d}", "start": starts[name], "end": round(starts[name] + secs, 2), "source": PV + f"{name}.png",
         "motion": SKETCH["push"], "captionY": cap, "breath": True, "previz": name}
    if name == "1":
        s.update(source=PLATE + "plate-s1.png", motion={"type": "pull", "from": 1.08, "to": 1.02},
                 hit={"at": 0, "strength": 3.2, "seconds": 0.8}, fx=[DUST1], breath=False,
                 layers={"bg": "proj:assets/images/refs/plate-s1.png", "actors": [GAGE1, IRON, HAT]})
    if name == "4":
        s.update(source=PLATE + "plate-s4.png", breath=False,
                 motion={"type": "push", "from": 1.02, "to": 1.1, "x": -2, "y": 4},
                 layers={"bg": "proj:assets/images/refs/plate-s4.png", "mg": [GAGE4]})
    if name == "8":
        s.update(source=PLATE + "plate-s8.png", breath=False,
                 motion={"type": "push", "from": 1.0, "to": 1.04, "x": 0, "y": 0}, fx=[SMOKE8],
                 layers={"bg": "proj:assets/images/refs/plate-s8.png", "mg": [GAGE8],
                         "glows": [{"x": 0.3, "y": 0.25, "r": 320, "strength": 0.22}]})   # glow on the plate's light shaft, upper left
    shots.append(s)

overlays = [
    {"kind": "nameTag", "start": starts["2a"] + 0.2, "end": starts["2a"] + 2.5, "text": "Phineas Gage", "sub": "railroad foreman, 25", "y": 1000},
    {"kind": "stamp", "start": starts["2a"] + 0.3, "end": starts["2a"] + 2.3, "text": "CAVENDISH, VERMONT · 1848", "y": MID},   # TOP collided with the caption (text_check)
    {"kind": "stamp", "start": starts["3"] + 1.6, "end": starts["3"] + 3.1, "text": "3 ft 7 in · 13¼ lb (1.1 m · 6 kg)", "y": MID},
    {"kind": "stamp", "start": starts["7"] + 0.4, "end": starts["7"] + 1.9, "text": "≈ 80 ft (25 m)", "y": MID},
]

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"title": "He Took an Iron Bar Through the Skull… and Spoke", "format": "short", "loop": True, "tail_seconds": 1.0,
           "motion_lint": "warn",   # PRE-VIZ: the non-HERO shots are sketches (breath); the real cut runs the full lint
           "previz": "scratch timeline 2026-11-18; replace with the real narration", "shots": shots, "overlays": overlays,
           "sfx": [], "music": {"selected": "", "prompts": {}},
           "packaging": {"version": 2, "case": 11, "hook": {"card": "An iron bar / through his *skull*.", "anchor": "top"}}})
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(shots)} shots, {len(words)} scratch words, {TOTAL_NARR} s; turn at {TURN} s in shot 4, 'spoke' at {SPOKE} s in shot 8")
