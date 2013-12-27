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
        self.player = 0

    def setPlayer(self, p):
        self.player = p

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.model.key(0, True, self.player)
                elif event.key == K_DOWN:
                    self.model.key(1, True, self.player)
                elif event.key == K_LEFT:
                    self.model.key(2, True, self.player)
                elif event.key == K_RIGHT:
                    self.model.key(3, True, self.player)
                elif event.key == KEY_ATTACK_A:
                    self.model.key(4, True, self.player)
                elif event.key == KEY_ATTACK_B:
                    self.model.key(5, True, self.player)
                elif event.key == KEY_JUMP:
                    self.model.key(6, True, self.player)
                elif event.key == KEY_BLOCK:
                    self.model.key(7, True, self.player)
                elif event.key == KEY_SUPER:
                    self.model.key(8, True, self.player)
                elif event.key == K_F1:
                    self.model.testKey(1)
                elif event.key == K_F2:
                    self.model.testKey(2)
                elif event.key == K_F3:
                    self.model.testKey(3)
                elif event.key == K_F4:
                    self.model.testKey(4)
                elif event.key == K_F5:
                    self.model.testKey(5)
                elif event.key == K_F6:
                    self.model.testKey(6)
                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    self.model.key(0, False, self.player)
                elif event.key == K_DOWN:
                    self.model.key(1, False, self.player)
                elif event.key == K_LEFT:
                    self.model.key(2, False, self.player)
                elif event.key == K_RIGHT:
                    self.model.key(3, False, self.player)
                elif event.key == KEY_ATTACK_A:
                    self.model.key(4, False, self.player)
                elif event.key == KEY_ATTACK_B:
                    self.model.key(5, False, self.player)
                elif event.key == KEY_JUMP:
                    self.model.key(6, False, self.player)
                elif event.key == KEY_BLOCK:
                    self.model.key(7, False, self.player)
                elif event.key == KEY_SUPER:
                    self.model.key(8, False, self.player)
            elif event.type == pygame.QUIT:
                sys.exit(0)
