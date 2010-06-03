import os
import sys
import pygame

import incint
import boundint
import battlechar
import move

from constants import *

class Hare(battlechar.BattleChar):
    def __init__(self, name="Unnamed Hare"):
        self.name = name
        self.spriteSet = HARE_IMAGES
        self.groundAccel = 1.2
        self.groundVelMax = 14.0
        self.groundFriction = 2.2
        self.airAccel = 0.7
        self.airVelMax = 11.0
        self.airFriction = 0.4
        self.vertAccel = 1.4
        self.vertVelMax = 19.5
        self.jumpVel = -26.0
        self.hareEnergy = boundint.BoundInt(0, HARE_ENERGY_MAX, 0)
        self.prevEnergy = self.hareEnergy.value
        self.energyDelayTick = HARE_ENERGY_DELAY
        self.energy = self.hareEnergy
        super(Hare, self).__init__(850)
        self.initSpecMoves()

    def beginBattle(self):
        self.hareEnergy.change(HARE_ENERGY_BATTLE_START)

    def update(self):
        super(Hare, self).update()

        if self.prevEnergy != self.hareEnergy.value:
            self.energyDelayTick = 0
        self.prevEnergy = self.hareEnergy.value

        if self.energyDelayTick < HARE_ENERGY_DELAY:
            self.energyDelayTick += 1
        else:
            self.hareEnergy.add(HARE_ENERGY_RECHARGE)
            self.prevEnergy = self.hareEnergy.value
        
    def initSpecMoves(self):
        self.createMoveIdle()
        self.createMoveIdleLike()
        self.createMoveDash()
        self.createMoveAir()
        self.createMoveAirLike()
        self.createMoveLanding()
        self.createMoveJumping()
        self.createMoveDucking()
        self.createMoveJabA()
        self.createMoveJabB()
        self.createDashAttackA()
        self.createDashAttackB()
        self.createMoveDownA()
        self.createMoveDownB()
        self.createNeutralAirA()
        self.createNeutralAirB()
        self.createUpAirB()
        self.createDownAirB()

    def createMoveIdle(self):
        r = [
                [
                    (-13, -44, 1, -35),
                    (-13, -52, -2, -44),
                    (-12, -35, 1, -19),
                    (0, -33, 5, -29),
                    (-18, -32, -11, -26),
                    (-24, -29, -17, -24),
                    (-12, -19, -5, 0),
                    (-8, -19, 1, -12),
                    (0, -16, 7, -11),
                    (3, -12, 8, 0),
                    (5, -4, 17, 1)
                 ]
            ]
        f = [ self.frameData(0, 10, r[0]),
              self.frameData(1, 9, r[0])]
        self.moves['idle'].append(f, [])

    def createMoveIdleLike(self):
        f = [ self.frameData(66, 1),
              self.frameData(0, 1),
              self.frameData(66, 1) ]
        self.moves['idleLike'].append(f, [])
        self.moves['idleLike'].frames[0].ignoreFriction = True
        self.moves['idleLike'].frames[0].ignoreSpeedCap = True
        self.moves['idleLike'].frames[1].ignoreFriction = True
        self.moves['idleLike'].frames[1].ignoreSpeedCap = True

    def createMoveDash(self):
        r = [
                [
                    (-8, -47, 5, -37),
                    (-8, -53, 2, -47),
                    (-10, -37, 4, -22),
                    (2, -35, 13, -29),
                    (-18, -30, -10, -21),
                    (-25, -19, -6, -10),
                    (-11, -21, 8, -13),
                    (8, -18, 20, -12),
                    (19, -20, 26, -11),
                    (1, -31, 10, -24)
                ],
                [
                    (-8, -47, 5, -37),
                    (-8, -53, 2, -47),
                    (-10, -37, 5, -20),
                    (-9, -21, 8, -11),
                    (-16, -10, -4, 0),
                    (4, -12, 11, -3),
                    (9, -8, 22, -3),
                    (1, -30, 10, -25)
                ],
                [
                    (-8, -47, 5, -37),
                    (-8, -53, 2, -47),
                    (-10, -37, 5, -20),
                    (-7, -20, 5, -1),
                    (-3, -4, 9, 0)
                ]
            ]
                    
        f = [ self.frameData(2, 3, r[0]),
              self.frameData(3, 3, r[1]),
              self.frameData(4, 3, r[2]),
              self.frameData(5, 3, r[0]),
              self.frameData(6, 3, r[1]),
              self.frameData(7, 3, r[2]) ]
        self.moves['dash'].append(f, [])

    def createMoveAir(self):
        f = [ self.frameData(8, 2) ]
        self.moves['air'].append(f, [])

    def createMoveAirLike(self):
        f = [ self.frameData(67, 1),
              self.frameData(8, 1),
              self.frameData(67, 1) ]
        self.moves['airLike'].append(f, [])
        self.moves['airLike'].frames[0].ignoreFriction = True
        self.moves['airLike'].frames[0].ignoreSpeedCap = True
        self.moves['airLike'].frames[1].ignoreFriction = True
        self.moves['airLike'].frames[1].ignoreSpeedCap = True

    def createMoveLanding(self):
        f = [ self.frameData(9, 3) ]
        self.moves['landing'].append(f, [])

    def createMoveJumping(self):
        f = [ self.frameData(9, 3) ]
        self.moves['jumping'].append(f, [])

    def createMoveDucking(self):
        f = [ self.frameData(10, 2) ]
        self.moves['ducking'].append(f, [])

    def createMoveJabA(self):
        r = [
                [
                    (-9, -43, 4, -32),
                    (-9, -48, 1, -43),
                    (-9, -33, 5, -17),
                    (-10, -18, -4, 1),
                    (-9, -17, 6, -11),
                    (5, -14, 10, 0),
                    (6, -2, 18, 1),
                    (-12, -40, -9, -35)
                ],
                [
                    (-5, -44, 8, -32),
                    (-5, -49, 6, -44),
                    (-7, -32, 8, -15),
                    (-14, -29, -6, -24),
                    (6, -33, 20, -25),
                    (-9, -16, -2, 1),
                    (-6, -18, 13, -9),
                    (6, -11, 12, 1),
                    (8, -2, 18, 2)
                ]
            ]

        h = [
                [
                    (22, -34, 52, -20, 40, 8, 10, 3, [])
                ]
            ]
                    
        f = [ self.frameData(41, 4, r[0]),
              self.frameData(42, 2, r[1], h[0]),
              self.frameData(43, 2, r[1]),
              self.frameData(43, 10, r[1])]
        t = [ ['attackA', move.Transition(None, None, 3, None, 'jab2')] ]
        self.moves['jabA'].append(f, t)
        self.moves['jabA'].canDI = False

        self.createMoveJab2()

    def createMoveJab2(self):
        r = [
                [
                    (-5, -44, 8, -32),
                    (-5, -49, 6, -44),
                    (-7, -32, 8, -15),
                    (-14, -29, -6, -24),
                    (6, -33, 20, -25),
                    (-9, -16, -2, 1),
                    (-6, -18, 13, -9),
                    (6, -11, 12, 1),
                    (8, -2, 18, 2)
                ],
                [
                    (-5, -44, 8, -32),
                    (-5, -49, 6, -44),
                    (-7, -32, 8, -15),
                    (6, -33, 20, -25),
                    (-9, -16, -2, 1),
                    (-6, -18, 13, -9),
                    (6, -11, 12, 1),
                    (8, -2, 18, 2)
                ],
                [
                    (-5, -44, 8, -32),
                    (-5, -49, 6, -44),
                    (-7, -32, 8, -15),
                    (6, -28, 17, -23),
                    (-9, -16, -2, 1),
                    (-6, -18, 13, -9),
                    (6, -11, 12, 1),
                    (8, -2, 18, 2),
                    (-15, -36, -1, -28)
                ]
            ]

        h = [
                [
                    (22, -34, 52, -20, 40, 8, 10, 3, [])
                ]
            ]
        
        f = [ self.frameData(43, 2, r[0]),
              self.frameData(44, 3, r[1], h[0]),
              self.frameData(45, 8, r[2]),
              self.frameData(45, 3, r[2])]
        t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 1, 2, 'idleLike')] ]
        self.moves['jab2'] = move.Move(f, t)
        self.moves['jab2'].canDI = False

    def createMoveJabB(self):
        f = [ self.frameData(46, 3),
              self.frameData(47, 1),
              self.frameData(48, 1),
              self.frameData(49, 5),
              self.frameData(50, 6) ]
        self.moves['jabB'].append(f, [])
        self.moves['jabB'].canDI = False

    def createDashAttackA(self):
        f = [ self.frameData(59, 3),
              self.frameData(59, 2),
              self.frameData(59, 4),
              self.frameData(60, 1),
              self.frameData(61, 1),
              self.frameData(62, 2),
              self.frameData(63, 5),
              self.frameData(64, 2),
              self.frameData(65, 2) ]
        t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 2, 3, 'idleLike')] ]
        self.moves['dashAttackA'].append(f, t)
        self.moves['dashAttackA'].canDI = False
        self.moves['dashAttackA'].frames[0].setVelX = 15
        self.moves['dashAttackA'].frames[0].ignoreFriction = True
        self.moves['dashAttackA'].frames[0].ignoreSpeedCap = True
        self.moves['dashAttackA'].frames[1].ignoreFriction = True
        self.moves['dashAttackA'].frames[1].ignoreSpeedCap = True
        self.moves['dashAttackA'].frames[2].ignoreSpeedCap = True


    def createDashAttackB(self):
        f = [ self.frameData(19, 2),
              self.frameData(23, 2),
              self.frameData(20, 1),
              self.frameData(33, 2),
              self.frameData(21, 1),
              self.frameData(24, 2),
              self.frameData(22, 1),
              self.frameData(34, 2),
              self.frameData(19, 1),
              self.frameData(23, 2),
              self.frameData(19, 1),
              self.frameData(23, 2),
              self.frameData(20, 1),
              self.frameData(33, 2)]
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'rollingSlash')],
              ['releaseB', move.Transition(-1, None, 5, None, 'rollingSlash')],
              ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 4, None, 'idleLike')]]
        self.moves['dashAttackB'].append(f, t)
        self.moves['dashAttackB'].canDI = False
        self.moves['dashAttackB'].frames[0].setVelX = 17
        for i in range(len(self.moves['dashAttackB'].frames)):
            self.moves['dashAttackB'].frames[i].ignoreFriction = True
            self.moves['dashAttackB'].frames[i].ignoreSpeedCap = True

        self.createMoveRollingSlash()

    def createMoveRollingSlash(self):
        f = [ self.frameData(25, 2),
              self.frameData(26, 2),
              self.frameData(27, 3),
              self.frameData(28, 10)]
        self.moves['rollingSlash'] = move.Move(f, [])
        self.moves['rollingSlash'].canDI = False
        self.moves['rollingSlash'].frames[0].setVelX = 0

    def createMoveDownA(self):
        f = [ self.frameData(29, 2),
              self.frameData(30, 3),
              self.frameData(31, 6),
              self.frameData(32, 4) ]
        self.moves['downA'].append(f, [])
        self.moves['downA'].canDI = False

    def createMoveDownB(self):
        f = [ self.frameData(11, 7),
              self.frameData(11, 2),
              self.frameData(12, 5),
              self.frameData(13, 20)]
        t = [ ['land', move.Transition(None, None, None, None, 'downBLag')] ]
        self.moves['downB'].append(f, t)
        self.moves['downB'].canDI = False
        self.moves['downB'].liftOff = True
        self.moves['downB'].frames[0].setVelX = -24
        self.moves['downB'].frames[0].setVelY = -9.5
        self.moves['downB'].frames[0].ignoreSpeedCap = True
        self.moves['downB'].frames[0].ignoreFriction = True
        self.moves['downB'].frames[1].ignoreFriction = True
        
        self.createLagDownB()

    def createLagDownB(self):
        f = [ self.frameData(9, 8) ]
        self.moves['downBLag'] = move.Move(f, [])
        self.moves['downBLag'].canDI = False

    def createNeutralAirA(self):
        f = [ self.frameData(14, 3),
              self.frameData(15, 1),
              self.frameData(16, 1),
              self.frameData(17, 3),
              self.frameData(18, 5) ]
        self.moves['neutralAirA'].append(f, [])
        self.moves['neutralAirA'].reversable = True

    def createNeutralAirB(self):
        f = [ self.frameData(35, 3),
              self.frameData(36, 1),
              self.frameData(37, 4),
              self.frameData(38, 3),
              self.frameData(39, 1),
              self.frameData(40, 4),
              self.frameData(35, 3),
              self.frameData(36, 1),
              self.frameData(37, 5),
              self.frameData(8, 4)]
        self.moves['neutralAirB'].append(f, [])
        self.moves['neutralAirB'].canDI = False
        self.moves['neutralAirB'].reversable = True
        self.moves['neutralAirB'].frames[1].setVelYIfDrop = -3.0
        self.moves['neutralAirB'].frames[4].setVelYIfDrop = -1.5
        self.moves['neutralAirB'].frames[7].setVelYIfDrop = -1.5
        for i in range(len(self.moves['neutralAirB'].frames)):
            self.moves['neutralAirB'].frames[i].ignoreFriction = True

    def createUpAirB(self):
        f = [ self.frameData(51, 3),
              self.frameData(52, 1),
              self.frameData(53, 1),
              self.frameData(54, 1),
              self.frameData(52, 1),
              self.frameData(53, 1),
              self.frameData(54, 1),
              self.frameData(52, 1),
              self.frameData(53, 1),
              self.frameData(54, 1),
              self.frameData(52, 1),
              self.frameData(53, 1),
              self.frameData(54, 1),
              self.frameData(52, 1),
              self.frameData(53, 1),
              self.frameData(54, 1),
              self.frameData(52, 1),
              self.frameData(53, 1),
              self.frameData(54, 1),
              self.frameData(8, 2),
              self.frameData(8, 5)]
        t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 1, 17, 'airLike')] ]
        self.moves['upAirB'].append(f, t)
        self.moves['upAirB'].canDI = False
        self.moves['upAirB'].reversable = True
        for i in range(len(self.moves['upAirB'].frames)):
            self.moves['upAirB'].frames[i].setVelY = -12.0
            self.moves['upAirB'].frames[i].setVelX = 10.0
        self.moves['upAirB'].frames[0].setVelY = 0
        self.moves['upAirB'].frames[0].setVelX = 0
        self.moves['upAirB'].frames[19].setVelY = 0
        self.moves['upAirB'].frames[19].setVelX = None
        self.moves['upAirB'].frames[20].setVelY = None
        self.moves['upAirB'].frames[20].setVelX = None

    def createDownAirB(self):
        f = [ self.frameData(55, 5),
              self.frameData(56, 1),
              self.frameData(57, 1),
              self.frameData(58, 1),
              self.frameData(56, 1),
              self.frameData(57, 1),
              self.frameData(58, 1),
              self.frameData(56, 1),
              self.frameData(57, 1),
              self.frameData(58, 1),
              self.frameData(56, 1),
              self.frameData(57, 1),
              self.frameData(58, 1),
              self.frameData(56, 1),
              self.frameData(57, 1),
              self.frameData(58, 1),
              self.frameData(58, 1),
              self.frameData(56, 1),
              self.frameData(57, 1),
              self.frameData(58, 1)]
        
        t = [ ['land', move.Transition(None, None, None, None, 'downBAirLag')] ]
        
        self.moves['downAirB'].append(f, t)
        self.moves['downAirB'].canDI = False
        self.moves['downAirB'].reversable = True
        for i in range(len(self.moves['downAirB'].frames)):
            self.moves['downAirB'].frames[i].ignoreSpeedCap = True
            self.moves['downAirB'].frames[i].ignoreFriction = True
            self.moves['downAirB'].frames[i].setVelY = 15.0
            self.moves['downAirB'].frames[i].setVelX = 17.0
        self.moves['downAirB'].frames[0].setVelY = 0
        self.moves['downAirB'].frames[0].setVelX = 0

        self.createLagDownBAir()

    def createLagDownBAir(self):
        f = [ self.frameData(9, 10) ]
        self.moves['downBAirLag'] = move.Move(f, [])
        self.moves['downBAirLag'].canDI = False
