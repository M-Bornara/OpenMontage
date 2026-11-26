"""HC002-S1 cover image (FREE, user 2026-11-19): the shot 1 blast frame (Gage's silhouette thrown back + the flying bar)
instead of the skull engraving. Renders frames of shot 1 from the real composition with every text layer removed
(captions, stamps, hook card, CASE chip, end line) at 1440 x 2560, the size step_cover uses.

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/cover_frame_hc002s1.py 0.3 0.5 0.7   # try
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/cover_frame_hc002s1.py --pick 0.5    # keep

Tries go to review/cover-frames/; --pick writes assets/images/covers/s1-blast.png (publish.cover.image points there).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
P = REPO / "projects/hc002-s1"
FPS = 30


def render(t: float, out: Path):
    rem = P / "remotion"
    props = json.load(open(rem / "props.json", encoding="utf-8"))
    props.update(words=[], overlays=[])
    for k in ("hook", "caseNo", "endLine"):
        props.pop(k, None)
    clean = rem / "cover-frame-props.json"
    json.dump(props, open(clean, "w", encoding="utf-8"))
    sys.path.insert(0, str(REPO))
    from tools.tool_registry import registry  # noqa: E402
    registry.discover()
    composer = REPO / "remotion-composer"
    entry = registry._tools["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    subprocess.run(["npx", "remotion", "still", str(entry), "StorybookShort", str(out), f"--props={clean.resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", f"--frame={round(t * FPS)}", "--scale=1.3333334",
                    "--log=error"], cwd=composer, check=True, shell=sys.platform == "win32")


def main():
    args = sys.argv[1:]
    if args and args[0] == "--pick":
        t = float(args[1])
        dst = P / "assets/images/covers/s1-blast.png"
        dst.parent.mkdir(parents=True, exist_ok=True)
        src = P / f"review/cover-frames/s1-{t:.2f}.png"
        if src.exists():
            shutil.copy(src, dst)
        else:
            render(t, dst)
        print("cover image ->", dst)
        return
    out = P / "review/cover-frames"
    out.mkdir(parents=True, exist_ok=True)
    for a in args or ["0.3", "0.5", "0.7"]:
        f = out / f"s1-{float(a):.2f}.png"
        render(float(a), f)
        print(f)


if __name__ == "__main__":
    main()
