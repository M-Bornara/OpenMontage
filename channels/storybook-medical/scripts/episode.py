"""Storybook Medical channel kit: one command per production step, driven by projects/<id>/episode.json.

Run from the repo root:
    python channels/storybook-medical/scripts/episode.py <step> <project-id> [names...]

Steps (in order):
    init        create the project workspace and an episode.json skeleton
    narrate     ElevenLabs v3 take -> speed + loudness + edge fades -> word timestamps   (~$0.07)
    refs        character sheets / location plates from episode.json "references"       (~$0.13 each)
    keyframes   shot keyframes from episode.json "keyframes" (dependency-ordered)        (~$0.13 each)
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
    thumbs      long-video thumbnails A/B/C + phone-size check (plan/thumbnail-craft.md)  (~$0.07 each, batch)
    covers      Shorts cover poster art, 1 per Short                                      (~$0.07, batch)
    cost        print the paid-call ledger (episode, then the whole channel vs the budget gates)

Every paid step prints an ESTIMATE line before it starts and a COST line after each paid call, with running
totals for the episode and the channel. All calls also go to cost-ledger.csv (scripts/cost_ledger.py).

Tiers: "tier": "premium" (default, V2: Nano Banana Pro + Kling v2.1) or "budget" (Nano Banana 2 +
MiniMax H3-max). Escalate a failed shot to premium without editing JSON:
    episode.py keyframes <id> sh14 --premium      episode.py clips <id> sh09 --premium
A single keyframe/clip may also pin "model"; "models": {...} overrides the tier.

Optional names limit refs/keyframes/clips/music to those entries (e.g. re-roll one keyframe).

Images go straight to the Google Gemini API (google_imagen, GOOGLE_API_KEY) unless episode.json sets
"image_route": "fal". Add --batch to refs/keyframes for the Gemini Batch API: half price, each dependency
wave waits for its batch (usually minutes):   episode.py keyframes <id> --batch
"image_resolution": "1K" | "2K" (default) | "4K"; a single item may pin "resolution".
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import google_images as gimg  # noqa: E402
import cost_ledger  # noqa: E402
import prompt_kit  # noqa: E402

PLAYBOOK = "storybook-medical"
VOICE = {"voice": "Liam", "model_id": "eleven-v3", "stability": 0.4, "speed": 1.2}
# Channel narrator: Liam, always (master instructions v3.1). "narration": {"convert": true} (Chatterbox voice
# conversion with a reference kept outside git) exists but is not used for the channel.
VOICE_REF = REPO / "projects/voice/ref-hook.mp3"
VC_PER_MIN = 0.015
LOOP_SECONDS = 0.5  # opt-in ("loop": true) only when the story ends naturally on its opening: last 0.5 s dissolves into the start
TEMPO = 1.14
CLIP_VARIANT = "v2.1/standard"
PRICES = {"image": 0.15, "clip": 0.28, "music": 0.03, "tts_per_1k_chars": 0.10}
# Channel defaults are the V2 setup. An episode may override them for experiments with
# "models": {"image": "nano-banana-2", "clip": "h3-max"} in episode.json.
IMAGE_MODELS = {"gemini-3-pro-image": 0.15, "nano-banana-2": 0.08}
CLIP_MODELS = {"kling-v2.1-standard": 0.28, "kling-v2.1-pro": 0.49, "h3-max": 0.0325 * 5}
TIERS = {
    "premium": ("gemini-3-pro-image", "kling-v2.1-standard"),  # V2 pilot setup (default)
    "budget": ("nano-banana-2", "h3-max"),                      # tested on episode 2, ~$2.60
}
PREMIUM = TIERS["premium"]
KIT_REMOTION = ("StorybookShort.tsx", "StorybookLong.tsx", "Clock.tsx", "Brand.tsx", "Fx.tsx", "Life.tsx", "Transitions.tsx", "MapScene.tsx", "Sections.tsx", "Animatic.tsx", "Puppet.tsx", "Stage.tsx", "Graphics.tsx", "Cut.tsx", "LabReels.tsx", "Root.tsx", "index.tsx")


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
    """Every paid call: the episode's cost_log.json, the channel ledger, and a COST line on screen."""
    with cost_ledger._lock:
        p = proj(pid) / "artifacts/cost_log.json"
        rows = json.load(open(p)) if p.exists() else []
        rows.append({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "item": item, "usd": round(usd, 4)})
        json.dump(rows, open(p, "w"), indent=1)
    print(cost_ledger.record(pid, item, usd), flush=True)


def tools():
    registry.discover()
    return registry._tools


def style_prefix() -> str:
    return yaml.safe_load(open(REPO / f"styles/{PLAYBOOK}.yaml", encoding="utf-8"))["asset_generation"]["image_prompt_prefix"].strip()


def resolve_ref(pid: str, ref: str) -> str:
    """'kit:style-anchor.jpg' | 'ref:<name>' | 'kf:<shot>' | 'proj:<relative path>' | absolute/relative path."""
    p = proj(pid)
    if ref.startswith("brand:"):
        return str(KIT / "brand/video" / ref[6:])
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
    """Generate references or keyframes. Route: "image_route" in episode.json, "google" (default, direct Gemini API)
    or "fal". `--batch` sends each dependency wave through the Gemini Batch API at half price (Google route only)."""
    only, premium = split_premium(only)
    use_batch = "--batch" in only
    missing = "--missing" in only          # only items that have no image yet
    lint_ok = "--lint-ok" in only          # proceed despite prompt-lint findings (after reading them)
    only = [n for n in only if n not in ("--batch", "--missing", "--lint-ok")]
    ep = load_ep(pid)
    items = ep.get(section, {})
    out = proj(pid) / "assets/images" / out_dir
    names = [n for n in items if (not only or n in only) and not (missing and (out / f"{n}.png").exists())]
    out.mkdir(parents=True, exist_ok=True)
    route = ep.get("image_route", "google")
    if use_batch and route != "google":
        raise SystemExit('--batch needs "image_route": "google"')
    resolution = ep.get("image_resolution", "2K")
    t = tools()
    image_model, _ = model_choice(ep)
    style = style_prefix()
    wide = proj(pid) / "assets/images/keyframes16x9"
    dual = section == "keyframes" and ep.get("dual_format", True)

    def main_spec(name):
        spec = items[name]
        frame = " Single frame from an animated film, not a model sheet." if section == "keyframes" else ""
        return {"name": name, "model": PREMIUM[0] if premium else spec.get("model", image_model),
                "refs": [resolve_ref(pid, r) for r in spec["refs"]], "aspect": spec.get("aspect", "9:16"),
                "resolution": spec.get("resolution", resolution), "out": out / f"{name}.png",
                "prompt": LOCK + spec.get("roles", "") + " " + spec["prompt"] + frame + f" Aspect {spec.get('aspect', '9:16')}." + TAIL + " " + style}

    def wide_spec(name):
        # Same moment recomposed for long-form 16:9, anchored on the approved 9:16 frame.
        m = main_spec(name)
        return {**m, "name": name + ":16x9", "refs": [str(m["out"])] + m["refs"], "aspect": "16:9", "out": wide / f"{name}.png",
                "prompt": ("Reference 1 is an approved vertical frame. Recompose EXACTLY this moment as a 16:9 "
                           "widescreen frame from a slightly wider camera: same characters, faces, costumes, props, "
                           "lighting and art style; extend the set naturally to the left and right; keep the main "
                           "action centred. Other references are for identity only." + TAIL + " " + style)}

    def cost_of(s, batched):
        if route == "google":
            return gimg.price(s["model"], s["resolution"], batched)
        return IMAGE_MODELS.get(s["model"], PRICES["image"])

    def log(s, batched):
        kind = section + ("16x9" if s["name"].endswith(":16x9") else "")
        tag = f"{route}{'-batch' if batched else ''}"
        log_cost(pid, f"{kind}:{s['name'].split(':')[0]}:{s['model']}:{tag}", cost_of(s, batched))

    def run_one(s):
        missing = [r for r in s["refs"] if not Path(r).exists()]
        if missing:
            return s["name"], False, f"missing refs {missing}"
        if route == "google":
            ok, err = gimg.generate(s, t["google_imagen"])
        else:
            r = t["gemini_fal_image"].execute({"model": s["model"], "prompt": s["prompt"], "image_paths": s["refs"],
                                               "aspect_ratio": s["aspect"], "resolution": s["resolution"], "output_format": "png",
                                               "safety_tolerance": "5", "output_path": str(s["out"])})
            ok, err = r.success, (r.error or "")[:200]
        if ok:
            log(s, False)
        return s["name"], ok, err

    def run_wave(specs):
        if not specs:
            return
        if use_batch:
            ready = [s for s in specs if all(Path(r).exists() for r in s["refs"])]
            for s in specs:
                if s not in ready:
                    print((s["name"], False, "missing refs"))
            res = gimg.batch(ready, f"{pid}-{section}", state_file=proj(pid) / "artifacts/batch_jobs.json")
            for s in ready:
                ok, err = res.get(s["name"], (False, "no result"))
                if ok:
                    log(s, True)
                print((s["name"], ok, err))
        else:
            with ThreadPoolExecutor(6) as ex:
                for res in ex.map(run_one, specs):
                    print(res)

    # dependency waves: an item waits for any kf:/ref: it references that is still being generated
    # pre-flight: known prompt mistakes (plan/prompt-lessons.md) stop the run before any money is spent
    found = prompt_kit.lint_all({x: items[x] for x in names})
    for x, problems in found.items():
        for pr in problems:
            print(f"LINT {x}: {pr}")
    if found and not lint_ok:
        raise SystemExit(f"prompt lint: {len(found)} item(s) need a fix (see plan/prompt-lessons.md), or re-run with --lint-ok")
    if names:
        specs = [main_spec(x) for x in names] * (2 if dual else 1)
        res = sorted({x["resolution"] for x in specs})
        cost_ledger.estimate(f"{section} ({route}{' batch' if use_batch else ''}, {specs[0]['model']}, {'/'.join(res)})",
                             len(specs), 0, total_usd=sum(cost_of(x, use_batch) for x in specs), fal=route == "fal")
    pending = list(names)
    if dual:
        wide.mkdir(parents=True, exist_ok=True)
    while pending:
        def ready(n):
            deps = [r.split(":", 1)[1] for r in items[n]["refs"] if r.startswith(("kf:", "ref:"))]
            return all(d not in pending or d == n for d in deps)
        wave = [n for n in pending if ready(n)] or pending[:1]
        run_wave([main_spec(n) for n in wave])
        if dual:
            run_wave([wide_spec(n) for n in wave if (out / f"{n}.png").exists()])
        pending = [n for n in pending if n not in wave]


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


def _voice_take(pid: str, ep: dict, text: str, raw: Path, out: Path):
    """One ElevenLabs take -> speed + loudness only (memory: narration-audio-processing) -> out (no tail pad)."""
    cost = len(text) / 1000 * PRICES["tts_per_1k_chars"]
    cost_ledger.estimate(f"narration {out.stem} ({len(text)} characters, ElevenLabs v3)", 1, cost, fal=True)
    r = tools()["fal_elevenlabs_tts"].execute({"text": text, **VOICE, "output_path": str(raw)})
    if not r.success:
        raise SystemExit(r.error)
    log_cost(pid, f"narration:{out.stem}", cost)
    take = raw
    ref = Path(ep["narration"].get("voice_ref", VOICE_REF))
    if ep["narration"].get("convert", False) and ref.exists():
        conv = raw.with_name(raw.stem + "_converted.wav")
        to_uri = lambda f: "data:audio/mpeg;base64," + base64.b64encode(Path(f).read_bytes()).decode()
        r = tools()["chatterbox_fal"].execute({
            "model": "chatterbox", "operation": "speech_to_speech", "output_path": str(conv),
            "provider_params": {"source_audio_url": to_uri(raw), "target_voice_audio_url": to_uri(ref)}})
        if r.success:
            take = conv
            log_cost(pid, f"narration-voice-convert:{out.stem}", duration(raw) / 60 * VC_PER_MIN)
        else:
            print("voice conversion failed, using Liam:", (r.error or "")[:200])
    sped = out.with_name("_sped.wav")
    ff("-i", str(take), "-af", f"atempo={ep['narration'].get('tempo', TEMPO)}", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(sped))
    i, _ = loudness(sped)
    stage = out.with_name("_stage.wav")
    lim = "alimiter=limit=0.79:attack=1:release=40:level=disabled:asc=1"
    ff("-i", str(sped), "-af", f"volume={-14 - i:.2f}dB,{lim}", str(stage))
    i2, _ = loudness(stage)
    d = duration(stage)
    ff("-i", str(stage), "-af", f"volume={-14 - i2:.2f}dB,{lim},afade=t=in:st=0:d=0.015,afade=t=out:st={d - 0.08:.3f}:d=0.08",
       "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(out))
    sped.unlink(); stage.unlink()


def _timed_words(path: Path) -> list[dict]:
    r = tools()["azure_stt"].execute({"input_path": str(path), "language": "en-US"})
    return r.data.get("word_timestamps") or [w for s in r.data.get("segments", []) for w in s.get("words", [])]


def step_narrate(pid: str, *only):
    """Liam's narration. Shorts: "narration.v3_text" (one take). Long videos: "narration.chapters" =
    [{"id": "ch0", "v3_text": "...", "gap_after": 2.4}, ...], one take per chapter, joined with gap_after seconds
    of silence (default 0.8; the sting gap after the cold open is longer). `narrate <id> ch4` re-records one
    chapter and re-joins. Every take gets the sentence-spacing check."""
    ep, p = load_ep(pid), proj(pid)
    n = ep["narration"]
    chapters = n.get("chapters") or [{"id": "all", "v3_text": n["v3_text"], "gap_after": 0.5}]
    cdir = p / "assets/audio/chapters"
    cdir.mkdir(parents=True, exist_ok=True)
    for c in chapters:
        wav = cdir / f"{c['id']}.wav"
        if only and c["id"] not in only and wav.exists():
            continue
        _voice_take(pid, ep, c["v3_text"], cdir / f"{c['id']}_raw.mp3", wav)
        words = _timed_words(wav)
        json.dump(words, open(cdir / f"{c['id']}.json", "w", encoding="utf-8"), indent=1)
        print(f"{c['id']}: {duration(wav):.2f}s, {len(words)} words")
        check_spacing(c["v3_text"], words, n.get("min_gap", MIN_SENTENCE_GAP))
    # join: chapter, silence, chapter, ... (sample-exact, no crossfades, nothing cut)
    parts, all_words, marks, t = [], [], [], 0.0
    for c in chapters:
        wav = cdir / f"{c['id']}.wav"
        d = duration(wav)
        gap = c.get("gap_after", 0.8)
        for w in json.load(open(cdir / f"{c['id']}.json", encoding="utf-8")):
            all_words.append({**w, "start": round(w["start"] + t, 3), "end": round(w["end"] + t, 3), "chapter": c["id"]})
        marks.append({"id": c["id"], "start": round(t, 3), "end": round(t + d, 3), "gap_after": gap})
        parts.append(str(wav))
        t += d + gap
    out = p / "assets/audio/narration.wav"
    ins, chain = [], []
    for k, (c, f) in enumerate(zip(chapters, parts)):
        ins += ["-i", f]
        chain.append(f"[{k}:a]apad=pad_dur={c.get('gap_after', 0.8)}[a{k}]")
    ff(*ins, "-filter_complex", ";".join(chain) + ";" + "".join(f"[a{k}]" for k in range(len(parts))) +
       f"concat=n={len(parts)}:v=0:a=1[m]", "-map", "[m]", "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(out))
    json.dump(all_words, open(p / "artifacts/word_timestamps.json", "w", encoding="utf-8"), indent=1)
    json.dump(marks, open(p / "artifacts/chapters.json", "w", encoding="utf-8"), indent=1)
    li, lp = loudness(out)
    print(f"narration.wav {duration(out):.2f}s  {li} LUFS  peak {lp} dBFS  ({len(chapters)} take(s), {len(all_words)} words)")


MIN_SENTENCE_GAP = 0.30  # seconds of silence wanted after every sentence, so edits never land inside the voice


def check_spacing(text: str, words: list[dict], min_gap: float = MIN_SENTENCE_GAP) -> list[tuple[str, float]]:
    """Measure the silence after each sentence of the script in the timed take; print the ones that run together.
    Fix a tight one by writing a line break or '…' after that sentence in v3_text and re-recording that section."""
    import difflib
    clean = re.sub(r"\[[^\]]*\]", " ", text)
    clean = re.sub(r"\s*\n", " ¶ ", clean)                # every line end is a sentence boundary
    tokens = re.findall(r"[\w'’$.,]+[.?!…]*|[.?!¶]+", clean)
    script, ends = [], set()
    for tkn in tokens:
        w = re.sub(r"[^\w$]", "", tkn.lower())
        if not w:
            if script:
                ends.add(len(script) - 1)
            continue
        script.append(w)
        if re.search(r"[.?!]$", tkn):            # "…" inside a line is a deliberate breath, not a sentence end
            ends.add(len(script) - 1)
    heard = [re.sub(r"[^\w$]", "", w["word"].lower()) for w in words]
    match = {}
    for blk in difflib.SequenceMatcher(None, script, heard, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            match[blk.a + k] = blk.b + k
    tight, gaps = [], []
    for e in sorted(ends):
        j = match.get(e)
        if j is None or j + 1 >= len(words):
            continue
        gap = words[j + 1]["start"] - words[j]["end"]
        gaps.append(gap)
        if gap < min_gap:
            tight.append((" ".join(script[max(0, e - 4):e + 1]), round(gap, 2)))
    if gaps:
        gs = sorted(gaps)
        print(f"sentence gaps: {len(gaps)} measured, min {gs[0]:.2f}s, median {gs[len(gs) // 2]:.2f}s, wanted >= {min_gap:.2f}s")
    for t, g in tight:
        print(f"  TIGHT {g:.2f}s after: ...{t}")
    if not tight and gaps:
        print("  every sentence has a clean gap for cutting")
    return tight


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
        spec = ep["clips"][sid]
        kf = p / "assets/images/keyframes" / f"{spec.get('source', sid)}.png"   # "source": the keyframe to animate
        out = p / "assets/video" / f"{sid}.mp4"
        aspect = spec.get("aspect", "16:9" if ep.get("format") == "long" else "9:16")
        model = PREMIUM[1] if premium else spec.get("model", clip_model)
        prompt = spec["motion"] + keep
        if model == "h3-max":
            r = t["h3_max_video"].execute({"model": "h3-max", "prompt": prompt, "image_path": str(kf), "duration": 5,
                                           "resolution": "768P", "prompt_expansion_mode": "balanced",
                                           "enable_safety_checker": False, "output_path": str(out)})
        else:
            fit = (1920, 1080) if aspect == "16:9" else (1080, 1920)

            def data_url(path):
                im = Image.open(path).convert("RGB")
                if abs(im.width / im.height - fit[0] / fit[1]) > 0.02:
                    raise SystemExit(f"clip {sid}: keyframe aspect {im.size} does not match {aspect}")
                buf = io.BytesIO()
                im.resize(fit, Image.LANCZOS).save(buf, "JPEG", quality=92)
                return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

            req = {"prompt": prompt, "operation": "image_to_video", "image_url": data_url(kf), "model_variant": CLIP_VARIANT,
                   "duration": "5", "aspect_ratio": aspect, "output_path": str(out)}
            if spec.get("tail"):  # first + last frame: the clip must END on this keyframe (v2.1 pro)
                req["tail_image_url"] = data_url(p / "assets/images/keyframes" / f"{spec['tail']}.png")
                req["model_variant"] = "v2.1/pro"
                model = "kling-v2.1-pro"
            r = t["kling_video"].execute(req)
        if r.success:
            log_cost(pid, f"clip:{sid}:{model}", r.cost_usd or CLIP_MODELS.get(model, PRICES["clip"]))
        return sid, model, r.success, (r.error or "")[:200]

    ids = [s for s in ep["clips"] if not only or s in only]
    m = PREMIUM[1] if premium else clip_model
    cost_ledger.estimate(f"clips ({m}, 5 s)", len(ids), CLIP_MODELS.get(m, PRICES["clip"]), fal=True)
    with ThreadPoolExecutor(7) as ex:
        for res in ex.map(run, ids):
            print(res)


def step_music(pid, *only):
    ep, p = load_ep(pid), proj(pid)
    t = tools()
    todo = [n for n in ep["music"]["prompts"] if not only or n in only]
    cost_ledger.estimate("music (MiniMax Music v2)", len(todo), PRICES["music"], fal=True)
    for name, spec in ep["music"]["prompts"].items():
        if only and name not in only:
            continue
        out = p / "assets/music" / f"{name}.mp3"
        prompt, sections = (spec, 2) if isinstance(spec, str) else (spec["prompt"], spec.get("sections", 2))
        lyrics = "[Intro]\n" + "[Instrumental]\n" * sections + "[Outro]"
        r = t["fal_minimax_music"].execute({"prompt": prompt, "lyrics_prompt": lyrics, "output_path": str(out)})
        if not r.success:
            print(name, False, r.error)
            continue
        log_cost(pid, f"music:{name}", PRICES["music"])
        stt = t["azure_stt"].execute({"input_path": str(out)})
        d = stt.data or {}
        txt = (d.get("text") or " ".join(s.get("text", "") for s in d.get("segments", []))).strip()
        vocals = bool(re.search(r"[A-Za-z]{2,}", txt))     # STT returns "." or a stray letter on pure instrumentals
        print(f"{name}: {duration(out):.1f}s, vocals detected: {vocals} {txt[:80]}")


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


def caption_spellings() -> dict[str, str]:
    """editorial/pronunciation.csv: words Liam is given a phonetic spelling for, mapped back to the real spelling."""
    import csv
    out = {}
    f = KIT / "editorial/pronunciation.csv"
    if f.exists():
        for row in csv.DictReader(open(f, encoding="utf-8")):
            real = re.sub(r"\(.*?\)", "", row["term"]).split()
            said = (row.get("narrator_spelling") or "").split()
            if real and len(real) == len(said):
                for r, n in zip(real, said):
                    if r.lower() != n.lower():
                        out[re.sub(r"\W", "", n.lower())] = re.sub(r"[^\w'.-]", "", r)
    return out


def fit_frame(src: Path, dst: Path, size: tuple[int, int], focus: float = 0.5, keep_full: bool = False):
    """Fit a still to the format without distortion. Normally: crop a window of the target aspect, centred on
    `focus` (0 = left/top edge, 1 = right/bottom), then resize. keep_full (for "pan" shots): keep the whole
    master and only scale it to the target height, so the template can slide across it."""
    im = Image.open(src).convert("RGB")
    W, H = size
    if keep_full:
        h = H
        w = round(im.width * h / im.height)
        im.resize((w, h), Image.LANCZOS).save(dst, "JPEG", quality=92)
        return
    target = W / H
    if im.width / im.height > target:                       # too wide: choose a horizontal window
        cw = round(im.height * target)
        x = round((im.width - cw) * min(1, max(0, focus)))
        im = im.crop((x, 0, x + cw, im.height))
    elif im.width / im.height < target:                     # too tall: choose a vertical window
        ch = round(im.width / target)
        y = round((im.height - ch) * min(1, max(0, focus)))
        im = im.crop((0, y, im.width, y + ch))
    if im.width < W * 0.75:
        print(f"  WARNING {src.name}: only {im.width}px wide for a {W}px frame (quality rule: no soft crops)")
    im.resize((W, H), Image.LANCZOS).save(dst, "JPEG", quality=92)


def step_build(pid, *_):
    ep, p = load_ep(pid), proj(pid)
    rem = p / "remotion"
    if rem.exists():
        for f in KIT_REMOTION + ("art-direction.md",):
            shutil.copy(KIT / "remotion" / f, rem / f)
    else:
        shutil.copytree(KIT / "remotion", rem)
    pub = rem / "public"
    (pub / "img").mkdir(parents=True, exist_ok=True)
    (pub / "vid").mkdir(parents=True, exist_ok=True)
    words_raw = json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8"))
    total = round(duration(p / "assets/audio/narration.wav"), 2)
    long = ep.get("format", "short") == "long"
    frame_size = (3840, 2160) if long else (1440, 2560)
    shots = []
    for s in ep["shots"]:
        src = Path(resolve_ref(p.name, s["source"]))
        if src.suffix.lower() == ".mp4":
            dst = pub / "vid" / f"{s['id']}.mp4"
            shutil.copy(src, dst)
            kind, rel = "video", f"vid/{s['id']}.mp4"
        else:
            dst = pub / "img" / f"{s['id']}.jpg"
            motion = s.get("motion", {"type": "push"})
            fit_frame(src, dst, frame_size, s.get("focus", 0.5), keep_full=motion.get("type") == "pan")
            kind, rel = "image", f"img/{s['id']}.jpg"
        shots.append({"id": s["id"], "src": rel, "kind": kind, "start": s["start"], "end": s["end"],
                      "inPoint": s.get("in", 0), "motion": s.get("motion", {"type": "push"}),
                      "transitionIn": s.get("transition", "cut"), "darken": s.get("darken", 0)})
    # a dissolve needs the previous shot underneath it: overlap by 0.5 s
    for a, b in zip(shots, shots[1:]):
        if b["transitionIn"] == "dissolve":
            a["end"] = round(a["end"] + 0.5, 3)
    if long and shots[-1]["end"] > total:
        total = round(shots[-1]["end"], 2)        # outro sting + end screen run past the narration
    else:
        shots[-1]["end"] = total
    punch = {w.lower() for w in ep["narration"].get("punch_words", [])}
    respell = caption_spellings()
    words = []
    for w in words_raw:
        t = w["word"]
        shown = "ST." if t.lower() == "st." else re.sub(r"[^\w'?$-]", "", t).strip("-")   # keep "stomach-lining"
        shown = respell.get(shown.lower(), shown)   # narrator spelling (e.g. "Mackinaw") -> real spelling on screen
        words.append({"word": shown, "start": round(w["start"], 3), "end": round(w["end"], 3),
                      "punch": re.sub(r"\W", "", t.lower()) in punch,
                      "breakAfter": bool(re.search(r"[.,?!]$", t)) and t.lower() != "st."})
    if long:
        props = {"totalSeconds": total, "shots": shots, "overlays": ep["overlays"], "words": words,
                 "wordsPerPage": 4, "captionY": 900, "captions": ep.get("captions", True)}
    else:
        props = {"totalSeconds": total, "shots": shots, "overlays": ep["overlays"], "words": words,
                 "wordsPerPage": 3, "captionY": 1180, "loopSeconds": loop_len(ep)}
    json.dump(props, open(rem / "props.json", "w", encoding="utf-8"), indent=1)
    gaps = [(a["id"], b["id"]) for a, b in zip(shots, shots[1:])
            if abs(a["end"] - b["start"]) > 0.02 and b["transitionIn"] != "dissolve"]
    edit = {
        "version": "1.0", "render_runtime": "remotion", "composition_mode": "atelier", "renderer_family": "animation-first",
        "cuts": [{"id": s["id"], "source": s["src"], "in_seconds": s["start"], "out_seconds": s["end"]} for s in shots],
        "bespoke": {"entry": str((rem / "index.tsx").resolve()), "composition_id": "StorybookLong" if long else "StorybookShort",
                    "props_path": str((rem / "props.json").resolve()), "public_dir": str(pub.resolve()),
                    "art_direction": str((rem / "art-direction.md").resolve()), "concurrency": 8, "crf": 18,
                    **({"scale": 2} if long else {})},
        "metadata": {"playbook": PLAYBOOK, "audio": "assets/audio/mix.wav"},
    }
    json.dump(edit, open(p / "artifacts/edit_decisions.json", "w", encoding="utf-8"), indent=1)
    print(f"props: {len(shots)} shots, {len(ep['overlays'])} overlays, {len(words)} words, {total}s, gaps={gaps or 'none'}")


def step_mix(pid, *_):
    ep, p = load_ep(pid), proj(pid)
    narr = p / "assets/audio/narration.wav"
    total = round(duration(narr), 2)
    props_path = p / "remotion/props.json"
    if props_path.exists():
        total = max(total, json.load(open(props_path, encoding="utf-8"))["totalSeconds"])
    tmp = p / "assets/audio/_mix"
    tmp.mkdir(exist_ok=True)
    cues = ep["music"].get("cues")
    src = p / "assets/music" / f"{(cues[0]['track'] if cues else ep['music']['selected'])}.mp3"
    L = loop_len(ep)
    if cues:
        # each cue: the track looped to fit, faded 2 s in/out, placed at its start; neighbours overlap by 2 s
        ins, chains = [], []
        for k, c in enumerate(cues):
            f = p / "assets/music" / f"{c['track']}.mp3"
            ins += ["-stream_loop", "-1", "-i", str(f)]
            d = min(c["end"], total) - c["start"] + (2 if k < len(cues) - 1 else 0)
            ms = int(c["start"] * 1000)
            chains.append(f"[{k}:a]atrim=0:{d:.2f},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,"
                          f"afade=t=in:d={0.4 if k == 0 else 2},afade=t=out:st={max(0, d - 2):.2f}:d=2,adelay={ms}|{ms}[c{k}]")
        ff(*ins, "-filter_complex", ";".join(chains) + ";" + "".join(f"[c{k}]" for k in range(len(cues))) +
           f"amix=inputs={len(cues)}:duration=longest:normalize=0,atrim=0:{total}[m]", "-map", "[m]", "-ar", "48000", "-ac", "2",
           str(tmp / "m.wav"))
    elif duration(src) < total + L + 1:
        ff("-i", str(src), "-i", str(src), "-filter_complex", "[0:a][1:a]acrossfade=d=2:c1=tri:c2=tri[a]", "-map", "[a]",
           "-ar", "48000", str(tmp / "loop.wav"))
        src = tmp / "loop.wav"
    if cues:
        pass
    elif L:
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
    parts = [f"[0:a]aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={total},asplit=2[narr][key]",
             "[1:a][key]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=450:makeup=1[music]"]
    labels = ["[narr]", "[music]"]
    lib = KIT / "library/sfx"
    for n, c in enumerate(ep["sfx"]):
        # "file": any ref (e.g. "brand:sting.mp4" carries the sting's own sound); otherwise a library name
        f = Path(resolve_ref(pid, c["file"])) if c.get("file") else lib / f"{c['name']}.mp3"
        if not f.exists():
            raise SystemExit(f"missing sfx {f} - run the sfx step")
        inputs += ["-i", str(f)]
        gain = c.get("gain_db", -12) - 1 - peak_db(f) if not c.get("as_is") else 0.0
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


def step_render(pid, *flags):
    """Render. `--preview`: long videos at 1080p into renders/preview.mp4 (about 4x faster) for the edit review."""
    p = proj(pid)
    ed = json.load(open(p / "artifacts/edit_decisions.json", encoding="utf-8"))
    pp_path = p / "artifacts/proposal_packet.json"
    out = p / "renders/final.mp4"
    if "--preview" in flags:
        ed["bespoke"].pop("scale", None)
        out = p / "renders/preview.mp4"
    t0 = time.time()
    ep = load_ep(pid)
    review_words = p / "artifacts/transcript_review.json"   # the final review expects {"word_timestamps": [...]}
    json.dump({"word_timestamps": json.load(open(p / "artifacts/word_timestamps.json", encoding="utf-8"))},
              open(review_words, "w", encoding="utf-8"))
    n = ep.get("narration", {})
    script = " ".join(c["v3_text"] for c in n.get("chapters") or [{"v3_text": n.get("v3_text", "")}])
    script = re.sub(r"\[[^\]]*\]", " ", script)   # strip v3 delivery tags before the transcript check
    r = tools()["video_compose"].execute({"operation": "render", "edit_decisions": ed,
                                          "proposal_packet": json.load(open(pp_path)) if pp_path.exists() else None,
                                          "output_path": str(out), "audio_path": str(p / "assets/audio/mix.wav"),
                                          # final review compares what Liam said with the script (free, catches misreads)
                                          "narration_transcript_path": str(review_words),
                                          "script_text": script})
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


DISCLOSURE = ("Illustrations are AI-assisted artistic reconstructions based on the cited historical record. "
              "Research, scripting, editorial decisions and final production are human-directed.\n\n"
              "Educational historical content. Not medical advice.")


def loop_len(ep):
    """Seamless-loop length: 0 unless the episode opts in with "loop": true (only when the ending is natural)."""
    return ep.get("loop_seconds", LOOP_SECONDS) if ep.get("loop") else 0


CHECKLIST = """## Upload checklist

**YouTube Shorts** (Studio on desktop)
- Upload `short.mp4`; paste title, description, tags.
- Thumbnail: upload `cover.jpg` if your account shows the custom-thumbnail option for Shorts; otherwise pick the frame closest to the cover.
- Subtitles → upload `captions.srt` (English).
- Audience: **No, it's not made for kids**. Category: Education. Add to the series playlist.
- Altered or synthetic content: tick it only if a scene could be mistaken for real footage or a real event; illustrated
  reconstructions are covered by the transparency line in the description.
- Before publishing: Stage 7 review (whole video watched; claims.csv has no UNKNOWN/REMOVE claims left in the script;
  rights.csv complete). Upload as Private first; never auto-publish.
- After publishing: post and pin the pinned comment. When a long video exists, set it as the Short's **Related video**.

**TikTok**
- Upload `short.mp4`; Edit cover → upload `cover.jpg`; paste the TikTok caption.
- Turn on the **AI-generated content** label (safe default for AI-assisted visuals). Allow Duet/Stitch.
- During the YouTube probe cross-posting is optional: keep the watermark-free master and post natively later.

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
    for f in KIT_REMOTION:
        shutil.copy(KIT / "remotion" / f, rem / f)
    Image.open(resolve_ref(pid, c["image"])).convert("RGB").resize((1440, 2560), Image.LANCZOS).save(
        rem / "public/img/cover.jpg", "JPEG", quality=92)
    props = {"image": "img/cover.jpg", "title": c["title"], "kicker": c.get("kicker", ""),
             "accentWords": c.get("accent", []), "scale": c.get("scale", 1.05), "x": c.get("x", 0), "y": c.get("y", 0),
             "textY": c.get("textY", 1010)}
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
    desc = "\n\n".join(x for x in (yt["description"].strip(), yt.get("sources", "").strip(), credits.strip(), DISCLOSURE,
                                    " ".join(yt.get("hashtags", []))) if x)
    md = [f"# {ep['title']}", "", f"Length {duration(out / 'short.mp4'):.1f}s · 1080×1920 · -14 LUFS" + (" · loops seamlessly" if loop_len(ep) else ""), "",
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


def step_covers(pid, *only):
    """Shorts cover art as a movie poster (plan/thumbnail-craft.md): one image per entry in episode.json "covers"
    (same fields as keyframes, 9:16, prompt reserves the text band). Point publish.cover.image at
    "proj:assets/images/covers/<name>.png" and set publish.cover.textY to that band (~330 top, ~1240 bottom)."""
    gen_images(pid, "covers", "covers", list(only))


def step_thumbs(pid, *only):
    """Long-video thumbnails (plan/thumbnail-craft.md): generate the 3 concepts in episode.json "thumbnails"
    (same fields as keyframes, plus "text": {kicker, lines, side, accentLine}), then lay the text on with the
    OddlyThumbnail template -> renders/thumbnails/thumb-<name>.jpg (1280x720) and thumb-check.jpg (phone sizes).
    `--compose` skips generation and only re-lays the text (free)."""
    only = list(only)
    compose_only = "--compose" in only
    only = [n for n in only if n != "--compose"]
    if not compose_only:
        gen_images(pid, "thumbnails", "thumbnails", only)
    ep, p = load_ep(pid), proj(pid)
    names = [n for n in ep.get("thumbnails", {}) if (p / "assets/images/thumbnails" / f"{n}.png").exists()]
    rem = p / "remotion"
    (rem / "public/img").mkdir(parents=True, exist_ok=True)
    for f in KIT_REMOTION:
        shutil.copy(KIT / "remotion" / f, rem / f)
    composer = REPO / "remotion-composer"
    entry = tools()["video_compose"]._stage_atelier_project((rem / "index.tsx").resolve(), composer.resolve())
    out = p / "renders/thumbnails"
    out.mkdir(parents=True, exist_ok=True)
    finals = []
    for n in names:
        Image.open(p / "assets/images/thumbnails" / f"{n}.png").convert("RGB").resize((2560, 1440), Image.LANCZOS).save(
            rem / f"public/img/thumb-{n}.jpg", "JPEG", quality=92)
        props = {"image": f"img/thumb-{n}.jpg", "kicker": "", **ep["thumbnails"][n].get("text", {"lines": []})}  # no kicker = none, not the template sample
        pf = rem / f"thumb-{n}-props.json"
        json.dump(props, open(pf, "w", encoding="utf-8"))
        png = out / f"thumb-{n}.png"
        subprocess.run(["npx", "remotion", "still", str(entry), "OddlyThumbnail", str(png), f"--props={pf.resolve()}",
                        f"--public-dir={(rem / 'public').resolve()}", "--log=error"], cwd=composer, check=True, shell=sys.platform == "win32")
        jpg = out / f"thumb-{n}.jpg"
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=90, optimize=True)
        png.unlink()
        finals.append((n, jpg))
    # phone test: full size, then the sizes YouTube actually shows on phones (246x138 home, 168x94 suggested)
    if finals:
        row_h = 720 + 40
        sheet = Image.new("RGB", (1280 + 40 + 246 + 40 + 168 + 40, row_h * len(finals) + 20), "#0f0f0f")
        d = ImageDraw.Draw(sheet)
        for i, (n, jpg) in enumerate(finals):
            im = Image.open(jpg)
            y = 20 + i * row_h
            sheet.paste(im, (0, y))
            sheet.paste(im.resize((246, 138), Image.LANCZOS), (1320, y))
            sheet.paste(im.resize((168, 94), Image.LANCZOS), (1320 + 246 + 40, y))
            d.text((1320, y + 150), f"{n}  ({jpg.stat().st_size / 1e6:.2f} MB)", fill="white")
        sheet.save(out / "thumb-check.jpg", quality=88)
        print("thumbnails ->", out, "| check:", out / "thumb-check.jpg")


def step_brandkit(_pid="-", *_):
    """Render the reusable brand video pieces once into brand/video/ (run: episode.py brandkit -).
    sting.mp4 / sting-outro.mp4 (3840x2160, 1.8 s, with SFX), endscreen.mp4 (20 s, silent), thumb-example.png."""
    brand = KIT / "brand"
    out = brand / "video"
    out.mkdir(parents=True, exist_ok=True)
    stage = REPO / "projects/_brandkit/remotion"
    stage.mkdir(parents=True, exist_ok=True)
    for f in KIT_REMOTION:
        shutil.copy(KIT / "remotion" / f, stage / f)
    composer = REPO / "remotion-composer"
    entry = tools()["video_compose"]._stage_atelier_project((stage / "index.tsx").resolve(), composer.resolve())
    public = (brand / "public").resolve()

    def remotion(kind, comp, dst, props=None):
        cmd = ["npx", "remotion", kind, str(entry), comp, str(dst), f"--public-dir={public}", "--scale=2", "--log=error"]
        if props is not None:
            pf = stage / f"{comp}-props.json"
            json.dump(props, open(pf, "w"))
            cmd.append(f"--props={pf.resolve()}")
        subprocess.run(cmd, cwd=composer, check=True, shell=sys.platform == "win32")

    sfx = KIT / "library/sfx"

    def score(video, cues, dst):
        """Lay SFX cues [(file, start_s, gain)] under a silent render. Kept subtle: peaks at -14 dBFS, well under
        the -14 LUFS narration, so the sting never jolts the rhythm of the video."""
        ins, chains = ["-i", str(video)], []
        for k, (name, at, gain) in enumerate(cues, 1):
            ins += ["-i", str(sfx / name)]
            chains.append(f"[{k}:a]adelay={int(at * 1000)}:all=1,volume={gain}[a{k}]")
        mix = "".join(f"[a{k}]" for k in range(1, len(cues) + 1))
        tmp = out / "_score.wav"
        ff(*ins, "-filter_complex", ";".join(chains) + f";{mix}amix=inputs={len(cues)}:normalize=0,atrim=0:{duration(video):.3f}[m]",
           "-map", "[m]", "-ar", "48000", str(tmp))
        gain = -14 - peak_db(tmp)
        ff("-i", str(video), "-i", str(tmp), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af",
           f"volume={gain:.2f}dB,afade=t=out:st={duration(video) - 0.15:.3f}:d=0.15", "-c:a", "aac", "-b:a", "192k", "-shortest", str(dst))
        tmp.unlink()

    silent = out / "_sting.mp4"
    remotion("render", "OddlySting", silent, {"reverse": False})
    # whoosh on the fall, thud + wire tick on the landing (0.5 s), glass chime on the sparkle (0.9 s)
    score(silent, [("whoosh.mp3", 0.0, 0.35), ("stamp-thud.mp3", 0.48, 0.6), ("tick-click.mp3", 0.52, 0.5),
                   ("glass-clink.mp3", 0.88, 0.45)], out / "sting.mp4")
    remotion("render", "OddlySting", silent, {"reverse": True})
    # outro: letters go, the sparkle chimes (0.9 s), the glasses lift away with a whoosh (1.3 s)
    score(silent, [("glass-clink.mp3", 0.86, 0.4), ("whoosh.mp3", 1.25, 0.35)], out / "sting-outro.mp4")
    silent.unlink()
    remotion("render", "OddlyEndScreen", out / "endscreen.mp4")
    remotion("still", "OddlyThumbnail", out / "thumb-example.png")
    credits = json.load(open(KIT / "library/sfx-credits.json", encoding="utf-8"))
    lines = ["Sound effects in the Oddly Matt sting (credit in any video that uses sting.mp4 / sting-outro.mp4):"]
    for k in ("stamp-thud", "tick-click", "glass-clink", "whoosh"):
        c = credits[k]
        lines.append(f'- "{c["title"]}" by {c["author"]} ({c["url"]}), {c["license"]}')
    (out / "CREDITS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for f in sorted(out.iterdir()):
        print(f.name, f"{f.stat().st_size / 1e6:.2f} MB")


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
    print()
    cost_ledger.summary()


STEPS = {name[5:]: fn for name, fn in globals().items() if name.startswith("step_")}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in STEPS:
        print(__doc__)
        raise SystemExit(1)
    STEPS[sys.argv[1]](sys.argv[2], *sys.argv[3:])
