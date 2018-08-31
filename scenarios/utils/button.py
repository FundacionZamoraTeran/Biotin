import pygame
from scenarios.utils import utils

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, base_file, end_file, width, height, folder, flag=False):
        self.pos = pos
        self.base = utils.load_image(base_file, folder, -1, (width, height))
        self.end = utils.load_image(end_file, folder, -1, (width, height))

        self.base_rect = self.base.get_rect(topleft=self.pos)
        self.end_rect = self.end.get_rect(topleft=self.pos)
        self.flag = flag
    def on_press(self, screen):
        pygame.display.update(screen.blit(self.end, (self.pos[0], self.pos[1])))
        pygame.time.delay(150)
    def on_focus(self, screen):
        screen.blit(self.end, (self.pos[0], self.pos[1]))
        self.base, self.end = self.end, self.base
