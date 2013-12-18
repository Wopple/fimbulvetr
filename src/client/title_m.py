import os
import sys
import pygame

import mvc
import boundint
import textrect

from common.constants import *
from client.constants import *

class Model(mvc.Model):
    def __init__(self):
        super(Model, self).__init__()
        self.fadeSurface = pygame.Surface(SCREEN_SIZE)
        self.fadeSurfaceColor = []
        for i in range(3):
            self.fadeSurfaceColor.append(boundint.BoundInt(0, INTRO_MAX_FADE, 0))

        self.transSurface = pygame.Surface(SCREEN_SIZE)
        self.transSurface.fill((INTRO_MAX_FADE, INTRO_MAX_FADE, INTRO_MAX_FADE))
        self.transAlpha = boundint.BoundInt(0, 255, 255)
        self.centerTextPos = (0, SCREEN_SIZE[1]/2)
        self.stage = 0
        self.ticker = 0

        self.textMessages = [ ("Games from Beyond the Farth", 2, ALMOST_BLACK, WHITE, 1, True) ]
        self.textRects = []
        for i in self.textMessages:
            f = FONTS[i[1]]
            size = (SCREEN_SIZE[0], f.get_linesize() + f.get_height())
            tempRect = pygame.Rect( (0, 0), size )
            self.textRects.append(textrect.render_textrect(
                i[0], f, tempRect, i[2], i[3], i[4], i[5]))

    def escape(self):
        self.advanceNow = True

    def update(self):
        if self.stage == 0:
            color = []
            for i in range(3):
                self.fadeSurfaceColor[i].add(INTRO_SPEEDS[0])
                color.append(self.fadeSurfaceColor[i].value)
            self.fadeSurface.fill(color)
            
            if self.fadeSurfaceColor[0].value == INTRO_MAX_FADE:
                self.stage = 1

        elif self.stage == 1:
            self.ticker += 1
            if self.ticker >= INTRO_SPEEDS[1]:
                self.stage = 2
                self.ticker = 0

        elif self.stage == 2:
            self.transAlpha.add(-INTRO_SPEEDS[2])
            self.transSurface.set_alpha(self.transAlpha.value)
            if self.transAlpha.value == 0:
                self.stage = 3

        elif self.stage == 3:
            self.ticker += 1
            if self.ticker >= INTRO_SPEEDS[3]:
                self.stage = 4
                self.ticker = 0

        elif self.stage == 4:
            self.transAlpha.add(INTRO_SPEEDS[4])
            self.transSurface.set_alpha(self.transAlpha.value)
            if self.transAlpha.value == 255:
                self.stage = 5

        elif self.stage == 5:
            self.ticker += 1
            if self.ticker >= INTRO_SPEEDS[5]:
                self.stage = 6
                self.ticker = 0

        elif self.stage == 6:
            self.advanceNow = True
