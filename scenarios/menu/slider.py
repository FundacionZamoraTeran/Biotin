import pygame
from scenarios.utils import utils

class Slider(pygame.sprite.Sprite):
    """
       Acts as a slider constructor, expects:
       pos => a tuple with the X & Y positions,
       pos_title => the X & Y positions for title,
       title => a tuple with both files for title states
       folder => the base directory where the images are,
       width => the width the slider should be
       height => the height the slider should be
       level => the level the slider should be initialised
    """
    def __init__(self, pos, pos_title, title, folder, width=624, height=61, level=1.0, flag=False):
        # pygame Sprite class constructor
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos

        self.pos_title = pos_title

        # set the states images
        self.unfocused_title = utils.load_image(title[0], folder, -1)

        self.focused_title = utils.load_image(title[1], folder, -1)

        self.zero = utils.load_image("0.0.png",
                                     folder,
                                     -1,
                                     (width, height))
        self.ten = utils.load_image("0.1.png",
                                    folder,
                                    -1,
                                    (width, height))
        self.twenty = utils.load_image("0.2.png",
                                       folder,
                                       -1,
                                       (width, height))
        self.thirty = utils.load_image("0.3.png",
                                       folder,
                                       -1,
                                       (width, height))
        self.forty = utils.load_image("0.4.png",
                                      folder,
                                      -1,
                                      (width, height))
        self.fifty = utils.load_image("0.5.png",
                                      folder,
                                      -1,
                                      (width, height))
        self.sixty = utils.load_image("0.6.png",
                                      folder,
                                      -1,
                                      (width, height))
        self.seventy = utils.load_image("0.7.png",
                                        folder,
                                        -1,
                                        (width, height))
        self.eighty = utils.load_image("0.8.png",
                                       folder,
                                       -1,
                                       (width, height))
        self.ninety = utils.load_image("0.9.png",
                                       folder,
                                       -1,
                                       (width, height))
        self.hundred = utils.load_image("1.0.png",
                                        folder,
                                        -1,
                                        (width, height))
        self.repo = {"0.0": self.zero,
                     "0.1": self.ten,
                     "0.2": self.twenty,
                     "0.3": self.thirty,
                     "0.4": self.forty,
                     "0.5": self.fifty,
                     "0.6": self.sixty,
                     "0.7": self.seventy,
                     "0.8": self.eighty,
                     "0.9": self.ninety,
                     "1.0": self.hundred}

        # define the rects for all the sprite's states
        self.unfocused_title_rect = self.unfocused_title.get_rect(
            topleft=self.pos_title)
        self.focused_title_rect = self.focused_title.get_rect(
            topleft=self.pos_title)
        self.zero_rect = self.zero.get_rect(topleft=self.pos)
        self.ten_rect = self.ten.get_rect(topleft=self.pos)
        self.twenty_rect = self.twenty.get_rect(topleft=self.pos)
        self.thirty_rect = self.thirty.get_rect(topleft=self.pos)
        self.forty_rect = self.forty.get_rect(topleft=self.pos)
        self.fifty_rect = self.fifty.get_rect(topleft=self.pos)
        self.sixty_rect = self.sixty.get_rect(topleft=self.pos)
        self.seventy_rect = self.seventy.get_rect(topleft=self.pos)
        self.eighty_rect = self.eighty.get_rect(topleft=self.pos)
        self.ninety_rect = self.ninety.get_rect(topleft=self.pos)
        self.hundred_rect = self.hundred.get_rect(topleft=self.pos)

        self.flag = flag
        self.level = level


    def get_current_level_image(self):
        return self.repo[str(self.level)]

    def increase_level(self, screen):
        if self.level != 1.0:
            self.level += 0.1
            self.level = round(self.level, 1)
            screen.blit(self.repo[str(self.level)], self.pos)
    def decrease_level(self, screen):
        if self.level != 0.0:
            self.level -= 0.1
            self.level = round(self.level, 1)
            screen.blit(self.repo[str(self.level)], self.pos)
    def on_title_focus(self, screen):
        screen.blit(self.focused_title, self.pos_title)
    def no_title_ocus(self, screen):
        screen.blit(self.unfocused_title, self.pos_title)
