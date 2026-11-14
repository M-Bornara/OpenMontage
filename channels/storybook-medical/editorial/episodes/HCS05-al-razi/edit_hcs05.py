"""HCS05 rough cut (plan/production-v3.md §3): storyboard v1.1 as shots, overlays, SFX and music in
projects/hcs05-al-razi/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (projects/hcs05-al-razi/review/_grid.jpg, fractions of the source image).
Captions never sit on a face or on an FX target.
    python channels/storybook-medical/editorial/episodes/HCS05-al-razi/edit_hcs05.py
"""
import json
import re
from pathlib import Path

PID = "hcs05-al-razi"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030
FIX = {"Ray,": "Rey,", "Ray": "Rey"}   # STT heard the city as "Ray"
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())  # noqa: E731


def push(cx=0.5, cy=0.5, to=1.15, frm=1.03):
    lim = (to - 1) / 2 * 100
    clamp = lambda v: max(-lim, min(lim, v))  # noqa: E731
    return {"type": "push", "from": frm, "to": to, "x": round(clamp(-(cx - 0.5) * to * 100), 2),
            "y": round(clamp(-(cy - 0.5) * to * 100), 2)}


def rel(word_t, shot_t):
    return round(word_t - (shot_t - 0.05), 2)


class Cut:
    def __init__(self):
        f = P / "artifacts/word_timestamps.json"
        self.words = json.load(open(f, encoding="utf-8"))
        for w in self.words:
            w["word"] = FIX.get(w["word"], w["word"])
        json.dump(self.words, open(f, "w", encoding="utf-8"), indent=1)
        self.toks = [norm(w["word"]) for w in self.words]
        self.cur, self.shots, self.ov, self.fx = 0, [], [], []

    def at(self, phrase, word=0):
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
# 1a: he stops the assistant
c.shot(0.0, KF + "s1a.png", push(0.6, 0.45, 1.12), cap=LOW)
c.o("stamp", 0.2, 2.4, text="c. 900 AD", y=TOP)
c.s("fire-crackle", 0.0)
# 1b: on purpose (face in the upper half: caption LOW on the robe)
t = c.at("on purpose")
c.shot(t, KF + "s1b.png", push(0.5, 0.35, 1.1), cap=TOP)  # cut 1: LOW crossed his beard
c.s("hit-suspense", t)
# 2: Rey under Damavand
t = c.at("al-razi was")
rey = c.at("rey")
c.shot(t, KF + "s2.png", {"type": "pull", "from": 1.16, "to": 1.03}, cap=LOW)
c.o("nameTag", t, rey - 0.1, text="al-Razi", sub="Persian physician", y=MID)
c.o("location", rey, rey + 2.0, text="REY", sub="near today's Tehran", y=TOP)
c.s("desert-wind", t)
# 3: meningitis and the treatment waiting (lancet measured at 0.64, 0.78; faces ~0.45-0.5: caption TOP)
t = c.at("for the first signs")
blood = c.at("bloodletting")
c.shot(t, KF + "s3.png", push(0.55, 0.6, 1.12), cap=TOP,
       fx=[{"kind": "glint", "x": 0.64, "y": 0.78, "at": rel(blood, t), "size": 26}])
c.s("water-drip", t)
# 4: he doubts it
t = c.at("al-razi wasnt sure")
c.shot(t, KF + "s4.png", push(0.6, 0.3, 1.12), cap=LOW)
c.s("quill-writing", t)
# 5: two groups (rows measured: A centre x 0.27, B centre x 0.72)
t = c.at("so he bled")
a = c.at("one group")
b = c.at("another group")
c.shot(t, KF + "s5.png", {"type": "static"}, cap=LOW,
       fx=[{"kind": "spot", "cx": 0.27, "cy": 0.45, "rx": 0.16, "ry": 0.42, "at": rel(a, t), "dur": 1.6, "dim": 0.5},
           {"kind": "spot", "cx": 0.72, "cy": 0.45, "rx": 0.16, "ry": 0.42, "at": rel(b, t), "dur": 1.6, "dim": 0.5}])
c.o("stamp", a, b + 1.2, text="A", y=MID, x=290)
c.o("stamp", b, b + 1.2, text="B", y=MID, x=780)
c.s("cloth-rustle", t); c.s("stamp-thud", a); c.s("stamp-thud", b)
# 6: he watches (Matt's cameo; heads at 0.5-0.62: caption TOP)
t = c.at("then he watched")
c.shot(t, KF + "s6.png", push(0.5, 0.55, 1.1), cap=TOP)
c.s("crickets-field", t, query="crickets chirping field night quiet")  # v1 pick had traffic + a car
# 7a: his notes (glasses measured at 0.55, 0.20: stamp MID, caption LOW)
t = c.at("the bled group")
c.shot(t, KF + "s7a.png", push(0.55, 0.45, 1.12), cap=LOW,
       fx=[{"kind": "glint", "x": 0.55, "y": 0.20, "at": 1.2, "size": 24}])
c.o("stamp", c.at("giant medical"), t + 3.6, text="HIS NOTES → KITAB AL-HAWI", y=MID)
c.s("quill-writing", t)
# 7b: he keeps the treatment
t = c.at("so he kept")
c.shot(t, KF + "s7b.png", push(0.5, 0.6, 1.12), cap=TOP)
c.s("metal-clank", t + 0.3, query="small metal bowl set down")
# 8: wrong (bowl at 0.52: stamp MID, caption TOP); colour drains
t = c.at("he was wrong")
c.shot(t, KF + "s8.png", push(0.48, 0.52, 1.1), cap=TOP,
       fx=[{"kind": "tint", "at": 0.2, "dur": 0.8, "from": "rgba(128,128,128,0)", "to": "rgba(128,128,128,0.6)",
            "blend": "saturation"}])
c.o("stamp", t + 0.25, t + 1.6, text="WRONG", y=MID)
c.s("buzzer-wrong", t + 0.25)
# 9a: the museum card
t = c.at("some call it")
nq = c.at("not quite")
c.shot(t, KF + "s9a.png", push(0.47, 0.6, 1.15), cap=TOP)
c.o("stamp", nq, nq + 1.3, text="OVERSTATEMENT", y=MID)
c.s("footsteps-hall", t); c.s("stamp-thud", nq)
# 9b: two groups today (bottle groups measured at x 0.35 and 0.67, y 0.53: letters above them)
t = c.at("but comparing")
c.shot(t, KF + "s9b.png", push(0.5, 0.5, 1.08), cap=TOP)
c.o("stamp", t + 0.3, t + 3.5, text="A", y=780, x=378)
c.o("stamp", t + 0.5, t + 3.5, text="B", y=780, x=724)
c.s("glass-clink", t + 0.3)

HITS = {"stamp-thud", "glass-clink", "hit-suspense", "quill-writing", "metal-clank", "buzzer-wrong"}
for cue in c.fx:
    cue["gain_db"] = -8 if cue["name"] in HITS else -15

TAIL = 1.0
total = round(c.words[-1]["end"] + 0.8 + TAIL, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"loop": True, "tail_seconds": TAIL, "shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]),
           "sfx": sorted(c.fx, key=lambda x: x["at"])})
ep["music"] = {"lufs": -22, "selected": "m1", "prompts": {
    "m1": {"sections": 3, "prompt": "Instrumental Persian classical music in dastgah Shur for a true story about a "
           "10th-century physician: santur and setar, a breathy ney flute, soft daf and tombak; curious and careful, a "
           "playful, slightly mischievous turn near the end, then a calm close. No Western orchestra, no vocals, no "
           "modern drums, no synths."}}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
