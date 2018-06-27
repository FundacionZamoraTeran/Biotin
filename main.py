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
        self.levels = {
            "0": menu.Menu #actually is comics
        }

    def reset_clock(self):
        self.clock = pygame.time.Clock()

    def quit(self):
        self.running =False

    def loop(self):
        self.reset_clock()
        self.clock.tick(consts.FPS)
        meny = menu.Menu(self.screen , self.clock)
        meny.run()
        level = meny.level_selected
        slot = meny.slot_selected
        del meny
        if level is not None and slot is not None:
            pass
            #here we should load against a dict the selected level
            #var = self.levels[str(level)](self.screen, self.clock, slot)
            #var.run()
        pygame.quit()
        sys.exit(0)

    def level_selector(self, level, slot):
        if level is not None and slot is not None:
            pass
            #here we should load against a dict the selected level
            #var = self.levels[str(level)](self.screen, self.clock, slot)
            #var.run()


if __name__ == "__main__":
    SCREEN = pygame.display.set_mode(consts.RESOLUTION,0,32)
    pygame.display.set_caption("Biotin: Una aventura energizante")

    BIOTIN = Biotin(SCREEN)
    BIOTIN.loop()
    #profile.run('BIOTIN.loop()')
