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

# ── the timeline: the REAL narration once it exists (a non-silent narration.wav from `episode.py narrate`), else the
# SCRATCH one (silent wav + words spread over each shot's storyboard length, for the pre-viz)
def _audible(wav: Path) -> bool:
    if not wav.exists():
        return False
    import wave
    with wave.open(str(wav)) as f:
        data = f.readframes(f.getnframes())
    return any(b not in (0, 255) for b in data[::97])        # pcm16 silence = 00 00 / ff ff around zero


WAV, WT = P / "assets/audio/narration.wav", P / "artifacts/word_timestamps.json"
REAL = _audible(WAV) and WT.exists()
words, starts, dur = [], {}, {}
if REAL:
    # each shot starts `lead` before its first word (never before the previous shot's last word ends) and runs to the
    # next shot; the shot's first words are found in order in the transcript (2 tokens, then 1)
    real = json.load(open(WT, encoding="utf-8"))
    toks = [norm(x["word"]) for x in real]
    firsts, i = [], 0
    for name, secs, line, cap, lead, tail in PLAN:
        want = [norm(x) for x in line.split() if norm(x)][:2]
        j = next((k for k in range(i, len(toks)) if toks[k:k + 2] == want), None)
        if j is None:
            j = next((k for k in range(i, len(toks)) if toks[k] == want[0]), i)
        firsts.append(j)
        i = j + 1
    for n_, (name, secs, line, cap, lead, tail) in enumerate(PLAN):
        j = firsts[n_]
        last = firsts[n_ + 1] - 1 if n_ + 1 < len(PLAN) else len(real) - 1
        prev_end = real[j - 1]["end"] + 0.12 if j > 0 else 0.0
        starts[name] = 0.0 if n_ == 0 else round(max(prev_end, real[j]["start"] - lead), 2)
        for x in real[j:last + 1]:
            words.append({**x, "shot": name})
    names = [x[0] for x in PLAN]
    end_all = round(real[-1]["end"] + PLAN[-1][5], 2)
    for k, name in enumerate(names):
        dur[name] = round((starts[names[k + 1]] if k + 1 < len(names) else end_all) - starts[name], 2)
    import subprocess as _sp
    TOTAL_NARR = float(_sp.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(WAV)],
                               capture_output=True, text=True).stdout.strip())
else:
    t = 0.0
    for name, secs, line, *_rest in PLAN:
        a_, b_ = t + _rest[1], t + secs - _rest[2]
        toks = line.split()
        wt = [len(norm(x)) + 2 for x in toks]
        k = (b_ - a_) / sum(wt)
        x = a_
        for tok, wgt in zip(toks, wt):
            words.append({"word": tok, "start": round(x, 3), "end": round(x + wgt * k - 0.04, 3), "shot": name})
            x += wgt * k
        starts[name], dur[name] = round(t, 2), secs
        t += secs
    TOTAL_NARR = round(t, 2)
    (P / "artifacts").mkdir(parents=True, exist_ok=True)
    json.dump([{k: v for k, v in w_.items() if k != "shot"} for w_ in words],
              open(WT, "w", encoding="utf-8"), indent=1)
    (P / "assets/audio").mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono", "-t", f"{TOTAL_NARR}",
                    "-c:a", "pcm_s16le", str(WAV)], check=True)


def w(phrase: str, shot: str, word: int = 0) -> float:
    """Start of `phrase` (inside `shot`) in seconds RELATIVE to the shot start."""
    want = [norm(x) for x in phrase.split()]
    ws = [x for x in words if x["shot"] == shot]
    toks = [norm(x["word"]) for x in ws]
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            return round(ws[i + word]["start"] - starts[shot], 2)
    raise SystemExit(f"{phrase!r} not in shot {shot}")


# ── HERO 1: the bar in the air (user 2026-11-18: the bar 2-3x bigger and closer, sunlit edge + glint + trail, visible until
# "skull"; Gage clearly thrown backward, a TRUE silhouette carrying his shot-4 look; HERO rule: the subject >= 1/3 frame)
# plate-s1: the blast hole at (0.47, 0.68), the two ducking crewmen at x 0.22-0.37 and 0.62-0.73; Gage between them in the
# foreground. The hook card covers y 0.19-0.33 until ~2.5 s; captions only after it (the LOW line at 0.54-0.58 on "skull").
SKULL = w("skull", "1")
D1 = dur["1"]   # the real shot length: the last keys end on the cut, nothing freezes
# v2 (story-craft Rule 0b, user 2026-11-19, option A): the hit is SHOWN, softened by silhouette + white flash + head snap.
# The bar bursts UP out of the top of his PURE black silhouette (gage-s1-black: no face, no wound, no blood): it starts
# BEHIND him (layer order), so only the part above his head shows; its tail stays inside the black torso.
# v3 (user 2026-11-19: "the impact is too small and too short, then 3 s of the bar sliding flat"): the same layers,
# re-cut with a keyframed camera (StorybookShort motion "keys"):
#   0-0.8 s   TIGHT on his head + shoulders (x2.8, the silhouette fills the frame), the burst at ~50 % speed (every key of
#             v2's first 0.4 s at twice the time): the flash and the bar coming up out of his head, big;
#   0.8-1.8 s a whip up (blur) and pull out following the bar; Gage falls, the two crewmen flinch (cut out of the plate,
#             crew_hc002s1.py), the rock cut opens up;
#   1.8 s-cut the bar spins END OVER END at the top (~415 deg/s, horizontal with the glint on "skull"), under the hook
#             card until 2.5 s and above the LOW caption after it.
HEAD1 = (0.552, 0.676)          # the top of his head at frame 0 (stand pose, w 0.48, anchor y 1.065)


def cam(t, s, fx, fy, sx=0.5, sy=0.5, **k):
    """Camera key: frame point (fx, fy) shown at screen point (sx, sy) at zoom s (translate % after the scale)."""
    return {"t": round(t, 3), "scale": s, "x": round((sx - 0.5 - (fx - 0.5) * s) * 100, 2),
            "y": round((sy - 0.5 - (fy - 0.5) * s) * 100, 2), **k}


CAM1 = {"type": "keys", "keys": [cam(0.0, 2.8, 0.552, 0.70, 0.5, 0.66),                # head + shoulders fill the frame
                                 cam(0.8, 2.4, 0.63, 0.57, 0.5, 0.56, ease="sine"),     # drifts up with the burst
                                 cam(1.05, 1.8, 0.66, 0.46, ease="in", blur=5),         # the whip up after the bar
                                 cam(1.35, 1.3, 0.60, 0.45, ease="out", blur=0),
                                 cam(1.8, 1.08, 0.5, 0.5, ease="inOut"),                # ...lands on the wide
                                 cam(D1, 1.04, 0.5, 0.5, ease="linear")]}

# Gage: gage-s1-black, thrown BACKWARD; the head snaps back on the pose swap (0.12 s at half speed) with a rot kick, then
# he tips back and falls out of the bottom of the wide. The thrown pose's head sits 0.15 of the frame further right than
# the standing one, so he steps LEFT on the swap: the head stays in the tight frame.
GKEYS = [{"t": 0.0, "x": 0.50, "y": 1.065, "rot": 0, "z": 1.0, "state": "stand"},
         {"t": 0.12, "x": 0.44, "y": 1.045, "rot": 6, "z": 1.04, "state": "thrown"},
         {"t": 0.32, "x": 0.40, "y": 1.02, "rot": 11, "z": 1.09},                    # the snap overshoots...
         {"t": 0.8, "x": 0.41, "y": 1.005, "rot": 11, "z": 1.13, "ease": "out"},     # ...and hangs
         {"t": 1.3, "x": 0.43, "y": 1.05, "rot": 16, "z": 1.2, "ease": "in"},        # then he goes down
         {"t": 1.8, "x": 0.46, "y": 1.12, "rot": 24, "z": 1.26},
         {"t": D1, "x": 0.50, "y": 1.34, "rot": 40, "z": 1.36, "ease": "in"}]
GAGE1 = {"id": "gage", "sprites": SPR + "gage-s1-black/sprites.json", "w": 0.48, "face": "keys", "xfade": 0.04,
         "depth": {"blur": 0}, "motionBlur": False,     # a blurred / cross-faded black body turns see-through: the bar behind showed
         "states": {"stand": {}, "thrown": {}}, "keys": GKEYS}

# The bar rides the BODY'S AXIS while it comes out: the line from the torso through the top of the head, measured on the
# two pose sprites (canvas 906 x 1379, anchor (0.5, 0.9826)); emerged = the share of the bar already out of the head. Its
# tail stays inside the black torso, so it reads as coming OUT OF HIS HEAD in every frame of the tight shot.
AXIS = {"stand": ((0.60, 0.025), (0.47, 0.40)), "thrown": ((0.586, 0.085), (0.32, 0.42))}   # (head top, torso) sprite fractions


def gage_at(t):
    """Gage's key values at t (linear between his keys; the bar keys sit on or near them)."""
    for p, q in zip(GKEYS, GKEYS[1:]):
        if t <= q["t"]:
            u = (t - p["t"]) / (q["t"] - p["t"])
            return {k: p[k] + (q[k] - p[k]) * u for k in ("x", "y", "rot", "z")}
    return GKEYS[-1]


def on_axis(t, emerged, z, pose):
    import math
    g = gage_at(t)
    w_ = 0.48 * g["z"] * 1080
    h_ = w_ * 1379 / 906

    def px(u, v):
        dx, dy, r = (u - 0.5) * w_, (v - 0.9826) * h_, math.radians(g["rot"])
        return g["x"] * 1080 + dx * math.cos(r) - dy * math.sin(r), g["y"] * 1920 + dx * math.sin(r) + dy * math.cos(r)
    (hx, hy), (bx, by) = px(*AXIS[pose][0]), px(*AXIS[pose][1])
    n = math.hypot(hx - bx, hy - by)
    dx, dy = (hx - bx) / n, (hy - by) * 1 / n
    L = 0.6 * z * 1080
    return {"x": round((hx + dx * (emerged - 0.5) * L) / 1080, 4), "y": round((hy + dy * (emerged - 0.5) * L) / 1920, 4),
            "rot": round(math.degrees(math.atan2(dy, dx)), 1), "z": z}


def spin(t):            # the end-over-end rotation after the burst: from 70 deg at 1.2 s to 900 (horizontal) on "skull"
    return round(70 + (900 - 70) * (t - 1.2) / (SKULL - 1.2), 1)


def arc(t):             # the bar's centre after 1.2 s: up and across, slowing as it tops out
    u = (t - 1.2) / (D1 - 1.2)
    return round(0.67 - 0.14 * u, 4), round(0.43 - 0.07 * u + 0.05 * u * u, 4)


ZS = 0.7                # the bar's depth in the spin: ~0.45 of the frame wide at the wide's zoom (HERO >= 1/3)
IRON_KEYS = [{"t": 0.0, **on_axis(0.0, 0.30, 0.7, "stand"), "state": "rod"},     # tip just out of the skull top
             {"t": 0.12, **on_axis(0.12, 0.40, 0.85, "thrown")},                   # bursts up (half speed), on his axis
             {"t": 0.32, **on_axis(0.32, 0.55, 0.92, "thrown")},
             {"t": 0.55, **on_axis(0.55, 0.72, 0.97, "thrown")},
             {"t": 0.8, **on_axis(0.8, 0.86, 1.0, "thrown")},
             {"t": 1.0, "x": 0.70, "y": 0.46, "rot": 10, "z": 0.88},                # out: it tips over...
             {"t": 1.2, "x": arc(1.2)[0], "y": arc(1.2)[1], "rot": 70, "z": 0.78},   # ...end over end
             *[{"t": t, "x": arc(t)[0], "y": arc(t)[1], "rot": spin(t), "z": round(max(ZS, 0.78 - 0.2 * (t - 1.2)), 3)}
               for t in (1.5, 1.8, 2.1, 2.5, 2.85)],
             {"t": SKULL, "x": arc(SKULL)[0], "y": arc(SKULL)[1], "rot": 900, "z": ZS, "state": "glint"},  # glint on "skull"
             {"t": round(SKULL + 0.45, 2), "x": arc(SKULL + 0.45)[0], "y": arc(SKULL + 0.45)[1], "rot": spin(SKULL + 0.45),
              "z": ZS, "state": "rod"},
             {"t": D1, "x": arc(D1)[0], "y": arc(D1)[1], "rot": spin(D1), "z": ZS}]
IRON = {"id": "iron", "sprites": SPR + "iron-lit/sprites.json", "w": 0.6, "face": "keys", "xfade": 0.18,
        "depth": {"blur": 0}, "motionBlur": {"samples": 10, "shutter": 0.6}, "keys": IRON_KEYS}
# the trail: the same bar a moment earlier, fainter (behind the bar): in the spin it smears the rotation
TRAILS = [{**IRON, "id": f"iron-trail{i}", "opacity": op, "xfade": 0, "motionBlur": {"samples": 6, "shutter": 1.2},
           "keys": [{**{k: v for k, v in key.items() if k != "state"}, "t": round(key["t"] + lag, 3), "state": "rod"}
                    for key in IRON_KEYS]}
          for i, (lag, op) in enumerate(((0.04, 0.38), (0.08, 0.18)), 1)]
FLASH1 = {"kind": "flash", "x": HEAD1[0], "y": HEAD1[1] - 0.01, "r": 0.13, "at": 0, "rise": 0.1, "dur": 0.46, "start": 0.6,
          "lift": 0.14}
HAT = {"id": "hat", "sprites": SPR + "hat-black/sprites.json", "w": 0.13, "face": "keys", "depth": {"blur": 0},
       "states": {"side": {}, "tumble": {}},
       "keys": [{"t": 0.0, "x": 0.475, "y": 0.632, "rot": -26, "state": "tumble"},   # already knocked off, clear of the exit point
                {"t": 0.5, "x": 0.44, "y": 0.59, "rot": -70},
                {"t": 1.7, "x": 0.22, "y": 0.58, "rot": -220, "ease": "out"},
                {"t": D1, "x": 0.08, "y": 0.62, "rot": -300}]}
# the crew (cut from the plate by crew_hc002s1.py; at rest exactly on the painted men): they flinch AWAY from the blast
# as the camera pulls out (lean + a squash = ducking), then settle. Out of frame while the camera is tight.
CREW = json.load(open(P / "assets/images/sprites/crew.json", encoding="utf-8"))
CREW1 = [{"id": n, "sprites": SPR + f"{n}/sprites.json", "w": CREW[n]["w"], "anchor": CREW[n]["anchor"], "face": "keys",
          "depth": {"blur": 0}, "motionBlur": False, "states": {"stand": {}},
          "keys": [{"t": 0.0, "x": CREW[n]["x"], "y": CREW[n]["y"], "rot": 0, "state": "stand"},
                   {"t": 0.95, "x": CREW[n]["x"], "y": CREW[n]["y"], "rot": 0},
                   {"t": 1.25, "x": CREW[n]["x"], "y": CREW[n]["y"], "rot": sgn * 5, "ease": "out",
                    "contact": {"squash": 0.07, "hz": 3.0, "decay": 5}},
                   {"t": D1, "x": CREW[n]["x"], "y": CREW[n]["y"], "rot": sgn * 3.5, "ease": "sine"}]}
         for n, sgn in (("crew-l", -1), ("crew-r", 1))]
DUST1 = {"kind": "particles", "style": "haze", "x": 0.40, "y": 0.66, "tx": 0.36, "ty": 0.5, "spread": 0.1, "every": 0.16,
         "life": 2.4, "size": 200, "color": "196,186,166", "opacity": 0.3, "from": 0.9, "to": D1}

# ── HERO 4: the look over the shoulder (on "shoulder"). User 2026-11-18: push in on Gage during the shot so the head turn
# is big (end at MS). Gage on the ledge: x 0.487, feet 0.512, head top ~0.274 (0.24 of the frame tall). The push ends at
# 3.6x with his head top at y 0.30 (under the TOP caption, 0.15-0.26): he fills ~0.86 of the frame height (HERO >= 1/3);
# the shared ease puts ~93 % of the push before the turn. Sprite 513 px wide shown ~590 px: no soft upscale on him.
TURN = w("shoulder", "4")
PUSH4 = {"type": "push", "from": 1.02, "to": 3.6, "x": round(-(0.487 - 0.5) * 3.6 * 100, 2),
         "y": round((0.30 - 0.5 - (0.274 - 0.5) * 3.6) * 100, 2)}
GAGE4 = {"id": "gage", "sprites": SPR + "gage-s4/sprites.json", "w": 0.152, "face": "fixed", "xfade": 0.2,
         "grade": "sepia(0.12)", "breath": {"amp": 0.008, "period": 3.0, "states": ["down", "turn"]},
         "keys": [{"t": 0.0, "x": 0.487, "y": 0.512, "state": "down"}, {"t": TURN, "x": 0.487, "y": 0.512, "state": "turn"}]}

# ── HERO 8: the climax, in silence (fingers move, then up on the elbow on "spoke") ──────────────────────────────────────
SPOKE = w("spoke", "8")
# plate-s8 v4 (ground level, user 2026-11-18): the bare floor fills the lower half. The close pose sheet (v4): the waist cut
# just off the left edge, his open hand large at the lower left, the back of his head at the right; up on his elbow on
# "spoke" (the shoulder rises to ~y 0.47). Width ~0.97 of the frame (HERO >= 1/3).
GAGE8 = {"id": "gage", "sprites": SPR + "gage-s8/sprites.json", "w": 1.0, "face": "fixed", "xfade": 0.25,
         "grade": "brightness(0.86) sepia(0.15) saturate(0.85)",
         "breath": {"amp": 0.010, "period": 2.6, "states": ["lie", "fingers", "lift", "prop"]},
         # user 2026-11-18: the prop frame is matched to the lying body (match_s8.py: same scale, pinned at the waist) and
         # "lift" (the fingers frame tipped up at the waist) bridges them, so the shoulder rises from where it lay
         "keys": [{"t": 0.0, "x": 0.47, "y": 1.0, "state": "lie"}, {"t": round(max(0.6, SPOKE - 1.3), 2), "x": 0.47, "y": 1.0, "state": "fingers"},
                  {"t": round(SPOKE - 0.45, 2), "x": 0.47, "y": 1.0, "state": "lift"},
                  {"t": SPOKE, "x": 0.47, "y": 1.0, "state": "prop"}]}
SMOKE8 = {"kind": "particles", "style": "haze", "x": 0.5, "y": 0.45, "tx": 0.5, "ty": 0.62, "spread": 0.3, "every": 0.3,
          "life": 3.5, "size": 260, "color": "200,194,182", "opacity": 0.3, "from": 0, "to": 5}

# ── ALIVE shots (rough cut 1, user 2026-11-18 "go ahead with the first full cut"): the approved stills with FREE moves made
# from the image itself (storyboard v1 tricks): masks + clean plates by alive_hc002s1.py, the iron sprite from shot 1,
# shot 6 = Harlow's engraving on paper (paper_s6.py). Times are word-relative, positions measured on the stills.
KF = f"projects/{PID}/assets/images/keyframes/"
FX = KF + "fx/"


def wag(still, name, hinge, deg, period, a, b=None):
    return {"kind": "wag", "mask": FX + f"{still}-{name}.mask.png", "bg": FX + f"{still}-{name}.clean.png", "hinge": hinge,
            "deg": deg, "period": period, "from": a, **({"to": b} if b is not None else {})}


def iron(keys, w_, blur=True, spr="iron-lit"):
    """spr "iron-thick" in the close-ups (shots 3, 5; user 2026-11-19): 1 1/4 in = ~2 finger-widths next to the hand."""
    return {"id": "iron", "sprites": SPR + f"{spr}/sprites.json", "w": w_, "face": "keys", "depth": {"blur": 0},
            **({"motionBlur": {"samples": 8, "shutter": 0.5}} if blur else {}), "keys": keys}


def along(c, d, px):
    """A point `px` pixels from c along the unit direction d (pixel space), back in frame fractions."""
    return round(c[0] + d[0] * px / 1080, 4), round(c[1] + d[1] * px / 1920, 4)


# shot 3: the flask pours (grains, nozzle 0.465,0.53 -> hole 0.42,0.61); on "iron" the bar slides into the hole (blunt end
# down, the point up and a little left: rot -97, clear of the CASE chip; rough cut 1 had -114 and the point ran into the
# chip), on "13" one tamp. w 1.0 = 1031 px long: its centre sits 515 px up the axis from the hole, the point at y ~0.08.
IRON3_T, TAMP3 = w("iron bar", "3"), w("13", "3")
D3 = (-0.12, -0.993)
C3 = along((0.42, 0.615), D3, 515)
IN3, UP3 = along(C3, D3, 1250), along(C3, D3, 45)
# user 2026-11-19: POUR, THEN BAR. The pour stops 0.75 s before "iron" (the last grains land ~0.33 s before), the flask
# tips up and the hand + flask slide out to the right (hand_hc002s1.py cut them out of the still) while the bar slides in;
# the hand is out of frame before the bar reaches the hole. No powder falls beside the bar.
POUR_END = round(IRON3_T - 0.75, 2)
H3 = {"w": 0.554, "x": 0.723, "y": 0.3}            # hand_hc002s1.py: the sprite at rest sits exactly on the painted hand
HAND3 = {"id": "hand3", "sprites": SPR + "hand3/sprites.json", "w": H3["w"], "face": "keys", "depth": {"blur": 0},
         "motionBlur": {"samples": 8, "shutter": 0.5},
         "keys": [{"t": 0.0, "x": H3["x"], "y": H3["y"], "rot": 0, "state": "stand"},
                  {"t": POUR_END, "x": H3["x"], "y": H3["y"], "rot": 0},
                  {"t": round(IRON3_T - 0.6, 2), "x": H3["x"] + 0.01, "y": H3["y"] - 0.01, "rot": 7, "ease": "out"},   # tips up: the pour stops
                  {"t": round(IRON3_T - 0.12, 2), "x": 1.45, "y": H3["y"] - 0.06, "rot": 10, "ease": "in"}]}         # out right
IRON3 = iron([{"t": 0.0, "x": IN3[0], "y": IN3[1], "rot": -97, "state": "rod"},
              {"t": round(IRON3_T - 0.4, 2), "x": IN3[0], "y": IN3[1], "rot": -97},
              {"t": IRON3_T, "x": C3[0], "y": C3[1], "rot": -97, "ease": "out", "contact": {"squash": 0.04}},
              {"t": round(TAMP3 - 0.25, 2), "x": UP3[0], "y": UP3[1], "rot": -97, "ease": "out"},
              {"t": TAMP3, "x": C3[0], "y": C3[1], "rot": -97, "ease": "in", "contact": {"squash": 0.05}}], 1.0, spr="iron-thick")
# shot 5: the bar drives straight down (blunt end first, rot -90) and strikes the lip of the hole (0.495, 0.48) on "struck";
# the big spark + glow + jolt on "spark". 1.3 frame widths long: the top end stays out of frame.
STRUCK, SPARK5 = w("struck", "5"), w("spark", "5")
Y5 = round(0.48 - 1.3 * 1080 * 0.955 / 2 / 1920, 4)
IRON5 = iron([{"t": 0.0, "x": 0.495, "y": -0.42, "rot": -90, "state": "rod"},
              {"t": 0.12, "x": 0.495, "y": -0.42, "rot": -90},
              {"t": STRUCK, "x": 0.495, "y": Y5, "rot": -90, "ease": "in", "contact": {"squash": 0.06}},
              {"t": round(SPARK5, 2), "x": 0.495, "y": round(Y5 + 0.004, 4), "rot": -90, "state": "glint"}], 1.3, spr="iron-thick")
# shot 6: the bar's path draws itself over the engraving (straight, as engraved): in under the cheekbone on "cheekbone",
# behind the eye on "eye", out of the top on "top". Points in ENGRAVING fractions, placed by paper_s6.py's layout.
LAY6 = json.load(open(P / "assets/images/keyframes/s6_layout.json", encoding="utf-8"))["9x16"]
E6 = lambda u, v: [round(LAY6["x0"] + u * LAY6["w"], 4), round(LAY6["y0"] + v * LAY6["h"], 4)]  # noqa: E731
CHEEK, EYE, TOPW = w("cheekbone", "6"), w("eye", "6"), w("top", "6")
# measured on the full plate (Harlow 1868 p.24 scan, refs/harlow_skull_1868_full.png): the bar's centre line runs
# (0.372, 0.00) -> (0.612, 0.95); the path stays ON it, from the entry under the cheekbone to the exit at the top of the
# skull, and stops there (user 2026-11-19: no lead-in from the jaw, nothing above the skull)
PATH6 = [((0.548, 0.69), (0.511, 0.55), CHEEK - 0.1, EYE + 0.05), ((0.511, 0.55), (0.411, 0.155), EYE + 0.05, TOPW + 0.1)]
DRAW6 = [{"points": [E6(*a), E6(*b)], "from": round(t0, 2), "to": round(t1, 2), "color": "#F0A23A", "width": 14, "glow": True}
         for a, b, t0, t1 in PATH6]
# shot 7: the bar falls in from the top and sticks point-first in the grass between the two runners (tip 0.555, 0.72) on "landed"
LANDED = w("landed", "7")
TIP7, D7 = (0.555, 0.72), (-0.087, 0.996)         # pointing down, 5 degrees left of vertical
C7 = along(TIP7, D7, -0.45 * 1080 * 0.955 / 2)
IRON7 = iron([{"t": 0.0, "x": 0.50, "y": -0.22, "rot": 80, "state": "rod"},
              {"t": LANDED, "x": C7[0], "y": C7[1], "rot": 95, "ease": "in", "contact": {"squash": 0.1, "bounce": 0.02}}], 0.45)
SAY10, BIZ = w("doctor here", "10"), w("business", "10")
KEPT = w("kept", "11")
SAID, NO12 = w("said", "12"), w("no longer", "12")

ALIVE = {
    "2a": dict(motion={"type": "push", "from": 1.02, "to": 1.09, "x": 2.0, "y": 1.0},
               fx=[wag("s2a", "arm", [0.545, 0.39], 8, 0.55, 0.25, 0.25 + 2 * 0.55),
                   {"kind": "particles", "style": "haze", "x": 0.7, "y": 0.62, "tx": 0.85, "ty": 0.55, "spread": 0.15,
                    "every": 0.4, "life": 3.0, "size": 260, "color": "214,196,160", "opacity": 0.22}]),
    "2b": dict(motion={"type": "slide", "from": 2.5, "to": -2.5, "scale": 1.1},
               fx=[wag("s2b", "hammer1", [0.31, 0.678], 7, 0.7, 0.0), wag("s2b", "hammer2", [0.728, 0.757], 5, 0.7, 0.35),
                   {"kind": "particles", "style": "haze", "x": 0.3, "y": 0.45, "tx": 0.5, "ty": 0.3, "spread": 0.2,
                    "every": 0.45, "life": 3.2, "size": 300, "color": "205,200,190", "opacity": 0.2}]),
    "3": dict(motion={"type": "push", "from": 1.02, "to": 1.08, "x": 0.5, "y": -0.5},
              fx=[{"kind": "particles", "style": "grains", "x": 0.466, "y": 0.535, "tx": 0.425, "ty": 0.607, "spread": 0.012,
                   "every": 0.034, "life": 0.42, "size": 7, "from": 0.05, "to": POUR_END}],
              layers={"bg": f"proj:assets/images/keyframes/s3-nohand.png", "actors": [IRON3, HAND3]}),
    "5": dict(motion={"type": "push", "from": 1.03, "to": 1.1, "x": 0, "y": 1.0}, hit={"at": SPARK5, "strength": 3.4, "seconds": 0.6},
              captionY=LOW,
              fx=[{"kind": "spark", "x": 0.495, "y": 0.48, "r": 0.05, "from": STRUCK, "to": round(STRUCK + 0.3, 2)},
                  {"kind": "spark", "x": 0.495, "y": 0.48, "r": 0.16, "from": SPARK5},
                  {"kind": "glow", "x": 0.495, "y": 0.48, "r": 0.55, "at": SPARK5, "dur": 0.12, "strength": 0.85, "color": "255,214,150"}],
              layers={"bg": f"proj:assets/images/keyframes/s5.png", "actors": [IRON5]}),
    "6": dict(motion={"type": "push", "from": 1.0, "to": 1.06, "x": 0, "y": 1.0}, transition="flash", captionY=TOP4, draw=DRAW6),
    "7": dict(motion={"type": "push", "from": 1.04, "to": 1.1, "x": -1.0, "y": -1.0}, hit={"at": LANDED, "strength": 2.4, "seconds": 0.45},
              fx=[{"kind": "particles", "style": "haze", "x": TIP7[0], "y": TIP7[1], "tx": TIP7[0], "ty": TIP7[1] - 0.05,
                   "spread": 0.05, "every": 0.05, "life": 1.0, "size": 170, "color": "196,184,150", "opacity": 0.55,
                   "from": LANDED, "to": round(LANDED + 0.35, 2)}],
              layers={"bg": f"proj:assets/images/keyframes/s7.png", "actors": [IRON7]}),
    "9": dict(motion={"type": "slide", "from": -2.5, "to": 2.5, "scale": 1.1},
              fx=[wag("s9", "ox1", [0.40, 0.53], 2.5, 1.0, 0.0), wag("s9", "ox2", [0.14, 0.52], 2.5, 1.15, 0.3),
                  {"kind": "particles", "style": "haze", "x": 0.55, "y": 0.66, "tx": 0.75, "ty": 0.62, "spread": 0.12,
                   "every": 0.3, "life": 2.4, "size": 240, "color": "214,190,150", "opacity": 0.28}]),
    "10": dict(motion={"type": "push", "from": 1.02, "to": 1.035, "x": 0, "y": 0},
               fx=[wag("s10", "hand", [0.47, 0.49], 7, 0.6, round(SAY10 - 0.1, 2), round(SAY10 - 0.1 + 2 * 0.6, 2)),
                   {"kind": "glint", "x": 0.165, "y": 0.392, "at": round(BIZ + 0.1, 2), "size": 34}]),
    "11": dict(motion={"type": "push", "from": 1.03, "to": 1.12, "x": -1.0, "y": 1.0},
               fx=[{"kind": "travel", "points": [[0.74, 0.185], [0.635, 0.40]], "at": round(KEPT - 0.1, 2), "dur": 0.35,
                    "colors": ["rgba(255,240,205,1)", "rgba(255,206,130,1)"], "width": 10},
                   {"kind": "travel", "points": [[0.595, 0.52], [0.385, 0.925]], "at": round(KEPT + 0.22, 2), "dur": 0.55,
                    "colors": ["rgba(255,240,205,1)", "rgba(255,206,130,1)"], "width": 10}]),
    "12": dict(motion={"type": "push", "from": 1.02, "to": 1.05, "x": 1.0, "y": 0}, grey={"from": SAID, "to": round(NO12 + 0.3, 2)},
               fx=[{"kind": "nudge", "mask": FX + "s12-lean.mask.png", "bg": FX + "s12-lean.clean.png", "at": round(SAID - 0.2, 2),
                    "dur": 1.2, "dx": 0.007, "dy": 0.003},
                   {"kind": "spot", "at": round(NO12 - 0.1, 2), "dur": 10.0, "cx": 0.2, "cy": 0.36, "rx": 0.16, "ry": 0.17, "dim": 0.45}]),
}

# ── the shots ──────────────────────────────────────────────────────────────────────────────────────────────────────────
SKETCH = {"push": {"type": "push", "from": 1.02, "to": 1.08, "x": 0, "y": 0}}
shots = []
for i, (name, _secs, line, cap, *_r) in enumerate(PLAN):
    s = {"id": f"s{i + 1:02d}", "start": starts[name], "end": round(starts[name] + dur[name], 2), "source": PV + f"{name}.png",
         "motion": SKETCH["push"], "captionY": cap, "breath": True, "previz": name}
    if name in ALIVE:
        s.update(source=KF + f"s{name}.png", breath=False, **ALIVE[name])
    if name == "1":
        s.update(source=PLATE + "plate-s1-nocrew.png", motion=CAM1,
                 hit={"at": 0, "strength": 2.6, "seconds": 0.9}, fx=[DUST1, FLASH1], breath=False,
                 # the crew at the back, the bar BEHIND Gage (it bursts out of the top of his head), the hat in front
                 layers={"bg": "proj:assets/images/refs/plate-s1-nocrew.png", "actors": [*CREW1, *TRAILS, IRON, GAGE1, HAT]})
    if name == "4":
        s.update(source=PLATE + "plate-s4.png", breath=False,
                 motion=PUSH4,
                 layers={"bg": "proj:assets/images/refs/plate-s4.png", "mg": [GAGE4]})
    if name == "8":
        s.update(source=PLATE + "plate-s8.png", breath=False,
                 motion={"type": "push", "from": 1.0, "to": 1.04, "x": 0, "y": 0}, fx=[SMOKE8],
                 layers={"bg": "proj:assets/images/refs/plate-s8.png", "mg": [GAGE8],
                         "glows": [{"x": 0.3, "y": 0.25, "r": 320, "strength": 0.22}]})   # glow on the plate's light shaft, upper left
    shots.append(s)

overlays = [
    {"kind": "nameTag", "start": starts["2a"] + 0.2, "end": starts["2a"] + 2.5, "text": "Phineas Gage", "sub": "railroad foreman, 25", "y": 1000},
    # the place stamp on 2b, the wide of the cut (rough cut 1: on 2a it sat on Gage's hat or under the caption, and
    # text_check's caption box leaves no room above his raised hand); 2b's caption is LOW
    {"kind": "stamp", "start": starts["2b"] + 0.1, "end": starts["2b"] + 2.3, "text": "CAVENDISH, VERMONT · 1848", "y": TOP},
    # the bar's length, BESIDE the bar (user 2026-11-19: less text; the weight stamp is gone, the caption says 13 POUNDS;
    # metric stays in the description). The bar runs up-left from the hole (x ~0.42): at y 640-760 it covers x ~330-440,
    # the stamp sits right of it, inside the safe zone (x 65-888), on the wall the hand has left
    {"kind": "stamp", "start": starts["3"] + IRON3_T + 0.1, "end": starts["3"] + TAMP3 + 1.0, "text": "3 ft 7 in", "y": 640, "x": 690, "size": 84},
    {"kind": "stamp", "start": starts["7"] + LANDED + 0.1, "end": starts["7"] + 1.9, "text": "≈ 80 ft (25 m)", "y": MID},
]
# rough cut 1: a stamp never outlives its shot (the real narration made shot 7 1.62 s: "≈ 80 FT" ran into shot 8's silence)
for o in overlays:
    sh = next(x for x in shots if x["start"] <= o["start"] < x["end"])
    o["start"], o["end"] = round(o["start"], 2), round(min(o["end"], sh["end"] - 0.05), 2)

# sound (storyboard SFX column; library names in channels/storybook-medical/library/sfx, new ones fetched by `episode.py sfx`)
S_ = lambda name, t, **k: {"name": name, "at": round(t, 2), **k}  # noqa: E731
SFX = [
    S_("whoosh", starts["1"] + 0.82, gain_db=-11),     # v3: on the whip up
    S_("metal-clank", starts["2a"] + 0.2, gain_db=-18), S_("crow-caw", starts["2a"] + 1.9, gain_db=-22),
    S_("metal-clank", starts["2b"] + 0.15, gain_db=-21), S_("metal-clank", starts["2b"] + 0.85, gain_db=-23),
    S_("sand-pour", starts["3"] + 0.05, gain_db=-18, dur=round(POUR_END + 0.3, 2), fade_out=0.25, query="sand pouring"),
    S_("stone-grind", starts["3"] + IRON3_T - 0.2, gain_db=-16, dur=0.5),
    S_("metal-clank", starts["3"] + TAMP3, gain_db=-16),
    S_("metal-clank", starts["5"] + STRUCK, gain_db=-12), S_("boom-low", starts["5"] + SPARK5, gain_db=-5),
    S_("quill-writing", starts["6"] + CHEEK - 0.3, gain_db=-20, dur=round(TOPW - CHEEK + 0.6, 2)),
    S_("whoosh", starts["7"], gain_db=-14), S_("stamp-thud", starts["7"] + LANDED, gain_db=-8),
    S_("ear-ring", starts["8"], gain_db=-22, dur=2.4, fade_out=0.8), S_("gasp", starts["8"] + SPOKE - 0.35, gain_db=-22),
    S_("horse-carriage", starts["9"], gain_db=-20, dur=2.6, fade_out=0.6),
    S_("cow-moo", starts["9"] + 1.1, gain_db=-22, query="cow moo"),
    S_("horse-carriage", starts["10"], gain_db=-18, dur=1.2, fade_out=0.5),
    S_("metal-ring", starts["11"] + KEPT, gain_db=-18, dur=0.9, fade_out=0.6, query="metal rod ring"),   # the file is 30 s of hits: one
    S_("whisper", starts["12"] + 0.2, gain_db=-16, dur=1.4, query="whisper"),
]

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"title": "He Took an Iron Bar Through the Skull… and Spoke", "format": "short", "loop": True, "tail_seconds": 1.0,
           # rough cut 1: every shot is real now, so the full motion lint runs (the pre-viz ran it as "warn")
           "motion_lint": "fail" if REAL else "warn",
           "previz": "rough cut 1 (real narration)" if REAL else "scratch timeline 2026-11-18; replace with the real narration", "shots": shots, "overlays": overlays,
           "sfx": SFX,
           # music prompts live in build_hc002s1.py; the music stops for shot 8's silence (cut -> just after "spoke")
           "music": {**ep.get("music", {}), "gaps": [{"from": starts["8"], "to": round(starts["8"] + SPOKE + 0.25, 2),
                                                     "fade_out": 0.3, "fade_in": 0.6}]},
           "packaging": {"version": 2, "case": 11, "hook": {"card": "An iron bar / through his *skull*.", "anchor": "top"}}})
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{'REAL' if REAL else 'SCRATCH'} timeline: {len(shots)} shots, {len(words)} words, {TOTAL_NARR} s; turn at {TURN} s in shot 4, 'spoke' at {SPOKE} s in shot 8")
