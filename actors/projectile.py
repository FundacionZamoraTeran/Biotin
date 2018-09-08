import random
import pygame

from scenarios.utils import utils

class Projectile(pygame.sprite.Sprite):
    """
        Class representing a food projectile
    """
    def __init__(self, screen, clock, pos, food, folder, velocity=36):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.image = utils.load_image(food, folder)
        self.x = pos[0]
        self.y = pos[1]
        self.velocity = velocity
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = pos
        self.throw = False
        self.player = None
        self.food = []
        for i in range(1, 17):
            self.food.append(utils.load_image(str(i)+".png", folder))

    def update(self):
        if self.rect.y+self.rect.height > 900:
            self.rect.y = self.y
        elif self.rect.y <= 0:
            self.rect.y = self.y
            self.throw = False
        if self.throw:
            self.rect.y -= self.velocity
        self.screen.blit(random.choice(self.food), (self.rect.x, self.rect.y))
