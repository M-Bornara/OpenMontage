"""HC002-L first full cut (2026-11-25, Mahdi): every row of long-storyboard-v2.md as a timeline on Liam's recorded narration.
Rows start on their row time (artifacts/row_times.json); the stamps, name tags and quote cards start on their key words (found in the timed
narration); Tier A stills get a slow camera move; Tier D clips are rows 49 (Kling) and 19 (Omni) only, frame-blended to 30 fps, and row 65 is
a free evening grade of the row-49 clip. No music (held); sound effects are free placeholders from the channel library.
Writes shots / overlays / sfx / music into projects/hc002-l/episode.json; then:
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/prep_hc002l_cut.py     (free assets, once)
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/edit_hc002l.py
    python channels/storybook-medical/scripts/episode.py build hc002-l  ->  mix hc002-l  ->  render hc002-l --preview
"""
import json
import re
import subprocess
from pathlib import Path

PID = "hc002-l"
P = Path("projects") / PID
ep = json.load(open(P / "episode.json", encoding="utf-8"))
words = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
chapters = {c["id"]: c for c in json.load(open(P / "artifacts/chapters.json", encoding="utf-8"))}
rowt = {int(k): v for k, v in json.load(open(P / "artifacts/row_times.json", encoding="utf-8")).items()}
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
toks = [norm(w["word"]) for w in words]


def rs(r):   # row start
    return rowt[r][0]


def re_(r):  # row end
    return rowt[r][1]


def W(row, phrase, nth=0, lead=0.0):
    """Start time of the nth occurrence of `phrase` inside the row's narration (key-word sync); `lead` shifts it earlier."""
    want = [norm(x) for x in phrase.split()]
    hits = []
    for i in range(len(toks) - len(want) + 1):
        if toks[i:i + len(want)] == want and rs(row) - 0.15 <= words[i]["start"] <= re_(row) + 0.6:
            hits.append(i)
    if len(hits) <= nth:
        raise SystemExit(f"row {row}: {phrase!r} (#{nth}) not found in the narration")
    return round(words[hits[nth]]["start"] - lead, 2)


K = lambda n: f"proj:assets/images/keyframes16x9/{n}.png"
S1 = lambda n: f"projects/hc002-s1/assets/images/keyframes16x9/{n}.png"
REF = lambda n: f"proj:assets/images/refs/{n}.png"
VID = lambda n: f"proj:assets/video/{n}.mp4"
push = lambda a=1.04, b=1.14, x=0, y=0: {"type": "push", "from": a, "to": b, "x": x, "y": y}
pull = lambda a=1.14, b=1.04, x=0, y=0: {"type": "pull", "from": a, "to": b, "x": x, "y": y}
slide = lambda a=-2, b=2, s=1.12: {"type": "slide", "from": a, "to": b, "scale": s}
static = {"type": "static"}
shots, overlays, sfx = [], [], []


def clip_len(name):   # a clip plays at its natural speed and length (review 2026-11-25): the row is cut to its length, never slowed, sped up or frozen
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(P / f"assets/video/{name}.mp4")],
                         capture_output=True, text=True, check=True).stdout.strip()
    return round(float(out), 2)


def keys(cx, cy, a, b, dur):
    """A fixed-centre crop that eases from zoom a to b: window centre (cx, cy) in frame fractions (keys use x = (0.5 - cx) * 100 * scale)."""
    mk = lambda t, sc: {"t": t, "ease": "linear", "scale": sc, "x": round((0.5 - cx) * 100 * sc, 1), "y": round((0.5 - cy) * 100 * sc, 1)}
    return {"type": "keys", "keys": [mk(0, a), mk(round(dur, 2), b)]}


def shot(sid, start, source, motion=None, **kw):
    shots.append({"id": sid, "start": round(start, 2), "source": source, "motion": motion or push(), **kw})


def ov(kind, start, end, **kw):
    overlays.append({"kind": kind, "start": round(start, 2), "end": round(end, 2), **kw})


def fx(name, t, gain=-20, **kw):
    sfx.append({"name": name, "at": round(t, 2), "gain_db": gain, **kw})


ch = lambda cid: chapters[cid]["start"]
CHAPTERS = {"ch1": "The Foreman", "ch2": "What Happened", "ch3": "No Longer Gage", "ch4": "The Myth", "ch5": "The Evidence",
            "ch6": "The Other Side of the World", "ch7": "The Ending", "ch8": "Why It Matters"}
for i in range(1, 9):
    ov("chapter", ch(f"ch{i}") + 0.1, ch(f"ch{i}") + 2.8, n=i, text=CHAPTERS[f"ch{i}"])

# ── 0 · cold open ──
shot("r01", 0.0, S1("s3"), push(1.04, 1.18)); fx("sand-pour", 0.8, -24, dur=2.5)
shot("r02a", rs(2), REF("plate-r2-v2"), push(1.04, 1.12)); fx("crowd-murmur", rs(2), -26, dur=1.5)
shot("r02b", W(2, "glances"), K("row2-glance-v1"), push(1.06, 1.16))
shot("r03", rs(3), S1("s5"), push(1.08, 1.2), transition="flash", hit={"at": 0.15, "strength": 3, "seconds": 0.5}); fx("metal-clank", rs(3) + 0.15, -14)
shot("r04", rs(4), REF("plate-r4"), pull(1.25, 1.05), transition="flash", hit={"at": 0.1, "strength": 4, "seconds": 0.7}); fx("boom-low", rs(4) + 0.1, -10)
shot("r05a", rs(5), K("row5a-lying-v1"), push(1.04, 1.12))
shot("r05b", W(5, "talking"), K("row5b-elbow-v1"), push(1.04, 1.14)); fx("gasp", rs(5) + 0.4, -26)
shot("r06", rs(6), K("row6-textbook-v1"), pull(1.16, 1.04)); fx("paper-slide", rs(6) + 0.2, -22)
shot("r07", rs(7), K("row7-monster-v1"), push(1.04, 1.16), grey={"from": 1.0, "to": 3.2}); fx("riser-drone", rs(7), -26, dur=3.0)
sting = round(chapters["ch0"]["end"] + 0.15, 2)
shot("STING", sting, "brand:sting.mp4", static); sfx.append({"file": "brand:sting.mp4", "at": sting, "as_is": True, "dur": 1.8})
title_at = round(sting + 1.8, 2)
shot("TITLE", title_at, S1("s2b"), push(1.04, 1.1), darken=0.3, transition="dissolve")
ov("title", title_at + 0.2, ch("ch1") + 0.4, text="Phineas Gage: The Story Everyone Gets Wrong", sub="AN ODDLY MATT STORY")

# ── 1 · The Foreman ──
shot("r08", rs(8), K("row8-farm-v1"), slide(-2, 2)); fx("birdsong", rs(8), -26, dur=3.2)
ov("location", W(8, "born", lead=0.2), W(8, "born") + 3.2, text="GRAFTON COUNTY, N.H.", sub="c. 1823")
shot("r09", rs(9), S1("s2b"), keys(0.50, 0.70, 1.9, 2.0, re_(9) - rs(9) + 0.7));   # the crew; the title card holds the wide of this still
fx("metal-clank", rs(9) + 0.3, -26, dur=2.0)
shot("r10", rs(10), S1("s2a"), push(1.04, 1.16, y=2))
shot("r11", rs(11), K("row11-keg-v1"), push(1.04, 1.14)); fx("children-laughing", rs(11) + 2.2, -26, dur=1.5)
ov("quote", W(11, "iron"), re_(11) + 0.3, text="an iron will as well as an iron frame.", source="Harlow, 1868", highlight="iron will")
shot("r12a", rs(12), K("row12a-drill-v1"), push(1.04, 1.12)); fx("metal-clank", rs(12) + 1.6, -20)
shot("r12b", W(12, "pour", lead=0.1), K("row12b-pour-v1"), push(1.04, 1.12)); fx("sand-pour", W(12, "pour"), -18, dur=1.5)
shot("r12c", W(12, "fuse", lead=0.1), K("row12c-fuse-v1"), push(1.04, 1.12)); fx("cloth-rustle", W(12, "fuse"), -20)
shot("r12d", W(12, "pack", lead=0.1), K("row12d-tamp-v1"), push(1.04, 1.12)); fx("metal-ring", W(12, "pack") + 0.2, -22)
shot("r13", rs(13), K("row13-iron-v3redraw"), push(1.02, 1.1)); fx("metal-ring", rs(13) + 1.0, -26)
ov("nameTag", W(13, "three", lead=0.3), W(13, "three") + 4.2, text="3 ft 7 in · 13¼ lb", sub="1.1 m · 6 kg")
shot("r14", rs(14), K("row13-iron-v3redraw"), keys(0.77, 0.52, 2.4, 2.2, re_(14) - rs(14) + 0.7))   # the pointed end
ov("stamp", W(14, "crowbar") - 0.1, re_(14) + 0.3, strike="CROWBAR", text="TAMPING IRON"); fx("stamp-thud", W(14, "crowbar") + 0.5, -14)
shot("r15", rs(15), K("row15-endofcut-v1"), push(1.0, 1.1, x=-4)); fx("crowd-angry", rs(15) + 0.6, -28, dur=1.5)
shot("r16", rs(16), S1("s5"), push(1.3, 1.55, x=3, y=2), hit={"at": 2.2, "strength": 2, "seconds": 0.3}); fx("metal-clank", W(16, "struck"), -16)
ov("quote", W(16, "struck", lead=0.2), re_(16) + 0.3, text="struck fire upon the rock.", source="Harlow", highlight="struck fire")

# ── 2 · What Happened ──
shot("r17", rs(17), K("row17-doc"), push(1.0, 1.1)); fx("boom-low", rs(17) + 0.4, -22)
shot("r18", rs(18), K("row5b-elbow-v1"), push(1.3, 1.45, x=-3)); fx("cloth-rustle", rs(18) + 1.0, -26)
C19 = clip_len("row19-oxcart-omni-v1-1080p30")
shot("r19", rs(19), VID("row19-oxcart-omni-v1-1080p30"), static); fx("horse-carriage", rs(19), -24, dur=C19)
shot("r19d", rs(19) + C19, K("row19-detail"), push(1.0, 1.08))      # the row is longer than its clip: cut to a tight Tier A still of the cart
shot("r20", rs(20), K("row20-stairs-v1"), {"type": "tilt", "from": 4, "to": -4}); fx("footsteps-hall", rs(20), -24, dur=3.0)
shot("r21", rs(21), K("row21-s10-fix"), push(1.02, 1.12)); fx("horse-carriage", rs(21), -26, dur=1.5)
ov("nameTag", W(21, "edward", lead=0.4), re_(21), text="Dr Edward Williams", sub="first doctor on the scene")
shot("r22", rs(22), S1("s11"), push(1.0, 1.1))
ov("quote", rs(22) + 0.1, re_(22) + 0.4, text="Doctor, here is business enough for you.", source="Gage, to Dr Williams (Williams's account)", highlight="business enough")
shot("r23", rs(23), K("row23-harlow-v1"), push(1.04, 1.16)); fx("cloth-rustle", rs(23) + 0.2, -22)
ov("nameTag", W(23, "john", lead=0.3), re_(23) + 0.2, text="Dr John Harlow")
shot("r24", rs(24), K("row24-sickroom-v1"), push(1.02, 1.1)); fx("water-drip", rs(24) + 0.4, -24, dur=3.0)
shot("r25", rs(25), K("row25-candle-v1"), push(1.04, 1.12)); fx("night-wind", rs(25), -30, dur=2.5)
shot("r26", rs(26), K("row26-farmhouse-v1"), push(1.02, 1.12)); fx("door-swing", rs(26), -22); fx("night-wind", rs(26) + 0.6, -30, dur=4.5)
ov("location", rs(26) + 0.4, rs(26) + 3.8, text="LEBANON, N.H.", sub="NOV 1848")
shot("r27", rs(27), K("row27-profile-v2paint"), push(1.02, 1.08))

# ── 3 · No Longer Gage ──
shot("r28", rs(28), K("row28-desk-v1"), push(1.04, 1.14)); fx("quill-writing", rs(28) + 0.3, -24, dur=3.0)
shot("r29", rs(29), K("row29-doorway-v1-flip"), push(1.02, 1.1), grey={"from": 0.4, "to": 3.0})
ov("quote", W(29, "fitful", lead=0.2), W(29, "impatient", lead=0.1), text="fitful, irreverent,", source="Harlow, 1868", highlight="irreverent")
ov("quote", W(29, "impatient", lead=0.2), W(29, "grossest", lead=0.1), text="impatient of restraint,", source="Harlow, 1868", highlight="restraint")
ov("quote", W(29, "grossest", lead=0.2), re_(29) + 0.3, text="the grossest profanity.", source="Harlow, 1868", highlight="grossest profanity")
shot("r30", rs(30), K("row30-s12-fix"), push(1.0, 1.08), grey={"from": 0.8, "to": 3.0}); fx("whisper", rs(30) + 0.2, -22)
ov("quote", W(30, "longer", lead=0.3), re_(30) + 0.3, text="no longer Gage.", source="his friends, via Harlow", highlight="no longer Gage")
shot("r31", rs(31), K("row31-gate-v1"), push(1.04, 1.14)); fx("gate-clank", W(31, "couldnt"), -20)
shot("r32", rs(32), K("row32-rim-v1"), pull(1.16, 1.02)); fx("metal-clank", rs(32) + 0.4, -30, dur=2.0)
shot("r33", rs(33), K("row6-textbook-v1"), push(1.0, 1.08), transition="dissolve"); fx("paper-slide", rs(33), -22)

# ── 4 · The Myth ──
shot("r34", rs(34), K("row7-monster-v1"), keys(0.50, 0.50, 1.3, 1.4, re_(34) - rs(34) + 0.7)); fx("riser-drone", rs(34), -26, dur=3.0)
shot("r35", rs(35), K("row7-monster-v1"), keys(0.56, 0.36, 2.3, 2.45, re_(35) - rs(35) + 0.7))   # the eye
for k, wd in enumerate(("violent", "drunk", "liar", "drifter")):
    t0 = W(35, wd, lead=0.05)
    ov("stamp", t0, t0 + (1.2 if wd == "drifter" else 0.75), text=wd.upper(), color="oxblood"); fx("stamp-thud", t0 + 0.04, -14)
shot("r36a", rs(36), K("row36a-oldbook-v1"), push(1.02, 1.1))
shot("r36b", W(36, "textbooks", lead=0.1), K("row36b-textbook-v2crop"), push(1.0, 1.06)); fx("paper-slide", W(36, "textbooks"), -22)
shot("r36c", W(36, "popular", lead=0.1), K("row36c-paperback-v2ink"), push(1.0, 1.06)); fx("paper-slide", W(36, "popular"), -22)
shot("r37", rs(37), K("row37-reports-v1"), push(1.02, 1.1)); fx("paper-slide", rs(37) + 0.5, -24)
ov("nameTag", W(37, "malcolm", lead=0.3), re_(37), text="Malcolm Macmillan", sub="psychologist")
shot("r38", rs(38), K("row38-slips-v1"), push(1.02, 1.12)); fx("wood-pile-fall", rs(38), -26)
shot("r39", rs(39), K("row7-monster-v1"), keys(0.50, 0.62, 2.1, 1.5, re_(39) - rs(39) + 0.7), grey={"from": 0.0, "to": 0.1}); fx("quill-writing", rs(39) + 0.5, -26, dur=3.0)
ov("quote", W(39, "aggressive", lead=0.3), re_(39) + 0.3, text="aggressive and boastful dissipated drunken bully.",
   source="Macmillan, 2008, on how modern writers portray Gage", highlight="drunken bully")
shot("r40", rs(40), K("row36b-textbook-v2crop"), push(1.04, 1.14)); fx("paper-crumple", rs(40) + 2.2, -20)

# ── 5 · The Evidence ──
shot("r41", rs(41), K("row41-boston-v2-flip"), push(1.02, 1.12)); fx("crowd-murmur", rs(41), -28, dur=3.5); fx("chair-scrape", rs(41) + 1.4, -26)
ov("location", rs(41) + 0.2, rs(41) + 3.4, text="BOSTON", sub="1849–50")
shot("r42", rs(42), K("row42-barnum-v2paint"), push(1.02, 1.1)); fx("crowd-murmur", rs(42), -26, dur=3.5)
ov("location", rs(42) + 0.2, rs(42) + 3.4, text="NEW YORK")
shot("r43a", rs(43), K("row43a-shelf-v1"), push(1.02, 1.08))
shot("r43b", W(43, "then", lead=0.1), K("row43b-shelf-v1paint"), push(1.02, 1.08), cut="same-camera cut intended")   # the iron is gone: the locked frame is the point
fx("glass-clink", W(43, "then"), -20)
shot("r44", rs(44), K("row44-bedside-v1"), push(1.02, 1.1)); fx("watch-ticking", rs(44), -30, dur=3.0)
ov("quote", W(44, "constant", lead=0.3), re_(44) + 0.3, text="constant companion.", source="Harlow", highlight="constant companion")
shot("r45", rs(45), K("row45-stable-v2"), push(1.02, 1.12)); fx("horse-carriage", rs(45), -26, dur=4.0)
ov("location", rs(45) + 0.2, rs(45) + 3.6, text="HANOVER, N.H.", sub="1850s")
shot("r46", rs(46), K("row46-stabledoors-v1"), push(1.02, 1.08), transition="dissolve"); fx("door-swing", rs(46) + 0.6, -22)

# ── 6 · The Other Side of the World ──
shot("r47", rs(47), K("row47-map"), static)
# the route in % of the map plate (lon -165..38, lat 62S..52N, as prep_hc002l_cut.py draws it): a schematic sea route round Cape Horn
ROUTE = [(42.4, -71.0), (34, -68), (20, -58), (5, -40), (-10, -31), (-25, -40), (-40, -52), (-52, -58), (-56.5, -67.3), (-55, -72), (-45, -77.5), (-36, -74.5), (-33.05, -71.6)]
ov("route", rs(47) + 0.15, rowt[48][0] + 0.2, points=[[round((lo + 165) / 203 * 100, 1), round((52 - la) / 114 * 100, 1)] for la, lo in ROUTE],
   label="BOSTON → VALPARAÍSO", schematic="SCHEMATIC ROUTE · NOT A RECORDED TRACK", drawSeconds=4.0)
ov("location", rs(47) + 0.1, rs(47) + 2.6, text="VALPARAÍSO"); fx("ship-bell", rs(47) + 0.1, -22)
# ship ambience in the 3.6 s pause after "He went to Chile." (pad_hc002l.py); library cues, untuned
fx("gulls-water", rs(47) + 0.9, -27, dur=3.6); fx("rope-creak", rs(47) + 1.3, -26, dur=3.0)
shot("r48", rs(48), K("row48-valparaiso-v1"), slide(-2, 2, 1.1)); fx("gulls-water", rs(48), -24, dur=3.7); fx("rope-creak", rs(48) + 0.5, -30, dur=2.0)
C49 = clip_len("row49-coach-kling-1080p30")
shot("r49", rs(49), VID("row49-coach-kling-1080p30"), static); fx("horse-carriage", rs(49), -22, dur=5.5)
shot("r49d", rs(49) + C49, K("row49-detail"), push(1.0, 1.08))      # coach and driver, tight
ov("location", rs(49) + 0.3, rs(49) + 3.8, text="VALPARAÍSO – SANTIAGO")
shot("r50", rs(50), K("row50-reins-v1"), push(1.04, 1.14)); fx("rope-creak", rs(50), -24, dur=3.5)
shot("r52", rs(52), K("row52-innyard-v1-flip"), push(1.02, 1.1))
ov("quote", W(52, "surprisingly", lead=0.5), re_(52), text="a surprisingly good psychosocial adaptation.", source="Macmillan & Lena, 2010", highlight="surprisingly good")
shot("r53", rs(53), K("row53-innhearth-v1-flip"), push(1.02, 1.12)); fx("tavern-laughter", rs(53), -28, dur=5.0); fx("fire-crackle", rs(53), -28, dur=5.0)
shot("r54a", rs(54), K("row54a-caseclosed-v1"), push(1.02, 1.1))
shot("r54b", W(54, "photographs", lead=0.1), K("row54b-caseopen-v1"), push(1.02, 1.1), transition="dissolve"); fx("watch-snap", W(54, "photographs"), -18)
shot("r55", rs(55), K("row55-portrait-v4paint"), push(1.02, 1.14))
ov("nameTag", rs(55) + 0.2, re_(55) + 0.2, text="after the Wilgus daguerreotype")
shot("r56", rs(56), K("row55-portrait-v4paint"), keys(0.49, 0.40, 2.0, 2.15, re_(56) - rs(56) + 0.7))   # the face
ov("quote", W(56, "exploded", lead=0.3), W(56, "exploded") + 2.6, text="exploded", source="S. Kean, Slate, 2014", highlight="exploded")
shot("r57", rs(57), K("row57-split"), push(1.0, 1.08), transition="dissolve")

# ── 7 · The Ending ──
shot("r58", rs(58), K("row58-deck-v3"), slide(2, -2)); fx("gulls-water", rs(58), -30, dur=5.0)
ov("location", rs(58) + 0.1, rs(58) + 3.4, text="SAN FRANCISCO")
shot("r59", rs(59), K("row59-field-v1"), slide(-2, 2)); fx("desert-wind", rs(59), -26, dur=5.5)
ov("location", rs(59) + 0.4, rs(59) + 3.8, text="CALIFORNIA")
shot("r60", rs(60), K("row60-porch-v2"), push(1.02, 1.1)); fx("crickets-field", rs(60), -24, dur=4.0)
shot("r61", rs(61), K("row61-letter-v1"), push(1.04, 1.12)); fx("paper-slide", rs(61) + 0.4, -24)
shot("r62", rs(62), K("row62-doorstep-v1"), push(1.02, 1.1)); fx("door-knock", rs(62), -20); fx("door-swing", rs(62) + 0.9, -22)
shot("r63", rs(63), K("row63-case-v1"), push(1.0, 1.1)); fx("machine-hum", rs(63), -30, dur=3.5)
ov("location", rs(63) + 0.2, rs(63) + 3.4, text="BOSTON")

# ── 8 · Why It Matters ──
shot("r64", rs(64), K("row64-lecture-v2"), push(1.02, 1.16, x=-4)); fx("tick-click", rs(64) + 2.0, -22)
C65 = clip_len("row65-evening-from49")
shot("r65", rs(65), VID("row65-evening-from49"), static); fx("horse-carriage", rs(65), -30, dur=C65)
shot("r65d", rs(65) + C65, K("row65-detail"), push(1.0, 1.08))      # the team, tight
shot("r66a", rs(66), K("row55-portrait-v4paint"), keys(0.46, 0.72, 2.1, 2.2, W(66, "coach", lead=0.2) - rs(66)))   # the hand on the iron
shot("r66b", W(66, "coach", lead=0.2), K("row50-reins-v1"), push(1.04, 1.12), transition="dissolve")
shot("r67", rs(67), K("row55-portrait-v4paint"), push(1.0, 1.12))   # the whole case, wide
outro = round(words[-1]["end"] + 0.9, 2)
shot("OUTRO", outro, "brand:sting-outro.mp4", static); sfx.append({"file": "brand:sting-outro.mp4", "at": outro, "as_is": True, "dur": 1.8})
shot("END", round(outro + 1.8, 2), "brand:endscreen.mp4", static)
END = round(outro + 1.8 + 20.0, 2)

# clips shorter than their slot continue as a still of their own last frame ("use" = the clip's length)
shots.sort(key=lambda s: s["start"])
final = []
for i, s in enumerate(shots):
    s["end"] = round(shots[i + 1]["start"] if i + 1 < len(shots) else END, 2)
    s.pop("use", None)
    m = s.get("motion") or {}
    if m.get("type") == "keys":           # the camera must still be moving at the cut: stretch the last key to the slot (+0.4 s)
        m["keys"][-1]["t"] = round(s["end"] - s["start"] + 0.4, 2)
    final.append(s)
ep["shots"], ep["overlays"], ep["sfx"] = final, sorted(overlays, key=lambda o: o["start"]), sorted(sfx, key=lambda x: x["at"])
ep["music"] = {"selected": "silent", "lufs": -85, "prompts": []}      # no music in this cut (held); a near-silent bed keeps the mix step happy
ep["captions"] = True
ep["motion_lint"] = ep["cutout_lint"] = ep["cut_lint"] = "warn"          # first full cut: warn, do not stop
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{len(final)} shots, {len(overlays)} overlays, {len(sfx)} sfx, video {END:.1f}s ({END / 60:.1f} min)")
