import os
from pygame.locals import *
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

# General constants

FPS = 60
WIDTH_SCREEN = 1200
HEIGHT_SCREEN = 900
RESOLUTION = (WIDTH_SCREEN, HEIGHT_SCREEN)

# Save values

SAVEFILE = "../../saves.json"
MAX_SAVES = "3"

# Movement values

INCREASE_BY_X = 15
INCREASE_BY_Y = 15
SHIFT_SPEED = 10
LEFT = -1
RIGHT = 1
UP = -1
DOWN = 1
CLOCKWISE = -1
COUNTERCLOCKWISE = 1

# Keybindings

KEYS_HELP = [K_F1, K_LALT, K_RALT]
KEYS_EXIT = [K_ESCAPE]
KEYS_DELETE = [K_BACKSPACE]
KEYS_SELECT = [K_RETURN, K_e]
KEYS_CTRL = [K_LCTRL]
KEYS_UP = [K_UP, K_w]
KEYS_DOWN = [K_DOWN, K_s]
KEYS_LEFT = [K_LEFT, K_a]
KEYS_RIGHT = [K_RIGHT, K_d]

# Colours
MENU_BG_COLOUR = (72, 27, 132)
MENU_BT_COLOUR = (97, 206, 245)

# Mixer Values
vol_list = ()
path = os.path.join(MAIN_DIR, "../../config.ini")
with open(path, "r+") as f:
    from ast import literal_eval
    vol_list = literal_eval(f.read()) # tuple (vx,bg,fx)
VX_VOLUME = vol_list[0]
BG_VOLUME = vol_list[1]
FX_VOLUME = vol_list[2]

# Actors values

BLOCKED = "BLOCKED"
IDLE = "IDLE"
RUNNING = "RUNNING"
START_JUMP = "START_JUMP"
JUMPING = "JUMPING"
FALLING = "FALLING"
HANGING = "HANGING"
