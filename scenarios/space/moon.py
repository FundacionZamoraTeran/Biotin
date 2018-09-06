import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from actors.player import Player
from actors.prompt import Prompt

class Moon:
    """
        Class representing the moon and lab stage of Space, recieves
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
        self.background = utils.load_image("background.png", "space/moon")
        self.background_width = self.background.get_size()[0]
        self.interact = Prompt(self.screen,
                               self.clock,
                               (1830, 420),
                               "interact.png",
                               "space",
                               (250, 500))

        self.player = Player(self.screen,
                             self.clock,
                             (150, 530),
                             self.character,
                             2400,
                             True)
        self.current_slide = 1
        self.frame = 0
        self.played = [0] * 17
        self.conversation = {
            "1" : utils.load_image("d1.png", "space/moon/"),
            "2" : utils.load_image("d2.png", "space/moon/"),
            "3" : utils.load_image("d3.png", "space/moon/"),
            "4" : utils.load_image("d4.png", "space/moon/"),
            "5" : utils.load_image("d5.png", "space/moon/"),
            "6" : utils.load_image("d6.png", "space/moon/"),
            "7" : utils.load_image("d7.png", "space/moon/"),
            "8" : utils.load_image("d8.png", "space/moon/"),
            "9" : utils.load_image("d9.png", "space/moon/"),
            "10" : utils.load_image("d10.png", "space/moon/"),
            "11" : utils.load_image("d11.png", "space/moon/"),
            "12" : utils.load_image("d12.png", "space/moon/"),
            "13" : utils.load_image("d13.png", "space/moon/"),
            "14" : utils.load_image("d14.png", "space/moon/"),
            "15" : utils.load_image("d15.png", "space/moon/"),
            "16" : utils.load_image("d16.png", "space/moon/")

        }
        self.voices = {
            "1" : utils.load_vx("space/moon/1.ogg"),
            "2" : utils.load_vx("space/moon/2.ogg"),
            "3" : utils.load_vx("space/moon/3.ogg"),
            "4" : utils.load_vx("space/moon/4.ogg"),
            "5" : utils.load_vx("space/moon/5.ogg"),
            "6" : utils.load_vx("space/moon/6.ogg"),
            "7" : utils.load_vx("space/moon/7.ogg"),
            "8" : utils.load_vx("space/moon/8.ogg"),
            "9" : utils.load_vx("space/moon/9.ogg"),
            "10" : utils.load_vx("space/moon/10.ogg"),
            "11" : utils.load_vx("space/moon/11.ogg"),
            "12" : utils.load_vx("space/moon/12.ogg"),
            "13" : utils.load_vx("space/moon/13.ogg"),
            "14" : utils.load_vx("space/moon/14.ogg"),
            "15" : utils.load_vx("space/moon/15.ogg"),
            "16" : utils.load_vx("space/moon/16.ogg")
        }

        self.portal = {
            "0" : utils.load_image("portal1.png", "space/moon/"),
            "1" : utils.load_image("portal2.png", "space/moon/"),
        }

        self.bars = utils.load_image("bars.png", "space/moon/")

        self.biotin = utils.load_image("team.png", "space/moon/")
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "space")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "space")

    def run(self):
        utils.load_bg("space.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.render_scene(self.current_slide, abs(rel_x))
            else:
                self.screen.blit(self.background, (rel_x - self.background_width, 0))
                self.render_scene(self.current_slide, rel_x)
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
                        elif 2< self.current_slide < 17:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1

                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                        elif self.current_slide < 16:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 16:
                            utils.loading_screen(self.screen)
                            running = False
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 1:
                            if (self.player.real_x+self.player.rect.width > 1815
                                    and self.player.real_x+self.player.rect.width < 1976):
                                self.current_slide = 2
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        if self.current_slide == 1:
                            self.player.jumping = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 1:
                            self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.player.direction = "stand"
    def render_scene(self, number, rel_x):
        if number == 1:
            self.actors_load(rel_x)
        elif 1 < number < 11:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.biotin, (300, 520))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 11:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.biotin, (300, 520))
            self.screen.blit(self.bars, (865, 610))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif 11 < number < 17:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.render_portal(rel_x)
            self.screen.blit(self.biotin, (300, 520))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def actors_load(self, rel_x):
        if (self.player.real_x+self.player.rect.width > 1815
                and self.player.real_x+self.player.rect.width < 1976):
            self.interact.float(rel_x)
        self.player.update()
    def render_portal(self, rel_x):
        self.frame += 1
        if self.frame > 3:
            self.frame = 0
        self.screen.blit(self.portal[str(self.frame//2)], (1750-rel_x, 0))
