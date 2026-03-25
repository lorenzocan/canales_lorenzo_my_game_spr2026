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
        pg.mixer.init()
        # settings up pygame screen using tuple value for width and height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.paused = False
        self.game_cooldown = Cooldown(3000)
        self.current_level = 1
        self.levels = ["LevelSelect","level1.txt","level2.txt"]
    
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

    
    def new(self):
        self.load_data(self.levels[1])

        # groups that objects in the sprite module will call on
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

            if not self.paused:
                self.update()
            self.draw()

    def events(self):
        # stuff that happens with peripherals - keyboard, mouse, camera, microphone, joystick, controller, touchscreen, stylus, trackpad
        for event in pg.event.get(): # to interate through every event
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                print("mouse input")
                print(event.pos)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    self.quit()
                if event.key == pg.K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

    def quit(self):
        if self.playing:
            self.playing = False
        self.running = False

    def update(self):
        self.all_sprites.update() # using the update method for all sprites under the group 'all_sprites'
        if len(self.all_projectiles) > 1:
            self.next_level(self.levels[self.current_level+1])
    

    def draw(self): # method that is responsible for displaying everything on the screen
        self.screen.fill(BLUE)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)

        if self.paused:
            self.draw_text("PAUSED", 100, WHITE, WIDTH/2, HEIGHT/2)

        self.all_sprites.draw(self.screen) # draws all sprites (walls, mobs, players, etc)

        pg.display.flip() # display the images and text on screen
        
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("FRAGMENT", 50, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip() # basically drawing the stuff
        self.wait_for_key()
    
    def show_pause_screen(self):
        self.draw_text("PAUSED", 100, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                    self.running = False
                if event.type == pg.KEYDOWN:
                    waiting = False


# makes sure you are calling Game from main.py
if __name__ == "__main__":
    g = Game() # instantiates game upon running the code

g.show_start_screen()

while g.running: # upon instantiation the game which will set self.running() to True
    g.new()

g.quit