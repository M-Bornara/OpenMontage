"""Generate music with MiniMax Music v2 through fal.ai.

MiniMax Music v2 is a song model: fal requires a ``lyrics_prompt`` and offers no
duration or instrumental switch. For background beds, pass structure tags only
(e.g. ``[Intro]\\n[Instrumental]\\n[Outro]``) and verify the result has no vocals.
The track length is chosen by the model, so trim it in the edit.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

INSTRUMENTAL_LYRICS = "[Intro]\n[Instrumental]\n[Instrumental]\n[Outro]"


class FalMinimaxMusic(BaseTool):
    """Generate a low-cost music track through fal.ai."""

    name = "fal_minimax_music"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "music_generation"
    provider = "fal.ai"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = ["env:FAL_KEY"]
    install_instructions = (
        "Set FAL_KEY to a fal.ai API key. "
        "Get one at https://fal.ai/dashboard/keys"
    )
    fallback_tools = ["fal_elevenlabs_music", "music_gen"]
    agent_skills = ["music"]

    capabilities = ["generate_background_music", "generate_song"]
    supports = {
        "instrumental": False,
        "style_control": True,
        "exact_duration": False,
    }
    best_for = [
        "very cheap music drafts and alternatives ($0.03 per generation)",
        "songs with lyrics",
    ]
    not_good_for = [
        "guaranteed instrumentals (verify no vocals)",
        "exact durations",
        "offline generation",
    ]

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Style, mood, instruments and scenario (10-300 characters recommended)",
            },
            "lyrics_prompt": {
                "type": "string",
                "default": INSTRUMENTAL_LYRICS,
                "description": "Lyrics with optional [Intro]/[Verse]/[Chorus]/[Outro] tags; "
                "structure tags only for a background bed",
            },
            "output_path": {"type": "string", "default": "fal_minimax_music.mp3"},
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=50, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=0, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["prompt", "lyrics_prompt"]
    side_effects = [
        "writes an MP3 file to output_path",
        "submits one paid fal.ai generation request",
    ]
    user_visible_verification = [
        "Listen for vocals, mood and mix; trim to the video length",
    ]

    _MODEL = "fal-ai/minimax-music/v2"
    _QUEUE_URL = f"https://queue.fal.run/{_MODEL}"
    _POLL_INTERVAL_SECONDS = 5
    _MAX_WAIT_SECONDS = 600

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if self._get_api_key() else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        """fal bills $0.03 per generation (api.fal.ai/v1/models/pricing, 2026-10-17)."""
        return 0.03

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(
                success=False,
                error="No fal.ai API key found. " + self.install_instructions,
            )

        import requests

        started = time.time()
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": inputs["prompt"],
            "lyrics_prompt": inputs.get("lyrics_prompt") or INSTRUMENTAL_LYRICS,
        }

        try:
            submit_response = requests.post(self._QUEUE_URL, headers=headers, json=payload, timeout=30)
            submit_response.raise_for_status()
            queue_data = submit_response.json()
            status_url = queue_data["status_url"]
            response_url = queue_data["response_url"]

            deadline = time.monotonic() + self._MAX_WAIT_SECONDS
            while True:
                if time.monotonic() >= deadline:
                    return ToolResult(
                        success=False,
                        error="fal.ai MiniMax music generation timed out while waiting in the queue",
                        duration_seconds=round(time.time() - started, 2),
                    )
                time.sleep(self._POLL_INTERVAL_SECONDS)
                status_response = requests.get(status_url, headers=headers, timeout=20)
                status_response.raise_for_status()
                status = status_response.json().get("status", "UNKNOWN")
                if status == "COMPLETED":
                    break
                if status in {"FAILED", "CANCELLED"}:
                    return ToolResult(
                        success=False,
                        error=f"fal.ai MiniMax music generation {status.lower()}",
                        duration_seconds=round(time.time() - started, 2),
                    )

            result_response = requests.get(response_url, headers=headers, timeout=30)
            result_response.raise_for_status()
            audio_url = result_response.json()["audio"]["url"]

            audio_response = requests.get(audio_url, timeout=120)
            audio_response.raise_for_status()
            output_path = Path(inputs.get("output_path", "fal_minimax_music.mp3"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_response.content)
        except Exception as exc:
            safe_error = str(exc).replace(api_key, "[REDACTED]")
            return ToolResult(
                success=False,
                error=f"fal.ai MiniMax music generation failed: {safe_error}",
                duration_seconds=round(time.time() - started, 2),
            )

        return ToolResult(
            success=True,
            data={
                "provider": "fal.ai",
                "model": self._MODEL,
                "prompt": inputs["prompt"],
                "lyrics_prompt": payload["lyrics_prompt"],
                "output": str(output_path),
                "format": "mp3",
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - started, 2),
            model=self._MODEL,
        )
