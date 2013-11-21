import os
import sys
import pygame
import copy
import math

from common.constants import *

class RezSpark:

    def __init__(self, inCharacter):
        self.character = inCharacter
        self.pos = [int(self.character.precisePos[0]),
                    int(self.character.precisePos[1])]
        self.color = TERRITORY_DOT_COLORS[self.character.team+1]
        self.circles = []
        self.tick = REZ_SPARK_TICK_MAX


    def update(self):

        if (not self.character is None) and (not self.character.rezzing):
            self.character = None
            self.circles = [1, (1+REZ_SPARK_TICK_MAX)]

        newList = []
        for i in range(len(self.circles)):
            self.circles[i] += REZ_SPARK_INCREASE
            c = self.circles[i]
            alpha = self.getAlpha(c)
            if alpha > 0:
                newList.append(c)

        self.circles = newList

        if not self.character is None:
            self.tick += 1
            if self.tick >= REZ_SPARK_TICK_MAX:
                self.tick = 0
                self.circles.append(1)
        else:
            self.tick = 0


    def draw(self, screen, inZoom, inOffset):

        pos = ( int((self.pos[0] * inZoom) + inOffset[0]),
                int((self.pos[1] * inZoom) + inOffset[1]) )

        for c in self.circles:
            alpha = self.getAlpha(c)
            color = [REZ_SPARK_COLOR[0], REZ_SPARK_COLOR[1],
                     REZ_SPARK_COLOR[2], alpha]
            size = c
            if self.character is None:
                size *= REZ_SPARK_BIG_MULT

            pygame.draw.circle(screen, self.color, pos, size, 1)


    def getAlpha(self, val):
        if self.character is None:
            mult = REZ_SPARK_BIG_ALPHA_MULT
        else:
            mult = REZ_SPARK_ALPHA_MULT
        result = 255 - (val * mult)

        if (result < 0):
            result = 0

        return result


    def isRemovable(self):
        return ((self.character is None) and (len(self.circles) == 0))
