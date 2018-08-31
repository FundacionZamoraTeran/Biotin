import pygame
from scenarios.utils import utils

class Slider(pygame.sprite.Sprite):
    """
       Acts as a slider constructor, expects:
       pos => a tuple with the X & Y positions,
       folder => the base directory where the images are,
       width => the width the slider should be
       height => the height the slider should be
       level => the level the slider should be initialised
    """
    def __init__(self, pos, folder, width=320, height=40, level=4):
        # pygame Sprite class constructor
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        # set the states images

        self.quarter = utils.load_image("1.png",
                                        folder,
                                        -1,
                                        (width, height))
        self.half = utils.load_image("2.png",
                                     folder,
                                     -1,
                                     (width, height))
        self.almost = utils.load_image("3.png",
                                       folder,
                                       -1,
                                       (width, height))
        self.full = utils.load_image("4.png",
                                     folder,
                                     -1,
                                     (width, height))

        self.repo = {"1": self.quarter,
                     "2": self.half,
                     "3": self.almost,
                     "4": self.full}

        # define the rects for all the sprite's states
        self.quarter_rect = self.quarter.get_rect(topleft=self.pos)
        self.half_rect = self.half.get_rect(topleft=self.pos)
        self.almost_rect = self.almost.get_rect(topleft=self.pos)
        self.full_rect = self.full.get_rect(topleft=self.pos)
        self.level = level


    def get_current_level_image(self):
        return self.repo[str(self.level)]

    def increase_level(self, screen, amount):
        if self.level != 4:
            self.level += amount
            if self.level > 4: self.level = 4
            screen.blit(self.repo[str(self.level)], self.pos)

    def decrease_level(self, screen, amount):
        if self.level != 1:
            self.level -= amount
            if self.level < 1: self.level = 1
            screen.blit(self.repo[str(self.level)], self.pos)
