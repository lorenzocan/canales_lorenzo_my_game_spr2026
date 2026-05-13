# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"

'''
main file responsible for game loop including input, update, and draw methods
'''

import pygame as pg
import sys
from os import path # accesses file system/operating system
from random import *
from settings import *
from sprites import *
from utils import *
from ctypes import Array
from state_machine import *
from game_states import *

# the game class that will be instantiated in order to run the game
class Game: # the pen factory-the outline of the game-instances of the pen arent the factory itself!!!
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # settings up pygame screen using tuple value for width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.paused = False
        self.game_cooldown = Cooldown(3000)
        self.current_level = 0
        self.levels = ["level1.txt","level2.txt"]
        self.state_machine = StateMachine()
        self.states: Array[State] = [Start(self), LevelSelect(self), Playing(self)]
        self.state_machine.start_machine(self.states)
        
    # a method is a function tied to a Class
    def load_data(self, map):
        self.game_dir = path.dirname(__file__) # '__file__' is representative of this whole file - self.game_dir is set to all files in my_game
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'Audio')
        self.wall_image = pg.image.load(path.join(self.img_dir, 'Wall1.png'))
        # self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, ""))
        self.map = Map(path.join(self.game_dir, map))
        print('data loaded')

    def next_level(self, map):
        for s in self.all_sprites:
            s.kill()
        self.load_data(map)

        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_collectables = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    Wall(self, col + 0.5, row + 0.5)
                if tile == 'P':
                    self.player = Player(self, col + 0.5, row + 0.5)
                if tile == 'M':
                    Mob(self, col + 0.5, row + 0.5)
                if tile == 'C':
                    Coin(self, col + 0.5, row + 0.5)
                if tile == "X":
                    self.xerxes = Xerxes(self, col + 0.5, row + 0.5)
    
    def new(self):
        self.load_data(self.levels[self.current_level])

        # groups that objects in the sprite module will call on
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_collectables = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.selections = pg.sprite.Group()

        # nested for loop to display each sprite to its respective position in level1.text
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    # call class constructor without assigning variable when you want to call it multiple times where they don't need a special name assigned to it
                    Wall(self, col + 0.5, row + 0.5) # + 0.5 is adjustment for rect center
                if tile == 'P':
                    self.player = Player(self, col + 0.5, row + 0.5)
                if tile == 'M':
                    Mob(self, col + 0.5, row + 0.5)
                if tile == 'C':
                    Coin(self, col + 0.5, row + 0.5)
        # pg.mixer.music.load(path.join(self.snd_dir, ""))
        # pg.mixer.music.play(loops=-1)
        self.run()
        
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # delta time in seconds 
            self.events()
            self.update()
            self.draw()

    def events(self):
        # stuff that happens with peripherals - keyboard, mouse, camera, microphone, joystick, controller, touchscreen, stylus, trackpad
        game_state = self.state_machine.current_state.get_state_name()
        for event in pg.event.get(): # to interate through every event
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.quit()
                if game_state == "Start":
                        self.state_machine.transition("LevelSelect")
            if event.type == pg.MOUSEBUTTONDOWN and game_state == "LevelSelect":
                self.selections.click_check()
                """
                why won't this work?????????????????
                it says the Group object has no attribute 'click_check' but it should because its a method of
                selections ?????
                STILL DONT UNDERSTAND WHAT IS APPENING HERE
                """

    def quit(self):
        self.playing = False
        self.running = False

    def update(self):
        self.state_machine.update()
        
    def draw(self): # method that is responsible for displaying everything on the screen
        game_state = self.state_machine.current_state.get_state_name()

        if game_state == "Start":
            self.screen.fill(BLACK)
            self.draw_text("FRAGMENT", 50, WHITE, WIDTH/2, HEIGHT/2.5)
            self.draw_text("press any key to start", 25, WHITE, WIDTH/2, HEIGHT/2)

        if game_state == "Playing":
            self.screen.fill(BLUE)
            self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
            self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
            self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
            self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)

            self.all_sprites.draw(self.screen) # draws all sprites (walls, mobs, players, etc)
            # draw_health_bar(self.screen, 10, 10, self.player.health)

        if game_state == "Paused":
            self.draw_text("PAUSED", 100, WHITE, WIDTH/2, HEIGHT/2)

        pg.display.flip() # display the images and text on screen
    
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)




# makes sure you are calling Game from main.py
if __name__ == "__main__":
    g = Game() # instantiates game upon running the code

while g.running: # upon instantiation the game which will set self.running() to True
    g.new()

g.quit