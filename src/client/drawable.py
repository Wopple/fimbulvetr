import os

import pygame

from common.constants import *
from client.constants import *

class Drawable(object):
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class ItemDrawable(object):
    """
    This is intended to wrap a model-only item with a Drawable
    so it can be drawn in a view.
    """

    def __init__(self, item, rect=None, image=None):
        super(ItemDrawable, self).__init__(rect, image)
        self.item = item
