"""HC001 real cut: what every beat shows, where the camera goes and where every effect sits, MEASURED on each image
(coordinate-grid review of every still; % of the frame, x then y). Rule (user, 2026-10-20): an effect on an object sits
exactly on that object; a glow sits on its light source. `python cut_hc001.py` writes the cut spec, cuts the effect
masks (rembg BiRefNet inside the measured box) and draws a verification sheet of every anchor and mask.

Spec per beat: img (public path) · cam {target, from, to, panTo, snapAt, centre} · fx [...] · life [...] · clip/morph/sprite.
fx `at` = frames after the beat starts (the beat starts 6 frames before its key word, so at≈6 lands ON the word).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
PUB = REPO / "projects/_fxlab/remotion/public"
OUT = PUB / "cut/cut.json"


def C(target, frm=1.04, to=1.16, **kw):
    return dict(target=list(target), **{"from": frm, "to": to}, **kw)


# ── shots: beat → (image, camera, fx, life, extra) ─────────────────────────────────────────────────────────────
SH = {}


def s(id, img, cam, fx=(), life=(), **kw):
    SH[id] = dict(img=img, cam=cam, fx=list(fx), life=list(life), **kw)


K = "cut/"
# 0 · hook (letterboxed)
s("0.01", None, None, clip="cut/clips/v0.01.mp4")
# 0.02 / 0.04 / 0.06 (user review 2026-10-26: the clips looked AI — food sinking on a still string, Alexis walking back to
# a window): stills under the same timing. 0.02 = a slow dissolve from the beef beside the opening (s0.02a) to the string
# going in (s0.02b) while the camera pushes in; 0.04 = the same dissolve backwards; 0.06 = Alexis toward the real door.
s("0.02", None, C([44, 54], 1.04, 1.14), morph=dict(dir="cut/morph-0.02", n=48))
# the painted dial (scripts/dial_fit.py on keyframes/wI03a.png, in image-space px): the hands pivot on the pin and land on
# the painted hour marks, 12 = the mark under the stem; one steady hour in 2 s (user review 2026-10-26: the old hands spun off-centre and lurched)
WI03A_PIN = [945.3, 544.5]
WI03A_MARKS = [[1046.5, 458.3], [1084.9, 498.6], [1101.1, 555.5], [1075.3, 612.7], [1015.5, 653.1], [941.5, 663.6],
               [873.0, 644.4], [826.2, 600.5], [817.8, 541.8], [855.5, 493.2], [906.9, 455.9], [979.1, 440.6]]
s("0.03", K + "wI03a.jpg", C([50, 52], 1.12, 1.2), [dict(t="clock", pin=WI03A_PIN, marks=WI03A_MARKS, from_=12, to=1, at=6, dur=60),
                                                    dict(t="shine", mask="wI03a-watch", at=30)])
s("0.04", None, C([42, 60], 1.18, 1.06), morph=dict(dir="cut/morph-0.04", n=48))
s("0.05", K + "s0.05.jpg", C([84, 50], 1.04, 1.22, centre=0.6),
  [dict(t="ink", x=85, y=52, rx=8, ry=30, at=8, note="half. gone.", noteAt=[62, 22]), dict(t="shine", mask="s0.05-beef", at=30)])
s("0.06", K + "s0.06.jpg", C([70, 52], 1.12, 1.12, panTo=[84, 52], centre=0.6))
# 0.07 + 0.08: ONE slow pull-back from the opening over both beats (user review 2026-10-24: Beaumont after Beaumont in the
# same room was a jump cut; the opening covers "Nobody cut him open… three years" instead)
s("0.07", K + "s4.07b.jpg", C([49, 73], 2.6, 1.7, centre=1.0))
s("0.08", K + "s4.07b.jpg", None, [dict(t="counter", text=["1822", "1823", "1824", "1825"], at=6, every=12)], cont="0.07")
s("0.10", "img/M21-lake.jpg", C([62, 58], 1.06, 1.14), [dict(t="hand", y=34)],
  sprite=dict(src=K + "prop-canoe-solo-cut.png", x=[66, 60], y=62, w=13, aspect=0.5, flip=True), dark=0.45)
# 1 · the case
s("1.01", K + "s1.01.jpg", C([37, 18], 1.03, 1.14), [dict(t="location", text="MACKINAC ISLAND · 1822", at=50)],
  life=[dict(t="fog", top=50, bottom=75), dict(t="birds", **{"from": [70, 18], "to": [100, 8]}), dict(t="smoke", x=3.5, y=23.4)])
s("1.03", None, None, clip="cut/clips/v1.03.mp4")
s("1.04", K + "s1.04.jpg", C([55, 40], 1.04, 1.14), life=[dict(t="spray", x=88, y=72)])
s("1.05", K + "s1.05.jpg", C([74, 42], 1.03, 1.15),
  [dict(t="callout", name="ALEXIS ST. MARTIN", sub="ABOUT 18 · VOYAGEUR", aside="about to have a very bad summer", x=74, y=36, side="left", at=10),
   # which one is Alexis: his friends dim while the name card is up, and he lights up as it lands
   dict(t="isolate", mask="s1.05-alexis2", at=6, dur=120, soft=True), dict(t="pulse", mask="s1.05-alexis2", at=12, dur=26)])
s("1.05b", K + "s1.05b.jpg", C([58, 42], 1.12, 1.12, panTo=[66, 55], centre=0.6))
s("1.06", K + "s1.06.jpg", C([45, 40], 1.04, 1.18), [dict(t="spot", x=48, y=48, rx=16, ry=26, at=14, dur=80),
                                                       dict(t="date", text="6 JUNE 1822", at=4)],
  life=[dict(t="motes", x=93, y=22)])
s("1.07", K + "wI06.jpg", C([52, 45], 1.03, 1.05, snapAt=4, snapTo=1.3), [dict(t="flash", at=3), dict(t="shake", at=3)])
s("1.08", K + "s1.08.jpg", C([55, 78], 1.04, 1.2, centre=0.55), [dict(t="ink", x=58, y=85, rx=11, ry=8, at=10, note="duck shot", noteAt=[70, 62])],
  life=[dict(t="smoke", x=61, y=70)])
# the distance (user review 2026-10-24: the diagram was too plain): the clerk's musket an arm's length from Alexis; the ruler
# runs under the barrel from Alexis's side to the clerk, its label on "meter"
s("1.09", K + "s1.09c.jpg", C([55, 52], 1.04, 1.14), [dict(t="measure", x0=38, x1=74, y=57, at=4, labelAt=18, text="< 1 m")])
s("1.10", None, None, clip="cut/clips/v1.10.mp4", fx=[dict(t="tag", text="DR. WILLIAM BEAUMONT", sub="ARMY SURGEON", at=12)])
# a steady highlight (user review 2026-10-26: the pulse's growing halo made him look as if he stepped in and back)
s("1.11", K + "s1.11.jpg", C([86, 32], 1.03, 1.14, centre=0.5), [dict(t="lift", mask="s1.11-beaumont", at=8)])
s("1.12", K + "s1.12.jpg", C([38, 22], 1.03, 1.14, centre=0.5), [dict(t="spot", x=38, y=24, rx=16, ry=26, at=10, dur=90)],
  life=[dict(t="glow", x=64.5, y=26.4, r=160)])
s("1.13", K + "s1.13-soft.jpg", C([21, 76], 1.04, 1.28, centre=0.65))
s("1.14", K + "s1.14.jpg", C([66, 70], 1.18, 1.04), [dict(t="isolate", mask="s1.14-alexis3", at=10, dur=999)])
# 1.15 + 1.16 (user review 2026-10-26: the eyes-opening clip gasped "like a fish", and both close-ups sat on the same sharp
# store as the wide shot): the eyes-open still, and a shallow depth of field on both so they read as close-ups
s("1.15", K + "s1.15b.jpg", C([52, 80], 1.06, 1.14), [dict(t="dof", mask="s1.15b-alexis2")])
s("1.16", K + "s1.16.jpg", C([48, 27], 1.04, 1.2), [dict(t="dof", mask="s1.16-beaumont")])
# 2 · what happened next (Mackinac post hospital)
s("2.01", K + "s2.01.jpg", C([80, 60], 1.03, 1.14, centre=0.5), [dict(t="counter", text=[f"DAY {d}" for d in (1, 3, 6, 9, 12, 15, 17)], at=6, every=10)],
  life=[dict(t="glow", x=70, y=55, r=120)])
s("2.02", None, None, clip="cut/clips/v2.02.mp4", use=[0, 3.7])
s("2.03", K + "s2.03.jpg", C([46, 22]))
s("2.04", K + "s2.04.jpg", C([77, 40], 1.03, 1.14, centre=0.5), life=[dict(t="rays", x=14, y=24), dict(t="motes", x=24, y=40)])
s("2.05", K + "s2.05.jpg", C([52, 32], 1.06, 1.1), [dict(t="counter", text=["8–10 MONTHS"], at=8, every=99)])
s("2.06", K + "wI07.jpg", C([48, 50], 1.04, 1.2), [dict(t="shine", mask="wI07-tray2", at=12)])
s("2.07", K + "s2.07.jpg", C([48, 34], 1.04, 1.18))
s("2.08", K + "s2.08.jpg", C([70, 40], 1.06, 1.06), [dict(t="stamp", text="NO", x=32, y=36, size=150, at=6)])
s("2.09", K + "s2.09.jpg", C([24, 40], 1.04, 1.16, centre=0.6))
s("2.10", K + "s2.10.jpg", C([58, 55], 1.04, 1.18), [dict(t="stamp", text="NONE", x=50, y=24, size=110, at=30, strike="ANAESTHETIC")])
s("2.13", K + "s2.13.jpg", C([66, 22], 1.04, 1.18, centre=0.6), life=[dict(t="glow", x=5, y=45, r=220)])
# 3 · the science
s("3.02", K + "s3.02.jpg", C([30, 30], 1.12, 1.12, panTo=[66, 30], centre=0.6), [dict(t="rack", a="s3.02-prof1", b="s3.02-prof2b", at=50)])
s("3.03", K + "wI20.jpg", C([50, 40]))
s("3.04", K + "wI21.jpg", C([50, 45]))
# "you'd need to watch a living stomach while it worked" (user review 2026-10-26: the closed door wasn't related)
s("3.05", K + "s4.07a.jpg", C([47, 66], 1.04, 1.16))
s("3.06", K + "s3.06.jpg", C([48, 22], 1.25, 1.04, centre=0.4))
s("3.07", "img/M15.jpg", C([25, 45], 1.12, 1.12, panTo=[70, 45], centre=0.6), [dict(t="pulse", mask="img/M15-alexis.png", at=40)])
# 4 · the experiments
# the six paper tags (measured centres, same in s4.03 and s4.05c): each food's name is written on its own tag
FOOD_TAGS = [["spiced beef", 26, 80], ["salt pork", 41, 70.5], ["raw beef", 53, 63], ["boiled beef", 64, 55], ["stale bread", 76, 47], ["raw cabbage", 86, 41]]
s("4.01", K + "s0.01.jpg", C([49, 70], 1.06, 1.14))
s("4.03", K + "s4.03.jpg", C([28, 56], 1.22, 1.22, panTo=[72, 33], centre=0.7),
  [dict(t="foods", at=6, items=FOOD_TAGS)])
# v3 image (user review 2026-10-24): cabbage, bread, pork and boiled beef gone, raw beef left, spiced beef half-dissolved; the
# tags keep their names; an ink circle lands on each empty string as its word is spoken (cabbage 35, bread 54, pork 72, beef 91)
# the clock (user review 2026-10-26): top centre on the empty table, drawn LAST so no ink circle crosses it, one steady
# forward sweep 12 -> 2 landing on "2 hours"
s("4.05", K + "s4.05c.jpg", C([55, 50], 1.04, 1.12), [dict(t="foods", at=0, every=2, items=FOOD_TAGS),
                                                      dict(t="ink", x=80, y=31, rx=5.5, ry=6, at=33), dict(t="ink", x=69, y=37, rx=5.5, ry=6, at=52),
                                                      dict(t="ink", x=32, y=57, rx=5.5, ry=6, at=70), dict(t="ink", x=57, y=42, rx=5.5, ry=6, at=90),
                                                      dict(t="clock", x=56, y=15, r=7, from_=12, to=2, at=2, dur=48, chip=True)])
s("4.06", K + "s4.06.jpg", C([62, 28]))
s("4.07", None, None, clip="cut/clips/v4.07.mp4", fx=[dict(t="note", text="no forms. none.", x=72, y=30, at=40)])
s("4.08", K + "s4.08.jpg", C([48, 40], 1.3, 1.36), [dict(t="stamp", text="NO FORMS", x=28, y=30, size=90, at=10),
                                                     dict(t="stamp", text="NO ETHICS BOARD", x=72, y=70, size=80, at=34)])
s("4.10", K + "s4.10.jpg", C([24, 45], 1.04, 1.16, centre=0.6), [dict(t="glint", x=20.5, y=25, at=40, size=40)],
  life=[dict(t="glow", x=15, y=78, r=150), dict(t="steam", x=17, y=52)])
s("4.11", K + "s4.11.jpg", C([59, 64], 1.04, 1.16), [dict(t="shine", mask="s4.11-vials", at=8),
                                                     dict(t="ink", x=59, y=68, rx=19, ry=22, at=30, note="warm as a stomach. lovely.", noteAt=[52, 18])],
  life=[dict(t="steam", x=60, y=46)])
s("4.12", None, C([60, 62], 1.06, 1.2), morph=dict(dir="cut/morph-4.12", n=48))
s("4.13", K + "s4.12b.jpg", C([60, 62], 1.2, 1.24), [dict(t="stamp", text="OUTSIDE THE BODY", x=34, y=34, size=90, at=6)])
s("4.15", K + "s4.15.jpg", C([72, 30], 1.04, 1.16, centre=0.5), [dict(t="note", text="he really did this.", x=30, y=72, at=24)])
s("4.17", K + "s4.17.jpg", C([62, 30], 1.03, 1.05, snapAt=6, snapTo=1.28))
s("4.18", K + "s4.18.jpg", C([51, 25]), [dict(t="quote", text="anger and impatience", at=10)])
s("4.19", K + "s4.19.jpg", C([36, 30], 1.14, 1.14, panTo=[82, 50], centre=0.6))
s("4.20", K + "wI12.jpg", C([58, 48], 1.2, 1.04), [dict(t="counter", text=[str(n) for n in range(1, 239, 9)] + ["238"], at=4, every=3, big=True)])
s("4.21", K + "s4.21.jpg", C([53, 20]))
s("4.22", K + "s4.22.jpg", C([70, 55], 1.04, 1.16), life=[dict(t="rays", x=14, y=20), dict(t="motes", x=84, y=60)])
# 5 · the human experiment
s("5.02", K + "s5.02.jpg", C([52, 22]), [dict(t="quote", text="without obtaining my consent", at=10)])
s("5.03", K + "s5.03.jpg", C([65, 47], 1.04, 1.18, centre=0.5))
s("5.04", "img/M20.jpg", C([50, 45]))
s("5.05", K + "s5.05.jpg", C([28, 38], 1.14, 1.14, panTo=[60, 50], centre=0.6))
s("5.07", None, None)  # graphic
# a still (user review 2026-10-26: the clip chopped nothing while logs fell by themselves)
s("5.08", K + "s5.08.jpg", C([52, 48], 1.04, 1.14))
s("5.09", K + "s5.09.jpg", C([72, 34], 1.14, 1.14, panTo=[25, 40], centre=0.6))
# canoes (user review 2026-10-24: "flying"): y = the hull bottom, the lower 14% of the hull sits under the waterline;
# the family canoe 10 points lower than before; the lake's water starts at y≈56%. (The old glint here had no glasses to sit on.)
s("5.11", "img/M21-lake.jpg", C([50, 60], 1.16, 1.03),
  sprite=dict(src=K + "prop-canoe-family-cut.png", x=[40, 46], y=72, w=24, aspect=0.5), life=[dict(t="glow", x=50, y=40, r=420)])
s("5.11b", K + "s5.11b.jpg", C([49, 30], 1.04, 1.16))
s("5.12", "img/M22.jpg", C([50, 50]), life=[dict(t="fog", top=40, bottom=85)])
s("5.13", K + "s5.13.jpg", C([55, 30]))
s("5.14", K + "s5.14.jpg", C([50, 50], 1.04, 1.2), [dict(t="location", text="WASHINGTON · 1833", at=8)])
s("5.15", K + "s5.15.jpg", C([49, 40]), [dict(t="stamp", text="SERGEANT", x=74, y=30, size=100, at=8)])
s("5.16", K + "s5.16.jpg", C([61, 55], 1.06, 1.2), [dict(t="quote", text="covenant servant", at=10)])
s("5.16b", K + "s5.16.jpg", C([61, 55], 1.2, 1.3), [dict(t="quote", text="on or in the stomach of him", at=6)])
s("5.17", K + "s5.16.jpg", C([61, 55], 1.3, 1.36), [dict(t="stamp", text="$150 / YEAR", x=38, y=32, size=110, at=6)])
s("5.18", "img/M24.jpg", C([50, 45]))
s("5.19", K + "s5.19.jpg", C([44, 45], 1.04, 1.16))
s("5.20", K + "s5.19.jpg", C([44, 45], 1.16, 1.26), [dict(t="spot", x=40, y=48, rx=14, ry=22, at=4, dur=999)])
s("5.21", K + "s5.21.jpg", C([20, 42], 1.04, 1.16, centre=0.55))
s("5.21b", K + "s5.21b.jpg", C([49, 25]), [dict(t="quote", text="the man with a lid on his stomach", at=10)])
s("5.22", K + "s5.22.jpg", C([42, 50]), [dict(t="date", text="1834", at=6)])
s("5.23", K + "s5.23.jpg", C([62, 30]))
s("5.24", K + "s5.24.jpg", C([66, 55], 1.04, 1.04))
s("5.25", K + "s5.25.jpg", C([43, 28]), life=[dict(t="glow", x=9, y=12, r=120)])
# 6 · what they learned
s("6.03", K + "s6.03.jpg", C([42, 72], 1.04, 1.16), [dict(t="shine", mask="s6.03-coins", at=10)])
s("6.05", K + "s6.05.jpg", C([46, 50], 1.12, 1.12, panTo=[56, 45], centre=0.6), life=[dict(t="dust", x=46, y=92)])
s("6.06", K + "s6.06.jpg", C([73, 48], 1.04, 1.16, centre=0.6))
s("6.09", "img/M29.jpg", C([22, 35]), [], life=[dict(t="rain"), dict(t="glow", x=23.3, y=42, r=150)])
s("6.10", "img/M30.jpg", C([62, 45]), [dict(t="counter", text=["27 YEARS"], at=12, every=99)], life=[dict(t="shift")])
# 7 · case file photos
s("7.01", "img/M30.jpg", None)
s("7.02", K + "wI06.jpg", None)
s("7.03", K + "s7.03.jpg", None)
s("7.04", K + "wI07.jpg", None)
s("7.05", K + "s7.05.jpg", None)
s("7.06", K + "s4.15.jpg", None)
s("7.08", "img/M31.jpg", None)
# 8 · the last word
s("8.01", "img/M31.jpg", C([80, 55], 1.0, 1.1, centre=0.5), [dict(t="chapter", n=8, title="The Last Word", at=20)],
  life=[dict(t="fog", top=55, bottom=90), dict(t="glowout", x=88, y=60, r=140)])
s("8.02", K + "s8.02.jpg", C([54, 22]), [dict(t="tag", text="DR. WILLIAM OSLER", sub="MONTREAL · 1880", at=10)], life=[dict(t="glow", x=14, y=40, r=180)])
s("8.03", K + "s8.03.jpg", C([51, 50], 1.04, 1.2), [dict(t="shine", mask="s8.03-jar", at=14)])
s("8.04", K + "s8.04.jpg", C([34, 74], 1.06, 1.12), [dict(t="stamp", text="NO", x=62, y=34, size=120, at=6, quiet=True)], life=[dict(t="glow", x=86, y=76, r=150)])
s("8.05", K + "s8.05.jpg", C([50, 34]))
s("8.06", K + "s8.06.jpg", C([56, 52]), life=[dict(t="glow", x=46, y=44, r=90), dict(t="glow", x=55, y=44, r=90), dict(t="glow", x=64, y=48, r=90),
                                                   dict(t="glow", x=31, y=62, r=90), dict(t="glow", x=35, y=62, r=90)])
s("8.07", "img/M33.jpg", C([60, 50]), [dict(t="counter", text=["8 FEET"], at=12, every=99)], life=[dict(t="leaves")])
s("8.08", "img/M34.jpg", C([50, 50]), life=[dict(t="leaves")])
s("8.09", K + "s8.09.jpg", C([56, 30], 1.04, 1.18, centre=0.6), [dict(t="epitaph", at=30)])
s("8.10", K + "s8.10.jpg", C([52, 38], 1.16, 1.03), life=[dict(t="glow", x=20, y=15, r=380), dict(t="leaves")])
# 9 · why it matters
s("9.01", K + "s0.01.jpg", C([49, 70], 1.04, 1.16), warm=True, life=[dict(t="rays", x=82, y=10), dict(t="motes", x=80, y=30)])
s("9.01b", K + "s1.01.jpg", C([37, 20], 1.14, 1.03), warm=True, life=[dict(t="birds", **{"from": [20, 20], "to": [80, 6]})])
# going home: starts slightly right of centre, drifts slowly down toward the lower left (closer, so it grows), facing the
# way it moves; the camera holds still (a following camera cancelled the drift toward the viewer)
s("9.02", "img/M21-lake.jpg", C([50, 62], 1.06, 1.08),
  sprite=dict(src=K + "prop-canoe-solo-cut.png", x=[60, 40], y=[67, 80], w=[15, 21], aspect=0.5, flip=True),
  life=[dict(t="glow", x=50, y=40, r=420)])
s("9.03", K + "s9.03.jpg", C([59, 33], 1.04, 1.2), [dict(t="shine", mask="s9.03-tuque", at=10)])
s("9.04", K + "s9.04.jpg", C([50, 35], 1.03, 1.2))

# ── effect masks: measured box (% x0 y0 x1 y1) per object ───────────────────────────────────────────────────
MASKS = {
    "wI03a-watch": ("wI03a", (40, 34, 61, 71)), "s0.05-beef": ("s0.05", (77, 14, 94, 98)),
    "s1.11-beaumont": ("s1.11", (78, 2, 95, 78)),
    # v2 (user review 2026-10-24): boxes re-measured to hold the WHOLE subject (Alexis + blanket, the tray to its lower rim,
    # the pointing hand); third value = padding around the box (small where a neighbour stands close)
    "wI07-tray2": ("wI07", (31, 40, 74, 78), 0.1),
    "s3.02-prof1": ("s3.02", (18, 18, 42, 100)), "s3.02-prof2b": ("s3.02", (46, 22, 82, 100), 0.08),
    "s4.11-vials": ("s4.11", (41, 44, 79, 89)), "s6.03-coins": ("s6.03", (18, 50, 60, 95)), "s8.03-jar": ("s8.03", (45, 36, 58, 62)),
    "s9.03-tuque": ("s9.03", (51, 20, 67, 46)),
    # depth of field on the 1.15 / 1.16 close-ups (user review 2026-10-26)
    "s1.15b-alexis": ("s1.15b", (66, 62, 100, 100), 0.1), "s1.16-beaumont": ("s1.16", (36, 12, 64, 100), 0.1),
}
# subjects a box can't isolate, outlined on a coordinate grid (% of the frame, checked on an overlay):
# 1.05 — whole-picture cut-out, limited to Alexis's side along his back and the top of his arm (the three friends touch)
# 1.14 — Alexis lying under the blanket, the barrel rim in front of him: a measured polygon (no model separates him)
# 1.05 v2 (user review 2026-10-26: the old limit cut through his nose and hands): traced generously around the cap, the
#   face profile (nose, open mouth), both hands and the bread between them, the shirt and the sash
WHOLE = {"s1.05-alexis2": ("s1.05", (70, 32, 86, 90), [(67.4, 37.5), (69.3, 32), (72.5, 29.8), (76.5, 29.6), (79.8, 32.3), (80.6, 36.5),
                                                       (80.1, 40.5), (79.2, 44), (79.4, 47.5), (81.4, 50.4), (83.6, 55), (85, 60.5), (85.3, 67),
                                                       (85, 74), (84.7, 80), (84, 86), (83.2, 91), (82.7, 100), (71, 100), (70.8, 93), (71.2, 88.5),
                                                       (72, 84.5), (70, 82), (66, 81.4), (62, 82.4), (58.4, 80.8), (55.6, 78.4), (55.8, 75.8),
                                                       (60.6, 71.8), (61.1, 69.3), (63.6, 69.2), (65.6, 70.7), (68.2, 70.7), (69.6, 68.8),
                                                       (69.8, 64), (69.4, 59), (70.2, 55), (70.3, 53.4), (69.1, 52), (68.8, 49.6), (68.1, 48.2),
                                                       (67.9, 46.8), (66.9, 45.7), (67.3, 43.8), (67.7, 41.5), (67.1, 39.5)]),
         "s1.05-alexis": ("s1.05", (70, 32, 86, 90), [(68, 0), (100, 0), (100, 100), (71.5, 100), (71.4, 86), (68.8, 83), (63.5, 83),
                                                      (60.4, 79.4), (60.7, 71.9), (62, 70.5), (65.6, 70), (71.9, 62.6), (71.9, 55), (68, 37)])}
# 1.15b — Alexis lying (face, cap, shirt, sash), the barrel in front left OUT so it blurs as a foreground (rembg took the
#   fur bundle and missed his face)
POLY = {"s1.15b-alexis2": ("s1.15b", [(43, 73), (46, 69.5), (50, 68.3), (54, 68.8), (55.6, 71), (57, 73.5), (58.8, 76.5), (60.2, 79),
                                      (61.4, 81.5), (63, 80.2), (66, 77.2), (70, 75.2), (74, 74), (78, 74.4), (80.6, 75.8), (83.8, 76.2),
                                      (85.2, 80), (85.6, 90), (85.2, 99.5), (81, 99.5), (78, 94.5), (74, 90.6), (68, 88.6), (63, 89),
                                      (58, 90.6), (55, 91.2), (51, 92.6), (48, 90.8), (45, 89), (42.2, 86), (41, 82), (41.4, 77)]),
        "s1.14-alexis3": ("s1.14", [(72.5, 71.6), (74.5, 71.6), (76.3, 73.5), (76.2, 76.5), (75.4, 79.5), (75.6, 84), (74.5, 87.5), (73.5, 89.8),
                                    (68, 89.6), (62, 89.7), (56, 90.6), (51.5, 92.8), (50, 95.2), (46, 94.6), (42, 93.2), (38, 92.2), (35.3, 91.8),
                                    (36.5, 90.2), (40, 88.6), (44, 87.2), (48, 85.8), (52, 84.6), (55.5, 83.2), (57, 81.5), (57.8, 80), (60, 79),
                                    (62.5, 78.4), (64.5, 77.2), (66.5, 76), (68.5, 74.6), (70.5, 73), (71.5, 72.2)])}


def build_masks():
    from masks import polygon_mask, subject_mask, whole_mask
    for name, (img, box, limit) in WHOLE.items():
        if not (PUB / f"cut/{name}.png").exists():
            whole_mask(str(PUB / f"cut/{img}.jpg"), str(PUB / f"cut/{name}.png"), box, limit=limit)
    for name, (img, pts) in POLY.items():
        if not (PUB / f"cut/{name}.png").exists():
            polygon_mask(str(PUB / f"cut/{img}.jpg"), str(PUB / f"cut/{name}.png"), pts)
    for name, (img, box, *pad) in MASKS.items():
        out = PUB / f"cut/{name}.png"
        if not out.exists():
            subject_mask(str(PUB / f"cut/{img}.jpg"), str(out), box, width=1920, **({"pad": pad[0]} if pad else {}))


def hold_dissolve(a, b, out, mix, n=48):
    """n frames: picture a, then a `mix`-frame eased dissolve centred in the sequence, then picture b."""
    import math
    from PIL import Image
    A, B = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    out.mkdir(parents=True, exist_ok=True)
    s0 = (n - mix) // 2
    for i in range(n):
        t = min(1, max(0, (i - s0) / mix))
        Image.blend(A, B, 0.5 - 0.5 * math.cos(math.pi * t)).save(out / f"{i:03d}.jpg", quality=92)


def verify_sheet(path):
    """Every anchor drawn on its image: camera target (cyan cross), pan end (cyan arrow), fx points/ellipses (amber),
    masks (green tint), glows (orange rings), so a misplaced effect is visible before the render."""
    from PIL import Image, ImageDraw
    tiles = []
    for id, sp in SH.items():
        if not sp.get("img"):
            continue
        im = Image.open(PUB / sp["img"]).convert("RGB").resize((640, 357))
        d = ImageDraw.Draw(im, "RGBA")
        P = lambda x, y: (x * 6.4, y * 3.57)
        for f in sp["fx"]:
            if f.get("mask"):
                m = f["mask"]
                mp = PUB / (m if m.startswith("img/") else f"cut/{m}.png")
                if mp.exists():
                    a = Image.open(mp).split()[-1].resize((640, 357))
                    im.paste(Image.new("RGB", (640, 357), (40, 230, 90)), (0, 0), a.point(lambda v: v // 2))
            for key in ("a", "b"):
                if f.get("t") == "rack":
                    a = Image.open(PUB / f"cut/{f[key]}.png").split()[-1].resize((640, 357))
                    im.paste(Image.new("RGB", (640, 357), (40, 230, 90) if key == "a" else (230, 90, 220)), (0, 0), a.point(lambda v: v // 2))
            if "x" in f and "rx" in f:
                x, y = P(f["x"], f["y"])
                d.ellipse((x - f["rx"] * 6.4, y - f["ry"] * 3.57, x + f["rx"] * 6.4, y + f["ry"] * 3.57), outline=(255, 180, 40), width=3)
            elif "x" in f and f.get("t") in ("glint", "clock"):
                x, y = P(f["x"], f["y"])
                d.ellipse((x - 7, y - 7, x + 7, y + 7), outline=(255, 180, 40), width=3)
        for l in sp["life"]:
            if "x" in l:
                x, y = P(l["x"], l["y"])
                r = 9 if l["t"] != "glow" else 14
                d.ellipse((x - r, y - r, x + r, y + r), outline=(255, 110, 30), width=3)
                d.text((x + r + 2, y - 6), l["t"], fill=(255, 140, 40))
        if sp["cam"]:
            x, y = P(*sp["cam"]["target"])
            d.line((x - 12, y, x + 12, y), fill=(0, 230, 255), width=3)
            d.line((x, y - 12, x, y + 12), fill=(0, 230, 255), width=3)
            if sp["cam"].get("panTo"):
                x2, y2 = P(*sp["cam"]["panTo"])
                d.line((x, y, x2, y2), fill=(0, 230, 255), width=2)
                d.ellipse((x2 - 5, y2 - 5, x2 + 5, y2 + 5), fill=(0, 230, 255))
        d.rectangle((0, 0, 70, 16), fill=(0, 0, 0))
        d.text((4, 2), id, fill=(255, 255, 0))
        tiles.append(im)
    cols = 4
    for p in range(0, len(tiles), 16):
        grp = tiles[p:p + 16]
        sheet = Image.new("RGB", (640 * cols, 357 * ((len(grp) + cols - 1) // cols)))
        for i, t in enumerate(grp):
            sheet.paste(t, ((i % cols) * 640, (i // cols) * 357))
        sheet.save(f"{path}-{p // 16}.jpg", quality=85)


if __name__ == "__main__":
    build_masks()
    from trans_prep import morph
    # 0.02 / 0.04: hold, ONE short film dissolve at the action, hold (a flow morph smeared the arm; a full-length dissolve
    # showed three ghost hands, user review 2026-10-26)
    for name, a_, b_, mix in (("morph-0.02", "s0.02a", "s0.02b", 8), ("morph-0.04", "s0.02b", "s0.02a", 12)):
        if not (PUB / f"cut/{name}/047.jpg").exists():
            hold_dissolve(PUB / f"cut/{a_}.jpg", PUB / f"cut/{b_}.jpg", PUB / f"cut/{name}", mix)
    if not (PUB / "cut/morph-4.12/047.jpg").exists():
        morph(str(PUB / "cut/s4.12.jpg"), str(PUB / "cut/s4.12b.jpg"), str(PUB / "cut/morph-4.12"), frames=48)
    # canoes: the waterline along the measured keel + the reflection under it (masks.canoe_water)
    from masks import canoe_water
    for sp in SH.values():
        spr = sp.get("sprite")
        if spr:
            src = PUB / spr["src"]
            base = spr["src"][:-4]
            info = canoe_water(str(src), spr.get("sink", 0.14))
            spr.update(water=f"{base}-water.png", refl=f"{base}-refl.png", wmid=round(info["wmid"], 4), E=info["E"], tilt=9.55)
    json.dump({"shots": SH}, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(SH), "shots ->", OUT)
    if len(sys.argv) > 1:
        verify_sheet(sys.argv[1])
