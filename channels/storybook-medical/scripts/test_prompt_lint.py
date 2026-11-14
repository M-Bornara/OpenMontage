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
# L29 (user 2026-11-07): a video with no Matt cameo in any story shot
l29 = prompt_kit.lint_all({"s1": {"prompt": "SHOT: MS, eye level. A doctor at a desk."}})
l29ok = prompt_kit.lint_all({"s1": {"prompt": "SHOT: MS, eye level. A doctor at a desk. " + prompt_kit.matt_beat("a 1980s suit", "reading a newspaper")}})
status = "PASS" if any("L29" in m for m in l29.get("s1", [])) and not any("L29" in m for v in l29ok.values() for m in v) else "FAIL"
print(f"{status} L29 Matt cameo: missing cameo caught, matt_beat() accepted")
ok = ok and status == "PASS"
# L30 (HCS04 prop-eye v1): a prop model sheet referencing a room plate
l30 = prompt_kit.lint_all({"prop-eye": {"aspect": "16:9", "refs": ["x/plate-study.png"], "prompt": "Clean prop model sheet: a gold eye."}}, require_matt=False)
l30ok = prompt_kit.lint_all({"prop-eye": {"aspect": "16:9", "refs": ["x/sheet-osler.png"], "prompt": "Clean prop model sheet: a gold eye."}}, require_matt=False)
status = "PASS" if any("L30" in m for m in l30.get("prop-eye", [])) and not l30ok else "FAIL"
print(f"{status} L30 model sheet with a room plate reference caught")
ok = ok and status == "PASS"
# L31 (HCS06 s3b v1): a memory look "with a soft vignette" painted as a bordered card
l31 = prompt_kit.lint_all({"s3b": {"prompt": "SHOT: insert. A village with a soft vignette at the edges. " + prompt_kit.matt_beat("x", "y")}})
l31ok = prompt_kit.lint_all({"s3b": {"prompt": "SHOT: insert. A village with a soft vignette. " + prompt_kit.FULL_BLEED + prompt_kit.matt_beat("x", "y")}})
status = "PASS" if any("L31" in m for m in l31.get("s3b", [])) and not any("L31" in m for v in l31ok.values() for m in v) else "FAIL"
print(f"{status} L31 vignette without full-bleed caught")
ok = ok and status == "PASS"
# L32 (HCS06 s6a v1): a crowd passed to cast() as one person
l32 = prompt_kit.lint_all({"s6a": {"prompt": "SHOT: LS. " + prompt_kit.cast("six angry townspeople at the door") + prompt_kit.matt_beat("x", "y")}})
l32ok = prompt_kit.lint_all({"s6a": {"prompt": "SHOT: LS. " + prompt_kit.cast("a doctor", "his son") + prompt_kit.matt_beat("x", "y")}})
status = "PASS" if any("L32" in m for m in l32.get("s6a", [])) and not any("L32" in m for v in l32ok.values() for m in v) else "FAIL"
print(f"{status} L32 crowd passed to cast() as one person caught")
ok = ok and status == "PASS"
# L34 (HCS08 s2/s9a v1): a plate role without "only" was copied whole
mb = prompt_kit.matt_beat("x", "y")
l34 = prompt_kit.lint_all({"s2": {"refs": ["ref:plate-x"], "roles": "Reference 1 is the plate, for the painting style and the pump's design. ", "prompt": "SHOT: LS. " + mb}})
l34ok = prompt_kit.lint_all({"s2": {"refs": ["ref:plate-x"], "roles": "Reference 1 is the plate, for the painting style ONLY. ", "prompt": "SHOT: LS. " + mb}})
status = "PASS" if any("L34" in m for m in l34.get("s2", [])) and not any("L34" in m for v in l34ok.values() for m in v) else "FAIL"
print(f"{status} L34 plate reference without 'only' caught")
ok = ok and status == "PASS"
# L35 (HCS09 s4a v1): a macro insert painted as a framed card
l35 = prompt_kit.lint_all({"s4a": {"prompt": "SHOT: insert shot of a detail, macro. A scalpel. " + mb}})
l35ok = prompt_kit.lint_all({"s4a": {"prompt": "SHOT: insert shot of a detail, macro. A scalpel. " + prompt_kit.FULL_BLEED + mb}})
status = "PASS" if any("L35" in m for m in l35.get("s4a", [])) and not any("L35" in m for v in l35ok.values() for m in v) else "FAIL"
print(f"{status} L35 macro insert without full-bleed caught")
ok = ok and status == "PASS"
# L36 (HCS08 s1b/s2/s3/s4b/s8 v1): five shots on one street, different sizes, same background
st = "SET: Broad Street, Soho (1854). "
l36 = prompt_kit.lint_all({"s2": {"prompt": st + "SHOT: long shot, eye level. " + mb},
                           "s3": {"prompt": "SET: elsewhere. SHOT: medium shot, x."},
                           "s8": {"prompt": st + "SHOT: medium shot, low. " + mb}})
l36b = prompt_kit.lint_all({"s2": {"prompt": st + "SHOT: long shot. " + prompt_kit.camera("across", "north", "three doors") + mb},
                            "s8": {"prompt": st + "SHOT: medium shot. " + prompt_kit.camera("across", "north", "three doors") + mb}})
l36ok = prompt_kit.lint_all({"s2": {"prompt": st + "SHOT: long shot. " + prompt_kit.camera("across", "north", "three doors") + mb},
                             "s8": {"prompt": st + "SHOT: medium shot. " + prompt_kit.camera("on the corner", "south-east", "the crossroads") + mb}})
has = lambda r: any("L36" in m for v in r.values() for m in v)  # noqa: E731
status = "PASS" if has(l36) and has(l36b) and not has(l36ok) else "FAIL"
print(f"{status} L36 same set without distinct camera() lines caught (non-consecutive shots too)")
ok = ok and status == "PASS"
# L37 (user 2026-11-09): every story shot carries a camera() line
l37 = prompt_kit.lint_all({"s1": {"prompt": "SHOT: close-up, low. A pump. " + mb}})
l37ok = prompt_kit.lint_all({"s1": {"prompt": "SHOT: close-up, low. " + prompt_kit.camera("at the kerb", "north", "a brick wall") + mb}})
status = "PASS" if any("L37" in m for m in l37.get("s1", [])) and not any("L37" in m for v in l37ok.values() for m in v) else "FAIL"
print(f"{status} L37 story shot without a camera() line caught")
ok = ok and status == "PASS"
# L38 (user 2026-11-14): a character sheet as reference without the appear-once line
shot = "SHOT: medium shot, x. " + prompt_kit.camera("here", "north", "a wall") + mb
l38 = prompt_kit.lint_all({"s1": {"refs": ["ref:sheet-finlay"], "prompt": shot}})
l38ok = prompt_kit.lint_all({"s1": {"refs": ["ref:sheet-finlay"], "prompt": shot + prompt_kit.ONE_EACH}})
status = "PASS" if any("L38" in m for m in l38.get("s1", [])) and not any("L38" in m for v in l38ok.values() for m in v) else "FAIL"
print(f"{status} L38 sheet reference without ONE_EACH caught")
ok = ok and status == "PASS"
# L39 (user 2026-11-14): a set plate leaking into another set (HCS07 v1 draft: the street plate on the camp and tent shots)
l39 = prompt_kit.lint_all({"s6a": {"refs": ["ref:plate-street"], "set": "camp", "prompt": shot},
                           "s7b": {"refs": ["ref:plate-street"], "prompt": shot}})
l39ok = prompt_kit.lint_all({"s2b": {"refs": ["ref:plate-street"], "set": "street", "prompt": shot}})
status = "PASS" if all(any("L39" in m for m in l39.get(n, [])) for n in ("s6a", "s7b")) \
    and not any("L39" in m for v in l39ok.values() for m in v) else "FAIL"
print(f"{status} L39 set plate used on another set caught")
ok = ok and status == "PASS"
sys.exit(0 if ok else 1)

