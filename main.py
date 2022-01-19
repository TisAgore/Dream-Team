from cgitb import text
import sys
import pygame
import time
import os
from pygame.color import THECOLORS
import math

path = os.path.abspath(os.getcwd())

pygame.init()

screen = pygame.display.set_mode((1200, 800))

tanks_group = pygame.sprite.Group()
textures_group = pygame.sprite.Group()
missles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Texture(pygame.sprite.Sprite):
    def __init__(self, path, x, y, ispassable, iskillable):
        super().__init__(textures_group, all_sprites)
        self.x = x
        self.y = y
        self.ispassable = ispassable
        self.iskillable = iskillable
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect().move(16*y, 16*x)

        self.add(textures_group, all_sprites)

    def get_coords(self):
        return self.x, self.y

class Tank(pygame.sprite.Sprite):

    sprites = {"gold": ["gold_tank_up.png", "gold_tank_down.png", "gold_tank_right.png", "gold_tank_left.png"],
                "red": ["red_tank_up.png", "red_tank_down.png", "red_tank_right.png", "red_tank_left.png"],
                "green": ["green_tank_up.png", "green_tank_down.png", "green_tank_right.png", "green_tank_left.png"],
                "grey": ["grey_tank_up.png", "grey_tank_down.png", "grey_tank_right.png", "grey_tank_left.png"]}

    def __init__(self, path, x, y, type):
        super().__init__(tanks_group, all_sprites)
        self.images = Tank.sprites.get(type)
        self.x = x
        self.y = y
        self.path = path
        self.image = pygame.image.load(path + Tank.sprites.get(type)[0])
        self.rect = self.image.get_rect().move(16*y, 16*x)

        self.add(tanks_group, all_sprites)
    
    def move(self, x, y, image):
        self.image = pygame.image.load(self.path + self.images[image])
        if check_borders(self.x+x, self.y+y):
            self.x += x
            self.y += y
        self.rect = self.image.get_rect().move(16*self.y, 16*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

class Missle(pygame.sprite.Sprite):

    sprites = {"up": "missle_up.png", "down": "missle_down.png", "right": "missle_right.png", "left": "missle_left.png"}

    def __init__(self, path, x, y, ttl, type):
        super().__init__(missles_group, all_sprites)
        self.image = Missle.sprites.get(type)
        self.x = x
        self.y = y
        self.ttl = ttl
        self.image = pygame.image.load(path + Missle.sprites.get(type))
        self.rect = self.image.get_rect().move(16*y, 16*x)

        self.add(missles_group, all_sprites)

        self.type = [1/4, 0]
    
    def move(self):
        if check_borders(self.x + self.type[0], self.y + self.type[1]) and self.ttl > 0:
            self.x = self.x + self.type[0]
            self.y = self.y + self.type[1]
            self.rect = self.image.get_rect().move(16*self.y, 16*self.x)
            self.remove(tanks_group, all_sprites)
            self.add(tanks_group, all_sprites)
        
        else:
            self.remove(tanks_group, all_sprites)

        self.ttl -= 1

def check_borders(x, y):
    global screen, textures_group

    width, height = screen.get_size()

    for texture in textures_group:
        if (texture.x == math.ceil(x) and texture.y == math.ceil(y) or texture.x == math.floor(x) and texture.y == math.floor(y) or \
            texture.x == math.ceil(x) and texture.y == math.floor(y) or texture.x == math.floor(x) and texture.y == math.ceil(y)) and texture.ispassable == False:
            return False

    if y*16+10 > width or x < 0 or x*16+10 > height or y < 0:
        return False
    return True

def draw_level():   #level's size is 75x50 textures
    global tank

    f = open(path + "/levels/new_level.txt", "r")
    level = list([str(i).replace("\n", '') for i in f.readlines()])
    for i in range(0, len(level)):
        for j in range(0, len(level[0])):
            if level[i][j] == '%':
                Texture(path + "/sprites/grass.png", i, j, ispassable=True, iskillable=False)
            elif level[i][j] == '*':
                Texture(path + "/sprites/bricks.png", i, j, ispassable=False, iskillable=True)
            elif level[i][j] == 'A':
                tank = Tank(path=(path + "/sprites/"), x=i, y=j, type="gold")
            elif level[i][j] == 'B':
                Tank(path=(path + "/sprites/"), x=i, y=j, type="grey")
            elif level[i][j] == 'C':
                Tank(path=(path + "/sprites/"), x=i, y=j, type="red")
            elif level[i][j] == 'D':
                Tank(path=(path + "/sprites/"), x=i, y=j, type="green")
tank = 0
draw_level()
Missle(path=(path + "/sprites/"), x=30, y=45, ttl=5, type="up")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        tank.move(x=-1/4, y=0, image=0)
    if keys[pygame.K_DOWN]:
        tank.move(x=1/4, y=0, image=1)
    if keys[pygame.K_LEFT]:
        tank.move(x=0, y=-1/4, image=3)
    if keys[pygame.K_RIGHT]:
        tank.move(x=0, y=1/4, image=2)
    
    for missle in missles_group:
        missle.move()
    screen.fill(THECOLORS['black'])
    tanks_group.draw(screen)
    missles_group.draw(screen)
    textures_group.draw(screen)
    pygame.display.flip()
    time.sleep(0.01)