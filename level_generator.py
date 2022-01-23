import os
from PIL import Image

path = os.path.abspath(os.getcwd())

img = Image.open(path + "/levels/test_level.png", "r")
rgb_img = img.convert("RGB")
pixels = list(img.getdata())

f = open(path + "/levels/test_level.txt", "w")

c = 0

for i in range(0, 50):
    for j in range(0, 75):
        r, g, b = rgb_img.getpixel((j, i))
        if r == 0 and g == 0 and b == 0:
            f.write("-")
        elif r == 255 and g == 0 and b == 0:
            f.write("*")
        elif r == 0 and g == 255 and b == 0:
            f.write("%")

    if i != 49: f.write("\n")