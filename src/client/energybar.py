import sys
import pygame
from pygame.locals import *
from math import sqrt
import textrect

from common.constants import *
from client.constants import *

from common import boundint
from common.util.rect import Rect

class EnergyBar(object):
    def __init__(self, inVal, inRect, inBorders, inColors, pulse,
                 text=None, threshold=None, textJust=0, barJust=True):
        if not isinstance(inVal, boundint.BoundInt):
            raise RuntimeError, "EnergyBar must be given BoundInt"

        if (  ((inBorders[0] * 2) >= inRect.width) or
              ((inBorders[1] * 2) >= inRect.height)   ):
            raise RuntimeError, "Borders too large / Area too small for EnergyBar"

        if threshold is None:
            threshold = inVal.maximum

        if textJust > 2:
            textJust -= 3
            self.textOnBottom = False
        else:
            self.textOnBottom = True

        self.barJust = barJust
        self.value = inVal
        self.rect = inRect
        self.horizBorderSize = inBorders[0]
        self.vertBorderSize = inBorders[1]
        self.fillColor = inColors[0]
        self.fullLowColor = inColors[1]
        self.fullHighColor = inColors[2]
        self.emptyColor = inColors[3]
        self.borderColor = inColors[4]
        self.fontColor = inColors[5]
        self.prevVal = -1
        self.pulse = pulse
        self.currPulse = 0
        self.pulseUp = True
        self.colorChanged = False
        self.threshold = threshold

        self.createPulse()
        self.createBackground()
        self.createForeground()
        self.createText(text, textJust)
        self.createFinish()

    def update(self):
        if self.pulseUp:
            i = 1
        else:
            i = -1
        self.currPulse += i
        if self.currPulse == 0 or self.currPulse == self.pulse-1:
            self.pulseUp = not(self.pulseUp)
        
        if  ((self.prevVal != self.value.value)
             or (self.value.value >= self.threshold)
             or (self.colorChanged)):
            self.colorChanged = False
            if (self.value.value >= self.threshold) and (self.prevVal < self.threshold):
                self.currPulse = 0
                self.pulseUp = True
            self.createForeground()
            self.createFinish()
        
        self.prevVal = self.value.value

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        if not self.text is None:
            x = self.rect.left
            if self.textOnBottom:
                y = self.rect.bottom
            else:
                y = self.rect.top - (ENERGY_BAR_FONT.get_height() + 2)
            screen.blit(self.text, (x, y))

    def createBackground(self):
        self.backImage = pygame.Surface((self.rect.width, self.rect.height))
        self.backImage.fill(self.borderColor)

    def createForeground(self):
        width = self.rect.width - (self.horizBorderSize * 2)
        height = self.rect.height - (self.vertBorderSize * 2)
        fillNum = (float(self.value.value) / float(self.value.maximum)) * width
        self.foreImage = pygame.Surface((width, height))

        if self.value.value >= self.threshold:
            fillColor = self.pulseColors[self.currPulse]
        else:
            fillColor = self.fillColor

        self.foreImage.fill(self.emptyColor)
        self.foreImage.fill(fillColor, (0, 0, fillNum, height))

    def createFinish(self):
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.blit(self.backImage, (0, 0))
        self.image.blit(self.foreImage, (self.horizBorderSize, self.vertBorderSize))
        if not self.barJust:
            self.image = pygame.transform.flip(self.image, True, False)

    def createPulse(self):
        self.pulseColors = []

        self.pulseColors.append(self.fullLowColor)

        inc = []
        for c in range(3):
            inc.append( float(self.fullLowColor[c] - self.fullHighColor[c])
                        / float(self.pulse) )
            
        for i in range(self.pulse - 2):
            j = i+1
            newColor = []
            for c in range(3):
                newSub = float(self.fullLowColor[c]) - float(float(inc[c]) * float(j))
                newColor.append(int(newSub))

            self.pulseColors.append((newColor[0], newColor[1], newColor[2]))

        self.pulseColors.append(self.fullHighColor)

    def createText(self, t, just):
        if t is None:
            self.text = None
        else:
            w = self.rect.width
            h = ENERGY_BAR_FONT.get_height() + 2
            self.text = textrect.render_textrect(t, ENERGY_BAR_FONT,
                                                 Rect((0, 0), (w, h)),
                                                 self.fontColor,
                                                 (0, 0, 0), just, True)

    def changeColor(self, c):
        self.colorChanged = True
        self.fillColor = c
        
    def changeFullColors(self, c1, c2):
        self.fullLowColor = c1
        self.fullHighColor = c2
        self.createPulse()
