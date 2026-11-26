"""Packaging v2 for Shorts (plan/packaging-v2-spec.md, change C006, approved 2026-11-15).

Applied at BUILD time from the episode's "packaging" block, so edit_<ep>.py stays as it was (re-running it rewrites
"shots" but keeps "packaging"). Used by episode.py build + mix and by text_check.py, so all three see the same timeline.

    "packaging": {
      "version": 2, "case": 7,
      "hook": {"card": "She wore *gold* / in her eye socket", "anchor": "top"},   # v2.1 teaser card; `until` optional
      "open": {"source": "...s8.png", "until": 3.9, "motion": {...}, "fx": [...]},   # an existing action shot as frame 1
      "frame1": {"motion": {...}, "fx": [...]},              # motion from frame 0 on the (new) first shot
      "sfx": [{"name": "metal-clank", "at": 0.1, "gain_db": -8}], "sfx_move": {"gulls-water": 2.2},
      "keep_overlays": false                                   # overlays starting inside the hook window are dropped
    }

The three changes: 1. (v2.1, 2026-11-17) a short teaser card, 4-8 words on max 2 lines with one amber word, approved per
episode and written in publish.md `hook_card:`; the whole card is on screen from frame 0 (the amber word brightens over 0.4 s), it holds to the end of the spoken hook (max 2.5 s) and
collapses into the CASE chip, then the word-by-word captions start; something moves in frame 0 and frame 0 shows the
danger or the strange act already happening. (v2.0 put the whole narration sentence on a 5-line card: spoiled endings,
showed Snow's overstatement as fact.) 2. the CASE NN
chip for the whole Short (top-left of the safe area; text tops above CHIP_BOTTOM move down). 3. the end line on the final
held frame.
"""
from __future__ import annotations

import copy
import math
import re

END_LINE = "More strange cases: follow Oddly Matt"
SAFE_TOP, SAFE_BOTTOM, SAFE_LEFT, SAFE_RIGHT = 288, 1248, 65, 888
CHIP_BOTTOM = 356          # the chip covers y 288-~344, x 65-~270 (StorybookShort CaseChip); text tops move below it
CHIP_BOX = (SAFE_LEFT, SAFE_TOP, 275, 346)
END_LINE_H = 150
TAIL_ADD = 0.7             # extra held seconds so the end line is read (1.8 s after the last word -> 2.5 s)
TIME_KEYS = ("at", "from", "to", "beatAt")


def config(ep: dict) -> dict | None:
    pk = ep.get("packaging") or {}
    return pk if pk.get("version") == 2 and ep.get("format", "short") == "short" else None


# v2.1 hook card (2026-11-17): a short teaser, not the narration sentence. Written "She wore *gold* / in her eye socket":
# "/" breaks the line, *word* is the one amber word. The same string is publish.md `hook_card:` (text_check compares).
HOOK_MAX_S = 2.5           # the card collapses into the chip by then (or when the spoken hook ends, if sooner)
HOOK_MIN_S = 1.8           # ignore phrase breaks before this (too soon to read the card); none after it -> hold HOOK_MAX_S
HOOK_MAX_FS = 100          # px; StorybookShort fits each line to the width, never above this
HOOK_PAD = 48              # card padding top + bottom (StorybookShort HookCard)
HOOK_MAX_H = int(1920 * 0.15)
HOOK_MAX_WORDS, HOOK_MAX_LINES = 8, 2


def card_lines(card: str) -> list[str]:
    return [ln.strip() for ln in card.split("/") if ln.strip()]


def card_words(card: str) -> list[str]:
    return [w for ln in card_lines(card) for w in ln.split() if re.sub(r"[^\w]", "", w)]


def card_amber(card: str) -> list[str]:
    return [w.strip("*.,!?:;") for w in card_words(card) if w.startswith("*")]


def card_plain(card: str) -> str:
    """For comparing: no marks, no line breaks, one space, lower case."""
    return " ".join(card.replace("*", "").replace("/", " ").split()).lower()


def card_height(card: str) -> int:
    """Upper bound of the card box (the font never goes above HOOK_MAX_FS)."""
    return int(math.ceil(len(card_lines(card)) * HOOK_MAX_FS * 1.1 + HOOK_PAD))


def card_problems(card: str) -> list[str]:
    out = []
    n, ln, amb = len(card_words(card)), len(card_lines(card)), card_amber(card)
    if not 4 <= n <= HOOK_MAX_WORDS:
        out.append(f"{n} words (4-{HOOK_MAX_WORDS})")
    if ln > HOOK_MAX_LINES:
        out.append(f"{ln} lines (max {HOOK_MAX_LINES})")
    if len(amb) > 1:
        out.append(f"{len(amb)} amber words (max 1)")
    if card_height(card) > HOOK_MAX_H:
        out.append(f"box {card_height(card)} px > 15% ({HOOK_MAX_H})")
    return out


def hook_until(words: list[dict], cap: float = HOOK_MAX_S) -> float:
    """The spoken hook's end if it is said within `cap`; otherwise the last phrase break (a word starting after a
    gap of >= 0.1 s) at or before `cap`, so the captions take over on a clean word. No break in the first `cap` s
    (one unbroken phrase, e.g. Onesimus "In 1721, smallpox hit Boston"): hold the full `cap`; the captions resume on
    the first word that starts after it."""
    end = first_sentence_end(words)
    if end <= cap:
        return end
    starts = [(w["start"], w["start"] - (words[i - 1]["end"] if i else 0.0)) for i, w in enumerate(words) if w["start"] <= cap]
    breaks = [s for s, gap in starts[1:] if gap >= 0.1 and s >= HOOK_MIN_S]   # an earlier break is too soon to read the card
    return round((breaks or [cap])[-1], 2)


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
                if s.get("motion", {}).get("at") is not None:   # a timed move (snap) is shot-relative too
                    s["motion"] = {**s["motion"], "at": round(max(0.0, s["motion"]["at"] - d), 2)}
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

    # 1c. the hook card (v2.1: the approved teaser card, never the narration sentence)
    hk = pk.get("hook") or {}
    card = hk.get("card")
    if not card:
        raise SystemExit("packaging hook: no 'card' (v2.1: the approved hook_card text, plan/hook-cards-v2.1.md)")
    bad = card_problems(card)
    if bad:
        raise SystemExit(f"packaging hook card {card!r}: " + "; ".join(bad))
    until = min(hk.get("until") or hook_until(words), HOOK_MAX_S)
    h = card_height(card)
    anchor = hk.get("anchor", "top")
    y = hk.get("y", CHIP_BOTTOM + 4) if anchor == "top" else SAFE_BOTTOM - h
    text = card_plain(card).upper()
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
    ep["_v2"] = {"hook": {"until": until, "y": y, "anchor": anchor, "lines": card_lines(card), "maxSize": HOOK_MAX_FS},
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
    until, end_from = v2["hook"]["until"], v2["endLine"]["from"]
    out = []
    for w in words:
        if w["start"] >= end_from:
            continue
        if w["start"] >= until - 0.05:
            out.append(w)
        elif w["end"] > until + 0.15:      # still being spoken after the card leaves (Onesimus "Boston."): show it from then
            out.append({**w, "start": until})
    return out
