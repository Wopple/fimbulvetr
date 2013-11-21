
import os
import sys
import pygame
import math

from common.constants import *

class Background(object):
    def __init__(self, inRect, inImage):

        self.mainRect = inRect
        self.mainPane = pygame.Surface((self.mainRect.width, self.mainRect.height))
        pattern = inImage
        
        imageSize = inImage.get_size()

        tempFloat = float(float(inRect.width) / float(imageSize[0]))
        repeatX = int(math.ceil(tempFloat))
        tempFloat = float(float(inRect.height) / float(imageSize[1]))
        repeatY = int(math.ceil(tempFloat))

        sizeX = repeatX * imageSize[0]
        sizeY = repeatY * imageSize[0]
        self.subRect = pygame.Rect( (0, 0), (sizeX, sizeY) )
        self.subPane = pygame.Surface((self.subRect.width, self.subRect.height))

        for x in range (repeatX):
            for y in range (repeatY):
                self.subPane.blit(pattern, ( (x*imageSize[0]), (y*imageSize[1]) ) )


        self.mainPane.blit(self.subPane, self.subRect.topleft)

    def draw(self, screen):
        screen.blit(self.mainPane, self.mainRect.topleft)

    def update(self):
        pass
