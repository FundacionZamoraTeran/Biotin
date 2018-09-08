import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.luis import game

class Stomach:
    """
        Class representing the stomach comic before the final battle, recieves
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
        self.background = utils.load_image("background.png", "luis/stomach")
        self.pilori = utils.load_image("pilori.png", "luis/stomach")
        self.monster = utils.load_image("monster.png", "luis/stomach")
        self.biotin = utils.load_image("team.png", "luis/stomach")
        self.next_level = 1
        self.frame = 0
        self.current_slide = 1
        self.played = [0] * 12
        self.conversation = {
            "1" : utils.load_image("d1.png", "luis/stomach/dialogue"),
            "2" : utils.load_image("d2.png", "luis/stomach/dialogue"),
            "3" : utils.load_image("d3.png", "luis/stomach/dialogue"),
            "4" : utils.load_image("d4.png", "luis/stomach/dialogue"),
            "5" : utils.load_image("d5.png", "luis/stomach/dialogue"),
            "6" : utils.load_image("d6.png", "luis/stomach/dialogue"),
            "7" : utils.load_image("d7.png", "luis/stomach/dialogue"),
            "8" : utils.load_image("d8.png", "luis/stomach/dialogue"),
            "9" : utils.load_image("d9.png", "luis/stomach/dialogue"),
            "10" : utils.load_image("d10.png", "luis/stomach/dialogue"),
            "11" : utils.load_image("d11.png", "luis/stomach/dialogue"),
            "12" : utils.load_image("d12.png", "luis/stomach/dialogue")
        }
        self.voices = {
            "2" : utils.load_vx("luis/stomach/2.ogg"),
            "3" : utils.load_vx("luis/stomach/3.ogg"),
            "4" : utils.load_vx("luis/stomach/4.ogg"),
            "5" : utils.load_vx("luis/stomach/5.ogg"),
            "6" : utils.load_vx("luis/stomach/6.ogg"),
            "7" : utils.load_vx("luis/stomach/7.ogg"),
            "8" : utils.load_vx("luis/stomach/8.ogg"),
            "9" : utils.load_vx("luis/stomach/9.ogg"),
            "10" : utils.load_vx("luis/stomach/10.ogg"),
            "11" : utils.load_vx("luis/stomach/11.ogg"),
            "12" : utils.load_vx("luis/stomach/12.ogg")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "castle")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "castle")

    def run(self):
        utils.load_bg("etude1.ogg")
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
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide > 1:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 12:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 12:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            gam = game.Game(self.screen, self.clock, self.character)
                            gam.run()
                            del gam
                            running = False

    def render_scene(self, number):
        if number == 1:
            self.screen.blit(self.biotin, (140, 407))
            self.screen.blit(self.pilori, (930, 367))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 2:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.biotin, (140, 407))
            self.screen.blit(self.pilori, (930, 367))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif 2 < number < 13:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.biotin, (140, 407))
            self.screen.blit(self.monster, (850, 367))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
