"""Regression test for prompt_kit.lint: the recorded first-pass failures must stay caught.
Run: python channels/storybook-medical/scripts/test_prompt_lint.py   (add each new episode's failed prompts below)"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
import prompt_kit  # noqa: E402

CASES = [
    # (prompt file that defines KF, names that failed review, minimum number the lint must catch)
    (REPO / "channels/storybook-medical/editorial/episodes/HC001-st-martin/keyframes_hc001.py",
     "M03 M10 M13 M14 M17 M25 M29 M31 M32 M33 M34 I02 I05 I06 I08 I09 I10 I11 I12 I13 I14 I17 I19 I20 I22".split(), 23),
]

ok = True
for path, failed, minimum in CASES:
    src = path.read_text(encoding="utf-8")
    ns: dict = {}
    exec(src[:src.index("ep = json.load(open(P")], ns)            # prompt definitions only, no file writes
    kf = ns["KF"]
    flagged = prompt_kit.lint_all(kf)
    caught = [n for n in failed if n in kf and n in flagged]
    status = "PASS" if len(caught) >= minimum else "FAIL"
    ok &= status == "PASS"
    print(f"{status} {path.parent.name}: lint catches {len(caught)}/{len([n for n in failed if n in kf])} recorded failures (min {minimum})")
# L28 (HCS03 v1 s5 -> s6): the same valley twice at the same size, and a story frame with no SHOT line
valley = "SET: Snowy mountains and a frozen river outside Narvik, May 1999. "
seq = {"s5": {"aspect": "9:16", "prompt": valley + prompt_kit.framing("ELS", "eye level", "24 mm", "rescuers at the hole")},
       "s6": {"aspect": "9:16", "prompt": valley + prompt_kit.framing("ELS", "eye level", "24 mm", "a helicopter lands")},
       "s7": {"aspect": "9:16", "prompt": valley + "Wide frame: a helicopter."}}
l28 = prompt_kit.lint_all(seq)
status = "PASS" if any("L28: s5 -> s6" in m for m in l28.get("s6", [])) and any("no SHOT" in m for m in l28.get("s7", [])) else "FAIL"
ok &= status == "PASS"
print(f"{status} L28 decoupage: repeated set+size and missing SHOT line caught")
sys.exit(0 if ok else 1)
