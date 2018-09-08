import pygame

from gi.repository import Gtk
from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
#from scenarios.epilogue import end

class End:
    """
        Class representing the epilogue of the game, recieves
        a Surface as a screen, and a Clock as clock, and the selectd food
    """
    def __init__(self, screen, clock, food):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.background = utils.load_image("background.png", "epilogue/end")
        self.modal = utils.load_image("ending.png", "epilogue/end")
        self.next_level = None
        self.food = food
        self.path = "epilogue/end/"+self.food
        self.current_slide = 1
        self.played = [0] * 15
        self.conversation = {
            "1" : utils.load_image("d1.png", self.path),
            "2" : utils.load_image("d2.png", self.path),
            "3" : utils.load_image("d3.png", self.path),
            "4" : utils.load_image("d4.png", self.path),
            "5" : utils.load_image("d5.png", self.path),
            "6" : utils.load_image("d6.png", self.path),
            "7" : utils.load_image("d7.png", self.path),
            "8" : utils.load_image("d8.png", self.path),
            "9" : utils.load_image("d9.png", self.path),
            "10" : utils.load_image("d10.png", self.path),
            "11" : utils.load_image("d11.png", self.path),
            "12" : utils.load_image("d12.png", self.path),
            "13" : utils.load_image("d13.png", self.path),
            "14" : utils.load_image("d14.png", self.path)
        }
        self.voices = {
            "0" : utils.load_vx("epilogue/end/0.ogg"),
            "1" : utils.load_vx("epilogue/end/1.ogg"),
            "2" : utils.load_vx("epilogue/end/2.ogg"),
            "3" : utils.load_vx("epilogue/end/3.ogg"),
            "4" : utils.load_vx("epilogue/end/4.ogg"),
            "5" : utils.load_vx("epilogue/end/5.ogg"),
            "6" : utils.load_vx("epilogue/end/6.ogg"),
            "7" : utils.load_vx("epilogue/end/7.ogg"),
            "8" : utils.load_vx("epilogue/end/8.ogg"),
            "9" : utils.load_vx("epilogue/end/9.ogg"),
            "10" : utils.load_vx("epilogue/end/10.ogg"),
            "11" : utils.load_vx("epilogue/end/11.ogg"),
            "12" : utils.load_vx("epilogue/end/12.ogg"),
            "13" : utils.load_vx("epilogue/end/13.ogg"),
            "14" : utils.load_vx("epilogue/end/14.ogg")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "epilogue")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "epilogue")
        self.exit = Button((888, 780), "exit1.png", "exit2.png", 273, 99, "epilogue/end")
        self.back = Button((55, 780), "back1.png", "back2.png", 350, 100, "epilogue/end")
        self.no = Button((430, 580), "no1.png", "no2.png", 163, 124, "epilogue/end")
        self.si = Button((600, 580), "si1.png", "si2.png", 163, 124, "epilogue/end")

    def run(self):
        utils.load_bg("house.ogg")
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
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 15:
                            self.vx_channel.stop()
                            self.back.on_press(self.screen)
                            self.next_level = 1
                            running = False
                        if self.current_slide == 16:
                            self.vx_channel.stop()
                            self.no.on_press(self.screen)
                            self.next_level = 1
                            running = False
                        elif self.current_slide > 1:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1

                    if event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if  self.current_slide == 15:
                            self.vx_channel.stop()
                            self.exit.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide < 16:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 16:
                            self.vx_channel.stop()
                            self.si.on_press(self.screen)
                            running = False

    def render_scene(self, number):
        if number == 1:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices["0"])
                self.played[number-1] = 1
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
        elif number < 15:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.screen.blit(self.conversation[str(number-1)], (0, 0))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number == 15:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.screen.blit(self.conversation[str(number-1)], (0, 0))
            self.screen.blit(self.exit.base, (888, 780))
            self.screen.blit(self.back.base, (55, 780))
        elif number == 16:
            self.screen.blit(self.conversation["14"], (0, 0))
            self.screen.blit(self.modal, (0, 0))
            self.screen.blit(self.no.base, (430, 580))
            self.screen.blit(self.si.base, (600, 580))
