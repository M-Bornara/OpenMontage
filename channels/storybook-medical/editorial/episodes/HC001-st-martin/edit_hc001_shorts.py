"""HC001 Shorts S1/S2/S3 (shot-plan.md section C): vertical cuts from the long video's image pool, each shot starting
on its script line's first words in that Short's timed narration. Writes shots/overlays/sfx/music into each project."""
import json
import re
import shutil
import sys
from pathlib import Path

POOL = "projects/hc001-window-into-his-stomach/assets/images/keyframes/"
REFS = "projects/hc001-window-into-his-stomach/assets/images/refs/"
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
c.o("location", t2, t2 + 3.0, text="MACKINAC ISLAND", sub="1822")
t = c.at("the shot tore open"); c.shot(t, K("T1"), shake); c.s("stamp-thud", t + 0.3, -16)
c.shot(c.at("half an hour later"), K("M08"), push, focus=L)
t = c.at("days everything"); c.shot(t, K("M09"), static, focus=0.8)
c.o("counter", t + 0.3, t + 3.2, to=17, label="DAYS")
c.shot(c.at("he should have died"), K("T2a"), static)
c.shot(c.at("he didnt"), K("T2b"), static)
c.shot(c.at("but the hole"), K("M10"), {"type": "slide", "from": -2, "to": 2, "scale": 1.12}, focus=0.25)
t = c.at("the only option left"); c.shot(t, K("I07"), push); c.s("tick-click", t + 0.5, -22)
t = c.at("alexis said no"); c.shot(t, K("M11"), static, focus=R)
c.o("stamp", t + 0.45, t + 1.9, text="NO"); c.s("stamp-thud", t + 0.5, -14)
c.shot(c.at("so his stomach did"), K("I19"), {"type": "tilt", "from": -4, "to": 4})
c.shot(c.at("he lived with that opening"), K("T3"), pull)
c.shot(c.at("and his doctor"), K("M12"), push, focus=L)
c.save("mA", "T3: Matt's glasses on the palisade post above the river")

# ── S2 · The Doctor Who Put Food on a String ──
c = Cut("hc001-s2")
c.shot(0.0, K("I02"), {"type": "tilt", "from": -5, "to": 3})
t = c.at("army surgeon william beaumont"); c.shot(round(t - 1.2, 2), K("M01"), {"type": "pan", "from": 0, "to": 100})
c.o("stamp", t - 1.2, t + 0.4, text="1825")
c.o("nameTag", t + 0.2, t + 3.6, text="Dr. William Beaumont", sub="U.S. Army surgeon")
c.shot(c.at("doctors were still arguing"), K("I20"), static)
c.shot(c.at("did food just"), K("I21"), static)
t = c.at("so beaumont tied"); c.shot(t, K("I08"), {"type": "push", "from": 1.02, "to": 1.12})
for w in ("spiced", "salt", "raw", "boiled", "stale", "raw"):
    c.s("stamp-thud", c.at(w), -22)
# watch dial in the 9:16 crop of the square I03a: centre (55.0 %, 52.6 %), radius 251 px
t = c.at("at noon"); c.shot(t, K("I03a"), static); c.s("watch-ticking", t + 0.2, -24, dur=2.0)
t1 = c.at("one hour later")
c.o("clock", t, t1 + 1.4, cx=55.0, cy=52.6, r=251, **{"from": 12.0, "to": 13.0, "at": t1 - t, "spin": 1.2})
c.shot(round(t1 + 1.4, 2), K("I04"), static)
t2 = c.at("hours cabbage"); c.shot(t2, K("I03a"), static)
c.o("clock", t2, t2 + 1.6, cx=55.0, cy=52.6, r=251, **{"from": 13.0, "to": 14.0, "at": 0.1, "spin": 1.2})
c.shot(round(t2 + 1.6, 2), K("I05"), static); c.s("ding-correct", t2 + 1.7, -20)
c.shot(c.at("the next day alexis"), K("M16"), static, focus=R)
c.shot(c.at("so beaumont dropped"), K("I09"), {"type": "tilt", "from": -4, "to": 4})
c.shot(c.at("medical ethics committees"), K("T4"), static)
t = c.at("and that was experiment"); c.shot(t, K("I12"), pull)
c.o("counter", t + 0.9, t + 3.6, to=238, label="EXPERIMENTS", countSeconds=1.6); c.s("tick-click", t + 0.9, -20)
c.save("mB", "T4: Matt's glasses on the study windowsill behind Beaumont")

# ── S3 · The Human Experiment Who Walked Away ──
c = Cut("hc001-s3")
c.shot(0.0, K("T5"), static)
c.shot(c.at("martin couldnt"), K("M24"), push, focus=R)
c.shot(c.at("a gunshot had left"), K("M24"), push, focus=L)
t = c.at("alexis left"); c.shot(t, REFS + "plate-map.png", {"type": "pan", "from": 20, "to": 85})
c.shot(c.at("without obtaining my consent"), K("M27"), push, focus=L)
c.shot(c.at("years later"), K("M21m"), {"type": "pan", "from": 80, "to": 20})
t = c.at("miles"); c.o("counter", t, t + 2.6, to=2000, label="MILES", countSeconds=1.2)
t = c.at("between experiments"); c.shot(t, "projects/human-test-tube/assets/video/sh06.mp4", static); c.s("axe-chop", t + 0.9, -12)
c.shot(round(t + 2.0, 2), K("M15"), push, focus=R)
t = c.at("came a contract"); c.shot(t, K("I13"), {"type": "push", "from": 1.3, "to": 1.42, "y": 10})
t = c.at("one hundred fifty dollars") if "hundred" in c.toks else c.at("a year")
c.o("stamp", t, t + 2.0, text="$150"); c.s("stamp-thud", t + 0.05, -16)
c.shot(c.at("then his wife said no"), K("M26"), static, focus=L)
t = c.at("years beaumont sent"); c.shot(t, K("M27"), {"type": "push", "from": 1.05, "to": 1.15}, focus=0.2)
c.o("stamp", t + 0.2, t + 2.4, text="18 YEARS")
c.shot(c.at("dont disappoint me more"), K("M27"), {"type": "push", "from": 1.2, "to": 1.35}, focus=0.2)
c.shot(c.at("alexis never went"), K("T6"), pull)
c.save("mC", "T6: Matt's glasses hanging from the fence rail")
