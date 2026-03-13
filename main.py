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


# the game class that will be instantiated in order to run the game
class Game: # the pen factory-the outline of the game-instances of the pen arent the factory itself!!!
    def __init__(self):
        pg.init()
        # settings up pygame screen using tuple value for width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(3000)
    
    # a method is a function tied to a Class
    def load_data(self):
        self.game_dir = path.dirname(__file__) # '__file__' is representative of this whole file - self.game_dir is set to all files in my_game
        self.img_dir = path.join(self.game_dir, 'images')
        self.wall_image = pg.image.load(path.join(self.img_dir, 'Wall1.png'))
        self.map = Map(path.join(self.game_dir, 'level1.txt'))
        print('data loaded')

    def new(self):
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_collectables = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()

        # nested for loop to display each sprite to its respective position in level1.text
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    # call class constructor without assigning variable when you want to call it multiple times where they don't need a special name assigned to it
                    Wall(self, col + 0.5, row + 0.5)
                if tile == 'P':
                    self.player = Player(self, col + 0.5, row + 0.5)
                if tile == 'M':
                    Mob(self, col + 0.5, row + 0.5)
                if tile == 'C':
                    Coin(self, col + 0.5, row + 0.5)
        
        self.run()
        

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000 # delta time in seconds 

            self.events()
            self.update()
            self.draw()

    def events(self):
        # stuff that happens with peripherals - keyboard, mouse, camera, microphone, joystick, controller, touchscreen, stylus, trackpad
        for event in pg.event.get(): # to interate through every event
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                print("mouse input")
                print(event.pos)
            if event.type == pg.KEYUP:
                if event.key == pg.K_k: # Upon releasing lowercase k, print the text below
                    print("i can determine when keys are released")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_t:
                    print("i can determine when keys are pressed")
                if event.key == pg.K_r:
                    self.running = False

    def quit(self):
        pass

    def update(self):
        self.all_sprites.update() # using the update method for all sprites under the group 'all_sprites'

    def draw(self): # method that is responsible for displaying everything on the screen
        self.screen.fill(BLUE)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        self.all_sprites.draw(self.screen) # draws all sprites (walls, mobs, players, etc)

        pg.display.flip() # display the images and text on screen
        
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

# makes sure you are calling Game from main.py ??
if __name__ == "__main__":
    g = Game() # instantiates game upon running the code

while g.running: # upon instantiation the game which will set self.running() to True
    g.new()

g.quit