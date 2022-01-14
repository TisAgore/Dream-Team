import sys
import pygame
import time
import os
from pygame.color import THECOLORS

path = os.path.abspath(os.getcwd())

pygame.init()

screen = pygame.display.set_mode((1200, 800))

screen.fill(THECOLORS['blue'])

textures_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

class Texture(pygame.sprite.Sprite):
    def __init__(self, path, x, y):
        super().__init__(textures_group, all_sprites)
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect().move(16*x, 15*y)

        self.add(textures_group, all_sprites)

def draw_level():

    f = open(path + "/Dream-Team/levels/level1.txt", "r")
    level = list([str(i)[0:10] for i in f.readlines()])
    for i in range(0, 10):
        for j in range(0, 10):
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
    screen.fill(THECOLORS['blue'])
    textures_group.draw(screen)
    pygame.display.flip()
    time.sleep(0.04)