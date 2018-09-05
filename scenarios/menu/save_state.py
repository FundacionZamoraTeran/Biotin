import pygame
from scenarios.utils import utils

STAGES = ("casa",
          "aldea_1",
          "aldea_2",
          "bazar",
          "bosque",
          "valle",
          "espacio",
          "ciudad",
          "cuerpo",
          "completado")

class SaveState(pygame.sprite.Sprite):
    """
       Acts as a slider constructor, expects:
       pos => a tuple with the X & Y positions,
       team => a tuple containing the X & Y positions
       title => a tuple with the title X & Y positions,
       slots => a tuple containg the two images state of the save state slots,
       folder => the base directory where the images are,
       save_slot => a dict which can be None or filled with save data.
       width => the width the slider should be
       height => the height the slider should be
       flag=> boolean to check whether the object is on focus or not
    """
    def __init__(self,
                 pos,
                 team,
                 title,
                 slots,
                 folder,
                 save_slot,
                 width=812,
                 height=135,
                 flag=False):
        # pygame Sprite class constructor
        pygame.sprite.Sprite.__init__(self)

        self.pos = pos
        self.pos_focused = (pos[0]-25, pos[1]-24)
        self.pos_team = team
        self.pos_title = title

        self.font = utils.load_font("xxii.ttf", 40)
        # set the states images
        if save_slot is None:
            title_text = "Partida Vacia"
            self.code = 0
            self.team = utils.load_image("e&c.png", folder, -1)
        else:
            title_text = save_slot["last_level_passed"]["name"]
            self.code = save_slot["last_level_passed"]["code"]
            if save_slot["team_ena"]:
                self.team = utils.load_image("e&c.png", folder, -1)
            else:
                self.team = utils.load_image("e&d.png", folder, -1)

        self.title = self.font.render(title_text,
                                      True,
                                      (255, 255, 255))

        self.base = utils.load_image(slots[0], folder, -1)
        self.end = utils.load_image(slots[1], folder, -1)

        self.stages = []

        for stage in STAGES:
            if save_slot is None or save_slot["stages"][stage] is False:
                self.stages.append(utils.load_image("inactive.png", folder, -1))
            else:
                self.stages.append(utils.load_image("active.png", folder, -1))

        # define the rects for all the sprite's states
        self.title_rect = self.title.get_rect(
            topleft=self.pos_title)

        self.team_rect = self.team.get_rect(
            topleft=self.pos_team)

        self.base_rect = self.base.get_rect(
            topleft=self.pos)
        self.end_rect = self.end.get_rect(
            topleft=self.pos_focused)

        #self.stages_rect = [] is it necessary?
        self.flag = flag

    def render(self, screen):
        if not self.flag:
            screen.blit(self.base, self.pos)
        else:
            screen.blit(self.end, self.pos_focused)
        screen.blit(self.team, self.pos_team)
        screen.blit(self.title, self.pos_title)
        stage_pos= (620,self.pos_title[1]+50)
        for stage in self.stages:
            screen.blit(stage, stage_pos)
            stage_pos= (stage_pos[0]+20, stage_pos[1])

    def on_focus(self, screen):
        screen.blit(self.end, self.pos_focused)
    def no_focus(self, screen):
        screen.blit(self.base, self.pos)
