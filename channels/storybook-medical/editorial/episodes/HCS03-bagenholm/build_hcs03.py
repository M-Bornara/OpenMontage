"""HCS03 Bågenholm: writes projects/hcs03-bagenholm/episode.json (title, narration, references, keyframes) from
storyboard-v1.md, with the prompt_kit blocks, then lints every image prompt. Run from the repo root:
    python channels/storybook-medical/editorial/episodes/HCS03-bagenholm/build_hcs03.py
Then:  episode.py refs hcs03-bagenholm   ->   episode.py keyframes hcs03-bagenholm
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
from prompt_kit import (NO_HANDS, NO_PEOPLE, NO_TEXT, PERIOD, SAFE_FRAMING, cast, glasses_gag, lint_all,  # noqa: E402
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
    "s1": dict(aspect="9:16", resolution="4K", refs=["ref:plate-river"],
        roles=RIV,
        prompt=f"{RIVER} Extreme close-up: an old glass medical thermometer lying diagonally on blue-white snow, "
               "lower left to upper right; fine engraved tick marks with NO numbers; its thin red line stops very low, "
               "near the bulb. Delicate frost crystals on the snow around it. The thermometer fills the middle of the "
               f"frame; the top third is soft out-of-focus snow. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s2a": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles=RIV + "Reference 2 shows the three skiers (same jackets). ",
        prompt=f"{RIVER} Extreme wide vertical frame. {cast(ANNA + ', first in line', FRIEND_B, FRIEND_G, extra='The three skiers are tiny, in a line crossing a snowy slope in the middle of the frame, the red jacket leading.')} "
               f"A near snow ridge in the foreground, peaks behind. The top 25% is pale sky. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    # v2: v1's red sleeve under the ice read as blood, and s3 v1 stood her upright on the riverbed (user review)
    "s2b": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles=RIV + "Reference 2 shows the skier's skis and boots. ",
        prompt=f"{RIVER} High angle, looking down on the frozen river: a dark jagged hole in the grey-blue ice in the "
               "centre; two skis and two dark ski boots stick up out of the hole at an angle, crossed slightly. "
               "Nothing else of the person is visible: no jacket, no body, no face. NO red anywhere near the hole: the "
               "water in the hole is dark blue-black and the ice around it is clean white and grey. "
               f"{cast(ANNA + ' (only her boots and skis visible above the ice)')} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s3": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles="Reference 1 is for the painting style and palette only. Reference 2 shows the skier's red jacket. ",
        prompt=f"{UNDER} Calm and quiet, not frightening. The underside of the ice sheet runs across the TOP third of "
               "the frame. Just under it, a small flat silvery pocket of trapped air. "
               f"{cast(ANNA + ', UPSIDE DOWN (she went in head first): her body hangs down into the blue water below the ice, her legs going UP toward the hole in the ice at the top right, her head at the top in the air pocket; we see her from behind, only the back of her red hood inside the silvery air pocket, NO face visible at all')} "
               f"A few small separate bubbles. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4a": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles=RIV + "Reference 2 shows the blue-jacket and green-jacket companions. ",
        prompt=f"{RIVER} Medium shot from the side, low on the ice. {cast(FRIEND_B + ', kneeling on the ice', FRIEND_G + ', kneeling beside him', extra='Both grip a pair of skis that stick up out of a hole in the ice, with both gloved hands, leaning back, straining; faces turned away from the viewer.')} "
               f"The gloves and skis are in the centre of the frame. The top 20% is pale sky. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s4b": dict(aspect="9:16", refs=["ref:plate-river"],
        roles=RIV,
        prompt=f"{RIVER} Extreme close-up: a chunky black 1990s digital sports watch on a blue gloved wrist (only "
               "the wrist and glove of one person, nobody else), the watch face turned to the viewer, its grey LCD "
               "display completely BLANK (the digits are added later). Snow and the river out of focus behind. The "
               f"watch is centred. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s5": dict(aspect="9:16", refs=["ref:plate-river", S],
        roles=RIV + "Reference 2 shows the red jacket. ",
        prompt=f"{RIVER} Wide vertical frame at dusk. {cast('two rescuers in orange suits and helmets, one holding an ice axe, by the hole in the ice', 'a still person wrapped in a red jacket and a grey blanket, lying on an orange stretcher on the snow, seen from the feet end, far away, no face visible')} "
               f"The group is small in the middle of the frame; the white plain stretches around them. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s6": dict(aspect="9:16", refs=["ref:plate-river", "kit:glasses-sheet.jpg"],
        roles=RIV + "Reference 2 shows Matt's amber spectacles. ",
        prompt=f"{RIVER} Extreme wide vertical frame: an endless white plain at dusk; in the middle distance a red "
               "and white rescue helicopter landing, blowing snow, beside a tiny group of figures (no faces). A snowy "
               f"rock in the lower foreground. {glasses_gag('resting on top of the snowy rock in the foreground, half dusted with snow')} "
               f"{SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s7": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and amber light). ",
        prompt=f"{TROMSO} Night, from outside in the blue snow: wide hospital double doors swinging open, warm amber "
               "light pouring out across the snow; a stretcher being wheeled in by three medical staff seen only as "
               f"dark silhouettes from behind. The doors are in the centre. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s8": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and amber light). ",
        prompt=f"{TROMSO} Medium shot in an operating room: a 1990s heart-lung machine on a trolley, steel roller "
               "pumps, round gauges, long loops of CLEAR EMPTY tubing curving across the frame toward a bed at the "
               "edge (only the white sheet visible). Behind, a team in green gowns and caps as soft silhouettes, faces "
               f"turned away. NO blood, NO body. The machine and tubing fill the centre. {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s9": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style and amber light). ",
        prompt=f"{TROMSO} Close-up: a 1990s heart monitor on a bracket, its dark green screen completely EMPTY (the "
               f"line is added later); behind it on the wall a round clock ({NO_HANDS}). Warm amber light. The screen "
               f"fills the middle of the frame. {NO_PEOPLE} {SAFE_FRAMING} {PERIOD} {NO_TEXT}"),
    "s10": dict(aspect="9:16", refs=["ref:plate-tromso"],
        roles="Reference 1 is this hospital (style; now in bright daylight). ",
        prompt=f"{TROMSO} Daytime, bright: sunlight through tall windows along the corridor. {cast('a woman doctor in a white coat with a red knitted scarf, seen only from behind, walking away from the viewer down the middle of the corridor')} "
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
