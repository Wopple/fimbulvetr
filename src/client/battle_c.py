import sys
import pygame
from pygame.locals import *

from common import mvc

from common.constants import *
from client.constants import *

class Controller(mvc.Controller):
    def __init__(self, inputQueue=None, screen=None):
        super(Controller, self).__init__()
        self.inputQueue = inputQueue
        self.player = 0

    def update(self):
        for event in pygame.event.get():
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                k = None

                if event.key == K_UP:
                    k = UP
                elif event.key == K_DOWN:
                    k = DOWN
                elif event.key == K_LEFT:
                    k = LEFT
                elif event.key == K_RIGHT:
                    k = RIGHT
                elif event.key == PY_ATTACK_A:
                    k = ATT_A
                elif event.key == PY_ATTACK_B:
                    k = ATT_B
                elif event.key == PY_JUMP:
                    k = JUMP
                elif event.key == PY_BLOCK:
                    k = BLOCK
                elif event.key == PY_SUPER:
                    k = SUPER
                elif event.key == K_ESCAPE:
                    self.inputQueue.put(None)
                    sys.exit(0)

                if k is not None:
                    isDown = event.type == pygame.KEYDOWN
                    self.inputQueue.put(Key(k, isDown))
            elif event.type == pygame.QUIT:
                self.inputQueue.put(None)
                sys.exit(0)

class Key(object):
    def __init__(self, key, isDown):
        self.key = key
        self.isDown = isDown
