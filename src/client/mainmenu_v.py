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
        self.model.bg.draw(self.screen)
        self.model.menu.draw(self.screen)

        for i in range(2):
            self.screen.blit(self.model.textRects[i], MAIN_MENU_TITLE_POS[i])

        if self.model.transAlpha.value > 0:
            self.screen.blit(self.model.transSurface, (0, 0))

        if tickClock:
            pygame.display.flip()
