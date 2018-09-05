import sys
import os
import pygame
from scenarios.utils import utils, consts
from scenarios.menu.button import Button
from scenarios.menu.slider import Slider

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

class Option:
    def __init__(self, screen, clock):
        self.screen = screen
        self.screen2 = pygame.Surface((1200, 900),
                                      flags=pygame.SRCALPHA).convert_alpha()
        self.opts = ()
        self.path = os.path.join(MAIN_DIR, "../../config.ini")
        with open(self.path, "r+") as f:
            from ast import literal_eval
            self.opts = literal_eval(f.read()) # tuple (vx,bg,fx)
        self.clock = clock
        self.background = utils.load_image("options_door/background.png", "menu")
        self.title = utils.load_image("options_door/title.png", "menu")
        self.voice_slider = Slider((380, 350),
                                   (210, 350),
                                   ("vt1.png",
                                    "vt2.png"),
                                   "menu/options_door",
                                   level=self.opts[0],
                                   flag=True)
        self.music_slider = Slider((380, 480),
                                   (210, 480),
                                   ("mt1.png",
                                    "mt2.png"),
                                   "menu/options_door",
                                   level=self.opts[1])
        self.fx_slider = Slider((380, 610),
                                (180, 610),
                                ("ft1.png",
                                 "ft2.png",),
                                "menu/options_door",
                                level=self.opts[2])
        self.exit_button = Button(1030,
                                  120,
                                  "exit.png",
                                  "exit.png",
                                  "exit.png",
                                  36,
                                  38)
    def save(self):
        opts = (self.voice_slider.level, self.music_slider.level, self.fx_slider.level)
        with open(self.path, "w") as f:
            f.write(str(opts))

    def run(self):
        """ control the actions happening on the Help modal """
        running = True
        while running:
            for event in [pygame.event.wait()] + pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == consts.K_CIRCLE:
                        running = False
                        self.save()
                        pygame.mixer.music.set_volume(self.opts[1])
                    elif event.key == pygame.K_RETURN or event.key == consts.K_CHECK:
                        running = False
                        self.save()
                        pygame.mixer.music.set_volume(self.opts[1])
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        if self.voice_slider.flag is True:
                            self.voice_slider.flag = False
                            self.music_slider.flag = True
                            self.music_slider.on_title_focus(self.screen2)
                        elif self.music_slider.flag is True:
                            self.music_slider.flag = False
                            self.fx_slider.flag = True
                            self.fx_slider.on_title_focus(self.screen2)
                    elif event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        if self.music_slider.flag is True:
                            self.music_slider.flag = False
                            self.voice_slider.flag = True
                            self.voice_slider.on_title_focus(self.screen2)
                        elif self.fx_slider.flag is True:
                            self.fx_slider.flag = False
                            self.music_slider.flag = True
                            self.music_slider.on_title_focus(self.screen2)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.voice_slider.flag is True:
                            self.voice_slider.increase_level(self.screen2)
                        elif self.music_slider.flag is True:
                            self.music_slider.increase_level(self.screen2)
                        elif self.fx_slider.flag is True:
                            self.fx_slider.increase_level(self.screen2)
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.voice_slider.flag is True:
                            self.voice_slider.decrease_level(self.screen2)
                        elif self.music_slider.flag is True:
                            self.music_slider.decrease_level(self.screen2)
                        elif self.fx_slider.flag is True:
                            self.fx_slider.decrease_level(self.screen2)

            self.screen2.blit(self.background, (0, 0))
            self.screen2.blit(self.title, (460, 190))
            if self.voice_slider.flag is True:
                self.screen2.blit(self.voice_slider.focused_title, (210, 350))
                self.screen2.blit(self.music_slider.unfocused_title, (210, 480))
                self.screen2.blit(self.fx_slider.unfocused_title, (180, 610))
            elif self.music_slider.flag is True:
                self.screen2.blit(self.voice_slider.unfocused_title, (210, 350))
                self.screen2.blit(self.music_slider.focused_title, (210, 480))
                self.screen2.blit(self.fx_slider.unfocused_title, (180, 610))
            else:
                self.screen2.blit(self.voice_slider.unfocused_title, (210, 350))
                self.screen2.blit(self.music_slider.unfocused_title, (210, 480))
                self.screen2.blit(self.fx_slider.focused_title, (180, 610))
            self.screen2.blit(self.voice_slider.get_current_level_image(), (380, 350))
            self.screen2.blit(self.music_slider.get_current_level_image(), (380, 480))
            self.screen2.blit(self.fx_slider.get_current_level_image(), (380, 610))
            self.screen.blit(self.screen2, (0, 0))
            self.screen.blit(self.exit_button.base, (1030, 120))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
