import random
import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Pilori(pygame.sprite.Sprite):
    """
        Class representing the main villain
    """
    def __init__(self, screen, clock, pos, limits, velocity=30, defeated=False):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.x = pos[0]
        self.y = pos[1]
        self.limits = limits
        self.velocity = velocity
        self.defeated = defeated
        self.health = 8
        self.image = utils.load_image("pilori.png","castle/game")
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = (self.rect.x, self.rect.y)
        self.projectile = None

    def control(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if self.rect.y > 900:
            self.rect.y = 900-self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0

    def update(self):
        self.control(self.velocity, random.randint(-20, 20))
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.collision_projectile()

    def move(self):
        if self.rect.x+self.rect.width > self.limits[1]:
            self.velocity = -abs(self.velocity)
        elif self.rect.x < self.limits[0]:
            self.velocity = abs(self.velocity)
        self.update()

    def collision_projectile(self):
        if pygame.sprite.collide_rect(self, self.projectile):
            self.health -= 1
            self.projectile.throw = False
            self.projectile.rect.y = 900
