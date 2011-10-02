import os
import sys
import pygame
import copy

from pygame.locals import *

import drawable
import util

import mapitem

from constants import *

class MapChar(mapitem.MapItem):
    def __init__(self, inImages, speedBase, speedTerrainModifiers,
                 speedTerritoryModifiers, team, name, battleChar, portrait):
        self.team = team
        self.name = name
        self.initPortrait(portrait)
        self.battleChar = battleChar
        
        self.speedBase = speedBase
        self.speedTerrainModifiers = speedTerrainModifiers
        self.speedTerritoryModifiers = speedTerritoryModifiers
        
        self.vel = [0.0, 0.0]
        self.target = None
        
        self.currTerrain = 0
        self.oldTerrain = 0
        self.region = None
        self.currTerritory = "allied"
        self.oldTerritory = "allied"
        
        self.addToPos = [0, 0]
        self.blinkOn = True
        self.blinkTick = 0
        self.removed = False

        self.triggerColor = BATTLE_TRIGGER_AREA_COLOR_WITH_ALPHA
        self.triggerSize = BATTLE_TRIGGER_RANGE

        super(MapChar, self).__init__((0, 0), inImages)

    def update(self):
        if self.speedHasChanged():
            self.startMovement(self.target)
            print self.name + ": " + self.currTerritory + " " + str(self.currTerrain)
        self.oldTerrain = self.currTerrain
        self.oldTerritory = self.currTerritory
        
        for i in range(2):
            self.precisePos[i] += self.vel[i]

        self.checkForStop()

    def speedHasChanged(self):
        return ( (self.oldTerrain != self.currTerrain) or
                 (self.oldTerritory != self.currTerritory) )

    def checkForStop(self):
        if not self.target is None:
            currDist = util.distance(self.precisePos, self.target)

            nextLoc = []
            for i in range(2):
                nextLoc.append(self.precisePos[i] + self.vel[i]) 
            nextDist = util.distance(nextLoc, self.target)
            if nextDist > currDist:
                self.stop()

    def stop(self):
        self.vel = [0.0, 0.0]
        self.target = None

    def modifyImages(self):
        colorSwap(self.images[0][0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_OFF[self.team], 60)

        colorSwap(self.images[1][0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_HIGHLIGHTED[self.team], 60)

        colorSwap(self.images[2][0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_SELECTED, 60)

    def startMovement(self, target):
        self.target = target
        if target is None:
            return
        direction = util.get_direction(self.precisePos, self.target)
        speed = self.getCurrSpeed()

        for i in range(2):
            self.vel[i] = direction[i] * speed

    def getCurrSpeed(self):
        print (str(self.speedBase) + " * " +
               str(self.speedTerrainModifiers[self.currTerrain]) + " * " +
               str(self.speedTerritoryModifiers[self.currTerritory]) )
        val = (self.speedBase *
                self.speedTerrainModifiers[self.currTerrain] *
                self.speedTerritoryModifiers[self.currTerritory] )

        print val
        return val

                

    def initPortrait(self, p):
        q = pygame.Surface(MAP_CHAR_BAR_PORTRAIT_SIZE)
        if not p is None:
            q.blit(p, (0, 0))
        q.convert()
        self.portrait = q

    def getHP(self):
        return self.battleChar.hp.value

    def getMaxHP(self):
        return self.battleChar.hp.maximum

    def getSuperEnergy(self):
        return 50

    def isDead(self):
        return (self.battleChar.hp.value <= 0)

    def resetRegion(self):
        if self.region is None:
            return

        if (util.distance(self.precisePos, self.region.pos) >
            MAP_REGION_SIZE):
            self.region = None
        

def Hare(team, battleChar, name="Unnamed Hare", portrait=None):
    c = MapChar(HARE_TOKENS, HARE_MAP_SPEED_BASE,
                HARE_MAP_SPEED_TERRAIN_MODIFIERS,
                HARE_MAP_SPEED_TERRITORY_MODIFIERS,
                team, name, battleChar, portrait)
    return c


def Fox(team, battleChar, name="Unnamed Fox", portrait=None):
    c = MapChar(FOX_TOKENS, FOX_MAP_SPEED_BASE,
                FOX_MAP_SPEED_TERRAIN_MODIFIERS,
                FOX_MAP_SPEED_TERRITORY_MODIFIERS,
                team, name, battleChar, portrait)
    return c

def Cat(team, battleChar, name="Unnamed Cat", portrait=None):
    c = MapChar(CAT_TOKENS, CAT_MAP_SPEED_BASE,
                CAT_MAP_SPEED_TERRAIN_MODIFIERS,
                CAT_MAP_SPEED_TERRITORY_MODIFIERS,
                team, name, battleChar, portrait)
    return c
