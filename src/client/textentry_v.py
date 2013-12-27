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
        self.screen.blit(self.model.image, self.model.rect.topleft)
        self.screen.blit(self.model.titlePanel, self.model.titleRect.topleft)

        if tickClock:
            pygame.display.flip()
