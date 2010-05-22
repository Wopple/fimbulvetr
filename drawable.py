import os

import pygame

from constants import *

class Drawable(object):
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

