import os
import sys
import pygame

import mvc

import minimenu

from constants import *

class Model(mvc.Model):
    def __init__(self):
        super(Model, self).__init__()
        tempRect = pygame.Rect( (50, 50), (200, 0) )
        menuOptions = ["Combat Debug", "Map Debug", "Network Debug - Server",
                       "Network Debug - Client", "Play Game Normally", "Exit"]
        self.debugMenu = minimenu.MiniMenu(tempRect, menuOptions,
                                           12, (250, 250, 250),
                                           (125, 125, 125), (15, 15, 15))
        self.debugMenu.center(ENTIRE_SCREEN, True, True)

    def incMenu(self):
        self.debugMenu.inc()

    def decMenu(self):
        self.debugMenu.dec()

    def confirm(self):
        self.advanceNow = True

    def update(self):
        pass

    def cancel(self):
        pass

    def mouseMoved(self, pos):
        val = self.debugMenu.isAreaRect(pos)
        if val > 0:
            self.debugMenu.setVal(val)
