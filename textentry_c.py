import os
import sys
import pygame
from pygame.locals import *

import mvc

from constants import *

class Controller(mvc.Controller):
    def __init__(self, model=None, screen=None):
        super(Controller, self).__init__()
        self.holdCtrl = [False, False]

    def getCtrl(self):
        return (self.holdCtrl[0] or self.holdCtrl[1])

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    self.model.escape()
                elif event.key == K_RETURN:
                    self.model.enter()
                elif event.key == K_BACKSPACE:
                    self.model.backspace()
                elif event.key == K_LCTRL:
                    self.holdCtrl[0] = True
                elif event.key == K_RCTRL:
                    self.holdCtrl[1] = True
                elif self.model.validEntry(event.unicode):
                    self.model.key(event.unicode)
                elif (event.key == K_v) and (self.getCtrl()):
                    self.model.pasteFromClipboard()
            elif event.type == pygame.KEYUP:
                if event.key == K_LCTRL:
                    self.holdCtrl[0] = False
                elif event.key == K_RCTRL:
                    self.holdCtrl[1] = False
            elif event.type == pygame.QUIT:
                sys.exit(0)
