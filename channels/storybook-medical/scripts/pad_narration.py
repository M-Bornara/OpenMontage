"""Lengthen pauses in a Short's narration without re-recording (user, 2026-11-15: "the climax is too rushed").

Adds digital silence INSIDE an existing pause (after a word), never cuts anything (memory: narration-audio-processing).
Pads live in episode.json so the result is reproducible:
    "narration": {"pads": [{"after": "waited", "seconds": 0.7}, {"after": "both", "seconds": 1.0}]}
"after" is a phrase; the silence goes in the middle of the pause that follows its last word.
Always rebuilds from the untouched take (assets/audio/narration.unpadded.wav + artifacts/word_timestamps.unpadded.json,
saved on the first run), so running it twice never doubles a pad. Run after `episode.py narrate`, before the edit:
    python channels/storybook-medical/scripts/pad_narration.py <project-id>
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())  # noqa: E731


def main(pid: str) -> None:
    p = REPO / "projects" / pid
    wav, words_f = p / "assets/audio/narration.wav", p / "artifacts/word_timestamps.json"
    raw_wav, raw_words = p / "assets/audio/narration.unpadded.wav", p / "artifacts/word_timestamps.unpadded.json"
    if not raw_wav.exists():
        shutil.copy(wav, raw_wav)
        shutil.copy(words_f, raw_words)
    words = json.load(open(raw_words, encoding="utf-8"))
    pads = json.load(open(p / "episode.json", encoding="utf-8"))["narration"].get("pads", [])
    toks = [norm(w["word"]) for w in words]
    cuts = []  # (time in the raw take, seconds)
    for pad in pads:
        want = [norm(x) for x in pad["after"].split()]
        hit = next((i for i in range(len(toks) - len(want) + 1) if toks[i:i + len(want)] == want), None)
        if hit is None:
            raise SystemExit(f"pad phrase not found: {pad['after']!r}")
        last = hit + len(want) - 1
        if last + 1 >= len(words):
            raise SystemExit(f"pad after the last word: {pad['after']!r}")
        a, b = words[last]["end"], words[last + 1]["start"]
        cuts.append((round((a + b) / 2, 3), float(pad["seconds"])))
    cuts.sort()
    if not cuts:
        shutil.copy(raw_wav, wav)
        shutil.copy(raw_words, words_f)
        print("no pads: restored the untouched take")
        return
    # ffmpeg: split at each cut, put silence between the pieces, concat (sample-exact)
    sr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate,channels",
                         "-of", "csv=p=0", str(raw_wav)], capture_output=True, text=True).stdout.strip().split(",")
    rate, ch = int(sr[0]), int(sr[1])
    layout = "mono" if ch == 1 else "stereo"
    parts, labels, prev = [], [], 0.0
    for k, (t, sec) in enumerate(cuts):
        parts.append(f"[0:a]atrim={prev}:{t},asetpts=PTS-STARTPTS[p{k}]")
        parts.append(f"anullsrc=r={rate}:cl={layout},atrim=0:{sec}[z{k}]")
        labels += [f"[p{k}]", f"[z{k}]"]
        prev = t
    parts.append(f"[0:a]atrim={prev},asetpts=PTS-STARTPTS[p{len(cuts)}]")
    labels.append(f"[p{len(cuts)}]")
    parts.append(f"{''.join(labels)}concat=n={len(labels)}:v=0:a=1[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw_wav), "-filter_complex", ";".join(parts), "-map", "[out]",
                    "-ar", str(rate), str(wav)], check=True)
    out = []
    for w in words:
        shift = sum(sec for t, sec in cuts if t <= w["start"])
        out.append({**w, "start": round(w["start"] + shift, 3), "end": round(w["end"] + shift, 3)})
    json.dump(out, open(words_f, "w", encoding="utf-8"), indent=1)
    print(f"{pid}: {len(cuts)} pad(s), +{sum(s for _, s in cuts):.2f}s -> {wav.name}, {words_f.name}")


if __name__ == "__main__":
    main(sys.argv[1])
