"""HCS10 Pettenkofer: the upload texts (episode.json "publish"), then `episode.py publish` builds
projects/hcs10-pettenkofer/renders/deliverables/ (short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json,
CREDITS.txt). Slot (storyboard-v1.md): YouTube Tue Dec 1, 15:00 ET = 14:00 Alberta; socials Wed Dec 2, 18:00 ET = 17:00
Alberta. Pair: Marshall ("The Doctor Who Drank Bacteria"), pinned comment "Who was braver?".
Every fact is VERIFIED or ATTRIBUTED in claims.csv; kept out on purpose: "Koch sent it" (C11, REMOVE), "a whole glass"
(C16), "a billion germs" (C15), how he died (C43), any amounts beyond his own 1 cc (C12/C14: no copy risk on screen).
The cover is the hook moment composed from the real pieces (plate-s1 + the hand-and-glass at his lips, clear glass).
Run from the repo root:  python channels/storybook-medical/editorial/episodes/HCS10-pettenkofer/publish_hcs10.py [--texts-only]
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SCRIPTS = REPO / "channels/storybook-medical/scripts"
PID = "hcs10-pettenkofer"
P = REPO / "projects" / PID

SOURCES = """SOURCES
- Max von Pettenkofer's own account, English translation in the Journal of Hygiene obituary (1901).
- "Professor von Pettenkofer on Cholera", British Medical Journal, 19 November 1892.
- R. Burnett, "Max von Pettenkofer and the cholera experiment" (2009), with the BMJ report reprinted.
- SRF Wissen, "Der Selbstversuch des Max von Pettenkofer" (2015).
- P. Manson, Tropical Diseases (1919): Hamburg cholera deaths, 1892.
- R. A. Cash et al., "Response of man to infection with Vibrio cholerae", Journal of Infectious Diseases 129 (1974)."""

DESCRIPTION = (
    "Munich, 7 October 1892. Max von Pettenkofer, 73, drank a fresh culture of cholera germs in front of witnesses.\n\n"
    "Cholera had just killed about 8,600 people in Hamburg. Robert Koch blamed a germ carried in the drinking water. "
    "Pettenkofer believed the germ alone was not enough: the soil and the ground water had to be right too. Some of his "
    "students offered to take the risk in place of their old teacher. He refused.\n\n"
    "First he drank a little bicarbonate of soda, to neutralise his stomach acid. Then one cubic centimetre of a broth "
    "culture made in Munich from cultures of the Hamburg outbreak, prepared by Georg Gaffky, Koch's former assistant. "
    "He wrote that it tasted like the purest water.\n\n"
    "Two days later came stomach cramps and diarrhoea, for about a week, and the lab found his gut swarming with cholera "
    "germs. But it never turned dangerous, and he declared victory. His critics said he had simply had a mild case of "
    "cholera, and most experts now think so too. Ten days after him, his pupil Rudolf Emmerich repeated the drink and got "
    "much sicker, but survived. And the irony: modern studies show that neutralising stomach acid makes cholera far "
    "easier to catch. The soda made his experiment more dangerous, not less.\n\n"
    "He lost the argument about the water. But his clean-water and sewer work did help Munich. "
    "This is a history story, not medical advice. Never try anything like this.\n\n"
    "Another doctor who drank his own germs: \"The Doctor Who Drank Bacteria\" (linked above).")

HOOK_CARD = "He drank *cholera*. / On purpose."   # chosen 2026-11-18 (storyboard-v1.md: hook card A)

# per-platform captions (oddly-matt-platform-captions rules: facts from claims.csv only, no gore words, Matt's voice,
# 3-5 hashtags on TikTok / Instagram, 1-3 on Facebook) + the first comment for each platform
FIRST = "Who was braver: Pettenkofer or Marshall? 🧪 (Did you spot Matt's glasses? 👓)"
CAPTIONS = {
    "tiktok": ("A 73-year-old professor drank cholera on purpose. Munich, 1892.\n"
               "He wanted to prove his rival wrong. It didn't go to plan.\n"
               "#history #medicalhistory #cholera #oddlymatt\n\n"
               f"First comment: {FIRST}"),
    "instagram": ("1892: a 73-year-old professor drank cholera to win an argument.\n"
                  "Max von Pettenkofer said germs alone couldn't make you sick. He survived the bet… but not the argument. "
                  "(Source: his own account, BMJ 1892.)\n"
                  "#history #medicalhistory #cholera #oddlymatt\n\n"
                  f"First comment: {FIRST}"),
    "facebook": ("In 1892 a famous Munich professor, Max von Pettenkofer, drank a culture of cholera germs in front of "
                 "witnesses.\n"
                 "Cholera had just killed about 8,600 people in Hamburg, and his rival Robert Koch blamed a germ in the "
                 "water. Pettenkofer was sure the germ alone wasn't enough. He got sick for a week, survived, and declared "
                 "victory. His critics said: that was cholera, just a mild case.\n"
                 "#history #oddlymatt\n\n"
                 f"First comment: {FIRST}"),
}


def cover_source() -> str:
    """The hook moment, composed from the approved real pieces (no new image): plate-s1-clean + the hand and the clear
    glass at his lips (hero_real keys at "cholera")."""
    sys.path.insert(0, str(HERE))
    import hero_real_hcs10 as hr
    import hero_previz_hcs10 as hp
    out = P / "assets/images/keyframes/cover-src.png"
    shot, _ = hr.build("1")
    for a in shot["actors"]:
        if a["id"] == "student-hand":
            a["keys"] = [{**k, "x": 2.0} for k in a["keys"]]          # off frame: the cover is him and the glass
    # build() already set the 1080 x 1920 plate (paper edge painted out) the keys are measured on; a full-size plate here
    # put the glass on his forehead (first cover, 2026-11-20)
    world, _boxes = hp._world(shot, shot["hero_at"])
    world.convert("RGB").save(out)
    return "proj:assets/images/keyframes/cover-src.png"


def main():
    p = P / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep["publish"] = {
        # the title in the dark band above his head (his hair top at y ~0.36), the glass at his lips below it
        "cover": {"image": cover_source(), "title": "He Drank Cholera", "accent": ["CHOLERA"], "kicker": "MUNICH · 1892",
                  "textY": 300, "scale": 1.0, "x": 0, "y": 0},
        "hook_card": HOOK_CARD,
        "youtube": {
            "title": "He Drank Cholera to Prove His Rival Wrong", "description": DESCRIPTION, "sources": SOURCES,
            "tags": ["Max von Pettenkofer", "Pettenkofer cholera", "Robert Koch", "cholera 1892", "Hamburg cholera",
                     "self-experiment", "germ theory", "history of medicine", "Oddly Matt"],
            "hashtags": ["#history", "#medicalhistory", "#oddlymatt"],
            "pinned_comment": FIRST,
            "related_video": "The Doctor Who Drank Bacteria",
            "playlists": "Season Zero + Crazy Science",
            "schedule": "Tue Dec 1, 15:00 ET = 14:00 Alberta (socials Wed Dec 2, 18:00 ET = 17:00 Alberta)",
        },
        **{plat: {"caption": cap} for plat, cap in CAPTIONS.items()},
    }
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    if "--texts-only" in sys.argv:
        return
    subprocess.run([sys.executable, "episode.py", "publish", PID], cwd=SCRIPTS, check=True)


if __name__ == "__main__":
    main()
