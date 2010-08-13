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

    return m
