import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Player(pygame.sprite.Sprite):
    """
        Class representing the playable character
    """
    def __init__(self, screen, clock, pos, character, speed=12, jump_distance=18, gravity=1.2):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.clock = clock
        self.character = character
        self.x = pos[0]
        self.y = pos[1]
        self.frame = 0
        self.speed = speed
        self.jumping = False
        self.jump_distance = jump_distance
        self.gravity = gravity

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

        #test assets
        self.background = utils.load_image("test.png", "")
    def run(self):
        running = True

        while running:
            self.screen.blit(self.background, (0, 0))
            self.act()
            pygame.display.flip()
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction = "left"
                        self.speed = -abs(self.speed)
                    elif event.key == pygame.K_RIGHT:
                        self.direction = "right"
                        self.speed = abs(self.speed)
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

        self.rect.center = (self.x, self.y)

    def act(self):
        if self.direction == "right" or self.direction == "left":
            self.control(self.speed, 0)
            self.frame += 1
            if self.frame > 17:
                self.frame = 0
            pygame.display.update(self.screen.blit(self.sprites[self.direction][(self.frame//6)], (self.x, self.y)))
        else:#elif self.direction == "stand":
            pygame.display.update(self.screen.blit(self.sprites["down"][0], (self.x, self.y)))

    #experimental
    def on_ground(self):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False


