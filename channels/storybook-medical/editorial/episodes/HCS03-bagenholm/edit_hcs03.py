"""HCS03 rough cut (plan/production-v3.md §3): storyboard-v1 as shots, overlays, SFX and music in
projects/hcs03-bagenholm/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
Not in the rough cut yet (need masks): the frost spreading on the thermometer (s1), the red-jacket highlight (s2a), the
rising bubbles (s3), the glove pull (s4a), the blue-to-amber warm-up (s7), the glow through the tubing (s8), 2.5D
parallax (s2a, s6: plain camera moves stand in).
    python channels/storybook-medical/editorial/episodes/HCS03-bagenholm/edit_hcs03.py
"""
import json
import re
from pathlib import Path

PID = "hcs03-bagenholm"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 1180, 1430                 # caption tops (StorybookShort)
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

# measured on the frames (memory: effects-on-exact-object). s9: the monitor's dark screen spans x 0.365-0.765,
# y 0.345-0.625 of the source; the line runs along its middle. The wall clock's pin + 12 marks: review/dial_s9.json,
# in source px (1536 x 2752), mapped to the 1080 x 1920 layout (scale 0.703, 7.7 px cropped top and bottom), then the
# static shot's 1.04 zoom around the frame centre (StorybookShort), or the hands sit ~30 px off the painted pin.
SCREEN_Y = 0.485
FLAT = [[0.40, SCREEN_Y], [0.52, SCREEN_Y]]
BEAT = [[0.52, SCREEN_Y], [0.55, SCREEN_Y], [0.565, SCREEN_Y - 0.05], [0.58, SCREEN_Y + 0.03], [0.595, SCREEN_Y],
        [0.64, SCREEN_Y], [0.655, SCREEN_Y - 0.05], [0.67, SCREEN_Y + 0.03], [0.685, SCREEN_Y], [0.73, SCREEN_Y]]
DIAL = json.load(open(P / "review/dial_s9.json"))
k, dy = 1080 / 1536, (2752 * 1080 / 1536 - 1920) / 2
lay = lambda x, y: [round(540 + (x * k - 540) * 1.04, 1), round(960 + (y * k - dy - 960) * 1.04, 1)]
PIN = lay(*DIAL["pin"])
MARKS = [lay(x, y) for x, y in DIAL["marks"]]


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

    def shot(self, t, source, motion, cap=MID, **kw):
        self.shots.append({"id": f"s{len(self.shots) + 1:02d}", "start": max(0.0, round(t - 0.05, 2)), "source": source,
                           "motion": motion, "captionY": cap, **kw})

    def o(self, kind, start, end, **kw):
        self.ov.append({"kind": kind, "start": round(start, 2), "end": round(end, 2), **kw})

    def s(self, name, t, gain=-14, **kw):
        self.fx.append({"name": name, "at": round(t, 2), "gain_db": gain, **kw})


c = Cut()
# v2 decoupage (user review): one image per idea in the opening line, not one thermometer for all three
c.shot(0.0, KF + "s1a.png", push(0.45, 0.4, 1.15), cap=LOW)         # the gloved hand under the ice
c.s("heartbeat", 0.3, -16)
t = c.at("her body cooled")
c.shot(t, KF + "s1b.png", push(0.45, 0.6, 1.25), cap=TOP)          # along the glass to the low red line
c.s("ice-crack", t + 0.1, -24)
seven = c.at("137")
c.o("stamp", seven + 0.3, seven + 2.6, text="13.7 °C", y=1180); c.s("stamp-thud", seven + 0.35, -14)
c.shot(c.at("and she lived"), KF + "s1c.png", push(0.55, 0.5, 1.12), cap=TOP)   # warmth: the mug
t = c.at("norway")
c.shot(t, KF + "s2a.png", {"type": "slide", "from": -3, "to": 3, "scale": 1.1}, cap=LOW)
anna = c.at("anna")
c.o("nameTag", anna + 0.1, anna + 2.4, text="Anna Bågenholm", sub="young doctor · Norway, 1999", y=190)
c.s("wind-snow", t, -26)
t = c.at("when she went")
c.shot(t, KF + "s2b.png", push(0.5, 0.45, 1.2), cap=TOP)            # ice level: the boots and skis
c.s("ice-crack", c.at("headfirst"), -14)
t = c.at("underneath")
c.shot(t, KF + "s3.png", push(0.4, 0.4, 1.12), cap=LOW)             # her head in the air gap
c.s("bubbles", t + 0.4, -20)
t = c.at("her friends held")
c.shot(t, KF + "s4a.png", {"type": "static"}, cap=TOP)
t = c.at("after about 40")
forty = c.at("40")
# the watch now reads 40:00 itself (user review: the blank screen), so no stamp
c.shot(t, KF + "s4b.png", push(0.42, 0.45, 1.2), cap=LOW)
c.s("heartbeat", c.at("heart stopped"), -14)
t = c.at("they cut her free")
eighty = c.at("80")
# v2: two close shots instead of the s5/s6 valley repeat (user review)
c.shot(t, KF + "s5a.png", push(0.5, 0.6, 1.15), cap=TOP)
c.o("stamp", eighty, eighty + 1.8, text="80 MIN", y=1560); c.s("axe-chop", t + 0.1, -18)
c.shot(c.at("no pulse"), KF + "s5b.png", push(0.6, 0.45, 1.15), cap=LOW)
t = c.at("most people")
c.shot(t, KF + "s6.png", {"type": "pull", "from": 1.2, "to": 1.04}, cap=TOP)
c.s("helicopter", t, -24)
t = c.at("but doctors have")
c.shot(t, KF + "s7.png", push(0.5, 0.5, 1.2), cap=LOW)
c.s("door-swing", t + 0.1, -20)
t = c.at("in tromsa")
c.shot(t, KF + "s8.png", {"type": "slide", "from": 3, "to": -3, "scale": 1.1}, cap=TOP)
c.s("machine-hum", t, -24)
t = c.at("that night")
beat = c.at("beating")
# static: the clock hands are a frame-space overlay, so the camera must not move on this shot
c.shot(t, KF + "s9.png", {"type": "static"}, cap=LOW,
       draw=[{"points": FLAT, "from": 0.0, "to": 0.4, "color": "#7CFF9A", "width": 8, "glow": True},
             {"points": BEAT, "from": round(beat - t, 2), "to": round(beat - t + 1.2, 2), "color": "#7CFF9A", "width": 8, "glow": True}])
c.o("clock", t, beat + 2.5, pin=PIN, marks=MARKS, **{"from": 10.25, "to": 10.25})
c.s("monitor-beep", beat + 0.1, -16); c.s("monitor-beep", beat + 0.9, -16)
t = c.at("today")
c.shot(t, KF + "s10.png", push(0.5, 0.55, 1.15), cap=TOP, transition="dissolve")
c.s("running-footsteps", t + 0.2, -28)

total = round(c.words[-1]["end"] + 0.8, 2)
c.shots.sort(key=lambda x: x["start"])
for i, x in enumerate(c.shots):
    x["end"] = c.shots[i + 1]["start"] if i + 1 < len(c.shots) else total

ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.update({"loop": True, "shots": c.shots, "overlays": sorted(c.ov, key=lambda x: x["start"]), "sfx": sorted(c.fx, key=lambda x: x["at"]),
           "glasses": "s6: Matt's spectacles on the snowy rock in the foreground"})
ep["music"] = {"lufs": -22, "selected": "m1", "prompts": {
    "m1": "Instrumental, cold and suspenseful Nordic score for a true survival story: soft felt piano, glassy high "
          "strings, a slow low pulse like a faint heartbeat, icy shimmering bells, near-silence in the middle, then a "
          "warm swell of cello and horns that blooms into hope at the end. No vocals."}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
