"""HCS06 Onesimus: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs06-onesimus/renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json,
CREDITS.txt). Related Video = HC001-L. Live Mon Nov 23, 15:00 ET (upload-schedule.md plan v2).
Facts: research.md (all VERIFIED except where noted; the note is quoted only as far as the sources agree).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS06-onesimus/publish_hcs06.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
PID = "hcs06-onesimus"

SOURCES = """SOURCES
- Zabdiel Boylston, An Historical Account of the Small-Pox Inoculated in New England (London, 1726).
- Cotton Mather, letters to the Royal Society (1716) and diary (1721).
- "1721 Boston smallpox outbreak", Wikipedia (figures and timeline, with references). https://en.wikipedia.org/wiki/1721_Boston_smallpox_outbreak
- History of Vaccines (College of Physicians of Philadelphia), "Onesimus spreads wisdom that saves lives". https://historyofvaccines.org/blog/black-history-month-onesimus-spreads-wisdom-that-saves-lives-of-bostonians-during-a-smallpox-epidemic/
- E. Blakemore, History.com, on Onesimus and Cotton Mather. https://www.history.com/articles/smallpox-vaccine-onesimus-slave-cotton-mather"""

DESCRIPTION = (
    "1721, Boston. Smallpox swept through the town. Years earlier, Onesimus, an enslaved West African man in the "
    "household of the minister Cotton Mather, had told Mather how people in West Africa protected themselves: a tiny "
    "cut, a little matter from a smallpox sore, a mild illness, then protection for life.\n\n"
    "Mather begged the town's doctors to try it. Only Zabdiel Boylston agreed. On 26 June 1721 he inoculated his own "
    "six-year-old son and two enslaved people in his household. The town was furious: in November someone threw a "
    "grenade through Mather's window, and the fuse went out. The note began: \"Cotton Mather, you dog, damn you! I'll "
    "inoculate you with this...\"\n\n"
    "About 1 in 7 people who caught smallpox in Boston that year died (844 of about 5,759). Among Boylston's "
    "inoculated patients, about 1 in 40 (6 of 247). Inoculation still carried real risk; vaccination, safer, came "
    "75 years later. The idea came from Onesimus, and for centuries his name was mostly left out of the story. "
    "This is a history story, not medical advice.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

# NOTE (2026-11-17): publish.md now has per-platform TikTok/IG/FB captions + first comments written by hand; running
# episode.py publish (this script without --texts-only) would replace them with this single caption. Carry them over first.
CAPTION = ("1721: smallpox hit Boston. The idea that saved lives came from an enslaved man named Onesimus. "
           "#history #blackhistory #medicalhistory #oddlymatt")
HOOK_CARD = "A *grenade* through / the window. Why?"   # C006 v2.1, card A picked 2026-11-17 (plan/hook-cards-v2.1.md)


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["publish"] = {
        # the approved 4K s9 close-up (his face, looking at us). Title in the TOP band (v1 at 1450 was cut by the crops
        # and sat under TikTok's UI); the picture moves down so his face sits under the title
        "cover": {"image": "proj:assets/images/keyframes/s9.png", "title": "He Saved Boston", "accent": ["SAVED"],
                  "kicker": "BOSTON · 1721", "textY": 300, "scale": 1.08, "x": 0, "y": 14},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": "The Enslaved Man Who Saved Boston", "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["Onesimus", "Cotton Mather", "Zabdiel Boylston", "smallpox", "inoculation", "variolation",
                     "Boston 1721", "Black history", "history of medicine", "Oddly Matt"],
            "hashtags": ["#history", "#blackhistory", "#oddlymatt"],
            "pinned_comment": "Should Onesimus be as famous as Edward Jenner? 🤔 Tell us why. (And did you spot Matt's glasses? 👓)",
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + History Got It Wrong (NEW playlist: create it on upload; cover in projects/_playlists/renders/)",
            "schedule": "Mon Nov 23, 15:00 ET = 14:00 Alberta",
        },
        **{plat: {"caption": CAPTION} for plat in ("tiktok", "instagram", "facebook")},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only: short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
