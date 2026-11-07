"""HCS02 rough cut (plan/production-v3.md §3): storyboard-v1 as shots, overlays, SFX and music in
projects/hcs02-marshall/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
Not in the rough cut yet (need masks): the wiggling spirals (s2b), the wagging tail (s5a), the green haze (s6), the pill
bottle shake (s8), the phone handset rattle (s3), 2.5D parallax on s2a (a slide stands in).
    python channels/storybook-medical/editorial/episodes/HCS02-marshall/edit_hcs02.py
"""
import json
import re
from pathlib import Path

PID = "hcs02-marshall"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 1180, 1430                 # caption tops (StorybookShort)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())


def push(cx=0.5, cy=0.5, to=1.18, frm=1.04):
    """Push toward (cx, cy) of the frame: the end translate puts that point at the centre, clamped so no edge shows."""
    lim = (to - 1) / 2 * 100
    clamp = lambda v: max(-lim, min(lim, v))
    return {"type": "push", "from": frm, "to": to, "x": round(clamp(-(cx - 0.5) * to * 100), 2),
            "y": round(clamp(-(cy - 0.5) * to * 100), 2)}


def rel(word_t, shot_t):
    """A word's time in seconds after the shot starts (Cut.shot starts each shot 0.05 s before its first word)."""
    return round(word_t - (shot_t - 0.05), 2)


class Cut:
    def __init__(self):
        self.words = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
        self.toks = [norm(w["word"]) for w in self.words]
        self.cur, self.shots, self.ov, self.fx = 0, [], [], []

    def at(self, phrase, word=0):
        """Start of the phrase (or of its word-th word), searching forward from the last match."""
        want = [norm(x) for x in phrase.split()]
        for i in range(self.cur, len(self.toks) - len(want) + 1):
            if self.toks[i:i + len(want)] == want:
                self.cur = i + 1
                return round(self.words[i + word]["start"], 2)
        raise SystemExit(f"phrase not found: {phrase!r}")

    def shot(self, t, source, motion, cap=MID, **kw):
        self.shots.append({"id": f"s{len(self.shots) + 1:02d}", "start": max(0.0, round(t - 0.05, 2)), "source": source,
                           "motion": motion, "captionY": cap, **kw})

    def o(self, kind, start, end, **kw):
        self.ov.append({"kind": kind, "start": round(start, 2), "end": round(end, 2), **kw})

    def s(self, name, t, gain=-14, **kw):
        self.fx.append({"name": name, "at": round(t, 2), "gain_db": gain, **kw})


c = Cut()
c.shot(0.0, KF + "s1.png", push(0.3, 0.25, 1.22), cap=LOW)            # the beaker, upper left
c.s("glass-clink", 0.4, -18)
t = c.at("barry marshall")
# FX: the brand "?" glint on Matt's spectacles on the reception counter (left lens, measured 0.666 / 0.689)
c.shot(t, KF + "s2a.png", {"type": "slide", "from": -3, "to": 3, "scale": 1.1}, cap=LOW,
       fx=[{"kind": "glint", "x": 0.671, "y": 0.689, "at": 1.1, "size": 30}])
c.o("nameTag", t + 0.2, t + 2.2, text="Barry Marshall", sub="young doctor · Perth, 1984", y=190)
t = c.at("and pathologist")
t2b = t
c.o("nameTag", c.at("robin warren") + 0.1, t + 3.0, text="Robin Warren", sub="pathologist", y=190)
spiral = c.at("spiral")
c.s("bubbles", spiral, -24)
# FX: the spirals wiggle from "spiral" on (the microscope circle, measured: centre 0.50/0.215, radius 0.33 of the width)
c.shot(t2b, KF + "s2b.png", push(0.45, 0.3, 1.15), cap=LOW,           # v2: up from Warren to the glowing circle
       fx=[{"kind": "wiggle", "cx": 0.50, "cy": 0.215, "rx": 0.31, "ry": 0.175, "strength": 14, "period": 2.2, "from": rel(spiral, t2b)}])
t = c.at("back then")
t3 = t
stress = c.at("stress")
# FX: the ringing phone IS the stress: its handset (fx_prep.py cut-out, clipped to its outline) rattles on its cradle
# with each ring (user review: the zigzag flash meant nothing)
RATTLE = {"kind": "shake", "mask": KF + "fx/s3-handset.mask.png", "bg": KF + "fx/s3-handset.clean.png", "hinge": [0.83, 0.628],
          "dur": 0.75, "deg": 4, "amp": 0.005}
c.shot(t3, KF + "s3.png", push(0.45, 0.55, 1.15), cap=TOP,
       fx=[{**RATTLE, "at": a} for a in (0.12, 0.82, 1.52)])             # through the 2 s ring burst
c.s("phone-ring-old", t + 0.1, -22, dur=2.0)
t = c.at("marshall said")
c.shot(t, KF + "s4.png", push(0.35, 0.5, 1.18), cap=LOW)              # v2 reverse angle: push down the tiers to him
c.s("kookaburra-laugh", c.at("believed"), -16)
t = c.at("the bacteria wouldnt")
# FX: the curly tail (fx_prep.py cut-out) wags over its clean plate, hinged where it meets the back
c.shot(t, KF + "s5a.png", push(0.6, 0.55, 1.2), cap=TOP,
       fx=[{"kind": "wag", "mask": KF + "fx/s5a-tail.mask.png", "bg": KF + "fx/s5a-tail.clean.png", "hinge": [0.237, 0.538],
            "deg": 14, "period": 0.45, "from": 0.2}])
c.s("pig-oink", c.at("pigs"), -16)
t = c.at("so he tested")
c.shot(t, KF + "s5b.png", push(0.5, 0.4, 1.12), cap=TOP)              # v2 close-up at night; LOW sat on the beaker
t = c.at("within days")
t6 = t
breath = c.at("breath")
# FX: a green haze drifts from him to the two colleagues on "breath" (along the painted haze, 0.20 -> 0.72)
c.shot(t6, KF + "s6.png", push(0.4, 0.55, 1.12), cap=TOP,             # v2 corridor: toward him on his chair
       fx=[{"kind": "particles", "style": "haze", "x": 0.21, "y": 0.47, "tx": 0.72, "ty": 0.43, "spread": 0.02, "size": 170,
            "every": 0.12, "life": 1.8, "from": rel(breath, t6) - 0.3, "opacity": 0.4}])
c.s("groan", t + 0.3, -18)
t = c.at("on day 10")
ten = c.at("10")
c.shot(t, KF + "s7.png", push(0.5, 0.45, 1.2), cap=LOW)               # v2: the view fills the frame
c.o("stamp", ten, ten + 1.8, text="DAY 10", y=1180); c.s("stamp-thud", ten + 0.05, -14)
t = c.at("his wife")
treat = c.at("treat")
# FX: the pill bottle (with her hand, fx_prep.py cut-out) gives one shake on "treat", pivoting at the wrist
c.shot(t, KF + "s8.png", push(0.5, 0.45, 1.1), cap=TOP,               # v2: pale him in front, her with the pills behind
       fx=[{"kind": "shake", "mask": KF + "fx/s8-bottle.mask.png", "bg": KF + "fx/s8-bottle.clean.png", "hinge": [0.56, 0.395],
            "at": rel(treat, t), "dur": 0.7, "deg": 9, "amp": 0.004}])
c.s("pill-bottle-rattle", treat, -16)
t = c.at("21 years later")
c.shot(t, KF + "s9a.png", {"type": "pull", "from": 1.3, "to": 1.04}, cap=LOW)
c.o("stamp", t + 0.3, t + 2.6, text="2005", y=300); c.s("applause", c.at("nobel"), -20)
t = c.at("and most ulcers")
c.shot(t, KF + "s9b.png", push(0.7, 0.35, 1.15), cap=LOW, transition="dissolve")   # v2: the cured patient
c.s("ding-correct", c.at("curable"), -20)

TAIL = 1.0                                       # user review: a breath after "curable" before the loop restarts
total = round(c.words[-1]["end"] + 0.8 + TAIL, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"loop": True, "tail_seconds": TAIL, "shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]), "sfx": sorted(c.fx, key=lambda x: x["at"]),
           "glasses": "s2a: Matt's spectacles on the reception counter behind the glass doors"})
ep["music"] = {"lufs": -22, "selected": "m1", "prompts": {
    "m1": "Instrumental, bright and cheeky 1980s-flavoured comedy score for a true science story: plucky marimba, "
          "pizzicato strings, a bouncy bass clarinet, light shaker percussion, a mischievous middle with a wobbly "
          "queasy trombone, then a warm triumphant brass swell near the end. No vocals."}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
