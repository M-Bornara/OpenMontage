"""HC002-S1 Gage: the upload texts (episode.json "publish"); approved 2026-11-19 with "near Cavendish" (C01) and the shot 1 cover.
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

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
sys.path.insert(0, str(SCRIPTS))
import claim_tags  # noqa: E402
import publish_social  # noqa: E402

PID = "hc002-s1"
TITLE = "He Took an Iron Bar Through the Skull… and Spoke [C04 C05]"    # title 1, approved 2026-11-18
YT_WHEN = "Sun Nov 29, 15:00 ET = 14:00 Alberta"
SOCIAL_WHEN = "Mon Nov 30, 18:00 ET = 17:00 Alberta"

SOURCES = """SOURCES
- J. M. Harlow, "Recovery from the passage of an iron bar through the head", Publications of the Massachusetts Medical Society, 1868. https://archive.org/details/66210360R.nlm.nih.gov
- H. J. Bigelow, "Dr. Harlow's case of recovery from the passage of an iron bar through the head", American Journal of the Medical Sciences, 1850 (with Dr Edward Williams' statement).
- M. Macmillan, "An Odd Kind of Fame: Stories of Phineas Gage", MIT Press, 2000.
- "Phineas Gage", Wikipedia (with references). https://en.wikipedia.org/wiki/Phineas_Gage
- Skull engraving: Harlow 1868, plate Fig. 2 (public domain), from the Internet Archive scan of the National Library of Medicine copy."""

# Every public sentence ends with its claim tag (scripts/claim_tags.py; [NF] = no factual claim, added 2026-11-21).
# claim_tags.strip() removes the tags before episode.json; fact-gate/package-s1.md is what the fact gate reads.
DESCRIPTION = (
    "Near Cavendish, Vermont, 13 September 1848. [C01] Phineas Gage, 25, was a railroad construction foreman, and his "
    "employers thought him the most efficient and capable foreman they had. [C01 C18] His job: pack blasting powder into "
    "holes in the rock with a smooth iron tamping bar, 3 ft 7 in long and 13¼ lb (1.1 m, 6 kg). [C23 C02]\n\n"
    "His men caught his attention, he looked over his shoulder, and the iron struck a spark on the rock. [C03] The "
    "powder exploded. [C03] The bar went in under his left cheekbone, passed behind his left eye and came out through "
    "the top of his head. [C04] It landed about 80 feet (24 m) away. [C04]\n\n"
    "Within minutes he spoke. [C05] He rode to his hotel sitting up in an ox cart, and Dr Williams later "
    "remembered his greeting: \"Doctor, here is business enough for you.\" [C05 C06] He survived, and he kept the "
    "iron. [C32 C07] But his friends said he was \"no longer Gage\". [C08] What that really meant is a longer story. "
    "[NF] This is a history story, not medical advice. [NF]\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above). [NF]")

# comment challenge (plan/comment-challenges.md formats): "Your guess" sets up the long video + S2. Approved 2026-11-19
CHALLENGE = ("\"No longer Gage.\" [C08] What do you think changed in him? [NF] Your guess 👇 (And did you spot Matt's "
             "glasses? 👓) [NF]")

TIKTOK = """Phineas Gage, 1848: a 13¼-pound iron bar went through his head. [C01 C02 C04] Minutes later, he spoke. [C05]

His friends said he was "no longer Gage." [C08] More true stories on YouTube: Oddly Matt

#history #medicalhistory #phineasgage #neuroscience #oddlymatt"""

INSTAGRAM = """1848, Vermont: a 13¼-pound iron bar went through Phineas Gage's head. [C01 C02 C04] Minutes later, he spoke. [C05]

He rode to his hotel sitting up in an ox cart, and he kept the iron. [C05 C07]
Source: Dr John Harlow's 1868 report. [C30]

More true stories on YouTube (link in bio)

#history #medicalhistory #phineasgage #neuroscience #oddlymatt"""

FACEBOOK = """In 1848, a blast on a Vermont railroad sent an iron bar through a foreman's head. [C01 C03 C04] Minutes later, he was talking. [C05]

Phineas Gage rode to his hotel sitting up in an ox cart, and Dr Williams later remembered his greeting: "Doctor, here is business enough for you." [C05 C06] He survived and kept the iron. [C32 C07] But his friends said he was "no longer Gage." [C08]

More true stories on YouTube: oddlymatt.com

#history #phineasgage"""

HOOK_CARD = "An iron bar / through his *skull*. [C04]"   # hook card A, approved 2026-11-18


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["title"] = TITLE
    ep["publish"] = {
        # cover (user 2026-11-19): the shot 1 blast frame at 0.45 s (cover_frame_hc002s1.py, no text layers): the bar
        # flying against the sky, Gage's silhouette thrown back, the hat in the air. The title sits in the sky band.
        "cover": {"image": "proj:assets/images/covers/s1-blast.png", "title": "Iron Through His Skull", "accent": ["SKULL"],
                  "kicker": "VERMONT · 1848", "textY": 300, "scale": 1.12, "x": 0, "y": 6.5},
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
    tagged = ep["publish"]
    claim_tags.check(tagged, HERE / "claims.csv")    # every public sentence has a claim ID that may be used
    (HERE / "fact-gate").mkdir(exist_ok=True)
    (HERE / "fact-gate/package-s1.md").write_text(claim_tags.gate_text(tagged, "HC002-S1 Gage package"),
                                                  encoding="utf-8")
    ep["publish"] = claim_tags.strip(tagged)
    ep["title"] = claim_tags.strip(TITLE)
    publish_social.check(ep["publish"])          # caption lint (CTA lines)
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only: short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)
    publish_social.finish(PID)


if __name__ == "__main__":
    main()
