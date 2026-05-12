import pygame as pg
from pygame.sprite import Sprite
from settings import *
from utils import *
from os import path
from state_machine import *
from ctypes import Array
from player_states import *
from xerxes_states import *

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

        self.last_update = 0
        self.current_frame = 0
        self.state_machine = StateMachine()
        self.states: Array[State] = [PlayerFlyState(self), PlayerDashState(self)]
        self.state_machine.start_machine(self.states)
        
        self.direction = "left"
        self.projectile_cd = Cooldown(250)

        self.dash_rect = (0,0,0,0)
        self.is_key_locked = False
        self.dash_slash_cd = Cooldown(2000)
        self.effect_cd = Cooldown(100)

        # self.dash_rect = pg.Rect(self.pos.x - TILESIZE, self.pos.y - TILESIZE,0,0)
        self.health = 100

    def get_keys(self):
        self.vel.x = 0 # setting velocity to 0 to make sure player stops after key release
        # this has to be self.vel.x or else any y vel manipulation wont work
        keys = pg.key.get_pressed()
        
        # move to main later to fix the problem of being able to hold the key
        if self.state_machine.current_state != "dash" and self.dash_slash_cd.ready():
            if keys[pg.K_LSHIFT]:
                print(self.state_machine.current_state)
                self.state_machine.transition("dash")
                print(12321313)

        if keys[pg.MOUSEBUTTONDOWN]:
            if self.projectile_cd.ready():
                self.projectile_cd.start() # resetting cooldown so that it's not a one time thing
                p = Projectile(self.game, self.rect.x, self.rect.y, pg.MOUSEBUTTONDOWN.pos)
                # print('p', self.pos)
                # print('p', self.rect.center)
                print(len(self.game.all_projectiles))
        
        if not self.is_key_locked:
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

    def load_images(self):
        # list to represent each sprite in the spritesheet
        self.fly_frames = [self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)]

        self.dash_frames = [self.spritesheet.get_image(0, TILESIZE, TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE, TILESIZE, TILESIZE, TILESIZE)]
        
        # removes the background in each item in the list
        for frame in self.fly_frames:
            frame.set_colorkey(BLACK)
        for frame in self.dash_frames:
            frame.set_colorkey(BLACK)

    def effects_trail(self):
        if self.effect_cd.ready():
            EffectTrail(self.game, self.rect.x, self.rect.y, self.image)

    def animate(self):
        now = pg.time.get_ticks()

        if self.state_machine.current_state.get_state_name() == "fly":
            if now - self.last_update > 500:
                self.last_update = now # this is basically 'restarting' the timer but the numbers are relative to the value of now
                self.current_frame = (self.current_frame + 1) % len(self.fly_frames) # makes current_frame += 1, but if it is the last item in list, current_frame = 0
                bottom = self.rect.bottom
                self.image = self.fly_frames[self.current_frame] # updates image using the new value for self.current_frame
                self.rect = self.image.get_rect() # this is necessary to know the coordinates of the sprite
                self.rect.bottom = bottom
        elif self.state_machine.current_state.get_state_name() == "dash":
            if now - self.last_update > 500:
                self.last_update = now # this is basically 'restarting' the timer but the numbers are relative to the value of now
                self.current_frame = (self.current_frame + 1) % len(self.dash_frames) # makes current_frame += 1, but if it is the last item in list, current_frame = 0
                bottom = self.rect.bottom
                self.image = self.dash_frames[self.current_frame] # updates image using the new value for self.current_frame
                self.rect = self.image.get_rect() # this is necessary to know the coordinates of the sprite
                self.rect.bottom = bottom

    def state_check(self):
        pass

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob": # gets the class name, turns it into a string which is compared with "Mob"
                print("i collide with a mob")

    def update(self):
        self.state_machine.update()
        self.get_keys()
        gravity(self)
        self.state_check()

        # position correction for now since you can just 0f through the wall when dashing
        if self.pos.x > WIDTH-TILESIZE:
            self.pos.x = WIDTH-TILESIZE
            self.StDash = False
        elif self.pos.x < TILESIZE:
            self.pos.x = TILESIZE
            self.StDash = False
        
        if not self.is_key_locked:
            self.pos += self.vel * self.game.dt

        self.rect.center = self.pos
        
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

        if self.game.player.is_key_locked: # reduce health when in the hitbox of player slash
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
    def __init__(self, game, x, y, mouse_pos):
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

            # adjusts to new scaling
            self.rect.x += 1
            self.rect.y += 1








# Level Select
class Selections(Sprite):
    def __init__(self, game, level_number=0):
        self.groups = game.selections
        Sprite.__init__(self, self.groups)
        self.game = game
        self.num = level_number

        self.width = SELECT_X_OFFSET + self.num*TILESIZE*4
        self.height = SELECT_Y_OFFSET 
        """
        potential future goal: height will compare offset x and the width of the entire screen
        and when they are at a certain number or something then height will go up TILESIZE * 2
        """
        self.image = pg.Surface((TILESIZE*2, TILESIZE*2))
        self.image.fill(WHITE) 
        self.rect = self.image.get_rect()

        self.pos = vec(self.width, self.height)
        self.rect.center = self.pos

        self.game.draw_text(str(self.num), 12, BLACK, self.width, self.height)

    # wil only be called by game upon click event
    def click_check(self):
        collision_bound = tuple(abs(a-b) for a,b in zip(pg.mouse.get_pos(), self.pos))
        if collision_bound[0] <= TILESIZE and collision_bound[1] <= TILESIZE:
            self.game.state_machine.transition("Playing")

    def update(self):
        if self.game.state_machine.current_state.get_state_name() != "LevelSelect":
            self.kill()
        
        self.pos = self.rect.center
        
        # checking how close the distance btwn mouse selection square is
        collision_bound = tuple(abs(a-b) for a,b in zip(pg.mouse.get_pos(), self.pos))
        # zip stores the tuples of mouse pos and sel.pos
        # gets the first value of each tuple, gets absval of the difference, then makes it the first value of the new tuple, etc.

        # i am indexing this b/c i dont know how to do tuple inequalities
        if collision_bound[0] <= TILESIZE and collision_bound[1] <= TILESIZE:
            self.image.fill(YELLOW)
            self.game.current_level = self.num
        else:
            self.image.fill(WHITE)
        self.game.draw_text(str(self.num+1), TILESIZE, BLACK, self.width, self.height-TILESIZE/2)
        
        










# Bosses

# base boss object that will be used for any boss i create because i dont want to have to do this every time
class Boss(Sprite):
    def __init__(self, game, x, y, health, max_health, hitbox, color, height, length, states):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((length, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x, y) * TILESIZE

        self.hit_rect = hitbox
        self.health = health
        self.max_health = max_health

        self.rect.center = self.pos

        # im so lazy lmao
        self.state_machine = StateMachine()
        self.states: Array[State] = states
        self.state_machine.start_machine(self.states)
    
    def basic_update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos + (TILESIZE, TILESIZE)
    
    

class Xerxes(Boss):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, 500, 500, XERXES_HITRECT.copy(), CYAN, TILESIZE * 2, TILESIZE * 2,
                         [XerxesProjectileState(self), XerxesMovingState(self), XerxesStunState(self)])


    def mode_switch(self):
        pass

    def update(self):
        self.basic_update()
        
        """
        ring of projectiles, it go spin, xerxes move around with that projectiles, it does ouchie to you, 
        end of state, shoot them away!!!!

        vulnerability time! without projectiles it cant do anythign!1
        No contact dmagea lmao you get time to hit while it moves around aimlessly!
        then it STOPS!1!
        repeat!
        """

class X_Proj():
    def __init__(self, game, ref_x, ref_y, radius, angle_offset):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((12, 12))
        
        self.image.fill(MAGENTA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos + (TILESIZE/2, TILESIZE/2)

        self.angle = angle_offset
        self.vel = vec(0,0)

        x = 0 # placeholder values until i figure out what to do
        y = 0 # placeholder values until i figure out what to do
        self.pos = vec(x,y)
        self.hit_rect = pg.Rect(x, y, 12, 12)
    
    def update(self):
        pass
        """
        idea: get pos in polar coordinates -> update in rectangular coords
        """