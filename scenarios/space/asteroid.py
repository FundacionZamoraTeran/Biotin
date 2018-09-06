import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from actors.player import Player
from actors.prompt import Prompt

class Asteroid:
    """
        Class representing the asteroid of the space scenario, recieves
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
        self.background_1 = utils.load_image("background1.png", "space/asteroid")
        self.background_2 = utils.load_image("background2.png", "space/asteroid")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (300, 330),
                               "interact.png",
                               "space",
                               (250, 400))
        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (850, 330),
                                 "interact.png",
                                 "space",
                                 (250, 400))
        self.player = Player(self.screen,
                             self.clock,
                             (850, 450),
                             self.character,
                             1200,
                             False)

        self.current_slide = 1
        self.played = [0] * 8
        self.conversation = {
            "1" : utils.load_image("d1.png", "space/asteroid/dialogue"),
            "2" : utils.load_image("d2.png", "space/asteroid/dialogue"),
            "3" : utils.load_image("d3.png", "space/asteroid/dialogue"),
            "4" : utils.load_image("d4.png", "space/asteroid/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("space/asteroid/1.ogg"),
            "2" : utils.load_vx("space/asteroid/2.ogg"),
            "3" : utils.load_vx("space/asteroid/3.ogg"),
            "4" : utils.load_vx("space/asteroid/4.ogg")
        }
        self.visited = False
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "space")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "space")

    def run(self):
        utils.load_bg("space.ogg")
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
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 1:
                            self.current_slide = 2
                        if 2 < self.current_slide < 7:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 2:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.current_slide = 2
                        if self.current_slide == 6:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide = 2
                        elif 2 < self.current_slide < 7:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 2:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 2:
                            if 250 < self.player.rect.left < 350:
                                self.current_slide = 3
                                self.visited = True
                            if (650 < self.player.rect.left < 950) and self.visited:
                                running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 2:
                            self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 2:
                            self.player.direction = "stand"
    def render_scene(self, number):
        if number == 1:
            self.screen.blit(self.background_1, (0, 0))
        elif number == 2:
            self.screen.blit(self.background_2, (0, 0))
            self.actors_load()
        elif 2 < number < 7:
            if self.played[number-2] == 0:
                self.vx_channel.play(self.voices[str(number-2)])
                self.played[number-2] = 1
            self.screen.blit(self.conversation[str(number-2)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def actors_load(self):
        if self.player.rect.left < 50:
            self.player.rect.left = 50
        if self.player.rect.right > 850:
            self.player.rect.right = 850
        if (250 < self.player.rect.left < 350):
            self.interact.float(0)
        elif (750 < self.player.rect.right < 850) and self.visited:
            self.interact_2.float(0)
        self.player.update()
