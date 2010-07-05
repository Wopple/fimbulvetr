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
        self.vertAccel = 0.8
        self.vertVelMax = 19.5
        self.jumpVel = -15.0
        super(Cat, self).__init__(850)
        self.initSpecMoves()

        self.speciesDesc = ("jhgjhk")

    def beginBattle(self):
        pass

    def update(self):
        super(Cat, self).update()

    def initSpecMoves(self):
        self.createMoveIdle()
        self.createMoveDash()
        self.createMoveAir()
        self.createMoveJumping()

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
