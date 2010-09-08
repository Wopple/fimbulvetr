import os
import sys
import pygame

import incint
import boundint
import battlechar
import move

from constants import *

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
        f = [ self.frameData(8, 2) ]
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
                    (22, -34, 52, -20, 40, 40, 8, 8, []),
                    (22, -34, 52, -20, 40, 40, 4, 0, [])
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
                    (22, -34, 52, -20, 40, 60, 8, 8, []),
                    (22, -34, 52, -20, 40, 60, 11, 0, [])
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
        h = [
                [
                    (22, -43, 56, -27, 60, 60, 6, 45, []),
                    (21, -33, 35, -21, 60, 60, 6, 45, [])
                ],
                [
                    (39, -47, 67, -36, 60, 60, 6, 45, []),
                    (30, -42, 58, -32, 60, 60, 6, 45, []),
                    (25, -37, 47, -25, 60, 60, 6, 45, []),
                    (54, -50, 70, -42, 60, 60, 6, 45, [])
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
        h = [
                [
                    (19, -62, 35, -36, dam1, stun1, force1, angle1, []),
                    (34, -62, 41, -41, dam1, stun1, force1, angle1, []),
                    (41, -60, 46, -45, dam1, stun1, force1, angle1, []),
                    (46, -58, 51, -47, dam1, stun1, force1, angle1, []),
                    (50, -54, 56, -49, dam1, stun1, force1, angle1, [])
                ],
                [
                    (41, -35, 53, -26, dam1, stun1, force1, angle1, []),
                    (46, -40, 65, -24, dam1, stun1, force1, angle1, []),
                    (53, -46, 71, -22, dam1, stun1, force1, angle1, []),
                    (59, -50, 77, -22, dam1, stun1, force1, angle1, []),
                    (64, -54, 73, -49, dam1, stun1, force1, angle1, []),
                    (75, -45, 81, -19, dam1, stun1, force1, angle1, []),
                    (78, -39, 84, -22, dam1, stun1, force1, angle1, []),
                    (62, -22, 75, -20, dam1, stun1, force1, angle1, [])
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
        h = [
                [
                    (-16, -74, 9, -49, 65, 15, 12, 20, []),
                    (2, -77, 14, -52, 65, 15, 12, 20, []),
                    (11, -75, 19, -56, 65, 15, 12, 20, []),
                    (16, -73, 24, -60, 65, 15, 12, 20, []),
                    (23, -71, 28, -62, 65, 15, 12, 20, []),
                    (25, -67, 30, -63, 65, 15, 12, 20, [])
                ],
                [
                    (4, -71, 33, -45, 65, 15, 12, 20, []),
                    (25, -68, 39, -38, 65, 15, 12, 20, []),
                    (36, -63, 46, -22, 65, 15, 12, 20, []),
                    (10, -45, 37, -30, 65, 15, 12, 20, []),
                    (18, -30, 37, -25, 65, 15, 12, 20, []),
                    (28, -26, 38, -20, 65, 15, 12, 20, [])
                ],
                [
                    (16, -34, 25, -24, 65, 15, 12, 20, []),
                    (22, -28, 27, -22, 65, 15, 12, 20, []),
                    (25, -25, 29, -20, 65, 15, 12, 20, []),
                    (27, -23, 31, -18, 65, 15, 12, 20, []),
                    (28, -22, 33, -16, 65, 15, 12, 20, []),
                    (30, -20, 35, -14, 65, 15, 12, 20, [])
                ]
            ]
        f = [ self.frameData(14, 3, r[0]),
              self.frameData(15, 1, r[0], h[0]),
              self.frameData(16, 1, r[0], h[1]),
              self.frameData(17, 3, r[0], h[2]),
              self.frameData(18, 5, r[0]) ]
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

    def createMoveStun1(self):
        f = [ self.frameData(68, 5) ]

        self.moves['stun1'].append(f, [])

        for i in range(len(self.moves['stun1'].frames)):
            self.moves['stun1'].frames[i].ignoreSpeedCap = True

    def createMoveStun2(self):
        f = [ self.frameData(69, 8) ]

        self.moves['stun2'].append(f, [])

        for i in range(len(self.moves['stun2'].frames)):
            self.moves['stun2'].frames[i].ignoreSpeedCap = True

    def createMoveStun3(self):
        f = [ self.frameData(70, 8),
              self.frameData(71, 5),
              self.frameData(72, 2),
              self.frameData(73, 2),
              self.frameData(74, 10)]

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
