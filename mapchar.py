import os
import sys
import pygame
import copy

import drawable
import util

from constants import *

class MapChar(object):
    def __init__(self, inImages, speedBase, speedModifiers, team, name):
        self.team = team
        self.name = name
        self.images = []
        for i in inImages:
            self.images.append(copy.copy(i))
        self.imageNum = -1
        self.speedBase = speedBase
        self.speedModifiers = speedModifiers
        self.precisePos = [0.00, 0.00]
        self.vel = [0.0, 0.0]
        self.target = None

        self.modifyImages()

        self.setImage(0)

    def update(self):
        for i in range(2):
            self.precisePos[i] += self.vel[i]

        self.checkForStop()

    def checkForStop(self):
        if not self.target is None:
            currDist = util.distance(self.precisePos, self.target)

            nextLoc = []
            for i in range(2):
                nextLoc.append(self.precisePos[i] + self.vel[i]) 
            nextDist = util.distance(nextLoc, self.target)
            if nextDist > currDist:
                self.vel = [0.0, 0.0]

    def setPos(self, inPos):
        self.precisePos[0] = float(inPos[0] * 1.00)
        self.precisePos[1] = float(inPos[1] * 1.00)

    def setImage(self, i):
        if i != self.imageNum:
            self.imageNum = i
            self.image = self.images[i]
            pos = ( int(self.precisePos[0]), int(self.precisePos[1]) )
            self.tokenRect = pygame.Rect(pos, self.image.get_size())

    def draw(self, screen, inZoom, inOffset):
            
        pos = (int(self.precisePos[0] * inZoom) + inOffset[0],
               int(self.precisePos[1] * inZoom) + inOffset[1])
        self.tokenRect.center = pos
        screen.blit(self.image, self.tokenRect.topleft)

    def modifyImages(self):
        colorSwap(self.images[0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_OFF[self.team], 100)

        colorSwap(self.images[1], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_HIGHLIGHTED[self.team], 100)

        colorSwap(self.images[2], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_SELECTED, 100)

    def startMovement(self, target):
        self.target = target
        direction = util.get_direction(self.precisePos, self.target)
        speed = self.getCurrSpeed()

        for i in range(2):
            self.vel[i] = direction[i] * speed

    def getCurrSpeed(self):
        return self.speedBase
        

def Hare(team, name="Unnamed Hare"):
    c = MapChar(HARE_TOKENS, HARE_MAP_SPEED_BASE,
                HARE_MAP_SPEED_MODIFIERS, team, name)
    return c
