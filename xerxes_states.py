from settings import *
from state_machine import State
from utils import *
import sprites # i have to do this because i get an error other wise - it may have to do with both modules importing each other
import pygame as pg
from math import pi

class XerxesStartProjState(State):
    def __init__(self, xerxes):
        self.xerxes = xerxes
        self.name = "XStart"

    def get_state_name(self):
        return "XStart"

    def enter(self):
        self.xerxes.grav_switch = False
        self.ring_cd = Cooldown(100)
        self.ring_count = 1
        self.xerxes.image.fill(GREEN)
        print('enter xerxes XStart state')

    def exit(self):
        print('exit xerxes XStart state')

    def update(self):
        # invincibility at start state
        self.xerxes.health = 500

        # makes the instantiaton of the projectiles really cool
        if self.ring_count <= 8 and self.ring_cd.ready():
            self.ring_cd.start()
            self.ring_count += 1
            sprites.X_Proj(self.xerxes.game, self.xerxes.pos.x, self.xerxes.pos.y, TILESIZE * 3, self.ring_count * pi/4, self.xerxes)
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
        self.xerxes.grav_switch = False
        self.xerxes.image.fill(CYAN)
        print('enter xerxes XMove state')

    def exit(self):
        pass
        print('exit xerxes XMove state')

    def update(self):
        pass

class XerxesJumpState(State):
    def __init__(self, xerxes):
        self.xerxes = xerxes
        self.name = "XJump"

    def get_state_name(self):
        return "XJump"

    def enter(self):
        self.xerxes.grav_switch = True
        self.xerxes.image.fill(BLACK)
        print('enter xerxes XJump state')

    def exit(self):
        print('exit xerxes XJump state')

    def update(self):
        pass

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

