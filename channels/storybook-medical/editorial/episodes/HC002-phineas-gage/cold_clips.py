"""2026-11-25 (Mahdi): cold-open clips C2 (blast, 4 s) and C3 (iron in flight, 3 s) on Omni 1.2 Flash, 720p, ONE take each.
fal price (page read 2026-11-25): 720p $0.0819 per second of output -> 7 s = $0.573 (cap: stop if above $0.65). Stop after this run; a retake needs Mahdi's yes.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/cold_clips.py
"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import episode  # noqa: E402

RATE = 0.0819
KEEP = " Keep the hand-painted storybook style, faces and colours exactly as in the image. No new people."
CLIPS = {
    "cold-c2-blast-omni-v1": ("cold-b2-ledge-v1", 4, "A blast erupts from the ledge: rock chunks, smoke and dust burst outward. The men flinch. The camera shakes."),
    "cold-c3-rod-omni-v1": ("cold-b3-rod-v1", 3, "The thin iron rod spins and shoots upward, trailing a ribbon of smoke into the bright sky. The camera tilts up with it."),
}
assert sum(d for _, d, _ in CLIPS.values()) * RATE <= 0.65, "over the $0.65 stop line"
P = REPO / "projects/hc002-l"
tool = episode.tools()["gemini_omni_fal"]


def run(item):
    cid, (src, dur, prompt) = item
    out = P / "assets/video" / f"{cid}.mp4"
    r = tool.execute({"prompt": prompt + KEEP, "operation": "image_to_video", "model_version": "v1.2", "resolution": "720p", "duration": dur,
                      "aspect_ratio": "16:9", "image_path": str(P / "assets/images/keyframes" / f"{src}.png"), "output_path": str(out)})
    if r.success:
        episode.log_cost("hc002-l", f"clip:{cid}:gemini-omni-1.2-flash-fal-720p", round(RATE * dur, 4))
    return cid, r.success, (r.error or "")[:300]


if __name__ == "__main__":
    (P / "assets/video").mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(2) as ex:
        for res in ex.map(run, CLIPS.items()):
            print(res)
