# named mapp just because i don't want
# a clash between this and the map function
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import dialogue
from scenarios.utils import saves
from scenarios.utils.button import Button

class Map:
    """
        Class representing the food selection minigame, recieves
        a Surface as a screen, a Clock as clock, and the save slot selected
    """
    def __init__(self, screen, clock, slot):
        self.screen = screen
        self.clock = clock
        self.slot = saves.load_slot(slot)
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.font = utils.load_font("notoregu.ttf", 20)
        self.next_level = 1

        self.session = {
            "stages": self.slot["stages"],
            "is_new?": self.slot["last_level_passed"]["code"] == 1 if True else False,
            "current_level": self.slot["last_level_passed"]["code"]
        }

        self.current_slide = 1

        self.background = utils.load_image("base.png", "map")

        self.voices = {
            "1" : utils.load_vx("map/dialogue/1.ogg"),
            "2" : utils.load_vx("map/dialogue/2.ogg"),
            "3" : utils.load_vx("map/dialogue/3.ogg"),
            "4" : utils.load_vx("map/dialogue/4.ogg"),
            "5" : utils.load_vx("map/dialogue/5.ogg"),
            "h" : utils.load_vx("map/help/1.ogg")
        }

        self.dialogue = dialogue.get_dialogue_subscenario("mapa", "dialogo")
        self.next = Button((918, 780), "next1.png", "next2.png", 257, 99, "map")
        self.prev = Button((25, 780), "prev1.png", "prev2.png", 257, 99, "map")

    def run(self):
        utils.load_bg("scherzo.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0,0))
            self.render_scene(self.current_slide)
            pygame.display.flip()
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_LEFT:
                        if self.current_slide != 1 and self.current_slide < 5:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            #self.played[self.current_slide-1] = 0
                            self.current_slide -= 1

                    elif event.key == pygame.K_RIGHT:
                        if self.current_slide < 5:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            #self.played[self.current_slide-1] = 0
                            self.current_slide += 1

    def render_scene(self, number):
        if number is 1:
            # if self.played[0] == 0:
            #     self.vx_channel.play(self.voices["1"])
            #     self.played[0] = 1
            # text = self.font.render(self.dialogue['1'],
            #                         True,
            #                         (246, 212, 0))
            #self.screen.blit(text, (350, 810))
            #self.screen.blit(self.next.base, (918, 780))
            #self.screen.blit(self.prev.base, (25, 780))
            pass
