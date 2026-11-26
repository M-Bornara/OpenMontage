"""Layered shots, the Python side (plan/layered-animation.md; user 2026-11-16). The motion itself lives in
remotion/Stage.tsx (<Actor>, <LayerStack>); this module does what Python must do for it:

    lint_motion(shots)   a story shot with only CAM motion (push / pan / zoom) fails unless it is marked "breath"
    lint_hero_size(shots, proj)   a layered (HERO) shot whose biggest moving actor never fills 1/3 of the frame
    sfx_cues(ep)         sound fired from actor keyframes -> ordinary sfx cues for episode.py sfx / mix
    all_sfx(ep)          ep["sfx"] + the keyframe cues (what step_sfx and step_mix read)
    build_layers(...)    episode.json shot "layers" -> props.json (plate, masks and sprites fitted / copied to public/)

A shot's layers, written in edit_<ep>.py (all x, y = fractions of the 9:16 FRAME; t = seconds after the shot starts):

    c.shot(t, KF + "s3.png", push(...), layers={
        "bg": "proj:assets/images/plates/s3-empty.png",          # the clean plate (replaces the still)
        "masks": {"hand": "proj:assets/images/plates/fx/s3-empty-hand.mask.png"},
        "glows": [{"x": 0.95, "y": 0.52, "r": 220, "strength": 0.22}],
        "actors": [{"id": "mosquito", "sprites": "proj:assets/images/sprites/mosquito/sprites.json",
                    "states": {"fly": {"fps": 48}, "land": {"fps": 10, "loop": False, "then": "rest"}},
                    "w": 0.07, "anchor": [0.5, 0.5], "face": "path", "wobble": {...}, "shadow": {...},
                    "keys": [{"t": 0.1, "x": 1.1, "y": 0.6, "z": 1.6, "state": "fly",
                              "sfx": {"name": "mosquito-buzz", "until": "contact", "fade_out": 0.25}},
                             ...,
                             {"t": 2.3, "x": 0.66, "y": 0.55, "z": 1, "state": "land", "contact": {"squash": 0.12}}]}],
        "fg": [], "mg": [], "three": []})
    Mark a deliberate pause shot with breath=True (lint).
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

# ShortFx kinds that MOVE something in the picture (an action); spot / tint / glow / glint / light only point at things
MOVING_FX = {"wiggle", "wag", "shake", "nudge", "pulse", "frost", "particles", "travel", "ecg", "lcd"}
CAM_ONLY = "only CAM motion (push/pull/pan/snap)"


def _actor_moves(a: dict) -> bool:
    keys = a.get("keys", [])
    moved = len({(round(k["x"], 3), round(k["y"], 3), round(k.get("z", 1), 3)) for k in keys}) > 1
    states = len({k["state"] for k in keys if k.get("state")}) > 1
    procedural = any(a.get(p) for p in ("wobble", "bob", "breath", "flap"))
    return moved or states or procedural or a.get("kind") == "3d"


def moving_layers(shot: dict) -> list[str]:
    """What in this shot moves besides the camera (empty = CAM only)."""
    out = []
    lay = shot.get("layers") or {}
    for group in ("mg", "actors", "three", "fg"):
        out += [f"{group}:{a['id']}" for a in lay.get(group, []) if _actor_moves(a)]
    out += [f"fx:{e['kind']}" for e in shot.get("fx", []) if e.get("kind") in MOVING_FX]
    out += ["draw"] * bool(shot.get("draw"))
    if str(shot.get("source", "")).lower().endswith(".mp4"):
        out.append("clip")
    return out


def lint_motion(shots: list[dict]) -> list[str]:
    """story-craft Rule 0 / production-v3 §2: every story shot carries an action besides the camera, unless it is a
    deliberate breath between beats (shot "breath": True)."""
    return [f"shot {s['id']} ({Path(str(s.get('source', ''))).name}): {CAM_ONLY}; give it a moving layer "
            f"(plan/layered-animation.md) or mark it breath=True"
            for s in shots if not s.get("breath") and not moving_layers(s)]


# L53 (user 2026-11-19, Gage S1: the 2a arm, the 2b hammers, the 0:43 head + hand): "do not just grab a piece of picture
# and keep animating it". A wag / shake / nudge moves a piece CUT OUT OF THE STILL over an inpainted plate: the edge and the
# filled hole show. Anything that moves is a separately generated prop / actor sprite (layered-shot skill), or the shot
# holds still. A cut-out fx passes only with "cut": "approved" (the user saw the cut and called it perfect).
CUTOUT_FX = {"wag", "shake", "nudge"}


def lint_cutouts(shots: list[dict]) -> list[str]:
    return [f"L53: shot {s['id']} fx {e['kind']} ({Path(str(e.get('mask', ''))).name}): a piece cut out of the still is "
            f"animated; generate it as a separate prop / actor sprite, or drop the move (\"cut\": \"approved\" only after "
            f"the user OKs the cut)"
            for s in shots for e in s.get("fx", [])
            if e.get("kind") in CUTOUT_FX and str(e.get("cut", "")).lower() != "approved"]


HERO_MIN = 1 / 3   # user 2026-11-18: "in a HERO shot the moving subject fills at least 1/3 of the frame" (phone)


def lint_hero_size(shots: list[dict], proj: Path) -> list[str]:
    """Each layered shot: the largest on-screen extent (width or height, as a fraction of the frame) of its biggest
    moving actor at any key, times the camera's zoom at that moment (push / pull scale at the key's time), must reach
    1/3. Sprite aspect from its sprites.json canvas."""
    out = []
    for s in shots:
        lay = s.get("layers") or {}
        if not lay or s.get("breath"):
            continue
        m, dur = s.get("motion") or {}, max(1e-6, s["end"] - s["start"])
        def cam(t: float) -> float:
            if m.get("type") in ("push", "pull"):
                a = m.get("from", 1.04 if m["type"] == "push" else 1.18)
                b = m.get("to", 1.18 if m["type"] == "push" else 1.04)
                return a + (b - a) * min(1.0, t / dur)
            if m.get("type") == "keys" and m.get("keys"):    # keyframed camera: linear between its keys is enough here
                ks = m["keys"]
                if t <= ks[0]["t"]:
                    return ks[0]["scale"]
                for p, q in zip(ks, ks[1:]):
                    if t <= q["t"]:
                        return p["scale"] + (q["scale"] - p["scale"]) * (t - p["t"]) / max(1e-6, q["t"] - p["t"])
                return ks[-1]["scale"]
            return m.get("scale", 1.04)
        best = 0.0
        for g in ("mg", "actors", "three", "fg"):
            for a in lay.get(g, []):
                keys = a.get("keys", [])
                if len(keys) < 2 and not a.get("breath"):
                    continue
                sp = str(a.get("sprites", ""))
                f = proj / sp.split(":", 1)[1] if sp.startswith("proj:") else Path(sp)
                try:
                    cw, ch = json.load(open(f))["canvas"]
                    aspect = ch / cw
                except Exception:
                    aspect = a.get("aspect", 1.0)
                for k in keys:
                    z = k.get("z", 1.0) * cam(k["t"])
                    best = max(best, a["w"] * z, a["w"] * z * aspect * 1080 / 1920)
        if best < HERO_MIN:
            out.append(f"shot {s['id']}: the moving subject fills at most {best:.0%} of the frame (HERO rule: >= 33%; "
                       f"bring it closer, push in, or use a closer plate)")
    return out


def _until(keys: list[dict], i: int, until) -> float | None:
    """Time the sound started at keys[i] ends: a number (seconds in the shot), "contact", or a state name."""
    if isinstance(until, (int, float)):
        return float(until)
    for k in keys[i + 1:]:
        if (until == "contact" and k.get("contact")) or k.get("state") == until:
            return k["t"]
    return None


def sfx_cues(ep: dict) -> list[dict]:
    """Every actor keyframe with `sfx` -> a cue on the episode timeline. sfx = "name" or
    {name, gain (dB, default -15), until ("contact" | state | seconds), dur, fade_in, fade_out, query}."""
    cues = []
    for s in ep.get("shots", []):
        lay = s.get("layers") or {}
        for group in ("mg", "actors", "three", "fg"):
            for a in lay.get(group, []):
                keys = a.get("keys", [])
                for i, k in enumerate(keys):
                    for x in (k.get("sfx") if isinstance(k.get("sfx"), list) else [k.get("sfx")] if k.get("sfx") else []):
                        x = {"name": x} if isinstance(x, str) else dict(x)
                        cue = {"name": x["name"], "at": round(s["start"] + k["t"], 3), "gain_db": x.get("gain", -15),
                               "layer": f"{s['id']}/{a['id']}"}
                        end = _until(keys, i, x["until"]) if "until" in x else None
                        if end is not None:
                            cue["dur"] = round(end - k["t"], 3)
                        elif "dur" in x:
                            cue["dur"] = x["dur"]
                        for f in ("fade_in", "fade_out", "query", "in"):
                            if f in x:
                                cue[f] = x[f]
                        cues.append(cue)
    return cues


def all_sfx(ep: dict) -> list[dict]:
    return sorted(ep.get("sfx", []) + sfx_cues(ep), key=lambda c: c["at"])


def _sprite_states(spec: dict, resolve) -> tuple[dict, dict]:
    """Read a sprite set (fx_prep.sheet's sprites.json) and merge the shot's per-state timing over it."""
    sj = Path(resolve(spec["sprites"]))
    meta = json.load(open(sj, encoding="utf-8"))
    states = {}
    for name, files in meta["frames"].items():
        st = {"frames": [str(sj.parent / f) for f in files], "fps": 12, "loop": True}
        st.update(spec.get("states", {}).get(name, {}))
        states[name] = st
    return states, meta


def build_layers(shot: dict, pid: str, pub: Path, frame_size, fit_frame, resolve_ref) -> dict:
    """episode.json shot["layers"] -> props layers: masks fitted like the still (fit_frame), sprite frames copied to
    public/layers/, sprite aspect from the set's canvas, sfx stripped from the keys the renderer gets."""
    lay = shot["layers"]
    out_dir = pub / "layers"
    out_dir.mkdir(exist_ok=True)
    sid = shot["id"]
    resolve = lambda r: resolve_ref(pid, r)  # noqa: E731
    props = {"masks": {}, "glows": lay.get("glows", [])}
    for name, ref in (lay.get("masks") or {}).items():
        dst = out_dir / f"{sid}-mask-{name}.png"
        fit_frame(Path(resolve(ref)), dst, frame_size, shot.get("focus", 0.5))
        props["masks"][name] = f"layers/{dst.name}"
    for group in ("mg", "actors", "three", "fg"):
        acts = []
        for a in lay.get(group, []):
            a = json.loads(json.dumps(a))
            for k in a.get("keys", []):
                k.pop("sfx", None)
            if a.get("sprites"):
                states, meta = _sprite_states(a, resolve)
                for st_name, st in states.items():
                    pubs = []
                    for j, f in enumerate(st["frames"]):
                        dst = out_dir / f"{sid}-{a['id']}-{st_name}-{j}.png"
                        shutil.copy(f, dst)
                        pubs.append(f"layers/{dst.name}")
                    st["frames"] = pubs
                a["states"] = states
                cw, ch = meta["canvas"]
                a.setdefault("aspect", round(ch / cw, 4))
                a.setdefault("anchor", meta.get("anchor", [0.5, 0.5]))
                a.pop("sprites")
            acts.append(a)
        if acts:
            props[group] = acts
    return props


def layer_plan(shot: dict) -> list[tuple[str, str, str]]:
    """The shot's layer plan as rows (layer, what, motion) for the storyboard page and the review sheet."""
    lay = shot.get("layers") or {}
    rows = [("BG", Path(str(lay.get("bg") or shot.get("source"))).name, "static plate" + (" + glow" if lay.get("glows") else ""))]
    for group, label in (("mg", "MG"), ("actors", "ACTOR"), ("three", "3D"), ("fg", "FG")):
        for a in lay.get(group, []):
            keys = a.get("keys", [])
            states = " → ".join(dict.fromkeys(k["state"] for k in keys if k.get("state")))
            extra = [p for p in ("wobble", "bob", "breath", "flap", "shadow", "behind") if a.get(p)]
            rows.append((label, a["id"], f"{len(keys)} keys {keys[0]['t']:.2f}–{keys[-1]['t']:.2f} s"
                         + (f"; states {states}" if states else "") + (f"; {', '.join(extra)}" if extra else "")))
    return rows
