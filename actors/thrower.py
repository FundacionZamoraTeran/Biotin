import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Thrower(pygame.sprite.Sprite):
    """
        Class representing the player in the castle lab
        game
    """
    def __init__(self, screen, clock, pos, velocity=28):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.character = "bowl"
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.velocity = velocity
        self.image = utils.load_image("team.png","castle/game")
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = (self.x, self.rect.y)
        self.direction = "stand"
        self.collided = []
        self.score = 0

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
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        elif self.direction == "stand":
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
