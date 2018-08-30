import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Player(pygame.sprite.Sprite):
    """
        Class representing the playable character
    """
    def __init__(self, screen, clock, pos, character,
                 stage_width=1200, scrolls=False, physics=(12, 18, 1.2)):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.character = character
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.stage = {
            "width": stage_width,
            "x": 0,
            "startscroll": consts.WIDTH_SCREEN/2
        }
        self.velocity = physics[0]
        self.jumping = False
        self.jump_distance = physics[1]
        self.gravity = physics[2]

        self.sprites = {
            "up": (utils.load_image("up1.png", self.character),
                   utils.load_image("up2.png", self.character),
                   utils.load_image("up3.png", self.character)),
            "down": (utils.load_image("down1.png", self.character),
                     utils.load_image("down2.png", self.character),
                     utils.load_image("down3.png", self.character)),
            "left": (utils.load_image("left1.png", self.character),
                     utils.load_image("left2.png", self.character),
                     utils.load_image("left3.png", self.character)),
            "right": (utils.load_image("right1.png", self.character),
                      utils.load_image("right2.png", self.character),
                      utils.load_image("right3.png", self.character)),
            "jump": (utils.load_image("jump1.png", self.character),
                     utils.load_image("jump2.png", self.character),
                     utils.load_image("jump3.png", self.character)),
            "climb": (utils.load_image("climb1.png", self.character),
                      utils.load_image("climb2.png", self.character))
        }
        self.direction = "stand"
        self.rect = pygame.Rect(pos, self.sprites["left"][0].get_size())
        self.rect.topleft = (self.x, self.y)
        self.real_x = self.x # this means the real x position within the stage
        self.scrolls = scrolls
        #test assets
        self.background = utils.load_image("test.png", "")
    def run(self):
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.update()
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = "left"
                        self.velocity = -abs(self.velocity)
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"
                        self.velocity = abs(self.velocity)
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        self.direction = "jump"
                        self.jumping = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.direction = "stand"
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "stand"

    def control(self, x, y):
        self.x += x
        self.y += y

        if self.x < 0:
            self.x = 0
        elif self.x+self.rect.width > consts.WIDTH_SCREEN:
            self.x = consts.WIDTH_SCREEN-self.rect.width

        if self.y > 900:
            self.y = 900-self.rect.height
        elif self.y < 0:
            self.y = 0

        self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.direction == "right" or self.direction == "left":
            self.control(self.velocity, 0)
            self.frame += 1
            if self.frame > 17:
                self.frame = 0
            self.screen.blit(self.sprites[self.direction][(self.frame//6)], (self.x, self.y))
        else:#elif self.direction == "stand":
            self.screen.blit(self.sprites["down"][0], (self.x, self.y))
        if self.scrolls is True:
            self.scroll()

    def scroll(self):
        if self.direction != "stand":
            self.real_x += self.velocity
            if self.real_x > self.stage["width"]- self.rect.width:
                self.real_x = self.stage["width"] - self.rect.width
            elif self.real_x < 0:
                self.real_x = 0
            elif self.real_x <= self.stage["startscroll"]: self.stage["x"] = 0
            elif self.real_x >= self.stage["width"] - self.stage["startscroll"]:
                self.x = self.real_x - self.stage["width"] + consts.WIDTH_SCREEN
                self.stage["x"] = -(self.stage["width"]/2)
            else:
                self.x = self.stage["startscroll"]
                self.stage["x"] += -self.velocity


    #experimental
    def on_ground(self):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False
