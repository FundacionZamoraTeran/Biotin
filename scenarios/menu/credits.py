import sys
import pygame
from scenarios.utils import utils
from scenarios.menu.button import Button

class Credit:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((1200, 900),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.exit_button = Button(1030,
                                  140,
                                  "exit.png",
                                  "exit.png",
                                  "exit.png",
                                  36,
                                  38)

        # Logos

        self.background = utils.load_image("credits_door/background.png", "menu")
        self.title = utils.load_image("credits_door/title.png", "menu")
        self.logos = utils.load_image("credits_door/logos.png", "menu")
        self.team = utils.load_image("credits_door/team.png", "menu")

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
                    print(pygame.key.get_pressed())
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif  event.key == pygame.K_RETURN:
                        running = False

            # set all the elements to appear on the credit's modal

            self.screen2.blit(self.background, (0, 0))
            self.screen2.blit(self.title, (465, 160))
            self.screen2.blit(self.logos, (275, 270))
            self.screen2.blit(self.team, (215, 460))

            # make everything appear on the screen

            self.screen.blit(self.screen2, (0, 0))
            self.screen.blit(self.exit_button.base, (1030, 120))
            pygame.display.flip()
            self.clock.tick(30)
