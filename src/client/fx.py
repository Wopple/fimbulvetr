import os
import sys
import pygame

from common.constants import *
from client.constants import *

from common import boundint
from common.util.rect import Rect

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
        self.rect = Rect(self.getRectPos(), size)

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
            f = [ [12, 4],
                  [13, 3]]
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
        elif t == 'runicexplosion':
            f = [ [29, 2],
                  [30, 1],
                  [31, 2],
                  [32, 2],
                  [33, 2] ]
        elif t == 'runicflame1':
            f = [ [35, 3],
                  [36, 1],
                  [37, 1],
                  [38, 1] ]
        elif t == 'runicflame2':
            f = [ [39, 3],
                  [40, 2],
                  [41, 1]]
        elif t == 'runicflame3':
            f = [ [42, 3],
                  [43, 2],
                  [44, 1]]
        elif t == 'fullshockwave':
            f = [ [45, 3],
                  [46, 2],
                  [47, 2],
                  [48, 2],
                  [49, 2],
                  [50, 2] ]

        for i in f:
            self.frames.append(Frame(FX_IMAGES[i[0]][0],
                                     FX_IMAGES[i[0]][1], i[1]))

class Frame(object):
    def __init__(self, inImage, inOffset, inLength):
        self.image = inImage
        self.offset = inOffset
        self.length = inLength
        
