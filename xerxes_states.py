from settings import *
from state_machine import State
from utils import *
import sprites # i have to do this because i get an error other wise - it may have to do with both modules importing each other
import pygame as pg
from math import pi
from random import randint
from math import sqrt

vec = pg.math.Vector2

class XerxesStartProjState(State):
    def __init__(self, xerxes):
        self.xerxes = xerxes
        self.name = "XStart"

    def get_state_name(self):
        return "XStart"

    def enter(self):
        self.health_lock = self.xerxes.health
        self.xerxes.grav_switch = False
        self.ring_cd = Cooldown(100)
        self.ring_count = 1
        self.xerxes.image.fill(GREEN)
        print('enter xerxes XStart state')

    def exit(self):
        print('exit xerxes XStart state')

    def update(self):
        self.xerxes.vel.y = 0
        # invincibility at start state
        self.xerxes.health = self.health_lock

        # makes the instantiaton of the projectiles really cool
        if self.ring_count <= 8 and self.ring_cd.ready():
            self.ring_cd.start()
            self.ring_count += 1
            sprites.X_Proj(self.xerxes.game, self.xerxes.pos.x - TILESIZE/2, self.xerxes.pos.y - TILESIZE/2, TILESIZE * 3, self.ring_count * pi/4, self.xerxes)
        if self.ring_count > 8:
            # after everything has been instantiated, everything starts rotating, transition to next state
            self.xerxes.game.all_xproj.update(True, False)
            self.xerxes.state_machine.transition("XMove")

class XerxesMovingState(State):
    def __init__(self, xerxes):
        self.xerxes = xerxes
        self.name = "XMove"

    def get_state_name(self):
        return "XMove"

    def enter(self):
        self.name = "XMove"
        self.move_count = randint(12, 23)
        self.move_counter = 0
        self.xerxes.grav_switch = False
        self.xerxes.image.fill(CYAN)
        self.move_spots = []

        self.init_pos = self.xerxes.pos

        # get random number of positions to move to (these positions are random)
        for count in range(self.move_count):
            self.move_spots.append(vec(randint(TILESIZE*2, WIDTH-TILESIZE*2), randint(TILESIZE*2, HEIGHT-TILESIZE*2)))
        print('enter xerxes XMove state')

    def exit(self):
        self.name = None
        self.xerxes.vel = vec(0,0)
        self.xerxes.game.all_xproj.update(False, True)
        print('exit xerxes XMove state')

    def update(self):
        dx = self.move_spots[self.move_counter].x - self.init_pos.x
        dy = self.move_spots[self.move_counter].y - self.init_pos.y

        # same thing used in Projectile - get unit vector, uniform vel each time it moves
        self.xerxes.vel.x = (dx / sqrt(dx**2 + dy**2)) * TILESIZE * 30
        self.xerxes.vel.y = (dy / sqrt(dx**2 + dy**2)) * TILESIZE * 30

        # explanation update of Selections object in sprites
        move_bound = tuple(abs(a-b) for a,b in zip(self.move_spots[self.move_counter], self.xerxes.pos))

        if move_bound <= (TILESIZE, TILESIZE):
            self.xerxes.game.all_xproj.update(False, True) # expels current set of 8 upon changing direction
            if self.move_counter < len(self.move_spots):
                self.move_counter += 1 
            self.init_pos = self.xerxes.pos

            if self.move_counter == len(self.move_spots):
                self.xerxes.state_machine.transition("XJump")
                # transition calls on exit method but still finished the updating here
                # exit sets self.name to None to ensure that 8 projectiles dont show up when they arent supposed to
            
            if self.xerxes.current_state == self.name:
                for i in range(8):
                    sprites.X_Proj(self.xerxes.game, self.xerxes.pos.x, self.xerxes.pos.y, TILESIZE * 3, i * pi/4, self.xerxes)
            self.xerxes.game.all_xproj.update(True, False)


class XerxesJumpState(State):
    def __init__(self, xerxes):
        self.xerxes = xerxes
        self.name = "XJump"

    def get_state_name(self):
        return "XJump"

    def enter(self):
        self.name = "XJump"
        self.jump_count = randint(7,14)
        self.jump_counter = 0
        self.xerxes.vel = vec(0,0)
        self.xerxes.grav_switch = True
        self.xerxes.image.fill(BLACK)
        self.jump_cd = Cooldown(1000)
        self.player_x = self.xerxes.game.player.pos.x
        self.init_pos_x = self.xerxes.pos.x
        print('enter xerxes XJump state')

    def exit(self):
        sprites.ScreenPulse(self.xerxes.game,RED,2)
        self.name = None
        self.xerxes.grav_switch = False
        self.xerxes.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)

    def update(self):
        self.player_x = self.xerxes.game.player.pos.x
        if self.jump_cd.ready():
            self.jump_cd.start()
            self.jump_counter += 1

            if self.jump_counter == self.jump_count:
                self.xerxes.state_machine.transition("XStart")
            
            if self.name == "XJump":
                self.xerxes.pos.y -= 12
                self.xerxes.vel.y = TILESIZE** 2 * 4 * -1
                self.xerxes.vel.x = (self.player_x - self.init_pos_x) * 1.5

            self.init_pos_x = self.xerxes.pos.x

        if self.xerxes.vel.y >= 0:
            self.xerxes.vel.x = 0

class XerxesStunState(State):
    def __init__(self, xerxes):
        self.xerxes = xerxes
        self.name = "XStun"

    def get_state_name(self):
        return "XStun"

    def enter(self):
        self.xerxes.grav_switch = True
        print('enter xerxes XStun state')

    def exit(self):
        pass
        print('exit xerxes XStun state')

    def update(self):
        pass

