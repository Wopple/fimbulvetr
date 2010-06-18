import os
import sys
import pygame

import mvc

from constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(self.model.baseSurface, self.model.baseSurfaceRect)
        for i in self.model.blackPanelPos:
            self.screen.blit(self.model.blackPanel, i)
        self.model.menu.draw(self.screen)
        self.model.charMenu.draw(self.screen)


        if tickClock:
            pygame.display.flip()
