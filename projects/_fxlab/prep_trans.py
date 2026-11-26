import sys
sys.path.insert(0, "channels/storybook-medical/scripts")
from trans_prep import depth_bands, luma_bands, morph, depth
from PIL import Image
import numpy as np
K = "projects/hc001-window-into-his-stomach/assets/images/keyframes/"
I = "projects/_fxlab/remotion/public/img/"
for n in ["M05", "M03", "M13", "M01", "M08"]:
    depth_bands(K + n + ".png", I + f"{n}-d", 4)
luma_bands(K + "M33.png", I + "M33-l", 6)
Image.fromarray((depth(K + "M05.png") * 255).astype(np.uint8)).save("C:/Users/Morad/AppData/Local/Temp/claude/e--Projects-OpenMontage/f41d9574-a217-4922-bafb-90264635b450/scratchpad/depth_M05.png")
# morph pairs: designed shape match (watch → porthole, both square close-ups cropped 16:9) and same place (dig → grave)
def crop169(src, out):
    im = Image.open(src).convert("RGB"); w, h = im.size; nh = round(w * 9 / 16); y = (h - nh) // 2
    im.crop((0, y, w, y + nh)).save(out, quality=93); return out
crop169(K + "I03a.png", I + "I03a-169.jpg"); crop169(K + "I19.png", I + "I19-169.jpg")
morph(I + "I03a-169.jpg", I + "I19-169.jpg", I + "morph-watch-porthole", 30)
morph(K + "M33.png", K + "M34.png", I + "morph-grave", 40)
print("ok")
