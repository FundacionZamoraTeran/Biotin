import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.luis import stomach

class Descend:
    """
        Class representing the descend to Luis stomach, recieves
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
        self.background_1 = utils.load_image("background1.png", "luis/descend")
        self.background_2 = utils.load_image("background2.png", "luis/descend")
        self.next_level = 1
        self.frame = 0
        self.current_slide = 1
        self.played = [0] * 2

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
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.next.on_press(self.screen)
                            self.current_slide = 2
                        elif self.current_slide == 2:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            sto = stomach.Stomach(self.screen, self.clock, self.character)
                            sto.run()
                            del sto
                            running = False
                            if not self.slot["stages"]["completado"] is True:
                                    saves.save(self.slotname, 10, "Completado", "completado")
                            utils.loading_screen(self.screen)
                            self.next_level = 11

    def render_scene(self, number):
        if number == 1:
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 2:
            self.screen.blit(self.background_2, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
