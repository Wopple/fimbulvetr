import os
import sys
import copy
import math

from common.constants import *
from client.constants import *

from common import mvc
from common import process_m

from common import boundint
from common import countdown
from client import fx
from client import platform
from client import textrect

from client import colorswapper

from client import hare, fox, cat

from common.util.rect import Rect

class Model(process_m.ProcessModel):
    def __init__(self, stateQueue, inChars, terrainLeft, terrainRight):
        super(Model, self).__init__(resultQueue)
        self.stateQueue = stateQueue
        self.terrainLeft = terrainLeft
        self.terrainRight = terrainRight
        self.rect = Rect((0, 0), BATTLE_ARENA_SIZE)

        self.testBool = False
        self.testBool2 = False
        
        self.players = inChars
        for p in self.players:
            p.beginBattle()
            pos = (self.rect.centerx,
                   self.rect.height - BATTLE_AREA_FLOOR_HEIGHT)
            self.players[0].setLoc(add_points(pos,
                            ((-BATTLE_PLAYER_START_DISTANCE / 2), 0)))
            self.players[0].facingRight = True
            self.players[1].setLoc(add_points(pos,
                            ((BATTLE_PLAYER_START_DISTANCE / 2), 0)))
            self.players[1].facingRight = False
            
        self.keys = [[False, False, False, False, False, False, False, False, False],
                     [False, False, False, False, False, False, False, False, False]]
        self.keysNow = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.frameByFrame = [0, 0]
        
        self.returnCode = [0, 0]
        self.projectiles = []
        self.retreatProhibitTime = boundint.BoundInt(0, RETREAT_PROHIBIT_TIME,
                                                     RETREAT_PROHIBIT_TIME)
        self.retreatPhase = 0
        
        self.netPlayer = 0
        self.catBar = None
        self.createBars()
        self.resetHitMemory()

        self.endingVal = -1
        self.endingValTick = 0

        self.fx = []

        self.platforms = getPlatforms(terrainLeft, terrainRight)

        self.countdown = countdown.Countdown(BATTLE_COUNTDOWN_LENGTH)
        
        self.damageTagRects = []
        self.damagePercentRects = []
        for i in range(2):
            rect = Rect((0, 0), (80, 100))
            if (i == 0):
                rect.left = 0
            else:
                rect.right = SCREEN_SIZE[0]
            rect.top = SCREEN_SIZE[1] - 55
            self.damageTagRects.append(rect)
            
            rect2 = Rect((0, 0), (80, 100))
            if (i == 0):
                rect2.left = 0
            else:
                rect2.right = SCREEN_SIZE[0]
            rect2.top = rect.top + 18
            self.damagePercentRects.append(rect2)
            
        self.damageTag = textrect.render_textrect("Strength", STRUCTURE_COUNT_FONT, self.damageTagRects[0],
                                                  ALMOST_BLACK, BLACK, 1, True)
        
        

    def checkFrameByFrame(self):
        highest = 0

        for i in range(len(self.frameByFrame)):
            if self.frameByFrame[i] > highest:
                highest = self.frameByFrame[i]
            if self.frameByFrame[i] == 2:
                self.frameByFrame[i] = 1

        return (highest == 1)

    def update(self):
        #if self.testBool:
        #    self.keys[1][1] = True
        #    self.keysNow[1][1] = 3
        #else:
        #    self.keys[1][1] = False
        #    self.keysNow[1][1] = 0
        #if self.testBool2:
        #    self.keys[1][7] = True
        #    self.keysNow[1][7] = 3
        #else:
        #    self.keys[1][7] = False
        #    self.keysNow[1][7] = 0
        
        #self.keys[1][7] = True
        #self.keysNow[1][7] = 0

        fbf = self.checkFrameByFrame()

        if not fbf:

            self.checkEnding()

            if self.endingVal >= 0:
                self.endingValTick += 1
                if self.endingValTick >= BATTLE_ENDING_TIME_LENGTHS[self.endingVal]:
                    self.endingValTick = 0
                    self.endingVal += 1
                    if self.endingVal == len(BATTLE_ENDING_TIME_LENGTHS):
                        self.advanceNow = True
            
            self.countdown.update()

            if self.countdown.checkStartFlag():
                for p in self.players:
                    p.countdownComplete()
                self.retreatPhase = 1
                
            isFlash = self.isFlash()

            if self.retreatPhase == 1 and self.endingVal == -1 and not isFlash:
                self.retreatProhibitTime.add(-1)
                if self.retreatProhibitTime.value == 0:
                    self.retreatPhase = 2
                    self.retreatBar.createText("Retreat", 1)
                    self.retreatBar.value.maximum = RETREAT_HOLD_TOTAL
                    self.retreatBar.threshold = self.retreatBar.value.maximum + 1

            

            
            for i, p in enumerate(self.players):

                if (isFlash) and (not p.currMove.isSuperFlash):
                    continue
                
                if self.countdown.isGoing() or self.returnCode[i] == 1:
                    keys = [False, False, False, False, False, False, False, False, False]
                    keysNow = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    keys = self.keys[i]
                    keysNow = self.keysNow[i]

                if keys[7] and (keysNow[7] == KEY_BUFFER):
                    if p.techBuffer == TECH_BUFFER_MIN:
                        p.techBuffer = TECH_BUFFER_MAX
                    
                l, r = self.exclusiveKeys(keys[2], keys[3])
                self.resetKeysNow(keysNow)
                self.act(p, keys, keysNow)
                self.checkReversable(l, r, p)
                self.checkForGround(i, p)
                self.checkForEdge(l, r, p, isFlash)
                if self.returnCode[i] != 0:
                    p.retreat.value = 0
                self.checkForFX(i, p)
                if not p.dropThroughPlatform is None:
                    p.dropThroughPlatform = self.checkForPlatform(p)

            if (not isFlash):
                self.checkRetreat()
                self.resetHitMemory()
                
                self.updateProjectiles()

                self.checkForBlock()
                self.checkForProjectileBlock()
                for i, p in enumerate(self.players):
                    if self.returnCode[i] != 1:
                        self.actOnBlock(i, p)
                
                self.checkForHits()
                self.checkForProjectileHit()
                for i, p in enumerate(self.players):
                    if self.returnCode[i] != 1:
                        self.actOnHit(i, p)

                self.checkGrabPair()

            for i, p in enumerate(self.players):
                if (isFlash) and (not p.currMove.isSuperFlash):
                    continue
                
                keys = self.keys[i]
                keysNow = self.keysNow[i]
                l, r = self.exclusiveKeys(keys[2], keys[3])
                p.update()
                self.checkShoot(p)
                p.DI(l, r)

            if not isFlash:
                self.checkDisplacement()
                self.centerCamera(self.players[self.cameraPlayer])

            for f in self.fx:
                f.update()
            newList = []
            for i in range(len(self.fx)):
                if not self.fx[i].removeFlag:
                    newList.append(self.fx[i])
            self.fx = newList

        for b in self.bars:
            if not self.catBar is None:
                self.updateCatBarColors()
            b.update()
            
            
    def updateProjectiles(self):
        temp = []
        for i in range(len(self.projectiles)):
            self.projectiles[i].update()
            self.checkProjForEdge(self.projectiles[i])
            self.checkProjForDissolve(self.projectiles[i])
            if not self.projectiles[i].destroy:
                temp.append(self.projectiles[i])
        self.projectiles = temp

    def resetKeysNow(self, keysNow):
        for k in range(len(keysNow)):
            if keysNow[k] > 0:
                keysNow[k] -= 1

    def wasKeyPressed(self, k, keysNow):
        if k == -1:
            return ((keysNow[2] > 0) or (keysNow[3] > 0))
        else:
            return (keysNow[k] > 0)

    def exclusiveKeys(self, k1, k2):
        if k1 and k2:
            k1 = False
            k2 = False
        return k1, k2

    def keyTowardFacing(self, p, keys):
        l, r = self.exclusiveKeys(keys[2], keys[3])
        return p.keyTowardFacing(l, r)

    def centerCamera(self, target):
        self.rect.left = -(int(target.preciseLoc[0]) - (SCREEN_SIZE[0] / 2))
        self.rect.top = -(int(target.preciseLoc[1]) - (SCREEN_SIZE[1] / 2))

        if self.rect.left > 0:
            self.rect.left = 0
        if self.rect.right < SCREEN_SIZE[0]:
            self.rect.right = SCREEN_SIZE[0]

        if self.rect.top > 0:
            self.rect.top = 0
        if self.rect.bottom < SCREEN_SIZE[1]:
            self.rect.bottom = SCREEN_SIZE[1]

    def act(self, p, keys, keysNow):
        p.actLeft = True
        u, d = self.exclusiveKeys(keys[0], keys[1])
        l, r = self.exclusiveKeys(keys[2], keys[3])

        if p.hp.value <= 0 and not p.currMove.isDead:
            p.setCurrMove('deadFalling')
            p.inAir = True
            return
        
        if not self.keyTowardFacing(p, keys):
            p.actTransition('noXMove')
        if p.holdJump:
            if p.vel[1] > 0 or (not keys[6]):
                p.unholdJump()
        if p.onHitTrigger:
            p.actTransition('onHit')
        if p.techBuffer >= 0 and p.canTech:
            if p.actTransition('tech'):
                p.techBuffer = TECH_BUFFER_MIN
        if p.canAct():
            if d:
                p.actTransition('doDuck')
            if l or r:
                if (l and self.wasKeyPressed(2, keysNow)):
                    keysNow[2] = 0
                    if (p.dashBuffer[0] > 0 and p.dashBuffer[0] < DASH_BUFFER_MAX):
                        if p.actTransitionFacing('doDash', l, r):
                            p.dashBuffer = [0, 0]
                    else:
                        p.dashBuffer[0] = DASH_BUFFER_MAX
                        p.dashBuffer[1] = 0
                        
                if (r and self.wasKeyPressed(3, keysNow)):
                    keysNow[3] = 0
                    if (p.dashBuffer[1] > 0 and p.dashBuffer[1] < DASH_BUFFER_MAX):
                        if p.actTransitionFacing('doDash', l, r):
                            p.dashBuffer = [0, 0]
                    else:
                        p.dashBuffer[1] = DASH_BUFFER_MAX
                        p.dashBuffer[0] = 0
                        
                p.actTransitionFacing('doWalk', l, r)
                if l:
                    if p.facingRight:
                        p.actTransition('backward')
                    else:
                        p.actTransition('forward')
                elif r:
                    if p.facingRight:
                        p.actTransition('forward')
                    else:
                        p.actTransition('backward')
            if u:
                p.actTransition('up')
            if not d:
                p.actTransition('stopDuck')
            if self.wasKeyPressed(4, keysNow):
                if u:
                    if p.actTransition('attackAUp'):
                        keysNow[4] = 0
                elif d:
                    if p.actTransition('attackADown'):
                        keysNow[4] = 0
                else:
                    if p.actTransition('attackA'):
                        keysNow[4] = 0
            if self.wasKeyPressed(5, keysNow):
                if u:
                    if p.actTransition('attackBUp'):
                        keysNow[5] = 0
                    elif p.aerialCharge:
                        if p.actTransition('attackBUpCharge'):
                            keysNow[5] = 0
                            p.aerialCharge = False
                        
                elif d:
                    if p.actTransition('attackBDown'):
                        keysNow[5] = 0
                    elif p.aerialCharge:
                        if p.actTransition('attackBDownCharge'):
                            keysNow[5] = 0
                            p.aerialCharge = False
                            
                else:
                    if p.actTransition('attackB'):
                        keysNow[4] = 0
            if self.wasKeyPressed(6, keysNow):
                if not self.checkForPlatform(p) is None:
                    if p.actTransition('dropThrough'):
                        self.dropThrough(p)
                if p.actTransitionFacing('jump', l, r):
                    keysNow[6] = 0
            if keys[7]:
                if d:
                    if p.actTransition('downBlock'):
                        keysNow[7] = 0
                else:
                    if p.actTransition('block'):
                        keysNow[7] = 0
            if self.wasKeyPressed(8, keysNow):
                if p.superEnergy.isMax() and self.endingVal == -1:
                    if p.actTransition('super'):
                        keysNow[8] = 0
                        p.superEnergy.setToMin()
                        
            if not keys[4]:
                p.actTransition('releaseA')
            if not keys[5]:
                p.actTransition('releaseB')
            if not keys[7]:
                p.actTransition('releaseBlock')

            lev = p.getCatEnergyLevel()
            if lev == 1:
                p.actTransition('bladelv1')
            if lev == 2:
                p.actTransition('bladelv2')
            if lev == 3:
                p.actTransition('bladelv3')

    def checkReversable(self, l, r, p):
        if p.currFrame == 0 and p.currSubframe == 1:
            if p.currMove.reversable:
                if l:
                    p.facingRight = False
                if r:
                    p.facingRight = True

    def checkForGround(self, i, c):
        old = c.inAir
        landed = False
        p = self.checkForPlatform(c)
        if p == c.dropThroughPlatform:
            p = None
        if (c.preciseLoc[1] >= self.rect.height - BATTLE_AREA_FLOOR_HEIGHT):
            c.preciseLoc[1] = self.rect.height - BATTLE_AREA_FLOOR_HEIGHT
            landed = True
        elif (not p is None):
            landed = True
            c.preciseLoc[1] = p.rect.top

        if landed:
            if (c.vel[1] > 0):
                c.inAir = False
                c.vel[1] = 0.0
                c.aerialCharge = True
                if old and (not c.currMove.ignoreGroundAir):
                    c.transToGround()
                    self.createTransitionDust(i, c)
        else:
            c.inAir = True
            if not old and (not c.currMove.ignoreGroundAir):
                c.transToAir()

    def dropThrough(self, p):
        p.dropThroughPlatform = self.checkForPlatform(p)

    def checkForPlatform(self, c):
        if c.vel[1] < 0:
            return None
        
        for p in self.platforms:
            if p.rect.colliderect(c.footRect):
                return p
        return None
    
    def checkDisplacement(self):
        
        for i in range(2):
            m = self.players[i].currMove
            if (not m.grabPos is None) or (m.grabVal != 0) or (m.isDead) or (m.isOnGround) or (self.returnCode[i] == 1):
                return
        
        if self.players[0].footRect.colliderect(self.players[1].footRect):
            if (self.players[0].footRect.left <= self.players[1].footRect.left):
                displace = [-1, 1]
            else:
                displace = [1, -1]
                
            for i in range(2):
                self.players[i].preciseLoc[0] += DISPLACEMENT_AMOUNT * displace[i]
            

    def checkForEdge(self, l, r, p, isFlash):
        check = False
        if p.preciseLoc[0] < BATTLE_EDGE_COLLISION_WIDTH:
            p.preciseLoc[0] = BATTLE_EDGE_COLLISION_WIDTH
            check = True
        if p.preciseLoc[0] > self.rect.width - BATTLE_EDGE_COLLISION_WIDTH:
            p.preciseLoc[0] = self.rect.width - BATTLE_EDGE_COLLISION_WIDTH
            check = True

        if not p.currMove.canRetreat:
            check = False
            

        if p.currMove.isDead:
            p.retreat.value = 0
        elif self.retreatPhase == 2 and not isFlash:
            if self.endingVal in [-1, 0, 1]: 
                if check:
                    if self.endingVal == -1:
                        amount = RETREAT_ADD
                    else:
                        amount = RETREAT_ADD_FAST
                    p.retreat.add(amount)
                else:
                    p.retreat.add(-RETREAT_RECEED)
            else:
                p.retreat.add(-RETREAT_RECEED_FAST)

    def checkRetreat(self):
        high = 0
        highestP = None
        for i, p in enumerate(self.players):
            if p.retreat.value > high:
                high = p.retreat.value
                highestP = i

        if high > 0:
            self.retreatBar.changeColor(RETREAT_TEAM_COLORS[highestP])
            self.retreatBar.value = self.players[highestP].retreat
            
    def checkShoot(self, p):
        m = p.currMove
        for s in m.shoot:
            if s[0] == p.currFrame and p.canShoot:
                proj = copy.copy(p.projectiles[s[1]].copySelf())
                proj.shooter = p
                p.canShoot = False
                

                poffset = s[2]
                temp = p.preciseLoc
                y = temp[1] + poffset[1]

                if p.facingRight:
                    x = temp[0] + poffset[0]
                else:
                    x = temp[0] - poffset[0]

                proj.facingRight = p.facingRight
                
                proj.preciseLoc = [x, y]
                self.projectiles.append(proj)
                

    def testKey(self, k):
        p = self.players[self.cameraPlayer]
        
        #xVel = -10;
        #if (not p.facingRight):
        #    xVel *= -1
        #p.getHit(5, 150, [xVel, -8])

        #self.players[0].superEnergy.add(self.players[0].superEnergy.maximum / 5)


    def checkProjForEdge(self, p):
        if ( (p.preciseLoc[0] < (0 - PROJECTILE_SCREEN_ALLOWANCE))
             or (p.preciseLoc[0] > (self.rect.width + PROJECTILE_SCREEN_ALLOWANCE))
             or (p.preciseLoc[1] < (0 - PROJECTILE_SCREEN_ALLOWANCE))
             or (p.preciseLoc[1] > (self.rect.height + PROJECTILE_SCREEN_ALLOWANCE)) ):
            p.destroy = True

    def checkProjForDissolve(self, p):
        if (p.dissolveOnPhysical) and (not p.isEndingAnimation()):
            if p.preciseLoc[1] >= self.rect.height - BATTLE_AREA_FLOOR_HEIGHT:
                p.liveTime = 0
        if (p.hitsRemaining <= 0):
            p.liveTime = 0
                
        if (p.isEndingAnimation()) and (p.currFrame == len(p.currMove.frames)-1):
            p.destroy = True
            p.currFrame = 0

    def setNetPlayer(self, p):
        self.netPlayer = p

##    def buildNetMessage(self):
##        p = self.netPlayer - 1
##        msg = ''
##        for i in self.keys[p]:
##            if i:
##                j = '1'
##            else:
##                j = '0'
##            msg += j
##        for i in self.keysNow[p]:
##            msg += str(i)
##
##        msg += str(self.frameByFrame[p])
##
##        return msg

    def buildNetMessage(self):

        keys = self.keys[self.netPlayer-1]
        keysNow = self.keysNow[self.netPlayer-1]

        byte1S = ""
        for k in keys[0:8]:
            if k:
                byte1S += "1"
            else:
                byte1S += "0"
        byte1 = chr(int(byte1S, 2))

        msg = byte1
        moreBytes = ""
        for i in range(4):
            byteS = ""
            for j in range(2):
                byteS += convertIntToBinary(keysNow[i + (j*4)], 4)
                
            byte = chr(int(byteS, 2))

            msg += byte
            
        if keys[8]:
            superByte = "0001"
        else:
            superByte = "0000"
        superByte += convertIntToBinary(keysNow[8], 4)
        
        msg += chr(int(superByte, 2))
        
        

        checksum = self.getChecksum()
        msg += checksum

        return msg


    def parseNetMessage(self, msg, p):
        if p == 0:
            return

        #print msg

        msgC = list(msg)

        keysByte = convertIntToBinary(ord(msgC[0]), 8)

        for i in range(8):
            self.keys[p-1][i] = (keysByte[i] == "1")

        for i in range(4):
            nowByte = convertIntToBinary(ord(msgC[i+1]), 8)

            for j in range(2):
                plus = 4 * j
                bits = nowByte[plus:4+plus]
                value = int(bits, 2)

                self.keysNow[p-1][i + (j*4)] = value
                
        superByte = convertIntToBinary(ord(msgC[5]), 8)
        self.keys[p-1][8] = (superByte[3] == "1")
        self.keysNow[p-1][8] = int(superByte[4:], 2)


        recvChecksum = ord(msgC[6])
        myChecksum = ord(self.getChecksum())

        if (recvChecksum != myChecksum):
            print "Checksums to not match!!"


        

##    def parseNetMessage(self, msg, p):
##        if p == 0:
##            return
##        else:
##            keys = self.keys[p-1]
##            keysNow = self.keysNow[p-1]
##            
##        msg1 = msg[0:8]
##        if len(msg1) != 8:
##            print "!"
##            print msg1
##            sys.exit()
##        msg2 = msg[8:16]
##        if len(msg2) != 8:
##            print "!!"
##            print msg2
##            sys.exit()
##        msg3 = msg[16:]
##        if len(msg3) != 1:
##            print "!!!"
##            print msg3
##            sys.exit()
##        
##        for i, c in enumerate(msg1):
##            if c == '1':
##                keys[i] = True
##            elif c == '0':
##                keys[i] = False
##            else:
##                print "Error in message parsing"
##                sys.exit()
##
##        for i, c in enumerate(msg2):
##            try:
##                keysNow[i] = int(c)
##            except:
##                print "Error in message parsing"
##                sys.exit()
##
##        if keys[7] and (keysNow[7] == KEY_BUFFER):
##            if self.players[p-1].techBuffer == TECH_BUFFER_MIN:
##                self.players[p-1].techBuffer = TECH_BUFFER_MAX
##
##        try:
##            self.frameByFrame[p-1] = int(msg3)
##        except:
##            print "Error in message parsing"
##            print "Message:", msg3
##            sys.exit()

    def getChecksum(self):
        tempsum = 0
        for p in self.players:
            for i in range(2):
                tempsum += int(p.preciseLoc[i])

        checksum = chr(tempsum % 256)

        return checksum

    def reverse01(self, val):
        if val == 0:
            return 1
        elif val == 1:
            return 0
        return val

    def updateCatBarColors(self):
        x = len(CAT_ENERGY_SECTIONS)
        for i in range(x):
            if self.catBar.value.value <= CAT_ENERGY_SECTIONS[i]:
                if self.catBar.fillColor is not CAT_ENERGY_BAR_COLORS[i]:
                    self.catBar.changeColor(CAT_ENERGY_BAR_COLORS[i])
                return
        self.catBar.changeColor(CAT_ENERGY_BAR_COLORS[x])
                                                 
    def resetHitMemory(self):
        self.hitMemory = [None, None]
        self.blockMemory = [None, None]
        self.fxMemory = [[], []]

    def checkGrabPair(self):
        for i in range(2):
            if i == 0:
                a = 0
                b = 1
            else:
                a = 1
                b = 0

            if not self.players[a].currMove.isThrow():
                if ( ((self.players[a].currMove.isGrab()) and (not self.players[b].currMove.isGrabbed()))
                     or ((not self.players[a].currMove.isGrab()) and (self.players[b].currMove.isGrabbed())) ):
                    self.players[a].setCurrMove('grabRelease')
                    self.players[b].setCurrMove('grabbedRelease')
                    return

            if self.players[a].currMove.isGrab() and self.players[b].currMove.isGrabbed():
                offset = self.getGrabOffset(self.players[a], self.players[b])
                
                self.players[a].preciseLoc = sub_points(self.players[b].preciseLoc, offset)
                self.players[b].preciseLoc = add_points(self.players[a].preciseLoc, offset)
                self.players[b].inAir = False

    def getGrabOffset(self, p1, p2):
        if p1.facingRight:
            mult = 1
        else:
            mult = -1

        offset = [ p1.currMove.grabPos[0] * mult,
                   p1.currMove.grabPos[1] ]

        temp = [ p2.currMove.grabPos[0] * (mult * -1),
                 p2.currMove.grabPos[1] ]

        return sub_points(offset, temp)
            

    def checkForBlock(self):
        offset = self.rect.topleft
        for i, p in enumerate(self.players):
            for j, q in enumerate(self.players):
                if (not q is p) and (p.attackCanHit):
                    for h in p.getHitboxes():
                        if h.ignoreBlock():
                            continue
                        for r in q.getBlockboxes():
                            hRect = p.getBoxRect(h)
                            rRect = q.getBoxRect(r)
                            
                            if hRect.colliderect(rRect):
                                if (self.blockMemory[j] is None):
                                    self.blockMemory[j] = [h, p]
                                    p.attackCanHit = False
                                    p.onHitTrigger = True

                                if q.currMove == q.moves['blocking']:
                                    ind = 0
                                elif q.currMove == q.moves['lowBlocking']:
                                    ind = 1
                                else:
                                    ind = 2

                                self.fxMemory[j].append(q.getBlockFXPoint(ind))
                                
                                

    def checkForHits(self):
        if self.blockMemory is None:
            self.fxMemory = [[], []]
        offset = self.rect.topleft
        for i, p in enumerate(self.players):
            for j, q in enumerate(self.players):
                if (not q is p) and (p.attackCanHit):
                    for h in p.getHitboxes():
                        for r in q.getHurtboxes():
                            hRect = p.getBoxRect(h)
                            rRect = q.getBoxRect(r)
                            if hRect.colliderect(rRect):
                                if q.blockstun > 0:
                                    if (self.blockMemory[j] is None):
                                        self.blockMemory[j] = [h, p]
                                        p.attackCanHit = False
                                        p.onHitTrigger = True
                                else:
                                    if (self.hitMemory[j] is None):
                                        self.hitMemory[j] = [h, p]
                                        p.attackCanHit = False
                                        p.onHitTrigger = True

                                self.fxMemory[j].append(average_points(
                                    hRect.center, rRect.center))
                 
                 
    def checkForProjectileBlock(self):
        for proj in self.projectiles:
            if not proj.canHit():
                return
        
            for j, q in enumerate(self.players):
                if (not q is proj.shooter):
                    for h in proj.getHitboxes():
                        if h.ignoreBlock():
                            continue
                        for r in q.getBlockboxes():
                            hRect = proj.getBoxRect(h)
                            rRect = q.getBoxRect(r)
                            if hRect.colliderect(rRect):
                                if (self.blockMemory[j] is None):
                                    self.blockMemory[j] = [h, proj]

                                if q.currMove == q.moves['blocking']:
                                    ind = 0
                                elif q.currMove == q.moves['lowBlocking']:
                                    ind = 1
                                else:
                                    ind = 2

                                self.fxMemory[j].append(q.getBlockFXPoint(ind))
    
    
    def checkForProjectileHit(self):
        for proj in self.projectiles:
            print proj.freezeFrame
            if not proj.canHit():
                continue
        
            for j, q in enumerate(self.players):
                if (not q is proj.shooter):
                    for h in proj.getHitboxes():
                        for r in q.getHurtboxes():
                            hRect = proj.getBoxRect(h)
                            rRect = q.getBoxRect(r)
                            if hRect.colliderect(rRect):
                                if (self.hitMemory[j] is None):
                                    self.hitMemory[j] = [h, proj]
                                
                                self.fxMemory[j].append(average_points(
                                    hRect.center, rRect.center))

                                

    def createFX(self, h, hitter, hittee, pointList, blocked):
        fxPos = average_point_list(pointList)

        if blocked:
            self.fx.append(fx.FX(fxPos, hitter.facingRight, 'block'))
        elif hitter.currMove.isGrab():
            self.fx.append(fx.FX(fxPos, hitter.facingRight, 'grab'))
        else:
            if not h.noStandardFX():
                self.fx.append(fx.FX(fxPos, hitter.facingRight, 'pow'))
                self.fx.append(fx.FX(fxPos, hitter.facingRight, 'side'))
        

    def actOnBlock(self, i, p):
        self.actOnHit(i, p, True)
            

    def actOnHit(self, i, p, blocked=False):
        if blocked:
            memory = self.blockMemory
        else:
            memory = self.hitMemory
        
        if not memory[i] is None:
            mem = memory[i][0]
            hitter = memory[i][1]

            p.facingRight = not hitter.facingRight

            grab = mem.getGrabData()
            if grab is not None:
                self.actOnGrab(i, p, mem, hitter, grab)
                return

            damage = int(mem.damage * hitter.getDamageMultiplier())
            chip = mem.chipDamagePercentage
            stun = mem.stun
            prop = mem.properties

            kb = mem.knockback
            if blocked:
                kb *= BLOCKED_KNOCKBACK_FACTOR

            xVel = math.cos(math.radians(mem.angle)) * kb
            yVel = math.sin(math.radians(mem.angle)) * kb

            if blocked:
                yVel *= BLOCKED_LIFT_RESIST

            yVel *= -1
            if p.facingRight:
                xVel *= -1

            if not p.inAir:
                if (mem.angle > 180) and (not blocked):
                    yVel *= -1

            if not blocked:
                p.getHit(damage, stun, (xVel, yVel))

            p.freezeFrame = mem.freezeFrame
            hitter.freezeFrame = mem.freezeFrame
            
            hitter.performHit()

            p.canTech = not mem.untechable()
            p.techBuffer = TECH_BUFFER_MIN

            if blocked:
                damage = int(damage * chip)
                p.getBlockstun(damage, stun, (xVel, yVel), prop)

            if mem.reverseUserFacing():
                hitter.facingRight = (not hitter.facingRight)

            if mem.reverseTargetFacing():
                p.facingRight = (not p.facingRight)

            self.createFX(mem, hitter, p, self.fxMemory[i], blocked)

    def actOnGrab(self, i, p, mem, hitter, grab):
        hitter.setCurrMove(grab[1])
        p.setCurrMove(grab[2])

        offset = self.getGrabOffset(hitter, p)
                
        p.preciseLoc = add_points(hitter.preciseLoc, offset)

        self.createFX(mem, hitter, p, self.fxMemory[i], False)

    def netMessageSize(self):
        return NET_MESSAGE_SIZE

    def checkForFX(self, i, p):
        if self.returnCode[i] != 1 and p.currSubframe == 0 and p.canEffect:
            for i in p.getCurrentFrame().fx:
                facing = i[2]
                basePos = [i[1][0], i[1][1]]
                if not p.facingRight:
                    facing = not facing
                    basePos[0] *= -1
                pos = add_points(p.preciseLoc, basePos)
                self.fx.append(fx.FX(pos, facing, i[0]))
                p.canEffect = False

    def createTransitionDust(self, i, p):
        if p.currMove == p.moves['groundHit'] or p.currMove.isStun or self.returnCode[i] == 1:
            return
        
        pos = add_points(p.preciseLoc, (0,0))
        self.fx.append(fx.FX(pos, True, 'dust'))
        self.fx.append(fx.FX(pos, False, 'dust'))

    def checkEnding(self):

        if self.endingVal in [-1, 0, 1]:
            for i, p in enumerate(self.players):
                if self.players[i].retreat.isMax():
                    self.returnCode[i] = 1
                    self.players[i].retreat.setToMin()
                    self.players[i].preciseLoc[1] = self.rect.height - BATTLE_AREA_FLOOR_HEIGHT
                    if self.endingVal == -1:
                        self.endingVal = 0

        
        if self.endingVal == -1:
            temp = False
            for p in self.players:
                if p.currMove.isDead:
                    temp = True
            if temp:
                self.endingVal = 0
                for proj in self.projectiles:
                    proj.freezeFrame += DEATH_FREEZE_FRAME
                for i, p in enumerate(self.players):
                    p.freezeFrame += DEATH_FREEZE_FRAME
                    if p.currMove.isDead:
                        if p.vel[1] > DEATH_FLY_VERT_VEL_MIN:
                            p.vel[1] = DEATH_FLY_VERT_VEL_MIN
                        self.returnCode[i] = -1
                    else:
                        self.returnCode[i] = 0
        
    def getDamagePercentText(self, i):
        if self.cameraPlayer == 1:
            if i == 0:
                i = 1
            else:
                i = 0
        c = self.players[i]
        return textrect.render_textrect(c.getDamagePercentText(), DAMAGE_PERCENT_FONT, self.damagePercentRects[i],
                                                 ALMOST_BLACK, BLACK, 1, True)
        
    def superDarken(self):
        for p in self.players:
            if p.currMove.isSuperFlash:
                return True
            
        return False

    def isFlash(self):
        for p in self.players:
            if p.currMove.isSuperFlash:
                return True

        return False
                

def testData():
    heroes = [hare.Hare(), hare.Hare()]
    
    for h in heroes:
        h.superEnergy.change(h.superEnergy.maximum)
    
    return [heroes, PLAINS, PLAINS]


def getPlatforms(leftTerrain, rightTerrain):
    
    platformsLeft = getPlatformsForSingleTerrain(leftTerrain, False)
    platformsRight = getPlatformsForSingleTerrain(rightTerrain, True)
    
    masterList = []
    for i in range(len(platformsLeft)):
        masterList.append(platformsLeft[i])
    for i in range(len(platformsRight)):
        masterList.append(platformsRight[i])
        
    return masterList
    
    
def getPlatformsForSingleTerrain(terrain, isRight):
    
    platforms = []
    
    HALF_SCREEN = (BATTLE_ARENA_SIZE[0] / 2)
    
    if terrain == PLAINS:
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 200, terrain ) )
    elif terrain == FOREST:
        platforms.append( platform.Platform(
            (100, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), 175, terrain ) )
        platforms.append( platform.Platform(
            (375, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 280), HALF_SCREEN - 350, terrain ) )
    elif terrain == MOUNTAIN:
        platforms.append( platform.Platform(
            (400, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 400, terrain ) )
        platforms.append( platform.Platform(
            (150, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 280), 140, terrain ) )
        platforms.append( platform.Platform(
            (400, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 380), HALF_SCREEN - 400, terrain ) )
        platforms.append( platform.Platform(
            (150, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 480), 140, terrain ) )
    elif terrain == SNOW:
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 200, terrain ) )
    elif terrain == FORTRESS:
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 200, terrain ) )
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 380), HALF_SCREEN - 200, terrain ) )
        
        
    if isRight:
        for p in platforms:
            p.rect.right = BATTLE_ARENA_SIZE[0] - p.rect.left
    
    return platforms
    
    
    
    
    
