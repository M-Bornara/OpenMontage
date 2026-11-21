"""HC003-S1 Dancing Plague: writes projects/hc003-s1/episode.json (title, narration, theme) from the approved script v3
(s1-story-v3.md, user 2026-11-21: ending A, hook card A, title 1, theme rhine-1518 pending the listen; fact gate
21 PASS: fact-gate/2026-11-21-script-s1-v3.md). The narration is read from the script block of s1-story-v3.md, so
what Liam reads is exactly what the gate passed.
Order (as Gage / Pettenkofer): narration -> refs (the user downloads them) -> cast sheets -> the 3 HERO shots' pieces
on real art (user 2026-11-21: "generate the HERO pieces first and show me them on real art") -> story stills.
    python channels/storybook-medical/editorial/episodes/HC003-dancing-plague/build_hc003s1.py
    python channels/storybook-medical/scripts/episode.py narrate hc003-s1
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PID = "hc003-s1"
P = REPO / "projects" / PID


def narration() -> str:
    md = (HERE / "s1-story-v3.md").read_text(encoding="utf-8")
    block = re.search(r"```\n(\[intense\] Strasbourg.*?)\n```", md, re.S).group(1)
    assert "four hundred people had joined the dancing" in block and "others started dancing too" in block
    return block.strip()


def main():
    for d in ("assets/audio", "artifacts", "refs"):
        (P / d).mkdir(parents=True, exist_ok=True)
    f = P / "episode.json"
    ep = json.load(open(f, encoding="utf-8")) if f.exists() else {}
    ep.update(title="The Woman Who Couldn't Stop Dancing", playbook="storybook-medical", format="short",
              dual_format=False, theme={"culture": "rhine-1518", "font": "montserrat"}, motion_lint="fail")
    ep.setdefault("narration", {"punch_words": []})
    ep["narration"]["v3_text"] = narration()
    json.dump(ep, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"{f}: narration {len(ep['narration']['v3_text'])} characters")


if __name__ == "__main__":
    main()
