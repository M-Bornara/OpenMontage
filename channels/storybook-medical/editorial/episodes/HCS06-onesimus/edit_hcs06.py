"""HCS06 rough cut (plan/production-v3.md §3): storyboard-v1 (script v2) as shots, overlays, SFX and music in
projects/hcs06-onesimus/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (review/_grid.jpg, fractions of the source image).
Not in the rough cut yet: s1b as a true silhouette (a dark tint stands in; needs a figure mask), his name writing
itself in ink (s9; a stamp stands in), the quote in a period hand (s7; the captions carry it).
    python channels/storybook-medical/editorial/episodes/HCS06-onesimus/edit_hcs06.py
"""
import json
import re
from pathlib import Path

PID = "hcs06-onesimus"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030   # caption tops inside the platform safe zone (y 288-1248; StorybookShort SAFE)
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
        self.words = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
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
c.shot(0.0, KF + "s1a.png", {"type": "pull", "from": 1.18, "to": 1.04}, cap=LOW)
c.o("stamp", 0.2, 2.6, text="BOSTON · 1721", y=TOP)
c.s("ship-bell", 0.1, -20, query="ship bell harbor"); c.s("gulls-water", 0.0, -28)
t = c.at("the idea that saved")
# s1b: his face is held back until his name; a dark tint stands in for the silhouette
c.shot(t, KF + "s1b.png", push(0.55, 0.22, 1.15), cap=LOW,
       fx=[{"kind": "tint", "at": 0.0, "dur": 0.01, "from": "rgba(10,20,45,0.62)", "to": "rgba(10,20,45,0.62)", "blend": "multiply"}])
t = c.at("his name was")
one, mather = c.at("onesimus"), c.at("cotton mather")
c.shot(t, KF + "s2.png", {"type": "static"}, cap=LOW,
       fx=[{"kind": "spot", "cx": 0.79, "cy": 0.45, "rx": 0.11, "ry": 0.25, "at": rel(one, t), "dur": 1.8, "dim": 0.6},
           {"kind": "spot", "cx": 0.36, "cy": 0.48, "rx": 0.14, "ry": 0.16, "at": rel(mather, t), "dur": 1.8, "dim": 0.6},
           {"kind": "glint", "x": 0.285, "y": 0.648, "at": rel(mather, t) + 1.9, "size": 26}])
c.o("nameTag", one, one + 1.9, text="Onesimus", sub="enslaved in Boston", y=300)
c.o("nameTag", mather, mather + 2.0, text="Cotton Mather", sub="minister", y=300)
t = c.at("he had told")
c.shot(t, KF + "s3a.png", push(0.62, 0.28, 1.15), cap=LOW)
c.s("paper-slide", t + 0.1, -24)
t = c.at("a tiny cut")
matter = c.at("matter")
c.shot(t, KF + "s3b.png", push(0.45, 0.66, 1.15), cap=TOP,
       fx=[{"kind": "spot", "cx": 0.39, "cy": 0.65, "rx": 0.08, "ry": 0.045, "at": 0.15, "dur": 1.2, "dim": 0.45},
           {"kind": "spot", "cx": 0.73, "cy": 0.77, "rx": 0.13, "ry": 0.05, "at": rel(matter, t), "dur": 1.2, "dim": 0.45}])
t = c.at("then protection")
c.shot(t, KF + "s3c.png", {"type": "slide", "from": -3, "to": 3, "scale": 1.1}, cap=TOP)
c.s("children-laughing", t, -24, query="kids laughing playground")
t = c.at("only one doctor")
zab = c.at("zabdiel")
c.shot(t, KF + "s4.png", {"type": "static"}, cap=LOW,
       fx=[{"kind": "spot", "cx": 0.80, "cy": 0.46, "rx": 0.1, "ry": 0.23, "at": rel(zab, t), "dur": 2.0, "dim": 0.6}])
c.o("nameTag", zab, zab + 2.0, text="Zabdiel Boylston", sub="doctor", y=300)
c.s("chair-scrape", zab - 0.2, -20, query="wooden chair scrape floor")
t = c.at("he started")
c.shot(t, KF + "s5.png", push(0.6, 0.4, 1.15), cap=LOW)
c.o("stamp", t + 0.6, t + 2.6, text="26 JUNE 1721", y=TOP)
t = c.at("the town was furious")
c.shot(t, KF + "s6a.png", push(0.5, 0.55, 1.1), cap=TOP)
c.s("crowd-angry", t, -18, query="angry crowd shouting")
t = c.at("someone threw")
gren, out = c.at("grenade"), c.at("went out")
# s6b: the fuse's last ember glows, then dies on "went out"
c.shot(t, KF + "s6b.png", push(0.55, 0.57, 1.18), cap=TOP,
       fx=[{"kind": "glow", "x": 0.57, "y": 0.49, "r": 0.04, "at": 0.0, "dur": rel(out, t), "color": "rgba(255,90,30,1)", "strength": 0.6}])
c.s("glass-shatter", gren, -16, query="window glass shatter"); c.s("fizz", out - 0.1, -18)
c.o("stamp", t + 0.4, t + 2.2, text="3 A.M.", y=MID)
t = c.at("the note said")
c.shot(t, KF + "s7.png", push(0.6, 0.52, 1.15), cap=TOP)
c.s("paper-slide", t + 0.1, -22)
t = c.at("about one in seven")
c.shot(t, KF + "s8a.png", {"type": "static"}, cap=MID)
seven = c.at("seven")
boyl = c.at("of boylstons")
c.o("stamp", seven, boyl - 0.1, text="1 IN 7", y=TOP); c.s("night-wind", t, -26)
t = boyl
forty = c.at("40")
c.shot(t, KF + "s8b.png", push(0.45, 0.6, 1.12), cap=MID)
c.o("stamp", forty, forty + 1.6, text="1 IN 40", y=TOP); c.s("stamp-thud", forty + 0.05, -16)
c.s("children-laughing", t + 0.2, -28)
t = c.at("the idea came")
name = c.at("name")
c.shot(t, KF + "s9.png", push(0.5, 0.4, 1.1), cap=LOW)
c.o("stamp", name, name + 2.0, text="ONESIMUS", y=TOP); c.s("quill-writing", name, -20)

# user (rough cut 1): "no sound effect is clear". Each cue is peak-normalised to its gain, and at -20 to -28 dB they
# vanished under the voice (-14 LUFS). Levels by type: hits clearly audible, beds under the voice.
HITS = {"stamp-thud", "glass-shatter", "fizz", "chair-scrape", "paper-slide", "quill-writing", "tick-click", "chime-soft",
        "brush-sweep", "ship-bell"}
for cue in c.fx:
    cue["gain_db"] = -8 if cue["name"] in HITS else -15

TAIL = 1.0
total = round(c.words[-1]["end"] + 0.8 + TAIL, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"loop": True, "tail_seconds": TAIL, "shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]),
           "sfx": sorted(c.fx, key=lambda x: x["at"]), "glasses": "s2: Matt's spectacles on Mather's desk by the quill"})
# user (2026-11-09): IM Fell tried and dropped ("keep the original setup for the fonts"): channel Montserrat
ep["theme"] = {"culture": "colonial-english", "font": "montserrat"}
ep["music"] = {"lufs": -22, "selected": "m1", "prompts": {
    "m1": "Instrumental, 18th-century chamber score for a serious true story: solo cello and harpsichord, a low tense "
          "pulse, a dark sudden sting in the middle, then a hopeful, dignified string swell rising at the end. No vocals."}}
# packaging v2 (plan/packaging-v2-spec.md, C006; built 2026-11-16): applied at build time by scripts/packaging_v2.py
ep["packaging"] = {
 "version": 2,
 "case": 8,
 "hook": {
  "until": 6.7,
  "anchor": "bottom",
  "size": 54
 },
 "open": {
  "source": "projects/hcs06-onesimus/assets/images/keyframes/s7.png",
  "until": 2.14,
  "captionY": 1030,
  "motion": {
   "type": "snap",
   "from": 1.12,
   "to": 1.28,
   "at": 0,
   "frames": 50,
   "x": -7.0,
   "y": -4,
   "y0": -4
  },
  "fx": [
   {
    "kind": "spark",
    "x": 0.555,
    "y": 0.305,
    "r": 0.03
   },
   {
    "kind": "particles",
    "style": "steam",
    "x": 0.56,
    "y": 0.29,
    "tx": 0.64,
    "ty": 0.03,
    "spread": 0.01,
    "every": 0.22,
    "life": 2.4,
    "size": 100,
    "color": "205,205,200",
    "opacity": 0.4
   }
  ]
 },
 "sfx": [
  {
   "name": "paper-burn",
   "at": 0.0,
   "gain_db": -12,
   "dur": 2.2,
   "fade_out": 0.4
  }
 ],
 "sfx_move": {
  "gulls-water": 2.14,
  "ship-bell": 2.2
 }
}
ep["motion_lint"] = "warn"   # cut before Rule 0; v2 changes only the opening
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
