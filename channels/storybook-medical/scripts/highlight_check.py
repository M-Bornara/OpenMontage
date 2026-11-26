"""Regression frame for the marker behind highlighted words (review 2026-11-25, preview v19: the quote card's marker was HALF the text height
because it was `linear-gradient(transparent 55%, amber 55%)`; the caption marker had been fixed but the quote card never was).

Renders ONE frame of the long at 2x (3840 x 2160): the first quote card, at the moment its highlight is fully lit, then measures it:
  - the marker box (the amber pixels) must reach above the top and below the bottom of the glyph ink inside it (nothing sits in a half-height strip)
  - and be at least 90 % of the card text's own line height (54 px x 1.35 at 1080p = 146 px at 2x).
The crop is saved for the human to LOOK at (a check that nobody looked at is not a fix):
    python channels/storybook-medical/scripts/highlight_check.py hc002-l        -> projects/hc002-l/review/highlight_check/quote_highlight_2x.png
`episode.py render` runs it for the long and stops on a failure.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import episode  # noqa: E402

LINE_PX_2X = 54 * 1.35 * 2          # the quote text: fontSize 54, lineHeight 1.35, at 2x


def render_frame(pid: str, out: Path) -> tuple[Path, dict]:
    p = episode.proj(pid)
    rem = p / "remotion"
    shutil.copy(episode.KIT / "remotion/StorybookLong.tsx", rem / "StorybookLong.tsx")    # the kit's current component, not the build's old copy
    ep = json.load(open(p / "episode.json", encoding="utf-8"))
    q = next(o for o in sorted(ep["overlays"], key=lambda o: o["start"]) if o["kind"] == "quote" and o.get("highlight"))
    frame = int(round((q["start"] + 1.0) * 30))                                           # 1.0 s in: the glow is full (it ramps over 12-30 frames)
    composer = episode.REPO / "remotion-composer"
    entry = episode.tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    png = out / "frame_2x.png"
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["npx", "remotion", "still", str(entry), "StorybookLong", str(png), f"--props={(rem / 'props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", f"--frame={frame}", "--scale=2", "--log=error"],
                   cwd=composer, check=True, shell=sys.platform == "win32")
    return png, q


def measure(png: Path, out: Path) -> tuple[bool, str]:
    im = cv2.imread(str(png))
    b, g, r = [im[..., i].astype(int) for i in range(3)]
    # the marker: amber over paper (about 235, 188, 115 RGB); paper is 241, 230, 204 and its gradient, ink is near black
    amber = ((np.abs(r - 235) < 22) & (np.abs(g - 188) < 22) & (np.abs(b - 115) < 26)).astype(np.uint8)
    H, W = amber.shape
    band = np.zeros_like(amber)
    band[int(H * 0.40):int(H * 0.56), int(W * 0.20):int(W * 0.80)] = 1          # the quote card sits in the middle of the frame (the arm of the still has a similar tone elsewhere)
    amber *= band
    amber = cv2.morphologyEx(amber, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(amber)
    if n < 2:
        return False, "no marker found in the frame"
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h, _ = st[i]
    ink = (cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)[y - 40:y + h + 40, x:x + w] < 90)
    rows = np.where(ink.any(axis=1))[0]
    if not len(rows):
        return False, "no glyph ink inside the marker"
    top, bot = y - 40 + rows.min(), y - 40 + rows.max()
    covers = y <= top and y + h >= bot
    tall = h >= 0.9 * LINE_PX_2X
    msg = f"marker {h}px tall (line {LINE_PX_2X:.0f}px), glyph ink {bot - top}px, marker top {y} vs ink top {top}, marker bottom {y + h} vs ink bottom {bot}"
    crop = im[max(0, y - 140):y + h + 140, max(0, x - 520):x + w + 520]
    cv2.imwrite(str(out / "quote_highlight_2x.png"), crop)
    return bool(covers and tall), msg + (" · OK" if covers and tall else " · FAIL: the marker does not cover the full text height")


def check(pid: str) -> list[str]:
    out = episode.proj(pid) / "review/highlight_check"
    png, q = render_frame(pid, out)
    ok, msg = measure(png, out)
    print(f"highlight check ({q['text'][:34]!r}): {msg}\n  crop: {out / 'quote_highlight_2x.png'}")
    return [] if ok else [f"HIGHLIGHT: {msg}"]


if __name__ == "__main__":
    bad = check(sys.argv[1] if len(sys.argv) > 1 else "hc002-l")
    sys.exit(1 if bad else 0)
