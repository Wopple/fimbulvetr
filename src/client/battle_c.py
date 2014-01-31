import sys
import pygame

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

                if event.key == PY_UP:
                    k = K_UP
                elif event.key == PY_DOWN:
                    k = K_DOWN
                elif event.key == PY_LEFT:
                    k = K_LEFT
                elif event.key == PY_RIGHT:
                    k = K_RIGHT
                elif event.key == PY_ATTACK_A:
                    k = K_ATT_A
                elif event.key == PY_ATTACK_B:
                    k = K_ATT_B
                elif event.key == PY_JUMP:
                    k = K_JUMP
                elif event.key == PY_BLOCK:
                    k = K_BLOCK
                elif event.key == PY_SUPER:
                    k = K_SUPER
                elif event.key == PY_ESCAPE:
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
