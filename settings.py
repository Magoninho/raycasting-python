import math


TILESIZE = 32
ROWS = 10
COLS = 10

WINDOW_WIDTH = ROWS * TILESIZE
WINDOW_HEIGHT = COLS * TILESIZE

FOV = 60 * (math.pi / 180)

RES = 4
NUM_RAYS = WINDOW_WIDTH / RES