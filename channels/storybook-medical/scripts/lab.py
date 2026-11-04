"""Render a test reel for review (plan/editing-v2.md P8): python lab.py FocusReel [--frames 0-60]
Stages the kit's Remotion files into projects/_fxlab/remotion (its public/img holds the sample images + masks) and
writes projects/_fxlab/renders/<Reel>.mp4. Free: local render only."""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from episode import KIT, KIT_REMOTION, REPO, tools  # noqa: E402

reel = sys.argv[1]
extra = sys.argv[2:]
stage = REPO / "projects/_fxlab/remotion"
(stage / "public/img").mkdir(parents=True, exist_ok=True)
for f in KIT_REMOTION:
    shutil.copy(KIT / "remotion" / f, stage / f)
# music coverage: every cue must be at least as long as the section it scores (+ the 2 s crossfade tail), or the music
# would silently stop mid-section (HC001 cut v2 had 2.5 min without music: user review 2026-10-24)
props = next((a.split("=", 1)[1] for a in extra if a.startswith("--props=")), None)
if props:
    import json
    from episode import duration
    music = json.load(open(props, encoding="utf-8")).get("music", [])
    short = []
    for i, m in enumerate(music):
        need = m["to"] - m["from"] + (2 if i < len(music) - 1 else 0)
        have = duration(stage / "public" / m["src"]) - m.get("offset", 0)
        if not m.get("loop") and have + 0.05 < need:
            short.append(f"{m['src']}: {have:.1f}s for a {need:.1f}s section")
    if short:
        raise SystemExit("music cue shorter than its section (silence): " + "; ".join(short))
composer = REPO / "remotion-composer"
entry = tools()["video_compose"]._stage_atelier_project((stage / "index.tsx").resolve(), composer.resolve())
out = REPO / "projects/_fxlab/renders"
out.mkdir(parents=True, exist_ok=True)
dst = out / f"{reel}.mp4"
subprocess.run(["npx", "remotion", "render", str(entry), reel, str(dst), f"--public-dir={(stage / 'public').resolve()}",
                "--log=error", "--concurrency=8", *extra], cwd=composer, check=True, shell=sys.platform == "win32")
print("reel ->", dst)
