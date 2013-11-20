import os
import sys
import pygame

import incint
import textrect

from constants import *

class Countdown(object):
    def __init__(self, time):
        self.time = time
        self.tick = incint.IncInt(0, 0, FRAME_RATE)

        size = (SCREEN_SIZE[0], COUNTDOWN_FONT.get_linesize() + 4)
        pos = (0, (SCREEN_SIZE[1] / 2) - (size[1] / 2) - 15)
        self.rect = pygame.Rect(pos, size)
        self.startFlag = False

        self.updateImage()

    def setTime(self, time):
        self.time = time
        self.updateImage()

    def update(self):
        if self.isValid():
            self.tick.inc()

            if self.tick.isMin():
                self.time -= 1
                self.updateImage()
                    

    def updateImage(self):
        if self.time == 0:
            msg = "GO!"
            self.startFlag = True
        else:
            msg = str(self.time)
        
        self.image = textrect.render_textrect(msg, COUNTDOWN_FONT, self.rect,
                                              COUNTDOWN_COLOR, ALMOST_BLACK, 1, True)

    def draw(self, screen):
        if self.isValid():
            screen.blit(self.image, self.rect.topleft)

    def isValid(self):
        return (self.time >= 0)

    def isGoing(self):
        return (self.time > 0)

    def checkStartFlag(self):
        if self.startFlag:
            self.startFlag = False
            return True
        else:
            return False
