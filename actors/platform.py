import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Platform(pygame.sprite.Sprite):
    """
        Class representing a platform
    """
    def __init__(self, screen, clock, pos, platform, folder):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.image = utils.load_image(platform, folder)
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = pos

    # might expand
