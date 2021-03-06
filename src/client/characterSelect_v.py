import os
import sys
import pygame

from common import mvc

from common.constants import *
from client.constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(self.model.bg, (0, 0))

        border, pos = self.model.getSelectionBorder()
        if not pos is None:
            self.screen.blit(border, pos)

        self.model.group.draw(self.screen)

        self.model.hostPanel.draw(self.screen)
        self.model.clientPanel.draw(self.screen)

        self.model.readyButton.draw(self.screen)
        if not self.model.startButton is None:
            self.model.startButton.draw(self.screen)

        if self.model.starting:
            print "YO!"
            self.screen.blit(self.model.loadingImage,
                             self.model.loadingRect.topleft)

        if tickClock:
            pygame.display.flip()

