import sys
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import dialogue
from scenarios.utils.button import Button
from scenarios.house import game

class Kitchen:
    """
        Class representing the prologue part 2 comics before minigame, recieves
        a Surface as a screen, and a Clock as clock
    """
    def __init__(self, screen, clock, slot):
        self.screen = screen
        self.clock = clock
        self.slot = slot
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.border = utils.load_image("border.png", "house/kitchen")

        self.current_slide = 1
        self.slide_1 = utils.load_image("kit1.png", "house/kitchen")
        self.slide_2 = utils.load_image("kit2.png", "house/kitchen")
        self.slide_3 = utils.load_image("kit3.png", "house/kitchen")
        self.slide_4 = utils.load_image("kit4.png", "house/kitchen")
        self.slide_5 = utils.load_image("kit5.png", "house/kitchen")
        self.slide_6 = utils.load_image("kit6.png", "house/kitchen")
        self.slide_7 = utils.load_image("kit7.png", "house/kitchen")
        self.slide_8 = utils.load_image("kit8.png", "house/kitchen")

        self.bubble_1 = utils.load_image("d1.png", "house/kitchen")
        self.bubble_2 = utils.load_image("d2.png", "house/kitchen")
        self.bubble_3 = utils.load_image("d3.png", "house/kitchen")
        self.bubble_4 = utils.load_image("d4.png", "house/kitchen")
        self.bubble_5 = utils.load_image("d5.png", "house/kitchen")
        self.bubble_6 = utils.load_image("d6.png", "house/kitchen")
        self.bubble_7 = utils.load_image("d7.png", "house/kitchen")
        self.bubble_8 = utils.load_image("d8.png", "house/kitchen")

        self.voice_1 = utils.load_vx("house/kitchen/1.ogg")
        self.voice_2 = utils.load_vx("house/kitchen/2.ogg")
        self.voice_3 = utils.load_vx("house/kitchen/3.ogg")
        self.voice_4 = utils.load_vx("house/kitchen/4.ogg")
        self.voice_5 = utils.load_vx("house/kitchen/5.ogg")
        self.voice_6 = utils.load_vx("house/kitchen/6.ogg")
        self.voice_7 = utils.load_vx("house/kitchen/7.ogg")
        self.voice_8 = utils.load_vx("house/kitchen/8.ogg")

        self.next = Button((918, 780), "kitchen/next1.png", "kitchen/next2.png", 257, 99, "house")
        self.prev = Button((25, 780), "kitchen/prev1.png", "kitchen/prev2.png", 257, 99, "house")
        self.played = [0, 0, 0, 0, 0, 0, 0, 0]

    def run(self):
        utils.load_bg("house.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.render_scene(self.current_slide)
            self.screen.blit(self.border, (0,0))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
            pygame.display.flip()
            self.clock.tick(consts.FPS)

            for event in [pygame.event.wait()] + pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide != 1:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide != 8:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        else:
                            self.vx_channel.stop()
                            minigame = game.Game(self.screen, self.clock, self.slot)
                            minigame.run()
                            running = False

    def render_scene(self, number):
        if number == 1:
            self.screen.blit(self.slide_1, (0, 0))
            if self.played[0] == 0:
                self.vx_channel.play(self.voice_1)
                self.played[0] = 1
            self.screen.blit(self.bubble_1, (480,390))
        elif number == 2:
            self.screen.blit(self.slide_2, (0, 0))
            if self.played[1] == 0:
                self.vx_channel.play(self.voice_2)
                self.played[1] = 1
            self.screen.blit(self.bubble_2, (200,620))
        elif number == 3:
            self.screen.blit(self.slide_3, (0, 0))
            if self.played[2] == 0:
                self.vx_channel.play(self.voice_3)
                self.played[2] = 1
            self.screen.blit(self.bubble_3, (270,250))
        elif number == 4:
            self.screen.blit(self.slide_4, (0, 0))
            if self.played[3] == 0:
                self.vx_channel.play(self.voice_4)
                self.played[3] = 1
            self.screen.blit(self.bubble_4, (120,500))
        elif number == 5:
            self.screen.blit(self.slide_5, (0, 0))
            if self.played[4] == 0:
                self.vx_channel.play(self.voice_5)
                self.played[4] = 1
            self.screen.blit(self.bubble_5, (50,250))
        elif number == 6:
            self.screen.blit(self.slide_6, (0, 0))
            if self.played[5] == 0:
                self.vx_channel.play(self.voice_6)
                self.played[5] = 1
            self.screen.blit(self.bubble_6, (740,50))
        elif number == 7:
            self.screen.blit(self.slide_7, (0, 0))
            if self.played[6] == 0:
                self.vx_channel.play(self.voice_7)
                self.played[6] = 1
            self.screen.blit(self.bubble_7, (860,390))
        elif number == 8:
            self.screen.blit(self.slide_8, (0, 0))
            if self.played[7] == 0:
                self.vx_channel.play(self.voice_8)
                self.played[7] = 1
            self.screen.blit(self.bubble_8, (360,200))
