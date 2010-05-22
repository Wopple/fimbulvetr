import os
import sys
import pygame

import mvc

from constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.screen.blit(self.model.mapImage, self.model.mapRect.topleft)

        for c in self.model.characters:
            c.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        if tickClock:
            pygame.display.flip()
