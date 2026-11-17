"""HCS08 rough cut (plan/production-v3.md §3): storyboard-v1 (script v2) as shots, overlays, SFX and music in
projects/hcs08-john-snow/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (review/_grid.jpg, fractions of the source image).
    python channels/storybook-medical/editorial/episodes/HCS08-john-snow/edit_hcs08.py
"""
import json
import re
from pathlib import Path

PID = "hcs08-john-snow"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030   # caption tops inside the platform safe zone (y 288-1248; StorybookShort SAFE)
FIX = {}                          # STT spelling -> caption spelling
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
# s1a: foggy rooftops
c.shot(0.0, KF + "s1a.png", {"type": "pull", "from": 1.18, "to": 1.04}, cap=LOW)
c.o("stamp", 0.2, 2.8, text="LONDON · 1854", y=TOP)
c.s("church-bell", 0.1, query="church bell"); c.s("night-wind", 0.0)
# s1b: the pump; a glint runs on the handle (measured: handle top at 0.32, 0.24)
t = c.at("by taking")
handle = c.at("handle")
c.shot(t, KF + "s1b.png", push(0.45, 0.35, 1.15), cap=LOW,
       fx=[{"kind": "glint", "x": 0.32, "y": 0.24, "at": rel(handle, t), "size": 30}])
c.s("pump-creak", handle, query="old iron hand pump creak")
# s2: the street in mourning
t = c.at("london soho")
killed = c.at("killed")
c.shot(t, KF + "s2.png", push(0.45, 0.55, 1.1), cap=LOW)
c.o("stamp", killed, killed + 2.4, text="500 DEAD · 10 DAYS", y=TOP)
c.s("night-wind", t, query=None)
# s3: the miasma doctors in green fog
t = c.at("most doctors")
c.shot(t, KF + "s3.png", push(0.5, 0.4, 1.12), cap=TOP,
       fx=[{"kind": "tint", "at": 0.0, "dur": 1.2, "from": "rgba(70,140,70,0)", "to": "rgba(70,140,70,0.28)", "blend": "multiply"}])
# s4a: Snow and the glass of water (glass measured at 0.88, 0.37)
t = c.at("john snow")
water = c.at("water")
c.shot(t, KF + "s4a.png", push(0.7, 0.36, 1.15), cap=LOW)
c.o("nameTag", t + 0.05, t + 2.0, text="John Snow", sub="doctor, London", y=300)
c.s("glass-clink", water, -14)
# s4b: door to door
t = c.at("he went door")
c.shot(t, KF + "s4b.png", {"type": "slide", "from": -2, "to": 2, "scale": 1.08}, cap=TOP)
c.s("door-knock", t + 0.1)
# s5: the pattern around one pump (pump measured at 0.50, 0.60)
t = c.at("they clustered")
pump, broad = c.at("one pump"), c.at("broad street")
c.shot(t, KF + "s5.png", {"type": "static"}, cap=MID,
       fx=[{"kind": "spot", "cx": 0.50, "cy": 0.60, "rx": 0.09, "ry": 0.08, "at": rel(pump, t), "dur": 2.4, "dim": 0.55}])
c.o("stamp", broad, broad + 1.2, text="BROAD STREET", y=TOP)
c.s("hit-suspense", pump, -14)
# s6: the brewery (Matt's cameo)
t = c.at("the brewery")
beer = c.at("beer")
c.shot(t, KF + "s6.png", push(0.5, 0.45, 1.12), cap=TOP)
c.s("tavern-laughter", t + 0.2, query="men laughing"); c.s("glass-clink", beer)
# s7a: the house in Hampstead
t = c.at("a widow")
c.shot(t, KF + "s7a.png", {"type": "static"}, cap=LOW)
c.o("stamp", t + 0.3, t + 1.8, text="HAMPSTEAD", y=TOP)
c.s("birdsong", t, query="birdsong countryside morning")
# s7b: she drinks it
t = c.at("she liked")
c.shot(t, KF + "s7b.png", push(0.8, 0.45, 1.15), cap=TOP)
c.s("water-pour", c.at("brought"), query="pouring water into glass")
# s8: the handle comes off (glasses measured at 0.38, 0.79)
t = c.at("on the 8th")
took = c.at("took the handle")
c.shot(t, KF + "s8.png", push(0.45, 0.6, 1.12), cap=LOW,
       fx=[{"kind": "glint", "x": 0.38, "y": 0.79, "at": rel(took, t) + 1.0, "size": 26}])
c.o("stamp", t + 0.2, took - 0.1, text="8 SEPT 1854", y=TOP)
c.s("metal-clank", took + 0.2, query="metal clang")
# s9a: the street days later, in sun
t = c.at("the twist")
c.shot(t, KF + "s9a.png", {"type": "pull", "from": 1.15, "to": 1.03}, cap=MID)
c.s("whoosh", t)
# s9b: Snow admits it
t = c.at("snow admitted")
c.shot(t, KF + "s9b.png", push(0.5, 0.45, 1.08), cap=LOW)
c.o("stamp", t + 0.4, t + 1.9, text="OVERSTATEMENT", y=TOP)
c.s("quill-writing", t); c.s("stamp-thud", t + 0.45)
# s10: the map (pump symbol measured at 0.58, 0.51)
t = c.at("but his map")
c.shot(t, KF + "s10.png", push(0.58, 0.51, 1.18), cap=TOP,
       fx=[{"kind": "glow", "x": 0.58, "y": 0.51, "r": 0.06, "at": rel(t, t) + 0.3, "dur": 3.0, "color": "rgba(255,200,90,1)", "strength": 0.5}])
c.s("paper-slide", t)

HITS = {"stamp-thud", "glass-clink", "door-knock", "pump-creak", "metal-clank", "paper-slide", "quill-writing",
        "church-bell", "hit-suspense", "whoosh", "water-pour"}
for cue in c.fx:
    cue["gain_db"] = -8 if cue["name"] in HITS else -15
    if cue.get("query") is None:
        cue.pop("query", None)

TAIL = 1.0
total = round(c.words[-1]["end"] + 0.8 + TAIL, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"loop": True, "tail_seconds": TAIL, "shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]),
           "sfx": sorted(c.fx, key=lambda x: x["at"]), "glasses": "s8: Matt's spectacles on the pump's stone trough"})
ep["theme"] = {"culture": "victorian-london", "font": "montserrat"}
ep["music"] = {"lufs": -22, "selected": "m2", "prompts": {
    # m1 came back 37 s (2 sections) for a 46 s Short; m2 asks for 3 sections
    "m2": {"sections": 3, "prompt": "Instrumental, Victorian London 1850s mystery score for a true detective story: solo cello and upright piano, "
          "a light pizzicato walking pulse like a detective's footsteps, a faint music-box motif, minor key and curious, "
          "a short playful lift near the end, then a warm resolving chord. No vocals, no modern drums."}}}
# packaging v2 (plan/packaging-v2-spec.md, C006; built 2026-11-16): applied at build time by scripts/packaging_v2.py
ep["packaging"] = {
 "version": 2,
 "case": 9,
 "hook": {
  "anchor": "top"
 },
 "open": {
  "source": "projects/hcs08-john-snow/assets/images/keyframes/s8.png",
  "until": 3.9,
  "captionY": 1030,
  "motion": {
   "type": "snap",
   "from": 1.08,
   "to": 1.22,
   "at": 0,
   "frames": 45,
   "x": -12,
   "y": 0
  },
  "fx": [
   {
    "kind": "particles",
    "style": "haze",
    "x": 0.05,
    "y": 0.5,
    "tx": 0.95,
    "ty": 0.44,
    "spread": 0.05,
    "every": 0.35,
    "life": 3.2,
    "size": 260,
    "color": "205,198,185",
    "opacity": 0.22
   }
  ]
 },
 "sfx": [
  {
   "name": "metal-clank",
   "at": 0.2,
   "gain_db": -10
  }
 ]
}
ep["motion_lint"] = "warn"   # cut before Rule 0; v2 changes only the opening
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
