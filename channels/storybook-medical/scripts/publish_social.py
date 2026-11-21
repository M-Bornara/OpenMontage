"""After `episode.py publish`: the publish.md layout of the C001 packages (HCS08/HCS09), generated instead of hand-edited.

Adds the "Publish times" table and turns each platform's plain caption block into Publish / Caption / First comment /
Playlist (change C001, plan/change-log.csv). Reads everything from episode.json "publish":
    publish.youtube.schedule                      "Thu Dec 3, 15:00 ET = 14:00 Alberta"
    publish.<tiktok|instagram|facebook>.caption / first_comment / playlist / when
Usage (from a publish_<ep>.py, after episode.py publish):  publish_social.finish(pid)
"""
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WHERE = {"tiktok": ("TikTok", "TikTok Studio (web)"), "instagram": ("Instagram Reel", "Meta Business Suite → Planner"),
         "facebook": ("Facebook Reel", "Meta Business Suite → Planner")}

# captions skill v2 (.claude/skills/oddly-matt-platform-captions): each platform's call-to-action line, in the caption
# and (the earlier packages' wording) under the challenge in the first comment
CAPTION_CTA = {"tiktok": "More true stories on YouTube: Oddly Matt",
               "instagram": "More true stories on YouTube (link in bio)",
               "facebook": "More true stories on YouTube: oddlymatt.com"}
COMMENT_CTA = {"tiktok": "More true stories: search Oddly Matt on YouTube",
               "instagram": "More true stories: link in bio",
               "facebook": "More true stories on YouTube: https://www.youtube.com/@oddlymatt"}


# C011 (user, 2026-11-21): weekend (Sat/Sun) TikTok posts at 12:00 ET = 10:00 Alberta; weekdays and Instagram/Facebook
# stay 18:00 ET = 17:00 Alberta; YouTube unchanged. Applied to every package (and every rebuild) in finish().
WEEKEND_TIKTOK = "12:00 ET = 10:00 Alberta"
TIKTOK_CHECKLIST_OLD = ("- When to post: the day after the YouTube Short, **18:00 ET** (TikTok shows your local time: "
                        "winter 17:00 Alberta).")
TIKTOK_CHECKLIST_NEW = ("- When to post: the day after the YouTube Short. Weekdays **18:00 ET** (17:00 Alberta); "
                        "weekends **12:00 ET** (10:00 Alberta), change C011. TikTok shows your local time.")


def c011_when(platform: str, when: str) -> str:
    """Weekend TikTok slot (C011): 'Sun Nov 22, 18:00 ET = 17:00 Alberta' -> 'Sun Nov 22, 12:00 ET = 10:00 Alberta
    (weekend TikTok test, C011)'. Other platforms and weekdays are returned unchanged."""
    if platform != "tiktok" or not when.strip()[:3] in ("Sat", "Sun"):
        return when
    day = when.split(",")[0].strip()
    return f"{day}, {WEEKEND_TIKTOK} (weekend TikTok test, C011)"


def c011_publish_json(f: Path) -> None:
    """C011 in publish.json: a weekend tiktok.publish_at {date, et, alberta} moves to 12:00 ET / 10:00 Alberta."""
    import datetime as _dt
    if not f.exists():
        return
    j = json.load(open(f, encoding="utf-8"))
    pa = (j.get("tiktok") or {}).get("publish_at")
    if isinstance(pa, dict) and pa.get("date"):
        if _dt.date.fromisoformat(pa["date"]).weekday() >= 5 and pa.get("et") != "12:00":
            pa["et"], pa["alberta"] = "12:00", "10:00"
            f.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")


def lint_captions(pub: dict) -> list[str]:
    """Caption lint (user, 2026-11-21, HCS10): every TikTok / Instagram / Facebook caption carries its platform's CTA
    line, every first comment carries its own, and the first comment is not pasted into the caption."""
    issues = []
    for k in WHERE:
        s = pub.get(k)
        if not s:
            issues.append(f"{k}: no caption block")
            continue
        cap, fc = s.get("caption", ""), s.get("first_comment", "")
        if CAPTION_CTA[k] not in cap:
            issues.append(f"{k} caption: missing the CTA line '{CAPTION_CTA[k]}'")
        if not fc.strip():
            issues.append(f"{k}: no first_comment")
        elif COMMENT_CTA[k] not in fc:
            issues.append(f"{k} first comment: missing the CTA line '{COMMENT_CTA[k]}'")
        if "first comment" in cap.lower():
            issues.append(f"{k} caption: the first comment is pasted into the caption (use the first_comment field)")
    return issues


def check(pub: dict) -> None:
    bad = lint_captions(pub)
    if bad:
        raise SystemExit("CAPTION LINT:\n  " + "\n  ".join(bad))


def finish(pid: str) -> Path:
    p = REPO / "projects" / pid
    pub = json.load(open(p / "episode.json", encoding="utf-8"))["publish"]
    check(pub)
    if "tiktok" in pub:
        pub["tiktok"]["when"] = c011_when("tiktok", pub["tiktok"]["when"])
    md_f = p / "renders/deliverables/publish.md"
    md = md_f.read_text(encoding="utf-8")
    yt_when = pub["youtube"]["schedule"]
    rows = ["## Publish times", "", "| Platform | When | Scheduled in |", "|---|---|---|",
            f"| YouTube Shorts | **{yt_when}** | YouTube Studio |"]
    rows += [f"| {WHERE[k][0]} | **{pub[k]['when']}** | {WHERE[k][1]} |" for k in WHERE if k in pub]
    rows += ["", "First comments can't be scheduled: post + pin them when each post goes live.", ""]
    head, rest = md.split("## YouTube Shorts", 1)
    md = head.rstrip("\n") + "\n\n" + "\n".join(rows) + "\n## YouTube Shorts" + rest
    for k in WHERE:
        if k not in pub:
            continue
        s = pub[k]
        plain = f"## {k.title()}\n```\n{s['caption'].strip()}\n```\n"
        rich = (f"## {k.title()}\n**Publish:** {s['when']}\n\n**Caption:**\n```\n{s['caption'].strip()}\n```\n"
                f"**First comment** (post it right after the post goes live, then pin it):\n```\n{s['first_comment'].strip()}\n```\n"
                f"**Playlist:** {s.get('playlist', 'none')}\n")
        if plain not in md:
            raise SystemExit(f"publish.md: the plain {k} block was not found (was episode.py publish run first?)")
        md = md.replace(plain, rich, 1)
    md = md.replace("\n## Upload checklist", "\n_Per-platform captions are change C001 in "
                    "`channels/storybook-medical/plan/change-log.csv`._\n\n## Upload checklist", 1)
    md = md.replace(TIKTOK_CHECKLIST_OLD, TIKTOK_CHECKLIST_NEW)
    md_f.write_text(md, encoding="utf-8")
    c011_publish_json(p / "renders/deliverables/publish.json")
    print(f"publish.md: publish times + per-platform blocks -> {md_f}")
    return md_f


def _selftest() -> None:
    good = {k: {"caption": f"Hook.\n\n{CAPTION_CTA[k]}\n\n#history", "first_comment": f"Q?\n\n{COMMENT_CTA[k]}"}
            for k in WHERE}
    assert lint_captions(good) == [], lint_captions(good)
    bad = {**good, "tiktok": {"caption": "Hook.\n#history\n\nFirst comment: Q?", "first_comment": "Q?"}}
    got = lint_captions(bad)
    assert len(got) == 3 and all(g.startswith("tiktok") for g in got), got
    assert lint_captions({k: v for k, v in good.items() if k != "facebook"}) == ["facebook: no caption block"]
    print("caption lint self-test PASS")
    assert c011_when("tiktok", "Sun Nov 22, 18:00 ET = 17:00 Alberta") == \
        "Sun Nov 22, 12:00 ET = 10:00 Alberta (weekend TikTok test, C011)"
    assert c011_when("tiktok", "Sat Nov 28, 18:00 ET = 17:00 Alberta").startswith("Sat Nov 28, 12:00 ET")
    assert c011_when("tiktok", "Tue Nov 24, 18:00 ET = 17:00 Alberta") == "Tue Nov 24, 18:00 ET = 17:00 Alberta"
    assert c011_when("instagram", "Sun Nov 22, 18:00 ET = 17:00 Alberta") == "Sun Nov 22, 18:00 ET = 17:00 Alberta"
    print("C011 weekend TikTok self-test PASS")


if __name__ == "__main__":
    # python publish_social.py [<pid> ...]: lint those episodes' captions (no pid: the self-test)
    import sys
    if len(sys.argv) == 1:
        _selftest()
    for pid in sys.argv[1:]:
        found = lint_captions(json.load(open(REPO / "projects" / pid / "episode.json", encoding="utf-8"))["publish"])
        print(f"{pid}: " + ("OK" if not found else "\n  " + "\n  ".join(found)))
