import os
import sys
import pygame
import copy

from constants import *



def ColorSwapImage(inImage, colorData, isFirst):
    
    canvasImage = copy.copy(inImage)
        
    for data in colorData:
        baseColor = data.baseColor
        baseVariance = data.baseVariance
        newColor = data.getColor(isFirst)
        if newColor is None:
            continue
        newImage = copy.copy(inImage)
            
        colorSwap(newImage, baseColor,
                  newColor, baseVariance)
        
        for x in range(inImage.get_size()[0]):
            for y in range(inImage.get_size()[1]):
                pixelOrig = inImage.get_at((x, y))
                pixelNew = newImage.get_at((x, y))
                
                if pixelOrig != pixelNew:
                    canvasImage.set_at((x, y), pixelNew)
                
        
    return canvasImage
    
    

class ColorData(object):
    
    def __init__(self, baseColor, baseVariance, replacementColor1, replacementColor2, colorName):
        self.baseColor = baseColor
        self.baseVariance = baseVariance
        self.replacementColor1 = replacementColor1
        self.replacementColor2 = replacementColor2
        self.colorName = colorName
        
    def getColor(self, isFirst):
        if isFirst:
            return self.replacementColor1
        else:
            return self.replacementColor2