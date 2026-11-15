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


def finish(pid: str) -> Path:
    p = REPO / "projects" / pid
    pub = json.load(open(p / "episode.json", encoding="utf-8"))["publish"]
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
    md_f.write_text(md, encoding="utf-8")
    print(f"publish.md: publish times + per-platform blocks -> {md_f}")
    return md_f
