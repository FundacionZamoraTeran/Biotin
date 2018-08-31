import sys
import pygame
from scenarios.utils import utils, consts
from scenarios.menu.button import Button

class Help:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((1200, 900),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.background = utils.load_image("help/background.png", "menu")
        self.title = utils.load_image("help/title.png", "menu")
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
            for event in [pygame.event.wait()] + pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_PAGEUP:
                        running = False
                    elif  event.key == pygame.K_RETURN or event.key == pygame.K_END:
                        running = False

            self.screen2.blit(self.background, (0, 0))
            self.screen2.blit(self.title, (520, 160))
            self.screen.blit(self.screen2, (0, 0))
            self.screen.blit(self.exit_button.base, (1030, 120))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
