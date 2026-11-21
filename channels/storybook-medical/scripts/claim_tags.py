"""Claim IDs on every public sentence of a publish package (user, 2026-11-21, after the Pettenkofer captions).

In a publish_<ep>.py every sentence of the public texts ends with its claim tag from the episode's claims.csv:
    "Cholera had just killed about 8,600 people in Hamburg. [C06]"
    "He got sick for a week, survived, and declared victory. [C19 C25]"
    "Who was braver: Pettenkofer or Marshall? [NF]"          NF = no factual claim (a question, a CTA, a disclaimer)
    "... drank his own germs: ... [HCS10:C45]"                another episode's log: <EPISODE_ID>:<claim>
Checked fields: youtube.title / description / pinned_comment, hook_card, <tiktok|instagram|facebook>.caption /
first_comment. Exempt lines: blank, hashtags only, the platform CTA lines (publish_social.CAPTION_CTA / COMMENT_CTA).

    check(pub, claims_csv)      SystemExit when a sentence has no tag, two sentences share one tag, or a tag is
                                unknown / UNKNOWN / REMOVE (VERIFIED, ATTRIBUTED, DISPUTED pass; DISPUTED wording and
                                "about" / "said" / "he wrote" are the fact gate's job: plan/fact-gate.md)
    strip(pub)                  the same dict with every tag removed: what goes into episode.json / publish.md
    gate_text(pub)              the tagged texts as markdown, for the independent fact gate
Self-test:  python claim_tags.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ID = r"(?:[A-Z0-9-]+:)?C\d+[a-z]?"
TAG = re.compile(rf"\[(NF|{ID}(?:[ ,]+{ID})*)\]")
STRIP = re.compile(rf"[ \t]*\[(?:NF|{ID}(?:[ ,]+{ID})*)\]")
# a sentence boundary inside one tagged segment: . ! ? … (optionally closing quote / bracket), space, a capital
BOUNDARY = re.compile(r"[.!?…][\"”')]?\s+(?=[\"“(]?[A-Z])")
FIELDS = [("youtube", "title"), ("youtube", "description"), ("youtube", "pinned_comment"), (None, "hook_card")] + \
         [(p, f) for p in ("tiktok", "instagram", "facebook") for f in ("caption", "first_comment")]
OK_STATUS = {"VERIFIED", "ATTRIBUTED", "DISPUTED"}
EPISODES = Path(__file__).resolve().parents[1] / "editorial/episodes"


def _exempt_lines() -> set[str]:
    import publish_social
    return set(publish_social.CAPTION_CTA.values()) | set(publish_social.COMMENT_CTA.values())


def load_claims(claims_csv: Path) -> dict[str, str]:
    return {r["claim_id"].strip(): r["review_status"].strip().upper()
            for r in csv.DictReader(open(claims_csv, encoding="utf-8"))}


def _other(episode: str, cache: dict) -> dict[str, str]:
    if episode not in cache:
        hits = [d / "claims.csv" for d in EPISODES.iterdir() if d.name.upper().startswith(episode + "-")
                and (d / "claims.csv").exists()]
        cache[episode] = load_claims(hits[0]) if hits else {}
    return cache[episode]


def lint_text(name: str, text: str, claims: dict[str, str], exempt: set[str] | None = None) -> list[str]:
    exempt = _exempt_lines() if exempt is None else exempt
    issues, cache = [], {}
    for line in text.split("\n"):
        s = line.strip()
        for cta in exempt:                        # a CTA line may share a line with a sentence (HC002-S1 TikTok)
            s = s.replace(cta, "").strip()
        if not s or all(w.startswith("#") for w in s.split()):
            continue
        parts = TAG.split(s)                      # text, tag, text, tag, ..., trailing text
        for i in range(0, len(parts) - 1, 2):
            seg, tag = parts[i].strip(), parts[i + 1]
            if not seg:
                issues.append(f"{name}: a tag [{tag}] with no sentence before it")
            elif BOUNDARY.search(seg.rstrip(".!?…\"”') ")):
                issues.append(f"{name}: two sentences share one tag [{tag}] (tag each one): \"{seg[:70]}\"")
            if tag == "NF":
                continue
            for cid in re.split(r"[ ,]+", tag):
                ep, _, c = cid.rpartition(":")
                st = (_other(ep, cache) if ep else claims).get(c)
                if st is None:
                    issues.append(f"{name}: [{cid}] is not in {'the ' + ep + ' claims' if ep else 'claims.csv'}")
                elif st not in OK_STATUS:
                    issues.append(f"{name}: [{cid}] is {st}: \"{seg[:70]}\"")
        tail = parts[-1].strip()
        if re.search(r"\w", tail):
            issues.append(f"{name}: sentence without a claim ID: \"{tail[:80]}\"")
    return issues


def _fields(pub: dict):
    for plat, f in FIELDS:
        holder = pub if plat is None else pub.get(plat, {})
        if isinstance(holder, dict) and holder.get(f):
            yield (f if plat is None else f"{plat}.{f}"), holder[f]


def lint(pub: dict, claims_csv: Path) -> list[str]:
    claims = load_claims(claims_csv)
    return [i for name, text in _fields(pub) for i in lint_text(name, text, claims)]


def check(pub: dict, claims_csv: Path) -> None:
    bad = lint(pub, claims_csv)
    if bad:
        raise SystemExit("CLAIM-ID LINT:\n  " + "\n  ".join(bad))


def strip(obj):
    if isinstance(obj, str):
        return STRIP.sub("", obj)
    if isinstance(obj, dict):
        return {k: strip(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip(v) for v in obj]
    return obj


def gate_text(pub: dict, title: str) -> str:
    """The tagged public texts for the fact gate (plan/fact-gate.md): one block per field."""
    out = [f"# {title}: public texts with claim tags", "",
           "[Cnn] = claim ID in claims.csv; [NF] = marked as no factual claim; [EP:Cnn] = another episode's claim.", ""]
    for name, text in _fields(pub):
        out += [f"## {name}", "```", text.strip(), "```", ""]
    return "\n".join(out)


def _selftest() -> None:
    claims = {"C01": "VERIFIED", "C02": "ATTRIBUTED", "C03": "UNKNOWN", "C04": "REMOVE", "C05": "DISPUTED"}
    ex = {"More true stories on YouTube: Oddly Matt"}
    t = lambda s: lint_text("x", s, claims, ex)   # noqa: E731
    assert t("He drank it. [C01] He wrote so. [C02]\n\nMore true stories on YouTube: Oddly Matt\n\n#a #b") == []
    assert t("Who was braver? [NF]") == []
    assert t("He drank it. [C01, C05]") == []
    assert len(t("He drank it.")) == 1                                  # no tag
    assert len(t("He drank it. He liked it. [C01]")) == 1              # two sentences, one tag
    assert "UNKNOWN" in t("It went wrong. [C03]")[0]
    assert "REMOVE" in t("A whole glass. [C04]")[0]
    assert "not in" in t("Fact. [C99]")[0]
    assert len(t("Fact. [C01] Then this.")) == 1                       # trailing untagged sentence
    assert t('He said: "Doctor, here is business." [C02]') == []      # a quote ending the sentence
    assert t('He said "no." [C02] More true stories on YouTube: Oddly Matt') == []   # CTA on the same line
    assert strip({"a": "He drank it. [C01] Then. [NF]\nNext [C01, C02]."}) == {"a": "He drank it. Then.\nNext."}
    print("claim-ID lint self-test PASS")


if __name__ == "__main__":
    _selftest()
