import sys
import pygame

from common import mvc

from common.constants import *
from client.constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.screen.blit(self.model.m.mapImage, self.model.m.mapRect.topleft)

        for s in self.model.m.structures:
            s.draw(self.screen, self.model.m.zoomVal, self.model.m.mapRect.topleft)

        for c in self.model.m.characters:
            c.draw(self.screen, self.model.m.zoomVal, self.model.m.mapRect.topleft)


        if tickClock:
            pygame.display.flip()
