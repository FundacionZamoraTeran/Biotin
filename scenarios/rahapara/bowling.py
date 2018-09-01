import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button

class Bowling:
    """
        Class representing Rahapara Village, recieves
        a Surface as a screen, a Clock as clock, and the save slot name
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
        self.next_level = 1

        self.background = utils.load_image("background.png", "rahapara")
        self.modal = utils.load_image("h1.png", "rahapara/help")
        self.current_slide = 1

        self.dialogue = {
            "1" : utils.load_image("d1.png", "rahapara/dialogue"),
            "2" : utils.load_image("d2.png", "rahapara/dialogue"),
            "3" : utils.load_image("d3.png", "rahapara/dialogue"),
            "4" : utils.load_image("d3.png", "rahapara/dialogue"),
            "5" : utils.load_image("d3.png", "rahapara/dialogue"),
            "6" : utils.load_image("d3.png", "rahapara/dialogue")
        }

        self.voices = {
            "1" : utils.load_vx("rahapara/dialogue/1.ogg"),
            "2" : utils.load_vx("rahapara/dialogue/2.ogg"),
            "3" : utils.load_vx("rahapara/dialogue/3.ogg"),
            "4" : utils.load_vx("rahapara/dialogue/4.ogg"),
            "5" : utils.load_vx("rahapara/dialogue/5.ogg"),
            "6" : utils.load_vx("rahapara/dialogue/6.ogg")
        }

        self.show_help = False
        self.played = [0] * 5
        self.next = Button((918, 780), "next1.png", "next2.png", 257, 99, "rahapara")
        self.prev = Button((25, 780), "prev1.png", "prev2.png", 257, 99, "rahapara")

    def run(self):
        utils.load_bg("rahapara.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            if not self.show_help:
                self.render_scene(self.current_slide)
            else:
                self.screen.blit(self.modal, (0, 0))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_END:
                        pass
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        pass
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        pass
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_PAGEUP:
                        pass
    def render_scene(self, number):
        if number == 1:
            pass
        elif number == 2:
            pass
        elif number > 2:
            pass
