import os
import sys
import pygame
import copy
import math

import mvc

import incint
import boundint
import energybar
import countdown

import hare, fox, cat

from constants import *

class Model(mvc.Model):
    def __init__(self, inChars, areaSize, bg):
        super(Model, self).__init__()
        self.background = bg
        self.rect = pygame.Rect((0, 0), areaSize)
        
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
            
        self.keys = [[False, False, False, False, False, False, False],
                     [False, False, False, False, False, False, False]]
        self.keysNow = [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]]
        self.returnCode = [0, 0]
        self.projectiles = []
        self.retreatProhibitTime = boundint.BoundInt(0, RETREAT_PROHIBIT_TIME,
                                                     RETREAT_PROHIBIT_TIME)
        self.retreatPhase = 0
        
        self.cameraPlayer = 0
        self.netPlayer = 0
        self.catBar = None
        self.createBars()
        self.resetHitMemory()

        self.countdown = countdown.Countdown(BATTLE_COUNTDOWN_LENGTH)

    def update(self):

        self.checkForEnd()
        self.countdown.update()

        if self.countdown.checkStartFlag():
            for p in self.players:
                p.countdownComplete()
            self.retreatPhase = 1

        if self.retreatPhase == 1:
            self.retreatProhibitTime.add(-1)
            if self.retreatProhibitTime.value == 0:
                self.retreatPhase = 2
                self.retreatBar.createText("Retreat", 1)
        
        for i, p in enumerate(self.players):
            if self.countdown.isGoing():
                keys = [False, False, False, False, False, False, False]
                keysNow = [0, 0, 0, 0, 0, 0, 0]
            else:
                keys = self.keys[i]
                keysNow = self.keysNow[i]
            l, r = self.exclusiveKeys(keys[2], keys[3])
            self.resetKeysNow(keysNow)
            self.act(p, keys, keysNow)
            self.checkReversable(l, r, p)
            self.checkForGround(p)
            self.checkForEdge(l, r, p)

        self.checkRetreat()
        self.resetHitMemory()
        self.checkForHits()
        for i, p in enumerate(self.players):
            self.actOnHit(i, p)

        for i, p in enumerate(self.players):
            keys = self.keys[i]
            keysNow = self.keysNow[i]
            l, r = self.exclusiveKeys(keys[2], keys[3])
            p.update()
            self.checkShoot(p)
            p.DI(l, r)

        temp = []
        for i in range(len(self.projectiles)):
            self.projectiles[i].update()
            self.checkProjForEdge(self.projectiles[i])
            self.checkProjForDissolve(self.projectiles[i])
            if not self.projectiles[i].destroy:
                temp.append(self.projectiles[i])
        self.projectiles = temp

        self.centerCamera(self.players[self.cameraPlayer])

        for b in self.bars:
            if not self.catBar is None:
                self.updateCatBarColors()
            b.update()

    def setCameraPlayer(self, c):
        if (c >= 0) and (c <= 1):
            self.cameraPlayer = c
        self.createBars()

    def key(self, k, t, p):
        if p == 0:
            return
        self.keys[p-1][k] = t
        if t:
            self.keysNow[p-1][k] = KEY_BUFFER

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
        if not self.keyTowardFacing(p, keys):
            p.actTransition('noXMove')
        if p.holdJump:
            if p.vel[1] > 0 or (not keys[6]):
                p.unholdJump()
        if p.canAct():
            if d:
                p.actTransition('doDuck')
            if l or r:
                p.actTransitionFacing('doDash', l, r)
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
                else:
                    if p.actTransition('attackB'):
                        keysNow[5] = 0
            if self.wasKeyPressed(6, keysNow):
                if p.actTransitionFacing('jump', l, r):
                    keysNow[6] = 0
            if not keys[4]:
                p.actTransition('releaseA')
            if not keys[5]:
                p.actTransition('releaseB')

            lev = p.getCatEnergyLevel()
            if lev == 1:
                p.actTransition('bladelv1')
            if lev == 2:
                p.actTransition('bladelv2')
            if lev == 3:
                p.actTransition('bladelv3')

    def checkForEnd(self):
        if self.players[0].retreat.isMax():
            self.returnCode[0] = 1
            if self.players[1].retreat.value > 0:
                self.returnCode[1] = 1
        elif self.players[1].retreat.isMax():
            self.returnCode[1] = 1
            if self.players[0].retreat.value > 0:
                self.returnCode[0] = 1


        if (self.returnCode[0] != 0) or (self.returnCode[1] != 0):
            self.advanceNow = True

    def checkReversable(self, l, r, p):
        if p.currFrame == 0 and p.currSubframe == 1:
            if p.currMove.reversable:
                if l:
                    p.facingRight = False
                if r:
                    p.facingRight = True

    def checkForGround(self, c):
        old = c.inAir
        if c.preciseLoc[1] >= self.rect.height - BATTLE_AREA_FLOOR_HEIGHT:
            c.preciseLoc[1] = self.rect.height - BATTLE_AREA_FLOOR_HEIGHT
            c.inAir = False
            c.vel[1] = 0.0
            c.aerialCharge = True
            if old:
                c.transToGround()
        else:
            c.inAir = True
            if not old:
                c.transToAir()

    def checkForEdge(self, l, r, p):
        check = False
        if p.preciseLoc[0] < BATTLE_EDGE_COLLISION_WIDTH:
            p.preciseLoc[0] = BATTLE_EDGE_COLLISION_WIDTH
            check = True
        if p.preciseLoc[0] > self.rect.width - BATTLE_EDGE_COLLISION_WIDTH:
            p.preciseLoc[0] = self.rect.width - BATTLE_EDGE_COLLISION_WIDTH
            check = True

        if self.retreatPhase == 2:
            if check:
                p.retreat.add(1)
            else:
                p.retreat.add(-RETREAT_RECEED)

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
            if s[0] == p.currFrame:
                proj = copy.copy(p.projectiles[s[1]].copySelf())

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
        
        if k == 1:
            p.hp.add(-100)
        elif k == 2:
            p.hp.add(100)


    def checkProjForEdge(self, p):
        if ( (p.preciseLoc[0] < (0 - PROJECTILE_SCREEN_ALLOWANCE))
             or (p.preciseLoc[0] > (self.rect.width + PROJECTILE_SCREEN_ALLOWANCE))
             or (p.preciseLoc[1] < (0 - PROJECTILE_SCREEN_ALLOWANCE))
             or (p.preciseLoc[1] > (self.rect.height + PROJECTILE_SCREEN_ALLOWANCE)) ):
            p.destroy = True

    def checkProjForDissolve(self, p):
        if (p.dissolveOnPhysical) and (p.currMove != p.moves['dissolve']):
            if p.preciseLoc[1] >= self.rect.height - BATTLE_AREA_FLOOR_HEIGHT:
                p.setCurrMove('dissolve')
        if (p.currMove == p.moves['dissolve']) and (p.currFrame == len(p.currMove.frames)-1):
            p.destroy = True
            p.currFrame = 0

    def setNetPlayer(self, p):
        self.netPlayer = p

    def buildNetMessage(self):
        p = self.netPlayer - 1
        msg = ''
        for i in self.keys[p]:
            if i:
                j = '1'
            else:
                j = '0'
            msg += j
        for i in self.keysNow[p]:
            msg += str(i)

        return msg

    def parseNetMessage(self, msg, p):
        if p == 0:
            return
        else:
            keys = self.keys[p-1]
            keysNow = self.keysNow[p-1]
            
        msg1 = msg[0:7]
        if len(msg1) != 7:
            print "!!!!"
            sys.exit()
        msg2 = msg[7:]
        if len(msg2) != 7:
            print "!!!!"
            sys.exit()
        
        for i, c in enumerate(msg1):
            if c == '1':
                keys[i] = True
            elif c == '0':
                keys[i] = False
            else:
                print "Error in message parsing"
                sys.exit()

        for i, c in enumerate(msg2):
            try:
                keysNow[i] = int(c)
            except:
                print "Error in message parsing"
                sys.exit()

    def createBars(self):
        self.bars = []
        p = self.players[self.cameraPlayer]

        self.bars.append(energybar.EnergyBar(p.hp,
                                             pygame.Rect(HEALTH_BAR_POSITION,
                                                         HEALTH_BAR_SIZE),
                                             HEALTH_BAR_BORDERS,
                                             HEALTH_BAR_COLORS,
                                             HEALTH_BAR_PULSE,
                                             self.players[self.cameraPlayer].name)
            )

        x = (SCREEN_SIZE[0] / 2) - (RETREAT_BAR_SIZE[0] / 2)
        y = HEALTH_BAR_POSITION[1]

        self.retreatBar = energybar.EnergyBar(self.retreatProhibitTime,
                                             pygame.Rect((x, y),
                                                         RETREAT_BAR_SIZE),
                                             RETREAT_BAR_BORDERS,
                                             RETREAT_BAR_COLORS,
                                             5, "Battle", None, 1)
        self.bars.append(self.retreatBar)
        

        x = HEALTH_BAR_POSITION[0]
        y = HEALTH_BAR_POSITION[1] + HEALTH_BAR_SIZE[1] + SPECIAL_BAR_OFFSET
        if isinstance(p, hare.Hare):
            self.bars.append(energybar.EnergyBar(p.hareEnergy,
                                                 pygame.Rect((x, y), SPECIAL_BAR_SIZE),
                                                 SPECIAL_BAR_BORDERS,
                                                 SPECIAL_BAR_COLORS,
                                                 SPECIAL_BAR_PULSE,
                                                 HARE_ENERGY_NAME,
                                                 HARE_ENERGY_USAGE)
                             )

        if isinstance(p, cat.Cat):
            self.catBar = energybar.EnergyBar(p.catEnergy,
                                                 pygame.Rect((x, y), SPECIAL_BAR_SIZE),
                                                 SPECIAL_BAR_BORDERS,
                                                 SPECIAL_BAR_COLORS,
                                                 SPECIAL_BAR_PULSE,
                                                 CAT_ENERGY_NAME,
                                                 CAT_ENERGY_MAX+1)
            self.bars.append(self.catBar)

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

    def checkForHits(self):
        offset = self.rect.topleft
        for i, p in enumerate(self.players):
            for j, q in enumerate(self.players):
                if not q is p:
                    for h in p.getHitboxes():
                        for r in q.getHurtboxes():
                            if (self.hitMemory[j] is None) and (p.attackCanHit):
                                hRect = p.getBoxAbsRect(h, offset)
                                rRect = q.getBoxAbsRect(r, offset)
                                if hRect.colliderect(rRect):
                                    self.hitMemory[j] = [h, p]
                                    p.attackCanHit = False

    def actOnHit(self, i, p):
        if not self.hitMemory[i] is None:
            mem = self.hitMemory[i][0]
            hitter = self.hitMemory[i][1]
            print "Player " + str(i+1) + " got hit!"

            p.facingRight = not hitter.facingRight

            damage = mem.damage
            stun = mem.stun

            xVel = math.cos(math.radians(mem.angle)) * mem.knockback
            yVel = math.sin(math.radians(mem.angle)) * mem.knockback

            yVel *= -1
            if p.facingRight:
                xVel *= -1

            p.getHit(damage, stun, (xVel, yVel))


    def netMessageSize(self):
        return NET_MESSAGE_SIZE
            

def testData():
    heroes = [hare.Hare(), hare.Hare()]
    
    size = (1600, 800)
    bg = pygame.Surface(size)
    bg.fill((220, 220, 220))
    barSpace = 200
    x = barSpace
    while x < size[0]:
        bg3 = pygame.Surface((2, size[1]))
        bg3.fill((180, 180, 180))
        bg.blit(bg3, (x, 0))
        x += barSpace
    bg2 = pygame.Surface((size[0], BATTLE_AREA_FLOOR_HEIGHT))
    bg2.fill((120, 120, 120))
    bg.blit(bg2, (0, size[1] - BATTLE_AREA_FLOOR_HEIGHT))
    return [heroes, size, bg]
