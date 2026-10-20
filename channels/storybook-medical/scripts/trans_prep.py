"""Free prep for the AI-style transitions (Transitions.tsx v2): depth layers, luma layers and optical-flow morphs.

- depth_bands(img, prefix, n): Depth Anything V2 Small (Apache-2.0, ONNX, CPU) → n soft masks from NEAR to FAR
  (prefix-0.png = nearest). Used by the "peel" (the scene leaves element by element) and "build" transitions.
- luma_bands(img, prefix, n): the same from brightness (brightest first): the "light spreads" dissolve.
- morph(a, b, out_dir, frames): dense optical flow both ways (OpenCV DIS), each image warped toward the other and
  blended → a JPG sequence the transition plays. Best on designed pairs (same shape, same place).
"""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

MODEL = Path.home() / ".cache/openmontage/models/depth_anything_v2_vits.onnx"
MASK_W = 1920
_sess = None


def _load(img: str, width: int = MASK_W) -> np.ndarray:
    im = Image.open(img).convert("RGB")
    return np.array(im.resize((width, round(im.height * width / im.width)), Image.LANCZOS))


def depth(img: str) -> np.ndarray:
    """Relative depth, 0 = far … 1 = near, at MASK_W width."""
    global _sess
    import onnxruntime as ort
    if _sess is None:
        _sess = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    rgb = _load(img)
    H, W = rgb.shape[:2]
    x = cv2.resize(rgb, (518, 518), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    d = _sess.run(None, {_sess.get_inputs()[0].name: x})[0].squeeze()
    d = cv2.resize(d.astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    d = (d - d.min()) / max(1e-6, d.max() - d.min())
    return cv2.GaussianBlur(d, (0, 0), 3)


def _bands(v: np.ndarray, prefix: str, n: int, soft: float = 0.06) -> list[str]:
    """n soft bands of v from HIGH to LOW (band 0 = highest values), equal pixel counts, overlapping edges."""
    qs = np.quantile(v, np.linspace(1, 0, n + 1))
    out = []
    for k in range(n):
        hi, lo = qs[k], qs[k + 1]
        a = np.clip((v - lo) / soft + 0.5, 0, 1) * (1 if k == 0 else np.clip((hi - v) / soft + 0.5, 0, 1))
        a = cv2.dilate(a.astype(np.float32), np.ones((7, 7), np.uint8))
        m = Image.new("RGBA", (v.shape[1], v.shape[0]), (255, 255, 255, 0))
        m.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
        path = f"{prefix}-{k}.png"
        m.save(path)
        out.append(path)
    return out


def _kmeans_bands(v: np.ndarray, prefix: str, n: int, soft: float) -> list[str]:
    """Bands split at the natural gaps of v (1-D k-means), so each band holds whole objects (a person, the dock, the
    hills), not equal pixel slices that cut through people."""
    sample = v[::4, ::4].reshape(-1, 1).astype(np.float32)
    _, _, centres = cv2.kmeans(sample, n, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1e-3), 4,
                               cv2.KMEANS_PP_CENTERS)
    c = np.sort(centres.ravel())[::-1]
    cuts = [1.01] + [(c[i] + c[i + 1]) / 2 for i in range(n - 1)] + [-0.01]
    out = []
    for k in range(n):
        hi, lo = cuts[k], cuts[k + 1]
        a = np.clip((v - lo) / soft + 0.5, 0, 1) * np.clip((hi - v) / soft + 0.5, 0, 1)
        a = cv2.dilate(a.astype(np.float32), np.ones((7, 7), np.uint8))  # overlap neighbours: no seams when stacked
        m = Image.new("RGBA", (v.shape[1], v.shape[0]), (255, 255, 255, 0))
        m.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
        path = f"{prefix}-{k}.png"
        m.save(path)
        out.append(path)
    return out


def depth_bands(img: str, prefix: str, n: int = 4) -> list[str]:
    return _kmeans_bands(depth(img), prefix, n, soft=0.03)


def luma_bands(img: str, prefix: str, n: int = 6) -> list[str]:
    L = cv2.cvtColor(_load(img), cv2.COLOR_RGB2LAB)[:, :, 0].astype(np.float32) / 255
    return _bands(cv2.GaussianBlur(L, (0, 0), 12), prefix, n, soft=0.08)


def morph(a: str, b: str, out_dir: str, frames: int = 24, width: int = 1920) -> str:
    A = _load(a, width).astype(np.float32)
    B = _load(b, width).astype(np.float32)
    B = cv2.resize(B, (A.shape[1], A.shape[0]))
    small = lambda x: cv2.cvtColor(cv2.resize(x.astype(np.uint8), (A.shape[1] // 2, A.shape[0] // 2)), cv2.COLOR_RGB2GRAY)
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    up = lambda f: cv2.resize(f, (A.shape[1], A.shape[0])) * 2
    fab = up(dis.calc(small(A), small(B), None))
    fba = up(dis.calc(small(B), small(A), None))
    # heavy smoothing: the shapes flow into each other instead of melting
    fab = cv2.GaussianBlur(fab, (0, 0), 25)
    fba = cv2.GaussianBlur(fba, (0, 0), 25)
    H, W = A.shape[:2]
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(frames):
        t = i / (frames - 1)
        s = t * t * (3 - 2 * t)  # smoothstep: the blend lingers at both ends
        wa = cv2.remap(A, gx - t * fba[..., 0], gy - t * fba[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        wb = cv2.remap(B, gx - (1 - t) * fab[..., 0], gy - (1 - t) * fab[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        Image.fromarray(np.clip(wa * (1 - s) + wb * s, 0, 255).astype(np.uint8)).save(out / f"{i:03d}.jpg", quality=90)
    return str(out)


def peel_plates(img: str, bands: list[str], prefix: str, width: int = 1920) -> list[str]:
    """For the element peel: plate k = the image with layers 0..k painted out (OpenCV inpaint, on a blurred base so
    big holes read as soft background, not smears). The peel crossfades plate k-1 → plate k while layer k leaves."""
    rgb = _load(img, width)
    H, W = rgb.shape[:2]
    hole = np.zeros((H, W), np.uint8)
    out = []
    cur = rgb.copy()
    for k, m in enumerate(bands[:-1]):  # the farthest layer stays: it is the last thing on screen before the cut
        a = np.array(Image.open(m).getchannel("A").resize((W, H)))
        hole = np.maximum(hole, (a > 40).astype(np.uint8) * 255)
        grown = cv2.dilate(hole, np.ones((25, 25), np.uint8))
        small = cv2.resize(cur, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        hs = cv2.resize(grown, (W // 4, H // 4), interpolation=cv2.INTER_NEAREST)
        fill = cv2.inpaint(cv2.cvtColor(small, cv2.COLOR_RGB2BGR), hs, 15, cv2.INPAINT_TELEA)
        fill = cv2.GaussianBlur(cv2.cvtColor(fill, cv2.COLOR_BGR2RGB), (0, 0), 3)
        fill = cv2.resize(fill, (W, H), interpolation=cv2.INTER_CUBIC)
        soft = cv2.GaussianBlur(grown.astype(np.float32), (0, 0), 9)[:, :, None] / 255
        cur = (rgb * (1 - soft) + fill * soft).astype(np.uint8)
        path = f"{prefix}-{k}.jpg"
        Image.fromarray(cur).save(path, quality=90)
        out.append(path)
    return out
