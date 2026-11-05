"""Playlist covers for YouTube and Facebook (1280x720, both take 16:9): the story frames as a fan of posters on the
right, the playlist name in the OddlyThumbnail type on the left. Free (existing art only). Re-run when a playlist gets
a new story and swap its panels.
    python channels/storybook-medical/scripts/playlist_covers.py
-> projects/_playlists/renders/<slug>.jpg + check.jpg (full size and the phone sizes)"""
import json
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter

from episode import KIT, KIT_REMOTION, REPO, tools

P = REPO / "projects"
PLAYLISTS = {
    "season-zero": dict(name="Season Zero", kicker="ODDLY MATT · SEASON ZERO", lines=["TRUE", "MEDICAL", "STORIES"],
                        panels=[(P / "hc001-s1/assets/images/covers/cover.png", 0.36), (P / "hcs01-forssmann/assets/images/keyframes/s6a.png", 0.55),
                                (P / "hc001-s2/assets/images/covers/cover.png", 0.36)]),
    "alexis-st-martin": dict(name="Season Zero · Alexis St. Martin", kicker="MACKINAC · 1822", lines=["ALEXIS", "ST. MARTIN"],
                             panels=[(P / f"hc001-s{n}/assets/images/covers/cover.png", 0.28) for n in (2, 1, 3)], size=96),
    # one story so far: swap a panel for Marshall (HCS02) when it's out
    "crazy-science": dict(name="Crazy Science (true stories)", kicker="TRUE STORIES", lines=["CRAZY", "SCIENCE"],
                          panels=[(P / "hcs01-forssmann/assets/images/keyframes/s2.png", 0.5), (P / "hcs01-forssmann/assets/images/keyframes/s6a.png", 0.55),
                                  (P / "hcs01-forssmann/assets/images/keyframes/s8b.png", 0.45)]),
}
W, H = 2560, 1440
PH, PW = 880, 660                        # 3:4 panels: the action part of each 9:16 frame (Shorts covers keep an empty text band at the bottom)
FAN = [(1270, -4), (1555, 0), (1840, 4)]  # (left x, degrees): back, front, back


def background(panels):
    """The middle panel, blurred and darkened, filling the frame; the posters fanned on the right, the middle one on top."""
    mid = Image.open(panels[1][0] if isinstance(panels[1], tuple) else panels[1]).convert("RGB")
    bg = mid.resize((W, int(W * mid.height / mid.width))).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (12, 16, 18)), 0.62)
    for i in (0, 2, 1):
        x, deg = FAN[i]
        path, fy = panels[i] if isinstance(panels[i], tuple) else (panels[i], 0.5)
        src = Image.open(path).convert("RGB")
        ch = int(src.width * 4 / 3)                                                  # 3:4 crop centred on fy of the height
        top = max(0, min(src.height - ch, int(fy * src.height - ch / 2)))
        im = src.crop((0, top, src.width, top + ch)).resize((PW, PH), Image.LANCZOS)
        card = Image.new("RGBA", (PW + 16, PH + 16), (244, 238, 226, 255))           # bone-white print border
        card.paste(im, (8, 8))
        card = card.rotate(deg, resample=Image.BICUBIC, expand=True)
        shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
        ImageDraw.Draw(shadow).bitmap((0, 0), card.split()[3], fill=(0, 0, 0, 150))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        y = (H - card.height) // 2
        bg.paste(shadow, (x + 14, y + 22), shadow)
        bg.paste(card, (x, y), card)
    return bg


def main():
    stage = P / "_playlists/remotion"
    (stage / "public/img").mkdir(parents=True, exist_ok=True)
    for f in KIT_REMOTION:
        shutil.copy(KIT / "remotion" / f, stage / f)
    composer = REPO / "remotion-composer"
    entry = tools()["video_compose"]._stage_atelier_project((stage / "index.tsx").resolve(), composer.resolve())
    out = P / "_playlists/renders"
    out.mkdir(parents=True, exist_ok=True)
    done = []
    for slug, pl in PLAYLISTS.items():
        background(pl["panels"]).save(stage / f"public/img/{slug}.jpg", "JPEG", quality=92)
        pf = stage / f"{slug}-props.json"
        json.dump({"image": f"img/{slug}.jpg", "kicker": pl["kicker"], "lines": pl["lines"], "side": "left", "size": pl.get("size", 112)},
                  open(pf, "w", encoding="utf-8"))
        png = out / f"{slug}.png"
        subprocess.run(["npx", "remotion", "still", str(entry), "OddlyThumbnail", str(png), f"--props={pf.resolve()}",
                        f"--public-dir={(stage / 'public').resolve()}", "--log=error"], cwd=composer, check=True,
                       shell=sys.platform == "win32")
        jpg = out / f"{slug}.jpg"
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=90, optimize=True)
        png.unlink()
        done.append((pl["name"], jpg))
        print(f"{pl['name']:34} -> {jpg}  ({jpg.stat().st_size / 1e6:.2f} MB)")
    # phone check: full size, then about the size the playlist tile shows on a phone
    sheet = Image.new("RGB", (1280 + 40 + 320 + 40, 760 * len(done)), "#0f0f0f")
    d = ImageDraw.Draw(sheet)
    for i, (name, jpg) in enumerate(done):
        im = Image.open(jpg)
        sheet.paste(im, (0, i * 760))
        sheet.paste(im.resize((320, 180), Image.LANCZOS), (1320, i * 760))
        d.text((1320, i * 760 + 200), name, fill="white")
    sheet.save(out / "check.jpg", quality=88)
    print("check ->", out / "check.jpg")


if __name__ == "__main__":
    main()
