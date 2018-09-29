import sys
import random
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from actors.thrower import Thrower
from actors.pilori import Pilori
from actors.projectile import Projectile

class Game:
    """
        Class representing the first battle with pilori, recieves
        a Surface as a screen, and a Clock as clock, and a character name
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.character = character
        self.background = utils.load_image("background.png", "castle/game")
        self.background_1 = utils.load_image("background1.png", "castle/game")
        self.help = utils.load_image("help.png", "castle/game")
        self.congrats = utils.load_image("congrats.png", "castle/game")
        self.player = Thrower(self.screen,
                             self.clock,
                             (150, 700))
        self.pilori = Pilori(self.screen,
                             self.clock,
                             (550, 130),
                             (0, 1159))
        self.current_slide = 1
        self.played = [0] * 10
        self.conversation = {
            "1" : utils.load_image("d1.png", "castle/game/dialogue"),
            "2" : utils.load_image("d2.png", "castle/game/dialogue"),
            "3" : utils.load_image("d3.png", "castle/game/dialogue"),
            "4" : utils.load_image("d4.png", "castle/game/dialogue"),
            "5" : utils.load_image("d5.png", "castle/game/dialogue"),
            "6" : utils.load_image("d6.png", "castle/game/dialogue"),
            "7" : utils.load_image("d7.png", "castle/game/dialogue")
        }

        self.hp_bar = {
            "0" : utils.load_image("0.png", "castle/game/hp_bar"),
            "1" : utils.load_image("1.png", "castle/game/hp_bar"),
            "2" : utils.load_image("2.png", "castle/game/hp_bar"),
            "3" : utils.load_image("3.png", "castle/game/hp_bar"),
            "4" : utils.load_image("4.png", "castle/game/hp_bar"),
            "5" : utils.load_image("5.png", "castle/game/hp_bar"),
            "6" : utils.load_image("6.png", "castle/game/hp_bar"),
            "7" : utils.load_image("7.png", "castle/game/hp_bar"),
            "8" : utils.load_image("8.png", "castle/game/hp_bar"),
            "9" : utils.load_image("9.png", "castle/game/hp_bar"),
            "10" : utils.load_image("10.png", "castle/game/hp_bar"),
        }

        self.voices = {
            "1" : utils.load_vx("castle/game/1.ogg"),
            "2" : utils.load_vx("castle/game/2.ogg"),
            "3" : utils.load_vx("castle/game/3.ogg"),
            "4" : utils.load_vx("castle/game/4.ogg"),
            "5" : utils.load_vx("castle/game/5.ogg"),
            "6" : utils.load_vx("castle/game/6.ogg"),
            "7" : utils.load_vx("castle/game/7.ogg")
        }

        self.food = Projectile(self.screen, self.clock, (self.player.rect.center), "15.png", "castle/game/food")
        self.pilori.projectile = self.food
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "space")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "space")

    def run(self):
        utils.load_bg("masakh.ogg")
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
                        if self.current_slide == 2:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                        elif 4 < self.current_slide < 17:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-3] = 0
                            self.current_slide -= 1

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.next.on_press(self.screen)
                            self.current_slide = 2
                        elif self.current_slide == 2:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                        elif self.current_slide == 3:
                            self.next.on_press(self.screen)
                            self.current_slide = 4
                        elif self.current_slide < 10:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-3] = 0
                            self.current_slide += 1
                        elif self.current_slide == 10:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            running = False
                    elif (event.key == pygame.K_SPACE or event.key == consts.K_SQUARE):
                        if self.current_slide == 2:
                            self.food.throw = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 2:
                            self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 2:
                            self.player.direction = "stand"

    def render_scene(self, number):
        if number == 1:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.help, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 2:
            self.screen.blit(self.background, (0, 0))
            self.actors_load()
        elif number == 3:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.congrats, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 4:
            if self.played[number-3] == 0:
                self.vx_channel.play(self.voices[str(number-3)])
                self.played[number-3] = 1
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.conversation[str(number-3)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif 4 < number < 11:
            if self.played[number-3] == 0:
                self.vx_channel.play(self.voices[str(number-3)])
                self.played[number-3] = 1
            self.screen.blit(self.background_1, (0, 0))
            self.screen.blit(self.conversation[str(number-3)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def actors_load(self):
        if self.pilori.health > 0:
            self.pilori.move()
            if self.pilori.health == 16:
                self.screen.blit(self.hp_bar["10"], (665, 16))
            elif self.pilori.health > 14:
                self.screen.blit(self.hp_bar["9"], (665, 16))
            elif self.pilori.health > 12:
                self.screen.blit(self.hp_bar["8"], (665, 16))
            elif self.pilori.health > 10:
                self.screen.blit(self.hp_bar["7"], (665, 16))
            elif self.pilori.health > 8:
                self.screen.blit(self.hp_bar["6"], (665, 16))
            elif self.pilori.health > 6:
                self.screen.blit(self.hp_bar["5"], (665, 16))
            elif self.pilori.health > 4:
                self.screen.blit(self.hp_bar["4"], (665, 16))
            elif self.pilori.health > 2:
                self.screen.blit(self.hp_bar["2"], (665, 16))
            elif self.pilori.health > 0:
                self.screen.blit(self.hp_bar["1"], (665, 16))
            self.pilori.move()
            self.food.update()
            self.player.update()
            if not self.food.throw:
                self.food.rect.center = self.player.rect.center
        else:
            self.current_slide = 3
