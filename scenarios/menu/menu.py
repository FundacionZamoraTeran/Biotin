import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.menu.button import Button
from scenarios.menu import credits, options, help, load, start


class Menu:
    """
       Class representing the start menu for the game, receives
       a Surface as screen, and a Clock as clock.
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.background = utils.load_image("background.png", "menu")
        self.logo = utils.load_image("title.png", "menu")  # 616x204
        self.start = Button(395,
                            280,
                            "start_door/s1.png",
                            "start_door/s2.png",
                            "start_door/s3.png",
                            414,
                            568,
                            flag=True)  # 408x568
        self.load_but = Button(190,
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
        self.level_selected = None
        self.slot_selected = None

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
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.logo, (260, 60))
            self.screen.blit(self.credits_but.base, (23, 413)) # 5x430
            self.screen.blit(self.exit.base, (960, 413)) #985x543
            self.screen.blit(self.options.base, (740, 408)) #760x418
            self.screen.blit(self.load_but.base, (190, 405)) # 200x410
            self.screen.blit(self.start.end, (395, 280)) # 405x290
            self.screen.blit(self.help_but.base, (1050, 0))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == consts.K_CHECK:
                        if self.start.flag is True:
                            start_state = start.Start(self.screen, self.clock)
                            start_state.run()
                            if start_state.level_selected is not None:
                                self.level_selected = start_state.level_selected
                                self.slot_selected = start_state.slot_selected
                                running = False
                            del start_state
                            utils.loading_screen(self.screen)
                        elif self.load_but.flag is True:
                            load_state = load.Load(self.screen, self.clock)
                            load_state.run()
                            if load_state.level_selected is not None:
                                self.level_selected = 1
                                self.slot_selected = load_state.slot_selected
                                running = False
                            del load_state
                            utils.loading_screen(self.screen)
                        elif self.credits_but.flag is True:
                            credit = credits.Credit(self.screen, self.clock)
                            credit.run()
                            del credit
                        elif self.options.flag is True:
                            option = options.Option(self.screen, self.clock)
                            option.run()
                            del option
                        elif self.exit.flag is True:
                            running = False
                        elif self.help_but.flag is True:
                            hjelp = help.Help(self.screen, self.clock)
                            hjelp.run()
                            del hjelp
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.start.flag is True:
                            self.start.flag = False
                            self.load_but.flag = True
                            self.start.on_focus(self.screen)
                            self.load_but.on_focus(self.screen)
                        elif self.load_but.flag is True:
                            self.load_but.flag = False
                            self.credits_but.flag = True
                            self.load_but.on_focus(self.screen)
                            self.credits_but.on_focus(self.screen)
                        elif self.options.flag is True:
                            self.options.flag = False
                            self.start.flag = True
                            self.options.on_focus(self.screen)
                            self.start.on_focus(self.screen)
                        elif self.exit.flag is True:
                            self.exit.flag = False
                            self.options.flag = True
                            self.exit.on_focus(self.screen)
                            self.options.on_focus(self.screen)
                        elif self.help_but.flag is True:
                            self.help_but.flag = False
                            self.exit.flag = True
                            self.help_but.on_focus_altern(self.screen)
                            self.exit.on_focus(self.screen)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.start.flag is True:
                            self.start.flag = False
                            self.options.flag = True
                            self.start.on_focus(self.screen)
                            self.options.on_focus(self.screen)
                        elif self.options.flag is True:
                            self.options.flag = False
                            self.exit.flag = True
                            self.options.on_focus(self.screen)
                            self.exit.on_focus(self.screen)
                        elif self.exit.flag is True:
                            self.exit.flag = False
                            self.help_but.flag = True
                            self.exit.on_focus(self.screen)
                            self.help_but.on_focus_altern(self.screen)
                        elif self.load_but.flag is True:
                            self.load_but.flag = False
                            self.start.flag = True
                            self.load_but.on_focus(self.screen)
                            self.start.on_focus(self.screen)
                        elif self.credits_but.flag is True:
                            self.credits_but.flag = False
                            self.load_but.flag = True
                            self.credits_but.on_focus(self.screen)
                            self.load_but.on_focus(self.screen)
                    if event.key == pygame.K_ESCAPE or event.key == consts.K_CIRCLE:
                        hjelp = help.Help(self.screen, self.clock)
                        hjelp.run()
                        del hjelp
