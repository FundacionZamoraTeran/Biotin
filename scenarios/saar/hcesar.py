import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from actors.player import Player
from actors.prompt import Prompt


class Hcesar:
    """
        Class representing Cesar's house recieves
        a Surface as a screen, and a Clock as clock, and a save slot name
    """
    def __init__(self, screen, clock, character):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.background = utils.load_image("background.png", "saar/stage_1/hcesar")
        self.character = character
        self.interact = Prompt(self.screen,
                               self.clock,
                               (735, 280),
                               "interact.png",
                               "saar",
                               (150, 350))

        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (60, 380),
                                 "interact.png",
                                 "saar",
                                 (250, 450))

        self.player = Player(self.screen,
                             self.clock,
                             (80, 500),
                             self.character,
                             1200)
        self.current_slide = 1
        self.played = [0] * 14
        self.father = utils.load_image("happy.png", "npc/fcesar")
        self.conversation = {
            "1" : utils.load_image("d1.png", "saar/stage_1/hcesar"),
            "2" : utils.load_image("d2.png", "saar/stage_1/hcesar"),
            "3" : utils.load_image("d3.png", "saar/stage_1/hcesar"),
            "4" : utils.load_image("d4.png", "saar/stage_1/hcesar"),
            "5" : utils.load_image("d5.png", "saar/stage_1/hcesar"),
            "6" : utils.load_image("d6.png", "saar/stage_1/hcesar"),
            "7" : utils.load_image("d7.png", "saar/stage_1/hcesar"),
            "8" : utils.load_image("d8.png", "saar/stage_1/hcesar"),
            "9" : utils.load_image("d9.png", "saar/stage_1/hcesar"),
            "10": utils.load_image("d10.png", "saar/stage_1/hcesar"),
            "11": utils.load_image("d11.png", "saar/stage_1/hcesar"),
            "12": utils.load_image("d12.png", "saar/stage_1/hcesar"),
            "13": utils.load_image("d13.png", "saar/stage_1/hcesar")
        }
        self.voices = {
            "1" : utils.load_vx("saar/hcesar/1.ogg"),
            "2" : utils.load_vx("saar/hcesar/2.ogg"),
            "3" : utils.load_vx("saar/hcesar/3.ogg"),
            "4" : utils.load_vx("saar/hcesar/4.ogg"),
            "5" : utils.load_vx("saar/hcesar/5.ogg"),
            "6" : utils.load_vx("saar/hcesar/6.ogg"),
            "7" : utils.load_vx("saar/hcesar/7.ogg"),
            "8" : utils.load_vx("saar/hcesar/8.ogg"),
            "9" : utils.load_vx("saar/hcesar/9.ogg"),
            "10": utils.load_vx("saar/hcesar/10.ogg"),
            "11": utils.load_vx("saar/hcesar/11.ogg"),
            "12": utils.load_vx("saar/hcesar/12.ogg"),
            "13": utils.load_vx("saar/hcesar/13.ogg")
        }

        self.biotin = {
            "diego": utils.load_image("down1.png", "diego"),
            "ena": utils.load_image("down1.png", "ena"),
            "ezer": utils.load_image("down1.png", "ezer"),
            "cesar": utils.load_image("down1.png", "cesar")
        }

        self.next = Button((1038, 780), "hcesar/next1.png", "hcesar/next2.png", 123, 94, "saar/stage_1")
        self.prev = Button((55, 780), "hcesar/prev1.png", "hcesar/prev2.png", 123, 94, "saar/stage_1")

    def run(self):
        utils.load_bg("house.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.father, (750, 370))
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
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                        elif self.current_slide < 15:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                        elif self.current_slide > 1 and self.current_slide < 14:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 14:
                            self.vx_channel.stop()
                            self.current_slide = 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 1:
                            if (self.player.rect.x+self.player.rect.width > 720 and
                                    self.player.rect.x+self.player.rect.width < 865
                                    and self.current_slide == 1):
                                self.current_slide += 1
                            if (self.player.rect.x+self.player.rect.width > 45
                                    and self.player.rect.x+self.player.rect.width < 175):
                                running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"
        utils.loading_screen(self.screen)

    def render_scene(self, number):
        if number == 1:
            self.arrange_team(number)
            if (self.player.rect.x+self.player.rect.width > 720
                    and self.player.rect.x+self.player.rect.width < 865):
                self.interact.float(0)
            if (self.player.rect.x+self.player.rect.width > 45
                    and self.player.rect.x+self.player.rect.width < 175):
                self.interact_2.float(0)
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[1] = 1
            self.arrange_team(number)
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number < 15:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.arrange_team(number)
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def arrange_team(self, number):
        if self.character == "ena":
            self.screen.blit(self.biotin["ezer"], (420, 495))
            self.screen.blit(self.biotin["cesar"], (500, 500))
            self.screen.blit(self.biotin["diego"], (330, 480))
            if number == 1: # this check exist to blit the static image when the dialogue appears
                self.player.update()
            else:
                self.screen.blit(self.biotin["ena"], self.player.rect.topleft)
        elif self.character == "ezer":
            self.screen.blit(self.biotin["ena"], (420, 495))
            self.screen.blit(self.biotin["cesar"], (500, 500))
            self.screen.blit(self.biotin["diego"], (330, 480))
            if number == 1:
                self.player.update()
            else:
                self.screen.blit(self.biotin["ezer"], self.player.rect.topleft)
        elif self.character == "diego":
            self.screen.blit(self.biotin["cesar"], (420, 495))
            self.screen.blit(self.biotin["ena"], (500, 500))
            self.screen.blit(self.biotin["ezer"], (330, 480))
            if number == 1:
                self.player.update()
            else:
                self.screen.blit(self.biotin["diego"], self.player.rect.topleft)
        elif self.character == "cesar":
            self.screen.blit(self.biotin["diego"], (420, 495))
            self.screen.blit(self.biotin["ezer"], (500, 500))
            self.screen.blit(self.biotin["ena"], (330, 480))
            if number == 1:
                self.player.update()
            else: 
                self.screen.blit(self.biotin["cesar"], self.player.rect.topleft)
