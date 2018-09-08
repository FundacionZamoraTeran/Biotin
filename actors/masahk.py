import random
import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Masakh(pygame.sprite.Sprite):
    """
        Class representing the main villain monster form
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
        self.health = 18
        self.monster = (
            utils.load_image("monster2.png","luis/game"),
            utils.load_image("monster1.png","luis/game")
        )
        self.image = utils.load_image("monster2.png","luis/game")
        self.rect = pygame.Rect(pos, self.image.get_size())
        self.rect.topleft = (self.rect.x, self.rect.y)
        self.mouth_open = False
        self.jumping = False
        self.jump_distance = 350
        self.jump_frames = 0
        self.projectile = None
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)

    def control(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if self.rect.y > 900:
            self.rect.y = 900-self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0

    def update(self):
        self.jump()
        if self.mouth_open:
            self.screen.blit(self.monster[1], (self.rect.x, self.rect.y))
        else:
            self.screen.blit(self.monster[0], (self.rect.x, self.rect.y))
        self.collision_projectile()

    def jump(self):
        if self.jumping is True:
            self.jump_frames += abs(self.velocity)
            self.rect.y -= abs(self.velocity)
            if self.jump_frames >= self.jump_distance:
                self.jumping = False
        elif self.jumping is False and self.jump_frames > 0:
            self.jump_frames -= abs(self.velocity)
            self.rect.y += abs(self.velocity)
        else:
            self.jump_frames = 0

    def collision_projectile(self):
        if pygame.sprite.collide_rect(self, self.projectile) and self.mouth_open:
            self.health -= 1
            self.projectile.throw = False
            self.projectile.rect.x = 140
            self.vx_channel.play(utils.load_fx("goodthrow.ogg"))
        elif pygame.sprite.collide_rect(self, self.projectile) and not self.mouth_open:
            self.vx_channel.play(utils.load_fx("badthrow.ogg"))
