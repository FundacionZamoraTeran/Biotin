# named mapp just because i don't want
# a clash between this and the map function
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
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
        self.slotname = slot
        self.slot = saves.load_slot(slot)
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.next_level = 1
        self.frame = 0

        self.session = {
            "stages": self.slot["stages"],
            "is_new?": True if self.slot["last_level_passed"]["code"] == 1 else False,
            "current_level":  self.slot["last_level_passed"]["code"],
            "completed": self.slot["stages"]["completado"]
        }

        if self.session["is_new?"]:
            self.current_slide = 1
            self.marker_level = 0
        else:
            self.current_slide = 6
            self.marker_level = self.session["current_level"]
        if self.session["completed"]:
            self.background = utils.load_image("end.png", "map")
        else:
            self.background = utils.load_image("base.png", "map")

        self.modal = utils.load_image("modal.png", "map")
        self.denied = utils.load_fx("denied.ogg")

        self.dialogue = {
            "1" : utils.load_image("d1.png", "map/dialogue"),
            "2" : utils.load_image("d2.png", "map/dialogue"),
            "3" : utils.load_image("d3.png", "map/dialogue"),
            "nutriton" : utils.load_image("nutriton.png", "map/dialogue"),
            "background" : utils.load_image("background.png", "map/dialogue")
        }

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

        self.nutriton = {
            "0" : utils.load_image("1.png", "nutriton/mini"),
            "1" : utils.load_image("2.png", "nutriton/mini"),
            "2" : utils.load_image("3.png", "nutriton/mini")
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

        self.selector = {
            "ec" :  Button((230, 300), "e1_1.png", "e1_2.png", 358, 320, "map/selector", flag=True),
            "ed" :  Button((580, 300), "e2_1.png", "e2_2.png", 358, 320, "map/selector"),
            "background" : utils.load_image("background.png", "map/selector")
        }

        self.voices = {
            "1" : utils.load_vx("map/dialogue/1.ogg"),
            "2" : utils.load_vx("map/dialogue/2.ogg"),
            "3" : utils.load_vx("map/dialogue/3.ogg"),
            "4" : utils.load_vx("map/dialogue/4.ogg"),
            "5" : utils.load_vx("map/dialogue/5.ogg"),
            "h" : utils.load_vx("map/help/1.ogg")
        }

        self.show_help = False
        self.played = [0] * 5
        self.next = Button((918, 780), "next1.png", "next2.png", 257, 99, "map")
        self.prev = Button((25, 780), "prev1.png", "prev2.png", 257, 99, "map")

    def run(self):
        if self.session["completed"]:
            utils.load_bg("satie.ogg")
        else:
            utils.load_bg("scherzo.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            if not self.show_help:
                self.render_scene(self.current_slide)
            else:
                self.screen.blit(self.modal, (0, 0))
            pygame.display.flip()
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.current_slide == 2:
                            if self.selector["ec"].flag is True:
                                saves.specific_save(self.slotname, "team_ena", True)
                            elif self.selector["ed"].flag is True:
                                saves.specific_save(self.slotname, "team_ena", False)
                            self.current_slide += 1
                        elif self.current_slide == 6:
                            if self.marker_level == 0:
                                self.fx_channel.play(self.denied)
                            else:
                                self.next_level = self.marker_level
                                running = False
                    elif event.key == pygame.K_LEFT:
                        if self.current_slide > 3 and self.current_slide < 6:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 2:
                            if self.selector["ed"].flag is True:
                                self.selector["ed"].flag = False
                                self.selector["ec"].flag = True
                                self.selector["ed"].on_focus(self.screen)
                                self.selector["ec"].on_focus(self.screen)
                        elif self.current_slide == 6:
                            if self.marker_level > 0:
                                self.marker_level -= 1
                            else:
                                self.marker_level = 0
                    elif event.key == pygame.K_RIGHT:
                        if self.current_slide < 6 and self.current_slide != 2:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 2:
                            if self.selector["ec"].flag is True:
                                self.selector["ec"].flag = False
                                self.selector["ed"].flag = True
                                self.selector["ec"].on_focus(self.screen)
                                self.selector["ed"].on_focus(self.screen)
                        elif self.current_slide == 6:
                            if self.marker_level < 8:
                                if (self.marker_level+1 > self.session["current_level"]
                                        and not self.session["completed"]):
                                    self.marker_level = self.session["current_level"]
                                else:
                                    self.marker_level += 1
                            else:
                                self.marker_level = 8
                    elif event.key == pygame.K_ESCAPE:
                        if self.current_slide == 6:
                            self.hud["help"].on_press(self.screen)
                            if self.show_help is False:
                                self.show_help = True
                            elif self.show_help:
                                self.show_help = False

    def render_scene(self, number):
        if number == 1:
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["h"])
                self.played[0] = 1
            self.screen.blit(self.modal, (0, 0))
            self.screen.blit(self.next.base, (918, 780))
        if number == 2:
            self.screen.blit(self.selector["background"], (0, 0))
            self.screen.blit(self.selector["ec"].end, (230, 300))
            self.screen.blit(self.selector["ed"].base, (580, 300))

        elif number == 3:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.vx_channel.queue(self.voices["2"])
                self.played[1] = 1
            self.screen.blit(self.hud["1"], (30, 50))
            self.screen.blit(self.dialogue["background"], (0, 0))
            self.screen.blit(self.dialogue["nutriton"], (150, 402))
            self.screen.blit(self.dialogue["1"], (350, 350))
            self.screen.blit(self.next.base, (918, 780))
        elif number == 4:
            if self.played[2] == 0:
                self.vx_channel.play(self.voices["3"])
                self.vx_channel.queue(self.voices["4"])
                self.played[2] = 1
            self.screen.blit(self.hud["1"], (30, 50))
            self.screen.blit(self.dialogue["background"], (0, 0))
            self.screen.blit(self.dialogue["nutriton"], (150, 402))
            self.screen.blit(self.dialogue["2"], (350, 350))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number == 5:
            if self.played[3] == 0:
                self.vx_channel.play(self.voices["5"])
                self.played[3] = 1
            self.screen.blit(self.hud["1"], (30, 50))
            self.screen.blit(self.dialogue["background"], (0, 0))
            self.screen.blit(self.dialogue["nutriton"], (150, 402))
            self.screen.blit(self.dialogue["3"], (350, 350))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number == 6:
            if not self.session["is_new?"]:
                self.load_worlds()
            self.check_luis_status()
            self.screen.blit(self.hud["help"].base, (1070, 50))
            self.animate_marker()

    def check_luis_status(self):
        if self.session["completed"]:
            self.screen.blit(self.hud["8"], (30, 50))
        else:
            self.screen.blit(self.hud[str(self.session["current_level"])], (30, 50))

    def animate_marker(self):
        if self.marker_level == 0:
            pos = (105, 266) # home
        elif self.marker_level == 1:
            pos = (105, 475) # saar  # with new nutri is 26px more y axis
        elif self.marker_level == 2:
            pos = (340, 410) # rahapara
        elif self.marker_level == 3:
            pos = (425, 268) # bazar
        elif self.marker_level == 4:
            pos = (770, 385) # valley
        elif self.marker_level == 5:
            pos = (625, 510) # warp
        elif self.marker_level == 6:
            pos = (585, 10) # moon
        elif self.marker_level == 7:
            pos = (730, 650) # city
        elif self.session["completed"] or self.marker_level == 8:
            pos = (1073, 540) # castle
        self.frame += 1
        if self.frame > 17:
            self.frame = 0
        pygame.display.update(self.screen.blit(self.nutriton[str(self.frame//6)], pos))

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
