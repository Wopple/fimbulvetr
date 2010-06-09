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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.leftClick()
                elif event.button == 3:
                    self.model.rightClick()
                elif event.button == 4:
                    self.model.scrollIn()
                elif event.button == 5:
                    self.model.scrollOut()
            elif event.type == pygame.QUIT:
                sys.exit(0)
