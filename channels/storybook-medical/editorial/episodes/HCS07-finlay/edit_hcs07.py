"""HCS07 rough cut (plan/production-v3.md §3): storyboard v1.1 as shots, overlays, SFX and music in
projects/hcs07-finlay/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (projects/hcs05-al-razi/review/_grid.jpg, fractions of the source image).
Captions never sit on a face or on an FX target (L: shorts-safe-zone).
    python channels/storybook-medical/editorial/episodes/HCS07-finlay/edit_hcs07.py
"""
import json
import re
from pathlib import Path

PID = "hcs07-finlay"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030
FIX = {}
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
# 1a: the doubters
c.shot(0.0, KF + "s1a.png", push(0.5, 0.55, 1.12), cap=LOW)
c.o("stamp", 0.25, 2.3, text="19 YEARS", y=TOP)
c.s("crowd-murmur", 0.0)
# 1b: the mosquito in the jar
t = c.at("the man who")
c.shot(t, KF + "s1b.png", push(0.42, 0.42, 1.18), cap=TOP)  # cut 1: LOW covered the mosquito
c.s("mosquito-buzz", t, query="mosquito buzzing")
# 2a: Havana harbour
t = c.at("havana")
c.shot(t, KF + "s2a.png", {"type": "pull", "from": 1.16, "to": 1.03}, cap=LOW)
c.o("stamp", t + 0.1, t + 2.0, text="HAVANA · 1881", y=TOP)
c.s("gulls-water", t); c.s("ship-bell", t + 0.4)
# 2b: the wary street
t = c.at("yellow fever was")
c.shot(t, KF + "s2b.png", push(0.4, 0.55, 1.1), cap=LOW)
c.s("horse-carriage", t, query="horse carriage cobblestones")
# 3: the idea on his hand (mosquito measured at 0.66, 0.56; face 0.5, 0.38): caption TOP, name tag below the mosquito
t = c.at("dr carlos finlay")
mosq = c.at("mosquito")
c.shot(t, KF + "s3.png", push(0.58, 0.47, 1.14), cap=TOP,
       fx=[{"kind": "spot", "cx": 0.66, "cy": 0.56, "rx": 0.08, "ry": 0.05, "at": rel(mosq, t), "dur": 1.8, "dim": 0.5}])
c.o("nameTag", t + 0.05, t + 2.2, text="Carlos Finlay", sub="doctor, Havana", y=1000)  # ends before the mosquito spot
c.s("hit-suspense", mosq)
# 4a: the Academy
t = c.at("he told the academy")
c.shot(t, KF + "s4a.png", push(0.5, 0.5, 1.12), cap=TOP)  # cut 1: stamp doubled the caption; LOW sat on Finlay
c.s("footsteps-hall", t)
# 4b: disbelief (faces at y 0.4-0.55: caption TOP)
t = c.at("the reaction")
c.shot(t, KF + "s4b.png", push(0.5, 0.48, 1.1), cap=TOP)
c.s("crowd-murmur", t + 0.3)
# 5: nineteen years of jars (glasses measured at 0.41, 0.58: caption MID, clear of the glasses)
t = c.at("for 19 years")
c.shot(t, KF + "s5.png", push(0.5, 0.42, 1.12), cap=TOP,   # cut 1: MID covered the jar he lifts
       fx=[{"kind": "glint", "x": 0.41, "y": 0.58, "at": 2.9, "size": 26}])
c.o("stamp", t + 0.2, t + 2.6, text="1881 → 1900", y=980)
c.s("watch-ticking", t)
# 6a: the army camp (heads around y 0.57: caption MID)
t = c.at("in 1900")
reed = c.at("walter reed")
c.shot(t, KF + "s6a.png", push(0.5, 0.6, 1.12), cap=MID)
c.o("stamp", t + 0.1, reed - 0.15, text="1900", y=TOP)
c.o("nameTag", reed, reed + 2.0, text="Walter Reed", sub="US Army doctor", y=TOP)
c.s("bugle-call", t)
# 6b: the handover (tube measured at 0.53, 0.49: caption TOP)
t = c.at("and finally tested")
mosq = c.at("finlays mosquitoes")
c.shot(t, KF + "s6b.png", push(0.53, 0.49, 1.18), cap=TOP,
       fx=[{"kind": "glint", "x": 0.53, "y": 0.49, "at": rel(mosq, t), "size": 30}])
c.s("glass-clink", mosq)
# 7a: Lazear at work
t = c.at("one of the team")
c.shot(t, KF + "s7a.png", push(0.45, 0.45, 1.12), cap=TOP)  # cut 1: MID sat on his head; name is spoken
c.s("mosquito-buzz", c.at("was bitten"), query="mosquito buzzing")
# 7b: the empty cot (cot at y 0.55-0.65: caption TOP)
t = c.at("and died")
c.shot(t, KF + "s7b.png", {"type": "push", "from": 1.02, "to": 1.08}, cap=TOP)
c.s("night-wind", t)
# 8a: the carrier
t = c.at("the mosquito was")
c.shot(t, KF + "s8a.png", push(0.5, 0.48, 1.12), cap=LOW)
c.o("stamp", t + 0.5, t + 1.8, text="DOCUMENTED", y=TOP)
c.s("mosquito-buzz", t, query="mosquito buzzing"); c.s("stamp-thud", t + 0.55)
# 8b: right all along
t = c.at("finlay had been")
c.shot(t, KF + "s8b.png", push(0.45, 0.4, 1.1), cap=LOW)
c.s("paper-slide", t)
# 9a: the fame
t = c.at("reed got most")
c.shot(t, KF + "s9a.png", push(0.6, 0.4, 1.1), cap=LOW)
c.s("applause", t); c.s("whoosh", t + 0.3)
# 9b: the credit (name measured at 0.58, 0.47: caption TOP)
t = c.at("but reed himself")
fin = c.at("to finlay")
c.shot(t, KF + "s9b.png", push(0.58, 0.47, 1.18), cap=TOP,
       fx=[{"kind": "glow", "x": 0.58, "y": 0.47, "r": 0.1, "at": rel(fin, t), "dur": 2.5, "color": "rgba(255,200,90,1)",
            "strength": 0.5}])
c.s("quill-writing", t)

HITS = {"stamp-thud", "glass-clink", "ship-bell", "hit-suspense", "whoosh", "quill-writing", "paper-slide", "bugle-call"}
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
    "m1": {"sections": 3, "prompt": "Instrumental, 1880s Havana, Cuba: a slow Cuban habanera in a minor key for a true story "
           "about a patient doctor nobody believed. Solo piano playing the habanera rhythm, a tres guitar melody, soft guiro "
           "and claves; curious and warm, a hopeful lift near the end, then a gentle resolving close. No vocals, no modern "
           "drums, no synths."}}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
