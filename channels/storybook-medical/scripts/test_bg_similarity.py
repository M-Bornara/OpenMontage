"""Regression test for bg_similarity (review 2026-11-25): two stills of the same set a cut apart must FAIL; different sets and a
different crop of one still must PASS.
Known failure: HC002-L rows 9 -> 10 (S1 s2b -> s2a, the same quarry at the same size, read as a jump cut).
Mahdi's note named "rows 10 and 11"; in the cut those two are the quarry and the keg shed (different sets), so they are the NEGATIVE control.
Run: python channels/storybook-medical/scripts/test_bg_similarity.py   (needs the local HC002 media; skips when it is missing)"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bg_similarity as bg  # noqa: E402

S1 = "projects/hc002-s1/assets/images/keyframes16x9/"
L = "projects/hc002-l/assets/images/keyframes16x9/"
push = lambda a, b: {"type": "push", "from": a, "to": b}                                    # noqa: E731
keys = lambda cx, cy, s: {"type": "keys", "keys": [{"t": 0, "scale": s, "x": (0.5 - cx) * 100 * s, "y": (0.5 - cy) * 100 * s},
                                                    {"t": 4, "scale": s, "x": (0.5 - cx) * 100 * s, "y": (0.5 - cy) * 100 * s}]}   # noqa: E731
sh = lambda i, src, m, a, b: {"id": i, "source": src, "motion": m, "start": a, "end": b}     # noqa: E731

CASES = [   # (name, earlier shot, later shot, must the check flag it?)
    ("rows 9 -> 10: s2b then s2a, same quarry, same size (the known failure)",
     sh("r09", S1 + "s2b.png", push(1.04, 1.12), 0, 4), sh("r10", S1 + "s2a.png", push(1.04, 1.16), 4, 8), True),
    ("rows 10 -> 11: the quarry then the keg shed (different sets)",
     sh("r10", S1 + "s2a.png", push(1.04, 1.16), 0, 4), sh("r11", L + "row11-keg-v1.png", push(1.04, 1.14), 4, 8), False),
    ("one still used twice at the same crop (monster, rows 34 -> 35 before the new crops)",
     sh("a", L + "row7-monster-v1.png", push(1.06, 1.2), 0, 4), sh("b", L + "row7-monster-v1.png", push(1.2, 1.26), 4, 8), True),
    ("one still, two different crops (wide, then the eye at 2.3x)",
     sh("a", L + "row7-monster-v1.png", keys(0.5, 0.5, 1.3), 0, 4), sh("b", L + "row7-monster-v1.png", keys(0.56, 0.36, 2.3), 4, 8), False),
]
ok = True
if not (HERE.parents[2] / "projects/hc002-l").exists():
    print("SKIP: projects/hc002-l is not on this machine")
    sys.exit(0)
for name, a, b, want in CASES:
    res = bg.compare("hc002-l", a, b)
    got = bool(res and res[0])
    print(f"{'PASS' if got == want else 'FAIL'}  {name}: {'flagged' if got else 'passed'} ({res[1] if res else 'no picture'})")
    ok &= got == want
sys.exit(0 if ok else 1)
