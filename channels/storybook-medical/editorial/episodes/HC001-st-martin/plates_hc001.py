"""HC001 set plates: one EMPTY location plate per recurring set that has no good plate yet (sets_hc001.py).
Every story image of that set then uses its plate as the location reference, so a scene's shots share one room and two
places never look alike (lesson L19). Writes the specs into episode.json "references" (no generation here).
Run from the repo root: python channels/storybook-medical/editorial/episodes/HC001-st-martin/plates_hc001.py [--write]

Sets that already have a fitting plate (free): MAC_STORE plate-store16 · MAC_SHORE plate-harbor · FARM plate-farm ·
STTHOMAS plate-churchyard16 · LAKE M21-lake · WASH_DEPT plate-washington. Sets with only 1–2 new shots are generated
directly from their set block, without a plate.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
sys.path.insert(0, str(HERE))
import prompt_kit as K  # noqa: E402
from sets_hc001 import SETS  # noqa: E402

P = Path("projects/hc001-window-into-his-stomach/episode.json")
STYLE_REF = "ref:plate-harbor"   # people-free, so the model takes the painting style and never copies a person (L1)
ROLES = "Reference 1 is a STYLE reference only (brushwork, palette, line): never copy its place, buildings or objects."
COMMON = ("EMPTY location plate: no people, no animals in focus. Wide 16:9 view with three clear depth layers "
          "(foreground, midground, background) and an open, uncluttered centre where actors will stand. ")

PLATES = {
    "plate-niagara": ("NIAGARA",
        "Beaumont's officer's quarters inside the old stone 'French Castle' of Fort Niagara: thick rough grey limestone walls, "
        "one deep arched window on the right with lake light, a heavy plain army-issue table with an oil lamp, a cast-iron box stove, "
        "a narrow army cot along the back wall, a shelf with a few glass vials of amber liquid and a notebook. Cool grey stone with "
        "warm lamplight pools. No log walls anywhere."),
    "plate-machosp": ("MAC_HOSP",
        "The small post hospital at Fort Mackinac: whitewashed plaster walls and ceiling, a plain iron army cot with a grey wool "
        "blanket and white linen, a small square window on the left looking out on the blue straits, a wooden washstand with a "
        "basin, folded bandages on a stool. Cool clean daylight, pale blue-white palette, simple and military. No log walls."),
    "plate-washrooms": ("WASH_ROOMS",
        "A Federal-style rented parlour in Washington: cream plaster walls with a thin striped wallpaper band, a tall sash window "
        "with plain curtains on the left, a mahogany writing desk at the centre-left with brass candlesticks, an inkwell and quill "
        "and a few folded papers (blank), two Windsor chairs, a small fireplace with a white wooden mantel. Soft autumn daylight."),
    "plate-platts": ("PLATTS",
        "Inside a white New England clapboard house in Plattsburgh, summer 1825: painted blue-grey wainscot and window frames, "
        "white plaster walls, lace curtains moving at an open window, two Windsor chairs, a small pine table, and an open front "
        "door on the right showing a bright road and green trees. Bright summer light, airy and domestic."),
    "plate-cabin": ("CABIN",
        "Exterior of a French-Canadian habitant house in Lower Canada: whitewashed squared-log walls, a steep bell-cast roof "
        "with a stone chimney, small shuttered windows, a split-rail fence and a vegetable garden, fields sloping to a wide river "
        "behind, a birchbark canoe pulled up on the bank. Late afternoon light, early autumn."),
}


def spec(name):
    sid, desc = PLATES[name]
    s = SETS[sid]
    prompt = (f"{COMMON}{K.set_block(s['name'], s['year'], s['look'])} {desc} {K.PERIOD} {K.RED_RULE} "
              "No lettering, text, signs or labels anywhere.")
    return {"aspect": "16:9", "resolution": "4K", "refs": [STYLE_REF], "roles": ROLES, "prompt": prompt}


if __name__ == "__main__":
    specs = {n: spec(n) for n in PLATES}
    issues = K.lint_all(specs)
    for n, s in specs.items():
        print(f"\n## {n}  ({PLATES[n][0]})\n{s['prompt']}")
    print("\nlint:", issues or "clean")
    if "--write" in sys.argv:
        ep = json.load(open(P, encoding="utf-8"))
        ep["references"].update(specs)
        json.dump(ep, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("written ->", P)
