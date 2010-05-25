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
                if (event.key == K_x) or (event.key == K_RETURN):
                    self.model.confirm()
                elif (event.key == K_z) or (event.key == K_ESCAPE):
                    self.model.cancel()
                elif event.key == K_UP:
                    self.model.decMenu()
                elif event.key == K_DOWN:
                    self.model.incMenu()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.confirm()

            elif event.type == pygame.MOUSEMOTION:
                self.model.mouseMoved(pygame.mouse.get_pos())
                    
            elif event.type == pygame.QUIT:
                sys.exit(0)
