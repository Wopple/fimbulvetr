import os
import sys
import pygame

import mvc

import mapchar

from constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.screen.blit(self.model.mapImage, self.model.mapRect.topleft)

        for c in self.model.characters:
            if ((not c is self.model.currHighlighted) and
                (not c is self.model.currSelected)):
                c.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        if ( (isinstance(self.model.currHighlighted, mapchar.MapChar)) and
             (not self.model.currHighlighted is self.model.currSelected) ):
            self.model.currHighlighted.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        if isinstance(self.model.currSelected, mapchar.MapChar):
            self.model.currSelected.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)


        if tickClock:
            pygame.display.flip()
