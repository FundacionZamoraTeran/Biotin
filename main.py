#!/usr/bin/python2
import sys
import logging
import pygame
#import cProfile as profile

from pygame.locals import *
from gi.repository import Gtk
from scenarios.menu import menu
from scenarios.house import outside
from scenarios.map import mapp
from scenarios.saar import entrance
from scenarios.utils import consts
from actors import player

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
    def __init__(self, screen):
        self.actor = None
        self.clock = None
        self.screen = screen
        self.running = True
        self.next_level = 0
        self.levels = {
            "0": outside.Outside,
            "1": mapp.Map,
            "2": entrance.Entrance,
            "99": player.Player
        }

    def reset_clock(self):
        self.clock = pygame.time.Clock()

    def quit(self):
        self.running = False

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
        #self.level_selector(2, "slot_2")
        #self.char_selector(99, (50, 650), "cesar")
        pygame.quit()
        sys.exit(0)

    def level_selector(self, level, slot):
        if level is not None and slot is not None:
            #here we should load against a dict the selected level
            var = self.levels[str(level)](self.screen, self.clock, slot)
            var.run()
            self.next_level = var.next_level
    def char_selector(self, level, pos, char):
        if level is not None :
            #here we should load against a dict the selected level
            var = self.levels[str(level)](self.screen, self.clock, pos, char)
            var.run()
            self.next_level = var.next_level


if __name__ == "__main__":
    SCREEN = pygame.display.set_mode(consts.RESOLUTION, 0, 32)
    pygame.display.set_caption("Biotin: Una aventura energizante")

    BIOTIN = Biotin(SCREEN)
    BIOTIN.loop()
    #profile.run('BIOTIN.loop()')
