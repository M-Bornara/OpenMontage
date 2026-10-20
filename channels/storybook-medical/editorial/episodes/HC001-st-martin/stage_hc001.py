"""HC001 previz staging: what each beat's cut-out 2D animation shows (painted plate + puppets + props).
Merged into artifacts/beats.json by scripts/beats.py; drawn by remotion/Stage.tsx. Positions in % of the frame:
x = centre, y = ground line (feet), h = standing height. Close-ups put the ground below the frame and make h large.
Acts and props: see remotion/Puppet.tsx (ACTS, Hold) and Stage.tsx (PropArt)."""

STAGE = {}


def A(who, act, x, y, h, face="r", **kw):
    return dict(who=who, act=act, x=x, y=y, h=h, face=face, **kw)


def P(p, x, y, h, **kw):
    return dict(p=p, x=x, y=y, h=h, **kw)


def st(id, bg, *items, **kw):
    STAGE[id] = dict(bg=bg, actors=[i for i in items if "who" in i], props=[i for i in items if "p" in i], **kw)


HARBOR, STORE, SICK, STUDY, VIALS = "plate-harbor", "plate-store16", "plate-sickroom16", "plate-study", "M17"
FARM, DUSK, CHURCH, WASH, LAKE, STREET, DOCK = "plate-farm", "M31", "plate-churchyard16", "plate-washington", "M21-lake", "M29", "M03"

# 0 · hook
st("0.01", STUDY, P("handsTie", 50, 118, 120), blur=6, dark=0.15)
st("0.02", STUDY, P("porthole", 50, 112, 180), P("beefString", 50, 30, 60), blur=4)
st("0.05", SICK, A("beaumont", "stand", 78, 175, 190, "l", exp="shock"), P("stringHalf", 42, 75, 70), blur=5)
st("0.06", STUDY, A("beaumont", "sitWrite", 26, 96, 52, "r", hold="pen"), A("alexis", "getUpWalk", 55, 96, 54, "r", hold="none", move=[50, 92]),
   P("firewood", 70, 96, 18, move=[66, 108]))
st("0.07", STUDY, A("beaumont", "turnHead", 36, 150, 140, "r", hold="notebook"), dark=0.05)
st("0.10", LAKE, P("canoe", 62, 70, 12, move=[66, 58]), A("alexis", "paddle", 61, 67, 8, "r", hold="paddle", move=[65, 57]), dark=0.5)
# 1 · the case
st("1.01", HARBOR, P("gulls", 70, 40, 30))
st("1.03", HARBOR, P("canoe", 50, 98, 40, move=[105, 55]), A("voyageur", "paddle", 44, 88, 28, "l", hold="paddle", move=[99, 49]),
   A("friend2", "paddle", 56, 88, 28, "l", hold="paddle", move=[111, 61]), A("matt", "sitWrite", 66, 89, 26, "l", hold="notebook", move=[121, 71]))
st("1.04", LAKE, P("canoe", 50, 104, 75), A("voyageur", "paddle", 32, 86, 50, "r", hold="paddle"), A("friend1", "paddle", 52, 86, 50, "r", hold="paddle"),
   A("friend2", "paddle", 70, 86, 50, "r", hold="paddle"))
st("1.05", DOCK, A("friend1", "laugh", 24, 128, 105, "r"), A("friend2", "laugh", 46, 130, 100, "r", hold="bread"), A("alexis", "laugh", 72, 126, 110, "l", hold="bread"))
st("1.05b", DOCK, A("alexis", "carry", 40, 95, 55, "r", hold="sack", hold2="sack", move=[30, 60]), P("furBale", 75, 95, 22))
st("1.06", STORE, A("clerk", "hold", 64, 80, 44, "l", hold="musket"), A("voyageur", "stand", 46, 80, 42, "r"), A("friend1", "armsFold", 82, 82, 44, "l"),
   A("alexis", "stand", 22, 112, 88, "r"))
st("1.08", STORE, P("pellets", 50, 108, 110), blur=5)
st("1.10", HARBOR, A("beaumont", "run", 30, 92, 34, "r", hold="none", move=[20, 60]))
st("1.11", STORE, A("beaumont", "run", 70, 100, 70, "l", move=[78, 58]), A("friend2", "turnHead", 30, 100, 62, "r"))
st("1.12", STORE, A("alexis", "lie", 56, 98, 60, "r", exp="pain"), A("beaumont", "kneel", 30, 100, 64, "r", exp="shock"),
   A("matt", "kneelLantern", 80, 100, 66, "l", hold="lantern", exp="worried"))
st("1.13", STORE, P("wound", 50, 104, 120), blur=6, dark=0.15)
st("1.14", STORE, A("friend1", "hatInHands", 30, 78, 40, "r"), A("clerk", "hatInHands", 50, 78, 40, "r"), A("voyageur", "hatInHands", 68, 78, 40, "l"),
   A("alexis", "lie", 52, 100, 50, "r", exp="pain"), dark=0.1)
st("1.15", STORE, A("alexis", "faceWake", 50, 317, 300, "r"), dark=0.2, blur=4)
st("1.16", STORE, A("beaumont", "turnHead", 50, 160, 150, "r"))
# 2 · what happened next
st("2.01", SICK, A("alexis", "lie", 80, 66, 42, "r", exp="pain"))
st("2.02", SICK, A("alexis", "cough", 80, 66, 46, "l", hold="spoon"), A("beaumont", "hold", 56, 96, 60, "r", hold="basin", exp="worried"))
st("2.03", SICK, A("beaumont", "hold", 46, 160, 150, "r", exp="worried"))
st("2.04", SICK, A("alexis", "spoon", 80, 66, 46, "l", hold="spoon", exp="smile"))
st("2.05", SICK, A("beaumont", "hold", 58, 96, 60, "r", exp="determined"), A("alexis", "sitUpBed", 80, 66, 46, "l", exp="sad"))
st("2.07", SICK, P("needleHand", 50, 118, 120), blur=5)
st("2.08", SICK, A("alexis", "pushAway", 50, 150, 140, "r"))
st("2.09", SICK, A("alexis", "sitUpBed", 60, 135, 110, "l", exp="sad"))
st("2.10", SICK, P("tools", 50, 110, 120), blur=5, dark=0.2)
st("2.13", STUDY, A("beaumont", "lookUp", 40, 130, 115, "r", hold="pen"))
# 3 · the science
st("3.02", STUDY, A("prof1", "armsFold", 30, 100, 70, "r", exp="angry"), A("prof2", "point", 70, 100, 72, "l", exp="angry"))
st("3.05", STUDY, dark=0.25)
st("3.06", HARBOR)
# 4 · the experiments
st("4.03", STUDY, P("foods", 50, 100, 150), blur=6)
st("4.05", STUDY, P("foodsGone", 50, 100, 150), A("beaumont", "pull", 80, 170, 180, "l", exp="curious"), blur=6)
st("4.06", SICK, A("alexis", "sitUpBed", 62, 135, 110, "l", exp="pain"))
st("4.07", STUDY, P("porthole", 50, 112, 180), P("pill", 50, 40, 40), blur=4)
st("4.08", STUDY, A("beaumont", "sitWrite", 42, 100, 74, "r", hold="pen", exp="smile"))
st("4.10", VIALS, A("beaumont", "hold", 48, 96, 66, "r", exp="curious"))
st("4.11", VIALS)
st("4.12", VIALS, P("vial", 50, 100, 120), blur=6)
st("4.15", STUDY, A("alexis", "sit", 66, 145, 130, "l", exp="mortified"), A("beaumont", "hold", 8, 150, 150, "r", exp="curious"))
st("4.17", STUDY, A("beaumont", "stand", 50, 165, 160, "r", exp="sour"))
st("4.19", STUDY, A("alexis", "armsFold", 32, 98, 62, "r", exp="determined"))
st("4.21", STUDY, A("beaumont", "lookUp", 45, 130, 115, "r"))
st("4.22", STUDY, dark=0.1)
# 5 · the human experiment
st("5.02", STUDY, A("beaumont", "sitWrite", 42, 125, 110, "r", hold="pen", exp="angry"))
st("5.03", CHURCH, A("alexis", "stand", 36, 82, 30, "r", exp="smile"), A("wife", "stand", 42, 82, 28, "l", exp="smile"))
st("5.05", LAKE, P("canoe", 50, 96, 60, move=[25, 70]), A("alexis", "paddle", 40, 84, 40, "r", hold="paddle", move=[15, 60]),
   A("voyageur", "paddle", 60, 84, 40, "r", hold="paddle", move=[35, 80]))
st("5.08", FARM, A("alexis", "chop", 45, 96, 60, "r", hold="axe"), P("firewood", 62, 96, 16))
st("5.09", FARM, A("alexis", "carry", 50, 96, 56, "r", hold="sack", hold2="sack", move=[30, 62]), A("beaumont", "hold", 82, 96, 58, "l", hold="notebook"))
st("5.11", LAKE, P("canoe", 50, 74, 16, move=[30, 60]), A("alexis", "paddle", 47, 70, 11, "r", hold="paddle", move=[27, 57]),
   A("wife", "sit", 50.5, 70.5, 9, "r", move=[30.5, 60.5]), A("child1", "sit", 52.5, 71, 7, "r", move=[32.5, 62.5]), A("child2", "sit", 54, 71, 6, "r", move=[34, 64]))
st("5.11b", LAKE, P("canoe", 50, 120, 120), A("alexis", "paddle", 50, 150, 150, "r", hold="paddle", exp="determined"))
st("5.13", FARM, A("alexis", "stand", 70, 100, 70, "l", exp="smile"))
st("5.14", WASH, A("merchant", "walk", 40, 90, 46, "r", move=[30, 60]), A("osler", "walk", 70, 90, 44, "l", move=[80, 55]))
st("5.15", WASH, A("soldier", "stand", 50, 112, 92, "r", exp="sad"))
st("5.16", STUDY, P("contract", 50, 105, 160, text="covenant servant"), blur=6)
st("5.19", STUDY, P("pen", 50, 110, 120), blur=6)
st("5.21", WASH, A("soldier", "laugh", 60, 96, 60, "l"), A("soldier2", "laugh", 80, 96, 64, "l"), A("alexis", "armsFold", 28, 96, 58, "r", exp="sad"))
st("5.21b", WASH, A("alexis", "armsFold", 50, 160, 150, "r", exp="sad"))
st("5.22", STUDY, P("letter", 50, 105, 150, text="1834"), blur=6)
st("5.23", FARM, A("wife", "armsFold", 60, 150, 140, "l", exp="determined"))
st("5.24", FARM, A("alexis", "walk", 40, 88, 26, "r", move=[30, 75]))
# 6 · what they learned
st("6.03", WASH, A("merchant", "point", 32, 100, 66, "r"), A("prof1", "armsFold", 72, 100, 66, "l"), P("purse", 52, 96, 30))
st("6.05", FARM, A("son", "walk", 60, 88, 30, "l", move=[80, 45]))
st("6.06", FARM, A("alexisOld", "shakeHead", 50, 120, 100, "l"))
# 7 · case file photos
st("7.03", STORE, A("merchant", "hold", 50, 100, 70, "r", hold="hat"), P("furBale", 75, 98, 26))
st("7.05", STUDY, A("beaumont", "stand", 50, 150, 140, "r", exp="neutral"), dark=0.35)
# 8 · the last word
st("8.02", STUDY, A("osler", "sitWrite", 42, 110, 85, "r", hold="pen"))
st("8.03", STUDY, P("jar", 50, 96, 60), dark=0.15)
st("8.04", FARM, P("letter", 50, 105, 140, text="W. Osler"), blur=6)
st("8.05", CHURCH, A("priest", "stand", 32, 70, 34, "r"))
st("8.06", SICK, P("coffin", 60, 96, 60), dark=0.35)
st("8.09", CHURCH, P("grave", 50, 104, 80), P("tuquePost", 78, 104, 90))
st("8.10", CHURCH, A("digger2", "hatInHands", 40, 90, 40, "r", exp="sad"), A("friend1", "hatInHands", 54, 90, 40, "r"), A("friend2", "hatInHands", 64, 90, 42, "r"),
   P("grave", 50, 96, 30), dark=0.1)
# 9 · why it matters
st("9.02", LAKE, P("canoe", 50, 96, 50, move=[20, 70]), A("alexis", "paddle", 48, 84, 34, "r", hold="paddle", move=[18, 68]))
st("9.03", FARM, P("tuqueNail", 50, 92, 75), blur=4)
st("9.04", DUSK, A("osler", "hold", 50, 100, 80, "r", hold="musket"), dark=0.5, silhouette=True)
