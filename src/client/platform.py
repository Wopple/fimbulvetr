import os
import sys
import pygame
import copy

from common.constants import *
from client.constants import *

from common.util.rect import Rect

class Platform(object):
    def __init__(self, inPos, inLength, inTerrain):
        self.rect = Rect( inPos, (inLength, PLATFORM_HEIGHT) )

        self.image = pygame.Surface( (self.rect.width, self.rect.height) )
        
        self.image.fill(BLACK)
        
        innerImage = pygame.Surface( (self.rect.width, self.rect.height - (PLATFORM_BORDER_SIZE * 2)) )
        innerImage.fill(PLATFORM_COLORS[inTerrain])
        
        self.image.blit(innerImage, (0, PLATFORM_BORDER_SIZE))

    def draw(self, screen, inOffset):
        screen.blit(self.image, add_points(self.rect.topleft, inOffset))
