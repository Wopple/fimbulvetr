import os
import sys
import pygame

from constants import *

import copy

import time

class GameMap(object):
    def __init__(self, startingPoints, mapSize, horizAxis, flip,
                 mountains, water, forests, islands, rivers):

        self.horizAxis = horizAxis
        self.flip = flip

        if horizAxis:
            self.mapSize = [mapSize[0], mapSize[1] * 2]
        else:
            self.mapSize = [mapSize[0] * 2, mapSize[1]]

        self.primaryTerrain = 0

        self.surfaceTemplate = pygame.Surface(self.mapSize)
        self.surfaceTemplate.fill(TERRAIN_COLORS[self.primaryTerrain])

        self.mountains = mountains
        self.water = water
        self.forests = forests
        self.islands = islands
        self.rivers = rivers

        self.testCircles = []

        self.mirror(self.mountains)
        self.mirror(self.water)
        self.mirror(self.forests)
        self.mirror(self.islands)
        self.mirror(self.rivers)

        self.mirrorStartingPoints(startingPoints)

    def mirror(self, inList):
        temp = []

        for i in inList:
            p = self.flipPoint(i[0])
            temp.append( (p, i[1]) )

        for i in temp:
            inList.append(i)

    def mirrorStartingPoints(self, inPoints):
        self.startingPoints = []

        temp = []
        for i in inPoints:
            temp.append(i)

        self.startingPoints.append(temp)

        temp = []
        for i in inPoints:
            temp.append(self.flipPoint(i))

        self.startingPoints.append(temp)

    def flipPoint(self, p):
        if self.flip:
            if self.horizAxis:
                x = p[0]
                y = self.mapSize[1] - p[1]
            else:
                x = self.mapSize[0] - p[0]
                y = p[1]

        return (x, y)
        

def getMap(s):
    try:
        i = int(s)
    except:
        return None

    if i == 0:
        startingPoints = [(0, 0),
                          (20, 20),
                          (10, 35)]
        
        mapSize = (4000, 1500)
        horizAxis = True
        flip = True
        
        mountains = [((-20, 420), 125),
                     ((60, 435), 80),
                     ((50, 470), 70),
                     ((12, 512), 45)]
        
        water = []
        
        forests = [((220, 225), 80),
                   ((240, 200), 65),
                   ((275, 200), 70),
                   ((290, 200), 72),]

        islands = []
        
        rivers = []
        
    else:
        return None

    return GameMap(startingPoints, mapSize, horizAxis, flip,
                   mountains, water, forests, islands, rivers)

def drawMap(inMap):
    mapImage = pygame.Surface.copy(inMap.surfaceTemplate)
    for i in inMap.water:
        pygame.draw.circle(mapImage, WATER_FILL_COLOR, i[0], i[1])
    for i in inMap.islands:
        pygame.draw.circle(mapImage, TERRAIN_COLORS[0], i[0], i[1])
    for i in inMap.mountains:
        pygame.draw.circle(mapImage, MOUNTAIN_FILL_COLOR, i[0], i[1])
    for i in inMap.forests:
        pygame.draw.circle(mapImage, FOREST_FILL_COLOR, i[0], i[1])
    for i in inMap.rivers:
        pygame.draw.circle(mapImage, WATER_FILL_COLOR, i[0], i[1])

    if DEBUG_MODE:
        for m in range(2):
            for n in range(2):
                for i in inMap.testCircles:
                    if i[2] == m and i[3] == n:
                        pygame.draw.circle(mapImage, TEST_CIRCLE_COLORS[m][n],
                                           i[0], i[1])
    
    return mapImage
    

