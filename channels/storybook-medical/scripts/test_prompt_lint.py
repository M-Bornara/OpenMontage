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
# L40 (HCS07 s4b v1): a keyframe of the same set as reference for another camera = a copy of that keyframe
l40 = prompt_kit.lint_all({"s4b": {"refs": ["kf:s4a"], "set": "academy", "prompt": shot}})
l40ok = prompt_kit.lint_all({"s1b": {"refs": ["kf:s1a"], "set": "ward", "kf_same_view": True, "prompt": shot}})
status = "PASS" if any("L40" in m for m in l40.get("s4b", [])) and not any("L40" in m for v in l40ok.values() for m in v) else "FAIL"
print(f"{status} L40 earlier keyframe as reference for another camera caught")
ok = ok and status == "PASS"
# L41 (HCS07 s1a v1): "faces are above the frame" -> headless bodies
l41 = prompt_kit.lint_all({"s1a": {"prompt": shot + " Three pairs of crossed arms; their faces are above the frame."}})
l41ok = prompt_kit.lint_all({"s1a": {"prompt": shot + " Three men, whole heads in frame, arms crossed."}})
status = "PASS" if any("L41" in m for m in l41.get("s1a", [])) and not any("L41" in m for v in l41ok.values() for m in v) else "FAIL"
print(f"{status} L41 'faces above the frame' (headless) caught")
ok = ok and status == "PASS"
# L42 (HCS07 s4b v1, user 2026-11-15): one shared crowd description -> one bearded face cloned on every body
l42 = prompt_kit.lint_all({"s4b": {"prompt": shot + " CROWD: about twelve bearded Spanish-Cuban academics in black "
                                   "frock coats on the benches, most with their arms crossed, sceptical."}})
l42ok = prompt_kit.lint_all({"s4b": {"prompt": shot + " " + prompt_kit.crowd("academics on the benches", [
    "an old bald man with white side-whiskers, shaking his head", "a thin clean-shaven young man hiding a smirk"])}})
status = "PASS" if any("L42" in m for m in l42.get("s4b", [])) and not any("L42" in m for v in l42ok.values() for m in v) else "FAIL"
print(f"{status} L42 crowd without casting cards (cloned faces) caught")
ok = ok and status == "PASS"
# L43 (layered shots, user 2026-11-16): a sprite sheet on a busy background / unlit to the plate; an empty plate that
# doesn't hold the frame. The kit's templates pass, and pass the sheet rules (no SHOT / SET / framing demands).
bad = {"sprite-x": {"aspect": "16:9", "prompt": "Sprite sheet of a mosquito in four states on a wooden desk."},
       "plate-x": {"aspect": "9:16", "refs": ["kf:s3"], "prompt": "Empty plate: the same hand without the mosquito."}}
good = {"sprite-x": {"aspect": "16:9", "prompt": prompt_kit.sprite_sheet(
            "mosquito", ["flying, wings up", "landed"], "s3", "warm lamp light from the right", "from above")},
        "plate-x": {"aspect": "9:16", "refs": ["kf:s3"], "prompt": prompt_kit.empty_plate(
            "Finlay at his desk", "the mosquito on his hand", "the clean skin of the back of his hand")}}
l43, l43ok = prompt_kit.lint_all(bad, require_matt=False), prompt_kit.lint_all(good, require_matt=False)
status = "PASS" if all(any("L43" in m for m in l43.get(n, [])) for n in bad) and not l43ok else "FAIL"
print(f"{status} L43 sprite sheet / empty plate without the layered-shot templates caught{'' if not l43ok else f' (template findings: {l43ok})'}")
ok = ok and status == "PASS"
# L44-L46 (HC002-S1 first HERO pieces, 2026-11-18): swatches; a model sheet printed as ghosts under a sprite / pose
# sheet; "(no bar drawn)" drawn as the wrong tool.
bad = {"pose-x": {"aspect": "16:9", "refs": ["ref:sheet-gage"], "prompt": prompt_kit.pose_sheet(
           "a man", ["standing, both hands on a bar (no bar drawn)", "thrown back"], "s1", "light from the left", "front"
       ).replace(prompt_kit.REF_IDENTITY_ONLY, "")}}
good = {"pose-x": {"aspect": "16:9", "refs": ["ref:sheet-gage"], "prompt": prompt_kit.pose_sheet(
            "a man", ["standing. " + prompt_kit.EMPTY_HANDS, "thrown back"], "s1", "light from the left", "front")}}
bad["lie-x"] = {"aspect": "16:9", "refs": ["ref:sheet-gage"], "prompt": prompt_kit.pose_sheet(
    "a man", ["lying flat on his back", "propped on an elbow"], "s8", "light from the right", "side")}
bad["plate-x"] = {"aspect": "9:16", "prompt": "EMPTY LOCATION PLATE: no people. The near foreground is clear (a man's shoulder and hand are added there later, large). " + prompt_kit.SAFE_FRAMING}
lb, lg = prompt_kit.lint_all(bad, require_matt=False), prompt_kit.lint_all(good, require_matt=False)
assert any(m.startswith("L47") for m in lb.get("plate-x", [])), "L47 empty plate naming body parts not caught"
assert any(m.startswith("L45b") for m in lb.get("lie-x", [])), "L45b lying pose with a sheet reference not caught"
import episode  # noqa: E402
status = ("PASS" if {"L45", "L46"} <= {m[:3] for m in lb.get("pose-x", [])} and not lg
          and "swatch" in prompt_kit.NO_TEXT and "swatch" in episode.TAIL else "FAIL")
print(f"{status} L44 swatches forbidden, L45 sheet ghosts, L46 '(no X drawn)' caught{'' if not lg else f' (template findings: {lg})'}")
ok = ok and status == "PASS"
# L51 (user 2026-11-19, HC002-S1 s3): a close-up with a hand must state every object's size against the hand
bad = {"s3": {"prompt": prompt_kit.framing("INSERT", "top view", "50 mm", "a hand tips a small powder flask over a drill hole")
              + " A small wooden powder keg at the edge. Only one hand and cuff are in the picture."},
       "s11": {"prompt": prompt_kit.framing("CU", "eye level", "85 mm", "a young man's hand grips an iron rod")}}
good = {"s3": {"prompt": bad["s3"]["prompt"] + " " + prompt_kit.scale({"the powder flask": "about the size of his fist",
                                                                       "the drill hole": "about 2 in across"})},
        "s5": {"prompt": prompt_kit.framing("ECU", "low", "100 mm macro", "the lip of a drill hole") + " No iron bar, no hand, no spark."},
        "plate": {"prompt": prompt_kit.framing("CU", "eye level", "50 mm", "an empty desk") + " NO PEOPLE anywhere: no people, no hands."}}
lb, lg = prompt_kit.lint_all(bad, require_matt=False), prompt_kit.lint_all(good, require_matt=False)
caught = [n for n in bad if any(m.startswith("L51") for m in lb.get(n, []))]
fp = {n: m for n, ms in lg.items() for m in ms if m.startswith("L51")}
status = "PASS" if len(caught) == len(bad) and not fp else "FAIL"
print(f"{status} L51 hand close-ups without a SCALE line caught ({len(caught)}/{len(bad)}), no false positives ({fp or 'none'})")
ok = ok and status == "PASS"
# L50 (story-craft Rule 0b, user 2026-11-19): a violent storyboard row must name its softening tool
import storyboard_lint  # noqa: E402
H = ["| # | Narration | What we see | SFX |", "|---|---|---|---|"]
bad = storyboard_lint.lint_md(chr(10).join(H + [
    "| 1 | The bar shot through his skull. | Gage thrown back | a hit |",
    "| 2 | He drank the cholera. | glass to his lips · 0b: dramatic | gulp |"]))
good = storyboard_lint.lint_md(chr(10).join(H + [
    "| 1 | The bar shot through his skull. | 0b: silhouette + white flash + head snap | hit |",
    "| 2 | The iron falls in from the top. | the bar lands in the grass | thud |",
    "| 3 | His job: pack powder in the rock cut, arm up. | a hand pours powder | hiss |"]))
status = "PASS" if len(bad) == 2 and not good else "FAIL"
print(f"{status} L50 violent rows without a Rule 0b tool caught ({len(bad)}/2), no false positives ({good or 'none'})")
ok = ok and status == "PASS"
# L47b (user 2026-11-19, HC002-S1 2a/2b): a full set plate as a reference carries its camera
mb = "SHOT: LS, high angle from the hillside. The crew swing sledgehammers."
l47b_bad = [prompt_kit.lint("s2b", {"refs": ["ref:plate-cut", "ref:sheet-gage"], "roles": "Reference 1 is the set plate, for the style ONLY: do NOT copy its camera. ", "prompt": mb}),
            prompt_kit.lint("s9", {"refs": ["proj:refs/plate-s1.png"], "prompt": mb})]
l47b_good = [prompt_kit.lint("s2b", {"refs": ["proj:refs/plate-cut-detail.png", "ref:sheet-gage"], "prompt": mb}),
             prompt_kit.lint("s2b", {"refs": ["ref:sheet-gage"], "prompt": mb}),
             prompt_kit.lint("s5b", {"refs": ["ref:plate-ward"], "prompt": mb + " " + prompt_kit.SAME_CAMERA})]
ok47 = all(any(i.startswith("L47b") for i in x) for x in l47b_bad) and not any(i.startswith("L47b") for x in l47b_good for i in x)
status = "PASS" if ok47 else "FAIL"
print(f"{status} L47b full set plate reference caught (2 bad), detail crop / no plate / SAME_CAMERA pass (3 good)")
ok = ok and status == "PASS"
# L54 (HC002-S1 pose-friend-s12, 2026-11-20): a pose sheet must be 16:9
ps = prompt_kit.pose_sheet("a man", ["standing", "leaning"], "12: a doorway", "daylight", "eye level")
l54_bad = prompt_kit.lint("pose-friend-s12", {"aspect": "9:16", "refs": ["kf:s12"], "prompt": ps})
l54_good = prompt_kit.lint("pose-friend-s12", {"aspect": "16:9", "refs": ["kf:s12"], "prompt": ps})
status = "PASS" if any(i.startswith("L54") for i in l54_bad) and not any(i.startswith("L54") for i in l54_good) else "FAIL"
print(f"{status} L54 9:16 pose sheet caught, 16:9 passes")
ok = ok and status == "PASS"
# L40 (no set) / L55 / L55b (user 2026-11-20 "backgrounds keep looking the same"; view_check audit: 28 stills copied their plate)
import importlib.util  # noqa: E402


def _kf(rel):
    f = REPO / "channels/storybook-medical/editorial/episodes" / rel
    spec = importlib.util.spec_from_file_location(f.stem, f)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.KEYFRAMES


semm, snow = _kf("HCS09-semmelweis/build_hcs09.py"), _kf("HCS08-john-snow/build_hcs08.py")
has_code = lambda iss, c: any(re.match(rf"{c}\b", i) for i in iss)  # noqa: E731
import re  # noqa: E402
l55_bad = prompt_kit.lint("s1b", semm["s1b"])                       # "SET: the hospital, a corridor." and no camera()
l47c_bad = [prompt_kit.lint(n, snow[n]) for n in ("s2", "s3")]       # kf:s1a as a reference -> s1a's street
good = {"aspect": "9:16", "refs": ["ref:sheet-x"], "prompt": prompt_kit.set_block("A hygiene laboratory", "1892", "wooden benches") + " "
        + prompt_kit.framing("MS", "eye level", "50 mm", "he raises his palm") + " "
        + prompt_kit.camera("by the window", "east", "the long bench with flasks and a brass microscope, the shelves of jars behind")}
twin = dict(good, prompt=good["prompt"].replace("MS,", "CU,").replace("SHOT: medium", "SHOT: close"))
seq = prompt_kit.lint_sequence({"a": good, "b": twin})
# a later return to the same place from ANOTHER camera passes (user 2026-11-20); the same camera later still fails
other = {"aspect": "9:16", "refs": [], "prompt": prompt_kit.framing("LS", "eye level", "24 mm", "a street") + " "
         + prompt_kit.camera("on the kerb", "south", "a row of brick houses with green doors and a gas lamp on the corner")}
back = dict(good, prompt=good["prompt"].replace("standing by the window", "standing at the door").replace("facing east", "facing west"))
ret_ok = not [m for m in prompt_kit.lint_sequence({"a": good, "x": other, "c": back}) if m.startswith(("L55b", "L36"))]
ret_bad = any(m.startswith("L55b") for m in prompt_kit.lint_sequence({"a": good, "x": other, "c": twin}))
ok55 = (has_code(l55_bad, "L55") and all(has_code(x, "L40") for x in l47c_bad)
        and not [i for i in prompt_kit.lint("a", good) if re.match(r"L(37|40|47b|55)", i)] and any(m.startswith("L55b") for m in seq)
        and ret_ok and ret_bad)
status = "PASS" if ok55 else "FAIL"
print(f"{status} L55 thin setting (HCS09 s1b), L40 kf: reference without a set (HCS08 s2/s3), L55b back-to-back / same-camera background caught, a return from another camera passes; full spec passes")
ok = ok and status == "PASS"
# L57 / L58 / L59 (HCS10 2026-11-20): the first pose-hand-s7 and plate-s4 prompts, as they were sent
hand_v1 = {"aspect": "16:9", "refs": [], "prompt": prompt_kit.pose_sheet(
    "his RIGHT hand, seen from above, with a loose sheet of paper covered in faint wavy handwriting under the hand",
    ["the hand lying flat on the sheet", "the fingers curl and clutch the paper, crumpling it into the palm"],
    "s7", "grey light", "from above", "the hand only")}
hand_v2 = {"aspect": "16:9", "refs": [], "prompt": prompt_kit.pose_sheet(
    "his RIGHT hand, seen from above, with a loose sheet of paper with faint grey wavy lines, no letters, under the hand",
    ["the hand lying flat on the sheet", "the fingers curl and clutch the paper, crumpling it: the sheet still at its full size, "
     "mostly spread, its near half dragged into creases"], "s7", "grey light", "from above", "the hand only")}
plate_v1 = {"aspect": "9:16", "refs": [], "prompt": "the empty space behind the bench. The professor is NOT in this picture. "
            + prompt_kit.matt_beat("a suit", "by the cabinets, writing")}
plate_v2 = dict(plate_v1, prompt=plate_v1["prompt"].replace("by the cabinets", "at the far right by the cabinets, away from the empty place"))
c1, c2 = prompt_kit.lint("h1", hand_v1), prompt_kit.lint("h2", hand_v2)
ok57 = (has_code(c1, "L57") and has_code(c1, "L58") and not has_code(c2, "L57") and not has_code(c2, "L58")
        and has_code(prompt_kit.lint("p1", plate_v1), "L59") and not has_code(prompt_kit.lint("p2", plate_v2), "L59"))
status = "PASS" if ok57 else "FAIL"
print(f"{status} L57 'handwriting' in a sheet (Lorem ipsum), L58 a crumpled prop keeps its full size, L59 Matt away from the empty place (HCS10 s7 / s4)")
ok = ok and status == "PASS"
sys.exit(0 if ok else 1)
