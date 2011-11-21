import os
import sys
import pygame
import math
import copy

import mvc
import gamemap
import mapchar
import util
import incint
import pauseplayicon
import mapcharacterbar
import targetmarker
import countdown

import mapstructure

import hare, fox, cat

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
        self.mapRect = None
        self.currHighlighted = None
        self.currSelected = None
        self.drawOrigMap()
        self.mousePos = pygame.mouse.get_pos()
        self.createRegions()
        self.placeChars()
        self.placeStructures()
        self.checkForStructureOwnership(True)
        
        self.pendingBattle = None
        self.pause = [False, False]
        self.keys = [False, False, False, False, False, False]
        self.currentFrameOrder = None
        self.countdown = countdown.Countdown(MAP_COUNTDOWN_LENGTH)

        if SHOW_TRIGGER_AREA:
            self.setTriggerAreas()

        self.encounterPause = -1
        self.encounterPauseTick = 0

        self.charBarSideRight = True

        self.setCountdown()

        self.buildInterface()

        self.initialCount = 5

        for c in self.characters:
            self.checkTerrain(c)
            self.checkTerritory(c)
        

    def update(self):
        if self.countdown.isGoing():
            if (not self.pause[0]) and (not self.pause[1]):
                self.countdown.setTime(0)
        self.countdown.update()

        if self.countdown.checkStartFlag():
            self.pause = [False, False]
        
        self.currentFrameOrder = None

        self.updateEncounterPause()
        
        self.checkForBattle()

        if self.runCharacters():
            self.checkForStructureOwnership()
            self.addSuperEnergy()
            self.addRespawn()

        self.mousePos = pygame.mouse.get_pos()
        if self.encounterPause == -1:
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

        if self.runCharacters():
            for c in self.characters:
                self.checkBounds(c)
                self.checkTerrain(c)
                self.checkTerritory(c)
                c.update()

        if self.initialCount > 0:
            self.initialCount -= 1
            self.centerOnCharacter(self.charactersInTeams[self.team][0])    

    def runCharacters(self):
        return ( (self.pendingBattle is None) and (not self.paused()) and
                 (self.encounterPause == -1) )
        
    def zoom(self):
        self.drawZoomMap()
        self.adjustMap()
        if SHOW_TRIGGER_AREA:
            self.setTriggerAreas()
            

    def drawOrigMap(self):
        
        self.mapOrigImage = gamemap.drawMap(self.map)
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
            
        if (self.keys[4] and not self.keys[5]):
            self.scrollIn()
        elif (self.keys[5] and not self.keys[4]):
            self.scrollOut()
            
        

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
                    c.respawnPoint = spot
                    count += 1

    def placeStructures(self):
        self.structures = []

        for s in self.map.structures:
            sType = s[1]
            result = None

            if sType == "F":
                result = mapstructure.Fortress(s[0])
            elif sType == "S":
                result = mapstructure.Spire(s[0])

            if not result is None:
                self.structures.append(result)

    def leftClick(self):
        if self.encounterPause == -1:
            if isinstance(self.currHighlighted, mapchar.MapChar):
                if (self.currHighlighted.team == self.team and
                    not self.currHighlighted.isDead()):
                    self.currSelected = self.currHighlighted
                    return

            self.currSelected = None

    def rightClick(self, waypoint):
        if self.encounterPause == -1:
            if (not self.currSelected is None):
                pos = self.absMousePos()
                
                if self.currSelected.isDead() and (not self.isInTerritory(pos, self.currSelected.team)):
                    return
                
                pos = [int(pos[0]), int(pos[1])]
                self.currSelected.setTarget(pos, waypoint)
                self.currentFrameOrder = [self.currSelected, pos, waypoint]

    def absMousePos(self):
        temp = []
        for i in range(2):
            temp.append(round(
                (self.mousePos[i] - self.mapRect.topleft[i]) / self.zoomVal, 3))

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

        #Confirm current region
        c.resetRegion()
        if c.region is None:
            for r in self.regions:
                dist = util.distance(c.precisePos, r.pos)
                if dist <= MAP_REGION_SIZE:
                    c.region = r
                    break

        #Check for Fortress
        for i in self.structures:
            sTeam = i.team
            cTeam = c.team + 1
            if isinstance(i, mapstructure.Fortress) and (sTeam == cTeam):
                dist = util.distance(c.precisePos, i.precisePos)
                if (dist <= i.triggerSize):
                    c.currTerrain = FORTRESS
                    return
                 
        #Check all terrain circles in current region
        for i in c.region.terrainMasterList:
            circle = i[0]
            terrainType = i[1]
            dist = util.distance(c.precisePos, circle[0])
            if dist <= circle[1]:
                c.currTerrain = terrainType
                return

        c.currTerrain = PLAINS

    def checkTerritory(self, c):
        c.currTerritory = "neutral"
        for s in self.structures:
            if s.team == 0:
                continue
            
            dist = util.distance(c.precisePos, s.precisePos)
            if dist <= s.territorySize:
                sTeam = s.team
                cTeam = c.team + 1
                if sTeam == cTeam:
                    if c.currTerritory == "enemy":
                        c.currTerritory = "contested"
                    else:
                        c.currTerritory = "allied"
                else:
                    if c.currTerritory == "allied":
                        c.currTerritory = "contested"
                    else:
                        c.currTerritory = "enemy"
                        
    
    def isInTerritory(self, pos, team):
        cTeam = team + 1
        for s in self.structures:
            sTeam = s.team
            if sTeam == cTeam:
                dist = util.distance(pos, s.precisePos)
                if dist <= s.territorySize:
                    return True
                
        return False
                
                    
            
            

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


    def setTriggerAreas(self):
        for c in self.characters:
            c.createTriggerArea(self.zoomVal)

        for s in self.structures:
            s.createTriggerArea(self.zoomVal)

    def checkForBattle(self):
        if self.encounterPause != -1 or self.encounterPause != -1:
            return
        
        self.pendingBattle = None
        for c in self.charactersInTeams[0]:
            if c.isDead():
                continue
            for d in self.charactersInTeams[1]:
                if d.isDead():
                    continue
                dist = util.distance(c.precisePos, d.precisePos)
                if dist <= BATTLE_TRIGGER_RANGE:
                    self.pendingBattle = [c, d]
                    self.encounterPause = 0
                    return

    def checkForStructureOwnership(self, first=False):
        for s in self.structures:
            s.emptyPlayerList()
        
        for t, team in enumerate(self.charactersInTeams):
            for c in team:
                if c.isDead():
                    continue

                for s in self.structures:
                    dist = util.distance(c.precisePos, s.precisePos)
                    if dist <= STRUCTURE_TRIGGER_RANGE:
                        s.playersInArea[t].append(c)


        checker = False
        for s in self.structures:
            if (s.checkForOwnershipChange(first)):
                checker = True


        if checker:
            self.recreateTerritory()
            
            for c in self.characters:
                if c.isDead():
                    if not c.target is None:
                        if not self.isInTerritory(c.target, c.team):
                            c.target = None


    def recreateTerritory(self):
        for s in self.structures:
            if (s.team != 0):
                self.createTerritoryForStructure(s)


    def createTerritoryForStructure(self, s):
        s.territoryPoints = []
        
        for i in range(360 / TERRITORY_DEGREES_PER_DOT):
            deg = TERRITORY_DEGREES_PER_DOT * i
            pos = degreesToPoint(deg, s.territorySize, s.precisePos)

            checker = True
            contested = False
            for t in self.structures:
                if (s == t) or t.team == 0:
                    continue
                
                if s.team == t.team:
                    if util.distance(t.precisePos, pos) <= t.territorySize:
                        checker = False
                        break
                else:
                   if util.distance(t.precisePos, pos) <= t.territorySize:
                       contested = True

            if checker:
                s.territoryPoints.append([pos, contested])

    def addSuperEnergy(self):
        for team in range(2):
            total = 0
            
            for s in self.structures:
                if (isinstance(s, mapstructure.Spire)
                    and team+1 == s.team):
                    total += 1

            if total == 0:
                continue

            gain = getSuperEnergyGain(total)
            
            for c in self.charactersInTeams[team]:
                if not c.isDead():
                    c.addSuperEnergy(gain)


    def addRespawn(self):
        for c in self.characters:
            if c.isDead():
                c.respawnTime.add(RESPAWN_GAIN)
                if c.respawnTime.isMax() and (not c.target is None):
                    c.revive()
            
                

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
                    self.pendingBattle[i].addToPos[j] += retreat[j]

    def paused(self):
        return (self.pause[0] or self.pause[1])

    def pausePressed(self):
        if self.countdown.isGoing():
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
        
        self.waypointMarkers = []
        for i in range(MAX_WAYPOINTS):
            self.waypointMarkers.append(targetmarker.TargetMarker(True))

    def updateInterface(self):
        self.updatePausePlayIcons()
        updateSide = self.checkCharBarSide()
        for i in self.charBars:
            i.update()
            i.setActive(i.character is self.currSelected)
            i.setAlphaFade(self.isHighlightedOrSelected(i.character))

            if updateSide:
                if self.charBarSideRight:
                    i.rect.right = SCREEN_SIZE[0] - MAP_CHAR_BAR_INIT_POS[0]
                else:
                    i.rect.left = MAP_CHAR_BAR_INIT_POS[0]

    def checkCharBarSide(self):

        fraction = SCREEN_SIZE[0] / MAP_CHAR_BAR_SIDE_FRACTION

        newSideRight = None
        if self.mousePos[0] <= fraction:
            newSideRight = True
        elif self.mousePos[0] >= (fraction * (MAP_CHAR_BAR_SIDE_FRACTION-1)):
            newSideRight = False

        if newSideRight is None:
            return False

        if newSideRight == self.charBarSideRight:
            return False

        self.charBarSideRight = newSideRight

        return True

        

    def updatePausePlayIcons(self):
        self.bigPausePlayIcon.update(self.paused())
        self.bigPausePlayIcon.setAlphaFade(self.paused())

        for i in range(2):
            self.littlePausePlayIcons[i].update(self.pause[i])
            self.littlePausePlayIcons[i].setAlphaFade(self.paused())

    def isHighlightedOrSelected(self, i):
        return ((i is self.currHighlighted) or (i is self.currSelected))

    def numberKey(self, k):
        try:
            k = int(k)
        except:
            k = 0

        if self.encounterPause != -1:
            return

        k -= 1

        if (k >= 0) and (k < len(self.charactersInTeams[self.team])):
            if ( (self.currSelected is self.charactersInTeams[self.team][k]) and
                 (not self.charactersInTeams[self.team][k].isDead()) ):
                self.centerOnCharacter(self.currSelected)
            else:
                self.currSelected = self.charactersInTeams[self.team][k]

    def key(self, k, t):
        self.keys[k] = t


    def setCountdown(self, t=0):
        self.pause = [True, True]
        if t == 0:
            time = MAP_COUNTDOWN_LENGTH
        else:
            time = ENCOUNTER_COUNTDOWN_LENGTH
        self.countdown.setTime(time)

    def netMessageSize(self):
        return MAP_MODE_NET_MESSAGE_SIZE

##    def buildNetMessage(self):
##        if self.pause[self.team]:
##            msg = "p#"
##        else:
##            msg = "n#"
##
##        if not self.currentFrameOrder is None:
##            charNum = None
##            for i, c in enumerate(self.charactersInTeams[self.team]):
##                if c is self.currentFrameOrder[0]:
##                    charNum = i
##                    break
##
##            if charNum is None:
##                raise Exception()
##
##            msg = msg + str(charNum) + "#"
##            msg = (msg + str(self.currentFrameOrder[1][0]) + "#" +
##                   str(self.currentFrameOrder[1][1]) + "#")
##
##        size = len(msg)
##
##        if size > MAP_MODE_NET_MESSAGE_SIZE:
##            print msg
##            raise Exception()
##
##        add = MAP_MODE_NET_MESSAGE_SIZE - size
##
##        for i in range(add):
##            msg = msg + "-"
##
##        return msg

    def buildNetMessage(self):
        if self.pause[self.team]:
            pauseBit = 1
        else:
            pauseBit = 0
            
        xBytes = [chr(0), chr(0)]
        yBytes = [chr(0), chr(0)]
        specialByte = chr(pauseBit)

        if not self.currentFrameOrder is None:
            xBytes[0], xBytes[1] = convertIntToTwoASCII(self.currentFrameOrder[1][0])
            yBytes[0], yBytes[1] = convertIntToTwoASCII(self.currentFrameOrder[1][1])

            charNum = None
            for i, c in enumerate(self.charactersInTeams[self.team]):
                if c is self.currentFrameOrder[0]:
                    charNum = i
                    break

            if charNum is None:
                raise Exception()
            
            if self.currentFrameOrder[2]:
                waypoint = "1"
            else:
                waypoint = "0"

            specialByte = chr(int("0" + waypoint + convertIntToBinary(charNum, 4) +
                              "1" + str(pauseBit), 2))



        msg = xBytes[0] + xBytes[1] + yBytes[0] + yBytes[1] + specialByte

        return msg      


##    def parseNetMessage(self, msg, p):
##        p = p-1
##        
##        vals = msg.split('#')
##
##        pause = (vals[0] == "p")
##        self.pause[p] = pause
##
##        if len(vals) > 2:
##            charNum = int(vals[1])
##            x = float(vals[2])
##            y = float(vals[3])
##
##            self.charactersInTeams[p][charNum].startMovement((x, y))


    def parseNetMessage(self, msg, p):
        p = p-1

        msgC = list(msg)

        xBytes = [msgC[0], msgC[1]]
        yBytes = [msgC[2], msgC[3]]
        specialByte = msgC[4]

        xVal = (ord(xBytes[0]) * 256) + ord(xBytes[1])
        yVal = (ord(yBytes[0]) * 256) + ord(yBytes[1])

        specialString = convertIntToBinary(ord(specialByte), 8)

        waypointNum = int(specialString[1:2], 2)
        charNum = int(specialString[2:6], 2)
        moveNum = int(specialString[6:7], 2)
        pauseNum = int(specialString[7:8], 2)

        waypoint = (waypointNum == 1)

        self.pause[p] = (pauseNum == 1)

        if (moveNum == 1):
            self.charactersInTeams[p][charNum].setTarget((xVal, yVal), waypoint)
        

    def getBattleData(self):
        data = []

        chars = []
        for i in self.pendingBattle:
            chars.append(i.battleChar)

        data.append(chars)

        return data

    def startBattle(self):
        if self.encounterPause == 4:
            self.encounterPause += 1
            for c in self.characters:
                c.blinkOn = True
                c.blinkTick = 0
            return True
        else:
            return False

    def updateEncounterPause(self):
        if self.encounterPause != -1:

            if self.encounterPause == 1:
                self.zoomToEncounter()

            if self.encounterPause == 2:
                self.blinkEncounter()

            if self.encounterPause == 6:
                self.backOffEncounter()

            self.encounterPauseTick += 1
            if self.encounterPauseTick >= MAP_PAUSE_TIME_LENGTHS[self.encounterPause]:
                self.encounterPauseTick = 0
                self.encounterPause += 1
                if self.encounterPause >= len(MAP_PAUSE_TIME_LENGTHS):
                    self.encounterPause = -1
                    self.setCountdown(1)
                elif self.encounterPause == 7:
                    self.backOffEncounterFinal()

    def blinkEncounter(self):
        for c in self.pendingBattle:
            c.blinkTick += 1
            if c.blinkTick == ENCOUNTER_START_BLINK:
                c.blinkTick = 0
                c.blinkOn = not c.blinkOn

    def backOffEncounter(self):
        for c in self.characters:
            for i in range(2):
                if c.addToPos[i] != 0:
                    temp = c.addToPos[i] / 10
                    c.addToPos[i] -= temp
                    c.precisePos[i] += temp
            if c.isDead():
                c.blinkTick += 1
                if c.blinkTick == ENCOUNTER_END_BLINK:
                    c.blinkTick = 0
                    c.blinkOn = not c.blinkOn

    def backOffEncounterFinal(self):
        for c in self.characters:
            c.blinkOn = True
            c.blinkTick = 0
            if c.isDead():
                c.removed = True
                c.battleChar.superEnergy.change(0)
                if c == self.currSelected:
                    self.currSelected = None
            for i in range(2):
                if c.addToPos[i] != 0:
                    c.precisePos[i] += c.addToPos[i]
                    c.addToPos[i] = 0

    def zoomToEncounter(self):
        pos1 = self.mapRect.center
        
        encPos = self.getEncounterCenter()

        self.mapRect.topleft = add_points(self.mapRect.topleft, encPos)
        self.adjustMap()

        pos2 = self.mapRect.center

        self.mapRect.center = pos1
        self.adjustMap()

        dist = sub_points(pos1, pos2)
        scaled = scale_point(dist, 6)

        self.mapRect.center = sub_points(self.mapRect.center, scaled)
        self.adjustMap()


    def getEncounterCenter(self):
        newLoc = [0, 0]
        c = self.pendingBattle[self.team]
        for i in range(2):
            newLoc[i] = -(int(c.tokenRect.center[i])) + (SCREEN_SIZE[i] / 2)

        return newLoc

    def centerOnCharacter(self, c):
        newLoc = [0, 0]
        for i in range(2):
            newLoc[i] = -(int(c.tokenRect.center[i])) + (SCREEN_SIZE[i] / 2)

        self.mapRect.topleft = add_points(self.mapRect.topleft, newLoc)
        self.adjustMap()

    def createRegions(self):
        self.regions = []
        for rx in range(0, self.map.mapSize[0], MAP_REGION_SIZE):
            for ry in range(0, self.map.mapSize[1], MAP_REGION_SIZE):
                r = MapRegion((rx * 1.0, ry * 1.0))
                self.regions.append(r)

                for t in [(self.map.mountains, "m"), (self.map.water, "w"),
                          (self.map.forests, "f"), (self.map.islands, "i"),
                          (self.map.rivers, "r")]:
                    for i in t[0]:
                        terrPos = i[0]
                        terrRadius = i[1]
                        if (util.distance(terrPos, r.pos) <=
                            MAP_REGION_SIZE + terrRadius):
                            r.append(i, t[1])

                r.createTerrainMasterList()
                

class MapRegion(object):
    def __init__ (self, pos):
        
        self.pos = pos
        
        self.mountains = []
        self.water = []
        self.forests = []
        self.islands = []
        self.rivers = []

    def append(self, i, c):

        
        if (c == "m"):
            l = self.mountains
        elif (c == "w"):
            l = self.water
        elif (c == "f"):
            l = self.forests
        elif (c == "i"):
            l = self.islands
        elif (c == "r"):
            l = self.rivers

        l.append(i)

    def createTerrainMasterList(self):
        self.terrainMasterList = []

        orderToAdd = [[self.rivers, WATER], [self.forests, FOREST],
                      [self.mountains, MOUNTAIN], [self.islands, PLAINS],
                      [self.water, WATER]]

        for o in orderToAdd:
            for i in range(len(o[0])):
                self.terrainMasterList.append([o[0][i], o[1]])

    def printList(self):
        print "Region at (" + str(self.pos[0]) + ", " + str(self.pos[1]) + "):"

        for t in [(self.mountains, "Mountains:"),
                  (self.water, "Water:"),
                  (self.forests, "Forests:"),
                  (self.islands, "Islands:"),
                  (self.rivers, "Rivers:") ]:

            print t[1]

            for i in t[0]:
                print ("(" + str(i[0][0]) + ", " + str(i[0][1]) + "), " +
                       str(i[1]))
        


def ConvertBattleCharsToMapChars(hostChars, clientChars):
    masterList = [hostChars, clientChars]

    returnList = []
    for i, l in enumerate(masterList):
        for c in l:
            if isinstance(c, hare.Hare):
                mod = mapchar.Hare
            elif isinstance(c, fox.Fox):
                mod = mapchar.Fox
            elif isinstance(c, cat.Cat):
                mod = mapchar.Cat
            else:
                raise Exception()

            returnList.append(mod(i, c, c.name))

    return returnList
