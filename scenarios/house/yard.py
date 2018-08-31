import sys
import pygame

from scenarios.utils import utils
from scenarios.utils import consts
from scenarios.utils import dialogue
from scenarios.utils.button import Button

class Yard:
    """
        Class representing the prologue part 4 comic after minigame, recieves
        a Surface as a screen, a Clock as clock
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.fx_channel = pygame.mixer.Channel(0)
        self.fx_channel.set_volume(consts.FX_VOLUME)
        self.vx_channel = pygame.mixer.Channel(1)
        self.vx_channel.set_volume(consts.VX_VOLUME)
        self.font = utils.load_font("notoregu.ttf", 20)

        self.current_slide = 1

        # using a dict to avoid creating >30 variables per elements
        self.slides = {
            "1" : utils.load_image("1.png", "house/yard"),
            "2" : utils.load_image("2.png", "house/yard"),
            "3" : utils.load_image("3.png", "house/yard"),
            "4" : utils.load_image("4.png", "house/yard"),
            "5" : utils.load_image("5.png", "house/yard"),
            "6" : utils.load_image("6.png", "house/yard"),
            "7" : utils.load_image("7.png", "house/yard"),
            "8" : utils.load_image("8.png", "house/yard"),
            "9" : utils.load_image("9.png", "house/yard"),
            "10" : utils.load_image("10.png", "house/yard"),
            "11" : utils.load_image("11.png", "house/yard"),
            "12" : utils.load_image("12.png", "house/yard"),
            "13" : utils.load_image("13.png", "house/yard"),
            "14-1" : utils.load_image("14-1.png", "house/yard"),
            "14-2" : utils.load_image("14-2.png", "house/yard"),
            "14-3" : utils.load_image("14-3.png", "house/yard"),
            "14-4" : utils.load_image("14-4.png", "house/yard"),
            "14-5" : utils.load_image("14-5.png", "house/yard"),
            "14-6" : utils.load_image("14-6.png", "house/yard"),
            "15" : utils.load_image("15.png", "house/yard"),
            "16" : utils.load_image("16.png", "house/yard"),
            "17" : utils.load_image("17.png", "house/yard"),
            "18" : utils.load_image("18.png", "house/yard"),
            "19" : utils.load_image("19.png", "house/yard"),
            "20" : utils.load_image("20.png", "house/yard"),
            "21" : utils.load_image("21.png", "house/yard"),
            "22" : utils.load_image("22.png", "house/yard"),
            "23" : utils.load_image("23.png", "house/yard"),
            "24" : utils.load_image("24.png", "house/yard"),
            "25" : utils.load_image("25.png", "house/yard"),
            "26" : utils.load_image("26.png", "house/yard"),
            "27" : utils.load_image("27.png", "house/yard"),
            "28" : utils.load_image("28.png", "house/yard"),
            "29" : utils.load_image("29.png", "house/yard"),
            "30" : utils.load_image("30.png", "house/yard")
        }

        self.bubbles = {
            "1" : utils.load_image("D1.png", "house/yard"),
            "2" : utils.load_image("D2.png", "house/yard"),
            "3" : utils.load_image("D3.png", "house/yard"),
            "4" : utils.load_image("D4.png", "house/yard"),
            "5" : utils.load_image("D5.png", "house/yard"),
            "7" : utils.load_image("D7.png", "house/yard"),
            "8" : utils.load_image("D8.png", "house/yard"),
            "9" : utils.load_image("D9.png", "house/yard"),
            "10" : utils.load_image("D10.png", "house/yard"),
            "11" : utils.load_image("D11.png", "house/yard"),
            "12" : utils.load_image("D12.png", "house/yard"),
            "13" : utils.load_image("D13.png", "house/yard"),
            "15" : utils.load_image("D15.png", "house/yard"),
            "16" : utils.load_image("D16.png", "house/yard"),
            "17" : utils.load_image("D17.png", "house/yard"),
            "18" : utils.load_image("D18.png", "house/yard"),
            "19" : utils.load_image("D19.png", "house/yard"),
            "20" : utils.load_image("D20.png", "house/yard"),
            "21" : utils.load_image("D21.png", "house/yard"),
            "22" : utils.load_image("D22.png", "house/yard"),
            "23" : utils.load_image("D23.png", "house/yard"),
            "24" : utils.load_image("D24.png", "house/yard"),
            "25" : utils.load_image("D25.png", "house/yard"),
            "26" : utils.load_image("D26.png", "house/yard"),
            "27" : utils.load_image("D27.png", "house/yard"),
            "28" : utils.load_image("D28.png", "house/yard"),
            "29" : utils.load_image("D29.png", "house/yard"),
            "30" : utils.load_image("D30.png", "house/yard"),
        }

        self.voices = {
            "1" : utils.load_vx("house/yard/1.ogg"),
            "2" : utils.load_vx("house/yard/2.ogg"),
            "3" : utils.load_vx("house/yard/3.ogg"),
            "4" : utils.load_vx("house/yard/4.ogg"),
            "5" : utils.load_vx("house/yard/5.ogg"),
            "6" : utils.load_vx("house/yard/6.ogg"),
            "7" : utils.load_vx("house/yard/7.ogg"),
            "8" : utils.load_vx("house/yard/8.ogg"),
            "9" : utils.load_vx("house/yard/9.ogg"),
            "10" : utils.load_vx("house/yard/10.ogg"),
            "11" : utils.load_vx("house/yard/11.ogg"),
            "12" : utils.load_vx("house/yard/12.ogg"),
            "13" : utils.load_vx("house/yard/13.ogg"),
            "14" : utils.load_vx("house/yard/14.ogg"),
            "15" : utils.load_vx("house/yard/15.ogg"),
            "16" : utils.load_vx("house/yard/16.ogg"),
            "17" : utils.load_vx("house/yard/17.ogg"),
            "18" : utils.load_vx("house/yard/18.ogg"),
            "19" : utils.load_vx("house/yard/19.ogg"),
            "20" : utils.load_vx("house/yard/20.ogg"),
            "21" : utils.load_vx("house/yard/21.ogg"),
            "22" : utils.load_vx("house/yard/22.ogg"),
            "23" : utils.load_vx("house/yard/23.ogg"),
            "24" : utils.load_vx("house/yard/24.ogg"),
            "25" : utils.load_vx("house/yard/25.ogg"),
            "26" : utils.load_vx("house/yard/26.ogg"),
            "27" : utils.load_vx("house/yard/27.ogg"),
            "28" : utils.load_vx("house/yard/28.ogg"),
            "29" : utils.load_vx("house/yard/29.ogg"),
            "30" : utils.load_vx("house/yard/30.ogg")
        }
        self.dialogue = dialogue.get_dialogue_subscenario("casa", "patio")
        self.next = Button((918, 780), "yard/next1.png", "yard/next2.png", 257, 99, "house")
        self.prev = Button((25, 780), "yard/prev1.png", "yard/prev2.png", 257, 99, "house")
        self.played = [0] * 30

    def run(self):
        utils.load_bg("house.ogg")
        pygame.mixer.music.set_volume(consts.BG_VOLUME-0.3)
        pygame.mixer.music.play(-1, 0.0)
        running = True

        while running:
            self.render_scene(self.current_slide)
            self.screen.blit(self.next.base, (918, 780))
            self.screen.blit(self.prev.base, (25, 780))
            pygame.display.flip()
            self.clock.tick(consts.FPS)
            for event in [pygame.event.wait()] + pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        if self.current_slide != 1:
                            self.vx_channel.stop()
                            self.prev.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide -= 1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        if self.current_slide != 30:
                            self.vx_channel.stop()
                            self.next.on_press(self.screen)
                            self.played[self.current_slide-1] = 0
                            self.current_slide += 1
                        else:
                            running = False

    def render_scene(self, number):
        if number is 1:
            self.screen.blit(self.slides["1"], (0, 0))
            if self.played[0] == 0:
                self.vx_channel.play(self.voices["1"])
                self.played[0] = 1
            self.screen.blit(self.bubbles["1"], (570, 210))
        elif number == 2:
            self.screen.blit(self.slides["2"], (0, 0))
            if self.played[1] == 0:
                self.vx_channel.play(self.voices["2"])
                self.played[1] = 1
            self.screen.blit(self.bubbles["2"], (570, 210))
        elif number == 3:
            self.screen.blit(self.slides["3"], (0, 0))
            if self.played[2] == 0:
                self.vx_channel.play(self.voices["3"])
                self.played[2] = 1
            self.screen.blit(self.bubbles["3"], (570, 210))
        elif number == 4:
            self.screen.blit(self.slides["4"], (0, 0))
            if self.played[3] == 0:
                self.vx_channel.play(self.voices["4"])
                self.played[3] = 1
            self.screen.blit(self.bubbles["4"], (390, 220))
        elif number == 5:
            self.screen.blit(self.slides["5"], (0, 0))
            if self.played[4] == 0:
                self.vx_channel.play(self.voices["5"])
                self.played[4] = 1
            self.screen.blit(self.bubbles["5"], (390, 220))
        elif number == 6:
            self.screen.blit(self.slides["6"], (0, 0))
            if self.played[5] == 0:
                self.vx_channel.play(self.voices["6"])
                self.played[5] = 1
            text = self.font.render(self.dialogue['6'],
                                    True,
                                    (246, 212, 0))
            self.screen.blit(text, (300, 810))
        elif number == 7:
            self.screen.blit(self.slides["7"], (0, 0))
            if self.played[6] == 0:
                self.vx_channel.play(self.voices["7"])
                self.played[6] = 1
            self.screen.blit(self.bubbles["7"], (300, 200))
        elif number == 8:
            self.screen.blit(self.slides["8"], (0, 0))
            if self.played[7] == 0:
                self.vx_channel.play(self.voices["8"])
                self.played[7] = 1
            self.screen.blit(self.bubbles["8"], (300, 200))
        elif number == 9:
            self.screen.blit(self.slides["9"], (0, 0))
            if self.played[8] == 0:
                self.vx_channel.play(self.voices["9"])
                self.played[8] = 1
            self.screen.blit(self.bubbles["9"], (80, 230))
        elif number == 10:
            self.screen.blit(self.slides["10"], (0, 0))
            if self.played[9] == 0:
                self.vx_channel.play(self.voices["10"])
                self.played[9] = 1
            self.screen.blit(self.bubbles["10"], (700, 250))
        elif number == 11:
            self.screen.blit(self.slides["11"], (0, 0))
            if self.played[10] == 0:
                self.vx_channel.play(self.voices["11"])
                self.played[10] = 1
            self.screen.blit(self.bubbles["11"], (700, 250))
        elif number == 12:
            self.screen.blit(self.slides["12"], (0, 0))
            if self.played[11] == 0:
                self.vx_channel.play(self.voices["12"])
                self.played[11] = 1
            self.screen.blit(self.bubbles["12"], (700, 250))
        elif number == 13:
            self.screen.blit(self.slides["13"], (0, 0))
            if self.played[12] == 0:
                self.vx_channel.play(self.voices["13"])
                self.played[12] = 1
            self.screen.blit(self.bubbles["13"], (570, 210))
        elif number == 14:
            #special one
            if self.played[13] == 0:
                self.vx_channel.play(self.voices["14"])
                self.played[13] = 1
                self.screen.blit(self.slides["14-1"], (0, 0))
                self.screen.blit(self.next.base, (918, 780))
                self.screen.blit(self.prev.base, (25, 780))
                text = self.font.render(self.dialogue['14'],
                                        True,
                                        (246, 212, 0))
                self.screen.blit(text, (360, 810))
                pygame.display.flip()
                pygame.display.update(self.screen.blit(self.slides["14-2"], (732, 262)))
                pygame.time.delay(60)
                pygame.display.update(self.screen.blit(self.slides["14-3"], (732, 262)))
                pygame.time.delay(60)
                pygame.display.update(self.screen.blit(self.slides["14-4"], (732, 262)))
                pygame.time.delay(60)
                pygame.display.update(self.screen.blit(self.slides["14-5"], (732, 262)))
                pygame.time.delay(60)
                pygame.display.update(self.screen.blit(self.slides["14-6"], (732, 262)))

        elif number == 15:
            self.screen.blit(self.slides["15"], (0, 0))
            if self.played[14] == 0:
                self.vx_channel.play(self.voices["15"])
                self.played[14] = 1
            self.screen.blit(self.bubbles["15"], (650, 200))
        elif number == 16:
            self.screen.blit(self.slides["16"], (0, 0))
            if self.played[15] == 0:
                self.vx_channel.play(self.voices["16"])
                self.played[15] = 1
            self.screen.blit(self.bubbles["16"], (260, 200))
        elif number == 17:
            self.screen.blit(self.slides["17"], (0, 0))
            if self.played[16] == 0:
                self.vx_channel.play(self.voices["17"])
                self.played[16] = 1
            self.screen.blit(self.bubbles["17"], (380, 210))
        elif number == 18:
            self.screen.blit(self.slides["18"], (0, 0))
            if self.played[17] == 0:
                self.vx_channel.play(self.voices["18"])
                self.played[17] = 1
            self.screen.blit(self.bubbles["18"], (650, 200))
        elif number == 19:
            self.screen.blit(self.slides["19"], (0, 0))
            if self.played[18] == 0:
                self.vx_channel.play(self.voices["19"])
                self.played[18] = 1
            self.screen.blit(self.bubbles["19"], (650, 200))
        elif number == 20:
            self.screen.blit(self.slides["20"], (0, 0))
            if self.played[19] == 0:
                self.vx_channel.play(self.voices["20"])
                self.played[19] = 1
            self.screen.blit(self.bubbles["20"], (650, 200))
        elif number == 21:
            self.screen.blit(self.slides["21"], (0, 0))
            if self.played[20] == 0:
                self.vx_channel.play(self.voices["21"])
                self.played[20] = 1
            self.screen.blit(self.bubbles["21"], (650, 200))
        elif number == 22:
            self.screen.blit(self.slides["22"], (0, 0))
            if self.played[21] == 0:
                self.vx_channel.play(self.voices["22"])
                self.played[21] = 1
            self.screen.blit(self.bubbles["22"], (650, 200))
        elif number == 23:
            self.screen.blit(self.slides["23"], (0, 0))
            if self.played[22] == 0:
                self.vx_channel.play(self.voices["23"])
                self.played[22] = 1
            self.screen.blit(self.bubbles["23"], (650, 200))
        elif number == 24:
            self.screen.blit(self.slides["24"], (0, 0))
            if self.played[23] == 0:
                self.vx_channel.play(self.voices["24"])
                self.played[23] = 1
            self.screen.blit(self.bubbles["24"], (260, 200))
        elif number == 25:
            self.screen.blit(self.slides["25"], (0, 0))
            if self.played[24] == 0:
                self.vx_channel.play(self.voices["25"])
                self.played[24] = 1
            self.screen.blit(self.bubbles["25"], (300, 20))
        elif number == 26:
            self.screen.blit(self.slides["26"], (0, 0))
            if self.played[25] == 0:
                self.vx_channel.play(self.voices["26"])
                self.played[25] = 1
            self.screen.blit(self.bubbles["26"], (610, 420))
        elif number == 27:
            self.screen.blit(self.slides["27"], (0, 0))
            if self.played[26] == 0:
                self.vx_channel.play(self.voices["27"])
                self.played[26] = 1
            self.screen.blit(self.bubbles["27"], (650, 200))
        elif number == 28:
            self.screen.blit(self.slides["28"], (0, 0))
            if self.played[27] == 0:
                self.vx_channel.play(self.voices["28"])
                self.played[27] = 1
            self.screen.blit(self.bubbles["28"], (650, 200))
        elif number == 29:
            self.screen.blit(self.slides["29"], (0, 0))
            if self.played[28] == 0:
                self.vx_channel.play(self.voices["29"])
                self.played[28] = 1
            self.screen.blit(self.bubbles["29"], (450, 200))
        elif number == 30:
            self.screen.blit(self.slides["30"], (0, 0))
            if self.played[29] == 0:
                self.vx_channel.play(self.voices["30"])
                self.played[29] = 1
            self.screen.blit(self.bubbles["30"], (280, 200))
