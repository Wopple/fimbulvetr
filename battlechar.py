import os
import sys
import pygame

import incint
import boundint

import move

from constants import *

class BattleChar(object):
    def __init__(self, hp, footRectSize=30):
        self.hp = boundint.BoundInt(0, hp, hp)
        self.superEnergy = boundint.BoundInt(0, SUPER_ENERGY_MAX,
                    int(SUPER_ENERGY_MAX * SUPER_ENERGY_INITIAL_FACTOR))
        self.preciseLoc = [50.0, 50.0]
        self.accel = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.inAir = False
        self.facingRight = True
        self.holdJump = True
        self.aerialCharge = True
        self.projectiles = []
        self.attackCanHit = True
        self.retreat = boundint.BoundInt(0, RETREAT_HOLD_TOTAL, 0)
        self.freezeFrame = 0
        self.blockstun = 0
        self.onHitTrigger = False
        self.techBuffer = TECH_BUFFER_MIN
        self.canTech = True
        self.dropThroughPlatform = None
        self.dashBuffer = [0, 0]

        self.superMoves = []
        self.superMovesAir = []
        self.currSuperMove = None
        
        temp = pygame.Surface((50, 80))
        temp.fill((2, 2, 2))
        self.setImage(temp, (40, 25))

        self.initMoves()
        self.setCurrMove('idle')

        self.createDust = None

        self.footRect = pygame.Rect((0, 0), ((footRectSize * 2)+1, 5))
        self.positionFootRect()

    def beginBattle(self):
        self.retreat.change(0)
        self.freezeFrame = 0
        self.blockstun = 0
        if self.hp.value == 0:
            self.hp.value = 1
        self.setCurrMove('idle')
        self.dashBuffer = [0, 0]
        self.inAir = False
        
        self.setupSuper()

    def countdownComplete(self):
        pass

    def setLoc(self, loc):
        self.preciseLoc[0] = float(loc[0])
        self.preciseLoc[1] = float(loc[1])

    def update(self):
        for i in range(2):
            if self.dashBuffer[i] > 0:
                self.dashBuffer[i] -= 1
            
        if self.freezeFrame == 0:
            self.onHitTrigger = False
            self.proceedFrame()
            self.frameSpecial()

        frame = self.getCurrentFrame()

        if not (self.currMove.isStun or (self.currMove == self.moves['groundHit'])):
            self.canTech = True

        if self.techBuffer > TECH_BUFFER_MIN:
            self.techBuffer -= 1

        if self.freezeFrame == 0:
            if not frame.setSpeedCapX is None:
                speedCap = frame.setSpeedCapX
            elif self.inAir:
                speedCap = self.airVelMax
            else:
                if (self.currMove == self.moves['dashing']) or (self.currMove == self.moves['grabbing']):
                    speedCap = self.dashVelMax
                elif self.currMove == self.moves['running']:
                    speedCap = self.runVelMax
                else:
                    speedCap = self.walkVelMax

            for i in range(2):
                self.vel[i] += self.accel[i]
                self.speedCap([speedCap, self.vertVelMax], i)
                self.preciseLoc[i] += self.vel[i]

        self.rect.topleft = self.getRectPos()
        self.positionFootRect()

        self.setImage(frame.image, frame.offset)

        if self.freezeFrame > 0:
            self.freezeFrame -= 1
        elif self.blockstun > 0:
            self.blockstun -= 1

    #Updates the character for non-battle viewing, such as
    #in the character editor.
    def staticUpdate(self):
        self.actLeft = True
        self.proceedFrame()
        self.frameSpecial()
        frame = self.getCurrentFrame()
        self.setImage(frame.image, frame.offset)


    def positionFootRect(self):
        self.footRect.center = add_points(self.preciseLoc, (0, 0))
        

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
            self.accel[0] = 0.0
        if not f.setVelY is None:
            self.vel[1] = f.setVelY
            self.accel[1] = 0.0
        if not f.addVelX is None:
            self.vel[0] += f.addVelX * self.facingMultiplier()
        if not f.addVelY is None:
            self.vel[1] += f.addVelY
        if not f.setVelYIfDrop is None:
            if self.vel[1] > 0:
                self.vel[1] = f.setVelYIfDrop
                self.accel[1] = 0.0
        if not f.addVelYIfDrop is None:
            if self.vel[1] > 0:
                self.vel[1] += f.addVelYIfDrop

        if self.currSubframe == 0 and f.resetHitPotential:
            self.attackCanHit = True

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
        if SHOW_BLOCKBOXES:
            self.drawBoxes(self.getCurrentFrame().blockboxes, screen, inOffset)
        
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

    def getBoxRect(self, box):
        return self.getBoxAbsRect(box, (0, 0))

    def testMove(self, t):
        self.accel[0] = self.airAccel * t

    def facingMultiplier(self):
        if self.facingRight:
            return 1
        else:
            return -1

    def DI(self, l, r):
        if self.freezeFrame == 0:
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
                if self.currMove == self.moves['dashing']:
                    accel = self.dashAccel
                elif not self.keyTowardFacing(l, r):
                    f = 0
                else:
                    accel = self.walkAccel
            else:
                accel = self.airAccel

            if not self.getCurrentFrame().setAccelX is None:
                accel = self.getCurrentFrame().setAccelX

            if f == 0 or ((l and self.vel[0] > 0) or(r and self.vel[0] < 0)):
                if not self.getCurrentFrame().ignoreFriction:
                    self.friction()
                else:
                    
                    if self.facingRight:
                        f2 = 1
                    else:
                        f2 = -1
                    
                    if self.getCurrentFrame().setAccelX is None:
                        self.accel[0] = 0.0
                    else:
                        self.accel[0] = self.getCurrentFrame().setAccelX * f2
                        
                    if self.getCurrentFrame().setAccelY is None:
                        self.accel[1] = 0.0
                    else:
                        self.accel[1] = self.getCurrentFrame().setAccelY * f2
            else:
                self.accel[0] = accel * f

            if self.inAir:
                if not self.getCurrentFrame().setAccelY is None:
                    accel = self.getCurrentFrame().setAccelY
                else:
                    accel = self.vertAccel
                self.accel[1] = accel
            else:
                self.accel[1] = 0

    def friction(self):
        c = self.getCurrentFrame()
        if self.freezeFrame == 0 and self.blockstun == 0:
            if not c.setFrictionX is None:
                friction = c.setFrictionX
            elif self.inAir:
                if self.currMove.isStun:
                    friction = self.airFrictionStunned
                else:
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
        self.moves['walking'] = move.baseWalking()
        self.moves['dashing'] = move.baseDashing()
        self.moves['running'] = move.baseRunning()
        self.moves['air'] = move.baseAir()
        self.moves['flipping'] = move.baseAir()
        self.moves['airLike'] = move.baseBlank()
        self.moves['landing'] = move.baseLanding()
        self.moves['jumping'] = move.baseJumping()
        self.moves['jumpingLike'] = move.baseJumping()
        self.moves['ducking'] = move.baseDucking()
        self.moves['jabA'] = move.baseBlank()
        self.moves['jabB'] = move.baseBlank()
        self.moves['dashAttackA'] = move.baseBlank()
        self.moves['dashAttackB'] = move.baseBlank()
        self.moves['downA'] = move.baseBlank()
        self.moves['downB'] = move.baseBlank()
        self.moves['upA'] = move.baseBlank()
        self.moves['upB'] = move.baseBlank()
        self.moves['neutralAirA'] = move.baseBlank()
        self.moves['neutralAirB'] = move.baseBlank()
        self.moves['upAirA'] = move.baseBlank()
        self.moves['upAirB'] = move.baseBlank()
        self.moves['downAirA'] = move.baseBlank()
        self.moves['downAirB'] = move.baseBlank()
        self.moves['droppingThrough'] = move.baseDroppingThrough()

        self.moves['grabbing'] = move.baseGrabbing()
        self.moves['grabHold'] = move.baseGrabHold()
        self.moves['grabbed'] = move.baseGrabbed()
        self.moves['grabbed2'] = move.baseGrabbed2()
        self.moves['grabRelease'] = move.baseGrabRelease()
        self.moves['grabbedRelease'] = move.baseGrabbedRelease()

        self.moves['throwBackward'] = move.baseThrow()
        self.moves['throwForward'] = move.baseThrow()

        self.moves['blocking'] = move.baseBlocking()
        self.moves['lowBlocking'] = move.baseLowBlocking()
        self.moves['airBlocking'] = move.baseAirBlocking()

        self.moves['stun1'] = move.baseStun()
        self.moves['stun2'] = move.baseStun()
        self.moves['stun3'] = move.baseStunNeedTech()
        self.moves['stun4'] = move.baseStunNeedTech()

        self.moves['groundHit'] = move.baseGroundHit()
        self.moves['standUp'] = move.baseStand()
        self.moves['standForward'] = move.baseStand()
        self.moves['standBackward'] = move.baseStand()

        self.moves['teching'] = move.baseTeching()
        self.moves['techUp'] = move.baseTechRoll()
        self.moves['techForward'] = move.baseTechRoll()
        self.moves['techBackward'] = move.baseTechRoll()

        self.moves['deadFalling'] = move.baseDeadFalling()
        self.moves['deadGroundHit'] = move.baseDeadGroundHit()
        self.moves['deadLaying'] = move.baseDeadLaying()
        
        self.moves['superFlash'] = None
        self.moves['superMove'] = None
        
        self.moves['superFlashAir'] = None
        self.moves['superMoveAir'] = None

    def setCurrMove(self, index, frame=0):
        self.currMove = self.moves[index]
        self.currFrame = frame
        self.currSubframe = 0
        self.attackCanHit = True

        if (self.currMove is None) or (len(self.currMove.frames) == 0):
            if (self.inAir):
                self.currMove = self.moves['air']
            else:
                self.currMove = self.moves['idle']

    def getCurrentFrame(self):
        return self.currMove.frames[self.currFrame]

    def canAct(self):
        if self.blockstun > 0:
            return False
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
                self.setCurrMove('flipping')
            elif self.inAir:
                self.setCurrMove('air')
            else:
                self.setCurrMove('idle')

    def jump(self):
        self.inAir = True
        self.holdJump = True
        self.vel[1] = self.jumpVel

    def unholdJump(self):
        self.holdJump = False
        if self.currMove.canDI:
            self.vel[1] /= 3

    def checkTransition(self, key, var1=None, var2=None):
        t = self.currMove.transitions[key]
        if t is None:
            return False

        if not t.rangeMin is None:
            rMin = t.rangeMin
            if rMin < 0:
                rMin = len(self.currMove.frames)+rMin
            if self.currFrame < rMin:
                return False

        if not t.rangeMax is None:
            rMax = t.rangeMax
            if rMax < 0:
                rMax = len(self.currMove.frames)+rMax
            if self.currFrame > rMax:
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
        
        if (key == 'super') and (not t is None) and (self.moves[t.destination] is None):
            return 
        
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
        if (self.blockstun > 0):
            self.setCurrMove('airBlocking')
        elif (not self.currMove.liftOff) and (not self.currMove.isStun):
            self.setCurrMove('flipping')

    def transToGround(self):
        if self.currMove.isStun:
            if self.currMove.needTech:
                self.setCurrMove('groundHit')
                self.createDust = 0
            return
        c = self.actTransition('land')
        if not c:
            self.setCurrMove('idle')

    def frameData(self, i, j, r=[], h=[], b=[]):
        return [self.spriteSet[i][0], self.spriteSet[i][1], j, r, h, b]

    def getHitboxes(self):
        return self.getCurrentFrame().hitboxes

    def getHurtboxes(self):
        return self.getCurrentFrame().hurtboxes

    def getBlockboxes(self):
        return self.getCurrentFrame().blockboxes

    def getHit(self, damage, stun, vel):
        self.hp.add(-damage)

        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

        if stun <= STUN_THRESHOLD_1:
            self.setCurrMove('stun1')
        elif stun <= STUN_THRESHOLD_2:
            self.setCurrMove('stun2')
        elif stun <= STUN_THRESHOLD_3:
            self.setCurrMove('stun3')
        else:
            self.setCurrMove('stun4')

    def getBlockstun(self, damage, stun, vel, properties):
        self.blockstun = int(stun * BLOCKSTUN_FACTOR)

        self.vel[0] = vel[0]
        self.vel[1] = vel[1]
        

    def getSuper(self):
        return self.superMoves[self.currSuperMove]

    def getCatEnergyLevel(self):
        return 0

    def getBlockFXPoint(self, i):
        p = [self.blockFXPoints[i][0], self.blockFXPoints[i][1]]
        if not self.facingRight:
            p[0] *= -1
        return add_points(self.preciseLoc, p)
    
    def setSuperValue(self, s):
        if (s < 0) or (s >= len(self.superMoves)) or (s >= len(self.superMovesAir)):
            s = 0
            
        self.currSuperMove = s
        
    def setupSuper(self):
        
        self.moves['superMove'] = None
        self.moves['superFlash'] = None
        self.moves['superMoveAir'] = None
        self.moves['superFlashAir'] = None
        
        m = self.superMoves[self.currSuperMove]
        self.moves['superMove'] = m
        if (not m is None):
            self.moves['superFlash'] = m.flash
        
        m = self.superMovesAir[self.currSuperMove]
        self.moves['superMoveAir'] = m
        if (not m is None):
            self.moves['superFlashAir'] = m.flash
        
    def appendSuperMove(self, ground, air):
        
        self.superMoves.append(ground)
        self.superMovesAir.append(air)
        
        
    def getSuperIcon(self):
        
        if (self.currSuperMove >= len(self.superIcons)):
            s = pygame.Surface(BATTLE_SUPER_ICON_SIZE)
            s.fill(BLACK)
        else:
            s = self.superIcons[self.currSuperMove]
            
        return s
        
