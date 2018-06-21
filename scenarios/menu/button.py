import pygame
from scenarios.utils import utils

class Button(pygame.sprite.Sprite):
    """
       Acts as a button constructor, expects:
       x => X position,
       y => Y position,
       base_file => the base image the button will display
       transition_file => transition between states image
       end_file => final state image,
       width => the width the button should be
       height => the height the button should be
       folder => the folder where the images are in
    """
    def __init__(self, x, y, base_file, transition_file,
                 end_file=None, width=100, height=100, folder="menu", flag=False):
        # pygame Sprite class constructor
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.pos = (x, y)

        # set the states images
        self.base = utils.load_image(base_file, folder, -1, (width, height))
        self.transition = utils.load_image(transition_file,
                                           folder, -1, (width, height))
        if end_file is not None:
            self.end = utils.load_image(end_file, folder, -1, (width, height))
            self.end_rect = self.end.get_rect(topleft=self.pos)

        # define the rects for all the sprite's states
        self.base_rect = self.base.get_rect(topleft=self.pos)
        self.transition_rect = self.transition.get_rect(topleft=self.pos)

        self.flag = flag

    def on_selection(self, screen, mouse_x, mouse_y):
        """
           makes the button change state/animation while selected
           requires three state images.
        """
        if (self.flag is False and
                self.base_rect.collidepoint(mouse_x, mouse_y)):
            pygame.display.update(screen.blit(self.transition, (self.x, self.y)))
            pygame.display.update(screen.blit(self.end, (self.x, self.y)))
            self.base, self.end = self.end, self.base
            self.flag = True
        elif (self.flag is True and
              not self.base_rect.collidepoint(mouse_x, mouse_y)):
            # the blits can be deleted if found that they slow performance
            pygame.display.update(screen.blit(self.transition, (self.x, self.y)))
            pygame.display.update(screen.blit(self.end, (self.x, self.y)))
            self.base, self.end = self.end, self.base
            self.flag = False

    def on_focus(self, screen):
        pygame.display.update(screen.blit(self.transition, (self.x, self.y)))
        pygame.display.update(screen.blit(self.end, (self.x, self.y)))
        self.base, self.end = self.end, self.base
    def on_focus_altern(self, screen):
        pygame.display.update(screen.blit(self.transition, (self.x, self.y)))
        self.base, self.transition = self.transition, self.base


    def on_selection_altern(self, screen, mouse_x, mouse_y):
        """
           makes the button change state/animation while selected
           requires two state images.
        """
        if (self.flag is False and
                self.base_rect.collidepoint(mouse_x, mouse_y)):
            pygame.display.update(screen.blit(self.transition, (self.x, self.y)))
            self.base, self.transition = (self.transition, self.base)
            self.flag = True
        elif (self.flag is True and
              not self.base_rect.collidepoint(mouse_x, mouse_y)):
            pygame.display.update(screen.blit(self.transition, (self.x, self.y)))
            self.base, self.transition = (self.transition, self.base)
            self.flag = False

    def flip(self):
        """
            Flips horizontally the button's base,
            transition and end images.
        """
        self.base = pygame.transform.flip(self.base, 180, 0)
        self.transition = pygame.transform.flip(self.transition, 180, 0)
        if self.end_file is not None:
            self.end = pygame.transform.flip(self.end, 180, 0)
        return self
