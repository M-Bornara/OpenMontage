"""Review of a Short's opening (packaging v2.1, C006 v2.1; user 2026-11-17): a 4 s preview MP4 with its sound and a
contact sheet of frames 0, 0.5, 1.5 and 3 s, rendered by the same Remotion composition as the final, BEFORE the full
render. The sheet also prints the card text, its rule checks and the hook timing.

    python channels/storybook-medical/scripts/hook_review.py <project-id> [--seconds 4] [--build]

--build runs `episode.py build` and `mix` first (free). Writes projects/<id>/review/hook/preview.mp4 and sheet.jpg.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import packaging_v2 as packaging  # noqa: E402
from layer_review import _font  # noqa: E402
from text_check import hook_card_problems  # noqa: E402

FPS = 30
MOMENTS = (0.0, 0.5, 1.5, 3.0)


def review(pid: str, seconds: float = 4.0, build: bool = False) -> tuple[Path, Path]:
    p = REPO / "projects" / pid
    if build:
        for step in ("build", "mix"):
            subprocess.run([sys.executable, "episode.py", step, pid], cwd=HERE, check=True)
    ep = json.load(open(p / "episode.json", encoding="utf-8"))
    words = json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8"))
    rem = p / "remotion"
    out = p / "review/hook"
    out.mkdir(parents=True, exist_ok=True)
    last = round(seconds * FPS) - 1
    silent = out / "_silent.mp4"
    sys.path.insert(0, str(REPO))
    from tools.tool_registry import registry  # noqa: E402
    registry.discover()
    composer = REPO / "remotion-composer"
    entry = registry._tools["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    subprocess.run(["npx", "remotion", "render", str(entry), "StorybookShort", str(silent), f"--props={(rem / 'props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", f"--frames=0-{last}", "--concurrency=8", "--log=error"],
                   cwd=composer, check=True, shell=sys.platform == "win32")
    mp4 = out / "preview.mp4"
    mix = p / "assets/audio/mix.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-t", f"{(last + 1) / FPS:.3f}", "-i", str(mix),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", str(mp4)], check=True)
    silent.unlink()

    tiles = []
    for t in MOMENTS:
        png = out / "_f.png"
        fr = min(last, round(t * FPS))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf", f"select=eq(n\\,{fr})", "-frames:v", "1", str(png)], check=True)
        im = Image.open(png).convert("RGB")
        im.thumbnail((540, 960))
        tiles.append((im, f"{t:.1f} s  (frame {fr})"))
        png.unlink()
    pk = packaging.config(ep) or {}
    card = (pk.get("hook") or {}).get("card", "")
    v2 = packaging.apply(ep, words)["_v2"]
    caps = packaging.caption_words(packaging.apply(ep, words), words)
    probs = hook_card_problems(ep, p)
    info = [f"{pid} · CASE {pk.get('case', 0):02d} · card: {card}",
            f"{len(packaging.card_words(card))} words · {len(packaging.card_lines(card))} lines · box <= {packaging.card_height(card)} px "
            f"(15% = {packaging.HOOK_MAX_H}) · amber: {', '.join(packaging.card_amber(card)) or '-'} · anchor {v2['hook']['anchor']}",
            f"full card on frame 0 · amber brightens 0-0.4 s · collapse into the chip {v2['hook']['until'] - 0.3:.2f}-{v2['hook']['until']:.2f} s · captions from "
            f"'{' '.join(w['word'] for w in caps[:4])}…'",
            "checks: " + ("all pass (words, lines, box, = publish.md hook_card)" if not probs else " | ".join(probs))]
    tw, th = tiles[0][0].size
    pad, head = 16, 40
    sheet = Image.new("RGB", (len(tiles) * tw + (len(tiles) + 1) * pad, head + th + pad + 30 * len(info) + pad), (24, 26, 28))
    d = ImageDraw.Draw(sheet)
    for j, (im, label) in enumerate(tiles):
        x = pad + j * (tw + pad)
        sheet.paste(im, (x, head))
        d.text((x, 10), label, fill=(239, 230, 210), font=_font(20))
    y = head + th + pad
    for k, line in enumerate(info):
        d.text((pad, y + 30 * k), line, fill=(232, 163, 61) if k == 0 else (239, 230, 210), font=_font(19))
    jpg = out / "sheet.jpg"
    sheet.save(jpg, quality=90)
    print(f"preview {mp4}\nsheet   {jpg}")
    for line in info:
        print("  " + line)
    return mp4, jpg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pid")
    ap.add_argument("--seconds", type=float, default=4.0)
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    review(a.pid, a.seconds, a.build)
