import os
import sys
import pygame

import mvc

from constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(self.model.bg, (0, 0))

        pos = self.model.getSelectionBorderPos()
        if not pos is None:
            self.screen.blit(self.model.selectionBorder, pos)

        self.model.group.draw(self.screen)

        if tickClock:
            pygame.display.flip()

