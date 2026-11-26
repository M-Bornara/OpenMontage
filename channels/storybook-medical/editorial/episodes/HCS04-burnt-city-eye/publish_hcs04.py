"""HCS04 golden eye: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs04-burnt-city-eye/renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt,
publish.md/json, CREDITS.txt). Related Video = HC001-L. Live Sat Nov 21, 15:00 ET (upload-schedule.md plan v2).
Facts: research.md (the find DOCUMENTED; priestess = LEGEND; eye vs eyepatch = DISPUTED; left socket VERIFIED).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS04-burnt-city-eye/publish_hcs04.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
PID = "hcs04-burnt-city-eye"

SOURCES = """SOURCES
- "Iran's burial goods", Archaeology Magazine (Nov/Dec 2011). https://archive.archaeology.org/1111/features/iran_burial_goods.html
- L. Moghadasi, "Artificial Eye in Burnt City and Theoretical Understanding of How Vision Works", Iranian Journal of Public Health (2014). https://pmc.ncbi.nlm.nih.gov/articles/PMC4449516/"""

DESCRIPTION = (
    "Around 2900 BC, at Shahr-e Sukhteh, the \"Burnt City\" in south-east Iran, a woman in her late twenties was buried "
    "with an artificial eye. It is a half-ball about 2.5 cm across, made of tar-like bitumen paste under a thin layer of "
    "gold, with an iris and fine lines like rays of light drawn on it. Tiny holes on both sides held it in place with a "
    "fine thread. It was found in her left eye socket, and under a microscope the socket showed an imprint: she had "
    "worn it for a long time.\n\n"
    "Was she a priestess, or a queen? That part is a legend: no source says so. And some archaeologists think it was "
    "an eyepatch, not an eye. Either way, 5,000 years ago, someone made her a golden eye.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

# user 2026-11-17: start with the eye, not the country (the description keeps Shahr-e Sukhteh, south-east Iran)
# user 2026-11-18 (Iran rule): the country stays out of the hook, captions, cover and tags; only the description facts name it
# NOTE (2026-11-17): publish.md now has per-platform TikTok/IG/FB captions + first comments written by hand; running
# episode.py publish (this script without --texts-only) would replace them with this single caption. Carry them over first.
CAPTION = ("A golden eye, worn in a woman's eye socket 5,000 years ago. Archaeologists still argue about what it was. "
           "#history #archaeology #truestory #oddlymatt")
HOOK_CARD = "She wore *gold* / in her eye socket"   # C006 v2.1, approved 2026-11-17 (plan/hook-cards-v2.1.md)


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["publish"] = {
        # the approved 4K s5 frame (her face, the golden eye in her left socket). Title in the TOP band (v1 at 1450 was cut
        # by the 3:4 / 4:5 crops and sat under TikTok's UI); the picture moves down so her face is under the title
        # kicker (user 2026-11-17): the place's own name, not the country; never "Persia" (anachronistic for 2900 BC)
        "cover": {"image": "proj:assets/images/keyframes/s5.png", "title": "Buried With a Golden Eye",
                  "accent": ["GOLDEN", "EYE"], "kicker": "BURNT CITY · 2900 BC", "textY": 300, "scale": 1.1, "x": 2, "y": 12},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": "She Was Buried With a Golden Eye", "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["Shahr-e Sukhteh", "Burnt City", "golden eye", "artificial eye", "ancient prosthetic",
                     "archaeology", "history of medicine", "Oddly Matt"],
            "hashtags": ["#history", "#archaeology", "#oddlymatt"],
            "pinned_comment": "Golden eye or fancy eyepatch? 👁️ Pick a side. (And did you spot Matt's glasses? 👓)",
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + Weirdest Moments (NEW playlist: create it on upload; cover in projects/_playlists/renders/)",
            "schedule": "Sat Nov 21, 15:00 ET = 14:00 Alberta",
        },
        **{plat: {"caption": CAPTION} for plat in ("tiktok", "instagram", "facebook")},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:   # episode.json only (then `episode.py cover`): short.mp4 stays until the render is approved
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
