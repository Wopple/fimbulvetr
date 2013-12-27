import os
import sys
import pygame
import copy

from pygame.locals import *

import drawable
import util

from common.constants import *
from client.constants import *

from common.util.rect import Rect

class MapItem(object):

    def __init__(self, inPos, inImages):
        self.precisePos = []
        for i in inPos:
            self.precisePos.append(i * 1.00)
        self.images = []
        for i in inImages:
            self.images.append([copy.copy(i[0]), i[1]])
        self.imageNum = -1

        self.triggerArea = None
        self.triggerRect = None

        self.modifyImages()
        self.setImage(0)
        

    def setPos(self, inPos):
        self.precisePos[0] = float(inPos[0] * 1.00)
        self.precisePos[1] = float(inPos[1] * 1.00)

    def setImage(self, i):
        if i != self.imageNum:
            self.imageNum = i
            self.image = self.images[i][0]
            self.tokenRect = Rect((0, 0), self.image.get_size())

    def draw(self, screen, inZoom, inOffset):
        if (not self.blinkOn) or self.removed:
            return
        
        self.setImagePos(inZoom, inOffset)
        screen.blit(self.image, self.tokenRect.topleft)
        
        if (SHOW_TRIGGER_AREA and (not self.triggerArea is None) and
            (not self.triggerRect is None)):
            screen.blit(self.triggerArea, self.triggerRect.topleft)

    def setImagePos(self, inZoom, inOffset):
        imageOffset = self.images[self.imageNum][1]
        pos = (int(self.precisePos[0] * inZoom) + inOffset[0] - imageOffset[0],
               int(self.precisePos[1] * inZoom) + inOffset[1] - imageOffset[1])
        self.tokenRect.topleft = pos
        
        if not self.triggerRect is None:
            self.triggerRect.center = (int(self.precisePos[0] * inZoom) + inOffset[0],
                                             int(self.precisePos[1] * inZoom) + inOffset[1])



    def createTriggerArea(self, zoom):
        r = int(self.triggerSize * zoom)
        d = int(r*2)
        self.triggerArea = pygame.Surface((d, d), SRCALPHA)
        self.triggerArea.fill ((0, 0, 0, 0))
        pygame.draw.circle(self.triggerArea, self.triggerColor,
                           (r, r), r)
        self.triggerRect = Rect((0, 0), (d, d))
