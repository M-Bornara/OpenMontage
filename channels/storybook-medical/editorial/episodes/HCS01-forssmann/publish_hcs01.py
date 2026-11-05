"""HCS01 Forssmann: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs01-forssmann/renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json,
CREDITS.txt). Related Video = HC001-L. Live Sun Nov 15, 15:00 ET (upload-schedule.md plan v2).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS01-forssmann/publish_hcs01.py
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
PID = "hcs01-forssmann"

SOURCES = """SOURCES
- Werner Forssmann, Biographical (Les Prix Nobel, 1956). https://www.nobelprize.org/prizes/medicine/1956/forssmann/biographical/
- W. Forssmann, "Die Sondierung des rechten Herzens", Klinische Wochenschrift 8 (1929): 2085-2087.
- H. W. Heiss, J. W. Hurst, "Werner Forssmann: a German problem with the Nobel Prize", Clinical Cardiology 15 (1992): 547-549.
- D. Siegel, "Werner Forssmann and the Nazis", American Journal of Cardiology 80 (1997): 1643-1644.
- LITFL, "Werner Forssmann". https://litfl.com/werner-forssmann/"""

DESCRIPTION = (
    "1929, Eberswalde, Germany. Werner Forssmann, a 25-year-old trainee surgeon, wanted to reach a living heart "
    "through a vein. His boss said no. So he numbed his own arm, slid a 65 cm catheter up the vein, and walked to the "
    "X-ray room to prove the tip was inside his heart. It was.\n\n"
    "His next boss, at the Charité in Berlin, dismissed him. 27 years later he shared the 1956 Nobel Prize in "
    "Medicine with André Cournand and Dickinson Richards, who turned his idea into cardiac catheterization, now used "
    "millions of times a year.\n\n"
    "He also joined the Nazi Party in 1932 and stayed a member until 1945. The experiment doesn't erase that, and we "
    "won't leave it out.\n\n"
    "More true medical stories: \"The Man With a Window Into His Stomach\" (linked above).")

CAPTION = ("1929: his boss said no, so this doctor pushed a tube through his own arm into his own heart. Then he "
           "walked to the X-ray room. #history #medicalhistory #truestory #oddlymatt")


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["publish"] = {
        # the approved 4K s6a frame (the action, his face); the generated poster put the tube on the wrong arm over a
        # flat band (covers/cover.png, unused)
        "cover": {"image": "proj:assets/images/keyframes/s6a.png", "title": "Into His Own Heart", "accent": ["HEART"],
                  "kicker": "EBERSWALDE · 1929", "textY": 290, "scale": 1.12, "y": 5.5, "x": -4},
        "youtube": {
            "title": "He Pushed a Tube Into His Own Heart", "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["Werner Forssmann", "cardiac catheterization", "self experimentation", "Nobel Prize 1956",
                     "history of medicine", "medical history", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": "Brave genius 🧠 or reckless rule-breaker ⚠️? Pick one. (And did you spot Matt's glasses? 👓)",
            "related_video": "The Man With a Window Into His Stomach",
            "playlists": "Season Zero + Crazy Science (true stories)",
            "schedule": "Sun Nov 15, 15:00 ET = 14:00 Alberta",
        },
        **{plat: {"caption": CAPTION} for plat in ("tiktok", "instagram", "facebook")},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
