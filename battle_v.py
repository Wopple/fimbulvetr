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

        for i, p in enumerate(self.model.players):
            if self.model.returnCode[i] != 1:
                p.draw(self.screen, self.model.rect.topleft)

        for p in self.model.projectiles:
            p.draw(self.screen, self.model.rect.topleft)

        for f in self.model.fx:
            f.draw(self.screen, self.model.rect.topleft)

        for b in self.model.bars:
            b.draw(self.screen)

        self.model.countdown.draw(self.screen)
        self.drawEndingText()

        if tickClock:
            pygame.display.flip()

    def drawEndingText(self):
        if self.model.endingVal == 0:
            self.screen.blit(self.model.endingText[2][0],
                             self.model.countdown.rect.topleft)
        elif self.model.endingVal == 3:
            self.screen.blit(self.model.endingText[0][self.model.returnCode[0]+1],
                             self.model.countdown.rect.topleft)
            self.screen.blit(self.model.endingText[0][self.model.returnCode[1]+1],
                             self.model.countdown.rect.bottomleft)
