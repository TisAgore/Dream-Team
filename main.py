import sys
import pygame
import time
import os
from pygame.color import THECOLORS

path = os.path.abspath(os.getcwd())

pygame.init()
#75x50 sprites
screen = pygame.display.set_mode((1200, 750))

textures_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Texture(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__(textures_group, all_sprites)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect().move(16*y, 15*x)

        self.add(textures_group, all_sprites)

def draw_level():

    f = open(path + "/Dream-Team/levels/new_level.txt", "r")
    level = list([str(i).replace("\n", '') for i in f.readlines()])
    for i in range(0, len(level)):
        for j in range(0, len(level[0])):
            if level[i][j] == '-':
                Texture(path + "/Dream-Team/sprites/void.png", i, j)
            elif level[i][j] == '*':
                Texture(path + "/Dream-Team/sprites/brick_wall.png", i, j)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    draw_level()
    screen.fill(THECOLORS['grey'])
    textures_group.draw(screen)
    pygame.display.flip()
    time.sleep(0.04)