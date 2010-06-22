import os
import sys
import pygame
from pygame.locals import *

import mvc

from constants import *

class Controller(mvc.Controller):
    def __init__(self, model=None, screen=None):
        super(Controller, self).__init__()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.model.escape()
                elif event.key == K_RETURN:
                    self.model.enter()
                elif event.key == K_BACKSPACE:
                    self.model.backspace()
                elif self.model.validEntry(event.unicode):
                    self.model.key(event.unicode)
            elif event.type == pygame.QUIT:
                sys.exit(0)
