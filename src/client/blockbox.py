import os
import sys
import pygame
import copy

from constants import *

class Blockbox(object):
    def __init__(self, inRect):
        self.rect = inRect

        self.image = pygame.Surface(self.rect.size)
        self.image.fill(BLOCKBOX_COLOR)
        self.image.set_alpha(BLOCKBOX_ALPHA)
