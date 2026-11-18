"""HC002-S1 s11 16:9 only (2026-11-18): the recompose painted a whole uninjured Gage in the doorway (the Gage sheet, given
for the sleeve, became a person). Redo the 16:9 alone from the approved 9:16 frame as the ONLY reference. Gemini Batch.
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/wide_s11.py
"""
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import episode as E  # noqa: E402
import google_images as g  # noqa: E402

PID = "hc002-s1"
p = E.proj(PID)
ep = E.load_ep(PID)
model = ep["keyframes"]["s11"].get("model", E.model_choice(ep)[0])
src = p / "assets/images/keyframes/s11.png"
out = p / "assets/images/keyframes16x9/s11.png"
if out.exists():
    (out.parent / "_v1").mkdir(exist_ok=True)
    shutil.move(str(out), str(out.parent / "_v1/s11.v2-figure.png"))
spec = {"name": "s11:16x9", "model": model, "refs": [str(src)], "aspect": "16:9", "resolution": "2K", "out": out,
        "prompt": ("Reference 1 is an approved vertical frame. Recompose EXACTLY this moment as a 16:9 widescreen frame from a "
                   "slightly wider camera: the same hand and rolled white sleeve gripping the same single iron rod, the same "
                   "spectacles hanging from the nail, the same bare plank walls, floor, light and painting style; extend the "
                   "bare plank wall and floor naturally to the left and right. NO person: only that one hand and sleeve "
                   "entering from the edge, no body, no face, no figure in any doorway. Exactly ONE iron rod. No furniture, "
                   "no shelves, no lamp." + E.TAIL + " " + E.style_prefix())}
E.cost_ledger.estimate("keyframes16x9 s11 redo (google batch)", 1, g.price(model, "2K", True))
res = g.batch([spec], f"{PID}-s11wide", state_file=p / "artifacts/batch_jobs.json")
ok, err = res.get("s11:16x9", (False, "no result"))
if ok:
    E.log_cost(PID, f"keyframes16x9:s11:{model}:google-batch", g.price(model, "2K", True))
    (p / "artifacts/batch_jobs.json").unlink(missing_ok=True)
print("s11:16x9", ok, err)
