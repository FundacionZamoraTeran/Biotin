import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.saar import hena
from scenarios.saar import hcesar
from scenarios.saar import middle
from actors.player import Player
from actors.enemy import Enemy
from actors.platform import Platform
from actors.prompt import Prompt


class Entrance:
    """
        Class representing the first stage of Saar village, recieves
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
        self.character = "ena" if self.slot["team_ena"] is True else "ezer"
        self.background = utils.load_image("background.png", "saar/stage_1")
        self.background_width = self.background.get_size()[0]
        self.foreground = utils.load_image("foreground.png", "saar/stage_1")
        self.ground = Platform(self.screen,
                               self.clock,
                               (0, 742),
                               "ground.png",
                               "saar/stage_1")
        self.interact = Prompt(self.screen,
                               self.clock,
                               (635, 480),
                               "interact.png",
                               "saar",
                               (400, 600))

        self.interact_2 = Prompt(self.screen,
                                 self.clock,
                                 (2155, 480),
                                 "interact.png",
                                 "saar",
                                 (400, 600))
        self.interact_3 = Prompt(self.screen,
                                 self.clock,
                                 (2280, 480),
                                 "interact.png",
                                 "saar",
                                 (400, 600))

        self.player = Player(self.screen,
                             self.clock,
                             (150, 640),
                             self.character,
                             2400,
                             True)
        self.gali = Enemy(self.screen,
                          self.clock,
                          (1000, 640),
                          "monsters/gali",
                          (300, 1000),
                          16)
        self.lopop = Enemy(self.screen,
                           self.clock,
                           (1940, 700),
                           "monsters/lopop",
                           (1300, 1940),
                           20,
                           35)
        self.visited = [False, False]

    def run(self):
        utils.load_bg("nocturne.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            rel_x = self.player.stage["x"]
            if rel_x < consts.WIDTH_SCREEN:
                self.screen.blit(self.background, (rel_x, 0))
                self.screen.blit(self.ground.image, (rel_x, 742))
                self.actors_load(abs(rel_x))
                self.screen.blit(self.foreground, (rel_x, 585))
            else:
                self.screen.blit(self.background, (rel_x - self.background_width, 0))
                self.screen.blit(self.ground.image, (rel_x - self.background_width, 742))
                self.actors_load(rel_x)
                self.screen.blit(self.foreground, (rel_x - self.background_width, 585))
            pygame.display.flip()
            self.clock.tick(consts.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.next_level = None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "left"
                        self.player.velocity = -abs(self.player.velocity)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "right"
                        self.player.velocity = abs(self.player.velocity)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if (self.player.real_x+self.player.rect.width > 620
                                and self.player.real_x+self.player.rect.width < 745):
                            utils.loading_screen(self.screen)
                            hus = hena.Hena(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            self.visited[0] = True
                            utils.load_bg("nocturne.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
                            pygame.mixer.music.play(-1, 0.0)
                        elif (self.player.real_x+self.player.rect.width > 2140 and
                              self.player.real_x+self.player.rect.width < 2280):
                            #self.lopop.squashing = True # test to see if monster get squashed
                            utils.loading_screen(self.screen)
                            hus = hcesar.Hcesar(self.screen, self.clock, self.character)
                            hus.run()
                            del hus
                            self.visited[1] = True
                            utils.load_bg("nocturne.ogg")
                            pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
                            pygame.mixer.music.play(-1, 0.0)
                        elif (self.player.real_x+self.player.rect.width > 2280
                              and self.player.real_x+self.player.rect.width < 2401 and
                              all(i is True for i in self.visited)):
                            utils.loading_screen(self.screen)
                            mid = middle.Middle(self.screen, self.clock, self.character)
                            mid.run()
                            del mid
                            running = False
                            utils.loading_screen(self.screen)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        self.player.direction = "stand"

    def actors_load(self, rel_x):
        if self.player.real_x < 1500 and not self.gali.defeated:
            self.gali.roam(rel_x)
        if self.player.real_x > 1000 and not self.lopop.defeated:
            self.lopop.roam(rel_x)
        if (self.player.real_x+self.player.rect.width > 620
                and self.player.real_x+self.player.rect.width < 745):
            self.interact.float(rel_x)
        if (self.player.real_x+self.player.rect.width > 2140
                and self.player.real_x+self.player.rect.width < 2280):
            self.interact_2.float(1200)
        if (self.player.real_x+self.player.rect.width > 2280
                and self.player.real_x+self.player.rect.width < 2401 and
                all(i is True for i in self.visited)):
            self.interact_3.float(1200)
        self.player.update()
