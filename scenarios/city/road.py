import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from actors.player import Player
from actors.prompt import Prompt


class Road:
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
        self.background = utils.load_image("background.png", "city/road")
        self.foreground = utils.load_image("foreground.png", "city/road")
        self.background_width = self.background.get_size()[0]
        self.interact = Prompt(self.screen,
                               self.clock,
                               (1705, 280),
                               "interact.png",
                               "city",
                               (300, 500))
        self.player = Player(self.screen,
                             self.clock,
                             (150, 470),
                             self.character,
                             2000,
                             True)
        self.current_slide = 1
        self.played = [0] * 4
        self.conversation = {
            "1" : utils.load_image("d1.png", "city/road/dialogue"),
            "2" : utils.load_image("d2.png", "city/road/dialogue"),
            "3" : utils.load_image("d3.png", "city/road/dialogue"),
        }
        self.voices = {
            "1" : utils.load_vx("city/road/1.ogg"),
            "2" : utils.load_vx("city/road/2.ogg"),
        }
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
                        if 1 < self.current_slide < 5:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 1:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 4:
                            self.vx_channel.stop()
                            running = False
                        elif 1 < self.current_slide < 4:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 1600
                              and self.player.real_x+self.player.rect.width < 2000 and
                              self.current_slide == 1):
                                self.current_slide = 2
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
            self.screen.blit(self.foreground, (-rel_x, 414))
        elif number == 2:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[number-1] = 1
            self.actors_load(rel_x)
            self.screen.blit(self.foreground, (-rel_x, 414))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 3:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["2"])
                self.played[number-1] = 1
            self.actors_load(rel_x)
            self.screen.blit(self.foreground, (-rel_x, 414))
            self.screen.blit(self.conversation["2"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 4:
            self.actors_load(rel_x)
            self.screen.blit(self.foreground, (-rel_x, 414))
            self.screen.blit(self.conversation["3"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def actors_load(self, rel_x):
        if (self.player.real_x > 1600
                and self.player.real_x+self.player.rect.width < 2000):
            self.interact.float(rel_x)
        self.player.update()
