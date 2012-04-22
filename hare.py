import os
import sys
import pygame

import incint
import boundint
import battlechar
import move

import colorswapper

from constants import *

# DAMAGE STUN KNOCKBACK ANGLE

class Hare(battlechar.BattleChar):
    def __init__(self, name="Unnamed Hare", inSuper=0):
        self.name = name
        self.speciesName = "Hare"
        self.spriteSet = HARE_IMAGES
        self.superIcons = HARE_SUPER_ICONS
        self.walkVelMax = 7.5
        self.dashVelMax = 26.0
        self.runVelMax = 13.0
        self.walkAccel = 2.5
        self.dashAccel = 12.0
        self.groundFriction = 2.2
        self.airAccel = 1.2
        self.airVelMax = 7.3
        self.airFriction = 0.9
        self.airFrictionStunned = self.airFriction * 0.3
        self.vertAccel = 1.4
        self.vertVelMax = 14.5
        self.jumpVel = -24.0
        self.youIconHeight = 75
        self.blockFXPoints = [ (9, -35), (33, -32), (9, -35) ]
        self.hareEnergy = boundint.BoundInt(0, HARE_ENERGY_MAX, 0)
        self.prevEnergy = self.hareEnergy.value
        self.energyDelayTick = HARE_ENERGY_DELAY
        self.energy = self.hareEnergy
        super(Hare, self).__init__(850, 13)
        self.initSpecMoves()

        self.speciesDesc = ("A speedy light-assault unit specializing in" +
                            " close-range combat and acrobatic mobility." +
                            "  Can quickly change distance in combat to" +
                            " close in for an offensive rush or back off" +
                            " defensively as needed.")

        self.setSuperValue(inSuper)
        

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
        self.createMoveWalking()
        self.createMoveDashing()
        self.createMoveRunning()
        self.createMoveAir()
        self.createMoveFlipping()
        self.createMoveAirLike()
        self.createMoveJumpingLike()
        self.createMoveLanding()
        self.createMoveJumping()
        self.createMoveDucking()
        self.createMoveJabA()
        self.createMoveJabB()
        self.createMoveDashAttackA()
        self.createMoveDashAttackB()
        self.createMoveDownA()
        self.createMoveDownB()
        self.createMoveUpA()
        self.createMoveUpB()
        self.createMoveNeutralAirA()
        self.createMoveNeutralAirB()
        self.createMoveUpAirA()
        self.createMoveUpAirB()
        self.createMoveDownAirA()
        self.createMoveDownAirB()
        self.createMoveDroppingThrough()
        
        self.createAirDash()

        self.createMoveGrabbing()
        self.createMoveGrabHold()
        self.createMoveGrabbed()
        self.createMoveGrabbed2()
        self.createMoveGrabRelease()
        self.createMoveGrabbedRelease()

        self.createMoveThrowBackward()
        self.createMoveThrowForward()

        self.createMoveStun1()
        self.createMoveStun2()
        self.createMoveStun3()
        self.createMoveStun4()

        self.createMoveDeadFalling()
        self.createMoveDeadGroundHit()
        self.createMoveDeadLaying()

        self.createMoveGroundHit()
        self.createMoveStandUp()
        self.createMoveStandForward()
        self.createMoveStandBackward()
        self.createMoveStandAttack()

        self.createMoveTeching()
        self.createMoveTechUp()
        self.createMoveTechForward()
        self.createMoveTechBackward()

        self.createMoveBlock()
        self.createMoveLowBlock()
        self.createMoveAirBlock()

        self.createSuperMoves()

    def createSuperMoves(self):
        self.createSuperMove1()
        #self.createSuperMove2()

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

    def createMoveBlock(self):

        r = [
                [
                    (-9, -47, 6, -32),
                    (-11, -34, 5, -15),
                    (-21, -32, -10, -24),
                    (3, -38, 11, -24),
                    (3, -24, 16, -7),
                    (-11, -16, -1, 3)
                ]
            ]

        b = [
                [
                    (15, -56, 17, -25),
                    (6, -50, 16, -48)
                ]
            ]


        f = [ self.frameData(81, 2, r[0], [], b[0]) ]

        self.moves['blocking'].append(f, [])

    def createMoveLowBlock(self):

        r = [
                [
                    (16, -38, 31, -24),
                    (3, -27, 29, -19),
                    (-2, -25, 13, -15),
                    (-7, -18, -1, 0),
                    (-3, -20, 11, -10),
                    (2, -12, 15, 1),
                    (-22, -5, -2, 0)
                ]
            ]

        b = [
                [
                   (32, -26, 34, 1),
                   (24, -11, 34, 1)
                ]
            ]


        f = [ self.frameData(108, 2, r[0], [], b[0]) ]

        self.moves['lowBlocking'].append(f, [])

    def createMoveAirBlock(self):

        r = [
                [
                    (-7, -50, 6, -37),
                    (-9, -37, 6, -16),
                    (5, -39, 9, -30),
                    (-20, -33, -6, -29),
                    (-16, -36, -7, -33),
                    (-9, -18, -2, 4),
                    (5, -24, 13, -18),
                    (8, -18, 11, -6),
                    (9, -8, 17, -4)
                ]
            ]

        b = [
                [
                    (11, -55, 17, 3),
                    (-4, -54, 16, -50)
                ]
            ]



        f = [ self.frameData(109, 2, r[0], [], b[0]) ]

        self.moves['airBlocking'].append(f, [])

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

    def createMoveWalking(self):
        
        r = [
                [
                    (-4, -49, 6, -44),
                    (-6, -44, 8, -34),
                    (-9, -35, 10, -28),
                    (-7, -28, 5, -16),
                    (-8, -17, -2, -11),
                    (1, -16, 8, -11),
                    (5, -11, 10, -7),
                    (8, -7, 13, -3),
                    (9, -3, 14, 1),
                    (11, -2, 22, 1),
                    (-9, -12, -6, -8),
                    (-12, -9, -8, -6),
                    (-14, -6, -11, -2),
                    (-14, -3, -4, 1)
                ],
                [
                    (-4, -49, 6, -44),
                    (-6, -44, 8, -34),
                    (-9, -35, 10, -28),
                    (-7, -28, 5, -16),
                    (-4, -16, 5, 1),
                    (-5, -2, 10, 1)
                ],
                [
                    (-4, -49, 6, -44),
                    (-6, -44, 8, -34),
                    (-9, -35, 10, -28),
                    (-6, -28, 6, -16),
                    (-7, -16, -2, -11),
                    (-8, -11, -5, -6),
                    (-10, -6, -6, 0),
                    (-9, -2, -2, 1),
                    (3, -15, 8, -12),
                    (4, -14, 8, -2),
                    (6, -6, 14, -2)
                ]

             ]
                    
        f = [self.frameData(149, 4, r[0]),
             self.frameData(150, 4, r[0]),
             self.frameData(151, 4, r[1]),
             self.frameData(152, 4, r[2]) ]
        
        self.moves['walking'].append(f, [])
        
    def createMoveDashing(self):
        
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
                ]
            ]
                    
        f = [self.frameData(2, 7, r[0])]
        
        self.moves['dashing'].append(f, [])
        
    def createMoveRunning(self):
        
        r = [
                [
                    (-5, -49, 11, -34),
                    (-5, -52, 9, -49),
                    (-5, -34, 10, -10),
                    (-18, -17, -2, -11),
                    (11, -16, 24, -11)
                ],
                [
                    (-5, -49, 11, -34),
                    (-5, -52, 9, -49),
                    (-3, -34, 5, -15),
                    (-2, -15, 6, 1)
                ],
                [
                    (-5, -49, 11, -34),
                    (-5, -52, 9, -49),
                    (-3, -34, 5, -15),
                    (6, -19, 14, -13),
                    (7, -15, 14, -4),
                    (-5, -15, 1, -10),
                    (-9, -11, -2, -6),
                    (-10, -7, -4, -2),
                    (-11, -4, -3, 2)
                ]
            ]
                    
        f = [self.frameData(3, 2, r[1]),
             self.frameData(4, 2, r[1]),
             self.frameData(5, 2, r[2]),
             self.frameData(6, 2, r[0]),
             self.frameData(7, 2, r[1]),
             self.frameData(161, 2, r[1]),
             self.frameData(162, 2, r[2]),
             self.frameData(2, 2, r[0])]
        
        self.moves['running'].append(f, [])

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
        
        t = [['doDash', move.Transition(2, HARE_ENERGY_USAGE, None, None, 'airDashing')]]
        
        self.moves['air'].append(f, t)
        
        self.moves['air'].transitions['attackBUpCharge'].var1 = 2
        self.moves['air'].transitions['attackBUpCharge'].var2 = HARE_ENERGY_USAGE
        
        self.moves['air'].transitions['attackBDown'].var1 = 2
        self.moves['air'].transitions['attackBDown'].var2 = HARE_ENERGY_USAGE

    def createMoveFlipping(self):
        r = [
                [
                    (-19, -20, -3, -10),
                    (-12, -10, -5, -1),
                    (-14, -32, 4, -19),
                    (-7, -22, 7, -13),
                    (-7, -15, 0, -12),
                    (0, -40, 17, -23)
                ],
                [
                    (-13, -35, 5, -22),
                    (-21, -32, -8, -26),
                    (-11, -24, 11, -15),
                    (0, -29, 12, -21),
                    (-2, -17, 18, -2)
                ],
                [
                    (-21, -19, -2, -3),
                    (-4, -27, 12, -10),
                    (-2, -35, 18, -25),
                    (9, -27, 16, -22),
                    (-7, -32, 1, -22),
                    (4, -43, 13, -35),
                    (-9, -26, 3, -18)
                ],
                [
                    (-19, -40, 0, -26),
                    (-15, -27, 5, -14),
                    (-6, -17, 12, -6),
                    (3, -25, 15, -12),
                    (12, -16, 21, -10)
                ]
            ]

        
        flippingSpeed = 3
        f = [ self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]),
              self.frameData(24, flippingSpeed, r[3]),
              self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]),
              self.frameData(24, flippingSpeed, r[3]) ]
        
        t = [['doDash', move.Transition(2, HARE_ENERGY_USAGE, None, None, 'airDashing')]]
        
        self.moves['flipping'].append(f, t)
        
        self.moves['flipping'].transitions['attackBUpCharge'].var1 = 2
        self.moves['flipping'].transitions['attackBUpCharge'].var2 = HARE_ENERGY_USAGE
        
        self.moves['flipping'].transitions['attackBDown'].var1 = 2
        self.moves['flipping'].transitions['attackBDown'].var2 = HARE_ENERGY_USAGE
        
    def createAirDash(self):
        
        f = [ self.frameData(159, 2),
              self.frameData(160, 1),
              self.frameData(159, 1),
              self.frameData(160, 1),
              self.frameData(159, 1),
              self.frameData(159, 8) ]
        
        t = [ ['exitFrame', move.Transition(-1, 0, None, None, 'air')],
             ['land', move.Transition(None, None, None, None, 'landing')],
             ['attackA', move.Transition(None, None, 5, 5, 'neutralAirA')],
             ['attackB', move.Transition(None, None, 5, 5, 'neutralAirB')],
             ['attackAUp', move.Transition(None, None, 5, 5, 'upAirA')],
             ['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 5, 5, 'upAirB')],
             ['attackADown', move.Transition(None, None, 5, 5, 'downAirA')],
             ['attackBDown', move.Transition(2, HARE_ENERGY_USAGE, 5, 5, 'downAirB')] ]
        
        self.moves['airDashing'] = move.Move(f, t)
        
        
        self.moves['airDashing'].frames[0].setVelX = 22
        self.moves['airDashing'].canDI = False
        
        for i in range(len(self.moves['airDashing'].frames)):
            self.moves['airDashing'].frames[i].setFrictionX = 1.0
            self.moves['airDashing'].frames[i].setVelY = 0
            self.moves['airDashing'].frames[i].ignoreSpeedCap = True
            
        self.moves['airDashing'].frames[0].fx.append(['airelementshockwave', (-20, -30), False])
            
            

    def createMoveAirLike(self):
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
        
    def createMoveJumpingLike(self):
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
        self.moves['jumpingLike'].append(f, [])

    def createMoveDucking(self):
        r = [
                [
                    (-1, -32, 16, -24),
                    (-7, -26, 24, -8),
                    (16, -9, 21, 1),
                    (-22, -4, -2, 0),
                    (-7, -9, -2, -3),
                    (2, -9, 15, 1),
                    (16, -34, 30, -23),
                    (16, -39, 28, -34)
                ]
            ]

        f = [ self.frameData(10, 2, r[0]) ]
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
                    (1, -36, 38, -20, 40, 40, 4, 0, [], 2),
                    (30, -40, 60, -16, 40, 40, 4, 0, [], 2),
                    (-4, -22, 30, -10, 40, 40, 4, 0, [], 2),
                    (-24, -43, 31, -33, 40, 40, 4, 0, [], 2)
                ]
            ]
                    
        f = [ self.frameData(41, 2, r[0]),
              self.frameData(42, 2, r[1], h[0]),
              self.frameData(43, 2, r[1]),
              self.frameData(43, 10, r[1])]
        t = [ ['attackA', move.Transition(None, None, 3, None, 'jab2')],
              ['attackAUp', move.Transition(None, None, 3, None, 'jab2')],
              ['attackADown', move.Transition(None, None, 3, None, 'jab2')]]
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
                    (1, -36, 38, -20, 45, 51, 8, 8, [], 2),
                    (30, -40, 60, -16, 45, 51, 8, 8, [], 2),
                    (-4, -22, 30, -10, 45, 51, 8, 8, [], 2),
                    (-24, -43, 31, -33, 45, 51, 8, 8, [], 2)
                ]
            ]
        
        f = [ self.frameData(43, 2, r[0]),
              self.frameData(44, 3, r[1], h[0]),
              self.frameData(45, 8, r[2]),
              self.frameData(45, 3, r[2])]
        t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 1, 2, 'idleLike')],
              ['attackB', move.Transition(0, 0, 1, 2, 'upB')],
              ['attackBUp', move.Transition(0, 0, 1, 2, 'upB')] ]
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
                ],
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
        dam1 = 110
        stun1 = 60
        force1 = 15
        angle1 = 30
        h = [
                [
                    (17, -28, 33, -21, dam1, stun1, force1, angle1, [], 0),
                    (25, -51, 63, -27, dam1, stun1, force1, angle1, [], 0)                ],
                [
                    (19, -37, 43, -21, dam1, stun1, force1, angle1, [], 0),
                    (28, -47, 58, -24, dam1, stun1, force1, angle1, [], 0),
                    (46, -56, 81, -28, dam1, stun1, force1, angle1, [], 0)
                ]
            ]

        f = [ self.frameData(46, 5, r[0]),
              self.frameData(47, 1, r[1]),
              self.frameData(48, 1, r[2], h[0]),
              self.frameData(49, 5, r[3], h[1]),
              self.frameData(50, 6, r[4]),
              self.frameData(0, 4, r[5])]
        self.moves['jabB'].append(f, [])
        self.moves['jabB'].canDI = False
        
    def createMoveDashAttackA(self):
        
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
                    (-13, -45, 1, -34),
                    (-14, -49, -1, -45),
                    (-19, -36, -6, -29),
                    (-9, -34, 5, -27),
                    (3, -32, 14, -27),
                    (-13, -29, 3, -19),
                    (-11, -20, 13, -9),
                    (12, -20, 27, -16)
                ],
                [
                    (-10, -45, 3, -34),
                    (-11, -49, 0, -45),
                    (-18, -37, -8, -31),
                    (-13, -34, 5, -28),
                    (2, -31, 13, -26),
                    (-11, -29, 2, -20),
                    (-10, -20, 11, -13),
                    (-7, -14, 4, -11),
                    (10, -19, 28, -15)
                ],
                [
                    (-9, -49, 0, -46),
                    (-10, -46, 4, -34),
                    (-18, -38, -7, -32),
                    (-13, -34, 5, -27),
                    (3, -31, 14, -26),
                    (-10, -27, 2, -19),
                    (-9, -19, 9, -12),
                    (9, -18, 23, -14),
                    (19, -16, 28, -13),
                    (-6, -13, 10, -10)
                ],
                [
                    (-7, -46, 4, -34),
                    (-7, -50, 3, -46),
                    (-16, -37, -8, -33),
                    (-14, -35, 5, -30),
                    (-10, -31, 2, -18),
                    (0, -32, 7, -26),
                    (6, -28, 10, -24),
                    (7, -25, 14, -21),
                    (-9, -19, 1, -10),
                    (-2, -19, 10, -13),
                    (8, -17, 19, -13),
                    (16, -15, 26, -10),
                    (22, -13, 23, -11),
                    (21, -13, 35, -9),
                    (-5, -10, 2, 1)
                ],
                [
                    (-4, -44, 8, -32),
                    (-4, -48, 7, -44),
                    (-5, -33, 5, -23),
                    (-8, -27, 4, -19),
                    (-10, -21, 3, -16),
                    (-10, -16, 6, -9),
                    (-10, -8, -5, 0),
                    (1, -10, 8, -7),
                    (5, -7, 10, -4),
                    (6, -4, 10, -1),
                    (7, -3, 17, -1),
                    (4, -28, 10, -24),
                    (6, -25, 13, -21),
                    (9, -21, 13, -19)
                ],
                [
                    (3, -41, 15, -30),
                    (4, -45, 14, -41),
                    (1, -31, 10, -26),
                    (-1, -27, 11, -22),
                    (-3, -24, 7, -20),
                    (-5, -21, 7, -17),
                    (-6, -14, 10, -8),
                    (7, -22, 13, -19),
                    (-7, -8, -4, -3),
                    (-13, -3, -5, 0),
                    (7, -9, 11, -2),
                    (7, -3, 18, 0)
                ]
             ]
        
        h = [
                [(-11, -27, 40, -9, 60, 90, 15, 40, [], 2)]
            ]
        
        f = [ self.frameData(2, 3, r[0]),
              self.frameData(153, 5, r[1], h[0]),
              self.frameData(154, 3, r[2], h[0]),
              self.frameData(155, 2, r[3], h[0]),
              self.frameData(156, 1, r[4]),
              self.frameData(157, 1, r[5]),
              self.frameData(158, 3, r[6]),
              self.frameData(157, 2, r[5]) ]
        
        t = [ ['attackB', move.Transition(0, 0, 2, 5, 'upB')],
              ['attackBUp', move.Transition(0, 0, 2, 5, 'upB')] ]
        
        self.moves['dashAttackA'].append(f, t)
        self.moves['dashAttackA'].canDI = False
        
        self.moves['dashAttackA'].frames[0].setVelX = 16
        for i in range(5):
            self.moves['dashAttackA'].frames[i].setFrictionX = 0.5
        for i in range(len(self.moves['dashAttackA'].frames)):
            self.moves['dashAttackA'].frames[i].ignoreSpeedCap = True

    def createMoveDashAttackB(self):
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
        dam1 = 140
        stun1 = 120
        force1 = 21
        angle1 = 22
        freeze1 = 5
        h = [
                [
                    (18, -70, 57, -31, dam1, stun1, force1, angle1, [], freeze1),
                    (-26, -61, 25, -40, dam1, stun1, force1, angle1, [], freeze1),
                    (49, -61, 62, -39, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (39, -56, 92, -15, dam1, stun1, force1, angle1, [], freeze1),
                    (49, -15, 84, 2, dam1, stun1, force1, angle1, [], freeze1)
                ]
            ]
        f = [ self.frameData(59, 3, r[0]),
              self.frameData(59, 2, r[0]),
              self.frameData(59, 3, r[0]),
              self.frameData(60, 1, r[1], h[0]),
              self.frameData(61, 1, r[2], h[1]),
              self.frameData(62, 2, r[3]),
              self.frameData(63, 5, r[4]),
              self.frameData(64, 2, r[5]),
              self.frameData(65, 2, r[6]) ]
        t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 2, 4, 'idleLike')] ]
        self.moves['dashAttackB'].append(f, t)
        self.moves['dashAttackB'].canDI = False
        self.moves['dashAttackB'].frames[0].setVelX = 15
        self.moves['dashAttackB'].frames[0].ignoreFriction = True
        self.moves['dashAttackB'].frames[0].ignoreSpeedCap = True
        self.moves['dashAttackB'].frames[1].ignoreFriction = True
        self.moves['dashAttackB'].frames[1].ignoreSpeedCap = True
        self.moves['dashAttackB'].frames[2].ignoreSpeedCap = True


    def createOldMoveDashAttackB(self):
        r = [
                [
                    (-21, -27, 18, -11),
                    (-18, -32, 16, -27),
                    (-14, -36, 14, -32),
                    (-10, -38, 8, -36),
                    (-19, -11, 16, -8),
                    (-17, -8, 13, -5),
                    (-14, -5, 11, -3),
                    (-11, -3, 8, 0)
                ]
            ]
        
        f = [ self.frameData(19, 2),
              self.frameData(23, 2),
              self.frameData(20, 1, r[0]),
              self.frameData(33, 2, r[0]),
              self.frameData(21, 1, r[0]),
              self.frameData(24, 2, r[0]),
              self.frameData(22, 1, r[0]),
              self.frameData(34, 2, r[0]),
              self.frameData(19, 1, r[0]),
              self.frameData(23, 2, r[0]),
              self.frameData(19, 1, r[0]),
              self.frameData(23, 2, r[0]),
              self.frameData(20, 1, r[0]),
              self.frameData(33, 2, r[0])]
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
                    [14, -17, 71, -1]
                ],
                [
                    [12, -31, 64, -9],
                    [38, -45, 68, -3]
                ],
                [
                    [-9, -51, 18, -34],
                    [11, -51, 65, -18],
                    [-18, -50, 0, -29]
                ]
            ]
        for j in range(3):
            h[j] = [i + [40, 60, 30, 45, [], 0] for i in h[j]]
        f = [ self.frameData(25, 3, r[0]),
              self.frameData(26, 1, r[0], h[0]),
              self.frameData(26, 1, r[0], h[1]),
              self.frameData(27, 2, r[0], h[2]),
              self.frameData(28, 11, r[0])]
        self.moves['rollingSlash'] = move.Move(f, [])
        self.moves['rollingSlash'].canDI = False
        self.moves['rollingSlash'].frames[0].setVelX = 0

    def createMoveDownA(self):
        r = [
                [
                    (-6, -42, 8, -36),
                    (-4, -36, 10, -28),
                    (-1, -28, 17, -5),
                    (-6, -21, -1, -13),
                    (8, -6, 15, 4),
                    (16, -15, 29, -10)
                ],
                [
                    (-19, -25, -5, -14),
                    (-24, -24, -19, -18),
                    (-22, -29, -15, -24),
                    (-10, -15, 17, 4),
                    (-6, -20, 15, -15),
                    (15, -8, 30, 0),
                    (29, -5, 51, 1)
                ],
                [
                    (-17, -30, -3, -18),
                    (-23, -29, -16, -24),
                    (-19, -35, -12, -29),
                    (-11, -18, 9, 1),
                    (-4, -23, 12, -12),
                    (7, -12, 15, 4),
                    (12, -11, 23, 0),
                    (21, -4, 37, 2),
                    (35, -2, 49, 4)
                ],
                [
                    (-5, -39, 11, -28),
                    (-6, -42, 6, -39),
                    (-2, -28, 15, -17),
                    (1, -17, 17, -11),
                    (3, -12, 25, -6),
                    (7, -6, 15, 4),
                    (14, -7, 26, -1),
                    (-6, -21, -1, -13),
                    (11, -31, 16, -25)
                ],
            ]

        dam1 = 80
        stun1 = 101
        force1 = 6
        angle1 = 30

        h = [
                [
                    [-3, -8, 68, 7],
                ]
            ]

        h[0] = [i + [dam1, stun1, force1, angle1, [('untechable')], 0] for i in h[0]]




        f = [ self.frameData(29, 3, r[0]),
              self.frameData(30, 3, r[1], h[0]),
              self.frameData(31, 7, r[2]),
              self.frameData(32, 5, r[3]) ]
        self.moves['downA'].append(f, [])
        self.moves['downA'].canDI = False

    def createMoveUpA(self):
        r = [
                [
                    (-9, -50, 1, -45),
                    (-9, -45, 4, -35),
                    (-9, -35, 1, -19),
                    (-22, -34, -7, -28),
                    (0, -32, 8, -27),
                    (-12, -27, -8, -15),
                    (-13, -20, 2, -15),
                    (0, -16, 7, -10),
                    (3, -12, 8, -1),
                    (5, -2, 17, 0),
                    (-18, -18, -10, -12),
                    (-23, -14, -12, -8),
                    (-25, -10, -19, -5)
                ],
                [
                    (-9, -49, 1, -45),
                    (-9, -45, 4, -35),
                    (-9, -35, 4, -19),
                    (-13, -31, -8, -22),
                    (3, -32, 10, -23),
                    (-9, -20, 6, -12),
                    (0, -13, 6, -5),
                    (-6, -7, 2, -1),
                    (-9, -3, -2, 3),
                    (-4, 0, 3, 5)
                ],
                [
                    (-8, -49, 2, -45),
                    (-9, -45, 4, -36),
                    (-9, -36, 3, -21),
                    (1, -35, 5, -31),
                    (-14, -33, -8, -24),
                    (-9, -23, 4, -17),
                    (-6, -17, 5, -12),
                    (2, -25, 11, -19),
                    (0, -12, 5, -6),
                    (-13, -9, 6, -5),
                    (-13, -5, -6, -2),
                    (-10, -2, -3, 3),
                    (11, -27, 27, -24),
                    (10, -25, 14, -22),
                    (22, -35, 28, -27)
                ],
                [
                    (-10, -48, 0, -44),
                    (-10, -44, 3, -35),
                    (-9, -35, 4, -19),
                    (-14, -32, -9, -23),
                    (-10, -22, 5, -17),
                    (3, -24, 11, -17),
                    (-9, -19, 6, -12),
                    (-2, -13, 4, -7),
                    (-13, -10, 4, -7),
                    (-13, -7, -7, -2),
                    (-10, -2, -5, 2),
                    (8, -27, 16, -23),
                    (13, -29, 26, -25),
                    (20, -36, 25, -27)
                ]
            ]

        dam1 = 35
        stun1 = 95
        force1 = 8
        angle1 = 65
        force2 = 16

        h = [
                [
                    [-12, -45, 40, -2],
                ],
                [
                    [-12, -45, 40, -2],
                ]
            ]

        h[0] = [i + [dam1, stun1, force1, angle1, [], 3] for i in h[0]]
        h[1] = [i + [dam1, stun1, force2, angle1, [], 3] for i in h[1]]

        t = [['onHit', move.Transition(None, None, 4, 4, 'upAConfirm')]]

        
        f = [ self.frameData(125, 4, r[0]),
              self.frameData(126, 2, r[1], h[0]),
              self.frameData(127, 1, r[2]),
              self.frameData(128, 3, r[3]),
              self.frameData(129, 3, r[1], h[1]),
              self.frameData(130, 1, r[2]),
              self.frameData(131, 20, r[3])]
        self.moves['upA'].append(f, t)
        self.moves['upA'].canDI = False
        self.moves['upA'].liftOff = True

        self.moves['upA'].frames[1].setVelY = -5.0
        self.moves['upA'].frames[1].setVelX = 6.0
        self.moves['upA'].frames[1].ignoreFriction = True
        self.moves['upA'].frames[4].setVelY = -5.5
        self.moves['upA'].frames[4].setVelX = 4.0
        self.moves['upA'].frames[4].ignoreFriction = True

        self.moves['upA'].frames[5].setAccelY = self.airAccel * 0.75
        self.moves['upA'].frames[6].setAccelY = self.airAccel * 0.75

        self.moves['upA'].frames[3].resetHitPotential = True

        self.createMoveUpAConfirm()

    def createMoveUpAConfirm(self):
        r = [
                [
                    (-9, -49, 1, -45),
                    (-9, -45, 4, -35),
                    (-9, -35, 4, -19),
                    (-13, -31, -8, -22),
                    (3, -32, 10, -23),
                    (-9, -20, 6, -12),
                    (0, -13, 6, -5),
                    (-6, -7, 2, -1),
                    (-9, -3, -2, 3),
                    (-4, 0, 3, 5)
                ],
                [
                    (-8, -49, 2, -45),
                    (-9, -45, 4, -36),
                    (-9, -36, 3, -21),
                    (1, -35, 5, -31),
                    (-14, -33, -8, -24),
                    (-9, -23, 4, -17),
                    (-6, -17, 5, -12),
                    (2, -25, 11, -19),
                    (0, -12, 5, -6),
                    (-13, -9, 6, -5),
                    (-13, -5, -6, -2),
                    (-10, -2, -3, 3),
                    (11, -27, 27, -24),
                    (10, -25, 14, -22),
                    (22, -35, 28, -27)
                ],
                [
                    (-10, -48, 0, -44),
                    (-10, -44, 3, -35),
                    (-9, -35, 4, -19),
                    (-14, -32, -9, -23),
                    (-10, -22, 5, -17),
                    (3, -24, 11, -17),
                    (-9, -19, 6, -12),
                    (-2, -13, 4, -7),
                    (-13, -10, 4, -7),
                    (-13, -7, -7, -2),
                    (-10, -2, -5, 2),
                    (8, -27, 16, -23),
                    (13, -29, 26, -25),
                    (20, -36, 25, -27)
                ]
            ]
                
        f = [ self.frameData(129, 3, r[0]),
              self.frameData(130, 1, r[1]),
              self.frameData(131, 3, r[2]),
              self.frameData(131, 20, r[2])]

        t = [['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 0, 2, 'upAirB')],
             ['attackB', move.Transition(None, None, 0, 2, 'upASideKick')],
             ['attackA', move.Transition(None, None, 0, 2, 'upADropSlash')],
             ['attackADown', move.Transition(None, None, 0, 2, 'upADropSlash')],
             ['attackAUp', move.Transition(None, None, 0, 2, 'upADropSlash')] ]

        self.moves['upAConfirm'] = move.Move(f, t)
        self.moves['upAConfirm'].canDI = False

        self.moves['upAConfirm'].frames[0].setVelY = -5.5
        self.moves['upAConfirm'].frames[0].setVelX = 4.0
        self.moves['upAConfirm'].frames[0].ignoreFriction = True

        self.moves['upAConfirm'].frames[1].setAccelY = self.airAccel * 0.75
        self.moves['upAConfirm'].frames[2].setAccelY = self.airAccel * 0.75
        self.moves['upAConfirm'].frames[3].setAccelY = self.airAccel * 0.75

        self.createMoveUpASideKick()
        self.createMoveUpADropSlash()

    def createMoveUpASideKick(self):
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
                ]
            ]

        dam1 = 50
        stun1 = 80
        force1 = 14
        angle1 = 30

        h = [
                [
                    [14, -50, 75, -15],
                    [-7, -35, 17, -23]
                ]
            ]

        h[0] = [i + [dam1, stun1, force1, angle1, [], 5] for i in h[0]]

        
        f = [ self.frameData(35, 9, r[0]),
              self.frameData(36, 1, r[1], h[0]),
              self.frameData(37, 3, r[2], h[0]),
              self.frameData(37, 7, r[2]),
              self.frameData(124, 20)]

        self.moves['upASideKick'] = move.Move(f, [])
        self.moves['upASideKick'].canDI = False

        self.moves['upASideKick'].frames[0].setVelY = -6
        self.moves['upASideKick'].frames[0].setVelX = -0.5
        self.moves['upASideKick'].frames[0].ignoreFriction = True
        self.moves['upASideKick'].frames[2].setVelY = -1.0
        self.moves['upASideKick'].frames[2].setVelX = -1.2

    def createMoveUpADropSlash(self):
        dam1 = 90
        stun1 = 140
        force1 = 20
        angle1 = 270
        
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
                    (-1, -53, 11, -41),
                    (-1, -57, 10, -53),
                    (-2, -43, 6, -19),
                    (-6, -44, 0, -38),
                    (-9, -46, -5, -43),
                    (-13, -48, -8, -44),
                    (-6, -31, -1, -17),
                    (-6, -17, -3, -11),
                    (-8, -11, -5, -6),
                    (-9, -6, -6, 2),
                    (3, -19, 8, -13),
                    (4, -13, 8, -8),
                    (1, -8, 4, -5),
                    (0, -6, 6, 1),
                    (5, -42, 11, -24)
                ],
             ]

        h = [
                [
                    [0, -75, 69, -4]
                ]
            ]

        h[0] = [i + [dam1, stun1, force1, angle1, [], 4] for i in h[0]]



        f = [ self.frameData(59, 2, r[0]),
              self.frameData(59, 10, r[0]),
              self.frameData(132, 2, r[1], h[0] ),
              self.frameData(132, 20, r[1] ) ]
        t = [ ['land', move.Transition(None, None, None, None, 'dropSlashLag')] ]

        
        self.moves['upADropSlash'] = move.Move(f, t)
        self.moves['upADropSlash'].canDI = False

        self.moves['upADropSlash'].frames[0].setVelY = -10.0
        self.moves['upADropSlash'].frames[0].setVelX = 8.0
        self.moves['upADropSlash'].frames[2].setVelY = 30.0
        self.moves['upADropSlash'].frames[0].setAccelY = self.airAccel * 0.6
        self.moves['upADropSlash'].frames[1].setAccelY = self.airAccel * 0.6
        self.moves['upADropSlash'].frames[2].setAccelY = self.airAccel * 1.5
        self.moves['upADropSlash'].frames[3].setAccelY = self.airAccel * 1.5

        self.createLagDropSlash()

    def createLagDropSlash(self):
        r = [
                [
                    (-4, -44, 7, -31),
                    (-4, -48, 6, -44),
                    (-10, -36, -2, -31),
                    (-8, -32, 3, -16),
                    (1, -31, 9, -1),
                    (3, -3, 13, 0),
                    (-11, -25, -7, -11),
                    (-12, -16, 6, -10),
                    (-17, -11, -11, -7),
                    (-19, -9, -15, -5),
                    (-22, -5, -17, -2),
                    (-28, -3, -20, -1),
                    (-19, -47, -15, -44),
                    (-17, -44, -11, -40),
                    (-14, -40, -9, -36)
                    ]
            ]
        
        f = [ self.frameData(133, 10, r[0] ) ]

        self.moves['dropSlashLag'] = move.Move(f, [])
        self.moves['dropSlashLag'].canDI = False

    def createMoveDownB(self):
        r = [
                [
                    (-20, -39, -5, -34),
                    (-18, -34, -5, -30),
                    (-16, -30, -4, -27),
                    (-13, -27, 5, -22),
                    (-6, -30, 1, -27),
                    (-23, -24, -6, -21),
                    (-11, -22, 8, -18),
                    (-6, -18, 11, -15),
                    (-2, -15, 13, -10),
                    (2, -10, 9, -6),
                    (11, -10, 18, -7),
                    (13, -7, 20, -3),
                    (16, -3, 22, 1)
                ],
                [
                    (-17, -41, -4, -30),
                    (-20, -42, -6, -39),
                    (-11, -30, 3, -21),
                    (-9, -22, 5, -17),
                    (-7, -17, 8, -14),
                    (-3, -14, 4, -5),
                    (2, -14, 10, -8),
                    (5, -8, 12, -1),
                    (-25, -28, -9, -23)
                ],
                [
                    (-15, -42, -2, -31),
                    (-16, -44, -3, -42),
                    (-12, -31, 1, -14),
                    (-25, -29, -10, -24),
                    (-8, -14, -3, -4),
                    (-2, -15, 4, -2)
                ]
            ]
        
        f = [ self.frameData(11, 7),
              self.frameData(11, 2, r[0]),
              self.frameData(12, 5, r[1]),
              self.frameData(13, 20, r[2])]
        t = [ ['land', move.Transition(None, None, None, None, 'downBLag')],
              ['attackBDown', move.Transition(2, HARE_ENERGY_USAGE, 3, 3, 'downAirB')],
              ['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 3, 3, 'upAirB')],
              ['doDash', move.Transition(2, HARE_ENERGY_USAGE, 3, 3, 'airDashing')] ]
        
        
        self.moves['downB'].append(f, t)
        self.moves['downB'].canDI = False
        self.moves['downB'].liftOff = True
        self.moves['downB'].frames[0].setVelX = -28
        self.moves['downB'].frames[0].setVelY = -9.5
        self.moves['downB'].frames[0].ignoreSpeedCap = True
        self.moves['downB'].frames[0].ignoreFriction = True
        self.moves['downB'].frames[1].ignoreFriction = True
        self.moves['downB'].frames[2].setFrictionX = self.airFriction * 0.35
        self.moves['downB'].frames[0].fx.append(['dust', (14, 0), True])
        self.moves['downB'].frames[0].fx.append(['dust', (-14, 0), False])
        
        
        self.createLagDownB()

    def createLagDownB(self):
        r = [
                [
                    (-9, -27, 6, -15),
                    (-14, -16, 8, -10),
                    (-7, -10, 9, 5)
                ]
            ]
        
        f = [ self.frameData(86, 8, r[0]) ]
        self.moves['downBLag'] = move.Move(f, [])
        self.moves['downBLag'].canDI = False

    def createMoveUpB(self):
        r = [
                [
                    (4, -52, 17, 2)
                ],
                [
                    (11, -50, 24, -15),
                    (12, -15, 27, 0),
                    (23, -32, 27, -22)
                ],
                [
                    (15, -53, 27, -47),
                    (15, -47, 28, -37),
                    (19, -37, 31, -29),
                    (15, -31, 36, -21),
                    (20, -24, 36, -14),
                    (18, -14, 26, 1),
                    (24, -14, 37, 2)
                ],
                [
                    (10, -39, 22, -25),
                    (21, -34, 40, -21),
                    (15, -26, 28, -15),
                    (25, -25, 37, -16),
                    (38, -36, 49, -26),
                    (33, -27, 40, -18),
                    (38, -28, 45, -21),
                    (30, -16, 39, 2)
                ],
                [
                    (5, -30, 37, -17),
                    (15, -17, 20, -1),
                    (8, -3, 18, 1),
                    (22, -19, 26, -15),
                    (28, -20, 38, 2),
                    (33, -38, 43, -30),
                    (37, -45, 44, -38),
                    (39, -51, 46, -45),
                    (41, -57, 48, -51),
                    (43, -59, 48, -56),
                    (37, -7, 40, -1)
                ]
            ]

        dam1 = 75
        stun1 = 110
        force1 = 23
        angle1 = 85
        freeze1 = 4

        h = [
                [
                    [16, -43, 56, -15],
                    [22, -62, 67, -43],
                    [39, -75, 61, -62],
                    [56, -43, 63, -27]
                ]
            ]
        h[0] = [i + [dam1, stun1, force1, angle1, [], freeze1] for i in h[0]]

                

                
        
        f = [ self.frameData(88, 1, r[0]),
              self.frameData(89, 1, r[1]),
              self.frameData(90, 1, r[2]),
              self.frameData(91, 1, r[3]),
              self.frameData(92, 2, r[4], h[0]),
              self.frameData(92, 4, r[4], h[0]),
              self.frameData(92, 7, r[4]),
              self.frameData(91, 2, r[3]),
              self.frameData(90, 2, r[2]),
              self.frameData(89, 1, r[1]),
              self.frameData(88, 1, r[0]) ]

        t = [['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 5, 7, 'idleLike')],
             ['jump', move.Transition(2, HARE_ENERGY_USAGE, 5, 7, 'jumpingLike')]]
        

        self.moves['upB'].append(f, t)
        self.moves['upB'].canDI = False
        self.moves['upB'].frames[0].setVelX = 10

    def createOldSpinAttack(self):
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

        dam1 = 3
        stun1 = 90
        force1 = 18
        force2 = 11
        angle1 = 50
        angle2 = 130
        freeze1 = 0

        h = [
                [
                    (-35, -61, 2, 3, dam1, stun1, force1, angle1, [], freeze1),
                    (2, -61, 29, 3, dam1, stun1, force1, angle2, [], freeze1)
                ],
                [
                    (-35, -61, 2, 3, dam1, stun1, force2, angle1, [], freeze1),
                    (2, -61, 29, 3, dam1, stun1, force2, angle2, [], freeze1)
                ]
            ]


        f = [ self.frameData(9, 6, r[0]),
              self.frameData(93, 1, [], h[0]),
              self.frameData(94, 1, [], h[0]),
              self.frameData(95, 1, [], h[0]),
              self.frameData(96, 1, [], h[0]),
              self.frameData(97, 1, [], h[0]),
              self.frameData(98, 1, [], h[0]),
              self.frameData(99, 1, [], h[0]),
              self.frameData(100, 1, [], h[0]),
              self.frameData(93, 1, [], h[1]),
              self.frameData(94, 1, [], h[1]),
              self.frameData(95, 1, [], h[1]),
              self.frameData(96, 1, [], h[1]),
              self.frameData(97, 1, [], h[1]),
              self.frameData(98, 1, [], h[1]),
              self.frameData(99, 1, [], h[1]),
              self.frameData(100, 1, [], h[1]) ]

        t = [['exitFrame', move.Transition(-1, None, None, None, 'rotateKick')]]

        self.moves['upB'].append(f, t)
        self.moves['upB'].canDI = False
        self.moves['upB'].liftOff = True

        self.moves['upB'].frames[0].setAccelX = 0
        for i in range(1,4):
            self.moves['upB'].frames[i].setVelY = -18.0
            self.moves['upB'].frames[i].setAccelY = 0

        for i in range(17):
            self.moves['upB'].frames[i].resetHitPotential = True

        self.createMoveRotateKick()


    def createMoveRotateKick(self):
        dam1 = 40
        stun1 = 110
        force1 = 18
        angle1 = 135
        angle2 = 45
        freeze1 = 6

        r = [
                [
                    
                ]
            ]
        
        h = [
                [
                    (-46, -31, -2, -15, dam1, stun1, force1, angle1, [], freeze1),
                    (-2, -31, 44, -15, dam1, stun1, force1, angle2, [], freeze1)
                ]
            ]

        
        f = [ self.frameData(107, 4, r[0]),
              self.frameData(101, 4, r[0], h[0]),
              self.frameData(102, 3, r[0], h[0]),
              self.frameData(103, 3, r[0], h[0]),
              self.frameData(104, 2, r[0]),
              self.frameData(105, 2, r[0]),
              self.frameData(106, 2, r[0]) ]

        
        self.moves['rotateKick'] = move.Move(f, [])
        self.moves['rotateKick'].canDI = True
        
        for i in range(6):
            self.moves['rotateKick'].frames[i].setAccelY = 0.55
            self.moves['rotateKick'].frames[i].setSpeedCapX = self.airVelMax * 1.2
            self.moves['rotateKick'].frames[i].setAccelX = self.airAccel * 2.0
            self.moves['rotateKick'].frames[i].setFrictionX = self.airFriction * 2.0

        
              

    def createMoveNeutralAirA(self):
        r = [
                [
                    (-16, -52, -6, -46),
                    (-9, -49, -1, -42),
                    (-5, -59, 6, -54),
                    (-5, -54, 9, -42),
                    (-6, -43, 8, -28),
                    (8, -40, 17, -35),
                    (-5, -29, 10, -19),
                    (-3, -20, 3, 3),
                    (-6, -8, -3, -1),
                    (5, -20, 9, 0),
                    (8, -19, 12, -12),
                    (2, -11, 6, 1),
                    (4, -3, 13, 1)

                ],
                [
                    (-3, -58, 7, -54),
                    (-3, -54, 10, -43),
                    (-3, -43, 7, -26),
                    (-5, -30, 8, -18),
                    (-4, -18, 1, 4),
                    (-9, -9, -4, 1),
                    (0, -21, 6, 3),
                    (4, -19, 9, 2)
                ],
                [
                    (0, -58, 11, -53),
                    (-1, -53, 12, -42),
                    (-2, -43, 10, -33),
                    (-5, -35, 8, -27),
                    (-6, -27, 8, -16),
                    (-5, -16, 2, 2),
                    (1, -16, 5, 3),
                    (4, -17, 7, -11),
                    (-9, -13, -3, 3),
                    (-13, -10, -8, -2),
                    (-15, -44, 0, -38)

                ],
                [
                    (5, -58, 14, -51),
                    (3, -53, 16, -42),
                    (13, -56, 15, -52),
                    (-13, -46, 6, -40),
                    (-4, -40, 6, -26),
                    (5, -43, 11, -32),
                    (9, -34, 16, -29),
                    (13, -30, 21, -25),
                    (17, -26, 21, -23),
                    (10, -38, 14, -33),
                    (-7, -28, 5, -13),
                    (-14, -14, 3, -10),
                    (-17, -10, -2, -8),
                    (-17, -8, -8, -5),
                    (-16, -5, -4, -3),
                    (-15, -3, 0, 1)

                ],
                [
                    (1, -58, 12, -53),
                    (0, -53, 13, -43),
                    (-5, -45, 7, -27),
                    (-16, -44, -4, -40),
                    (5, -42, 12, -35),
                    (5, -36, 14, -31),
                    (11, -32, 17, -29),
                    (14, -28, 21, -24),
                    (14, -30, 19, -28),
                    (-6, -29, 7, -14),
                    (-8, -14, 5, -9),
                    (-14, -11, -2, -5),
                    (-13, -5, -1, -2),
                    (-10, -2, 3, 2)
                ],
            ]
        
        dam1 = 70
        stun1 = 20
        force1 = 14
        angle1 = 20
        h = [
                [
                    [5, -70, 43, -58],
                    [24, -58, 47, -50],
                    [-36, -59, -12, -46],
                    [-20, -65, 11, -55],
                    [-5, -58, 24, -28],
                    [-12, -55, -1, -41]

                ],
                [
                    [14, -70, 54, -51],
                    [30, -51, 70, -23],
                    [-5, -55, 30, -18],
                    [-12, -55, -1, -41]
                ],
                [
                    [21, -23, 55, -8],
                    [28, -41, 58, -23],
                    [15, -8, 52, 8]

                ]
            ]

        for j in range(3):
            h[j] = [i + [dam1, stun1, force1, angle1, [], 2] for i in h[j]]
        
        f = [ self.frameData(14, 3, r[0]),
              self.frameData(15, 1, r[1], h[0]),
              self.frameData(16, 1, r[2], h[1]),
              self.frameData(17, 2, r[3], h[2]),
              self.frameData(18, 6, r[4]) ]
        self.moves['neutralAirA'].append(f, [])
        self.moves['neutralAirA'].reversable = True

    def createMoveNeutralAirB(self):
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
        dam1 = 35
        stun1 = 30
        force1 = 5
        angle1 = 80
        freeze1 = 3
        dam2 = 50
        stun2 = 60
        force2 = 14
        angle2 = 25
        freeze2 = 2
        h = [
                [
                    (-4, -57, 50, -18, dam1, stun1, force1, angle1, [], freeze1),
                    (-19, -30, 3, -17, dam1, stun1, force1, angle1, [], freeze1),
                    (26, -65, 56, -40, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (-4, -57, 50, -18, dam2, stun2, force2, angle2, [], freeze2),
                    (-19, -30, 3, -17, dam2, stun2, force2, angle2, [], freeze2),
                    (26, -63, 56, -43, dam2, stun2, force2, angle2, [], freeze2)
                ]
            ]
        f = [ self.frameData(35, 3, r[0]),
              self.frameData(36, 1, r[1], h[0]),
              self.frameData(37, 3, r[2], h[0]),
              self.frameData(38, 3, r[3]),
              self.frameData(39, 1, r[4], h[0]),
              self.frameData(40, 3, r[5], h[0]),
              self.frameData(35, 3, r[0]),
              self.frameData(36, 1, r[1], h[1]),
              self.frameData(37, 4, r[2], h[1]),
              self.frameData(8, 4, r[6])]
        
        t = [ ['attackBDown', move.Transition(2, HARE_ENERGY_USAGE, 6, 9, 'downAirB')],
              ['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 6, 9, 'upAirB')],
              ['doDash', move.Transition(2, HARE_ENERGY_USAGE, 6, 9, 'airDashing')] ]
        
        
        self.moves['neutralAirB'].append(f, t)
        self.moves['neutralAirB'].canDI = False
        self.moves['neutralAirB'].reversable = True
        self.moves['neutralAirB'].frames[1].setVelYIfDrop = -3.4
        self.moves['neutralAirB'].frames[4].setVelYIfDrop = -1.5
        self.moves['neutralAirB'].frames[7].setVelYIfDrop = -1.5
        self.moves['neutralAirB'].frames[4].resetHitPotential = True
        self.moves['neutralAirB'].frames[7].resetHitPotential = True
        for i in range(len(self.moves['neutralAirB'].frames)):
            self.moves['neutralAirB'].frames[i].ignoreFriction = True

    def createMoveUpAirA(self):
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
                    [-4, -77, 32, -29],
                    [-14, -48, 7, -24]


                ],
                [
                    [-38, -78, 17, -48],
                    [-23, -48, 8, -36],
                    [-33, -83, 8, -78]

                ],
                [
                    [-45, -71, -15, -44],
                    [-31, -77, 11, -58],
                    [-51, -50, -21, -34],
                    [-28, -60, 5, -28]

                ],
                [
                    [-45, -51, -8, -31],
                    [-13, -48, 6, -30]

                ],
            ]
        for j in range(4):
            h[j] = [i + [70, 60, 20, 60, [], 0] for i in h[j]]

        f = [ self.frameData(75, 4, r[0]),
              self.frameData(76, 2, r[1], h[0]),
              self.frameData(77, 1, r[2], h[1]),
              self.frameData(78, 1, r[3], h[2]),
              self.frameData(79, 2, r[4], h[3]),
              self.frameData(80, 5, r[4]) ]

        self.moves['upAirA'].append(f, [])

    def createMoveUpAirB(self):
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
                    [-26, -67, 18, -14],
                    [-13, -84, 28, -50],
                    [-1, -62, 32, -27],
                    [12, -89, 43, -61]

                ],
            ]

        h[0] = [i + [18, 40, 20, 60, [], 3] for i in h[0]]
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

    def createMoveDownAirA(self):
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
                ],
                [
                    (-11, -43, 3, -31),
                    (-10, -48, 1, -43),
                    (-16, -34, -10, -28),
                    (-11, -32, 6, -11),
                    (-6, -11, -1, -8),
                    (-3, -17, 5, -10),
                    (1, -10, 5, 16)
                ]
            ]

        h = [
                [
                    (-15, -28, 14, -10, 70, 105, 22, 270, [], 3),
                    (-8, -13, 15, 22, 70, 105, 22, 270, [], 3)
                ]
            ]

        f = [ self.frameData(85, 9, r[0]),
              self.frameData(82, 1, r[1]),
              self.frameData(83, 1, r[2], h[0]),
              self.frameData(84, 7, r[2], h[0]),
              self.frameData(84, 6, r[3]) ]

        t = [['land', move.Transition(None, None, None, None, 'downAAirLag')],
             ['onHit', move.Transition(None, None, None, None, 'headBounce')],
             ['attackA', move.Transition(None, None, 0, 0, 'stomp')],
             ['attackADown', move.Transition(None, None, 0, 0, 'stomp')]]

        

        self.moves['downAirA'].append(f, t)
        self.moves['downAirA'].frames[0].setVelY = -0.5
        self.moves['downAirA'].frames[1].setVelY = 20
        
        for i in range(len(self.moves['downAirA'].frames)):
            self.moves['downAirA'].frames[i].ignoreSpeedCap = True
            
        self.moves['downAirA'].canDI = False
        

        self.createLagDownAAir()
        self.createHeadBounce()
        self.createStomp()

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

    def createHeadBounce(self):
        r = [
                [
                    (-19, -20, -3, -10),
                    (-12, -10, -5, -1),
                    (-14, -32, 4, -19),
                    (-7, -22, 7, -13),
                    (-7, -15, 0, -12),
                    (0, -40, 17, -23)
                ],
                [
                    (-13, -35, 5, -22),
                    (-21, -32, -8, -26),
                    (-11, -24, 11, -15),
                    (0, -29, 12, -21),
                    (-2, -17, 18, -2)
                ],
                [
                    (-21, -19, -2, -3),
                    (-4, -27, 12, -10),
                    (-2, -35, 18, -25),
                    (9, -27, 16, -22),
                    (-7, -32, 1, -22),
                    (4, -43, 13, -35),
                    (-9, -26, 3, -18)
                ],
                [
                    (-19, -40, 0, -26),
                    (-15, -27, 5, -14),
                    (-6, -17, 12, -6),
                    (3, -25, 15, -12),
                    (12, -16, 21, -10)
                ],
                [
                    (-11, -51, 0, -46),
                    (-11, -46, 4, -36),
                    (-24, -47, -16, -41),
                    (-19, -42, -6, -34),
                    (-12, -40, 7, -30),
                    (3, -48, 10, -38),
                    (-11, -30, 5, -23),
                    (-13, -24, 14, -18),
                    (-10, -18, -1, -1),
                    (-10, -1, -4, 4),
                    (-12, 4, -6, 14),
                    (8, -18, 13, -3),
                    (8, -4, 14, 5),
                    (-4, -19, 9, -15)
                ]
            ]
        
        flippingSpeed = 3
        f = [ self.frameData(84, 3),
              self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]),
              self.frameData(24, flippingSpeed, r[3]),
              self.frameData(87, 6, r[4]),
              self.frameData(87, 6, r[4]),
              self.frameData(87, 2, r[4])]
        
        t = [['doDash', move.Transition(2, HARE_ENERGY_USAGE, 6, 7, 'airDashing')],
             ['attackADown', move.Transition(None, None, 2, 6, 'stomp')]]

        self.moves['headBounce'] = move.Move(f, t)
        self.moves['headBounce'].frames[0].setVelY = -22

        for i in range(len(f)-1):
            self.moves['headBounce'].frames[i].setAccelX = 5.0
            self.moves['headBounce'].frames[i].setFrictionX = self.airFriction * 8.0
            self.moves['headBounce'].frames[i].setSpeedCapX = self.vertVelMax * 1.2

             
    def createStomp(self):
        
        r = [
                [
                    (1, -49, 11, -38),
                    (-3, -40, 8, -30),
                    (-6, -35, 3, -20),
                    (-8, -22, 3, -15),
                    (1, -29, 7, -17),
                    (3, -17, 6, -8)
                ],
                [
                    (-4, -39, 4, -13),
                    (-8, -50, 3, -38)
                ],
                [
                    (-4, -39, 4, -13),
                    (-8, -50, 3, -38),
                    (-7, -2, -1, 5),
                    (-4, -16, 2, -2)
                ]
            ]
        
        
        dam1 = 60
        stun1 = 250
        force1 = 18
        angle1 = 270
        freeze1 = 3
        
        dam2 = 50
        stun2 = 175
        force2 = 15
        angle2 = 270
        freeze2 = 3
        
        h = [
                [
                    (-9, -33, 18, 9, dam1, stun1, force1, angle1, [], freeze1),
                    (-6, -46, 5, -12, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (-6, -46, 5, -12, dam2, stun2, force2, angle2, [], freeze2),
                    (-13, -12, 13, 8, dam2, stun2, force2, angle2, [], freeze2)
                ]
             ]
        
        f = [ self.frameData(163, 3, r[0]),
              self.frameData(164, 1, r[1], h[0]),
              self.frameData(165, 2, r[1], h[0]),
              self.frameData(165, 12, r[1], h[1]),
              self.frameData(165, 5, r[2]) ]
        
        t = []
             
        
        self.moves['stomp'] = move.Move(f, t)
        #self.moves['stomp'].canDI = False
        self.moves['stomp'].reversable = True
        
        self.moves['stomp'].frames[0].setVelY = 0
        

    def createMoveDownAirB(self):
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
                    [20, -22, 45, -3],
                    [6, -30, 29, -12],
                    [11, -16, 24, -8],
                    [24, -27, 34, -19],
                    [40, -18, 57, -1],
                    [26, -7, 52, 5]
                ],
            ]
        h[0] = [i + [50, 80, 14, 325, [], 2] for i in h[0]]
        f = [ self.frameData(55, 5, r[0]),
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
            self.moves['downAirB'].frames[i].setVelY = 20.0
            self.moves['downAirB'].frames[i].setVelX = 18.0
        self.moves['downAirB'].frames[0].setVelY = 0
        self.moves['downAirB'].frames[0].setVelX = 0

        self.createLagDownBAir()

    def createMoveDroppingThrough(self):
        f = [ self.frameData(8, 3) ]

        self.moves['droppingThrough'].append(f, [])

    def createMoveGrabbing(self):
        r = [
                [
                    (-6, -49, 5, -43),
                    (-8, -45, 6, -33),
                    (-12, -33, 2, -20),
                    (-12, -21, 2, -13),
                    (-18, -32, -10, -27),
                    (1, -31, 11, -26),
                    (-12, -14, -6, 0),
                    (-2, -16, 8, -10),
                    (3, -11, 9, 0),
                    (7, -3, 17, 0)
                ],
                [
                    (-5, -48, 5, -43),
                    (-7, -44, 7, -33),
                    (-7, -34, 2, -18),
                    (-10, -29, -5, -17),
                    (-11, -18, -6, 0),
                    (-9, -18, 7, -13),
                    (3, -15, 9, 0),
                    (6, -5, 18, 1),
                    (0, -31, 5, -27)
                ],
                [
                    (-5, -43, 8, -33),
                    (-5, -47, 7, -43),
                    (-6, -33, 5, -18),
                    (-10, -32, -4, -27),
                    (-15, -30, -4, -27),
                    (-9, -27, -3, -12),
                    (-6, -18, 7, -11),
                    (-12, -10, -7, -5),
                    (-14, -5, -7, 0),
                    (5, -12, 15, -6),
                    (5, -6, 15, 0),
                    (3, -32, 10, -28)
                ],
                [
                    (-4, -48, 7, -43),
                    (-4, -43, 9, -33),
                    (-4, -33, 5, -18),
                    (-6, -26, -4, -18),
                    (-7, -32, -4, -27),
                    (-10, -31, -3, -27),
                    (-15, -30, -7, -26),
                    (4, -32, 12, -28),
                    (-6, -18, 6, -12),
                    (-9, -15, -2, -10),
                    (-12, -11, -5, -7),
                    (-14, -7, -8, -4),
                    (-15, -4, -8, -1),
                    (3, -16, 10, -10),
                    (4, -13, 14, -7),
                    (8, -8, 12, -3),
                    (4, -5, 16, 0)
                ],
                [
                    (-7, -47, 3, -43),
                    (-8, -44, 5, -35),
                    (-7, -35, 4, -33),
                    (-9, -33, 6, -17),
                    (-15, -30, -7, -25),
                    (-21, -27, -12, -23),
                    (4, -34, 13, -31),
                    (-9, -18, 5, -12),
                    (3, -17, 9, -11),
                    (5, -13, 13, -9),
                    (8, -11, 12, -5),
                    (4, -5, 16, 0),
                    (-10, -13, -4, -8),
                    (-13, -10, -7, -5),
                    (-15, -5, -7, 0)
                ]
            ]

        h = [
                [
                    [-14, -34, 8, -25, 0, 0, 0, 0, [('grab', 'grabHold', 'grabbed')], 0 ]
                ],
                [
                    [-14, -40, 31, -24, 0, 0, 0, 0, [('grab', 'grabHold', 'grabbed')], 0 ]
                ]
            ]
                    
        
        f = [ self.frameData(110, 2, r[0]),
              self.frameData(111, 1, r[1], h[0]),
              self.frameData(112, 1, r[2], h[1]),
              self.frameData(113, 2, r[3], h[1]),
              self.frameData(114, 2, r[4], h[1]),
              self.frameData(114, 7, r[4]),
              self.frameData(111, 2, r[1]) ]

        self.moves['grabbing'].append(f, [])
        self.moves['grabbing'].frames[1].setVelX = 10.0
        self.moves['grabbing'].frames[1].ignoreFriction = True
        self.moves['grabbing'].frames[2].ignoreFriction = True
        self.moves['grabbing'].frames[6].setVelX = -10.0
        self.moves['grabbing'].frames[6].ignoreFriction = True

    def createMoveGrabHold(self):
        r = [
                [
                    (-7, -47, 3, -43),
                    (-8, -44, 5, -35),
                    (-7, -35, 4, -33),
                    (-9, -33, 6, -17),
                    (-15, -30, -7, -25),
                    (-21, -27, -12, -23),
                    (4, -34, 13, -31),
                    (-9, -18, 5, -12),
                    (3, -17, 9, -11),
                    (5, -13, 13, -9),
                    (8, -11, 12, -5),
                    (4, -5, 16, 0),
                    (-10, -13, -4, -8),
                    (-13, -10, -7, -5),
                    (-15, -5, -7, 0)
                ]
            ]

        f = [ self.frameData(114, 10, r[0]),
              self.frameData(114, 42, r[0]),
              self.frameData(114, 2, r[0])]

        self.moves['grabHold'].append(f, [])
        self.moves['grabHold'].grabPos = (13, 0)


    def createMoveGrabbed(self):
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
                ]
            ]

        f = [ self.frameData(70, 2, r[0]),
              self.frameData(70, 5, r[0]),
              self.frameData(70, 2, r[0]) ]

        self.moves['grabbed'].append(f, [])
        self.moves['grabbed'].grabPos = (12, 0)

    def createMoveGrabbed2(self):
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
                ]
            ]

        f = [ self.frameData(70, 2, r[0]) ]

        self.moves['grabbed2'].append(f, [])
        self.moves['grabbed2'].grabPos = (12, 0)
        

    def createMoveGrabRelease(self):

        r = [
                [
                    (-6, -49, 5, -43),
                    (-8, -45, 6, -33),
                    (-12, -33, 2, -20),
                    (-12, -21, 2, -13),
                    (-18, -32, -10, -27),
                    (1, -31, 11, -26),
                    (-12, -14, -6, 0),
                    (-2, -16, 8, -10),
                    (3, -11, 9, 0),
                    (7, -3, 17, 0)
                ]
            ]

        f = [ self.frameData(110, 2, r[0]),
              self.frameData(110, 1, r[0]),
              self.frameData(110, 22, r[0])]

        self.moves['grabRelease'].append(f, [])
        self.moves['grabRelease'].frames[1].setVelX = -20.0
        self.moves['grabRelease'].frames[1].setFrictionX = 0.5
        self.moves['grabRelease'].frames[2].setFrictionX = 0.75

    def createMoveGrabbedRelease(self):

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

        f = [ self.frameData(69, 2, r[0]),
              self.frameData(69, 1, r[0]),
              self.frameData(69, 22, r[0])]

        self.moves['grabbedRelease'].append(f, [])
        self.moves['grabbedRelease'].frames[1].setVelX = -20.0
        self.moves['grabbedRelease'].frames[1].setFrictionX = 0.5
        self.moves['grabbedRelease'].frames[2].setFrictionX = 0.75

    def createMoveThrowBackward(self):

        damage1 = 100
        stun1 = 155
        knockback1 = 23
        angle1 = 155

        h = [
                [
                    (-2, -42, 36, -3, damage1, stun1, knockback1, angle1,
                     [('reverseFacing', False, True), ('fx', None)], 0)
                ]
            ]

        f = [ self.frameData(115, 3),
              self.frameData(116, 2),
              self.frameData(117, 6),
              self.frameData(118, 2, [], h[0]),
              self.frameData(119, 14),
              self.frameData(120, 3),
              self.frameData(10, 6) ]

        self.moves['throwBackward'].append(f, [])

    def createMoveThrowForward(self):

        damage1 = 0
        stun1 = 52
        knockback1 = 18
        angle1 = 0

        damage2 = 100
        stun2 = 155
        knockback2 = 20
        angle2 = 28

        h = [
                [
                    (-1, -44, 36, -19, damage1, stun1, knockback1, angle1,
                     [('fx', None)], 0)
                ],
                [
                    (-12, -47, 70, -23, damage2, stun2, knockback2, angle2,
                     [], 0)
                ]
            ]

        f = [ self.frameData(35, 2, [], h[0]),
              self.frameData(35, 6),
              self.frameData(35, 2),
              self.frameData(121, 1),
              self.frameData(122, 1, [], h[1]),
              self.frameData(123, 5),
              self.frameData(123, 1),
              self.frameData(124, 10)]

        t = [ ['land', move.Transition(None, None, None, None, 'lagForwardThrow')] ]

        self.moves['throwForward'].append(f, t)
        self.moves['throwForward'].liftOff = True
        self.moves['throwForward'].frames[0].setVelY = -5.0
        self.moves['throwForward'].frames[2].setVelY = 0
        self.moves['throwForward'].frames[3].setVelY = 0
        self.moves['throwForward'].frames[4].setVelY = 0
        self.moves['throwForward'].frames[5].setVelY = 0

        self.moves['throwForward'].frames[2].resetHitPotential = True

        self.moves['throwForward'].frames[0].setVelX = 13
        for i in range(3):
            self.moves['throwForward'].frames[i].setFrictionX = 0

        self.createLagForwardThrow()

    def createLagForwardThrow(self):
        f = [ self.frameData(10, 8) ]
        self.moves['lagForwardThrow'] = move.Move(f, [])
        self.moves['lagForwardThrow'].canDI = False

    def createLagDownBAir(self):
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
        f = [ self.frameData(9, 7, r[0]) ]
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

        f = [ self.frameData(68, 9, r[0]) ]

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

    def createMoveStun4(self):
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

        
        f = [ self.frameData(70, 15, r[0]),
              self.frameData(71, 2, r[1]),
              self.frameData(72, 1, r[2]),
              self.frameData(73, 1, r[3]),
              self.frameData(74, 24, r[4])]

        self.moves['stun4'].append(f, [])

        for i in range(len(self.moves['stun4'].frames)):
            self.moves['stun4'].frames[i].ignoreSpeedCap = True

    def createMoveDeadFalling(self):
        f = [ self.frameData(74, 3) ]

        self.moves['deadFalling'].append(f, [])

        for i in range(len(self.moves['deadFalling'].frames)):
            self.moves['deadFalling'].frames[i].ignoreSpeedCap = True
            self.moves['deadFalling'].frames[i].ignoreFriction = True

    def createMoveDeadGroundHit(self):
        f = [ self.frameData(134, 2),
              self.frameData(135, 4),
              self.frameData(136, 2),
              self.frameData(137, 1) ]

        self.moves['deadGroundHit'].append(f, [])

    def createMoveDeadLaying(self):
        f = [ self.frameData(137, 3) ]

        self.moves['deadLaying'].append(f, [])

    def createMoveGroundHit(self):
        r = [
                [
                    (-25, -12, -14, 0),
                    (-28, -10, -25, 0),
                    (-15, -10, 15, -1),
                    (13, -12, 21, -7),
                    (15, -7, 41, -1)
                ]
            ]
        
        f = [ self.frameData(134, 2),
              self.frameData(135, 4),
              self.frameData(136, 2),
              self.frameData(137, 1),
              self.frameData(136, 1),
              self.frameData(137, 10),
              self.frameData(137, 2),
              self.frameData(137, 80, r[0]) ]

        self.moves['groundHit'].append(f, [])
        self.moves['groundHit'].frames[0].fx.append(['dust', (28, 0), True])
        self.moves['groundHit'].frames[0].fx.append(['dust', (-28, 0), False])
        self.moves['groundHit'].frames[1].fx.append(['shockwave', (0, 0), True])

    def createMoveStandUp(self):
        f = [ self.frameData(138, 4),
              self.frameData(139, 4),
              self.frameData(28, 6) ]

        self.moves['standUp'].append(f, [])

    def createMoveStandForward(self):
        f = [ self.frameData(138, 4),
              self.frameData(20, 1),
              self.frameData(33, 2),
              self.frameData(21, 1),
              self.frameData(24, 2),
              self.frameData(22, 1),
              self.frameData(34, 2),
              self.frameData(19, 1),
              self.frameData(28, 3) ]

        self.moves['standForward'].append(f, [])

        self.moves['standForward'].frames[1].setVelX = 22.8
        self.moves['standForward'].frames[8].setVelX = 0

        for i in range(len(self.moves['standForward'].frames)):
            self.moves['standForward'].frames[i].setFrictionX = self.groundFriction * 0.42
            self.moves['standForward'].frames[i].ignoreSpeedCap = True

    def createMoveStandBackward(self):
        f = [ self.frameData(138, 4),
              self.frameData(19, 1),
              self.frameData(34, 2),
              self.frameData(22, 1),
              self.frameData(24, 2),
              self.frameData(21, 1),
              self.frameData(33, 2),
              self.frameData(20, 1),
              self.frameData(28, 3) ]

        self.moves['standBackward'].append(f, [])

        self.moves['standBackward'].frames[1].setVelX = -22.8
        self.moves['standBackward'].frames[8].setVelX = 0

        for i in range(len(self.moves['standBackward'].frames)):
            self.moves['standBackward'].frames[i].setFrictionX = self.groundFriction * 0.42
            self.moves['standBackward'].frames[i].ignoreSpeedCap = True
            
    def createMoveStandAttack(self):
        
        r = [
                [
                    (17, -33, 29, -23),
                    (17, -37, 27, -32),
                    (12, -26, 23, -14),
                     (17, -14, 21, 1),
                     (0, -23, 15, -15),
                     (-4, -16, 1, -13),
                     (-7, -13, -1, -1),
                     (-15, -4, -3, -1),
                     (2, -17, 11, -10),
                     (6, -11, 16, 1)
                ]
            ]
        
        dam1 = 30
        stun1 = 30
        force1 = 20
        angle1 = 30
        freeze1 = 1
        
        h = [
                [
                    (9, -47, 63, 0, dam1, stun1, force1, angle1, [], freeze1),
                    (-11, -25, 9, 0, dam1, stun1, force1, angle1, [], freeze1)
                ]
             ]
        
        f = [ self.frameData(138, 4),
              self.frameData(139, 3),
              self.frameData(25, 2, r[0]),
              self.frameData(26, 1, r[0], h[0]),
              self.frameData(27, 2, r[0], h[0]),
              self.frameData(28, 11, r[0]) ]
        
        self.moves['standAttack'].append(f, [])
        

    def createMoveTeching(self):
        f = [ self.frameData(140, 4),
              self.frameData(140, 1)]

        self.moves['teching'].append(f, [])

    def createMoveTechUp(self):
        f = [ self.frameData(99, 3),
              self.frameData(94, 2) ]

        self.moves['techUp'].append(f, [])

    def createMoveTechForward(self):
        f = [ self.frameData(20, 1),
              self.frameData(33, 2),
              self.frameData(21, 1),
              self.frameData(24, 2),
              self.frameData(22, 1),
              self.frameData(34, 2),
              self.frameData(19, 1),
              self.frameData(23, 2),
              self.frameData(19, 1),
              self.frameData(23, 2),
              self.frameData(28, 6) ]


        self.moves['techForward'].append(f, [])

        self.moves['techForward'].frames[1].setVelX = 25
        self.moves['techForward'].frames[10].setVelX = 0

        for i in range(len(self.moves['techForward'].frames)):
            self.moves['techForward'].frames[i].setFrictionX = self.groundFriction * 0.75
            self.moves['techForward'].frames[i].ignoreSpeedCap = True

    def createMoveTechBackward(self):

        f = [ self.frameData(23, 2),
              self.frameData(19, 1),
              self.frameData(23, 2),
              self.frameData(19, 1),
              self.frameData(34, 2),
              self.frameData(22, 1),
              self.frameData(24, 2),
              self.frameData(21, 1),
              self.frameData(33, 2),
              self.frameData(20, 1),
              self.frameData(28, 6) ]


        self.moves['techBackward'].append(f, [])

        self.moves['techBackward'].frames[1].setVelX = -25
        self.moves['techBackward'].frames[10].setVelX = 0

        for i in range(len(self.moves['techBackward'].frames)):
            self.moves['techBackward'].frames[i].setFrictionX = self.groundFriction * 0.75
            self.moves['techBackward'].frames[i].ignoreSpeedCap = True

    def createSuperMove1(self):
        n = "Air Rush"
        
        d = ("Surrounds the user in a field of elemental air energy and" +
             " charges forward.  A dependable move that combos from several" +
             " normal attacks.")

        dam1 = 45
        stun1 = 155
        force1 = 19.5
        angle1 = 15
        freeze1 = 6
        h = [
                [
                    [-23, -78, 68, 18],
                    [-37, -73, -23, 16],
                    [-42, -45, -37, -1]
                ]
            ]

        for j in range(len(h)):
            h[j] = [i + [dam1, stun1, force1, angle1, [], freeze1] for i in h[j]]
        

        f = [ self.frameData(143, 2),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]),
              self.frameData(144, 1, [], h[0]),
              self.frameData(145, 1, [], h[0]),
              self.frameData(146, 1, [], h[0]) ]

        t = [['exitFrame', move.Transition(-1, None, None, None, 'super1Ending1')]]

        
        sg = move.SuperMove(n, d, f, t)

        for i in range(len(sg.frames)):
            sg.frames[i].setVelX = 19
            sg.frames[i].setVelY = 0
            sg.frames[i].ignoreSpeedCap = True
            sg.frames[i].ignoreFriction = True

            if (i % 3) == 1:
                sg.frames[i].resetHitPotential = True
        
        sg.flash = self.createSuperFlash1()
        
        
        sa = move.SuperMove(n, d, f, t)

        for i in range(len(sa.frames)):
            sa.frames[i].setVelX = 14
            sa.frames[i].setVelY = 0
            sa.frames[i].ignoreSpeedCap = True
            sa.frames[i].ignoreFriction = True

            if (i % 3) == 1:
                sa.frames[i].resetHitPotential = True
        
        sa.flash = self.createSuperFlash1Air()
        

        self.appendSuperMove(sg, sa)

        self.createSuper1Ending1()
        
    def createSuperFlash1(self):
        
        s = move.baseSuperFlash()
        
        f = [ self.frameData(87, 2),
             self.frameData(87, 16),
             self.frameData(141, 2),
             self.frameData(141, 12),
             self.frameData(142, 12),
             self.frameData(143, 2)]
        
        s.append(f, [])
        s.liftOff = True
        
        s.frames[0].setVelY = -7.4
        s.frames[0].setVelX = -6
        
        for i in range(1, 6):
            s.frames[i].ignoreFriction = True
            
        s.frames[1].setAccelY = 0.60
        s.frames[2].setAccelY = -0.05
        s.frames[3].setAccelY = -0.05
        s.frames[3].setAccelX = 0.3
        s.frames[4].setAccelY = -0.2
        s.frames[4].setAccelX = 0.3
        s.frames[4].setAccelY = -0.2
        s.frames[5].setAccelX = 0.3
        s.frames[5].setAccelY = -0.2
        
        return s
    
    def createSuperFlash1Air(self):
        
        s = move.baseSuperFlash()
        
        f = [ self.frameData(87, 22),
             self.frameData(141, 2),
             self.frameData(141, 1),
             self.frameData(142, 1),
             self.frameData(143, 1)]
        
        s.append(f, [])
        s.liftOff = True
        
        for i in range(len(s.frames)):
            s.frames[i].setVelX = 0
            s.frames[i].setVelY = 0
        
        return s


    def createSuper1Ending1(self):
        r = [
                [
                    (-19, -20, -3, -10),
                    (-12, -10, -5, -1),
                    (-14, -32, 4, -19),
                    (-7, -22, 7, -13),
                    (-7, -15, 0, -12),
                    (0, -40, 17, -23)
                ],
                [
                    (-13, -35, 5, -22),
                    (-21, -32, -8, -26),
                    (-11, -24, 11, -15),
                    (0, -29, 12, -21),
                    (-2, -17, 18, -2)
                ],
                [
                    (-21, -19, -2, -3),
                    (-4, -27, 12, -10),
                    (-2, -35, 18, -25),
                    (9, -27, 16, -22),
                    (-7, -32, 1, -22),
                    (4, -43, 13, -35),
                    (-9, -26, 3, -18)
                ]
            ]

        flippingSpeed = 3
        f = [ self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]) ]

        t = [['land', move.Transition(None, None, None, None, 'super1EndingLag1')],
             ['exitFrame', move.Transition(-1, None, None, None, 'super1Ending2')]]

        self.moves['super1Ending1'] = move.Move(f, t)
        self.moves['super1Ending1'].canDI = False
        self.moves['super1Ending1'].canRetreat = False

        self.moves['super1Ending1'].frames[0].ignoreFriction = True
        self.moves['super1Ending1'].frames[1].ignoreFriction = True

        self.createSuper1EndingLag1()
        self.createSuper1Ending2()


    def createSuper1EndingLag1(self):
        
        r = [
                [
                    (-18, -46, -5, -42),
                    (-19, -42, -3, -32),
                    (-22, -37, -12, -27),
                    (-18, -32, 5, -23),
                    (-13, -25, 3, -15),
                    (3, -25, 10, -21),
                    (7, -22, 15, -17),
                    (-13, -15, -5, 1),
                    (-8, -17, 5, -11),
                    (0, -11, 10, -7),
                    (5, -7, 13, -4),
                    (7, -4, 16, -1),
                    (9, -1, 25, 2),
                    (-25, -40, -18, -30)
                ]
             ]

        f = [ self.frameData(147, 8, r[0]),
              self.frameData(148, 14, r[0]) ]

        self.moves['super1EndingLag1'] = move.Move(f, [])
        self.moves['super1EndingLag1'].canDI = False
        self.moves['super1EndingLag1'].canRetreat = False

        self.moves['super1EndingLag1'].frames[0].setFrictionX = 0.3
        self.moves['super1EndingLag1'].frames[1].setFrictionX = 0.3

    def createSuper1Ending2(self):
        r = [
                [
                    (-19, -20, -3, -10),
                    (-12, -10, -5, -1),
                    (-14, -32, 4, -19),
                    (-7, -22, 7, -13),
                    (-7, -15, 0, -12),
                    (0, -40, 17, -23)
                ],
                [
                    (-13, -35, 5, -22),
                    (-21, -32, -8, -26),
                    (-11, -24, 11, -15),
                    (0, -29, 12, -21),
                    (-2, -17, 18, -2)
                ],
                [
                    (-21, -19, -2, -3),
                    (-4, -27, 12, -10),
                    (-2, -35, 18, -25),
                    (9, -27, 16, -22),
                    (-7, -32, 1, -22),
                    (4, -43, 13, -35),
                    (-9, -26, 3, -18)
                ],
                [
                    (-19, -40, 0, -26),
                    (-15, -27, 5, -14),
                    (-6, -17, 12, -6),
                    (3, -25, 15, -12),
                    (12, -16, 21, -10)
                ]
            ]

        
        flippingSpeed = 3
        f = [ self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]),
              self.frameData(24, flippingSpeed, r[3]),
              self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]),
              self.frameData(24, flippingSpeed, r[3]),
              self.frameData(34, flippingSpeed, r[0]),
              self.frameData(23, flippingSpeed, r[1]),
              self.frameData(33, flippingSpeed, r[2]),
              self.frameData(24, flippingSpeed, r[3]) ]

        t = [['land', move.Transition(None, None, None, None, 'super1EndingLag2')]]

        self.moves['super1Ending2'] = move.Move(f, t)
        self.moves['super1Ending2'].canDI = False
        self.moves['super1Ending2'].canRetreat = False

        self.createSuper1EndingLag2()

    def createSuper1EndingLag2(self):
        r = [
                [
                    (-9, -27, 6, -15),
                    (-14, -16, 8, -10),
                    (-7, -10, 9, 5)
                ]
            ]

        
        f = [ self.frameData(86, 16, r[0]) ]

        self.moves['super1EndingLag2'] = move.Move(f, [])
        self.moves['super1EndingLag2'].canDI = False
        self.moves['super1EndingLag2'].canRetreat = False

    def createSuperMove2(self):
        n = "Blazing Ambush"
        
        d = ("")
        
        s = move.SuperMove(n, d, [], [])

        self.superMoves.append(s)


    def createColors(self):
        self.colors =   [
                            colorswapper.ColorSlot("Clothing 1",
                            [
                                colorswapper.ColorDataSet("Team-colored",
                                [
                                    colorswapper.ColorData((70, 181, 255, 255), 5, (255, 70, 70, 255), (255, 70, 70, 255)),
                                    colorswapper.ColorData((0, 134, 223, 255), 5, (221, 0, 0, 255), (221, 0, 0, 255)),
                                    colorswapper.ColorData((23, 163, 255, 255), 5, (255, 17, 17, 255), (255, 17, 17, 255))
                                ])
                            ])
                        ]