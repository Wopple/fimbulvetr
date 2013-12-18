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
        if not self.model.menu is None:
            self.model.menu.draw(self.screen)

        if not self.model.text is None:
            self.screen.blit(self.model.text, self.model.textLoc)

        if self.model.phase == 3 or self.model.phase == 4:
            self.screen.blit(self.model.workingIconImage, self.model.textLoc)

        if tickClock:
            pygame.display.flip()
