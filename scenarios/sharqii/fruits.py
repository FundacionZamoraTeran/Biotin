import sys
import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils.button import Button
from scenarios.sharqii import dairy
from actors.player import Player
from actors.prompt import Prompt

class Fruit:
    """
        Class representing the third stage of Saar village, recieves
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
        self.background = utils.load_image("background.png", "sharqii/fruits")
        self.background_width = self.background.get_size()[0]
        self.interact = Prompt(self.screen,
                               self.clock,
                               (1387, 380),
                               "banana.png",
                               "sharqii/fruits/prompts",
                               (250, 500))
        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (1542, 480), #prompt width/2  +10
                                 "watermelon.png",
                                 "sharqii/fruits/prompts",
                                 (400, 600))
        self.interact_3 = Prompt(self.screen,
                                 self.clock,
                                 (1787, 480),
                                 "lemon.png",
                                 "sharqii/fruits/prompts",
                                 (400, 600))
        self.interact_4 = Prompt(self.screen,
                                 self.clock,
                                 (1917, 480),
                                 "orange.png",
                                 "sharqii/fruits/prompts",
                                 (400, 600))
        self.interact_5 = Prompt(self.screen,
                                 self.clock,
                                 (680, 480),
                                 "key.png",
                                 "sharqii/fruits/prompts",
                                 (400, 600))#this is the key part
        self.interact_6 = Prompt(self.screen,
                                 self.clock,
                                 (2280, 480),
                                 "interact.png",
                                 "sharqii",
                                 (400, 600))

        self.player = Player(self.screen,
                             self.clock,
                             (150, 530),
                             self.character,
                             2400,
                             True)
        self.current_slide = 1
        self.played = [0] * 8
        self.conversation = {
            "1" : utils.load_image("d1.png", "sharqii/fruits/"),
            "2" : utils.load_image("d2.png", "sharqii/fruits/"),
            "3" : utils.load_image("d3.png", "sharqii/fruits/"),
            "4" : utils.load_image("banana.png", "sharqii/fruits/"),
            "5" : utils.load_image("watermelon.png", "sharqii/fruits/"),
            "6" : utils.load_image("lemon.png", "sharqii/fruits/"),
            "7" : utils.load_image("orange.png", "sharqii/fruits/"),
            "8" : utils.load_image("key.png", "sharqii/fruits/")
        }
        self.voices = {
            "1" : utils.load_vx("sharqii/fruits/1.ogg"),
            "2" : utils.load_vx("sharqii/fruits/2.ogg"),
            "3" : utils.load_vx("sharqii/fruits/3.ogg"),
            "4" : utils.load_vx("sharqii/fruits/a2.ogg"),
            "5" : utils.load_vx("sharqii/fruits/a1.ogg"),
            "6" : utils.load_vx("sharqii/fruits/a3.ogg"),
            "7" : utils.load_vx("sharqii/fruits/a4.ogg")
        }
        self.biotin = {
            "diego": utils.load_image("down1.png", "diego"),
            "ena": utils.load_image("down1.png", "ena"),
            "ezer": utils.load_image("down1.png", "ezer"),
            "cesar": utils.load_image("down1.png", "cesar")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "sharqii")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "sharqii")
        self.visited = [False] * 5

    def run(self):
        utils.load_bg("bazar.ogg")
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
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[0] = 0
                            self.current_slide = 9
                        elif self.current_slide < 4:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif 3 < self.current_slide < 9:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide = 9
                        elif self.current_slide == 9:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 3:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif 2 < self.current_slide < 9:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide = 9
                        elif self.current_slide == 9:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 9:
                            if (self.player.real_x+self.player.rect.width > 1372
                                    and self.player.real_x+self.player.rect.width < 1533):
                                self.current_slide = 4
                                self.visited[0] = True
                            elif (self.player.real_x+self.player.rect.width > 1627
                                  and self.player.real_x+self.player.rect.width < 1778):
                                self.current_slide = 5
                                self.visited[1] = True
                            elif (self.player.real_x+self.player.rect.width > 1772
                                  and self.player.real_x+self.player.rect.width < 1900):
                                self.current_slide = 6
                                self.visited[2] = True
                            elif (self.player.real_x+self.player.rect.width > 1902
                                  and self.player.real_x+self.player.rect.width < 2060):
                                self.current_slide = 7
                                self.visited[3] = True
                            elif (self.player.real_x+self.player.rect.width > 650
                                  and self.player.real_x+self.player.rect.width < 796
                                  and len(filter(lambda x: x is False, self.visited)) == 1):
                                self.current_slide = 8
                                self.visited[4] = True
                            elif (self.player.real_x+self.player.rect.width > 2280
                                  and self.player.real_x+self.player.rect.width < 2401 and
                                  all(i is True for i in self.visited)):
                                utils.loading_screen(self.screen)
                                dai = dairy.Dairy(self.screen, self.clock, self.character)
                                dai.run()
                                del dai
                                running = False
                    elif ((event.key == pygame.K_SPACE or event.key == consts.K_CROSS) and
                          (self.player.jumping is False and self.player.jump_frames == 0)):
                        if self.current_slide == 9:
                            self.player.jumping = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 9:
                            self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 9:
                            self.player.direction = "stand"
    def render_scene(self, number, rel_x):
        if 1 <= number < 8:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number)])
                self.played[number-1] = 1
            self.actors_load(number, rel_x)
            self.screen.blit(self.conversation[str(number)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 8:
            self.actors_load(number, rel_x)
            self.screen.blit(self.conversation["8"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
        elif number == 9:
            self.actors_load(number, rel_x)

    def actors_load(self, number, rel_x):
        if (self.player.real_x+self.player.rect.width > 1372
                and self.player.real_x+self.player.rect.width < 1533):
            self.interact.float(rel_x)
        elif (self.player.real_x+self.player.rect.width > 1627
              and self.player.real_x+self.player.rect.width < 1778):
            self.interact_2.float(rel_x)
        elif (self.player.real_x+self.player.rect.width > 1772
              and self.player.real_x+self.player.rect.width < 1900):
            self.interact_3.float(rel_x)
        elif (self.player.real_x+self.player.rect.width > 1902
              and self.player.real_x+self.player.rect.width < 2060):
            self.interact_4.float(1200)
        elif (self.player.real_x+self.player.rect.width > 650
              and self.player.real_x+self.player.rect.width < 796
              and len(filter(lambda x: x is False, self.visited)) == 1):
            self.interact_5.float(rel_x)
        elif (self.player.real_x+self.player.rect.width > 2280
              and self.player.real_x+self.player.rect.width < 2401 and
              all(i is True for i in self.visited)):
            self.interact_6.float(1200)
        self.arrange_team(number, rel_x)

    def arrange_team(self, number, rel_x):
        if self.character == "ena":
            self.screen.blit(self.biotin["ezer"], (420-rel_x, 495))
            self.screen.blit(self.biotin["cesar"], (500-rel_x, 500))
            self.screen.blit(self.biotin["diego"], (330-rel_x, 480))
            if number == 9: # this check exist to blit the static image when the dialogue appears
                self.player.update()
            else:
                self.screen.blit(self.biotin["ena"], self.player.rect.topleft)
        elif self.character == "ezer":
            self.screen.blit(self.biotin["ena"], (420-rel_x, 495))
            self.screen.blit(self.biotin["cesar"], (500-rel_x, 500))
            self.screen.blit(self.biotin["diego"], (330-rel_x, 480))
            if number == 9:
                self.player.update()
            else:
                self.screen.blit(self.biotin["ezer"], self.player.rect.topleft)
        elif self.character == "diego":
            self.screen.blit(self.biotin["cesar"], (400-rel_x, 495))
            self.screen.blit(self.biotin["ena"], (480-rel_x, 500))
            self.screen.blit(self.biotin["ezer"], (310-rel_x, 480))
            if number == 9:
                self.player.update()
            else:
                self.screen.blit(self.biotin["diego"], self.player.rect.topleft)
        elif self.character == "cesar":
            self.screen.blit(self.biotin["diego"], (420-rel_x, 495))
            self.screen.blit(self.biotin["ezer"], (500-rel_x, 500))
            self.screen.blit(self.biotin["ena"], (330-rel_x, 480))
            if number == 9:
                self.player.update()
            else: 
                self.screen.blit(self.biotin["cesar"], self.player.rect.topleft)
