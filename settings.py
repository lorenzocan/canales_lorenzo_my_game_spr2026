import pygame as pg

WIDTH = 800
HEIGHT= 600
TITLE = "Boss Rush" # idk it might be something I want to do later on
FPS = 60
TILESIZE = 32


# Player values
PLAYER_SPEED = 280
PLAYER_HITRECT = pg.Rect(0, 0, TILESIZE-2, TILESIZE-2)

MOB_HITRECT = pg.Rect(0, 0, TILESIZE, TILESIZE)

PROJ_HITRECT = pg.Rect(0, 0, TILESIZE-2, 12)
PROJ_SPEED = 540

# Colour
# a tuple that represents an rgb value
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)