import sys
import random
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from scenarios.luis import ascend
from actors.masahk import Masakh
from actors.player import Player
from actors.vitamin import Vitamin

class Game:
    """
        Class representing the final battle, recieves
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
        self.background = utils.load_image("background.png", "luis/game")
        self.help = utils.load_image("help.png", "luis/game")
        self.congrats = utils.load_image("congrats.png", "luis/game")
        self.player = Player(self.screen,
                             self.clock,
                             (240, 417),
                             self.character)
        self.masakh = Masakh(self.screen,
                             self.clock,
                             (850, 367),
                             (0, 1159))
        self.current_slide = 1
        self.played = [0] * 10
        self.conversation = {
            "1" : utils.load_image("d1.png", "luis/game/dialogue"),
            "2" : utils.load_image("d2.png", "luis/game/dialogue"),
            "3" : utils.load_image("d3.png", "luis/game/dialogue")
        }
        self.voices = {
            "0" : utils.load_vx("luis/game/0.ogg"),
            "1" : utils.load_vx("luis/game/1.ogg"),
            "2" : utils.load_vx("luis/game/2.ogg"),
            "3" : utils.load_vx("luis/game/3.ogg")
        }

        self.vitamin = Vitamin(self.screen, self.clock, (self.player.rect.center), "v1.png", "luis/game/ammo")
        self.masakh.projectile = self.vitamin
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "space")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "space")

    def run(self):
        utils.load_bg("masakh2.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True
        pygame.time.set_timer(pygame.USEREVENT+1, 6000)
        pygame.time.set_timer(pygame.USEREVENT+2, 4000)
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
                if event.type == pygame.USEREVENT+1:
                    self.masakh.mouth_open = True
                if event.type == pygame.USEREVENT+2:
                    self.masakh.mouth_open = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 2:
                            pass
                        elif 4 < self.current_slide < 7:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-3] = 0
                            self.current_slide -= 1

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.next.on_press(self.screen)
                            self.current_slide = 2
                        elif self.current_slide == 2:
                            pass
                        elif self.current_slide == 3:
                            self.next.on_press(self.screen)
                            self.current_slide = 4
                        elif self.current_slide < 6:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-3] = 0
                            self.current_slide += 1
                        elif self.current_slide == 6:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            asd = ascend.Ascend(self.screen, self.clock)
                            asd.run()
                            del asd
                            running = False
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        if self.current_slide == 2:
                            self.player.jumping = True
                    elif (event.key == pygame.K_LCTRL or event.key == consts.K_SQUARE):
                        if self.current_slide == 2:
                            self.vitamin.throw= True
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
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["0"])
                self.played[0] = 1
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.congrats, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 4:
            if self.played[number-3] == 0:
                self.vx_channel.play(self.voices[str(number-3)])
                self.played[number-3] = 1
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.conversation[str(number-3)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif 4 < number < 7:
            if self.played[number-3] == 0:
                self.vx_channel.play(self.voices[str(number-3)])
                self.played[number-3] = 1
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.conversation[str(number-3)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def actors_load(self):
        if self.masakh.health > 0:
            self.masakh.update()
            if self.masakh.jumping is False and self.masakh.jump_frames == 0:
                self.masakh.jumping = True
            self.vitamin.update()
            self.player.update()
            if not self.vitamin.throw:
                self.vitamin.rect.center = self.player.rect.center
        else:
            self.current_slide = 3
