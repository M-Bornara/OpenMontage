"""Beat sheet builder (skills/creative/cinematic-production-standard.md §1).

    python beats.py <beats_module.py> <project_id> [--words path/to/word_timestamps.json]

Resolves each beat's KEY words in the timed narration (picture leads by 0.2 s), checks the standard's rules, estimates
the generation cost, and writes:
  projects/<id>/artifacts/beats.json         the timed beats (input of the animatic and later of the edit)
  <beats module dir>/beat-sheet.md           the review table for the user (timing, shot, what we see, source, fx…)
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LEAD = 0.2
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())

# generation cost per source type (USD): 4K stills in the Gemini batch, Kling clips on fal
COST = {"new": 0.12, "props": 0.24, "clip": 0.28 + 0.12, "flf": 0.49 + 0.24}
STILL_LIKE = ("new", "reuse", "callback", "props")
MAX_STILL, MIN_BEAT = 7.0, 1.0
PICTURE = ("new", "clip", "flf", "props")


def auto_transition(prev, b):
    """A change of set is never a plain cut: a jump in time dissolves, a move in place inks or whips (by energy)."""
    if b["trans"] != "cut" or not prev.get("set") or not b.get("set") or prev["set"] == b["set"]:
        return None
    yr = lambda x: int(re.search(r"\d{4}", x["setYear"]).group())
    jump = abs(yr(b) - yr(prev))
    if jump >= 3:  # years pass
        return "dip to black" if b["mood"] <= 1 else "film dissolve"
    if jump >= 1:
        return "light dissolve"
    return "whip" if b["mood"] >= 4 else "ink bleed"  # same time, another place ("cut!" in the sheet keeps a hard cut)


def load(path):
    spec = importlib.util.spec_from_file_location("beats_mod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.BEATS


def build(beats_path: str, pid: str, words_path: str | None = None):
    P = REPO / "projects" / pid
    words = json.load(open(words_path or P / "artifacts/word_timestamps.json", encoding="utf-8"))
    toks = [norm(w["word"]) for w in words]
    beats = load(beats_path)
    cur, problems = 0, []

    def find(phrase):
        nonlocal cur
        want = [norm(x) for x in phrase.split() if norm(x)]
        for i in range(cur, len(toks) - len(want) + 1):
            if toks[i:i + len(want)] == want:
                cur = i + 1
                return i, i + len(want) - 1
        return None

    stage_path = Path(beats_path).with_name(Path(beats_path).name.replace("beats_", "stage_"))
    stages = {}
    if stage_path.exists():
        spec = importlib.util.spec_from_file_location("stage_mod", stage_path)
        sm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sm)
        stages = sm.STAGE
    # sets (place + year + look) per beat: sets_<ep>.py next to the beats module
    sets_path = Path(beats_path).with_name(Path(beats_path).name.replace("beats_", "sets_"))
    SETS, SET_OF = {}, {}
    if sets_path.exists():
        spec = importlib.util.spec_from_file_location("sets_mod", sets_path)
        xm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(xm)
        SETS, SET_OF = xm.SETS, xm.SET_OF
    for b in beats:
        if b["id"] in stages:
            b["stage"] = dict(stages[b["id"]])
        sid = SET_OF.get(b["id"])
        if sid:
            st = SETS[sid]
            b.update(set=sid, setName=st["name"], setYear=st["year"], setLook=st["look"])
            if "stage" in b and st.get("plate"):  # the animatic draws the set's stand-in plate, graded per set
                b["stage"]["bg"] = st["plate"]
                if st.get("tint") and not b["stage"].get("tint"):
                    b["stage"]["tint"] = st["tint"]
        elif SETS and b["src"].split(":")[0] in PICTURE:
            problems.append(f"{b['id']}: a picture beat with no set: name its place + year in sets_*.py")
        hit = find(b["at"])
        if hit is None:
            problems.append(f"{b['id']}: key words not found after the previous beat: {b['at']!r}")
            b["start"] = None
            continue
        i, j = hit
        b["word_start"], b["word_end"] = round(words[i]["start"], 2), round(words[j]["end"], 2)
        b["start"] = 0.0 if not any(x.get("start") is not None for x in beats[:beats.index(b)]) else round(max(0, words[i]["start"] - LEAD), 2)
        if b["src"] == "newline":  # a new narration line goes after the anchor line ends
            b["start"] = round(words[j]["end"] + 0.3, 2)
    end_all = round(words[-1]["end"] + 0.9, 2)
    timed = [b for b in beats if b["start"] is not None]
    for k, b in enumerate(timed):
        t = auto_transition(timed[k - 1], b) if k else None
        if t:
            b["trans"], b["transAuto"] = t, True
        b["end"] = timed[k + 1]["start"] if k + 1 < len(timed) else end_all
        b["dur"] = round(b["end"] - b["start"], 2)
        kind = b["src"].split(":")[0]
        if kind in STILL_LIKE and b["dur"] > MAX_STILL:
            problems.append(f"{b['id']}: still holds {b['dur']}s (> {MAX_STILL}s): split it or add a beat")
        if b["dur"] < MIN_BEAT and kind not in ("trailer",):
            problems.append(f"{b['id']}: only {b['dur']}s on screen: merge it or move its key words")
        if kind in ("clip", "flf") and b["dur"] > 5.2:
            problems.append(f"{b['id']}: clip slot is {b['dur']}s but a clip is 5 s: plan a second image after it (never its own still)")
        m = re.match(r"push>(\w+)|pan:(\w+)>", b["cam"])
        tgt = m and (m.group(1) or m.group(2))
        names = [c.split("@")[0] for c in b["cast"].split()]
        if tgt and tgt not in names and tgt not in ("left", "right"):
            problems.append(f"{b['id']}: camera target '{tgt}' is not placed in the frame (cast: {b['cast'] or 'none'})")
    # a dip / chapter-style transition between two shots of the same picture looks like a glitch: dissolve instead
    for k in range(1, len(timed)):
        a, b = timed[k - 1], timed[k]
        same = a["src"].endswith(":" + b["id"]) or b["src"].endswith(":" + a["id"]) or (a["src"] == b["src"] and a["src"].startswith("reuse:"))
        if same and b["trans"].startswith(("dip", "page", "ink", "film", "light")):
            problems.append(f"{b['id']}: '{b['trans']}' between two shots of the same picture: continue the same frame instead (a dissolve onto the same picture ghosts)")
    # jump cut: a plain cut between two DIFFERENT pictures of the same set where both are wide/medium (the background fills
    # the frame and barely changes, so the subject seems to pop) — dissolve, or change the shot size (user review 2026-10-24)
    for k in range(1, len(timed)):
        a, b = timed[k - 1], timed[k]
        if (b["trans"] == "cut" and a.get("set") and a.get("set") == b.get("set") and a["shot"] in ("WS", "MS", "MWS")
                and b["shot"] in ("WS", "MS", "MWS") and not b["src"].startswith("callback:") and a["src"] != b["src"]):
            problems.append(f"{b['id']}: plain cut {a['shot']}→{b['shot']} inside set {b['set']}: same background, new subject = a jump; "
                            f"'light dissolve' or a different shot size")
    # repeats: the same reused image inside 60 s, unless the beat is a declared callback
    seen = {}
    for b in timed:
        if b["src"].startswith("reuse:"):
            name = b["src"][6:]
            if name in seen and b["start"] - seen[name] < 60:
                problems.append(f"{b['id']}: {name} was on screen {b['start'] - seen[name]:.0f}s ago (repeat): use a callback or a new image")
            seen[name] = b["start"]

    kinds = Counter(b["src"].split(":")[0] for b in timed)
    cost = sum(COST.get(b["src"].split(":")[0], 0) + (COST["new"] if b["src"] == "file:new" else 0) for b in timed)
    trans = Counter(b["trans"].split(" (")[0] for b in timed)
    durs = [b["dur"] for b in timed]
    stats = dict(beats=len(timed), avg=round(sum(durs) / len(durs), 2), longest=max(durs), kinds=dict(kinds), cost=round(cost, 2),
                 transitions=dict(trans.most_common()))
    out = P / "artifacts/beats.json"
    json.dump({"beats": timed, "stats": stats, "problems": problems, "total": end_all}, open(out, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)
    md = review_md(timed, stats, problems)
    sheet = Path(beats_path).with_name("beat-sheet.md")
    sheet.write_text(md, encoding="utf-8")
    print(f"{len(timed)} beats · avg {stats['avg']}s · longest {stats['longest']}s · est. generation ${stats['cost']}")
    print("sources:", dict(kinds))
    for p in problems:
        print("  !", p)
    print("->", out, "|", sheet)
    return timed, stats, problems


def _t(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def review_md(beats, stats, problems):
    bar = lambda m: "▁▂▄▆█"[max(1, min(5, m)) - 1]
    lines = ["# HC001 · Beat sheet v1 (for review)", "",
             f"**{stats['beats']} beats**, on average **{stats['avg']} s** each (longest {stats['longest']} s). "
             f"Estimated generation cost: **${stats['cost']}** (new stills $0.12, clips $0.40 incl. their image, "
             f"first+last-frame clips $0.73, props $0.24; reused / callbacks / maps / graphics are free).", "",
             "Sources: " + ", ".join(f"{k} {v}" for k, v in stats["kinds"].items()), "",
             "Transitions: " + ", ".join(f"{k} {v}" for k, v in stats["transitions"].items()), ""]
    # mood curve per chapter
    lines += ["## Mood curve", "", "```"]
    chap = {}
    for b in beats:
        chap.setdefault(b["id"].split(".")[0], []).append(b["mood"])
    for c, ms in chap.items():
        lines.append(f"ch{c}  " + "".join(bar(m) for m in ms))
    lines += ["```", ""]
    if problems:
        lines += ["## Checks that failed (to fix before the animatic is final)", ""] + [f"- {p}" for p in problems] + [""]
    decisions = [b for b in beats if "NEEDS" in b.get("note", "")]
    if decisions:
        lines += ["## Decisions for you", ""] + [f"- **{b['id']}** ({_t(b['start'])}): {b['note']}. {b['see']}" for b in decisions] + [""]
    used = {}
    for b in beats:
        if b.get("set"):
            used.setdefault(b["set"], [b["setName"], b["setYear"], b["setLook"], []])[3].append(b["id"])
    if used:
        lines += ["## Sets (each image prompt carries its set's look)", "", "| set | place | year | look | beats |", "|---|---|---|---|---|"]
        lines += [f"| {k} | {v[0]} | {v[1]} | {v[2]} | {', '.join(v[3])} |" for k, v in used.items()] + [""]
    lines += ["## Beats", "", "| # | time | s | key words | shot | set | what we see | source | camera | in | fx / life | mood |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for b in beats:
        fx = " · ".join(x for x in (b["fx"], b["life"]) if x)
        tr = b["trans"] + (" *(auto: set change)*" if b.get("transAuto") else "")
        lines.append(f"| {b['id']} | {_t(b['start'])} | {b['dur']} | {b['at']} | {b['shot']} | {b.get('set', '')} | {b['see']} | {b['src']} | {b['cam']} | "
                     f"{tr} | {fx} | {bar(b['mood'])} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    a = sys.argv[1:]
    wp = a[a.index("--words") + 1] if "--words" in a else None
    build(a[0], a[1], wp)
