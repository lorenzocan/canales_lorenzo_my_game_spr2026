import pygame as pg
from settings import *

class Map:
    def __init__(self, filename):
        # creating data for building the map using a list
        self.data = []

        # open a specific file and close it with 'with'
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip()) # people often add extra spaces - strip method makes sure to remove excess spaces at the start and end

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE


class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert() # gets spritesheet file on initialisation

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height)) 
        image.blit(self.spritesheet, (0,0), (x,y, width, height)) # basicaly draws the image
        new_image = pg.transform.scale(image, (width, height))
        image = new_image
        return image

# this class creates a countdown timer for a cooldown
class Cooldown:
    def __init__(self, time):
        self.start_time = 0
        # allows us to set property for time until cooldown
        self.time = time # coolodown time
    def start(self):
        self.start_time = pg.time.get_ticks() # "resets" the timer relative to the number of ticks when this was called
    def ready(self):
        current_time = pg.time.get_ticks() # time when this method has been called

        # checking if the difference between the time that has passed and the time when started is greater than the cooldown time
        if current_time - self.start_time >= self.time:
            return True
        return False

# def draw_health_bar(surf, x, y, pct):
#     if pct < 0:
#         pct = 0
#     BAR_LENGTH = 100
#     BAR_HEIGHT = 10
#     fill = (pct/100) * BAR_LENGTH
#     outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
#     fill_height = pg.Rect(x, y, fill, BAR_HEIGHT)
#     pg.draw.rect(surf, RED, fill_rect)
#     pg.draw.rect(surf, WHITE, outline_rect, 2)
