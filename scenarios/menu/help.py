import pygame
from scenarios.utils import utils

class Help:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((900, 600), flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.tutorial = utils.load_image("help.png", "menu")
    def run(self):
        """ control the actions happening on the Help modal"""
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            self.screen2.fill((250, 207, 149, 220))
            self.screen2.blit(self.tutorial, (50, 0))
            self.screen.blit(self.screen2, (150, 150))
            pygame.display.flip()
            self.clock.tick(30)
