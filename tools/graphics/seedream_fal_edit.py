"""Seedream 4.5 generation and multi-reference editing on fal."""

from tools.fal_media import FalMedia


class SeedreamFalEdit(FalMedia):
    name = "seedream_fal_edit"
    capability = "image_generation"
    capabilities = ["text_to_image", "image_edit"]
    supports = {"image_edit": True, "multiple_reference_images": True}
    best_for = ["Low-cost multi-reference image edits (Seedream 4.5, ~$0.04/image)"]
    routes = {
        "seedream-4.5": {
            "generate": "fal-ai/bytedance/seedream/v4.5/text-to-image",
            "edit": "fal-ai/bytedance/seedream/v4.5/edit",
        }
    }
