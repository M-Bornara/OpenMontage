"""HC002-L (review 2026-11-25): +3.6 s of silence in the pause after "He went to Chile." so the map has 5 s and the ship ambience has room.
Uses the channel's pad_narration (never cuts anything; the untouched take is kept as narration.unpadded.wav), then moves every
row time and chapter time at or after the pad by the same amount (the unpadded copies are kept, so running it twice never doubles it).
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/pad_hc002l.py
"""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, "channels/storybook-medical/scripts")
import pad_narration  # noqa: E402

PID, AFTER, SECONDS = "hc002-l", "He went to Chile", 3.6
P = Path("projects") / PID
ep = json.load(open(P / "episode.json", encoding="utf-8"))
ep.setdefault("narration", {})["pads"] = [{"after": AFTER, "seconds": SECONDS}]
json.dump(ep, open(P / "episode.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)

A = P / "artifacts"
for n in ("row_times", "chapters"):
    if not (A / f"{n}.unpadded.json").exists():
        shutil.copy(A / f"{n}.json", A / f"{n}.unpadded.json")
pad_narration.main(PID)
raw = json.load(open(A / "word_timestamps.unpadded.json", encoding="utf-8"))
toks = [w["word"].lower().strip(".,") for w in raw]
i = next(k for k in range(len(toks) - 3) if toks[k:k + 4] == ["he", "went", "to", "chile"])
cut = (raw[i + 3]["end"] + raw[i + 4]["start"]) / 2          # where pad_narration put the silence
sh = lambda t: round(t + SECONDS, 3) if t >= cut else t       # noqa: E731
rt = json.load(open(A / "row_times.unpadded.json", encoding="utf-8"))
json.dump({k: [sh(a), sh(b)] for k, (a, b) in rt.items()}, open(A / "row_times.json", "w", encoding="utf-8"), indent=1)
ch = json.load(open(A / "chapters.unpadded.json", encoding="utf-8"))
json.dump([{**c, **{k: sh(c[k]) for k in ("start", "end") if k in c}} for c in ch], open(A / "chapters.json", "w", encoding="utf-8"), indent=1)
print(f"pad at {cut:.3f} s, +{SECONDS} s; rows and chapters after it moved")
