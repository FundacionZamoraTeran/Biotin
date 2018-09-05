import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.candy import middle
from actors.player import Player
from actors.enemy import Enemy
from actors.prompt import Prompt

class Wood:
    """
        Class representing the first part of the candy woods, recieves
        a Surface as a screen, and a Clock as clock, and slot name
    """
    def __init__(self, screen, clock, slot):
        self.screen = screen
        self.clock = clock
        self.slotname = slot
        self.slot = saves.load_slot(slot)
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.next_level = 1
        self.character = "ena" if self.slot["team_ena"] is True else "diego"
        self.background = utils.load_image("background.png", "candy")
        self.background_width = self.background.get_size()[0]
        self.interact = Prompt(self.screen,
                               self.clock,
                               (2280, 480),
                               "interact.png",
                               "candy",
                               (400, 600))
        self.player = Player(self.screen,
                             self.clock,
                             (150, 600),
                             self.character,
                             2400,
                             True,
                             collisionable=True)
        self.gali = Enemy(self.screen,
                          self.clock,
                          (1000, 620),
                          "monsters/gali",
                          (300, 1640),
                          10)
        self.vlopop = Enemy(self.screen,
                            self.clock,
                            (1000, 660),
                            "monsters/vlopop",
                            (300, 1000),
                            24,
                            35)
        self.glopop = Enemy(self.screen,
                           self.clock,
                           (1940, 630),
                           "monsters/glopop",
                           (1300, 1940),
                           18,
                           35)
        self.menti = Enemy(self.screen,
                           self.clock,
                           (1940, 700),
                           "monsters/menti",
                           (1100, 2200),
                           26)

        self.enemies_list = pygame.sprite.Group()

    def run(self):
        utils.load_bg("valley.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.actors_load(abs(rel_x))
            else:
                self.screen.blit(self.background, (rel_x - self.background_width, 0))
                self.actors_load(rel_x)

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
                        self.player.direction = "left"
                        self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "right"
                        self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 2280 and
                                self.player.real_x+self.player.rect.width < 2401):
                            utils.loading_screen(self.screen)
                            mid = middle.Middle(self.screen, self.clock, self.character)
                            mid.run()
                            del mid
                            running = False
                            utils.loading_screen(self.screen)
                            # save here
                            if not self.slot["stages"]["bosque"] is True:
                                saves.save(self.slotname, 6, "El Bosque de caramelo", "bosque")
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.catching is False)):
                        self.player.catching = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.catching is True)):
                        self.player.catching = False

    def actors_load(self, rel_x):
        if self.player.real_x < 1500 and not self.vlopop.defeated:
            if not self.vlopop.alive():
                self.vlopop.add(self.enemies_list)
            if not self.vlopop.transformed:
                self.vlopop.roam(rel_x)
            else:
                self.vlopop.remove(self.enemies_list)
                self.screen.blit(self.vlopop.sprites["transform"], (self.vlopop.x-rel_x, 660))
        else:
            if self.vlopop.alive():
                self.vlopop.remove(self.enemies_list)
        if self.player.real_x < 2401 and not self.gali.defeated:
            if not self.gali.alive():
                self.gali.add(self.enemies_list)
            if not self.gali.transformed:
                self.gali.roam(rel_x)
            else:
                self.gali.remove(self.enemies_list)
                self.screen.blit(self.gali.sprites["transform"], (self.gali.x-rel_x, 620))
        else:
            if self.gali.alive():
                self.gali.remove(self.enemies_list)
        if self.player.real_x > 800 and not self.menti.defeated:
            if not self.menti.alive():
                self.menti.add(self.enemies_list)
            if not self.menti.transformed:
                self.menti.roam(rel_x)
            else:
                self.menti.remove(self.enemies_list)
                self.screen.blit(self.menti.sprites["transform"], (self.menti.x-rel_x, 700))
        else:
            if self.menti.alive():
                self.menti.remove(self.enemies_list)
        if self.player.real_x > 1000 and not self.glopop.defeated:
            if not self.glopop.alive():
                self.glopop.add(self.enemies_list)
            if not self.glopop.transformed:
                self.glopop.roam(rel_x)
            else:
                self.glopop.remove(self.enemies_list)
                self.screen.blit(self.glopop.sprites["transform"], (self.glopop.x-rel_x, 630))
        else:
            if self.glopop.alive():
                self.glopop.remove(self.enemies_list)

        if (self.player.real_x+self.player.rect.width > 2280
                and self.player.real_x+self.player.rect.width < 2401):
            self.interact.float(1200)
        self.player.set_sprite_groups([], self.enemies_list)
        self.player.update()
