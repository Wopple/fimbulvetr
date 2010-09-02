import os
import sys
import pygame

from constants import *

class GameMap(object):
    def __init__(self):
        self.startingPoints = [(0, 0)]
        self.mapSize = (1000, 1000)
        self.primaryTerrain = 0
        self.mountains = []
        self.water = []
        self.forests = []


def getMap(s):
    try:
        i = int(s)
    except:
        return None

    m = GameMap()

    if i == 0:
        m.startingPoints = [ [(100, 500),
                              (120, 520)],
                             [(800, 200)] ]
        m.mapSize = (1500, 1200)
        m.mountains = [((50, 50), 25),
                       ((125, 300), 50),
                       ((110, 310), 45),
                       ((115, 335), 37),
                       ((788, 500), 80)]
        m.water = [((260, 350), 70),
                   ((265, 330), 50)]
        m.forests = [((450, 120), 30)]

    return m

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

