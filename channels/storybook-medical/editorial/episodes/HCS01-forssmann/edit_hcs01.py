"""HCS01 rough cut (plan/production-v3.md §3): storyboard-v3 / storybook_hcs01.py as shots, overlays, SFX and music in
projects/hcs01-forssmann/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
Not in the rough cut yet (need masks): the highlight on Forssmann (s2, s5), the nurse dimmed (s5), the key-ring swing
(s4), the chart vein glow (s2), 2.5D depth parallax (s2, s7; plain camera moves stand in).
    python channels/storybook-medical/editorial/episodes/HCS01-forssmann/edit_hcs01.py
"""
import json
import re
from pathlib import Path

PID = "hcs01-forssmann"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 1180, 1430                 # caption tops (StorybookShort)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

# measured on the frames with a grid and checked with a marker overlay (memory: effects-on-exact-object)
VEIN = [[0.80, 0.63], [0.787, 0.56], [0.767, 0.49], [0.747, 0.43], [0.727, 0.39], [0.69, 0.36], [0.64, 0.346],
        [0.59, 0.347], [0.555, 0.362], [0.535, 0.392], [0.515, 0.44]]                     # s1b: elbow -> heart
FILM = [[0.765, 0.57], [0.75, 0.47], [0.74, 0.40], [0.71, 0.36], [0.65, 0.355], [0.58, 0.365], [0.53, 0.38],
        [0.48, 0.41], [0.465, 0.45], [0.46, 0.49]]                                          # s8a: left arm -> heart


def push(cx=0.5, cy=0.5, to=1.18, frm=1.04):
    """Push toward (cx, cy) of the frame: the end translate puts that point at the centre, clamped so no edge shows."""
    lim = (to - 1) / 2 * 100
    clamp = lambda v: max(-lim, min(lim, v))
    return {"type": "push", "from": frm, "to": to, "x": round(clamp(-(cx - 0.5) * to * 100), 2),
            "y": round(clamp(-(cy - 0.5) * to * 100), 2)}


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

    def end(self, phrase):
        want = [norm(x) for x in phrase.split()]
        for i in range(len(self.toks) - len(want) + 1):
            if self.toks[i:i + len(want)] == want:
                return round(self.words[i + len(want) - 1]["end"], 2)
        raise SystemExit(f"phrase not found: {phrase!r}")

    def shot(self, t, source, motion, cap=MID, **kw):
        self.shots.append({"id": f"s{len(self.shots) + 1:02d}", "start": max(0.0, round(t - 0.05, 2)), "source": source,
                           "motion": motion, "captionY": cap, **kw})

    def o(self, kind, start, end, **kw):
        self.ov.append({"kind": kind, "start": round(start, 2), "end": round(end, 2), **kw})

    def s(self, name, t, gain=-14, **kw):
        self.fx.append({"name": name, "at": round(t, 2), "gain_db": gain, **kw})


c = Cut()
c.shot(0.0, KF + "s1a.png", push(0.45, 0.62, 1.25), cap=TOP)
t = c.at("through his own arm")
heart = c.at("heart")
c.shot(t, KF + "s1b.png", push(0.6, 0.45, 1.15), cap=LOW,
       draw=[{"points": VEIN, "from": 0.3, "to": round(heart - t + 0.15, 2), "color": "#F0A23A", "width": 16}])
c.s("whoosh", t + 0.35, -24); c.s("heartbeat", heart + 0.1, -12)
t = c.at("werner")
c.shot(t, KF + "s2.png", {"type": "slide", "from": -3, "to": 3, "scale": 1.1}, cap=LOW)
c.o("nameTag", t + 0.2, t + 2.8, text="Werner Forssmann", sub="trainee surgeon · 1929", y=190)
t = c.at("his boss said no")
no = c.at("no")
c.shot(t, KF + "s3.png", {"type": "push", "from": 1.04, "to": 1.06}, cap=LOW)
c.shot(no, KF + "s3.png", push(0.5, 0.38, 1.16, 1.08), cap=LOW)          # the quick push on "no"
c.shot(c.at("the nurse"), KF + "s4.png", push(0.33, 0.5, 1.4), cap=LOW)
c.s("key-lock", c.at("her") + 0.1, -20)
c.shot(c.at("he tricked her"), KF + "s5.png", push(0.6, 0.52, 1.3), cap=TOP)
c.shot(c.at("he slid the catheter"), KF + "s6a.png", push(0.35, 0.72, 1.3), cap=TOP)
t = c.at("65")
c.shot(t, KF + "s6b.png", {"type": "slide", "from": 3, "to": -3, "scale": 1.12}, cap=LOW)
c.o("stamp", t + 0.2, t + 1.7, text="65 cm", y=1000); c.s("stamp-thud", t + 0.25, -14)
c.shot(c.at("then he walked"), KF + "s7.png", {"type": "pull", "from": 1.4, "to": 1.04}, cap=TOP)
t = c.at("the picture showed")
tip = c.at("tip")
c.shot(t, KF + "s8a.png", push(0.5, 0.45, 1.25), cap=TOP,
       draw=[{"points": FILM, "from": 0.15, "to": round(tip - t + 0.25, 2), "color": "#FFFFFF", "width": 9}])
c.s("riser-drone", t, -26)
c.shot(c.at("inside his heart"), KF + "s8b.png", push(0.3, 0.42, 1.35), cap=LOW)   # mirrored frame: he stands on the left
t = c.at("his reward")
fired = c.at("fired")
c.shot(t, KF + "s9.png", {"type": "static"}, cap=LOW)     # TOP covered the letterhead
c.o("stamp", fired, fired + 1.6, text="FIRED", y=760); c.s("stamp-thud", fired + 0.05, -12)
t = c.at("27 years later")
c.shot(t, KF + "s10a.png", push(0.55, 0.3, 1.3), cap=LOW); c.s("paper-slide", t, -20)
t = c.at("nobel prize")
c.shot(t - 0.3, f"projects/{PID}/assets/video/medal.mp4", {"type": "static"}, cap=LOW, **{"in": 0.27})
c.s("ding-correct", t + 0.05, -20)
t = c.at("but in 1932")
y32 = c.at("1932")
c.shot(t, KF + "s11.png", {"type": "pull", "from": 1.15, "to": 1.03}, cap=LOW, transition="dissolve",
       grey={"from": 0.2, "to": 2.0})
c.o("stamp", y32 + 0.1, y32 + 2.4, text="1932", y=1230); c.s("stamp-thud", y32 + 0.15, -16)

total = round(c.words[-1]["end"] + 0.8, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]), "sfx": sorted(c.fx, key=lambda x: x["at"]),
           "glasses": "s2: Matt's spectacles on the windowsill by the geranium"})
ep["music"] = {"lufs": -22, "selected": ep.get("music", {}).get("selected") or "m2", "prompts": {
    "m1": "Instrumental, 1920s chamber music with a mischievous, curious mood: pizzicato strings, a bassoon and clarinet, "
          "light brushed percussion like a ticking clock, building tension in the middle, then a warm brass swell of "
          "triumph near the end and a quiet, solemn close. No vocals.",
    "m2": "Instrumental, playful suspense score for a true story told like a storybook: plucked cello, celesta, soft "
          "muted trumpet, a steady ticking pulse that grows, a short bright fanfare, then a sombre low piano ending. "
          "No vocals."}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
