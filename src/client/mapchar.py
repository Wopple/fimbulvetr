import os
import sys
import pygame
import copy

from pygame.locals import *

import drawable
import util

import mapitem

import hare, cat, fox

from common.constants import *
from client.constants import *

from common import boundint

class MapChar(mapitem.MapItem):
    def __init__(self, mapCloneMethod, battleCloneMethod, speciesAbbrev, inImages,
                 speedBase, speedTerrainModifiers, speedTerritoryModifiers,
                 speedHealthMod, team, name, battleChar, portrait, homeTerrain):
        
        self.mapCloneMethod = mapCloneMethod
        self.battleCloneMethod = battleCloneMethod
        self.speciesAbbrev = speciesAbbrev
        
        self.team = team
        self.name = name
        self.initPortrait(portrait)
        self.battleChar = battleChar
        self.homeTerrain = homeTerrain
        self.altarCount = 0
        
        self.speedBase = speedBase
        self.speedTerrainModifiers = speedTerrainModifiers
        self.speedTerritoryModifiers = speedTerritoryModifiers
        self.speedHealthModifier = speedHealthMod
        
        self.vel = [0.0, 0.0]
        self.target = None
        
        self.targetBuffer = []
        
        self.currTerrain = 0
        self.oldTerrain = 0
        self.region = None
        self.currTerritory = "allied"
        self.oldTerritory = "allied"
        
        self.addToPos = [0, 0]
        self.blinkOn = True
        self.blinkTick = 0
        self.removed = False
        self.rezzing = False
        self.rezTime = 0

        self.respawnTime = boundint.BoundInt(0, RESPAWN_MAX, 0)

        self.healthRegainTick = 0

        self.triggerColor = BATTLE_TRIGGER_AREA_COLOR_WITH_ALPHA
        self.triggerSize = BATTLE_TRIGGER_RANGE

        super(MapChar, self).__init__((0, 0), inImages)

    def update(self):
        if self.speedHasChanged():
            self.startMovement()
        self.oldTerrain = self.currTerrain
        self.oldTerritory = self.currTerritory
        
        if (not self.isDead()):
            for i in range(2):
                self.precisePos[i] += self.vel[i]

        self.regainHealth()

        self.checkForStop()

        if self.rezzing:
            self.rezTime += 1
            if self.rezTime == REZ_TIME:
                self.rezTime = 0
                self.rez()
        else:
            self.rezTime = 0

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
                if len(self.targetBuffer) > 0:
                    self.target = self.targetBuffer[0]
                    self.targetBuffer = self.targetBuffer[1:]
                    self.startMovement()
                else:
                    self.stop()

    def stop(self):
        self.vel = [0.0, 0.0]
        self.target = None
        self.targetBuffer = []

    def modifyImages(self):
        colorSwap(self.images[0][0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_OFF[self.team], 5)

        colorSwap(self.images[1][0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_HIGHLIGHTED[self.team], 5)

        colorSwap(self.images[2][0], TOKEN_BORDER_NEUTRAL,
                  TOKEN_BORDER_SELECTED[self.team], 5)

    
    def setTarget(self, target, waypoint):
        if self.isDead() and (not self.rezzing):
            waypoint = False
            
        if waypoint and (not self.target is None):
            self.setTargetWaypoint(target)
            return
        else:
            self.setTargetSingle(target)
            
        self.startMovement()
            
            
    def startMovement(self):
        if self.target is None:
            return
        direction = util.get_direction(self.precisePos, self.target)
        speed = self.getCurrSpeed()

        for i in range(2):
            self.vel[i] = direction[i] * speed
            
    def setTargetWaypoint(self, target):
        if self.target is None:
            self.target = target
        else:
            if (not target is None) and (len(self.targetBuffer) < MAX_WAYPOINTS):
                self.targetBuffer.append(target)
                
    def setTargetSingle(self, target):
        self.target = target
        self.targetBuffer = []

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
        q = pygame.Surface(UNIT_HUD_PORTRAIT_SIZE)
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
        if ( (not self.battleChar.hp.isMax()) and (not self.isDead()) ):
            self.healthRegainTick += 1
            if self.healthRegainTick == HEALTH_REGAIN_SPEED:
                self.healthRegainTick = 0
                if (self.currTerrain == FORTRESS):
                    hpGain = FORTRESS_HEALTH_REGAIN_AMOUNT
                else:
                    hpGain = PASSIVE_HEALTH_REGAIN_AMOUNT
                self.battleChar.hp.add(hpGain)
            
        else:
            self.healthRegainTick = 0

    def revive(self):
        self.respawnTime.setToMin()
        self.setPos(self.target)
        self.rezzing = True

    def rez(self):
        self.battleChar.hp.setToMax()
        self.removed = False
        self.rezzing = False
        
    def getDamagePercentText(self):
        return str(self.damagePercent()) + "%"
        
    def damagePercent(self):
        mult = 100
        
        if self.currTerrain == self.homeTerrain:
            mult += HOME_TERRAIN_DAMAGE_BONUS
        elif self.currTerrain == FORTRESS:
            mult += FORTRESS_DAMAGE_BONUS
            
        mult += (ALTAR_DAMAGE_BONUS * self.altarCount)
            
        return mult
    
    def getSmallImage(self):
        return self.images[3][0]
    
    
    def getTextString(self, expand=False):
        text = self.name + "#" + self.speciesAbbrev + "#" + str(self.battleChar.currSuperMove) + "#"
        
        if expand:
            size = len(text)
            if size > CHARACTER_TRANSFER_NET_MESSAGE_SIZE:
                raise
            add = CHARACTER_TRANSFER_NET_MESSAGE_SIZE - size
            
            for i in range(add):
                text = text + "-"
                
        return text
    

def makeCharacterFromInfo(info, team):
    if info.speciesName == "hr":
        data = [Hare, hare.Hare]
    elif info.speciesName == "fx":
        data = [Fox, fox.Fox]
    elif info.speciesName == "ct":
        data = [Cat, cat.Cat]
    
    return data[0](team, data[1](info.name, info.currSuperMove), info.name)
    
def turnStringIntoInfo(text):
    vals = text.split('#')
    name = vals[0]
    speciesName = vals[1]
    currSuperMove = int(vals[2])
    return CharInfo(name, speciesName, currSuperMove)
    
def convertNetData(dataList, team):
    charList = []
    for d in dataList:
        info = turnStringIntoInfo(d)

        charList.append(makeCharacterFromInfo(info, team))

    return charList

class CharInfo(object):
    def __init__(self, name, speciesName, currSuperMove, valid=True):
        self.name = name
        self.speciesName = speciesName
        self.currSuperMove = currSuperMove
        self.valid = valid

        

def Hare(team, battleChar, name="Hare", portrait=None):
    c = MapChar(Hare, hare.Hare, "hr", HARE_TOKENS, HARE_MAP_SPEED_BASE,
                HARE_MAP_SPEED_TERRAIN_MODIFIERS,
                HARE_MAP_SPEED_TERRITORY_MODIFIERS,
                HARE_HEALTH_SPEED_MODIFIER,
                team, name, battleChar, portrait, HOME_TERRAINS["hare"])
    return c


def Fox(team, battleChar, name="Fox", portrait=None):
    c = MapChar(Fox, fox.Fox, "fx", FOX_TOKENS, FOX_MAP_SPEED_BASE,
                FOX_MAP_SPEED_TERRAIN_MODIFIERS,
                FOX_MAP_SPEED_TERRITORY_MODIFIERS,
                FOX_HEALTH_SPEED_MODIFIER,
                team, name, battleChar, portrait, HOME_TERRAINS["fox"])
    return c

def Cat(team, battleChar, name="Cat", portrait=None):
    c = MapChar(Cat, cat.Cat, "ct", CAT_TOKENS, CAT_MAP_SPEED_BASE,
                CAT_MAP_SPEED_TERRAIN_MODIFIERS,
                CAT_MAP_SPEED_TERRITORY_MODIFIERS,
                CAT_HEALTH_SPEED_MODIFIER,
                team, name, battleChar, portrait, HOME_TERRAINS["cat"])
    return c
