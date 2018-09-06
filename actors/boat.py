import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Boat(pygame.sprite.Sprite):
    """
        Class representing the boat in space
    """
    def __init__(self, screen, clock, pos, character, physics=(28, 250, 1.2)):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.character = character
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.velocity = physics[0]
        self.gravity = physics[2]

        self.sprites = {
            "left": [utils.load_image("left1.png", self.character),
                     utils.load_image("left2.png", self.character),
                     utils.load_image("left3.png", self.character)],
            "right": [utils.load_image("right1.png", self.character),
                      utils.load_image("right2.png", self.character),
                      utils.load_image("right3.png", self.character)],
        }
        self.direction = "stand"
        self.rect = pygame.Rect(pos, self.sprites["left"][0].get_size())
        self.rect.topleft = (self.x, self.rect.y)

    def control(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > consts.WIDTH_SCREEN:
            self.rect.x = consts.WIDTH_SCREEN-self.rect.width

        if self.rect.y > 900:
            self.rect.y = 900-self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0

    def update(self):
        if self.direction == "right" or self.direction == "left":
            self.control(self.velocity, 0)
            self.frame += 1
            if self.frame > 5:
                self.frame = 0
            self.screen.blit(self.sprites[self.direction][(self.frame//2)], (self.rect.x, self.rect.y))
        elif self.direction == "stand":
            if self.velocity > 0:
                direction = "right"
            else:
                direction = "left"
            self.screen.blit(self.sprites[direction][0], (self.rect.x, self.rect.y))
    def update_sprites(self):
        for i in range(0, 3):
            self.sprites["left"][i] = utils.load_image("left"+str(i+1)+".png", self.character)
            self.sprites["right"][i] = utils.load_image("right"+str(i+1)+".png", self.character)
