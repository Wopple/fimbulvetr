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

        self.setImage(0)


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
