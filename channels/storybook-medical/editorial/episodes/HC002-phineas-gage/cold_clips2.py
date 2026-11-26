"""2026-11-25 (Mahdi, $1.00 total): the cold-open Omni clips pour / tamp / spark, 720p, 3 s each, ONE take each (fal price 720p $0.0819/s: 9 s = $0.737).
Start frame decides (L72), minimal motion text (L73), the background named in every prompt (L55). No retake fits inside the cap: a failed clip goes to Tier A.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/cold_clips2.py"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import episode  # noqa: E402

RATE, DUR = 0.0819, 3
KEEP = " Keep the hand-painted storybook style exactly as in the image. No new objects."
CLIPS = {
    "cold-k1-pour-omni-v1": ("cold-r1-pour-v1", "Flat grey layered schist rock. Black powder pours into the drilled hole. Locked camera."),
    "cold-k2-tamp-omni-v1": ("cold-b1-tip-v1", "Flat grey layered schist rock. The iron bar pushes down into the drill hole. Locked camera."),
    "cold-k4-spark-omni-v1": ("cold-b1-tip-v1", "Flat grey layered schist rock. The iron bar's tip strikes the stone and sparks fly. Locked camera."),
}
assert len(CLIPS) * DUR * RATE <= 0.75, "over the clip budget"
P = REPO / "projects/hc002-l"
tool = episode.tools()["gemini_omni_fal"]


def run(item):
    cid, (src, text) = item
    r = tool.execute({"prompt": text + KEEP, "operation": "image_to_video", "model_version": "v1.2", "resolution": "720p", "duration": DUR,
                      "aspect_ratio": "16:9", "image_path": str(P / "assets/images/keyframes" / f"{src}.png"), "output_path": str(P / "assets/video" / f"{cid}.mp4")})
    if r.success:
        episode.log_cost("hc002-l", f"clip:{cid}:gemini-omni-1.2-flash-fal-720p", round(RATE * DUR, 4))
    return cid, r.success, (r.error or "")[:300]


if __name__ == "__main__":
    with ThreadPoolExecutor(3) as ex:
        for res in ex.map(run, CLIPS.items()):
            print(res)
