"""HCS01 storybook board (plan/production-v3.md §3): every frame with its line, timing, motion, effects, sound, and the
caption/stamp drawn where it will sit. Yellow dashed box = where the camera ends; cyan box = where it starts.
    python channels/storybook-medical/editorial/episodes/HCS01-forssmann/storybook_hcs01.py
-> projects/hcs01-forssmann/review/storybook.jpg  (free)"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[5]
P = REPO / "projects/hcs01-forssmann"
KF = P / "assets/images/keyframes"
FONT = "C:/Windows/Fonts/segoeui.ttf"
BOLD = "C:/Windows/Fonts/segoeuib.ttf"
ZONE = {"TOP": 300 / 1920, "MID": 1180 / 1920, "LOW": 1430 / 1920}  # StorybookShort captionY

# (frame, seconds, line with the KEY WORD in caps, camera, motion/fx note, caption zone, stamp (text, y), sound)
# camera: ("push", cx, cy, zoom) ends on that crop · ("pull", cx, cy, zoom) starts on it · ("slide", dx) · None
SHOTS = [
    ("s1a", 3.0, "In 1929, a young doctor pushed a TUBE…", ("push", .45, .62, 1.3), "slow push onto the tube's open end", "TOP", None, "lamp hum"),
    ("s1b", 3.2, "…through his own arm… all the way into his own HEART.", ("push", .6, .42, 1.2),
     "FX: an amber line draws itself up the blue vein, elbow → heart, arriving on 'heart'; the heart glows once", "LOW", None, "soft whoosh with the line"),
    ("s2", 6.3, "WERNER FORSSMANN, a trainee surgeon in Germany, wanted to reach a living heart through a VEIN.", ("slide", .08),
     "2.5D depth slide right · FX: steady highlight on him at his name · the chart's vein glows on 'vein'", "LOW",
     ("WERNER FORSSMANN · 1929", .1), "—"),
    ("s3", 2.5, "His boss said NO. Far too dangerous.", ("push", .5, .38, 1.1), "holds still, then a quick small push on 'no'", "LOW", None, "music drops out on 'no'"),
    ("s4", 4.5, "The nurse with the supplies agreed to help… if he tried it on HER.", ("push", .33, .5, 1.6),
     "push in to her · FX: the key ring is cut out and swings gently", "LOW", None, "keys jingle with the swing"),
    ("s5", 3.2, "He TRICKED her. He numbed his OWN ARM instead.", ("push", .6, .55, 1.4),
     "comedy hold · FX: she dims, he is highlighted on 'own arm'", "TOP", None, "small swab 'tsk'"),
    ("s6a", 1.6, "He slid the CATHETER in.", ("push", .35, .72, 1.3), "slow push down to his hands feeding the tube in under the gauze", "TOP", None, "—"),
    ("s6b", 1.7, "SIXTY-FIVE CENTIMETERS.", ("slide", -.06), "slide along the tube to its top end", None, ("65 cm", ZONE["MID"]), "stamp thud on 'five'"),
    ("s7", 4.1, "Then he WALKED to the X-ray room, the tube still in his arm.", ("pull", .5, .45, 1.45),
     "2.5D: the camera pulls back down the corridor, walls sliding past · CLIP? only if this feels dead in the rough cut", "TOP", None, "footsteps only if it becomes a clip"),
    ("s8a", 2.2, "The picture showed the TIP…", ("push", .5, .45, 1.3),
     "FX: a thin white line draws on the film from his left shoulder into the heart shadow, stopping on 'tip'", "TOP", None, "X-ray buzz"),
    ("s8b", 1.8, "…inside his heart. He was FINE.", ("push", .72, .5, 1.6), "push in to his relieved face", "LOW", None, "buzz stops"),
    ("s9", 2.5, "His reward? FIRED from his next job.", None, "deadpan hold", "TOP", ("FIRED", .42), "stamp thud on 'fired'"),
    ("s10a", 2.0, "TWENTY-SEVEN YEARS LATER, the world caught up.", ("push", .55, .3, 1.3), "push onto the headline", "LOW", None, "paper slide"),
    ("s10b", 2.1, "NOBEL PRIZE.", None, "3D: this painted medal turns half a turn and settles on 'Prize' (the medal test)", "LOW", None, "bright chord"),
    ("s11", 3.4, "But in 1932, he had joined the Nazi Party.", ("pull", .5, .4, 1.15), "FX: colour drains to grey · slow pull out · hold", "LOW",
     ("1932", .64), "music fades to one low note"),
    (None, 3.0, "(brand sting)", None, "", None, None, "sting"),
]


def dashed(d, box, color, w=3, dash=14):
    x0, y0, x1, y1 = box
    for (a, b) in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        n = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])) // dash)
        for k in range(0, n, 2):
            t0, t1 = k / n, min(1, (k + 1) / n)
            d.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)], fill=color, width=w)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    return lines + ([cur] if cur else [])


def panel(shot, n, t0, W=330, H=587, T=250):
    name, sec, line, cam, note, zone, stamp, sfx = shot
    im = Image.new("RGB", (W, H + T), "#F4EEE2")
    d = ImageDraw.Draw(im, "RGBA")
    if name:
        src = Image.open(KF / f"{name}.png").convert("RGB")
        if src.width / src.height > W / H:              # the square medal sits on its dark-red ground
            bg = Image.new("RGB", (W, H), "#6B1E1A")
            s = src.resize((W, W))
            bg.paste(s, (0, (H - W) // 2))
            src = bg
        im.paste(src.resize((W, H)), (0, 0))
        if cam and cam[0] in ("push", "pull"):
            _, cx, cy, z = cam
            bw, bh = W / z, H / z
            x0 = min(max(cx * W - bw / 2, 0), W - bw)
            y0 = min(max(cy * H - bh / 2, 0), H - bh)
            dashed(d, (x0, y0, x0 + bw, y0 + bh), "#FFD34D" if cam[0] == "push" else "#4DE1FF")
        elif cam and cam[0] == "slide":
            y = H * 0.93
            a, b = (W * .3, W * .7) if cam[1] > 0 else (W * .7, W * .3)
            d.line([(a, y), (b, y)], fill="#FFD34D", width=4)
            d.polygon([(b, y), (b - 12 * (1 if b > a else -1), y - 8), (b - 12 * (1 if b > a else -1), y + 8)], fill="#FFD34D")
        cf = ImageFont.truetype(BOLD, 15)
        if zone:                                        # the caption, where it will sit
            words = line.replace("…", "").split()[:4]
            cap = " ".join(w.strip(",.?") for w in words).upper()
            y = ZONE[zone] * H
            tw = d.textlength(cap, font=cf)
            d.rounded_rectangle((W / 2 - tw / 2 - 8, y - 13, W / 2 + tw / 2 + 8, y + 13), 6, fill=(20, 16, 12, 170))
            d.text((W / 2, y), cap, font=cf, fill="white", anchor="mm")
        if stamp:
            sf = ImageFont.truetype(BOLD, 30 if len(stamp[0]) < 8 else 16)
            y = stamp[1] * H
            tw = d.textlength(stamp[0], font=sf)
            d.rounded_rectangle((W / 2 - tw / 2 - 10, y - 22, W / 2 + tw / 2 + 10, y + 22), 4, outline="#C8392B", width=4)
            d.text((W / 2, y), stamp[0], font=sf, fill="#C8392B", anchor="mm")
    else:
        d.rectangle((0, 0, W, H), fill="#2A1F14")
        d.text((W / 2, H / 2), "ODDLY MATT\nsting", font=ImageFont.truetype(BOLD, 26), fill="#F0A23A", anchor="mm", align="center")
    hf, bf, sf = ImageFont.truetype(BOLD, 15), ImageFont.truetype(FONT, 13), ImageFont.truetype(FONT, 12)
    d.text((8, H + 6), f"{n}  {name or 'end'}   {t0:.1f}–{t0 + sec:.1f} s", font=hf, fill="#2A1F14")
    y = H + 28
    for ln in wrap(d, f"“{line}”", bf, W - 16)[:4]:
        d.text((8, y), ln, font=bf, fill="#2A1F14")
        y += 17
    y += 4
    for ln in wrap(d, note, sf, W - 16)[:5]:
        d.text((8, y), ln, font=sf, fill="#5A4A3A")
        y += 15
    d.text((8, H + T - 20), f"SFX: {sfx}", font=sf, fill="#8A5A2A")
    return im


def main():
    cols, W, H, T = 8, 330, 587, 250
    rows = -(-len(SHOTS) // cols)
    board = Image.new("RGB", (cols * (W + 10) + 10, rows * (H + T + 10) + 60), "#E4DCCB")
    d = ImageDraw.Draw(board)
    total = sum(s[1] for s in SHOTS)
    d.text((14, 14), f"HCS01 · He Pushed a Tube Into His Own Heart · storybook · {len(SHOTS) - 1} frames · {total:.1f} s   "
                     "(yellow dashed = where the camera ends · cyan = where it starts · caption and stamp drawn where they sit)",
           font=ImageFont.truetype(BOLD, 22), fill="#2A1F14")
    t = 0.0
    for i, s in enumerate(SHOTS):
        board.paste(panel(s, i + 1, t), (10 + (i % cols) * (W + 10), 60 + (i // cols) * (H + T + 10)))
        t += s[1]
    out = P / "review/storybook.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    board.save(out, quality=90)
    print("storybook ->", out, f"({total:.1f} s)")


if __name__ == "__main__":
    main()
