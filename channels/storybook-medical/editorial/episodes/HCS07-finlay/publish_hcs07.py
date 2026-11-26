"""HCS07 Finlay: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs07-finlay/renders/deliverables/ and publish_social.finish() adds the publish times + per-platform blocks
(change C001). Live Thu Dec 3, 15:00 ET (Finlay's birthday; Latin America's Medicine Day). Socials next day 18:00 ET:
C001's 4 posts are HCS08, HCS09, HCS07, HCS05 (unless the Dec 1/5 slots fill first); C003 (same-day TikTok) comes after.
Facts: research.md. "Almost nobody believed" (not "ridiculed", not "nobody"); Lazear's bite DISPUTED (said so);
Medicine Day: no founding year (research.md). Tags: vidIQ keyword research 2026-11-15 (change C004).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS07-finlay/publish_hcs07.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
sys.path.insert(0, str(SCRIPTS))
import publish_social  # noqa: E402

PID = "hcs07-finlay"
YT_WHEN = "Thu Dec 3, 15:00 ET = 14:00 Alberta"
SOCIAL_WHEN = "Fri Dec 4, 18:00 ET = 17:00 Alberta"

SOURCES = """SOURCES
- C. J. Finlay, "El mosquito hipotéticamente considerado como agente de transmisión de la fiebre amarilla", Havana Academy of Sciences, 14 August 1881.
- W. Reed, J. Carroll, A. Agramonte, J. Lazear: reports of the US Army Yellow Fever Commission, 1900–1901.
- "Carlos Finlay", Wikipedia (with references). https://en.wikipedia.org/wiki/Carlos_Finlay
- Thomas Jefferson University archives, notable alumni: Carlos Finlay. https://library.jefferson.edu/archives/exhibits/notable_alumni/juan_carlos_finlay.cfm
- Hektoen International, on Carlos Finlay. https://hekint.org/?p=33826"""

DESCRIPTION = (
    "Havana, 1881. Yellow fever was killing thousands, and nobody knew how it spread. On 14 August 1881 Dr Carlos "
    "Finlay told the Havana Academy of Sciences that a mosquito carried it. Almost nobody believed him, and for "
    "nineteen years he kept breeding mosquitoes and testing his idea.\n\n"
    "In 1900 a US Army commission led by Walter Reed came to Cuba and finally tested it, with mosquitoes from "
    "Finlay's own eggs. One of the team, Dr Jesse Lazear, was bitten and died of yellow fever. (How he was bitten is "
    "disputed: he said a stray mosquito bit him by accident, but a notebook entry suggests he may have infected himself "
    "on purpose.) The commission showed the mosquito was the carrier: Finlay had been right all along.\n\n"
    "Reed got most of the fame, but Reed himself gave the credit to Finlay. Finlay was born on 3 December 1833, and "
    "Latin America marks 3 December as Medicine Day in his honour. This is a history story, not medical advice.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

CHALLENGE = ("Who deserves the credit: Finlay 🦟 or Reed 🎖️? Pick one. (And did you spot Matt's glasses? 👓)")

TIKTOK = """Carlos Finlay found what spreads yellow fever: the mosquito 🦟 Havana, 1881. Almost nobody believed him for 19 years.

More true stories on YouTube: Oddly Matt

#history #medicalhistory #yellowfever #mosquito #oddlymatt"""

INSTAGRAM = """1881, Havana: a doctor said mosquitoes spread yellow fever. Almost nobody believed him.

19 years later, a US Army team tested his idea with his own mosquitoes, and proved him right.
Source: Finlay's 1881 paper; the Reed Commission reports (1900–01).

More true stories on YouTube (link in bio)

#history #medicalhistory #yellowfever #mosquito #oddlymatt"""

FACEBOOK = """In 1881, a Cuban doctor said a mosquito was spreading yellow fever. Almost nobody believed him.

Carlos Finlay kept breeding mosquitoes and testing his idea for nineteen years. In 1900, a US Army team led by Walter Reed tested it with Finlay's own mosquitoes, and proved him right. Reed himself gave Finlay the credit.

More true stories on YouTube: oddlymatt.com

#history #yellowfever"""

HOOK_CARD = "a tiny suspect. / *19* years of doubt."   # C006 v2.1, approved 2026-11-17 (plan/hook-cards-v2.1.md)


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["title"] = "He Was Right About the Mosquito. It Took 19 Years."
    ep["publish"] = {
        # s3: Finlay with the mosquito on his hand; the title sits in the TOP band above his head
        "cover": {"image": "proj:assets/images/keyframes/s3.png", "title": "It Was the Mosquito", "accent": ["MOSQUITO"],
                  "kicker": "HAVANA · 1881", "textY": 300, "scale": 1.06, "x": 0, "y": 10},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": "He Was Right About the Mosquito. It Took 19 Years.", "description": DESCRIPTION,
            "sources": SOURCES,
            "tags": ["Carlos Finlay", "yellow fever", "Aedes aegypti", "mosquito", "Walter Reed", "Jesse Lazear",
                     "Havana 1881", "medical history", "history of medicine", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": CHALLENGE,
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + History Got It Wrong",
            "schedule": YT_WHEN,
            "publish_at": {"date": "2026-12-03", "et": "15:00", "alberta": "14:00"},
        },
        "tiktok": {"caption": TIKTOK, "first_comment": CHALLENGE + "\n\nMore true stories: search Oddly Matt on YouTube",
                   "playlist": "none", "when": SOCIAL_WHEN, "change_log": "C001",
                   "publish_at": {"date": "2026-12-04", "et": "18:00", "alberta": "17:00"}},
        "instagram": {"caption": INSTAGRAM, "first_comment": CHALLENGE + "\n\nMore true stories: link in bio",
                      "playlist": "none (Instagram has no playlists)", "when": SOCIAL_WHEN, "change_log": "C001",
                      "publish_at": {"date": "2026-12-04", "et": "18:00", "alberta": "17:00"}},
        "facebook": {"caption": FACEBOOK,
                     "first_comment": CHALLENGE + "\n\nMore true stories on YouTube: https://www.youtube.com/@oddlymatt",
                     "playlist": "History Got It Wrong (one playlist only on Facebook; no cover needed)",
                     "when": SOCIAL_WHEN, "change_log": "C001",
                     "publish_at": {"date": "2026-12-04", "et": "18:00", "alberta": "17:00"}},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only: short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)
    publish_social.finish(PID)


if __name__ == "__main__":
    main()
