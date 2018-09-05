import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from actors.player import Player
from actors.enemy import Enemy
from actors.prompt import Prompt

class Last:
    """
        Class representing the last part of the valley, recieves
        a Surface as a screen, and a Clock as clock, and slot name
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.character = character
        self.background = utils.load_image("background.png", "valley")
        self.background_width = self.background.get_size()[0]
        self.interact = Prompt(self.screen,
                               self.clock,
                               (2280, 480),
                               "interact.png",
                               "sharqii",
                               (400, 600))
        self.player = Player(self.screen,
                             self.clock,
                             (150, 600),
                             self.character,
                             2400,
                             True,
                             collisionable=True)
        self.gali =  Enemy(self.screen,
                            self.clock,
                            (1000, 620),
                            "monsters/gali",
                            (300, 1640),
                            24,
                            35)
        
        self.glopop = Enemy(self.screen,
                            self.clock,
                            (1940, 540),
                            "monsters/glopop",
                            (1100, 2200),
                            26)
        self.lopop = Enemy(self.screen,
                           self.clock,
                           (1940, 700),
                           "monsters/lopop",
                           (1300, 1940),
                           18,
                           35)
        self.menti = Enemy(self.screen,
                           self.clock,
                           (1000, 660),
                           "monsters/menti",
                           (300, 1000),
                           16)


        self.current_slide = 6
        self.played = [0] * 5
        self.conversation = {
            "1" : utils.load_image("d1.png", "valley/dialogue"),
            "2" : utils.load_image("d2.png", "valley/dialogue"),
            "3" : utils.load_image("d3.png", "valley/dialogue"),
            "4" : utils.load_image("d4.png", "valley/dialogue"),
            "5" : utils.load_image("d5.png", "valley/dialogue"),
        }
        self.voices = {
            "1" : utils.load_vx("valley/1.ogg"),
            "2" : utils.load_vx("valley/2.ogg"),
            "3" : utils.load_vx("valley/3.ogg"),
            "4" : utils.load_vx("valley/4.ogg"),
            "5" : utils.load_vx("valley/5.ogg")
        }

        self.enemies_list = pygame.sprite.Group()
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "sharqii")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "sharqii")

    def run(self):
        utils.load_bg("valley.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.render_scene(self.current_slide, abs(rel_x))
            else:
                self.screen.blit(self.background, (rel_x - self.background_width, 0))
                self.render_scene(self.current_slide, rel_x)
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
                        if 1 < self.current_slide < 6:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 6:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if  self.current_slide < 6:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 6:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 6:
                            if (self.player.real_x+self.player.rect.width > 2280 and
                                    self.player.real_x+self.player.rect.width < 2401):
                                utils.loading_screen(self.screen)
                                running = False
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.catching is False)):
                        if self.current_slide == 6:
                            self.player.catching = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 6:
                            self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 6:
                            self.player.direction = "stand"
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.catching is True)):
                        if self.current_slide == 6:
                            self.player.catching = False
    def render_scene(self, number, rel_x):
        if number == 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[number-1] = 1
            self.screen.blit(self.conversation["1"], (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
        elif 1 < number < 6:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.conversation[str(number)], (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 6:
            self.actors_load(rel_x)

    def actors_load(self, rel_x):
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
        if self.player.real_x < 1500 and not self.menti.defeated:
            if not self.menti.alive():
                self.menti.add(self.enemies_list)
            if not self.menti.transformed:
                self.menti.roam(rel_x)
            else:
                self.menti.remove(self.enemies_list)
                self.screen.blit(self.menti.sprites["transform"], (self.menti.x-rel_x, 660))
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
                self.screen.blit(self.glopop.sprites["transform"], (self.glopop.x-rel_x, 540))
        else:
            if self.glopop.alive():
                self.glopop.remove(self.enemies_list)
        if self.player.real_x > 1000 and not self.lopop.defeated:
            if not self.lopop.alive():
                self.lopop.add(self.enemies_list)
            if not self.lopop.transformed:
                self.lopop.roam(rel_x)
            else:
                self.lopop.remove(self.enemies_list)
                self.screen.blit(self.lopop.sprites["transform"], (self.lopop.x-rel_x, 700))
        else:
            if self.lopop.alive():
                self.lopop.remove(self.enemies_list)

        if (self.player.real_x+self.player.rect.width > 2280
                and self.player.real_x+self.player.rect.width < 2401):
            self.interact.float(1200)
        self.player.set_sprite_groups([], self.enemies_list)
        self.player.update()
