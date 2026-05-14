from settings import *
from state_machine import *
from utils import *
import pygame as pg

class XerxesStartState(State):
    def __init__(self, boss):
        self.xerxes = boss
        self.name = "XStart"

    def get_state_name(self):
        return "XStart"

    def enter(self):
        for i in range(8):
            pass
        print('enter player XStart state')

    def exit(self):
        pass
        print('exit player XStart state')

    def update(self):
        pass

class XerxesProjectileState(State):
    def __init__(self, boss):
        self.xerxes = boss
        self.name = "XProjectiles"

    def get_state_name(self):
        return "XProjeciles"

    def enter(self):
        pass
        print('enter player XProjectiles state')

    def exit(self):
        pass
        print('exit player XProjectiles state')

    def update(self):
        pass

class XerxesMovingState(State):
    def __init__(self, boss):
        self.xerxes = boss
        self.name = "XMove"

    def get_state_name(self):
        return "XMove"

    def enter(self):
        pass
        print('enter player XMove state')

    def exit(self):
        pass
        print('exit player XMove state')

    def update(self):
        pass

class XerxesStunState(State):
    def __init__(self, boss):
        self.xerxes = boss
        self.name = "XStun"

    def get_state_name(self):
        return "XStun"

    def enter(self):
        pass
        print('enter player XStun state')

    def exit(self):
        pass
        print('exit player XStun state')

    def update(self):
        pass

