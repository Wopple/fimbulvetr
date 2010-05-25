import os
import sys
import pygame
import copy

import mvc

import incint

import hare, fox

from constants import *

class Model(mvc.Model):
    def __init__(self, inChars, areaSize, bg):
        super(Model, self).__init__()
        self.players = inChars
        for p in self.players:
            p.beginBattle()
        self.background = bg
        self.rect = pygame.Rect((0, 0), areaSize)
        self.keys = [[False, False, False, False, False, False, False],
                     [False, False, False, False, False, False, False]]
        self.keysNow = [[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]]
        self.projectiles = []
        self.cameraPlayer = 0
        self.netPlayer = 0

    def update(self):
        for i, p in enumerate(self.players):
            keys = self.keys[i]
            keysNow = self.keysNow[i]
            l, r = self.exclusiveKeys(keys[2], keys[3])
            self.resetKeysNow(keysNow)
            self.act(p, keys, keysNow)
            self.checkReversable(l, r, p)
            self.checkForGround(p)
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

    def setCameraPlayer(self, c):
        if (c >= 0) and (c <= 1):
            self.cameraPlayer = c

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
                    if p.aerialCharge:
                        if p.actTransition('attackBUpCharge'):
                            keysNow[5] = 0
                            p.aerialCharge = False
                    else:
                        if p.actTransition('attackBUp'):
                            keysNow[5] = 0
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

    def checkShoot(self, p):
        m = p.currMove
        for s in m.shoot:
            if s[0] == p.currFrame:
                proj = copy.copy(p.projectiles[s[1]])

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
        temp = self.players[0].preciseLoc
        
        if k == 1:
            self.players[0] = hare.Hare()
        if k == 2:
            self.players[0] = fox.Fox()

        self.players[0].preciseLoc = temp
        self.players[0].beginBattle()


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
        

def testData():
    heroes = [hare.Hare(), fox.Fox()]
    
    size = (1920, 1305)
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
