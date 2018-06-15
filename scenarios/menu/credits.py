import pygame
import sys
from scenarios.utils import utils
from scenarios.menu.button import Button

class Credit:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((900, 600),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.clock = clock
        self.exit_button = Button(1030,
                                  140,
                                  "exit.png",
                                  "exit.png",
                                  "exit.png",
                                  30,
                                  30)

        # Logos

        self.ci = utils.load_image("ci.png", "menu", -1, (250, 250))
        self.fzt = utils.load_image("fzt.png", "menu", -1, (250, 250))
        self.thb = utils.load_image("thb.png", "menu", -1, (150, 173))

        # People

        self.luis = utils.load_image("luis_card.png", "menu", size=(140, 170))
        self.rebeca = utils.load_image("rebe_card.png", "menu", size=(140, 170))
        self.hans = utils.load_image("hp_card.png", "menu", size=(140, 170))
        self.macri = utils.load_image("macris_card.png", "menu", size=(140, 170))
        self.ana = utils.load_image("ana_card.png", "menu", size=(140, 170))

        # Fonts

        self.title = utils.load_font("roboslab.ttf", 50)
        self.subtitle = utils.load_font("roboslab.ttf", 40)

    def run(self):
        """ control the actions happening on the Help modal"""
        credit_text = self.title.render("Creditos",
                                        True,
                                        (0, 0, 0),
                                        (250, 207, 149, 220))
        thb_text = self.subtitle.render("Equipo",
                                        True,
                                        (0, 0, 0),
                                        (250, 207, 149, 220))
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.exit_button.base_rect.collidepoint(mouse_x, mouse_y):
                        running = False
                if event.type == pygame.KEYDOWN:
                    print(pygame.key.get_pressed())
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif  event.key == pygame.K_RETURN:
                        running = False

            # set all the elements to appear on the credit's modal

            self.screen2.fill((250, 207, 149, 220))
            self.screen2.blit(credit_text, (365, 40))
            self.screen2.blit(self.fzt, (50, 100))
            self.screen2.blit(self.ci, (600, 100))
            self.screen2.blit(self.thb, (390, 145))
            self.screen2.blit(thb_text, (400, 330))
            self.screen2.blit(self.luis, (90, 400))
            self.screen2.blit(self.macri, (250, 400))
            self.screen2.blit(self.rebeca, (400, 400))
            self.screen2.blit(self.hans, (540, 400))
            self.screen2.blit(self.ana, (680, 400))

            # make everything appear on the screen

            self.screen.blit(self.screen2, (150, 150))
            self.screen.blit(self.exit_button.base, (1030, 140))
            pygame.display.flip()
            self.clock.tick(30)
