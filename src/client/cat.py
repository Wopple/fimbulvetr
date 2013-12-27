import os
import sys
import pygame

import boundint
import battlechar
import move
import projectile

from common.constants import *
from client.constants import *

class Cat(battlechar.BattleChar):
    def __init__(self, name="Unnamed Cat", inSuper=0):
        self.name = name
        self.speciesName = "Cat"
        self.spriteSet = CAT_IMAGES
        self.superIcons = CAT_SUPER_ICONS
        self.walkVelMax = 7.0
        self.dashVelMax = 11.5
        self.runVelMax = 9.5
        self.walkAccel = 2.5
        self.dashAccel = 13.0
        self.groundFriction = 1.4
        self.airAccel = 1.5
        self.airVelMax = 8.2
        self.airFriction = 1.2
        self.airFrictionStunned = self.airFriction * 0.3
        self.vertAccel = 0.8
        self.vertVelMax = 19.5
        self.jumpVel = -18.0
        self.youIconHeight = 80
        self.blockFXPoints = [ (9, -35), (33, -32), (9, -35) ]
        self.catEnergy = boundint.BoundInt(0, CAT_ENERGY_MAX, 0)
        self.prevEnergy = self.catEnergy.value
        self.energyDelayTick = CAT_ENERGY_DELAY
        self.energy = self.catEnergy
        super(Cat, self).__init__(1000, 15)
        self.initSpecMoves()
        self.bladeChargeHit = True

        self.speciesDesc = ("An all-around warrior that wields a blade" +
                            " enchanted with Galdr runes.  Capable of both" +
                            " melee and magical ranged attacks, and" +
                            " comfortable at many distances.  Requires time" +
                            " to charge their slowly-depleting energy" +
                            " in order to maintain strength.")

        self.setSuperValue(inSuper)

    def beginBattle(self):
        super(Cat, self).beginBattle()
        self.catEnergy.change(CAT_ENERGY_BATTLE_START)
        self.energyDelayTick = 0
        self.energyIsChangable = False

    def countdownComplete(self):
        self.energyIsChangable = True

    def update(self):
        super(Cat, self).update()
        
        hitCheck = False
        if (self.attackCanHit) and (not self.bladeChargeHit):
            self.bladeChargeHit = True
        elif (not self.attackCanHit) and (self.bladeChargeHit):
            self.bladeChargeHit = False
            hitCheck = True
            
            

        if self.energyIsChangable:
            if self.currMove.chargeBlade or hitCheck:
                self.catEnergy.add(CAT_ENERGY_RECHARGE)
                self.energyDelayTick = 0
            else:
                if self.energyDelayTick < CAT_ENERGY_DELAY:
                    self.energyDelayTick += 1
                else:
                    self.catEnergy.add(-CAT_ENERGY_USAGE)

    def initSpecMoves(self):
        self.createMoveIdle()
        self.createMoveWalking()
        self.createMoveDashing()
        self.createMoveRunning()
        self.createMoveAir()
        self.createMoveFlipping()
        self.createMoveJumping()
        self.createMoveDucking()
        self.createMoveJabA()
        self.createMoveJabB()
        self.createMoveDownA()
        self.createMoveDownB()
        self.createMoveDashAttackA()
        self.createMoveDashAttackB()
        self.createMoveUpA()
        self.createMoveUpB()
        self.createNeutralAirA()
        self.createNeutralAirB()
        self.createMoveDownAirA()
        self.createMoveDownAirB()

        self.createProjectiles()
        
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
        
        self.createMoveTeching()
        self.createMoveTechUp()
        self.createMoveTechForward()
        self.createMoveTechBackward()
        
        self.createMoveGrabbing()
        self.createMoveGrabHold()
        self.createMoveGrabbed()
        self.createMoveGrabbed2()
        self.createMoveGrabRelease()
        self.createMoveGrabbedRelease()
        
        self.createMoveThrowBackward()
        self.createMoveThrowForward()
        
        self.createMoveBlock()
        self.createMoveLowBlock()

        self.createSuperMoves()

    def createSuperMoves(self):
        self.createSuperMove1()
        #self.createSuperMove2()

    def createMoveIdle(self):
        r = [
                [
                    (-11, -62, 6, -18),
                    (4, -43, 13, -37),
                    (-10, -18, -3, 1),
                    (2, -19, 8, -12),
                    (3, -12, 10, 0),
                    (5, -4, 11, 1)
                ]
             ]
        
        f = [ self.frameData(0, 2, r[0]) ]
        self.moves['idle'].append(f, [])
        
    def createMoveBlock(self):

        b = [
                [
                    (10, -68, 12, -25),
                    (1, -62, 11, -48)
                ]
            ]


        f = [ self.frameData(95, 2, [], [], b[0]) ]

        self.moves['blocking'].append(f, [])
        
        
    def createMoveLowBlock(self):

        b = [
                [
                   (12, -26, 14, 1),
                   (4, -11, 14, 1)
                ]
            ]


        f = [ self.frameData(96, 2, [], [], b[0]) ]

        self.moves['lowBlocking'].append(f, [])
        

    def createMoveWalking(self):
        r = [
                [
                    (-5, -62, 10, -45),
                    (-7, -43, 7, -17),
                    (-3, -45, 10, -38),
                    (-14, -40, -9, -26),
                    (-9, -40, -2, -37),
                    (-5, -17, 9, 0),
                    (-9, -13, -4, 0),
                    (10, -60, 13, -45)
                ]
             ]
        
        f = [ self.frameData(1, 3, r[0]),
              self.frameData(2, 3, r[0]),
              self.frameData(3, 3, r[0]),
              self.frameData(4, 3, r[0]) ]
        self.moves['walking'].append(f, [])
        
    def createMoveDashing(self):
        
        r = [
                [
                    (-2, -63, 12, -45),
                    (-3, -46, 7, -23),
                    (-5, -38, -2, -23),
                    (-10, -45, 2, -42),
                    (-8, -25, 11, -19),
                    (-11, -20, -4, -14),
                    (-14, -15, -8, -10),
                    (-17, -12, -14, -6),
                    (-20, -8, -16, -2),
                    (7, -20, 11, -14),
                    (4, -15, 9, -11),
                    (2, -12, 8, -5)
                ],
                [
                    (-2, -65, 12, -48),
                    (-4, -49, 7, -26),
                    (-6, -35, -3, -21),
                    (-5, -28, 14, -21),
                    (10, -23, 19, -18),
                    (15, -19, 22, -14),
                    (-10, -25, -4, -18),
                    (-12, -20, -8, -14),
                    (-27, -22, -9, -16),
                    (-11, -47, 1, -44)
                ]
             ]
        
        f = [self.frameData(47, 2, r[0]),
             self.frameData(44, 8, r[1])]
        
        self.moves['dashing'].append(f, [])
        
    def createMoveRunning(self):
        
        r = [
                [
                    (-2, -65, 12, -48),
                    (-4, -49, 7, -26),
                    (-6, -35, -3, -21),
                    (-5, -28, 14, -21),
                    (10, -23, 19, -18),
                    (15, -19, 22, -14),
                    (-10, -25, -4, -18),
                    (-12, -20, -8, -14),
                    (-27, -22, -9, -16),
                    (-11, -47, 1, -44)
                ],
                [
                    (0, -60, 14, -42),
                    (-2, -43, 8, -20),
                    (4, -43, 13, -37),
                    (-8, -44, 2, -39),
                    (-6, -31, -1, -19),
                    (-9, -21, 6, -14),
                    (-17, -19, -8, -13),
                    (-23, -26, -15, -18),
                    (4, -16, 12, -11),
                    (7, -12, 13, -6),
                    (9, -6, 18, 0)
                ],
                [
                    (-2, -60, 12, -42),
                    (-4, -43, 7, -20),
                    (-6, -26, 5, -17),
                    (-6, -17, 7, -8),
                    (-13, -11, -6, -1),
                    (1, -9, 7, 1),
                    (-10, -42, 2, -38)
                ],
                [
                    (-2, -63, 12, -45),
                    (-3, -46, 7, -23),
                    (-5, -38, -2, -23),
                    (-10, -45, 2, -42),
                    (-8, -25, 11, -19),
                    (-11, -20, -4, -14),
                    (-14, -15, -8, -10),
                    (-17, -12, -14, -6),
                    (-20, -8, -16, -2),
                    (7, -20, 11, -14),
                    (4, -15, 9, -11),
                    (2, -12, 8, -5)
                ]
             ]
        
        f = [self.frameData(45, 3, r[1]),
             self.frameData(46, 3, r[2]),
             self.frameData(47, 3, r[3]),
             self.frameData(44, 3, r[0]) ]
        
        self.moves['running'].append(f, [])

    def createMoveAir(self):
        r = [
                [
                    (-10, -53, 6, -37),
                    (-9, -37, 9, -11),
                    (-12, -31, -7, -26),
                    (-16, -27, -11, -16),
                    (-7, -14, -1, 5),
                    (-10, -2, -2, 7),
                    (-3, -13, 8, 2),
                    (5, -12, 11, -2)
                ]
             ]
        
        f = [ self.frameData(5, 2, r[0]) ]
        self.moves['air'].append(f, [])
        
        self.moves['air'].transitions['attackBDown'] = None
        self.moves['air'].transitions['attackBDownCharge'] = move.Transition(None, None, None, None, 'downAirB')
        
    def createMoveFlipping(self):
        r = [
                [
                    (-10, -53, 6, -37),
                    (-9, -37, 9, -11),
                    (-12, -31, -7, -26),
                    (-16, -27, -11, -16),
                    (-7, -14, -1, 5),
                    (-10, -2, -2, 7),
                    (-3, -13, 8, 2),
                    (5, -12, 11, -2)
                ]
             ]
        
        f = [ self.frameData(5, 2, r[0]) ]
        self.moves['flipping'].append(f, [])

    def createMoveJumping(self):
        r = [
                [
                    (-10, -53, 6, -37),
                    (-9, -37, 9, -11),
                    (-12, -31, -7, -26),
                    (-16, -27, -11, -16),
                    (-7, -14, -1, 5),
                    (-10, -2, -2, 7),
                    (-3, -13, 8, 2),
                    (5, -12, 11, -2)
                ]
             ]
        
        f = [ self.frameData(5, 2, r[0]) ]
        self.moves['jumping'].append(f, [])

    def createMoveDucking(self):
        r = [
                [
                    (-11, -52, 5, -10),
                    (-12, -12, -7, 2),
                    (3, -16, 9, 1),
                    (4, -3, 10, 2),
                    (5, -31, 10, -23)
                ]
            ]
        f = [ self.frameData(18, 2, r[0]) ]
        self.moves['ducking'].append(f, [])

    
    def createMoveJabA(self):
        
        r = [
                [
                    (-4, -54, 11, -12),
                    (-7, -12, 0, -7),
                    (-10, -7, -3, -3),
                    (-13, -3, -4, 1),
                    (8, -14, 15, -11),
                    (12, -11, 17, -8),
                    (12, -7, 16, -3),
                    (11, -2, 17, 1)
                ],
                [
                    (12, -50, 22, -38),
                    (12, -38, 19, -30),
                    (9, -30, 19, -20),
                    (5, -19, 20, -13),
                    (17, -13, 25, -9),
                    (20, -9, 27, 0),
                    (1, -14, 7, -10),
                    (-4, -11, 2, -7),
                    (-7, -7, 0, -4),
                    (-11, -4, -3, 0)
                ]
            ]
        
        dam1 = 70
        stun1 = 60
        force1 = 13
        angle1 = 27
        h = [
                [
                    (-27, -23, 12, -4, dam1, stun1, force1, angle1, [], 0),
                    (6, -13, 43, -4, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (22, -36, 42, -5, dam1, stun1, force1, angle1, [], 0),
                    (42, -36, 54, -8, dam1, stun1, force1, angle1, [], 0),
                    (54, -36, 64, -12, dam1, stun1, force1, angle1, [], 0),
                    (64, -36, 70, -19, dam1, stun1, force1, angle1, [], 0),
                    (70, -35, 75, -28, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (22, -69, 79, -26, dam1, stun1, force1, angle1, [], 0),
                    (8, -29, 71, -16, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (-10, -70, 56, -61, dam1, stun1, force1, angle1, [], 0),
                    (1, -61, 58, -44, dam1, stun1, force1, angle1, [], 0),
                    (8, -44, 27, -20, dam1, stun1, force1, angle1, [], 0)
                ]
            ]
        
        f = [ self.frameData(48, 5, r[0]),
              self.frameData(49, 1, r[0], h[0]),
              self.frameData(50, 1, r[1], h[1]),
              self.frameData(51, 1, r[1], h[2]),
              self.frameData(52, 1, r[1], h[3]),
              self.frameData(53, 2, r[1]),
              self.frameData(54, 9, r[1]),
              self.frameData(55, 2, r[1]) ]
        
        
        
        self.moves['jabA'].append(f, [])
        
        self.moves['jabA'].canDI = False

    def createMoveJabB(self):
        r = [
                [
                    (-12, -61, 5, -18),
                    (-11, -19, -5, 2),
                    (1, -19, 6, -12),
                    (2, -14, 9, 0)
                ],
                [
                    (-4, -55, 7, -43),
                    (-4, -42, 4, -38),
                    (-9, -38, 5, -13),
                    (3, -14, 8, -10),
                    (3, -10, 10, 0),
                    (-10, -13, -6, -7),
                    (-11, -7, -7, 1)
                ]
             ]
        
        f = [ self.frameData(19, 2, r[0]),
              self.frameData(20, 2, r[0]),
              self.frameData(21, 1, r[0]),
              self.frameData(22, 3, r[0]),
              self.frameData(23, 1, r[1])]

        t = [ ['bladelv1', move.Transition(None, None, 4, 4, 'swordbeamGround1')],
              ['bladelv2', move.Transition(None, None, 4, 4, 'swordbeamGround2')],
              ['bladelv3', move.Transition(None, None, 4, 4, 'swordbeamGround3')] ]

        self.moves['jabB'].append(f, t)
        self.moves['jabB'].canDI = False

        self.createMoveSwordBeamGroundEnd()
        
    def createMoveDashAttackA(self):
        
        dam1 = 0
        stun1 = 105
        force1 = 16
        angle1 = 16
        
        
        dam2 = 120
        stun2 = 120
        force2 = 17
        angle2 = 18
        freeze2 = 5
        
        h = [
                [
                    (-16, -33, 33, -28, dam1, stun1, force1, angle1, [], 0),
                    (-1, -39, 39, -33, dam1, stun1, force1, angle1, [], 0),
                    (23, -40, 73, -35, dam1, stun1, force1, angle1, [], 0)
                ],
                [
                    (48, -44, 83, -34, dam2, stun2, force2, angle2, [], freeze2),
                    (25, -38, 53, -30, dam2, stun2, force2, angle2, [], freeze2)
                ]
            ]
        
        r = [
                [
                    (-8, -59, 6, -44),
                    (-6, -43, 7, -40),
                    (-7, -40, 7, -18),
                    (-7, -19, -3, 3),
                    (4, -19, 8, -14),
                    (5, -14, 9, -11),
                    (3, -10, 6, -3),
                    (2, -3, 6, 2)
                ],
                [
                    (-11, -58, 2, -47),
                    (-7, -46, 2, -42),
                    (-8, -43, 5, -19),
                    (-8, -20, -4, 1),
                    (2, -19, 6, -15),
                    (4, -15, 7, -9),
                    (2, -9, 5, -5),
                    (0, -4, 5, 1)
                ],
                [
                    (11, -47, 20, -41),
                    (9, -36, 18, -14)
                ],
                [
                    (25, -49, 35, -37),
                    (21, -38, 30, -27),
                    (17, -31, 26, -20),
                    (24, -28, 29, -23),
                    (15, -37, 23, -31),
                    (13, -26, 19, -14),
                    (19, -22, 25, -13),
                    (21, -13, 29, -9),
                    (27, -11, 33, -6),
                    (25, -7, 29, 0),
                    (8, -18, 13, -14),
                    (5, -14, 10, -11),
                    (3, -12, 7, -8),
                    (1, -9, 4, -6),
                    (-3, -7, 2, -3),
                    (-4, -3, 0, -1),
                    (-7, -2, -2, 0)
                ]
            ]
        
        f = [ self.frameData(14, 2, r[0]),
              self.frameData(15, 2, r[1]),
              self.frameData(17, 4, r[2], h[0]),
              self.frameData(43, 5, r[3], h[1]),
              self.frameData(43, 7, r[3])]
        
        self.moves['dashAttackA'].append(f, [])
        self.moves['dashAttackA'].canDI = False
        
        self.moves['dashAttackA'].frames[2].setVelX = 30
        self.moves['dashAttackA'].frames[2].ignoreSpeedCap = True
        self.moves['dashAttackA'].frames[2].ignoreFriction = True
        self.moves['dashAttackA'].frames[3].setVelX = 0
        self.moves['dashAttackA'].frames[3].resetHitPotential = True
        
        
    def createMoveDashAttackB(self):
        
        r = [
                [
                    (-6, -56, 6, -17),
                    (-3, -17, 2, 1)
                ],
                [
                    (1, -55, 13, -42),
                    (0, -42, 9, -30),
                    (-4, -30, 7, -17),
                    (-6, -19, -3, -10),
                    (-8, -11, -5, 0),
                    (5, -18, 10, -15),
                    (6, -16, 12, -11),
                    (7, -12, 13, 0)
                ]
            ]
        
        
        dam1 = 145
        stun1 = 120
        force1 = 15
        angle1 = 13
        freeze1 = 6
        h = [
                [
                    (-11, -37, 43, -30, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (4, -43, 71, -29, dam1, stun1, force1, angle1, [], freeze1),
                    (-5, -40, 15, -31, dam1, stun1, force1, angle1, [], freeze1),
                    (14, -52, 61, -40, dam1, stun1, force1, angle1, [], freeze1),
                    (56, -48, 67, -40, dam1, stun1, force1, angle1, [], freeze1),
                    (-5, -31, 8, -23, dam1, stun1, force1, angle1, [], freeze1)
                ]
            ]
        
        f = [ self.frameData(145, 4, r[0]),
              self.frameData(146, 1, r[0]),
              self.frameData(147, 1, r[0]),
              self.frameData(148, 2, r[0]),
              self.frameData(149, 2, r[0]),
              self.frameData(150, 2, r[0]),
              self.frameData(151, 2, r[0]),
              self.frameData(152, 2, r[0]),
              self.frameData(153, 1, r[1], h[0]),
              self.frameData(154, 1, r[1], h[1]),
              self.frameData(155, 1, r[1], h[1]),
              self.frameData(156, 8, r[1]) ]
        
        t = [ ['super', move.Transition(None, None, 9, 11, 'superFlash')] ]
        
        self.moves['dashAttackB'].append(f, t)
        
        frames = self.moves['dashAttackB'].frames
        
        frames[0].setVelX = 10
        
        
        for i in range(0, 10):
            frames[i].setSpeedCapX = 10.5
            frames[i].setFrictionX = 0.65
            
        for i in range(10, len(frames)):
            frames[i].setVelX = 0
            
        

    def createMoveSwordBeamGroundEnd(self):
        
        r = [
                [
                    (-1, -59, 11, -41),
                    (-2, -40, 8, -30),
                    (-5, -31, 6, -19),
                    (-8, -21, 8, -15),
                    (-10, -15, -5, -8),
                    (-11, -8, -7, 1),
                    (3, -16, 9, -12),
                    (5, -12, 11, 0),
                    (8, -38, 15, -32)
                ],
                [
                    (-11, -62, 6, -18),
                    (4, -43, 13, -37),
                    (-10, -18, -3, 1),
                    (2, -19, 8, -12),
                    (3, -12, 10, 0),
                    (5, -4, 11, 1)
                ]
            ]
        
        f = [ self.frameData(24, 2, r[0]),
              self.frameData(25, 1, r[0]),
              self.frameData(26, 10, r[0]),
              self.frameData(0, 2, r[1]) ]
        
        t = [ ['super', move.Transition(None, None, 1, 3, 'superFlash')] ]

        self.moves['swordbeamGround1'] = move.Move(f, t)
        self.moves['swordbeamGround1'].canDI = False
        self.moves['swordbeamGround1'].shoot.append( (0, 0, (45, -30)) )

        self.moves['swordbeamGround2'] = move.Move(f, t)
        self.moves['swordbeamGround2'].canDI = False
        self.moves['swordbeamGround2'].shoot.append( (0, 1, (45, -30)) )

        self.moves['swordbeamGround3'] = move.Move(f, t)
        self.moves['swordbeamGround3'].canDI = False
        self.moves['swordbeamGround3'].shoot.append( (0, 2, (45, -30)) )
        
        
        
        
    def createNeutralAirA(self):
        dam1 = 70
        stun1 = 60
        force1 = 12
        angle1 = 20
        freeze1 = 5
        
        h = [
                [
                    (-25, -45, -5, -31, dam1, stun1, force1, angle1, [], freeze1),
                    (-10, -42, 16, -26, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (-5, -40, 58, -21, dam1, stun1, force1, angle1, [], freeze1),
                    (8, -45, 72, -29, dam1, stun1, force1, angle1, [], freeze1)
                ]
             ]
        
        f = [ self.frameData(120, 3, []),
              self.frameData(121, 2, [], h[0]),
              self.frameData(122, 1, [], h[1]),
              self.frameData(123, 1, [], h[1]),
              self.frameData(124, 2, []),
              self.frameData(125, 4, []),
              self.frameData(124, 5, [])]
        
        t = [['land', move.Transition(None, None, None, None, 'neutralAirALag')]]
        
        self.moves['neutralAirA'].append(f, t)
        self.moves['neutralAirA'].reversable = True
        
        self.createMoveNeutralAirALag()

    def createNeutralAirB(self):
        r = [
                [
                    (-11, -58, 3, -10)
                ],
                [
                    (-4, -55, 7, -42),
                    (-4, -41, 5, -38),
                    (-8, -38, 4, -13),
                    (0, -15, 7, -10),
                    (2, -10, 6, -4),
                    (-9, -14, -5, -9),
                    (-12, -9, -7, -3)
                ]
            ]
        
        f = [ self.frameData(34, 3, r[0]),
              self.frameData(35, 3, r[0]),
              self.frameData(36, 3, r[0]),
              self.frameData(37, 3, r[0]),
              self.frameData(38, 1, r[1])]

        t = [ ['bladelv1', move.Transition(None, None, 4, 4, 'swordbeamAir1')],
              ['bladelv2', move.Transition(None, None, 4, 4, 'swordbeamAir2')],
              ['bladelv3', move.Transition(None, None, 4, 4, 'swordbeamAir3')],
              ['land', move.Transition(None, None, None, None, 'neutralAirBLag')] ]

        self.moves['neutralAirB'].append(f, t)
        self.moves['neutralAirB'].reversable = True

        self.createMoveSwordBeamAirEnd()

        self.createMoveNeutralAirBLag()
        
    def createMoveNeutralAirALag(self):
        r = [
                [
                    (-1, -59, 11, -41),
                    (-2, -40, 8, -30),
                    (-5, -31, 6, -19),
                    (-8, -21, 8, -15),
                    (-10, -15, -5, -8),
                    (-11, -8, -7, 1),
                    (3, -16, 9, -12),
                    (5, -12, 11, 0),
                    (8, -38, 15, -32)
                ]
            ]
        
        f = [ self.frameData(26, 6, r[0]) ]
        self.moves['neutralAirALag'] = move.Move(f, [])
        self.moves['neutralAirALag'].canDI = False

    def createMoveSwordBeamAirEnd(self):
        r = [
                [
                    (0, -53, 12, -40),
                    (0, -40, 7, -32),
                    (-4, -33, 6, -22),
                    (-6, -22, 7, -16),
                    (-7, -16, -4, -9),
                    (-9, -9, -5, 0),
                    (3, -16, 9, -14),
                    (5, -14, 8, -3)
                ],
                [
                    (-10, -53, 6, -37),
                    (-9, -37, 9, -11),
                    (-12, -31, -7, -26),
                    (-16, -27, -11, -16),
                    (-7, -14, -1, 5),
                    (-10, -2, -2, 7),
                    (-3, -13, 8, 2),
                    (5, -12, 11, -2)
                ]
            ]
        
        f = [ self.frameData(39, 2, r[0]),
              self.frameData(40, 1, r[0]),
              self.frameData(41, 12, r[0]),
              self.frameData(5, 2, r[1]) ]
        t = [['land', move.Transition(None, None, None, None, 'neutralAirBLag')]]

        self.moves['swordbeamAir1'] = move.Move(f, t)
        self.moves['swordbeamAir1'].shoot.append( (0, 0, (64, -30)) )

        self.moves['swordbeamAir2'] = move.Move(f, t)
        self.moves['swordbeamAir2'].shoot.append( (0, 1, (64, -30)) )

        self.moves['swordbeamAir3'] = move.Move(f, t)
        self.moves['swordbeamAir3'].shoot.append( (0, 2, (64, -30)) )

    def createMoveNeutralAirBLag(self):
        r = [
                [
                    (-1, -59, 11, -41),
                    (-2, -40, 8, -30),
                    (-5, -31, 6, -19),
                    (-8, -21, 8, -15),
                    (-10, -15, -5, -8),
                    (-11, -8, -7, 1),
                    (3, -16, 9, -12),
                    (5, -12, 11, 0),
                    (8, -38, 15, -32)
                ]
            ]
        
        f = [ self.frameData(26, 8, r[0]) ]
        self.moves['neutralAirBLag'] = move.Move(f, [])
        self.moves['neutralAirBLag'].canDI = False
        
    
    def createMoveDownAirA(self):
        
        r = [
                [
                    (11, -47, 20, -38),
                    (7, -42, 15, -34),
                    (2, -37, 12, -27),
                    (-1, -28, 8, -20),
                    (-5, -21, 5, -12),
                    (-8, -13, 0, -4),
                    (-12, -5, -4, 5)
                ]
            ]
        
        dam1 = 85
        stun1 = 70
        force1 = 12
        angle1 = 290
        freeze1 = 3
        
        h = [
                [
                    (-3, -33, 13, -19, dam1, stun1, force1, angle1, [], freeze1),
                    (7, -28, 25, -13, dam1, stun1, force1, angle1, [], freeze1),
                    (18, -24, 35, -8, dam1, stun1, force1, angle1, [], freeze1),
                    (26, -16, 45, -3, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (-5, -33, 46, -13, dam1, stun1, force1, angle1, [], freeze1),
                    (20, -38, 41, -31, dam1, stun1, force1, angle1, [], freeze1),
                    (24, -13, 71, 0, dam1, stun1, force1, angle1, [], freeze1),
                    (45, -29, 69, -10, dam1, stun1, force1, angle1, [], freeze1),
                    (14, -13, 28, -7, dam1, stun1, force1, angle1, [], freeze1)
                ]
            ]
        
    
        f = [ self.frameData(157, 5, r[0] ),
              self.frameData(158, 2, r[0] ),
              self.frameData(159, 2, r[0] ),
              self.frameData(160, 1, r[0], h[0] ),
              self.frameData(161, 1, r[0], h[1] ),
              self.frameData(162, 1, r[0], h[1] ),
              self.frameData(163, 2, r[0] ),
              self.frameData(164, 3, r[0] ),
              self.frameData(165, 3, r[0] ),
              self.frameData(157, 3, r[0] ),
              self.frameData(158, 4, r[0] ),
              self.frameData(159, 4, r[0] ) ]
        
        t = [ ['land', move.Transition(None, None, None, None, 'downAirALag')],
              ['attackADown', move.Transition(None, None, 9, 10, 'downAirA')] ]
        
        self.moves['downAirA'] = move.Move(f, t)
        
        self.moves['downAirA'].reversable = True
        
        self.createMoveDownAirALag()
        
        
    def createMoveDownAirALag(self):
        r = [
                [
                    (-1, -59, 11, -41),
                    (-2, -40, 8, -30),
                    (-5, -31, 6, -19),
                    (-8, -21, 8, -15),
                    (-10, -15, -5, -8),
                    (-11, -8, -7, 1),
                    (3, -16, 9, -12),
                    (5, -12, 11, 0),
                    (8, -38, 15, -32)
                ]
            ]
        
        f = [ self.frameData(26, 7, r[0]) ]
        self.moves['downAirALag'] = move.Move(f, [])
        self.moves['downAirALag'].canDI = False
        
    
    def createMoveDownAirB(self):
        
        r = [
                [
                    (-7, -46, 5, -36),
                    (-6, -32, 4, -11),
                    (-6, -11, -2, 0),
                    (1, -11, 5, 2)
                ]
            ]
        
        f = [ self.frameData(135, 5, r[0] ),
              self.frameData(136, 2, r[0] )]
        
        t = [ ['bladelv1', move.Transition(None, None, 1, 1, 'downAirBolt1')],
              ['bladelv2', move.Transition(None, None, 1, 1, 'downAirBolt2')],
              ['bladelv3', move.Transition(None, None, 1, 1, 'downAirBolt3')] ]
        
        
        self.moves['downAirB'].append(f, t)
        
        self.createMoveDownBoltShooting()
        
        
    def createMoveDownBoltShooting(self):
        
        r = [
                [
                    (-7, -46, 5, -36),
                    (-6, -32, 4, -11),
                    (-6, -11, -2, 0),
                    (1, -11, 5, 2)
                ]
            ]
        
        f = [ self.frameData(137, 2, r[0] ),
              self.frameData(137, 1, r[0] ) ]
        
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'downAirBoltEnd')] ]
        
        self.moves['downAirBolt1'] = move.Move(f, t)
        self.moves['downAirBolt1'].shoot.append( (0, 3, (6, 5)) )
        
        self.moves['downAirBolt2'] = move.Move(f, t)
        self.moves['downAirBolt2'].shoot.append( (0, 4, (6, 5)) )
        
        self.moves['downAirBolt3'] = move.Move(f, t)
        self.moves['downAirBolt3'].shoot.append( (0, 5, (6, 5)) )
        
        self.createMoveDownBoltEnd()
        
    def createMoveDownBoltEnd(self):
        
        r = [
                [
                    (-7, -46, 5, -36),
                    (-6, -32, 4, -11),
                    (-6, -11, -2, 0),
                    (1, -11, 5, 2)
                ]
            ]
        
        f = [ self.frameData(137, 2, r[0] ),
              self.frameData(137, 8, r[0] ) ]
        
        t = []
        
        
        self.moves['downAirBoltEnd'] = move.Move(f, t)
        self.moves['downAirBoltEnd'].frames[0].setVelYIfDrop = -10
        self.moves['downAirBoltEnd'].frames[0].setAccelY = 0
        self.moves['downAirBoltEnd'].frames[0].setVelX = 0
        self.moves['downAirBoltEnd'].frames[0].setAccelX = 0


    def createMoveUpA(self):
        
        r = [
                [
                    (-6, -56, 6, -17),
                    (-7, -17, -4, -4),
                    (-9, -6, -5, 1),
                    (4, -18, 7, -13),
                    (5, -13, 10, -8),
                    (6, -9, 12, 0)
                ]
            ]
        
        h = [
                [
                    [34, -84, 47, -67],
                    [39, -71, 54, -57],
                    [44, -59, 60, -47]
                ],
                [
                    [9, -98, 24, -85],
                    [19, -92, 35, -80],
                    [28, -86, 48, -73]
                ],
                [
                    [-20, -99, 27, -88]
                ],
                [
                    [-45, -85, -27, -74],
                    [-34, -91, -15, -81],
                    [-25, -97, -10, -90],
                    [-48, -76, -34, -68]
                ],
                [
                    [-51, -79, -40, -60],
                    [-53, -61, -45, -46],
                    [-56, -48, -47, -35]
                ],
                [
                    [-58, -44, -47, -33],
                    [-55, -34, -43, -25],
                    [-50, -26, -39, -16],
                    [-47, -17, -36, -6]
                ],
                [
                    [-33, -13, -18, -3],
                    [-22, -10, -7, 0],
                    [-14, -6, 1, 4],
                    [-3, -2, 10, 6]
                ],
                [
                    [-10, -3, 9, 8],
                    [5, -4, 20, 4],
                    [13, -6, 34, 2]
                ],
                [
                    [46, -36, 57, -23],
                    [43, -25, 51, -16],
                    [40, -20, 45, -10],
                    [35, -12, 44, -2],
                    [31, -5, 39, 4]
                ],
                [
                    [45, -62, 60, -17]
                ],
                [
                    [28, -88, 41, -76],
                    [35, -78, 45, -70],
                    [40, -71, 50, -64],
                    [44, -65, 55, -57],
                    [48, -57, 58, -52]
                ],
                [
                    [6, -97, 18, -89],
                    [14, -92, 28, -85],
                    [23, -87, 36, -81],
                    [31, -84, 45, -76]
                ],
                [
                    [-20, -98, 26, -88]
                ],
                [
                    [-39, -88, -24, -80],
                    [-29, -90, -17, -84],
                    [-20, -94, -9, -88],
                    [-15, -98, 0, -92]
                ],
                [
                    [-37, -89, -31, -79],
                    [-40, -82, -35, -71],
                    [-44, -75, -39, -67],
                    [-48, -68, -41, -61],
                    [-52, -62, -45, -55],
                    [-55, -57, -48, -51]
                ],
                [
                    [-57, -46, -48, -36],
                    [-54, -37, -44, -27],
                    [-51, -28, -42, -19],
                    [-48, -20, -40, -12],
                    [-45, -13, -38, -7]
                ],
                [
                    [-33, -13, -16, -3],
                    [-22, -10, -5, 1],
                    [-10, -5, 6, 5]
                ],
                [
                    [1, -2, 18, 6],
                    [13, -5, 29, 1],
                    [25, -8, 39, -2],
                    [33, -10, 42, -6]
                ],
                [
                    [39, -36, 49, -27],
                    [35, -28, 44, -18],
                    [30, -21, 36, -12],
                    [27, -14, 33, -7],
                    [23, -8, 29, -2]
                ]
             ]
        
        dam1 = 35
        stun1 = 150
        force1 = 14
        angle1 = 95
        freeze1 = 3
        
        for j in range(len(h)):
            h[j] = [i + [dam1, stun1, force1, angle1, [], freeze1] for i in h[j]]
        
        
        f = [ self.frameData(116, 5, r[0]),
              self.frameData(97, 3, r[0], h[0]),
              self.frameData(98, 3, r[0], h[1]),
              self.frameData(99, 2, r[0], h[2]),
              self.frameData(100, 2, r[0], h[3]),
              self.frameData(101, 2, r[0], h[4]),
              self.frameData(102, 2, r[0], h[5]),
              self.frameData(103, 1, r[0], h[6]),
              self.frameData(104, 1, r[0], h[7]),
              self.frameData(105, 1, r[0], h[8]),
              self.frameData(106, 2, r[0], h[9]),
              self.frameData(107, 2, r[0], h[10]),
              self.frameData(108, 2, r[0], h[11]),
              self.frameData(109, 2, r[0], h[12]),
              self.frameData(110, 2, r[0], h[13]),
              self.frameData(111, 2, r[0], h[14]),
              self.frameData(112, 1, r[0], h[15]),
              self.frameData(113, 1, r[0], h[16]),
              self.frameData(114, 2, r[0], h[17]),
              self.frameData(115, 3, r[0], h[18]),
              self.frameData(116, 6, r[0]) ]
        
        t = [['attackA', move.Transition(None, None, 17, 20, 'jabA')],
             ['attackAUp', move.Transition(None, None, 17, 20, 'jabA')],
             ['attackB', move.Transition(3, CAT_ENERGY_SECTIONS[1], 17, 20, 'aetherpiercer')],
             ['attackBUp', move.Transition(3, CAT_ENERGY_SECTIONS[1], 17, 20, 'aetherpiercer')]]
        
        self.moves['upA'].append(f, t)
        self.moves['upA'].canDI = False
        self.moves['upA'].frames[7].resetHitPotential = True
        self.moves['upA'].frames[17].resetHitPotential = True
        
        self.createMoveAetherPiercer()
        
    def createMoveAetherPiercer(self):
        
        
        r = [
                [
                    (4, -51, 17, -39),
                    (4, -38, 14, -26),
                    (1, -27, 11, -14),
                    (-4, -15, 0, -10),
                    (-6, -9, -2, -3),
                    (-10, -3, -5, 2),
                    (-1, -17, 13, -12),
                    (11, -13, 17, 1)
                ]
            ]

        
        dam1 = 0
        stun1 = 150
        force1 = 8
        angle1 = 75
        freeze1 = 0
        
        dam2 = 110
        stun2 = 230
        force2 = 34
        angle2 = 70
        freeze2 = 15
        
        h = [
                [
                    (22, -61, 41, -28, dam1, stun1, force1, angle1, [], freeze1),
                    (12, -36, 30, -4, dam1, stun1, force1, angle1, [], freeze1)

                ],
                [
                    (22, -61, 41, -28, dam2, stun2, force2, angle2, [], freeze2),
                    (12, -36, 30, -4, dam2, stun2, force2, angle2, [], freeze2),
                    (29, -101, 48, -71, dam2, stun2, force2, angle2, [], freeze2),
                    (40, -108, 56, -85, dam2, stun2, force2, angle2, [], freeze2),
                    (21, -82, 41, -48, dam2, stun2, force2, angle2, [], freeze2)
                ]
             ]
        
        f = [ self.frameData(117, 4, r[0]),
              self.frameData(118, 1, r[0], h[0]),
              self.frameData(119, 5, r[0], h[1]),
              self.frameData(119, 18, r[0])]
        
        t = []
        
        self.moves['aetherpiercer'] = move.Move(f, t)
        self.moves['aetherpiercer'].canDI = False
        
        self.moves['aetherpiercer'].frames[1].setVelX = 2.5
        self.moves['aetherpiercer'].frames[2].resetHitPotential = True
        
        self.moves['aetherpiercer'].frames[2].fx.append(['fullshockwave', (42, -97), True])
        

    def createMoveUpB(self):
        
        r = [
                [
                    (-18, -59, 9, -41),
                    (-10, -42, 5, -18),
                    (-10, -19, -3, 1),
                    (-1, -19, 7, -12),
                    (2, -14, 8, -7),
                    (3, -9, 10, 1)
                ]
             ]
        
        f = [ self.frameData(6, 4, r[0]),
              self.frameData(7, 4, r[0]),
              self.frameData(8, 3, r[0]),
              self.frameData(9, 3, r[0])]
        t = [ ['releaseB', move.Transition(None, None, 2, None, 'idle')],
              ['exitFrame', move.Transition(-1, None, None, None, 'chargeSword')] ]
        self.moves['upB'].append(f, t)
        self.moves['upB'].canDI = False

        self.createMoveChargeSword()

    def createMoveChargeSword(self):
        r = [
                [
                    (-18, -59, 9, -41),
                    (-10, -42, 5, -18),
                    (-10, -19, -3, 1),
                    (-1, -19, 7, -12),
                    (2, -14, 8, -7),
                    (3, -9, 10, 1)
                ]
             ]
        
        f = [ self.frameData(10, 2, r[0]),
              self.frameData(11, 2, r[0]),
              self.frameData(12, 2, r[0]),
              self.frameData(13, 2, r[0]),
              self.frameData(11, 2, r[0]),
              self.frameData(10, 2, r[0]),
              self.frameData(12, 2, r[0]),
              self.frameData(11, 2, r[0]),
              self.frameData(10, 2, r[0]),
              self.frameData(13, 2, r[0]),
              self.frameData(12, 2, r[0]),
              self.frameData(10, 2, r[0]),
              self.frameData(13, 2, r[0]),
              self.frameData(11, 2, r[0]) ]
        
        t = [ ['releaseB', move.Transition(None, None, None, None, 'idle')],
              ['exitFrame', move.Transition(-1, None, None, None, 'chargeSword')] ]
        self.moves['chargeSword'] = move.Move(f, t)
        self.moves['chargeSword'].canDI = False
        self.moves['chargeSword'].chargeBlade = True
        
        self.moves['chargeSword'].frames[0].fx.append(['runicflame1', (-20, -63), True])
        self.moves['chargeSword'].frames[1].fx.append(['runicflame2', (5, -65), False])
        self.moves['chargeSword'].frames[2].fx.append(['runicflame3', (-8, -63), True])
        self.moves['chargeSword'].frames[3].fx.append(['runicflame1', (-13, -63), True])
        self.moves['chargeSword'].frames[4].fx.append(['runicflame2', (2, -66), True])
        self.moves['chargeSword'].frames[5].fx.append(['runicflame3', (-18, -63), False])
        self.moves['chargeSword'].frames[6].fx.append(['runicflame1', (-16, -67), True])
        self.moves['chargeSword'].frames[7].fx.append(['runicflame2', (0, -63), False])
        self.moves['chargeSword'].frames[8].fx.append(['runicflame3', (-3, -67), True])
        self.moves['chargeSword'].frames[9].fx.append(['runicflame1', (-18, -62), False])
        self.moves['chargeSword'].frames[10].fx.append(['runicflame2', (-6, -63), True])
        self.moves['chargeSword'].frames[11].fx.append(['runicflame3', (4, -63), False])
        self.moves['chargeSword'].frames[12].fx.append(['runicflame3', (-14, -66), False])
        self.moves['chargeSword'].frames[13].fx.append(['runicflame2', (-2, -63), True])
        
        self.moves['chargeSword'].frames[0].fx.append(['runicflame3', (0, -63), True])
        self.moves['chargeSword'].frames[1].fx.append(['runicflame1', (-14, -65), False])
        self.moves['chargeSword'].frames[2].fx.append(['runicflame2', (-18, -63), True])
        self.moves['chargeSword'].frames[3].fx.append(['runicflame3', (-2, -63), True])
        self.moves['chargeSword'].frames[4].fx.append(['runicflame1', (-6, -66), True])
        self.moves['chargeSword'].frames[5].fx.append(['runicflame2', (-15, -63), False])
        self.moves['chargeSword'].frames[6].fx.append(['runicflame3', (3, -66), True])
        self.moves['chargeSword'].frames[7].fx.append(['runicflame1', (-2, -63), False])
        self.moves['chargeSword'].frames[8].fx.append(['runicflame1', (-6, -67), True])
        self.moves['chargeSword'].frames[9].fx.append(['runicflame2', (-13, -62), False])
        self.moves['chargeSword'].frames[10].fx.append(['runicflame2', (4, -63), True])
        self.moves['chargeSword'].frames[11].fx.append(['runicflame3', (8, -63), False])
        self.moves['chargeSword'].frames[12].fx.append(['runicflame1', (-11, -68), False])
        self.moves['chargeSword'].frames[13].fx.append(['runicflame2', (-1, -63), True])
        
        for f in self.moves['chargeSword'].frames:
            f.resetCanEffect = True
            
    def createMoveDownA(self):
        
        r = [
                [
                    (2, -50, 12, -36),
                    (1, -36, 11, -27),
                    (-6, -34, 4, -25),
                    (-4, -26, 8, -14),
                    (-9, -16, 9, -11),
                    (-10, -11, -5, 1),
                    (5, -12, 14, -7),
                    (-2, -8, 7, -3),
                    (-7, -4, 0, 0)
                ],
                [
                    (10, -46, 23, -33),
                    (8, -35, 17, -24),
                    (3, -32, 14, -19),
                    (-1, -24, 9, -10),
                    (6, -23, 16, -3),
                    (-3, -5, 9, -1),
                    (-6, -16, 0, -10),
                    (-9, -11, -4, -3)
                ],
                [
                    (25, -39, 36, -27),
                    (19, -30, 30, -21),
                    (25, -22, 32, -14),
                    (27, -15, 33, -9),
                    (29, -10, 35, -1),
                    (13, -28, 21, -21),
                    (13, -22, 22, -17),
                    (6, -23, 15, -18),
                    (6, -19, 17, -12),
                    (0, -19, 11, -13),
                    (6, -13, 14, -8),
                    (9, -9, 17, -2),
                    (-2, -5, 15, -1),
                    (-7, -2, 1, 1),
                    (-3, -15, 2, -10),
                    (-7, -11, -1, -6),
                    (-10, -8, -3, -3),
                    (-10, -4, -5, 0)
                ]
            ]
        
        
        dam1 = 60
        stun1 = 90
        force1 = 22
        angle1 = 72
        freeze1 = 2
        
        
        h= [
                [
                    (6, -28, 39, -11, dam1, stun1, force1, angle1, [], freeze1),
                    (20, -18, 59, -5, dam1, stun1, force1, angle1, [], freeze1),
                    (49, -23, 69, -9, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (32, -51, 58, -9, dam1, stun1, force1, angle1, [], freeze1),
                    (48, -55, 80, -33, dam1, stun1, force1, angle1, [], freeze1),
                    (56, -34, 78, -23, dam1, stun1, force1, angle1, [], freeze1),
                    (54, -24, 72, -15, dam1, stun1, force1, angle1, [], freeze1),
                    (54, -16, 67, -11, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (4, -80, 28, -40, dam1, stun1, force1, angle1, [], freeze1),
                    (25, -76, 41, -42, dam1, stun1, force1, angle1, [], freeze1),
                    (39, -73, 50, -35, dam1, stun1, force1, angle1, [], freeze1),
                    (49, -69, 59, -55, dam1, stun1, force1, angle1, [], freeze1),
                    (54, -62, 64, -50, dam1, stun1, force1, angle1, [], freeze1),
                    (59, -54, 68, -43, dam1, stun1, force1, angle1, [], freeze1),
                    (46, -55, 59, -20, dam1, stun1, force1, angle1, [], freeze1),
                    (12, -42, 48, -17, dam1, stun1, force1, angle1, [], freeze1)
                ],
                [
                    (-33, -59, 16, -39, dam1, stun1, force1, angle1, [], freeze1),
                    (-32, -68, 21, -49, dam1, stun1, force1, angle1, [], freeze1),
                    (-27, -75, 27, -56, dam1, stun1, force1, angle1, [], freeze1),
                    (-19, -80, 37, -71, dam1, stun1, force1, angle1, [], freeze1),
                    (8, -70, 34, -33, dam1, stun1, force1, angle1, [], freeze1),
                    (-17, -42, 22, -24, dam1, stun1, force1, angle1, [], freeze1)
                ]
            ]
        
        f = [ self.frameData(172, 3, r[0]),
              self.frameData(173, 2, r[1], h[0]),
              self.frameData(174, 1, r[2], h[1]),
              self.frameData(175, 1, r[2], h[2]),
              self.frameData(176, 2, r[2], h[3]),
              self.frameData(177, 2, r[2]),
              self.frameData(178, 2, r[2]),
              self.frameData(179, 4, r[2]),
              self.frameData(177, 2, r[2]),
              self.frameData(172, 2, r[0]) ]
        
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'ducking')],
              ['jump', move.Transition(None, None, 6, 8, 'jumping')] ]

        self.moves['downA'].append(f, t)
        self.moves['downA'].canDI = False
        

    def createOldMoveDownA(self):
        
        dam1 = 85
        stun1 = 45
        force1 = 14
        angle1 = 32
        freeze1 = 2
        
        r = [
                [
                    (10, -49, 22, -38),
                    (9, -37, 19, -27),
                    (6, -27, 15, -17),
                    (1, -17, 14, -12),
                    (-1, -12, 2, -6),
                    (-4, -9, -1, -5),
                    (-7, -5, -3, -2),
                    (14, -13, 21, -10),
                    (16, -10, 21, -5),
                    (16, -5, 20, 0),
                    (5, -35, 10, -25),
                    (-2, -34, 8, -31),
                    (19, -34, 24, -29),
                    (23, -30, 28, -25)
                ],
                [
                    (25, -49, 35, -37),
                    (21, -38, 30, -27),
                    (17, -31, 26, -20),
                    (24, -28, 29, -23),
                    (15, -37, 23, -31),
                    (13, -26, 19, -14),
                    (19, -22, 25, -13),
                    (21, -13, 29, -9),
                    (27, -11, 33, -6),
                    (25, -7, 29, 0),
                    (8, -18, 13, -14),
                    (5, -14, 10, -11),
                    (3, -12, 7, -8),
                    (1, -9, 4, -6),
                    (-3, -7, 2, -3),
                    (-4, -3, 0, -1),
                    (-7, -2, -2, 0)
                ],
                [
                    (-11, -52, 5, -10),
                    (-12, -12, -7, 2),
                    (3, -16, 9, 1),
                    (4, -3, 10, 2),
                    (5, -31, 10, -23)
                ]
            ]
        
        h = [
                [
                    (48, -44, 83, -34, dam1, stun1, force1, angle1, [], freeze1),
                    (25, -38, 53, -30, dam1, stun1, force1, angle1, [], freeze1)
                ]
             ]
        
        f = [ self.frameData(42, 2, r[0]),
              self.frameData(43, 6, r[1], h[0]),
              self.frameData(43, 2, r[1]),
              self.frameData(42, 2, r[0]),
              self.frameData(18, 2, r[2])]

        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'ducking')] ]

        self.moves['downA'].append(f, t)
        self.moves['downA'].canDI = False
        
    def createMoveDownB(self):
        
        dam1 = 22
        stun1 = 101
        force1 = 5
        angle1 = 90
        freeze1 = 2
        
        r = [
                [
                    (-7, -55, 4, -44),
                    (-7, -43, 3, -18),
                    (-10, -18, -6, -10),
                    (-12, -10, -8, 0),
                    (1, -19, 5, -14),
                    (3, -14, 7, -10),
                    (4, -10, 9, 0),
                    (8, -3, 13, 1)
                ]
            ]
        
        h = [
                [
                    (16, -12, 86, 3, dam1, stun1, force1, angle1, [('untechable')], freeze1),
                ]
            ]
        
        f = [self.frameData(22, 4, r[0]),
             self.frameData(56, 1, r[0]),
             self.frameData(57, 2, r[0]),
             self.frameData(58, 2, r[0]),
             self.frameData(59, 2, r[0]),
             
             self.frameData(60, 1, r[0], h[0]),
             self.frameData(61, 1, r[0], h[0]),
             self.frameData(62, 1, r[0], h[0]),
             self.frameData(63, 1, r[0], h[0]),
             self.frameData(60, 1, r[0], h[0]),
             self.frameData(61, 1, r[0], h[0]),
             self.frameData(62, 1, r[0], h[0]),
             self.frameData(63, 1, r[0], h[0]),
             self.frameData(60, 1, r[0], h[0]),
             self.frameData(61, 1, r[0], h[0]),
             self.frameData(62, 1, r[0], h[0]),
             self.frameData(63, 1, r[0], h[0]),
             self.frameData(60, 1, r[0], h[0]),
             self.frameData(61, 1, r[0], h[0]),
             self.frameData(62, 1, r[0], h[0]),
             self.frameData(63, 1, r[0], h[0]),
             self.frameData(60, 1, r[0], h[0]),
             self.frameData(61, 1, r[0], h[0]),
             self.frameData(62, 1, r[0], h[0]),
             self.frameData(63, 1, r[0], h[0]),
             
             self.frameData(58, 2, r[0]),
             self.frameData(57, 2, r[0]),
             self.frameData(22, 10, r[0]) ]
        
        t = [['attackB', move.Transition(3, CAT_ENERGY_SECTIONS[0], 6, 25, 'lowexplosion')],
             ['attackBDown', move.Transition(3, CAT_ENERGY_SECTIONS[0], 6, 25, 'lowexplosion')]]
        
        self.moves['downB'].append(f, t)
        self.moves['downB'].canDI = False
        
        self.moves['downB'].frames[10].resetHitPotential = True
        self.moves['downB'].frames[14].resetHitPotential = True
        self.moves['downB'].frames[18].resetHitPotential = True
        self.moves['downB'].frames[22].resetHitPotential = True
        
        self.createMoveLowExplosion()
        
    def createMoveLowExplosion(self):
        
        
        r = [
                [
                    (-7, -55, 4, -44),
                    (-7, -43, 3, -18),
                    (-10, -18, -6, -10),
                    (-12, -10, -8, 0),
                    (1, -19, 5, -14),
                    (3, -14, 7, -10),
                    (4, -10, 9, 0),
                    (8, -3, 13, 1)
                ]
            ]
        
        dam1 = 75
        stun1 = 200
        force1 = 15
        angle1 = 90
        freeze1 = 5
        
        h = [
                [
                    (6, -44, 86, 4, dam1, stun1, force1, angle1, [], freeze1),
                ]
            ]
        
        f = [self.frameData(86, 2, r[0], h[0]),
             self.frameData(86, 5, r[0]),
             self.frameData(87, 1, r[0]),
             self.frameData(88, 1, r[0]),
             self.frameData(89, 2, r[0]),
             self.frameData(90, 3, r[0]),
             self.frameData(91, 5, r[0]),
             self.frameData(92, 5, r[0]),
             self.frameData(93, 4, r[0]),
             self.frameData(94, 3, r[0]),
             self.frameData(0, 3, r[0]),
             ]
        
        t = [['attackA', move.Transition(None, None, 2, 8, 'lowexplosiondash')],
             ['attackAUp', move.Transition(None, None, 2, 8, 'lowexplosiondash')]]
        
        self.moves['lowexplosion'] = move.Move(f, t)
        self.moves['lowexplosion'].canDI = False
        
        self.moves['lowexplosion'].frames[1].setVelX = -3.5
        self.moves['lowexplosion'].frames[0].fx.append(['runicexplosion', (52, -1), True])
        for m in self.moves['lowexplosion'].frames:
            m.setFrictionX = 0.32
            
        self.createMoveLowExplosionDash()
            
    def createMoveLowExplosionDash(self):
        f = [self.frameData(97, 4,)]
        t = [['exitFrame', move.Transition(-1, None, None, None, 'upA')]]
        
        
        self.moves['lowexplosiondash'] = move.Move(f, t)
        self.moves['lowexplosiondash'].canDI = False
        self.moves['lowexplosiondash'].frames[0].setVelX = 5.5
        self.moves['lowexplosiondash'].frames[0].ignoreFriction = True

    def createProjectiles(self):
        self.createProjectileSwordBeams()
        self.createProjectileDownBolt()
        self.addSuperProjectile()

    def createProjectileSwordBeams(self):
        
        dam1 = 30
        stun1 = 80
        force1 = 8
        angle1 = 30
        freeze1 = 3
        chip = 0.35
        
        h = [
                [
                    (-18, -14, 0, 17, dam1, stun1, force1, angle1, [], freeze1, chip),
                    (-28, -21, -3, -12, dam1, stun1, force1, angle1, [], freeze1, chip),
                    (-22, 16, -3, 24, dam1, stun1, force1, angle1, [], freeze1, chip),
                ]
             ]
        
        f = [ self.frameData(27, 2, [], h[0]),
              self.frameData(28, 1, [], h[0]),
              self.frameData(29, 2, [], h[0]),
              self.frameData(30, 1, [], h[0]),
              self.frameData(28, 2, [], h[0]),
              self.frameData(29, 1, [], h[0]),
              self.frameData(27, 1, [], h[0]),
              self.frameData(30, 1, [], h[0]),
              self.frameData(27, 1, [], h[0]),
              self.frameData(28, 1, [], h[0]),
              self.frameData(30, 1, [], h[0]),
              self.frameData(29, 2, [], h[0]) ]
        
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]

        temp = projectile.Projectile()
        temp.hitsRemaining = 1
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 5.5
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 20
        self.createProjectileEnding1(temp)
        self.createProjectileExplosion1(temp)
        self.projectiles.append(temp)

        temp = projectile.Projectile()
        temp.hitsRemaining = 2
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 7.5
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 35
        self.createProjectileEnding1(temp)
        self.createProjectileExplosion1(temp)
        self.projectiles.append(temp)

        temp = projectile.Projectile()
        temp.hitsRemaining = 2
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 8.8
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 40
        self.createProjectileEnding1(temp)
        self.createProjectileExplosion1(temp)
        self.projectiles.append(temp)
        
    def createProjectileEnding1(self, m):
        f = [ self.frameData(31, 3),
              self.frameData(32, 3),
              self.frameData(33, 3) ]
        t = []

        m.moves['dissolve'].append(f, t)

        m.dissolveOnPhysical = True
        
    def createProjectileExplosion1(self, m):
        f = [ self.frameData(166, 3),
              self.frameData(167, 2),
              self.frameData(168, 3) ]
        t = []

        m.moves['explode'].append(f, t)

        
    def createProjectileDownBolt(self):
        
        dam1 = 45
        stun1 = 110
        force1 = 18
        angle1 = 270
        freeze1 = 3
        
        h = [
                [
                    (-6, -27, 7, 4, dam1, stun1, force1, angle1, [], freeze1)
                ]
            ]
        
        f = [ self.frameData(138, 2, [], h[0]),
              self.frameData(139, 1, [], h[0]),
              self.frameData(140, 2, [], h[0]),
              self.frameData(141, 1, [], h[0]),
              self.frameData(139, 1, [], h[0]),
              self.frameData(141, 2, [], h[0]),
              self.frameData(138, 1, [], h[0]),
              self.frameData(139, 1, [], h[0]),
              self.frameData(141, 2, [], h[0]),
              self.frameData(140, 1, [], h[0]),
              self.frameData(138, 1, [], h[0]),
              self.frameData(140, 2, [], h[0]),
              self.frameData(139, 1, [], h[0]) ]
        
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]
        
        
        temp = projectile.Projectile()
        temp.hitsRemaining = 1
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 0
        temp.moves['flying'].frames[0].setVelY = 8.0
        temp.liveTime = 15
        self.createProjectileEnding2(temp)
        self.projectiles.append(temp)
        
        temp = projectile.Projectile()
        temp.hitsRemaining = 1
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 0
        temp.moves['flying'].frames[0].setVelY = 11.0
        temp.liveTime = 15
        self.createProjectileEnding2(temp)
        self.projectiles.append(temp)
        
        temp = projectile.Projectile()
        temp.hitsRemaining = 1
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 0
        temp.moves['flying'].frames[0].setVelY = 14.0
        temp.liveTime = 15
        self.createProjectileEnding2(temp)
        self.projectiles.append(temp)
        
    
    def createProjectileEnding2(self, m):
        f = [ self.frameData(142, 3),
              self.frameData(143, 2),
              self.frameData(144, 2) ]
        t = []

        m.moves['dissolve'].append(f, t)

        m.dissolveOnPhysical = True
        
        
    def addSuperProjectile(self):
        
        dam1 = 30
        stun1 = 250
        force1 = 22
        angle1 = 25
        freeze1 = 2
        chip = 0.40
        
        h = [
                [
                    (-18, -14, 0, 17, dam1, stun1, force1, angle1, [], freeze1, chip),
                    (-28, -21, -3, -12, dam1, stun1, force1, angle1, [], freeze1, chip),
                    (-22, 16, -3, 24, dam1, stun1, force1, angle1, [], freeze1, chip),
                ]
             ]
        
        f = [ self.frameData(27, 2, [], h[0]),
              self.frameData(28, 1, [], h[0]),
              self.frameData(29, 2, [], h[0]),
              self.frameData(30, 1, [], h[0]),
              self.frameData(28, 2, [], h[0]),
              self.frameData(29, 1, [], h[0]),
              self.frameData(27, 1, [], h[0]),
              self.frameData(30, 1, [], h[0]),
              self.frameData(27, 1, [], h[0]),
              self.frameData(28, 1, [], h[0]),
              self.frameData(30, 1, [], h[0]),
              self.frameData(29, 2, [], h[0]) ]
        
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]

        temp = projectile.Projectile()
        temp.hitsRemaining = 10
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 16
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 300
        self.createProjectileEnding1(temp)
        self.createProjectileExplosion1(temp)
        self.projectiles.append(temp)
             
        
    def createMoveStun1(self):
        r = [
                [
                    (-12, -62, 4, -46),
                    (-9, -46, 6, -19),
                    (-12, -42, -7, -35),
                    (6, -41, 11, -36),
                    (-10, -21, -3, 2),
                    (3, -19, 8, 0),
                    (6, -2, 10, 1)
                ]
            ]

        f = [ self.frameData(64, 9, r[0]) ]

        self.moves['stun1'].append(f, [])

        for i in range(len(self.moves['stun1'].frames)):
            self.moves['stun1'].frames[i].ignoreSpeedCap = True
            
    def createMoveStun2(self):
        r = [
                [
                    (-8, -60, -1, -40),
                    (-2, -56, 3, -40),
                    (-11, -51, -2, -19),
                    (-15, -38, -10, -19),
                    (-16, -21, 0, -16),
                    (-13, -17, -7, -12),
                    (-10, -13, -4, 1),
                    (-7, -4, -2, 2),
                    (-4, -17, 2, -11),
                    (-2, -13, 3, -10),
                    (1, -12, 5, 0),
                    (1, -4, 6, 1)
                ]
            ]

        f = [ self.frameData(65, 14, r[0]) ]

        self.moves['stun2'].append(f, [])

        for i in range(len(self.moves['stun2'].frames)):
            self.moves['stun2'].frames[i].ignoreSpeedCap = True
            
    def createMoveStun3(self):
        r = [
                [
                    (-11, -61, 4, -44),
                    (-8, -44, 5, -22),
                    (4, -42, 9, -38),
                    (-6, -24, 8, -18),
                    (-3, -18, 2, 3),
                    (1, -17, 3, -6),
                    (5, -18, 8, 3),
                    (7, -17, 10, 3)
                ],
                [
                    (0, -58, 5, -38),
                    (5, -53, 9, -39),
                    (-5, -51, 2, -37),
                    (-10, -41, 3, -32),
                    (-12, -33, -1, -24),
                    (-14, -26, -2, -17),
                    (-14, -19, -1, -14),
                    (-9, -15, 5, -10),
                    (-1, -11, 12, -8),
                    (4, -13, 15, -9),
                    (-1, -32, 7, -30)
                ],
                [
                    (-9, -59, -1, -40),
                    (-11, -51, 2, -41),
                    (-2, -55, 3, -49),
                    (-12, -41, -2, -19),
                    (-15, -35, -9, -18),
                    (-14, -20, 0, -15),
                    (-12, -16, 7, -12),
                    (-6, -13, 11, -9),
                    (6, -15, 17, -12),
                    (-3, -36, 6, -30)
                ],
                [
                    (-13, -59, -5, -41),
                    (-16, -51, -10, -42),
                    (-6, -56, -1, -42),
                    (-13, -42, -3, -19),
                    (-16, -38, -11, -17),
                    (-5, -38, -1, -33),
                    (-16, -19, 0, -17),
                    (-13, -17, 11, -12),
                    (10, -18, 16, -15)
                ],
                [
                    (-23, -57, -15, -41),
                    (-14, -56, -9, -40),
                    (-18, -52, -8, -41),
                    (-19, -41, -6, -17),
                    (-16, -18, 10, -15),
                    (-8, -22, 13, -17),
                    (11, -24, 17, -21),
                    (-13, -16, 2, -13)
                ]
            ]

        
        f = [ self.frameData(66, 10, r[0]),
              self.frameData(67, 2, r[1]),
              self.frameData(68, 1, r[2]),
              self.frameData(69, 1, r[3]),
              self.frameData(70, 12, r[4])]

        self.moves['stun3'].append(f, [])

        for i in range(len(self.moves['stun3'].frames)):
            self.moves['stun3'].frames[i].ignoreSpeedCap = True
            
            
    def createMoveStun4(self):
        r = [
                [
                    (-11, -61, 4, -44),
                    (-8, -44, 5, -22),
                    (4, -42, 9, -38),
                    (-6, -24, 8, -18),
                    (-3, -18, 2, 3),
                    (1, -17, 3, -6),
                    (5, -18, 8, 3),
                    (7, -17, 10, 3)
                ],
                [
                    (0, -58, 5, -38),
                    (5, -53, 9, -39),
                    (-5, -51, 2, -37),
                    (-10, -41, 3, -32),
                    (-12, -33, -1, -24),
                    (-14, -26, -2, -17),
                    (-14, -19, -1, -14),
                    (-9, -15, 5, -10),
                    (-1, -11, 12, -8),
                    (4, -13, 15, -9),
                    (-1, -32, 7, -30)
                ],
                [
                    (-9, -59, -1, -40),
                    (-11, -51, 2, -41),
                    (-2, -55, 3, -49),
                    (-12, -41, -2, -19),
                    (-15, -35, -9, -18),
                    (-14, -20, 0, -15),
                    (-12, -16, 7, -12),
                    (-6, -13, 11, -9),
                    (6, -15, 17, -12),
                    (-3, -36, 6, -30)
                ],
                [
                    (-13, -59, -5, -41),
                    (-16, -51, -10, -42),
                    (-6, -56, -1, -42),
                    (-13, -42, -3, -19),
                    (-16, -38, -11, -17),
                    (-5, -38, -1, -33),
                    (-16, -19, 0, -17),
                    (-13, -17, 11, -12),
                    (10, -18, 16, -15)
                ],
                [
                    (-23, -57, -15, -41),
                    (-14, -56, -9, -40),
                    (-18, -52, -8, -41),
                    (-19, -41, -6, -17),
                    (-16, -18, 10, -15),
                    (-8, -22, 13, -17),
                    (11, -24, 17, -21),
                    (-13, -16, 2, -13)
                ]
            ]

        
        f = [ self.frameData(66, 15, r[0]),
              self.frameData(67, 2, r[1]),
              self.frameData(68, 1, r[2]),
              self.frameData(69, 1, r[3]),
              self.frameData(70, 24, r[4])]

        self.moves['stun4'].append(f, [])

        for i in range(len(self.moves['stun4'].frames)):
            self.moves['stun4'].frames[i].ignoreSpeedCap = True
            
    def createMoveGrabbing(self):
        
        h = [
                [
                    (-12, -44, 40, -34, 0, 0, 0, 0, [('grab', 'grabHold', 'grabbed')], 0)
                ],
                [
                    (-8, -42, 28, -36, 0, 0, 0, 0, [('grab', 'grabHold', 'grabbed')], 0)
                ]
             ]
        
        
        
        
        f = [ self.frameData(126, 2, []),
              self.frameData(127, 2, [], h[0]),
              self.frameData(128, 2, [], h[1]),
              self.frameData(129, 3, [], h[1]),
              self.frameData(129, 8, []),
              self.frameData(126, 2, []) ]

        self.moves['grabbing'].append(f, [])
        self.moves['grabbing'].frames[1].setVelX = 8.0
        self.moves['grabbing'].frames[1].ignoreFriction = True
        self.moves['grabbing'].frames[2].ignoreFriction = True
        self.moves['grabbing'].frames[5].setVelX = -8.0
        self.moves['grabbing'].frames[5].ignoreFriction = True
        
    def createMoveGrabHold(self):
        f = [ self.frameData(129, 10, []),
              self.frameData(129, 42, []),
              self.frameData(129, 2, [])]
        
        self.moves['grabHold'].append(f, [])
        self.moves['grabHold'].grabPos = (13, 0)
            
    def createMoveGrabbed(self):
        r = [
                [
                    (-11, -61, 4, -44),
                    (-8, -44, 5, -22),
                    (4, -42, 9, -38),
                    (-6, -24, 8, -18),
                    (-3, -18, 2, 3),
                    (1, -17, 3, -6),
                    (5, -18, 8, 3),
                    (7, -17, 10, 3)
                ]
             ]
        
        f = [ self.frameData(66, 2, r[0]),
              self.frameData(66, 5, r[0]),
              self.frameData(66, 2, r[0]) ]

        self.moves['grabbed'].append(f, [])
        self.moves['grabbed'].grabPos = (12, 0)
        
    def createMoveGrabbed2(self):
        
        r = [
                [
                    (-11, -61, 4, -44),
                    (-8, -44, 5, -22),
                    (4, -42, 9, -38),
                    (-6, -24, 8, -18),
                    (-3, -18, 2, 3),
                    (1, -17, 3, -6),
                    (5, -18, 8, 3),
                    (7, -17, 10, 3)
                ]
             ]

        f = [ self.frameData(66, 2, r[0]) ]

        self.moves['grabbed2'].append(f, [])
        self.moves['grabbed2'].grabPos = (12, 0)
        
    def createMoveGrabRelease(self):
        f = [ self.frameData(126, 2, []),
              self.frameData(126, 1, []),
              self.frameData(126, 22, [])]

        self.moves['grabRelease'].append(f, [])
        self.moves['grabRelease'].frames[1].setVelX = -20.0
        self.moves['grabRelease'].frames[1].setFrictionX = 0.5
        self.moves['grabRelease'].frames[2].setFrictionX = 0.75
        
    def createMoveGrabbedRelease(self):

        f = [ self.frameData(65, 2),
              self.frameData(65, 1),
              self.frameData(65, 22)]

        self.moves['grabbedRelease'].append(f, [])
        self.moves['grabbedRelease'].frames[1].setVelX = -20.0
        self.moves['grabbedRelease'].frames[1].setFrictionX = 0.5
        self.moves['grabbedRelease'].frames[2].setFrictionX = 0.75
        
    
    
    def createMoveThrowBackward(self):
        
        damage1 = 120
        stun1 = 200
        knockback1 = 17
        angle1 = 155
        freeze1 = 1
        
        h = [
                [
                    (-37, -32, 6, -25, damage1, stun1, knockback1, angle1, [], freeze1),
                    (-11, -38, 7, -20, damage1, stun1, knockback1, angle1, [], freeze1)
                ]
            ]
        
        f = [ self.frameData(17, 6, []),
               self.frameData(169, 1, []),
               self.frameData(170, 1, []),
               self.frameData(171, 2, [], h[0]),
               self.frameData(171, 12, []) ]
        
        self.moves['throwBackward'].append(f, [])
         
        self.moves['throwBackward'].frames[0].setVelX = 10
        self.moves['throwBackward'].frames[0].ignoreFriction = True
        self.moves['throwBackward'].frames[0].ignoreSpeedCap = True
        self.moves['throwBackward'].frames[1].setVelX = 0
         
         
        
    def createMoveThrowForward(self):
        
        damage1 = 6
        stun1 = 52
        knockback1 = 1.5
        angle1 = 90
        freeze1 = 1

        damage2 = 85
        stun2 = 210
        knockback2 = 18
        angle2 = 25
        freeze2 = 3
        
        h = [
                [
                    (8, -63, 35, -28, damage1, stun1, knockback1, angle1, [('fx', None)], freeze1)
                ],
                [
                    (8, -63, 35, -28, damage2, stun2, knockback2, angle2, [], freeze2)
                ]
            ]
        
        f = [ self.frameData(130, 3, []),
              self.frameData(132, 1, [], h[0]),
              self.frameData(133, 1, [], h[0]),
              self.frameData(134, 1, [], h[0]),
              self.frameData(132, 1, [], h[0]),
              self.frameData(134, 1, [], h[0]),
              self.frameData(133, 1, [], h[0]),
              self.frameData(132, 1, [], h[0]),
              self.frameData(134, 1, [], h[0]),
              self.frameData(133, 1, [], h[0]),
              self.frameData(132, 1, [], h[0]),
              self.frameData(134, 1, [], h[0]),
              self.frameData(133, 3, [], h[1]),
              self.frameData(130, 20, []),
              self.frameData(131, 5, []),
              self.frameData(126, 2, [])]
        
        t = []
        
        self.moves['throwForward'].append(f, t)
        
        self.moves['throwForward'].frames[12].setVelX = -16.0
        self.moves['throwForward'].frames[12].setFrictionX = 0.5
        self.moves['throwForward'].frames[13].setFrictionX = 0.5
        
        for f in self.moves['throwForward'].frames:
            f.resetHitPotential = True
            f.resetCanEffect = True
        
        self.moves['throwForward'].frames[1].fx.append(['runicflame3', (22, -43), True])
        self.moves['throwForward'].frames[2].fx.append(['runicflame1', (20, -49), True])
        self.moves['throwForward'].frames[3].fx.append(['runicflame3', (20, -44), True])
        self.moves['throwForward'].frames[4].fx.append(['runicflame2', (19, -42), True])
        self.moves['throwForward'].frames[5].fx.append(['runicflame1', (22, -47), True])
        self.moves['throwForward'].frames[6].fx.append(['runicflame3', (20, -45), True])
        self.moves['throwForward'].frames[7].fx.append(['runicflame2', (21, -41), True])
        self.moves['throwForward'].frames[8].fx.append(['runicflame1', (24, -44), True])
        self.moves['throwForward'].frames[9].fx.append(['runicflame3', (19, -43), True])
        self.moves['throwForward'].frames[10].fx.append(['runicflame2', (23, -49), True])
        self.moves['throwForward'].frames[11].fx.append(['runicflame1', (22, -47), True])
        
        self.moves['throwForward'].frames[12].fx.append(['runicexplosion', (19, -48), True])
        
        
        
        
    def createMoveDeadFalling(self):
        f = [ self.frameData(70, 3) ]

        self.moves['deadFalling'].append(f, [])

        for i in range(len(self.moves['deadFalling'].frames)):
            self.moves['deadFalling'].frames[i].ignoreSpeedCap = True
            self.moves['deadFalling'].frames[i].ignoreFriction = True

    def createMoveDeadGroundHit(self):
        f = [ self.frameData(71, 2),
              self.frameData(72, 4),
              self.frameData(73, 2),
              self.frameData(74, 1) ]

        self.moves['deadGroundHit'].append(f, [])

    def createMoveDeadLaying(self):
        f = [ self.frameData(74, 3) ]

        self.moves['deadLaying'].append(f, [])
        
            
    def createMoveGroundHit(self):
        
        r = [
                [
                    (-24, -12, 13, 0),
                    (-29, -9, -23, 1),
                    (12, -8, 41, 0),
                    (11, -11, 17, -7)
                ]
             ]
        
        f = [ self.frameData(71, 2),
              self.frameData(72, 4),
              self.frameData(73, 2),
              self.frameData(74, 1),
              self.frameData(73, 1),
              self.frameData(74, 10),
              self.frameData(74, 2),
              self.frameData(74, 80, r[0]) ]
        
        self.moves['groundHit'].append(f, [])
        self.moves['groundHit'].frames[0].fx.append(['dust', (28, 0), True])
        self.moves['groundHit'].frames[0].fx.append(['dust', (-28, 0), False])
        self.moves['groundHit'].frames[1].fx.append(['shockwave', (0, 0), True])
        
    def createMoveStandUp(self):
        f = [ self.frameData(75, 4),
              self.frameData(76, 7),
              self.frameData(85, 4)]

        self.moves['standUp'].append(f, [])
        
    def createMoveStandForward(self):
        f = [ self.frameData(75, 3),
              self.frameData(77, 3),
              self.frameData(78, 2),
              self.frameData(79, 2),
              self.frameData(80, 2),
              self.frameData(81, 2),
              self.frameData(82, 2),
              self.frameData(83, 1),
              self.frameData(84, 1),
              self.frameData(85, 4) ]

        self.moves['standForward'].append(f, [])

        self.moves['standForward'].frames[1].setVelX = 16.0
        self.moves['standForward'].frames[9].setVelX = 0

        for i in range(len(self.moves['standForward'].frames)):
            self.moves['standForward'].frames[i].setFrictionX = self.groundFriction * 0.55
            self.moves['standForward'].frames[i].ignoreSpeedCap = True
        
    def createMoveStandBackward(self):
        f = [ self.frameData(75, 3),
              self.frameData(84, 2),
              self.frameData(83, 2),
              self.frameData(82, 2),
              self.frameData(81, 2),
              self.frameData(80, 2),
              self.frameData(79, 1),
              self.frameData(78, 1),
              self.frameData(77, 1),
              self.frameData(85, 4) ]

        self.moves['standBackward'].append(f, [])

        self.moves['standBackward'].frames[1].setVelX = -16.0
        self.moves['standBackward'].frames[9].setVelX = 0

        for i in range(len(self.moves['standBackward'].frames)):
            self.moves['standBackward'].frames[i].setFrictionX = self.groundFriction * 0.55
            self.moves['standBackward'].frames[i].ignoreSpeedCap = True
            
            
            
    def createMoveTeching(self):
        f = [ self.frameData(81, 4),
              self.frameData(81, 1)]

        self.moves['teching'].append(f, [])

    def createMoveTechUp(self):
        f = [ self.frameData(84, 3),
              self.frameData(85, 2) ]

        self.moves['techUp'].append(f, [])

    def createMoveTechForward(self):
        f = [ self.frameData(75, 3),
              self.frameData(77, 3),
              self.frameData(78, 2),
              self.frameData(79, 2),
              self.frameData(80, 2),
              self.frameData(81, 2),
              self.frameData(82, 2),
              self.frameData(83, 1),
              self.frameData(84, 1),
              self.frameData(85, 4) ]


        self.moves['techForward'].append(f, [])

        self.moves['techForward'].frames[1].setVelX = 16
        self.moves['techForward'].frames[9].setVelX = 0

        for i in range(len(self.moves['techForward'].frames)):
            self.moves['techForward'].frames[i].setFrictionX = self.groundFriction * 0.55
            self.moves['techForward'].frames[i].ignoreSpeedCap = True

    def createMoveTechBackward(self):

        f = [ self.frameData(75, 3),
              self.frameData(84, 2),
              self.frameData(83, 2),
              self.frameData(82, 2),
              self.frameData(81, 2),
              self.frameData(80, 2),
              self.frameData(79, 1),
              self.frameData(78, 1),
              self.frameData(77, 1),
              self.frameData(85, 4) ]


        self.moves['techBackward'].append(f, [])

        self.moves['techBackward'].frames[1].setVelX = -16
        self.moves['techBackward'].frames[9].setVelX = 0

        for i in range(len(self.moves['techBackward'].frames)):
            self.moves['techBackward'].frames[i].setFrictionX = self.groundFriction * 0.55
            self.moves['techBackward'].frames[i].ignoreSpeedCap = True
            
            

    def getCatEnergyLevel(self):
        x = len(CAT_ENERGY_SECTIONS)
        for i in range(x):
            if self.energy.value <= CAT_ENERGY_SECTIONS[i]:
                return i+1
        return x+1


    def createSuperMove1(self):
        n = "Great Shockwave"
        
        d = ("A super-powered version of the user's normal protectile" +
             " ability, capable of dealing a great deal of damage.")
        
        r = [
                [
                    (-6, -56, 6, -17),
                    (-3, -17, 2, 1)
                ],
                [
                    (1, -55, 13, -42),
                    (0, -42, 9, -30),
                    (-4, -30, 7, -17),
                    (-6, -19, -3, -10),
                    (-8, -11, -5, 0),
                    (5, -18, 10, -15),
                    (6, -16, 12, -11),
                    (7, -12, 13, 0)
                ]
            ]
        
        f = [ self.frameData(152, 3, r[0]),
              self.frameData(153, 1, r[0]),
              self.frameData(154, 1, r[0]),
              self.frameData(155, 1, r[0]),
              self.frameData(156, 30, r[1]) ]
        
        
        
        sg = move.SuperMove(n, d, f, [])
        sg.flash = self.createSuperFlash1()
        
        sg.shoot.append( (0, 6, (45, -30)) )
        
        sg.canDI = False
        sg.frames[0].setVelX = 0

        self.appendSuperMove(sg, None)
        
    def createSuperFlash1(self):
        
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
              
              self.frameData(145, 4),
              self.frameData(146, 10),
              self.frameData(147, 4),
              self.frameData(148, 4),
              self.frameData(149, 1),
              self.frameData(150, 1),
              self.frameData(151, 2)]
        
        s = move.baseSuperFlash()
        s.append(f, [])
        
        s.frames[0].setVelX = 0
        
        return s
        
        
    def createColors(self):
        pass
