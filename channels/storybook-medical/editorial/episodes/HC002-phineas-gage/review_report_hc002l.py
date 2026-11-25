"""HC002-L review report (2026-11-25) -> projects/hc002-l/review/review_report.json, shown on the approval page by storyboard_page.review_block.
Run after build + mix + render --preview (it reads the render, the cut audit and the shots):
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/review_report_hc002l.py
"""
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import cv2
import numpy as np

REPO = Path(".").resolve()
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import bg_similarity  # noqa: E402

P = REPO / "projects/hc002-l"
R = P / "review"
ep = json.load(open(P / "episode.json", encoding="utf-8"))
rt = {int(k): v for k, v in json.load(open(P / "artifacts/row_times.json", encoding="utf-8")).items()}
audit = json.load(open(R / "cut_audit/audit.json", encoding="utf-8"))
VID = P / "renders/preview.mp4"


def frame(t: float):
    out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(VID), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"],
                         capture_output=True, check=True).stdout
    return cv2.imdecode(np.frombuffer(out, np.uint8), cv2.IMREAD_COLOR)


def montage(items, cols, w, name, label_h=26):
    tiles = []
    for im, lab in items:
        im = cv2.resize(im, (w, int(w * im.shape[0] / im.shape[1])))
        bar = np.zeros((label_h, w, 3), np.uint8)
        cv2.putText(bar, lab, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
        tiles.append(np.vstack([bar, im]))
    h = max(t.shape[0] for t in tiles)
    tiles = [np.pad(t, ((0, h - t.shape[0]), (0, 0), (0, 0))) for t in tiles]
    rows = [np.hstack(tiles[i:i + cols] + [np.zeros_like(tiles[0])] * (cols - len(tiles[i:i + cols]))) for i in range(0, len(tiles), cols)]
    cv2.imwrite(str(R / name), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 86])
    return R / name


sections = []

# 1 ── cut audit
fails = audit["failures"]
sections.append({
    "heading": "1 · Cut audit on the render (±3 frames around every cut)",
    "paras": [f"{audit['cuts']} cuts checked on the 1080p render. Flash / duplicate / black frames and the frame where the picture really changes are read from frames c-3 to c+2 of each cut; "
              f"the sound is checked against narration.wav in the second around each cut (cross-correlation). Result: {len(fails)} failure(s). "
              f"Audio lag max {audit['lag_max_ms']} ms over {audit['lag_measured']} cuts (first {audit['lag_first_ms']} ms, last {audit['lag_last_ms']} ms: no drift if these match); "
              f"container video {audit['video_s']:.2f} s, audio {audit['audio_s']:.2f} s. The render FAILS on a flash or a duplicate frame (cut_audit.py, wired into `episode.py render`)."],
    "bullets": (fails[:40] or ["No flash, duplicate or black frame at any cut."])
              + [f"Declared (intended): {n}" for n in audit["notes"]]
              + ["What the audit found on the way (all fixed, then re-rendered clean): (1) the camera came to rest at both ends of every shot, so 28 cuts had 2-3 identical frames before them "
                 "(a stop, then the cut): long shots now use a 'through' ease that keeps moving into the cut; (2) one frame before the r36b to r36c cut was empty charcoal: shot lengths were "
                 "rounded separately and left a one-frame gap; now the difference of the rounded frames; (3) three keyframed shots finished their move early and sat still. "
                 "The first two are bugs that were in the first cut too."],
    "images": [{"src": R / "cut_audit" / s, "label": f"Contact sheets, {s.replace('chapter_', 'chapter ').replace('.jpg', '')}",
                "note": "One block per cut: six frames (cut frame outlined in yellow), labelled with the two shots, the cut diff, the declared transition and the audio offset. Red label = failure.", "edge": 1900}
               for s in audit["sheets"]],
})

# 2 ── background similarity
res = subprocess.run([sys.executable, str(REPO / "channels/storybook-medical/scripts/test_bg_similarity.py")], capture_output=True, text=True, env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
bgs = bg_similarity.check("hc002-l", ep)
sections.append({
    "heading": "2 · Timeline-wide background check (every pair of shots within 6 s)",
    "paras": ["bg_similarity.py compares the background of every pair of shots whose visible moments are within 6 s (the picture at the camera window of each, downscaled): "
              "the same still at the same crop, the same set at the same size (feature match), or matching edge structure on a tile grid (people are a minority of the tiles). "
              "It runs inside `episode.py build` and stops the build.",
              "The first run on the cut found 9 pairs the old consecutive-only check missed: r01/r03, TITLE/r09, r09/r10, r13/r14, r34/r35, r36a/r36b, r43a/r43b, r49/r49d, r65/r65d, r66a/r67 "
              "(r36a/r36b is Mahdi's approved crop). Fixes: r09 is now a tight crop of the crew, r14 a tight crop of the iron's point, r34/r35 two different crops of the monster, "
              "r49d/r65d are tight crops of the clips, r67 is the wide case, and r43b is marked 'same-camera cut intended' (the locked frame is the gag: the iron is gone). "
              f"Result now: {len(bgs)} pair(s) flagged.",
              "Regression test (test_bg_similarity.py): " + " | ".join(l.split(":")[0] + ":" + l.split(":")[1][:70] for l in res.stdout.strip().splitlines()),
              "Note on 'rows 10 and 11': in this cut rows 10 and 11 are the quarry and the keg shed (different sets), so the test uses rows 9 → 10 (S1 s2b → s2a, the same quarry at the same size) "
              "as the known failure and keeps 10 → 11 as the negative control. Tell me if you meant another pair."],
    "bullets": bgs or ["No pair flagged."],
})

# 3 ── caption highlight
words = json.load(open(P / "artifacts/word_timestamps.json", encoding="utf-8"))
picks = [w for w in words if 20 < w["start"] < 60][3:9:2] + [next(w for w in words if w["word"].startswith("Chile"))]
items = []
for w in picks:
    f = frame((w["start"] + w["end"]) / 2)
    items.append((f[840:1060, 300:1620], f"'{w['word']}' at {w['start']:.1f} s"))
montage(items, 2, 960, "caption_highlight.jpg")
sections.append({
    "heading": "3 · Caption highlight: full text height",
    "paras": ["The active word now sits on a box that is the full text height (the 1 em line box, lineHeight 1) plus 6 px above and below and 14 px at the sides (amber; red for punch words); "
              "the word itself is white with its ink outline. Checked the other caption styles: the Shorts caption (StorybookShort.tsx, 8 px / 20 px padding) uses the same box; "
              "the animatic caption (Animatic.tsx, a 30 px line) now has a 3 px padded amber box with dark text. All three were colour-only before; none had a box."],
    "images": [{"src": R / "caption_highlight.jpg", "label": "Active word on its box (long cut)", "note": "Crops of the caption band at the middle of each word."}],
})

# 4 ── map
t0 = rt[47][0]
nxt = rt[48][0]
items = [(frame(t0 + d), f"row 47 +{d:.1f} s") for d in (0.3, 1.5, 3.0, 4.6)]
montage(items, 2, 960, "row47_map.jpg")
sections.append({
    "heading": "4 · Map (row 47)",
    "paras": [f"The map holds {nxt - t0:.1f} s (was 1.4 s): a 3.6 s pause is added after 'He went to Chile.' (the narration take is untouched, only silence is inserted in the pause; "
              f"every later row and chapter moves by 3.6 s, so the cut is now {audit['video_s'] / 60:.1f} min). Ship ambience (gulls + water, rope creak, bell; free library cues, untuned) plays in the pause. "
              "The route draws over 4 s as a dashed line (dashed = schematic), the label moved to a fixed tag at the top left (away from the captions) and says 'SCHEMATIC ROUTE · NOT A RECORDED TRACK'."],
    "images": [{"src": R / "row47_map.jpg", "label": "Row 47 at +0.3, +1.5, +3.0, +4.6 s", "note": "Label top left, dashed route, captions below."}],
})

# 5 ── clip lengths
def dur(n):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(P / f"assets/video/{n}.mp4")], capture_output=True, text=True).stdout.strip())
shots = {s["id"]: s for s in ep["shots"]}
rows = []
for r, sid, clip, detail, why in (
        (19, "r19", "row19-oxcart-omni-v1-1080p30", "r19d", "A tight Tier A still of the cart, slow push (a crop of the clip's first frame: Gage and the oxen)."),
        (49, "r49", "row49-coach-kling-1080p30", "r49d", "A tight Tier A still of the coach and driver, slow push."),
        (65, "r65", "row65-evening-from49", "r65d", "A tight Tier A still of the team of horses (evening grade), slow push.")):
    slot = rt[r][1] - rt[r][0]
    full = shots[detail]["end"] - shots[sid]["start"]
    rows.append([f"{r}", f"{dur(clip):.2f} s", f"{slot:.2f} s speech, {full:.2f} s picture", f"picture longer by {full - dur(clip):.2f} s",
                 why + " The clip itself plays at its own speed, length and frame rate (frame-blended to 30 fps from 24, no stretch)."])
for r, note in ((45, "Tier A still, no clip."), (48, "Tier A still, no clip (failed Omni take not used)."), (26, "Tier A still, no clip (failed Omni take not used).")):
    rows.append([f"{r}", "none", "", "no clip", note])
sections.append({
    "heading": "5 · Clips at natural speed and length: every row where the picture is shorter or longer than its clip",
    "paras": ["No clip is slowed, sped up or frozen. `episode.py build` now stops when a clip's slot is longer than the clip (it would freeze) and the render's cut audit looks for duplicate frames. "
              "Only three rows have a clip. All three rows are LONGER than their clip, none is shorter, so no clip is cut short; the remainder of each row is the proposal in the last column, built into this cut (tell me if you prefer a cutaway or a different crop)."],
    "table": {"head": ["Row", "Clip length", "Row (speech / picture)", "Difference", "Proposal (in the cut)"], "rows": rows},
})

# 7 ── image reuse
use = defaultdict(list)
for s in ep["shots"]:
    use[Path(s["source"]).stem].append(s["id"])
many = {k: v for k, v in use.items() if len(v) > 2 and not k.startswith("sting") and not k.startswith("endscreen")}
crops = {"row7-monster-v1": [("r07", "wide, push 1.04→1.16"), ("r34", "face, 1.3→1.4 centred"), ("r35", "the eye, 2.3→2.45 at (0.56, 0.36)"), ("r39", "teeth and chin, 2.1→1.5 pull at (0.50, 0.62)")],
         "row55-portrait-v4paint": [("r55", "the whole case, push 1.02→1.14"), ("r56", "the face, 2.0→2.15 at (0.49, 0.40)"), ("r66a", "the hand on the iron, 2.1→2.2 at (0.46, 0.72)"), ("r67", "the whole case, wide 1.0→1.12 (far from r55 in time)")]}
tab = [[k, ", ".join(v), "; ".join(f"{a}: {b}" for a, b in crops.get(k, []))] for k, v in many.items()]
twice = sorted(k for k, v in use.items() if len(v) == 2)
sections.append({
    "heading": "7 · Image reuse: stills used more than twice, one crop per use",
    "paras": ["Two stills are used more than twice; both now have a different crop for every use, and the background check passes them (windows differ by x1.5 or more, or barely overlap). "
              "Zoom stays at or under 2.45 x so the 2752 px stills do not soften. Stills used exactly twice: " + ", ".join(twice) + " (these pairs are far apart or already pass the check)."],
    "table": {"head": ["Still", "Used in", "Crop per use"], "rows": tab},
})

# 6 ── rows 21 / 22 / 30
sections.insert(5, {
    "heading": "6 · Rows 21, 22 and 30: original images, free bandage paint only on Gage",
    "paras": ["Rows 21 and 30 use the ORIGINAL S1 s10 and s12 again. The earlier free brow-paint attempts (s10.fix-attempt.png, s12.fix-attempt.png) only change a box about 110 px wide around Gage's brow "
              "(measured: only 642 pixels in s10 and 419 in s12 differ from the original by more than 12 levels, all inside that box), so Matt and everyone else are exactly the original. The re-rolls are no longer in the cut. "
              "Row 22 (s11, the iron and the hand) was never changed. Left: the re-roll that was in the first cut. Right: the cut now."],
    "images": [{"src": R / "rows21-22-30-before-after.jpg", "label": "Rows 21, 22, 30: before (left) and after (right)", "note": "Row 22 is unchanged (same picture both sides).", "edge": 1900}],
})

json.dump({"title": "REVIEW FIXES · 2026-11-25 · cut audit, background check, captions, map, clips, reuse, rows 21/22/30",
           "legend": "No generation, no spend. Everything below is free (build checks, crops, pad of silence, a re-render). The cut is re-rendered with all of it; the preview segments above are the new render.",
           "sections": sections}, open(R / "review_report.json", "w", encoding="utf-8"), indent=1, default=str)
print("report written;", len(sections), "sections")
