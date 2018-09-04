import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from scenarios.sharqii import grains
from actors.player import Player
from actors.prompt import Prompt


class Entrance:
    """
        Class representing the entrance of the great bazaar, recieves
        a Surface as a screen, and a Clock as clock, and a save slot name
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
        self.background = utils.load_image("background.png", "sharqii/entrance")
        self.player = Player(self.screen,
                             self.clock,
                             (150, 500),
                             self.character,
                             1200,
                             False)
        self.interact = Prompt(self.screen,
                               self.clock,
                               (745, 280),
                               "interact.png",
                               "sharqii",
                               (150, 350))
        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (540, 380),
                                 "interact.png",
                                 "sharqii",
                                 (250, 450))
        self.current_slide = 1
        self.played = [0] * 14
        self.pilori = utils.load_image("pilori.png", "sharqii/entrance")
        self.conversation = {
            "1" : utils.load_image("d1.png", "sharqii/entrance/"),
            "2" : utils.load_image("d2.png", "sharqii/entrance/"),
            "3" : utils.load_image("d3.png", "sharqii/entrance/"),
            "4" : utils.load_image("d4.png", "sharqii/entrance/"),
            "5" : utils.load_image("d5.png", "sharqii/entrance/"),
            "6" : utils.load_image("d6.png", "sharqii/entrance/"),
            "7" : utils.load_image("d7.png", "sharqii/entrance/"),
            "8" : utils.load_image("d8.png", "sharqii/entrance/"),
            "9" : utils.load_image("d9.png", "sharqii/entrance/"),
            "10": utils.load_image("d10.png", "sharqii/entrance/"),
            "11": utils.load_image("d11.png", "sharqii/entrance/"),
            "12": utils.load_image("d12.png", "sharqii/entrance/"),
            "13": utils.load_image("d13.png", "sharqii/entrance/")
        }
        self.voices = {
            "1" : utils.load_vx("sharqii/entrance/1.ogg"),
            "2" : utils.load_vx("sharqii/entrance/2.ogg"),
            "3" : utils.load_vx("sharqii/entrance/3.ogg"),
            "4" : utils.load_vx("sharqii/entrance/4.ogg"),
            "5" : utils.load_vx("sharqii/entrance/5.ogg"),
            "6" : utils.load_vx("sharqii/entrance/6.ogg"),
            "7" : utils.load_vx("sharqii/entrance/7.ogg"),
            "8" : utils.load_vx("sharqii/entrance/8.ogg"),
            "9" : utils.load_vx("sharqii/entrance/9.ogg"),
            "10": utils.load_vx("sharqii/entrance/10.ogg"),
            "11": utils.load_vx("sharqii/entrance/11.ogg"),
            "12": utils.load_vx("sharqii/entrance/12.ogg"),
            "13": utils.load_vx("sharqii/entrance/13.ogg")
        }
        self.biotin = {
            "diego": utils.load_image("down1.png", "diego"),
            "ena": utils.load_image("down1.png", "ena"),
            "ezer": utils.load_image("down1.png", "ezer"),
            "cesar": utils.load_image("down1.png", "cesar")
        }
        self.next = Button((1038, 780), "next1.png", "next2.png", 123, 94, "sharqii")
        self.prev = Button((55, 780), "prev1.png", "prev2.png", 123, 94, "sharqii")
        self.visited = False


    def run(self):
        utils.load_bg("bazar.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.pilori, (725, 370))
            self.render_scene(self.current_slide)
            pygame.display.flip()
            self.clock.tick(consts.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide == 1:
                            self.player.direction = "left"
                            self.player.velocity = -abs(self.player.velocity)
                        elif self.current_slide < 15:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide == 1:
                            self.player.direction = "right"
                            self.player.velocity = abs(self.player.velocity)
                        elif self.current_slide > 1 and self.current_slide < 14:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        elif self.current_slide == 14:
                            self.vx_channel.stop()
                            self.current_slide = 1
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.current_slide == 1:
                            if (self.player.rect.x+self.player.rect.width > 730 and
                                    self.player.rect.x+self.player.rect.width < 875
                                    and self.current_slide == 1):
                                self.current_slide += 1
                                self.visited = True
                            if (self.player.rect.x+self.player.rect.width > 525
                                and self.player.rect.x+self.player.rect.width < 655 and
                                self.visited is True):
                                utils.loading_screen(self.screen)
                                gra = grains.Grain(self.screen, self.clock, self.character)
                                gra.run()
                                del gra
                                running = False
                                utils.loading_screen(self.screen)
                                #save here
                                if not self.slot["stages"]["bazar"] is True:
                                    saves.save(self.slotname, 4, "El gran bazar", "bazar")
                    elif ((event.key == pygame.K_SPACE or event.key == pygame.K_PAGEDOWN) and
                             (self.player.jumping is False and self.player.jump_frames == 0)):
                        if self.current_slide == 1:
                            self.player.jumping = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"

    def render_scene(self, number):
        if number == 1:
            self.arrange_team(number)
            if (self.player.rect.x+self.player.rect.width > 730
                    and self.player.rect.x+self.player.rect.width < 875):
                self.interact.float(0)
            if (self.player.rect.x+self.player.rect.width > 525
                    and self.player.rect.x+self.player.rect.width < 655 and
                    self.visited is True):
                self.interact_2.float(0)
        elif number == 2:
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[1] = 1
            self.arrange_team(number)
            self.screen.blit(self.conversation["1"], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))
        elif number < 15:
            if self.played[number-1] == 0:
                self.vx_channel.play(self.voices[str(number-1)])
                self.played[number-1] = 1
            self.arrange_team(number)
            self.screen.blit(self.conversation[str(number-1)], (0, 617))
            self.screen.blit(self.next.base, (1038, 780))
            self.screen.blit(self.prev.base, (55, 780))

    def arrange_team(self, number):
        if self.character == "ena":
            self.screen.blit(self.biotin["ezer"], (420, 495))
            self.screen.blit(self.biotin["cesar"], (500, 500))
            self.screen.blit(self.biotin["diego"], (330, 480))
            if number == 1: # this check exist to blit the static image when the dialogue appears
                self.player.update()
            else:
                self.screen.blit(self.biotin["ena"], self.player.rect.topleft)
        elif self.character == "ezer":
            self.screen.blit(self.biotin["ena"], (420, 495))
            self.screen.blit(self.biotin["cesar"], (500, 500))
            self.screen.blit(self.biotin["diego"], (330, 480))
            if number == 1:
                self.player.update()
            else:
                self.screen.blit(self.biotin["ezer"], self.player.rect.topleft)
        elif self.character == "diego":
            self.screen.blit(self.biotin["cesar"], (400, 495))
            self.screen.blit(self.biotin["ena"], (480, 500))
            self.screen.blit(self.biotin["ezer"], (310, 480))
            if number == 1:
                self.player.update()
            else:
                self.screen.blit(self.biotin["diego"], self.player.rect.topleft)
        elif self.character == "cesar":
            self.screen.blit(self.biotin["diego"], (420, 495))
            self.screen.blit(self.biotin["ezer"], (500, 500))
            self.screen.blit(self.biotin["ena"], (330, 480))
            if number == 1:
                self.player.update()
            else: 
                self.screen.blit(self.biotin["cesar"], self.player.rect.topleft)
