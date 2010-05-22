import os
import sys
import pygame

import mvc
import gamemap
import mapchar

import incint

from constants import *

class Model(mvc.Model):
    def __init__(self, inMap, inChars):
        super(Model, self).__init__()
        self.map = inMap
        self.characters = inChars
        self.zoomVal = 1.0
        self.mapRect = None
        self.drawOrigMap()
        self.mousePos = pygame.mouse.get_pos()
        self.placeChars()

    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        self.checkScrolling()

    def zoom(self):
        self.drawZoomMap()
        self.adjustMap()

    def drawOrigMap(self):
        
        self.mapOrigImage = pygame.Surface(self.map.mapSize)
        self.mapOrigImage.fill(TERRAIN_COLORS[self.map.primaryTerrain])
        for i in self.map.mountains:
            pygame.draw.circle(self.mapOrigImage, MOUNTAIN_FILL_COLOR, i[0], i[1])

        self.drawZoomMap()

    def drawZoomMap(self):
        newSize = (int(self.map.mapSize[0] * self.zoomVal),
                       int(self.map.mapSize[1] * self.zoomVal))
        
        if not self.mapRect is None:
            diff = ((self.mapRect.width - newSize[0]),
                    (self.mapRect.height - newSize[1]))
            newPos = ((self.mapRect.left + (diff[0] / 2)),
                      (self.mapRect.top + (diff[1] / 2)))
            self.mapRect = pygame.Rect(newPos, newSize)
        else:
            self.mapRect = pygame.Rect((0, 0), newSize)
        self.mapImage = pygame.transform.scale(self.mapOrigImage, newSize)

    def scrollIn(self):
        self.zoomVal /= ZOOM_CLICK
        if self.zoomVal > ZOOM_MAX:
            self.zoomVal = ZOOM_MAX
        self.zoom()

    def scrollOut(self):
        self.zoomVal *= ZOOM_CLICK
        if self.zoomVal < ZOOM_MIN:
            self.zoomVal = ZOOM_MIN
        self.zoom()

    def checkScrolling(self):
        axis = [0, 0]

        for i in range(2):
            if self.mousePos[i] < SCROLL_AREA_WIDTH:
                axis[i] = -1
            if self.mousePos[i] > SCREEN_SIZE[i] - SCROLL_AREA_WIDTH:
                axis[i] = 1

        self.mapRect.left -= SCROLL_SPEED * axis[0]
        self.mapRect.top -= SCROLL_SPEED * axis[1]

        if (axis[0] != 0) or (axis[1] != 0):
            self.adjustMap()

    def scrollMap(self):
        
        self.adjustMap()

    def adjustMap(self):
        if self.mapRect.left > 0:
            self.mapRect.left = 0
        if self.mapRect.right < SCREEN_SIZE[0]:
            self.mapRect.right = SCREEN_SIZE[0]
        if self.mapRect.width < SCREEN_SIZE[0]:
            self.mapRect.left = (SCREEN_SIZE[0] / 2) - (self.mapRect.width / 2)

        if self.mapRect.top > 0:
            self.mapRect.top = 0
        if self.mapRect.bottom < SCREEN_SIZE[1]:
            self.mapRect.bottom = SCREEN_SIZE[1]
        if self.mapRect.height < SCREEN_SIZE[1]:
            self.mapRect.top = (SCREEN_SIZE[1] / 2) - (self.mapRect.height / 2)

    def placeChars(self):
        s = len(self.map.startingPoints)
        for i in range(len(self.characters)):
            if i < s:
                spot = self.map.startingPoints[i]
            else:
                spot = self.map.startingPoints[0]
            self.characters[i].setPos(spot)
                    
        

def testData():
    chars = [mapchar.Hare()]
    return [gamemap.map00(), chars]
