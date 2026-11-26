"""Render the Oddly Matt upload files (profile icons, banner, watermark, Facebook cover) with headless Chrome.
Source art: projects/oddly-matt-mascot/assets/images/brand/ (painted finals). Output: brand/upload/."""
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
B = REPO / "projects/oddly-matt-mascot/assets/images/brand"
OUT = REPO / "channels/storybook-medical/brand/upload"
TMP = REPO / "projects/_brandkit/export"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT.mkdir(parents=True, exist_ok=True); TMP.mkdir(parents=True, exist_ok=True)
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&display=swap">'

GLASSES = '''
<defs>
<radialGradient id="fLens" cx="0.4" cy="0.36" r="0.75"><stop offset="0" stop-color="#F7C974"/><stop offset="0.55" stop-color="#E8A33D"/><stop offset="1" stop-color="#B8761F"/></radialGradient>
<radialGradient id="fGlow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#E8A33D" stop-opacity="0.5"/><stop offset="1" stop-color="#E8A33D" stop-opacity="0"/></radialGradient>
</defs>
{bg}
<path d="M31 100 L14 93 M169 100 L186 93" stroke="#EFE6D2" stroke-width="{w}" stroke-linecap="round"/>
<path d="M90 99 Q100 85 110 99" fill="none" stroke="#EFE6D2" stroke-width="{w}" stroke-linecap="round"/>
<circle cx="62" cy="106" r="29" fill="url(#fLens)" stroke="#EFE6D2" stroke-width="{w}"/>
<circle cx="138" cy="106" r="29" fill="url(#fLens)" stroke="#EFE6D2" stroke-width="{w}"/>
<path d="M47 91 C47 84 59 84 59 91.5 C59 96 53 97 53 102" fill="none" stroke="#FFF7E6" stroke-width="4.6" stroke-linecap="round"/>
<circle cx="53" cy="109" r="2.7" fill="#FFF7E6"/>
{shine}'''
SHINE = '<path d="M123 93 A19 19 0 0 1 134 86" fill="none" stroke="#FFF7E6" stroke-opacity="0.65" stroke-width="3.5" stroke-linecap="round"/>'


def icon_svg(px, watermark=False):
    if watermark:
        inner = GLASSES.format(bg='<circle cx="100" cy="100" r="98" fill="#22262A" fill-opacity="0.82"/>', w=8, shine="")
    else:
        inner = GLASSES.format(bg='<rect width="200" height="200" fill="#1F4E5A"/><ellipse cx="100" cy="106" rx="96" ry="58" fill="url(#fGlow)"/>', w=7, shine=SHINE)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="{px}" height="{px}" style="display:block">{inner}</svg>'


def page(body, transparent=False):
    bg = "transparent" if transparent else "#22262A"
    return f'<!doctype html><html><head><meta charset="utf-8">{FONT}<style>html,body{{margin:0;background:{bg};overflow:hidden}}</style></head><body>{body}</body></html>'


def wordmark(size, tag):
    return (f'<div style="font-family:Montserrat,sans-serif;font-weight:900;font-size:{size}px;line-height:.86;letter-spacing:-.015em;'
            f'text-shadow:0 6px 40px rgba(10,12,14,.6)"><div style="color:#E8A33D">ODDLY</div><div style="color:#EFE6D2">MATT</div></div>'
            f'<div style="font-family:Montserrat,sans-serif;font-weight:700;font-size:{tag}px;line-height:1.3;color:#EFE6D2;'
            f'text-shadow:0 2px 18px rgba(10,12,14,.75);margin-top:{int(size*0.16)}px">True stories from the strange side of being human.</div>')


def render(name, w, h, html, transparent=False):
    src = TMP / f"{name}.html"
    src.write_text(html, encoding="utf-8")
    out = OUT / name
    args = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
            "--virtual-time-budget=4000", f"--screenshot={out}", src.as_uri()]
    if transparent:
        args.insert(2, "--default-background-color=00000000")
    subprocess.run(args, check=True, capture_output=True)
    print(name, out.stat().st_size // 1024, "KB")


img = lambda p: (B / p).as_uri()

# Profile pictures (same art everywhere; platforms crop to a circle)
render("profile-icon-800.png", 800, 800, page(icon_svg(800)))
render("profile-icon-1080.png", 1080, 1080, page(icon_svg(1080)))
# YouTube video watermark, transparent
render("youtube-watermark-150.png", 150, 150, page(icon_svg(150, watermark=True), transparent=True), transparent=True)
# YouTube banner 2560x1440 (title inside the 1235x338 all-device safe area)
render("youtube-banner-2560x1440.png", 2560, 1440, page(
    f'<div style="position:relative;width:2560px;height:1440px">'
    f'<img src="{img("web/banner-2560.jpg")}" style="position:absolute;inset:0;width:2560px;height:1440px;object-fit:cover">'
    f'<div style="position:absolute;left:780px;top:551px;width:860px;height:338px;display:flex;flex-direction:column;justify-content:center">'
    f'{wordmark(140, 27)}</div></div>'))
# Facebook cover 1640x624 (2x of 820x312); centred so the mobile crop keeps the name
render("facebook-cover-1640x624.png", 1640, 624, page(
    f'<div style="position:relative;width:1640px;height:624px;overflow:hidden">'
    f'<img src="{img("web/banner-2560.jpg")}" style="position:absolute;left:0;top:-250px;width:1640px;height:922px;object-fit:cover">'
    f'<div style="position:absolute;inset:0;background:radial-gradient(ellipse 45% 70% at 50% 50%,rgba(16,18,20,.72) 0%,rgba(16,18,20,0) 100%)"></div>'
    f'<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;gap:28px">{icon_svg(120).replace("<svg ", "<svg style=\"border-radius:50%\" ", 1)}'
    f'<div style="font-family:Montserrat,sans-serif;font-weight:900;font-size:92px;letter-spacing:-.015em;white-space:nowrap;text-shadow:0 6px 30px rgba(0,0,0,.6)">'
    f'<span style="color:#E8A33D">ODDLY</span> <span style="color:#EFE6D2">MATT</span></div></div></div>'))
# Optional channel-trailer / About image
render("key-art-1920x1080.png", 1920, 1080, page(
    f'<img src="{img("web/banner-2560.jpg")}" style="display:block;width:1920px;height:1080px;object-fit:cover">'))
