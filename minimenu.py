# Copyright 2009 Christopher Czyzewski
# This file is part of Project Mage.
#
#    Project Mage is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Project Mage is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Project Mage.  If not, see <http://www.gnu.org/licenses/>.

import sys
import pygame
from pygame.locals import *
from math import sqrt
import textrect
import incint

class MiniMenu(object):
    def __init__(self, inRect, options, inFont, colorOn, colorOff, colorBG):

        self.rectSingle = inRect
        self.options = options
        if len(options) > 0:
            self.selection = incint.IncInt(1, 1, len(options))
        else:
            self.selection = None
        self.font = inFont
        
        lineSize = self.font.get_height() + self.font.get_linesize()
        if self.rectSingle.height < lineSize:
            self.rectSingle.height = lineSize

        h = self.rectSingle.height * len(self.options)
        if h <= 0:
            h = 1
        self.rect = pygame.Rect( self.rectSingle.topleft, (self.rectSingle.width, h) )

        self.colorOn = colorOn
        self.colorOff = colorOff
        self.colorBG = colorBG

        self.noSelection = False

        
        self.slate = pygame.Surface( (self.rect.width, self.rect.height) )
        self.slate.fill(colorBG)

        self.update()

    def inc(self):
        if not self.selection is None:
            self.selection.increment()
            self.update()

    def dec(self):
        if not self.selection is None:
            self.selection.decrement()
            self.update()

    def setVal(self, val):
        if not self.selection is None:
            if val >= self.selection.minimum and val <= self.selection.maximum:
                self.selection.value = val
                self.noSelection = False

            if val == -1:
                self.noSelection = True

            self.update()

    def setToMax(self):
        if not self.selection is None:
            self.setVal(self.selection.maximum)

    def reset(self):
        if not self.selection is None:
            self.selection.value = 1

    def update(self):
        self.mainFrame = pygame.Surface( (self.rect.width, self.rect.height) )
        self.areaRects = []

        if not self.selection is None:
            offset = 0
            for x in range(len(self.options)):
                textRect = pygame.Rect( (0, offset), (self.rectSingle.width, self.rectSingle.height) )
                self.areaRects.append(textRect)
                if (self.selection.value == (x + 1)) and (not self.noSelection):
                    currColor = self.colorOn
                else:
                    currColor = self.colorOff
                textSurface = textrect.render_textrect(self.options[x], self.font, textRect, currColor, self.colorBG, 1)
                self.mainFrame.blit(textSurface, (0, offset))
                offset += textRect.height
            
    def draw(self, screen):
        screen.blit(self.mainFrame, self.rect.topleft)

    def value(self):
        if not self.selection is None:
            return self.selection.value
        else:
            return None

    def text(self):
        return self.options[self.selection.value - 1]

    def center(self, baseRect, doHoriz, doVert):
        if doHoriz:
            self.rect.left = (baseRect.width / 2) - (self.rect.width / 2)
        if doVert:
            self.rect.top = (baseRect.height / 2) - (self.rect.height / 2)

    def isAreaRect(self, pos):
        currPos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        for r in range(len(self.areaRects)):
            if self.areaRects[r].collidepoint(currPos):
                return r+1
        return 0

    def isMax(self):
        return self.selection.isMax()

    def isMin(self):
        return self.selection.isMin()
