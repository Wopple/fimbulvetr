import os
import sys
import pygame

import mvc

from common.constants import *
from client.constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.screen.blit(self.model.fadeSurface, (0, 0))

        if (self.model.stage >= 2) and (self.model.stage <= 4):
            self.screen.blit(self.model.textRects[0], self.model.centerTextPos)
            self.screen.blit(self.model.transSurface, (0, 0))


        if tickClock:
            pygame.display.flip()
