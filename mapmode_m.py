import os
import sys
import pygame

import mvc
import gamemap
import mapchar
import util
import incint
import pauseplayicon
import mapcharacterbar
import targetmarker

from constants import *

class Model(mvc.Model):
    def __init__(self, inMap, inChars, team):
        super(Model, self).__init__()
        self.team = team
        self.map = inMap
        self.zoomVal = 1.0
        
        self.characters = inChars
        self.charactersInTeams = [[], []]
        for c in self.characters:
            self.charactersInTeams[c.team].append(c)
        
        if SHOW_BATTLE_TRIGGER_AREA:
            self.setBattleTriggerAreas()
        self.mapRect = None
        self.currHighlighted = None
        self.currSelected = None
        self.drawOrigMap()
        self.mousePos = pygame.mouse.get_pos()
        self.placeChars()
        self.pendingBattle = None
        self.pause = [False, False]
        self.keys = [False, False, False, False]

        self.buildInterface()

    def update(self):
        self.checkForBattle()

        self.mousePos = pygame.mouse.get_pos()
        self.checkScrolling()
        self.checkMouseOverObject()
        for c in self.characters:
            if c is self.currSelected:
                c.setImage(2)
            elif c is self.currHighlighted:
                c.setImage(1)
            else:
                c.setImage(0)

        self.updateInterface()
        
        if (self.pendingBattle is None) and (not self.paused()):
            for c in self.characters:
                self.checkBounds(c)
                self.checkTerrain(c)
                c.update()

    def zoom(self):
        self.drawZoomMap()
        self.adjustMap()
        if SHOW_BATTLE_TRIGGER_AREA:
            self.setBattleTriggerAreas()
            

    def drawOrigMap(self):
        
        self.mapOrigImage = pygame.Surface(self.map.mapSize)
        self.mapOrigImage.fill(TERRAIN_COLORS[self.map.primaryTerrain])
        for i in self.map.mountains:
            pygame.draw.circle(self.mapOrigImage, MOUNTAIN_FILL_COLOR, i[0], i[1])

        self.drawZoomMap()

    def drawZoomMap(self):
        newSize = (int(self.map.mapSize[0] * self.zoomVal),
                       int(self.map.mapSize[1] * self.zoomVal))
        
        if not self.mapRect is None:
            diff = ((self.mapRect.width - newSize[0]),
                    (self.mapRect.height - newSize[1]))
            newPos = ((self.mapRect.left + (diff[0] / 2)),
                      (self.mapRect.top + (diff[1] / 2)))
            self.mapRect = pygame.Rect(newPos, newSize)
        else:
            self.mapRect = pygame.Rect((0, 0), newSize)
        self.mapImage = pygame.transform.scale(self.mapOrigImage, newSize)

    def scrollIn(self):
        self.zoomVal /= ZOOM_CLICK
        if self.zoomVal > ZOOM_MAX:
            self.zoomVal = ZOOM_MAX
        self.zoom()

    def scrollOut(self):
        self.zoomVal *= ZOOM_CLICK
        if self.zoomVal < ZOOM_MIN:
            self.zoomVal = ZOOM_MIN
        self.zoom()

    def checkScrolling(self):
        axis = [0, 0]

        for i in range(2):
            if self.mousePos[i] < SCROLL_AREA_WIDTH:
                axis[i] = -1
            if self.mousePos[i] > SCREEN_SIZE[i] - SCROLL_AREA_WIDTH:
                axis[i] = 1

        if self.keys[0] and not self.keys[1]:
            axis[1] = -1
        if self.keys[1] and not self.keys[0]:
            axis[1] = 1
        if self.keys[2] and not self.keys[3]:
            axis[0] = -1
        if self.keys[3] and not self.keys[2]:
            axis[0] = 1
        

        self.mapRect.left -= SCROLL_SPEED * axis[0]
        self.mapRect.top -= SCROLL_SPEED * axis[1]

        if (axis[0] != 0) or (axis[1] != 0):
            self.adjustMap()

    def scrollMap(self):
        
        self.adjustMap()

    def adjustMap(self):
        if self.mapRect.left > 0:
            self.mapRect.left = 0
        if self.mapRect.right < SCREEN_SIZE[0]:
            self.mapRect.right = SCREEN_SIZE[0]
        if self.mapRect.width < SCREEN_SIZE[0]:
            self.mapRect.left = (SCREEN_SIZE[0] / 2) - (self.mapRect.width / 2)

        if self.mapRect.top > 0:
            self.mapRect.top = 0
        if self.mapRect.bottom < SCREEN_SIZE[1]:
            self.mapRect.bottom = SCREEN_SIZE[1]
        if self.mapRect.height < SCREEN_SIZE[1]:
            self.mapRect.top = (SCREEN_SIZE[1] / 2) - (self.mapRect.height / 2)

    def placeChars(self):
        for team in range(2):
            s = len(self.map.startingPoints[team])
            count = 0
            for c in self.characters:
                if c.team == team:
                    if count < s:
                        spot = self.map.startingPoints[team][count]
                    else:
                        spot = self.map.startingPoints[team][0]
                    c.setPos(spot)
                    count += 1

    def leftClick(self):
        if isinstance(self.currHighlighted, mapchar.MapChar):
            if self.currHighlighted.team == self.team:
                self.currSelected = self.currHighlighted
                return

        self.currSelected = None

    def rightClick(self):
        if (not self.currSelected is None) and (not self.paused()):
            self.currSelected.startMovement(self.absMousePos())

    def absMousePos(self):
        temp = []
        for i in range(2):
            temp.append((self.mousePos[i] - self.mapRect.topleft[i]) / self.zoomVal)

        return temp

    def checkMouseOverObject(self):
        
        if self.mouseOverCharacter(self.currSelected):
            self.currHighlighted = self.currSelected
            return
        
        if self.mouseOverCharacter(self.currHighlighted):
            return
        
        for c in self.characters:
            if self.mouseOverCharacter(c):
                self.currHighlighted = c
                return

        self.currHighlighted = None

    def mouseOverCharacter(self, c):
        if isinstance(c, mapchar.MapChar):
            if c.tokenRect.collidepoint(self.mousePos):
                return True

        return False

    def checkTerrain(self, c):
        for i in self.map.mountains:
            dist = util.distance(c.precisePos, i[0])
            if dist <= i[1]:
                c.currTerrain = 2
                return

            c.currTerrain = 0

    def checkBounds(self, c):
        future = [c.precisePos[0] + c.vel[0],
                  c.precisePos[1] + c.vel[1]]

        for i in range(2):
            if (future[i] <= 0) or (future[i] >= self.map.mapSize[i]):
                c.stop()

            if c.precisePos[i] < 0:
                c.precisePos[i] = 0
            if c.precisePos[i] > self.map.mapSize[i]:
                c.precisePos[i] = self.map.mapSize[i]


    def setBattleTriggerAreas(self):
        for c in self.characters:
            c.createBattleTriggerArea(self.zoomVal)

    def checkForBattle(self):
        self.pendingBattle = None
        for c in self.charactersInTeams[0]:
            for d in self.charactersInTeams[1]:
                dist = util.distance(c.precisePos, d.precisePos)
                if dist <= BATTLE_TRIGGER_RANGE:
                    self.pendingBattle = [c, d]
                    return

    def resolveBattle(self, result):
        for i in range(2):
            self.pendingBattle[i].stop()

            if i == 0:
                temp = [1, 0]
            else:
                temp = [0, 1]
            temp2 = util.get_direction(self.pendingBattle[temp[0]].precisePos,
                                       self.pendingBattle[temp[1]].precisePos)
            retreat = []
            for j in range(2):
                retreat.append(temp2[j] * RETREAT_DISTANCE)
            
            if result[i] == 1:
                for j in range(2):
                    self.pendingBattle[i].precisePos[j] += retreat[j]

    def paused(self):
        return ((self.pause[0]) or (self.pause[1]))

    def pausePressed(self):
        self.pause[self.team] = not(self.pause[self.team])

    def buildInterface(self):
        self.bigPausePlayIcon = pauseplayicon.PausePlayIcon(2)

        self.littlePausePlayIcons = []
        for i in range(2):
            self.littlePausePlayIcons.append(pauseplayicon.PausePlayIcon(i))

        self.charBars = []
        for i, c in enumerate(self.charactersInTeams[self.team]):
            x = MAP_CHAR_BAR_INIT_POS[0]
            if i == 0:
                y = MAP_CHAR_BAR_INIT_POS[1]
            else:
                y = self.charBars[i-1].rect.bottom + MAP_CHAR_BAR_SPACING

            bar = mapcharacterbar.MapCharacterBar((x, y), c)
            self.charBars.append(bar)

        self.targetMarker = targetmarker.TargetMarker()

    def updateInterface(self):
        self.updatePausePlayIcons()

    def updatePausePlayIcons(self):
        self.bigPausePlayIcon.update(self.paused())
        self.bigPausePlayIcon.setAlphaFade(self.paused())

        for i in range(2):
            self.littlePausePlayIcons[i].update(self.pause[i])
            self.littlePausePlayIcons[i].setAlphaFade(self.paused())

        for i in self.charBars:
            i.update()
            i.setActive(i.character is self.currSelected)
            i.setAlphaFade(self.isHighlightedOrSelected(i.character))

    def isHighlightedOrSelected(self, i):
        return ((i is self.currHighlighted) or (i is self.currSelected))

    def numberKey(self, k):
        try:
            k = int(k)
        except:
            k = 0

        k -= 1

        if (k >= 0) and (k < len(self.charactersInTeams[self.team])):
            if self.currSelected is self.charactersInTeams[self.team][k]:
                self.centerOnCharacter(self.currSelected)
            else:
                self.currSelected = self.charactersInTeams[self.team][k]

    def key(self, k, t):
        self.keys[k] = t

    def centerOnCharacter(self, c):
        newLoc = [0, 0]
        for i in range(2):
            newLoc[i] = -(int(c.precisePos[i])) + (SCREEN_SIZE[i] / 2)

        self.mapRect.topleft = newLoc
        self.adjustMap()

def testData():
    chars = [mapchar.Hare(0, "Awesomez", HARE_PORTRAITS[0]),
             mapchar.Hare(1, "Bob"),
             mapchar.Hare(0, "Dude")]
    return [gamemap.map00(), chars]
