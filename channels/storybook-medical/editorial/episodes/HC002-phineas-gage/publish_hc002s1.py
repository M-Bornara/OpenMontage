"""HC002-S1 Gage: the upload texts (episode.json "publish"), DRAFT for the user's review with rough cut 1 (2026-11-18).
`--texts-only` writes episode.json only; without it, `episode.py publish` builds projects/hc002-s1/renders/deliverables/
and publish_social.finish() adds the publish times + the per-platform blocks (change C001). Run that only after the cut
is approved.

Slot (plan/slate-nov29-dec11.md): YouTube Sun Nov 29, 15:00 ET = 14:00 Alberta; socials Mon Nov 30, 18:00 ET = 17:00
Alberta. Family History Got It Wrong. Related video HC001-L until Dec 13, then HC002-L (the Gage long).
TEASER RULE: nothing after 1849 (no Chile, no later life, no death) in any text: the long and S2 answer "no longer Gage".
Facts: claims.csv C01-C08 (C06 the greeting is ATTRIBUTED to Dr Williams' statement: "the doctor remembered").
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/publish_hc002s1.py --texts-only
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
sys.path.insert(0, str(SCRIPTS))
import publish_social  # noqa: E402

PID = "hc002-s1"
TITLE = "He Took an Iron Bar Through the Skull… and Spoke"    # title 1, approved 2026-11-18
YT_WHEN = "Sun Nov 29, 15:00 ET = 14:00 Alberta"
SOCIAL_WHEN = "Mon Nov 30, 18:00 ET = 17:00 Alberta"

SOURCES = """SOURCES
- J. M. Harlow, "Recovery from the passage of an iron bar through the head", Publications of the Massachusetts Medical Society, 1868. https://archive.org/details/66210360R.nlm.nih.gov
- H. J. Bigelow, "Dr. Harlow's case of recovery from the passage of an iron bar through the head", American Journal of the Medical Sciences, 1850 (with Dr Edward Williams' statement).
- M. Macmillan, "An Odd Kind of Fame: Stories of Phineas Gage", MIT Press, 2000.
- "Phineas Gage", Wikipedia (with references). https://en.wikipedia.org/wiki/Phineas_Gage
- Skull engraving: Harlow 1868 (public domain), via Wikimedia Commons."""

DESCRIPTION = (
    "Cavendish, Vermont, 13 September 1848. Phineas Gage, 25, was a railroad construction foreman, and his employers "
    "thought him the most efficient and capable foreman they had. His job: pack blasting powder into holes in the rock "
    "with a smooth iron tamping bar, 3 ft 7 in long and 13¼ lb (1.1 m, 6 kg).\n\n"
    "His men caught his attention, he looked over his shoulder, and the iron struck a spark on the rock. The powder "
    "exploded. The bar went in under his left cheekbone, passed behind his left eye and came out through the top of "
    "his head. It landed about 80 feet (25 m) away.\n\n"
    "Within minutes he spoke. He rode to his hotel sitting up in an ox cart, and Dr Edward Williams later remembered "
    "his greeting: \"Doctor, here is business enough for you.\" He survived, and he kept the iron. But his friends said "
    "he was \"no longer Gage\". What that really meant is a longer story. This is a history story, not medical "
    "advice.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

# comment challenge (plan/comment-challenges.md formats): "Your guess" sets up the long video + S2. DRAFT: needs the
# user's OK and a score row in comment-challenges.md
CHALLENGE = ("\"No longer Gage.\" What do you think changed in him? Your guess 👇 (And did you spot Matt's glasses? 👓)")

TIKTOK = """Phineas Gage, 1848: a 13-pound iron bar went through his head. Minutes later, he spoke.

His friends said he was "no longer Gage." More true stories on YouTube: Oddly Matt

#history #medicalhistory #phineasgage #neuroscience #oddlymatt"""

INSTAGRAM = """1848, Vermont: a 13-pound iron bar went through Phineas Gage's head. Minutes later, he spoke.

He rode to his hotel sitting up in an ox cart, and he kept the iron.
Source: Dr John Harlow's 1868 report.

More true stories on YouTube (link in bio)

#history #medicalhistory #phineasgage #neuroscience #oddlymatt"""

FACEBOOK = """In 1848, a blast on a Vermont railroad sent an iron bar through a foreman's head. Minutes later, he was talking.

Phineas Gage rode to his hotel sitting up in an ox cart and greeted the doctor with "Doctor, here is business enough for you." He survived and kept the iron. But his friends said he was "no longer Gage."

More true stories on YouTube: oddlymatt.com

#history #phineasgage"""

HOOK_CARD = "An iron bar / through his *skull*."   # hook card A, approved 2026-11-18


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["title"] = TITLE
    ep["publish"] = {
        # DRAFT cover: Harlow's engraving (s6, the image people know); re-check after the full-size file replaces the
        # 165 px stand-in. The title sits in the TOP band above the bar's end.
        "cover": {"image": "proj:assets/images/keyframes/s6.png", "title": "Iron Through His Skull", "accent": ["SKULL"],
                  "kicker": "VERMONT · 1848", "textY": 300, "scale": 1.0, "x": 0, "y": 0},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": TITLE, "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["Phineas Gage", "Phineas Gage story", "tamping iron", "iron bar through skull", "1848",
                     "Cavendish Vermont", "medical history", "history of medicine", "neuroscience history", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": CHALLENGE,
            "related_video": "The Man With a Window Into His Stomach",   # Dec 13: switch to HC002-L (slate)
            "playlists": "Season Zero + History Got It Wrong",
            "schedule": YT_WHEN,
            "publish_at": {"date": "2026-11-29", "et": "15:00", "alberta": "14:00"},
        },
        "tiktok": {"caption": TIKTOK, "first_comment": CHALLENGE + "\n\nMore true stories: search Oddly Matt on YouTube",
                   "playlist": "none", "when": SOCIAL_WHEN, "change_log": "C001",
                   "publish_at": {"date": "2026-11-30", "et": "18:00", "alberta": "17:00"}},
        "instagram": {"caption": INSTAGRAM, "first_comment": CHALLENGE + "\n\nMore true stories: link in bio",
                      "playlist": "none (Instagram has no playlists)", "when": SOCIAL_WHEN, "change_log": "C001",
                      "publish_at": {"date": "2026-11-30", "et": "18:00", "alberta": "17:00"}},
        "facebook": {"caption": FACEBOOK,
                     "first_comment": CHALLENGE + "\n\nMore true stories on YouTube: https://www.youtube.com/@oddlymatt",
                     "playlist": "History Got It Wrong (one playlist only on Facebook; no cover needed)",
                     "when": SOCIAL_WHEN, "change_log": "C001",
                     "publish_at": {"date": "2026-11-30", "et": "18:00", "alberta": "17:00"}},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only: short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)
    publish_social.finish(PID)


if __name__ == "__main__":
    main()
