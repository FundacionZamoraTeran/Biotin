import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Bowl(pygame.sprite.Sprite):
    """
        Class representing the playable bowl in
        rahapara village
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

        self.sprites = {
            "left": (utils.load_image("left1.png", self.character),
                     utils.load_image("left2.png", self.character),
                     utils.load_image("left3.png", self.character)),
            "right": (utils.load_image("right1.png", self.character),
                      utils.load_image("right2.png", self.character),
                      utils.load_image("right3.png", self.character)),
            "fleft": (utils.load_image("fleft1.png", self.character),
                      utils.load_image("fleft2.png", self.character),
                      utils.load_image("fleft3.png", self.character)),
            "fright": (utils.load_image("fright1.png", self.character),
                       utils.load_image("fright2.png", self.character),
                       utils.load_image("fright3.png", self.character))
        }
        self.direction = "stand"
        self.rect = pygame.Rect(pos, self.sprites["left"][0].get_size())
        self.rect.topleft = (self.x, self.rect.y)
        self.foods = []

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
            self.screen.blit(self.sprites["left"][0], (self.rect.x, self.rect.y))

    def collision_enemy(self): #use this if you dont scroll the background
        for block in self.foods:
            if self.rect.colliderect(block.rect):
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.velocity > 0:
                    self.rect.right = block.rect.left
                    self.real_x = self.rect.x
                elif self.velocity < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                    self.real_x = self.rect.x
