"""HC001 Shorts S1/S2/S3: the upload texts (episode.json "publish"), then `episode.py publish` builds each project's
renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json, CREDITS.txt).
Pinned comments = the scored comment challenges (plan/comment-challenges.md). Every Short's Related Video = HC001-L.
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HC001-st-martin/publish_hc001_shorts.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"

SOURCES = """SOURCES
- William Beaumont, Experiments and Observations on the Gastric Juice, and the Physiology of Digestion (1833). https://archive.org/details/2543009R.nlm.nih.gov
- William Osler, "William Beaumont: A Backwoods Physiologist" (1902). https://archive.org/details/b31349092
- Becker Medical Library, Washington University. https://becker.wustl.edu/news/william-beaumonts-momentous-and-unethical-experiments/"""
FULL = "The full story, from the accident to the last letter: \"The Man With a Window Into His Stomach\" (linked above)."
TAGS = ["Alexis St. Martin", "William Beaumont", "history of medicine", "medical history", "digestion", "strange medical cases",
        "Oddly Matt"]
HASH = ["#history", "#medicalhistory", "#oddlymatt"]
PLAYLIST = "Season Zero · Alexis St. Martin"

SHORTS = {
    "hc001-s1": dict(
        schedule="Wed Nov 11, 13:00 MT (15:00 ET)",
        kicker="MACKINAC · 1822",                      # one line on the cover
        title="He Survived a Hole in His Stomach",
        description="1822, Mackinac Island. A musket went off by accident less than a meter from Alexis St. Martin, an "
                    "18-year-old canoeman. For 17 days, everything he swallowed came back out through the wound. He "
                    "should have died. He lived 58 more years, with an opening into his stomach that never closed.",
        tags=["Mackinac Island", "gunshot survivor"],
        pinned="Alexis refused the surgery that could have closed it. Would you have said no? 🤔",
        caption="He was shot from less than a meter away in 1822, and lived 58 more years with a hole in his stomach. "
                "True story. #history #medicalhistory #truestory #oddlymatt",
    ),
    "hc001-s2": dict(
        schedule="Mon Nov 9, 13:00 MT (15:00 ET)",
        kicker="FORT NIAGARA · 1825", textY=220,       # the title clears his cap
        title="The Doctor Who Put Food on a String",
        description="1825. Army surgeon William Beaumont tied six foods to a silk string and lowered them into a living "
                    "man's stomach, through an opening a gunshot had left. After one hour, the bread and cabbage were "
                    "half gone. After two, four of the six had vanished. It was experiment #1 of 238.",
        tags=["Fort Niagara", "gastric juice", "medical experiments"],
        pinned="Beaumont: genius 🧠 or went too far ⚠️? Pick one.",
        caption="In 1825 a doctor lowered lunch into a living man's stomach. On a string. Experiment #1 of 238. "
                "#history #medicalhistory #truestory #oddlymatt",
    ),
    "hc001-s3": dict(
        schedule="Fri Nov 13, 13:00 MT (15:00 ET)",
        kicker="1825 · 1852",
        title="The Human Experiment Who Walked Away",
        description="The most famous stomach in medical history belonged to a man who kept leaving. Alexis St. Martin "
                    "walked away from Dr. Beaumont in 1825, was brought back with his wife and two children, signed a "
                    "contract as a \"covenant servant\" in 1833, and then never went back, despite 18 years of letters "
                    "and bigger offers.",
        tags=["medical ethics", "covenant servant", "consent"],
        pinned="Who was right: Alexis 🛶 or Beaumont 🩺?",
        caption="The most famous stomach in medical history belonged to a man who kept walking away. "
                "#history #medicalhistory #truestory #oddlymatt",
    ),
}


def main():
    for pid, s in SHORTS.items():
        p = REPO / "projects" / pid / "episode.json"
        ep = json.load(open(p, encoding="utf-8"))
        pub = ep.setdefault("publish", {})
        pub["cover"]["kicker"] = s["kicker"]
        if "textY" in s:
            pub["cover"]["textY"] = s["textY"]
        pub["youtube"] = {
            "title": s["title"], "description": s["description"] + "\n\n" + FULL, "sources": SOURCES,
            "tags": TAGS[:2] + s["tags"] + TAGS[2:], "hashtags": HASH, "pinned_comment": s["pinned"],
            "related_video": "The Man With a Window Into His Stomach", "playlists": PLAYLIST,
            "schedule": s["schedule"],
        }
        for plat in ("tiktok", "instagram", "facebook"):
            pub[plat] = {"caption": s["caption"]}
        json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        subprocess.run([sys.executable, "episode.py", "publish", pid], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
