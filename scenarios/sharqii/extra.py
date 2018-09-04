import sys
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button


class Extra:
    """
        Class representing an extra comic after the great bazar but before the next level,
        recieves a Surface as a screen, and a Clock as clock
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.character = character
        self.background = utils.load_image("background.png", "sharqii/extra")
        self.current_slide = 1
        self.played = [0] * 6
        self.conversation = {
            "1" : utils.load_image("d1.png", "sharqii/extra/"),
            "2" : utils.load_image("d2.png", "sharqii/extra/"),
            "3" : utils.load_image("d3.png", "sharqii/extra/"),
            "4" : utils.load_image("d4.png", "sharqii/extra/"),
            "5" : utils.load_image("d5.png", "sharqii/extra/"),
            "6" : utils.load_image("d6.png", "sharqii/extra/")
        }
        self.voices = {
            "1" : utils.load_vx("sharqii/extra/1.ogg"),
            "2" : utils.load_vx("sharqii/extra/2.ogg"),
            "3" : utils.load_vx("sharqii/extra/3.ogg"),
            "4" : utils.load_vx("sharqii/extra/4.ogg"),
            "5" : utils.load_vx("sharqii/extra/5.ogg"),
            "6" : utils.load_vx("sharqii/extra/6.ogg")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "sharqii")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "sharqii")

    def run(self):
        utils.load_bg("bazar.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.render_scene(self.current_slide)
            pygame.display.flip()
            self.clock.tick(consts.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if 1 < self.current_slide < 7:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 6:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 6:
                            self.vx_channel.stop()
                            running = False

    def render_scene(self, number):
        if number == 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        else:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
