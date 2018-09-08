import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.castle import game

class Lab:
    """
        Class representing the alchemy lab in the castle scenario, recieves
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
        self.character = "ena" if self.slot["team_ena"] is True else "diego"
        self.background_1 = utils.load_image("background1.png", "castle/lab")
        self.background_2 = utils.load_image("background2.png", "castle/lab")
        self.background_3 = utils.load_image("background3.png", "castle/lab")
        self.next_level = 1
        self.frame = 0
        self.current_slide = 1
        self.played = [0] * 9
        self.conversation = {
            "1" : utils.load_image("d1.png", "castle/lab/dialogue"),
            "2" : utils.load_image("d2.png", "castle/lab/dialogue"),
            "3" : utils.load_image("d3.png", "castle/lab/dialogue"),
            "4" : utils.load_image("d4.png", "castle/lab/dialogue"),
            "5" : utils.load_image("d5.png", "castle/lab/dialogue"),
            "6" : utils.load_image("d6.png", "castle/lab/dialogue"),
            "7" : utils.load_image("d7.png", "castle/lab/dialogue"),
            "8" : utils.load_image("d8.png", "castle/lab/dialogue"),
            "9" : utils.load_image("d9.png", "castle/lab/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("castle/lab/1.ogg"),
            "2" : utils.load_vx("castle/lab/2.ogg"),
            "3" : utils.load_vx("castle/lab/3.ogg"),
            "4" : utils.load_vx("castle/lab/4.ogg"),
            "5" : utils.load_vx("castle/lab/5.ogg"),
            "6" : utils.load_vx("castle/lab/6.ogg"),
            "7" : utils.load_vx("castle/lab/7.ogg"),
            "8" : utils.load_vx("castle/lab/8.ogg"),
            "9" : utils.load_vx("castle/lab/9.ogg")
        }
        self.visited = False
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "castle")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "castle")

    def run(self):
        utils.load_bg("etude1.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:

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
                        if self.current_slide < 9:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 9:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            gam = game.Game(self.screen, self.clock, self.character)
                            gam.run()
                            del gam
                            running = False
                            if not self.slot["stages"]["castillo"] is True:
                                saves.save(self.slotname, 9, "El Castillo", "castillo")
                            utils.loading_screen(self.screen)
                            self.next_level = 10

    def render_scene(self, number):
        if number == 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[number-1] = 1
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif 1 < number < 5:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.background_2, (0, 0))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif 4 < number < 10:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.background_3, (0, 0))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
