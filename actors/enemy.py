import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Enemy(pygame.sprite.Sprite):
    """
        Class representing an enemy character
    """
    def __init__(self, screen, clock, pos, character, limits, velocity=20, s_vel=50, defeated=False):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.character = character
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.limits = limits
        self.velocity = velocity
        self.defeated = defeated
        self.squashing = False
        self.squash_vel = s_vel

        self.sprites = {
            "lsquash": (utils.load_image("lsquash1.png", self.character),
                     utils.load_image("lsquash2.png", self.character),
                     utils.load_image("lsquash3.png", self.character)),
            "rsquash": (utils.load_image("rsquash1.png", self.character),
                     utils.load_image("rsquash2.png", self.character),
                     utils.load_image("rsquash3.png", self.character)),
            "left": (utils.load_image("left1.png", self.character),
                     utils.load_image("left2.png", self.character),
                     utils.load_image("left3.png", self.character)),
            "right": (utils.load_image("right1.png", self.character),
                      utils.load_image("right2.png", self.character),
                      utils.load_image("right3.png", self.character))
        }
        self.direction = "left"
        self.rect = pygame.Rect(pos, self.sprites["left"][0].get_size())
        self.rect.topleft = (self.rect.x, self.rect.y)

    def control(self, x, y):
        self.x += x
        self.y += y

        if self.y > 900:
            self.y = 900-self.rect.height
        elif self.y < 0:
            self.y = 0

    def update(self, rel_x):
        if self.squashing and not self.defeated:
            if self.direction == "left":
                self.direction = "lsquash"
            else:
                self.direction = "rsquash"
            if self.frame > 5:
                self.frame = 0
                self.defeated = True
                self.squashing = False
                self.kill()
            self.screen.blit(self.sprites[self.direction][(self.frame//2)],
                             (self.x - rel_x, self.y))
            self.y += self.squash_vel
            self.rect.topleft = (self.x-rel_x, self.y)
        else:
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

    def roam(self, rel_x):
        if self.x+self.rect.width > self.limits[1]:
            self.direction = "left"
            self.velocity = -abs(self.velocity)
        elif self.x < self.limits[0]:
            self.direction = "right"
            self.velocity = abs(self.velocity)
        self.update(rel_x)
