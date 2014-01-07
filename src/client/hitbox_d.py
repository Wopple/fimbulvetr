import pygame

from client.constants import *

from client.drawable import ItemDrawable

class HurtboxDrawable(ItemDrawable):
    def __init__(self, item):
        super(HurtboxDrawable, self).__init__(item, rect=item.rect)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(HITBOX_COLOR)
        self.image.set_alpha(HITBOX_ALPHA)
