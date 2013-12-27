import os
import sys
import pygame
from pygame.locals import *

from common import mvc

from common.constants import *
from client.constants import *

class Controller(mvc.Controller):
    def __init__(self, model=None, screen=None):
        super(Controller, self).__init__()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.model.escape()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.escape()
            elif event.type == pygame.QUIT:
                sys.exit(0)
