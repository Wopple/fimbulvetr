import os
import sys
import pygame
import copy

from common.constants import *
from client.constants import *

class Hurtbox(object):
    def __init__(self, inRect):
        self.rect = inRect
        self.immunity = dict([(x, False) for x in ATTACK_PROPERTIES])

        self.image = pygame.Surface(self.rect.size)
        self.image.fill(HURTBOX_COLOR)
        self.image.set_alpha(HURTBOX_ALPHA)
