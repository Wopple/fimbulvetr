import os
import sys
import pygame

import drawable

from constants import *

class MapChar(object):
    def __init__(self):
        self.tokenRect = pygame.Rect((0, 0), MAP_CHAR_TOKEN_SIZE)
        self.precisePos = [0.00, 0.00]
        self.tokenImage = pygame.Surface(MAP_CHAR_TOKEN_SIZE)

    def setPos(self, inPos):
        self.precisePos[0] = float(inPos[0] * 1.00)
        self.precisePos[1] = float(inPos[1] * 1.00)

    def draw(self, screen, inZoom, inOffset):
        pos = (int(self.precisePos[0] * inZoom) + inOffset[0],
               int(self.precisePos[1] * inZoom) + inOffset[1])
        self.tokenRect.center = pos
        screen.blit(self.tokenImage, self.tokenRect.topleft)

def Hare():
    c = MapChar()
    return c
