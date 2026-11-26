"""HC002-L clip map (Mahdi 2026-11-25, preview v19 review, item 2): for EVERY shot in the long: row, timecode, the picture used, and any existing clip of the
same scene (HC002-S1 Short layered clips, row 49 Kling / Omni, row 19, C2, the failed tests). Written from projects/hc002-l/episode.json, so it follows the edit.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/clip_map_hc002l.py      (from the repo root)
Output: projects/hc002-l/review/clip_map.csv and review/clip_map.json (the table for the approval page)."""
import csv
import json
import re
from pathlib import Path

P = Path("projects/hc002-l")
ep = json.load(open(P / "episode.json", encoding="utf-8"))
fmt = lambda t: f"{int(t // 60)}:{t % 60:04.1f}"

# scene -> existing clips. status: USED (in the cut at natural speed and length), FAIL (kept on disk, not used: why), ALT (passes, held), 9:16 (S1 Short, wrong format)
S1_NOTE = "HC002-S1 Short layered clip {s} exists (1080x1920, 9:16, captions burned in): does not match the 16:9 frame"
CLIPS = {
    "r19": "USED: row19-oxcart-omni-v1 (Omni, 5.0 s natural speed and length); then a tight still for the rest of the row. S1 s09 preview is 9:16: no",
    "r19d": "follows the row-19 clip (its remainder)",
    "r26": "SCENE MATCHES, NOT USED: row26-farmhouse-omni-v1 (5.0 s): FAIL, his face is redrawn as he walks toward the camera (breaks the shut-eye rule) and leaves appear. Flagged by Mahdi (~2:09)",
    "r45": "SCENE MATCHES, NOT USED: row45-stable-omni-v1 (5.0 s): FAIL, white breath scribbles about 2-3.5 s; row45-stable-omni-v2: FAIL, a second brush appears 0.5-1.3 s. Flagged by Mahdi (~3:45)",
    "r48": "SCENE MATCHES, NOT USED: row48-harbour-omni-v1 (5.0 s): FAIL, about seven gulls added to the empty sky from ~1.5 s",
    "r49": "USED: row49-coach-kling (Kling v2.1 pro, 5.07 s natural); ALT held: row49-coach-omni-v1 (also passes)",
    "r49d": "follows the row-49 clip (its remainder)",
    "r65": "USED: row65-evening-from49 (a graded wide crop of the Kling clip, natural speed and length)",
    "r65d": "follows the row-65 clip (its remainder): the horse-leg still Mahdi flagged (~5:41)",
    "c2": "USED: cold-c2-blast-omni-v1 (Omni, 4.0 s; plays 2.5 s here, natural speed)",
    "hit": "C2 footage again (natural speed, from 0.45 s) under the HIT layers; C3 retired",
    "r01": "CLIP SLOT waiting (not generated): pour, 0-3 s (Omni, one take); the still is the stand-in",
    "r01a": "CLIP SLOT waiting (not generated): tamp, 3-5.95 s (Omni, one take); the still is the stand-in",
    "r02a": "CLIP SLOT waiting (not generated): glance, 7.2-9.8 s (Omni); the two stills are the stand-in",
    "r02b": "CLIP SLOT waiting (see r02a)",
    "c1": "CLIP SLOT waiting (not generated): spark, 9.82-11.76 s (Omni); Tier A stand-in (still + comic kit). S1 s05/s01 previews are 9:16: no",
    "r10": S1_NOTE.format(s="s02 (shot 2a)"),
    "r16": S1_NOTE.format(s="s05 (shot 5)"),
    "r22": S1_NOTE.format(s="s11 (shot 11)"),
}
for k in ("cb17", "cb40", "cb67"):
    CLIPS[k] = "C2 footage again (natural speed, from 0.45 s) under the HIT layers"
    CLIPS[k + "g"] = "Gage down (cold-b5-dust still, 0.2 s)"

rows, table = [], []
for s in ep["shots"]:
    sid, src = s["id"], s["source"].split("/")[-1]
    kind = "clip" if src.endswith(".mp4") else ("brand" if s["source"].startswith("brand:") else "still")
    note = CLIPS.get(sid, "none")
    m = re.match(r"r(\d+)", sid)
    row = m.group(1) if m else ("cold open" if sid in ("c1", "c2", "hit", "c4") else sid.upper())
    rows.append([sid, row, fmt(s["start"]), fmt(s["end"]), round(s["end"] - s["start"], 2), src, kind, note])
    table.append([sid, fmt(s["start"]), f"{s['end'] - s['start']:.1f} s", src + (" (clip)" if kind == "clip" else ""), note])
with open(P / "review/clip_map.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["shot", "row", "start", "end", "seconds", "picture used", "kind", "existing clip of the same scene"])
    w.writerows(rows)
json.dump({"head": ["Shot (row)", "From", "Length", "Picture used", "Existing clip of the same scene"], "rows": table}, open(P / "review/clip_map.json", "w", encoding="utf-8"), indent=1)
n_clip = sum(1 for r in rows if r[6] == "clip")
print(f"{len(rows)} shots, {n_clip} use a clip; map: {P / 'review/clip_map.csv'}")
