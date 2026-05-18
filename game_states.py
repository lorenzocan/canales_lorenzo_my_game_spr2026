from settings import *
from utils import *
from sprites import Selections
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
        self.game.paused = True
        self.game.playing = False
        self.game.screen.fill(LEVEL_SELECT_GREEN)
        self.game.draw_text("CHOOSE", 32, WHITE, WIDTH/2, HEIGHT/8)
        self.game.selections = pg.sprite.Group()

        for i in range(len(self.game.levels)):
            Selections(self.game, i)

    def exit(self):
        pass

    def update(self):
        self.game.selections.draw(self.game.screen)
        self.game.selections.update()

    def get_state_name(self):
        return "LevelSelect"

class Playing(State):
    def __init__(self, game):
        self.game = game
    
    def enter(self):
        self.game.paused = False
        self.game.playing = True
        try:
            self.game.next_level(self.game.levels[self.game.current_level])
        except:
            self.game.next_level(self.game.levels[0])
        else:
            self.game.next_level(self.game.levels[self.game.current_level])
        

    def exit(self):
        pass

    def update(self):
        self.game.all_sprites.update() # using the update method for all sprites under the group in main 'all_sprites'

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