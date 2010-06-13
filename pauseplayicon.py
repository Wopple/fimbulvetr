import os
import sys
import pygame
import copy

from constants import *

import mapinterfaceitem

class PausePlayIcon(mapinterfaceitem.MapInterfaceItem):
    def __init__(self, inType):
        self.images = [copy.copy(INTERFACE_GRAPHICS[0]),
                       copy.copy(INTERFACE_GRAPHICS[1])]
        self.currImage = 0

        super(PausePlayIcon, self).__init__()

        if inType == 0:
            xMod = -PAUSE_PLAY_LITTLE_ADJUSTMENT[0]
            yMod = PAUSE_PLAY_LITTLE_ADJUSTMENT[1]
            colorMod = PAUSE_PLAY_LITTLE_COLORS[0]
            resize = PAUSE_PLAY_RESIZE_FACTOR
            self.moveFactor = -1
        elif inType == 1:
            xMod = PAUSE_PLAY_LITTLE_ADJUSTMENT[0]
            yMod = PAUSE_PLAY_LITTLE_ADJUSTMENT[1]
            colorMod = PAUSE_PLAY_LITTLE_COLORS[1]
            resize = PAUSE_PLAY_RESIZE_FACTOR
            self.moveFactor = 1
        elif inType == 2:
            xMod = 0
            yMod = 0
            colorMod = None
            resize = None
            self.moveFactor = 0

        size = self.images[0].get_size()
        
        if not colorMod is None:
            for i in self.images:
                i = colorSwap(i, PAUSE_PLAY_ORIG_COLOR, colorMod, 80)

        if not resize is None:
            for i, s in enumerate(self.images):
                self.images[i] = pygame.transform.scale(s,
                                                        (int(size[0] * resize),
                                                         int(size[1] * resize)))
            size = self.images[0].get_size()
        


        x = (SCREEN_SIZE[0] / 2) - (size[0] / 2) + xMod
        y = PAUSE_PLAY_BIG_FROM_TOP + yMod

        self.rect = pygame.Rect((x, y), size)

        self.pauseX = self.rect.left
        self.xMovement = 0

    def update(self, val):
        if val:
            self.currImage = 0
        else:
            self.currImage = 1


        if self.currImage == 0:
            self.xMovement -= PAUSE_PLAY_MOVEMENT_SPEED
            if self.xMovement < 0:
                self.xMovement = 0
        else:
            self.xMovement += PAUSE_PLAY_MOVEMENT_SPEED
            if self.xMovement > PAUSE_PLAY_MOVEMENT_DISTANCE:
                self.xMovement = PAUSE_PLAY_MOVEMENT_DISTANCE

        self.rect.left = self.pauseX + (self.xMovement * self.moveFactor)

        self.image = self.images[self.currImage]

        super(PausePlayIcon, self).update()
