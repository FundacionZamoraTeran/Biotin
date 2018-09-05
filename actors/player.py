import pygame

from scenarios.utils import utils
from scenarios.utils import consts

class Player(pygame.sprite.Sprite):
    """
        Class representing the playable character
    """
    def __init__(self, screen, clock, pos, character,
                 stage_width=1200, scrolls=False,
                 physics=(28, 250, 1.2), collisionable=False):
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
        self.jump_frames = 0
        self.jump_distance = physics[1]
        self.gravity = physics[2]
        self.catching = False

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
            "jump":{ "right": (utils.load_image("rjump1.png", self.character),
                               utils.load_image("rjump2.png", self.character),
                               utils.load_image("rjump3.png", self.character)),
                     "left": (utils.load_image("ljump1.png", self.character),
                              utils.load_image("ljump2.png", self.character),
                              utils.load_image("ljump3.png", self.character))},
            "net":{ "right": (utils.load_image("rnet1.png", self.character),
                               utils.load_image("rnet2.png", self.character),
                               utils.load_image("rnet3.png", self.character)),
                     "left": (utils.load_image("lnet1.png", self.character),
                              utils.load_image("lnet2.png", self.character),
                              utils.load_image("lnet3.png", self.character))},
            "climb": (utils.load_image("climb1.png", self.character),
                      utils.load_image("climb2.png", self.character))
        }
        self.direction = "stand"
        self.rect = pygame.Rect(pos, self.sprites["down"][0].get_size())
        self.rect.topleft = (self.x, self.rect.y)
        self.real_x = self.x # this means the real x position within the stage
        self.scrolls = scrolls
        self.platforms = []
        self.enemies = []
        self.collisionable = collisionable

    def control(self, x, y):
        self.rect.x += x
        self.rect.y += y

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > consts.WIDTH_SCREEN:
            self.rect.x = consts.WIDTH_SCREEN-self.rect.width

        if self.rect.y > 900:
            self.rect.y = 900-self.rect.height
        elif self.rect.y < 0:
            self.rect.y = 0

    def update(self):
        if self.collisionable and self.scroll:
            self.scrolled_collision_enemy()
        elif self.collisionable and not self.scroll:
            self.collision_enemy()
        else:
            pass
        self.jump()
        #self.catch()
        if (self.catching is True) and (self.direction == "right" or self.direction == "left"):
            self.control(self.velocity, 0)
            self.frame += 1
            if self.frame > 29:
                self.frame = 0
                self.catching = False
            self.screen.blit(self.sprites["net"][self.direction][self.frame//10], (self.rect.x, self.rect.y))
        elif (self.jumping is False and self.jump_frames == 0) and (self.direction == "right" or self.direction == "left"):
            self.control(self.velocity, 0)
            self.frame += 1
            if self.frame > 5:
                self.frame = 0
            self.screen.blit(self.sprites[self.direction][(self.frame//2)], (self.rect.x, self.rect.y))

        elif self.direction == "stand" and self.catching is True:
            if self.velocity >0:
                direction = "right"
            else:
                direction = "left"
            self.frame += 1
            if self.frame > 29:
                self.frame = 0
            self.screen.blit(self.sprites["net"][direction][self.frame//10], (self.rect.x, self.rect.y))
        elif self.direction == "stand":
            self.screen.blit(self.sprites["down"][0], (self.rect.x, self.rect.y))
        elif (self.jumping is True or (self.jump_frames > 0 and self.jumping is False)) and (self.direction == "right" or self.direction == "left"):
            self.control(self.velocity, 0)
            if self.jumping is True and self.jump_frames < 29:
                self.screen.blit(self.sprites["jump"][self.direction][0], (self.rect.x, self.rect.y))
            elif self.jump_frames > 0:
                self.screen.blit(self.sprites["jump"][self.direction][1], (self.rect.x, self.rect.y))
            else:
                self.screen.blit(self.sprites["jump"][self.direction][2], (self.rect.x, self.rect.y))

        if self.scrolls is True:
            self.scroll()

    def scroll(self):
        if self.direction != "stand":
            self.real_x += self.velocity
            if self.real_x > self.stage["width"]- self.rect.width:
                self.real_x = self.stage["width"] - self.rect.width
            elif self.real_x < 0:
                self.real_x = 0
            elif self.real_x <= self.stage["startscroll"]: pass
            elif self.real_x >= self.stage["width"] - self.stage["startscroll"]:
                self.rect.x = self.real_x - self.stage["width"] + consts.WIDTH_SCREEN
                self.stage["x"] = -(self.stage["width"]/2)
            else:
                self.rect.x = self.stage["startscroll"]
                self.stage["x"] += -self.velocity

    def collision_enemy(self): #use this if you dont scroll the background
        for block in self.enemies:
            if self.rect.colliderect(block.rect):
                if self.catching is True:
                    block.squashing = True
                elif self.jump_frames == 0:
                    # If we are moving right,
                    # set our right side to the left side of the item we hit
                    if self.velocity > 0:
                        self.rect.right = block.rect.left
                        self.real_x = self.rect.x
                    elif self.velocity < 0:
                        # Otherwise if we are moving left, do the opposite.
                        self.rect.left = block.rect.right
                        self.real_x = self.rect.x
                else:
                    block.squashing = True

    def scrolled_collision_enemy(self):
        blocks_hit_list = pygame.sprite.spritecollide(self, self.enemies, True)
        for block in blocks_hit_list:
            if self.catching is True:
                block.transformed = True
            elif self.jump_frames == 0:
                self.real_x = 150
                self.rect.left = 150
                self.stage["x"] = 0
            else:
                block.squashing = True

    def jump(self):
        if self.jumping is True:
            self.jump_frames += abs(self.velocity)
            self.rect.y -= abs(self.velocity)
            if self.jump_frames >= self.jump_distance:
                self.jumping = False
        elif self.jumping is False and self.jump_frames > 0:
            self.jump_frames -= abs(self.velocity)
            self.rect.y += abs(self.velocity)
        else:
            self.jump_frames = 0

    def set_sprite_groups(self, plats, enemies):
        self.platforms = plats
        self.enemies = enemies

    #experimental
    def on_ground(self, p_rects):
        collision = self.rect.collidelist(p_rects)
        if collision > -1:
            return True
        else:
            return False
