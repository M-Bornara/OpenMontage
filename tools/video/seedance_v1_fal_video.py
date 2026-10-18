"""Seedance v1 Pro Fast image-to-video on fal (token-priced; ~$0.11 per 5 s at 720p)."""

from tools.fal_media import FalMedia


class SeedanceV1FalVideo(FalMedia):
    name = "seedance_v1_fal_video"
    capability = "video_generation"
    capabilities = ["image_to_video"]
    supports = {"image_to_video": True, "camera_fixed": True}
    best_for = ["Low-cost image-to-video clips from approved keyframes"]
    routes = {
        "seedance-v1-pro-fast": {
            "image_to_video": "fal-ai/bytedance/seedance/v1/pro/fast/image-to-video",
        }
    }
