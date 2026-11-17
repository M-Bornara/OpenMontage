"""Text-placement check for a Short (user, 2026-11-15: "the captions covering faces and labels ... make sure to re-evaluate
the text placements after each change"). Runs automatically at the end of `episode.py render`; also by hand:

    python channels/storybook-medical/scripts/text_check.py <project-id>

1. COLLISIONS (from episode.json, no render needed): every overlay (stamp, location card, name tag) against the caption
   band of the shot on screen at the same time; and overlays against each other.
2. SHEET (needs renders/final.mp4): one frame per caption page and per overlay, taken from the final render (the real
   positions after camera moves), tiled into review/text_sheet.jpg with a label (time, shot, text). Look at it for words
   on faces, hands, the FX target or a label. The machine can't see faces in a painting; this sheet is for the eye.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

REPO = Path(__file__).resolve().parents[3]
# vertical extent (px of 1920) below an element's "y" (its top): measured from StorybookShort.tsx
CAPTION_H, STAMP_H, LOCATION_H, NAMETAG_H = 200, 230, 190, 170
HEIGHTS = {"stamp": STAMP_H, "location": LOCATION_H, "nameTag": NAMETAG_H}
DEFAULT_Y = {"stamp": 300, "location": 250, "nameTag": 250}


def _span(o: dict) -> tuple[float, float]:
    y = o.get("y", DEFAULT_Y.get(o["kind"], 300))
    return y, y + HEIGHTS.get(o["kind"], 200)


def _x_span(o: dict) -> tuple[float, float]:
    if o["kind"] == "stamp" and "x" in o:          # a single letter stamp (A / B) is narrow
        half = 60 + 45 * len(o.get("text", ""))
        return o["x"] - half, o["x"] + half
    return 65, 888


def collisions(ep: dict, words: list[dict]) -> list[str]:
    shots, ovs, out = ep["shots"], ep.get("overlays", []), []
    spoken = [(w["start"], w["end"]) for w in words]
    for o in ovs:
        y0, y1 = _span(o)
        # caption band of every shot the overlay overlaps, but only while words are on screen
        for s in shots:
            a, b = max(o["start"], s["start"]), min(o["end"], s["end"])
            if a >= b or not any(ws < b and we > a for ws, we in spoken):
                continue
            c0 = s.get("captionY", 1180)
            c1 = c0 + CAPTION_H
            if y0 < c1 and c0 < y1:
                out.append(f"{a:6.2f}s  {o['kind']} '{o.get('text', '')}' (y {y0:.0f}-{y1:.0f}) overlaps the caption "
                           f"(y {c0}-{c1}) on {s['id']} ({Path(s['source']).stem})")
    for i, o in enumerate(ovs):
        for q in ovs[i + 1:]:
            if o["start"] < q["end"] and q["start"] < o["end"]:
                (a0, a1), (b0, b1) = _span(o), _span(q)
                (ax0, ax1), (bx0, bx1) = _x_span(o), _x_span(q)
                if a0 < b1 and b0 < a1 and ax0 < bx1 and bx0 < ax1:
                    out.append(f"{max(o['start'], q['start']):6.2f}s  {o['kind']} '{o.get('text', '')}' overlaps "
                               f"{q['kind']} '{q.get('text', '')}'")
    return out


def sheet(pid: str, ep: dict, words: list[dict], per: int = 3) -> Path | None:
    p = REPO / "projects" / pid
    video = p / "renders/final.mp4"
    if not video.exists():
        return None
    moments = []  # (time, label)
    for k in range(0, len(words), per):
        page = words[k:k + per]
        t = (page[0]["start"] + page[-1]["end"]) / 2
        moments.append((t, " ".join(w["word"] for w in page)))
    for o in ep.get("overlays", []):
        moments.append(((o["start"] + o["end"]) / 2, f"[{o['kind']}] {o.get('text', '')}"))
    if ep.get("_v2"):   # frame 1 (what people decide on), the hook card mid-way, the end line
        moments += [(0.0, "[v2] FRAME 1"), (ep["_v2"]["hook"]["until"] / 2, "[v2 hook card]"),
                    (ep["_v2"]["endLine"]["from"] + 1.0, "[v2 end line]")]
    moments.sort()
    W, H = 216, 384
    tiles = []
    tmp = p / "review/_text_frame.jpg"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    for t, label in moments:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1",
                        "-vf", f"scale={W}:{H}", str(tmp)], check=True)
        im = Image.open(tmp).convert("RGB")
        shot = next((s for s in ep["shots"] if s["start"] <= t < s["end"]), {"source": "?"})
        bar = Image.new("RGB", (W, 34), (20, 20, 20))
        d = ImageDraw.Draw(bar)
        d.text((4, 2), f"{t:5.1f}s {Path(shot['source']).stem}", fill=(255, 200, 80))
        d.text((4, 17), label[:34], fill=(230, 230, 230))
        tile = Image.new("RGB", (W, H + 34))
        tile.paste(bar, (0, 0))
        tile.paste(im, (0, 34))
        tiles.append(tile)
    tmp.unlink(missing_ok=True)
    cols = 8
    rows = (len(tiles) + cols - 1) // cols
    out = Image.new("RGB", (cols * W, rows * (H + 34)), (40, 40, 40))
    for i, tile in enumerate(tiles):
        out.paste(tile, ((i % cols) * W, (i // cols) * (H + 34)))
    dst = p / "review/text_sheet.jpg"
    out.save(dst, quality=82)
    return dst


def v2_collisions(ep: dict, words: list[dict]) -> list[str]:
    """Packaging v2: the hook card, CASE chip and end line against the captions and every overlay."""
    out = []
    for kind, label, t0, t1, y0, y1, x0, x1 in ep.get("_v2_boxes", []):
        for o in ep.get("overlays", []):
            a, b = max(t0, o["start"]), min(t1, o["end"])
            (oy0, oy1), (ox0, ox1) = _span(o), _x_span(o)
            if a < b and y0 < oy1 and oy0 < y1 and x0 < ox1 and ox0 < x1:
                out.append(f"{a:6.2f}s  {kind} '{label[:30]}' (y {y0:.0f}-{y1:.0f}) overlaps {o['kind']} '{o.get('text', '')}'")
        for s in ep["shots"]:
            a, b = max(t0, s["start"]), min(t1, s["end"])
            c0 = s.get("captionY", 1180)
            if a < b and any(w["start"] < b and w["end"] > a for w in words) and y0 < c0 + CAPTION_H and c0 < y1:
                out.append(f"{a:6.2f}s  {kind} '{label[:30]}' (y {y0:.0f}-{y1:.0f}) overlaps the caption (y {c0}) on {s['id']}")
    return out


def check(pid: str) -> list[str]:
    p = REPO / "projects" / pid
    ep = json.load(open(p / "episode.json", encoding="utf-8"))
    words = json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8"))
    import packaging_v2 as packaging
    ep = packaging.apply(ep, words)          # the same v2 timeline the build rendered
    words = packaging.caption_words(ep, words)
    issues = collisions(ep, words) + v2_collisions(ep, words)
    for m in issues:
        print("TEXT COLLISION", m)
    dst = sheet(pid, ep, words)
    print(f"text check: {len(issues)} collision(s); review sheet -> {dst}" if dst else
          f"text check: {len(issues)} collision(s); no render yet for the sheet")
    return issues


if __name__ == "__main__":
    check(sys.argv[1])
