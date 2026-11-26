"""Free prep for the new cold open (Mahdi 2026-11-25), once:
  - the two Omni 720p clips (C2 blast 24 fps, C3 iron in flight) -> 1920x1080 lanczos, frame-blended to 30 fps, a little grain like the other clips, no audio
    (they play at natural speed and length; the edit only chooses how much of them it shows)
  - the new stills copied into assets/images/keyframes16x9 (the long's still folder)
    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/prep_cold_open.py
"""
import shutil
import subprocess
from pathlib import Path

P = Path("projects/hc002-l")
V, K, K16 = P / "assets/video", P / "assets/images/keyframes", P / "assets/images/keyframes16x9"
for src, dst in (("cold-c2-blast-omni-v1", "cold-c2-1080p30"), ("cold-c3-rod-omni-v1", "cold-c3-1080p30")):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / f"{src}.mp4"), "-vf", "scale=1920:1080:flags=lanczos,framerate=fps=30,noise=alls=5:allf=t",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-an", str(V / f"{dst}.mp4")], check=True)
    print(dst)
# the four cold-open Omni clips (when they exist): raw cold-kN-<name>-omni-v1.mp4 -> cold-kN-<name>-1080p30.mp4, the files the edit script's slots look for
for raw, dst in (("cold-k1-pour-omni-v1", "cold-k1-pour-1080p30"), ("cold-k2-tamp-omni-v1", "cold-k2-tamp-1080p30"),
                 ("cold-k3-glance-omni-v1", "cold-k3-glance-1080p30"), ("cold-k4-spark-omni-v1", "cold-k4-spark-1080p30")):
    if (V / f"{raw}.mp4").exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / f"{raw}.mp4"), "-vf", "scale=1920:1080:flags=lanczos,framerate=fps=30,noise=alls=5:allf=t",
                        "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-an", str(V / f"{dst}.mp4")], check=True)
        print(dst, "(slot filled)")
for n in ("cold-r1-pour-v1", "cold-b1-tip-v1", "cold-b5-dust-v1", "row5-dazed-v1-soot", "row9-hilltop-v1", "row43b-shelf-v2", "title-bg-v1"):
    shutil.copy(K / f"{n}.png", K16 / f"{n}.png")
    print(n)
