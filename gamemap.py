import os
import sys
import pygame

from constants import *

class GameMap(object):
    def __init__(self, startingPoints, mapSize, horizAxis, flip,
                 mountains, water, forests):

        self.horizAxis = horizAxis
        self.flip = flip

        if horizAxis:
            self.mapSize = [mapSize[0], mapSize[1] * 2]
        else:
            self.mapSize = [mapSize[0] * 2, mapSize[1]]

        self.primaryTerrain = 0

        self.mountains = mountains
        self.water = water
        self.forests = forests

        self.mirror(self.mountains)
        self.mirror(self.water)
        self.mirror(self.forests)

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
        startingPoints = [(100, 500),
                          (120, 520)]
        
        mapSize = (1500, 1200)
        horizAxis = False
        flip = True
        
        mountains = [((50, 50), 25),
                       ((125, 300), 50),
                       ((110, 310), 45),
                       ((115, 335), 37),
                       ((788, 500), 80)]
        water = [((260, 350), 70),
                   ((265, 330), 50)]
        forests = [((450, 120), 30)]
        
    else:
        return None

    return GameMap(startingPoints, mapSize, horizAxis, flip,
                   mountains, water, forests)

def drawMap(inMap):
    mapImage = pygame.Surface(inMap.mapSize)
    mapImage.fill(TERRAIN_COLORS[inMap.primaryTerrain])
    for i in inMap.mountains:
        pygame.draw.circle(mapImage, MOUNTAIN_FILL_COLOR, i[0], i[1])
    for i in inMap.water:
        pygame.draw.circle(mapImage, WATER_FILL_COLOR, i[0], i[1])
    for i in inMap.forests:
        pygame.draw.circle(mapImage, FOREST_FILL_COLOR, i[0], i[1])

    return mapImage
    

