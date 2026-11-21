"""Stamp rule (user 2026-11-20, HCS10 rough cut 1): a stamp only ADDS what the narration doesn't say (a place, a date; name
tags are their own overlay), never the spoken words. "≈ 8,600", "LESS THAN A TEASPOON", "2 DAYS LATER" and the "Like the
purest water" quote all repeated Liam. A stamp that repeats the narration may stay only if it lands BEFORE the words are
spoken (a pre-announce: "1 WEEK" before "For a week").

Run by `episode.py build` next to the SAFE ZONE check; the build fails on a finding.
    python channels/storybook-medical/scripts/stamp_lint.py      # self-test
"""
from __future__ import annotations

import re

STOP = {"a", "an", "the", "of", "than", "to", "in", "on", "at", "and", "or", "he", "his", "it", "is", "was", "for", "with",
        "like", "about"}
NUM = {"zero": "0", "one": "1", "a": "1", "an": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
       "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20",
       "hundred": "100", "thousand": "1000"}
YEAR = re.compile(r"\b1[0-9]{3}\b|\b20[0-9]{2}\b")


def _tok(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def content(text: str) -> list[str]:
    """The stamp's words that carry meaning (numbers kept, articles and fillers dropped)."""
    toks = [_tok(t) for t in text.split()]
    return [t for t in toks if t and (t.isdigit() or t not in STOP)]


def _spoken_forms(word: str) -> set[str]:
    t = _tok(word)
    return {t, NUM.get(t, t)}


def lint_stamps(overlays: list[dict], shots: list[dict], words: list[dict]) -> list[str]:
    out = []
    for o in overlays:
        if o.get("kind") != "stamp":
            continue
        if YEAR.search(o["text"]):                   # place / date stamp: allowed (the hook hides the spoken line)
            continue
        sh = next((s for s in shots if s["start"] <= o["start"] < s["end"]), None)
        if not sh:
            continue
        said = [(w["start"], _spoken_forms(w["word"])) for w in words if sh["start"] <= w["start"] < sh["end"]]
        need = content(o["text"])
        hits = {t: next((ts for ts, forms in said if t in forms), None) for t in need}
        if need and all(v is not None for v in hits.values()):
            first = min(hits.values())
            if o["start"] >= first - 0.05:
                txt = o["text"].encode("ascii", "replace").decode()
                out.append(f"STAMP repeats the narration: '{txt}' at {o['start']:.2f}s (Liam says it at "
                           f"{first:.2f}s in shot {sh['id']}); a stamp adds a place, date or name, or lands BEFORE the words")
    return out


if __name__ == "__main__":
    shots = [{"id": "s02", "start": 5.0, "end": 9.0}, {"id": "s09", "start": 31.3, "end": 34.8}]
    words = [{"word": "about", "start": 7.0}, {"word": "8,600", "start": 7.28}, {"word": "people", "start": 8.4},
             {"word": "For", "start": 31.6}, {"word": "a", "start": 31.84}, {"word": "week.", "start": 31.96}]
    ov = [{"kind": "stamp", "text": "≈ 8,600", "start": 7.28}, {"kind": "stamp", "text": "1 WEEK", "start": 31.45},
          {"kind": "stamp", "text": "1 WEEK", "start": 32.2}, {"kind": "stamp", "text": "HAMBURG · 1892", "start": 5.5},
          {"kind": "stamp", "text": "CAVENDISH", "start": 5.5}]
    got = lint_stamps(ov, shots, words)
    ok = (len(got) == 2 and "8,600" in got[0] and "32.20" in got[1])
    print("PASS" if ok else "FAIL", "stamp lint: repeats fail, a pre-announce and a place/date pass;", len(got), "findings")
    raise SystemExit(0 if ok else 1)
