"""Free pre-viz (user, 2026-11-09: "a better storybook with no charge before generation"). Draws, with no paid call:

  1. the SET MAP: a top-down plan of a set that appears in several shots (streets, buildings, landmarks) with every
     shot's camera as a numbered marker and a view cone, so two shots facing the same way are seen before they cost;
  2. BLOCKING FRAMES: one 9:16 sketch per shot (background zones, landmarks, people as silhouettes, labels), next to
     the current image when there is one ("now" vs "planned").

The episode's spec lives with the episode (e.g. editorial/episodes/HCS08-john-snow/previz_hcs08.py) and calls render().
Shapes are in 0..1 frame coordinates (x right, y down). Map coordinates are 0..1000 (north up).
"""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "arialbd.ttf"
INK, PAPER, GREY = (30, 30, 34), (246, 241, 230), (150, 150, 150)
CAM_COLORS = [(214, 69, 65), (38, 120, 178), (46, 150, 90), (200, 130, 20), (140, 70, 170), (20, 150, 160),
              (180, 60, 120), (90, 90, 90), (120, 100, 40)]


def _font(size):
    try:
        return ImageFont.truetype(FONT, size)
    except OSError:
        return ImageFont.load_default()


def _wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


# ── map ──────────────────────────────────────────────────────────────────────────────────────────────────────────
def draw_map(spec: dict, size: int = 1100) -> Image.Image:
    """spec: {"title", "streets": [(x0,y0,x1,y1,label)], "blocks": [(x0,y0,x1,y1,label,fill)],
    "landmarks": [(x,y,label)], "cameras": [(name, x, y, facing_deg, fov_deg, note, old?)]}; facing 0 = north, 90 = east."""
    m, s = 60, (size - 120) / 1000
    im = Image.new("RGB", (size, size + 60), PAPER)
    d = ImageDraw.Draw(im)
    P = lambda x, y: (m + x * s, m + 40 + y * s)  # noqa: E731
    d.text((m, 14), spec["title"], fill=INK, font=_font(34))
    for x0, y0, x1, y1, label, fill in spec.get("blocks", []):
        d.rectangle([P(x0, y0), P(x1, y1)], fill=fill, outline=INK, width=2)
        if label:
            cx, cy = P((x0 + x1) / 2, (y0 + y1) / 2)
            f = _font(22)
            for i, ln in enumerate(_wrap(d, label, f, (x1 - x0) * s - 10)):
                d.text((cx, cy + i * 24 - 12), ln, fill=INK, font=f, anchor="mm")
    for x0, y0, x1, y1, label in spec.get("streets", []):
        d.rectangle([P(x0, y0), P(x1, y1)], fill=(214, 208, 196))
        cx, cy = P((x0 + x1) / 2, (y0 + y1) / 2)
        vertical = (y1 - y0) > (x1 - x0)
        if vertical:
            t = Image.new("RGBA", (400, 40), (0, 0, 0, 0))
            ImageDraw.Draw(t).text((200, 20), label, fill=(110, 105, 95), font=_font(24), anchor="mm")
            t = t.rotate(90, expand=True)
            im.paste(t, (int(cx - 20), int(cy - 200 + 230)), t)
        else:
            d.text((cx - 230, cy), label, fill=(110, 105, 95), font=_font(24), anchor="mm")
    for x, y, label in spec.get("landmarks", []):
        cx, cy = P(x, y)
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=INK)
        d.text((cx + 18, cy - 30), label, fill=INK, font=_font(24))
    for i, (name, x, y, facing, fov, note, *old) in enumerate(spec.get("cameras", [])):
        col = GREY if old and old[0] else CAM_COLORS[i % len(CAM_COLORS)]
        cx, cy = P(x, y)
        r = 230 * s
        a0, a1 = math.radians(facing - fov / 2 - 90), math.radians(facing + fov / 2 - 90)
        cone = [(cx, cy)] + [(cx + r * math.cos(a0 + (a1 - a0) * k / 12), cy + r * math.sin(a0 + (a1 - a0) * k / 12))
                             for k in range(13)]
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).polygon(cone, fill=col + (60,), outline=col + (230,))
        im.paste(ov, (0, 0), ov)
        d = ImageDraw.Draw(im)
        d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=col, outline=INK, width=2)
        d.text((cx, cy), name, fill="white", font=_font(18), anchor="mm")
    # compass
    d.text((size - 70, 70), "N", fill=INK, font=_font(30), anchor="mm")
    d.line([(size - 70, 130), (size - 70, 90)], fill=INK, width=4)
    d.polygon([(size - 80, 98), (size - 60, 98), (size - 70, 84)], fill=INK)
    return im


# ── blocking frames ──────────────────────────────────────────────────────────────────────────────────────────────
def figure(d, W, H, x, y, h, col=INK, hat=False, sitting=False, back=False):
    """A slim silhouette: feet at (x, y), height h (frame fractions): head, shoulders, tapered coat, two legs."""
    X, Y, hh = x * W, y * H, h * H
    if sitting:
        hh *= 0.7
    head = hh * 0.12
    top = Y - hh
    sh_w, hip_w = hh * 0.11, hh * 0.085
    d.ellipse([X - head * .42, top, X + head * .42, top + head], fill=col)
    neck = top + head * 1.05
    hip = Y - hh * (0.2 if sitting else 0.42)
    d.polygon([(X - sh_w, neck + hh * .03), (X + sh_w, neck + hh * .03), (X + hip_w * 1.2, hip), (X - hip_w * 1.2, hip)],
              fill=col)
    if sitting:
        d.rectangle([X - hip_w * 1.6, hip - hh * .02, X + hip_w * 1.6, Y], fill=col)
    else:
        lw = hh * 0.03
        d.rectangle([X - hip_w * .8 - lw, hip, X - hip_w * .8 + lw, Y], fill=col)
        d.rectangle([X + hip_w * .8 - lw, hip, X + hip_w * .8 + lw, Y], fill=col)
    if hat:
        d.rectangle([X - head * .38, top - head * .75, X + head * .38, top + head * .15], fill=col)
        d.rectangle([X - head * .7, top + head * .05, X + head * .7, top + head * .2], fill=col)


def draw_frame(shapes: list, W: int = 360, H: int = 640) -> Image.Image:
    """shapes: ("rect", x0,y0,x1,y1, fill[, label]) · ("grad", top_rgb, bottom_rgb) · ("poly", [(x,y)...], fill)
    · ("line", x0,y0,x1,y1, fill, width) · ("ellipse", x0,y0,x1,y1, fill) · ("fig", x, y, h, {opts}, label)
    · ("text", x, y, label) · ("pump", x, y, h, handle_side)."""
    im = Image.new("RGB", (W, H), (200, 196, 186))
    d = ImageDraw.Draw(im)
    f = _font(15)
    for sh in shapes:
        k = sh[0]
        if k == "grad":
            for yy in range(H):
                t = yy / H
                d.line([(0, yy), (W, yy)], fill=tuple(int(a + (b - a) * t) for a, b in zip(sh[1], sh[2])))
        elif k == "rect":
            d.rectangle([sh[1] * W, sh[2] * H, sh[3] * W, sh[4] * H], fill=sh[5], outline=INK)
            if len(sh) > 6:
                d.text(((sh[1] + sh[3]) / 2 * W, (sh[2] + sh[4]) / 2 * H), sh[6], fill="white", font=f, anchor="mm",
                       stroke_width=2, stroke_fill=INK)
        elif k == "poly":
            d.polygon([(x * W, y * H) for x, y in sh[1]], fill=sh[2], outline=INK)
        elif k == "line":
            d.line([sh[1] * W, sh[2] * H, sh[3] * W, sh[4] * H], fill=sh[5], width=sh[6])
        elif k == "ellipse":
            d.ellipse([sh[1] * W, sh[2] * H, sh[3] * W, sh[4] * H], fill=sh[5])
        elif k == "fig":
            o = sh[4]
            figure(d, W, H, sh[1], sh[2], sh[3], col=o.get("col", INK), hat=o.get("hat", False),
                   sitting=o.get("sitting", False))
            if len(sh) > 5:
                d.text((sh[1] * W, (sh[2] - sh[3]) * H - 14), sh[5], fill="white", font=f, anchor="mm",
                       stroke_width=2, stroke_fill=INK)
        elif k == "pump":
            x, y, h, side = sh[1:5]
            X, Y, hh = x * W, y * H, h * H
            w = hh * 0.06
            d.rectangle([X - w, Y - hh * .92, X + w, Y], fill=INK)
            d.ellipse([X - w * 1.3, Y - hh, X + w * 1.3, Y - hh * .86], fill=INK)
            sgn = 1 if side == "right" else -1
            if side in ("left", "right"):
                d.arc([X + sgn * w - hh * .18, Y - hh * .85, X + sgn * w + hh * .18, Y - hh * .2],
                      *((-90, 90) if side == "right" else (90, 270)), fill=INK, width=max(3, int(w * .5)))
            tx = sorted([X - sgn * w - sgn * hh * .25, X - sgn * w])
            d.rectangle([tx[0], Y - hh * .14, tx[1], Y], fill=(110, 110, 110), outline=INK)
        elif k == "text":
            for i, ln in enumerate(_wrap(d, sh[3], f, W - 20)):
                d.text((sh[1] * W, sh[2] * H + i * 18), ln, fill="white", font=f, anchor="mm", stroke_width=2,
                       stroke_fill=INK)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)
    return im


ZONES = {"TOP": 300 / 1920, "MID": 660 / 1920, "LOW": 1030 / 1920}  # Shorts text zones (safe zone y 288-1248)


def render_frames(out_dir: Path, shots: list[dict], W: int = 360, H: int = 640) -> list[Path]:
    """One PNG per shot (for the storyboard page): the blocking frame plus the Shorts safe zone (dotted) and the
    shot's text zone as a labelled band. shot: {"name", "shapes", "zone": "TOP"|"MID"|"LOW"|None, "text": str}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for s in shots:
        im = draw_frame(s["shapes"], W, H).convert("RGBA")
        ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        y0, y1, x0, x1 = 288 / 1920 * H, 1248 / 1920 * H, 65 / 1080 * W, 888 / 1080 * W
        for x in range(int(x0), int(x1), 8):
            d.line([(x, y0), (x + 4, y0)], fill=(255, 255, 255, 150), width=1)
            d.line([(x, y1), (x + 4, y1)], fill=(255, 255, 255, 150), width=1)
        z = s.get("zone")
        if z:
            cy = ZONES[z] * H
            d.rectangle([x0, cy - 22, x1, cy + 22], fill=(232, 163, 61, 120), outline=(232, 163, 61, 255), width=2)
            d.text(((x0 + x1) / 2, cy), s.get("text", z), fill=(255, 255, 255, 255), font=_font(16), anchor="mm",
                   stroke_width=2, stroke_fill=INK)
        im = Image.alpha_composite(im, ov).convert("RGB")
        p = out_dir / f"{s['name']}.png"
        im.save(p)
        paths.append(p)
    return paths


def render(out: Path, map_spec: dict | None, shots: list[dict], keyframes_dir: Path | None = None):
    """shots: [{"name", "camera": text, "shapes": [...], "now": bool}] -> one review PNG."""
    W, H, pad = 360, 640, 24
    cols = len(shots)
    rows_h = (H + 40) * 2 + 260
    mp = draw_map(map_spec) if map_spec else None
    width = (mp.width + pad if mp else 0) + cols * (W + pad) + pad
    height = max(mp.height + 2 * pad if mp else 0, rows_h + 2 * pad)
    sheet = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(sheet)
    x0 = pad
    if mp:
        sheet.paste(mp, (pad, pad))
        x0 += mp.width + pad
    for i, s in enumerate(shots):
        x = x0 + i * (W + pad)
        y = pad
        cur = keyframes_dir / f"{s['name']}.png" if keyframes_dir else None
        d.text((x, y), f"{s['name']}  now" if cur and cur.exists() else s["name"], fill=INK, font=_font(24))
        if cur and cur.exists():
            im = Image.open(cur).convert("RGB").resize((W, H))
            sheet.paste(im, (x, y + 34))
        y2 = y + 34 + H + 12
        d.text((x, y2), f"{s['name']}  planned", fill=(214, 69, 65), font=_font(24))
        sheet.paste(draw_frame(s["shapes"], W, H), (x, y2 + 34))
        f = _font(17)
        for k, ln in enumerate(_wrap(d, s["camera"], f, W)[:12]):
            d.text((x, y2 + 34 + H + 10 + k * 20), ln, fill=INK, font=f)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=90)
    return out
