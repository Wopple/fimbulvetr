import os
import sys
import pygame
import copy

import mvc

import incint

import hare, fox

from constants import *

class Model(mvc.Model):
    def __init__(self, inChar, areaSize, bg):
        super(Model, self).__init__()
        self.player = inChar
        self.player.beginBattle()
        self.background = bg
        self.rect = pygame.Rect((0, 0), areaSize)
        self.keys = [False, False, False, False, False, False, False]
        self.keysNow = [0, 0, 0, 0, 0, 0, 0]
        self.projectiles = []

    def update(self):
        l, r = self.exclusiveKeys(self.keys[2], self.keys[3])
        self.resetKeysNow()
        self.act()
        self.checkReversable(l, r)
        self.checkForGround(self.player)
        self.player.update()
        self.checkShoot(self.player)
        self.player.DI(l, r)

        temp = []
        for i in range(len(self.projectiles)):
            self.projectiles[i].update()
            self.checkProjForEdge(self.projectiles[i])
            self.checkProjForDissolve(self.projectiles[i])
            if not self.projectiles[i].destroy:
                temp.append(self.projectiles[i])
        self.projectiles = temp

        self.centerCamera(self.player)

    def key(self, k, t, p):
        if p == 0:
            return
        self.keys[k] = t
        if t:
            self.keysNow[k] = KEY_BUFFER

    def resetKeysNow(self):
        for k in range(len(self.keysNow)):
            if self.keysNow[k] > 0:
                self.keysNow[k] -= 1

    def wasKeyPressed(self, k):
        if k == -1:
            return ((self.keysNow[2] > 0) or (self.keysNow[3] > 0))
        else:
            return (self.keysNow[k] > 0)

    def exclusiveKeys(self, k1, k2):
        if k1 and k2:
            k1 = False
            k2 = False
        return k1, k2

    def keyTowardFacing(self):
        l, r = self.exclusiveKeys(self.keys[2], self.keys[3])
        return self.player.keyTowardFacing(l, r)

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

    def act(self):
        self.player.actLeft = True
        u, d = self.exclusiveKeys(self.keys[0], self.keys[1])
        l, r = self.exclusiveKeys(self.keys[2], self.keys[3])
        if not self.keyTowardFacing():
            self.player.actTransition('noXMove')
        if self.player.holdJump:
            if self.player.vel[1] > 0 or (not self.keys[6]):
                self.player.unholdJump()
        if self.player.canAct():
            if d:
                self.player.actTransition('doDuck')
            if l or r:
                self.player.actTransitionFacing('doDash', l, r)
            if not d:
                self.player.actTransition('stopDuck')
            if self.wasKeyPressed(4):
                if u:
                    if self.player.actTransition('attackAUp'):
                        self.keysNow[4] = 0
                elif d:
                    if self.player.actTransition('attackADown'):
                        self.keysNow[4] = 0
                else:
                    if self.player.actTransition('attackA'):
                        self.keysNow[4] = 0
            if self.wasKeyPressed(5):
                if u:
                    if self.player.aerialCharge:
                        if self.player.actTransition('attackBUpCharge'):
                            self.keysNow[5] = 0
                            self.player.aerialCharge = False
                    else:
                        if self.player.actTransition('attackBUp'):
                            self.keysNow[5] = 0
                elif d:
                    if self.player.actTransition('attackBDown'):
                        self.keysNow[5] = 0
                else:
                    if self.player.actTransition('attackB'):
                        self.keysNow[5] = 0
            if self.wasKeyPressed(6):
                if self.player.actTransitionFacing('jump', l, r):
                    self.keysNow[6] = 0
            if not self.keys[4]:
                self.player.actTransition('releaseA')
            if not self.keys[5]:
                self.player.actTransition('releaseB')

    def checkReversable(self, l, r):
        if self.player.currFrame == 0 and self.player.currSubframe == 1:
            if self.player.currMove.reversable:
                if l:
                    self.player.facingRight = False
                if r:
                    self.player.facingRight = True

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
        temp = self.player.preciseLoc
        
        if k == 1:
            self.player = hare.Hare()
        if k == 2:
            self.player = fox.Fox()

        self.player.preciseLoc = temp


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

    def buildNetMessage(self):
        msg = ''
        for i in self.keys:
            if i:
                j = '1'
            else:
                j = '0'
            msg += j
        for i in self.keysNow:
            msg += str(i)

        return msg

    def parseNetMessage(self, msg, p):
        if p == 0:
            return
        elif p == 1:
            keys = self.keys
            keysNow = self.keysNow
            
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
    hero = hare.Hare()
    #hero = fox.Fox()
    
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
    return [hero, size, bg]
