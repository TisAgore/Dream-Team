import sys
import pygame
import time
import os
from pygame.color import THECOLORS

path = os.path.abspath(os.getcwd())

pygame.init()
#75x50 sprites
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
        self.x = x
        self.y = y
        self.path = path
        self.image = pygame.image.load(path + "gold_tank_up.png")
        self.rect = self.image.get_rect().move(16*y, 15*x)

        self.add(tanks_group, all_sprites)
    
    def move_up(self):
        self.image = pygame.image.load(self.path + "gold_tank_up.png")
        self.x -= 2
        self.rect = self.image.get_rect().move(16*self.y, 15*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

    def move_down(self):
        self.image = pygame.image.load(self.path + "gold_tank_down.png")
        self.x += 2
        self.rect = self.image.get_rect().move(16*self.y, 15*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

    def move_left(self):
        self.image = pygame.image.load(self.path + "gold_tank_left.png")
        self.y -= 2
        self.rect = self.image.get_rect().move(16*self.y, 15*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

    def move_right(self):
        self.image = pygame.image.load(self.path + "gold_tank_right.png")
        self.y += 2
        self.rect = self.image.get_rect().move(16*self.y, 15*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

def draw_level():
    global tank

    f = open(path + "/levels/new_level.txt", "r")
    level = list([str(i).replace("\n", '') for i in f.readlines()])
    for i in range(0, len(level)):
        for j in range(0, len(level[0])):
            if level[i][j] == '-':
                Texture(path + "/sprites/void.png", i, j)
            elif level[i][j] == '*':
                Texture(path + "/sprites/brick_wall.png", i, j)
            elif level[i][j] == 'A':
                Tank(path + "/sprites/", i, j)

draw_level()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            for tank in tanks_group:
                if event.key == pygame.K_UP:
                    print(1)
                    tank.move_up()
                if event.key == pygame.K_DOWN:
                    print(2)
                    tank.move_down()
                if event.key == pygame.K_LEFT:
                    print(3)
                    tank.move_left()
                if event.key == pygame.K_RIGHT:
                    print(4)
                    tank.move_right()
    #draw_level()
    screen.fill(THECOLORS['black'])
    textures_group.draw(screen)
    tanks_group.draw(screen)
    pygame.display.flip()
    time.sleep(0.04)