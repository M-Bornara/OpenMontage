"""HCS07 cut v2 (story-v2.md, storyboard-v2.md; rough cut 1 in projects/hcs07-finlay/rough-cut-1): shots, overlays, SFX and music in
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
# ── v2 cut (story-v2.md rhythm map, 2026-11-15) ───────────────────────────────────────────────────────────────────────
MOSQ_S1C = (0.55, 0.55)        # s1c mosquito on the forearm (measured)
# B1 HOOK: the mosquito lands (snap zoom on "yellow fever"), then nineteen years of jars
yf = c.at("yellow fever")
c.shot(0.0, KF + "s1c.png", {"type": "snap", "from": 1.03, "to": 1.3, "at": round(yf - 0.05, 2),
       "x": round(-(MOSQ_S1C[0] - 0.5) * 30, 2), "y": round(-(MOSQ_S1C[1] - 0.5) * 30, 2)}, cap=TOP)
c.s("mosquito-buzz", 0.0, query="mosquito buzzing"); c.s("hit-suspense", yf)
t = c.at("then spent")
c.shot(t, KF + "s5.png", push(0.5, 0.42, 1.12), cap=870,   # text check: TOP/MID covered the jar, LOW the glasses gag: the strip between
       fx=[{"kind": "glint", "x": 0.41, "y": 0.58, "at": 1.6, "size": 26}])
# (no "19 YEARS" stamp: it covered the glasses gag, and Liam says it)
c.s("watch-ticking", t)
# B2 STAKES: Havana 1881, then the epidemic at a door
t = c.at("havana")
c.shot(t, KF + "s2a.png", {"type": "pull", "from": 1.16, "to": 1.03}, cap=LOW)
c.o("stamp", t + 0.1, t + 1.6, text="HAVANA · 1881", y=TOP)
c.s("gulls-water", t); c.s("ship-bell", t + 0.3)
t = c.at("yellow fever was killing")
c.shot(t, KF + "s2c.png", {"type": "slide", "from": 3, "to": -3, "scale": 1.12}, cap=TOP)
c.s("horse-carriage", t, query="horse carriage cobblestones")
# B3: the suspect on his hand (mosquito measured at 0.66, 0.56); name tag below it
t = c.at("dr")
mosq = c.at("the mosquito")
c.shot(t, KF + "s3.png", push(0.58, 0.47, 1.14), cap=TOP,
       fx=[{"kind": "spot", "cx": 0.66, "cy": 0.56, "rx": 0.08, "ry": 0.05, "at": rel(mosq, t), "dur": 1.6, "dim": 0.5}])
c.o("nameTag", t + 0.05, mosq - 0.2, text="Carlos Finlay", sub="doctor, Havana", y=1000)
c.s("mosquito-buzz", t, query="mosquito buzzing"); c.s("hit-suspense", mosq)
# B4 ESCALATION: the Academy, the disbelief (whip), he keeps going (snaps), the years tick, Reed arrives
t = c.at("he told the academy")
c.shot(t, KF + "s4a.png", push(0.5, 0.5, 1.12), cap=TOP)
c.s("footsteps-hall", t)
t = c.at("almost nobody")
c.shot(t, KF + "s4b.png", push(0.5, 0.6, 1.1), cap=TOP, transition="whip")
c.s("whoosh", t - 0.05); c.s("crowd-murmur", t + 0.1)
t = c.at("so he kept going")
c.shot(t, KF + "s5b.png", {"type": "snap", "from": 1.03, "to": 1.16, "at": 0.0, "frames": 5}, cap=TOP)  # LOW crossed the pitcher
c.s("water-drip", t + 0.2)
t = c.at("testing")
c.shot(t, KF + "s1b.png", {"type": "snap", "from": 1.05, "to": 1.22, "at": 0.0, "frames": 5, "x": 3, "y": 3}, cap=TOP)
# (no 1885/1890/1895 stamps: they sat on the jar in front of his face; LOW crossed his moustache. Text check 2026-11-15)
c.s("watch-ticking", t)
t6a = t = c.at("then in 1900")
reed = c.at("walter reed")
c.shot(t, KF + "s6a.png", {"type": "slide", "from": -3, "to": 3, "scale": 1.12}, cap=LOW)
c.s("bugle-call", t); c.s("gulls-water", t + 0.2)
t = c.at("finally tested")
c.o("nameTag", t6a + 0.4, t - 0.15, text="Walter Reed", sub="US Army doctor", y=TOP)  # the whole shot (user: "gone before can read"); no "1900" stamp (Liam says it)
mosq = c.at("finlays own mosquitoes")
c.shot(t, KF + "s6b.png", push(0.53, 0.49, 1.18), cap=TOP,
       fx=[{"kind": "glint", "x": 0.53, "y": 0.49, "at": rel(mosq, t), "size": 30}])
c.s("glass-clink", mosq)
# B5 CLIMAX: bitten... and died (music silent from the pause to the turn)
t = c.at("one of them")
c.shot(t, KF + "s7a.png", {"type": "push", "from": 1.04, "to": 1.1, "x": 0, "y": 0}, cap=TOP)
bit = c.at("was bitten")
c.s("mosquito-buzz", bit, query="mosquito buzzing")
died = c.at("and died")
c.shot(died, KF + "s7b.png", {"type": "push", "from": 1.02, "to": 1.05}, cap=TOP)
c.s("night-wind", died - 0.2)
# B6 TWIST: the killer (hit + stamp), right all along
turn = t = c.at("the mosquito was")
c.shot(t, KF + "s8a.png", push(0.5, 0.48, 1.12), cap=LOW, hit={"at": 0.5, "strength": 3})
c.o("stamp", t + 0.5, t + 1.7, text="DOCUMENTED", y=TOP)
c.s("stamp-thud", t + 0.5)
t = c.at("finlay had been")
c.shot(t, KF + "s8b.png", push(0.45, 0.4, 1.1), cap=LOW)
c.s("paper-slide", t)
# B7: the fame, and the credit (name measured at 0.58, 0.47)
t = c.at("reed got most")
c.shot(t, KF + "s9a.png", push(0.6, 0.4, 1.1), cap=LOW)
c.s("applause", t); c.s("whoosh", t + 0.3)
t = c.at("but reed himself")
fin = c.at("to finlay")
c.shot(t, KF + "s9b.png", push(0.58, 0.47, 1.18), cap=TOP,
       fx=[{"kind": "glow", "x": 0.58, "y": 0.47, "r": 0.1, "at": rel(fin, t), "dur": 2.5, "color": "rgba(255,200,90,1)",
            "strength": 0.5}])
c.s("quill-writing", t)
MUSIC_GAPS = [{"from": round(died - 0.85, 2), "to": round(turn - 0.1, 2), "fade_out": 0.35, "fade_in": 0.1}]

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
ep["music"] = {"lufs": -22, "selected": "m1", "gaps": MUSIC_GAPS, "prompts": {
    "m1": {"sections": 3, "prompt": "Instrumental, 1880s Havana, Cuba: a slow Cuban habanera in a minor key for a true story "
           "about a patient doctor nobody believed. Solo piano playing the habanera rhythm, a tres guitar melody, soft guiro "
           "and claves; curious and warm, a hopeful lift near the end, then a gentle resolving close. No vocals, no modern "
           "drums, no synths."}}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
