"""Nano Banana Pro generation and editing on fal."""

from tools.fal_media import FalMedia


class GeminiFalImage(FalMedia):
    name = "gemini_fal_image"
    capability = "image_generation"
    capabilities = ["text_to_image", "image_edit"]
    supports = {"image_edit": True, "multiple_reference_images": True}
    best_for = [
        "Gemini 3 Pro Image with an existing fal account",
        "nano-banana-2: about half the price of Pro for multi-reference edits",
    ]
    routes = {
        "gemini-3-pro-image": {
            "generate": "fal-ai/nano-banana-pro",
            "edit": "fal-ai/nano-banana-pro/edit",
        },
        "nano-banana-2": {
            "generate": "fal-ai/nano-banana-2",
            "edit": "fal-ai/nano-banana-2/edit",
        },
    }
