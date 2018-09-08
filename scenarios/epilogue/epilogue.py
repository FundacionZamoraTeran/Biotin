import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.epilogue import end

class Epilogue:
    """
        Class representing the epilogue of the game, recieves
        a Surface as a screen, and a Clock as clock, and a slot name
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
        self.selected_food = self.slot["food"]["base"]
        self.background_1 = utils.load_image("background1.png", "epilogue/epilogue")
        self.background_2 = utils.load_image("background2.png", "epilogue/epilogue")
        self.background_3 = utils.load_image("background3.png", "epilogue/epilogue")
        self.next_level = 1
        self.frame = 0
        self.current_slide = 1
        self.played = [0] * 13
        self.conversation = {
            "1" : utils.load_image("d1.png", "epilogue/epilogue/dialogue"),
            "2" : utils.load_image("d2.png", "epilogue/epilogue/dialogue"),
            "3" : utils.load_image("d3.png", "epilogue/epilogue/dialogue"),
            "4" : utils.load_image("d4.png", "epilogue/epilogue/dialogue"),
            "5" : utils.load_image("d5.png", "epilogue/epilogue/dialogue"),
            "6" : utils.load_image("d6.png", "epilogue/epilogue/dialogue"),
            "7" : utils.load_image("d7.png", "epilogue/epilogue/dialogue"),
            "8" : utils.load_image("d8.png", "epilogue/epilogue/dialogue"),
            "9" : utils.load_image("d9.png", "epilogue/epilogue/dialogue"),
            "10" : utils.load_image("d10.png", "epilogue/epilogue/dialogue"),
            "11" : utils.load_image("d11.png", "epilogue/epilogue/dialogue"),
            "12" : utils.load_image("d12.png", "epilogue/epilogue/dialogue"),
            "13" : utils.load_image("d13.png", "epilogue/epilogue/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("epilogue/epilogue/1.ogg"),
            "2" : utils.load_vx("epilogue/epilogue/2.ogg"),
            "3" : utils.load_vx("epilogue/epilogue/3.ogg"),
            "4" : utils.load_vx("epilogue/epilogue/4.ogg"),
            "5" : utils.load_vx("epilogue/epilogue/5.ogg"),
            "7" : utils.load_vx("epilogue/epilogue/7.ogg"),
            "8" : utils.load_vx("epilogue/epilogue/8.ogg"),
            "9" : utils.load_vx("epilogue/epilogue/9.ogg"),
            "10" : utils.load_vx("epilogue/epilogue/10.ogg"),
            "11" : utils.load_vx("epilogue/epilogue/11.ogg"),
            "12" : utils.load_vx("epilogue/epilogue/12.ogg"),
            "13" : utils.load_vx("epilogue/epilogue/13.ogg")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "epilogue")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "epilogue")

    def run(self):
        utils.load_bg("house.ogg")
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
                        if self.current_slide < 13:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 13:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            endo = end.End(self.screen, self.clock, self.selected_food)
                            endo.run()
                            self.next_level = endo.next_level
                            del endo
                            running = False

    def render_scene(self, number):
        if number == 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[number-1] = 1
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif 1 < number < 6:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 6:
            self.screen.blit(self.background_2, (0, 0))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif 6 < number < 12:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.background_2, (0, 0))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif 11 < number < 14:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.background_3, (0, 0))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
