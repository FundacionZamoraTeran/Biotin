#!/usr/bin/python2
import pygame
import sys
import random
import logging
from pygame.locals import *
from gi.repository import Gtk

pygame.mixer.pre_init(44100, -16, 4, 2048)
pygame.init() #comment only when using GameActivity.py

log = logging.getLogger('activity.b7')
logging.basicConfig()

class Biotin:
    running = True
    def __init__(self):
        self.actor = None
        self.clock = None

    def menu(self):
        while self.running:
            print ("BLablab!")
            #self.running = False

    def reset_clock(self):
        self.clock= pygame.time.Clock()

    def quit(self):
        self.running =False

    def loop(self):
        self.reset_clock()
        self.clock.tick(60)
        self.menu()

def main():
    biotin = Biotin()
    while biotin.running:
        biotin.loop()

if __name__ == "__main__":
    main()
