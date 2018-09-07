import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.city import city


class Fall:
    """
        Class representing the beginning of the royal city scenario, recieves
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
        self.background = utils.load_image("background.png", "city/fall/")
        self.plant = utils.load_image("plant.png", "city/fall/")
        self.next_level = 1
        self.frame = 0
        self.current_slide = 1
        self.played = [0] * 21
        self.conversation = {
            "1" : utils.load_image("d1.png", "city/fall/dialogue"),
            "2" : utils.load_image("d2.png", "city/fall/dialogue"),
            "3" : utils.load_image("d3.png", "city/fall/dialogue"),
            "4" : utils.load_image("d4.png", "city/fall/dialogue"),
            "5" : utils.load_image("d5.png", "city/fall/dialogue"),
            "6" : utils.load_image("d6.png", "city/fall/dialogue"),
            "7" : utils.load_image("d7.png", "city/fall/dialogue"),
            "8" : utils.load_image("d8.png", "city/fall/dialogue"),
            "9" : utils.load_image("d9.png", "city/fall/dialogue"),
            "10" : utils.load_image("d10.png", "city/fall/dialogue"),
            "11" : utils.load_image("d11.png", "city/fall/dialogue"),
            "12" : utils.load_image("d12.png", "city/fall/dialogue"),
            "13" : utils.load_image("d13.png", "city/fall/dialogue"),
            "14" : utils.load_image("d14.png", "city/fall/dialogue"),
            "15" : utils.load_image("d15.png", "city/fall/dialogue"),
            "16" : utils.load_image("d16.png", "city/fall/dialogue"),
            "17" : utils.load_image("d17.png", "city/fall/dialogue"),
            "18" : utils.load_image("d18.png", "city/fall/dialogue"),
            "19" : utils.load_image("d19.png", "city/fall/dialogue"),
            "20" : utils.load_image("d20.png", "city/fall/dialogue"),
            "21" : utils.load_image("d21.png", "city/fall/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("city/fall/1.ogg"),
            "2" : utils.load_vx("city/fall/2.ogg"),
            "3" : utils.load_vx("city/fall/3.ogg"),
            "4" : utils.load_vx("city/fall/4.ogg"),
            "5" : utils.load_vx("city/fall/5.ogg"),
            "6" : utils.load_vx("city/fall/6.ogg"),
            "7" : utils.load_vx("city/fall/7.ogg"),
            "8" : utils.load_vx("city/fall/8.ogg"),
            "9" : utils.load_vx("city/fall/9.ogg"),
            "10" : utils.load_vx("city/fall/10.ogg"),
            "11" : utils.load_vx("city/fall/11.ogg"),
            "12" : utils.load_vx("city/fall/12.ogg"),
            "13" : utils.load_vx("city/fall/13.ogg"),
            "14" : utils.load_vx("city/fall/14.ogg"),
            "15" : utils.load_vx("city/fall/15.ogg"),
            "16" : utils.load_vx("city/fall/16.ogg"),
            "17" : utils.load_vx("city/fall/17.ogg"),
            "18" : utils.load_vx("city/fall/18.ogg"),
            "19" : utils.load_vx("city/fall/19.ogg"),
            "20" : utils.load_vx("city/fall/20.ogg"),
            "21" : utils.load_vx("city/fall/21.ogg")
        }

        self.portal = {
            "0" : utils.load_image("portal1.png", "city/fall/"),
            "1" : utils.load_image("portal2.png", "city/fall/"),
        }
        self.biotin = {
            "fall": utils.load_image("fall.png", "city/fall/"),
            "team": utils.load_image("team.png", "city/fall/"),
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "city")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "city")

    def run(self):
        utils.load_bg("al_mohren.ogg")
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
                        if 1 < self.current_slide < 22:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-2] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 21:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-2] = 0
                            self.current_slide += 1
                        elif self.current_slide == 21:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            cit = city.City(self.screen, self.clock, self.character)
                            cit.run()
                            del cit
                            running = False
                            utils.loading_screen(self.screen)
                            # save here
                            if not self.slot["stages"]["ciudad"] is True:
                                saves.save(self.slotname, 6, "Al Mohren", "ciudad")

    def render_scene(self, number):
        if number == 1:
            self.render_portal()
            self.screen.blit(self.biotin["fall"], (250, 237))
            self.screen.blit(self.plant, (100, 587))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number < 4:
            if self.played[number-2] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-2] = 1
            self.render_portal()
            self.screen.blit(self.biotin["fall"], (250, 237))
            self.screen.blit(self.plant, (100, 587))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 12:
            self.screen.blit(self.biotin["team"], (360, 417))
            self.screen.blit(self.plant, (100, 587))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number < 22:
            if self.played[number-2] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-2] = 1
            self.screen.blit(self.biotin["team"], (360, 417))
            self.screen.blit(self.plant, (100, 587))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
    def render_portal(self):
        self.frame += 1
        if self.frame > 3:
            self.frame = 0
        self.screen.blit(self.portal[str(self.frame//2)], (0, 0))
