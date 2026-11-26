"""HC003-S1 Dancing Plague: the 3 HERO shots on REAL art (user 2026-11-22: "cast sheets + HERO pieces on real art, shot 14
without the coif; show me the HERO shots before the story stills"). Free: no paid call.

Each shot = the generated empty plate (assets/images/refs/plate-s<n>.png) + the cut-outs of its paid sheets
(assets/images/sprites/<name>/, fx_prep.sheet), keyed on Liam's REAL words (artifacts/word_timestamps.json), with the
shot's window of narration.wav as the sound. The compositor is the HCS10 one (hero_previz_hcs10: plate + keyed actors +
camera keys), with three additions: a "rot" key (the wagon wheels turn as it rolls), a flat-black silhouette mode
(shot 4, Rule 0b: no face at the fall) and the hook-card band at the BOTTOM (y 980-1248, shot 1).
Out: projects/hc003-s1/review/hero/<n>-real.mp4 + <n>-real-sheet.jpg (start / key / end) + pieces.jpg

    python channels/storybook-medical/editorial/episodes/HC003-dancing-plague/hero_real_hc003s1.py [1 4 10 pieces]
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO = Path(__file__).resolve().parents[5]
P = REPO / "projects/hc003-s1"
OUT = Path(os.environ["HERO_OUT"]) if os.environ.get("HERO_OUT") else P / "review/hero"   # HERO_OUT: render to a scratch folder
W, H, FPS, OW, OH = 1080, 1920, 30, 540, 960
WORDS = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
NARR = P / "assets/audio/narration.wav"
EASE = {"linear": lambda u: u, "inout": lambda u: u * u * (3 - 2 * u), "out": lambda u: 1 - (1 - u) ** 2, "in": lambda u: u * u}


def word_t(word: str, after: float = 0.0) -> float:
    """Liam's start time of `word` (first occurrence at or after `after`)."""
    for w in WORDS:
        if w["start"] >= after and w["word"].lower().strip(".,…?!\"") == word.lower():
            return w["start"]
    raise SystemExit(f"'{word}' not found after {after}")


def _font(size):
    for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            pass
    return ImageFont.load_default()


def interp(keys, t, field, default=0.0):
    ks = [k for k in keys if field in k]
    if not ks:
        return default
    if t <= ks[0]["t"]:
        return ks[0][field]
    for a, b in zip(ks, ks[1:]):
        if t <= b["t"]:
            u = (t - a["t"]) / max(1e-6, b["t"] - a["t"])
            return a[field] + (b[field] - a[field]) * EASE[b.get("ease", "linear")](u)
    return ks[-1][field]


def state(keys, t):
    cur, since, prev = None, 0.0, None
    for k in keys:
        if "state" in k and k["t"] <= t:
            if cur is not None and k["state"] != cur:
                prev = cur
            cur, since = k["state"], k["t"]
    return cur, since, prev


def silhouette(im: Image.Image, rim=(255, 170, 90)) -> Image.Image:
    """Rule 0b: a pure black shape (no face) with a thin warm rim on its right edge (the lit doorway)."""
    import cv2
    a = (np.array(im.getchannel("A")) > 40).astype(np.uint8)
    cnts, _ = cv2.findContours(a, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    a = np.zeros_like(a)
    cv2.drawContours(a, cnts, -1, 1, -1)
    a = cv2.GaussianBlur(a * 255, (3, 3), 0)
    black = np.zeros((*a.shape, 4), np.uint8)
    black[..., 3] = a
    edge = (a > 128) & (np.roll(a, -3, axis=1) <= 128)
    black[edge, :3] = rim
    return Image.fromarray(black, "RGBA")


def load_piece(name: str, height: float, anchor: str = "bottom", sil: bool = False, ref: str | None = None,
               states: list[str] | None = None, shared: bool = False, crop: bool = False):
    """The cut-out states of a paid sheet, scaled so the `ref` state's (default: the first) opaque height is `height`
    (frame fractions); `states` keeps only those (the wagon body and its wheel share one sheet and one canvas)."""
    d = P / "assets/images/sprites" / name
    meta = json.load(open(d / "sprites.json", encoding="utf-8"))
    frames = {s: Image.open(d / fs[0]).convert("RGBA") for s, fs in meta["frames"].items() if not states or s in states}
    if crop:   # tight canvas: the pivot of a rotation is the CENTRE of the canvas, so a wheel must be cut to its own bbox
        frames = {s: im.crop(im.getbbox()) for s, im in frames.items()}
    first = ref or next(iter(frames))
    bb = frames[first].getbbox()
    k = height * H / (bb[3] - bb[1])
    frames = {s: im.convert("RGBa").resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS).convert("RGBA")
              for s, im in frames.items()}
    if sil:
        frames = {s: silhouette(im) for s, im in frames.items()}
    def anc_of(im):
        a = np.array(im.getchannel("A")) > 128
        ys, xs = np.nonzero(a)
        p = {"bottom": ((xs.min() + xs.max()) / 2, ys.max()), "center": ((xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2),
             "top": ((xs.min() + xs.max()) / 2, ys.min())}[anchor]
        return p[0] / im.width, p[1] / im.height
    per = {s: anc_of(im) for s, im in frames.items()}
    return frames, per[first], (per if anchor == "bottom" and not shared else {})


SPOKES = 12   # spokes of the wagon wheel (count them on sprite-wagon-s10 if the sheet is re-rolled)
ROLL_LOG: list[float] = []


def _spin(a, t):
    """Wheel angle in degrees, counter-clockwise positive, from the distance the wagon has rolled left: d / r."""
    keys = a["keys"]
    x = interp(keys, t, "x") * W
    x0 = keys[0]["x"] * W
    return (x0 - x) / (a["roll"]["r"]) * 180 / math.pi


def roll_sprite(spr, a, t):
    """The wheel is a 3/4 view (an ellipse): stretch it to the true circle, turn the spokes about the hub, squash it back.
    A plain 2D rotate would tilt the ellipse instead of turning the spokes. Anti-strobe: when one frame turns the wheel
    by more than half a spoke gap (a spinning wheel then looks stopped or backwards) the frame averages the sub-steps
    of the frame's own travel: real film motion blur."""
    w, h = spr.size
    ang, prev = _spin(a, t), _spin(a, t - 1 / FPS)
    step = abs(ang - prev)
    ROLL_LOG.append(step)
    n = 1 if step <= 4 else min(24, math.ceil(step / 3))
    circ = spr.convert("RGBa").resize((h, h), Image.LANCZOS)
    acc = None
    for i in range(n):
        d = ang if n == 1 else prev + (ang - prev) * (i + 0.5) / n
        r = np.asarray(circ.rotate(d, resample=Image.BICUBIC, expand=False), dtype=np.float32)
        acc = r if acc is None else acc + r
    out = Image.fromarray((acc / n).round().astype(np.uint8), "RGBa").resize((w, h), Image.LANCZOS)
    return out.convert("RGBA")


def world(shot, t):
    im = Image.open(shot["plate"]).convert("RGBA").resize((W, H), Image.LANCZOS)
    boxes = []
    for a in shot["actors"]:
        if t < a.get("from", -1) or t >= a.get("to", 1e9):
            continue
        frames, anchor, per = a["piece"]
        st, since, prev = state(a["keys"], t)
        anchor = per.get(st, anchor)
        spr = frames[st]
        xf = a.get("xfade", 0)
        if prev and xf and t - since < xf and frames[prev].size == spr.size:   # different canvases: a clean swap
            spr = Image.blend(frames[prev], spr, (t - since) / xf)
        rot = interp(a["keys"], t, "rot", 0.0)
        if a.get("roll"):   # a wheel: the angle comes from the distance rolled (never from time), see roll_sprite
            spr = roll_sprite(spr, a, t)
        elif rot:
            spr = spr.rotate(rot, resample=Image.BICUBIC, expand=False)
        x, y = interp(a["keys"], t, "x") * W, interp(a["keys"], t, "y") * H
        ox, oy = int(x - anchor[0] * spr.width), int(y - anchor[1] * spr.height)
        if a.get("shadow"):   # contact shadow on the ground line (feet / body bottom = the anchor y)
            sw, sh_, al = a["shadow"]
            bb0 = spr.getbbox() or (0, 0, spr.width, spr.height)
            cx, gw = ox + (bb0[0] + bb0[2]) / 2, (bb0[2] - bb0[0]) * sw
            sl = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(sl).ellipse([cx - gw / 2, y - sh_ * H / 2, cx + gw / 2, y + sh_ * H / 2], fill=(10, 8, 14, al))
            im.alpha_composite(sl.filter(ImageFilter.GaussianBlur(10)))
        lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
        lay.paste(spr, (ox, oy), spr)
        im.alpha_composite(lay)
        if a.get("hero"):
            bb = spr.getbbox()
            if bb:
                boxes.append((ox + bb[0], oy + bb[1], ox + bb[2], oy + bb[3]))
    return im, boxes


def camera(im, cam, t, boxes):
    s, tx, ty = interp(cam, t, "scale", 1.0), interp(cam, t, "x") * W / 100, interp(cam, t, "y") * H / 100
    cx, cy = W / 2, H / 2
    x0, y0 = cx + (0 - cx - tx) / s, cy + (0 - cy - ty) / s
    x1, y1 = cx + (W - cx - tx) / s, cy + (H - cy - ty) / s
    out = im.crop((int(x0), int(y0), int(x1), int(y1))).resize((OW, OH), Image.LANCZOS)
    k = OW / (x1 - x0)
    return out, [((b[0] - x0) * k, (b[1] - y0) * k, (b[2] - x0) * k, (b[3] - y0) * k) for b in boxes]


def overlay(fr, shot, t, boxes):
    d = ImageDraw.Draw(fr, "RGBA")
    f, fb = _font(17), _font(24)
    ky = lambda y: y * OH / H  # noqa: E731
    for y in (288, 1248):                                                                   # the Shorts safe zone
        for x in range(0, OW, 14):
            d.line([(x, ky(y)), (x + 7, ky(y))], fill=(255, 255, 255, 150), width=1)
    if shot.get("card") and shot["card"][0] <= t < shot["card"][1]:                         # hook card A, BOTTOM band
        d.rectangle([20, ky(980), OW - 20, ky(1248)], fill=(232, 163, 61, 80), outline=(232, 163, 61, 220), width=2)
        d.text((OW / 2, ky(1114)), "HOOK CARD A: She couldn't / stop dancing.", fill=(255, 255, 255, 235), font=fb, anchor="mm")
    for txt, t0, t1, y in shot.get("texts", []):                                            # stamps / name tags (stand-ins)
        if t0 <= t < t1:
            d.rectangle([40, ky(y) - 22, OW - 40, ky(y) + 22], fill=(20, 20, 20, 150))
            d.text((OW / 2, ky(y)), txt, fill=(255, 230, 190, 255), font=fb, anchor="mm")
    if t >= shot["hero_at"] - 0.5:                                                          # HERO 1/3 rule
        for b in boxes:
            bw, bh = (min(b[2], OW) - max(b[0], 0)) / OW, (min(b[3], OH) - max(b[1], 0)) / OH
            ok = max(bw, bh) >= 1 / 3
            col = (80, 220, 120, 230) if ok else (240, 70, 60, 230)
            d.rectangle(b, outline=col, width=2)
            d.text((max(6, b[0] + 4), max(4, b[1] + 4)), f"HERO {max(bw, bh):.2f} {'≥' if ok else '<'} 1/3", fill=col, font=f)
    word = next((w["word"] for w in reversed(WORDS) if w["start"] <= shot["win"][0] + t), "")
    d.rectangle([0, OH - 64, OW, OH], fill=(0, 0, 0, 170))
    d.text((14, OH - 56), f"shot {shot['name']}  t={t:4.2f}s  (Liam's real timing)", fill=(200, 200, 200, 255), font=f)
    d.text((14, OH - 32), word, fill=(255, 255, 255, 255), font=fb)
    return fr


def render(shot) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    mp4 = OUT / f"{shot['name']}-real.mp4"
    a0, a1 = shot["win"]
    dur = a1 - a0
    n = round(dur * FPS)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
           "-i", str(NARR), "-filter_complex", f"[1:a]atrim={a0}:{a1},asetpts=PTS-STARTPTS[a]", "-map", "0:v", "-map", "[a]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    keep = {0: None, min(n - 1, round(shot["hero_at"] * FPS)): None, n - 1: None}
    for i in range(n):
        t = i / FPS
        w_, boxes = world(shot, t)
        fr, sb = camera(w_, shot["cam"], t, boxes)
        fr = overlay(fr.convert("RGB"), shot, t, sb)
        proc.stdin.write(fr.tobytes())
        if i in keep:
            keep[i] = fr.copy()
    proc.stdin.close()
    proc.wait()
    if ROLL_LOG:
        print(f"wheel: max {max(ROLL_LOG):.1f} deg per frame (> {180 / SPOKES:.0f} = half a spoke gap: blurred by sub-steps)")
        ROLL_LOG.clear()
    sheet = Image.new("RGB", (OW * 3 + 20, OH), "white")
    for j, fr in enumerate(keep.values()):
        sheet.paste(fr, (j * (OW + 10), 0))
    sheet.save(OUT / f"{shot['name']}-real-sheet.jpg", quality=88)
    return mp4


def pieces_sheet(names: list[str]) -> Path:
    """review/hero/pieces.jpg: every paid piece on one contact sheet (the approval page shows it)."""
    refs = P / "assets/images/refs"
    th, tiles = 420, []
    for nm in names:
        im = Image.open(refs / f"{nm}.png").convert("RGB")
        im = im.resize((round(im.width * th / im.height), th), Image.LANCZOS)
        t = Image.new("RGB", (im.width, th + 34), "white")
        t.paste(im, (0, 0))
        ImageDraw.Draw(t).text((6, th + 8), nm, fill="black", font=_font(18))
        tiles.append(t)
    rows, row = [], []
    for t in tiles:
        if row and sum(x.width + 10 for x in row) + t.width > 2600:
            rows.append(row)
            row = []
        row.append(t)
    rows.append(row)
    out = Image.new("RGB", (max(sum(x.width + 10 for x in r) for r in rows), len(rows) * (th + 44)), "white")
    for i, r in enumerate(rows):
        x = 0
        for t in r:
            out.paste(t, (x, i * (th + 44)))
            x += t.width + 10
    path = OUT / "pieces.jpg"
    OUT.mkdir(parents=True, exist_ok=True)
    out.save(path, quality=85)
    return path


# ── the three shots (positions measured on the real plates; times from Liam's words) ────────────────────────────────
def shot1():
    dance = word_t("dance")
    win = (0.0, word_t("she") - 0.05)                       # to the cut before "She can't stop."
    return {"name": "1", "win": win, "plate": P / "assets/images/refs/plate-s1.png", "card": (0.0, 2.5), "hero_at": dance,
            "actors": [
                {"id": "shutter", "piece": load_piece("shutter-s1", 0.10, "center"),
                 "keys": [{"t": 0.0, "x": POS["1"]["shutter"][0], "y": POS["1"]["shutter"][1], "state": "closed"},
                          {"t": 0.25, "state": "open"}], "xfade": 0.12},
                {"id": "troffea", "hero": True, "piece": load_piece("troffea-s1", 0.70, "bottom"),
                 "keys": [{"t": 0.0, "x": POS["1"]["troffea"][0] - 0.02, "y": POS["1"]["troffea"][1], "state": "turnA"},
                          {"t": dance, "x": POS["1"]["troffea"][0] + 0.02, "y": POS["1"]["troffea"][1], "state": "turnB", "ease": "inout"},
                          {"t": win[1], "x": POS["1"]["troffea"][0] - 0.02, "y": POS["1"]["troffea"][1]}], "xfade": 0.10}],
            "cam": [{"t": 0.0, "scale": 1.0, "x": 0, "y": 0}, {"t": 1.0, "scale": 1.12, "x": 0, "y": -2, "ease": "out"},
                    {"t": win[1], "scale": 1.14, "x": 0, "y": -2}]}


def shot4():
    t0 = word_t("she", word_t("trofea"))   # whisper spells it "Trofea"                   # "She danced for hours… until she collapsed."
    coll = word_t("collapsed")
    win = (t0 - 0.05, word_t("next") - 0.05)
    c = coll - win[0]
    return {"name": "4", "win": win, "plate": P / "assets/images/refs/plate-s4.png", "hero_at": c,
            "actors": [
                {"id": "troffea", "hero": True, "piece": load_piece("troffea-s4", S4_H, "bottom", sil=True, ref="turning"),
                 "shadow": (0.9, 0.022, 120),
                 "keys": [{"t": 0.0, "x": POS["4"]["troffea"][0], "y": POS["4"]["troffea"][1], "state": "turning"},
                          {"t": c, "state": "fallen"}], "xfade": 0},   # a fall is a hard cut (states have their own anchors)
                {"id": "coif", "piece": load_piece("coif-s4", COIF_H, "center"), "from": c, "shadow": (0.9, 0.008, 110),
                 "keys": [{"t": c, "x": POS["4"]["head"][0], "y": POS["4"]["head"][1], "rot": -40, "state": "falling"},
                          {"t": c + 0.40, "x": POS["4"]["coif"][0], "y": POS["4"]["coif"][1], "rot": 25, "state": "rest", "ease": "in"},
                          {"t": c + 0.52, "x": POS["4"]["coif"][0] - 0.012, "y": POS["4"]["coif"][1] - 0.012, "rot": 10, "ease": "out"},
                          {"t": c + 0.64, "x": POS["4"]["coif"][0] - 0.02, "y": POS["4"]["coif"][1], "rot": 0, "ease": "in"}],
                 "xfade": 0.10}],
            "cam": [{"t": 0.0, "scale": 1.0, "x": 0, "y": 0}, {"t": win[1] - win[0], "scale": 1.0, "x": 0, "y": 0}]}


def shot10():
    t0 = word_t("frightened")
    wag, shr = word_t("wagon"), word_t("shrine")
    win = (t0 - 0.05, word_t("but", shr) - 0.05)
    a, b = wag - win[0], shr - win[0]
    end = win[1] - win[0]
    wx, wy = POS["10"]["wagon"]
    gx, gy = POS["10"]["group"]
    dx = -0.95                                                      # the wagon rolls out of frame to the LEFT
    group = load_piece("group-s10", S10_GROUP, "bottom", ref="lifted", shared=True)
    body = load_piece("wagon-s10", S10_BODY, "bottom", states=["body"])
    wheel = load_piece("wagon-s10", S10_WHEEL, "center", states=["wheel"], crop=True)   # cut to its own bbox: pivot = hub
    r_px = S10_WHEEL * H / 2                                             # the wheel's true radius (its height is the circle's diameter)
    def path(x, y, **kw):
        return [{"t": 0.0, "x": x, "y": y, **kw}, {"t": b, "x": x, "y": y}, {"t": end, "x": x + dx, "y": y, "ease": "in"}]
    wheels = [{"id": f"wheel{i}", "piece": wheel, "roll": {"r": r_px},
               "keys": path(wx + off, wy - S10_WHEEL * 0.346, state="wheel")}
              for i, off in enumerate(POS["10"]["wheels"])]
    return {"name": "10", "win": win, "plate": P / "assets/images/refs/plate-s10.png", "hero_at": (a + b) / 2,
            "actors": [{"id": "wagon", "hero": True, "piece": body, "keys": path(wx, wy, state="body")}, *wheels,
                       # depth, back to front: wagon + wheels, then HER (she rides the wagon), then the men (they stay):
                       # as the wagon rolls out she passes BEHIND the men, never over them
                       {"id": "troffea", "piece": group, "from": b, "keys": path(gx, gy, state="troffea")},
                       {"id": "group", "hero": True, "piece": group, "xfade": 0.10,
                        "keys": [{"t": 0.0, "x": gx, "y": gy, "state": "lifted"}, {"t": a, "state": "seated"},
                                 {"t": b, "state": "men"}]}],
            "cam": [{"t": 0.0, "scale": 1.08, "x": 0, "y": 0}, {"t": b, "scale": 1.08, "x": 0, "y": 0},
                    {"t": end, "scale": 1.08, "x": 3.5, "y": 0, "ease": "inout"}]}


# measured on the real plates (frame fractions; anchor points: feet for people, centre for the coif / shutter)
# Shot 4 scale rule (L51): she is 1.6 m; the lit door at her depth is 2 m and 0.31 of the frame tall, so she is 0.25-0.27 of
# the frame (not 0.50). The fallen pose is then 0.52 of the frame wide: the HERO 1/3 rule still holds. The coif is a
# 25 cm prop: 0.04-0.05. It must stay between the lane floor and the safe line below.
# Shot 10 scale (user 2026-11-22: "she sits on nothing, her body is bigger than the wagon"): the bed's floor must stand at
# the men's hip height (about 0.52 of their height) so a seated woman sits ON it. Men 0.40 of the frame, so the bed floor
# (half the body sprite's height above its feet) is 0.195 high: S10_BODY 0.39; the wheel is 0.5 of a man's height.
S10_GROUP, S10_BODY, S10_WHEEL = 0.40, 0.39, 0.195
S4_H, COIF_H = 0.28, 0.05   # closer to the camera (feet y 0.78): door-consistent 0.28 at that depth (perspective: the 0.30 door at y 0.73 -> 0.35 at 0.78, x 0.8)
# Shot 1 stays as approved (user 2026-11-22: the door-scaled version lost the dance; only the silhouette shot 4 had the scale problem)
POS = {"1": {"troffea": (0.50, 0.95), "shutter": (0.15, 0.27)},
       "4": {"troffea": (0.52, 0.78), "head": (0.644, 0.666), "coif": (0.60, 0.815)},
       "10": {"wagon": (0.19, 0.86), "group": (0.66, 0.94), "wheels": (-0.30, 0.18)}}
SHOTS = {"1": shot1, "4": shot4, "10": shot10}
PIECES = ["sheet-troffea", "sheet-townsfolk", "plate-s1", "pose-troffea-s1", "sprite-shutter-s1", "plate-s4",
          "pose-troffea-s4", "sprite-coif-s4", "plate-s10", "pose-s10", "sprite-wagon-s10"]

if __name__ == "__main__":
    args = sys.argv[1:] or list(SHOTS)
    if "pieces" in args:
        print(pieces_sheet(PIECES))
    for k in [a for a in args if a != "pieces"]:
        print(render(SHOTS[k]()))
