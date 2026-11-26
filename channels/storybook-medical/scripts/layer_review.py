"""Review of one layered shot (plan/layered-animation.md §4; user 2026-11-16): a 3 s preview MP4 with its sound and a
3-frame contact sheet (start, middle, end) BEFORE the full cut, rendered by the same Remotion composition as the final.

    python channels/storybook-medical/scripts/layer_review.py <project-id> <shot> [--from S] [--seconds 3] [--build]

<shot> = the shot id in props.json (e.g. s05) or its still's stem (e.g. s3). --from = seconds into the shot where the
preview starts (default: 0.3 s before the first actor key). --build runs `episode.py build` and `mix` first (free).
Writes projects/<id>/review/layers/<shot>-preview.mp4 and <shot>-sheet.jpg (with the shot's layer plan under it).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import layers  # noqa: E402

FPS = 30


def _font(size: int):
    for f in ("C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def find_shot(ep: dict, props: dict, key: str) -> tuple[dict, dict]:
    for s, ps in zip(ep["shots"], props["shots"]):
        if key in (s["id"], Path(str(s["source"])).stem):
            return s, ps
    raise SystemExit(f"no shot {key!r} (ids: {[s['id'] for s in ep['shots']]})")


def review(pid: str, key: str, start: float | None = None, seconds: float = 3.0, build: bool = False) -> tuple[Path, Path]:
    p = REPO / "projects" / pid
    scripts = HERE
    if build:
        for step in ("build", "mix"):
            subprocess.run([sys.executable, "episode.py", step, pid], cwd=scripts, check=True)
    ep = json.load(open(p / "episode.json", encoding="utf-8"))
    rem = p / "remotion"
    props = json.load(open(rem / "props.json", encoding="utf-8"))
    shot, pshot = find_shot(ep, props, key)
    acts = [a for g in ("mg", "actors", "three", "fg") for a in (shot.get("layers") or {}).get(g, [])]
    first = min((a["keys"][0]["t"] for a in acts if a.get("keys")), default=0.0)
    off = max(0.0, first - 0.3) if start is None else start
    dur = min(seconds, pshot["end"] - pshot["start"] - off) if seconds > 0 else pshot["end"] - pshot["start"] - off
    a_f = round((pshot["start"] + off) * FPS)
    b_f = a_f + round(dur * FPS) - 1
    out = p / "review/layers"
    out.mkdir(parents=True, exist_ok=True)
    sid = shot["id"]
    silent = out / f"{sid}-silent.mp4"
    sys.path.insert(0, str(REPO))
    from tools.tool_registry import registry  # noqa: E402
    registry.discover()
    composer = REPO / "remotion-composer"
    entry = registry._tools["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    subprocess.run(["npx", "remotion", "render", str(entry), "StorybookShort", str(silent), f"--props={(rem / 'props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", f"--frames={a_f}-{b_f}", "--concurrency=8", "--log=error"],
                   cwd=composer, check=True, shell=sys.platform == "win32")
    mp4 = out / f"{sid}-preview.mp4"
    mix = p / "assets/audio/mix.wav"
    if mix.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-ss", f"{a_f / FPS:.3f}", "-t", f"{(b_f - a_f + 1) / FPS:.3f}",
                        "-i", str(mix), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                        str(mp4)], check=True)
        silent.unlink()
    else:
        silent.replace(mp4)
    # contact sheet: start, middle, end of the preview, with the time in the shot and the layer plan
    n = b_f - a_f + 1
    tiles = []
    # the tiles come from the frames the preview really has: with the mix muxed in, -shortest can drop a few frames
    got = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                          "stream=nb_read_frames", "-of", "csv=p=0", str(mp4)], capture_output=True, text=True).stdout
    n = min(n, int(got.strip().strip(",") or n))
    for j, fr in enumerate((0, n // 2, max(0, n - 1))):
        png = out / f"_{sid}-{j}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select=eq(n\\,{fr})", "-frames:v", "1", str(png)], check=True)
        im = Image.open(png).convert("RGB")
        im.thumbnail((540, 960))
        tiles.append((im, f"{off + fr / FPS:.2f} s in shot  ·  {pshot['start'] + off + fr / FPS:.2f} s in video"))
        png.unlink()
    plan = layers.layer_plan(shot)
    tw, th = tiles[0][0].size
    pad, head = 16, 44
    sheet = Image.new("RGB", (3 * tw + 4 * pad, th + head + pad + 28 * (len(plan) + 1) + pad), (24, 26, 28))
    d = ImageDraw.Draw(sheet)
    for j, (im, label) in enumerate(tiles):
        x = pad + j * (tw + pad)
        sheet.paste(im, (x, head))
        d.text((x, 12), ("START", "MIDDLE", "END")[j] + "  " + label, fill=(239, 230, 210), font=_font(18))
    y = head + th + pad
    d.text((pad, y), f"{pid} · {sid} ({Path(str(shot['source'])).name}) · layer plan", fill=(232, 163, 61), font=_font(18))
    for layer, what, motion in plan:
        y += 28
        d.text((pad, y), f"{layer:<6} {what:<28} {motion}", fill=(239, 230, 210), font=_font(16))
    jpg = out / f"{sid}-sheet.jpg"
    sheet.save(jpg, quality=90)
    print(f"preview {mp4}  ({dur:.2f} s from {off:.2f} s into the shot)\nsheet   {jpg}")
    return mp4, jpg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pid"); ap.add_argument("shot")
    ap.add_argument("--from", dest="start", type=float)
    ap.add_argument("--seconds", type=float, default=3.0)
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    review(a.pid, a.shot, a.start, a.seconds, a.build)
