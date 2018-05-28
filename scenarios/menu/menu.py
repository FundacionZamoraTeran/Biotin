import pygame
import scenarios.menu.help

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.menu.button  import Button
from scenarios.menu import credits


class Menu:
    """
       Class representing the start menu for the game, receives
       a Surface as screen, and a Clock as clock.
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.bg_color = consts.MENU_BG_COLOUR
        self.clock = clock
        self.logo = utils.load_image("Menu_01.png", "menu")
        self.iniciar = Button(515, 470, "Menu_04.png", "Menu_03.png", "Menu_02.png", 150, 300)
        self.continuar = Button(720, 470, "Menu_03.png", "Menu_04.png",
                                "Menu_04.png", 150, 300).flip()
        self.salir = Button(920, 490, "Menu_02.png", "Menu_04.png", "Menu_04.png", 125, 260).flip()
        self.opciones = Button(310, 470, "Menu_03.png", "Menu_04.png", "Menu_04.png", 150, 300)
        self.creditos = Button(135, 490, "Menu_02.png", "Menu_04.png", "Menu_04.png", 125, 260)
        self.ayuda = Button(975, 320, "Menu_05.png", "Menu_05.png", "Menu_05.png", 70, 70)


    def run(self):
        """
           The main loop event for the menu, run everything related to the Main menu here
        """
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.fill(self.bg_color)
            self.screen.blit(self.logo, (105, 25))
            self.screen.blit(self.creditos.base, (135, 490))
            self.screen.blit(self.opciones.base, (310, 470))
            self.screen.blit(self.iniciar.base, (515, 470))
            self.screen.blit(self.continuar.base, (720, 470))
            self.screen.blit(self.salir.base, (920, 490))
            self.screen.blit(self.ayuda.base, (975, 320))
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    # what happens after the player release the click of a button?
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle the clicks on the buttons
                    if self.iniciar.base_rect.collidepoint(mouse_x, mouse_y):
                        print("You clicked Iniciar")
                    if self.continuar.base_rect.collidepoint(mouse_x, mouse_y):
                        print("You clicked Continuar")
                    if self.salir.base_rect.collidepoint(mouse_x, mouse_y):
                        running = False
                    if self.opciones.base_rect.collidepoint(mouse_x, mouse_y):
                        print("You clicked Opciones")
                    if self.creditos.base_rect.collidepoint(mouse_x, mouse_y):
                        credit = credits.Credit(self.screen, self.clock)
                        credit.run()
                        del credit
                    if self.ayuda.base_rect.collidepoint(mouse_x, mouse_y):
                        hjelp = scenarios.menu.help.Help(self.screen, self.clock)
                        hjelp.run()
                        del hjelp

                if event.type == pygame.MOUSEMOTION:
                    # Handle the hovering on the buttons
                    if self.iniciar.base_rect.collidepoint(mouse_x, mouse_y):
                        pygame.display.update(pygame.draw.rect(self.screen, self.bg_color,
                                                               ((515, 470), (150, 300))))
                        pygame.display.update(self.screen.blit(self.iniciar.transition, (515, 470)))
                        pygame.display.update(self.screen.blit(self.iniciar.end, (515, 470)))
                        self.iniciar.base, self.iniciar.end = self.iniciar.end, self.iniciar.base

