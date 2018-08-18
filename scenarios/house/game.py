import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import dialogue
from scenarios.utils import saves
from scenarios.house.button import Button
from scenarios.house.slider import Slider
from scenarios.house import yard

class Game:
    """
        Class representing the food selection minigame, recieves
        a Surface as a screen, a Clock as clock, and the save slot selected
    """
    def __init__(self, screen, clock, slot):
        self.screen = screen
        self.clock = clock
        self.slot = slot
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.font = utils.load_font("notoregu.ttf", 20)

        self.current_slide = 5

        self.title = utils.load_image("title.png", "house/game")
        self.background = utils.load_image("background.png", "house/game")
        self.sparkle_1 = utils.load_image("sparkle_1.png", "house/game")
        self.sparkle_2 = utils.load_image("sparkle_2.png", "house/game")

        # using a dict to avoid creating more variables per elements
        self.foods = {
            "1": Button((40, 200), "game/food_1-1.png", "game/food_1-2.png", 381, 506, flag=True),
            "2": Button((410, 200), "game/food_2-1.png", "game/food_2-2.png", 381, 506),
            "3": Button((780, 200), "game/food_3-1.png", "game/food_3-2.png", 381, 506)
        }
        self.food_1 = {
            "bg" : utils.load_image("background.png", "house/game/food_1"),
            "1" : [utils.load_image("cream.png", "house/game/food_1"), "cream", (1, 0, 1)], # (nutrients, energy, fats)
            "2" : [utils.load_image("salad.png", "house/game/food_1"), "salad", (1, 1, 0)],
            "3" : [utils.load_image("platain.png", "house/game/food_1"), "platain", (1, 1, 1)],
            "4" : [utils.load_image("barley.png", "house/game/food_1"), "barley", (1, 1, 0)],
            "nutrients_level": 2,
            "energy_level": 2,
            "fats_level": 2
        }

        self.food_2 = {
            "bg" : utils.load_image("background.png", "house/game/food_2"),
            "1" : [utils.load_image("cream.png", "house/game/food_2"), "cream", (1, 0, 1)],
            "2" : [utils.load_image("tomato.png", "house/game/food_2"), "tomato", (1, 1, 0)],
            "3" : [utils.load_image("salt.png", "house/game/food_2"), "salt", (0, 1, 0)],
            "4" : [utils.load_image("oat.png", "house/game/food_2"), "oat", (1, 1, 0)],
            "nutrients_level": 3,
            "energy_level": 3,
            "fats_level": 2
        }

        self.food_3 = {
            "bg" : utils.load_image("background.png", "house/game/food_3"),
            "1" : [utils.load_image("butter.png", "house/game/food_3"), "butter", (0, 1, 1)],
            "2" : [utils.load_image("cereal.png", "house/game/food_3"), "cereal", (1, 1, 0)],
            "3" : [utils.load_image("chocolate.png", "house/game/food_3"), "chocolate", (0, 1, 1)],
            "4" : [utils.load_image("pinolillo.png", "house/game/food_3"), "pinolillo", (1, 1, 0)],
            "nutrients_level": 3,
            "energy_level": 2,
            "fats_level": 1
        }

        self.metrics = {
            "nutrients":  utils.load_image("nutrients.png", "house/game/metrics"),
            "energy":  utils.load_image("energy.png", "house/game/metrics"),
            "fats": utils.load_image("fats.png", "house/game/metrics"),
            "nutrients_slider": Slider((670, 240),
                                       "house/game/metrics",
                                       level=1),
            "energy_slider": Slider((670, 320),
                                    "house/game/metrics",
                                    level=1),
            "fats_slider": Slider((670, 400),
                                  "house/game/metrics",
                                  level=1)
        }

        self.voices = {
            "1" : utils.load_vx("house/game/1.ogg"),
            "2" : utils.load_vx("house/game/2.ogg"),
            "3" : utils.load_vx("house/game/3.ogg"),
            "4" : utils.load_vx("house/game/4.ogg"),
            "5" : utils.load_vx("house/game/5.ogg")
        }

        self.dialogue = dialogue.get_dialogue_subscenario("casa", "juego")
        self.next = Button((918, 780), "yard/next1.png", "yard/next2.png", 257, 99)
        self.prev = Button((25, 780), "yard/prev1.png", "yard/prev2.png", 257, 99)
        self.played = [0, 0, 0, 0, 0]
        self.selected_food = {"base": None, "extra": None}
        self.food_code = None
        self.pos = (110, 480)
        self.first = True

    def run(self):
        utils.load_bg("avant.ogg")
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
                        if self.current_slide == 5:
                            if self.foods["1"].flag is True:
                                self.selected_food["base"] = "tortilla"
                                self.current_slide = 6
                                self.food_code = self.food_1
                            elif self.foods["2"].flag is True:
                                self.selected_food["base"] = "beans"
                                self.current_slide = 6
                                self.food_code = self.food_2
                            elif self.foods["3"].flag is True:
                                self.selected_food["base"] = "bread"
                                self.current_slide = 6
                                self.food_code = self.food_3
                            self.reset_slider()
                        elif self.current_slide == 6:
                            if self.pos == (110, 480):
                                self.selected_food["extra"] = self.food_code["1"][1]
                                self.current_slide = 7
                            elif self.pos == (350, 480):
                                self.selected_food["extra"] = self.food_code["2"][1]
                                self.current_slide = 7
                            elif self.pos == (590, 480):
                                self.selected_food["extra"] = self.food_code["3"][1]
                                self.current_slide = 7
                            elif self.pos == (830, 480):
                                self.selected_food["extra"] = self.food_code["4"][1]
                                self.current_slide = 7

                    elif event.key == pygame.K_LEFT:
                        if self.current_slide != 1 and self.current_slide < 5:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 5:
                            if self.foods["2"].flag is True:
                                self.foods["2"].flag = False
                                self.foods["1"].flag = True
                                self.foods["2"].on_focus(self.screen)
                                self.foods["1"].on_focus(self.screen)
                            elif self.foods["3"].flag is True:
                                self.foods["3"].flag = False
                                self.foods["2"].flag = True
                                self.foods["3"].on_focus(self.screen)
                                self.foods["2"].on_focus(self.screen)
                        elif self.current_slide == 6:
                            if self.pos == (350, 480):
                                self.reset_slider()
                                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["1"][2][0])
                                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["1"][2][1])
                                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["1"][2][2])
                                self.pos = (110, 480)
                            elif self.pos == (590, 480):
                                self.reset_slider()
                                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["2"][2][0])
                                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["2"][2][1])
                                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["2"][2][2])
                                self.pos = (350, 480)
                            elif self.pos == (830, 480):
                                self.reset_slider()
                                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["3"][2][0])
                                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["3"][2][1])
                                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["3"][2][2])
                                self.pos = (590, 480)

                    elif event.key == pygame.K_RIGHT:
                        if self.current_slide < 5:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 5:
                            if self.foods["1"].flag is True:
                                self.foods["1"].flag = False
                                self.foods["2"].flag = True
                                self.foods["1"].on_focus(self.screen)
                                self.foods["2"].on_focus(self.screen)
                            elif self.foods["2"].flag is True:
                                self.foods["2"].flag = False
                                self.foods["3"].flag = True
                                self.foods["2"].on_focus(self.screen)
                                self.foods["3"].on_focus(self.screen)
                        elif self.current_slide == 6:
                            if self.pos == (110, 480):
                                self.reset_slider()
                                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["2"][2][0])
                                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["2"][2][1])
                                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["2"][2][2])
                                self.pos = (350, 480)
                            elif self.pos == (350, 480):
                                self.reset_slider()
                                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["3"][2][0])
                                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["3"][2][1])
                                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["3"][2][2])
                                self.pos = (590, 480)
                            elif self.pos == (590, 480):
                                self.reset_slider()
                                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["4"][2][0])
                                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["4"][2][1])
                                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["4"][2][2])
                                self.pos = (830, 480)
                        elif self.current_slide == 7:
                            self.next.on_press(self.screen)
                            courtyard = yard.Yard(self.screen, self.clock)
                            courtyard.run()
                            #here we save/ init the save file after knowing the comic was finished
                            saves.first_save(self.slot, True, self.selected_food)
                            running = False

    def reset_slider(self):
        self.metrics["nutrients_slider"].level = self.food_code["nutrients_level"]
        self.metrics["energy_slider"].level = self.food_code["energy_level"]
        self.metrics["fats_slider"].level = self.food_code["fats_level"]

    def render_scene(self, number):
        if number is 1:
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[0] = 1
            text = self.font.render(self.dialogue['1'],
                                    True,
                                    (246, 212, 0))
            self.screen.blit(text, (350, 810))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["2"])
                self.played[1] = 1
            text = self.font.render(self.dialogue['2'],
                                    True,
                                    (246, 212, 0))
            self.screen.blit(text, (440, 810))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number == 3:
            if self.played[2] == 0:
                self.vx_channel.play(self.voices["3"])
                self.played[2] = 1
            text = self.font.render(self.dialogue['3'],
                                    True,
                                    (246, 212, 0))
            self.screen.blit(text, (390, 810))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number == 4:
            if self.played[3] == 0:
                self.vx_channel.play(self.voices["4"])
                self.played[3] = 1
            text = self.font.render(self.dialogue['4'],
                                    True,
                                    (246, 212, 0))
            self.screen.blit(text, (530, 810))
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
        elif number == 5:
            self.screen.blit(self.title, (190, 50))
            self.screen.blit(self.foods["1"].end, (40, 200))
            self.screen.blit(self.foods["2"].base, (410, 200))
            self.screen.blit(self.foods["3"].base, (780, 200))
        elif number == 6:
            self.screen.blit(self.food_code["bg"], (180, 90))
            if self.first is True:
                self.metrics["nutrients_slider"].increase_level(self.screen, self.food_code["1"][2][0])
                self.metrics["energy_slider"].increase_level(self.screen, self.food_code["1"][2][1])
                self.metrics["fats_slider"].increase_level(self.screen, self.food_code["1"][2][2])
                self.first = False
            self.screen.blit(self.metrics["nutrients"], (590, 230))
            self.screen.blit(self.metrics["nutrients_slider"].get_current_level_image(), (670, 240))
            self.screen.blit(self.metrics["energy"], (590, 310))
            self.screen.blit(self.metrics["energy_slider"].get_current_level_image(), (670, 320))
            self.screen.blit(self.metrics["fats"], (590, 390))
            self.screen.blit(self.metrics["fats_slider"].get_current_level_image(), (670, 400))
            self.screen.blit(self.sparkle_2, self.pos)
            self.screen.blit(self.food_code["1"][0], (130, 490))
            self.screen.blit(self.food_code["2"][0], (370, 490))
            self.screen.blit(self.food_code["3"][0], (610, 490))
            self.screen.blit(self.food_code["4"][0], (850, 490))
            self.screen.blit(self.sparkle_1, self.pos)
        elif number == 7:
            if self.played[4] == 0:
                self.vx_channel.play(self.voices["5"])
                self.played[4] = 1
            text = self.font.render(self.dialogue['5'],
                                    True,
                                    (246, 212, 0))
            self.screen.blit(text, (390, 810))
            self.screen.blit(self.next.base, (918, 780))
