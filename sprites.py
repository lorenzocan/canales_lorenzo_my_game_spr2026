import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path

vec = pg.math.Vector2


# creating a function for wall collision instead of in a class because it will be used regularly by all the classes
# checks for collisions between "one" and "two" using colliderect method in the pygame library (returns boolean)
# the "hit_rect" is the PLAYER_HIT_RECT constant in settings
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


# tells if "one" has collided with "two" using the boolean returned from the collide_hit_rect function
# checks for x and y collision - sets pos based on collison dir
def collide_with_walls(sprite, group, dir):
    if dir == "x":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect) # the thing that checks the collision
        if hits:
            # print("collided with wall from x dir")
            # checking position of wall relative to position of players hitbox to determine where to adjust player
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0 # makes sure you don't phase through the wall
            sprite.hit_rect.centerx = sprite.pos.x
    # separation of x and y collision so that if you do something like collide in the x direction, you wouldn't want it to check for y collision
    
    if dir == "y":
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # print("collided with wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
    

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'sprite_sheet.png'))
        # self note to make the spritesheet better since there is still black stuff in the bg of it
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect() # gives the engine the ability to know where the pixels are for the player
        self.load_images()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = PLAYER_HITRECT
        self.jumping = False
        self.walking = False
        self.last_update = 0
        self.current_frame = 0

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
        if self.vel.x != 0 and self.vel.y != 0: # adjusting speed for diagonal movement
            self.vel *= 0.7071

    def load_images(self):
        # list to represent each sprite in the spritesheet
        self.standing_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)]
        self.walking_frames = [self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE)]
        # removes the background in each item in the list
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        for frame in self.walking_frames:
            frame.set_colorkey(BLACK)
        self.image = self.standing_frames[0]
        # print("loaded image")

    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.walking: # self.jumping and self.walking are just theoretical states the player could be in for now
            if now - self.last_update > 500:
                self.last_update = now # this is basically 'restarting' the timer but the numbers are relative to the value of now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames) # makes current_frame += 1, but if it is the last item in list, current_frame = 0
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame] # updates image using the new value for self.current_frame
                self.rect = self.image.get_rect() # I think this is necessary for coordinates?
                self.rect.bottom = bottom
        elif self.walking:
            if now - self.last_update > 500:
                self.last_update = now # this is basically 'restarting' the timer but the numbers are relative to the value of now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames) # makes current_frame += 1, but if it is the last item in list, current_frame = 0
                bottom = self.rect.bottom
                self.image = self.walking_frames[self.current_frame] # updates image using the new value for self.current_frame
                self.rect = self.image.get_rect() # I think this is necessary for coordinates?
                self.rect.bottom = bottom
    
    # I am keeping this in here for now since I am trying to figure out what is different between these two
    # because the one below (the one I typed) doesn't work, but the one above (copy & pasted) does work
    # def animate(self):
    #     now = pg.time.get_ticks()
    #     if not self.jumping and not self.walking:
    #         if now - self.last_update > 3500:
    #             self.last_update = now
    #             self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
    #             bottom = self.rect.bottom
    #             self.iamge = self.standing_frames[self.current_frame]
    #             self.rect = self.image.get_rect()
    #             self.rect.bottom = bottom

    def update(self):
        self.get_keys()
        
        if self.vel != (0,0):
            self.walking = True
            # print("StWalk")
        else:
            self.walking = False
        
        
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        # state update
        

        # updating hitbox to align with sprite,  
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        # updating sprite to align with moved hitbox
        self.rect.center = self.hit_rect.center


        # hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        collect = pg.sprite.spritecollide(self, self.game.all_collectables, True)
        # if hits:
        #     print("wahoooo")
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
        self.hit_rect = MOB_HITRECT

    def update(self):
        self.rect.center = self.pos
        
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centerx = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

        # self.pos += self.game.player.pos*-self.game.dt
        # self.pos += self.vel * self.speed * self.game.dt
    
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls # adding an all_walls group to be able to dileniate between an entity and a wall
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
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
        self.rect.center = self.pos
    def update(self):
        pass