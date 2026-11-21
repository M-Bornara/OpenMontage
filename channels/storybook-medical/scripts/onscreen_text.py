"""On-screen text as tagged sentences (user, 2026-11-21): the fact gate must see what the VIDEO shows, not only the
upload texts. Exports every hook card, stamp, name tag and narration sentence (= the burned-in caption phrases) of a
built Short (remotion/props.json + artifacts/word_timestamps.json) and checks each against claims.csv.

Tags live in editorial/episodes/<EP>/fact-gate/onscreen-tags.json, keyed by the exact on-screen text:
    {"hook: He drank *cholera*. / On purpose.": "C01 C12 C18",
     "stamp: MUNICH · 1892": "C01",
     "name: Max von Pettenkofer · Munich, 73": "C01 C02",
     "say: Cholera had just killed about 8,600 people in Hamburg.": "C06"}
"NF" = no factual claim. A text that has no entry yet gets one with "" (so the lint fails until it is tagged).
The end line ("More strange cases: follow Oddly Matt") and the CASE chip are exempt.

    python onscreen_text.py <pid> [<pid> ...]     write fact-gate/onscreen.md (gate input) + lint; exit 1 on issues
    check(pid)                                    called by `episode.py build` after props.json: fails on issues when
                                                  the tags file exists, warns when it doesn't (episodes before 2026-11-21)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import claim_tags  # noqa: E402

CH = HERE.parent
REPO = CH.parents[1]
EXEMPT = {"More strange cases: follow Oddly Matt"}
SENT = re.compile(claim_tags.NOT_ABBR + r"(?<=[.!?…])[\"”']?\s+(?=[\"“(]?[A-Z0-9])")   # "Dr." / "U.S." don't end one


def episode_dir(pid: str) -> Path:
    for f in (CH / "editorial/episodes").glob("*/edit_*.py"):
        if re.search(rf'^PID\s*=\s*"{re.escape(pid)}"', f.read_text(encoding="utf-8"), re.M):
            return f.parent
    raise SystemExit(f"no editorial/episodes/*/edit_*.py with PID = \"{pid}\"")


def items(pid: str) -> list[tuple[str, str]]:
    """(section, key) for everything a viewer reads on screen, in order of appearance."""
    p = REPO / "projects" / pid
    props = json.load(open(p / "remotion/props.json", encoding="utf-8"))
    out = []
    if props.get("hook"):
        out.append(("hook card", "hook: " + " / ".join(props["hook"]["lines"])))
    for o in sorted(props.get("overlays", []), key=lambda o: o.get("start", 0)):
        if o.get("kind") == "stamp" and o.get("text"):
            out.append(("stamps + name tags", "stamp: " + o["text"]))
        elif o.get("kind") == "nameTag":
            out.append(("stamps + name tags", "name: " + " · ".join(x for x in (o.get("text"), o.get("sub")) if x)))
    words = json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8"))
    text = " ".join(w.get("word", w.get("text", "")).strip() for w in (words.get("words", words) if isinstance(words, dict) else words))
    for s in SENT.split(re.sub(r"\s+", " ", text).strip()):
        if s.strip():
            out.append(("narration (burned-in captions)", "say: " + s.strip()))
    return [(sec, k) for sec, k in dict.fromkeys(out) if k.split(": ", 1)[1] not in EXEMPT]


def run(pid: str, strict: bool = True) -> list[str]:
    epd = episode_dir(pid)
    tf = epd / "fact-gate/onscreen-tags.json"
    if not tf.exists() and not strict:
        print(f"ON-SCREEN CLAIMS: no {tf.relative_to(REPO)} yet (python onscreen_text.py {pid}) - not checked")
        return []
    tags = json.load(open(tf, encoding="utf-8")) if tf.exists() else {}
    its = items(pid)
    tags = {k: tags.get(k, "") for _, k in its}      # a changed text loses its tag: it must be tagged (and gated) again
    tf.parent.mkdir(exist_ok=True)
    json.dump(tags, open(tf, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    claims = claim_tags.load_claims(epd / "claims.csv")
    md = [f"# {epd.name}: on-screen text with claim tags", "",
          "What the video shows: the hook card, stamps, name tags (name · subtitle), and the narration sentence by "
          "sentence (it is burned in as captions). [Cnn] = claim ID in claims.csv; [NF] = no factual claim.", ""]
    issues, sec_now = [], None
    for sec, k in its:
        if sec != sec_now:
            md += ["", f"## {sec}", ""]
            sec_now = sec
        shown = k.split(": ", 1)[1]
        t = tags.get(k, "").strip()
        line = f"{shown} [{t}]" if t else shown
        md.append(f"- {line}")
        issues += [i.replace("x:", f"{k[:60]}:", 1) for i in claim_tags.lint_text("x", line, claims, set())]
    (epd / "fact-gate/onscreen.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return issues


def check(pid: str) -> None:
    bad = run(pid, strict=False)
    if bad:
        raise SystemExit("ON-SCREEN CLAIM-ID LINT (fact-gate/onscreen-tags.json):\n  " + "\n  ".join(bad))


if __name__ == "__main__":
    fail = False
    for pid in sys.argv[1:]:
        found = run(pid)
        print(f"{pid}: " + ("OK" if not found else f"{len(found)} issue(s)\n  " + "\n  ".join(found)))
        fail |= bool(found)
    sys.exit(1 if fail else 0)
