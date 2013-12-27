import os
import sys
import pygame
import copy

from pygame.locals import *

import drawable
import util
import boundint
import energybar

import mapitem

from common.constants import *
from client.constants import *

from common.util.rect import Rect

class MapStructure(mapitem.MapItem):
    def __init__(self, inPos, inImages, captureTime):

        self.blinkOn = True
        self.removed = False
        self.locked = False

        self.capture = boundint.BoundInt(0, captureTime, 0)
        self.captureTeam = 0

        tempRect = Rect( (0, 0), CAPTURE_BAR_SIZE)
        self.captureBar = energybar.EnergyBar(self.capture, tempRect,
                        CAPTURE_BAR_BORDERS, CAPTURE_BAR_COLORS, 2)

        super(MapStructure, self).__init__(inPos, inImages)

        self.changeOwnership(0)

        self.triggerColor = STRUCTURE_TRIGGER_AREA_COLOR_WITH_ALPHA
        self.triggerSize = STRUCTURE_TRIGGER_RANGE

        self.territoryPoints = []

        self.emptyPlayerList()

    def emptyPlayerList(self):
        self.playersInArea = [[],[]]

    def checkForOwnershipChange(self, autoCap=False):
        
        blueCount = len(self.playersInArea[0])
        redCount = len(self.playersInArea[1])

        #If some blue and no red characters
        if (blueCount > 0 and redCount == 0):
            if autoCap:
                self.changeOwnership(1)
                return True
            else:
                return self.addCapture(1)
            
        #If some red and no blue characters
        elif (redCount > 0 and blueCount == 0):
            if autoCap:
                self.changeOwnership(2)
                return True
            else:
                return self.addCapture(2)
            
        #If no characters of either team
        elif (redCount == 0 and blueCount == 0):
            if not self.capture.isMin():
                self.capture.add(-BASE_CAPTURE_DEGRADE)
                if self.capture.isMin():
                    self.captureTeam = 0

        return False

    def addCapture(self, val):
        
        #If in winter, capture rate is slowed
        if self.locked:
            multiplier = FIMBULVETR_MULTIPLIER
        else:
            multiplier = 1.0
        captureRate = int(BASE_CAPTURE_RATE * multiplier)
        
        #If no team was previously capturing, set current capturing team to input
        if (self.captureTeam == 0 or self.capture.value == 0):
            self.captureTeam = val
        
        #If the input team is capturing it, add to capture bar.  If maximum is reached, change ownership
        if (self.captureTeam == val):
            self.capture.add(captureRate)
            self.captureBar.changeColor(CAPTURE_TEAM_COLORS[val-1])
            if self.capture.isMax():
                if self.team == 0:
                    self.changeOwnership(val)
                else:
                    self.changeOwnership(0)
                return True
        else:
            self.capture.add(-captureRate)
            if self.capture.isMin():
                if (val != self.team):
                    self.changeOwnership(0)
                    return True

        if (self.captureTeam == val and self.team == val and
            (not self.capture.isMin())):
            self.changeOwnership(self.team)
            return False
        
        return False
            
            
        

    def changeOwnership(self, val):
        self.team = val
        self.captureTeam = 0
        self.capture.setToMin()
        self.setImage(self.team)

    def draw(self, screen, inZoom, inOffset):
        if not isinstance(self, Origin):
            super(MapStructure, self).draw(screen, inZoom, inOffset)
        self.setBarPosition()

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


    def setBarPosition(self):
        self.captureBar.rect.midtop = self.tokenRect.midbottom


    def drawBar(self, screen):
        if not self.capture.isMin():
            self.captureBar.update()
            self.captureBar.draw(screen)


class Fortress(MapStructure):
    def __init__(self, inPos):

        self.territorySize = FORTRESS_TERRITORY_RADIUS

        super(Fortress, self).__init__(inPos, MAP_ITEMS["fortress"],
                                       FORTRESS_CAPTURE_TIME)


    def modifyImages(self):
        pass

class Spire(MapStructure):
    def __init__(self, inPos):

        self.territorySize = SPIRE_TERRITORY_RADIUS

        super(Spire, self).__init__(inPos, MAP_ITEMS["spire"],
                                    SPIRE_CAPTURE_TIME)


    def modifyImages(self):
        pass
    
class Altar(MapStructure):
    def __init__(self, inPos):
        
        self.territorySize = ALTAR_TERRITORY_RADIUS
        
        super(Altar, self).__init__(inPos, MAP_ITEMS["altar"],
                                    ALTAR_CAPTURE_TIME)
        
    def modifyImages(self):
        pass
    
class Origin(MapStructure):
    def __init__(self, inPos):
        
        self.territorySize = ORIGIN_TERRITORY_RADIUS
        super(Origin, self).__init__(inPos, MAP_ITEMS["fortress"], 1)
        
    def modifyImages(self):
        pass
