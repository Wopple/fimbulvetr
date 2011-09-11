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
    def __init__(self, inImages, speedBase, speedModifiers, team, name,
                 battleChar, portrait):
        self.team = team
        self.name = name
        self.initPortrait(portrait)
        self.battleChar = battleChar
        
        self.speedBase = speedBase
        self.speedModifiers = speedModifiers
        self.vel = [0.0, 0.0]
        self.target = None
        self.currTerrain = 0
        self.oldTerrain = 0
        self.battleTriggerArea = None
        self.battleTriggerRect = None
        self.addToPos = [0, 0]
        self.blinkOn = True
        self.blinkTick = 0
        self.removed = False

        super(MapChar, self).__init__((0, 0), inImages)

    def update(self):
        if self.oldTerrain != self.currTerrain:
            self.startMovement(self.target)
        self.oldTerrain = self.currTerrain
        
        for i in range(2):
            self.precisePos[i] += self.vel[i]

        self.checkForStop()

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
        direction = util.get_direction(self.precisePos, self.target)
        speed = self.getCurrSpeed()

        for i in range(2):
            self.vel[i] = direction[i] * speed

    def getCurrSpeed(self):
        return self.speedBase * self.speedModifiers[self.currTerrain]

    def createBattleTriggerArea(self, zoom):
        r = int(BATTLE_TRIGGER_RANGE * zoom)
        d = int(r*2)
        self.battleTriggerArea = pygame.Surface((d, d), SRCALPHA)
        self.battleTriggerArea.fill ((0, 0, 0, 0))
        pygame.draw.circle(self.battleTriggerArea, BATTLE_TRIGGER_AREA_COLOR_WITH_ALPHA,
                           (r, r), r)
        self.battleTriggerRect = pygame.Rect((0, 0), (d, d))

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
        

def Hare(team, battleChar, name="Unnamed Hare", portrait=None):
    c = MapChar(HARE_TOKENS, HARE_MAP_SPEED_BASE,
                HARE_MAP_SPEED_MODIFIERS, team,
                name, battleChar, portrait)
    return c


def Fox(team, battleChar, name="Unnamed Fox", portrait=None):
    c = MapChar(FOX_TOKENS, FOX_MAP_SPEED_BASE,
                FOX_MAP_SPEED_MODIFIERS, team,
                name, battleChar, portrait)
    return c

def Cat(team, battleChar, name="Unnamed Cat", portrait=None):
    c = MapChar(CAT_TOKENS, CAT_MAP_SPEED_BASE,
                CAT_MAP_SPEED_MODIFIERS, team,
                name, battleChar, portrait)
    return c
