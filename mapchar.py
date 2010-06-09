import os
import sys
import pygame

import drawable

from constants import *

class MapChar(object):
    def __init__(self, inImages, team, name):
        self.team = team
        self.name = name
        self.images = inImages
        self.imageNum = -1
        self.precisePos = [0.00, 0.00]

        self.modifyImages()

        self.setImage(0)

    def setPos(self, inPos):
        self.precisePos[0] = float(inPos[0] * 1.00)
        self.precisePos[1] = float(inPos[1] * 1.00)

    def setImage(self, i):
        if i != self.imageNum:
            self.imageNum = i
            self.image = self.images[i]
            pos = ( int(self.precisePos[0]), int(self.precisePos[1]) )
            self.tokenRect = pygame.Rect(pos, self.image.get_size())

    def draw(self, screen, inZoom, inOffset):
            
        pos = (int(self.precisePos[0] * inZoom) + inOffset[0],
               int(self.precisePos[1] * inZoom) + inOffset[1])
        self.tokenRect.center = pos
        screen.blit(self.image, self.tokenRect.topleft)

    def modifyImages(self):
        colorSwap(self.images[0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_OFF[self.team], 100)

        colorSwap(self.images[1], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_HIGHLIGHTED[self.team], 100)

        colorSwap(self.images[2], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_SELECTED, 100)
        

def Hare(team, name="Unnamed Hare"):
    c = MapChar(HARE_TOKENS, team, name)
    return c
