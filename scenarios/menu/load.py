import sys
import os
import pygame
import json
from scenarios.utils import utils
from scenarios.menu.button import Button
from scenarios.menu.slider import Slider

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

class Load:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((1200, 900),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.background = utils.load_image("load_door/background.png", "menu")
        self.title = utils.load_image("load_door/title.png", "menu")
        self.slot1 = utils.load_image("load_door/slot2.png", "menu")
        self.team = utils.load_image("load_door/e&c.png", "menu")
        self.slot2 = utils.load_image("load_door/slot1.png", "menu")
        self.team2 = utils.load_image("load_door/e&c.png", "menu")
        self.slot3 = utils.load_image("load_door/slot1.png", "menu")
        self.team3 = utils.load_image("load_door/e&c.png", "menu")


        self.exit_button = Button(1030,
                                  120,
                                  "exit.png",
                                  "exit.png",
                                  "exit.png",
                                  36,
                                  38)
    def load(self):
        pass

    def run(self):
        """ control the actions happening on the Help modal"""
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.base_rect.collidepoint(mouse_x, mouse_y):
                        running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_DOWN:
                        pass
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_RIGHT:
                        pass
                    elif event.key == pygame.K_LEFT:
                        pass


            self.screen2.blit(self.background, (0, 0))
            self.screen2.blit(self.title, (340, 190))
            self.screen2.blit(self.slot1, (200, 310))
            self.screen2.blit(self.team, (280,315))
            self.screen2.blit(self.slot2, (225, 480))
            self.screen2.blit(self.team, (280,465))
            self.screen2.blit(self.slot3, (225, 630))
            self.screen2.blit(self.team, (280,615))
            self.screen.blit(self.screen2, (0, 0))
            self.screen.blit(self.exit_button.base, (1030, 120))
            pygame.display.flip()
            self.clock.tick(30)
