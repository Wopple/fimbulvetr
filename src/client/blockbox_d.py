import pygame

from client.constants import *

from client.drawable import ItemDrawable

class BlockboxDrawable(ItemDrawable):
    def __init__(self, item):
        super(BlockboxDrawable, self).__init__(item, rect=item.rect)
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(BLOCKBOX_COLOR)
        self.image.set_alpha(BLOCKBOX_ALPHA)
