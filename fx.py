import os
import sys
import pygame

import incint
import boundint

from constants import *

class FX(object):
    def __init__(self, inPos, inFacing, inType):
        self.preciseLoc = inPos
        self.facingRight = inFacing

        self.frames = []
        self.setType(inType)

        self.frameNum = 0
        self.subframeNum = 0
        self.removeFlag = False

        self.setImage()
        

    def update(self):
        self.subframeNum += 1
        if self.subframeNum >= self.frames[self.frameNum].length:
            self.subframeNum = 0
            self.frameNum += 1
            if self.frameNum == len(self.frames):
                self.removeFlag = True
            else:
                self.setImage()
        
        self.rect.topleft = self.getRectPos()

    def draw(self, screen, inOffset):
        screen.blit(self.image, add_points(self.rect.topleft, inOffset))

    def setImage(self):
        f = self.frames[self.frameNum]
        inImage = f.image
        o = f.offset
        
        size = inImage.get_size()
        
        if self.facingRight:
            offset = o
            self.image = inImage
        else:
            offset = (-o[0] + size[0], o[1])
            self.image = pygame.transform.flip(inImage, True, False)
        
        self.offset = offset
        self.rect = pygame.Rect(self.getRectPos(), size)

    def getRectPos(self):
        return ( int(self.preciseLoc[0]) - self.offset[0],
                 int(self.preciseLoc[1]) - self.offset[1] )

    def setType(self, t):
        if t == 'pow':
            f = [ [0, 3],
                  [1, 1],
                  [2, 1],
                  [3, 1] ]
        elif t == 'side':
            f = [ [7, 3],
                  [4, 1],
                  [5, 1],
                  [6 , 1] ]
        elif t == 'block':
            f = [ [8, 3],
                  [9, 1],
                  [10, 1],
                  [11, 1] ]
        elif t == 'grab':
            f = [ [12, 2],
                  [13, 2]]
        elif t == 'dust':
            f = [ [14, 3],
                  [15, 2],
                  [16, 2],
                  [17, 2],
                  [18, 2] ]
        elif t == 'shockwave':
            f = [ [19, 2],
                  [20, 1],
                  [21, 1],
                  [22, 1],
                  [23, 1] ]
        elif t == 'airelementshockwave':
            f = [ [24, 2],
                  [25, 1],
                  [26, 1],
                  [27, 1],
                  [28, 1] ]

        for i in f:
            self.frames.append(Frame(FX_IMAGES[i[0]][0],
                                     FX_IMAGES[i[0]][1], i[1]))

class Frame(object):
    def __init__(self, inImage, inOffset, inLength):
        self.image = inImage
        self.offset = inOffset
        self.length = inLength
        
