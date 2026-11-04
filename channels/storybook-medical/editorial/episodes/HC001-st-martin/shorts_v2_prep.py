"""HC001 Shorts v2: free composites from the long's approved 4K art (user review 2026-10-26: the Shorts used inaccurate
stills - three children in the canoe, food that never digests). Writes into the long's keyframe pool:
  v2-food-1h.png    the ONE-hour state (Beaumont 1833, exp. 1): s4.03 with the bread crumbling (from s4.05) and the cabbage
                    half gone (its right half replaced by the empty string of s4.05c, ragged edge). Same table, same tags.
  v2-family-canoe.png  wife + two children (claims C17): the long's family canoe on the 4K lake M21, left of the old canoe.
`python shorts_v2_prep.py [sheet]` - sheet writes a check image to the scratch dir given as the second argument."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[5]
KF = REPO / "projects/hc001-window-into-his-stomach/assets/images/keyframes"
CUT = REPO / "projects/_fxlab/remotion/public/cut"


def soft_ellipse(size, box, blur):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).ellipse(box, fill=255)
    return m.filter(ImageFilter.GaussianBlur(blur))


def food_1h():
    base = Image.open(KF / "s4.03.png").convert("RGB")
    base_src = base.copy()
    crumb = Image.open(KF / "s4.05.png").convert("RGB")
    gone = Image.open(KF / "s4.05c.png").convert("RGB")
    W, H = base.size
    # bread (measured on the 3 aligned stills): centre (3714, 1000)
    bx, by = 3714, 1000
    base.paste(crumb, (0, 0), soft_ellipse((W, H), (bx - 300, by - 210, bx + 300, by + 230), 25))
    # cabbage centre (4350, 770): half digested = the same cabbage at ~half size, still tied where the string enters it,
    # on the empty-string background of s4.05c (cut out by colour: its greens plus the dark ink outline around them)
    cx, cy = 4350, 770
    box = (cx - 330, cy - 300, cx + 330, cy + 300)
    clear = (cx - 420, cy - 380, cx + 420, cy + 380)          # wider than the leaf, so no old leaf edge survives
    base.paste(gone.crop(clear), clear[:2], soft_ellipse((840, 760), (10, 10, 830, 750), 14))
    leaf = base_src.crop(box).convert("RGB")
    hsv = np.array(leaf.convert("HSV"), dtype=np.int32)
    green = ((hsv[..., 0] > 40) & (hsv[..., 0] < 110) & (hsv[..., 1] > 70)).astype(np.uint8) * 255
    m = Image.fromarray(green).filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(2))
    leaf.putalpha(m)
    k = 0.55
    small = leaf.resize((round(660 * k), round(600 * k)), Image.LANCZOS)
    knot = (cx - 230, cy + 40)                                  # where the string enters the cabbage (left side)
    ox, oy = knot[0] - round((knot[0] - box[0]) * k), knot[1] - round((knot[1] - box[1]) * k)
    base.paste(small, (ox, oy), small)
    base.save(KF / "v2-food-1h.png")
    return base


def family_canoe():
    lake = Image.open(KF / "M21.png").convert("RGB")          # 5504 x 3072; the old canoe sits right of x ~ 3900
    canoe = Image.open(CUT / "prop-canoe-family-cut.png").convert("RGBA")
    w = 1500
    canoe = canoe.resize((w, round(canoe.height * w / canoe.width)), Image.LANCZOS)
    x, bottom = 900, 2330                                       # hull bottom; water starts at y ~ 1720
    sink = round(canoe.height * 0.14)                           # the lower 14 % of the hull under the waterline
    y = bottom - canoe.height
    a = np.array(canoe.split()[3], dtype=np.float32)
    ramp = np.ones(canoe.height, np.float32)
    ramp[-sink:] = np.linspace(1, 0.15, sink)
    canoe.putalpha(Image.fromarray((a * ramp[:, None]).astype(np.uint8)))
    # reflection: flipped, faded, rippled; contact shadow on the water
    refl = canoe.transpose(Image.FLIP_TOP_BOTTOM)
    ra = np.array(refl.split()[3], dtype=np.float32) * np.linspace(0.22, 0, refl.height)[:, None]
    refl.putalpha(Image.fromarray(ra.astype(np.uint8)))
    refl = refl.filter(ImageFilter.GaussianBlur(7))
    out = lake.convert("RGBA")
    refl = refl.crop((0, sink, refl.width, refl.height))      # mirrored about the waterline, drawn only below it
    out.alpha_composite(refl, (x, bottom - sink))
    sh = Image.new("RGBA", lake.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((x + 60, bottom - sink - 40, x + w - 60, bottom - sink + 70), fill=(10, 25, 35, 90))
    out = Image.alpha_composite(out, sh.filter(ImageFilter.GaussianBlur(30)))
    out.alpha_composite(canoe, (x, y))
    # ripples behind the stern
    rp = Image.new("RGBA", lake.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(rp)
    for i in range(4):
        d.arc((x + w - 120 + i * 90, bottom - sink - 20 - i * 6, x + w + 160 + i * 150, bottom - sink + 40 + i * 6), 200, 340,
              fill=(235, 245, 250, 110 - i * 22), width=6)
    out = Image.alpha_composite(out, rp.filter(ImageFilter.GaussianBlur(2)))
    out.convert("RGB").save(KF / "v2-family-canoe.png")
    return out


if __name__ == "__main__" and (len(sys.argv) < 2 or sys.argv[1] == "sheet"):
    f, c = food_1h(), family_canoe()
    if len(sys.argv) > 2 and sys.argv[1] == "sheet":
        f.crop((2900, 300, 4900, 1500)).resize((1000, 600)).save(Path(sys.argv[2]) / "v2-food-1h.jpg")
        c.convert("RGB").crop((300, 900, 3000, 2900)).resize((1080, 800)).save(Path(sys.argv[2]) / "v2-canoe.jpg")


def soft_wound():
    """s1.13-soft.png (+ the cut's 2880 jpg): the open wound with its drips, and the blood patch on the shirt, blurred
    and calmed (user review 2026-10-26: "too harsh and bloody" for YouTube; "the blur right on the wound only").
    Two ovals measured on the 4K still (a colour mask also caught the red sash, the knuckles and the floor), feathered so
    the blur has no edge. Writes a check sheet."""
    im = Image.open(KF / "s1.13.png").convert("RGB")
    W, H = im.size
    box = (round(W * 0.40), round(H * 0.45), round(W * 0.72), round(H * 0.88))   # the check sheet's crop
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((3105 - 175, 2350 - 250, 3105 + 175, 2350 + 250), fill=255)       # the wound and the drips below it
    d.ellipse((3414 - 95, 2150 - 130, 3414 + 95, 2150 + 130), fill=255)        # the blood patch on the shirt
    m = m.filter(ImageFilter.GaussianBlur(30))
    soft = im.filter(ImageFilter.GaussianBlur(22))
    soft = Image.blend(soft, soft.convert("L").convert("RGB"), 0.35)            # a little less red, still the same colours
    out = Image.composite(soft, im, m)
    out.save(KF / "s1.13-soft.png")
    out.resize((2880, 1607), Image.LANCZOS).save(CUT / "s1.13-soft.jpg", quality=92)
    return im, out, m, box


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "wound":
    im, out, m, box = soft_wound()
    c = (box[0] - 200, box[1] - 200, box[2], box[3])
    a, b = im.crop(c), out.crop(c)
    mm = Image.composite(Image.new("RGB", a.size, (40, 230, 90)), a, m.crop(c).point(lambda v: v // 2))
    sheet = Image.new("RGB", (a.width * 3, a.height))
    for i, x in enumerate((a, mm, b)):
        sheet.paste(x, (i * a.width, 0))
    sheet.thumbnail((2400, 2400))
    sheet.save(Path(sys.argv[2]) / "wound-check.jpg", quality=88)
