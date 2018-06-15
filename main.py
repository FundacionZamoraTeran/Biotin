#!/usr/bin/python2
import sys
import logging
import pygame
#import cProfile as profile

from pygame.locals import *
from gi.repository import Gtk
from scenarios.menu import menu

from scenarios.utils import consts

pygame.mixer.pre_init(44100, -16, 4, 2048)
pygame.init() #comment only when using GameActivity.py

LOG = logging.getLogger('activity.b7')
logging.basicConfig()

class Biotin:
    """
        Main class that handle the game loop
    """
    running = True
    def __init__(self,screen):
        self.actor = None
        self.clock = None
        self.screen = screen
        self.running = True

    def reset_clock(self):
        self.clock = pygame.time.Clock()

    def quit(self):
        self.running =False

    def loop(self):
        self.reset_clock()
        self.clock.tick(consts.FPS)
        meny = menu.Menu(self.screen , self.clock)
        meny.run()
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    SCREEN = pygame.display.set_mode(consts.RESOLUTION,0,32)
    pygame.display.set_caption("Biotin: Una aventura energizante")
    BIOTIN = Biotin(SCREEN)
    BIOTIN.loop()
    #profile.run('BIOTIN.loop()')
