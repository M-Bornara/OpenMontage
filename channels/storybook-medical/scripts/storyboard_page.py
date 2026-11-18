"""Visual storyboard page (user, 2026-11-14: "I cannot see the formatted md file ... more visuals before generation").

Reads each episode's storyboard .md (script block, shot table, sets/cast table, cost), puts the free pre-viz frame next
to every shot and the reference photos (portraits, period places) next to the cast, and writes one HTML page plus an
img/ folder, ready to publish as an Artifact. Run from the repo root:

    python channels/storybook-medical/scripts/storyboard_page.py <out_dir> <episode-key> [<episode-key> ...]

Episode keys are in EPISODES below; add a new episode there (storyboard, previz dir, refs with credits).
"""
from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[3]
EP = REPO / "channels/storybook-medical/editorial/episodes"

EPISODES = {
    "hcs07": {
        "anchor": "finlay", "short": "Finlay", "slot": "Thu Dec 3 · 15:00 ET = 14:00 Alberta",
        "storyboard": EP / "HCS07-finlay/storyboard-v2.md", "story": EP / "HCS07-finlay/story-v2.md", "project": REPO / "projects/hcs07-finlay",
        "previz": REPO / "projects/hcs07-finlay/review/previz", "maps": ["map-academy.png"],
        "refs_dir": REPO / "projects/hcs07-finlay/refs",
        "refs": [
            ("finlay.jpg", "Carlos Finlay", "Moustache into side whiskers, shaved chin, round spectacles.", "Photo, c. 1900s · Wikimedia Commons · public domain"),
            ("reed.jpg", "Walter Reed", "Moustache, dark-blue US Army uniform with shoulder cords.", "Photo, 1890s · Wikimedia Commons · public domain"),
            ("lazear.jpg", "Jesse Lazear", "Full trimmed beard, centre-parted hair.", "Photo, before 1900 · Wikimedia Commons · public domain"),
            ("havana_harbor_1860.jpg", "Havana harbour", "Morro Castle and lighthouse, busy harbour (shot 2a).", "Photo, c. 1860 · Wikimedia Commons · public domain"),
            ("havana_street_1880s.jpg", "A Havana house front", "Lime plaster, iron window grille (shot 2b).", "Photo, 1870s–80s · Wikimedia Commons · public domain"),
            ("academy_building.jpg", "The Academy building today", "Stone and scale only; the street front is a later remodel.", "Photo, 2026 · Wikimedia Commons · CC BY-SA 4.0"),
        ],
    },
    "hcs05": {
        "anchor": "al-razi", "short": "al-Razi", "slot": "Mon Dec 7 · 15:00 ET = 14:00 Alberta",
        "storyboard": EP / "HCS05-al-razi/storyboard-v2.md", "story": EP / "HCS05-al-razi/story-v2.md", "project": REPO / "projects/hcs05-al-razi",
        "previz": REPO / "projects/hcs05-al-razi/review/previz", "maps": ["map-ward.png"],
        "refs_dir": REPO / "projects/hcs05-al-razi/refs",
        "refs": [
            ("razi_1956.jpg", "Al-Razi, the look we follow", "White turban, full black beard, sand robe with a gold collar over a blue tunic.", "Painting for the 5th Iranian Medical Congress, 1956 · Wellcome Collection S0001954 · CC BY 4.0"),
            ("razi_behzad.jpg", "Al-Razi by Hossein Behzad", "For comparison only: old, white beard, an alchemist's flask.", "Miniature, 20th c. · Wikimedia Commons · public domain"),
            ("samanid_mausoleum.jpg", "Brick of his century", "Patterned baked brick and a plain dome: Rey and the ward.", "Samanid Mausoleum, Bukhara, c. 914–943 · Wikimedia Commons · public domain"),
            ("nain_stucco.jpg", "Carved stucco", "Wall decoration for the ward.", "Jameh Mosque of Nain, 10th c. · Wikimedia Commons · CC BY-SA 2.0"),
            ("quran_folio_950.jpg", "Handwriting of his time", "Angular cursive on paper: the look of his notebook pages (shot 7a).", "Quran folio, 950–1000 · The Met via Wikimedia Commons · public domain"),
        ],
    },
    "hc002s1": {
        "anchor": "gage-s1", "short": "Gage S1", "slot": "CASE 11 · Sun Nov 29 · 15:00 ET = 14:00 Alberta · ready by Wed Nov 25",
        "storyboard": EP / "HC002-phineas-gage/s1-storyboard-v1.md", "story": EP / "HC002-phineas-gage/s1-story-v2.md",
        "project": REPO / "projects/hc002-s1", "previz": REPO / "projects/hc002-s1/review/previz", "maps": [],
        "refs_dir": REPO / "projects/hc002-s1/refs",
        "refs": [
            ("gage_wilgus.jpg", "Phineas Gage (likeness only)", "Square face, clean-shaven, dark hair. Taken years after the accident: used for his face, never shown (it belongs to the long video's twist).", "Daguerreotype, 1850s · Wilgus collection via Wikimedia Commons · CC BY-SA 3.0"),
            ("gage_miller.jpg", "Phineas Gage, second portrait (likeness only)", "The same face from a second angle; not shown in S1.", "Photograph, 1850s · Wikimedia Commons · public domain"),
            ("tamping_iron.jpg", "The tamping iron", "Smooth, round, pointed at one end: not a crowbar (shots 1, 3, 5, 7, 11).", "Harlow 1868 · Wikimedia Commons · public domain"),
            ("harlow_skull_1868.jpg", "Harlow's skull drawing, 1868", "Shot 6: the bar's path draws itself on this engraving; no flesh anywhere.", "Harlow 1868, fig. 1 · Wikimedia Commons · public domain"),
            ("bigelow_1850_side.png", "Bigelow 1850, side view", "The path through the skull as the doctors drew it in 1850.", "Am J Med Sci 1850 · Wikimedia Commons · public domain"),
            ("cavendish_cut.jpg", "The rock cut at Cavendish today", "Grey rock walls of the cut (presumed site): the set of shots 1–5 and 8.", "Photo, 2009 · Wikimedia Commons · CC BY-SA 3.0"),
            ("ox_carts_1850s.jpg", "Ox carts, 1850s", "Wooden carts and oxen of the period (shot 9).", "Photo, 1850s, St. Anthony, Minnesota · DPLA via Wikimedia Commons · public domain"),
        ],
        "extra": [EP / "HC002-phineas-gage/script-long-v1.md", EP / "HCS10-pettenkofer/story-v1.md", EP / "HCS11-hilliard/story-v1.md",
                  EP / "HCS13-koepcke/story-v1.md", EP / "HCS12-ffirth/story-v1.md"],
        "page_title": "Slate Scripts for Approval",
        "status": "Gage S1 HERO motion pre-viz + all image prompts · waiting for your OK",
        "layered_title": "Gage S1: the three HERO shots, moving (free stand-ins)",
        "layered_lede": ("Shots 1, 4 and 8 run in the real renderer on drawn stand-ins: plates drawn here and simple cut-out figures. "
                         "Judge the MOTION and the timing, not the drawing: in shot 1 the bar leaves the dust above his hat, hangs and turns once in slow motion under the hook card, "
                         "then flies out top right while Gage falls back and his hat tumbles; in shot 4 his head turns on “shoulder”; in shot 8, in silence, "
                         "his fingers move and he props up on his elbow on “spoke”. The timing comes from a SCRATCH timeline (no narration yet): "
                         "every key is tied to a word, so the real narration re-times it. No sound yet (no narration or music). "
                         "The paid pieces below replace the stand-ins with the same names (Gemini Batch, <b>${tot}</b> for the sheets; the three plates are with the references)."),
        "plate_note": "a drawn stand-in plate, empty of what moves (Gage, the bar, the hat). The paid plate is painted in our style.",
        "story_kicker": "Story doctor · story v2 · 2026-11-18 · for approval",
        "v1_label": "v1 (S1 script, Oct 18)",
        "script_heading": "Script v2 (for approval; not recorded yet)",
        "h1": "Gage S1: the HERO motion pre-viz and the image prompts",
        "lede": "Round 2 for Gage S1 (CASE 11, Sun Nov 29). The storyboard is approved (2026-11-18). At the top: the three HERO shots moving in the real renderer on free stand-ins. Below them, every shot with its blocking sketch and, for the story stills, its image prompt (open “Image prompt”). The cast sheets, the set plate and the three HERO plates are in “Reference images made first”. All 21 prompts pass the prompt lint (0 findings). Below the Short: the approved long script and the four Short scripts, for reference. Tap any picture to enlarge it.",
        "ask": "<p><b>Gage S1:</b> OK the motion of shots 1, 4 and 8 (or tell me what to change: timing, how far he falls, how long the bar hangs) and the 21 image prompts. Also confirm hook card A, title 1 and the fiddle/banjo theme, which are still my recommendations. Cost after your OK: 21 images on Gemini Batch ≈ $1.41 (Google credit), narration ≈ $0.07 and music ≈ $0.13 on fal (balance $20.97); total ≈ $1.61, plus a retry margin. The reference photo of the cut (and three other Commons pictures) still has to be fetched: Wikimedia was blocking downloads on Nov 18.</p><p><b>Hilliard and Koepcke scripts:</b> your OK is still open (the cuts are in).</p>",
    },
}


def inline(md: str) -> str:
    t = html.escape(md.strip())
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


def table(lines: list[str], start_pat: str) -> list[list[str]]:
    """Rows of the first markdown table whose header line matches start_pat."""
    rows, on = [], False
    for ln in lines:
        if not on and ln.startswith("|") and re.search(start_pat, ln):
            on = True
            continue
        if on:
            if not ln.startswith("|"):
                break
            if re.match(r"^\|[-\s|]+\|$", ln):
                continue
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows


def parse(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = lines[0].lstrip("# ").split(" · ")[0]
    m = re.search(r"```\n(.*?)```", text, re.S)
    script = m.group(1).strip().splitlines() if m else []
    shots = table(lines, r"^\| # \|")
    cast = table(lines, r"^\| Who / where \|")
    notes, cur = [], None  # bold-led paragraphs (Care, Period, Theme...), joined across wrapped lines
    for ln in lines:
        if ln.startswith("**") and not ln.startswith("**Total"):
            if cur:
                notes.append(cur)
            cur = ln
        elif cur and ln.strip() and not ln.startswith(("|", "#", "```")):
            cur += " " + ln.strip()
        else:
            if cur:
                notes.append(cur)
            cur = None
    if cur:
        notes.append(cur)
    notes = [n for n in notes if not n.startswith(("**Loop", "**Decoupage"))][:7]
    cost = re.search(r"\*\*Total ≈ (\$[\d.]+)\.\*\*", text)
    secs = sum(float(r[1]) for r in shots if re.match(r"^[\d.]+$", r[1]))
    return {"title": title, "script": script, "shots": shots, "cast": cast, "notes": notes,
            "cost": cost.group(1) if cost else "", "secs": secs}


def tension_svg(beats: list[tuple[str, int, int]], v1_label: str = "v1 (rough cut 1)") -> str:
    """v1 vs v2 tension per beat (editorial rating 0-10). Two series: legend + direct labels; native hover titles."""
    W, H, L, R, T, B = 640, 250, 34, 44, 14, 46
    n = len(beats)
    x = lambda i: L + (W - L - R) * (i / max(1, n - 1))  # noqa: E731
    y = lambda v: T + (H - T - B) * (1 - v / 10)  # noqa: E731
    grid = "".join(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="g"/>'
                   f'<text x="{L - 8}" y="{y(v) + 4:.1f}" class="ax" text-anchor="end">{v}</text>' for v in (0, 5, 10))
    ticks = "".join(f'<text x="{x(i):.1f}" y="{H - B + 18}" class="ax" text-anchor="middle">{html.escape(b[0])}</text>'
                    for i, b in enumerate(beats))
    out = []
    for key, idx, label in (("v1", 1, v1_label), ("v2", 2, "v2 (proposed)")):
        pts = " ".join(f"{x(i):.1f},{y(b[idx]):.1f}" for i, b in enumerate(beats))
        dots = "".join(f'<circle cx="{x(i):.1f}" cy="{y(b[idx]):.1f}" r="4.5" class="d {key}"><title>{label} · {html.escape(b[0])}: '
                       f'{b[idx]}/10</title></circle>' for i, b in enumerate(beats))
        last = beats[-1][idx]
        out.append(f'<polyline points="{pts}" class="l {key}"/>{dots}'
                   f'<text x="{x(n - 1) + 8:.1f}" y="{y(last) + 4:.1f}" class="lab">{key}</text>')
    return (f'<svg viewBox="0 0 {W} {H}" class="tension" role="img" aria-label="Tension per beat, v1 versus v2">{grid}{ticks}'
            f'{"".join(out)}</svg>')


def story_block(k: str, e: dict, img: Path) -> str:
    """Round 2 (user 2026-11-15, 'the rhythm is flat'): story-v2.md from the story-doctor skill, for approval."""
    f = e.get("story")
    if not f or not f.exists():
        return ""
    lines = f.read_text(encoding="utf-8").splitlines()
    def para(prefix: str) -> str:  # a paragraph that wraps over several md lines
        out = None
        for ln in lines:
            if out is None and ln.startswith(prefix):
                out = ln
            elif out is not None:
                if not ln.strip() or ln.startswith(("|", "#", "- ")):
                    break
                out += " " + ln.strip()
        return out or ""
    why = para("Why:")
    spine = [ln[2:] for ln in lines if ln.startswith("- **")]
    beats = table(lines, r"^\| Beat \| Line")
    shots = table(lines, r"^\| # \| Beat")
    rhythm = table(lines, r"^\| Beat \| Cuts")
    score = table(lines, r"^\| \| Hook")
    cost = next((ln for ln in lines if "**≈ $" in ln), "")
    changed = para("**Changed from v1")
    kf_dir = e["project"] / "assets/images/keyframes"
    pts, rows = [], []
    for b in beats:
        m = re.match(r"(\d+)\s*→\s*(\d+)", b[3])
        name = b[0].split()[0]
        if m:
            pts.append((name, int(m.group(1)), int(m.group(2))))
        tags = re.match(r"^((?:\[[^\]]+\]\s*)*)(.*)$", b[1])
        tg = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in re.findall(r"\[[^\]]+\]", tags.group(1)))
        body = re.sub(r"\[(pause|beat)\]", r'<span class="tag">[\1]</span>', inline(tags.group(2)))
        rows.append(f'<tr><td><span class="beat">{html.escape(b[0])}</span></td><td>{tg}{body}</td>'
                    f'<td class="tn">{html.escape(b[3])}</td></tr>')
    # merge repeated beat names so the chart has one point per beat (the highest v2 inside it)
    merged: dict[str, tuple[str, int, int]] = {}
    for nme, a, b2 in pts:
        merged[nme] = (nme, max(a, merged.get(nme, (0, 0, 0))[1]), max(b2, merged.get(nme, (0, 0, 0))[2]))
    cards = []
    for r in shots:
        n, beat, act, status = (r + [""] * 4)[:4]
        sid = n.split(",")[0].strip().strip("~")  # "9a, 9b" / "~~5~~, ~~9a~~": the first shot's picture
        st = re.search(r"\*\*(KEEP|REDO|NEW|DROP)\*\*|^(KEEP|DROP)", status)
        kind = (st.group(1) or st.group(2)) if st else "KEEP"
        kf = kf_dir / f"s{sid}.png"
        pic = (f'<img src="img/{shrink(kf, img / f"{k}-v2-{sid}", 600)}" alt="Current image, shot {html.escape(sid)}" loading="lazy">'
               if kf.exists() and not sid.startswith("N") else '<div class="newpic">new image</div>')
        cards.append(f'<article class="v2 {kind.lower()}">{pic}<div><div class="head"><span class="num">{html.escape(n.replace("~", ""))}</span>'
                     f'<span class="st {kind.lower()}">{kind}</span><span class="size">{inline(beat)}</span></div>'
                     f'<p>{inline(act)}</p><p class="muted">{inline(status)}</p></div></article>')
    rh = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rhythm)
    sc = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in score)
    return f"""
  <div class="block story"><div class="kicker">{html.escape(e.get("story_kicker", "Round 2 · story v2 · approved 2026-11-15"))}</div>
  <p class="lede">{inline(why.removeprefix('Why: '))}</p>
  <h3>The tension curve (editorial rating per beat)</h3>
  <div class="chart"><div class="key"><span><i class="sw v1"></i>{html.escape(e.get("v1_label", "v1, rough cut 1"))}</span><span><i class="sw v2"></i>v2, proposed</span></div>
  {tension_svg(list(merged.values()), e.get("v1_label", "v1 (rough cut 1)"))}</div>
  <h3>Spine</h3><ul class="spine">{''.join(f'<li>{inline(s)}</li>' for s in spine)}</ul>
  <h3>Script v2, beat by beat</h3><div class="cast"><table><tr><th>Beat</th><th>Line (Liam)</th><th>Tension v1 → v2</th></tr>{''.join(rows)}</table></div>
  <div class="notes"><p>{inline(changed)}</p></div>
  <h3>Shots: keep, fix, redo, new (every shot has an action)</h3><div class="v2grid">{''.join(cards)}</div>
  <h3>Rhythm map (the edit plan)</h3><div class="cast"><table><tr><th>Beat</th><th>Cuts</th><th>Camera</th><th>Music</th><th>Hero sound</th></tr>{rh}</table></div>
  <h3>Score</h3><div class="cast"><table><tr><th></th><th>Hook</th><th>Stakes</th><th>Turns</th><th>Climax</th><th>Payoff</th><th>Action</th><th>Rhythm</th><th>Avg</th></tr>{sc}</table></div>
  <p class="meta">{inline(cost)}</p></div>"""


PROMPT_KEYS = r"(SET:|GEOGRAPHY:|SHOT:|CAMERA:|BACKGROUND \(exactly this, nothing else\):|CAST:|CROWD:|FRAMING:|Hidden detail|Small background cameo of MATT)"


def prompt_html(spec: dict) -> str:
    """One image spec -> readable blocks: which references go in, then the prompt split at its labelled parts."""
    parts = re.split(PROMPT_KEYS, spec.get("prompt", ""))
    out, cur = [], parts[0].strip()
    if cur:
        out.append(cur)
    for i in range(1, len(parts), 2):
        out.append(parts[i] + parts[i + 1])
    refs = ", ".join(r.split(":", 1)[-1].split("/")[-1] for r in spec.get("refs", []))
    meta = f"{spec.get('aspect', '9:16')} · {spec.get('resolution', '2K')} · references: {refs or 'none'}"
    roles = f'<p class="roles">{inline(spec["roles"])}</p>' if spec.get("roles") else ""
    return (f'<details class="prompt"><summary>Image prompt</summary><p class="pmeta">{html.escape(meta)}</p>{roles}'
            + "".join(f"<p>{inline(x)}</p>" for x in out) + "</details>")


def md_section(f: Path) -> str:
    """A markdown file (headings, paragraphs, bullet lists, tables) as one page block: the long script on the S1 page."""
    out, para, tbl, lst = [], [], [], []
    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>"); para.clear()
        if lst:
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in lst) + "</ul>"); lst.clear()
        if tbl:
            rows = [r for r in tbl if not re.match(r"^\|[-\s|]+\|$", r)]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells[0])
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in cells[1:])
            out.append(f'<div class="cast"><table><tr>{head}</tr>{body}</table></div>'); tbl.clear()
    lines = f.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ")
    for ln in lines[1:]:
        if ln.startswith("|"):
            if para or lst:
                flush()
            tbl.append(ln); continue
        if tbl:
            flush()
        if ln.startswith("#"):
            flush(); out.append(f"<h3>{inline(ln.lstrip('# '))}</h3>")
        elif re.match(r"^\s*- ", ln):
            if para:
                flush()
            lst.append(ln.strip()[2:])
        elif re.match(r"^\s{2,}\S", ln) and lst:
            lst[-1] += " " + ln.strip()
        elif not ln.strip() or ln.strip() == "---":
            flush()
        else:
            if lst:
                flush()
            para.append(ln.strip())
    flush()
    return f'<div class="block mdsec"><div class="kicker">for approval</div><h2>{inline(title)}</h2>{"".join(out)}</div>'


def episode_json(e: dict) -> dict:
    import json
    f = e.get("project") and e["project"] / "episode.json"
    return json.load(open(f, encoding="utf-8")) if f and f.exists() else {}


def image_cost(ep: dict) -> tuple[int, float]:
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import google_images as g
    except Exception:
        return 0, 0.0
    n, tot = 0, 0.0
    for sec in ("references", "keyframes"):
        for spec in ep.get(sec, {}).values():
            n += 1
            tot += g.price(spec.get("model", "gemini-3-pro-image"), spec.get("resolution", ep.get("image_resolution", "2K")), True)
    return n, tot


def web_preview(render: Path, dst: Path) -> bool:
    """A light 540x960 copy of the rough cut for the page (an Artifact file must stay under 15 MB)."""
    import subprocess
    if not render.exists():
        return False
    if not dst.exists() or dst.stat().st_mtime < render.stat().st_mtime:
        dst.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(render), "-vf", "scale=540:960", "-c:v", "libx264",
                        "-preset", "slow", "-crf", "26", "-maxrate", "1500k", "-bufsize", "3000k", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(dst)], check=True)
    return True


def layered_block(k: str, e: dict, ep: dict, out: Path, img: Path) -> str:
    """Layered shots (user 2026-11-16, .claude/skills/layered-shot): per shot the 3 s preview with sound, the contact
    sheet, the layer plan, the free stand-in pieces and the prompts of the paid pieces (waiting for the user's OK)."""
    sys.path.insert(0, str(Path(__file__).parent))
    import layers
    p = e.get("project")
    if not p:
        return ""
    arts = []
    for s in ep.get("shots", []):
        if not s.get("layers"):
            continue
        sid = s["id"]
        rev = p / "review/layers"
        vid = ""
        if web_preview(rev / f"{sid}-preview.mp4", out / "video" / f"{p.name}-{sid}-layers.mp4"):
            vid = (f'<video class="cut" controls playsinline loop preload="metadata" '
                   f'src="video/{p.name}-{sid}-layers.mp4"></video>')
        sheet = ""
        if (rev / f"{sid}-sheet.jpg").exists():
            sheet = (f'<img class="wide" src="img/{shrink(rev / f"{sid}-sheet.jpg", img / f"{k}-{sid}-layersheet", 1500)}" '
                     f'alt="Start, middle and end frames of the layered shot" loading="lazy">')
        plan = "".join(f"<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>"
                       for a, b, c in layers.layer_plan(s))
        stand = []
        bg = (s["layers"].get("bg") or "")
        if bg:
            f = Path(p / bg.split(":", 1)[-1]) if bg.startswith("proj:") else Path(bg)
            if f.exists():
                cap = ('<b>Plate (free stand-in)</b><span>' + html.escape(f.name) + ': ' + html.escape(e.get("plate_note",
                       "the mosquito painted out locally. The paid plate repaints it cleanly.")) + '</span>') if ".free" in f.name else (
                      '<b>Plate (real, $0.067)</b><span>The same painting repainted without the mosquito; it lines up with '
                      'the still within 1.5 px, so the landing spot holds.</span>')
                stand.append(f'<figure><img src="img/{shrink(f, img / f"{k}-{sid}-plate", 900)}" alt="Plate without the mosquito" loading="lazy">'
                             f'<figcaption>{cap}</figcaption></figure>')
        for a in s["layers"].get("actors", []):
            sp = a.get("sprites", "")
            f = (p / sp.split(":", 1)[-1]).parent / "check.png" if sp.startswith("proj:") else None
            if f and f.exists():
                stand.append(f'<figure><img src="img/{shrink(f, img / f"{k}-{sid}-{a["id"]}-check", 1300)}" alt="Cut-outs over magenta" loading="lazy">'
                             + (f'<figcaption><b>{html.escape(a["id"])}: cut-outs (free stand-in)</b><span>Every state over '
                                f'magenta, and the onion skin: one body outline means it doesn’t jump when the wings fold.</span>'
                                if "free" in sp else
                                f'<figcaption><b>{html.escape(a["id"])}: real cut-outs ($0.067 sheet)</b><span>Wing beat (2 frames), '
                                f'the fold (2 frames), at rest. The sheet gave 2 top-down frames and 2 side views; the side views '
                                f'don’t match a camera looking down at the hand, so the beat and the fold are made from the '
                                f'top-down frame by turning each wing at its root.</span>')
                             + '</figcaption></figure>')
        arts.append(f'<article class="layered"><div class="head"><span class="num">{html.escape(Path(str(s["source"])).stem)}</span>'
                    f'<span class="chip">{s["end"] - s["start"]:.1f} s</span><span class="size">{html.escape(sid)} · layered</span></div>'
                    f'<div class="lgrid">{vid}<div class="cast"><table><tr><th>Layer</th><th>What</th><th>Motion</th></tr>{plan}</table></div></div>'
                    f'{sheet}<div class="refs">{"".join(stand)}</div></article>')
    if not arts:
        return ""
    pieces = []
    tot = 0.0
    try:
        import google_images as g
    except Exception:
        g = None
    for rn, spec in ep.get("references", {}).items():
        if "for cut-out animation" not in spec.get("prompt", "").lower():
            continue
        made = (p / "assets/images/refs" / f"{rn}.png").exists()
        usd = g.price(spec.get("model", "gemini-3-pro-image"), spec.get("resolution", ep.get("image_resolution", "2K")), True) if g else 0
        tot += 0 if made else usd
        pieces.append(f'<article><b>{html.escape(rn)}</b><span class="st {"" if made else "new"}">'
                      f'{"made" if made else f"waiting for your OK · ${usd:.3f}"}</span>'
                      f'{prompt_html(spec).replace("<details", "<details open", 1)}</article>')
    if tot == 0 and pieces:
        return (f'<div class="block"><h3>Layered shots: our own animation (pilot)</h3>'
                f'<p class="lede">The preview now runs on the <b>real pieces</b> (made 2026-11-16, $0.134): the plate without the '
                f'mosquito and the cut-out mosquito, warmed to the lamp’s light. Same motion you approved.</p>'
                f'{"".join(arts)}'
                f'<details><summary>The two prompts</summary><div class="refgen">{"".join(pieces)}</div></details></div>')
    if e.get("layered_lede"):
        return (f'<div class="block"><h3>{html.escape(e.get("layered_title", "Layered shots"))}</h3>'
                f'<p class="lede">{e["layered_lede"].replace("{tot}", f"{tot:.2f}")}</p>{"".join(arts)}'
                f'<h3>The paid pieces (prompts)</h3><div class="refgen">{"".join(pieces)}</div></div>')
    return (f'<div class="block"><h3>Layered shots: our own animation (pilot)</h3>'
            f'<p class="lede">The preview runs on free stand-ins: the plate with the mosquito painted out on this machine, '
            f'and a drawn mosquito. It shows the MOTION: the path, the landing on “suspect”, the wings folding, the shadow on the skin, '
            f'the buzz stopping. The paid pieces below replace the stand-ins (Gemini Batch, <b>${tot:.2f}</b> together).</p>'
            f'{"".join(arts)}'
            f'<h3>The two paid pieces (prompts)</h3><div class="refgen">{"".join(pieces)}</div></div>')


def shrink(src: Path, dst: Path, edge: int = 900):
    im = Image.open(src).convert("RGB")
    im.thumbnail((edge, edge))
    im.save(dst.with_suffix(".jpg"), quality=82)
    return dst.with_suffix(".jpg").name


CSS = """
:root{--bg:#f3eee3;--surface:#fbf8f1;--ink:#22262a;--muted:#5d625f;--line:#d9cfbd;--amber:#b8740f;--amber-soft:#f4dfb6;--teal:#1f4e5a;--teal-soft:#d5e4e4;--s1:#2f6fc0;--s2:#c07a12;
--display:'Montserrat',system-ui,sans-serif;--body:'Inter',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1a1d20;--surface:#23282c;--ink:#efe6d2;--muted:#a9a99f;--line:#3a4044;--amber:#e8a33d;--amber-soft:#4a3a1e;--teal:#8cc0c4;--teal-soft:#1f3a40;--s1:#4a86d0;--s2:#b9781a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1a1d20;--surface:#23282c;--ink:#efe6d2;--muted:#a9a99f;--line:#3a4044;--amber:#e8a33d;--amber-soft:#4a3a1e;--teal:#8cc0c4;--teal-soft:#1f3a40;--s1:#4a86d0;--s2:#b9781a;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:15px;line-height:1.55}
.wrap{max-width:1180px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
h1,h2,h3{font-family:var(--display);font-weight:800;letter-spacing:-.01em;text-wrap:balance;margin:0}
h1{font-size:clamp(26px,4vw,38px)} h2{font-size:clamp(22px,3vw,30px)} h3{font-size:13px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);font-weight:700}
.kicker{font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--amber)}
.lede{color:var(--muted);max-width:68ch;margin:10px 0 0}
nav{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 8px}
nav a{font-family:var(--display);font-weight:700;font-size:13px;padding:8px 14px;border-radius:999px;background:var(--surface);border:1px solid var(--line);color:var(--ink);text-decoration:none}
nav a:hover,nav a:focus-visible{border-color:var(--amber);outline:none}
section.ep{margin-top:44px;padding-top:12px;border-top:3px solid var(--ink)}
.meta{display:flex;flex-wrap:wrap;gap:6px 18px;margin:10px 0 0;color:var(--muted);font-size:14px;font-variant-numeric:tabular-nums}
.meta b{color:var(--ink)}
.block{margin-top:28px;display:grid;gap:12px;grid-template-columns:minmax(0,1fr)}
.notes{background:var(--teal-soft);border-radius:10px;padding:14px 18px;display:grid;gap:8px;font-size:14px}
.notes p{margin:0}
.script{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:16px 18px;display:grid;gap:6px;font-size:15px}
.script p{margin:0}.tag{font-family:var(--mono);font-size:12px;color:var(--teal);margin-right:6px}
.refs{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
figure img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top;display:block;cursor:zoom-in;background:var(--line)}
figcaption{padding:10px 12px;display:grid;gap:4px;font-size:13px;min-width:0}
figcaption b{font-family:var(--display);font-size:14px}
.credit{color:var(--muted);font-size:11.5px}
.cast{overflow-x:auto}
.cast table{border-collapse:collapse;width:100%;font-size:13.5px;min-width:560px}
.cast td,.cast th{border-bottom:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
.cast th{font-family:var(--display);font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
.maps{display:flex;flex-wrap:wrap;gap:14px}.maps img{max-width:min(420px,100%);border-radius:10px;border:1px solid var(--line);cursor:zoom-in}
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,520px),1fr));gap:16px}
.shot{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;grid-template-columns:150px 1fr;gap:14px;align-items:start}
.shot img{width:150px;aspect-ratio:9/16;border-radius:6px;display:block;cursor:zoom-in;border:1px solid var(--line)}
.shot .info{min-width:0;display:grid;gap:8px}
.head{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.num{font-family:var(--display);font-weight:800;font-size:22px}
.chip{font-family:var(--mono);font-size:12px;background:var(--amber-soft);color:var(--ink);padding:2px 8px;border-radius:999px;font-variant-numeric:tabular-nums}
.size{font-family:var(--mono);font-size:12px;color:var(--teal)}
.line{font-size:15.5px;margin:0}.line strong{color:var(--amber)}
.shot dl{margin:0;display:grid;grid-template-columns:62px 1fr;gap:4px 10px;font-size:13.5px}
.shot dt{font-family:var(--display);font-weight:700;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);padding-top:2px}
.shot dd{margin:0;min-width:0}
.legend{font-size:13px;color:var(--muted)}
.legend span{display:inline-block;width:26px;height:10px;background:var(--amber-soft);border:1px solid var(--amber);vertical-align:middle;margin-right:6px;border-radius:2px}
.ask{margin-top:48px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:18px 20px;display:grid;gap:6px}
.ask p{margin:0}
details.prompt{border-top:1px dashed var(--line);padding-top:8px;font-size:13px}
details.prompt summary{cursor:pointer;font-family:var(--display);font-weight:700;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--teal)}
details.prompt p{margin:6px 0 0;overflow-wrap:anywhere}.pmeta{font-family:var(--mono);font-size:11.5px;color:var(--muted)}
.roles{color:var(--muted);font-style:italic}
.pics{display:grid;gap:6px;justify-items:start}.pics small{font-family:var(--mono);font-size:11px;color:var(--muted)}
.refgen{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,340px),1fr));gap:14px}
.refgen article{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:grid;gap:6px;min-width:0}
.refgen b{font-family:var(--display)}
video.cut{width:min(360px,100%);aspect-ratio:9/16;border-radius:12px;background:#000;display:block}
.story{background:var(--surface);border:2px solid var(--amber);border-radius:14px;padding:18px 20px}
.story h3{margin-top:10px}
.chart{display:grid;gap:6px}.key{display:flex;gap:16px;font-size:13px;color:var(--muted)}
.sw{display:inline-block;width:18px;height:3px;border-radius:2px;vertical-align:middle;margin-right:6px}
.sw.v1{background:var(--s1)}.sw.v2{background:var(--s2)}
svg.tension{width:100%;max-width:680px;height:auto}
svg.tension .g{stroke:var(--line);stroke-width:1}svg.tension .ax{fill:var(--muted);font:11px var(--mono)}
svg.tension .l{fill:none;stroke-width:2;stroke-linejoin:round}svg.tension .l.v1{stroke:var(--s1)}svg.tension .l.v2{stroke:var(--s2)}
svg.tension .d{stroke:var(--surface);stroke-width:2}svg.tension .d.v1{fill:var(--s1)}svg.tension .d.v2{fill:var(--s2)}
svg.tension .lab{fill:var(--ink);font:700 12px var(--display)}
.spine{margin:0;padding-left:18px;display:grid;gap:3px;font-size:14px}
.beat{font-family:var(--mono);font-size:12px;white-space:nowrap}.tn{font-family:var(--mono);white-space:nowrap}
.v2grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,330px),1fr));gap:12px}
.v2grid article{display:grid;grid-template-columns:84px 1fr;gap:12px;border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--bg);font-size:13.5px}
.v2grid article p{margin:4px 0 0}.v2grid .muted{color:var(--muted);font-size:12.5px}
.v2grid img,.newpic{width:84px;aspect-ratio:9/16;border-radius:6px;object-fit:cover;cursor:zoom-in}
.newpic{display:grid;place-items:center;border:2px dashed var(--amber);color:var(--amber);font:700 11px var(--display);text-align:center}
.v2grid article.drop{opacity:.55}
.st{font:700 11px var(--display);letter-spacing:.06em;padding:2px 8px;border-radius:999px;background:var(--line)}
.st.redo,.st.new{background:var(--amber-soft);color:var(--ink)}
.layered{background:var(--surface);border:2px solid var(--teal);border-radius:14px;padding:14px;display:grid;gap:14px;margin-top:12px}
.lgrid{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:16px;align-items:start}
img.wide{width:100%;height:auto;border-radius:8px;border:1px solid var(--line);cursor:zoom-in}
.layered figure img{aspect-ratio:auto;object-fit:contain;background:var(--bg)}
.layered .refs{grid-template-columns:minmax(0,220px) minmax(0,1fr)}
.refgen .st{justify-self:start}
@media (max-width:640px){.layered .refs{grid-template-columns:minmax(0,1fr)}}
@media (max-width:640px){.lgrid{grid-template-columns:minmax(0,1fr)}}
#lb{position:fixed;inset:0;background:rgba(10,12,14,.88);display:flex;align-items:center;justify-content:center;padding:24px;z-index:20;cursor:zoom-out}
#lb[hidden]{display:none}
#lb img{max-width:100%;max-height:100%;border-radius:6px}
@media (max-width:560px){.shot{grid-template-columns:110px 1fr}.shot img{width:110px}.shot dl{grid-template-columns:1fr}.shot dt{padding-top:6px}}
@media (prefers-reduced-motion:no-preference){nav a{transition:border-color .15s}}
"""


def build(out: Path, keys: list[str]) -> Path:
    img = out / "img"
    img.mkdir(parents=True, exist_ok=True)
    eps = [(k, EPISODES[k], parse(EPISODES[k]["storyboard"])) for k in keys]
    nav = "".join(f'<a href="#{e["anchor"]}">{html.escape(p["title"].split(" — ")[0])} · {e["short"]}</a>' for k, e, p in eps)
    body = []
    stages = []
    pilots: list[str] = []
    for k, e, p in eps:
        ep = episode_json(e)
        kf_dir = e.get("project", Path("-")) / "assets/images/keyframes"
        ref_dir = e.get("project", Path("-")) / "assets/images/refs"
        has_imgs = any((kf_dir / f"{n}.png").exists() for n in ep.get("keyframes", {}))
        stage = ("images · waiting for your OK" if has_imgs else
                 "image prompts · waiting for your OK" if ep.get("previz_approved") and ep.get("keyframes") else
                 "storyboard + pre-viz · waiting for your OK")
        stages.append(stage)
        n_img, img_usd = image_cost(ep)
        vid = ""
        if e.get("project") and web_preview(e["project"] / "renders/final.mp4", out / "video" / f"{e['project'].name}.mp4"):
            vid = (f'<div class="block"><h3>Rough cut (watch with sound)</h3><video class="cut" controls playsinline '
                   f'preload="metadata" src="video/{e["project"].name}.mp4"></video></div>')
            if not e.get("story"):
                stage = "rough cut · waiting for your OK"
                stages[-1] = stage
        story = story_block(k, e, img)
        layered = layered_block(k, e, ep, out, img)
        if layered:
            pilots.append(e["short"])
        if story:
            stage = stages[-1] = ("rough cut 2 · waiting for your OK" if all((kf_dir / f"{n}.png").exists() for n in ep.get("keyframes", {}))
                                  else "v2 sketches + prompts · waiting for your OK")
        if layered:
            stage = stages[-1] = "layered pilot · real pieces · waiting for your OK"
        if e.get("status"):
            stage = stages[-1] = e["status"]
        # reference images to make (cast sheets, set plates) with their prompts
        refgen = []
        for rn, spec in ep.get("references", {}).items():
            done = ref_dir / f"{rn}.png"
            pic = ""
            if done.exists():
                pic = f'<img src="img/{shrink(done, img / f"{k}-gen-{rn}", 1100)}" alt="{html.escape(rn)}" loading="lazy">'
            refgen.append(f'<article><b>{html.escape(rn)}</b>{pic}{prompt_html(spec).replace("<details", "<details open", 0)}</article>')
        # script
        sc = []
        for ln in p["script"]:
            m = re.match(r"^\[(\w+)\]\s*(.*)$", ln)
            sc.append(f'<p><span class="tag">[{m.group(1)}]</span>{inline(m.group(2))}</p>' if m else f"<p>{inline(ln)}</p>")
        # refs
        figs = []
        for fn, name, note, credit in e["refs"]:
            src = e["refs_dir"] / fn
            if not src.exists():
                continue
            local = shrink(src, img / f"{k}-ref-{Path(fn).stem}")
            figs.append(f'<figure><img src="img/{local}" alt="{html.escape(name)}" loading="lazy">'
                        f'<figcaption><b>{html.escape(name)}</b><span>{html.escape(note)}</span>'
                        f'<span class="credit">{html.escape(credit)}</span></figcaption></figure>')
        maps = []
        for mp in e["maps"]:
            if (e["previz"] / mp).exists():
                local = shrink(e["previz"] / mp, img / f"{k}-{Path(mp).stem}", 1100)
                maps.append(f'<img src="img/{local}" alt="Set map: camera positions" loading="lazy">')
        cast = "".join(f"<tr><td>{inline(r[0])}</td><td>{inline(r[1])}</td><td>{inline(r[2])}</td></tr>"
                       for r in p["cast"] if len(r) >= 3)
        cards = []
        for r in p["shots"]:
            if len(r) < 8:
                continue
            n, s, line, size, see, fx, txt, sfx = r[:8]
            fr = e["previz"] / f"{n}.png"
            pics = []
            if fr.exists():
                shutil.copy(fr, img / f"{k}-{n}.png")
                pics.append(f'<img src="img/{k}-{n}.png" alt="Pre-viz sketch, shot {html.escape(n)}" loading="lazy"><small>sketch</small>')
            kf = kf_dir / f"s{n}.png"
            redo = "**REDO**" in see
            if kf.exists():
                pics.append(f'<img src="img/{shrink(kf, img / f"{k}-kf-{n}", 900)}" alt="Image, shot {html.escape(n)}" loading="lazy">'
                            f'<small>{"rough cut 1 image: being REDONE" if redo else "image"}</small>')
            elif "**NEW**" in see:
                pics.append('<small>new image: after your OK</small>')
            pic = f'<div class="pics">{"".join(pics)}</div>'
            spec = ep.get("keyframes", {}).get(f"s{n}")
            ptxt = prompt_html(spec) if spec else ""
            cards.append(
                f'<article class="shot">{pic}<div class="info"><div class="head"><span class="num">{html.escape(n)}</span>'
                f'<span class="chip">{html.escape(s)} s</span><span class="size">{inline(size)}</span></div>'
                f'<p class="line">“{inline(line)}”</p><dl><dt>We see</dt><dd>{inline(see)}</dd>'
                f'<dt>Motion</dt><dd>{inline(fx)}</dd><dt>Text</dt><dd>{inline(txt)}</dd>'
                f'<dt>Sound</dt><dd>{inline(sfx)}</dd></dl>{ptxt}</div></article>')
        notes = "".join(f"<p>{inline(n)}</p>" for n in p["notes"])
        body.append(f"""
<section class="ep" id="{e['anchor']}">
  <div class="kicker">{html.escape(k.upper())} · {html.escape(e['slot'])}</div>
  <h2>{html.escape(p['title'].split(' — ', 1)[-1])}</h2>
  <div class="meta"><span><b>{len(cards)}</b> shots</span><span>≈ <b>{p['secs']:.0f} s</b> of pictures</span>
  <span>{f"images <b>{n_img}</b> · <b>${img_usd:.2f}</b> (Gemini Batch) + narration and music ≈ <b>$0.13</b>" if n_img else f"estimate <b>{html.escape(p['cost'])}</b>"}</span>
  <span>status <b>{html.escape(stage)}</b></span></div>
  {layered}
  {story}
  {vid}
  <div class="block"><h3>Notes and period rules</h3><div class="notes">{notes}</div></div>
  <div class="block"><h3>{html.escape(e.get("script_heading", "Script v2 (approved, recorded)"))}</h3><div class="script">{''.join(sc)}</div></div>
  <div class="block"><h3>People and places: the real pictures we follow</h3><div class="refs">{''.join(figs)}</div></div>
  <div class="block"><h3>Cast and sets</h3><div class="cast"><table><tr><th>Who / where</th><th>Look</th><th>Shots</th></tr>{cast}</table></div></div>
  <div class="block"><h3>Set map (where each camera stands)</h3><div class="maps">{''.join(maps)}</div></div>
  {f'<div class="block"><h3>Reference images made first (cast sheets and empty sets)</h3><div class="refgen">{"".join(refgen)}</div></div>' if refgen else ''}
  <div class="block"><h3>Shots</h3><p class="legend"><span></span>orange band = where the on-screen text sits · dotted lines = the Shorts safe zone</p>
  <div class="shots">{''.join(cards)}</div></div>
  {"".join(md_section(f) for f in e.get("extra", []))}
</section>""")
    first = eps[0][1]
    if first.get("h1"):
        h1, lede, ask = first["h1"], first["lede"], first["ask"]
    elif pilots:
        h1 = "Layered animation pilot: Finlay’s mosquito"
        lede = ("Our own animation instead of AI clips: the painting becomes layers (a clean plate, a mosquito cut out in four "
                "states, a shadow, the lamp’s glow) and we move them with keyframes, like After Effects. Watch the 3 s preview "
                "with sound at the top of Finlay. Both Shorts’ storyboards stay below for reference. Tap any picture to enlarge it.")
        ask = ("<p><b>The real mosquito</b> (the preview at the top of Finlay): the same motion you approved, now with the "
               "real plate and the real mosquito. Check the wing beat in flight, the landing on “suspect”, the wings folding "
               "and that it sits on the skin, not on top of the picture.</p>"
               "<p>After your OK: the full Finlay render, the text check, and a new short.mp4 in the package.</p>")
    else:
        h1 = "Next two Shorts: rough cut 2"
        lede = ("Round 2 (after your rough-cut review): each Short now starts with the proposed story v2, its tension curve against rough cut 1, and which shots stay, get fixed, are redone or are new. Below it: rough cut 1 and the approved v1 storyboard for reference. Each shot shows a rough sketch of the framing (people as silhouettes, where the text goes), the narration line it covers, and what the painting will show. The real portraits and period pictures set how people and places look. Tap any picture to enlarge it.")
        ask = ("<p>Rough cut 2 is at the top of each Short (watch with sound): story v2, the 11 new images, the silent climaxes. Tell me by time or shot number what to change, or say it is ready for covers and publish packages. Reply in chat with the shot numbers you want changed (for example \"al-Razi 6: Matt holds the lamp higher\"), or say both are OK. The order is always: storyboard and sketches, then the image prompts (open \"Image prompt\" under any shot), then the images. Nothing is paid for until you approve the step before it.</p>")
    page = f"""<title>{html.escape(first.get("page_title", "Finlay and al-Razi Storyboards"))}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400&family=Montserrat:wght@700;800&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <div class="kicker">Oddly Matt · approval page · {html.escape(first.get("status") or "layered pilot · real pieces · waiting for your OK" if first.get("status") or pilots else (stages[0] if len(set(stages)) == 1 else ", ".join(stages)))}</div>
  <h1>{html.escape(h1)}</h1>
  <p class="lede">{html.escape(lede)}</p>
  <nav>{nav}</nav>
  {''.join(body)}
  <div class="ask"><h3>What I need from you</h3>{ask}</div>
</div>
<div id="lb" hidden><img alt=""></div>
<script>
const lb=document.getElementById('lb'),lbi=lb.querySelector('img');
document.addEventListener('click',e=>{{const t=e.target;if(t.tagName==='IMG'&&t.closest('figure,.shot,.maps,.v2grid,.layered')){{lbi.src=t.src;lbi.alt=t.alt;lb.hidden=false}}else if(t.closest('#lb')){{lb.hidden=true}}}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.hidden=true}});
</script>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    return out / "index.html"


if __name__ == "__main__":
    print(build(Path(sys.argv[1]), sys.argv[2:] or ["hcs07", "hcs05"]))
