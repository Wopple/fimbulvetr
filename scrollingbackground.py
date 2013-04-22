
import os
import sys
import pygame

from constants import *

class ScrollingBackground():
    def __init__ (self, inRect, inImage, inSpeed):
        
        self.rect = inRect
        self.pattern = inImage
        self.vel = inSpeed
        
        mainSizes = [self.rect.width, self.rect.height]
        imageSizes = [inImage.get_size()[0], inImage.get_size()[1]]
        subSizes = [self.rect.width, self.rect.height]
        for i in range(2):
            subSizes[i] += imageSizes[i] + (imageSizes[i] - (mainSizes[i] % imageSizes[i]))
            
        self.subSurface = pygame.Surface(subSizes, pygame.SRCALPHA, 32)
        self.subSurface.convert_alpha()
        for x in range(0, subSizes[0], imageSizes[0]):
            for y in range(0, subSizes[1], imageSizes[1]):
                self.subSurface.blit(inImage, (x, y))
                
        self.precisePos = [0.0, 0.0]
        
    def update(self):
        
        for i in range(2):
            self.precisePos[i] += self.vel[i]
            
            while (self.precisePos[i] > 0):
                self.precisePos[i] -= self.pattern.get_size()[i]
            while (self.precisePos[i] + self.subSurface.get_size()[i] < self.rect.size[i]):
                self.precisePos[i] += self.pattern.get_size()[i]
                
    def draw(self, screen):
        mainSurface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA, 32)
        mainSurface.convert_alpha()
        
        mainSurface.blit(self.subSurface, (int(self.precisePos[0]), int(self.precisePos[1])))
        screen.blit(mainSurface, self.rect.topleft)