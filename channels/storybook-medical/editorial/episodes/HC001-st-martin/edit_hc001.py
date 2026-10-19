"""HC001-L edit: shot-plan.md section B as a timeline. Every shot starts on the word its script line starts with (found
in Liam's timed narration), so the picture changes on the words. Writes shots / overlays / sfx / music cues into
episode.json; then: episode.py build -> mix -> render."""
import json
import re
from pathlib import Path

PID = "hc001-window-into-his-stomach"
P = Path("projects") / PID
ep = json.load(open(P / "episode.json", encoding="utf-8"))
words = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
chapters = {c["id"]: c for c in json.load(open(P / "artifacts/chapters.json", encoding="utf-8"))}
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
toks = [norm(w["word"]) for w in words]
cursor = 0


def at(phrase: str) -> float:
    """Start time of the next occurrence of `phrase` (from the cursor on): the shot cuts here."""
    global cursor
    want = [norm(x) for x in phrase.split()]
    for i in range(cursor, len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            cursor = i + 1
            return round(words[i]["start"] - 0.05, 2)
    raise SystemExit(f"phrase not found after word {cursor}: {phrase!r}")


def end_of(phrase: str) -> float:
    global cursor
    want = [norm(x) for x in phrase.split()]
    for i in range(cursor, len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want:
            return round(words[i + len(want) - 1]["end"], 2)
    raise SystemExit(f"phrase not found: {phrase!r}")


KF = lambda n: f"kf:{n}"
CLIP = lambda n: f"proj:assets/video/{n}.mp4"
push, pull, static = {"type": "push"}, {"type": "pull"}, {"type": "static"}
shots, overlays, sfx = [], [], []


def shot(sid, start, source, motion=push, **kw):
    shots.append({"id": sid, "start": start, "source": source, "motion": motion, **kw})


def ov(kind, start, end, **kw):
    overlays.append({"kind": kind, "start": round(start, 2), "end": round(end, 2), **kw})


def fx(name, t, gain=-14, **kw):
    sfx.append({"name": name, "at": round(t, 2), "gain_db": gain, **kw})


ch = lambda cid: chapters[cid]["start"]
CHAPTER_NAMES = {"ch1": "The Case", "ch2": "What Happened Next", "ch3": "The Science, 1825", "ch4": "The Experiments",
                 "ch5": "The Human Experiment", "ch6": "What They Learned", "ch7": "The Myth vs the Record",
                 "ch8": "The Last Word", "ch9": "Why It Matters"}

# ── 0 · cold open ──
shot("L01", 0.0, KF("I01"))
t = at("then he lowers"); shot("L02", t, CLIP("C1"), static, use=2.5)
shot("L02b", round(t + 2.5, 2), KF("I02"), push)
t = at("he checks his watch"); shot("L03", t, KF("I03a"), static)
ov("clock", t, at("half the food") , cx=52.8, cy=54.6, r=252, **{"from": 12.0, "to": 13.0, "at": 1.4, "spin": 1.6})
fx("tick-click", t + 0.2, -20); fx("watch-ticking", t + 0.3, -24, dur=2.5)
shot("L04", at_l4 := round(overlays[-1]["end"], 2), KF("I04"), static)
fx("ding-correct", at_l4 + 0.35, -20)
shot("L05", at("and the man"), KF("M02"), {"type": "slide", "from": -2, "to": 2, "scale": 1.12})
shot("L06", at("nobody cut him open"), KF("M02"), {"type": "push", "from": 1.12, "to": 1.32, "x": 8, "y": 2})
sting = round(chapters["ch0"]["end"] + 0.15, 2)
shot("STING", sting, "brand:sting.mp4", static)
sfx.append({"file": "brand:sting.mp4", "at": sting, "as_is": True, "dur": 1.8})
title_at = round(sting + 1.8, 2)
shot("L07", title_at, KF("M03"), {"type": "push", "from": 1.04, "to": 1.12}, transition="dissolve")
ov("title", title_at + 0.2, ch("ch1") + 0.4, text="The Man With a Window Into His Stomach", sub="AN ODDLY MATT STORY")

# ── 1 · The Case ──
ov("chapter", ch("ch1") + 0.6, ch("ch1") + 3.4, n=1, text=CHAPTER_NAMES["ch1"])
ov("location", ch("ch1") + 0.6, ch("ch1") + 4.0, text="MACKINAC ISLAND", sub="1822")
t = at("every summer"); shot("L09", t, CLIP("C8"), static); fx("canoe-paddle", t, -24, dur=4)
t = at("one of them is alexis"); shot("L10", t, KF("M05"), {"type": "slide", "from": 2, "to": -2, "scale": 1.12})
ov("nameTag", t + 0.3, t + 4.5, text="Alexis St. Martin", sub="voyageur, about 18")
shot("L11", at("of june"), KF("I06"), push)
t = end_of("fired from less than a meter away")
fx("musket-shot", t - 0.35, -10)
shot("L13", at("the army surgeon at the fort"), CLIP("C3"), static, transition="flash")
ov("nameTag", shots[-1]["start"] + 0.4, shots[-1]["start"] + 4.4, text="Dr. William Beaumont", sub="U.S. Army surgeon")
shot("L14", at("what he sees is"), KF("M08"), push)
shot("L15", at("by every rule of"), KF("M08"), {"type": "pull", "from": 1.25, "to": 1.05})
shot("L16", at("he does"), KF("M09"), {"type": "push", "from": 1.2, "to": 1.3, "x": 10, "y": 3})

# ── 2 · What Happened Next ──
ov("chapter", ch("ch2") + 0.1, ch("ch2") + 2.8, n=2, text=CHAPTER_NAMES["ch2"])
t = at("everything he swallows"); shot("L17", round(ch("ch2"), 2), KF("M09"), static)
ov("counter", t, t + 3.2, to=17, label="DAYS", **{"from": 1})
shot("L18", at("then slowly he gets"), KF("M09"), pull)
shot("L19", at("beaumont spends"), KF("M10"), push, transition="dissolve")
shot("L20", at("theres one option left"), KF("I07"), push); fx("tick-click", shots[-1]["start"] + 0.6, -22)
t = at("alexis says no"); shot("L21", t, KF("M11"), static)
ov("stamp", t + 0.5, t + 2.2, text="NO", color="oxblood"); fx("stamp-thud", t + 0.55, -14)
shot("L22", at("we dont know his reasons"), KF("I07"), {"type": "push", "from": 1.15, "to": 1.3})
shot("L23", at("so his body found"), KF("I19"), push)
shot("L24", at("and beaumont"), KF("M12"), {"type": "push", "from": 1.04, "to": 1.2, "x": -6})

# ── 3 · The Science, 1825 ──
ov("chapter", ch("ch3") + 0.1, ch("ch3") + 2.8, n=3, text=CHAPTER_NAMES["ch3"])
shot("L25", round(ch("ch3"), 2), KF("M13"), static)
shot("L26a", at("some said it grinds"), KF("I20"), static)
shot("L26b", at("others said food"), KF("I21"), static)
shot("L27", at("to settle it"), KF("M12"), {"type": "push", "from": 1.1, "to": 1.3, "x": 12}, focus=0.7)
shot("L28", at("beaumont had no laboratory"), KF("M14"), pull)
t = at("what he had"); shot("L29", t, CLIP("C5"), static, use=2.0); fx("axe-chop", t + 0.85, -12)
shot("L29b", round(t + 2.0, 2), KF("M15"), {"type": "push", "from": 1.04, "to": 1.1})

# ── 4 · The Experiments ──
ov("chapter", ch("ch4") + 0.1, ch("ch4") + 2.8, n=4, text=CHAPTER_NAMES["ch4"])
shot("L30", round(ch("ch4"), 2), KF("I08"), static)
t = at("hours the cabbage"); shot("L31", t, KF("I05"), static)
ov("quote", t + 1.4, t + 6.0, text="cleanly digested, and gone from the string", source="William Beaumont, 1833"); fx("paper-slide", t + 1.4, -20)
shot("L32", at("the next day alexis"), KF("I09"), {"type": "tilt", "from": -4, "to": 4})
shot("L33", at("no forms"), KF("M16"), static)
t = at("then he went further"); shot("L34", t, CLIP("C6"), static); fx("fire-crackle", t, -26, dur=5)
shot("L35", at("the meat dissolved"), KF("I10"), push)
shot("L36", at("a clear slightly salty"), KF("I22"), push)
t = at("and yes"); shot("L37", t, KF("I11"), push)
ov("stamp", at("beaumont wrote that he put"), at("empty no acid") , text="HIS OWN WORDS", color="amber")
shot("L38", at("he also noted"), KF("M18"), static)
t = at("in the end there would be"); shot("L39", t, KF("I12"), pull)
ov("counter", t + 0.8, t + 4.6, to=238, label="EXPERIMENTS", countSeconds=2.2); fx("tick-click", t + 0.8, -20)
shot("L40", at("but beaumonts experiment"), KF("M19"), push)

# ── 5 · The Human Experiment ──
ov("chapter", ch("ch5") + 0.1, ch("ch5") + 2.8, n=5, text=CHAPTER_NAMES["ch5"])
t = round(ch("ch5"), 2); shot("L41", t, "ref:plate-map", static)
ov("route", t + 0.5, t + 7.0, points=[[37, 40], [52, 30], [66, 22], [74, 18]], label="BACK TO CANADA", drawSeconds=3)
t = at("without obtaining my consent")
ov("quote", t - 0.2, t + 3.6, text="without obtaining my consent", source="William Beaumont, 1833")
shot("L42", at("years he lived"), KF("M20"), {"type": "slide", "from": 2, "to": -2, "scale": 1.12})
t = at("then in 1829") if "1829" in toks else at("fur company agents")
shot("L43", t, CLIP("C4"), static); fx("canoe-paddle", t, -24, dur=5)
t = at("nearly"); ov("counter", t, t + 3.0, to=2000, label="MILES", countSeconds=1.6)
t = at("at great expense"); shot("L44", t, KF("M21m"), static)
ov("quote", t, t + 3.2, text="At great expense to me", source="William Beaumont, 1833")
shot("L45", at("between experiments alexis"), KF("M15"), push)
t = at("the family left again"); shot("L46", t, "ref:plate-map", static)
ov("route", t + 0.3, t + 8.5, points=[[23, 74], [26, 60], [40, 58], [47, 48], [58, 42], [70, 34], [78, 26]],
   label="HOME TO MONTREAL", drawSeconds=6)
shot("L47", at("think about that"), KF("M21"), pull)
shot("L48", at("the next year cholera"), KF("M22"), static)
shot("L49", at("he was back with beaumont"), KF("M23"), push)
t = at("and there was a contract"); shot("L50", t, KF("I13"), {"type": "push", "from": 1.1, "to": 1.25, "y": 6}, focus=0.25)
t_made = at("it made him"); t_pay = at("the pay")
ov("quote", t_made, t_pay, text="covenant servant … submit to … experiments … on or in the stomach",
   highlight="on or in the stomach", source="Contract, 19 October 1833"); fx("paper-slide", overlays[-1]["start"], -20)
t = t_pay; ov("stamp", t + 0.8, t + 3.6, text="$150 / YEAR", color="amber"); fx("stamp-thud", t + 0.85, -16)
shot("L51", at("alexis couldnt read it"), KF("M24"), push)
shot("L53", at("his comrades"), KF("M25"), static)
shot("L54", at("a letter came from canada"), KF("M26"), static)
shot("L55", at("he never worked for beaumont"), KF("M26"), pull)
shot("L56", at("beaumont never stopped trying"), KF("M27"), push)

# ── 6 · What They Learned ──
ov("chapter", ch("ch6") + 0.1, ch("ch6") + 2.8, n=6, text=CHAPTER_NAMES["ch6"])
t = round(ch("ch6"), 2); shot("L57", t, KF("I11"), static)
ov("quote", t + 2.8, t + 9.5, text="Experiments and Observations on the Gastric Juice, and the Physiology of Digestion",
   source="William Beaumont, Plattsburgh, 1833")
shot("L58", at("doctors in europe"), KF("I14"), push)
t = at("beaumont kept writing"); shot("L59", t, KF("M27"), static)
ov("stack", t + 0.2, t + 4.6, items=["1836", "1837", "1838", "1839", "1840", "1842", "1846", "1851", "1852"], every=0.38)
for i in range(9):
    fx("paper-slide", t + 0.2 + i * 0.38, -26)
shot("L60", at("he sent his own son"), KF("M28"), {"type": "slide", "from": -2, "to": 2, "scale": 1.12})
t = at("offered"); shot("L61", t, KF("M27"), {"type": "push", "from": 1.1, "to": 1.2})
ov("counter", t + 0.3, t + 3.4, to=500, prefix="$", label="A YEAR", countSeconds=1.0, **{"from": 150})
t = at("his last letter ends"); shot("L62", t, KF("M27"), {"type": "push", "from": 1.2, "to": 1.35, "x": -8})
ov("quote", t + 1.0, t + 4.6, text="Don't disappoint me more.", source="William Beaumont, 15 October 1852")
shot("L63", at("months later beaumont"), KF("M29"), static)
shot("L64", at("alexis outlived him"), KF("M30"), pull)

# ── 7 · The Myth vs the Record ──
ov("chapter", ch("ch7") + 0.1, ch("ch7") + 2.8, n=7, text=CHAPTER_NAMES["ch7"])
shot("L65", round(ch("ch7"), 2), KF("M01"), static, darken=0.25)
t = at("it wasnt a shotgun"); shot("L66", t, KF("I06"), static, darken=0.35)
ov("stamp", t + 0.3, t + 3.4, strike="SHOTGUN", text="MUSKET"); fx("stamp-thud", t + 1.0, -14)
t = at("alexis wasnt a fur trader"); shot("L67", t, KF("M04"), static, darken=0.3)
ov("stamp", t + 0.3, t + 4.8, strike="FUR TRADER", text="VOYAGEUR"); fx("stamp-thud", t + 1.0, -14)
t = at("the wound never healed"); shot("L68", t, KF("I19"), static, darken=0.3)
ov("stamp", t + 0.3, t + 4.6, strike="NEVER HEALED", text="HE SAID NO"); fx("stamp-thud", t + 1.0, -14)
shot("L69", at("even the library"), KF("M12"), {"type": "push", "from": 1.05, "to": 1.3, "x": -10})
t = at("and the strangest bit"); shot("L70", t, KF("I11"), static)
t = at("that ones true"); ov("stamp", t, t + 2.6, text="TRUE", color="amber"); fx("stamp-thud", t + 0.05, -14)
shot("L71", at("even alexiss age"), KF("M30"), static)
shot("L72", at("which brings us"), KF("M30"), {"type": "push", "from": 1.05, "to": 1.4})

# ── 8 · The Last Word ──
ov("chapter", ch("ch8") + 0.1, ch("ch8") + 2.8, n=8, text=CHAPTER_NAMES["ch8"])
shot("L73", round(ch("ch8"), 2), KF("M31"), static)
t = at("a young doctor in montreal"); shot("L74", t, KF("M32"), push)
ov("nameTag", t + 0.5, t + 4.5, text="Dr. William Osler", sub="Montreal, 1880")
shot("L75", at("the family said no"), KF("M32"), static)
shot("L76", at("according to the parish priest"), KF("M33"), push)
shot("L77", at("so that nobody"), KF("M34"), {"type": "pull", "from": 1.15, "to": 1.0})

# ── 9 · Why It Matters ──
ov("chapter", ch("ch9") + 0.1, ch("ch9") + 2.8, n=9, text=CHAPTER_NAMES["ch9"])
shot("L78", round(ch("ch9"), 2), KF("I01"), push)
t = at("it came from a man"); shot("L79", t, CLIP("C7"), static); fx("canoe-paddle", t, -24, dur=5)
shot("L80", at("medicine owes a lot"), KF("I17"), static)
shot("L81", at("and alexis wasnt the last"), KF("I18"), push)
outro = round(words[-1]["end"] + 0.9, 2)
shot("OUTRO", outro, "brand:sting-outro.mp4", static)
sfx.append({"file": "brand:sting-outro.mp4", "at": outro, "as_is": True, "dur": 1.8})
shot("END", round(outro + 1.8, 2), "brand:endscreen.mp4", static)
END = round(outro + 1.8 + 20.0, 2)

# clips: a trimmed clip continues as a still of its own source frame
src_of = {c: ep["clips"][c]["source"] for c in ep["clips"]}
shots.sort(key=lambda s: s["start"])
final = []
for i, s in enumerate(shots):
    nxt = shots[i + 1]["start"] if i + 1 < len(shots) else END
    s["end"] = round(nxt, 2)
    use = s.pop("use", None)
    m = re.match(r"proj:assets/video/(C\d+)\.mp4", s["source"])
    clip_len = use or 5.0
    if m and s["end"] - s["start"] > clip_len + 0.05 and not any(x["start"] == round(s["start"] + clip_len, 2) for x in shots):
        hold = {"id": s["id"] + "h", "start": round(s["start"] + clip_len, 2), "end": s["end"],
                "source": KF(src_of[m.group(1)]), "motion": {"type": "push", "from": 1.0, "to": 1.06}}
        s["end"] = hold["start"]
        final += [s, hold]
    else:
        final.append(s)
ep["shots"], ep["overlays"], ep["sfx"] = final, sorted(overlays, key=lambda o: o["start"]), sorted(sfx, key=lambda x: x["at"])
ep["music"]["cues"] = [{"track": "mA", "start": 0, "end": ch("ch3")}, {"track": "mB", "start": ch("ch3"), "end": ch("ch5")},
                       {"track": "mC", "start": ch("ch5"), "end": ch("ch7")}, {"track": "mD", "start": ch("ch7"), "end": END}]
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(final)} shots, {len(overlays)} overlays, {len(sfx)} sfx, video {END:.1f}s ({END / 60:.1f} min)")
