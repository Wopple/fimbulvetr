import os
import sys
import pygame
import boundint

from common.constants import *

import drawable

class MapInterfaceItem(drawable.Drawable):
    def __init__(self):
        self.alpha = boundint.BoundInt(MAP_INTERFACE_ALPHA_MIN, 240, 240)
        self.alphaUp = True
        self.tick = MAP_INTERFACE_ALPHA_TICK
        self.pastImage = None
        self.pastHP = None

        self.image = pygame.Surface((1, 1))

    def update(self):
        oldVal = self.alpha.value
        
        if self.alphaUp:
            mult = 1
        else:
            mult = -1

        self.alpha.add(self.tick * mult)

        if (self.alpha.value != oldVal) or (not self.pastImage is self.image):
            self.image.set_alpha(self.alpha.value)

        self.pastImage = self.image

    def setAlphaFade(self, val):
        if val is True or val is False:
            self.alphaUp = val
