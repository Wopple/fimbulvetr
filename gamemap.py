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


def map00():
    m = GameMap()
    m.startingPoints = [(100, 500)]
    m.mapSize = (1500, 1200)
    m.mountains = [((50, 50), 25),
                   ((125, 300), 50),
                   ((110, 310), 45),
                   ((115, 335), 37),
                   ((788, 500), 80)]
    return m
