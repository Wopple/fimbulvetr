import sys
import pygame

from common import mvc

from client.constants import *

class Controller(mvc.Controller):
    def __init__(self, model=None, screen=None):
        super(Controller, self).__init__()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == PY_X) or (event.key == PY_RETURN):
                    self.model.confirm()
                elif (event.key == PY_Z) or (event.key == PY_ESCAPE):
                    self.model.cancel()
                elif event.key == PY_UP:
                    self.model.decMenu()
                elif event.key == PY_DOWN:
                    self.model.incMenu()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.model.confirm()

            elif event.type == pygame.MOUSEMOTION:
                self.model.mouseMoved(pygame.mouse.get_pos())

            elif event.type == pygame.QUIT:
                sys.exit(0)
