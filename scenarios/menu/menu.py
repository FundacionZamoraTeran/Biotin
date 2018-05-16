import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Menu():
    """
       Class representing the start menu for the game, receives
       a Surface as screen, and a Clock as clock.
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.bg_color = consts.MENU_BG_COLOUR
        self.clock = clock
        self.logo = utils.load_image("Menu_01.png", "menu")
        self.iniciar = utils.load_image("Menu_04.png", "menu",
                                        -1, (150, 300)) #should be a class
        self.continuar = pygame.transform.flip(utils.load_image("Menu_03.png",
                                                                "menu", -1, (150, 300)), 180, 0)
        self.salir = pygame.transform.flip(utils.load_image("Menu_02.png",
                                                            "menu", -1, (125, 260)), 180, 0)
        self.opciones = utils.load_image("Menu_03.png", "menu", -1, (150, 300))
        self.creditos = utils.load_image("Menu_02.png", "menu", -1, (125, 260))
        self.ayuda = utils.load_image("Menu_05.png", "menu")


    def run(self):
        """
           The main loop event for the menu, run everything related to the Main menu here
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill(self.bg_color)
            self.screen.blit(self.logo, (105, 25))
            self.screen.blit(self.creditos, (135, 490))
            self.screen.blit(self.opciones, (310, 470))
            self.screen.blit(self.iniciar, (515, 470))
            self.screen.blit(self.continuar, (720, 470))
            self.screen.blit(self.salir, (920, 490))
            pygame.display.flip()
            self.clock.tick(30)
