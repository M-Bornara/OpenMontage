"""A SHORT preview of the first seconds of the long (default 0-20 s), without the 20-minute full render: remotion render --frames from the project's built props,
the matching bit of mix.wav, then the cut audit on the cuts inside it (review/cut_audit_cold/) and the background check.
    python channels/storybook-medical/scripts/render_cold_preview.py hc002-l [seconds=20]   -> projects/hc002-l/renders/cold-open-preview.mp4
Run `episode.py build` and `mix` first (props and mix must match the edit)."""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bg_similarity  # noqa: E402
import cut_audit  # noqa: E402
import episode  # noqa: E402


def main(pid: str, seconds: float = 20.0) -> dict:
    p = episode.proj(pid)
    rem = p / "remotion"
    for f in ("StorybookLong.tsx", "ComicFx.tsx"):
        shutil.copy(episode.KIT / "remotion" / f, rem / f)
    composer = episode.REPO / "remotion-composer"
    entry = episode.tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    out = p / "renders"
    silent, final = out / "cold-open-silent.mp4", out / "cold-open-preview.mp4"
    n = int(round(seconds * 30))
    t0 = time.time()
    subprocess.run(["npx", "remotion", "render", str(entry), "StorybookLong", str(silent), f"--props={(rem / 'props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", f"--frames=0-{n - 1}", "--concurrency=8", "--log=error"],
                   cwd=composer, check=True, shell=sys.platform == "win32")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-t", f"{seconds}", "-i", str(p / "assets/audio/mix.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(final)], check=True)
    print(f"{final}  {episode.duration(final):.2f}s  rendered in {time.time() - t0:.0f}s")
    res = cut_audit.audit(pid, final, until=seconds, out_name="cut_audit_cold")
    bg = bg_similarity.check(pid)
    print(f"background check: {len(bg)} similar pair(s)")
    for b in bg:
        print("  " + b)
    res["bg"] = bg
    return res


if __name__ == "__main__":
    r = main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 20.0)
    sys.exit(1 if r["failures"] or r["bg"] else 0)
