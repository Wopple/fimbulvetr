import os
import sys
import pygame

from constants import *

import drawable

class TargetMarker(object):
    def __init__(self):
        self.image = INTERFACE_GRAPHICS[2]
        self.rect = pygame.Rect((0, 0), self.image.get_size())

    def draw(self, screen, charPos, inZoom, inOffset):
        pos = [0, 0]
        for i in range(2):
            pos[i] = int(charPos[i] * inZoom) + inOffset[i]
        self.rect.center = (pos[0], pos[1])
        screen.blit(self.image, self.rect.topleft)
