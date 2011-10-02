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

        self.territoryPoints = []

        self.emptyPlayerList()

    def emptyPlayerList(self):
        self.playersInArea = [[],[]]

    def checkForOwnershipChange(self):
        blueCount = len(self.playersInArea[0])
        redCount = len(self.playersInArea[1])

        if (blueCount > 0 and redCount == 0):
            if self.team != 1:
                self.changeOwnership(1)
                return True

        if (redCount > 0 and blueCount == 0):
            if self.team != 2:
                self.changeOwnership(2)
                return True

        return False

    def changeOwnership(self, val):
        self.team = val
        self.setImage(self.team)

    def draw(self, screen, inZoom, inOffset):
        super(MapStructure, self).draw(screen, inZoom, inOffset)

        for p in self.territoryPoints:
            pos = p[0]
            contested = p[1]
            
            dp = (int(pos[0] * inZoom)
                      + inOffset[0] - TERRITORY_DOT_OFFSET,
                  int(pos[1] * inZoom)
                      + inOffset[1] - TERRITORY_DOT_OFFSET)

            if contested:
                image = TERRITORY_DOT_IMAGES[0]
            else:
                image = TERRITORY_DOT_IMAGES[self.team]
                
            screen.blit(image, dp)


class Fortress(MapStructure):
    def __init__(self, inPos):

        self.territorySize = FORTRESS_TERRITORY_RADIUS

        super(Fortress, self).__init__(inPos, MAP_ITEMS["fortress"])


    def modifyImages(self):
        colorSwap(self.images[1][0], FORTRESS_NEUTRAL,
                  FORTRESS_TEAM_COLORS[0], 135)

        colorSwap(self.images[2][0], FORTRESS_NEUTRAL,
                  FORTRESS_TEAM_COLORS[1], 135)

class Spire(MapStructure):
    def __init__(self, inPos):

        self.territorySize = SPIRE_TERRITORY_RADIUS

        super(Spire, self).__init__(inPos, MAP_ITEMS["spire"])


    def modifyImages(self):
        colorSwap(self.images[1][0], SPIRE_NEUTRAL,
                  SPIRE_TEAM_COLORS[0], 75)

        colorSwap(self.images[2][0], SPIRE_NEUTRAL,
                  SPIRE_TEAM_COLORS[1], 75)
