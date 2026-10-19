"""Direct Google Gemini image generation for the channel kit.

Two paths, same request shape:
  generate(spec)        one image now, through the registry's google_imagen tool
  batch(specs, label)   many images through the Gemini Batch API (half price, usually minutes, up to 24 h)

A spec is {"name", "model", "prompt", "refs": [paths], "aspect", "resolution", "out"}.
"""
from __future__ import annotations

import base64
import io
import json
import time
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[3]

# Channel model names -> Gemini API model ids
MODEL_IDS = {"gemini-3-pro-image": "gemini-3-pro-image", "nano-banana-2": "gemini-3.1-flash-image"}
# Standard (non-batch) price per output image, USD. Batch is half. Estimates for the cost ledger.
PRICES = {
    "gemini-3-pro-image": {"1K": 0.134, "2K": 0.134, "4K": 0.24},
    "gemini-3.1-flash-image": {"1K": 0.067, "2K": 0.101, "4K": 0.151},
}
INLINE_LIMIT = 15_000_000  # bytes of base64 per batch request (API cap is 20 MB)


def model_id(model: str) -> str:
    return MODEL_IDS.get(model, model)


def price(model: str, resolution: str = "2K", batch: bool = False) -> float:
    p = PRICES.get(model_id(model), PRICES["gemini-3-pro-image"]).get(resolution, 0.24)
    return round(p / 2 if batch else p, 4)


def generate(spec: dict, tool) -> tuple[bool, str]:
    r = tool.execute({"model": model_id(spec["model"]), "prompt": spec["prompt"], "image_paths": spec["refs"],
                      "aspect_ratio": spec["aspect"], "resolution": spec["resolution"], "output_path": str(spec["out"])})
    return r.success, (r.error or "")[:200]


def _ref_part(path: str) -> dict:
    """References go in as JPEG, long side <= 2048, so a batch of chained keyframes stays under the inline cap."""
    im = Image.open(path).convert("RGB")
    im.thumbnail((2048, 2048), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}


def _request(spec: dict) -> dict:
    return {"contents": [{"role": "user", "parts": [{"text": spec["prompt"]}] + [_ref_part(r) for r in spec["refs"]]}],
            "config": {"response_modalities": ["IMAGE"],
                       "image_config": {"aspect_ratio": spec["aspect"], "image_size": spec["resolution"]}}}


def _client():
    from dotenv import load_dotenv
    load_dotenv(REPO / ".env")
    from tools.google_credentials import get_genai_client
    return get_genai_client()


def batch(specs: list[dict], label: str, poll: int = 30, state_file: Path | None = None) -> dict[str, tuple[bool, str]]:
    """Run specs through the Batch API. One job per model, split so each job stays under the inline cap."""
    results: dict[str, tuple[bool, str]] = {}
    if not specs:
        return results
    client = _client()
    jobs = []
    for model in sorted({model_id(s["model"]) for s in specs}):
        chunk, size = [], 0
        for s in (s for s in specs if model_id(s["model"]) == model):
            req = _request(s)
            n = len(json.dumps(req))
            if chunk and size + n > INLINE_LIMIT:
                jobs.append((model, chunk)); chunk, size = [], 0
            chunk.append((s, req)); size += n
        if chunk:
            jobs.append((model, chunk))
    running = []
    for i, (model, chunk) in enumerate(jobs):
        job = client.batches.create(model=model, src=[req for _, req in chunk],
                                    config={"display_name": f"{label}-{i}"})
        print(f"batch submitted {job.name} ({len(chunk)} images, {model})", flush=True)
        running.append((job.name, [s for s, _ in chunk]))
    if state_file:
        state_file.write_text(json.dumps([{"job": n, "names": [s["name"] for s in ss]} for n, ss in running], indent=1))
    for name, chunk in running:
        while True:
            job = client.batches.get(name=name)
            state = str(job.state)
            if any(x in state for x in ("SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED")):
                break
            print(time.strftime("%H:%M:%S"), name.split("/")[-1], state.split(".")[-1], flush=True)
            time.sleep(poll)
        if "SUCCEEDED" not in state:
            for s in chunk:
                results[s["name"]] = (False, f"batch {state}: {getattr(job, 'error', '')}")
            continue
        for s, resp in zip(chunk, job.dest.inlined_responses):
            if resp.error:
                results[s["name"]] = (False, str(resp.error)[:200]); continue
            data = next((p.inline_data.data for p in (resp.response.candidates[0].content.parts or [])
                         if getattr(p, "inline_data", None) and p.inline_data.data), None)
            if not data:
                results[s["name"]] = (False, "no image returned"); continue
            Path(s["out"]).parent.mkdir(parents=True, exist_ok=True)
            Path(s["out"]).write_bytes(data)
            results[s["name"]] = (True, "")
    return results
