"""HCS09 rough cut (plan/production-v3.md §3): storyboard-v1 (script v2) as shots, overlays, SFX and music in
projects/hcs09-semmelweis/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (review/_grid.jpg, fractions of the source image).
    python channels/storybook-medical/editorial/episodes/HCS09-semmelweis/edit_hcs09.py
"""
import json
import re
from pathlib import Path

PID = "hcs09-semmelweis"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030   # caption tops inside the platform safe zone (y 288-1248; StorybookShort SAFE)
# STT spelling -> caption spelling (the doctors' ward; the mothers; Semmelweis's friend)
FIX = {"doctor's": "doctors'", "mother's.": "mothers.", "Semmelweis'": "Semmelweis's"}
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())


def push(cx=0.5, cy=0.5, to=1.18, frm=1.04):
    lim = (to - 1) / 2 * 100
    clamp = lambda v: max(-lim, min(lim, v))
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
# s1a: wet hands held out to the doctors (hands measured at 0.32, 0.52)
c.shot(0.0, KF + "s1a.png", push(0.38, 0.45, 1.12), cap=LOW)
c.o("stamp", 0.2, 2.8, text="VIENNA · 1847", y=TOP)
c.s("water-drip", c.at("wash"), query="water drop")
# s1b: the professor's scorn
t = c.at("they hated")
# user 2026-11-20 (L52): 1b and 2a share the corridor's camera (the professor vanished from the same hall). 1b is now a
# CU on his face over s1b-dof.png (dof1b_hcs09.py: the hall soft behind him), so 1b -> 2a cuts close -> wide.
# framed from frame 0 (push pans from the centre over the shot: on a x1.6 CU that read as a slide); only the zoom moves.
# Face in the top third, the LOW caption on his collar.
CU1B = {"x": -17.0, "y": 10.2}
c.shot(t, KF + "s1b-dof.png", {"type": "keys", "keys": [{"t": 0, "scale": 1.62, **CU1B}, {"t": 2.0, "scale": 1.7, "ease": "linear", **CU1B}]},
       cap=LOW)
c.s("hit-suspense", t)
# s2a: two wards (left door green at 0.40, 0.58; right door gold at 0.58, 0.58)
t = c.at("vienna had")
two = c.at("two maternity")
c.shot(t, KF + "s2a.png", {"type": "push", "from": 1.02, "to": 1.1, "x": 0, "y": -2}, cap=TOP,
       fx=[{"kind": "glow", "x": 0.40, "y": 0.58, "r": 0.05, "at": rel(two, t), "dur": 1.4, "color": "rgba(90,230,170,1)", "strength": 0.5},
           {"kind": "glow", "x": 0.58, "y": 0.58, "r": 0.05, "at": rel(two, t) + 0.3, "dur": 1.1, "color": "rgba(255,190,90,1)", "strength": 0.5}])
c.s("footsteps-hall", t, query="footsteps hallway")
# s2b: the doctors' ward
t = c.at("in the doctors")
one = c.at("one mother")
c.shot(t, KF + "s2b.png", push(0.5, 0.45, 1.1), cap=LOW)
c.o("stamp", one, one + 1.8, text="1 IN 10", y=TOP); c.s("stamp-thud", one + 0.05)
# s3a: the midwives' ward
t = c.at("in the midwives")
c.shot(t, KF + "s3a.png", push(0.4, 0.45, 1.12), cap=TOP)
c.s("chime-soft", t + 0.3)
# s3b: a woman begs at the door
t = c.at("women begged")
c.shot(t, KF + "s3b.png", push(0.45, 0.6, 1.1), cap=TOP)
# s4a: the scalpel (cut measured at 0.55, 0.50)
t = c.at("ignaz")
cut = c.at("cut")
c.shot(t, KF + "s4a.png", push(0.55, 0.5, 1.15), cap=TOP,
       fx=[{"kind": "spot", "cx": 0.55, "cy": 0.5, "rx": 0.07, "ry": 0.045, "at": rel(cut, t), "dur": 1.2, "dim": 0.5}])
c.s("tick-click", cut)
# s4b: Semmelweis at the empty bed
t = c.at("and died")
c.shot(t, KF + "s4b.png", push(0.62, 0.4, 1.12), cap=LOW)
c.o("nameTag", t + 0.05, t + 1.6, text="Ignaz Semmelweis", sub="doctor, Vienna", y=300)
# s5: from the dead to the mothers
t = c.at("the doctors went")
c.shot(t, KF + "s5.png", push(0.5, 0.55, 1.1), cap=TOP)
c.s("door-swing", t + 0.1)
# s6a: the students scrub (Matt's cameo)
t = c.at("so semmelweis")
c.shot(t, KF + "s6a.png", {"type": "slide", "from": -2, "to": 2, "scale": 1.08}, cap=TOP)
c.s("hands-washing", t + 0.2, query="hand washing")
# s6b: hands in the basin. Glint: user 2026-11-20 "check the glasses glint at 0:29": 0.55, 0.35 was the BRIDGE between the
# lenses; now on the right lens's painted highlight (measured on s6b.png: lens x 0.57-0.65, highlight 0.59, 0.34)
t = c.at("deaths fell")
hundred = c.at("one in 100")
# user 2026-11-20: the LOW captions covered the hands (they reached y ~1230 of the 1248 safe zone). The picture is raised
# (fixed-framing keys, x1.22 -> x1.24, up 11-12 %) so the hands end ~y 1035-1050 (captionY max 1038) and the captions sit under the fingertips;
# the 1 IN 100 stamp moves into the gap between Matt's glasses and the hands (it would land on the glasses at TOP).
c.shot(t, KF + "s6b.png", {"type": "keys", "keys": [{"t": 0, "scale": 1.22, "x": 0, "y": -11},
                                                    {"t": 3.0, "scale": 1.24, "x": 0, "y": -12, "ease": "linear"}]}, cap=1038,
       fx=[{"kind": "glint", "x": 0.59, "y": 0.34, "at": rel(hundred, t) + 0.8, "size": 26}])
c.o("stamp", hundred, hundred + 1.2, text="1 IN 100", y=520); c.s("stamp-thud", hundred + 0.05)
# s7a: the doctors refuse
t = c.at("but many")
c.shot(t, KF + "s7a.png", push(0.4, 0.4, 1.1), cap=TOP)
c.s("crowd-murmur", t)
# s7b: he leaves through the gate
t = c.at("he lost")
c.shot(t, KF + "s7b.png", {"type": "static"}, cap=TOP)
c.s("gate-clank", t + 0.2, query="iron gate closing clank"); c.s("wind-snow", t)
# s8: the asylum corridor
t = c.at("in 1865")
c.shot(t, KF + "s8.png", push(0.5, 0.5, 1.1), cap=LOW)
c.o("stamp", t + 0.2, t + 1.6, text="1865", y=TOP)
c.s("night-wind", t)
# s9: his face; the reflex gets its name
t = c.at("today")
reflex = c.at("the semmelweis")
c.shot(t, KF + "s9.png", push(0.5, 0.75, 1.12), cap=LOW)   # lift his face clear of the LOW caption
c.o("stamp", reflex, reflex + 2.0, text="SEMMELWEIS REFLEX", y=TOP); c.s("stamp-thud", reflex + 0.05)

HITS = {"stamp-thud", "tick-click", "door-swing", "gate-clank", "water-drip", "hit-suspense", "chime-soft"}
for cue in c.fx:
    cue["gain_db"] = -8 if cue["name"] in HITS else -15

TAIL = 1.0
total = round(c.words[-1]["end"] + 0.8 + TAIL, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"loop": True, "tail_seconds": TAIL, "shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]),
           "sfx": sorted(c.fx, key=lambda x: x["at"]), "glasses": "s6b: Matt's spectacles on the chlorine basin's rim"})
ep["theme"] = {"culture": "vienna-1840s", "font": "montserrat"}
ep["music"] = {"lufs": -22, "selected": "m2", "prompts": {
    # m1 came back 410 s WITH VOCALS; m2: instrumental-only wording first, 3 sections
    "m2": {"sections": 3, "prompt": "Purely instrumental, no voice, no choir, no singing. 1840s Vienna chamber score for a tragic true story: a string quartet in a minor key, "
          "Schubert-like, a slow grave pulse with a faint Hungarian cimbalom colour, building tension in the middle, "
          "a lonely solo violin near the end, then a quiet unresolved close. No modern drums."}}}
# packaging v2 (plan/packaging-v2-spec.md, C006; built 2026-11-16): applied at build time by scripts/packaging_v2.py
ep["packaging"] = {
 "version": 2,
 "case": 10,
 # v2.1 (C006 v2.1, approved 2026-11-17): card "doctors' HANDS / killing mothers?" (cadaverous particles on the doctors'
 # hands, deaths fell after washing: VERIFIED S1; a question). Bottom: a top card would sit on the doctors' faces.
 # No pause after 1.8 s: hold to "doctors" (captions "doctors to wash their hands", as approved), not the 2.5 s cap.
 "hook": {"card": "doctors' *hands* / killing mothers?", "anchor": "bottom",
          "until": next(round(w["start"], 2) for w in c.words if norm(w["word"]) == "doctors")},
 "frame1": {
  "motion": {
   "type": "snap",
   # 1.22+: y -10 needs >= 10% spare per side; at 1.10 it showed a black band at the bottom (rule: no black frames)
   "from": 1.22,
   "to": 1.28,
   "at": 0,
   "frames": 40,
   "x0": 4,
   "y0": -10,
   "x": 6,
   "y": -10
  },
  "fx": [
   {
    "kind": "particles",
    "style": "bubbles",
    # user 2026-11-20: the bubbles sat on his right WRIST (0.40) and fell to the basin rim; the lather is on the palms
    # between his hands (measured on s1a.png: palms x 0.24-0.33, y 0.51-0.53): born there, floating a little up
    "x": 0.285,
    "y": 0.523,
    "tx": 0.28,
    "ty": 0.505,
    "spread": 0.035,
    "every": 0.12,
    "life": 0.5,
    "size": 9,
    "opacity": 0.85
   }
  ]
 },
 "sfx": [
  {
   "name": "hands-washing",
   "at": 0.05,
   "gain_db": -12,
   "dur": 3.0,
   "fade_out": 0.6
  }
 ]
}
ep["motion_lint"] = "warn"   # cut before Rule 0; v2 changes only the opening
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
