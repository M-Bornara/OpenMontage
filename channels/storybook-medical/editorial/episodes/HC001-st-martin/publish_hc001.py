"""HC001 long video: the upload package -> projects/hc001-window-into-his-stomach/renders/deliverables-long/
(video, thumbnails A/B/C, captions.srt timed to the FINAL cut, publish.md, publish.json, CREDITS.txt).

The captions come from the cut's own word timings: the narration words shifted by the 4 s hook insert, the caption
spelling fixes (wordFix) and the inserted hook line. Chapters are the cut's chapter starts. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HC001-st-martin/publish_hc001.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from episode import DISCLOSURE, _write_srt, duration, studio_settings  # noqa: E402

PID = "hc001-window-into-his-stomach"
P = REPO / "projects" / PID
LAB = REPO / "projects/_fxlab"
# v5 (2026-10-27, user review of v4): clock 12 under the stem + forward, no burned-in captions (YouTube shows captions.srt),
# calm canoes on a keel-parallel waterline, stills for the AI-looking clips, wound blurred, no black frames at cuts
VIDEO = LAB / "renders/HC001-cut-v5.mp4"
OUT = P / "renders/deliverables-long"

TITLE = "The Man With a Window Into His Stomach"

# chapter starts in the final cut (beat starts + the 4 s hook insert); each is at least 10 s long
CHAPTERS = [
    ("00:00", "Lunch on a string"),
    ("00:34", "The case: Mackinac Island, 1822"),
    ("01:27", "What happened next"),
    ("02:05", "The science, 1825"),
    ("02:33", "The experiments"),
    ("04:01", "The human experiment"),
    ("05:56", "What they learned"),
    ("06:43", "Myth vs record: Matt's case file"),
    ("07:35", "The last word"),
    ("08:12", "Why it matters"),
]

DESCRIPTION = """In 1822, a musket went off by accident in a fur-trade store on Mackinac Island, and a young voyageur named Alexis St. Martin was shot in the side from less than a meter away. He survived, with an opening into his stomach that never closed.

Between 1825 and 1833, army surgeon William Beaumont used that opening for 238 experiments on digestion: food on a silk string, gastric juice in a vial, and a contract that bound Alexis to him as a servant. It changed what doctors knew about the stomach. It also leaves a question the record can't fully answer: what did Alexis want?"""

SOURCES = """SOURCES

Primary / archival:
- William Beaumont, Experiments and Observations on the Gastric Juice, and the Physiology of Digestion (Plattsburgh, 1833). https://archive.org/details/2543009R.nlm.nih.gov
- William Osler, "William Beaumont: A Backwoods Physiologist" (1902; quotes the 1833 contract, Alexis's letters, the 1852 letter and the parish account of his burial). https://archive.org/details/b31349092

Scholarly / institutional:
- Becker Medical Library, Washington University: "William Beaumont's momentous and unethical experiments". https://becker.wustl.edu/news/william-beaumonts-momentous-and-unethical-experiments/
- M. Raymond, Tangence 133 (2023), on how St. Martin was represented. https://erudit.org/en/revue/tce/2023/v/n133/1112235ar.html

Additional reading:
- A. Green, "Working Ethics: William Beaumont, Alexis St. Martin, and Medical Research in Antebellum America", Bulletin of the History of Medicine 84 (2010).
- Hektoen International, "William Beaumont and Alexis St. Martin" (2020). https://hekint.org/2020/02/06/william-beaumont-and-alexis-st-martin/"""

# sounds the final cut plays (beats + the brand sting); CC-BY ones are credited by name, CC0 counted
SFX_USED = ["buzzer-wrong", "ding-correct", "glass-clink", "hit-suspense", "paper-slide", "riser-drone", "stamp-thud",
            "tick-click", "watch-snap", "whoosh"]

TAGS = ["Alexis St. Martin", "William Beaumont", "history of medicine", "medical history", "digestion", "gastric juice",
        "Mackinac Island", "strange medical cases", "Oddly Matt"]
HASHTAGS = ["#history", "#medicalhistory", "#oddlymatt"]

PINNED = ("Matt lost his glasses somewhere in Beaumont's quarters. Did you spot them? "
          "(No timestamps in the replies, let others look.)")

# viewer-facing spellings for the caption file (the cut's burned-in captions already carry wordFix)
SPELL = {("Saint", "Lawrence"): "St.", ("Saint", "Louis"): "St."}


def words_final():
    props = json.load(open(LAB / "cut-props.json", encoding="utf-8"))
    pub = LAB / "remotion/public"
    words = json.load(open(pub / props["words"], encoding="utf-8"))
    beats = json.load(open(pub / props["beats"], encoding="utf-8"))["beats"]
    fix = props.get("wordFix", {})
    words = [{**w, "word": fix.get(str(i), w["word"])} for i, w in enumerate(words)]
    words = [w for w in words if w["word"]]
    for i in range(len(words) - 1):
        k = (words[i]["word"], words[i + 1]["word"].strip(",."))
        if k in SPELL:
            words[i]["word"] = SPELL[k]
    cut = next(b for b in beats if b["id"] == props["insertAfter"])["start"]
    ins = props["insertSecs"]
    shift = lambda t: t + ins if t >= cut else t
    out = [{**w, "start": shift(w["start"]), "end": shift(w["end"])} for w in words]
    # the inserted hook line plays 6 frames after the insert point (Animatic.tsx); its words spread over its length
    line = "…and why, for the rest of his life, he kept running away.".split()
    a, d = cut + 6 / 30, duration(pub / props["insertAudio"]) - 0.1
    step = d / len(line)
    hook = [{"word": t, "start": a + i * step, "end": a + (i + 1) * step - 0.02} for i, t in enumerate(line)]
    return sorted(out + hook, key=lambda w: w["start"])


def credits():
    lib = json.load(open(REPO / "channels/storybook-medical/library/sfx-credits.json", encoding="utf-8"))
    lines = ["CREDITS", "Music: original, generated with MiniMax Music v2.", "Narration: ElevenLabs v3 (voice: Liam).",
             "Illustrations and animation: AI-assisted, art-directed.", "",
             "Sound effects from Freesound.org:"]
    by = [lib[n] for n in SFX_USED if n in lib and "zero" not in lib[n]["license"]]
    for m in by:
        lic = "CC BY 3.0" if "/3.0" in m["license"] else "CC BY 4.0"
        lines.append(f'- "{m["title"]}" by {m["author"]} ({lic}) {m["url"]}')
    cc0 = sum(1 for n in SFX_USED if n in lib and "zero" in lib[n]["license"])
    lines.append(f"- plus {cc0} CC0 (public domain) sounds")
    return "\n".join(lines)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy(VIDEO, OUT / "HC001-L.mp4")
    for n in "ABC":
        shutil.copy(P / f"renders/thumbnails/thumb-{n}.jpg", OUT / f"thumb-{n}.jpg")
    _write_srt(words_final(), OUT / "captions.srt")
    cr = credits()
    (OUT / "CREDITS.txt").write_text(cr, encoding="utf-8")
    chapters = "CHAPTERS\n" + "\n".join(f"{t} {name}" for t, name in CHAPTERS)
    desc = "\n\n".join([DESCRIPTION, chapters, SOURCES, cr, DISCLOSURE, " ".join(HASHTAGS)])
    secs = duration(OUT / "HC001-L.mp4")
    md = [f"# {TITLE}", "", f"Length {int(secs // 60)}:{secs % 60:04.1f} · 1920×1080 · -14 LUFS · thumbnails A (main), B, C", "",
          "## YouTube (long video)", f"**Title:** {TITLE}", "", "**Description:**", "```", desc, "```", "",
          f"**Tags:** {', '.join(TAGS)}", "", f"**Pinned comment:** {PINNED}", "",
          "**Thumbnails:** upload `thumb-A.jpg`; Test & compare: add `thumb-B.jpg` and `thumb-C.jpg`.", "",
          *studio_settings("long", "Season Zero · Alexis St. Martin", schedule="Sun Nov 8, 9:00 MT (11:00 ET)"),
          "## Video elements", "", "| Element | Value |", "|---|---|",
          "| Subtitles | Upload file → With timing → `captions.srt` (no burned-in captions; this file is the only one) |",
          "| End screen | 8:35 to the end (12 s, the brand end screen). YouTube needs at least one video or playlist "
          "element, so Subscribe alone is refused. **Launch (Nov 8):** Subscribe (left, under STILL CURIOUS?) + "
          "Playlist \"Season Zero · Alexis St. Martin\" (right). **From Nov 9** (first Short live): replace the playlist "
          "with Video \"Most recent upload\" (top right) + \"Best for viewer\" (bottom right). **From HC002-L:** top box = "
          "that specific video. Editable any time, no re-upload. |",
          "| Cards | none yet (no other video to link). From cluster 2 on, one card where another case is mentioned. |",
          "| Quiz | skip for HC001 (new feature, no evidence yet that it helps; we can test it on a later video) |", "",
          "**Before scheduling:** rights.csv has 2 PENDING rows: save PDF copies of the fal.ai and Google generative-AI "
          "terms (images) and of the fal.ai / Kling terms (clips) into the episode folder."]
    (OUT / "publish.md").write_text("\n".join(md), encoding="utf-8")
    json.dump({"title": TITLE, "description": desc, "tags": TAGS, "pinned_comment": PINNED, "chapters": CHAPTERS,
               "thumbnails": {"main": "thumb-A.jpg", "test": ["thumb-B.jpg", "thumb-C.jpg"]}},
              open(OUT / "publish.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("deliverables ->", OUT)
    print(f"  description {len(desc)} chars (limit 5000)")


if __name__ == "__main__":
    main()
