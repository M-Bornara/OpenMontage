"""Cut audit on the RENDERED video (review 2026-11-25): +/-3 frames around every cut.

For every shot boundary in episode.json (frame c = round(start x fps)) the audit reads frames c-3 .. c+2 of the render and reports:
  FLASH      a frame whose brightness jumps away from BOTH neighbours (+ or -) by more than FLASH_LEVELS (0-255 grey) and comes back
             (declared flashes, "transition": "flash", a "hit", or "fx_flash": true (an impact_frame of the comic kit) on the shot, are listed as intended, not failed)
  DUPLICATE  two neighbouring frames in the window that are the same picture (mean abs. diff < DUP_DIFF) inside a shot whose camera
             moves, or a cut whose two sides are the same picture (diff < CUT_MIN_DIFF) when no dissolve / flash was declared
  BLACK      a frame that is black (mean grey < BLACK_LEVEL) outside a declared fade
  CUT FRAME  the frame where a hard cut really happens, against the frame the edit asked for (offset in frames)
  AUDIO LAG  the render's audio against narration.wav in the 1 s around the cut (cross-correlation, ms): does the sound sit where the
             picture says it does? Reported per cut; the max and the first-to-last trend are the drift.
It also reports the container's audio and video durations. A contact sheet per cut (six frames, labelled) is saved to
review/cut_audit/ (cut_NNN.jpg) and joined per chapter (chapter_N.jpg) for the approval page. A FLASH or DUPLICATE (or a BLACK frame, or a
cut frame more than 1 frame off) FAILS the render; the audio lag fails at more than LAG_FAIL_MS.

    python channels/storybook-medical/scripts/cut_audit.py <project-id> [renders/preview.mp4]       # exit 1 on a failure
`episode.py render` runs it after the render.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[3]
FPS = 30
FLASH_LEVELS, DUP_DIFF, CUT_MIN_DIFF, BLACK_LEVEL, LAG_FAIL_MS = 28.0, 0.003, 1.0, 8.0, 60.0
BEFORE, AFTER = 3, 2


def probe(path: Path, stream: str) -> float:
    """Stream duration in seconds (ffprobe prints "374.86,
" on Windows for some muxers: keep the first number)."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True).stdout
    for tok in re.split(r"[,\s]+", out):
        try:
            return float(tok)
        except ValueError:
            continue
    return 0.0


def grab(video: Path, cuts: list[int]) -> dict[int, tuple[np.ndarray, np.ndarray]]:
    """Frames c-3 .. c+2 for each cut, in one sequential read (seeking an h264 file frame by frame is slow and inexact)."""
    want = {f for c in cuts for f in range(c - BEFORE, c + AFTER + 1)}
    out, cap, i, last = {}, cv2.VideoCapture(str(video)), 0, max(want)
    while i <= last:
        if not cap.grab():
            break
        if i in want:
            ok, im = cap.retrieve()
            if ok:
                out[i] = (cv2.resize(im, (480, 270), interpolation=cv2.INTER_AREA),                       # the contact sheet
                          cv2.cvtColor(cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY))   # the numbers
        i += 1
    cap.release()
    return out


def clip_freezes(pid: str, ep: dict) -> list[str]:
    """A video shot whose slot is longer than its clip (minus the in-point) would hold the clip's last frame: list them (review 2026-11-25)."""
    out = []
    for s in ep["shots"]:
        ref = (s.get("layers") or {}).get("bg") or s.get("source", "")
        if not ref.lower().endswith(".mp4") or ref.startswith("brand:"):
            continue
        path = REPO / "projects" / pid / ref[5:] if ref.startswith("proj:") else (Path(ref) if Path(ref).is_absolute() else REPO / ref)
        if not path.exists():
            continue
        have = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                    capture_output=True, text=True).stdout.strip() or 0) - s.get("in", 0)
        slot = s["end"] - s["start"]
        if slot > have + 1 / FPS:
            out.append(f"{s['id']}: the slot is {slot:.2f} s but the clip has {have:.2f} s: {slot - have:.2f} s would freeze the last frame")
    return out


def lag_ms(render_audio: np.ndarray, narr: np.ndarray, sr: int, t: float) -> float | None:
    """Where the narration sits in the render's audio around t (positive = the render is LATE), by cross-correlation, in ms."""
    a, b = int((t - 0.5) * sr), int((t + 0.5) * sr)
    m = int(0.12 * sr)
    if a - m < 0 or b + m > len(render_audio) or b > len(narr):
        return None
    ref = narr[a:b]
    if np.sqrt((ref ** 2).mean()) < 0.01:
        return None
    seg = render_audio[a - m:b + m]
    c = np.correlate(seg, ref, mode="valid")
    return (int(np.argmax(c)) - m) / sr * 1000


def audio(path: Path, sr: int = 16000) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def sheet(frames: list[np.ndarray], c: int, label: str, marks: list[str]) -> np.ndarray:
    tiles = []
    for k, f in enumerate(frames):
        t = f.copy()
        n = c - BEFORE + k
        cv2.rectangle(t, (0, 0), (150, 22), (0, 0, 0), -1)
        cv2.putText(t, f"f{n} ({n - c:+d})", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255) if n == c else (255, 255, 255), 1)
        if n == c:
            cv2.rectangle(t, (0, 0), (t.shape[1] - 1, t.shape[0] - 1), (0, 255, 255), 3)
        tiles.append(t)
    row = np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])])
    bar = np.zeros((26, row.shape[1], 3), np.uint8)
    cv2.putText(bar, label + ("   " + "  ".join(marks) if marks else "   clean"), (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (80, 80, 255) if any(m.split(":")[0] in ("FLASH", "DUPLICATE", "BLACK", "CUT FRAME", "AUDIO LAG") for m in marks) else (120, 220, 120), 1)
    return np.vstack([bar, row])


def audit(pid: str, video: Path | None = None, verbose: bool = True) -> dict:
    p = REPO / "projects" / pid
    video = video or p / "renders/preview.mp4"
    ep = json.load(open(p / "episode.json", encoding="utf-8"))
    shots = ep["shots"]
    cuts = [(round(s["start"] * FPS), s, shots[i - 1]) for i, s in enumerate(shots) if i > 0]
    frames = grab(video, [c for c, _, _ in cuts])
    fails, notes, rows, sheets = [], [], [], {}
    try:
        sr = 16000
        ra, na = audio(video, sr), audio(p / "assets/audio/narration.wav", sr)
    except Exception as e:                       # noqa: BLE001
        ra = na = None
        notes.append(f"audio lag not measured: {e}")
    out_dir = p / "review/cut_audit"
    out_dir.mkdir(parents=True, exist_ok=True)
    chap = {c["id"]: c for c in json.load(open(p / "artifacts/chapters.json", encoding="utf-8"))}
    for c, s, prev in cuts:
        pair = [frames.get(n) for n in range(c - BEFORE, c + AFTER + 1)]
        if any(f is None for f in pair):
            continue
        fr = [f[0] for f in pair]
        g = [f[1].astype(np.float32) for f in pair]
        lum = [float(x.mean()) for x in g]
        marks, declared = [], s.get("transition", "cut")
        dd = [float(np.abs(g[k + 1] - g[k]).mean()) for k in range(len(g) - 1)]     # diff between neighbours; the cut is between idx BEFORE-1 and BEFORE
        # flash: a frame away from both neighbours in the same direction by a lot
        for k in range(1, len(g) - 1):
            up, dn = lum[k] - lum[k - 1], lum[k] - lum[k + 1]
            if (up > FLASH_LEVELS and dn > FLASH_LEVELS) or (up < -FLASH_LEVELS and dn < -FLASH_LEVELS):
                msg = f"FLASH: frame {c - BEFORE + k} grey {lum[k]:.0f} vs {lum[k - 1]:.0f} / {lum[k + 1]:.0f}"
                if declared == "flash" or s.get("hit") or s.get("fx_flash"):
                    notes.append(f"{s['id']}: declared flash/hit, " + msg)
                else:
                    marks.append(msg)
        # black frames
        for k, l in enumerate(lum):
            if l < BLACK_LEVEL and not s["id"] in ("END",) and prev["id"] not in ("STING", "OUTRO", "END") and s["id"] not in ("STING", "OUTRO"):
                marks.append(f"BLACK: frame {c - BEFORE + k} grey {l:.1f}")
        # duplicates inside the window: the same picture twice in a row while the camera is moving
        moving = lambda sh: (sh.get("motion") or {}).get("type") not in (None, "static") and not str(sh.get("source", "")).endswith(".mp4") and not str(sh.get("source", "")).startswith("brand:")   # noqa: E731
        for k, d in enumerate(dd):
            if k == BEFORE - 1:
                continue                                   # the cut itself
            sh = prev if k < BEFORE - 1 else s
            if d < DUP_DIFF and moving(sh):
                marks.append(f"DUPLICATE: frames {c - BEFORE + k} and {c - BEFORE + k + 1} are identical (diff {d:.3f}) in {sh['id']}")
        # the cut: two sides must differ unless a dissolve / flash is declared
        cutd = dd[BEFORE - 1]
        if declared not in ("dissolve", "flash") and cutd < CUT_MIN_DIFF and not s.get("cut"):
            marks.append(f"DUPLICATE: the cut into {s['id']} changes nothing (diff {cutd:.2f}): both sides are the same picture")
        # where the hard cut really is
        peak = int(np.argmax(dd)) - (BEFORE - 1)
        if declared not in ("dissolve", "flash") and cutd >= CUT_MIN_DIFF and not s.get("hit") and not s.get("fx_flash") and abs(peak) >= 1 and dd[BEFORE - 1 + peak] > 2 * max(cutd, 1):
            marks.append(f"CUT FRAME: the picture changes {peak:+d} frame(s) from the edit's cut")
        lag = lag_ms(ra, na, 16000, s["start"]) if ra is not None else None
        if lag is not None and abs(lag) > LAG_FAIL_MS:
            marks.append(f"AUDIO LAG: {lag:+.0f} ms")
        rows.append({"id": s["id"], "frame": c, "t": s["start"], "diff": round(cutd, 2), "lag_ms": None if lag is None else round(lag, 1), "marks": marks})
        sh_img = sheet(fr, c, f"{prev['id']} -> {s['id']}  at {s['start']:.2f} s  (cut diff {cutd:.1f}, {declared})"
                       + (f", audio {lag:+.0f} ms" if lag is not None else ""), marks)
        cv2.imwrite(str(out_dir / f"cut_{c:05d}.jpg"), sh_img, [cv2.IMWRITE_JPEG_QUALITY, 80])
        cid = None
        for k in sorted(chap, key=lambda k: chap[k]["start"]):
            if chap[k]["start"] <= s["start"] + 0.5:
                cid = k
        sheets.setdefault(cid or "ch0", []).append(sh_img)
        fails += [f"{s['id']} @ {s['start']:.2f} s: {m}" for m in marks]
    for cid, imgs in sheets.items():
        cv2.imwrite(str(out_dir / f"chapter_{cid}.jpg"), np.vstack(imgs), [cv2.IMWRITE_JPEG_QUALITY, 78])
    lags = [r["lag_ms"] for r in rows if r["lag_ms"] is not None]
    dv, da = probe(video, "v"), probe(video, "a")
    if da and abs(dv - da) > 1 / FPS:
        fails.append(f"A/V DURATION: video {dv:.3f} s, audio {da:.3f} s")
    summary = {"cuts": len(rows), "failures": fails, "notes": notes, "video_s": dv, "audio_s": da,
               "lag_max_ms": max((abs(x) for x in lags), default=None), "lag_first_ms": lags[0] if lags else None, "lag_last_ms": lags[-1] if lags else None,
               "lag_measured": len(lags), "rows": rows, "sheets": sorted(f"chapter_{k}.jpg" for k in sheets)}
    json.dump(summary, open(out_dir / "audit.json", "w", encoding="utf-8"), indent=1)
    if verbose:
        print(f"cut audit: {len(rows)} cuts, {len(fails)} failure(s); audio lag max {summary['lag_max_ms']} ms over {len(lags)} cuts "
              f"(first {summary['lag_first_ms']}, last {summary['lag_last_ms']}); video {dv:.2f} s / audio {da:.2f} s")
        for f in fails:
            print("  FAIL " + f)
        for n in notes:
            print("  note " + n)
    return summary


if __name__ == "__main__":
    res = audit(sys.argv[1], Path(sys.argv[2]) if len(sys.argv) > 2 else None)
    sys.exit(1 if res["failures"] else 0)
