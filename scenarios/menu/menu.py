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
        self.background = utils.load_image("background.png", "menu")
        self.logo = utils.load_image("title.png", "menu") #616x200
        self.start = Button(405, 290, "start_door/s1.png", "start_door/s2.png",
                            "start_door/s3.png", 408, 568) #408x568
        self.load = Button(760, 418, "load_door/l1.png", "load_door/l2.png",
                           "load_door/l3.png", 241, 336)
        self.exit = Button(985, 453, "exit_door/e1.png", "exit_door/e2.png",
                            "exit_door/e3.png", 181, 253)
        self.options = Button(205, 410, "options_door/o1.png", "options_door/o2.png",
                               "options_door/o3.png", 274, 338)
        self.credits_but = Button(5, 430, "credits_door/c1.png", "credits_door/c2.png",
                               "credits_door/c3.png", 224, 280)
        self.help_but = Button(1080, 0, "help/h1.png", "help/h2.png", None, 112, 202)


    def run(self):
        """
           The main loop event for the menu, run everything related to the Main menu here
        """

        # Channels

        FX_CHANNEL = pygame.mixer.Channel(0)
        VOICE_CHANNEL = pygame.mixer.Channel(1)
        EXTRA_CHANNEL = pygame.mixer.Channel(2)

        utils.load_bg("meny.ogg")
        pygame.mixer.music.play(-1, 0.0)

        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            #self.screen.fill(self.bg_color)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo, (300, 60))
            self.screen.blit(self.credits_but.base, (5, 430))
            self.screen.blit(self.exit.base, (985, 453))
            self.screen.blit(self.options.base, (205, 410))
            self.screen.blit(self.load.base, (760, 418))
            self.screen.blit(self.start.base, (405, 290)) # original 400,305
            self.screen.blit(self.help_but.base, (1080, 0))
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
                    if self.start.base_rect.collidepoint(mouse_x, mouse_y):
                        print("You clicked Start")
                    if self.load.base_rect.collidepoint(mouse_x, mouse_y):
                        print("You clicked Load")
                    if self.exit.base_rect.collidepoint(mouse_x, mouse_y):
                        running = False
                    if self.options.base_rect.collidepoint(mouse_x, mouse_y):
                        print("You clicked Options")
                    if self.credits_but.base_rect.collidepoint(mouse_x, mouse_y):
                        credit = credits.Credit(self.screen, self.clock)
                        credit.run()
                        del credit
                    if self.help_but.base_rect.collidepoint(mouse_x, mouse_y):
                        hjelp = scenarios.menu.help.Help(self.screen, self.clock)
                        hjelp.run()
                        del hjelp

                if event.type == pygame.MOUSEMOTION:
                    # Handle the hovering on the buttons

                    # Start Button
                    if self.start.flag == False and self.start.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        pygame.display.update(self.screen.blit(self.start.transition, (405, 290)))
                        pygame.display.update(self.screen.blit(self.start.end, (405, 290)))
                        self.start.base, self.start.end = self.start.end, self.start.base
                        self.start.flag = True
                    elif self.start.flag == True and not self.start.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        #the blits can be deleted if found that they slow performance
                        pygame.display.update(self.screen.blit(self.start.transition, (405, 290)))
                        pygame.display.update(self.screen.blit(self.start.end, (405, 290)))
                        self.start.base, self.start.end = self.start.end, self.start.base
                        self.start.flag = False

                    # Load Button
                    if self.load.flag == False and self.load.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        pygame.display.update(self.screen.blit(self.load.transition, (760, 418)))
                        pygame.display.update(self.screen.blit(self.load.end, (760, 418)))
                        self.load.base, self.load.end = self.load.end, self.load.base
                        self.load.flag = True
                    elif self.load.flag == True and not self.load.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        #the blits can be deleted if found that they slow performance
                        pygame.display.update(self.screen.blit(self.load.transition, (760, 418)))
                        pygame.display.update(self.screen.blit(self.load.end, (760, 418)))
                        self.load.base, self.load.end = self.load.end, self.load.base
                        self.load.flag = False

                    # Exit Button
                    if self.exit.flag == False and self.exit.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        pygame.display.update(self.screen.blit(self.exit.transition, (985, 453)))
                        pygame.display.update(self.screen.blit(self.exit.end, (985, 453)))
                        self.exit.base, self.exit.end = self.exit.end, self.exit.base
                        self.exit.flag = True
                    elif self.exit.flag == True and not self.exit.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        #the blits can be deleted if found that they slow performance
                        pygame.display.update(self.screen.blit(self.exit.transition, (985, 453)))
                        pygame.display.update(self.screen.blit(self.exit.end, (985, 453)))
                        self.exit.base, self.exit.end = self.exit.end, self.exit.base
                        self.exit.flag = False

                    # Options Button
                    if self.options.flag == False and self.options.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        pygame.display.update(self.screen.blit(self.options.transition, (205, 410)))
                        pygame.display.update(self.screen.blit(self.options.end, (205, 410)))
                        self.options.base, self.options.end = self.options.end, self.options.base
                        self.options.flag = True
                    elif self.options.flag == True and not self.options.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        #the blits can be deleted if found that they slow performance
                        pygame.display.update(self.screen.blit(self.options.transition, (205, 410)))
                        pygame.display.update(self.screen.blit(self.options.end, (205, 410)))
                        self.options.base, self.options.end = self.options.end, self.options.base
                        self.options.flag = False

                    # Credits Button
                    if self.credits_but.flag == False and self.credits_but.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        pygame.display.update(self.screen.blit(self.credits_but.transition, (5, 430)))
                        pygame.display.update(self.screen.blit(self.credits_but.end, (5, 430)))
                        self.credits_but.base, self.credits_but.end = self.credits_but.end, self.credits_but.base
                        self.credits_but.flag = True
                    elif self.credits_but.flag == True and not self.credits_but.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        #the blits can be deleted if found that they slow performance
                        pygame.display.update(self.screen.blit(self.credits_but.transition, (5, 430)))
                        pygame.display.update(self.screen.blit(self.credits_but.end, (5, 430)))
                        self.credits_but.base, self.credits_but.end = self.credits_but.end, self.credits_but.base
                        self.credits_but.flag = False

                    # Help Button
                    if self.help_but.flag == False and self.help_but.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        pygame.display.update(self.screen.blit(self.help_but.transition, (1080, 0)))
                        self.help_but.base, self.help_but.transition = self.help_but.transition, self.help_but.base
                        self.help_but.flag = True
                    elif self.help_but.flag == True and not self.help_but.base_rect.collidepoint(
                            mouse_x, mouse_y):
                        #the blits can be deleted if found that they slow performance
                        pygame.display.update(self.screen.blit(self.help_but.transition, (1080, 0)))
                        self.help_but.base, self.help_but.transition = self.help_but.transition, self.help_but.base
                        self.help_but.flag = False
