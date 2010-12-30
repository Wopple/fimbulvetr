import os
import sys
import pygame

import incint
import boundint
import battlechar
import move

from constants import *

# DAMAGE STUN KNOCKBACK ANGLE

class Hare(battlechar.BattleChar):
    def __init__(self, name="Unnamed Hare", inSpecial=0):
        self.name = name
        self.speciesName = "Hare"
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

        self.speciesDesc = ("A speedy light-assault unit specializing in" +
                            " chasing down opponents, using hit-and-run" +
                            " tactics, and evading danger with acrobatic" +
                            " mobility.")

        if (inSpecial < 0) or (inSpecial >= len(self.superMoves)):
            inSpecial = 0
        self.currSuperMove = inSpecial

    def beginBattle(self):
        super(Hare, self).beginBattle()
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
        self.createMoveFlipping()
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
        self.createUpAirA()
        self.createUpAirB()
        self.createDownAirA()
        self.createDownAirB()

        self.createMoveStun1()
        self.createMoveStun2()
        self.createMoveStun3()

        self.createSuperMoves()

    def createSuperMoves(self):
        self.createSuperMove1()
        self.createSuperMove2()

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
        
        f = [ self.frameData(66, 1, r[0]),
              self.frameData(0, 1, r[0]),
              self.frameData(66, 1, r[0]) ]
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
        r = [
                [
                    (-1, -58, 10, -52),
                    (-1, -52, 12, -41),
                    (-7, -40, 16, -33),
                    (-14, -39, -3, -34),
                    (-6, -34, 10, -24),
                    (-3, -25, 12, -13),
                    (-5, -13, 10, 2)
                ]
            ]

        f = [ self.frameData(8, 2, r[0]) ]
        self.moves['air'].append(f, [])

    def createMoveFlipping(self):
        flippingSpeed = 3
        f = [ self.frameData(34, flippingSpeed),
              self.frameData(23, flippingSpeed),
              self.frameData(33, flippingSpeed),
              self.frameData(24, flippingSpeed),
              self.frameData(34, flippingSpeed),
              self.frameData(23, flippingSpeed),
              self.frameData(33, flippingSpeed),
              self.frameData(24, flippingSpeed) ]
        self.moves['flipping'].append(f, [])

    def createMoveAirLike(self):
        f = [ self.frameData(67, 1),
              self.frameData(8, 1),
              self.frameData(67, 1) ]
        r = [
                [
                    (-1, -58, 10, -52),
                    (-1, -52, 12, -41),
                    (-7, -40, 16, -33),
                    (-14, -39, -3, -34),
                    (-6, -34, 10, -24),
                    (-3, -25, 12, -13),
                    (-5, -13, 10, 2)
                ]
            ]
        
        f = [ self.frameData(67, 1, r[0]),
              self.frameData(8, 1, r[0]),
              self.frameData(67, 1, r[0]) ]
        self.moves['airLike'].append(f, [])
        self.moves['airLike'].frames[0].ignoreFriction = True
        self.moves['airLike'].frames[0].ignoreSpeedCap = True
        self.moves['airLike'].frames[1].ignoreFriction = True
        self.moves['airLike'].frames[1].ignoreSpeedCap = True

    def createMoveLanding(self):
        f = [ self.frameData(9, 3) ]
        r = [
                [
                    (4, -48, 17, -32),
                    (-2, -34, 16, -24),
                    (0, -26, 15, -14),
                    (12, -27, 21, -20),
                    (-13, -41, -1, -33),
                    (-1, -17, 19, -7),
                    (-10, -8, 0, -1),
                    (12, -8, 23, 2)
                ]
            ]
        f = [ self.frameData(9, 3, r[0]) ]
        self.moves['landing'].append(f, [])

    def createMoveJumping(self):
        f = [ self.frameData(9, 2) ]
        r = [
                [
                    (4, -48, 17, -32),
                    (-2, -34, 16, -24),
                    (0, -26, 15, -14),
                    (12, -27, 21, -20),
                    (-13, -41, -1, -33),
                    (-1, -17, 19, -7),
                    (-10, -8, 0, -1),
                    (12, -8, 23, 2)
                ]
            ]
        f = [ self.frameData(9, 3, r[0]) ]
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
                    (22, -34, 52, -20, 40, 40, 4, 0, [], 2),
                    (22, -34, 52, -20, 40, 40, 4, 0, [], 2)
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
                    (22, -34, 52, -20, 40, 60, 8, 8, [], 2),
                    (22, -34, 52, -20, 40, 60, 8, 8, [], 2)
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
        r = [
                [
                    (2, -52, 18, -35),
                    (-1, -35, 21, 2)
                ],
                [
                    (14, -54, 28, -38),
                    (10, -38, 42, -19),
                    (13, -20, 25, 0),
                    (28, -54, 29, -39)
                ],
                [
                    (16, -62, 31, -47),
                    (14, -48, 45, -30),
                    (42, -42, 56, -29),
                    (7, -43, 16, -33),
                    (20, -32, 30, -10),
                    (15, -12, 23, 1),
                    (17, -19, 26, -6)
                ],
                [
                    (11, -58, 29, -46),
                    (10, -45, 42, -28),
                    (42, -45, 64, -33),
                    (21, -28, 33, -10),
                    (15, -11, 23, -1),
                    (18, -19, 26, -7),
                    (11, -46, 29, -45)
                ],
                [
                    (2, -61, 18, -45),
                    (1, -45, 22, -18),
                    (9, -18, 19, -1)
                ]
            ]
        dam1 = 80
        stun1 = 60
        force1 = 15
        angle1 = 30
        h = [
                [
                    (22, -43, 56, -27, dam1, stun1, force1, angle1, [], 0),
                    (21, -33, 35, -21, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (39, -47, 67, -36, dam1, stun1, force1, angle1, [], 0),
                    (30, -42, 58, -32, dam1, stun1, force1, angle1, [], 0),
                    (25, -37, 47, -25, dam1, stun1, force1, angle1, [], 0),
                    (54, -50, 70, -42, dam1, stun1, force1, angle1, [], 0)
                ]
            ]

        f = [ self.frameData(46, 3, r[0]),
              self.frameData(47, 1, r[1]),
              self.frameData(48, 1, r[2], h[0]),
              self.frameData(49, 5, r[3], h[1]),
              self.frameData(50, 6, r[4]) ]
        self.moves['jabB'].append(f, [])
        self.moves['jabB'].canDI = False

    def createDashAttackA(self):
        r = [
                [
                    (-3, -50, 13, -35),
                    (-12, -47, -7, -43),
                    (-10, -45, -4, -38),
                    (-7, -41, 9, -32),
                    (-9, -32, 7, -19),
                    (4, -35, 14, -27),
                    (-27, -21, 7, -13),
                    (1, -16, 10, -6),
                    (5, -10, 17, 1),
                    (-14, -49, -9, -44)
                ],
                [
                    (17, -52, 37, -35),
                    (29, -59, 54, -43),
                    (4, -37, 30, -21),
                    (12, -23, 21, 1),
                    (20, -22, 37, -14),
                    (30, -18, 46, -12)
                ],
                [
                    (29, -46, 44, -33),
                    (16, -42, 29, -34),
                    (24, -37, 42, -15),
                    (40, -35, 49, -26),
                    (47, -40, 62, -23),
                    (54, -45, 71, -23),
                    (69, -40, 75, -23),
                    (74, -32, 77, -21),
                    (59, -50, 71, -44),
                    (24, -15, 45, -7),
                    (20, -9, 25, -4),
                    (16, -6, 22, -1),
                    (12, -3, 19, 1),
                    (41, -9, 47, 1),
                    (44, -3, 54, 1),
                    (30, -50, 44, -46)
                ],
                [
                    (36, -44, 50, -31),
                    (22, -47, 28, -41),
                    (26, -44, 30, -38),
                    (28, -41, 33, -35),
                    (30, -38, 39, -29),
                    (31, -34, 50, -12),
                    (46, -24, 51, -14),
                    (27, -24, 49, -5),
                    (21, -8, 27, -3),
                    (14, -4, 24, 1),
                    (43, -4, 54, 1),
                    (37, -48, 49, -42)
                ],
                [
                    (36, -44, 50, -31),
                    (22, -47, 28, -41),
                    (26, -44, 30, -38),
                    (28, -41, 33, -35),
                    (30, -38, 39, -29),
                    (31, -32, 47, -15),
                    (27, -23, 50, -6),
                    (21, -9, 29, -3),
                    (17, -5, 25, 0),
                    (13, -2, 22, 1),
                    (43, -6, 55, 1),
                    (37, -47, 49, -44)
                ],
                [
                    (30, -49, 46, -33),
                    (18, -33, 50, -20),
                    (23, -20, 48, -8),
                    (19, -8, 27, -4),
                    (14, -4, 23, 1),
                    (42, -8, 50, 0),
                    (45, -4, 57, 2)
                ],
                [
                    (8, -52, 27, -37),
                    (13, -37, 27, -22),
                    (27, -37, 35, -29),
                    (10, -26, 26, -15),
                    (25, -22, 30, -15),
                    (13, -15, 20, 0),
                    (14, 0, 18, 1),
                    (20, -15, 27, -8)
                ]
            ]
        dam1 = 150
        stun1 = 120
        force1 = 24
        angle1 = 45
        freeze1 = 5
        h = [
                [
                    (19, -62, 35, -36, dam1, stun1, force1, angle1, [], freeze1),
                    (34, -62, 41, -41, dam1, stun1, force1, angle1, [], freeze1),
                    (41, -60, 46, -45, dam1, stun1, force1, angle1, [], freeze1),
                    (46, -58, 51, -47, dam1, stun1, force1, angle1, [], freeze1),
                    (50, -54, 56, -49, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (41, -35, 53, -26, dam1, stun1, force1, angle1, [], freeze1),
                    (46, -40, 65, -24, dam1, stun1, force1, angle1, [], freeze1),
                    (53, -46, 71, -22, dam1, stun1, force1, angle1, [], freeze1),
                    (59, -50, 77, -22, dam1, stun1, force1, angle1, [], freeze1),
                    (64, -54, 73, -49, dam1, stun1, force1, angle1, [], freeze1),
                    (75, -45, 81, -19, dam1, stun1, force1, angle1, [], freeze1),
                    (78, -39, 84, -22, dam1, stun1, force1, angle1, [], freeze1),
                    (62, -22, 75, -20, dam1, stun1, force1, angle1, [], freeze1)
                ]
            ]
        f = [ self.frameData(59, 3, r[0]),
              self.frameData(59, 2, r[0]),
              self.frameData(59, 4, r[0]),
              self.frameData(60, 1, r[1], h[0]),
              self.frameData(61, 1, r[2], h[1]),
              self.frameData(62, 2, r[3]),
              self.frameData(63, 5, r[4]),
              self.frameData(64, 2, r[5]),
              self.frameData(65, 2, r[6]) ]
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
        r = [
                [
                    (9, -37, 32, -20),
                    (-1, -29, 27, -11),
                    (-8, -21, 24, 3),
                    (-23, -5, -5, 1)
                ]
            ]
        h = [
                [
                    [48, -39, 57, -30],
                    [53, -35, 66, -15],
                    [48, -18, 58, -9],
                    [36, -36, 56, -12],
                    [28, -32, 43, -16]
                ],
                [
                    [-18, -44, 35, -37],
                    [19, -41, 46, -34]
                ]
            ]
        h[0] = [i + [40, 60, 30, 45, [], 0] for i in h[0]]
        h[1] = [i + [40, 60, 30, 135, [], 0] for i in h[1]]
        f = [ self.frameData(25, 2, r[0]),
              self.frameData(26, 2, r[0], h[0]),
              self.frameData(27, 3, r[0], h[1]),
              self.frameData(28, 10, r[0])]
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
        r = [
                [
                    (-7, -58, 11, -38),
                    (-21, -53, -1, -41),
                    (-4, -40, 19, -32),
                    (-9, -33, 10, -20),
                    (-3, -22, 11, -8),
                    (-9, -9, 6, 0),
                    (-5, -1, 14, 7)
                ],
                [
                    (-6, -64, 13, -47),
                    (-4, -48, 12, -14),
                    (-11, -40, -1, -26),
                    (-10, -16, 11, 1)
                ],
                [
                    (-4, -62, 15, -46),
                    (-18, -49, 23, -34),
                    (-11, -38, 10, -13),
                    (-14, -16, 6, -1)
                ],
                [
                    (-1, -62, 16, -45),
                    (-17, -50, 14, -41),
                    (-10, -42, 14, -28),
                    (12, -37, 21, -29),
                    (16, -32, 22, -27),
                    (-8, -29, 7, -13),
                    (-18, -18, 4, -1)
                ],
                [
                    (-2, -57, 16, -39),
                    (-18, -44, 14, -34),
                    (-11, -35, 21, -21),
                    (-7, -23, 8, -8),
                    (-16, -12, 5, 5)
                ],
            ]
        dam1 = 80
        stun1 = 20
        force1 = 14
        angle1 = 20
        h = [
                [
                    (-16, -74, 9, -49, dam1, stun1, force1, angle1, [], 0),
                    (2, -77, 14, -52, dam1, stun1, force1, angle1, [], 0),
                    (11, -75, 19, -56, dam1, stun1, force1, angle1, [], 0),
                    (16, -73, 24, -60, dam1, stun1, force1, angle1, [], 0),
                    (23, -71, 28, -62, dam1, stun1, force1, angle1, [], 0),
                    (25, -67, 30, -63, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (4, -71, 33, -45, dam1, stun1, force1, angle1, [], 0),
                    (25, -68, 39, -38, dam1, stun1, force1, angle1, [], 0),
                    (36, -63, 46, -22, dam1, stun1, force1, angle1, [], 0),
                    (10, -45, 37, -30, dam1, stun1, force1, angle1, [], 0),
                    (18, -30, 37, -25, dam1, stun1, force1, angle1, [], 0),
                    (28, -26, 44, -14, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (13, -32, 30, -25, dam1, stun1, force1, angle1, [], 0),
                    (16, -25, 34, -22, dam1, stun1, force1, angle1, [], 0),
                    (19, -22, 37, -19, dam1, stun1, force1, angle1, [], 0),
                    (22, -19, 40, -16, dam1, stun1, force1, angle1, [], 0),
                    (24, -16, 42, -12, dam1, stun1, force1, angle1, [], 0)
                ]
            ]
        f = [ self.frameData(14, 3, r[0]),
              self.frameData(15, 2, r[0], h[0]),
              self.frameData(16, 2, r[0], h[1]),
              self.frameData(17, 3, r[0], h[2]),
              self.frameData(18, 3, r[0]) ]
        self.moves['neutralAirA'].append(f, [])
        self.moves['neutralAirA'].reversable = True

    def createNeutralAirB(self):
        r = [
                [
                    (1, -61, 18, -45),
                    (-12, -47, 21, -36),
                    (-5, -36, 16, -19),
                    (-17, -28, -5, -20),
                    (4, -20, 15, -11),
                    (-3, -11, 8, -2),
                    (5, -6, 13, 0)
                ],
                [
                    (-12, -59, 7, -43),
                    (-15, -40, -6, -30),
                    (-8, -45, 19, -25),
                    (19, -46, 31, -31),
                    (31, -44, 38, -39),
                    (0, -25, 13, 5),
                    (27, -50, 37, -44),
                    (37, -47, 41, -40)
                ],
                [
                    (-10, -60, 8, -44),
                    (-17, -41, -5, -32),
                    (-7, -45, 19, -25),
                    (19, -37, 44, -28),
                    (-2, -25, 11, 5)
                ],
                [
                    (-2, -58, 17, -44),
                    (0, -44, 18, -18),
                    (-14, -43, -3, -31),
                    (-8, -34, 2, -26),
                    (5, -18, 15, 7)
                ],
                [
                    (-11, -59, 6, -44),
                    (-11, -46, 13, -37),
                    (-4, -37, 19, -25),
                    (18, -42, 27, -33),
                    (19, -34, 23, -31),
                    (22, -46, 35, -37),
                    (25, -49, 35, -46),
                    (34, -48, 37, -45),
                    (34, -47, 40, -41),
                    (-3, -25, 9, 4),
                    (35, -44, 41, -39)
                ],
                [
                    (-9, -58, 8, -44),
                    (-9, -45, 14, -39),
                    (-3, -40, 15, -24),
                    (14, -35, 31, -28),
                    (27, -38, 45, -32),
                    (-4, -23, 5, 4),
                    (-3, -24, 12, -22)
                ],
                [
                    (-3, -56, 15, -40),
                    (-15, -42, 19, -31),
                    (-7, -31, 11, -24),
                    (-4, -24, 14, -11),
                    (-4, -11, 13, -4),
                    (-8, -7, 5, 5),
                    (3, 0, 14, 5)
                ]
            ]
        dam1 = 30
        stun1 = 5
        force1 = 6
        angle1 = 80
        freeze1 = 3
        dam2 = 50
        stun2 = 60
        force2 = 14
        angle2 = 25
        freeze2 = 2
        h = [
                [
                    (26, -50, 43, -40, dam1, stun1, force1, angle1, [], freeze1),
                    (20, -45, 36, -36, dam1, stun1, force1, angle1, [], freeze1),
                    (13, -40, 28, -33, dam1, stun1, force1, angle1, [], freeze1),
                    (8, -37, 21, -30, dam1, stun1, force1, angle1, [], freeze1),
                    (8, -34, 16, -28, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (8, -35, 26, -26, dam1, stun1, force1, angle1, [], freeze1),
                    (20, -37, 35, -31, dam1, stun1, force1, angle1, [], freeze1),
                    (30, -39, 45, -33, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (26, -50, 43, -40, dam2, stun2, force2, angle2, [], freeze2),
                    (20, -45, 36, -36, dam2, stun2, force2, angle2, [], freeze2),
                    (13, -40, 28, -33, dam2, stun2, force2, angle2, [], freeze2),
                    (8, -37, 21, -30, dam2, stun2, force2, angle2, [], freeze2),
                    (8, -34, 16, -28, dam2, stun2, force2, angle2, [], freeze2)
                ],
                [
                    (8, -35, 26, -26, dam2, stun2, force2, angle2, [], freeze2),
                    (20, -37, 35, -31, dam2, stun2, force2, angle2, [], freeze2),
                    (30, -39, 45, -33, dam2, stun2, force2, angle2, [], freeze2)
                ]
            ]
        f = [ self.frameData(35, 3, r[0]),
              self.frameData(36, 1, r[1], h[0]),
              self.frameData(37, 4, r[2], h[1]),
              self.frameData(38, 3, r[3]),
              self.frameData(39, 1, r[4], h[0]),
              self.frameData(40, 4, r[5], h[1]),
              self.frameData(35, 3, r[0]),
              self.frameData(36, 1, r[1], h[2]),
              self.frameData(37, 5, r[2], h[3]),
              self.frameData(8, 4, r[6])]
        self.moves['neutralAirB'].append(f, [])
        self.moves['neutralAirB'].canDI = False
        self.moves['neutralAirB'].reversable = True
        self.moves['neutralAirB'].frames[1].setVelYIfDrop = -3.0
        self.moves['neutralAirB'].frames[4].setVelYIfDrop = -1.5
        self.moves['neutralAirB'].frames[7].setVelYIfDrop = -1.5
        self.moves['neutralAirB'].frames[4].resetHitPotential = True
        self.moves['neutralAirB'].frames[7].resetHitPotential = True
        for i in range(len(self.moves['neutralAirB'].frames)):
            self.moves['neutralAirB'].frames[i].ignoreFriction = True

    def createUpAirA(self):
        r = [
                [
                    (-10, -56, 7, -41),
                    (-9, -41, 11, -33),
                    (-12, -33, 5, -14),
                    (0, -17, 11, 3),
                    (-9, -14, 0, 7)
                ],
                [
                    (-10, -56, 7, -41),
                    (-9, -41, 11, -33),
                    (-12, -33, 5, -14),
                    (0, -17, 11, 3),
                    (-9, -14, 0, 7),
                    (-2, -61, 9, -40),
                    (6, -39, 17, -31)
                ],
                [
                    (-17, -59, 8, -46),
                    (-11, -46, 7, -15),
                    (5, -40, 17, -32),
                    (-9, -17, 0, -11),
                    (-7, -12, 4, 7),
                    (3, -19, 14, 1)
                ],
                [
                    (-17, -59, 8, -46),
                    (-11, -46, 7, -15),
                    (5, -40, 17, -32),
                    (-9, -17, 0, -11),
                    (-7, -12, 4, 7),
                    (3, -19, 14, 1),
                    (-22, -52, -10, -40)
                ],
                [
                    (-16, -55, 3, -40),
                    (-25, -43, 16, -33),
                    (-12, -37, 7, -13),
                    (5, -20, 16, -1),
                    (-4, -14, 9, 6)
                ],
            ]
        h = [
                [
                    [-4, -75, 11, -58],
                    [4, -69, 17, -52],
                    [7, -55, 16, -42],
                    [3, -45, 12, -37]
                ],
                [
                    [-34, -71, -21, -61],
                    [-27, -63, -14, -53],
                    [-27, -75, 8, -68],
                    [3, -71, 14, -61],
                    [5, -64, 16, -47],
                    [-24, -71, 10, -53]
                ],
                [
                    [-44, -54, -19, -40],
                    [-41, -60, -16, -52],
                    [-38, -64, -6, -56],
                    [-33, -69, 8, -59],
                    [-27, -73, 7, -68],
                    [-20, -76, 3, -71],
                    [4, -70, 11, -64],
                    [-24, -60, -7, -51],
                    [-24, -54, -12, -47],
                    [-11, -63, 1, -56]
                ],
                [
                    [-46, -47, -18, -35]
                ],
            ]
        h[0] = [i + [50, 60, 25, 60, [], 0] for i in h[0]]
        h[1] = [i + [50, 60, 25, 90, [], 0] for i in h[1]]
        h[2] = [i + [50, 60, 25, 120, [], 0] for i in h[2]]
        h[3] = [i + [50, 60, 25, 180, [], 0] for i in h[3]]
        f = [ self.frameData(75, 4, r[0]),
              self.frameData(76, 1, r[1], h[0]),
              self.frameData(77, 1, r[2], h[1]),
              self.frameData(78, 1, r[3], h[2]),
              self.frameData(79, 2, r[4], h[3]),
              self.frameData(80, 5, r[4]) ]

        self.moves['upAirA'].append(f, [])

    def createUpAirB(self):
        r = [
                [
                    (-11, -59, 8, -44),
                    (-20, -50, 19, -38),
                    (-11, -39, 9, -18),
                    (4, -24, 12, -18),
                    (-21, -20, -11, -9),
                    (-5, -19, 10, -5)
                ],
                [
                    (-9, -60, 9, -45),
                    (-18, -50, 12, -42),
                    (-8, -42, 11, -34),
                    (-11, -36, 9, -23),
                    (5, -28, 14, -21),
                    (-8, -26, 8, -13),
                    (-21, -24, -5, -19),
                    (-21, -22, -14, -12)
                ],
                [
                    (-2, -58, 15, -41),
                    (-15, -43, 19, -31),
                    (-7, -32, 12, -22),
                    (-4, -24, 15, -9),
                    (-9, -10, 13, 7)
                ],
            ]
        h = [
                [
                    [-35, -68, -18, -58],
                    [-27, -72, -7, -64],
                    [-18, -77, 1, -68],
                    [-4, -77, 21, -69],
                    [13, -74, 26, -64],
                    [20, -69, 30, -35],
                    [19, -37, 27, -28],
                    [13, -32, 22, -24],
                    [8, -29, 18, -20],
                    [1, -24, 13, -16],
                    [-4, -20, 5, -13],
                    [-19, -70, 22, -56],
                    [4, -68, 21, -28]
                ],
            ]

        h[0] = [i + [28, 40, 20, 60, [], 3] for i in h[0]]
        f = [ self.frameData(51, 3, r[0]),
              self.frameData(52, 1, r[1], h[0]),
              self.frameData(53, 1, r[1], h[0]),
              self.frameData(54, 1, r[1], h[0]),
              self.frameData(52, 1, r[1], h[0]),
              self.frameData(53, 1, r[1], h[0]),
              self.frameData(54, 1, r[1], h[0]),
              self.frameData(52, 1, r[1], h[0]),
              self.frameData(53, 1, r[1], h[0]),
              self.frameData(54, 1, r[1], h[0]),
              self.frameData(52, 1, r[1], h[0]),
              self.frameData(53, 1, r[1], h[0]),
              self.frameData(54, 1, r[1], h[0]),
              self.frameData(52, 1, r[1], h[0]),
              self.frameData(53, 1, r[1], h[0]),
              self.frameData(54, 1, r[1], h[0]),
              self.frameData(52, 1, r[1], h[0]),
              self.frameData(53, 1, r[1], h[0]),
              self.frameData(54, 1, r[1], h[0]),
              self.frameData(8, 2, r[1], h[0]),
              self.frameData(8, 5, r[2])]
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

        self.moves['upAirB'].frames[4].resetHitPotential = True
        self.moves['upAirB'].frames[7].resetHitPotential = True
        self.moves['upAirB'].frames[10].resetHitPotential = True
        self.moves['upAirB'].frames[13].resetHitPotential = True
        self.moves['upAirB'].frames[16].resetHitPotential = True
        self.moves['upAirB'].frames[19].resetHitPotential = True

    def createDownAirA(self):
        r = [
                [
                    (-11, -43, 3, -31),
                    (-10, -48, 1, -43),
                    (-17, -34, 5, -28),
                    (-11, -28, 7, -11),
                    (-8, -11, 5, -6),
                    (0, -6, 5, -1)
                ],
                [
                    (-11, -43, 3, -31),
                    (-10, -48, 1, -43),
                    (-18, -30, 14, -24),
                    (-10, -24, 5, -13),
                    (-6, -13, 5, -7)
                ],
                [
                    (-11, -43, 3, -31),
                    (-10, -48, 1, -43),
                    (-16, -34, -10, -28),
                    (-11, -32, 6, -11),
                    (-6, -11, -1, -8)
                ]
            ]

        h = [
                [
                    (-1, -9, 7, 18, 75, 105, 23, 270, [], 4)
                ]
            ]

                

                

        
        f = [ self.frameData(85, 8, r[0]),
              self.frameData(82, 1, r[1]),
              self.frameData(83, 1, r[2], h[0]),
              self.frameData(84, 6, r[2], h[0]),
              self.frameData(84, 8, r[2]) ]

        t = [['land', move.Transition(None, None, None, None, 'downAAirLag')]]

        

        self.moves['downAirA'].append(f, t)
        self.moves['downAirA'].frames[0].addVelYIfDrop = -0.6

        self.createLagDownAAir()

    def createLagDownAAir(self):
        r = [
                [
                    (-9, -27, 6, -15),
                    (-14, -16, 8, -10),
                    (-7, -10, 9, 5)
                ]
            ]

        
        f = [ self.frameData(86, 12, r[0]) ]

        self.moves['downAAirLag'] = move.Move(f, [])
        self.moves['downAAirLag'].canDI = False
        

    def createDownAirB(self):
        r = [
                [
                    (-6, -57, 12, -43),
                    (-9, -43, 15, -36),
                    (-4, -36, 12, -31),
                    (-7, -31, 9, -26),
                    (-4, -26, 19, -16),
                    (4, -16, 17, -12),
                    (-2, -12, 14, -5)
                ],
                [
                    (1, -54, 18, -39),
                    (-1, -39, 30, -29),
                    (-2, -29, 13, -23),
                    (-5, -23, 18, -15),
                    (-6, -17, 4, -12),
                    (-1, -14, 8, -8),
                    (12, -21, 23, -13),
                    (16, -18, 29, -11),
                    (22, -15, 33, -8),
                    (26, -13, 42, -6)
                ],
            ]
        h = [
                [
                    [-6, -43, 4, -34],
                    [-1, -38, 19, -21],
                    [6, -32, 26, -17],
                    [12, -29, 34, -13],
                    [16, -26, 40, -10],
                    [19, -24, 44, -7],
                    [25, -19, 48, -2]
                ],
            ]
        h[0] = [i + [28, 60, 25, 315, [], 2] for i in h[0]]
        f = [ self.frameData(55, 6, r[0]),
              self.frameData(56, 1, r[1], h[0]),
              self.frameData(57, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0]),
              self.frameData(56, 1, r[1], h[0]),
              self.frameData(57, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0]),
              self.frameData(56, 1, r[1], h[0]),
              self.frameData(57, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0]),
              self.frameData(56, 1, r[1], h[0]),
              self.frameData(57, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0]),
              self.frameData(56, 1, r[1], h[0]),
              self.frameData(57, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0]),
              self.frameData(56, 1, r[1], h[0]),
              self.frameData(57, 1, r[1], h[0]),
              self.frameData(58, 1, r[1], h[0])]
        
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

    def createMoveStun1(self):
        r = [
                [
                    (-15, -46, -3, -35),
                    (-16, -50, -6, -46),
                    (-12, -35, 1, -17),
                    (-22, -31, -9, -27),
                    (-11, -19, -5, -1),
                    (-7, -19, 7, -12),
                    (2, -13, 9, 0),
                    (6, -1, 17, 2)
                ]
            ]

        f = [ self.frameData(68, 8, r[0]) ]

        self.moves['stun1'].append(f, [])

        for i in range(len(self.moves['stun1'].frames)):
            self.moves['stun1'].frames[i].ignoreSpeedCap = True

    def createMoveStun2(self):
        r = [
                [
                    (-7, -46, 4, -35),
                    (-4, -49, 4, -45),
                    (-9, -36, 0, -29),
                    (-14, -33, -8, -29),
                    (-14, -29, 0, -16),
                    (-2, -33, 12, -29),
                    (-13, -17, -3, -8),
                    (-6, -19, 4, -9),
                    (-7, -8, 2, 2),
                    (-1, -11, 10, 1),
                    (-5, -11, 2, -7)
                ]
            ]

        f = [ self.frameData(69, 14, r[0]) ]

        self.moves['stun2'].append(f, [])

        for i in range(len(self.moves['stun2'].frames)):
            self.moves['stun2'].frames[i].ignoreSpeedCap = True

    def createMoveStun3(self):
        r = [
                [
                    (-12, -50, -3, -48),
                    (-12, -48, 1, -39),
                    (-10, -40, 2, -23),
                    (0, -36, 10, -33),
                    (-11, -24, 2, -19),
                    (-8, -20, 6, -14),
                    (-5, -14, -1, 5),
                    (-3, -17, 4, 2),
                    (1, -16, 9, -4),
                    (-6, 2, 10, 5),
                    (-1, 5, 4, 7)
                ],
                [
                    (0, -46, 13, -35),
                    (3, -49, 13, -46),
                    (-1, -35, 9, -28),
                    (-7, -27, 6, -21),
                    (-6, -31, 6, -27),
                    (2, -29, 7, -23),
                    (-8, -21, 8, -15),
                    (-3, -15, 13, -9),
                    (9, -9, 15, 0),
                    (5, -32, 14, -28),
                    (11, -30, 18, -27),
                    (11, -12, 19, 0),
                    (14, -5, 21, -2)
                ],
                [
                    (-5, -45, 8, -36),
                    (-5, -49, 6, -45),
                    (-5, -36, 6, -21),
                    (-7, -20, 8, -13),
                    (0, -14, 11, -12),
                    (8, -18, 12, -15),
                    (10, -17, 16, -10),
                    (13, -12, 20, -5),
                    (18, -10, 23, -4),
                    (5, -33, 14, -31)
                ],
                [
                    (-8, -45, 5, -35),
                    (-7, -35, 6, -20),
                    (-7, -20, 11, -12),
                    (8, -18, 18, -11),
                    (15, -12, 25, -7),
                    (15, -15, 21, -12),
                    (22, -13, 28, -8),
                    (20, -8, 27, -6)
                ],
                [
                    (-15, -42, 0, -34),
                    (-16, -46, -4, -42),
                    (-10, -34, -1, -32),
                    (-8, -32, 4, -23),
                    (-3, -34, 5, -32),
                    (-8, -24, 7, -16),
                    (-6, -17, 13, -13),
                    (2, -22, 13, -17),
                    (10, -21, 26, -16),
                    (9, -17, 28, -13),
                    (26, -20, 30, -14),
                    (4, -36, 10, -33)
                ]
            ]

        
        f = [ self.frameData(70, 10, r[0]),
              self.frameData(71, 2, r[1]),
              self.frameData(72, 1, r[2]),
              self.frameData(73, 1, r[3]),
              self.frameData(74, 12, r[4])]

        self.moves['stun3'].append(f, [])

        for i in range(len(self.moves['stun3'].frames)):
            self.moves['stun3'].frames[i].ignoreSpeedCap = True


    def createSuperMove1(self):
        n = "Blazing Ambush"
        
        d = ("A powerup effect that can be used at the beginning of battle" +
             " in order to deal additional damage for the first few moments" +
             " of the encounter.")
        
        s = move.SuperMove(n, d, [], [])

        self.superMoves.append(s)

    def createSuperMove2(self):
        n = "Lightning Strike"
        
        d = ("A heavily damaging assault of steel and electricity that is" +
             " initiated with a slash at close range.")
        
        s = move.SuperMove(n, d, [], [])

        self.superMoves.append(s)
