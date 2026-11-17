"""Packaging v2 for Shorts (plan/packaging-v2-spec.md, change C006, approved 2026-11-15).

Applied at BUILD time from the episode's "packaging" block, so edit_<ep>.py stays as it was (re-running it rewrites
"shots" but keeps "packaging"). Used by episode.py build + mix and by text_check.py, so all three see the same timeline.

    "packaging": {
      "version": 2, "case": 7,
      "hook": {"until": 4.9, "y": 360, "anchor": "top"},     # card from frame 0 to `until` s (default: the first sentence)
      "open": {"source": "...s8.png", "until": 3.9, "motion": {...}, "fx": [...]},   # an existing action shot as frame 1
      "frame1": {"motion": {...}, "fx": [...]},              # motion from frame 0 on the (new) first shot
      "sfx": [{"name": "metal-clank", "at": 0.1, "gain_db": -8}], "sfx_move": {"gulls-water": 2.2},
      "keep_overlays": false                                   # overlays starting inside the hook window are dropped
    }

The three changes: 1. the whole spoken hook as ONE card from frame 0 (each word lights as it is spoken), the word-by-word
captions start after it; something moves in frame 0 and frame 0 shows the strange act already happening. 2. the CASE NN
chip for the whole Short (top-left of the safe area; text tops above CHIP_BOTTOM move down). 3. the end line on the final
held frame.
"""
from __future__ import annotations

import copy
import math

END_LINE = "More strange cases: follow Oddly Matt"
SAFE_TOP, SAFE_BOTTOM, SAFE_LEFT, SAFE_RIGHT = 288, 1248, 65, 888
CHIP_BOTTOM = 356          # the chip covers y 288-~344, x 65-~270 (StorybookShort CaseChip); text tops move below it
CHIP_BOX = (SAFE_LEFT, SAFE_TOP, 275, 346)
END_LINE_H = 150
TAIL_ADD = 0.7             # extra held seconds so the end line is read (1.8 s after the last word -> 2.5 s)
TIME_KEYS = ("at", "from", "to", "beatAt")
FONT_SCALE = {"montserrat": 1.0, "lalezar": 1.08, "im-fell": 1.12}


def config(ep: dict) -> dict | None:
    pk = ep.get("packaging") or {}
    return pk if pk.get("version") == 2 and ep.get("format", "short") == "short" else None


def hook_font_size(chars: int) -> int:     # = StorybookShort hookFontSize
    return 84 if chars <= 40 else 74 if chars <= 64 else 64 if chars <= 90 else 56


def hook_words(words: list[dict], until: float) -> list[dict]:
    return [w for w in words if w["start"] < until - 0.05]


def hook_height(text: str, font: str = "montserrat", size: int | None = None) -> int:
    """Estimated card height (px of 1920): Montserrat Black capitals average ~0.68 em with the word gap
    (checked on the HCS09 render: estimate 456, real ~445)."""
    fs = (size or hook_font_size(len(text))) * FONT_SCALE.get(font, 1.0)
    inner = SAFE_RIGHT - SAFE_LEFT - 14 - 58
    lines, cur = 1, 0.0
    for w in text.upper().split():
        ww = len(w) * fs * 0.68
        if cur and cur + fs * 0.28 + ww > inner:
            lines, cur = lines + 1, ww
        else:
            cur += (fs * 0.28 if cur else 0) + ww
    return int(math.ceil(lines * fs * 1.1 + 48))


def first_sentence_end(words: list[dict]) -> float:
    for w in words:
        if w["word"].rstrip('"\'').endswith((".", "?", "!")) and w["word"].lower() not in ("dr.", "st.", "mr."):
            return round(w["end"] + 0.15, 2)
    return round(words[0]["end"] + 2.5, 2)


def _shift_fx(fx: list[dict], d: float) -> list[dict]:
    out = []
    for e in fx:
        e = dict(e)
        for k in TIME_KEYS:
            if isinstance(e.get(k), (int, float)):
                e[k] = round(e[k] - d, 3)
        out.append(e)
    return out


def apply(ep: dict, words: list[dict]) -> dict:
    """A copy of the episode with v2 applied, plus ep["_v2"] = the StorybookShort props (hook, caseNo, endLine)."""
    pk = config(ep)
    if not pk:
        return ep
    ep = copy.deepcopy(ep)
    shots = sorted(ep["shots"], key=lambda s: s["start"])

    # 1a. cold open: an existing action shot as frame 0 (no new generation); shots it covers are trimmed or dropped
    op = pk.get("open")
    if op:
        until = op["until"]
        new = {"id": "s00", "source": op["source"], "start": 0.0, "end": until, "motion": op.get("motion", {"type": "static"}),
               "captionY": op.get("captionY", 1030), **{k: op[k] for k in ("fx", "focus", "hit", "breath", "darken") if k in op}}
        keep = []
        for s in shots:
            if s["end"] <= until + 0.3:
                continue                                   # fully covered (or a sliver would remain): dropped
            if s["start"] < until:
                if s.get("layers"):
                    raise SystemExit(f"packaging open: {s['id']} has layers; trim it in edit_<ep>.py instead")
                d = until - s["start"]
                if s.get("fx"):
                    s["fx"] = _shift_fx(s["fx"], d)
                s["start"] = until
            keep.append(s)
        shots = [new] + keep

    # 1b. frame-0 motion on the first shot (replaces a slow push/pull start)
    f1 = pk.get("frame1") or {}
    if f1:
        s0 = shots[0]
        if "motion" in f1:
            s0["motion"] = f1["motion"]
        s0["fx"] = list(s0.get("fx", [])) + list(f1.get("fx", []))
        for k in ("hit", "captionY"):
            if k in f1:
                s0[k] = f1[k]

    # 1c. the hook card
    hk = pk.get("hook") or {}
    until = hk.get("until") or first_sentence_end(words)
    hw = hook_words(words, until)
    text = hk.get("text") or " ".join(w["word"] for w in hw)
    font = (ep.get("theme") or {}).get("font", "montserrat")
    h = hook_height(text, font, hk.get("size"))
    anchor = hk.get("anchor", "top")
    y = hk.get("y", CHIP_BOTTOM + 4) if anchor == "top" else SAFE_BOTTOM - h
    if not pk.get("keep_overlays"):
        ep["overlays"] = [o for o in ep["overlays"] if o["start"] >= until - 0.05 or o["kind"] == "clock"]

    # 2. the chip: captions, stamps, cards and tags move below it
    for s in shots:
        if s.get("captionY", 1030) < CHIP_BOTTOM:
            s["captionY"] = CHIP_BOTTOM
    for o in ep["overlays"]:
        if o["kind"] in ("stamp", "location", "nameTag") and o.get("y", 300 if o["kind"] == "stamp" else 250) < CHIP_BOTTOM:
            o["y"] = CHIP_BOTTOM

    # sound for frame 0 (and sounds that belonged to a replaced opening shot)
    moves = pk.get("sfx_move", {})
    for c in ep.get("sfx", []):
        if c["name"] in moves:
            c["at"] = moves[c["name"]]
    ep["sfx"] = sorted(ep.get("sfx", []) + list(pk.get("sfx", [])), key=lambda c: c["at"])

    # 3. the end line: after the last word, over a slightly longer held frame
    ep["tail_seconds"] = round(ep.get("tail_seconds", 0) + pk.get("tail_add", TAIL_ADD), 2)
    end_from = round(words[-1]["end"] + 0.25, 2)
    # the last shot's caption band was chosen to keep words off its subject: the end line takes that band
    end_y = pk.get("end_y", shots[-1].get("captionY", 1030))

    ep["shots"] = shots
    # the card is read as one sentence: it keeps the narration's punctuation ("5,000 years ago,"); captions strip it
    ep["_v2"] = {"hook": {"until": until, "y": y, "anchor": anchor, "display": [w["word"] for w in hw],
                          **{k: hk[k] for k in ("text", "size") if hk.get(k)}},
                 "caseNo": pk["case"], "endLine": {"text": END_LINE, "from": end_from, "y": end_y}}
    ep["_v2_boxes"] = [   # for text_check: (kind, label, t0, t1, y0, y1, x0, x1)
        ("hook", text, 0.0, until, y, y + h, SAFE_LEFT, SAFE_RIGHT),
        ("chip", f"CASE {pk['case']:02d}", 0.0, 1e9, CHIP_BOX[1], CHIP_BOX[3], CHIP_BOX[0], CHIP_BOX[2]),
        ("endLine", END_LINE, end_from, 1e9, end_y, end_y + END_LINE_H, SAFE_LEFT, SAFE_RIGHT),
    ]
    return ep


def caption_words(ep: dict, words: list[dict]) -> list[dict]:
    """The words the word-by-word captions show (the hook is on the card; the end line follows the last word)."""
    v2 = ep.get("_v2")
    if not v2:
        return words
    return [w for w in words if w["start"] >= v2["hook"]["until"] - 0.05 and w["start"] < v2["endLine"]["from"]]
