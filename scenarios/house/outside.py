import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import dialogue
from scenarios.utils.button import Button
from scenarios.house import kitchen

class Outside:
    """
        Class representing the prologue comics before minigame, recieves
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
        self.font = utils.load_font("notoregu.ttf", 30)

        self.current_slide = 1
        self.slide_1 = utils.load_image("out1.png", "house/outside")
        self.slide_2 = utils.load_image("out2.png", "house/outside")
        self.slide_3 = utils.load_image("out3.png", "house/outside")
        self.voice_1 = utils.load_vx("house/outside/1.ogg")
        self.voice_2 = utils.load_vx("house/outside/2.ogg")
        self.voice_3 = utils.load_vx("house/outside/3.ogg")

        self.next = Button((580, 240), "outside/next1.png", "outside/next2.png", 257, 99, "house")
        self.prev = Button((320, 240), "outside/prev1.png", "outside/prev2.png", 257, 99, "house")
        self.played = [0, 0, 0]
        self.dialogue = dialogue.get_dialogue_subscenario("casa", "afuera")
        self.next_level = 1

    def run(self):
        utils.load_bg("house.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.render_scene(self.current_slide)
            self.screen.blit(self.next.base, (580, 240))
            self.screen.blit(self.prev.base, (320, 240))
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.current_slide != 1:
                            self.vx_channel.stop()
                            self.played[self.current_slide-1] = 0
                            self.prev.on_press(self.screen)
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.current_slide != 3:
                            self.vx_channel.stop()
                            self.played[self.current_slide-1] = 0
                            self.next.on_press(self.screen)
                            self.current_slide += 1
                        else:
                            kit = kitchen.Kitchen(self.screen, self.clock, self.slot)
                            kit.run()
                            del kit
                            running = False

    def render_scene(self, number):
        if number == 1:
            self.screen.blit(self.slide_1, (0, 0))
            if self.played[0] == 0:
                self.vx_channel.play(self.voice_1)
                self.played[0] = 1
            text = self.font.render(self.dialogue['1'],
                                    True,
                                    (255, 255, 255))
            self.screen.blit(text, (250,180))
        elif number == 2:
            self.screen.blit(self.slide_2, (0, 0))
            if self.played[1] == 0:
                self.vx_channel.play(self.voice_2)
                self.played[1] = 1
            text = self.font.render(self.dialogue['2'],
                                    True,
                                    (255, 255, 255))
            self.screen.blit(text, (200,180))
        elif number == 3:
            self.screen.blit(self.slide_3, (0, 0))
            if self.played[2] == 0:
                self.vx_channel.play(self.voice_3)
                self.played[2] = 1
            text = self.font.render(self.dialogue['3'],
                                    True,
                                    (255, 255, 255))
            self.screen.blit(text, (300,180))
