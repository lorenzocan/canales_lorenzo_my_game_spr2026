import pygame as pg
from pygame.sprite import Sprite
from settings import *

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect() # gives the engine the ability to know where the pixels are for the player
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE

    def get_keys(self):
        self.vel = vec(0,0) # setting velocity to 0 in order to make sure the character doesnt fly randomly 
        keys = pg.key.get_pressed()
        
        if keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        collect = pg.sprite.spritecollide(self, self.game.all_collectables, True)
        if hits:
            print("wahoooo")
        if collect:
            print("you collected the coin thing")

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.speed = 3
    def update(self):
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        # if hits:
        #     print("COLLIDE")
        
        # self.pos += self.game.player.pos*-self.game.dt
        # self.rect.center = self.pos
        # self.pos += self.vel * self.speed * self.game.dt
    
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls # adding an all_walls group to be able to dileniate between an entity and a wall
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_collectables
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0,0)
    def update(self):
        pass