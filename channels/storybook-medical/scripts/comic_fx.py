"""Comic effects kit, Python half (Mahdi 2026-11-25). The drawn and animated presets are Remotion (remotion/ComicFx.tsx, events in the
episode's "comic_fx" list); this file holds what is better done on pixels or on the mix:

  PRESETS            name -> what it does, where to use it, sound hook (the table plan/comic-fx-presets.md is written from)
  sfx_for(events)    the sound hooks: whoosh / impact / bass hit cues from the FREE channel library for a list of events
  recolor_blood      mask + hue shift: red -> green / orange / black ink on a still (a still in, a still out; the original stays)
  list               python channels/storybook-medical/scripts/comic_fx.py list
  recolor            python channels/storybook-medical/scripts/comic_fx.py recolor <in.png> <out.png> green|orange|ink [--mask mask.png]

Rules: effects are LAYERS. Nothing here changes a clip's speed or length, and none of it freezes a frame.
"""
from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

# the free library names behind the three sound hooks (channels/storybook-medical/library/sfx)
SOUND = {"whoosh": ("whoosh", -16.0), "impact": ("stamp-thud", -10.0), "bass_hit": ("boom-low", -8.0), "metal": ("metal-clank", -14.0)}

PRESETS = [
    # (name, what it does, where to use it, sound hook)
    ("impact_frame", "2-4 frames of white (or flickering inverted ink): starburst, halftone dots, speed lines; then screen shake and an RGB split that decay over 0.4 s",
     "THE moment a story beat lands: the iron strikes, the diagnosis, the reveal. One per act at most.", "bass hit + impact"),
    ("comic_burst", "a spiky starburst with halftone fill and a hard ink shadow that pops in with overshoot over a masked area",
     "hiding violent detail the rules say to soften (rule 0b): put it where the wound or the blood would show.", "impact"),
    ("onomatopoeia", "hand-lettered word (BOOM, KRAK, ZAP) with a thick ink outline, hard block shadow, skew and an overshoot pop",
     "the sound made visible, on the same frame as the burst or on a small action (a spark, a latch). Our own overlay, never text inside a generated image.", "none (the burst carries it)"),
    ("recolor_blood", "mask + hue shift of red to green, orange or black ink on a still (Python: comic_fx.py recolor)",
     "a still where red would read as gore: shift before the cut, keep the original.", "none"),
    ("halftone_flashback", "benday dots over the picture plus a palette grade (amber duotone, cyan-magenta plates printed off register, or mono)",
     "a callback to an earlier moment or a memory; pick one palette per episode and keep it.", "none"),
    ("line_boil", "the ink lines wobble; the noise re-seeds at a low frame rate (8 fps) so the picture feels hand-redrawn",
     "stills that would feel dead, and under a flashback grade. Subtle: amount 4-7.", "none"),
    ("panel_wipe", "a skewed comic panel with an ink border sweeps across; the cut sits under it at the middle of the event",
     "change of place or time inside a chapter, instead of a plain cut.", "whoosh"),
    ("split_panel", "2 or 3 framed pictures slide in one after another over paper gutters with slanted edges",
     "two or three things at once: the doctors, the three accounts, before and after.", "whoosh"),
    ("zoom_punch", "a fast push (reaches the peak in the first fifth) with a little blur, then settles back",
     "a beat on a word or a hit; 0.08-0.16 is a nudge, more is a shout.", "bass hit (soft)"),
    ("whip_pan", "the picture slides off with horizontal motion blur and the next one slides in; the cut is at the middle of the event",
     "a hard change of place at speed (the coach, the ship).", "whoosh"),
    ("dust", "soft dust particles drift and thin out over a region (count, size, drift, colour); a layer on a still", "settling dust after a blast, a shaft of light, a quiet aftermath: pair it with a slow push on the still.", "wind / ringing ears (free library)"),
    ("hit_shot", "the iron passes through the head, the head never shown: a rigid iron sprite flies from below the jaw through the head and out the top while an orange-ink comic burst with an ink splash covers the head; sprite and burst slow to 40 % for 0.5 s, the footage under them stays at natural speed",
     "the moment the iron goes through (the cold open, the three callbacks): put it over the C2 explosion, impact frame + shake + whoosh with it (rule 0b).", "bass hit + impact + whoosh"),
    ("glint", "a soft white band sweeps along a region with a four-point flare at the end", "a metal object shown still (the bar of iron): a bit of life without moving the picture.", "none"),
    ("screen_shake", "a decaying shake of the whole picture (also built into impact_frame)", "any heavy hit.", "impact"),
    ("rgb_split", "red and blue channels slide apart and re-join (also built into impact_frame)", "shock, a glitch of memory.", "none"),
]


def sfx_for(events: list[dict]) -> list[dict]:
    """The sound hooks as episode "sfx" cues (name, at, gain_db) for the events; free library files only."""
    cues: list[dict] = []

    def add(hook: str, at: float, gain: float | None = None, **kw):
        name, g = SOUND[hook]
        cues.append({"name": name, "at": round(at, 2), "gain_db": g if gain is None else gain, **kw})

    for e in events:
        p, at = e["preset"], e["at"]
        if p == "impact_frame":
            add("bass_hit", at); add("impact", at + 0.02)
        elif p == "hit_shot":                                   # impact frame + shake are their own events; the pass gets a whoosh and a soft hit
            add("whoosh", at + 0.25, -14.0)
        elif p == "comic_burst":
            add("impact", at, -14.0)
        elif p in ("panel_wipe", "split_panel"):
            add("whoosh", at + e.get("dur", 0.6) * 0.15)
        elif p == "whip_pan":
            add("whoosh", at + e.get("dur", 0.5) * 0.1, -13.0)
        elif p == "zoom_punch":
            add("bass_hit", at, -16.0)
        elif p == "screen_shake":
            add("impact", at, -14.0)
    return sorted(cues, key=lambda c: c["at"])


def recolor_blood(src: Path, out: Path, mode: str = "green", mask: Path | None = None, feather: int = 5, min_sat: int = 110) -> Path:
    """Hue-shift the red inside a mask. mode: "green" | "orange" | "ink" (black ink with a cold sheen). With no mask file the mask is
    every strongly red, saturated pixel (skin has red hue too: ALWAYS paint a mask for a real shot, white = recolour; min_sat lowers the saturation floor for darker reds). The original is never touched."""
    im = cv2.imread(str(src))
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    red = (((h < 10) | (h > 170)) & (s > min_sat) & (v > 40)).astype(np.float32)
    m = red if mask is None else cv2.imread(str(mask), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0 * red
    if mask is not None and m.max() == 0:                         # a mask over non-red pixels: trust the mask
        m = cv2.imread(str(mask), cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255.0
    m = cv2.GaussianBlur(m, (0, 0), feather)[..., None]
    out_hsv = hsv.copy()
    if mode == "green":
        out_hsv[..., 0] = 62                                      # OpenCV hue 0-180: 62 = a sickly green
    elif mode == "orange":
        out_hsv[..., 0] = 14
        out_hsv[..., 1] = np.clip(s * 0.95, 0, 255)
    elif mode == "ink":
        out_hsv[..., 1] = np.clip(s * 0.18, 0, 255)               # nearly colourless
        out_hsv[..., 0] = 105                                     # with a cold blue-black sheen
        out_hsv[..., 2] = np.clip(v * 0.22, 0, 255)
    else:
        raise ValueError("mode: green | orange | ink")
    rec = cv2.cvtColor(out_hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    res = im.astype(np.float32) * (1 - m) + rec * m
    out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out), np.clip(res, 0, 255).astype(np.uint8))
    return out


# ── the HIT shot (Mahdi 2026-11-25): geometry shared by fx_hit.py (the prototype) and the long's edit script ─────────────────────────────────────────────
HIT_BASE_IN = 1.0                       # the HIT uses C2 frames from 1.0 s on; the blast shot (c2) shows only 0.15-1.0 s, so no frame is shown twice
HIT_CROP = (0.25, 0.164, 2.2)           # crop centre (frame fractions) and zoom; the footage is shifted down 14 % of the frame (headroom = the sky_pad layer)
HIT_HEAD = (36.4, 33.0)                 # the hat/head in the crop at the shot start (% of the frame)
# where the head is, by seconds from the shot start (C2 clip 1.0 s on: he stands with his arms up until ~1.3 s, then sinks into the smoke; read off a sheet of the
# footage, % of the HIT frame, shift included)
HIT_TRACK = [[0.0, 36.4, 33.0], [0.1, 34.6, 36.7], [0.2, 34.5, 37.6], [0.3, 33.5, 39.0], [0.4, 35.0, 45.4], [0.5, 35.3, 48.1], [0.6, 34.2, 51.3],
             [0.7, 38.3, 56.7], [0.8, 39.4, 60.8], [0.9, 39.9, 61.3], [1.0, 38.3, 61.3], [1.1, 39.1, 61.8], [1.2, 39.3, 62.7], [1.3, 40.4, 62.7]]
# the footage's own top-edge sky colour by seconds from the shot start (median of the top rows of the crop's columns; the smoke darkens it from 0.7 s)
HIT_SKY = [[0.0, 207, 223, 213], [0.1, 208, 224, 214], [0.2, 208, 224, 213], [0.3, 208, 223, 212], [0.4, 207, 222, 212], [0.5, 206, 221, 210], [0.6, 205, 220, 208],
           [0.7, 200, 213, 202], [0.8, 180, 164, 153], [0.9, 177, 152, 140], [1.0, 171, 133, 106], [1.1, 168, 128, 99], [1.2, 165, 127, 102], [1.3, 160, 126, 103]]


def hit_events(t0: float, palette: str | None, graded_to: float, sprite: str) -> list[dict]:
    """The comic-kit events of one HIT shot that starts at t0 (absolute seconds): sky headroom, a 1-frame impact frame, the iron sprite flying through the head
    (a head-following ellipse mask hides the bar wherever it overlaps the head; a small spark where it enters and one where it leaves, no wider than the head, with a few
    orange-ink flecks; the slow window is 0.5 s at 40 %), a shake and, when palette is given, a halftone grade for graded_to seconds. The C2 footage under it is its own
    shot (natural speed)."""
    ev = [{"preset": "sky_pad", "at": round(t0, 2), "dur": 1.3, "pad": 14, "fade": 16, "colors": HIT_SKY},
          {"preset": "impact_frame", "at": round(t0, 2), "frames": 1, "x": HIT_HEAD[0], "y": HIT_HEAD[1]},
          {"preset": "hit_shot", "at": round(t0, 2), "dur": 1.3, "x": HIT_HEAD[0], "y": HIT_HEAD[1], "w": 4.4, "h": 7.8, "sprite": sprite, "sprite_len": 700,
           "from": [35.0, 40.0], "to": [40.0, -30.0], "color": "#FF8A1F", "slow_at": 0.43, "slow_dur": 0.5, "rate": 0.4, "track": HIT_TRACK,
           "mask": [50, 62, 8], "speed": 1750, "pass_tau": 0.45},
          {"preset": "screen_shake", "at": round(t0 + 0.1, 2), "dur": 0.5, "strength": 12}]
    if palette:
        ev.append({"preset": "halftone_flashback", "at": round(t0, 2), "dur": round(graded_to, 2), "palette": palette, "dot": 9})
    return ev


def hit_sfx(t0: float) -> list[dict]:
    return [{"name": "boom-low", "at": round(t0, 2), "gain_db": -8.0}, {"name": "stamp-thud", "at": round(t0 + 0.02, 2), "gain_db": -10.0},
            {"name": "whoosh", "at": round(t0 + 0.25, 2), "gain_db": -14.0}]


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["list"]:
        for n, what, where, snd in PRESETS:
            print(f"{n:20s} {what}\n{'':20s} use: {where}  [sound: {snd}]")
    elif a[:1] == ["recolor"] and len(a) >= 4:
        mk = Path(a[a.index("--mask") + 1]) if "--mask" in a else None
        print(recolor_blood(Path(a[1]), Path(a[2]), a[3], mk))
    else:
        print(__doc__)
