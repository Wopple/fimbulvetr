import os
import sys
import pygame
import copy

from pygame.locals import *

import drawable
import util

import mapitem

from constants import *

class MapStructure(mapitem.MapItem):
    def __init__(self, inPos, inImages):

        self.blinkOn = True
        self.removed = False

        super(MapStructure, self).__init__(inPos, inImages)

        self.changeOwnership(0)

        self.triggerColor = STRUCTURE_TRIGGER_AREA_COLOR_WITH_ALPHA
        self.triggerSize = STRUCTURE_TRIGGER_RANGE

        self.emptyPlayerList()

    def emptyPlayerList(self):
        self.playersInArea = [[],[]]

    def checkForOwnershipChange(self):
        blueCount = len(self.playersInArea[0])
        redCount = len(self.playersInArea[1])

        if (blueCount > 0 and redCount == 0):
            self.changeOwnership(1)

        if (redCount > 0 and blueCount == 0):
            self.changeOwnership(2)

    def changeOwnership(self, val):
        self.team = val
        self.setImage(self.team)


class Fortress(MapStructure):
    def __init__(self, inPos):

        super(Fortress, self).__init__(inPos, MAP_ITEMS["fortress"])


    def modifyImages(self):
        colorSwap(self.images[1][0], FORTRESS_NEUTRAL,
                  FORTRESS_TEAM_COLORS[0], 135)

        colorSwap(self.images[2][0], FORTRESS_NEUTRAL,
                  FORTRESS_TEAM_COLORS[1], 135)

class Spire(MapStructure):
    def __init__(self, inPos):

        super(Spire, self).__init__(inPos, MAP_ITEMS["spire"])


    def modifyImages(self):
        colorSwap(self.images[1][0], SPIRE_NEUTRAL,
                  SPIRE_TEAM_COLORS[0], 75)

        colorSwap(self.images[2][0], SPIRE_NEUTRAL,
                  SPIRE_TEAM_COLORS[1], 75)
