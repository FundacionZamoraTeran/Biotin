import json
import sys
import pygame
from scenarios.utils import utils
from scenarios.menu.button import Button

class Option:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((1200, 900),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.background = utils.load_image("options_door/background.png", "menu")
        self.title = utils.load_image("options_door/title.png", "menu")
        self.voice_title = Button(210,
                                  350,
                                  "options_door/vt1.png",
                                  "options_door/vt2.png",
                                  None,
                                  157,
                                  73)
        self.voice_slider = utils.load_image("options_door/1.0.png", "menu")
        self.music_title = Button(210,
                                  480,
                                  "options_door/mt1.png",
                                  "options_door/mt2.png",
                                  None,
                                  157,
                                  73)
        self.music_slider = utils.load_image("options_door/0.4.png", "menu")
        self.fx_title = Button(180,
                               610,
                               "options_door/ft1.png",
                               "options_door/ft2.png",
                               None,
                               181,
                               73)
        self.fx_slider = utils.load_image("options_door/0.8.png", "menu")
        self.exit_button = Button(1030,
                                  120,
                                  "exit.png",
                                  "exit.png",
                                  "exit.png",
                                  36,
                                  38)

    def run(self):
        """ control the actions happening on the Help modal"""
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEMOTION:
                    self.voice_title.on_selection_altern(self.screen, mouse_x, mouse_y)
                    # Load Button
                    self.music_title.on_selection_altern(self.screen, mouse_x, mouse_y)
                    # Exit Button
                    self.fx_title.on_selection_altern(self.screen, mouse_x, mouse_y)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.base_rect.collidepoint(mouse_x, mouse_y):
                        running = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.get_pressed())
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif  event.key == pygame.K_RETURN:
                        running = False

            self.screen2.blit(self.background, (0, 0))
            self.screen2.blit(self.title, (460, 190))
            self.screen2.blit(self.voice_title.base, (210, 350))
            self.screen2.blit(self.voice_slider, (380, 350))
            self.screen2.blit(self.music_title.base, (210, 480))
            self.screen2.blit(self.music_slider, (380, 480))
            self.screen2.blit(self.fx_title.base, (180, 610))
            self.screen2.blit(self.fx_slider, (380, 610))
            self.screen.blit(self.screen2, (0, 0))
            self.screen.blit(self.exit_button.base, (1030, 120))
            pygame.display.flip()
            self.clock.tick(30)
