import pygame
from scenarios.utils import utils

class Prompt(pygame.sprite.Sprite):
    """
        Class representing the interaction prompt
    """
    def __init__(self, screen, clock, pos, prompt, folder, limits):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.image = utils.load_image(prompt, folder)
        self.x = pos[0]
        self.y = pos[1]
        self.limits = limits
        self.velocity = 10
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = pos

    def float(self, rel_x):
        if self.y+self.rect.height > self.limits[1]:
            self.velocity = -abs(self.velocity)
        elif self.y < self.limits[0]:
            self.velocity = abs(self.velocity)
        self.y += self.velocity
        self.screen.blit(self.image, (self.x - rel_x, self.y))
