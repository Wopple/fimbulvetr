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
                    self.model.click()

            elif event.type == pygame.MOUSEMOTION:
                self.model.mouseMoved(pygame.mouse.get_pos())
                
            elif event.type == pygame.QUIT:
                sys.exit(0)
