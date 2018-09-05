import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.sharqii import extra
from actors.player import Player
from actors.prompt import Prompt


class End:
    """
        Class representing the end of the great bazaar, recieves
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
        self.background = utils.load_image("background.png", "sharqii/end")
        self.modal = utils.load_image("modal.png", "sharqii/end")
        self.lock = utils.load_image("lock.png", "sharqii/end")
        self.player = Player(self.screen,
                             self.clock,
                             (150, 550),
                             self.character,
                             1200,
                             False)
        self.interact = Prompt(self.screen,
                                 self.clock,
                                 (540, 380),
                                 "interact.png",
                                 "sharqii",
                                 (250, 450))
        self.current_slide = 1
        self.played = [0] * 5
        self.nutriton = utils.load_image("nutriton.png", "sharqii/end")
        self.conversation = {
            "1" : utils.load_image("d1.png", "sharqii/end/"),
            "2" : utils.load_image("d2.png", "sharqii/end/"),
            "3" : utils.load_image("d3.png", "sharqii/end/"),
            "4" : utils.load_image("d4.png", "sharqii/end/")
        }
        self.voices = {
            "1" : utils.load_vx("sharqii/end/1.ogg"),
            "2" : utils.load_vx("sharqii/end/2.ogg"),
            "3" : utils.load_vx("sharqii/end/3.ogg"),
            "4" : utils.load_vx("sharqii/end/4.ogg")
        }
        self.biotin = {
            "diego": utils.load_image("diego.png", "sharqii/end/"),
            "ena": utils.load_image("ena.png", "sharqii/end/"),
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
            self.screen.blit(self.nutriton, (725, 370))
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
                        elif 2 < self.current_slide < 6:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                        elif self.current_slide > 1 and self.current_slide < 6:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 6:
                            self.vx_channel.stop()
                            utils.loading_screen(self.screen)
                            ext = extra.Extra(self.screen, self.clock, self.character)
                            ext.run()
                            del ext
                            running = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 1:
                            if (self.player.rect.x+self.player.rect.width > 525
                                    and self.player.rect.x+self.player.rect.width < 655):
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
            self.arrange_team()
            if (self.player.rect.x+self.player.rect.width > 525
                    and self.player.rect.x+self.player.rect.width < 655):
                self.interact.float(0)
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[1] = 1
            self.arrange_team()
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 3:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.arrange_team()
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif 3 < number < 6:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.arrange_team()
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.lock, (508, 297))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 6:
            self.arrange_team()
            self.screen.blit(self.modal, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))

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
