import os
import pygame

from pygame.locals import *

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

IMG_DIR = "../../assets/images"
FONTS_DIR = "../../assets/fonts"
FX_DIR = "../../assets/sounds/fx"
VX_DIR = "../../assets/sounds/vx"
BG_DIR = "../../assets/sounds/bg"
DATA_DIR = "../../assets/data"

def load_image(file, path=None, colorkey=-1, size=None):
    """
    Load image, convert its pixel format to match
    the display's and set colorkey to be optimised
    for non accelerated displays.
    """
    filedir = IMG_DIR
    if path != None:
        filedir = IMG_DIR + '/' + path
        file = os.path.join(MAIN_DIR, filedir, file)
        surface = pygame.image.load(file).convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = surface.get_at((0, 0))
            surface.set_colorkey(colorkey, RLEACCEL)
    if size != None:
        surface = pygame.transform.scale(surface, size)
    return surface

def load_images(*files):
    """
    get multiple images whilst applying the
    same changes on load_image()
    """
    images = []
    for file in files:
        images.append(load_image(file))
    return images

def load_font(name, size):
    file = os.path.join(MAIN_DIR, FONTS_DIR, name)
    return pygame.font.Font(file, size)

def open_data(name, mode):
    return open_file(DATA_DIR + "/" + name, mode)

def open_file(name, mode):
    filename = os.path.join(MAIN_DIR, name)
    return open(filename, mode)

def load_fx(name):
    filename = os.path.join(MAIN_DIR, FX_DIR, name)
    return pygame.mixer.Sound(filename)

def load_vx(name):
    filename = os.path.join(MAIN_DIR, VX_DIR, name)
    return pygame.mixer.Sound(filename)

def load_bg(name):
    filename = os.path.join(MAIN_DIR, BG_DIR, name)
    return pygame.mixer.music.load(filename)
def loading_screen(screen):
    pygame.display.update(screen.blit(load_image("loading.png", ""), (0, 0)))
