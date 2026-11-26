"""Render SINGLE frames of the long (no full render) to look at new shots in context: remotion still at 1080p from the project's built props.
    python channels/storybook-medical/scripts/still_frames.py hc002-l <outdir> name=seconds [name=seconds ...]
e.g. still_frames.py hc002-l projects/hc002-l/review/hitcheck hit35=14.65 portrait=342.5
Run `episode.py build` first (the props must match the edit). Used 2026-11-25 to check the HIT shot, the dazed cut and the portrait without a re-render."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import episode  # noqa: E402


def main(pid: str, out: Path, items: list[str]):
    p = episode.proj(pid)
    rem = p / "remotion"
    for f in ("StorybookLong.tsx", "ComicFx.tsx"):
        shutil.copy(episode.KIT / "remotion" / f, rem / f)
    composer = episode.REPO / "remotion-composer"
    entry = episode.tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    out.mkdir(parents=True, exist_ok=True)
    for it in items:
        name, sec = it.split("=")
        png = out / f"{name}.png"
        subprocess.run(["npx", "remotion", "still", str(entry), "StorybookLong", str(png), f"--props={(rem / 'props.json').resolve()}",
                        f"--public-dir={(rem / 'public').resolve()}", f"--frame={int(round(float(sec) * 30))}", "--log=error"],
                       cwd=composer, check=True, shell=sys.platform == "win32")
        print(png)


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]).resolve(), sys.argv[3:])
