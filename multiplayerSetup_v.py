import os
import sys
import pygame

import mvc

from constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.model.menu.draw(self.screen)

        if not self.model.text is None:
            self.screen.blit(self.model.text, self.model.textLoc)

        if tickClock:
            pygame.display.flip()
