from settings import *
from state_machine import *
from utils import *
import pygame as pg

class XerxesProjectileState(State):
    def __init__(self, boss):
        pass
        self.xerxes = boss
        self.name = "fly"

    def get_state_name(self):
        pass
        return "fly"

    def enter(self):
        pass
        print('enter player fly state')

    def exit(self):
        pass
        print('exit player fly state')

    def update(self):
        pass

class XerxesMovingState(State):
    def __init__(self, boss):
        pass
        self.xerxes = boss
        self.name = "fly"

    def get_state_name(self):
        pass
        return "fly"

    def enter(self):
        pass
        print('enter player fly state')

    def exit(self):
        pass
        print('exit player fly state')

    def update(self):
        pass

class XerxesStunState(State):
    def __init__(self, boss):
        pass
        self.xerxes = boss
        self.name = "fly"

    def get_state_name(self):
        pass
        return "fly"

    def enter(self):
        pass
        print('enter player fly state')

    def exit(self):
        pass
        print('exit player fly state')

    def update(self):
        pass

