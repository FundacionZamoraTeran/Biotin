import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import saves
from scenarios.utils.button import Button
from actors.player import Player
from actors.platform import Platform


class Entrance:
    """
        Class representing the prologue comics before minigame, recieves
        a Surface as a screen, and a Clock as clock
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
        self.font = utils.load_font("notoregu.ttf", 30)
        self.next_level = 1
        self.character = "ena" if self.slot["team_ena"] is True else "ezer"

        self.background = utils.load_image("background.png", "saar/stage_1")
        self.foreground = utils.load_image("foreground.png", "saar/stage_1")
        self.ground = Platform(self.screen, self.clock, (0, 742), "ground.png", "saar/stage_1")
        self.player = Player(self.screen, self.clock, (0, 640), self.character)

    def run(self):
        utils.load_bg("nocturne.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.ground.image, (0, 742))
            self.player.update()
            self.screen.blit(self.foreground, (0, 585))

            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.direction = "left"
                        self.player.speed = -abs(self.player.speed)
                    elif event.key == pygame.K_RIGHT:
                        self.player.direction = "right"
                        self.player.speed = abs(self.player.speed)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.direction = "stand"
                    elif event.key == pygame.K_RIGHT:
                        self.player.direction = "stand"
