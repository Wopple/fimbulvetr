import os
import sys
import pygame

import incint
import boundint

import move

from constants import *

class BattleChar(object):
    def __init__(self, hp):
        self.hp = boundint.BoundInt(0, hp, hp)
        self.preciseLoc = [50.0, 50.0]
        self.accel = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.inAir = False
        self.facingRight = True
        self.holdJump = True
        self.aerialCharge = True
        self.projectiles = []
        self.attackCanHit = True
        
        temp = pygame.Surface((50, 80))
        temp.fill((2, 2, 2))
        self.setImage(temp, (40, 25))

        self.initMoves()
        self.setCurrMove('idle')

    def beginBattle(self):
        pass

    def update(self):
        self.proceedFrame()
        self.frameSpecial()
        
        if self.inAir:
            speedCap = self.airVelMax
        else:
            speedCap = self.groundVelMax
        
        for i in range(2):
            self.vel[i] += self.accel[i]
            self.speedCap([speedCap, self.vertVelMax], i)
            self.preciseLoc[i] += self.vel[i]

        self.rect.topleft = self.getRectPos()

        frame = self.getCurrentFrame()
        self.setImage(frame.image, frame.offset)

    def speedCap(self, caps, i):
        if not self.getCurrentFrame().ignoreSpeedCap:
            if self.vel[i] > caps[i]:
                self.vel[i] = caps[i]
            if i == 0:
                if self.vel[i] < -caps[i]:
                    self.vel[i] = -caps[i]

    def frameSpecial(self):
        f = self.getCurrentFrame()
        if not f.setVelX is None:
            self.vel[0] = f.setVelX * self.facingMultiplier()
            self.accelToZero()
        if not f.setVelY is None:
            self.vel[1] = f.setVelY
            self.accelToZero()
        if not f.addVelX is None:
            self.vel[0] += f.addVelX * self.facingMultiplier()
        if not f.addVelY is None:
            self.vel[1] += f.addVelY
        if not f.setVelYIfDrop is None:
            if self.vel[1] > 0:
                self.vel[1] = f.setVelYIfDrop
                self.accelToZero()

    def accelToZero(self):
        self.accel = [0.0, 0.0]

    def setImage(self, inImage, o):
        size = inImage.get_size()
        
        if self.facingRight:
            offset = o
            self.image = inImage
        else:
            offset = (-o[0] + size[0], o[1])
            self.image = pygame.transform.flip(inImage, True, False)
        
        self.offset = offset
        self.rect = pygame.Rect(self.getRectPos(), size)

    def draw(self, screen, inOffset):
        screen.blit(self.image, add_points(self.rect.topleft, inOffset))

        if SHOW_HURTBOXES:
            self.drawBoxes(self.getCurrentFrame().hurtboxes, screen, inOffset)
        if SHOW_HITBOXES:
            self.drawBoxes(self.getCurrentFrame().hitboxes, screen, inOffset)
        
        if SHOW_RED_DOT:
            screen.blit(RED_DOT, add_points(self.preciseLoc, inOffset))

    def drawBoxes(self, boxes, screen, inOffset):
        for b in boxes:
            boxpos = self.getBoxAbsRect(b, inOffset).topleft
            screen.blit(b.image, boxpos)

    def getBoxAbsRect(self, box, inOffset):
        if self.facingRight:
            boxPos = box.rect.topleft
        else:
            boxPos = flipRect(box.rect)

        topleft = add_points(add_points(self.preciseLoc, boxPos), inOffset)

        return pygame.Rect(topleft, box.rect.size)

    def testMove(self, t):
        self.accel[0] = self.airAccel * t

    def facingMultiplier(self):
        if self.facingRight:
            return 1
        else:
            return -1

    def DI(self, l, r):
        if not self.inAir:
            f = self.facingMultiplier()
        else:
            f = 0
            if l:
                f = -1
            if r:
                f = 1
            
        if not self.canDI():
            f = 0
        if not self.inAir:
            if not self.keyTowardFacing(l, r):
                f = 0
            accel = self.groundAccel
        else:
            accel = self.airAccel

        if f == 0 or ((l and self.vel[0] > 0) or(r and self.vel[0] < 0)):
            if not self.getCurrentFrame().ignoreFriction:
                self.friction()
        else:
            self.accel[0] = accel * f

        if self.inAir:
            self.accel[1] = self.vertAccel
        else:
            self.accel[1] = 0

    def friction(self):
        if self.inAir:
            friction = self.airFriction
        else:
            friction = self.groundFriction
        
        if self.vel[0] > friction:
            self.accel[0] = -friction
        elif self.vel[0] < -friction:
            self.accel[0] = friction
        else:
            self.accel[0] = 0
            self.vel[0] = 0

    def keyTowardFacing(self, l, r):
        if l and not self.facingRight:
            return True
        if r and self.facingRight:
            return True
        return False

    def getRectPos(self):
        return ( int(self.preciseLoc[0]) - self.offset[0],
                 int(self.preciseLoc[1]) - self.offset[1] )

    def initMoves(self):
        self.moves = {}
        self.moves['idle'] = move.baseIdle()
        self.moves['idleLike'] = move.baseBlank()
        self.moves['dash'] = move.baseDash()
        self.moves['air'] = move.baseAir()
        self.moves['airLike'] = move.baseBlank()
        self.moves['landing'] = move.baseLanding()
        self.moves['jumping'] = move.baseJumping()
        self.moves['ducking'] = move.baseDucking()
        self.moves['jabA'] = move.baseBlank()
        self.moves['jabB'] = move.baseBlank()
        self.moves['dashAttackA'] = move.baseBlank()
        self.moves['dashAttackB'] = move.baseBlank()
        self.moves['downA'] = move.baseBlank()
        self.moves['downB'] = move.baseBlank()
        self.moves['neutralAirA'] = move.baseBlank()
        self.moves['neutralAirB'] = move.baseBlank()
        self.moves['upAirB'] = move.baseBlank()
        self.moves['downAirB'] = move.baseBlank()

        self.moves['stun1'] = move.baseStun()
        self.moves['stun2'] = move.baseStun()

    def setCurrMove(self, index, frame=0):
        self.currMove = self.moves[index]
        self.currFrame = frame
        self.currSubframe = 0
        self.attackCanHit = True

        if len(self.currMove.frames) == 0:
            self.currMove = self.moves['idle']

    def getCurrentFrame(self):
        return self.currMove.frames[self.currFrame]

    def canAct(self):
        return True

    def canDI(self):
        return self.currMove.canDI

    def proceedFrame(self):
        frame = self.getCurrentFrame()

        self.currSubframe += 1
        if self.currSubframe == frame.length:
            self.currSubframe = 0
            t = self.actTransition('exitFrame', self.currFrame)
            if not t:
                self.currFrame += 1

        if self.currFrame >= len(self.currMove.frames):
            if self.currMove.isJump:
                self.jump()
            if self.inAir:
                self.setCurrMove('air')
            else:
                self.setCurrMove('idle')

    def jump(self):
        self.inAir = True
        self.holdJump = True
        self.vel[1] = self.jumpVel

    def unholdJump(self):
        self.holdJump = False
        self.vel[1] /= 3

    def checkTransition(self, key, var1=None, var2=None):
        t = self.currMove.transitions[key]
        if t is None:
            return False

        if not t.rangeMin is None:
            if self.currFrame < t.rangeMin:
                return False

        if not t.rangeMax is None:
            if self.currFrame > t.rangeMax:
                return False

        if (key == 'exitFrame'):
            i = t.var1
            if i == -1:
                i = len(self.currMove.frames) - 1
            if i != var1:
                return False

        return True
    
    def actTransition(self, key, var1=None, var2=None):
        t = self.currMove.transitions[key]
        if self.actLeft and self.checkTransition(key, var1, var2):
            
            if t.var1 == 2: #Energy cost to perform
                if self.energy.value < t.var2:
                    return False
                else:
                    self.energy.add(-t.var2)
            self.setCurrMove(t.destination)
            if not key == 'exitFrame':
                self.actLeft = False
            return True
        else:
            return False

    def actTransitionFacing(self, key, l, r, var1=None, var2=None):
        c = self.actTransition(key, var1, var2)
        if c:
            if l and not r:
                self.facingRight = False
            elif r and not l:
                self.facingRight = True

        return c

    def transToAir(self):
        if (not self.currMove.liftOff) and (not self.currMove.isStun):
            self.setCurrMove('air')

    def transToGround(self):
        c = self.actTransition('land')
        if not c:
            self.setCurrMove('idle')

    def frameData(self, i, j, r=[], h=[]):
        return [self.spriteSet[i][0], self.spriteSet[i][1], j, r, h]

    def getHitboxes(self):
        return self.getCurrentFrame().hitboxes

    def getHurtboxes(self):
        return self.getCurrentFrame().hurtboxes

    def getHit(self, damage, stun, vel):
        self.hp.add(-damage)

        print vel
        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

        if stun <= STUN_THRESHOLD_1:
            self.setCurrMove('stun1')
        elif stun <= STUN_THRESHOLD_2:
            self.setCurrMove('stun2')
        else:
            self.setCurrMove('stun3')
        
