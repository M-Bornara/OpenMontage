"""HCS05 cut v2 (story-v2.md, storyboard-v2.md; rough cut 1 in projects/hcs05-al-razi/rough-cut-1): shots, overlays, SFX and music in
projects/hcs05-al-razi/episode.json. Every shot starts on its line's first word in the timed narration.
Then: episode.py sfx -> music -> build -> mix -> render.
FX positions measured on the frames (projects/hcs05-al-razi/review/_grid.jpg, fractions of the source image).
Captions never sit on a face or on an FX target.
    python channels/storybook-medical/editorial/episodes/HCS05-al-razi/edit_hcs05.py
"""
import json
import re
from pathlib import Path

PID = "hcs05-al-razi"
P = Path("projects") / PID
KF = f"projects/{PID}/assets/images/keyframes/"
TOP, MID, LOW = 300, 660, 1030
FIX = {"Ray,": "Rey,", "Ray": "Rey"}   # STT heard the city as "Ray"
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
        for a, b in zip(self.words, self.words[1:]):
            if norm(a["word"]) == "blood" and norm(b["word"]) == "group":
                a["word"] = a["word"].replace("blood", "bled").replace("Blood", "Bled")
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
# measured on the frames (fractions of the source image)
LANCET_S3 = (0.66, 0.765)       # s3 lancet blade (rough cut 1: the glint sat below it, on the cloth)
GLASSES_S7A = (0.56, 0.235)     # s7a glasses (rough cut 1 had 0.20: too high)
BLADE_S3B = (0.34, 0.60)        # s3b blade (measured on the grid; the painted sparkle sits here)
ROW_A, ROW_B = (0.25, 0.68), (0.75, 0.68)   # s5b bed rows left/right of the curtain (measured)
# B1 HOOK: he stops the assistant; snap zoom onto the raised palm on "refused"
ref = c.at("refused")
c.shot(0.0, KF + "s1a.png", {"type": "snap", "from": 1.03, "to": 1.28, "at": round(ref - 0.05, 2), "x": -4, "y": 4}, cap=TOP)   # text check: LOW sat on his raised palm
# (no "c. 900 AD" stamp: under a TOP caption it sat on his raised palm, and Liam says "1100 years ago")
c.s("fire-crackle", 0.0); c.s("metal-clank", ref, query="small metal bowl set down")
t = c.at("on purpose")
c.shot(t, KF + "s1b.png", {"type": "static"}, cap=TOP)
c.s("hit-suspense", t)
# B2 STAKES: the fever (the lancet waits on the table)
t = c.at("persia")
stiff = c.at("stiff")
men = c.at("meningitis")
NECK_S3 = (0.62, 0.53)   # his hand at his stiff neck (measured on the s3 grid)
c.shot(t, KF + "s3.png", {"type": "snap", "from": 1.04, "to": 1.22, "at": rel(stiff, t), "frames": 6,
       "x": round(-(NECK_S3[0] - 0.5) * 22, 2), "y": round(-(NECK_S3[1] - 0.5) * 22, 2)}, cap=TOP,
       fx=[{"kind": "glint", "x": LANCET_S3[0], "y": LANCET_S3[1], "at": rel(men, t), "size": 24}])
# (no PERSIA card: it collided with the caption, and Liam says it; text check 2026-11-15)
c.s("water-drip", t)
# the standard cure: the lancet lifted (glint runs along the blade on "vein")
t = c.at("the standard cure")
vein = c.at("vein")
c.shot(t, KF + "s3b.png", push(BLADE_S3B[0], BLADE_S3B[1], 1.18), cap=TOP,
       fx=[{"kind": "glint", "x": BLADE_S3B[0], "y": BLADE_S3B[1], "at": rel(vein, t), "size": 30}])
c.s("glass-clink", vein)
# B3 THE CHOICE: his doubt
# rough cut 2 review (user): "the climax is too rushed": 7a moved here (his pen writing -> the pen stops in s4), so the
# twist after the climax has two calm shots instead of four short ones
t = c.at("but alrazi")
had = c.at("had a doubt")
c.shot(t, KF + "s7a.png", push(GLASSES_S7A[0], 0.4, 1.1), cap=MID,   # LOW covered the writing hand; TOP = the glasses
       fx=[{"kind": "glint", "x": GLASSES_S7A[0], "y": GLASSES_S7A[1], "at": 0.9, "size": 24}])
c.s("quill-writing", t)
c.shot(had, KF + "s4.png", push(0.6, 0.3, 1.16), cap=LOW)
c.o("nameTag", had + 0.05, had + 1.8, text="al-Razi", sub="physician of Rey", y=MID)
wi = c.at("what if")   # s4 holds through the question (rough cut 2: fewer, longer shots)
c.s("hit-suspense", wi)
# B4 ESCALATION: he splits the ward (whip in), then the two groups down the hall
t = c.at("so he split")
c.shot(t, KF + "s5a.png", push(0.45, 0.45, 1.1), cap=TOP, transition="whip")   # LOW sat on his turban
c.s("whoosh", t - 0.05); c.s("cloth-rustle", t + 0.1)
t = c.at("one group he bled")
oth = c.at("the other")
# s5b and s6 share one camera (curtain at x 0.5, same arches): s5b ENDS on the zoom s6 STARTS with, and s6 dissolves in,
# so al-Razi and Matt fade in on the spot (user: "the cut is a jump ... same zoom on the cut and apply a fade")
MATCH_ZOOM = 1.08
c.shot(t, KF + "s5b.png", {"type": "push", "from": 1.02, "to": MATCH_ZOOM, "x": 2, "y": 0}, cap=TOP,   # x 2: curtain 0.49 -> s6's 0.51
       fx=[{"kind": "spot", "cx": ROW_A[0], "cy": ROW_A[1], "rx": 0.2, "ry": 0.3, "at": 0.05, "dur": rel(oth, t) - 0.1, "dim": 0.5},
           {"kind": "spot", "cx": ROW_B[0], "cy": ROW_B[1], "rx": 0.2, "ry": 0.3, "at": rel(oth, t), "dur": 1.8, "dim": 0.5}])
c.o("stamp", t + 0.1, oth - 0.05, text="A", y=MID, x=int(ROW_A[0] * 1080))
c.o("stamp", oth, oth + 1.8, text="B", y=MID, x=int(ROW_B[0] * 1080))
c.s("stamp-thud", t + 0.1); c.s("stamp-thud", oth)
# B5 CLIMAX: he waits and watches, in silence (music gap)
wait = c.at("then he waited")
c.shot(wait, KF + "s6.png", {"type": "push", "from": MATCH_ZOOM, "to": 1.12, "x": 0, "y": 0}, cap=TOP, darken=0.3,
       transition="dissolve")  # LOW: "BOTH" on his turban  # night
# (no fire-crackle here: with the music down its crackle read as noise, user 2026-11-15)
# B6 TWIST: dawn, a bled patient sits up; he writes; he keeps the cure; he was wrong
bled = t = c.at("the bled group")
c.shot(t, KF + "s6b.png", push(0.45, 0.55, 1.1), cap=TOP)
c.s("crickets-field", t)   # klankbeeld 'calm forest morning' (CC-BY): birds at dawn only (user: no birds at night)
t = c.at("so he kept")
c.shot(t, KF + "s7b.png", {"type": "snap", "from": 1.03, "to": 1.18, "at": 0.0, "frames": 5}, cap=TOP)
c.s("metal-clank", t + 0.2, query="small metal bowl set down")
wrong = c.at("he was wrong")
c.shot(wrong, KF + "s8.png", push(0.48, 0.52, 1.1), cap=TOP, hit={"at": 0.3, "strength": 3},
       fx=[{"kind": "tint", "at": 0.25, "dur": 0.6, "from": "rgba(128,128,128,0)", "to": "rgba(128,128,128,0.6)",
            "blend": "saturation"}])
c.o("stamp", wrong + 0.3, wrong + 1.6, text="WRONG", y=MID)
c.s("buzzer-wrong", wrong + 0.3)
# B7 RESONANCE: wrong answer, right method (bottle groups measured at x 0.35 and 0.67, y 0.53)
ans = c.at("his answer")
meth = c.at("his method")
c.shot(ans, KF + "s1b.png", {"type": "pull", "from": 1.12, "to": 1.03}, cap=TOP)   # his knowing face: answer wrong...
c.shot(meth - 0.3, KF + "s9b.png", {"type": "pull", "from": 1.14, "to": 1.03}, cap=TOP)   # ...method right
c.o("stamp", meth + 0.6, meth + 4.0, text="A", y=780, x=378)
c.o("stamp", meth + 0.9, meth + 4.0, text="B", y=780, x=724)
c.s("glass-clink", meth + 0.6)
# rough cut 2 review: no hard stop. The music fades slowly into the waiting and comes back slowly with the dawn;
# it keeps playing under "He was wrong" (the stamp and the buzzer carry that beat).
MUSIC_GAPS = [{"from": round(wait - 0.1, 2), "to": round(bled - 0.2, 2), "fade_out": 1.2, "fade_in": 2.0, "level": 0.25}]

HITS = {"stamp-thud", "glass-clink", "hit-suspense", "quill-writing", "metal-clank", "buzzer-wrong", "whoosh"}
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
    "m1": {"sections": 3, "prompt": "Instrumental Persian classical music in dastgah Shur for a true story about a "
           "10th-century physician: santur and setar, a breathy ney flute, soft daf and tombak; curious and careful, a "
           "playful, slightly mischievous turn near the end, then a calm close. No Western orchestra, no vocals, no "
           "modern drums, no synths."}}}
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(c.shots)} shots, {len(c.ov)} overlays, {len(c.fx)} sfx, {total} s")
