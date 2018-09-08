import random
import pygame

from scenarios.utils import utils

class Vitamin(pygame.sprite.Sprite):
    """
        Class representing a vitamin projectile
    """
    def __init__(self, screen, clock, pos, vitamin, folder, velocity=36):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.image = utils.load_image(vitamin, folder)
        self.x = pos[0]
        self.y = pos[1]
        self.velocity = velocity
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = pos
        self.throw = False
        self.player = None
        self.vitamin = []
        for i in range(1, 13):
            self.vitamin.append(utils.load_image("v"+str(i)+".png", folder))
        self.choice = random.choice(self.vitamin)

    def update(self):
        if self.rect.x >= 900:
            self.rect.x = self.x
            self.rect.y = self.y
            self.choice = random.choice(self.vitamin)
            self.throw = False
        if self.throw:
            self.rect.x += self.velocity
            self.screen.blit(self.choice, (self.rect.x, self.rect.y))
