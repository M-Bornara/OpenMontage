"""HC002-L Gage long: projects/hc002-l/episode.json from the approved, fact-gated script (script-long-v1.md; user
2026-11-21: changed lines approved, record the narration). The narration chapters are read straight from the script
table, so what Liam reads is exactly what the gate passed (fact-gate/2026-11-21-long-script.md):
  - one chapter per "## N · ..." section, one script row per line, the row's `[tag]`s kept as ElevenLabs v3 tags;
  - struck-through rows (~~...~~, e.g. row 51) are skipped;
  - gap_after: 3.3 s after the cold open (sting 1.8 s + title), 1.2 s between chapters (as HC001-L).
Then:  python channels/storybook-medical/scripts/episode.py narrate hc002-l
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/build_hc002l.py [--print]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
PID = "hc002-l"
P = REPO / "projects" / PID


def chapters() -> list[dict]:
    out, cur = [], None
    for line in (HERE / "script-long-v1.md").read_text(encoding="utf-8").splitlines():
        h = re.match(r"## (\d+) · (.+?) \(", line)
        if h:
            cur = {"id": f"ch{h.group(1)}", "title": h.group(2).strip(), "rows": []}
            out.append(cur)
            continue
        if line.startswith("## "):
            cur = None
            continue
        m = re.match(r"\| (\d+) \| (.*?) \| .* \| [^|]* \|\s*$", line)
        if cur is None or not m or "~~" in m.group(2):
            continue
        text = re.sub(r"`(\[[^\]]+\])`", r"\1", m.group(2)).strip()
        cur["rows"].append((int(m.group(1)), text))
    return out


def main():
    chs = chapters()
    assert [c["id"] for c in chs] == [f"ch{i}" for i in range(9)], [c["id"] for c in chs]
    rows = [n for c in chs for n, _ in c["rows"]]
    assert rows == [n for n in range(1, 68) if n != 51], "script rows missing or out of order"
    narr = [{"id": c["id"], "title": c["title"], "v3_text": "\n".join(t for _, t in c["rows"]),
             "gap_after": 3.3 if c["id"] == "ch0" else 1.2} for c in chs]
    if "--print" in sys.argv:
        for c in narr:
            print(f"== {c['id']} {c['title']} ({len(c['v3_text'])} chars)\n{c['v3_text']}\n")
        print(sum(len(c["v3_text"]) for c in narr), "characters")
        return
    for d in ("assets/audio", "artifacts"):
        (P / d).mkdir(parents=True, exist_ok=True)
    f = P / "episode.json"
    ep = json.load(open(f, encoding="utf-8")) if f.exists() else {}
    ep.update({"title": "Phineas Gage: The Story Everyone Gets Wrong (HC002-L)", "playbook": "storybook-medical",
               "format": "long", "theme": {"culture": "new-england-1840s", "font": "montserrat"}})
    ep.setdefault("narration", {})
    ep["narration"]["chapters"] = narr
    ep["narration"].setdefault("punch_words", [])
    json.dump(ep, open(f, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"{f}: {len(narr)} chapters, {sum(len(c['v3_text']) for c in narr)} characters")


if __name__ == "__main__":
    main()
