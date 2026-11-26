"""HCS09 Semmelweis: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs09-semmelweis/renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json,
CREDITS.txt). Related Video = HC001-L. Live Fri Nov 27, 15:00 ET (upload-schedule.md plan v2).
Facts: research.md. "He lost his job" = his post ended in March 1849 and was not renewed (said exactly below);
"nobody listened" is an OVERSTATEMENT (some doctors did adopt the washing), so the description says so.
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS09-semmelweis/publish_hcs09.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
PID = "hcs09-semmelweis"

SOURCES = """SOURCES
- Ignaz Semmelweis, Die Ätiologie, der Begriff und die Prophylaxis des Kindbettfiebers (1861), with the clinic tables.
- "Ignaz Semmelweis", Wikipedia (figures and timeline, with references). https://en.wikipedia.org/wiki/Ignaz_Semmelweis
- Museum of Health Care at Kingston, "Ignaz Semmelweis: The Saviour of Mothers". https://museumofhealthcare.blog/ignaz-semmelweis-the-saviour-of-mothers"""

DESCRIPTION = (
    "1847, Vienna General Hospital. It had two maternity clinics, taking women on alternate days. In the First, run by "
    "doctors and medical students, about one mother in ten died of childbed fever; in the Second, run by midwives, far "
    "fewer. Women begged not to be sent to the First.\n\n"
    "Then Ignaz Semmelweis's friend Jakob Kolletschka was cut by a student's scalpel during an autopsy and died with "
    "the same signs as the mothers. The doctors were going from the dissecting room straight to the deliveries. In May "
    "1847 Semmelweis made them wash in chlorinated lime, and by July deaths in the First Clinic fell to about one in a "
    "hundred.\n\n"
    "Many senior doctors rejected his idea, though some did adopt the washing, and he published his full case only in "
    "1861. His post in Vienna ended in March 1849 and was not renewed. In 1865 he was committed to an asylum, where he "
    "died two weeks later of an infected wound (whether it came from a beating there isn't proven). Today, rejecting "
    "new evidence because it clashes with what we already believe is called the Semmelweis reflex. "
    "This is a history story, not medical advice.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

CAPTION = ("1847: a doctor told other doctors to wash their hands. They hated him for it. "
           "#history #medicalhistory #semmelweis #oddlymatt")

HOOK_CARD = "doctors' *hands* / killing mothers?"   # C006 v2.1, approved 2026-11-17 (plan/hook-cards-v2.1.md)


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["publish"] = {
        # the approved 4K s9 close-up of his face; title in the TOP band, his face below it
        "cover": {"image": "proj:assets/images/keyframes/s9.png", "title": "Wash Your Hands", "accent": ["WASH"],
                  "kicker": "VIENNA · 1847", "textY": 300, "scale": 1.08, "x": 0, "y": 14},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": "They Hated Him for Saying \"Wash Your Hands\"", "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["Ignaz Semmelweis", "Semmelweis reflex", "hand washing", "childbed fever", "puerperal fever",
                     "Vienna 1847", "history of medicine", "germ theory", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": "Would YOU have believed him in 1847? 🧼 Be honest. (And did you spot Matt's glasses? 👓)",
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + History Got It Wrong",
            "schedule": "Fri Nov 27, 15:00 ET = 14:00 Alberta",
        },
        **{plat: {"caption": CAPTION} for plat in ("tiktok", "instagram", "facebook")},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only: short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
