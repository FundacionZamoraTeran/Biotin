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
        self.iniciar = Button(515, 470, "Menu_04.png", "Menu_03.png", "Menu_02.png", 150, 300)
        self.continuar = Button(720, 470, "Menu_03.png", "Menu_04.png", "Menu_04.png", 150, 300).flip()
        self.salir = Button(920, 490, "Menu_02.png", "Menu_04.png", "Menu_04.png", 125, 260).flip()
        self.opciones = Button(310, 470, "Menu_03.png", "Menu_04.png", "Menu_04.png", 150, 300)
        self.creditos = Button(135, 490, "Menu_02.png", "Menu_04.png", "Menu_04.png", 125, 260)
        self.ayuda = Button(920, 270, "Menu_05.png", "Menu_05.png", "Menu_05.png", 70, 70)


    def run(self):
        """
           The main loop event for the menu, run everything related to the Main menu here
        """
        running = True
        while running:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    # what happens after the player release the click of a button?
                    pass
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # what happens when the player click a button?
                    pass
                if event.type == pygame.MOUSEMOTION:
                    # when the player hovers a button what to do?
                    if self.iniciar.base_rect.collidepoint(mouse_x,mouse_y): # should expect the transition and/or the final point as well
                        pygame.display.update(pygame.draw.rect(self.screen, self.bg_color, ((515,470),(150,300))))
                        pygame.display.update(self.screen.blit(self.iniciar.transition, (515, 470)))
                        pygame.display.update(self.screen.blit(self.iniciar.end, (515, 470)))
                        self.iniciar.base, self.iniciar.end = self.iniciar.end, self.iniciar.base


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




class Button(pygame.sprite.Sprite):
    """
       Acts as a button constructor, expects:
       x => X position,
       y => Y position,
       base_file => the base image the button will display
       transition_file => transition between states image
       end_file => final state image,
       width => the width the button should be
       height => the height the button should be
       folder => the folder where the images are in
    """
    def __init__(self, x,y, base_file, transition_file, end_file , width=100, height=100, folder = "menu"):
        #pygame Sprite class constructor
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.pos = (x,y)

        #set the states images
        self.base = utils.load_image(base_file, folder, -1, (width, height))
        self.transition = utils.load_image(transition_file, folder, -1, (width, height))
        self.end = utils.load_image(end_file, folder, -1, (width, height))

        #define the rects for all the sprite's states, _rect.x and _rect.y set the position of the objects
        self.base_rect = self.base.get_rect(topleft=self.pos)
        self.transition_rect = self.transition.get_rect(topleft=self.pos)
        self.end_rect = self.end.get_rect(topleft=self.pos)

    def update(self):
        pass

    def flip(self):
        self.base = pygame.transform.flip(self.base, 180, 0)
        self.transition = pygame.transform.flip(self.transition, 180, 0)
        self.end = pygame.transform.flip(self.end, 180, 0)
        return self
