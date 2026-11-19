"""Storyboard lint L50 · story-craft Rule 0b (user, 2026-11-19): show the main action, soften the harshness.

Every storyboard row that shows a violent beat (a hit, a fall, a cut into skin, drinking a germ, a wound, frostbite,
insects in a wound, ...) must NAME its softening tool in the row, as `0b: <tool> + <tool>`, e.g.
`0b: silhouette + white flash + head snap`. A violent row without a `0b:` tag, or with a tag that names none of the
Rule 0b tools, fails. A false positive (the word matched but nothing violent is shown) is written `0b: n/a (why)`.

Which tables: shot tables (first header cell `#`) and any table with a `0b` column. Beat tables of story files
(`| Beat | Line | ...`) are scripts, not storyboards, and are not linted. Sound / text / music columns are skipped
("a hit on the turn" is a sound, not a blow).

    python channels/storybook-medical/scripts/storyboard_lint.py <storyboard.md> [...]     # exit 1 on any L50
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# what makes a row a violent beat (lower-case text of the row's picture / narration columns)
VIOLENT = [
    r"\bthrough (?:his|her|a man's|a woman's|the) (?:skull|head|cheek|brain|eye|chest|body)\b",
    r"\b(?:went|goes|bursts?|shoots?) (?:in|into|out|up)\b[^|]{0,40}\b(?:cheek(?:bone)?|skull|head|eye|chest)\b",
    r"\b(?:wounds?|wounded|blood|bloody|bleed\w*|gore|injur\w*|fractur\w*|broken (?:bone|collarbone|leg|arm|neck))\b",
    r"\b(?:cuts?|cutting|slic\w+|stab\w*)\s+(?:into\s+)?(?:his|her|their)\s+(?:own\s+)?(?:arm|skin|wrist|hand|leg|veins?)\b",
    r"\b(?:incisions?|scalpel|lancet)\b",
    r"\b(?:vomit\w*|maggots?|larvae|insect eggs|pus)\b",
    r"\b(?:drinks?|drank|drinking|swallow(?:s|ed|ing)?|gulps?)\b[^|]{0,40}\b(?:cholera|vomit|germs?|cultures?|poison|it)\b",
    r"\b(?:cramps?|convuls\w+|seizures?|agony|in pain|screams?)\b",
    r"\b(?:frostbit\w*|frozen (?:solid|stiff)|hypotherm\w*)\b",
    # a PERSON falls / is thrown (an iron bar or a leaf falling is not a violent beat)
    r"\b(?:he|she|they|him|her|girl|boy|man|woman|-old|passengers?|seat row|plane)\b[^|.]{0,30}"
    r"\b(?:falls?|fell|falling|plunges?|crash(?:es|ed|ing)?|thrown|hurled|collapses?|collapsed)\b",
    r"\b(?:corpses?|dead bod(?:y|ies)|amputat\w*|catheter|needles?|inject\w*)\b",
]
# the Rule 0b tools (story-craft.md): a tag must name at least one
TOOLS = [
    "silhouette", "flash", "smear", "speed line", "shake", "transient", "white light", "amber", "teal", "no-blood",
    "no blood", "colour drain", "color drain", "drain", "grey", "gray", "blur", "soft focus", "out of focus", "framing",
    "edge", "reaction", "off frame", "off-frame", "document", "engraving", "diagram", "period page", "page", "object",
    "bowl", "cup", "narration", "frost", "n/a",
]
SKIP_COLS = ("sfx", "sound", "text", "music", "hero sound", "cut length", "claims", "fact", "tension", "≈s", "cost")
TAG = re.compile(r"0b:\s*([^|]+)", re.I)


def tables(md: str):
    """Yield (header cells, [row cells]) for every markdown table."""
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                j += 1
            yield head, rows
            i = j
        else:
            i += 1


def lint_rows(head: list[str], rows: list[list[str]], where: str = "") -> list[str]:
    out = []
    keep = [k for k, h in enumerate(head) if not h.lower().startswith(SKIP_COLS)]
    for r in rows:
        text = " | ".join(r[k] for k in keep if k < len(r)).lower().replace("*", "")
        hit = next((m.group(0) for p in VIOLENT for m in [re.search(p, text)] if m), None)
        if not hit:
            continue
        tag = TAG.search(" | ".join(r))
        name = r[0] if r else "?"
        if not tag:
            out.append(f"L50: {where}row {name}: violent beat ('{hit}') without a named softening tool (story-craft "
                       f"Rule 0b): add '0b: silhouette + white flash + ...' (or '0b: n/a (why)' if nothing violent is shown)")
        elif not any(t in tag.group(1).lower() for t in TOOLS):
            out.append(f"L50: {where}row {name}: '0b: {tag.group(1).strip()[:60]}' names no Rule 0b tool (silhouette, "
                       f"effects (flash / smear / shake), no-blood colour, blur, framing, document)")
    return out


def lint_md(md: str, where: str = "") -> list[str]:
    out = []
    for head, rows in tables(md):
        if head and (head[0] == "#" or any(h.lower().startswith("0b") for h in head)):
            out += lint_rows(head, rows, where)
    return out


def lint_file(path: Path) -> list[str]:
    return lint_md(Path(path).read_text(encoding="utf-8"), f"{Path(path).name} ")


if __name__ == "__main__":
    bad = 0
    for f in sys.argv[1:]:
        issues = lint_file(Path(f))
        bad += len(issues)
        print(f"{Path(f).name}: {'OK' if not issues else f'{len(issues)} issue(s)'}")
        for m in issues:
            print("  " + m)
    sys.exit(1 if bad else 0)
