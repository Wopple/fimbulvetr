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
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_UP:
                    self.model.key(0, True)
                elif event.key == K_DOWN:
                    self.model.key(1, True)
                elif event.key == K_LEFT:
                    self.model.key(2, True)
                elif event.key == K_RIGHT:
                    self.model.key(3, True)
                elif event.key == K_LEFTBRACKET:
                    self.model.changeHighlight(False)
                elif event.key == K_RIGHTBRACKET:
                    self.model.changeHighlight(True)
                elif event.key == K_RETURN:
                    self.model.toggleSelected()
                elif event.key == K_BACKSLASH:
                    self.model.removeAll()
                elif event.key == K_BACKSPACE:
                    self.model.deleteHighlighted()
                elif event.key == K_EQUALS:
                    self.model.changeMagnitude(True)
                elif event.key == K_MINUS:
                    self.model.changeMagnitude(False)
                elif event.key == K_SPACE:
                    self.model.printListToOutput()
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    self.model.key(0, False)
                elif event.key == K_DOWN:
                    self.model.key(1, False)
                elif event.key == K_LEFT:
                    self.model.key(2, False)
                elif event.key == K_RIGHT:
                    self.model.key(3, False)
            elif event.type == pygame.QUIT:
                sys.exit(0)
