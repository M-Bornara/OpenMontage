"""Blind A/B of Liam's speed-up (memory: narration-audio-processing; the HC001 "warble").
Three ElevenLabs v3 takes of one passage, six versions through the same loudness chain as `_voice_take`, named 1..6
in random order -> projects/voice-ab/<tag>/. The key is in key.json; listen before opening it.
    python voice_ab.py            (generates; about $0.10)
"""
import json
import random
import sys

from episode import REPO, VOICE, duration, ff, log_cost, loudness, tools

PID = "voice-ab"
TAG = "forssmann-1"
# HCS01 shots 1-6 (script-v2.md): one sentence per line so every edit point is a gap
TEXT = """[excited] In 1929, a young doctor pushed a tube through his own arm… all the way into his own heart.
Werner Forssmann, a trainee surgeon in Germany, had an idea: reach a living heart through a vein.
His boss said no. Far too dangerous.
The nurse with the supplies agreed to help… if he tried it on HER.
[mischievously] He tricked her. He numbed his own arm instead.
Then he slid a thin catheter into a vein. Sixty-five centimeters."""

TAKES = {"t12": dict(speed=1.2, stability=0.4), "t10": dict(speed=1.0, stability=0.4), "t10n": dict(speed=1.0, stability=0.5)}
VERSIONS = {
    "HC001 chain: ElevenLabs 1.2 + atempo 1.14": ("t12", "atempo=1.14"),
    "ElevenLabs 1.2 only": ("t12", None),
    "ElevenLabs 1.0 + atempo 1.14": ("t10", "atempo=1.14"),
    "ElevenLabs 1.0 + plain rubberband 1.14": ("t10", "rubberband=tempo=1.14"),
    "ElevenLabs 1.0, no speed-up": ("t10", None),
    "ElevenLabs 1.0, stability 0.5 + atempo 1.14": ("t10n", "atempo=1.14"),
}
LIM = "alimiter=limit=0.79:attack=1:release=40:level=disabled:asc=1"


def finish(src, af, out):
    """Speed (or not), then -14 LUFS + peak limit + fades: the `_voice_take` chain."""
    sped = out.with_name("_sped.wav")
    ff("-i", str(src), *(["-af", af] if af else []), "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(sped))
    i, _ = loudness(sped)
    stage = out.with_name("_stage.wav")
    ff("-i", str(sped), "-af", f"volume={-14 - i:.2f}dB,{LIM}", str(stage))
    i2, _ = loudness(stage)
    d = duration(stage)
    ff("-i", str(stage), "-af", f"volume={-14 - i2:.2f}dB,{LIM},afade=t=in:st=0:d=0.015,afade=t=out:st={d - 0.08:.3f}:d=0.08",
       "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(out))
    sped.unlink(); stage.unlink()


def main():
    out = REPO / "projects" / PID / TAG
    (REPO / "projects" / PID / "artifacts").mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    cost = len(TEXT) / 1000 * 0.10
    for t, s in TAKES.items():
        raw = out / f"_{t}.mp3"
        if not raw.exists():
            r = tools()["fal_elevenlabs_tts"].execute({"text": TEXT, **{**VOICE, **s}, "output_path": str(raw)})
            if not r.success:
                raise SystemExit(r.error)
            log_cost(PID, f"voice A/B take {t} ({len(TEXT)} chars)", cost)
    names = list(VERSIONS)
    random.Random(7).shuffle(names)
    key = {}
    for n, name in enumerate(names, 1):
        t, af = VERSIONS[name]
        f = out / f"{n}.wav"
        finish(out / f"_{t}.mp3", af, f)
        key[n] = f"{name} ({duration(f):.1f} s)"
    json.dump(key, open(out / "key.json", "w"), indent=1)
    print("listen:", out, "->", ", ".join(f"{n}.wav" for n in key))


if __name__ == "__main__":
    sys.exit(main())
