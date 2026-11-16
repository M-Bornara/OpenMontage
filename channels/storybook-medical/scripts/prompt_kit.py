"""Shared prompt building blocks + a pre-flight lint. Every lesson in plan/prompt-lessons.md that can be enforced in
code lives here, so the next episode can't repeat it. Episode prompt files import these blocks; episode.py runs
lint() on every image prompt before any paid call (stops the run on a known mistake unless --lint-ok)."""
from __future__ import annotations

import re

# L1/L2 · the style anchor shows the pilot's red-tuque voyageur, so the model pastes him into scenes. Use it only when
# Alexis-era characters are in the shot; otherwise a people-free plate of the episode is the style reference.
STYLE_ANCHOR = "kit:style-anchor.jpg"
ANCHOR_NOTE = ("Reference 1 is a STYLE reference only: copy its painting style; do NOT copy or include the man in it, "
               "and no red tuque unless this prompt asks for that character.")
NO_PEOPLE = ("NO PEOPLE anywhere in the frame: no figures, no faces, no hands unless stated. Reference 1 is a STYLE "
             "reference only: copy its painting style, never its contents.")
# L3 · square prompts drew a framed card with a white margin.
FULL_BLEED = "Full-bleed image to every edge: no border, no frame, no white margin, no vignette card."
# L4 · thumbnail/cover text side came back as a flat panel with a hard seam.
TEXT_SIDE = ("The {side} is the same scene continuing, darker, calmer and out of focus, with nothing in it. NO panel, NO "
             "border, NO flat colour block, NO split screen.")
# L5 · clock hands are never exact: draw the watch without hands, animate them in Remotion.
NO_HANDS = "the watch face has its numerals as simple marks but NO HANDS AT ALL (a centre pin only)"
# L6 · with two people in frame the model gave the opening to the wrong person / side.
def body_mark(person: str, what: str, side: str = "LEFT", where: str = "lower abdomen, just below the ribs",
              facing_camera: bool = False) -> str:
    view = {"LEFT": "RIGHT", "RIGHT": "LEFT"}[side]
    mirror_hint = f" Because he faces the camera, his {side} side appears on the VIEWER'S {view} side of the image." if facing_camera else ""
    return (f"CRITICAL: {what} is on {person}'s body only, on the {side} side of the {where}; nobody else has it.{mirror_hint} "
            f"(Check after generation; mirror the image if it lands on the wrong side.)")


# L13 · cover/thumbnail layout: a reserved band alone is ignored (hand drawn through it) or faked (blurred strip + seam).
def poster_layout(text_band: str, head_at: str, entries: str = "") -> str:
    return (f"LAYOUT: the {text_band} contains only the calm, darker continuation of the background (no hands, objects or "
            f"faces there, no blur strip, no seam). The hero's head is at about {head_at} of the frame height. {entries}")
# L7 · the model adds extra people (a duplicate of the hero, onlookers). Always state the cast.
def cast(*people: str, extra: str = "") -> str:
    n = len(people)
    who = "; ".join(people)
    return f"CAST: exactly {n} {'person' if n == 1 else 'people'}: {who}. Nobody else in the frame.{(' ' + extra) if extra else ''}"
# L8 · props with writing: the model writes words (labels on maps, "Contract", signatures).
NO_TEXT = "No text, letters, numbers, labels, signatures or watermark anywhere; any writing is illegible scribble."
# L15 · "illegible copperplate" came back as readable "Lorem ipsum ... Contract ... signature" (HC001 I13, twice).
WAVY_WRITING = ("Any handwriting is drawn ONLY as rows of soft wavy ink lines with no letters, words, numbers or signature, "
                "slightly out of focus, like writing seen from too far away to read. No heading or title on the page.")
# L16 · give the page REAL words: the model invents "Lorem ipsum" because it needs filler. A short real heading or quote
# (period-true, from the script/sources, under ~8 words) is rendered exactly; the rest of the page stays wavy lines.
def real_writing(text: str, where: str = "at the top of the page") -> str:
    return (f'The only legible writing is "{text}", handwritten in period ink {where}, spelled exactly like that. '
            f"Every other line is soft wavy ink lines with no letters. Never Latin or placeholder text.")
# L17 · story subjects at the frame edge (HC001 M17 vials) can't be zoomed, panned or focused on. Keep them in the inner area.
SAFE_FRAMING = ("FRAMING: every story-relevant person, object and action sits inside the central 70% of the frame (not touching "
                "or cut by any edge), with room around it so the camera can zoom and pan toward it; the edges hold only "
                "background.")
# L19 · every story image names its SET (place + year) with that set's own look (editorial/.../sets_<ep>.py). In HC001 v1
# the model fell back on one generic log-cabin room, so Beaumont's office was everywhere from 1822 to Osler in 1880.
def set_block(name: str, year: str, look: str) -> str:
    return (f"SET: {name}, {year}. {look}. This place has its own materials, palette and light, and must not look like "
            f"any other room or place in the film.")
# L9 · red rule and string/vial colours drift.
RED_RULE = ("Only the story's motif may be saturated red (e.g. Alexis's tuque); everything else avoids pure red. Strings "
            "are cream-white; glass vials hold amber liquid.")
# L38 · a model sheet shows several views of one person; the shot must show each person once (user, 2026-11-14).
ONE_EACH = ("Each named person appears ONCE in this image, never twice and never as a second smaller copy: the "
            "character references show several views of ONE person, so take only the face, hair and clothes from them, not "
            "their extra poses or layout. Everyone else in the image has a clearly different face, hair and age from "
            "the named people (no look-alikes, no twins).")
# L42 · one shared crowd description ("about twelve bearded academics in black frock coats", HCS07 s1a/s4b/s6a) came back
# as ONE face cloned on every body (user, 2026-11-15). A crowd is at most five visible faces, each its own casting card
# (age, build, hair, facial hair, expression all different); everyone else is seen from behind or in shadow.
def crowd(where: str, faces: list[str], rest: str = "") -> str:
    if not 1 <= len(faces) <= 5:
        raise ValueError("crowd(): give 1-5 visible faces; the rest are backs or shadow")
    cards = " ".join(f"({i}) {f}." for i, f in enumerate(faces, 1))
    return (f"CROWD: {where}. Only {len(faces)} faces are visible, and each is a different person: {cards} No two of "
            f"them share the same age, build, hair, beard or expression; they are not relatives and not look-alikes. "
            f"{rest or 'Everyone else is seen only from behind or in shadow, with no other visible faces.'}")
# L10 · period accuracy slips (castle-like forts, modern maps).
PERIOD = "Period-accurate only: nothing modern, no modern maps or borders, no anachronistic objects."
# L11 · Matt's glasses: hide them as a small visual joke (brand-signature.md).
def glasses_gag(gag: str) -> str:
    return (f"Hidden detail, small and easy to miss: a pair of round wire spectacles with amber-tinted lenses (exactly as "
            f"in the glasses reference) {gag}. It is a gentle visual joke, physically plausible, in the background or "
            f"midground, never the focus.")
# L12 · Matt's cameo: era clothes + teal scarf + amber notebook, a small comic beat, face partly shaded by the hat.
def matt_beat(era_outfit: str, beat: str) -> str:
    return (f"Small background cameo of MATT (from the Matt reference): {era_outfit}, teal scarf, amber notebook; {beat}. "
            f"He is small in frame, never at the centre of the action, and must not draw attention on first viewing.")


# L28 · decoupage (user review of the HCS02/HCS03 rough cuts): the same lab or valley in shot after shot, the same angle
# with only the centre moved, one image held over three ideas of narration, a happy face on a line about being sick.
# Every story keyframe names its shot like a cinematographer: size, angle, lens, the action of THIS line and the
# emotion it carries. Shots that keep a set must change size and angle (long -> medium -> close).
SHOT_SIZES = {"ELS": "extreme long shot", "LS": "long shot", "MLS": "medium long shot (knees up)",
              "MS": "medium shot (waist up)", "MCU": "medium close-up (chest up)", "CU": "close-up",
              "ECU": "extreme close-up", "OTS": "over-the-shoulder shot", "POV": "point-of-view shot",
              "INSERT": "insert shot of a detail"}


def framing(size: str, angle: str, lens: str, action: str, mood: str = "") -> str:
    """SHOT line: e.g. framing("CU", "low angle", "85 mm, shallow focus", "he lifts the beaker to his lips", "reckless")."""
    return (f"SHOT: {SHOT_SIZES[size]}, {angle}, {lens}. The image shows the action of this moment: {action}."
            f"{(' Mood and faces: ' + mood + '.') if mood else ''} Background and props support the action; the "
            f"set is seen from a new angle, not as a repeat of another shot.")


# L36 (user, HCS08 Snow, 2026-11-09): s1b, s2, s3, s4b and s8 all came back with the same street behind them. framing()
# said "a new angle" but never WHICH, and the set plate (one fixed camera view) won over the words. Every shot on a set
# that appears more than once states where the camera stands, which way it faces and exactly what fills the background,
# from the set's map (a fixed geography: where the pump, the brewery, the houses are). Draw it in the free pre-viz first.
def camera(position: str, facing: str, background: str, landmark: str = "") -> str:
    """CAMERA line: camera("on the kerb across the street", "north", "three front doors side by side, flat-on, filling the frame",
    "the pump is NOT in view")."""
    return (f"CAMERA: standing {position}, facing {facing}. BACKGROUND (exactly this, nothing else): {background}."
            f"{(' ' + landmark[0].upper() + landmark[1:] + '.') if landmark else ''} Do not reuse the reference's "
            f"camera position or composition.")


def lint_sequence(keyframes: dict[str, dict]) -> list[str]:
    """L28: consecutive story keyframes that repeat the same set at the same shot size (a repeat with the centre moved).
    L36: any two keyframes on the same set must each carry a camera() line, facing different ways or with different
    backgrounds (not only consecutive shots, and not only the size label)."""
    def key(spec):
        p = spec.get("prompt", "").lower()
        s = re.search(r"set: ([^,.]+)", p)
        z = re.search(r"shot: ([a-z -]+?)(?: \(|,)", p)
        return (s.group(1).strip() if s else None, z.group(1).strip() if z else None)

    def cam(spec):
        m = re.search(r"camera: standing (.+?), facing (.+?)\. background \(exactly this, nothing else\): (.+?)\.",
                      spec.get("prompt", "").lower())
        return (m.group(2), m.group(3)) if m else None
    names, out = list(keyframes), []
    for a, b in zip(names, names[1:]):
        (sa, za), (sb, zb) = key(keyframes[a]), key(keyframes[b])
        if sa and sa == sb and za and za == zb:
            out.append(f"L28: {a} -> {b}: same set ({sa}) and same shot size ({za}); change the size or the angle")
    story = [n for n in names if "shot:" in keyframes[n].get("prompt", "").lower()]
    for i, a in enumerate(story):
        for b in story[i + 1:]:
            sa, sb = key(keyframes[a])[0], key(keyframes[b])[0]
            if not sa or sa != sb:
                continue
            ca, cb = cam(keyframes[a]), cam(keyframes[b])
            if not ca or not cb:
                out.append(f"L36: {b if ca else a}: same set as {a if ca else b} ({sa}) without a camera() line "
                           "(position, facing, exact background)")
            elif ca == cb:
                out.append(f"L36: {b}: same set, facing and background as {a}; the two images will look the same")
    return out


# K1 · clips: one action, then stillness (Kling fills spare seconds by repeating the action).
CLIP_HOLD = "ONE single action only; once it is done, everything holds completely still until the end of the clip."


# ── layered shots: the PIECES (plan/layered-animation.md §2; user 2026-11-16) ─────────────────────────────────────────
# AI paints stills; we animate them (Stage.tsx <Actor>). A thing that moves is never painted into the plate.
# Sheets come back on a flat chroma-key green so fx_prep.sheet() cuts them cleanly (the green is unmixed from smoky,
# semi-transparent parts such as insect wings); their light and angle are the plate's, or they never sit in it.
KEY_BG = ("BACKGROUND: one flat, solid, evenly lit chroma-key green (#00B140) from edge to edge: no shadow on it, no "
          "floor line, no gradient, no texture, no vignette, nothing else on it.")


def sprite_sheet(obj: str, states: list[str], plate: str, light: str, angle: str, scale: str = "") -> str:
    """One object (an insect, a letter, a cup, a needle) in every state the shot needs, side by side.
    states: what each drawing shows, in order (["flying, wings raised", "flying, wings lowered", ...]).
    plate: the shot it goes into; light: where the light comes from there; angle: the camera's view of the object."""
    cells = " ".join(f"({i}) {s}." for i, s in enumerate(states, 1))
    return (f"SPRITE SHEET for cut-out animation: {len(states)} drawings of the SAME {obj}, in ONE row from left to "
            f"right, evenly spaced, each drawing whole and separate with wide empty space around it (nothing touches, "
            f"overlaps or leaves the picture): {cells} Every drawing is the identical design, the identical size and "
            f"scale, seen from the same angle: {angle}. LIGHT: as in the shot it will be animated into ({plate}): "
            f"{light}. {scale + ' ' if scale else ''}Ink outline, colours and brushwork of our film's painting style. "
            f"Only the {obj}: no people, no hands, no props, no ground under it. {KEY_BG} {FULL_BLEED} {NO_TEXT}")


def pose_sheet(person: str, poses: list[str], plate: str, light: str, angle: str, crop: str = "the whole figure") -> str:
    """The same character in the 2-4 poses of ONE shot (reach, flinch, look up), for pose swaps + ACT on the plate.
    crop: how much of the person the shot shows (e.g. "head and shoulders", "from the waist up")."""
    cells = " ".join(f"({i}) {s}." for i, s in enumerate(poses, 1))
    return (f"POSE SHEET for cut-out animation: the SAME person, {person}, drawn {len(poses)} times in ONE row from "
            f"left to right, each drawing separate with wide empty space around it: {cells} Each drawing shows "
            f"{crop}, the identical size, costume, face and proportions, seen from the same camera: {angle}. LIGHT: as "
            f"in the shot ({plate}): {light}. The person appears only in these {len(poses)} poses; no other people, no "
            f"furniture, no ground. Ink outline and painting style of our film. {KEY_BG} {FULL_BLEED} {NO_TEXT}")


def empty_plate(frame: str, remove: str, behind: str) -> str:
    """The approved frame without the thing that will move (the actor is animated onto it).
    frame: what reference 1 is; remove: the thing to take out; behind: what is naturally under / behind it."""
    return (f"EMPTY PLATE for cut-out animation. Reference 1 is the approved frame: {frame}. Repaint EXACTLY the same "
            f"picture: the same camera, composition, people, faces, hands, light, colours, ink lines and brush texture, "
            f"with ONE change only: {remove} is GONE. Where it was, paint what is naturally there: {behind}. Nothing "
            f"else changes and nothing is added. {FULL_BLEED} {NO_TEXT}")


# ── pre-flight lint ─────────────────────────────────────────────────────────

def lint(name: str, spec: dict) -> list[str]:
    """Return problems in one image spec (episode.json keyframes/references/thumbnails/covers entry)."""
    p = (spec.get("prompt", "") + " " + spec.get("roles", "")).lower()
    refs = spec.get("refs", [])
    issues = []
    people_free = "no people" in p or "empty location plate" in p
    # sheets (cast model sheets, layered-shot sprite / pose sheets) and empty plates of an approved frame have no story
    # framing and no set of their own
    model_sheet = any(s in p for s in ("model sheet", "sprite sheet", "pose sheet", "empty plate for cut-out"))
    hero_in_shot = any("sheet-alexis" in r or "sheet-young-family" in r for r in refs)
    if STYLE_ANCHOR in refs and (people_free or not hero_in_shot):
        issues.append("L1: the style anchor (it shows the red-tuque voyageur) on a shot without that character: "
                      "use a people-free episode plate as reference 1")
    if STYLE_ANCHOR in refs and "style reference only" not in p and "style only" not in p:
        issues.append("L2: style anchor without the 'style only, never its man' note (ANCHOR_NOTE)")
    if spec.get("aspect") == "1:1" and "border" not in p:
        issues.append("L3: square image without FULL_BLEED (the model draws a framed card)")
    if re.search(r"(plain|empty|blank)[^.]{0,40}(background|side)[^.]{0,30}(for|text)", p) and "no panel" not in p:
        issues.append("L4: 'empty background for text' without TEXT_SIDE (flat panel + seam)")
    if re.search(r"(o'clock|hands (at|pointing))", p) and "no hands" not in p:
        issues.append("L5: exact clock hands requested: draw NO_HANDS and animate them in Remotion")
    if re.search(r"porthole|opening in|wound|fistula", p) and "left" not in p:
        issues.append("L6: body opening without a side (use body_mark(..., side='LEFT'))")
    if re.search(r"\b(and|with)\b[^.]{0,60}\b(alexis|beaumont|osler)\b", p) and "cast:" not in p and not people_free:
        issues.append("L7: several characters but no CAST line (the model adds duplicates/onlookers)")
    # the kit's own "no text, letters, labels" lines are not writing-bearing props
    props_p = p.replace(NO_TEXT.lower(), "").replace("no text, labels or watermark", "").replace("no text, no labels", "")
    if re.search(r"\b(map|contract|letters?|poster|signpost|label|document|title page)\b", props_p) and "wavy ink lines" not in p \
            and "no lettering" not in p and "only legible writing" not in p:
        issues.append("L8/L15: a writing-bearing prop without WAVY_WRITING or real_writing() ('illegible' still produces lorem ipsum)")
    if spec.get("aspect", "16:9") in ("16:9", "9:16") and not people_free_plate(p) and not model_sheet and "central 70%" not in p:
        issues.append("L17: no SAFE_FRAMING (story subjects drift to the edges, where the camera can't zoom or focus on them)")
    if spec.get("aspect", "16:9") == "16:9" and "set:" not in p and not model_sheet and not re.match(r"(thumb|cover|sheet|troupe|ref|prop)", name.lower()):
        issues.append("L19: no SET line (set_block): without its place, year and look the model reuses one generic room")
    if not people_free_plate(p) and not model_sheet and not re.match(r"(thumb|cover|sheet|troupe|ref|prop|plate)", name.lower()) \
            and "shot:" not in p:
        issues.append("L28: no SHOT line (framing(): size, angle, lens, this line's action and mood)")
    # L30 (HCS04 prop-eye, 2026-11-09): a prop sheet with a ROOM plate as reference came back as the room (a log cabin)
    # with four giant foggy half-domes in it. Model sheets take a plain-paper sheet as reference, never a room plate.
    if model_sheet and any("plate-" in r for r in refs):
        issues.append("L30: a model sheet with a room plate as reference (the model paints the room): use a plain-paper "
                      "model sheet (e.g. sheet-osler) for layout + style")
    # L31 (HCS06 s3b, 2026-11-09): "a soft vignette at the edges" for a memory look came back as a painted card with a
    # white paper border. The vignette is added in the edit; the image itself stays full-bleed.
    if "vignette" in p and "no border" not in p:
        issues.append("L31: 'vignette' without FULL_BLEED (the model paints a white-bordered card); do the vignette in the edit")
    # L32 (HCS06 s6a, 2026-11-09): cast() counts its arguments, so one string "six angry townspeople" became "CAST: exactly
    # 1 person: six angry townspeople", and the crowd shot came out confused (a door standing alone among them).
    if re.search(r"cast: exactly 1 person: (two|three|four|five|six|seven|eight|nine|ten|a crowd|a group|several|about|rows of) ", p):
        issues.append("L32: a group passed to cast() as ONE person ('exactly 1 person: six ...'): write a CROWD line instead")
    # L34 (HCS08 s2/s9a, 2026-11-09): a plate given as "the painting style, palette and the pump's exact design" (no
    # "only") was copied whole: same camera, same fog, so two different story beats came back as the same picture.
    if any("plate-" in r for r in refs) and not model_sheet and "plate" in spec.get("roles", "").lower() \
            and "only" not in spec.get("roles", "").lower() and "do not copy" not in spec.get("roles", "").lower():
        issues.append("L34: plate reference without 'ONLY' / 'do NOT copy its composition' in roles (the model copies "
                      "the plate's camera and composition)")
    # L35 (HCS09 s4a, 2026-11-09): a macro insert came back as a framed picture-in-picture card with a border.
    if "insert shot" in p and "macro" in p and "no border" not in p:
        issues.append("L35: macro insert without FULL_BLEED (the model may paint it as a framed card)")
    # L37 (user, 2026-11-09: "do this for every single shot analysis from now, high restrictions on rules"): every story
    # keyframe states its camera (position, facing, exact background) with camera(), and appears on the pre-viz map.
    if "shot:" in p and "camera: standing" not in p:
        issues.append("L37: story shot without a camera() line (position, facing, exact background): every shot is "
                      "mapped, then drawn in the free pre-viz before generation")
    # L38 (user, 2026-11-14, HCS07/HCS05: "since you are using a reference image make sure duplications are not
    # happening"): a model sheet shows several views of ONE person, and a sheet holding two ages of one man can put both
    # in a shot. Every story shot that takes a sheet says each person appears once (ONE_EACH).
    if "shot:" in p and any("sheet" in r for r in refs) and "appears once" not in p:
        issues.append("L38: a character sheet as reference without ONE_EACH (the model may paint the person twice, "
                      "or copy the sheet's extra poses)")
    # L39 (same note): a set plate passed to a shot on ANOTHER set leaks its room into it (HCS08: the street everywhere).
    # Story shots that use a plate declare "set": the plate must be that set's own (ref:plate-<set>).
    plates = [r.split("plate-", 1)[1] for r in refs if r.startswith("ref:plate-")]
    if "shot:" in p and plates and (not spec.get("set") or any(pl != spec["set"] for pl in plates)):
        issues.append(f"L39: plate reference {plates} on a shot whose set is {spec.get('set')!r}: a plate is a reference "
                      "only for shots on its own set (declare \"set\"; elsewhere use the character sheets or a style-only "
                      "plate from outside this film)")
    # L40 (HCS07 s4b v1, 2026-11-14): an earlier keyframe of the SAME set as reference for a different camera came back
    # as a copy of that keyframe (same view, Matt added). kf: references copy the camera; use them only for a closer
    # shot of the same view (e.g. CU after MS), never for a reverse or another angle.
    if "shot:" in p and any(r.startswith("kf:") for r in refs) and spec.get("set") and spec.get("kf_same_view") is not True:
        issues.append("L40: an earlier keyframe as reference (it copies its camera): allowed only for a closer shot of "
                      "the same view, marked \"kf_same_view\": true; otherwise use the set plate or an outside style plate")
    # L41 (HCS07 s1a v1): "faces above the frame" came back as headless bodies inside the frame.
    if re.search(r"(faces?|heads?) (are |is )?(above|out of|outside|cropped (off|by))( the)? frame", p):
        issues.append("L41: faces/heads 'out of frame' wording: the model paints headless bodies; frame the shot so heads "
                      "are in it, or describe only hands/objects with no people")
    # L42 (HCS07 rough cut 1): a CROWD line with faces must be crowd() casting cards, or backs only.
    if "shot:" in p and "crowd:" in p and "faces are visible" not in p and "seen only from behind" not in p:
        issues.append("L42: CROWD line without casting cards: one shared description clones one face on every body; "
                      "use crowd(where, [up to 5 distinct faces]) or show the crowd only from behind")
    # L43 (layered shots, user 2026-11-16): a sprite / pose sheet must come back on the flat key colour, lit like the
    # plate it goes into; an empty plate must repaint the approved frame unchanged except for the removed thing.
    if ("sprite sheet" in p or "pose sheet" in p) and ("chroma-key green" not in p or "light:" not in p):
        issues.append("L43: sprite/pose sheet without KEY_BG and a LIGHT line matching its plate (use sprite_sheet() / "
                      "pose_sheet()): a busy or shaded background doesn't cut cleanly; a sprite lit from another side "
                      "never sits in the plate")
    if "empty plate" in p and "exactly the same picture" not in p:
        issues.append("L43: empty plate without empty_plate() (the model recomposes the frame: the actor's landing spot moves)")
    if "spectacles" in p and "amber" not in p and "no spectacles" not in p:
        issues.append("L11: spectacles that aren't Matt's (confuses the spot-the-glasses game)")
    return issues


def people_free_plate(p: str) -> bool:
    return "empty location plate" in p


def lint_all(specs: dict[str, dict], require_matt: bool = True) -> dict[str, list[str]]:
    out = {n: v for n, v in ((n, lint(n, s)) for n, s in specs.items()) if v}
    for msg in lint_sequence(specs):
        out.setdefault((msg.split()[3] if msg.startswith("L28") else msg.split()[1]).rstrip(":"), []).append(msg)
    # L29 (user, 2026-11-07): every video, Shorts included, has Matt in one of its new shots (matt_beat), besides the
    # hidden spectacles. Existing images are never regenerated just for him.
    story = [n for n, s in specs.items() if "shot:" in s.get("prompt", "").lower()]
    if require_matt and story and not any("cameo of matt" in specs[n].get("prompt", "").lower() for n in story):
        out.setdefault(story[0], []).append("L29: no Matt cameo in any shot; add matt_beat() to one shot with people in it")
    return out
