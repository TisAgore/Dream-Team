import sys
import pygame
import time
import os
from pygame.color import THECOLORS

path = os.path.abspath(os.getcwd())

pygame.init()

screen = pygame.display.set_mode((1200, 750))

tanks_group = pygame.sprite.Group()
textures_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Texture(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__(textures_group, all_sprites)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect().move(16*y, 15*x)

        self.add(textures_group, all_sprites)

class Tank(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__(tanks_group, all_sprites)
        self.images = ["gold_tank_up.png", "gold_tank_down.png", "gold_tank_right.png", "gold_tank_left.png"]
        self.x = x
        self.y = y
        self.path = path
        self.image = pygame.image.load(path + "gold_tank_up.png")
        self.rect = self.image.get_rect().move(16*y, 15*x)

        self.add(tanks_group, all_sprites)
    
    def move(self, x, y, image):
        self.image = pygame.image.load(self.path + self.images[image])
        if check_borders(self.x+x, self.y+y):
            self.x += x
            self.y += y
        self.rect = self.image.get_rect().move(16*self.y, 15*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)


def check_borders(x, y):
    global screen

    width, height = screen.get_size()
    if y*16+10 > width or x < 0 or x*15+10 > height or y < 0:
        return False
    return True

def draw_level():   #level's size is 75x50 textures
    global tank

    f = open(path + "/levels/new_level.txt", "r")
    level = list([str(i).replace("\n", '') for i in f.readlines()])
    for i in range(0, len(level)):
        for j in range(0, len(level[0])):
            if level[i][j] == '-':
                #Texture(path + "/sprites/void.png", i, j)
                pass
            elif level[i][j] == '*':
                Texture(path + "/sprites/brick_wall.png", i, j)
            elif level[i][j] == 'A':
                tank = Tank(path + "/sprites/", i, j)
tank = 0
draw_level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        tank.move(x=-1/2, y=0, image=0)
    if keys[pygame.K_DOWN]:
        tank.move(x=1/2, y=0, image=1)
    if keys[pygame.K_LEFT]:
        tank.move(x=0, y=-1/2, image=3)
    if keys[pygame.K_RIGHT]:
        tank.move(x=0, y=1/2, image=2)
    
    screen.fill(THECOLORS['black'])
    textures_group.draw(screen)
    tanks_group.draw(screen)
    pygame.display.flip()
    time.sleep(0.04)