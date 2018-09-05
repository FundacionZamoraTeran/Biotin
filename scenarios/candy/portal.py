import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from actors.player import Player
from actors.prompt import Prompt


class Portal:
    """
        Class representing the end portal of the candy woods, recieves
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
        self.background = utils.load_image("background.png", "candy/portal/")
        self.frame = 0
        self.player = Player(self.screen,
                             self.clock,
                             (150, 550),
                             self.character,
                             1200,
                             False)
        self.interact = Prompt(self.screen,
                               self.clock,
                               (870, 380),
                               "interact.png",
                               "candy",
                               (250, 450))
        self.current_slide = 1
        self.played = [0] * 10
        self.conversation = {
            "1" : utils.load_image("d1.png", "candy/portal/dialogue"),
            "2" : utils.load_image("d2.png", "candy/portal/dialogue"),
            "3" : utils.load_image("d3.png", "candy/portal/dialogue"),
            "4" : utils.load_image("d4.png", "candy/portal/dialogue"),
            "5" : utils.load_image("d5.png", "candy/portal/dialogue"),
            "6" : utils.load_image("d6.png", "candy/portal/dialogue"),
            "7" : utils.load_image("d7.png", "candy/portal/dialogue"),
            "8" : utils.load_image("d8.png", "candy/portal/dialogue"),
            "9" : utils.load_image("d9.png", "candy/portal/dialogue"),
            "10" : utils.load_image("d10.png", "candy/portal/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("candy/1.ogg"),
            "2" : utils.load_vx("candy/2.ogg"),
            "3" : utils.load_vx("candy/3.ogg"),
            "4" : utils.load_vx("candy/4.ogg"),
            "5" : utils.load_vx("candy/5.ogg"),
            "6" : utils.load_vx("candy/6.ogg"),
            "7" : utils.load_vx("candy/7.ogg"),
            "8" : utils.load_vx("candy/8.ogg"),
            "9" : utils.load_vx("candy/9.ogg"),
            "10" : utils.load_vx("candy/10.ogg")
        }
        self.portal = {
            "0" : utils.load_image("portal1.png", "candy/portal/"),
            "1" : utils.load_image("portal2.png", "candy/portal/"),
        }
        self.biotin = {
            "diego": utils.load_image("diego.png", "sharqii/end/"),
            "ena": utils.load_image("ena.png", "sharqii/end/"),
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "candy")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "candy")

    def run(self):
        utils.load_bg("to_space.ogg")
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
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 1:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                        elif 2 < self.current_slide < 11:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                        elif self.current_slide > 1 and self.current_slide < 10:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 10:
                            self.vx_channel.stop()
                            running = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 1:
                            if (self.player.rect.x+self.player.rect.width > 755
                                    and self.player.rect.x+self.player.rect.width < 885):
                                self.current_slide = 2
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        if self.current_slide == 1:
                            self.player.jumping = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"

    def render_scene(self, number):
        if number == 1:
            self.render_portal()
            self.arrange_team()
            if (self.player.rect.x+self.player.rect.width > 755
                    and self.player.rect.x+self.player.rect.width < 885):
                self.interact.float(0)
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[1] = 1
            self.screen.blit(self.portal["0"], (600, 0))
            self.arrange_team()
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number < 11:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.screen.blit(self.portal["0"], (600, 0))
            self.arrange_team()
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def arrange_team(self):
        if self.character == "ena":
            self.screen.blit(self.biotin["ena"], (420, 495))
            self.player.update()
        elif self.character == "ezer":
            self.screen.blit(self.biotin["ena"], (420, 495))
            self.player.update()
        elif self.character == "diego":
            self.screen.blit(self.biotin["diego"], (400, 495))
            self.player.update()
        elif self.character == "cesar":
            self.screen.blit(self.biotin["diego"], (420, 495))
            self.player.update()
    def render_portal(self):
        self.frame += 1
        if self.frame > 3:
            self.frame = 0
        self.screen.blit(self.portal[str(self.frame//2)], (600, 0))
