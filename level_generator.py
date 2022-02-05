import os
from PIL import Image
from sys import argv

def main():

    image_name, level_path = argv[1::]

    path = os.path.abspath(os.getcwd())

    img = Image.open(path + "/levels/" + image_name, "r")
    rgb_img = img.convert("RGB")

    f = open(path + "/levels/" + level_path + ".txt", "w")

    for i in range(0, 50):
        for j in range(0, 75):
            r, g, b = rgb_img.getpixel((j, i))
            if r == 0 and g == 0 and b == 0:    #RGB(0, 0, 0) equals void
                f.write("-")
            elif r == 255 and g == 0 and b == 0:    #RGB(255, 0, 0) equals brick wall
                f.write("*")
            elif r == 0 and g == 255 and b == 0:    #RGB(0, 255, 0) equals grass
                f.write("%")
            elif r == 255 and g == 255 and b == 255: #RGB(255, 255, 255) equals steel wall
                f.write("#")
            elif r == 50 and g == 50 and b == 50:   #RGB(50, 50, 50) equals 1st player
                f.write("P")
            elif r == 150 and g == 150 and b == 150:    #RGB(150, 150, 150) equals 2nd player 
                f.write("E")
            else:
                f.write("-")

        if i != 49: f.write("\n")

if __name__ == "__main__":
    if "--help" in argv or len(argv) != 3:
        print("Tool for generating levels\n\nUsage: \n>level_generator.py {level_image_name - Must be stored in /levels/ folder} {level_file_name}\n\nExample: \n>level_generator.py level.png level")
    else:
        main()