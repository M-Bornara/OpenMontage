"""HIT shot prototype (Mahdi 2026-11-25), no spend: the C2 explosion (a clip at NATURAL speed from 0.45 s) in a tight crop on the ledge, headroom added with the
sky_pad layer; the iron SPRITE (cut from the approved 1:34 iron, rigid) rises out of the head under an orange-ink comic burst that FOLLOWS the head and covers it
the whole time (rule 0b: the bar is never shown inside a head); sprite and burst slow to 40 % for 0.5 s; impact frame (3 frames), shake, whoosh; in the
callback version 0.2 s of Gage down follows (1.5 s in all). The geometry lives in comic_fx.py (HIT_*).
    python channels/storybook-medical/scripts/fx_hit.py     -> projects/fx-demo/renders/hit-cold-open.mp4, hit-callback-amber/cyan-magenta/mono.mp4"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import comic_fx as cf  # noqa: E402
import fx_demo as d  # noqa: E402

V = d.L / "assets/video/cold-c2-1080p30.mp4"
K = d.L / "assets/images/keyframes"
SPRITE = str(d.L / "assets/images/sprites/iron-hit-sprite.png")
CX, CY, ZOOM = cf.HIT_CROP
mk = lambda t, sc: {"t": t, "ease": "linear", "scale": sc, "x": round((0.5 - CX) * 100 * sc, 1), "y": round((0.5 - CY) * 100 * sc, 1)}
CROP = {"type": "keys", "keys": [mk(0, ZOOM), mk(1.7, ZOOM + 0.06)]}

if __name__ == "__main__":
    d.main("hit-cold-open", [("h1", 0.0, 1.3, V, CROP, {"in": cf.HIT_BASE_IN})], cf.hit_events(0.0, None, 1.3, SPRITE), 1.3, cf.hit_sfx(0.0), auto_sfx=False)
    for pal in ("amber", "cyan_magenta", "mono"):
        d.main(f"hit-callback-{pal}", [("h1", 0.0, 1.3, V, CROP, {"in": cf.HIT_BASE_IN}), ("h2", 1.3, 1.5, K / "cold-b5-dust-v1.png", {"type": "push", "from": 1.08, "to": 1.14})],
               cf.hit_events(0.0, pal, 1.5, SPRITE), 1.5, cf.hit_sfx(0.0), auto_sfx=False)
