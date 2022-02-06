import socket
from cgitb import text
import sys
import pygame
import os
from pygame.color import THECOLORS
import math
import threading

class Texture(pygame.sprite.Sprite):
    def __init__(self, path, x, y, ispassable, isdestroyable):
        super().__init__(textures_group, all_sprites)
        self.x = x
        self.y = y
        self.ispassable = ispassable
        self.isdestroyable = isdestroyable
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect().move(16*y, 16*x)

        if self.isdestroyable == True:
            self.add(destroyable_textures)
        elif self.ispassable == True:
            self.add(walk_through_textures)
        else:
            self.add(undestroyable_textures)

        self.add(textures_group, all_sprites)

    def get_coords(self):
        return self.x, self.y

class Tank(pygame.sprite.Sprite):

    sprites = {"gold": ["gold_tank_up.png", "gold_tank_down.png", "gold_tank_right.png", "gold_tank_left.png"],
                "red": ["red_tank_up.png", "red_tank_down.png", "red_tank_right.png", "red_tank_left.png"],
                "green": ["green_tank_up.png", "green_tank_down.png", "green_tank_right.png", "green_tank_left.png"],
                "grey": ["grey_tank_up.png", "grey_tank_down.png", "grey_tank_right.png", "grey_tank_left.png"]}

    def __init__(self, path, x, y, type, hitpoints):
        super().__init__(tanks_group, all_sprites)
        self.images = Tank.sprites.get(type)
        self.x = x
        self.y = y
        self.hitpoints = hitpoints
        self.path = path
        self.image = pygame.image.load(path + Tank.sprites.get(type)[0])
        self.rect = self.image.get_rect().move(16*y, 16*x)

        self.add(tanks_group, all_sprites)
    
    def move(self, x, y, image):
        self.direction = list(Missle.sprites.keys())[image]
        self.image = pygame.image.load(self.path + self.images[image])
        if check_borders(self.x+x, self.y+y):
            self.x += x
            self.y += y
        if self.hitpoints == 0:
            print("Killed")
            self.remove(tanks_group, all_sprites)
        self.rect = self.image.get_rect().move(16*self.y, 16*self.x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

    def place(self, x, y, image):
        self.direction = list(Missle.sprites.keys())[image]
        self.image = pygame.image.load(self.path + self.images[image])
        self.rect = self.image.get_rect().move(16*y, 16*x)
        self.remove(tanks_group, all_sprites)
        self.add(tanks_group, all_sprites)

class Missle(pygame.sprite.Sprite):

    sprites = {"up": "missle_up.png", "down": "missle_down.png", "right": "missle_right.png", "left": "missle_left.png", "blaze": "blaze.png"}

    def __init__(self, path, x, y, ttl, type, speed, owner):
        if type == "up":
            self.type = [-speed, 0]
        elif type == "down":
            self.type = [speed, 0]
        elif type == "right":
            self.type = [0, speed]
        elif type == "left":
            self.type = [0, -speed]

        super().__init__(missles_group, all_sprites)
        self.image = Missle.sprites.get(type)
        self.path = path
        self.x = x + 0.4 + self.type[0]*3
        self.y = y + 0.4 + self.type[1]*3
        self.ttl = ttl
        self.owner = owner
        self.image = pygame.image.load(path + Missle.sprites.get(type))
        self.rect = self.image.get_rect().move(16*self.y, 16*self.x)

        self.add(missles_group, all_sprites)

    def move(self):
        
        texture_hits = pygame.sprite.spritecollide(self, destroyable_textures, True)
        undestroyable_texture_hits = pygame.sprite.spritecollide(self, undestroyable_textures, False)
        tank_hits = pygame.sprite.spritecollide(self, tanks_group, False)

        if undestroyable_texture_hits:  #check collisions with undestroyable textures
            self.remove(missles_group, all_sprites)
        elif len(tank_hits) > 0:    #check collisions with tanks
            for tank in tank_hits:
                tank.hitpoints -= 1
            self.remove(missles_group, all_sprites)
        elif self.y*16+8 > width or self.x < 0 or self.x*16+8 > height or self.y < 0: #check collisions with screen borders
            self.remove(missles_group, all_sprites)
        elif not(texture_hits) and self.ttl > 0:    #move missle
            self.x = self.x + self.type[0]
            self.y = self.y + self.type[1]
            self.rect = self.image.get_rect().move(16*self.y, 16*self.x)
            self.remove(missles_group, all_sprites)
            self.add(missles_group, all_sprites)        
        else:
            self.remove(missles_group, all_sprites)

        self.ttl -= 1

def check_borders(x, y):
    global screen, textures_group

    width, height = screen.get_size()

    for texture in textures_group:  #check texture's collisions
        if (texture.x == math.ceil(x) and texture.y == math.ceil(y) or texture.x == math.floor(x) and texture.y == math.floor(y) or \
            texture.x == math.ceil(x) and texture.y == math.floor(y) or texture.x == math.floor(x) and texture.y == math.ceil(y)) and texture.ispassable == False:
            return False

    if y*16+16 > width or x < 0 or x*16+16 > height or y < 0:   #check window borders
        return False
    return True

def draw_level():   #level's size is 75x50 textures
    global tank, enemy

    f = open(path + "/levels/test_level.txt", "r")
    level = list([str(i).replace("\n", '') for i in f.readlines()])
    for i in range(0, len(level)):
        for j in range(0, len(level[0])):
            if level[i][j] == '%':
                Texture(path + "/sprites/grass.png", i, j, ispassable=True, isdestroyable=False)
            elif level[i][j] == '*':
                Texture(path + "/sprites/bricks.png", i, j, ispassable=False, isdestroyable=True)
            elif level[i][j] == "#":
                Texture(path + "/sprites/steel_wall.png", i, j, ispassable=False, isdestroyable=False)
            elif level[i][j] == 'P':
                if flag:
                    tank = Tank(path=(path + "/sprites/"), x=i, y=j, type="red", hitpoints=3)
                else:
                    tank = Tank(path=(path + "/sprites/"), x=i, y=j, type="gold", hitpoints=3)
            elif level[i][j] == 'E':
                if flag:
                    enemy = Tank(path=(path + "/sprites/"), x=i, y=j, type="gold", hitpoints=3)
                else:
                    enemy = Tank(path=(path + "/sprites/"), x=i, y=j, type="red", hitpoints=3)

def get_data(sock): #Thread to get 2nd Palyer's data
    global enemy
    while True:

        data = sock.recv(50)

        data = data.decode("UTF-8")
        data = data[0:data.index("*")]
        
        if data.count(' ') == 2:
            x, y, image = map(float, data.split())

            enemy.place(x=x, y=y, image=int(image))

        elif data.count(' ') == 3:

            x, y, ttl, direction = data.split()

            x = float(x)
            y = float(y)
            ttl = int(ttl)

            Missle(path=(path + "/sprites/"), x=x, y=y, ttl=ttl, type=direction, speed=1/4, owner=enemy)
        
        elif data.count(' ') == 6:
            
            missle_x, missle_y, ttl, direction, tank_x, tank_y, image = data.split()

            missle_x = float(missle_x)
            missle_y = float(missle_y)
            ttl = int(ttl)
            tank_x = float(tank_x)
            tank_y = float(tank_y)
            image = int(image)

            Missle(path=(path + "/sprites/"), x=missle_x, y=missle_y, ttl=ttl, type=direction, speed=1/4, owner=enemy)
            enemy.place(x=tank_x, y=tank_y, image=image)
        


def main(clock, sock):  #Main function
    global flag, tank, enemy
    
    loading_message = message.render(str("LOADING..."), 1, (180,0,0))
    screen.blit(loading_message, (500, 300))
    pygame.display.flip()

    data = ''

    while data != "Connected":
        
        data = sock.recv(10).decode("utf-8")

    flag = sock.recv(1).decode("utf-8")
    flag = int(flag)

    draw_level()

    if flag:
        tank, enemy = enemy, tank

    t = threading.Thread(target=get_data, args=(sock,), daemon=True)
    t.start()

    while True: #Game cycle
        clock.tick(60)

        data = ''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spawn = True
                    for missle in missles_group:
                        if missle.owner == tank:
                            spawn = False
                    if spawn:
                        Missle(path=(path+"/sprites/"), x=tank.x, y=tank.y, ttl=240, type=tank.direction, speed=1/4, owner=tank)
                        data += str(tank.x) + ' ' + str(tank.y) + ' ' + str(240) + ' ' + str(tank.direction)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            tank.move(x=-1/8, y=0, image=0)
            if len(data) > 0:
                data += ' '
            data += str(tank.x) + ' ' + str(tank.y) + ' ' + str(0)
        elif keys[pygame.K_DOWN]:
            tank.move(x=1/8, y=0, image=1)
            if len(data) > 0:
                data += ' '
            data += str(tank.x) + ' ' + str(tank.y) + ' ' + str(1)
        elif keys[pygame.K_LEFT]:
            tank.move(x=0, y=-1/8, image=3)
            if len(data) > 0:
                data += ' '
            data += str(tank.x) + ' ' + str(tank.y) + ' ' + str(3)
        elif keys[pygame.K_RIGHT]:
            tank.move(x=0, y=1/8, image=2)
            if len(data) > 0:
                data += ' '
            data += str(tank.x) + ' ' + str(tank.y) + ' ' + str(2)

        for missle in missles_group:
            missle.move()
        
        for tanket in tanks_group:
            if tanket.hitpoints <= 0:
                tanket.remove(tanks_group, all_sprites)
        
        data = data + '*'*(50-len(data))
        sock.send(bytes(data, encoding="UTF-8"))    #send data to server

        text_hp = message.render(str(tank.hitpoints), 1, (180,0,0)) #HP text
        
        screen.fill(THECOLORS['black'])
        tanks_group.draw(screen)
        missles_group.draw(screen)
        textures_group.draw(screen)

        screen.blit(text_hp, (1, 1)) #draw HP

        pygame.display.flip()

if __name__ == "__main__":

    path = os.path.abspath(os.getcwd())

    pygame.init()

    screen = pygame.display.set_mode((1200, 800))

    width, height = screen.get_size()

    tanks_group = pygame.sprite.Group()
    textures_group = pygame.sprite.Group()
    destroyable_textures = pygame.sprite.Group()
    walk_through_textures = pygame.sprite.Group()
    undestroyable_textures = pygame.sprite.Group()
    missles_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    message = pygame.font.Font(None, 36)

    tank = 0
    enemy = 0
    flag = 0

    clock = pygame.time.Clock()
    
    sock = socket.socket()

    sock.connect(('localhost', 8088))

    main(clock, sock)