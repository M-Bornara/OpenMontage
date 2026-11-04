"""Chatterbox (Resemble AI, MIT) voice conversion and voice-cloned TTS on fal.

speech_to_speech re-voices a source performance with a target voice sample: keep a native
narrator's pronunciation, rhythm and emotion, swap in your own voice. text_to_speech clones the
target sample directly (carries more of the sample's accent). Pass audio as local paths via
provider_params data URIs; see channels/storybook-medical/scripts/episode.py.
"""

from tools.fal_media import FalMedia


class ChatterboxFal(FalMedia):
    name = "chatterbox_fal"
    capability = "voice_conversion"
    capabilities = ["speech_to_speech", "text_to_speech", "voice_cloning"]
    supports = {"voice_cloning": True, "speech_to_speech": True}
    best_for = [
        "Your own voice with a native narrator's delivery (speech_to_speech, ~$0.015/min)",
        "Zero-shot voice cloning from a 10-30 s sample (~$0.025 per 1,000 characters)",
    ]
    routes = {
        "chatterbox": {
            "speech_to_speech": "fal-ai/chatterbox/speech-to-speech",
            "text_to_speech": "fal-ai/chatterbox/text-to-speech",
        },
        "chatterbox-hd": {
            "speech_to_speech": "resemble-ai/chatterboxhd/speech-to-speech",
        },
    }
