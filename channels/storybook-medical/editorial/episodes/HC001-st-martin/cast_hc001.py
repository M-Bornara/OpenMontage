"""HC001 cast: the age versions of the leads and the troupe of stock characters the beat sheet needs (beats_hc001.py
cast + stage_hc001.py). Existing sheets are reused: young Alexis, old Alexis, Beaumont 1822, the young family, Osler,
Matt. Writes the specs into episode.json "references" (no generation here).
Run from the repo root: python channels/storybook-medical/editorial/episodes/HC001-st-martin/cast_hc001.py [--write]

Troupe sheets show 3–4 people side by side, identified by POSITION (left to right), never by written labels (L8).
Every troupe member must look unlike the leads: no red tuques, no navy army coats, no amber spectacles (L11).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "scripts"))
import prompt_kit as K  # noqa: E402

P = Path("projects/hc001-window-into-his-stomach/episode.json")
W = "projects/window-into-the-stomach/assets/images/"
LAYOUT = W + "sheet-beaumont.png"
SHEET = ("Clean character model sheet on plain bone-white paper. Same scale in every view, full body, even soft light. "
         "No lettering, text, labels, numbers or watermark anywhere.")
VIEWS = "Front view, three-quarter view, profile view, back view, plus three head close-ups ({faces})."
TROUPE = ("Line-up model sheet: {n} DIFFERENT people standing side by side, left to right, each shown in a front view and a "
          "three-quarter view, with clear space between them. Every face, build, hairline and outfit is clearly different "
          "from the others. Nobody wears a red knitted tuque, a navy army coat or tinted spectacles.")


def lead(ref, who, faces):
    return {"aspect": "16:9", "resolution": "2K", "refs": [ref, LAYOUT],
            "roles": "Reference 1 is THIS PERSON when younger: keep the same face, bone structure, eyes and nose, and age him "
                     "exactly as described. Reference 2 shows how our model sheets are laid out (layout only, not this person).",
            "prompt": f"{SHEET} {who} {VIEWS.format(faces=faces)} {K.PERIOD}"}


def troupe(people):
    body = " ".join(f"{pos}: {p}" for pos, p in zip(["LEFT", "SECOND", "THIRD", "RIGHT"] if len(people) == 4 else ["LEFT", "CENTRE", "RIGHT"], people))
    return {"aspect": "16:9", "resolution": "2K", "refs": [LAYOUT],
            "roles": "Reference 1 shows how our model sheets are drawn (line, colour, layout only): none of these people is the man in it.",
            "prompt": f"{SHEET} {TROUPE.format(n=len(people))} {body} {K.PERIOD} {K.RED_RULE}"}


CAST = {
    "sheet-alexis-1830s": lead(W + "sheet-alexis.png",
        "ALEXIS ST. MARTIN in 1833, about 30: the same French-Canadian face as reference 1, now a married working man, a little "
        "broader and weathered, short dark stubble, dark hair a little longer; red knitted tuque, a worn brown wool waistcoat over "
        "a linen shirt, the woven arrow sash, moccasin-style boots.",
        "tired, defiant, lost"),
    "sheet-beaumont-1833": lead(W + "sheet-beaumont.png",
        "DR. WILLIAM BEAUMONT in 1833, aged 48: the same face as reference 1, heavier in the face and body, hair greying at the "
        "temples and thinning; still the dark-blue US Army surgeon's coat with brass buttons and the brass watch chain.",
        "determined, writing, annoyed"),
    "sheet-beaumont-1850s": lead(W + "sheet-beaumont.png",
        "DR. WILLIAM BEAUMONT in St. Louis around 1850, aged 65: the same face as reference 1, white-grey hair, deep lines, a "
        "civilian black frock coat, waistcoat, white high collar and black stock, the same brass watch chain.",
        "weary, hopeful, stern"),
    "troupe-mackinac-1822": troupe([
        "a young stocky voyageur with a round cheerful face, clean-shaven, a brown wool cap, faded blue shirt and a green sash.",
        "a tall lanky voyageur with a thin face and a drooping black moustache, a blue wool cap, a striped shirt.",
        "an older voyageur, about 50, grey beard, weathered, a leather cap and a buckskin jacket.",
        "a thin fur-company clerk, about 35, clean-shaven, neat brown hair, a waistcoat, sleeve garters and a long canvas apron."]),
    "troupe-scholars-clergy": troupe([
        "a fat, completely bald European professor, about 60, with grey mutton-chop whiskers, a black tailcoat straining at the buttons.",
        "a very thin, tall professor with long white hair and a clean-shaven gaunt face, a dark-green frock coat.",
        "an elderly French-Canadian parish priest in 1880, kind round face, white hair, a black cassock with a row of small buttons and a plain cross."]),
    "troupe-later-years": troupe([
        "a young US infantry private in 1833, tall and fair, clean-shaven, a light-blue fatigue jacket and a black leather cap.",
        "a stout US infantry corporal in 1833 with dark side-whiskers and a red-cheeked grin, the same light-blue jacket.",
        "Beaumont's son Israel in 1846, about 20, slim, dark hair, a brown riding coat, tall boots, holding a riding crop.",
        "a portly fur merchant, about 50, a grey top hat, a fur-collared greatcoat, a heavy gold watch chain."]),
    "troupe-1880": troupe([
        "a Quebec farmer of 1880, about 40, lean, a straw hat, rolled shirt sleeves, braces, holding a shovel.",
        "a second farmer, about 25, broad and strong, bare-headed with curly hair, a work smock, holding a shovel.",
        "Alexis's grown son in 1880, about 45, a full dark beard, a black Sunday coat, hat in his hands.",
        "Alexis's grown daughter in 1880, about 40, dark hair under a black bonnet, a dark mourning dress."]),
}

if __name__ == "__main__":
    issues = K.lint_all(CAST)
    for n, s in CAST.items():
        print(f"\n## {n}\n{s['prompt']}")
    print("\nlint:", issues or "clean")
    if "--write" in sys.argv:
        ep = json.load(open(P, encoding="utf-8"))
        ep["references"].update(CAST)
        json.dump(ep, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        print("written ->", P)
