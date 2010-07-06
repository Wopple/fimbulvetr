import os
import sys
import pygame

import incint
import boundint
import battlechar
import move

from constants import *

class Cat(battlechar.BattleChar):
    def __init__(self, name="Unnamed Cat", inSpecial=0):
        self.name = name
        self.speciesName = "Cat"
        self.spriteSet = CAT_IMAGES
        self.groundAccel = 1.3
        self.groundVelMax = 9.0
        self.groundFriction = 2.6
        self.airAccel = 1.6
        self.airVelMax = 10.5
        self.airFriction = 0.9
        self.vertAccel = 0.6
        self.vertVelMax = 19.5
        self.jumpVel = -15.0
        self.catEnergy = boundint.BoundInt(0, CAT_ENERGY_MAX, 0)
        self.prevEnergy = self.catEnergy.value
        self.energyDelayTick = CAT_ENERGY_DELAY
        self.energy = self.catEnergy
        super(Cat, self).__init__(1000)
        self.initSpecMoves()

        self.speciesDesc = ("jhgjhk")

    def beginBattle(self):
        self.catEnergy.change(CAT_ENERGY_BATTLE_START)

    def update(self):
        super(Cat, self).update()

        if self.currMove.chargeBlade:
            self.catEnergy.add(CAT_ENERGY_RECHARGE)
            self.energyDelayTick = 0
        else:
            if self.energyDelayTick < CAT_ENERGY_DELAY:
                self.energyDelayTick += 1
            else:
                self.catEnergy.add(-CAT_ENERGY_USAGE)

    def initSpecMoves(self):
        self.createMoveIdle()
        self.createMoveDash()
        self.createMoveAir()
        self.createMoveJumping()
        self.createMoveUpB()

    def createMoveIdle(self):
        f = [ self.frameData(0, 2) ]
        self.moves['idle'].append(f, [])

    def createMoveDash(self):
        f = [ self.frameData(1, 4),
              self.frameData(2, 4),
              self.frameData(3, 4),
              self.frameData(4, 4) ]
        self.moves['dash'].append(f, [])

    def createMoveAir(self):
        f = [ self.frameData(5, 2) ]
        self.moves['air'].append(f, [])

    def createMoveJumping(self):
        f = [ self.frameData(5, 2) ]
        self.moves['jumping'].append(f, [])

    def createMoveUpB(self):
        print "Making this awesome move!"
        f = [ self.frameData(6, 4),
              self.frameData(7, 4),
              self.frameData(8, 4),
              self.frameData(9, 4)]
        t = [ ['releaseB', move.Transition(None, None, 2, None, 'idle')],
              ['exitFrame', move.Transition(-1, None, None, None, 'chargeSword')] ]
        self.moves['upB'].append(f, t)
        self.moves['upB'].canDI = False

        self.createMoveChargeSword()

    def createMoveChargeSword(self):
        f = [ self.frameData(10, 2),
              self.frameData(11, 2),
              self.frameData(12, 2),
              self.frameData(13, 2),
              self.frameData(11, 2),
              self.frameData(10, 2),
              self.frameData(12, 2),
              self.frameData(11, 2),
              self.frameData(10, 2),
              self.frameData(13, 2),
              self.frameData(12, 2),
              self.frameData(10, 2),
              self.frameData(13, 2),
              self.frameData(11, 2) ]
        t = [ ['releaseB', move.Transition(None, None, None, None, 'idle')],
              ['exitFrame', move.Transition(-1, None, None, None, 'chargeSword')] ]
        self.moves['chargeSword'] = move.Move(f, t)
        self.moves['chargeSword'].canDI = False
        self.moves['chargeSword'].chargeBlade = True
