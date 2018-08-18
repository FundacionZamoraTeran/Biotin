#!/usr/bin/python2
import sys
import logging
import pygame
#import cProfile as profile

from pygame.locals import *
from gi.repository import Gtk
from scenarios.menu import menu
from scenarios.house import outside
from scenarios.utils import consts

pygame.mixer.pre_init(44100, -16, 4, 2048)
pygame.mixer.init()
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
        self.next_level = 0
        self.levels = {
            "0": outside.Outside
            #"1": map.Map
        }

    def reset_clock(self):
        self.clock = pygame.time.Clock()

    def quit(self):
        self.running =False

    def loop(self):
        self.reset_clock()
        self.clock.tick(consts.FPS)
        meny = menu.Menu(self.screen, self.clock)
        meny.run()
        self.next_level = meny.level_selected
        slot = meny.slot_selected
        del meny
        while self.next_level is not None:
            self.level_selector(self.next_level, slot)
        #self.level_selector(0, "slot_2")
        pygame.quit()
        sys.exit(0)

    def level_selector(self, level, slot):
        if level is not None and slot is not None:
            #here we should load against a dict the selected level
            var = self.levels[str(level)](self.screen, self.clock, slot)
            var.run()
            self.next_level = var.next_level


if __name__ == "__main__":
    SCREEN = pygame.display.set_mode(consts.RESOLUTION, 0, 32)
    pygame.display.set_caption("Biotin: Una aventura energizante")

    BIOTIN = Biotin(SCREEN)
    BIOTIN.loop()
    #profile.run('BIOTIN.loop()')
