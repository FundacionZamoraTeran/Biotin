import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from scenarios.city import road

class Troll:
    """
        Class representing the first house in the city scenario, recieves
        a Surface as a screen, and a Clock as clock, and character name
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.character = character
        self.background = utils.load_image("background.png", "city/troll")
        self.team = utils.load_image("biotin.png", "city/troll")

        self.current_slide = 1
        self.played = [0] * 11
        self.conversation = {
            "1" : utils.load_image("d1.png", "city/troll/dialogue"),
            "2" : utils.load_image("d2.png", "city/troll/dialogue"),
            "3" : utils.load_image("d3.png", "city/troll/dialogue"),
            "4" : utils.load_image("d4.png", "city/troll/dialogue"),
            "5" : utils.load_image("d5.png", "city/troll/dialogue"),
            "6" : utils.load_image("d6.png", "city/troll/dialogue"),
            "7" : utils.load_image("d7.png", "city/troll/dialogue"),
            "8" : utils.load_image("d8.png", "city/troll/dialogue"),
            "9" : utils.load_image("d9.png", "city/troll/dialogue"),
            "10" : utils.load_image("d10.png", "city/troll/dialogue"),
            "11" : utils.load_image("d11.png", "city/troll/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("city/troll/1.ogg"),
            "2" : utils.load_vx("city/troll/2.ogg"),
            "3" : utils.load_vx("city/troll/3.ogg"),
            "4" : utils.load_vx("city/troll/4.ogg"),
            "5" : utils.load_vx("city/troll/5.ogg"),
            "6" : utils.load_vx("city/troll/6.ogg"),
            "7" : utils.load_vx("city/troll/7.ogg"),
            "8" : utils.load_vx("city/troll/8.ogg"),
            "9" : utils.load_vx("city/troll/9.ogg"),
            "10" : utils.load_vx("city/troll/10.ogg"),
            "11" : utils.load_vx("city/troll/11.ogg")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "city")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "city")

    def run(self):
        utils.load_bg("avant.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.render_scene(self.current_slide)
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
                        if self.current_slide > 1:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 11:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 11:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            roa = road.Road(self.screen, self.clock, self.character)
                            roa.run()
                            del roa
                            running = False

    def render_scene(self, number):
        if number == 1:
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[0] = 1
            self.screen.blit(self.team, (400, 367))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number > 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.team, (400, 367))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
