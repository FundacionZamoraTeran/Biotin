#!/usr/bin/python2
import sys
import logging
import pygame

from pygame.locals import *
from scenarios.menu import menu
from scenarios.house import outside
from scenarios.map import mapp
from scenarios.sharqii import start
from scenarios.saar import entrance
from scenarios.rahapara import bowling
from scenarios.valley import hill
from scenarios.candy import woods
from scenarios.space import river
from scenarios.city import fall
from scenarios.castle import lab
from scenarios.luis import descend
from scenarios.epilogue import epilogue
from scenarios.utils import consts
from actors import player

pygame.mixer.pre_init(44100, -16, 4, 2048)
pygame.mixer.init()
pygame.font.init()

LOG = logging.getLogger('activity.b7')
logging.basicConfig()

class Biotin:
    """
        Main class that handle the game loop
    """
    running = True
    def __init__(self):
        self.actor = None
        self.clock = None
        self.running = True
        self.next_level = 0
        self.levels = {
            "0": outside.Outside,
            "1": mapp.Map,
            "2": entrance.Entrance,
            "3": bowling.Bowling,
            "4": start.Entrance,
            "5": hill.Hill,
            "6": woods.Wood,
            "7": river.River,
            "8": fall.Fall,
            "9": lab.Lab,
            "10": descend.Descend,
            "11": epilogue.Epilogue
        }

    def reset_clock(self):
        self.clock = pygame.time.Clock()

    def quit(self):
        self.running = False

    def run(self):
        screen = pygame.display.get_surface()
        pygame.event.set_blocked([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN])
        self.reset_clock()
        self.clock.tick(consts.FPS)
        meny = menu.Menu(screen, self.clock)
        meny.run()
        self.next_level = meny.level_selected
        slot = meny.slot_selected
        del meny
        while self.next_level is not None:
            self.level_selector(screen, self.next_level, slot)
        pygame.quit()
        sys.exit(0)

    def level_selector(self, screen, level, slot):
        if level is not None and slot is not None:
            #here we should load against a dict the selected level
            var = self.levels[str(level)](screen, self.clock, slot)
            var.run()
            self.next_level = var.next_level
