import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from math import sqrt

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

# a simple gravity function that is supposed to be available by all objects this module
def gravity(sprite, terminal_yvel = STANDARD_MAX_YVEL, accel_multiplier = 1):
    if terminal_yvel > sprite.vel.y:
        sprite.vel.y += TILESIZE * accel_multiplier
        

class Player(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'sprite_sheet.png'))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.rect = self.image.get_rect() # gives the engine the ability to know where the pixels are for the player
        self.load_images()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.hit_rect = PLAYER_HITRECT
        self.StSprint = False
        self.StWalk = False
        self.StDash = False
        self.StFly = False 
        self.last_update = 0
        self.current_frame = 0
        self.direction = "left"
        self.projectile_cd = Cooldown(250)
        self.dash_slash_cd = Cooldown(2000)
        self.effect_cd = Cooldown(100)

        # using cooldown object to describe a time length for the dash rather than a length of waiting
        self.dash_slash_length = Cooldown(300) 
        self.dash_slash_freeze_length = Cooldown(200)
        self.dash_slash_end_freeze_length = Cooldown(500) # this long to account for the 300 ticks spent dashing

        self.dash_rect = pg.Rect(self.pos.x - TILESIZE, self.pos.y - TILESIZE,0,0)
        self.health = 100

    def get_keys(self):
        self.vel.x = 0 # setting velocity to 0 to make sure player stops after key release
        # this has to be self.vel.x or else any y vel manipulation wont work
        keys = pg.key.get_pressed()
        
        if keys[pg.K_f]:
            if self.projectile_cd.ready():
                self.projectile_cd.start() # resetting cooldown so that it's not a one time thing
                p = Projectile(self.game, self.rect.x, self.rect.y)
                # print('p', self.pos)
                # print('p', self.rect.center)
                print(len(self.game.all_projectiles))
        
        if not self.StDash:
            if keys[pg.K_a]:
                self.vel.x = -PLAYER_SPEED
                self.direction = "left"
            if keys[pg.K_d]:
                self.vel.x = PLAYER_SPEED
                self.direction = "right"
        
        # fly
        if keys[pg.K_SPACE]:
            if self.vel.y > PLAYER_FLY_VEL: # if player y vel is going downwards (positive) on the screen or not at max vel
                self.vel.y += PLAYER_FLY_ACCEL

        # checking dash cd
        if keys[pg.K_e]:
            if self.dash_slash_cd.ready():
                print("work\ning")



    def load_images(self):
        # list to represent each sprite in the spritesheet
        self.idle_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)]
        self.walking_frames = [self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE)]
        self.sprint_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
                                self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE)]
        self.dash_frames = [self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE),
                                self.spritesheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE)]
        # removes the background in each item in the list
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        for frame in self.walking_frames:
            frame.set_colorkey(BLACK)
        for frame in self.sprint_frames:
            frame.set_colorkey(BLACK)
        for frame in self.dash_frames:
            frame.set_colorkey(BLACK)

    def effects_trail(self):
        if self.effect_cd.ready():
            EffectTrail(self.game, self.rect.x, self.rect.y, self.image)

    def animate(self):
        now = pg.time.get_ticks()
        if not self.StSprint and not self.StWalk and not self.StDash: # self.jumping and self.walking are just theoretical states the player could be in for now
            if now - self.last_update > 500:
                self.last_update = now # this is basically 'restarting' the timer but the numbers are relative to the value of now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames) # makes current_frame += 1, but if it is the last item in list, current_frame = 0
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame] # updates image using the new value for self.current_frame
                self.rect = self.image.get_rect() # I think this is necessary for coordinates?
                self.rect.bottom = bottom
        elif self.StDash:
            if now - self.last_update > 50:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.dash_frames)
                bottom = self.rect.bottom
                self.image = self.dash_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.StWalk:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
                bottom = self.rect.bottom
                self.image = self.walking_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.StSprint:
            if now - self.last_update > 250:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
                bottom = self.rect.bottom
                self.image = self.walking_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

    # basic method to "change" the state of the player at a given point in time
    def state(self):
        keys = pg.key.get_pressed()

        # dashing -- this will definitely be moved back to get keys once i fugre out the state machine whenever
        if keys[pg.K_LSHIFT]:
            if self.dash_slash_cd.ready():
                self.dash_slash_cd.start()

                # starting timers to stop an action after a time period
                self.dash_slash_length.start()
                self.dash_slash_freeze_length.start()
                self.dash_slash_end_freeze_length.start()

                self.StDash = True
                self.StSprint = False
                self.StWalk = False
    
        elif keys[pg.K_RSHIFT] and self.vel.x != 0 and not self.StDash:
            self.StSprint = True
            self.StWalk = False
        elif self.vel.x != 0 and not self.StDash:
            self.StWalk = True
            self.StSprint = False
        else:
            self.StWalk = False
            self.StSprint = False

    def dash(self):
        if self.dash_slash_freeze_length.ready(): # after freeze time is done, do the moving

            # if the dash time is in between the end of end dash freeze and the end of dash length, do not do anything
            if not self.dash_slash_end_freeze_length.ready() and self.dash_slash_length.ready():
                pass

            elif not self.dash_slash_length.ready(): # without this, movement happens as soon as everything ends
                # check most recent direction to fix the direction of dash
                if self.direction == "left" and not self.dash_slash_length.ready():
                    self.pos.x -= PLAYER_SPEED * self.game.dt * 12
                else:
                    self.pos.x += PLAYER_SPEED * self.game.dt * 12
                self.dash_rect = pg.Rect(self.pos.x - TILESIZE, self.pos.y - TILESIZE, TILESIZE * 2, TILESIZE * 2)
        
        # stop calling this function once dash is over
        if self.dash_slash_end_freeze_length.ready():
            self.StDash = False
            self.vel.x = 0
            self.dash_rect = pg.Rect(self.pos.x - TILESIZE, self.pos.y - TILESIZE,0,0)

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob": # gets the class name, turns it into a string which is compared with "Mob"
                print("i collide with a mob")

    def update(self):
        self.get_keys()
        gravity(self)
        
        self.state()
        self.animate()

        # position correction for now since you can just 0f through the wall when dashing
        if self.pos.x > WIDTH-TILESIZE:
            self.pos.x = WIDTH-TILESIZE
            self.StDash = False
        elif self.pos.x < TILESIZE:
            self.pos.x = TILESIZE
            self.StDash = False
        
        self.rect.center = self.pos
        
        if self.StDash:
            self.effects_trail()
            self.dash()
        elif self.StSprint:
            self.pos.x += self.vel.x * 1.5 * self.game.dt
            
            # Height not affected by moving faster in x cordinates
            self.pos.y += self.vel.y * self.game.dt
        else:
            self.pos += self.vel * self.game.dt

        # updating hitbox to align with sprite
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')

        # updating sprite to align with moved hitbox
        self.rect.center = self.hit_rect.center


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.speed = 3
        self.hit_rect = MOB_HITRECT
        self.health = 100

    def update(self):
        if self.health <= 0:
            self.kill()
        
        gravity(self)
        self.rect.center = self.pos

        if self.game.player.StDash: # reduce health when in the hitbox of player slash
            if self.hit_rect.colliderect(self.game.player.dash_rect):
                self.health -= 10
                print(self.health)

        # self.vel.x = PLAYER_SPEED
        self.pos += self.vel * self.game.dt
        
        self.hit_rect.center = self.pos
        collide_with_walls(self, self.game.all_walls, 'x')
        collide_with_walls(self, self.game.all_walls, 'y')

        self.rect.center = self.hit_rect.center

 

    
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls # adding an all_walls group to be able to dileniate between an entity and a wall
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_image
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE

        self.rect.center = self.pos

    def update(self):
        # kill projectile
        pg.sprite.spritecollide(self, self.game.all_projectiles, True)


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

# Current Issue: first instance of projectile spawnws at (0,0)
class Projectile(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE-2, 12))
        self.hit_rect = PROJ_HITRECT
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.vel = vec(PROJ_SPEED,0)
        self.pos = vec(x, y)
        self.speed = 3
        self.rect.center = self.pos + (TILESIZE/2, TILESIZE/2) # the TILESIZE/2 makes the sprite show up at player position
        # instead of its center being placed at the top left corner

    def update(self):
        self.pos += self.speed * self.vel * self.game.dt
        self.rect.center = self.pos + (TILESIZE/2, TILESIZE/2)


        # trying to figure out how to kill proj before in phases inside the wall
        collide_with_walls(self, self.game.all_walls, 'x')
        self.rect.centerx = self.pos.x + TILESIZE/2
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.centery = self.pos.y + TILESIZE/2

# Intended to be a superclass used by different bosses
class Boss(Sprite):
    def __init__(self, game, x, y, health, damage, speed, size, weight):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * size, TILESIZE * size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE
        self.speed = speed
        self.hp = health
        self.attack_damage = damage
        self.accel_multiplier = weight
        self.hit_rect = self.image.get_rect()

    def update(self):
        self.rect.center = self.pos
        
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centerx = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

        gravity(self)

class EffectTrail(Sprite):
    def __init__(self, game, x, y, sprite):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)

        self.image = sprite

        self.alpha = 255
        self.rect = self.image.get_rect()
        self.cd = Cooldown(10) # how long it takes for each effect to shrink & change alpha
        self.rect.x = x
        self.rect.y = y
        self.scale_x = TILESIZE
        self.scale_y = TILESIZE

    def update(self):
        if self.alpha <= 10:
            self.kill()

        # sets the alpha of the sprite for every update to the effect
        self.image.set_alpha(self.alpha)
        
        # the effects to the sprite if cd is ready
        if self.cd.ready():
            self.scale_x -= 2
            self.scale_y -= 2
            self.alpha -= 25

            # sets the scale fo the sprite for every update to the effect
            new_image = pg.transform.scale(self.image, (self.scale_x, self.scale_y)) 
            self.image = new_image