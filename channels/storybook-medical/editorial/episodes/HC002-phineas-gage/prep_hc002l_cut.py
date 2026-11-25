"""HC002-L first full cut (2026-11-25): every free asset the cut needs that is not already a still. No generation, no spend.
  - row17-doc.png      Harlow's 1868 skull engraving centred on aged paper (16:9)
  - row47-map.png      the Americas on parchment from Natural Earth (public domain); the route is drawn by the cut's "route" overlay
  - row57-split.png    left: the grey doorway of row 29, right: the warm coach of row 49
  - row49 clip         Kling 1920x1080 24 fps -> frame-blended to 30 fps (ffmpeg framerate), grain as for the 19 test; its last frame
  - row19 clip         the existing 1080p30 passing clip; its last frame
  - row65 clip         the row-49 clip, mirrored (the team walks home), a 1.25x crop, an evening grade, frame-blended to 30 fps; its last frame
  - row19/49/65-detail.png  tight crops of each clip's first frame: what the row cuts to when it is longer than its clip (never a frozen last frame)
  - assets/music/silent.mp3   a near-silent bed (no music in this cut; music is held)
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/prep_hc002l_cut.py"""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

P = Path("projects/hc002-l")
K = P / "assets/images/keyframes16x9"
V = P / "assets/video"
W, H = 2752, 1536
ff = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", *map(str, a)], check=True)


def row17():
    eng = Image.open("projects/hc002-s1/refs/harlow_skull_1868_full.png").convert("RGB")
    bg = tuple(int(v) for v in np.asarray(eng.crop((0, 0, 40, 40))).reshape(-1, 3).mean(axis=0))
    out = Image.new("RGB", (W, H), bg)
    # aged paper: a soft vignette
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse((-W // 3, -H // 3, W + W // 3, H + H // 3), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), tuple(max(0, c - 55) for c in bg))
    out = Image.composite(out, dark, vig)
    h = int(H * 0.94)
    e = eng.resize((int(eng.width * h / eng.height), h), Image.LANCZOS)
    out.paste(e, ((W - e.width) // 2, (H - h) // 2))
    out.save(K / "row17-doc.png")


def land_polys():
    d = json.load(open(Path.home() / ".cache/openmontage/naturalearth/ne_50m_land.geojson", encoding="utf-8"))
    for f in d["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            yield poly


LON0, LON1, LAT0, LAT1 = -165.0, 38.0, -62.0, 52.0


def px(lon, lat):
    return ((lon - LON0) / (LON1 - LON0) * W, (LAT1 - lat) / (LAT1 - LAT0) * H)


def row47():
    sea, land, ink = (232, 219, 184), (214, 196, 150), (58, 46, 34)
    img = Image.new("RGB", (W, H), sea)
    d = ImageDraw.Draw(img)
    for poly in land_polys():
        ring = poly[0]
        if all(not (LON0 - 5 < x < LON1 + 5 and LAT0 - 5 < y < LAT1 + 5) for x, y in ring):
            continue
        pts = [px(x, y) for x, y in ring]
        d.polygon(pts, fill=land)
        d.line(pts + [pts[0]], fill=ink, width=5, joint="curve")
    rng = np.random.default_rng(2)
    grain = rng.normal(0, 5, (H, W, 1)).astype(np.float32)
    arr = np.clip(np.asarray(img).astype(np.float32) + grain, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr)
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse((-W // 4, -H // 4, W + W // 4, H + H // 4), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(260))
    img = Image.composite(img, Image.new("RGB", (W, H), (150, 128, 90)), v)
    d = ImageDraw.Draw(img)
    for lon, lat in ((-71.06, 42.36), (-71.6, -33.05)):          # Boston (where Gage was in 1849-50), Valparaiso
        x, y = px(lon, lat)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=(58, 46, 34))
        d.ellipse((x - 11, y - 11, x + 11, y + 11), fill=(232, 163, 61))
    img.save(K / "row47-map.png")


def row57():
    left = Image.open(K / "row29-doorway-v1-flip.png").convert("L").convert("RGB")
    right = Image.open(K / "row49-coach-v2-flip.png").convert("RGB")
    out = Image.new("RGB", (W, H))
    out.paste(left.crop((W // 4, 0, W // 4 + W // 2, H)), (0, 0))
    out.paste(right.crop((W // 4, 0, W // 4 + W // 2, H)), (W // 2, 0))
    ImageDraw.Draw(out).rectangle((W // 2 - 4, 0, W // 2 + 4, H), fill=(239, 230, 210))
    out.save(K / "row57-split.png")


def last_frame(mp4: Path, png: Path):
    ff("-sseof", "-0.1", "-i", mp4, "-frames:v", "1", png)


def clips():
    src49 = V / "row49-coach-test-v1.mp4"                   # Kling v2.1 pro, 1920x1080, 24 fps
    out49 = V / "row49-coach-kling-1080p30.mp4"
    ff("-i", src49, "-vf", "framerate=fps=30,noise=alls=5:allf=t", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-an", out49)
    last_frame(out49, K / "row49-clip-last.png")
    last_frame(V / "row19-oxcart-omni-v1-1080p30.mp4", K / "row19-clip-last.png")
    out65 = V / "row65-evening-from49.mp4"
    grade = ("hflip,crop=1536:864:384:216,scale=1920:1080:flags=lanczos,"
             "eq=brightness=-0.09:saturation=1.12:contrast=1.06,"
             "colorbalance=rs=0.22:gs=-0.02:bs=-0.22:rm=0.20:gm=0.0:bm=-0.20:rh=0.16:bh=-0.12,"
             "vignette=PI/5,framerate=fps=30,noise=alls=5:allf=t")
    ff("-i", src49, "-vf", grade, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-an", out65)
    last_frame(out65, K / "row65-clip-last.png")


def details():
    """Review 2026-11-25 (5): a clip plays at its natural speed and length and never freezes on its last frame. Where the row is longer than the
    clip, the remainder cuts to a DIFFERENT picture of the same scene: a tight crop of the clip's first frame (a Tier A still, slow push)."""
    for clip, png, (x, y, f) in (("row19-oxcart-omni-v1-1080p30", "row19-detail.png", (0.22, 0.20, 0.50)),
                                  ("row49-coach-kling-1080p30", "row49-detail.png", (0.12, 0.15, 0.45)),
                                  ("row65-evening-from49", "row65-detail.png", (0.02, 0.38, 0.55))):
        first = Path(K / f"_{png}.first.png")
        ff("-i", V / f"{clip}.mp4", "-frames:v", "1", first)
        im = Image.open(first)
        w, h = im.size
        box = (int(x * w), int(y * h), int((x + f) * w), int((y + f) * h))
        im.crop(box).resize((w, h), Image.LANCZOS).save(K / png)
        first.unlink()


def silent():
    d = P / "assets/music"
    d.mkdir(parents=True, exist_ok=True)
    ff("-f", "lavfi", "-i", "anoisesrc=color=pink:amplitude=0.0004:sample_rate=48000:duration=420", "-ac", "2", "-b:a", "128k", d / "silent.mp3")


if __name__ == "__main__":
    row17(); row47(); row57(); clips(); details(); silent()
    print("ok")
