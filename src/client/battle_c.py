import sys
import pygame
from pygame.locals import *

from common import mvc

from client.constants import *

class Controller(mvc.Controller):
    def __init__(self, inputQueue=None, screen=None):
        super(Controller, self).__init__()
        self.inputQueue = inputQueue
        self.player = 0

    def setPlayer(self, p):
        self.player = p

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.inputQueue.put(Key(0, True, self.player))
                elif event.key == K_DOWN:
                    self.inputQueue.put(Key(1, True, self.player))
                elif event.key == K_LEFT:
                    self.inputQueue.put(Key(2, True, self.player))
                elif event.key == K_RIGHT:
                    self.inputQueue.put(Key(3, True, self.player))
                elif event.key == KEY_ATTACK_A:
                    self.inputQueue.put(Key(4, True, self.player))
                elif event.key == KEY_ATTACK_B:
                    self.inputQueue.put(Key(5, True, self.player))
                elif event.key == KEY_JUMP:
                    self.inputQueue.put(Key(6, True, self.player))
                elif event.key == KEY_BLOCK:
                    self.inputQueue.put(Key(7, True, self.player))
                elif event.key == KEY_SUPER:
                    self.inputQueue.put(Key(8, True, self.player))
#                elif event.key == K_F1:
#                    self.model.testKey(1)
#                elif event.key == K_F2:
#                    self.model.testKey(2)
#                elif event.key == K_F3:
#                    self.model.testKey(3)
#                elif event.key == K_F4:
#                    self.model.testKey(4)
#                elif event.key == K_F5:
#                    self.model.testKey(5)
#                elif event.key == K_F6:
#                    self.model.testKey(6)
                elif event.key == K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    self.inputQueue.put(Key(0, False, self.player))
                elif event.key == K_DOWN:
                    self.inputQueue.put(Key(1, False, self.player))
                elif event.key == K_LEFT:
                    self.inputQueue.put(Key(2, False, self.player))
                elif event.key == K_RIGHT:
                    self.inputQueue.put(Key(3, False, self.player))
                elif event.key == KEY_ATTACK_A:
                    self.inputQueue.put(Key(4, False, self.player))
                elif event.key == KEY_ATTACK_B:
                    self.inputQueue.put(Key(5, False, self.player))
                elif event.key == KEY_JUMP:
                    self.inputQueue.put(Key(6, False, self.player))
                elif event.key == KEY_BLOCK:
                    self.inputQueue.put(Key(7, False, self.player))
                elif event.key == KEY_SUPER:
                    self.inputQueue.put(Key(8, False, self.player))
            elif event.type == pygame.QUIT:
                sys.exit(0)

class Key(object):
    def __init__(self, index, isDown, player):
        self.index = index
        self.isDown = isDown
        self.player = player
