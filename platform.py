import os
import sys
import pygame
import copy

from constants import *

class Platform(object):
    def __init__(self, inPos, inLength, inTerrain):
        self.rect = pygame.Rect( inPos, (inLength, PLATFORM_HEIGHT) )

        self.image = pygame.Surface( (self.rect.width, self.rect.height) )
        self.image.fill(PLATFORM_COLORS[inTerrain])

    def draw(self, screen, inOffset):
        screen.blit(self.image, add_points(self.rect.topleft, inOffset))
