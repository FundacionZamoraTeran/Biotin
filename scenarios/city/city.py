import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.city import house_1
from scenarios.city import house_2
from scenarios.city import troll
from actors.player import Player
from actors.prompt import Prompt


class City:
    """
        Class representing the first stage of City village, recieves
        a Surface as a screen, and a Clock as clock, and a character name
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.frame = 0
        self.character = character
        self.background = utils.load_image("background.png", "city/city")
        self.background_width = self.background.get_size()[0]
        self.plant = utils.load_image("plant.png", "city/city/")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (1475, 280),
                               "interact.png",
                               "city",
                               (300, 500))

        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (2615, 280),
                                 "interact.png",
                                 "city",
                                 (300, 500))
        self.interact_3 = Prompt(self.screen,
                                 self.clock,
                                 (3385, 280),
                                 "interact.png",
                                 "city",
                                 (200, 400))
        self.player = Player(self.screen,
                             self.clock,
                             (150, 540),
                             self.character,
                             3600,
                             True)
        self.troll = {
            "0" : utils.load_image("1.png", "troll"),
            "1" : utils.load_image("2.png", "troll"),
            "2" : utils.load_image("3.png", "troll"),
            "3" : utils.load_image("4.png", "troll"),
            "4" : utils.load_image("5.png", "troll"),
            "5" : utils.load_image("6.png", "troll"),
        }
        self.current_slide = 1
        self.played = [0] * 6
        self.conversation = {
            "1" : utils.load_image("d1.png", "city/city/dialogue"),
            "2" : utils.load_image("d2.png", "city/city/dialogue"),
            "3" : utils.load_image("d3.png", "city/city/dialogue"),
            "4" : utils.load_image("d4.png", "city/city/dialogue"),
            "5" : utils.load_image("d5.png", "city/city/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("city/city/1.ogg"),
            "2" : utils.load_vx("city/city/2.ogg"),
            "3" : utils.load_vx("city/city/3.ogg"),
            "4" : utils.load_vx("city/city/4.ogg"),
            "5" : utils.load_vx("city/city/5.ogg")
        }
        self.visited = [False, False]
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "city")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "city")


    def run(self):
        utils.load_bg("al_mohren.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.render_scene(self.current_slide, abs(rel_x))
                self.screen.blit(self.plant, (1860-abs(rel_x), 580))
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
                        if self.current_slide == 5:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide = 1
                        elif 1 < self.current_slide < 6:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 1:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 6 or self.current_slide == 4:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide = 1
                        elif 1 < self.current_slide < 6:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 1400
                                and self.player.real_x+self.player.rect.width < 1645 and
                                self.current_slide == 1):
                            utils.loading_screen(self.screen)
                            hus = house_1.House_1(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            utils.load_bg("al_mohren.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME)
                            pygame.mixer.music.play(-1, 0.0)
                        elif (self.player.real_x+self.player.rect.width > 2540 and
                              self.player.real_x+self.player.rect.width < 2780 and
                              self.current_slide == 1):
                            utils.loading_screen(self.screen)
                            hus = house_2.House_2(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            utils.load_bg("al_mohren.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME)
                            pygame.mixer.music.play(-1, 0.0)
                            self.visited[1] = True
                        elif (self.player.real_x+self.player.rect.width > 3200
                              and self.player.real_x+self.player.rect.width < 3600 and
                              self.current_slide == 1):
                            if self.visited[1]:
                                utils.loading_screen(self.screen)
                                tro = troll.Troll(self.screen, self.clock, self.character)
                                tro.run()
                                del tro
                                running = False
                            else:
                                self.current_slide = 5
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        self.player.jumping = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"
    def render_scene(self, number, rel_x):
        if number == 1:
            self.actors_load(rel_x)
        elif number > 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.actors_load(rel_x)
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def actors_load(self, rel_x):
        if (self.player.real_x+self.player.rect.width > 2620
                and self.player.real_x+self.player.rect.width < 3600):
            if self.visited[0] is False:
                self.current_slide = 2
                self.visited[0]= True
            self.render_troll(rel_x)
        if (self.player.real_x+self.player.rect.width > 1400
                and self.player.real_x+self.player.rect.width < 1645):
            self.interact.float(rel_x)
        elif (self.player.real_x+self.player.rect.width > 2540
                and self.player.real_x+self.player.rect.width < 2780):
            self.interact_2.float(rel_x)
        elif (self.player.real_x > 3200
                and self.player.real_x+self.player.rect.width < 3600):
            self.interact_3.float(rel_x)
            if self.player.velocity > 0:
                self.player.rect.x = 830
                self.player.real_x = 3230
        self.player.update()
    def render_troll(self, rel_x):
        self.frame += 1
        if self.frame > 11:
            self.frame = 0
        self.screen.blit(self.troll[str(self.frame//2)], (3300-rel_x, 400))
