import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.space import asteroid
#from scenarios.space import island
from actors.boat import Boat
from actors.prompt import Prompt

class River:
    """
        Class representing the first part of the space/river, recieves
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
        self.next_level = 1
        self.character = "ena" if self.slot["team_ena"] is True else "diego"
        self.background = utils.load_image("background.png", "space/river")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (15, 230),
                               "interact.png",
                               "space",
                               (150, 300))
        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (1065, 230),
                                 "interact.png",
                                 "space",
                                 (150, 300))
        self.player = Boat(self.screen,
                           self.clock,
                           (450, 300),
                           "sboat")
        self.boat = utils.load_image("right1.png", "sboat")

        self.current_slide = 1
        self.played = [0] * 7
        self.conversation = {
            "1" : utils.load_image("d1.png", "space/river/dialogue"),
            "2" : utils.load_image("d2.png", "space/river/dialogue"),
            "3" : utils.load_image("d3.png", "space/river/dialogue"),
            "4" : utils.load_image("d4.png", "space/river/dialogue"),
            "5" : utils.load_image("d5.png", "space/river/dialogue"),
            "6" : utils.load_image("d6.png", "space/river/dialogue"),
            "7" : utils.load_image("d7.png", "space/river/dialogue")
        }
        self.voices = {
            "1" : utils.load_vx("space/river/1.ogg"),
            "2" : utils.load_vx("space/river/2.ogg"),
            "3" : utils.load_vx("space/river/3.ogg"),
            "4" : utils.load_vx("space/river/4.ogg"),
            "5" : utils.load_vx("space/river/5.ogg"),
            "6" : utils.load_vx("space/river/6.ogg"),
            "7" : utils.load_vx("space/river/7.ogg")
        }
        self.strong = False
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "space")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "space")

    def run(self):
        utils.load_bg("space.ogg")
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
                        if 1 < self.current_slide < 8:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 8:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if  self.current_slide < 8:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 8:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 8:
                            if -100 < self.player.rect.left < 200:
                                utils.loading_screen(self.screen)
                                ast = asteroid.Asteroid(self.screen, self.clock, self.character)
                                ast.run()
                                del ast
                                self.strong = True
                                self.player.character = "hboat"
                                self.player.update_sprites()
                                self.player.velocity = abs(self.player.velocity)
                            if (950 < self.player.rect.right < 1300) and self.strong:
                                pass
                                # utils.loading_screen(self.screen)
                                # isl = last.Last(self.screen, self.clock, self.character)
                                # isl.run()
                                # del isl
                                # running = False
                                # utils.loading_screen(self.screen)
                                # #save here
                                # if not self.slot["stages"]["espacio"] is True:
                                #     saves.save(self.slotname, 7, "El Espacio", "espacio")
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.catching is False)):
                        if self.current_slide == 8:
                            self.player.catching = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 8:
                            self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 8:
                            self.player.direction = "stand"
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.catching is True)):
                        if self.current_slide == 8:
                            self.player.catching = False
    def render_scene(self, number):
        if number == 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[number-1] = 1
            self.screen.blit(self.boat, (450, 300))
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif 1 < number < 8:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.screen.blit(self.boat, (450, 300))
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 8:
            self.actors_load()

    def actors_load(self):
        if self.player.rect.right > 900 and not self.strong:
            self.player.rect.right = 900
        elif self.player.rect.right > 900:
            self.player.rect.y = 250
        if not self.strong:
            self.player.rect.x -= 30
            if self.player.rect.x < 100:
                self.player.rect.x = 100
        else:
            self.player.rect.y = self.player.y
        if (-100 < self.player.rect.left < 200):
            self.interact.float(0)
        elif (950 < self.player.rect.right < 1300):
            self.interact_2.float(0)
        self.player.update()
