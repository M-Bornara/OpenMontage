"""A short window of the long (start..end seconds) with its sound, without the 20-minute full render: remotion render --frames + the matching bit of mix.wav.
    python channels/storybook-medical/scripts/render_window.py hc002-l 88.5 93.5 cb17-preview     -> projects/hc002-l/renders/cb17-preview.mp4
Run `episode.py build` and `mix` first (props and mix must match the edit). Used 2026-11-25 for the row 17 HIT callback."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import episode  # noqa: E402


def main(pid: str, start: float, end: float, name: str) -> Path:
    p = episode.proj(pid)
    rem = p / "remotion"
    for f in ("StorybookLong.tsx", "ComicFx.tsx"):
        shutil.copy(episode.KIT / "remotion" / f, rem / f)
    composer = episode.REPO / "remotion-composer"
    entry = episode.tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    out = p / "renders"
    f0, f1 = int(round(start * 30)), int(round(end * 30)) - 1
    silent, final = out / f"{name}-silent.mp4", out / f"{name}.mp4"
    subprocess.run(["npx", "remotion", "render", str(entry), "StorybookLong", str(silent), f"--props={(rem / 'props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", f"--frames={f0}-{f1}", "--concurrency=8", "--log=error"],
                   cwd=composer, check=True, shell=sys.platform == "win32")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-ss", f"{f0 / 30:.3f}", "-t", f"{(f1 - f0 + 1) / 30:.3f}", "-i", str(p / "assets/audio/mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)], check=True)
    silent.unlink(missing_ok=True)
    print(final, f"{episode.duration(final):.2f}s")
    return final


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
