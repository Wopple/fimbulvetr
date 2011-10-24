import os
import sys
import pygame
import copy

from pygame.locals import *

import drawable
import util
import boundint

import mapitem

from constants import *

class MapChar(mapitem.MapItem):
    def __init__(self, inImages, speedBase, speedTerrainModifiers,
                 speedTerritoryModifiers, speedHealthMod, team, name, battleChar, portrait):
        self.team = team
        self.name = name
        self.initPortrait(portrait)
        self.battleChar = battleChar
        
        self.speedBase = speedBase
        self.speedTerrainModifiers = speedTerrainModifiers
        self.speedTerritoryModifiers = speedTerritoryModifiers
        self.speedHealthModifier = speedHealthMod
        
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

        self.respawnTime = boundint.BoundInt(0, RESPAWN_MAX, 0)

        self.healthRegainTick = 0

        self.triggerColor = BATTLE_TRIGGER_AREA_COLOR_WITH_ALPHA
        self.triggerSize = BATTLE_TRIGGER_RANGE

        super(MapChar, self).__init__((0, 0), inImages)

    def update(self):
        if self.speedHasChanged():
            self.startMovement(self.target)
        self.oldTerrain = self.currTerrain
        self.oldTerritory = self.currTerritory
        
        for i in range(2):
            self.precisePos[i] += self.vel[i]

        self.regainHealth()

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
        val = (self.speedBase *
               self.speedTerrainModifiers[self.currTerrain] *
               self.speedTerritoryModifiers[self.currTerritory] *
               self.getSpeedHealthModifier())

        return val

    def getSpeedHealthModifier(self):
        hp = self.battleChar.hp
        
        currDamageRatio = float( (float(hp.maximum) - float(hp.value))
                                 / float(hp.maximum))

        loss = (1 - self.speedHealthModifier) * currDamageRatio

        return 1.00 - loss

                

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
        return self.battleChar.superEnergy.value

    def addSuperEnergy(self, val):
        self.battleChar.superEnergy.add(val)

    def isDead(self):
        return (self.battleChar.hp.value <= 0)

    def resetRegion(self):
        if self.region is None:
            return

        if (util.distance(self.precisePos, self.region.pos) >
            MAP_REGION_SIZE):
            self.region = None

    def regainHealth(self):
        if ( (self.currTerrain == FORTRESS) and (not self.battleChar.hp.isMax()) and
            (not self.isDead()) ):
            self.healthRegainTick += 1
            if self.healthRegainTick == HEALTH_REGAIN_SPEED:
                self.healthRegainTick = 0
                self.battleChar.hp.add(HEALTH_REGAIN_AMOUNT)
            
        else:
            self.healthRegainTick = 0

    def revive(self):
        self.respawnTime.setToMin()
        self.battleChar.hp.setToMax()
        self.removed = False
        self.setPos(self.respawnPoint)
            
        

def Hare(team, battleChar, name="Unnamed Hare", portrait=None):
    c = MapChar(HARE_TOKENS, HARE_MAP_SPEED_BASE,
                HARE_MAP_SPEED_TERRAIN_MODIFIERS,
                HARE_MAP_SPEED_TERRITORY_MODIFIERS,
                HARE_HEALTH_SPEED_MODIFIER,
                team, name, battleChar, portrait)
    return c


def Fox(team, battleChar, name="Unnamed Fox", portrait=None):
    c = MapChar(FOX_TOKENS, FOX_MAP_SPEED_BASE,
                FOX_MAP_SPEED_TERRAIN_MODIFIERS,
                FOX_MAP_SPEED_TERRITORY_MODIFIERS,
                FOX_HEALTH_SPEED_MODIFIER,
                team, name, battleChar, portrait)
    return c

def Cat(team, battleChar, name="Unnamed Cat", portrait=None):
    c = MapChar(CAT_TOKENS, CAT_MAP_SPEED_BASE,
                CAT_MAP_SPEED_TERRAIN_MODIFIERS,
                CAT_MAP_SPEED_TERRITORY_MODIFIERS,
                CAT_HEALTH_SPEED_MODIFIER,
                team, name, battleChar, portrait)
    return c
