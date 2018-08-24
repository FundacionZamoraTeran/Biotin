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
            "current_level": self.slot["last_level_passed"]["code"],
            "completed": self.slot["stages"]["completado"]
        }

        self.nutri = utils.load_image("neutral.png", "nutriton/expressions", size=(104, 297)) # load as player class

        if self.session["is_new?"]:
            self.current_slide = 1
        else:
            self.current_slide = 8
        if self.session["completed"]:
            self.background = utils.load_image("end.png", "map")
        else:
            self.background = utils.load_image("base.png", "map")

        self.modal = utils.load_image("modal.png", "map")

        self.hud = {
            "1" : utils.load_image("1.png", "map/HUD"),
            "2" : utils.load_image("2.png", "map/HUD"),
            "3" : utils.load_image("3.png", "map/HUD"),
            "4" : utils.load_image("4.png", "map/HUD"),
            "5" : utils.load_image("5.png", "map/HUD"),
            "6" : utils.load_image("6.png", "map/HUD"),
            "7" : utils.load_image("7.png", "map/HUD"),
            "8" : utils.load_image("8.png", "map/HUD"),
            "help" : Button((1070, 50), "h1.png", "h2.png", 70, 71, "map/HUD")
        }

        self.worlds = {
            "2" : utils.load_image("rahapara.png", "map/worlds"),
            "3" : utils.load_image("bazar.png", "map/worlds"),
            "4" : utils.load_image("valley.png", "map/worlds"),
            "5" : utils.load_image("woods.png", "map/worlds"),
            "6" : utils.load_image("moon.png", "map/worlds"),
            "7" : utils.load_image("city.png", "map/worlds"),
            "8" : utils.load_image("castle.png", "map/worlds"),
        }

        self.voices = {
            "1" : utils.load_vx("map/dialogue/1.ogg"),
            "2" : utils.load_vx("map/dialogue/2.ogg"),
            "3" : utils.load_vx("map/dialogue/3.ogg"),
            "4" : utils.load_vx("map/dialogue/4.ogg"),
            "5" : utils.load_vx("map/dialogue/5.ogg"),
            "h" : utils.load_vx("map/help/1.ogg")
        }

        self.played = [0] * 7
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
            #self.screen.blit(self.nutri, (0,0))
            self.render_scene(self.current_slide)
            pygame.display.flip()
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.current_slide is 2:
                            self.current_slide += 1
                    elif event.key == pygame.K_LEFT:
                        if self.current_slide > 2 and self.current_slide < 8:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide is 7:
                            pass

                    elif event.key == pygame.K_RIGHT:
                        if self.current_slide < 8 and self.current_slide != 2:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide is 8:
                            pass
                    elif event.key == pygame.K_ESCAPE:
                            self.hud["help"].on_press(self.screen)

    def render_scene(self, number):
        if number is 1:
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["h"])
                self.played[0] = 1
            self.screen.blit(self.modal, (0, 0))
            self.screen.blit(self.next.base, (918, 780))
        if number is 2:
            text = self.font.render("Elige la pareja con la que quieres jugar",
                                    True,
                                    (246, 212, 0))
        elif number is 3:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[1] = 1
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number is 4:
            if self.played[2] == 0:
                self.vx_channel.play(self.voices["2"])
                self.played[2] = 1
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number is 5:
            if self.played[3] == 0:
                self.vx_channel.play(self.voices["3"])
                self.played[3] = 1
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number is 6:
            if self.played[4] == 0:
                self.vx_channel.play(self.voices["4"])
                self.played[4] = 1
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number is 7:
            if self.played[5] == 0:
                self.vx_channel.play(self.voices["5"])
                self.played[5] = 1
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number is 8:
            if not self.session["is_new?"]:
                self.load_worlds()
            self.check_luis_status()
            self.screen.blit(self.hud["help"].base, (1070, 50))

    def check_luis_status(self):
        if self.session["completed"]:
            self.screen.blit(self.hud["8"], (30, 50))
        else:
            self.screen.blit(self.hud[str(self.session["current_level"])], (30, 50))
    def load_worlds(self):
        if not self.session["completed"]:
            if self.session["current_level"] > 1:
                self.screen.blit(self.worlds["2"], (299, 502))
            if self.session["current_level"] > 2:
                self.screen.blit(self.worlds["3"], (414, 312))
            if self.session["current_level"] > 3:
                self.screen.blit(self.worlds["4"], (643, 420))
            if self.session["current_level"] > 4:
                self.screen.blit(self.worlds["5"], (626, 553))
            if self.session["current_level"] > 5:
                self.screen.blit(self.worlds["6"], (0, 0))
            if self.session["current_level"] > 6:
                self.screen.blit(self.worlds["7"], (670, 710))
            if self.session["current_level"] == 8:
                self.screen.blit(self.worlds["8"], (1032, 580))
