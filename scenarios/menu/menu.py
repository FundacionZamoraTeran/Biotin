import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.menu.button import Button
from scenarios.menu import credits, options, help


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
        self.logo = utils.load_image("title.png", "menu")  # 616x204
        self.start = Button(395,
                            280,
                            "start_door/s1.png",
                            "start_door/s2.png",
                            "start_door/s3.png",
                            414,
                            568)  # 408x568
        self.load = Button(190,
                           405,
                           "load_door/l1.png",
                           "load_door/l2.png",
                           "load_door/l3.png",
                           270,
                           337)
        self.exit = Button(960,
                           413,
                           "exit_door/e1.png",
                           "exit_door/e2.png",
                           "exit_door/e3.png",
                           229,
                           292)
        self.options = Button(740,
                              408,
                              "options_door/o1.png",
                              "options_door/o2.png",
                              "options_door/o3.png",
                              270,
                              337)
        self.credits_but = Button(23,
                                  413,
                                  "credits_door/c1.png",
                                  "credits_door/c2.png",
                                  "credits_door/c3.png",
                                  229,
                                  292)
        self.help_but = Button(1050,
                               0,
                               "help/h1.png",
                               "help/h2.png",
                               None,
                               126,
                               202)

    def run(self):
        """
           The main loop event for the menu
        """

        # Channels

        FX_CHANNEL = pygame.mixer.Channel(0)
        FX_CHANNEL.set_volume(consts.FX_VOLUME)
        VOICE_CHANNEL = pygame.mixer.Channel(1)
        VOICE_CHANNEL.set_volume(consts.VX_VOLUME)

        utils.load_bg("meny.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)

        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # self.screen.fill(self.bg_color)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo, (300, 60))
            self.screen.blit(self.credits_but.base, (23, 413)) # 5x430
            self.screen.blit(self.exit.base, (960, 413)) #985x543
            self.screen.blit(self.options.base, (740, 408)) #760x418
            self.screen.blit(self.load.base, (190, 405)) # 200x410
            self.screen.blit(self.start.base, (395, 280)) # 405x290
            self.screen.blit(self.help_but.base, (1050, 0))
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
                        option = options.Option(self.screen, self.clock)
                        option.run()
                        del option
                    if self.credits_but.base_rect.collidepoint(mouse_x, mouse_y):
                        credit = credits.Credit(self.screen, self.clock)
                        credit.run()
                        del credit
                    if self.help_but.base_rect.collidepoint(mouse_x, mouse_y):
                        hjelp = help.Help(self.screen, self.clock)
                        hjelp.run()
                        del hjelp

                if event.type == pygame.MOUSEMOTION:
                    # Handle the hovering on the buttons

                    # Start Button
                    self.start.on_selection(self.screen, mouse_x, mouse_y)
                    # Load Button
                    self.load.on_selection(self.screen, mouse_x, mouse_y)
                    # Exit Button
                    self.exit.on_selection(self.screen, mouse_x, mouse_y)
                    # Options Button
                    self.options.on_selection(self.screen, mouse_x, mouse_y)
                    # Credits Button
                    self.credits_but.on_selection(self.screen, mouse_x, mouse_y)
                    # Help Button
                    self.help_but.on_selection_altern(self.screen, mouse_x, mouse_y)
