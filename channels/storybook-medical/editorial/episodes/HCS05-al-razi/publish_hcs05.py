"""HCS05 al-Razi: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs05-al-razi/renders/deliverables/ and publish_social.finish() adds the publish times + per-platform blocks
(change C001). Live Mon Dec 7, 15:00 ET; socials next day 18:00 ET (C001's 4th post; C003 comes after).
Facts: research.md (P1 the Hawi passage via the James Lind Library, S1 Pormann 2019). "Half his patients" is NOT
claimed (group sizes unknown): the title says "some patients". "First clinical trial" = OVERSTATEMENT, said so.
His look: the 1956 Iranian portrait (Wellcome S0001954, CC BY 4.0: attribution below). Tags: vidIQ 2026-11-15 (C004).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS05-al-razi/publish_hcs05.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
sys.path.insert(0, str(SCRIPTS))
import publish_social  # noqa: E402

PID = "hcs05-al-razi"
YT_WHEN = "Mon Dec 7, 15:00 ET = 14:00 Alberta"
SOCIAL_WHEN = "Tue Dec 8, 18:00 ET = 17:00 Alberta"

SOURCES = """SOURCES
- al-Razi, Kitab al-Hawi (the Comprehensive Book), vol. 15 p. 122 (Hyderabad ed.), in the James Lind Library. https://www.jameslindlibrary.org/al-razi-10th-century-ce-4th-century-ah/
- P. E. Pormann, "Concepts of patient groups in 10th-century Iraq and Persia", J R Soc Med 2019. https://www.jameslindlibrary.org/articles/concepts-of-patient-groups-in-10th-century-iraq-and-persia/
- Al-Razi's look follows the portrait painted for the 5th Iranian Medical Congress, 1956: Wellcome Collection S0001954, CC BY 4.0. No portrait from his lifetime survives."""

DESCRIPTION = (
    "Rey, near today's Tehran, around 900 AD. For the first signs of meningitis, the standard treatment was "
    "bloodletting. The Persian physician Abu Bakr al-Razi (c. 865–925) had a doubt: what if it did nothing? So he bled "
    "one group of patients and deliberately left another group untreated, to compare them.\n\n"
    "He wrote that the bled group did better, and kept the treatment. He was wrong: bloodletting doesn't help "
    "meningitis. The passage survives in his Kitab al-Hawi, which his students compiled from his notebooks after his "
    "death, and it is the only passage in it that compares two groups of patients.\n\n"
    "Some call it the first clinical trial. That's an overstatement, but his method, two groups side by side, is how "
    "every medicine is tested today. This is a history story, not medical advice.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

CHALLENGE = ("Would YOU have left some patients untreated to find out if the cure worked? ⚖️ Be honest. "
             "(And did you spot Matt's glasses? 👓)")

TIKTOK = """Al-Razi, the Persian doctor who tested a cure 1,100 years ago ⚖️ He bled one group of patients and left another alone, on purpose.

More true stories on YouTube: Oddly Matt

#history #medicalhistory #alrazi #medievalmedicine #oddlymatt"""

INSTAGRAM = """1,100 years ago, a doctor refused to treat some of his patients. On purpose.

Al-Razi compared two groups to test a cure. His answer was wrong. His method is how we test medicines today.
Source: al-Razi's Kitab al-Hawi (via the James Lind Library).

More true stories on YouTube (link in bio)

#history #medicalhistory #alrazi #medievalmedicine #oddlymatt"""

FACEBOOK = """Around 900 AD, a Persian doctor deliberately left some of his patients untreated.

Al-Razi wanted to know if bloodletting really helped early meningitis, so he bled one group and left another alone. He decided it worked, and he was wrong. But comparing two groups side by side is still how every medicine is tested today.

More true stories on YouTube: oddlymatt.com

#history #medicalhistory"""

HOOK_CARD = "one group bled. / one left *alone*."   # C006 v2.1, approved 2026-11-17 (plan/hook-cards-v2.1.md)


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["title"] = "1,100 Years Ago, a Doctor Refused to Treat Patients on Purpose"
    ep["publish"] = {
        # s1b: his face close-up (the 1956 portrait look); title in the TOP band above the turban
        "cover": {"image": "proj:assets/images/keyframes/s1b.png", "title": "Untreated. On Purpose",
                  "accent": ["PURPOSE"], "kicker": "PERSIA · c. 900", "textY": 300, "scale": 1.06, "x": 0, "y": 24},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": "1,100 Years Ago, a Doctor Refused to Treat Patients on Purpose", "description": DESCRIPTION,
            "sources": SOURCES,
            "tags": ["al-Razi", "Rhazes", "Abu Bakr al-Razi", "medieval medicine", "Islamic Golden Age",
                     "clinical trial", "bloodletting", "history of medicine", "medical history", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": CHALLENGE,
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + Crazy Science",
            "schedule": YT_WHEN,
            "publish_at": {"date": "2026-12-07", "et": "15:00", "alberta": "14:00"},
        },
        "tiktok": {"caption": TIKTOK, "first_comment": CHALLENGE + "\n\nMore true stories: search Oddly Matt on YouTube",
                   "playlist": "none", "when": SOCIAL_WHEN, "change_log": "C001",
                   "publish_at": {"date": "2026-12-08", "et": "18:00", "alberta": "17:00"}},
        "instagram": {"caption": INSTAGRAM, "first_comment": CHALLENGE + "\n\nMore true stories: link in bio",
                      "playlist": "none (Instagram has no playlists)", "when": SOCIAL_WHEN, "change_log": "C001",
                      "publish_at": {"date": "2026-12-08", "et": "18:00", "alberta": "17:00"}},
        "facebook": {"caption": FACEBOOK,
                     "first_comment": CHALLENGE + "\n\nMore true stories on YouTube: https://www.youtube.com/@oddlymatt",
                     "playlist": "Crazy Science (one playlist only on Facebook; no cover needed)",
                     "when": SOCIAL_WHEN, "change_log": "C001",
                     "publish_at": {"date": "2026-12-08", "et": "18:00", "alberta": "17:00"}},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only: short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)
    publish_social.finish(PID)


if __name__ == "__main__":
    main()
