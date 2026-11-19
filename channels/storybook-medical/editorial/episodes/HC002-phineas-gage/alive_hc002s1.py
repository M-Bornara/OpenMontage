"""HC002-S1 ALIVE pieces (FREE, rough cut 1, 2026-11-18): masks + clean plates cut from the approved stills themselves, for
the small storyboard moves (layered-animation.md §6: a cut-out on a hinge, a nudge). Nothing is generated.

    python channels/storybook-medical/editorial/episodes/HC002-phineas-gage/alive_hc002s1.py
Writes assets/images/keyframes/fx/<still>-<name>.mask.png / .clean.png / .check.png (look at every check).
Boxes and outlines are 9:16 frame fractions measured on the stills (grids in the session scratchpad).
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "channels/storybook-medical/scripts"))
import fx_prep  # noqa: E402

KF = REPO / "projects/hc002-s1/assets/images/keyframes"

CUTS = [
    # shot 2a: Gage's raised forearm + hand (the signal to the crew), hinge at the rolled cuff (0.545, 0.39)
    ("s2a", "arm", (0.50, 0.28, 0.63, 0.405),
     [(0.525, 0.398), (0.567, 0.398), (0.577, 0.35), (0.612, 0.31), (0.607, 0.284), (0.568, 0.29), (0.552, 0.33),
      (0.523, 0.375)]),
    # shot 2b: the old driller's raised hammer (rotates about his grip, 0.31, 0.678): traced tight along head + handle +
    # hands (how="poly"; rembg took the rock between the handle and his hat)
    ("s2b", "hammer1", (0.18, 0.60, 0.34, 0.70),
     [(0.183, 0.618), (0.204, 0.607), (0.216, 0.621), (0.312, 0.664), (0.330, 0.670), (0.333, 0.690), (0.300, 0.692),
      (0.290, 0.676), (0.218, 0.637), (0.200, 0.641)], "poly"),
    # shot 2b: the moustached man's low hammer (rotates about his right hand, 0.728, 0.757), traced tight
    ("s2b", "hammer2", (0.54, 0.69, 0.76, 0.775),
     [(0.546, 0.720), (0.569, 0.700), (0.596, 0.715), (0.620, 0.720), (0.710, 0.744), (0.748, 0.746), (0.752, 0.768),
      (0.712, 0.770), (0.620, 0.740), (0.592, 0.739), (0.572, 0.741)], "poly"),
    # shot 9: the oxen heads (a slow bob about the yoke)
    ("s9", "ox1", (0.25, 0.495, 0.47, 0.65),
     [(0.25, 0.50), (0.45, 0.50), (0.465, 0.56), (0.40, 0.648), (0.31, 0.648), (0.268, 0.57)]),
    ("s9", "ox2", (0.0, 0.49, 0.2, 0.63),
     [(0.0, 0.50), (0.18, 0.493), (0.195, 0.56), (0.12, 0.628), (0.04, 0.628), (0.0, 0.585)]),
    # shot 10: Gage's raised hand (the greeting), hinge at the elbow (0.47, 0.49)
    ("s10", "hand", (0.43, 0.405, 0.495, 0.5),
     [(0.437, 0.413), (0.472, 0.408), (0.482, 0.45), (0.488, 0.492), (0.463, 0.497), (0.449, 0.46), (0.436, 0.445)]),
    # shot 12: the whispering friend's head + cupped hand (he leans in on "said")
    ("s12", "lean", (0.47, 0.20, 0.69, 0.49),
     [(0.48, 0.25), (0.52, 0.205), (0.62, 0.205), (0.665, 0.25), (0.66, 0.36), (0.685, 0.39), (0.685, 0.47), (0.64, 0.48),
      (0.60, 0.42), (0.55, 0.42), (0.50, 0.38), (0.48, 0.33)]),
]


def main():
    only = set(sys.argv[1:])
    for still, name, box, poly, *how in CUTS:
        if only and f"{still}-{name}" not in only:
            continue
        fx_prep.cut(str(KF / f"{still}.png"), name, box, how=(how or ["rembg"])[0], grow=2, check=True, poly=poly)


if __name__ == "__main__":
    main()
