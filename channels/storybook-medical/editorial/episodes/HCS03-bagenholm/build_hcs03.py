"""HCS03 Bågenholm: writes projects/hcs03-bagenholm/episode.json (title, narration, references, keyframes) from
storyboard-v2.md, with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS03-bagenholm/build_hcs03.py
Then:  episode.py refs hcs03-bagenholm   ->   episode.py keyframes hcs03-bagenholm
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (FULL_BLEED, NO_HANDS, NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, cast, framing, glasses_gag, lint_all,  # noqa: E402
                        set_block)

PID = "hcs03-bagenholm"
HC1 = "projects/hc001-window-into-his-stomach/assets/images/refs"

NARRATION = """[curious] Her heart stopped… Her body cooled to thirteen point seven degrees Celsius… And she lived.
Norway, 1999. Anna Bågenholm, a young doctor, was skiing… when she went head first through the ice of a frozen river.
Underneath, she found a pocket of air… and kept breathing.
Her friends held on to her skis… After about forty minutes, her heart stopped.
They cut her free after eighty minutes… No pulse… No breathing.
[whispers] Most people would call that dead.
But doctors have a saying: you're not dead… until you're warm and dead.
In Tromsø, they warmed her blood with a heart-lung machine.
That night… her heart started beating again.
[curious] Today, she works as a doctor."""

# ── people: she is a living private person, so a stand-in whose face is never shown (hood + goggles, from behind) ──
ANNA = ("THE SKIER (a young woman in a bright red ski jacket with the hood up, dark ski trousers, a red knitted hat "
        "under the hood, ski goggles; her face is NEVER visible: seen from behind, far away or hidden by hood and goggles)")
FRIEND_B = "a skier in a blue ski jacket, hood up, goggles, face turned away"
FRIEND_G = "a skier in a green ski jacket, hood up, goggles, face turned away"

# ── sets ─────────────────────────────────────────────────────────────────────────────────────────────────────
RIVER = set_block("Snowy mountains and a frozen river outside Narvik, northern Norway", "May 1999",
                  "deep blue-white snow, sharp white peaks, birch scrub, a winding frozen river with grey-blue ice, a "
                  "pale evening sky with a soft pink glow; cold and quiet")
UNDER = set_block("Under the ice of the frozen river", "1999",
                  "deep calm blue water, the white underside of the ice sheet above, soft light filtering through, "
                  "a few pebbles far below")
TROMSO = set_block("University Hospital of North Norway, Tromsø", "1999",
                   "a modern 1990s hospital: pale corridors, steel doors, warm amber ceiling lights inside, blue night "
                   "and snow outside; the only warm place in the film")

STYLE_PLATE = f"{HC1}/plate-study.png"            # HC001 people-free plate: painting style only
SHEET_LAYOUT = f"{HC1}/sheet-osler.png"           # HC001 model sheet: layout + style only

REFERENCES = {
    "sheet-skiers": dict(aspect="16:9", refs=[SHEET_LAYOUT],
        roles="Reference 1 shows our character model-sheet layout and painting style only (not these people). ",
        prompt=f"Clean character model sheet on plain bone-white paper, Norway, 1999: {ANNA}, and her two "
               f"companions: {FRIEND_B}; {FRIEND_G}. Each shown in back view, three-quarter back view and side view "
               "with hoods up and goggles on, skis on. No face is visible on anyone. Same scale in every view. No "
               "text, labels or watermark."),
    "plate-river": dict(aspect="9:16", refs=[STYLE_PLATE],
        roles="Reference 1 is a people-free plate used for STYLE only: copy its painting style, never its room. ",
        prompt=f"{RIVER} Vertical frame: the frozen river winding from the foreground into the valley, peaks "
               f"behind. EMPTY location plate: no people. Three clear depth layers. {PERIOD} {NO_TEXT}"),
    "plate-tromso": dict(aspect="9:16", refs=["ref:plate-river"],
        roles="Reference 1 is the same film (match its painting style; this place is warm amber inside). ",
        prompt=f"{TROMSO} Vertical frame of a long hospital corridor with warm amber light, steel doors at the end. "
               f"EMPTY location plate: no people. {PERIOD} {NO_TEXT}"),
}

S = "ref:sheet-skiers"
RIV = "Reference 1 is this river and these mountains (style, colours, light). "
KEYFRAMES = {
    # v2 (user review): v1 held one thermometer over three ideas. Now one image per idea: the stopped heart (a hand
    # under the ice), the 13.7 degrees (the v1 thermometer, kept), and "she lived" (warmth).
    # v3 (user review): the gloved hand under the ice meant nothing on "her heart stopped". Now the heart itself, frozen.
    "s1a": dict(aspect="9:16", refs=["ref:plate-river"],
        roles="Reference 1 is for the painting style and palette only. ",
        prompt="SET: a storybook anatomy painting, cold blue, 1999. "
               f"{framing('ECU', 'straight on', '100 mm macro', 'a human heart has stopped, frozen still inside a block of ice', 'silent, frozen, ominous but beautiful, not gory')} "
               "A softly painted anatomical human heart, muted dusty red, held motionless inside a clear block of blue "
               "ice, frost crystals growing over its surface, fine cracks in the ice, a faint cold glow. The heart is "
               "in the centre and fills the middle 60% of the frame; deep blue darkness all around. No blood, no body. "
               f"{NO_PEOPLE} {FULL_BLEED} {SAFE_FRAMING} {NO_TEXT}"),
    "s1b": dict(aspect="9:16", resolution="4K", refs=["ref:plate-river"],
        roles=RIV,
        prompt=f"{RIVER} {framing('ECU', 'top-down', '100 mm macro', 'the thermometer reads a deadly low body temperature', 'cold')} "
               "An old glass medical thermometer lying diagonally on blue-white snow, lower left to upper right; fine "
               "engraved tick marks with NO numbers; its thin red line stops very low, near the bulb. Delicate frost "
               "crystals on the snow around it. The thermometer fills the middle of the frame; the top third is soft "
               f"out-of-focus snow. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s1c": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and warm amber light). ",
        prompt=f"{TROMSO} {framing('CU', 'eye level', '85 mm, shallow focus', 'warmth and life: two hands hold a steaming mug of tea by a window', 'quiet relief, warm and safe')} "
               f"{cast('one person, seen only as two hands with a red knitted scarf end hanging beside them, holding a steaming white mug in the centre of the frame; no face')} "
               "Behind, out of focus, a hospital window with blue snow outside and amber lamplight inside. "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles=RIV + "Reference 2 shows the three skiers (same jackets). ",
        prompt=f"{RIVER} {framing('ELS', 'eye level', '24 mm', 'three skiers cross the mountains, the red jacket leading')} "
               f"{cast(ANNA + ', first in line', FRIEND_B, FRIEND_G, extra='The three skiers are tiny, in a line crossing a snowy slope in the middle of the frame, the red jacket leading.')} "
               f"A near snow ridge in the foreground, peaks behind. The top 25% is pale sky. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user review): v1/v2 repeated the s2a valley from the same angle with a hole that had no scale. Now at ice level,
    # close: the hole only a little wider than a person's shoulders, nothing of the valley.
    "s2b": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles="Reference 1 is for the painting style and palette only. Reference 2 shows the skier's skis and boots. ",
        prompt="SET: the surface of a frozen river at dusk, northern Norway, May 1999, grey-blue ice, snow crust, cold "
               f"pink light. {framing('CU', 'camera lying on the ice, ground level', '35 mm, shallow focus', 'she has just gone head first through the ice: only her boots and skis stick up out of a small broken hole', 'shock, sudden danger')} "
               f"{cast(ANNA + ': ONLY her two ski boots, still clipped into her two skis, sticking straight up out of the hole; nothing else of her visible')} "
               "The hole is small and jagged, only a little wider than a person's shoulders, black water inside; "
               "broken ice shards and snow in the foreground; the far riverbank is a soft blur. NO red, NO jacket, NO "
               f"blood. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v3 (user review): v2's legs folded outward. Now head and shoulders only, in the air gap under the ice.
    "s3": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles="Reference 1 is for the painting style and palette only. Reference 2 shows the skier's red hood and hat. ",
        prompt=f"{UNDER} {framing('MCU', 'underwater, from slightly below and behind her head', '35 mm', 'her head is in a thin pocket of air trapped under the ice, and she is breathing', 'calm, fragile hope')} "
               f"{cast(ANNA + ': ONLY the back of her head in the red knitted hat and red hood, and her shoulders; the rest of her body is out of frame below. Her head is tipped back so the hat touches the ice above')} "
               "The underside of the ice is a flat white ceiling across the top third of the frame; between the ice "
               "and the water a thin flat layer of silvery air, and her head is in that layer. Small bubbles. NO face, "
               f"NO legs, NO full body. Open river water to every edge: NO glass walls, NO tank, NO aquarium, "
               f"NO cutaway section lines. {FULL_BLEED} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4a": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles=RIV + "Reference 2 shows the blue-jacket and green-jacket companions. ",
        prompt=f"{RIVER} {framing('MS', 'low side angle on the ice', '35 mm', 'her two friends hold on to her skis with all their strength', 'desperate effort')} "
               f"{cast(FRIEND_B + ', kneeling on the ice', FRIEND_G + ', kneeling beside him', extra='Both grip a pair of skis that stick up out of a hole in the ice, with both gloved hands, leaning back, straining; faces turned away from the viewer.')} "
               f"The gloves and skis are in the centre of the frame. The top 20% is pale sky. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2 (user review): v1's watch screen was blank. Now it reads 40:00, on the wrist of a hand gripping a ski.
    "s4b": dict(aspect="9:16", refs=["ref:plate-river"],
        roles="Reference 1 is for the painting style and palette only. ",
        prompt="SET: the frozen river at dusk, northern Norway, May 1999, blue light. "
               f"{framing('INSERT', 'close and level with the wrist', '100 mm macro', 'time running out: the watch shows forty minutes', 'tense')} "
               "A chunky black 1990s digital sports watch on a blue-gloved wrist; the gloved hand grips a ski at the "
               "edge of the frame (only the wrist, glove and ski of one person, nobody else). The grey LCD screen "
               'shows exactly "40:00" in large black segment digits, spelled exactly like that; no other text, '
               f"numbers or logos anywhere. Snow blur behind. {SAFE_FRAMING} {PERIOD}"),
    # v2 (user review): v1's s5 and s6 were the same valley twice with the centre moved. s5 becomes two close shots.
    "s5a": dict(aspect="9:16", refs=["ref:plate-river"],
        roles="Reference 1 is for the painting style and palette only. ",
        prompt="SET: the surface of a frozen river at dusk, northern Norway, May 1999, grey-blue ice, cold pink light. "
               f"{framing('CU', 'low angle at ice level', '35 mm', 'a rescuer hacks the ice open with an ice axe', 'urgent, violent effort')} "
               f"{cast('one rescuer in an orange suit and helmet, seen from the chest down, swinging an ice axe down into the ice')} "
               f"Ice chips fly toward the camera. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5b": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles="Reference 1 is for the painting style and palette only. Reference 2 shows the red jacket. ",
        prompt="SET: snow beside the frozen river at dusk, northern Norway, May 1999, blue light. "
               f"{framing('ECU', 'top-down', '85 mm', 'a rescuer checks for a pulse and finds none', 'stillness, dread')} "
               f"{cast('a rescuer, seen only as one bare hand coming from an orange sleeve', 'the skier, seen only as a still pale wrist in a red jacket cuff lying on the snow')} "
               "Two of the rescuer's fingers rest on the inside of the pale wrist. Frost on the red cuff. Snow fills "
               f"the whole background: NO inset picture, NO box, NO second image inside the frame. {FULL_BLEED} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6": dict(aspect="9:16", refs=["ref:plate-river", "kit:glasses-sheet.jpg"],
        roles=RIV + "Reference 2 shows Matt's amber spectacles. ",
        prompt=f"{RIVER} {framing('ELS', 'eye level', '24 mm', 'a rescue helicopter lands beside a tiny group on the endless snow', 'lonely, vast')} "
               "An endless white plain at dusk; in the middle distance a red and white rescue helicopter landing, "
               "blowing snow, beside a tiny group of figures (no faces). A snowy rock in the lower foreground. "
               f"{glasses_gag('resting on top of the snowy rock in the foreground, half dusted with snow')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and amber light). ",
        prompt=f"{TROMSO} {framing('LS', 'from outside in the snow', '28 mm', 'the stretcher is rushed into the warm hospital', 'hope')} "
               "Night: wide hospital double doors swinging open, warm amber light pouring out across the snow; a "
               "stretcher being wheeled in by three medical staff seen only as dark silhouettes from behind. The doors "
               f"are in the centre. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and amber light). ",
        prompt=f"{TROMSO} {framing('MS', 'eye level', '35 mm', 'the heart-lung machine warms her blood', 'focused, clinical')} "
               "An operating room: a 1990s heart-lung machine on a trolley, steel roller pumps, round gauges, long "
               "loops of CLEAR EMPTY tubing curving across the frame toward a bed at the edge (only the white sheet "
               "visible). Behind, a team in green gowns and caps as soft silhouettes, faces turned away. NO blood, NO "
               f"body. The machine and tubing fill the centre. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and amber light). ",
        prompt=f"{TROMSO} {framing('CU', 'eye level', '50 mm', 'the heart monitor about to show a heartbeat again', 'held breath')} "
               "A 1990s heart monitor on a bracket, its dark green screen completely EMPTY (the line is added later); "
               f"behind it on the wall a round clock ({NO_HANDS}). Warm amber light. The screen fills the middle of the "
               f"frame. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s10": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style; now in bright daylight). ",
        prompt=f"{TROMSO} {framing('LS', 'eye level, down the corridor', '35 mm', 'she walks to work as a doctor today', 'warm, quietly triumphant')} "
               "Daytime, bright: sunlight through tall windows along the corridor. "
               f"{cast('a woman doctor in a white coat with a red knitted scarf, seen only from behind, walking away from the viewer down the middle of the corridor')} "
               f"She is in the middle distance at the centre. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
}

# The FX layers need: s1 thermometer mask (frost), s4a gloves (pull), s4b LCD rect (digits), s8 tubing (glow),
# s9 screen rect (heartbeat line) and the clock face (hands at 10:15) — masks.py after generation.


def main():
    p = REPO / "projects" / PID / "episode.json"
    ep = json.load(open(p, encoding="utf-8"))
    ep.update(title="She Was Trapped Under Ice for 80 Minutes", format="short", dual_format=False, image_resolution="2K",
              references=REFERENCES, keyframes=KEYFRAMES)
    ep["narration"]["v3_text"] = NARRATION
    json.dump(ep, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    issues = lint_all({**REFERENCES, **KEYFRAMES})
    for n, v in issues.items():
        print(n, *v, sep="\n  ")
    print(f"{len(REFERENCES)} references, {len(KEYFRAMES)} keyframes -> {p}  ({len(issues)} with lint findings)")


if __name__ == "__main__":
    main()
