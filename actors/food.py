import random
import pygame

from scenarios.utils import utils

class Food(pygame.sprite.Sprite):
    """
        Class representing rahapara game food
    """
    def __init__(self, screen, clock, pos, food, folder, limits, velocity=16):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.image = utils.load_image(food, folder)
        self.x = pos[0]
        self.y = pos[1]
        self.limits = limits
        self.velocity = velocity
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = pos
        self.hidden = None

    def update(self):
        if self.rect.y+self.rect.height > self.limits[1]:
            self.rect.y = self.y
        elif self.rect.y <= self.limits[0]:
            self.rect.x = random.randint(200, 1100)
        self.rect.y += self.velocity
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.is_hidden()
    def is_hidden(self):
        if self.rect.y < 0 or self.rect.y > 1200:
            self.hidden = True
        else:
            self.hidden = False
