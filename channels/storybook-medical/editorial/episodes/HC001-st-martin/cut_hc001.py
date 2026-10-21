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
s("0.02", None, None, clip="cut/clips/v0.02.mp4")
s("0.03", K + "wI03a.jpg", C([50, 52], 1.12, 1.2), [dict(t="clock", x=50.0, y=50.7, r=10.5, from_=12, to=1, at=4, dur=40),
                                                    dict(t="shine", mask="wI03a-watch", at=30)])
s("0.04", None, None, clip="cut/clips/v0.02-rev.mp4")
s("0.05", K + "s0.05.jpg", C([84, 50], 1.04, 1.22, centre=0.6),
  [dict(t="ink", x=85, y=52, rx=8, ry=30, at=8, note="half. gone.", noteAt=[62, 22]), dict(t="shine", mask="s0.05-beef", at=30)])
s("0.06", None, None, clip="cut/clips/v0.06.mp4")
s("0.07", K + "s0.07.jpg", C([47, 30]), life=[dict(t="glow", x=30, y=44, r=170), dict(t="motes", x=82, y=40)])
s("0.08", K + "s4.07b.jpg", C([49, 73], 2.3, 1.8, centre=1.0), [dict(t="counter", text=["1822", "1823", "1824", "1825"], at=6, every=12)])
s("0.10", "img/M21-lake.jpg", C([62, 58], 1.06, 1.14), [dict(t="hand", y=34)],
  sprite=dict(src=K + "prop-canoe-solo-cut.png", x=[66, 60], y=60, w=13), dark=0.45)
# 1 · the case
s("1.01", K + "s1.01.jpg", C([37, 18], 1.03, 1.14), [dict(t="location", text="MACKINAC ISLAND · 1822", at=50)],
  life=[dict(t="fog", top=50, bottom=75), dict(t="birds", **{"from": [70, 18], "to": [100, 8]}), dict(t="smoke", x=3.5, y=23.4)])
s("1.03", None, None, clip="cut/clips/v1.03.mp4")
s("1.04", K + "s1.04.jpg", C([55, 40], 1.04, 1.14), life=[dict(t="spray", x=88, y=72)])
s("1.05", K + "s1.05.jpg", C([74, 42], 1.03, 1.15),
  [dict(t="callout", name="ALEXIS ST. MARTIN", sub="ABOUT 18 · VOYAGEUR", aside="about to have a very bad summer", x=74, y=36, side="left", at=10)])
s("1.05b", K + "s1.05b.jpg", C([58, 42], 1.12, 1.12, panTo=[66, 55], centre=0.6))
s("1.06", K + "s1.06.jpg", C([45, 40], 1.04, 1.18), [dict(t="spot", x=48, y=48, rx=16, ry=26, at=14, dur=80),
                                                       dict(t="date", text="6 JUNE 1822", at=4)],
  life=[dict(t="motes", x=93, y=22)])
s("1.07", K + "wI06.jpg", C([52, 45], 1.03, 1.05, snapAt=4, snapTo=1.3), [dict(t="flash", at=3), dict(t="shake", at=3)])
s("1.08", K + "s1.08.jpg", C([55, 78], 1.04, 1.2, centre=0.55), [dict(t="ink", x=58, y=85, rx=11, ry=8, at=10, note="duck shot", noteAt=[70, 62])],
  life=[dict(t="smoke", x=61, y=70)])
s("1.10", None, None, clip="cut/clips/v1.10.mp4", fx=[dict(t="tag", text="DR. WILLIAM BEAUMONT", sub="ARMY SURGEON", at=12)])
s("1.11", K + "s1.11.jpg", C([86, 32], 1.03, 1.14, centre=0.5), [dict(t="pulse", mask="s1.11-beaumont", at=8)])
s("1.12", K + "s1.12.jpg", C([38, 22], 1.03, 1.14, centre=0.5), [dict(t="spot", x=38, y=24, rx=16, ry=26, at=10, dur=90)],
  life=[dict(t="glow", x=64.5, y=26.4, r=160)])
s("1.13", K + "s1.13.jpg", C([21, 76], 1.04, 1.28, centre=0.65))
s("1.14", K + "s1.14.jpg", C([66, 70], 1.18, 1.04), [dict(t="isolate", mask="s1.14-alexis", at=10, dur=999)])
s("1.15", None, None, clip="cut/clips/v1.15.mp4")
s("1.16", K + "s1.16.jpg", C([48, 27], 1.04, 1.2))
# 2 · what happened next (Mackinac post hospital)
s("2.01", K + "s2.01.jpg", C([80, 60], 1.03, 1.14, centre=0.5), [dict(t="counter", text=[f"DAY {d}" for d in (1, 3, 6, 9, 12, 15, 17)], at=6, every=10)],
  life=[dict(t="glow", x=70, y=55, r=120)])
s("2.02", None, None, clip="cut/clips/v2.02.mp4", use=[0, 3.7])
s("2.03", K + "s2.03.jpg", C([46, 22]))
s("2.04", K + "s2.04.jpg", C([77, 40], 1.03, 1.14, centre=0.5), life=[dict(t="rays", x=14, y=24), dict(t="motes", x=24, y=40)])
s("2.05", K + "s2.05.jpg", C([52, 32], 1.06, 1.1), [dict(t="counter", text=["8–10 MONTHS"], at=8, every=99)])
s("2.06", K + "wI07.jpg", C([48, 50], 1.04, 1.2), [dict(t="shine", mask="wI07-tray", at=12)])
s("2.07", K + "s2.07.jpg", C([48, 34], 1.04, 1.18))
s("2.08", K + "s2.08.jpg", C([70, 40], 1.06, 1.06), [dict(t="stamp", text="NO", x=32, y=36, size=150, at=6)])
s("2.09", K + "s2.09.jpg", C([24, 40], 1.04, 1.16, centre=0.6))
s("2.10", K + "s2.10.jpg", C([58, 55], 1.04, 1.18), [dict(t="stamp", text="NONE", x=50, y=24, size=110, at=30, strike="ANAESTHETIC")])
s("2.13", K + "s2.13.jpg", C([66, 22], 1.04, 1.18, centre=0.6), life=[dict(t="glow", x=5, y=45, r=220)])
# 3 · the science
s("3.02", K + "s3.02.jpg", C([30, 30], 1.12, 1.12, panTo=[66, 30], centre=0.6), [dict(t="rack", a="s3.02-prof1", b="s3.02-prof2", at=50)])
s("3.03", K + "wI20.jpg", C([50, 40]))
s("3.04", K + "wI21.jpg", C([50, 45]))
s("3.05", K + "s3.05.jpg", C([45, 60]), life=[dict(t="glow", x=45, y=77, r=150), dict(t="glow", x=86, y=72, r=160)])
s("3.06", K + "s3.06.jpg", C([48, 22], 1.25, 1.04, centre=0.4))
s("3.07", "img/M15.jpg", C([25, 45], 1.12, 1.12, panTo=[70, 45], centre=0.6), [dict(t="pulse", mask="img/M15-alexis.png", at=40)])
# 4 · the experiments
s("4.01", K + "s0.01.jpg", C([49, 70], 1.06, 1.14))
s("4.03", K + "s4.03.jpg", C([28, 56], 1.22, 1.22, panTo=[72, 33], centre=0.7),
  [dict(t="foods", at=6, items=[["spiced beef", 19, 60], ["salt pork", 32, 55], ["raw beef", 45, 49], ["boiled beef", 57, 42],
                                 ["stale bread", 68, 33], ["raw cabbage", 79, 27]])])
s("4.05", K + "s4.05.jpg", C([50, 45], 1.04, 1.12), [dict(t="clock", x=86, y=18, r=7, from_=12, to=2, at=2, dur=30, chip=True),
                                                     dict(t="ink", x=16, y=60, rx=6, ry=7, at=24), dict(t="ink", x=30, y=55, rx=6, ry=7, at=34),
                                                     dict(t="ink", x=56, y=43, rx=6, ry=6, at=44)])
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
s("5.08", None, None, clip="cut/clips/v5.08.mp4", use=[0, 3.0])
s("5.09", K + "s5.09.jpg", C([72, 34], 1.14, 1.14, panTo=[25, 40], centre=0.6))
s("5.11", "img/M21-lake.jpg", C([50, 55], 1.16, 1.03), [dict(t="glint", x=0, y=0, at=60, size=26, onSprite=[0.62, 0.62])],
  sprite=dict(src=K + "prop-canoe-family-cut.png", x=[40, 46], y=62, w=24), life=[dict(t="glow", x=50, y=40, r=420)])
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
s("9.02", "img/M21-lake.jpg", C([50, 55], 1.12, 1.12, panTo=[60, 55]), sprite=dict(src=K + "prop-canoe-solo-cut.png", x=[22, 70], y=63, w=20),
  life=[dict(t="glow", x=50, y=40, r=420)])
s("9.03", K + "s9.03.jpg", C([59, 33], 1.04, 1.2), [dict(t="shine", mask="s9.03-tuque", at=10)])
s("9.04", K + "s9.04.jpg", C([50, 35], 1.03, 1.2))

# ── effect masks: measured box (% x0 y0 x1 y1) per object ───────────────────────────────────────────────────
MASKS = {
    "wI03a-watch": ("wI03a", (40, 34, 61, 71)), "s0.05-beef": ("s0.05", (77, 14, 94, 98)),
    "s1.11-beaumont": ("s1.11", (78, 2, 95, 78)), "s1.14-alexis": ("s1.14", (55, 62, 92, 95)),
    "wI07-tray": ("wI07", (32, 36, 73, 66)), "s3.02-prof1": ("s3.02", (18, 18, 42, 100)), "s3.02-prof2": ("s3.02", (52, 18, 82, 100)),
    "s4.11-vials": ("s4.11", (41, 44, 79, 89)), "s6.03-coins": ("s6.03", (18, 50, 60, 95)), "s8.03-jar": ("s8.03", (45, 36, 58, 62)),
    "s9.03-tuque": ("s9.03", (51, 20, 67, 46)),
}


def build_masks():
    from masks import subject_mask
    for name, (img, box) in MASKS.items():
        out = PUB / f"cut/{name}.png"
        if not out.exists():
            subject_mask(str(PUB / f"cut/{img}.jpg"), str(out), box, width=1920)


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
    if not (PUB / "cut/morph-4.12/047.jpg").exists():
        morph(str(PUB / "cut/s4.12.jpg"), str(PUB / "cut/s4.12b.jpg"), str(PUB / "cut/morph-4.12"), frames=48)
    json.dump({"shots": SH}, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(SH), "shots ->", OUT)
    if len(sys.argv) > 1:
        verify_sheet(sys.argv[1])
