import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.space import egg
from actors.player import Player
from actors.platform import Platform
from actors.prompt import Prompt


class Game:
    """
        Class representing the jumping stage on space scenario, recieves
        a Surface as a screen, and a Clock as clock, and a save slot name
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.character = character
        self.background = utils.load_image("background.png", "space/game")
        self.background_width = self.background.get_size()[0]
        self.modal = utils.load_image("help.png", "space/game/modal")
        self.p1 = Platform(self.screen,
                           self.clock,
                           (0, 242),
                           "p1.png",
                           "space/game")
        self.p2 = Platform(self.screen,
                           self.clock,
                           (600, 642),
                           "p2.png",
                           "space/game")
        self.p3 = Platform(self.screen,
                           self.clock,
                           (1350, 342),
                           "p5.png",
                           "space/game")
        self.p4 = Platform(self.screen,
                           self.clock,
                           (1200, 742),
                           "p3.png",
                           "space/game")
        self.p5 = Platform(self.screen,
                           self.clock,
                           (1950, 642),
                           "p4.png",
                           "space/game")
        self.p7 = Platform(self.screen,
                           self.clock,
                           (2700, 542),
                           "p2.png",
                           "space/game")
        self.p8 = Platform(self.screen,
                           self.clock,
                           (3450, 402),
                           "p1.png",
                           "space/game")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (3480, 120),
                               "interact.png",
                               "space",
                               (200, 200))
        self.interact.velocity = 0

        self.player = Player(self.screen,
                             self.clock,
                             (150, 140),
                             self.character,
                             3600,
                             True,
                             collisionable=False,
                             physics=(28, 380, 1.2),
                             plataforming=True)
        self.player.plataforming = True

        #collision lists
        self.platforms_list = pygame.sprite.Group()
        self.platforms_list.add(self.p1, self.p2, self.p3, self.p4, self.p5, self.p7, self.p8)
        self.player.set_sprite_groups(self.platforms_list, [])
        self.help = Button((1058, 39), "h1.png", "h2.png", 82, 82, "space/game/")
        self.show_help = True

    def run(self):
        utils.load_bg("space.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.actors_load()
                if self.show_help:
                    self.screen.blit(self.modal, (0, 0))
                    self.screen.blit(self.help.end, (1058, 39))
                else:
                    self.screen.blit(self.help.base, (1058, 39))
            else:
                self.screen.blit(self.background, (rel_x, 0))
                self.actors_load()
                if self.show_help:
                    self.screen.blit(self.modal, (0, 0))
                    self.screen.blit(self.help.end, (1058, 39))
                else:
                    self.screen.blit(self.help.base, (1058, 39))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if not self.show_help:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if not self.show_help:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 3400
                              and self.player.real_x+self.player.rect.width < 3700):
                            utils.loading_screen(self.screen)
                            eggo = egg.Egg(self.screen, self.clock, self.character)
                            eggo.run()
                            del eggo
                            running = False
                            utils.loading_screen(self.screen)
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        if not self.show_help:
                            self.player.jumping = True
                    elif event.key == pygame.K_ESCAPE or event.key == consts.K_CIRCLE:
                        self.help.on_press(self.screen)
                        if self.show_help is False:
                            self.show_help = True
                        elif self.show_help:
                            self.show_help = False

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"

    def actors_load(self):
        self.platforms_list.update()
        if (self.player.real_x+self.player.rect.width > 3400
                and self.player.real_x+self.player.rect.width < 3700):
            self.interact.float(2400)
        self.player.set_sprite_groups(self.platforms_list, [])
        self.player.update()
