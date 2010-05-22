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
        self.screen.blit(self.model.background, self.model.rect)

        self.model.player.draw(self.screen, self.model.rect.topleft)

        for p in self.model.projectiles:
            p.draw(self.screen, self.model.rect.topleft)

        if tickClock:
            pygame.display.flip()
