"""HCS08 John Snow: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs08-john-snow/renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json,
CREDITS.txt). Related Video = HC001-L. Live Wed Nov 25, 15:00 ET (upload-schedule.md plan v2).
Facts: research.md (all VERIFIED; "the handle stopped it" is the OVERSTATEMENT the Short itself corrects).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS08-john-snow/publish_hcs08.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
PID = "hcs08-john-snow"

SOURCES = """SOURCES
- John Snow, On the Mode of Communication of Cholera, 2nd ed. (London, 1855), with the Broad Street map. https://johnsnow.matrix.msu.edu/
- Rev. Henry Whitehead, report to the Cholera Inquiry Committee of St James's parish (1855).
- "1854 Broad Street cholera outbreak", Wikipedia (figures and timeline, with references). https://en.wikipedia.org/wiki/1854_Broad_Street_cholera_outbreak
- UCLA Department of Epidemiology, John Snow site. https://epi-snow.ph.ucla.edu/
- E. W. Chave, "Henry Whitehead and cholera in Broad Street", Medical History (1958)."""

DESCRIPTION = (
    "1854, Soho, London. Cholera killed more than five hundred people within a few streets in about ten days. Most "
    "doctors blamed \"miasma\", bad air. The doctor John Snow suspected the water. He listed the deaths house by house, "
    "and they clustered around one public pump on Broad Street.\n\n"
    "The brewery next door had no cases: its workers had a beer allowance and didn't drink the pump water. A widow "
    "living miles away in Hampstead died too; she liked the taste of Broad Street water and had it brought to her. "
    "Snow showed the parish board on 7 September, and on 8 September the pump's handle was removed.\n\n"
    "The twist: the outbreak was already falling by then, and Snow said so himself in his 1855 book. Removing the "
    "handle didn't end the outbreak on its own. What lasted was his evidence, above all his map of the deaths, which "
    "is still how disease detectives work today. This is a history story, not medical advice.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

CAPTION = ("1854: cholera in London. One doctor blamed the water and took the handle off a pump. But there's a twist. "
           "#history #medicalhistory #johnsnow #oddlymatt")


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["publish"] = {
        # the approved 4K s1b close-up of the pump in the fog; title in the TOP band, the pump below it
        "cover": {"image": "proj:assets/images/keyframes/s1b.png", "title": "He Broke the Pump", "accent": ["PUMP"],
                  "kicker": "LONDON · 1854", "textY": 300, "scale": 1.08, "x": 0, "y": 10},
        "youtube": {
            "title": "He Stopped a Plague by Breaking a Pump?", "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["John Snow", "Broad Street pump", "cholera", "1854 cholera outbreak", "Soho", "epidemiology",
                     "Victorian London", "history of medicine", "disease detective", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": "The real source? A baby's nappies, washed into a cesspool about three feet from the well. 👶 "
                              "Did you know that one? (And did you spot Matt's glasses? 👓)",
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + Crazy Science",
            "schedule": "Wed Nov 25, 15:00 ET = 14:00 Alberta",
        },
        **{plat: {"caption": CAPTION} for plat in ("tiktok", "instagram", "facebook")},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
