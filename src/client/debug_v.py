import os
import sys
import pygame

import mvc

from common.constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.model.debugMenu.draw(self.screen)

        if tickClock:
            pygame.display.flip()

