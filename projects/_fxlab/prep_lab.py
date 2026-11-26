import sys
sys.path.insert(0, "channels/storybook-medical/scripts")
from life_prep import plate, region, subject, clean_plate
K = "projects/hc001-window-into-his-stomach/assets/images/keyframes/"
I = "projects/_fxlab/remotion/public/img/"
for n in ["M01","M03","M05","M08","M13","M15","M17","M20","M21","M22","M29","M30","M31","M33","M34","I10","I19"]:
    plate(K + n + ".png", I + n + ".jpg")
# M21: canoe bobs on shimmering water under drifting clouds
subject(K+"M21.png", I+"M21-canoe.png", (52, 52, 88, 84))
region(K+"M21.png", I+"M21-water.png", [(0,47),(100,47),(100,100),(0,100)], minus=[I+"M21-canoe.png"])
region(K+"M21.png", I+"M21-sky.png", [(0,0),(100,0),(100,44),(0,44)], brighter_than=150)
clean_plate(K+"M21.png", [I+"M21-canoe.png"], I+"M21-bg.jpg")
# M03: water shimmer (not the dock posts)
region(K+"M03.png", I+"M03-water.png", [(56,48),(100,48),(100,90),(78,90),(70,80),(56,62)], darker_than=None, brighter_than=105)
# M13: the fire
region(K+"M13.png", I+"M13-fire.png", [(70,50),(81,50),(81,68),(70,68)], feather=1.5)
# M22: the lantern swings on its bracket
subject(K+"M22.png", I+"M22-lantern.png", (37, 8, 48, 27))
clean_plate(K+"M22.png", [I+"M22-lantern.png"], I+"M22-bg.jpg", grow=10)
# M20: parallax, the family in front of the cabin and river
subject(K+"M20.png", I+"M20-wife.png", (35, 28, 59, 100))
subject(K+"M20.png", I+"M20-alexis.png", (69, 21, 94, 100))
subject(K+"M20.png", I+"M20-child.png", (62, 76, 77, 100))
clean_plate(K+"M20.png", [I+"M20-wife.png", I+"M20-alexis.png", I+"M20-child.png"], I+"M20-bg.jpg")
# M30: old Alexis breathes; sunset sky drifts
subject(K+"M30.png", I+"M30-alexis.png", (66, 24, 89, 97))
region(K+"M30.png", I+"M30-sky.png", [(0,0),(62,0),(62,26),(0,26)], brighter_than=120)
print("prep done")
