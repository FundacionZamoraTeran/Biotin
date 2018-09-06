import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from scenarios.space import island2
from actors.player import Player
from actors.prompt import Prompt

class Egg:
    """
        Class representing the  eggflame retrieval in  the space scenario, recieves
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
        self.background = utils.load_image("background.png", "space/egg")
        self.modal = utils.load_image("modal.png", "space/egg")
        self.frame = 0
        self.current_slide = 1
        self.played = [0] * 2
        self.conversation = {
            "1" : utils.load_image("d1.png", "space/egg/dialogue"),
            "2" : utils.load_image("d2.png", "space/egg/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("space/egg/1.ogg"),
            "2" : utils.load_vx("space/egg/2.ogg")
        }
        self.eggflame = {
            "0" : utils.load_image("f1.png", "space/egg/"),
            "1" : utils.load_image("f2.png", "space/egg/")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "space")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "space")

    def run(self):
        utils.load_bg("space.ogg")
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
                        if self.current_slide == 2:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide = 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 3:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 3:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            isl = island2.Island2(self.screen, self.clock, self.character)
                            isl.run()
                            del isl
                            running = False

    def render_scene(self, number):
        if number == 1:
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[0] = 1
            self.fire()
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["2"])
                self.played[1] = 1
            self.fire()
            self.screen.blit(self.conversation["2"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 3:
            self.screen.blit(self.modal, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
    def fire(self):
        self.frame += 1
        if self.frame > 3:
            self.frame = 0
        self.screen.blit(self.eggflame[str(self.frame//2)], (700, 200))
