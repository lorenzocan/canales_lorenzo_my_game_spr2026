from settings import *
from utils import *
from state_machine import State
import pygame as pg

class Start(State):
    def __init__(self, game):
        self.game = game
    
    def enter(self):
        self.game.playing = False
        self.game.paused = True

    def exit(self):
        pass

    def update(self):
        pass

    def get_state_name(self):
        return "Start"

class LevelSelect(State):
    def __init__(self, game):
        self.game = game

    def enter(self):
        self.game.screen.fill(LEVEL_SELECT_GREEN)
        self.game.paused = True
        self.game.playing = False

    def exit(self):
        pass

    def update(self):
        pass

    def get_state_name(self):
        return "LevelSelect"

class Playing(State):
    def __init__(self, game):
        self.game = game
    
    def enter(self):
        self.game.paused = False
        self.game.playing = True

    def exit(self):
        pass

    def update(self):
        pass

    def get_state_name(self):
        return "Playing"

class Paused(State):
    def __init__(self, game):
        self.game = game
    
    def enter(self):
        self.game.paused = True
        self.game.playing = False

    def exit(self):
        pass

    def update(self):
        pass

    def get_state_name(self):
        return "Paused"