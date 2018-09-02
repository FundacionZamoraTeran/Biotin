import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Npc(pygame.sprite.Sprite):
    """
        Class representing an npc character
    """
    def __init__(self, screen, clock, pos, character, limits, velocity=20):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.character = character
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.limits = limits
        self.velocity = velocity

        self.sprites = {
            "down": utils.load_image("down1.png", self.character),
            "left": (utils.load_image("left1.png", self.character),
                     utils.load_image("left2.png", self.character),
                     utils.load_image("left3.png", self.character)),
            "right": (utils.load_image("right1.png", self.character),
                      utils.load_image("right2.png", self.character),
                      utils.load_image("right3.png", self.character))
        }

        self.direction = "stand"
        self.rect = pygame.Rect(pos, self.sprites["down"].get_size())
        self.rect.topleft = (self.rect.x, self.rect.y)

    def control(self, x, y):
        self.x += x
        self.y += y

        if self.y > 900:
            self.y = 900-self.rect.height
        elif self.y < 0:
            self.y = 0

    def update(self, rel_x):
        if self.direction == "right" or self.direction == "left":
            self.control(self.velocity, 0)
            self.frame += 1
            if self.frame > 5:
                self.frame = 0
            self.screen.blit(self.sprites[self.direction][(self.frame//2)],
                             (self.x - rel_x, self.y))
        else:
            self.screen.blit(self.sprites["left"][0],
                             (self.x, self.y))
        self.rect.topleft = (self.x-rel_x, self.y)

    def patrol(self, rel_x):
        if self.x+self.rect.width > self.limits[1]:
            self.direction = "left"
            self.velocity = -abs(self.velocity)
        elif self.x < self.limits[0]:
            self.direction = "right"
            self.velocity = abs(self.velocity)
        self.update(rel_x)
