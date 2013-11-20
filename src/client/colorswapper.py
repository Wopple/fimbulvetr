import os
import sys
import pygame
import copy

from constants import *



def swapCharacter(inChar, isFirst, colorChoices, screen=None):
    if len(colorChoices) != len(inChar.colors):
        raise
    
    colorDataMasterList = []
    
    for i, choice in enumerate(colorChoices):
        colorSlot = inChar.colors[i]
        colorDataSet = colorSlot.colorDataSetList[choice]
        
        for data in colorDataSet.colorDataList:
            colorDataMasterList.append(data)
            
            
    imageMasterList = []
    for im in inChar.spriteSet:
        imageMasterList.append(im[0])
    
    imageAlteredList = []
    for im in imageMasterList:
        newIm = ColorSwapImage(im, colorDataMasterList, isFirst)
        imageAlteredList.append(newIm)
        
        
        
    newSpriteSet = []
    for i in range(len(inChar.spriteSet)):
        newSpriteSet.append([imageAlteredList[i], inChar.spriteSet[i][1]])
    
    inChar.setSpriteSet(newSpriteSet)
    


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
    
    def __init__(self, baseColor, baseVariance, replacementColor1, replacementColor2):
        self.baseColor = baseColor
        self.baseVariance = baseVariance
        self.replacementColor1 = replacementColor1
        self.replacementColor2 = replacementColor2
        
    def getColor(self, isFirst):
        if isFirst:
            return self.replacementColor1
        else:
            return self.replacementColor2
        
class ColorDataSet(object):
    
    def __init__(self, setName, colorDataList):
        self.setName = setName
        self.colorDataList = colorDataList
        
        
class ColorSlot(object):
    
    def __init__(self, slotName, colorDataSetList):
        self.slotName = slotName
        self.colorDataSetList = colorDataSetList
        
        