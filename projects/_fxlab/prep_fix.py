import sys
sys.path.insert(0, "channels/storybook-medical/scripts")
from life_prep import region
K = "projects/hc001-window-into-his-stomach/assets/images/keyframes/"
I = "projects/_fxlab/remotion/public/img/"
region(K+"M03.png", I+"M03-water.png", [(55,47),(100,47),(100,92),(76,92),(66,80),(55,62)], brighter_than=55)
region(K+"M13.png", I+"M13-fire.png", [(70,50),(78,50),(78,63),(70,63)], feather=1.0)
region(K+"M30.png", I+"M30-sky.png", [(0,0),(100,0),(100,27),(0,27)], brighter_than=120, feather=3)
region(K+"M21.png", I+"M21-sky.png", [(0,0),(100,0),(100,46),(0,46)], brighter_than=150, feather=3)
