"""Storybook Medical channel kit: one command per production step, driven by projects/<id>/episode.json.

Run from the repo root:
    python channels/storybook-medical/scripts/episode.py <step> <project-id> [names...]

Steps (in order):
    init        create the project workspace and an episode.json skeleton
    narrate     ElevenLabs v3 take -> speed + loudness + edge fades -> word timestamps   (~$0.07)
    refs        character sheets / location plates from episode.json "references"       ($0.15 each)
    keyframes   shot keyframes from episode.json "keyframes" (dependency-ordered)        ($0.15 each)
    clips       Kling v2.1 standard 5 s clips from episode.json "clips"                  ($0.28 each)
    music       MiniMax Music v2 candidates from episode.json "music.prompts"            ($0.03 each)
    sfx         fetch any SFX missing from the channel library (Freesound, CC0/CC-BY)    (free)
    sheet       contact sheet of keyframes for review                                     (free)
    build       props.json (shots, overlays, captions) + edit_decisions.json             (free)
    mix         narration + ducked music + SFX cues, -14 LUFS                             (free)
    render      Remotion render through video_compose (atelier) + final review           (free)
    credits     renders/CREDITS.txt for the video description                            (free)
    publish     renders/deliverables/: looping short.mp4, cover.jpg + crop check, captions.srt,
                per-platform titles/captions, upload checklist, credits                  (free)
    cost        print the paid-call ledger

Tiers: "tier": "premium" (default, V2: Nano Banana Pro + Kling v2.1) or "budget" (Nano Banana 2 +
MiniMax H3-max). Escalate a failed shot to premium without editing JSON:
    episode.py keyframes <id> sh14 --premium      episode.py clips <id> sh09 --premium
A single keyframe/clip may also pin "model"; "models": {...} overrides the tier.

Optional names limit refs/keyframes/clips/music to those entries (e.g. re-roll one keyframe).
Every paid call is appended to artifacts/cost_log.json.
"""
from __future__ import annotations

import base64
import io
import json
import re
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import yaml  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from tools.tool_registry import registry  # noqa: E402

PLAYBOOK = "storybook-medical"
VOICE = {"voice": "Liam", "model_id": "eleven-v3", "stability": 0.4, "speed": 1.2}
LOOP_SECONDS = 0.5  # Shorts/TikTok/Reels loop: last 0.5 s dissolves (picture) and crossfades (music) into the start
TEMPO = 1.14
CLIP_VARIANT = "v2.1/standard"
PRICES = {"image": 0.15, "clip": 0.28, "music": 0.03, "tts_per_1k_chars": 0.10}
# Channel defaults are the V2 setup. An episode may override them for experiments with
# "models": {"image": "nano-banana-2", "clip": "h3-max"} in episode.json.
IMAGE_MODELS = {"gemini-3-pro-image": 0.15, "nano-banana-2": 0.08}
CLIP_MODELS = {"kling-v2.1-standard": 0.28, "h3-max": 0.0325 * 5}
TIERS = {
    "premium": ("gemini-3-pro-image", "kling-v2.1-standard"),  # V2 pilot setup (default)
    "budget": ("nano-banana-2", "h3-max"),                      # tested on episode 2, ~$2.60
}
PREMIUM = TIERS["premium"]


def model_choice(ep: dict) -> tuple[str, str]:
    image, clip = TIERS[ep.get("tier", "premium")]
    m = ep.get("models", {})
    return m.get("image", image), m.get("clip", clip)


def split_premium(only) -> tuple[list[str], bool]:
    """`--premium` re-rolls the named items with the premium-tier model (escalation after a failed review)."""
    names = [n for n in only if n != "--premium"]
    return names, "--premium" in only


# ── helpers ──────────────────────────────────────────────────────────────

def proj(pid: str) -> Path:
    return REPO / "projects" / pid


def load_ep(pid: str) -> dict:
    return json.load(open(proj(pid) / "episode.json", encoding="utf-8"))


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def duration(path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).strip())


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", r.stderr, re.M)
    p = re.findall(r"^\s+Peak:\s+(-?[\d.]+) dBFS", r.stderr, re.M)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)


def peak_db(path) -> float:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    return float(re.findall(r"max_volume: (-?[\d.]+) dB", r.stderr)[-1])


def log_cost(pid: str, item: str, usd: float):
    p = proj(pid) / "artifacts/cost_log.json"
    rows = json.load(open(p)) if p.exists() else []
    rows.append({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "item": item, "usd": round(usd, 4)})
    json.dump(rows, open(p, "w"), indent=1)


def tools():
    registry.discover()
    return registry._tools


def style_prefix() -> str:
    return yaml.safe_load(open(REPO / f"styles/{PLAYBOOK}.yaml", encoding="utf-8"))["asset_generation"]["image_prompt_prefix"].strip()


def resolve_ref(pid: str, ref: str) -> str:
    """'kit:style-anchor.jpg' | 'ref:<name>' | 'kf:<shot>' | 'proj:<relative path>' | absolute/relative path."""
    p = proj(pid)
    if ref.startswith("kit:"):
        return str(KIT / "refs" / ref[4:])
    if ref.startswith("ref:"):
        return str(p / "assets/images/refs" / f"{ref[4:]}.png")
    if ref.startswith("kf:"):
        return str(p / "assets/images/keyframes" / f"{ref[3:]}.png")
    if ref.startswith("proj:"):
        return str(p / ref[5:])
    return str((REPO / ref) if not Path(ref).is_absolute() else Path(ref))


LOCK = ("Match the art style of the references EXACTLY: same ink line weight, same gouache brush texture, same two-tone "
        "cel shading, same amber/teal palette, same level of facial simplification. ")
TAIL = " No text, no labels, no captions, no watermark."


def gen_images(pid: str, section: str, out_dir: str, only: list[str]):
    only, premium = split_premium(only)
    ep = load_ep(pid)
    items = ep.get(section, {})
    names = [n for n in items if not only or n in only]
    out = proj(pid) / "assets/images" / out_dir
    out.mkdir(parents=True, exist_ok=True)
    nb = tools()["gemini_fal_image"]
    image_model, _ = model_choice(ep)
    style = style_prefix()
    done: set[str] = {n for n in items if (out / f"{n}.png").exists() and n not in names}

    def run(name):
        spec = items[name]
        refs = [resolve_ref(pid, r) for r in spec["refs"]]
        missing = [r for r in refs if not Path(r).exists()]
        if missing:
            return name, False, f"missing refs {missing}"
        frame = " Single frame from an animated film, not a model sheet." if section == "keyframes" else ""
        prompt = LOCK + spec.get("roles", "") + " " + spec["prompt"] + frame + f" Aspect {spec.get('aspect', '9:16')}." + TAIL + " " + style
        model = PREMIUM[0] if premium else spec.get("model", image_model)
        r = nb.execute({"model": model, "prompt": prompt, "image_paths": refs,
                        "aspect_ratio": spec.get("aspect", "9:16"), "resolution": "2K", "output_format": "png",
                        "safety_tolerance": "5", "output_path": str(out / f"{name}.png")})
        if not r.success:
            return name, False, (r.error or "")[:200]
        log_cost(pid, f"{section}:{name}:{model}", IMAGE_MODELS.get(model, PRICES["image"]))
        if section == "keyframes" and ep.get("dual_format", True):
            # Same moment recomposed for long-form 16:9, anchored on the approved 9:16 frame.
            wide = proj(pid) / "assets/images/keyframes16x9"
            wide.mkdir(parents=True, exist_ok=True)
            w = nb.execute({"model": model, "image_paths": [str(out / f"{name}.png")] + refs, "aspect_ratio": "16:9",
                            "resolution": "2K", "output_format": "png", "safety_tolerance": "5",
                            "output_path": str(wide / f"{name}.png"),
                            "prompt": ("Reference 1 is an approved vertical frame. Recompose EXACTLY this moment as a 16:9 "
                                       "widescreen frame from a slightly wider camera: same characters, faces, costumes, props, "
                                       "lighting and art style; extend the set naturally to the left and right; keep the main "
                                       "action centred. Other references are for identity only." + TAIL + " " + style)})
            if w.success:
                log_cost(pid, f"{section}16x9:{name}:{model}", IMAGE_MODELS.get(model, PRICES["image"]))
            else:
                return name, True, f"9:16 ok, 16:9 failed: {(w.error or '')[:150]}"
        return name, True, ""

    # dependency waves: an item waits for any kf:/ref: it references that is still being generated
    pending = list(names)
    while pending:
        def ready(n):
            deps = [r.split(":", 1)[1] for r in items[n]["refs"] if r.startswith(("kf:", "ref:"))]
            return all(d not in pending or d == n for d in deps)
        wave = [n for n in pending if ready(n)] or pending[:1]
        with ThreadPoolExecutor(6) as ex:
            for res in ex.map(run, wave):
                print(res)
        pending = [n for n in pending if n not in wave]
        done.update(wave)


# ── steps ────────────────────────────────────────────────────────────────

def step_init(pid: str, *_):
    from lib.checkpoint import init_project
    p = proj(pid)
    if not p.exists():
        init_project(pid, title=pid.replace("-", " ").title(), pipeline_type="animated-explainer")
    for d in ("assets/images/refs", "assets/images/keyframes", "assets/video", "assets/audio", "assets/music", "review", "renders"):
        (p / d).mkdir(parents=True, exist_ok=True)
    if not (p / "episode.json").exists():
        json.dump({
            "title": "", "playbook": PLAYBOOK,
            "narration": {"v3_text": "", "punch_words": []},
            "references": {}, "keyframes": {}, "clips": {},
            "music": {"prompts": {}, "selected": ""},
            "shots": [], "overlays": [], "sfx": [],
        }, open(p / "episode.json", "w", encoding="utf-8"), indent=2)
    print("ready:", p)


def step_narrate(pid: str, *_):
    ep, p = load_ep(pid), proj(pid)
    text = ep["narration"]["v3_text"]
    raw = p / "assets/audio/narration_raw.mp3"
    r = tools()["fal_elevenlabs_tts"].execute({"text": text, **VOICE, "output_path": str(raw)})
    if not r.success:
        raise SystemExit(r.error)
    log_cost(pid, "narration", len(text) / 1000 * PRICES["tts_per_1k_chars"])
    # speed + loudness only (see memory: narration-audio-processing)
    sped = p / "assets/audio/_sped.wav"
    ff("-i", str(raw), "-af", f"atempo={ep['narration'].get('tempo', TEMPO)}", "-ar", "48000", "-c:a", "pcm_s16le", str(sped))
    i, _ = loudness(sped)
    stage = p / "assets/audio/_stage.wav"
    lim = "alimiter=limit=0.79:attack=1:release=40:level=disabled:asc=1"
    ff("-i", str(sped), "-af", f"volume={-14 - i:.2f}dB,{lim}", str(stage))
    i2, _ = loudness(stage)
    d = duration(stage)
    out = p / "assets/audio/narration.wav"
    ff("-i", str(stage), "-af", f"volume={-14 - i2:.2f}dB,{lim},afade=t=in:st=0:d=0.015,afade=t=out:st={d - 0.08:.3f}:d=0.08,apad=pad_dur=0.5",
       "-ar", "48000", "-c:a", "pcm_s16le", str(out))
    sped.unlink(); stage.unlink()
    li, lp = loudness(out)
    print(f"narration.wav {duration(out):.2f}s  {li} LUFS  peak {lp} dBFS")
    r = tools()["azure_stt"].execute({"input_path": str(out), "language": "en-US"})
    words = r.data.get("word_timestamps") or [w for s in r.data.get("segments", []) for w in s.get("words", [])]
    json.dump(words, open(p / "artifacts/word_timestamps.json", "w", encoding="utf-8"), indent=1)
    print(f"{len(words)} words timed ->", " ".join(f"{w['word']}@{w['start']:.2f}" for w in words))


def step_refs(pid, *only):
    gen_images(pid, "references", "refs", list(only))


def step_keyframes(pid, *only):
    gen_images(pid, "keyframes", "keyframes", list(only))


def step_clips(pid, *only):
    only, premium = split_premium(only)
    ep, p = load_ep(pid), proj(pid)
    t = tools()
    _, clip_model = model_choice(ep)
    keep = (" Hand-painted 2D storybook animation. The camera stays completely still. Keep the art style, faces, costumes, "
            "colours and the room exactly as in the image. No new objects, no new people, no morphing, no text.")

    def run(sid):
        kf = p / "assets/images/keyframes" / f"{sid}.png"
        out = p / "assets/video" / f"{sid}.mp4"
        model = PREMIUM[1] if premium else ep["clips"][sid].get("model", clip_model)
        prompt = ep["clips"][sid]["motion"] + keep
        if model == "h3-max":
            r = t["h3_max_video"].execute({"model": "h3-max", "prompt": prompt, "image_path": str(kf), "duration": 5,
                                           "resolution": "768P", "prompt_expansion_mode": "balanced",
                                           "enable_safety_checker": False, "output_path": str(out)})
        else:
            im = Image.open(kf).convert("RGB").resize((1080, 1920), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=92)
            r = t["kling_video"].execute({"prompt": prompt, "operation": "image_to_video",
                                          "image_url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
                                          "model_variant": CLIP_VARIANT, "duration": "5", "aspect_ratio": "9:16",
                                          "output_path": str(out)})
        if r.success:
            log_cost(pid, f"clip:{sid}:{model}", r.cost_usd or CLIP_MODELS.get(model, PRICES["clip"]))
        return sid, model, r.success, (r.error or "")[:200]

    ids = [s for s in ep["clips"] if not only or s in only]
    with ThreadPoolExecutor(7) as ex:
        for res in ex.map(run, ids):
            print(res)


def step_music(pid, *only):
    ep, p = load_ep(pid), proj(pid)
    t = tools()
    for name, prompt in ep["music"]["prompts"].items():
        if only and name not in only:
            continue
        out = p / "assets/music" / f"{name}.mp3"
        r = t["fal_minimax_music"].execute({"prompt": prompt, "output_path": str(out)})
        if not r.success:
            print(name, False, r.error)
            continue
        log_cost(pid, f"music:{name}", PRICES["music"])
        stt = t["azure_stt"].execute({"input_path": str(out)})
        d = stt.data or {}
        txt = (d.get("text") or " ".join(s.get("text", "") for s in d.get("segments", []))).strip()
        print(f"{name}: {duration(out):.1f}s, vocals detected: {bool(txt)} {txt[:80]}")


def step_sfx(pid, *_):
    """Download any sfx named in episode.json that the channel library lacks (query = name with dashes as spaces)."""
    import requests
    ep = load_ep(pid)
    lib = KIT / "library/sfx"
    lib.mkdir(parents=True, exist_ok=True)
    credits_p = KIT / "library/sfx-credits.json"
    credits = json.load(open(credits_p)) if credits_p.exists() else {}
    env = {m.group(1): m.group(2).strip() for l in open(REPO / ".env", encoding="utf-8")
           if (m := re.match(r"\s*([A-Z_]+)\s*=\s*(.*?)\s*$", l)) and m.group(2)}
    ca = env.get("SSL_CERT_FILE") or True
    for name in sorted({c["name"] for c in ep["sfx"]}):
        if (lib / f"{name}.mp3").exists():
            continue
        q = next((c.get("query") for c in ep["sfx"] if c["name"] == name and c.get("query")), name.replace("-", " "))
        res = requests.get("https://freesound.org/apiv2/search/text/", verify=ca, timeout=30, params={
            "query": q, "filter": 'duration:[0.1 TO 60] license:("Creative Commons 0" OR "Attribution")',
            "fields": "id,name,duration,license,username,avg_rating,num_ratings,num_downloads,previews",
            "sort": "score", "page_size": "15", "token": env["FREESOUND_API_KEY"]}).json().get("results", [])
        if not res:
            print(f"{name}: NOT FOUND for '{q}' - add a 'query' to that cue")
            continue
        b = max(res, key=lambda s: s["avg_rating"] * min(s["num_ratings"], 20) + min(s["num_downloads"], 5000) / 1000)
        (lib / f"{name}.mp3").write_bytes(requests.get(b["previews"]["preview-hq-mp3"], verify=ca, timeout=60).content)
        credits[name] = {"file": f"{name}.mp3", "freesound_id": b["id"], "title": b["name"], "author": b["username"],
                         "license": b["license"], "duration": b["duration"], "url": f"https://freesound.org/s/{b['id']}/"}
        print(f"{name}: '{b['name']}' by {b['username']} ({'CC0' if 'zero' in b['license'] else 'CC-BY'}) - listen before use")
    json.dump(credits, open(credits_p, "w"), indent=1)


def step_sheet(pid, *_):
    ep, p = load_ep(pid), proj(pid)
    W, H, C = 300, 533, 6
    items = [(s["id"], s["source"]) for s in ep["shots"]]
    rows = (len(items) + C - 1) // C
    s = Image.new("RGB", (C * (W + 6), rows * (H + 6)), "white")
    d = ImageDraw.Draw(s)
    for i, (sid, src) in enumerate(items):
        path = Path(resolve_ref(pid, src))
        if path.suffix == ".mp4" and not path.exists():
            path = p / "assets/images/keyframes" / f"{path.stem}.png"  # clip not made yet: show its keyframe
        if path.suffix == ".mp4":
            frame = p / "review" / f"_{sid}.jpg"
            ff("-ss", "0.5", "-i", str(path), "-frames:v", "1", str(frame))
            path = frame
        if not path.exists():
            continue
        x, y = (i % C) * (W + 6), (i // C) * (H + 6)
        s.paste(Image.open(path).convert("RGB").resize((W, H)), (x, y))
        d.rectangle([x, y, x + 70, y + 26], fill="black")
        d.text((x + 6, y + 6), sid, fill="white")
    out = p / "review/_contact.jpg"
    s.save(out, quality=86)
    print(out)


def step_build(pid, *_):
    ep, p = load_ep(pid), proj(pid)
    rem = p / "remotion"
    if rem.exists():
        for f in ("StorybookShort.tsx", "Root.tsx", "index.tsx", "art-direction.md"):
            shutil.copy(KIT / "remotion" / f, rem / f)
    else:
        shutil.copytree(KIT / "remotion", rem)
    pub = rem / "public"
    (pub / "img").mkdir(parents=True, exist_ok=True)
    (pub / "vid").mkdir(parents=True, exist_ok=True)
    words_raw = json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8"))
    total = round(duration(p / "assets/audio/narration.wav"), 2)
    shots = []
    for s in ep["shots"]:
        src = Path(resolve_ref(p.name, s["source"]))
        if src.suffix.lower() == ".mp4":
            dst = pub / "vid" / f"{s['id']}.mp4"
            shutil.copy(src, dst)
            kind, rel = "video", f"vid/{s['id']}.mp4"
        else:
            dst = pub / "img" / f"{s['id']}.jpg"
            Image.open(src).convert("RGB").resize((1440, 2560), Image.LANCZOS).save(dst, "JPEG", quality=92)
            kind, rel = "image", f"img/{s['id']}.jpg"
        shots.append({"id": s["id"], "src": rel, "kind": kind, "start": s["start"], "end": s["end"],
                      "inPoint": s.get("in", 0), "motion": s.get("motion", {"type": "push"}),
                      "transitionIn": s.get("transition", "cut"), "darken": s.get("darken", 0)})
    shots[-1]["end"] = total
    punch = {w.lower() for w in ep["narration"].get("punch_words", [])}
    words = []
    for w in words_raw:
        t = w["word"]
        shown = "ST." if t.lower() == "st." else re.sub(r"[^\w'?$]", "", t)
        words.append({"word": shown, "start": round(w["start"], 3), "end": round(w["end"], 3),
                      "punch": re.sub(r"\W", "", t.lower()) in punch,
                      "breakAfter": bool(re.search(r"[.,?!]$", t)) and t.lower() != "st."})
    props = {"totalSeconds": total, "shots": shots, "overlays": ep["overlays"], "words": words,
             "wordsPerPage": 3, "captionY": 1180, "loopSeconds": ep.get("loop_seconds", LOOP_SECONDS)}
    json.dump(props, open(rem / "props.json", "w", encoding="utf-8"), indent=1)
    gaps = [(a["id"], b["id"]) for a, b in zip(shots, shots[1:]) if abs(a["end"] - b["start"]) > 0.02]
    edit = {
        "version": "1.0", "render_runtime": "remotion", "composition_mode": "atelier", "renderer_family": "animation-first",
        "cuts": [{"id": s["id"], "source": s["src"], "in_seconds": s["start"], "out_seconds": s["end"]} for s in shots],
        "bespoke": {"entry": str((rem / "index.tsx").resolve()), "composition_id": "StorybookShort",
                    "props_path": str((rem / "props.json").resolve()), "public_dir": str(pub.resolve()),
                    "art_direction": str((rem / "art-direction.md").resolve()), "concurrency": 8, "crf": 18},
        "metadata": {"playbook": PLAYBOOK, "audio": "assets/audio/mix.wav"},
    }
    json.dump(edit, open(p / "artifacts/edit_decisions.json", "w", encoding="utf-8"), indent=1)
    print(f"props: {len(shots)} shots, {len(ep['overlays'])} overlays, {len(words)} words, {total}s, gaps={gaps or 'none'}")


def step_mix(pid, *_):
    ep, p = load_ep(pid), proj(pid)
    narr = p / "assets/audio/narration.wav"
    total = round(duration(narr), 2)
    tmp = p / "assets/audio/_mix"
    tmp.mkdir(exist_ok=True)
    src = p / "assets/music" / f"{ep['music']['selected']}.mp3"
    L = ep.get("loop_seconds", LOOP_SECONDS)
    if duration(src) < total + L + 1:
        ff("-i", str(src), "-i", str(src), "-filter_complex", "[0:a][1:a]acrossfade=d=2:c1=tri:c2=tri[a]", "-map", "[a]",
           "-ar", "48000", str(tmp / "loop.wav"))
        src = tmp / "loop.wav"
    if L:
        # Bed plays source[L : L+total]; its last L seconds crossfade into source[0:L], so when the platform
        # loops back to 0 (which plays source[L...]) the music continues without a seam.
        ff("-i", str(src), "-filter_complex",
           f"[0:a]asplit=2[a][b];"
           f"[a]atrim={L}:{L + total},asetpts=PTS-STARTPTS,afade=t=out:st={total - L}:d={L}[body];"
           f"[b]atrim=0:{L},asetpts=PTS-STARTPTS,afade=t=in:d={L},adelay={int((total - L) * 1000)}|{int((total - L) * 1000)}[head];"
           f"[body][head]amix=inputs=2:duration=first:normalize=0[m]",
           "-map", "[m]", "-ar", "48000", "-ac", "2", str(tmp / "m.wav"))
    else:
        ff("-i", str(src), "-af", f"atrim=0:{total},afade=t=in:d=0.4,afade=t=out:st={total - 1.6}:d=1.6", "-ar", "48000", "-ac", "2", str(tmp / "m.wav"))
    i, _ = loudness(tmp / "m.wav")
    ff("-i", str(tmp / "m.wav"), "-af", f"volume={ep['music'].get('lufs', -22) - i:.2f}dB", str(tmp / "bed.wav"))
    inputs = ["-i", str(narr), "-i", str(tmp / "bed.wav")]
    parts = ["[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[narr][key]",
             "[1:a][key]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=450:makeup=1[music]"]
    labels = ["[narr]", "[music]"]
    lib = KIT / "library/sfx"
    for n, c in enumerate(ep["sfx"]):
        f = lib / f"{c['name']}.mp3"
        if not f.exists():
            raise SystemExit(f"missing sfx {f} - run the sfx step")
        inputs += ["-i", str(f)]
        gain = c.get("gain_db", -12) - 1 - peak_db(f)
        chain = f"[{n + 2}:a]aformat=sample_rates=48000:channel_layouts=stereo"
        # Library files can hold several hits or long beds; without an explicit "dur" cap one-shots at 3 s.
        d = c.get("dur") or min(3.0, duration(f))
        loop = ",aloop=loop=-1:size=2e9" if c.get("dur") and c["dur"] > duration(f) else ""
        chain += f"{loop},atrim=0:{d},afade=t=out:st={max(0, d - 0.2)}:d=0.2"
        ms = int(round(c["at"] * 1000))
        chain += f",volume={gain:.2f}dB,adelay={ms}|{ms}[s{n}]"
        parts.append(chain)
        labels.append(f"[s{n}]")
    parts.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=first:normalize=0,atrim=0:{total}[mix]")
    ff(*inputs, "-filter_complex", ";".join(parts), "-map", "[mix]", "-ar", "48000", str(tmp / "raw.wav"))
    i, _ = loudness(tmp / "raw.wav")
    out = p / "assets/audio/mix.wav"
    ff("-i", str(tmp / "raw.wav"), "-af", f"volume={-14 - i:.2f}dB,alimiter=limit=0.84:attack=1:release=40:level=disabled:asc=1", str(out))
    shutil.rmtree(tmp)
    li, lp = loudness(out)
    print(f"mix.wav {li} LUFS, peak {lp} dBFS, {len(ep['sfx'])} sfx cues")


def step_render(pid, *_):
    p = proj(pid)
    ed = json.load(open(p / "artifacts/edit_decisions.json", encoding="utf-8"))
    pp_path = p / "artifacts/proposal_packet.json"
    out = p / "renders/final.mp4"
    t0 = time.time()
    r = tools()["video_compose"].execute({"operation": "render", "edit_decisions": ed,
                                          "proposal_packet": json.load(open(pp_path)) if pp_path.exists() else None,
                                          "output_path": str(out), "audio_path": str(p / "assets/audio/mix.wav")})
    print("render:", r.success, r.error or "", f"{time.time() - t0:.0f}s")
    review = (r.data or {}).get("final_review", {})
    print("final review:", review.get("recommended_action"), review.get("issues_found"))
    if r.success:
        li, lp = loudness(out)
        print(f"{out}  {duration(out):.2f}s  {li} LUFS  peak {lp} dBFS")


def step_credits(pid, *_):
    """Write renders/CREDITS.txt (music + CC-BY sound effects + sources) for the video description."""
    ep, p = load_ep(pid), proj(pid)
    credits = json.load(open(KIT / "library/sfx-credits.json"))
    used = sorted({c["name"] for c in ep["sfx"]})
    lines = ["CREDITS", ""]
    lines.append(f"Music: original, generated with MiniMax Music v2 ({ep['music']['selected']})")
    lines.append("Narration: ElevenLabs v3. Illustrations/animation: AI-assisted, art-directed.")
    lines += ["", "Sound effects from Freesound.org (Creative Commons Attribution 4.0):"]
    for n in used:
        m = credits.get(n)
        if m and "zero" not in m["license"]:
            lines.append(f'- "{m["title"]}" by {m["author"]} - {m["url"]}')
    cc0 = [n for n in used if credits.get(n) and "zero" in credits[n]["license"]]
    lines.append(f"- plus {len(cc0)} CC0 (public domain) sounds")
    if ep.get("sources"):
        lines += ["", "Sources:"] + [f"- {s.split(' (')[0]}" for s in ep["sources"]]
    (p / "renders/CREDITS.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


def _srt_time(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _write_srt(words: list[dict], path: Path):
    """Caption cues of up to 7 words / 3 s, broken at sentence punctuation."""
    cues, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.?!,]$", w["word"]) and len(cur) >= 3 or len(cur) >= 7 or cur[-1]["end"] - cur[0]["start"] > 3.0:
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{_srt_time(c[0]['start'])} --> {_srt_time(c[-1]['end'] + 0.15)}", " ".join(w["word"] for w in c), ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def _cover_crops(cover: Path, out: Path):
    """Preview how the cover survives each platform crop: full 9:16, IG grid 3:4, 4:5 feed, TikTok UI overlay."""
    im = Image.open(cover).convert("RGB")
    W, H = im.size
    tiles = [("9:16 full", im.copy())]
    for label, h in (("IG grid 3:4", int(W * 4 / 3)), ("4:5 feed", int(W * 5 / 4))):
        top = (H - h) // 2
        tiles.append((label, im.crop((0, top, W, top + h))))
    tk = im.copy()
    d = ImageDraw.Draw(tk, "RGBA")
    d.rectangle([0, H - 320, W, H], fill=(255, 0, 0, 90))        # caption/UI zone
    d.rectangle([W - 140, H - 900, W, H - 320], fill=(255, 0, 0, 90))  # action buttons
    tiles.append(("TikTok UI", tk))
    th = 640
    row = [t.resize((int(t.width * th / t.height), th)) for _, t in tiles]
    sheet = Image.new("RGB", (sum(r.width + 12 for r in row), th + 40), "white")
    dd, x = ImageDraw.Draw(sheet), 0
    for (label, _), r in zip(tiles, row):
        sheet.paste(r, (x, 40))
        dd.text((x + 4, 10), label, fill="black")
        x += r.width + 12
    sheet.save(out, quality=86)


CHECKLIST = """## Upload checklist

**YouTube Shorts** (Studio on desktop)
- Upload `short.mp4`; paste title, description, tags.
- Thumbnail: upload `cover.jpg` if your account shows the custom-thumbnail option for Shorts; otherwise pick the frame closest to the cover.
- Subtitles → upload `captions.srt` (English).
- Audience: **No, it's not made for kids**. Category: Education. Add to the series playlist.
- Altered or synthetic content: our illustrated style is not realistic, so disclosure is not required; ticking it is harmless if unsure.
- After publishing: post and pin the pinned comment. When a long video exists, set it as the Short's **Related video**.

**TikTok**
- Upload `short.mp4`; Edit cover → upload `cover.jpg`; paste the TikTok caption.
- Turn on **AI-generated content** label (safe default for AI-assisted visuals). Allow Duet/Stitch.

**Instagram Reels**
- Upload `short.mp4`; Edit cover → Add from camera roll → `cover.jpg`; check the profile-grid preview.
- Paste the Instagram caption; add the AI label if Instagram prompts for it.

**Facebook Reels**
- Upload `short.mp4` with the Facebook caption and `cover.jpg`.

Credits: every description must include `CREDITS.txt` (CC-BY sound effects).
"""


def step_publish(pid, *_):
    """Assemble renders/deliverables/: short.mp4, cover.jpg, cover-crops.jpg, captions.srt, publish.md/json, CREDITS.txt."""
    ep, p = load_ep(pid), proj(pid)
    pub = ep.get("publish")
    if not pub:
        raise SystemExit('episode.json needs a "publish" section (cover, youtube, tiktok, instagram, facebook)')
    out = p / "renders/deliverables"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy(p / "renders/final.mp4", out / "short.mp4")

    # cover via the Remotion StorybookCover still (same fonts/colours as the video)
    c = pub["cover"]
    rem = p / "remotion"
    for f in ("StorybookShort.tsx", "Root.tsx", "index.tsx"):
        shutil.copy(KIT / "remotion" / f, rem / f)
    Image.open(resolve_ref(pid, c["image"])).convert("RGB").resize((1440, 2560), Image.LANCZOS).save(
        rem / "public/img/cover.jpg", "JPEG", quality=92)
    props = {"image": "img/cover.jpg", "title": c["title"], "kicker": c.get("kicker", ""),
             "accentWords": c.get("accent", []), "scale": c.get("scale", 1.05), "x": c.get("x", 0), "y": c.get("y", 0)}
    json.dump(props, open(rem / "cover-props.json", "w", encoding="utf-8"))
    composer = REPO / "remotion-composer"
    entry = tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    png = out / "cover.png"
    subprocess.run(["npx", "remotion", "still", str(entry), "StorybookCover", str(png), f"--props={(rem / 'cover-props.json').resolve()}",
                    f"--public-dir={(rem / 'public').resolve()}", "--log=error"], cwd=composer, check=True, shell=sys.platform == "win32")
    Image.open(png).convert("RGB").save(out / "cover.jpg", "JPEG", quality=88, optimize=True)
    png.unlink()
    _cover_crops(out / "cover.jpg", out / "cover-crops.jpg")

    _write_srt(json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8")), out / "captions.srt")
    step_credits(pid)
    shutil.copy(p / "renders/CREDITS.txt", out / "CREDITS.txt")
    credits = (p / "renders/CREDITS.txt").read_text(encoding="utf-8")

    yt = pub["youtube"]
    desc = yt["description"].strip() + "\n\n" + " ".join(yt.get("hashtags", [])) + "\n\n" + credits
    md = [f"# {ep['title']}", "", f"Length {duration(out / 'short.mp4'):.1f}s · 1080×1920 · -14 LUFS · loops seamlessly", "",
          "## YouTube Shorts", f"**Title:** {yt['title']}", "", "**Description:**", "```", desc, "```",
          f"**Tags:** {', '.join(yt.get('tags', []))}", "", f"**Pinned comment:** {yt.get('pinned_comment', '')}", ""]
    for plat in ("tiktok", "instagram", "facebook"):
        if plat in pub:
            md += [f"## {plat.title()}", "```", pub[plat]["caption"].strip(), "```", ""]
    md += [CHECKLIST]
    (out / "publish.md").write_text("\n".join(md), encoding="utf-8")
    json.dump({**pub, "youtube": {**yt, "full_description": desc}}, open(out / "publish.json", "w", encoding="utf-8"), indent=2)
    size = (out / "cover.jpg").stat().st_size / 1e6
    print(f"deliverables -> {out}\n  short.mp4, cover.jpg ({size:.2f} MB), cover-crops.jpg, captions.srt, publish.md, publish.json, CREDITS.txt")


def step_cost(pid, *_):
    p = proj(pid) / "artifacts/cost_log.json"
    rows = json.load(open(p)) if p.exists() else []
    by: dict[str, float] = {}
    for r in rows:
        k = r["item"].split(":")[0]
        by[k] = by.get(k, 0) + r["usd"]
    for k, v in sorted(by.items()):
        print(f"{k:12} ${v:.2f}")
    print(f"{'TOTAL':12} ${sum(by.values()):.2f}")


STEPS = {name[5:]: fn for name, fn in globals().items() if name.startswith("step_")}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in STEPS:
        print(__doc__)
        raise SystemExit(1)
    STEPS[sys.argv[1]](sys.argv[2], *sys.argv[3:])
