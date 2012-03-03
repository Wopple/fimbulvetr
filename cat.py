import os
import sys
import pygame

import incint
import boundint
import battlechar
import move
import projectile

from constants import *

class Cat(battlechar.BattleChar):
    def __init__(self, name="Unnamed Cat", inSpecial=0):
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
        self.blockFXPoints = [ (9, -35), (33, -32), (9, -35) ]
        self.catEnergy = boundint.BoundInt(0, CAT_ENERGY_MAX, 0)
        self.prevEnergy = self.catEnergy.value
        self.energyDelayTick = CAT_ENERGY_DELAY
        self.energy = self.catEnergy
        super(Cat, self).__init__(1000, 15)
        self.initSpecMoves()

        self.speciesDesc = ("An all-around warrior that wields a blade" +
                            " enchanted with Galdr runes.  Capable of both" +
                            " melee and magical ranged attacks, and" +
                            " comfortable at many distances.  Requires time" +
                            " to charge their slowly-depleting energy" +
                            " in order to maintain strength.")

        if (inSpecial < 0) or (inSpecial >= len(self.superMoves)):
            inSpecial = 0
        self.currSuperMove = inSpecial

    def beginBattle(self):
        super(Cat, self).beginBattle()
        self.catEnergy.change(CAT_ENERGY_BATTLE_START)
        self.energyDelayTick = 0
        self.energyIsChangable = False

    def countdownComplete(self):
        self.energyIsChangable = True

    def update(self):
        super(Cat, self).update()

        if self.energyIsChangable:
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
        self.createMoveUpA()
        self.createMoveUpB()
        self.createNeutralAirB()

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
        
        self.createMoveGrabbed()
        self.createMoveGrabbed2()
        self.createMoveGrabbedRelease()
        
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
        
        dam1 = 100
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
        
        f = [ self.frameData(48, 3, []),
              self.frameData(49, 1, [], h[0]),
              self.frameData(50, 1, [], h[1]),
              self.frameData(51, 1, [], h[2]),
              self.frameData(52, 1, [], h[3]),
              self.frameData(53, 2, []),
              self.frameData(54, 9, []),
              self.frameData(55, 2, []) ]
        
        
        
        self.moves['jabA'].append(f, [])
        
        self.moves['jabA'].canDI = False

    def createMoveJabB(self):
        f = [ self.frameData(19, 2),
              self.frameData(20, 2),
              self.frameData(21, 1),
              self.frameData(22, 3),
              self.frameData(23, 1)]

        t = [ ['bladelv1', move.Transition(None, None, 4, 4, 'swordbeamGround1')],
              ['bladelv2', move.Transition(None, None, 4, 4, 'swordbeamGround2')],
              ['bladelv3', move.Transition(None, None, 4, 4, 'swordbeamGround3')] ]

        self.moves['jabB'].append(f, t)
        self.moves['jabB'].canDI = False

        self.createMoveSwordBeamGroundEnd()
        
    def createMoveDashAttackA(self):
        
        dam1 = 0
        stun1 = 50
        force1 = 16
        angle1 = 16
        
        
        dam2 = 130
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
        
        f = [ self.frameData(14, 2, []),
              self.frameData(15, 2, []),
              self.frameData(17, 4, [], h[0]),
              self.frameData(43, 5, [], h[1]),
              self.frameData(43, 7, [])]
        
        self.moves['dashAttackA'].append(f, [])
        self.moves['dashAttackA'].canDI = False
        
        self.moves['dashAttackA'].frames[2].setVelX = 30
        self.moves['dashAttackA'].frames[2].ignoreSpeedCap = True
        self.moves['dashAttackA'].frames[2].ignoreFriction = True
        self.moves['dashAttackA'].frames[3].setVelX = 0
        self.moves['dashAttackA'].frames[3].resetHitPotential = True
        
        

    def createMoveSwordBeamGroundEnd(self):
        f = [ self.frameData(24, 2),
              self.frameData(25, 1),
              self.frameData(26, 10),
              self.frameData(0, 2) ]
        t = []

        self.moves['swordbeamGround1'] = move.Move(f, t)
        self.moves['swordbeamGround1'].canDI = False
        self.moves['swordbeamGround1'].shoot.append( (0, 0, (64, -30)) )

        self.moves['swordbeamGround2'] = move.Move(f, t)
        self.moves['swordbeamGround2'].canDI = False
        self.moves['swordbeamGround2'].shoot.append( (0, 1, (64, -30)) )

        self.moves['swordbeamGround3'] = move.Move(f, t)
        self.moves['swordbeamGround3'].canDI = False
        self.moves['swordbeamGround3'].shoot.append( (0, 2, (64, -30)) )

    def createNeutralAirB(self):
        f = [ self.frameData(34, 3),
              self.frameData(35, 3),
              self.frameData(36, 4),
              self.frameData(37, 4),
              self.frameData(38, 1)]

        t = [ ['bladelv1', move.Transition(None, None, 4, 4, 'swordbeamAir1')],
              ['bladelv2', move.Transition(None, None, 4, 4, 'swordbeamAir2')],
              ['bladelv3', move.Transition(None, None, 4, 4, 'swordbeamAir3')],
              ['land', move.Transition(None, None, None, None, 'neutralAirBLag')] ]

        self.moves['neutralAirB'].append(f, t)
        self.moves['neutralAirB'].reversable = True

        self.createMoveSwordBeamAirEnd()

        self.createMoveNeutralAirBLag()


    def createMoveSwordBeamAirEnd(self):
        f = [ self.frameData(39, 2),
              self.frameData(40, 1),
              self.frameData(41, 12),
              self.frameData(5, 2) ]
        t = [['land', move.Transition(None, None, None, None, 'neutralAirBLag')]]

        self.moves['swordbeamAir1'] = move.Move(f, t)
        self.moves['swordbeamAir1'].shoot.append( (0, 0, (64, -30)) )

        self.moves['swordbeamAir2'] = move.Move(f, t)
        self.moves['swordbeamAir2'].shoot.append( (0, 1, (64, -30)) )

        self.moves['swordbeamAir3'] = move.Move(f, t)
        self.moves['swordbeamAir3'].shoot.append( (0, 2, (64, -30)) )

    def createMoveNeutralAirBLag(self):
        f = [ self.frameData(26, 8) ]
        self.moves['neutralAirBLag'] = move.Move(f, [])
        self.moves['neutralAirBLag'].canDI = False


    def createMoveUpA(self):
        
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
                    [45, -62, 56, -17]
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
        
        dam1 = 65
        stun1 = 150
        force1 = 8
        angle1 = 90
        freeze1 = 3
        
        for j in range(len(h)):
            h[j] = [i + [dam1, stun1, force1, angle1, [], freeze1] for i in h[j]]
        
        
        f = [ self.frameData(116, 4),
              self.frameData(97, 3, [], h[0]),
              self.frameData(98, 3, [], h[1]),
              self.frameData(99, 2, [], h[2]),
              self.frameData(100, 2, [], h[3]),
              self.frameData(101, 2, [], h[4]),
              self.frameData(102, 2, [], h[5]),
              self.frameData(103, 1, [], h[6]),
              self.frameData(104, 1, [], h[7]),
              self.frameData(105, 1, [], h[8]),
              self.frameData(106, 2, [], h[9]),
              self.frameData(107, 2, [], h[10]),
              self.frameData(108, 2, [], h[11]),
              self.frameData(109, 2, [], h[12]),
              self.frameData(110, 2, [], h[13]),
              self.frameData(111, 2, [], h[14]),
              self.frameData(112, 1, [], h[15]),
              self.frameData(113, 1, [], h[16]),
              self.frameData(114, 2, [], h[17]),
              self.frameData(115, 3, [], h[18]),
              self.frameData(116, 5) ]
        
        t = []
        
        self.moves['upA'].append(f, t)
        self.moves['upA'].canDI = False
        self.moves['upA'].frames[7].resetHitPotential = True
        self.moves['upA'].frames[17].resetHitPotential = True

    def createMoveUpB(self):
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

    def createMoveDownA(self):
        
        dam1 = 60
        stun1 = 45
        force1 = 14
        angle1 = 32
        freeze1 = 2
        
        h = [
                [
                    (48, -44, 83, -34, dam1, stun1, force1, angle1, [], freeze1),
                    (25, -38, 53, -30, dam1, stun1, force1, angle1, [], freeze1)
                ]
             ]
        
        f = [ self.frameData(42, 2, []),
              self.frameData(43, 6, [], h[0]),
              self.frameData(43, 2, []),
              self.frameData(42, 2, []),
              self.frameData(18, 2, [])]

        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'ducking')] ]

        self.moves['downA'].append(f, t)
        self.moves['downA'].canDI = False
        
    def createMoveDownB(self):
        
        dam1 = 22
        stun1 = 101
        force1 = 3
        angle1 = 90
        freeze1 = 2
        
        h = [
                [
                    (16, -12, 86, 3, dam1, stun1, force1, angle1, [('untechable')], freeze1),
                ]
            ]
        
        f = [self.frameData(22, 4, []),
             self.frameData(56, 1, []),
             self.frameData(57, 2, []),
             self.frameData(58, 2, []),
             self.frameData(59, 2, []),
             
             self.frameData(60, 1, [], h[0]),
             self.frameData(61, 1, [], h[0]),
             self.frameData(62, 1, [], h[0]),
             self.frameData(63, 1, [], h[0]),
             self.frameData(60, 1, [], h[0]),
             self.frameData(61, 1, [], h[0]),
             self.frameData(62, 1, [], h[0]),
             self.frameData(63, 1, [], h[0]),
             self.frameData(60, 1, [], h[0]),
             self.frameData(61, 1, [], h[0]),
             self.frameData(62, 1, [], h[0]),
             self.frameData(63, 1, [], h[0]),
             self.frameData(60, 1, [], h[0]),
             self.frameData(61, 1, [], h[0]),
             self.frameData(62, 1, [], h[0]),
             self.frameData(63, 1, [], h[0]),
             self.frameData(60, 1, [], h[0]),
             self.frameData(61, 1, [], h[0]),
             self.frameData(62, 1, [], h[0]),
             self.frameData(63, 1, [], h[0]),
             
             self.frameData(58, 2, []),
             self.frameData(57, 2, []),
             self.frameData(22, 10, []) ]
        
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
        
        dam1 = 90
        stun1 = 200
        force1 = 15
        angle1 = 90
        freeze1 = 5
        
        h = [
                [
                    (6, -44, 86, 4, dam1, stun1, force1, angle1, [], freeze1),
                ]
            ]
        
        f = [self.frameData(86, 2, [], h[0]),
             self.frameData(86, 5, []),
             self.frameData(87, 1, []),
             self.frameData(88, 1, []),
             self.frameData(89, 2, []),
             self.frameData(90, 3, []),
             self.frameData(91, 5, []),
             self.frameData(92, 5, []),
             self.frameData(93, 4, []),
             self.frameData(94, 3, []),
             self.frameData(0, 3, []),
             ]
        
        t = [['attackA', move.Transition(None, None, 2, 8, 'lowexplosiondash')]]
        
        self.moves['lowexplosion'] = move.Move(f, t)
        self.moves['lowexplosion'].canDI = False
        
        self.moves['lowexplosion'].frames[1].setVelX = -4
        self.moves['lowexplosion'].frames[0].fx.append(['runicexplosion', (52, -1), True])
        for m in self.moves['lowexplosion'].frames:
            m.setFrictionX = 0.32
            
        self.createMoveLowExplosionDash()
            
    def createMoveLowExplosionDash(self):
        f = [self.frameData(97, 4,)]
        t = [['exitFrame', move.Transition(-1, None, None, None, 'upA')]]
        
        
        self.moves['lowexplosiondash'] = move.Move(f, t)
        self.moves['lowexplosiondash'].canDI = False
        self.moves['lowexplosiondash'].frames[0].setVelX = 4
        self.moves['lowexplosiondash'].frames[0].ignoreFriction = True

    def createProjectiles(self):
        self.createProjectileSwordBeams()

    def createProjectileSwordBeams(self):
        f = [ self.frameData(27, 2),
              self.frameData(28, 1),
              self.frameData(29, 2),
              self.frameData(30, 1),
              self.frameData(28, 2),
              self.frameData(29, 1),
              self.frameData(27, 1),
              self.frameData(30, 1),
              self.frameData(27, 1),
              self.frameData(28, 1),
              self.frameData(30, 1),
              self.frameData(29, 2) ]
        
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]

        temp = projectile.Projectile()
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 5.5
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 20
        self.createProjectileEnding1(temp)
        self.projectiles.append(temp)

        temp = projectile.Projectile()
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 7.5
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 35
        self.createProjectileEnding1(temp)
        self.projectiles.append(temp)

        temp = projectile.Projectile()
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 8.8
        temp.moves['flying'].frames[0].setVelY = 0
        temp.liveTime = 40
        self.createProjectileEnding1(temp)
        self.projectiles.append(temp)

    def createProjectileEnding1(self, m):
        f = [ self.frameData(31, 3),
              self.frameData(32, 3),
              self.frameData(33, 3) ]
        t = []

        m.moves['dissolve'].append(f, t)

        m.dissolveOnPhysical = True
        
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
        
    def createMoveGrabbedRelease(self):

        f = [ self.frameData(65, 2),
              self.frameData(65, 1),
              self.frameData(65, 22)]

        self.moves['grabbedRelease'].append(f, [])
        self.moves['grabbedRelease'].frames[1].setVelX = -20.0
        self.moves['grabbedRelease'].frames[1].setFrictionX = 0.5
        self.moves['grabbedRelease'].frames[2].setFrictionX = 0.75
        
        
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
        
        sg = move.SuperMove(n, d, [], [])

        self.appendSuperMove(sg, None)
