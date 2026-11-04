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


# K1 · clips: one action, then stillness (Kling fills spare seconds by repeating the action).
CLIP_HOLD = "ONE single action only; once it is done, everything holds completely still until the end of the clip."


# ── pre-flight lint ─────────────────────────────────────────────────────────

def lint(name: str, spec: dict) -> list[str]:
    """Return problems in one image spec (episode.json keyframes/references/thumbnails/covers entry)."""
    p = (spec.get("prompt", "") + " " + spec.get("roles", "")).lower()
    refs = spec.get("refs", [])
    issues = []
    people_free = "no people" in p or "empty location plate" in p
    model_sheet = "model sheet" in p  # sheets have no story framing and no set
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
    if re.search(r"\b(map|contract|letters?|poster|signpost|label|document|title page)\b", p) and "wavy ink lines" not in p \
            and "no lettering" not in p and "only legible writing" not in p:
        issues.append("L8/L15: a writing-bearing prop without WAVY_WRITING or real_writing() ('illegible' still produces lorem ipsum)")
    if spec.get("aspect", "16:9") in ("16:9", "9:16") and not people_free_plate(p) and not model_sheet and "central 70%" not in p:
        issues.append("L17: no SAFE_FRAMING (story subjects drift to the edges, where the camera can't zoom or focus on them)")
    if spec.get("aspect", "16:9") == "16:9" and "set:" not in p and not model_sheet and not re.match(r"(thumb|cover|sheet|troupe|ref|prop)", name.lower()):
        issues.append("L19: no SET line (set_block): without its place, year and look the model reuses one generic room")
    if "spectacles" in p and "amber" not in p and "no spectacles" not in p:
        issues.append("L11: spectacles that aren't Matt's (confuses the spot-the-glasses game)")
    return issues


def people_free_plate(p: str) -> bool:
    return "empty location plate" in p


def lint_all(specs: dict[str, dict]) -> dict[str, list[str]]:
    return {n: v for n, v in ((n, lint(n, s)) for n, s in specs.items()) if v}
