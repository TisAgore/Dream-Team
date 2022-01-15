import os
from PIL import Image

path = os.path.abspath(os.getcwd())

img = Image.open(path + "/Dream-Team/levels/new_level.png", "r")
pixels = list(img.getdata())

f = open(path + "/Dream-Team/levels/new_level.txt", "w")

c = 0

for i in range(0, len(pixels)):
    if c == 75:
        f.write("\n")
        c = 0
    if pixels[i] == 0:
        f.write("-")
    if pixels[i] == 1:
        f.write("*")
    c += 1