"""HCS10 Pettenkofer: the 4 HERO shots on REAL art (user 2026-11-20: "generate the 4 HERO shots' pieces FIRST and show
me them on real art before the 9 story images (same as Gage)"). Free: no paid call.

The approved motion (hero_previz_hcs10.py) is reused as it is; only three things change:
  1. the plate is the generated plate (assets/images/refs/plate-s<n>.png) and every piece is the cut-out of its paid
     sheet (assets/images/sprites/<name>/, fx_prep.sheet), scaled so its size matches the approved stand-in (the stand-ins
     were drawn to the storyboard's L51 centimetres, so the real pieces keep those sizes);
  2. every key time is warped from the estimated word to Liam's REAL word (artifacts/word_timestamps.json): a piecewise
     linear map through the key words, so a swap still lands ON its word;
  3. the sound is the narration itself (the shot's window of narration.wav) + the shot's SFX stand-ins.
Out: projects/hcs10-pettenkofer/review/hero/<n>-real.mp4 + <n>-real-sheet.jpg

    python channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/hero_real_hcs10.py [1 4 6 7]
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hero_previz_hcs10 as hp  # noqa: E402

P, W, H, FPS, OW, OH = hp.P, hp.W, hp.H, hp.FPS, hp.OW, hp.OH
WORDS = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
NARR = P / "assets/audio/narration.wav"

# shot windows on Liam's take (cuts in the pauses) and the warp: (estimated t in the shot, the real word it stands for)
SHOT = {
    "1": {"win": (0.00, 5.40), "warp": [(3.3, "drink"), (3.7, "cholera.")], "piece": "plate-s1"},
    "4": {"win": (15.60, 19.30), "warp": [(3.0, "no.")], "piece": "plate-s4"},
    "6": {"win": (24.85, 28.30), "warp": [(0.4, "gulp."), (1.55, "purest")], "piece": "plate-s6"},
    "7": {"win": (28.30, 31.30), "warp": [(2.8, "cramps")], "piece": "plate-s7"},
}
# how each real cut-out is matched to its stand-in: the size measured on (h = bbox height, w = width, m = the longer side)
# and the anchor rule (the same body point the stand-in's anchor marks)
PIECE = {("1", "hand-glass"): "hand-glass-s1", ("1", "student-hand"): "student-hand-s1", ("4", "pettenkofer"): "pettenkofer-s4",
         ("6", "pettenkofer"): "pettenkofer-s6", ("7", "hand"): "hand-s7"}
FIT = {"hand-glass-s1": ("h", "top"), "student-hand-s1": ("w", "left"), "pettenkofer-s4": ("h", "bottom"),
       "pettenkofer-s6": ("h", "bottom"), "hand-s7": ("m", "center")}
# the real plates put things in other places than the stand-ins (measured on a 0.1 grid, 2026-11-20), so the
# positions are re-set here; the TIMES stay the approved ones (warped onto Liam's words). Key lists match the
# stand-in keys one by one. SIZE: a target piece height (frame fractions) where the plate's scale differs from the
# stand-in's (s4: Pettenkofer behind the bench is as big as Matt, ≈ 0.24 of the frame, not the stand-in's MS).
SIZE = {"pettenkofer-s4": 0.33}   # v2 plate (close OTS): waist on the bench's far edge, head top ≈ 0.16 (glass ≈ 7 cm = 0.03 H)
REAL = {
    # v2 plate-s1 (2026-11-20): the head lower (hair top 0.36, under the hook card), his mouth at (0.63, 0.62)
    "1": {"actors": {"hand-glass": [(0.60, 0.93), (0.63, 0.625)],                 # the glass rim rises to his lower lip
                     "student-hand": [(1.05, 0.84), (0.86, 0.82), (0.76, 0.81)]}},  # reaches in, stops short of his wrist
    # v2 plate-s4: a true over-the-shoulder; he stands behind the near bench in the gap between the two backs
    "4": {"actors": {"pettenkofer": [(0.48, 0.49), (0.48, 0.49)]}, "glint": (0.814, 0.252)},
    "6": {"actors": {"pettenkofer": [(0.40, 1.02), (0.40, 1.02)]}},
    "7": {"actors": {"hand": [(0.47, 0.64), (0.47, 0.64)]},                       # on the bare wood, arm from lower right
          # v2 sheet: start at the 1.10 framing so the sleeve end and the sheet corner stay out of frame from frame 0
          "cam": [(1.10, 0, -2), (1.16, 0, -2)]},
}


def _word_t(word: str, win) -> float:
    for w in WORDS:
        if w["word"].lower() == word.lower() and win[0] <= w["start"] < win[1]:
            return w["start"] - win[0]
    raise SystemExit(f"'{word}' not in the window {win}")


def _warp_fn(shot, spec):
    real_d = spec["win"][1] - spec["win"][0]
    pts = [(0.0, 0.0)] + [(e, _word_t(w, spec["win"])) for e, w in spec["warp"]] + [(shot["dur"], real_d)]
    xs, ys = zip(*pts)
    return lambda t: float(np.interp(t, xs, ys)), real_d


def _bbox_fit(im: Image.Image, mode: str) -> float:
    b = im.getbbox()
    return {"h": b[3] - b[1], "w": b[2] - b[0], "m": max(b[2] - b[0], b[3] - b[1])}[mode]


def _anchor(im: Image.Image, rule: str):
    a = np.array(im.getchannel("A")) > 128
    ys, xs = np.nonzero(a)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if rule == "top":            # the glass rim: the middle of the opaque pixels in the top 6 % of the piece
        band = ys < y0 + 0.06 * (y1 - y0)
        return xs[band].mean() / im.width, y0 / im.height
    if rule == "left":           # the fingertips: the leftmost 6 %
        band = xs < x0 + 0.06 * (x1 - x0)
        return x0 / im.width, ys[band].mean() / im.height
    if rule == "bottom":
        return (x0 + x1) / 2 / im.width, y1 / im.height
    if rule == "center":
        return (x0 + x1) / 2 / im.width, (y0 + y1) / 2 / im.height
    raise ValueError(rule)


def _soften_writing(im: Image.Image, keep: float = 0.25) -> Image.Image:
    """Free fix (2026-11-20): pose-hand-s7 came back with "Lorem ipsum ..." on the sheet (L15 again, inside a pose sheet).
    The ink strokes inside the paper are inpainted with the paper and `keep` of them blended back: faint marks, no letters.
    v2 sheet (2026-11-20): the clutched sheet came back blank, so the flat one keeps only 10 % (no pop at the dissolve)."""
    import cv2
    rgba = np.array(im)
    rgb = np.ascontiguousarray(rgba[..., :3])
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    paper = ((hsv[..., 1] < 40) & (hsv[..., 2] > 170) & (rgba[..., 3] > 200)).astype(np.uint8)
    region = cv2.morphologyEx(paper, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    ink = (region > 0) & (paper == 0) & (hsv[..., 1] < 60) & (hsv[..., 2] < 170)
    ink = cv2.dilate(ink.astype(np.uint8), np.ones((3, 3), np.uint8))
    clean = cv2.inpaint(rgb, ink * 255, 5, cv2.INPAINT_TELEA)
    out = np.where(ink[..., None] > 0, ((1 - keep) * clean + keep * rgb).astype(np.uint8), rgb)
    return Image.fromarray(np.dstack([out, rgba[..., 3]]), "RGBA")


def _no_paper_s1(plate: Image.Image) -> Image.Image:
    """Free fix (2026-11-20): plate-s1 v2 has the edge of a sheet of paper at the bottom right (x > 0.5, y > 0.9), against
    "nothing lying in front of him": the light paper pixels there are inpainted from his dark coat."""
    import cv2
    rgba = np.array(plate)
    rgb = np.ascontiguousarray(rgba[..., :3])
    h, w = rgb.shape[:2]
    v = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[..., 2]
    m = np.zeros((h, w), np.uint8)
    m[int(0.88 * h):, int(0.45 * w):] = (v[int(0.88 * h):, int(0.45 * w):] > 90).astype(np.uint8)
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))
    out = cv2.inpaint(rgb, m * 255, 21, cv2.INPAINT_TELEA)
    return Image.fromarray(np.dstack([out, rgba[..., 3]]), "RGBA")


PLATE_FIX = {"1": _no_paper_s1}
SOFTEN = {("hand-s7", "flat"): 0.10}


def _real_piece(name: str, standin):
    frames_s, _ = standin
    d = P / "assets/images/sprites" / name
    meta = json.load(open(d / "sprites.json", encoding="utf-8"))
    mode, rule = FIT[name]
    first_state = next(iter(frames_s))
    real = {s: Image.open(d / fs[0]).convert("RGBA") for s, fs in meta["frames"].items()}
    real = {s: _soften_writing(im, SOFTEN[(name, s)]) if (name, s) in SOFTEN else im for s, im in real.items()}
    missing = set(frames_s) - set(real)
    if missing:
        raise SystemExit(f"{name}: the paid sheet has no state {missing} (cut it with these names)")
    target = SIZE[name] * H if name in SIZE else _bbox_fit(frames_s[first_state], mode)
    k = target / _bbox_fit(real[first_state], "h" if name in SIZE else mode)
    # premultiplied resize: fx_prep leaves stray colours (magenta, cyan) under alpha 0, and a straight LANCZOS resize
    # bleeds them into the edge as a pink line (s7 v2, 2026-11-20); browsers (Remotion) already scale premultiplied
    real = {s: im.convert("RGBa").resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
               .convert("RGBA") for s, im in real.items()}
    return real, _anchor(real[first_state], rule)



def build(n: str):
    shot = hp.SHOTS[n]()
    spec = SHOT[n]
    warp, real_d = _warp_fn(shot, spec)
    plate = Image.open(P / "assets/images/refs" / f"{spec['piece']}.png").convert("RGBA").resize((W, H), Image.LANCZOS)
    pth = P / "review/hero" / f"_plate-{n}.png"
    if n in PLATE_FIX:
        plate = PLATE_FIX[n](plate)
    plate.save(pth)
    shot["plate"] = pth
    shot.pop("fg", None)                                   # the stand-in's drawn foreground; the real plate has its own
    for a in shot["actors"]:
        name = PIECE[(n, a["id"])]
        a["piece"] = _real_piece(name, a["piece"])
        pos = REAL[n]["actors"][a["id"]]
        assert len(pos) == len(a["keys"]), (n, a["id"])
        for k, (x, y) in zip(a["keys"], pos):
            k["t"], k["x"], k["y"] = warp(k["t"]), x, y
    for i, c in enumerate(shot["cam"]):
        c["t"] = warp(c["t"])
        if "cam" in REAL[n]:
            c["scale"], c["x"], c["y"] = REAL[n]["cam"][i]
    for key in ("focus", "drain"):
        if key in shot:
            shot[key] = [(warp(t), v) for t, v in shot[key]]
    if "swell" in shot:
        t0, d_, amt = shot["swell"]
        shot["swell"] = (warp(t0), d_, amt)
    if "glint" in shot:
        shot["glint"] = (*REAL[n].get("glint", shot["glint"][:2]), warp(shot["glint"][2]))
    shot["hero_at"] = warp(shot["hero_at"])
    shot["crumple"] = [warp(t) for t in shot.get("crumple", [])]
    shot["clicks"] = []
    shot["words"] = [(w["start"] - spec["win"][0], w["word"]) for w in WORDS if spec["win"][0] <= w["start"] < spec["win"][1]]
    keyw = {w.lower() for _, w in spec["warp"]}
    shot["words"] = [(t, w.upper() if w.lower() in keyw else w) for t, w in shot["words"]]
    shot["dur"] = real_d
    shot["timing"] = "Liam's real timing"
    return shot, spec


def render(n: str):
    shot, spec = build(n)
    out = P / "review/hero"
    mp4 = out / f"{n}-real.mp4"
    frames = round(shot["dur"] * FPS)
    a0, d = spec["win"][0], shot["dur"]
    sfx = "".join(f"anoisesrc=d=0.45:c=pink:a=0.6,highpass=f=1800,tremolo=f=28:d=0.95,afade=t=in:d=0.03,"
                  f"afade=t=out:st=0.2:d=0.25,adelay={int(c * 1000)}|{int(c * 1000)},apad=whole_dur={d}[s{i}];"
                  for i, c in enumerate(shot["crumple"]))
    mix = f"[1:a]atrim={a0}:{a0 + d},asetpts=PTS-STARTPTS[n];" + sfx + \
          "[n]" + "".join(f"[s{i}]" for i in range(len(shot["crumple"]))) + \
          f"amix=inputs={1 + len(shot['crumple'])}:normalize=0:duration=first[a]"
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
           "-i", str(NARR), "-filter_complex", mix, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "20", "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    keep = {0: None, min(frames - 1, round(shot["hero_at"] * FPS)): None, frames - 1: None}
    for i in range(frames):
        t = i / FPS
        world, boxes = hp._world(shot, t)
        fr, sb, s = hp._camera(world, shot["cam"], t, boxes)
        fr = hp._overlay(fr.convert("RGB"), shot, t, sb, s)
        proc.stdin.write(fr.tobytes())
        if i in keep:
            keep[i] = fr.copy()
    proc.stdin.close()
    proc.wait()
    sheet = Image.new("RGB", (OW * 3 + 20, OH), "white")
    for j, fr in enumerate(keep.values()):
        sheet.paste(fr, (j * (OW + 10), 0))
    sheet.save(out / f"{n}-real-sheet.jpg", quality=88)
    return mp4


def pieces_sheet() -> Path:
    """review/hero/pieces.jpg: every paid piece on one contact sheet (the approval page shows it), name under each."""
    from PIL import ImageDraw
    refs = P / "assets/images/refs"
    names = ["sheet-pettenkofer", "sheet-students", "plate-s1", "sprite-hand-glass-s1", "sprite-student-hand-s1",
             "plate-s4", "pose-pettenkofer-s4", "plate-s6", "pose-pettenkofer-s6", "plate-s7", "pose-hand-s7"]
    th = 420
    tiles = []
    for n in names:
        im = Image.open(refs / f"{n}.png").convert("RGB")
        im = im.resize((round(im.width * th / im.height), th), Image.LANCZOS)
        t = Image.new("RGB", (im.width, th + 34), "white")
        t.paste(im, (0, 0))
        ImageDraw.Draw(t).text((6, th + 8), n + (" (v2)" if (refs / "v1" / f"{n}.png").exists() else ""), fill="black")
        tiles.append(t)
    rows, row, wmax = [], [], 2600
    for t in tiles:
        if row and sum(x.width + 10 for x in row) + t.width > wmax:
            rows.append(row); row = []
        row.append(t)
    rows.append(row)
    out = Image.new("RGB", (max(sum(x.width + 10 for x in r) for r in rows), len(rows) * (th + 44)), "white")
    for i, r in enumerate(rows):
        x = 0
        for t in r:
            out.paste(t, (x, i * (th + 44))); x += t.width + 10
    path = P / "review/hero/pieces.jpg"
    out.save(path, quality=85)
    return path


if __name__ == "__main__":
    args = sys.argv[1:] or list(SHOT)
    if "pieces" in args:
        print(pieces_sheet())
    for k in [a for a in args if a != "pieces"]:
        print(render(k))
