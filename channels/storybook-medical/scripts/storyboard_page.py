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
        "storyboard": EP / "HCS07-finlay/storyboard-v1.md",
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
        "storyboard": EP / "HCS05-al-razi/storyboard-v1.md",
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


def shrink(src: Path, dst: Path, edge: int = 900):
    im = Image.open(src).convert("RGB")
    im.thumbnail((edge, edge))
    im.save(dst.with_suffix(".jpg"), quality=82)
    return dst.with_suffix(".jpg").name


CSS = """
:root{--bg:#f3eee3;--surface:#fbf8f1;--ink:#22262a;--muted:#5d625f;--line:#d9cfbd;--amber:#b8740f;--amber-soft:#f4dfb6;--teal:#1f4e5a;--teal-soft:#d5e4e4;
--display:'Montserrat',system-ui,sans-serif;--body:'Inter',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1a1d20;--surface:#23282c;--ink:#efe6d2;--muted:#a9a99f;--line:#3a4044;--amber:#e8a33d;--amber-soft:#4a3a1e;--teal:#8cc0c4;--teal-soft:#1f3a40;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#1a1d20;--surface:#23282c;--ink:#efe6d2;--muted:#a9a99f;--line:#3a4044;--amber:#e8a33d;--amber-soft:#4a3a1e;--teal:#8cc0c4;--teal-soft:#1f3a40;color-scheme:dark}
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
.block{margin-top:28px;display:grid;gap:12px}
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
#lb{position:fixed;inset:0;background:rgba(10,12,14,.88);display:flex;align-items:center;justify-content:center;padding:24px;z-index:20;cursor:zoom-out}
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
    for k, e, p in eps:
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
            pic = ""
            if fr.exists():
                shutil.copy(fr, img / f"{k}-{n}.png")
                pic = f'<img src="img/{k}-{n}.png" alt="Pre-viz sketch, shot {html.escape(n)}" loading="lazy">'
            cards.append(
                f'<article class="shot">{pic}<div class="info"><div class="head"><span class="num">{html.escape(n)}</span>'
                f'<span class="chip">{html.escape(s)} s</span><span class="size">{inline(size)}</span></div>'
                f'<p class="line">“{inline(line)}”</p><dl><dt>We see</dt><dd>{inline(see)}</dd>'
                f'<dt>Motion</dt><dd>{inline(fx)}</dd><dt>Text</dt><dd>{inline(txt)}</dd>'
                f'<dt>Sound</dt><dd>{inline(sfx)}</dd></dl></div></article>')
        notes = "".join(f"<p>{inline(n)}</p>" for n in p["notes"])
        body.append(f"""
<section class="ep" id="{e['anchor']}">
  <div class="kicker">{html.escape(k.upper())} · {html.escape(e['slot'])}</div>
  <h2>{html.escape(p['title'].split(' — ', 1)[-1])}</h2>
  <div class="meta"><span><b>{len(cards)}</b> shots</span><span>≈ <b>{p['secs']:.0f} s</b> of pictures</span>
  <span>estimate <b>{html.escape(p['cost'])}</b></span><span>status <b>storyboard v1.1 · waiting for your OK</b></span></div>
  <div class="block"><h3>Notes and period rules</h3><div class="notes">{notes}</div></div>
  <div class="block"><h3>Script (approved)</h3><div class="script">{''.join(sc)}</div></div>
  <div class="block"><h3>People and places: the real pictures we follow</h3><div class="refs">{''.join(figs)}</div></div>
  <div class="block"><h3>Cast and sets</h3><div class="cast"><table><tr><th>Who / where</th><th>Look</th><th>Shots</th></tr>{cast}</table></div></div>
  <div class="block"><h3>Set map (where each camera stands)</h3><div class="maps">{''.join(maps)}</div></div>
  <div class="block"><h3>Shots</h3><p class="legend"><span></span>orange band = where the on-screen text sits · dotted lines = the Shorts safe zone</p>
  <div class="shots">{''.join(cards)}</div></div>
</section>""")
    page = f"""<title>Finlay and al-Razi Storyboards</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=JetBrains+Mono:wght@400&family=Montserrat:wght@700;800&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <div class="kicker">Oddly Matt · free pre-viz · nothing generated yet</div>
  <h1>Next two Shorts, shot by shot</h1>
  <p class="lede">Each shot shows a rough sketch of the framing (people as silhouettes, where the text goes), the narration line it covers, and what the painting will show. The real portraits and period pictures set how people and places look. Tap any picture to enlarge it.</p>
  <nav>{nav}</nav>
  {''.join(body)}
  <div class="ask"><h3>What I need from you</h3><p>Reply in chat with the shot numbers you want changed (for example "al-Razi 6: Matt holds the lamp higher"), or say both are OK. Next comes the image prompts; images are only made after you approve them.</p></div>
</div>
<div id="lb" hidden><img alt=""></div>
<script>
const lb=document.getElementById('lb'),lbi=lb.querySelector('img');
document.addEventListener('click',e=>{{const t=e.target;if(t.tagName==='IMG'&&t.closest('figure,.shot,.maps')){{lbi.src=t.src;lbi.alt=t.alt;lb.hidden=false}}else if(t.closest('#lb')){{lb.hidden=true}}}});
document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.hidden=true}});
</script>
"""
    (out / "index.html").write_text(page, encoding="utf-8")
    return out / "index.html"


if __name__ == "__main__":
    print(build(Path(sys.argv[1]), sys.argv[2:] or ["hcs07", "hcs05"]))
