"""HC002-S1 bandage paint fix (FREE, user 2026-11-19): in stills 9, 10 and 12 the band ran flat across BOTH brows and
read as a blindfold at video size. The fix keeps the patch over his LEFT eye, paints the band over his RIGHT brow back
as a DIAGONAL (the patch's lower edge rises across the forehead to his right temple: forehead + eyebrow show), and
draws a narrow wrap from the band OVER THE CROWN (claims C04: in under the left cheekbone, out through the top of the head).

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/paint_bandage_hc002s1.py [--preview DIR]

The originals stay as keyframes/<still>.orig.png (made on the first run), so the fix always starts from the generated
still. Coordinates are still PIXELS (1536 x 2752), measured on 10x grids. Afterwards re-run alive_hc002s1.py: the clean
plates of s9/s10/s12 carry the head.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[5]
KF = REPO / "projects/hc002-s1/assets/images/keyframes"
Z = 4   # supersampling for the drawn parts

# skin: the part of the band under its new DIAGONAL lower edge (`diag`, from his right temple down to where the patch's
#   own lower edge starts), repainted as forehead skin with a soft shadow under the band; brow: his right eyebrow
# wrap: a strip from the band's top up over the crown: centre line (foot, top), widths (foot, top), bow (px sideways at
#   the middle), clipped to `head` (traced contour), ink outline except along the foot, where it merges into the band
SPEC = {
    "s10": {
        "crop": (812, 1092, 906, 1170),
        "skin": [(823, 1134), (856, 1146), (854, 1150), (825, 1150)],
        "diag": [(823, 1135), (850, 1145), (856, 1148)],
        "brow": [(830, 1149), (835, 1147.5), (841, 1147), (846, 1148.5)],
        "wrap": {"c": [(844, 1129), (851, 1101)], "w": (16, 12), "bow": -1.5},
        "head": [(822, 1135), (823, 1125), (830, 1114), (836, 1109), (843, 1104), (858, 1102), (870, 1104),
                 (882, 1109), (890, 1119), (896, 1131), (898, 1140), (898, 1200), (822, 1200)],
        "tone": (830, 1180, 842, 1190), "band": (832, 1131, 846, 1141),
    },
    "s12": {
        "crop": (274, 690, 350, 748),
        "skin": [(280, 720), (302, 731), (300, 735), (281, 735)],
        "diag": [(280, 721), (297, 729), (302, 732)],
        "brow": [(282, 733), (286, 731.5), (291, 731.5), (295, 733)],
        "wrap": {"c": [(300, 716), (308, 694)], "w": (14, 10), "bow": -1.2},
        "head": [(279, 740), (280, 715), (285, 705), (290, 700), (300, 697), (316, 696), (326, 699), (336, 707),
                 (342, 715), (346, 725), (346, 760), (279, 760)],
        "tone": (284, 748, 292, 756), "band": (286, 718, 300, 726),
    },
    "s9": {
        "crop": (774, 830, 850, 900),
        "skin": [(781, 874), (800, 888), (798, 892), (782, 892)],
        "diag": [(781, 875), (796, 885), (801, 889)],
        "brow": [(781, 890), (785, 888.5), (790, 888.5), (794, 890)],
        "wrap": {"c": [(799, 864), (808, 832)], "w": (16, 12), "bow": -1.5},
        "head": [(781, 900), (782, 845), (787, 839), (796, 836), (806, 835), (816, 837), (824, 840), (832, 845),
                 (838, 852), (842, 860), (845, 870), (846, 900)],
        "tone": (786, 905, 796, 913), "band": (786, 867, 800, 876),
    },
}


def med(arr: np.ndarray, box) -> np.ndarray:
    x0, y0, x1, y1 = box
    return np.median(arr[y0:y1, x0:x1].reshape(-1, 3), axis=0).astype(np.float32)


def poly_mask(size, pts, ox=0, oy=0, z=1) -> Image.Image:
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon([((x - ox) * z, (y - oy) * z) for x, y in pts], fill=255)
    return m


def wrap_poly(w: dict, n: int = 12) -> list:
    """The strip's outline from its centre line (a gentle bow) and its widths, foot -> top -> foot."""
    (fx, fy), (tx, ty) = w["c"]
    L, R = [], []
    for i in range(n + 1):
        t = i / n
        cx = fx + (tx - fx) * t + w["bow"] * 4 * t * (1 - t)
        cy = fy + (ty - fy) * t
        half = (w["w"][0] + (w["w"][1] - w["w"][0]) * t) / 2
        dx, dy = tx - fx, ty - fy
        ln = (dx * dx + dy * dy) ** 0.5
        nx, ny = -dy / ln, dx / ln                           # normal to the centre line
        L.append((cx - nx * half, cy - ny * half))
        R.append((cx + nx * half, cy + ny * half))
    return L + R[::-1]


def fix(name: str, s: dict) -> Image.Image:
    orig = KF / f"{name}.orig.png"
    if not orig.exists():
        Image.open(KF / f"{name}.png").save(orig)
    arr = np.asarray(Image.open(orig).convert("RGB")).astype(np.float32)
    skin, band = med(arr, s["tone"]), med(arr, s["band"])
    cx0, cy0, cx1, cy1 = s["crop"]
    ink = np.percentile(arr[cy0:cy1, cx0:cx1].reshape(-1, 3), 2, axis=0)

    W, H = (cx1 - cx0) * Z, (cy1 - cy0) * Z
    crop = np.asarray(Image.fromarray(arr[cy0:cy1, cx0:cx1].astype(np.uint8)).resize((W, H), Image.LANCZOS),
                      np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    px, py = xx / Z + cx0, yy / Z + cy0

    # 1) forehead under the new diagonal edge: skin, darker right under the band
    dx_, dy_ = zip(*s["diag"])
    edge = np.interp(px, dx_, dy_)
    t = np.clip((py - edge) / 3.0, 0, 1)[..., None]
    paint = skin[None, None, :] * (0.90 + 0.10 * t)
    m = np.asarray(poly_mask((W, H), s["skin"], cx0, cy0, Z).filter(ImageFilter.GaussianBlur(Z * 0.5)),
                   np.float32)[..., None] / 255
    crop = crop * (1 - m) + paint * m

    # 2) the wrap over the crown, clipped to the head; far side shaded, one crease, ink ring except at the foot
    wp = wrap_poly(s["wrap"])
    wrap = (np.asarray(poly_mask((W, H), wp, cx0, cy0, Z), np.float32) / 255) *            (np.asarray(poly_mask((W, H), s["head"], cx0, cy0, Z), np.float32) / 255)
    (fx, fy), (tx, ty) = s["wrap"]["c"]
    v = np.clip((py - fy) / (ty - fy), 0, 1)
    cxl = fx + (tx - fx) * v + s["wrap"]["bow"] * 4 * v * (1 - v)
    half = (s["wrap"]["w"][0] + (s["wrap"]["w"][1] - s["wrap"]["w"][0]) * v) / 2
    u = np.clip((px - cxl) / half, -1, 1)                      # -1 left edge .. +1 right edge
    tone = 1.0 - 0.18 * np.clip((u - 0.3) / 0.6, 0, 1) - 0.10 * np.exp(-((u + 0.2) / 0.12) ** 2)
    tone *= 1.0 + 0.04 * v                                      # the top catches a little more light
    wa = np.asarray(Image.fromarray((wrap * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(Z * 0.3)),
                    np.float32)[..., None] / 255
    crop = crop * (1 - wa) + (band[None, None, :] * tone[..., None]) * wa
    wimg = Image.fromarray((wrap * 255).astype(np.uint8))
    ring = np.asarray(wimg.filter(ImageFilter.MaxFilter(2 * int(Z * 0.75) + 1)), np.float32) / 255 - wrap
    ring = np.clip(ring * (py < fy - 2.5), 0, 1)[..., None]
    crop = crop * (1 - ring) + ink[None, None, :] * ring

    out = Image.fromarray(np.clip(crop, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out)
    inkc = tuple(int(c) for c in ink)

    def stroke(pts, width):
        P = [((x - cx0) * Z, (y - cy0) * Z) for x, y in pts]
        d.line(P, fill=inkc, width=int(width), joint="curve")
        for x, y in (P[0], P[-1]):
            r = width / 2
            d.ellipse((x - r, y - r, x + r, y + r), fill=inkc)

    stroke(s["diag"], Z * 1.6)         # the band's new lower edge
    stroke(s["brow"], Z * 1.6)         # his right eyebrow
    full = Image.fromarray(arr.astype(np.uint8))
    full.paste(out.resize((cx1 - cx0, cy1 - cy0), Image.LANCZOS), (cx0, cy0))
    return full


def main():
    prev = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    for name, s in SPEC.items():
        im = fix(name, s)
        if prev:
            cx0, cy0, cx1, cy1 = s["crop"]
            w, h = (cx1 - cx0) * 6, (cy1 - cy0) * 6
            sheet = Image.new("RGB", (w * 2 + 20 + 300, max(h, 600)), "white")
            sheet.paste(Image.open(KF / f"{name}.orig.png").convert("RGB").crop(s["crop"]).resize((w, h), Image.LANCZOS))
            sheet.paste(im.crop(s["crop"]).resize((w, h), Image.LANCZOS), (w + 20, 0))
            # what the video shows: the still at 1080-wide scale, shown 2.5x
            f = 1080 / im.width
            vid = im.resize((1080, round(im.height * f)), Image.LANCZOS)
            cx, cy = (cx0 + cx1) / 2 * f, (cy0 + cy1) / 2 * f
            sheet.paste(vid.crop((round(cx - 60), round(cy - 60), round(cx + 60), round(cy + 180))).resize((300, 600)),
                        (w * 2 + 20, 0))
            sheet.save(Path(prev) / f"bandage_{name}.png")
        else:
            im.save(KF / f"{name}.png")
        print(name, "preview" if prev else "written")


if __name__ == "__main__":
    main()
