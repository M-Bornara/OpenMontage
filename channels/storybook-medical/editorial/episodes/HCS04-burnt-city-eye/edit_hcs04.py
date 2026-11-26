"""HCS04 rough cut (plan/production-v3.md §3): storyboard-v1 as shots, overlays, SFX and music in
projects/hcs04-burnt-city-eye/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (review/_grid.jpg, fractions of the source image).
Not in the rough cut yet: the iris and rays drawing themselves in light (s4), the thread tracing itself (s5; needs a
measured path), 2.5D parallax (s2a; a slide stands in).
    python channels/storybook-medical/editorial/episodes/HCS04-burnt-city-eye/edit_hcs04.py
"""
import json
import re
from pathlib import Path

PID = "hcs04-burnt-city-eye"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030   # caption tops inside the platform safe zone (y 288-1248; StorybookShort SAFE)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
FIX = {"1/2": "half"}                           # STT spelling -> caption spelling


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
# s1: the eye in the trench; a gold glint crosses it on "golden eye"
gold = c.at("golden eye")
c.shot(0.0, KF + "s1.png", push(0.40, 0.48, 1.2), cap=TOP,
       fx=[{"kind": "glint", "x": 0.40, "y": 0.47, "at": rel(gold, 0.05), "size": 60}])
c.s("brush-sweep", 0.1, -20, query="brushing")
# no stamp: the caption already says "5,000 years ago" (rough cut 1 showed it twice)
t = c.at("the burnt city")
c.shot(t, KF + "s2a.png", {"type": "slide", "from": -3, "to": 3, "scale": 1.1}, cap=LOW)
c.o("nameTag", t + 0.1, t + 2.6, text="Shahr-e Sukhteh", sub="the Burnt City · c. 2900 BC", y=300)
c.s("desert-wind", t, -26, query="desert wind gentle")
t = c.at("she died")
c.shot(t, KF + "s2b.png", {"type": "static"}, cap=LOW)
t = c.at("her eye was")
tar, gld = c.at("tar paste"), c.at("gold")
# s3: a ring on the chipped rim (black tar inside) on "tar paste", the gold glows on "gold"; Matt's glasses glint
c.shot(t, KF + "s3.png", push(0.50, 0.47, 1.18), cap=TOP,
       fx=[{"kind": "spot", "cx": 0.525, "cy": 0.565, "rx": 0.06, "ry": 0.035, "at": rel(tar, t), "dur": 1.4, "dim": 0.45},
           {"kind": "glow", "x": 0.50, "y": 0.47, "r": 0.22, "at": rel(gld, t), "dur": 1.0, "strength": 0.4},
           {"kind": "glint", "x": 0.91, "y": 0.43, "at": 0.6, "size": 26}])
t = c.at("drawn on it")
iris, rays = c.at("iris"), c.at("rays")
c.shot(t, KF + "s4.png", push(0.5, 0.47, 1.2), cap=TOP,
       fx=[{"kind": "glow", "x": 0.5, "y": 0.47, "r": 0.12, "at": rel(iris, t), "dur": 0.8, "strength": 0.45},
           {"kind": "glow", "x": 0.5, "y": 0.42, "r": 0.34, "at": rel(rays, t), "dur": 1.2, "strength": 0.35}])
c.s("chime-soft", rays, -22, query="soft magic chime shimmer")
t = c.at("two tiny holes")
thread = c.at("thread")
c.shot(t, KF + "s5.png", push(0.43, 0.42, 1.25), cap=TOP,           # v4 frame: eye at 0.43 / 0.418
       fx=[{"kind": "glow", "x": 0.43, "y": 0.418, "r": 0.06, "at": rel(thread, t) - 0.6, "dur": 1.0, "strength": 0.4}])
t = c.at("under a microscope")
c.shot(t, KF + "s6a.png", push(0.32, 0.6, 1.15), cap=TOP)
c.s("tick-click", t + 0.3, -20)
t = c.at("her eye socket")
marks, years = c.at("marks"), c.at("years")
c.shot(t, KF + "s6b.png", push(0.5, 0.48, 1.15), cap=LOW,
       fx=[{"kind": "glow", "x": 0.5, "y": 0.48, "r": 0.12, "at": rel(marks, t), "dur": 1.2, "strength": 0.3}])
c.o("stamp", years, years + 1.8, text="WORN FOR YEARS", y=TOP); c.s("stamp-thud", years + 0.05, -14)
t = c.at("was she a priestess")
legend = c.at("legend")
# s7: the legend fades to an old sepia sketch on "legend" (Matt at the crowd's left edge, writing)
c.shot(t, KF + "s7.png", {"type": "push", "from": 1.12, "to": 1.2, "x": 0, "y": 6}, cap=LOW,
       fx=[{"kind": "tint", "at": rel(legend, t) - 0.1, "dur": 0.9, "from": "rgba(150,110,60,0)", "to": "rgba(150,110,60,0.5)",
            "blend": "color"}])
c.s("crowd-murmur", t, -26)
c.o("stamp", legend + 0.1, legend + 1.6, text="LEGEND", y=720)   # above the LOW caption (1030), below her feet
t = c.at("some archaeologists")
patch = c.at("eye patch")
c.shot(t, KF + "s8.png", {"type": "static"}, cap=TOP)
c.o("stamp", patch + 0.1, patch + 1.6, text="DISPUTED", y=1010); c.s("stamp-thud", patch + 0.15, -16)
t = c.at("either way")
made = c.at("made")
c.shot(t, KF + "s9.png", push(0.82, 0.6, 1.15), cap=MID,
       fx=[{"kind": "glow", "x": 0.88, "y": 0.62, "r": 0.12, "at": rel(made, t), "dur": 1.0, "strength": 0.45}])

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
           "sfx": sorted(c.fx, key=lambda x: x["at"]), "glasses": "s3: Matt's spectacles hang from the dig sieve"})
# user (rough cut 1): ancient Persian music for a story set in Iran; the theme (music + caption font) follows the culture
ep["theme"] = {"culture": "persia", "font": "lalezar"}
ep["music"] = {"lufs": -22, "selected": "m2", "prompts": {
    "m1": "Instrumental, mysterious and curious score for an ancient true story: a plucked santur and oud, a soft frame "
          "drum, a low desert drone and airy flute; wondering at the start, a light playful plucked middle, then a warm "
          "golden swell at the end. No vocals.",
    "m2": "Instrumental traditional ancient Persian music: santur, setar and tar, a breathy ney flute, daf and tombak "
          "frame drums, in the Persian dastgah Homayoun mode; mysterious and wondering at the start, a light rhythmic "
          "playful middle on the tombak, then a warm, golden, noble close. Authentic Iranian classical sound, no "
          "Western orchestra, no synth, no vocals."}}
# packaging v2 (plan/packaging-v2-spec.md, C006; built 2026-11-16): applied at build time by scripts/packaging_v2.py.
# v2.1 card approved 2026-11-17 (plan/hook-cards-v2.1.md): no "golden eye" on the card (eye vs eyepatch is DISPUTED).
# Same day: "in Iran" cut from spoken line 1 (no re-voice; country out of the hook, facts unchanged in the description).
ep["packaging"] = {
 "version": 2,
 "case": 7,
 "hook": {
  "card": "She wore *gold* / in her eye socket",
  "anchor": "top",
  # the "in Iran" join (2026-11-17, re-cut with no gap: user heard a hole) leaves no pause before "was", so the
  # pause rule would collapse at "a woman" (1.6 s, too short to read); hold to "was" as approved (captions "was buried...")
  "until": next(round(w["start"], 2) for w in c.words if norm(w["word"]) == "was"),
 },
 "frame1": {
  "motion": {
   "type": "snap",
   "from": 1.04,
   "to": 1.2,
   "at": 0,
   "frames": 45,
   "x": 10.0,
   "y": 2.4
  },
  "fx": [
   {
    "kind": "particles",
    "style": "haze",
    "x": 0.66,
    "y": 0.52,
    "tx": 0.82,
    "ty": 0.38,
    "spread": 0.03,
    "every": 0.12,
    "life": 1.5,
    "size": 90,
    "color": "225,205,160",
    "opacity": 0.5,
    "from": 0,
    "to": 4.5
   },
   {
    "kind": "glint",
    "x": 0.4,
    "y": 0.47,
    "at": 0.15,
    "size": 46
   }
  ]
 }
}
ep["motion_lint"] = "warn"   # cut before Rule 0; v2 changes only the opening
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
