import sys
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.saar import hdiego
from scenarios.saar import last
from actors.player import Player
from actors.enemy import Enemy
from actors.platform import Platform
from actors.prompt import Prompt

class Middle:
    """
        Class representing the second stage of Saar village, recieves
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
        self.background = utils.load_image("background.png", "saar/stage_2")
        self.background_width = self.background.get_size()[0]
        self.foreground = utils.load_image("foreground.png", "saar/stage_2")
        self.modal = utils.load_image("modal.png", "saar")
        self.ground = Platform(self.screen,
                               self.clock,
                               (0, 747),
                               "ground.png",
                               "saar/stage_2")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (2065, 480),
                               "interact.png",
                               "saar",
                               (400, 600))
        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (2280, 480),
                                 "interact.png",
                                 "saar",
                                 (400, 600))

        self.player = Player(self.screen,
                             self.clock,
                             (150, 640),
                             self.character,
                             2400,
                             True,
                             collisionable=True)
        self.glopop = Enemy(self.screen,
                            self.clock,
                            (1000, 700),
                            "monsters/glopop",
                            (300, 1000),
                            24)
        self.vlopop = Enemy(self.screen,
                            self.clock,
                            (1940, 700),
                            "monsters/vlopop",
                            (1300, 1940),
                            22,
                            35)
        self.platforms_list = pygame.sprite.Group()
        self.enemies_list = pygame.sprite.Group()
        self.platforms_list.add(self.ground)
        self.help = Button((1058, 39), "h1.png", "h2.png", 82, 82, "saar")
        self.show_help = False
        self.visited = False

    def run(self):
        utils.load_bg("nocturne.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.screen.blit(self.ground.image, (rel_x, 747))
                self.actors_load(abs(rel_x))
                self.screen.blit(self.foreground, (rel_x, 711))
                if self.show_help:
                    self.screen.blit(self.help.end, (1058, 39))
                    self.screen.blit(self.modal, (0, 0))
                else:
                    self.screen.blit(self.help.base, (1058, 39))
            else:
                self.screen.blit(self.background, (rel_x - self.background_width, 0))
                self.screen.blit(self.ground.image, (rel_x - self.background_width, 747))
                self.actors_load(rel_x)
                self.screen.blit(self.foreground, (rel_x - self.background_width, 711))
                if self.show_help:
                    self.screen.blit(self.help.end, (1058, 39))
                    self.screen.blit(self.modal, (0, 0))
                else:
                    self.screen.blit(self.help.base, (1058, 39))
            pygame.display.flip()
            self.clock.tick(consts.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "left"
                        self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "right"
                        self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 2050 and
                                self.player.real_x+self.player.rect.width < 2190):
                            utils.loading_screen(self.screen)
                            hus = hdiego.Hdiego(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            self.visited = True
                            utils.load_bg("nocturne.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME)
                            pygame.mixer.music.play(-1, 0.0)
                        elif (self.player.real_x+self.player.rect.width > 2280
                              and self.player.real_x+self.player.rect.width < 2401 and
                              self.visited):
                            utils.loading_screen(self.screen)
                            end = last.Last(self.screen, self.clock, self.character)
                            end.run()
                            del end
                            running = False
                    elif event.key == pygame.K_ESCAPE or event.key == consts.K_CIRCLE:
                        self.help.on_press(self.screen)
                        if self.show_help is False:
                            self.show_help = True
                        elif self.show_help:
                            self.show_help = False
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        self.player.jumping = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"

    def actors_load(self, rel_x):
        if self.player.real_x < 1500 and not self.glopop.defeated:
            if not self.glopop.alive():
                self.glopop.add(self.enemies_list)
            self.glopop.roam(rel_x)
        else:
            if self.glopop.alive():
                self.glopop.remove(self.enemies_list)
        if self.player.real_x > 1000 and not self.vlopop.defeated:
            if not self.vlopop.alive():
                self.vlopop.add(self.enemies_list)
            self.vlopop.roam(rel_x)
        else:
            if self.vlopop.alive():
                self.vlopop.remove(self.enemies_list)
        if (self.player.real_x+self.player.rect.width > 2050
                and self.player.real_x+self.player.rect.width < 2190):
            self.interact.float(1200)
        if (self.player.real_x+self.player.rect.width > 2280
                and self.player.real_x+self.player.rect.width < 2401 and self.visited):
            self.interact_2.float(1200)
        self.player.set_sprite_groups(self.platforms_list, self.enemies_list)
        self.player.update()
