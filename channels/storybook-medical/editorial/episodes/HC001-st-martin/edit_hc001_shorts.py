"""HC001 Shorts S1/S2/S3 (shot-plan.md section C): vertical cuts from the long video's image pool, each shot starting
on its script line's first words in that Short's timed narration. Writes shots/overlays/sfx/music into each project.

v2 (user review 2026-10-26): inaccurate stills swapped for the long's approved 4K art, every shot that was right kept.
Swaps (v1 -> v2): S1 thrown out of a door (T1) -> lying shot in the store (s1.15a); the surgeon kneeling at a shelf (M08)
-> Beaumont running up / over Alexis (s1.10, s1.13); an empty bed (M09) -> Beaumont feeding him (s2.02).
S2 log cabin (M01) -> the 1825 stone room (s0.05, s0.02a); arguing doctors (s3.02); separate parcels (I08) -> the six foods
tied on ONE string (wI01, s4.03); food that never digested (I04, I05) -> one hour: bread crumbling + cabbage half gone
(v2-food-1h, shorts_v2_prep.py) and two hours: four foods gone (s4.05c); Alexis sick in a log room (M16) -> stone room (s4.06).
S3 grey-haired Beaumont in 1825 (M27) -> young Beaumont (s5.02); three children in the canoe (M21m) -> wife + two children
(v2-family-canoe, claims C17); "carried loads" (M15) -> Alexis carrying a sack (s5.09); the 1833 contract (s5.16) and coins
(s6.03) break up a 9 s hold. Clock: the hands pivot on the painted pin and land on the painted marks (dial_fit.py).
Captions and stamps (user review 2026-10-26): placed per shot (cap=, y=, x=) after looking at each picture on a height
grid, so the words cover at most part of the picture and never a face or the shot's subject. Caption tops: TOP 300
(sky/wall), CHEST 760, MID 1180 (default), LOW 1420-1450 (above the Shorts UI at the bottom).
SFX only on a picture event (rule from the cut-v2 review): the food-word thuds, the stitch-tray click and the ding are gone."""
import json
import re
import shutil
import sys
from pathlib import Path

POOL = "projects/hc001-window-into-his-stomach/assets/images/keyframes/"
REFS = "projects/hc001-window-into-his-stomach/assets/images/refs/"
TOP, CHEST, LOW = 300, 760, 1430           # caption tops (MID 1180 is the template default)
LONG_MUSIC = Path("projects/hc001-window-into-his-stomach/assets/music")
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
K = lambda n: POOL + n + ".png"
push, pull, static, shake = {"type": "push"}, {"type": "pull"}, {"type": "static"}, {"type": "shake"}
L, R = 0.12, 0.88          # window focus: Beaumont is always screen-left, Alexis screen-right


class Cut:
    def __init__(self, pid):
        self.pid, self.P = pid, Path("projects") / pid
        self.words = json.load(open(self.P / "artifacts/word_timestamps.json", encoding="utf-8"))
        self.toks = [norm(w["word"]) for w in self.words]
        self.cur, self.shots, self.ov, self.fx = 0, [], [], []

    def at(self, phrase):
        want = [norm(x) for x in phrase.split()]
        for i in range(self.cur, len(self.toks) - len(want) + 1):
            if self.toks[i:i + len(want)] == want:
                self.cur = i + 1
                return round(max(0, self.words[i]["start"] - 0.05), 2)
        raise SystemExit(f"{self.pid}: phrase not found: {phrase!r}")

    def word_times(self, *ws):
        out = []
        for w in ws:
            out.append(self.at(w))
        return out

    def shot(self, t, source, motion=push, **kw):
        if "cap" in kw:
            kw["captionY"] = kw.pop("cap")
        self.shots.append({"id": f"s{len(self.shots) + 1:02d}", "start": t, "source": source, "motion": motion, **kw})

    def o(self, kind, start, end, **kw):
        self.ov.append({"kind": kind, "start": round(start, 2), "end": round(end, 2), **kw})

    def s(self, name, t, gain=-14, **kw):
        self.fx.append({"name": name, "at": round(t, 2), "gain_db": gain, **kw})

    def save(self, music, glasses_note):
        total = round(self.words[-1]["end"] + 0.6, 2)
        self.shots.sort(key=lambda x: x["start"])
        for i, x in enumerate(self.shots):
            x["end"] = self.shots[i + 1]["start"] if i + 1 < len(self.shots) else total
        ep = json.load(open(self.P / "episode.json", encoding="utf-8"))
        (self.P / "assets/music").mkdir(parents=True, exist_ok=True)
        shutil.copy(LONG_MUSIC / f"{music}.mp3", self.P / "assets/music" / f"{music}.mp3")
        ep.update({"shots": self.shots, "overlays": sorted(self.ov, key=lambda x: x["start"]),
                   "sfx": sorted(self.fx, key=lambda x: x["at"]), "music": {"selected": music, "lufs": -22, "prompts": {}},
                   "glasses": glasses_note})
        json.dump(ep, open(self.P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"{self.pid}: {len(self.shots)} shots, {len(self.ov)} overlays, {len(self.fx)} sfx, {total}s")


# ── S1 · He Survived a Hole in His Stomach ──
c = Cut("hc001-s1")
t = c.at("a musket went off"); c.shot(0.0, K("I06"), push); c.s("musket-shot", t + 0.25, -10)
t = c.at("he was about"); c.shot(t, K("M05"), {"type": "slide", "from": 2, "to": -2, "scale": 1.12}, focus=R, transition="flash")
t2 = c.at("a canoeman") if "canoeman" in c.toks else c.at("canoe")
c.o("location", t2, t2 + 3.0, text="MACKINAC ISLAND", sub="1822", y=1430)     # under his hands, off his face
t = c.at("the shot tore open"); c.shot(t, K("s1.15a"), shake, focus=0.62, cap=TOP); c.s("stamp-thud", t + 0.05, -16)
c.shot(c.at("half an hour later"), K("s1.10"), push, focus=0.18, cap=280)
c.shot(c.at("could see straight"), K("s1.13-soft"), push, focus=0.5, cap=CHEST)
t = c.at("days everything"); c.shot(t, K("s2.02"), push, focus=0.5, cap=LOW)
c.o("counter", t + 0.3, t + 3.2, to=17, label="DAYS")
c.shot(c.at("he should have died"), K("T2a"), static, cap=LOW)
c.shot(c.at("he didnt"), K("T2b"), static, cap=LOW)
# Beaumont's hands at the basin + Alexis on the bed, not his back (user review 2026-10-26)
c.shot(c.at("but the hole"), K("M10"), push, focus=0.5)
c.shot(c.at("the only option left"), K("I07"), push, cap=TOP)
t = c.at("alexis said no"); c.shot(t, K("M11"), static, focus=R, cap=LOW)
c.o("stamp", t + 0.45, t + 1.9, text="NO", x=235, y=330); c.s("stamp-thud", t + 0.5, -14)   # on the wall beside his head
c.shot(c.at("so his stomach did"), K("I19"), {"type": "tilt", "from": -4, "to": 4})
c.shot(c.at("he lived with that opening"), K("T3"), pull, cap=TOP)
c.shot(c.at("and his doctor"), K("M12"), push, focus=L)
c.save("mA", "T3: Matt's glasses on the palisade post above the river")

# ── S2 · The Doctor Who Put Food on a String ──
# the painted dial of I03a in the static 9:16 frame (dial_fit.py: source px -> crop x 448..1600, x0.9375, scale 1.04);
# 12 o'clock = the mark under the stem (user review 2026-10-26: the top mark is 1 o'clock on this tilted dial)
I03A_PIN = [531.7, 962.2]
I03A_MARKS = [[697.5, 811.7], [772.0, 883.5], [801.2, 988.3], [753.7, 1093.5], [642.7, 1166.8], [505.5, 1186.1],
              [378.6, 1150.8], [292.9, 1070.1], [276.4, 963.0], [343.9, 872.1], [441.5, 805.8], [566.8, 783.5]]
c = Cut("hc001-s2")
c.shot(0.0, K("I02"), {"type": "tilt", "from": -5, "to": 3}, cap=LOW)
t0 = c.at("1825"); t = c.at("army surgeon william beaumont")
c.shot(round(t0 - 0.1, 2), K("s0.05"), push, focus=0.4)
c.o("stamp", t0 - 0.1, t0 + 1.2, text="1825", y=1430)                          # both below his face
c.o("nameTag", t + 0.2, t + 2.2, text="Dr. William Beaumont", sub="U.S. Army surgeon", y=1450)
c.shot(c.at("his patient"), K("s0.02a"), push, focus=0.57, cap=CHEST)
c.shot(c.at("doctors were still arguing"), K("s3.02"), {"type": "pan", "from": 10, "to": 75}, cap=LOW)
c.shot(c.at("did the stomach grind"), K("I20"), static, cap=LOW)
c.shot(c.at("did food just"), K("I21"), static, cap=LOW)
c.shot(c.at("so beaumont tied"), K("wI01"), push, focus=0.45, cap=LOW)
c.shot(c.at("spiced"), K("s4.03"), {"type": "pan", "from": 12, "to": 100}, cap=LOW)
t = c.at("at noon"); c.shot(t, K("I03a"), static, cap=1480); c.s("watch-ticking", t + 0.2, -24, dur=4.0)
t1 = c.at("one hour later")
# 12:00 on "noon"; one steady hour starts as "in they went" ends and lands on "later", before the string comes out
c.o("clock", t, t1 + 1.2, pin=I03A_PIN, marks=I03A_MARKS, **{"from": 12.0, "to": 13.0, "at": round(t1 - t - 0.65, 2), "spin": 1.2})
c.shot(c.at("he pulled the string"), K("v2-food-1h"), push, focus=0.75)
t2 = c.at("two hours"); c.shot(t2, K("I03a"), static, cap=1480)
c.o("clock", t2, t2 + 1.7, pin=I03A_PIN, marks=I03A_MARKS, **{"from": 13.0, "to": 14.0, "at": 0.1, "spin": 1.1})   # lands ~0.5 s before the cut
c.shot(round(t2 + 1.7, 2), K("s4.05c"), {"type": "pan", "from": 100, "to": 15}, cap=LOW)
c.shot(c.at("the next day alexis"), K("s4.06"), push, focus=0.6, cap=LOW)
c.shot(c.at("so beaumont dropped"), K("I09"), {"type": "tilt", "from": -4, "to": 4}, cap=LOW)
c.shot(c.at("medical ethics committees"), K("T4"), static)
t = c.at("and that was experiment"); c.shot(t, K("I12"), pull)
c.o("counter", t + 0.9, t + 3.6, to=238, label="EXPERIMENTS", countSeconds=1.6); c.s("tick-click", t + 0.9, -20)
c.save("mB", "T4: Matt's glasses on the study windowsill behind Beaumont")

# ── S3 · The Human Experiment Who Walked Away ──
c = Cut("hc001-s3")
c.shot(0.0, K("T5"), static, cap=TOP)
c.shot(c.at("martin couldnt"), K("M24"), push, focus=R)
c.shot(c.at("a gunshot had left"), K("M24"), push, focus=L)
t = c.at("alexis left"); c.shot(t, REFS + "plate-map.png", {"type": "pan", "from": 20, "to": 85})
c.shot(c.at("without obtaining my consent"), K("s5.02"), push, focus=0.5)
c.shot(c.at("years later"), K("v2-family-canoe"), push, focus=0.21, cap=TOP)
tm = c.at("miles")
t = c.at("between experiments"); c.shot(t, "projects/human-test-tube/assets/video/sh06.mp4", static, cap=LOW)
c.s("axe-chop", t + 0.9, -12)
c.o("counter", tm, t, to=2000, label="MILES", countSeconds=1.2, y=640)           # above the canoe, gone before the axe
c.shot(c.at("carried loads"), K("s5.09"), {"type": "pan", "from": 85, "to": 10}, cap=LOW)
c.shot(c.at("came a contract"), K("s5.16"), push, focus=0.5)
c.shot(c.at("a covenant servant"), K("I13"), {"type": "push", "from": 1.3, "to": 1.42, "y": 10})
t = c.at("one hundred fifty dollars") if "hundred" in c.toks else c.at("a year")
c.shot(round(t - 0.3, 2), K("s6.03"), push, focus=0.3, cap=CHEST)
c.o("stamp", t, t + 2.0, text="$150"); c.s("stamp-thud", t + 0.05, -16)
c.shot(c.at("then his wife said no"), K("M26"), static, focus=L)
t = c.at("years beaumont sent"); c.shot(t, K("M27"), {"type": "push", "from": 1.05, "to": 1.15}, focus=0.2)
c.o("stamp", t + 0.2, t + 2.4, text="18 YEARS", y=250)                          # sized to the frame, above his head
c.shot(c.at("dont disappoint me more"), K("M27"), {"type": "push", "from": 1.2, "to": 1.35}, focus=0.2)
c.shot(c.at("alexis never went"), K("T6"), pull, cap=TOP)
c.save("mC", "T6: Matt's glasses hanging from the fence rail")
