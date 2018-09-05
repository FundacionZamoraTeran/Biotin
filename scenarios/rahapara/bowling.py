import random
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from actors.bowl import Bowl
from actors.food import Food

class Bowling:
    """
        Class representing Rahapara Village, recieves
        a Surface as a screen, a Clock as clock, and the save slot name
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

        self.background = utils.load_image("background.png", "rahapara")
        self.ground = utils.load_image("ground.png", "rahapara")
        self.scoreboard = utils.load_image("score.png", "rahapara")
        self.team = utils.load_image("team.png", "rahapara")
        self.font = utils.load_font("xxii.ttf", 85)
        self.current_slide = 9

        self.bowl = Bowl(self.screen,
                         self.clock,
                         (200, 600),
                         30)

        self.good_food = {
            "banana": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "banana.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "carrot": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "carrot.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "pineapple": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "pineapple.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "cheese": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "cheese.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "dragonfruit": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "dragonfruit.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "spinach": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "spinach.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "sausage": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "sausage.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "meat": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "meat.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "orange": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "orange.png", "rahapara/food", (-400, 1100), random.randint(14, 22)),
            "bpepper": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "bpepper.png", "rahapara/food", (-400, 1100), random.randint(14, 22))
        }

        self.bad_food = {
            "c1": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c1.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c2": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c2.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c3": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c3.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c4": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c4.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c5": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c5.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c6": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c6.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c7": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c7.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
            "c8": Food(self.screen, self.clock, (random.randint(200, 1100), random.randint(-900, -200)), "c8.png", "rahapara/food", (-400, 1100), random.randint(10, 15)),
        }

        self.dialogue = {
            "1" : utils.load_image("d1.png", "rahapara/dialogue"),
            "2" : utils.load_image("d2.png", "rahapara/dialogue"),
            "3" : utils.load_image("d3.png", "rahapara/dialogue"),
            "4" : utils.load_image("d4.png", "rahapara/dialogue"),
            "5" : utils.load_image("d5.png", "rahapara/dialogue"),
            "6" : utils.load_image("d6.png", "rahapara/dialogue")
        }

        self.modal = {
            "1" : utils.load_image("h1.png", "rahapara/help"),
            "2" : utils.load_image("h2.png", "rahapara/help")
        }

        self.congrats = {
            "bg": utils.load_image("1.png", "rahapara/congrats"),
            "prev": Button((100, 798), "prev1.png", "prev2.png", 332, 81, "rahapara/congrats")
        }

        self.voices = {
            "1" : utils.load_vx("rahapara/dialogue/1.ogg"),
            "2" : utils.load_vx("rahapara/dialogue/2.ogg"),
            "3" : utils.load_vx("rahapara/dialogue/3.ogg"),
            "4" : utils.load_vx("rahapara/dialogue/4.ogg"),
            "5" : utils.load_vx("rahapara/dialogue/5.ogg"),
            "6" : utils.load_vx("rahapara/dialogue/6.ogg"),
            "h1" : utils.load_vx("rahapara/help/1.ogg"),
            "h2" : utils.load_vx("rahapara/help/2.ogg"),
        }

        self.bad_food_list = pygame.sprite.Group()
        self.good_food_list = pygame.sprite.Group()
        for food in self.good_food.values():
            self.good_food_list.add(food)
        for food in self.bad_food.values():
            self.bad_food_list.add(food)
        self.bowl.set_lists(self.good_food_list, self.bad_food_list)
        self.played = [0] * 8
        self.next = Button((918, 780), "next1.png", "next2.png", 257, 99, "rahapara")
        self.prev = Button((25, 780), "prev1.png", "prev2.png", 257, 99, "rahapara")

    def run(self):
        utils.load_bg("rahapara.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.ground, (0, 645))
            self.render_scene(self.current_slide)
            pygame.display.flip()
            self.clock.tick(consts.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == consts.K_CHECK:
                        pass
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide > 3 and self.current_slide < 9:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                        elif self.current_slide == 9:
                            self.bowl.direction = "left"
                            self.bowl.velocity = -abs(self.bowl.velocity)
                        elif self.current_slide == 10:
                            self.congrats["prev"].on_press(self.screen)
                            self.current_slide = 3
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide < 9:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 9:
                            self.bowl.direction = "right"
                            self.bowl.velocity = abs(self.bowl.velocity)
                        elif self.current_slide == 10:
                            self.next.on_press(self.screen)
                            utils.loading_screen(self.screen)
                            if not self.slot["stages"]["aldea_2"] is True:
                                saves.save(self.slotname, 3, "Aldea Rahapara", "aldea_2")
                            running = False
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.bowl.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.bowl.direction = "stand"

    def render_scene(self, number):
        if number == 1:
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["h1"])
                self.played[0] = 1
            self.screen.blit(self.modal["1"], (0, 0))
            self.screen.blit(self.next.base, (918, 780))
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["h2"])
                self.played[1] = 1
            self.screen.blit(self.modal["2"], (0, 0))
            self.screen.blit(self.next.base, (918, 780))
        elif number == 3:
            if self.played[2] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[2] = 1
            self.screen.blit(self.dialogue["1"], (0, 0))
            self.screen.blit(self.next.base, (918, 780))
        elif 3 < number < 9:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-2)])
                self.played[number-1] = 1
            self.screen.blit(self.dialogue[str(number-2)], (0, 0))
            self.screen.blit(self.prev.base, (25, 780))
            self.screen.blit(self.next.base, (918, 780))
        elif number == 9:
            self.screen.blit(self.scoreboard, (1007, 704)) #37x33
            text = self.font.render(str(self.bowl.score),
                                    True,
                                    (240, 211, 8),
                                    (255, 255, 249))
            self.screen.blit(self.team, (0, 588))
            self.good_food_list.update()
            self.bad_food_list.update()
            self.bowl.update()
            self.bowl.collision_food()
            if self.bowl.score > 9 and self.bowl.score < 16:
                self.screen.blit(text, (1035, 725))
            elif self.bowl.score >= 30:
                self.bowl.score = 0
                self.current_slide = 10
                self.screen.blit(self.congrats["bg"], (0, 0))
            else:
                self.screen.blit(text, (1060, 725))
        elif number == 10:
            self.screen.blit(self.congrats["bg"], (0, 0))
            self.screen.blit(self.congrats["prev"].base, (100, 798))
            self.screen.blit(self.next.base, (918, 780))
