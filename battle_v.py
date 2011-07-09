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

        for p in self.model.platforms:
            p.draw(self.screen, self.model.rect.topleft)

        for p in self.model.players:
            p.draw(self.screen, self.model.rect.topleft)

        for p in self.model.projectiles:
            p.draw(self.screen, self.model.rect.topleft)

        for f in self.model.fx:
            f.draw(self.screen, self.model.rect.topleft)

        for b in self.model.bars:
            b.draw(self.screen)

        self.model.countdown.draw(self.screen)

        if tickClock:
            pygame.display.flip()
