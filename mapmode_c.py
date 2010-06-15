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
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit(0)
                elif event.key == K_SPACE:
                    self.model.pausePressed()
                elif event.key == K_1:
                    self.model.numberKey(1)
                elif event.key == K_2:
                    self.model.numberKey(2)
                elif event.key == K_3:
                    self.model.numberKey(3)
                elif event.key == K_4:
                    self.model.numberKey(4)
                elif event.key == K_5:
                    self.model.numberKey(5)
                elif event.key == K_6:
                    self.model.numberKey(6)
                elif event.key == K_7:
                    self.model.numberKey(7)
                elif event.key == K_8:
                    self.model.numberKey(8)
                elif event.key == K_9:
                    self.model.numberKey(9)
                elif event.key == K_UP:
                    self.model.key(0, True)
                elif event.key == K_DOWN:
                    self.model.key(1, True)
                elif event.key == K_LEFT:
                    self.model.key(2, True)
                elif event.key == K_RIGHT:
                    self.model.key(3, True)
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
