import os
import sys
import pygame
from pygame.locals import *

import mvc

from common.constants import *
from client.constants import *

class Controller(mvc.Controller):
    def __init__(self, model=None, screen=None):
        super(Controller, self).__init__()

    def update(self):
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.click()
                elif event.button == 3:
                    self.model.click2()

            elif event.type == pygame.MOUSEMOTION:
                self.model.mouseMoved(pygame.mouse.get_pos())
                
            elif event.type == pygame.QUIT:
                sys.exit(0)
