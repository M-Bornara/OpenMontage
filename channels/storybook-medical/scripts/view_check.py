"""View check L56 (user 2026-11-20: "make sure the backgrounds are not going to be similar again"): right after the
keyframes come back, before any edit, find every story still that is the SAME VIEW as a full scene it was given as a
reference (a set plate, another keyframe) or as any other keyframe of the episode.

Why: the 2026-11-20 audit found the jump cuts were not thin prompts. HCS05 s5a / s5b / s6 had long camera() lines
facing west, south and north, and all three came back as plate-ward.png pixel for pixel with a person painted in. The
image model treats a full scene among the references as the picture to EDIT; no wording holds it back (L47b). Until
now this was only seen at the edit (cut_check L52), after the money was spent and the user had watched the cut.

Method: cut_check.match (ORB + ratio test + RANSAC similarity) on 900 px greyscale copies; >= 120 inliers and >= 25 %
of the good matches = the same view of the same set. Exempt: shots marked "kf_same_view" or whose prompt says
SAME_CAMERA, and empty plates / sheets (no "SHOT:" line).

    python channels/storybook-medical/scripts/view_check.py <project-id> [shot ...]     # exit 1 on any L56
`episode.py keyframes` runs it on the shots it just made.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cut_check import match  # noqa: E402
from prompt_kit import SAME_CAMERA  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
MIN_INLIERS, MIN_FRAC = 120, 0.25  # 2026-11-20 audit: a shared prop or face scores 47-77, a copied set 133-1858


def _load(p: Path):
    im = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
    if im is None:
        return None
    s = 900 / max(im.shape)
    return cv2.resize(im, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)


def _scene_ref(pid: str, ref: str) -> Path | None:
    """Only full scenes: set plates and other keyframes (sheets, portraits and kit files are identity, not a view)."""
    d = REPO / "projects" / pid / "assets/images"
    if ref.startswith("ref:plate-") and not any(w in ref for w in ("detail", "crop")):
        return d / "refs" / f"{ref[4:]}.png"
    if ref.startswith("kf:"):
        return d / "keyframes" / f"{ref[3:]}.png"
    return None


def check(pid: str, only: list[str] | None = None, verbose: bool = True) -> list[str]:
    ep = json.load(open(REPO / "projects" / pid / "episode.json", encoding="utf-8"))
    kfs = ep.get("keyframes", {})
    kdir = REPO / "projects" / pid / "assets/images/keyframes"

    def exempt(n):
        s = kfs[n]
        return s.get("kf_same_view") or SAME_CAMERA.lower() in s.get("prompt", "").lower() or \
            "shot:" not in s.get("prompt", "").lower()

    story = [n for n in kfs if (kdir / f"{n}.png").exists() and not exempt(n)]
    todo = [n for n in story if not only or n in only]
    cache: dict[Path, object] = {}

    def img(p):
        if p not in cache:
            cache[p] = _load(p)
        return cache[p]

    def same(a, b):
        m = match(a, b) if a is not None and b is not None else None
        return m[0] if m and m[0] >= MIN_INLIERS and m[1] >= MIN_FRAC else 0

    out = []
    for n in todo:
        me = img(kdir / f"{n}.png")
        for r in kfs[n].get("refs", []):
            p = _scene_ref(pid, r)
            if p and p.exists() and (k := same(img(p), me)):
                out.append(f"L56 {n}: the same view as its reference {r} ({k} matching points): the model edited the "
                           "reference instead of painting a new camera; re-roll without it (or a cropped detail)")
        for o in story:
            if o == n or (o in todo and story.index(o) < story.index(n)):
                continue
            if k := same(img(kdir / f"{o}.png"), me):
                out.append(f"L56 {n}: the same view as {o} ({k} matching points): two shots, one background")
    if verbose:
        print(*(out or [f"view check {pid}: {len(todo)} shot(s), no copied backgrounds"]), sep="\n")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    sys.exit(1 if check(sys.argv[1], sys.argv[2:] or None) else 0)
