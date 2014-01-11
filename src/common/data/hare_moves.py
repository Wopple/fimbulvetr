from common.constants import *

from common import move
from common.data.hare_stats import *

def load():
    move.initBattlecharMoves(moves)
    createMoveIdle()
    createMoveIdleLike()
    createMoveWalking()
    createMoveDashing()
    createMoveRunning()
    createMoveAir()
    createMoveFlipping()
    createMoveAirLike()
    createMoveJumpingLike()
    createMoveLanding()
    createMoveJumping()
    createMoveDucking()
    createMoveJabA()
    createMoveJabB()
    createMoveDashAttackA()
    createMoveDashAttackB()
    createMoveDownA()
    createMoveDownB()
    createMoveUpA()
    createMoveUpB()
    createMoveNeutralAirA()
    createMoveNeutralAirB()
    createMoveUpAirA()
    createMoveUpAirB()
    createMoveDownAirA()
    createMoveDownAirB()
    createMoveDroppingThrough()

    createAirDash()

    createMoveGrabbing()
    createMoveGrabHold()
    createMoveGrabbed()
    createMoveGrabbed2()
    createMoveGrabRelease()
    createMoveGrabbedRelease()

    createMoveThrowBackward()
    createMoveThrowForward()

    createMoveStun1()
    createMoveStun2()
    createMoveStun3()
    createMoveStun4()

    createMoveDeadFalling()
    createMoveDeadGroundHit()
    createMoveDeadLaying()

    createMoveGroundHit()
    createMoveStandUp()
    createMoveStandForward()
    createMoveStandBackward()
    createMoveStandAttack()

    createMoveTeching()
    createMoveTechUp()
    createMoveTechForward()
    createMoveTechBackward()

    createMoveBlock()
    createMoveLowBlock()
    createMoveAirBlock()

    createSuperMoves()
    move.setupSuper(moves, superMoves, superMovesAir)

def createSuperMoves():
    createSuperMove1()
    #createSuperMove2()

def createMoveIdle():
    r = [
            [
                (-7, -36, 1, -15),
                (-12, -16, -7, 0),
                (1, -18, 8, -12),
                (5, -12, 11, 1),
                (-4, -50, 6, -32),
                (-15, -34, -5, -30),
                (6, -3, 15, 1)
             ]
        ]

    f = [ move.frameData(0, 10, r[0]),
          move.frameData(1, 5, r[0]),
          move.frameData(166, 5, r[0]),
          move.frameData(167, 12, r[0]),
          move.frameData(1, 6, r[0])]

    moves['idle'].append(f, [])

def createMoveBlock():
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


    f = [ move.frameData(81, 2, r[0], [], b[0]) ]

    moves['blocking'].append(f, [])

def createMoveLowBlock():

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


    f = [ move.frameData(108, 2, r[0], [], b[0]) ]

    moves['lowBlocking'].append(f, [])

def createMoveAirBlock():

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



    f = [ move.frameData(109, 2, r[0], [], b[0]) ]

    moves['airBlocking'].append(f, [])

def createMoveIdleLike():
    f = [ move.frameData(66, 1),
          move.frameData(0, 1),
          move.frameData(66, 1) ]
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

    f = [ move.frameData(66, 1, r[0]),
          move.frameData(0, 1, r[0]),
          move.frameData(66, 1, r[0]) ]
    moves['idleLike'].append(f, [])
    moves['idleLike'].frames[0].ignoreFriction = True
    moves['idleLike'].frames[0].ignoreSpeedCap = True
    moves['idleLike'].frames[1].ignoreFriction = True
    moves['idleLike'].frames[1].ignoreSpeedCap = True

def createMoveWalking():

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

    f = [move.frameData(149, 3, r[0]),
         move.frameData(150, 3, r[0]),
         move.frameData(151, 3, r[1]),
         move.frameData(152, 3, r[2]),
         move.frameData(168, 3, r[0]) ]

    moves['walking'].append(f, [])

def createMoveDashing():

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

    f = [move.frameData(5, 7, r[0])]

    moves['dashing'].append(f, [])

def createMoveRunning():

    r = [
            [
                (-2, -39, 10, -21),
                (4, -45, 17, -34),
                (13, -52, 25, -42),
                (8, -23, 16, -15),
                (11, -16, 19, -4),
                (16, -9, 26, -2),
                (-7, -24, 0, -17),
                (-17, -21, -4, -16)
            ],
            [
                (12, -45, 21, -38),
                (3, -40, 12, -28),
                (-5, -34, 8, -15),
                (2, -16, 12, 0)
            ],
            [
                (12, -54, 24, -47),
                (5, -47, 18, -40),
                (-2, -42, 9, -33),
                (-6, -34, 12, -23),
                (7, -24, 16, -17),
                (10, -19, 22, -9),
                (-12, -25, -5, -17),
                (-21, -23, -8, -18)
            ]
        ]

    f = [move.frameData(6, 2, r[1]),
         move.frameData(7, 2, r[1]),
         move.frameData(161, 2, r[2]),
         move.frameData(2, 2, r[0]),
         move.frameData(3, 2, r[1]),
         move.frameData(4, 2, r[1]),
         move.frameData(5, 2, r[2])]

    moves['running'].append(f, [])

def createMoveAir():
    r = [
            [
                (-9, -36, 3, -11),
                (0, -15, 7, -5),
                (-9, -12, -4, -6),
                (-1, -47, 10, -32)
            ]
        ]

    f = [ move.frameData(8, 2, r[0]) ]

    t = [['doDash', move.Transition(2, HARE_ENERGY_USAGE, None, None, 'airDashing')]]

    moves['air'].append(f, t)

    moves['air'].transitions['attackBUpCharge'].var1 = 2
    moves['air'].transitions['attackBUpCharge'].var2 = HARE_ENERGY_USAGE

    moves['air'].transitions['attackBDown'].var1 = 2
    moves['air'].transitions['attackBDown'].var2 = HARE_ENERGY_USAGE

def createMoveFlipping():
    r = [
            [
                (-15, -29, 7, -6)
            ]
        ]

    flippingSpeed = 3
    f = [ move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[0]),
          move.frameData(33, flippingSpeed, r[0]),
          move.frameData(24, flippingSpeed, r[0]),
          move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[0]),
          move.frameData(33, flippingSpeed, r[0]),
          move.frameData(24, flippingSpeed, r[0]) ]

    t = [['doDash', move.Transition(2, HARE_ENERGY_USAGE, None, None, 'airDashing')]]

    moves['flipping'].append(f, t)

    moves['flipping'].transitions['attackBUpCharge'].var1 = 2
    moves['flipping'].transitions['attackBUpCharge'].var2 = HARE_ENERGY_USAGE

    moves['flipping'].transitions['attackBDown'].var1 = 2
    moves['flipping'].transitions['attackBDown'].var2 = HARE_ENERGY_USAGE

def createAirDash():

    f = [ move.frameData(159, 2),
          move.frameData(160, 1),
          move.frameData(159, 1),
          move.frameData(160, 1),
          move.frameData(159, 1),
          move.frameData(159, 8) ]

    t = [ ['exitFrame', move.Transition(-1, 0, None, None, 'air')],
         ['land', move.Transition(None, None, None, None, 'landing')],
         ['attackA', move.Transition(None, None, 5, 5, 'neutralAirA')],
         ['attackB', move.Transition(None, None, 5, 5, 'neutralAirB')],
         ['attackAUp', move.Transition(None, None, 5, 5, 'upAirA')],
         ['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 5, 5, 'upAirB')],
         ['attackADown', move.Transition(None, None, 5, 5, 'downAirA')],
         ['attackBDown', move.Transition(2, HARE_ENERGY_USAGE, 5, 5, 'downAirB')] ]

    moves['airDashing'] = move.Move(f, t)


    moves['airDashing'].frames[0].setVelX = 22
    moves['airDashing'].canDI = False

    for i in range(len(moves['airDashing'].frames)):
        moves['airDashing'].frames[i].setFrictionX = 1.0
        moves['airDashing'].frames[i].setVelY = 0
        moves['airDashing'].frames[i].ignoreSpeedCap = True

    moves['airDashing'].frames[0].fx.append(['airelementshockwave', (-20, -30), False])



def createMoveAirLike():
    r = [
            [
                (-9, -36, 3, -11),
                (0, -15, 7, -5),
                (-9, -12, -4, -6),
                (-1, -47, 10, -32)
            ]
        ]

    f = [ move.frameData(67, 1, r[0]),
          move.frameData(8, 1, r[0]),
          move.frameData(67, 1, r[0]) ]
    moves['airLike'].append(f, [])
    moves['airLike'].frames[0].ignoreFriction = True
    moves['airLike'].frames[0].ignoreSpeedCap = True
    moves['airLike'].frames[1].ignoreFriction = True
    moves['airLike'].frames[1].ignoreSpeedCap = True

def createMoveLanding():
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
    f = [ move.frameData(9, 3, r[0]) ]
    moves['landing'].append(f, [])

def createMoveJumping():
    r = [
            [
                (-7, -36, 1, -15),
                (-12, -16, -7, 0),
                (1, -18, 8, -12),
                (5, -12, 11, 1),
                (-4, -50, 6, -32),
                (-15, -34, -5, -30),
                (6, -3, 15, 1)
             ]
        ]
    f = [ move.frameData(9, 3, r[0]) ]
    moves['jumping'].append(f, [])

def createMoveJumpingLike():
    r = [
            [
                (-9, -36, 3, -11),
                (0, -15, 7, -5),
                (-9, -12, -4, -6),
                (-1, -47, 10, -32)
            ]
        ]

    f = [ move.frameData(67, 1, r[0]),
          move.frameData(8, 1, r[0]),
          move.frameData(67, 1, r[0]) ]
    moves['jumpingLike'].append(f, [])

def createMoveDucking():
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

    f = [ move.frameData(10, 2, r[0]) ]
    moves['ducking'].append(f, [])

def createMoveJabA():
    r = [
            [
                (-7, -46, 1, -31),
                (-13, -36, 1, -13),
                (-1, -13, 6, -6),
                (3, -8, 9, 1),
                (-16, -14, -10, -8),
                (-17, -9, -11, 3)
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

    f = [ move.frameData(41, 2, r[0]),
          move.frameData(42, 1, r[0], h[0]),
          move.frameData(43, 3, r[0]),
          move.frameData(43, 10, r[0])]
    t = [ ['attackA', move.Transition(None, None, 3, None, 'jab2')],
          ['attackAUp', move.Transition(None, None, 3, None, 'jab2')],
          ['attackADown', move.Transition(None, None, 3, None, 'jab2')]]
    moves['jabA'].append(f, t)
    moves['jabA'].canDI = False

    createMoveJab2()

def createMoveJab2():
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

    f = [ move.frameData(43, 2, r[0]),
          move.frameData(44, 2, r[1], h[0]),
          move.frameData(45, 9, r[2]),
          move.frameData(45, 3, r[2])]
    t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 1, 2, 'idleLike')],
          ['attackB', move.Transition(0, 0, 1, 2, 'upB')],
          ['attackBUp', move.Transition(0, 0, 1, 2, 'upB')] ]
    moves['jab2'] = move.Move(f, t)
    moves['jab2'].canDI = False

def createMoveJabB():
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

    f = [ move.frameData(46, 3, r[0]),
          move.frameData(47, 1, r[1]),
          move.frameData(48, 1, r[2], h[0]),
          move.frameData(49, 4, r[3], h[1]),
          move.frameData(49, 2, r[3]),
          move.frameData(50, 4, r[4]),
          move.frameData(169, 3, r[5]),
          move.frameData(0, 2, r[5])]
    moves['jabB'].append(f, [])
    moves['jabB'].canDI = False

def createMoveDashAttackA():

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

    f = [ move.frameData(2, 3, r[0]),
          move.frameData(153, 5, r[1], h[0]),
          move.frameData(154, 3, r[2], h[0]),
          move.frameData(155, 2, r[3], h[0]),
          move.frameData(156, 1, r[4]),
          move.frameData(157, 1, r[5]),
          move.frameData(158, 3, r[6]),
          move.frameData(157, 2, r[5]) ]

    t = [ ['attackB', move.Transition(0, 0, 2, 5, 'upB')],
          ['attackBUp', move.Transition(0, 0, 2, 5, 'upB')] ]

    moves['dashAttackA'].append(f, t)
    moves['dashAttackA'].canDI = False

    moves['dashAttackA'].frames[0].setVelX = 16
    for i in range(5):
        moves['dashAttackA'].frames[i].setFrictionX = 0.5
    for i in range(len(moves['dashAttackA'].frames)):
        moves['dashAttackA'].frames[i].ignoreSpeedCap = True

def createMoveDashAttackB():
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
    f = [ move.frameData(59, 3, r[0]),
          move.frameData(59, 2, r[0]),
          move.frameData(59, 3, r[0]),
          move.frameData(60, 1, r[1], h[0]),
          move.frameData(61, 1, r[2], h[1]),
          move.frameData(62, 2, r[3]),
          move.frameData(63, 5, r[4]),
          move.frameData(64, 2, r[5]),
          move.frameData(65, 2, r[6]) ]
    t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 2, 4, 'idleLike')] ]
    moves['dashAttackB'].append(f, t)
    moves['dashAttackB'].canDI = False
    moves['dashAttackB'].frames[0].setVelX = 15
    moves['dashAttackB'].frames[0].ignoreFriction = True
    moves['dashAttackB'].frames[0].ignoreSpeedCap = True
    moves['dashAttackB'].frames[1].ignoreFriction = True
    moves['dashAttackB'].frames[1].ignoreSpeedCap = True
    moves['dashAttackB'].frames[2].ignoreSpeedCap = True


def createOldMoveDashAttackB():
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

    f = [ move.frameData(19, 2),
          move.frameData(23, 2),
          move.frameData(20, 1, r[0]),
          move.frameData(33, 2, r[0]),
          move.frameData(21, 1, r[0]),
          move.frameData(24, 2, r[0]),
          move.frameData(22, 1, r[0]),
          move.frameData(34, 2, r[0]),
          move.frameData(19, 1, r[0]),
          move.frameData(23, 2, r[0]),
          move.frameData(19, 1, r[0]),
          move.frameData(23, 2, r[0]),
          move.frameData(20, 1, r[0]),
          move.frameData(33, 2, r[0])]
    t = [ ['exitFrame', move.Transition(-1, None, None, None, 'rollingSlash')],
          ['releaseB', move.Transition(-1, None, 5, None, 'rollingSlash')],
          ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 4, None, 'idleLike')]]
    moves['dashAttackB'].append(f, t)
    moves['dashAttackB'].canDI = False
    moves['dashAttackB'].frames[0].setVelX = 17
    for i in range(len(moves['dashAttackB'].frames)):
        moves['dashAttackB'].frames[i].ignoreFriction = True
        moves['dashAttackB'].frames[i].ignoreSpeedCap = True

    createMoveRollingSlash()

def createMoveRollingSlash():
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
    f = [ move.frameData(25, 3, r[0]),
          move.frameData(26, 1, r[0], h[0]),
          move.frameData(26, 1, r[0], h[1]),
          move.frameData(27, 2, r[0], h[2]),
          move.frameData(28, 11, r[0])]
    moves['rollingSlash'] = move.Move(f, [])
    moves['rollingSlash'].canDI = False
    moves['rollingSlash'].frames[0].setVelX = 0

def createMoveDownA():
    r = [
            [
                (4, -38, 16, 1),
                (15, -19, 21, -2),
                (-2, -27, 5, -19)
            ],
            [
                (6, -36, 21, -7),
                (4, -13, 13, 2),
                (17, -15, 36, -7)
            ],
            [
                (3, -33, 22, -6),
                (20, -12, 36, -3),
                (32, -6, 46, 1),
                (6, -6, 11, 1)
            ],
            [
             (9, -37, 19, -8),
             (1, -28, 12, 1),
             (17, -15, 29, -1)
            ],
        ]

    dam1 = 80
    stun1 = 101
    force1 = 6
    angle1 = 30

    h = [
            [
                [22, -13, 66, -1],
                [7, -18, 26, -5]
            ]
        ]

    h[0] = [i + [dam1, stun1, force1, angle1, [('untechable')], 0] for i in h[0]]




    f = [ move.frameData(29, 3, r[0]),
          move.frameData(30, 2, r[1], h[0]),
          move.frameData(31, 6, r[2]),
          move.frameData(32, 7, r[3]) ]
    moves['downA'].append(f, [])
    moves['downA'].canDI = False

def createMoveUpA():
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


    f = [ move.frameData(125, 4, r[0]),
          move.frameData(126, 2, r[1], h[0]),
          move.frameData(127, 1, r[2]),
          move.frameData(128, 3, r[3]),
          move.frameData(129, 3, r[1], h[1]),
          move.frameData(130, 1, r[2]),
          move.frameData(131, 20, r[3])]
    moves['upA'].append(f, t)
    moves['upA'].canDI = False
    moves['upA'].liftOff = True

    moves['upA'].frames[1].setVelY = -5.0
    moves['upA'].frames[1].setVelX = 6.0
    moves['upA'].frames[1].ignoreFriction = True
    moves['upA'].frames[4].setVelY = -5.5
    moves['upA'].frames[4].setVelX = 4.0
    moves['upA'].frames[4].ignoreFriction = True

    moves['upA'].frames[5].setAccelY = airAccel * 0.75
    moves['upA'].frames[6].setAccelY = airAccel * 0.75

    moves['upA'].frames[3].resetHitPotential = True

    createMoveUpAConfirm()

def createMoveUpAConfirm():
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

    f = [ move.frameData(129, 3, r[0]),
          move.frameData(130, 1, r[1]),
          move.frameData(131, 3, r[2]),
          move.frameData(131, 20, r[2])]

    t = [['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 0, 2, 'upAirB')],
         ['attackB', move.Transition(None, None, 0, 2, 'upASideKick')],
         ['attackA', move.Transition(None, None, 0, 2, 'upADropSlash')],
         ['attackADown', move.Transition(None, None, 0, 2, 'upADropSlash')],
         ['attackAUp', move.Transition(None, None, 0, 2, 'upADropSlash')] ]

    moves['upAConfirm'] = move.Move(f, t)
    moves['upAConfirm'].canDI = False

    moves['upAConfirm'].frames[0].setVelY = -5.5
    moves['upAConfirm'].frames[0].setVelX = 4.0
    moves['upAConfirm'].frames[0].ignoreFriction = True

    moves['upAConfirm'].frames[1].setAccelY = airAccel * 0.75
    moves['upAConfirm'].frames[2].setAccelY = airAccel * 0.75
    moves['upAConfirm'].frames[3].setAccelY = airAccel * 0.75

    createMoveUpASideKick()
    createMoveUpADropSlash()

def createMoveUpASideKick():
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


    f = [ move.frameData(35, 9, r[0]),
          move.frameData(36, 1, r[1], h[0]),
          move.frameData(37, 3, r[2], h[0]),
          move.frameData(37, 7, r[2]),
          move.frameData(124, 20)]

    moves['upASideKick'] = move.Move(f, [])
    moves['upASideKick'].canDI = False

    moves['upASideKick'].frames[0].setVelY = -6
    moves['upASideKick'].frames[0].setVelX = -0.5
    moves['upASideKick'].frames[0].ignoreFriction = True
    moves['upASideKick'].frames[2].setVelY = -1.0
    moves['upASideKick'].frames[2].setVelX = -1.2

def createMoveUpADropSlash():
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



    f = [ move.frameData(59, 2, r[0]),
          move.frameData(59, 10, r[0]),
          move.frameData(132, 2, r[1], h[0] ),
          move.frameData(132, 20, r[1] ) ]
    t = [ ['land', move.Transition(None, None, None, None, 'dropSlashLag')] ]


    moves['upADropSlash'] = move.Move(f, t)
    moves['upADropSlash'].canDI = False

    moves['upADropSlash'].frames[0].setVelY = -10.0
    moves['upADropSlash'].frames[0].setVelX = 8.0
    moves['upADropSlash'].frames[2].setVelY = 30.0
    moves['upADropSlash'].frames[0].setAccelY = airAccel * 0.6
    moves['upADropSlash'].frames[1].setAccelY = airAccel * 0.6
    moves['upADropSlash'].frames[2].setAccelY = airAccel * 1.5
    moves['upADropSlash'].frames[3].setAccelY = airAccel * 1.5

    createLagDropSlash()

def createLagDropSlash():
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

    f = [ move.frameData(133, 10, r[0] ) ]

    moves['dropSlashLag'] = move.Move(f, [])
    moves['dropSlashLag'].canDI = False

def createMoveDownB():
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

    f = [ move.frameData(11, 7),
          move.frameData(11, 2, r[0]),
          move.frameData(12, 5, r[1]),
          move.frameData(13, 20, r[2])]
    t = [ ['land', move.Transition(None, None, None, None, 'downBLag')],
          ['attackBDown', move.Transition(2, HARE_ENERGY_USAGE, 3, 3, 'downAirB')],
          ['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 3, 3, 'upAirB')],
          ['doDash', move.Transition(2, HARE_ENERGY_USAGE, 3, 3, 'airDashing')] ]


    moves['downB'].append(f, t)
    moves['downB'].canDI = False
    moves['downB'].liftOff = True
    moves['downB'].frames[0].setVelX = -28
    moves['downB'].frames[0].setVelY = -9.5
    moves['downB'].frames[0].ignoreSpeedCap = True
    moves['downB'].frames[0].ignoreFriction = True
    moves['downB'].frames[1].ignoreFriction = True
    moves['downB'].frames[2].setFrictionX = airFriction * 0.35
    moves['downB'].frames[0].fx.append(['dust', (14, 0), True])
    moves['downB'].frames[0].fx.append(['dust', (-14, 0), False])


    createLagDownB()

def createLagDownB():
    r = [
            [
                (-9, -27, 6, -15),
                (-14, -16, 8, -10),
                (-7, -10, 9, 5)
            ]
        ]

    f = [ move.frameData(86, 8, r[0]) ]
    moves['downBLag'] = move.Move(f, [])
    moves['downBLag'].canDI = False

def createMoveUpB():
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





    f = [ move.frameData(88, 1, r[0]),
          move.frameData(89, 1, r[1]),
          move.frameData(90, 1, r[2]),
          move.frameData(91, 1, r[3]),
          move.frameData(92, 2, r[4], h[0]),
          move.frameData(92, 4, r[4], h[0]),
          move.frameData(92, 7, r[4]),
          move.frameData(91, 2, r[3]),
          move.frameData(90, 2, r[2]),
          move.frameData(89, 1, r[1]),
          move.frameData(88, 1, r[0]) ]

    t = [['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 5, 7, 'idleLike')],
         ['jump', move.Transition(2, HARE_ENERGY_USAGE, 5, 7, 'jumpingLike')]]


    moves['upB'].append(f, t)
    moves['upB'].canDI = False
    moves['upB'].frames[0].setVelX = 10

def createOldSpinAttack():
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


    f = [ move.frameData(9, 6, r[0]),
          move.frameData(93, 1, [], h[0]),
          move.frameData(94, 1, [], h[0]),
          move.frameData(95, 1, [], h[0]),
          move.frameData(96, 1, [], h[0]),
          move.frameData(97, 1, [], h[0]),
          move.frameData(98, 1, [], h[0]),
          move.frameData(99, 1, [], h[0]),
          move.frameData(100, 1, [], h[0]),
          move.frameData(93, 1, [], h[1]),
          move.frameData(94, 1, [], h[1]),
          move.frameData(95, 1, [], h[1]),
          move.frameData(96, 1, [], h[1]),
          move.frameData(97, 1, [], h[1]),
          move.frameData(98, 1, [], h[1]),
          move.frameData(99, 1, [], h[1]),
          move.frameData(100, 1, [], h[1]) ]

    t = [['exitFrame', move.Transition(-1, None, None, None, 'rotateKick')]]

    moves['upB'].append(f, t)
    moves['upB'].canDI = False
    moves['upB'].liftOff = True

    moves['upB'].frames[0].setAccelX = 0
    for i in range(1,4):
        moves['upB'].frames[i].setVelY = -18.0
        moves['upB'].frames[i].setAccelY = 0

    for i in range(17):
        moves['upB'].frames[i].resetHitPotential = True

    createMoveRotateKick()

def createMoveRotateKick():
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


    f = [ move.frameData(107, 4, r[0]),
          move.frameData(101, 4, r[0], h[0]),
          move.frameData(102, 3, r[0], h[0]),
          move.frameData(103, 3, r[0], h[0]),
          move.frameData(104, 2, r[0]),
          move.frameData(105, 2, r[0]),
          move.frameData(106, 2, r[0]) ]


    moves['rotateKick'] = move.Move(f, [])
    moves['rotateKick'].canDI = True

    for i in range(6):
        moves['rotateKick'].frames[i].setAccelY = 0.55
        moves['rotateKick'].frames[i].setSpeedCapX = airVelMax * 1.2
        moves['rotateKick'].frames[i].setAccelX = airAccel * 2.0
        moves['rotateKick'].frames[i].setFrictionX = airFriction * 2.0




def createMoveNeutralAirA():
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

    f = [ move.frameData(14, 3, r[0]),
          move.frameData(15, 1, r[1], h[0]),
          move.frameData(16, 1, r[2], h[1]),
          move.frameData(17, 2, r[3], h[2]),
          move.frameData(18, 6, r[4]) ]
    moves['neutralAirA'].append(f, [])
    moves['neutralAirA'].reversable = True

def createMoveNeutralAirB():
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
    f = [ move.frameData(35, 3, r[0]),
          move.frameData(36, 1, r[1], h[0]),
          move.frameData(37, 3, r[2], h[0]),
          move.frameData(38, 3, r[3]),
          move.frameData(39, 1, r[4], h[0]),
          move.frameData(40, 3, r[5], h[0]),
          move.frameData(35, 3, r[0]),
          move.frameData(36, 1, r[1], h[1]),
          move.frameData(37, 4, r[2], h[1]),
          move.frameData(8, 4, r[6])]

    t = [ ['attackBDown', move.Transition(2, HARE_ENERGY_USAGE, 6, 9, 'downAirB')],
          ['attackBUpCharge', move.Transition(2, HARE_ENERGY_USAGE, 6, 9, 'upAirB')],
          ['doDash', move.Transition(2, HARE_ENERGY_USAGE, 6, 9, 'airDashing')] ]


    moves['neutralAirB'].append(f, t)
    moves['neutralAirB'].canDI = False
    moves['neutralAirB'].reversable = True
    moves['neutralAirB'].frames[1].setVelYIfDrop = -3.4
    moves['neutralAirB'].frames[4].setVelYIfDrop = -1.5
    moves['neutralAirB'].frames[7].setVelYIfDrop = -1.5
    moves['neutralAirB'].frames[4].resetHitPotential = True
    moves['neutralAirB'].frames[7].resetHitPotential = True
    for i in range(len(moves['neutralAirB'].frames)):
        moves['neutralAirB'].frames[i].ignoreFriction = True

def createMoveUpAirA():
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

    f = [ move.frameData(75, 4, r[0]),
          move.frameData(76, 2, r[1], h[0]),
          move.frameData(77, 1, r[2], h[1]),
          move.frameData(78, 1, r[3], h[2]),
          move.frameData(79, 2, r[4], h[3]),
          move.frameData(80, 5, r[4]) ]

    moves['upAirA'].append(f, [])

def createMoveUpAirB():
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
    f = [ move.frameData(51, 3, r[0]),
          move.frameData(52, 1, r[1], h[0]),
          move.frameData(53, 1, r[1], h[0]),
          move.frameData(54, 1, r[1], h[0]),
          move.frameData(52, 1, r[1], h[0]),
          move.frameData(53, 1, r[1], h[0]),
          move.frameData(54, 1, r[1], h[0]),
          move.frameData(52, 1, r[1], h[0]),
          move.frameData(53, 1, r[1], h[0]),
          move.frameData(54, 1, r[1], h[0]),
          move.frameData(52, 1, r[1], h[0]),
          move.frameData(53, 1, r[1], h[0]),
          move.frameData(54, 1, r[1], h[0]),
          move.frameData(52, 1, r[1], h[0]),
          move.frameData(53, 1, r[1], h[0]),
          move.frameData(54, 1, r[1], h[0]),
          move.frameData(52, 1, r[1], h[0]),
          move.frameData(53, 1, r[1], h[0]),
          move.frameData(54, 1, r[1], h[0]),
          move.frameData(8, 2, r[1], h[0]),
          move.frameData(8, 5, r[2])]
    t = [ ['doDuck', move.Transition(2, HARE_ENERGY_USAGE, 1, 17, 'airLike')] ]
    moves['upAirB'].append(f, t)
    moves['upAirB'].canDI = False
    moves['upAirB'].reversable = True
    for i in range(len(moves['upAirB'].frames)):
        moves['upAirB'].frames[i].setVelY = -12.0
        moves['upAirB'].frames[i].setVelX = 10.0
    moves['upAirB'].frames[0].setVelY = 0
    moves['upAirB'].frames[0].setVelX = 0
    moves['upAirB'].frames[19].setVelY = 0
    moves['upAirB'].frames[19].setVelX = None
    moves['upAirB'].frames[20].setVelY = None
    moves['upAirB'].frames[20].setVelX = None

    moves['upAirB'].frames[4].resetHitPotential = True
    moves['upAirB'].frames[7].resetHitPotential = True
    moves['upAirB'].frames[10].resetHitPotential = True
    moves['upAirB'].frames[13].resetHitPotential = True
    moves['upAirB'].frames[16].resetHitPotential = True
    moves['upAirB'].frames[19].resetHitPotential = True

def createMoveDownAirA():
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

    f = [ move.frameData(85, 9, r[0]),
          move.frameData(82, 1, r[1]),
          move.frameData(83, 1, r[2], h[0]),
          move.frameData(84, 7, r[2], h[0]),
          move.frameData(84, 6, r[3]) ]

    t = [['land', move.Transition(None, None, None, None, 'downAAirLag')],
         ['onHit', move.Transition(None, None, None, None, 'headBounce')],
         ['attackA', move.Transition(2, HARE_ENERGY_USAGE, 0, 0, 'stomp')],
         ['attackADown', move.Transition(2, HARE_ENERGY_USAGE, 0, 0, 'stomp')]]



    moves['downAirA'].append(f, t)
    moves['downAirA'].frames[0].setVelY = -0.5
    moves['downAirA'].frames[1].setVelY = 20

    for i in range(len(moves['downAirA'].frames)):
        moves['downAirA'].frames[i].ignoreSpeedCap = True

    moves['downAirA'].canDI = False


    createLagDownAAir()
    createHeadBounce()
    createStomp()

def createLagDownAAir():
    r = [
            [
                (-9, -27, 6, -15),
                (-14, -16, 8, -10),
                (-7, -10, 9, 5)
            ]
        ]


    f = [ move.frameData(86, 12, r[0]) ]

    moves['downAAirLag'] = move.Move(f, [])
    moves['downAAirLag'].canDI = False

def createHeadBounce():
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
    f = [ move.frameData(84, 3),
          move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[1]),
          move.frameData(33, flippingSpeed, r[2]),
          move.frameData(24, flippingSpeed, r[3]),
          move.frameData(87, 6, r[4]),
          move.frameData(87, 6, r[4]),
          move.frameData(87, 2, r[4])]

    t = [['doDash', move.Transition(2, HARE_ENERGY_USAGE, 6, 7, 'airDashing')],
         ['attackADown', move.Transition(2, HARE_ENERGY_USAGE, 2, 6, 'stomp')]]

    moves['headBounce'] = move.Move(f, t)
    moves['headBounce'].frames[0].setVelY = -22

    for i in range(len(f)-1):
        moves['headBounce'].frames[i].setAccelX = 5.0
        moves['headBounce'].frames[i].setFrictionX = airFriction * 8.0
        moves['headBounce'].frames[i].setSpeedCapX = vertVelMax * 1.2


def createStomp():

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

    f = [ move.frameData(163, 3, r[0]),
          move.frameData(164, 1, r[1], h[0]),
          move.frameData(165, 2, r[1], h[0]),
          move.frameData(165, 12, r[1], h[1]),
          move.frameData(165, 5, r[2]) ]

    t = []


    moves['stomp'] = move.Move(f, t)
    #moves['stomp'].canDI = False
    moves['stomp'].reversable = True

    moves['stomp'].frames[0].setVelY = 0


def createMoveDownAirB():
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
    f = [ move.frameData(55, 5, r[0]),
          move.frameData(56, 1, r[1], h[0]),
          move.frameData(57, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0]),
          move.frameData(56, 1, r[1], h[0]),
          move.frameData(57, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0]),
          move.frameData(56, 1, r[1], h[0]),
          move.frameData(57, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0]),
          move.frameData(56, 1, r[1], h[0]),
          move.frameData(57, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0]),
          move.frameData(56, 1, r[1], h[0]),
          move.frameData(57, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0]),
          move.frameData(56, 1, r[1], h[0]),
          move.frameData(57, 1, r[1], h[0]),
          move.frameData(58, 1, r[1], h[0])]

    t = [ ['land', move.Transition(None, None, None, None, 'downBAirLag')] ]

    moves['downAirB'].append(f, t)
    moves['downAirB'].canDI = False
    moves['downAirB'].reversable = True
    for i in range(len(moves['downAirB'].frames)):
        moves['downAirB'].frames[i].ignoreSpeedCap = True
        moves['downAirB'].frames[i].ignoreFriction = True
        moves['downAirB'].frames[i].setVelY = 20.0
        moves['downAirB'].frames[i].setVelX = 18.0
    moves['downAirB'].frames[0].setVelY = 0
    moves['downAirB'].frames[0].setVelX = 0

    createLagDownBAir()

def createMoveDroppingThrough():
    f = [ move.frameData(8, 3) ]

    moves['droppingThrough'].append(f, [])

def createMoveGrabbing():
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


    f = [ move.frameData(110, 2, r[0]),
          move.frameData(111, 1, r[1], h[0]),
          move.frameData(112, 1, r[2], h[1]),
          move.frameData(113, 2, r[3], h[1]),
          move.frameData(114, 2, r[4], h[1]),
          move.frameData(114, 7, r[4]),
          move.frameData(111, 2, r[1]) ]

    moves['grabbing'].append(f, [])
    moves['grabbing'].frames[1].setVelX = 10.0
    moves['grabbing'].frames[1].ignoreFriction = True
    moves['grabbing'].frames[2].ignoreFriction = True
    moves['grabbing'].frames[6].setVelX = -10.0
    moves['grabbing'].frames[6].ignoreFriction = True

def createMoveGrabHold():
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

    f = [ move.frameData(114, 10, r[0]),
          move.frameData(114, 42, r[0]),
          move.frameData(114, 2, r[0])]

    moves['grabHold'].append(f, [])
    moves['grabHold'].grabPos = (13, 0)


def createMoveGrabbed():
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

    f = [ move.frameData(70, 2, r[0]),
          move.frameData(70, 5, r[0]),
          move.frameData(70, 2, r[0]) ]

    moves['grabbed'].append(f, [])
    moves['grabbed'].grabPos = (12, 0)

def createMoveGrabbed2():
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

    f = [ move.frameData(70, 2, r[0]) ]

    moves['grabbed2'].append(f, [])
    moves['grabbed2'].grabPos = (12, 0)


def createMoveGrabRelease():

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

    f = [ move.frameData(110, 2, r[0]),
          move.frameData(110, 1, r[0]),
          move.frameData(110, 22, r[0])]

    moves['grabRelease'].append(f, [])
    moves['grabRelease'].frames[1].setVelX = -20.0
    moves['grabRelease'].frames[1].setFrictionX = 0.5
    moves['grabRelease'].frames[2].setFrictionX = 0.75

def createMoveGrabbedRelease():

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

    f = [ move.frameData(69, 2, r[0]),
          move.frameData(69, 1, r[0]),
          move.frameData(69, 22, r[0])]

    moves['grabbedRelease'].append(f, [])
    moves['grabbedRelease'].frames[1].setVelX = -20.0
    moves['grabbedRelease'].frames[1].setFrictionX = 0.5
    moves['grabbedRelease'].frames[2].setFrictionX = 0.75

def createMoveThrowBackward():

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

    f = [ move.frameData(115, 3),
          move.frameData(116, 2),
          move.frameData(117, 6),
          move.frameData(118, 2, [], h[0]),
          move.frameData(119, 14),
          move.frameData(120, 3),
          move.frameData(10, 6) ]

    moves['throwBackward'].append(f, [])

def createMoveThrowForward():

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

    f = [ move.frameData(35, 2, [], h[0]),
          move.frameData(35, 6),
          move.frameData(35, 2),
          move.frameData(121, 1),
          move.frameData(122, 1, [], h[1]),
          move.frameData(123, 5),
          move.frameData(123, 1),
          move.frameData(124, 10)]

    t = [ ['land', move.Transition(None, None, None, None, 'lagForwardThrow')] ]

    moves['throwForward'].append(f, t)
    moves['throwForward'].liftOff = True
    moves['throwForward'].frames[0].setVelY = -5.0
    moves['throwForward'].frames[2].setVelY = 0
    moves['throwForward'].frames[3].setVelY = 0
    moves['throwForward'].frames[4].setVelY = 0
    moves['throwForward'].frames[5].setVelY = 0

    moves['throwForward'].frames[2].resetHitPotential = True

    moves['throwForward'].frames[0].setVelX = 13
    for i in range(3):
        moves['throwForward'].frames[i].setFrictionX = 0

    createLagForwardThrow()

def createLagForwardThrow():
    f = [ move.frameData(10, 8) ]
    moves['lagForwardThrow'] = move.Move(f, [])
    moves['lagForwardThrow'].canDI = False

def createLagDownBAir():
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
    f = [ move.frameData(9, 7, r[0]) ]
    moves['downBAirLag'] = move.Move(f, [])
    moves['downBAirLag'].canDI = False

def createMoveStun1():
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

    f = [ move.frameData(68, 9, r[0]) ]

    moves['stun1'].append(f, [])

    for i in range(len(moves['stun1'].frames)):
        moves['stun1'].frames[i].ignoreSpeedCap = True

def createMoveStun2():
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

    f = [ move.frameData(69, 14, r[0]) ]

    moves['stun2'].append(f, [])

    for i in range(len(moves['stun2'].frames)):
        moves['stun2'].frames[i].ignoreSpeedCap = True

def createMoveStun3():
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


    f = [ move.frameData(70, 10, r[0]),
          move.frameData(71, 2, r[1]),
          move.frameData(72, 1, r[2]),
          move.frameData(73, 1, r[3]),
          move.frameData(74, 12, r[4])]

    moves['stun3'].append(f, [])

    for i in range(len(moves['stun3'].frames)):
        moves['stun3'].frames[i].ignoreSpeedCap = True

def createMoveStun4():
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


    f = [ move.frameData(70, 15, r[0]),
          move.frameData(71, 2, r[1]),
          move.frameData(72, 1, r[2]),
          move.frameData(73, 1, r[3]),
          move.frameData(74, 24, r[4])]

    moves['stun4'].append(f, [])

    for i in range(len(moves['stun4'].frames)):
        moves['stun4'].frames[i].ignoreSpeedCap = True

def createMoveDeadFalling():
    f = [ move.frameData(74, 3) ]

    moves['deadFalling'].append(f, [])

    for i in range(len(moves['deadFalling'].frames)):
        moves['deadFalling'].frames[i].ignoreSpeedCap = True
        moves['deadFalling'].frames[i].ignoreFriction = True

def createMoveDeadGroundHit():
    f = [ move.frameData(134, 2),
          move.frameData(135, 4),
          move.frameData(136, 2),
          move.frameData(137, 1) ]

    moves['deadGroundHit'].append(f, [])

def createMoveDeadLaying():
    f = [ move.frameData(137, 3) ]

    moves['deadLaying'].append(f, [])

def createMoveGroundHit():
    r = [
            [
                (-25, -12, -14, 0),
                (-28, -10, -25, 0),
                (-15, -10, 15, -1),
                (13, -12, 21, -7),
                (15, -7, 41, -1)
            ]
        ]

    f = [ move.frameData(134, 2),
          move.frameData(135, 4),
          move.frameData(136, 2),
          move.frameData(137, 1),
          move.frameData(136, 1),
          move.frameData(137, 10),
          move.frameData(137, 2),
          move.frameData(137, 80, r[0]) ]

    t = [ ['attackB', move.Transition(None, None, -2, -1, 'downB')],
          ['attackBDown', move.Transition(None, None, -2, -1, 'downB')] ]

    moves['groundHit'].append(f, t)
    moves['groundHit'].frames[0].fx.append(['dust', (28, 0), True])
    moves['groundHit'].frames[0].fx.append(['dust', (-28, 0), False])
    moves['groundHit'].frames[1].fx.append(['shockwave', (0, 0), True])

def createMoveStandUp():
    f = [ move.frameData(138, 4),
          move.frameData(139, 4),
          move.frameData(28, 6) ]

    moves['standUp'].append(f, [])

def createMoveStandForward():
    f = [ move.frameData(138, 4),
          move.frameData(20, 1),
          move.frameData(33, 2),
          move.frameData(21, 1),
          move.frameData(24, 2),
          move.frameData(22, 1),
          move.frameData(34, 2),
          move.frameData(19, 1),
          move.frameData(28, 3) ]

    moves['standForward'].append(f, [])

    moves['standForward'].frames[1].setVelX = 22.8
    moves['standForward'].frames[8].setVelX = 0

    for i in range(len(moves['standForward'].frames)):
        moves['standForward'].frames[i].setFrictionX = groundFriction * 0.42
        moves['standForward'].frames[i].ignoreSpeedCap = True

def createMoveStandBackward():
    f = [ move.frameData(138, 4),
          move.frameData(19, 1),
          move.frameData(34, 2),
          move.frameData(22, 1),
          move.frameData(24, 2),
          move.frameData(21, 1),
          move.frameData(33, 2),
          move.frameData(20, 1),
          move.frameData(28, 3) ]

    moves['standBackward'].append(f, [])

    moves['standBackward'].frames[1].setVelX = -22.8
    moves['standBackward'].frames[8].setVelX = 0

    for i in range(len(moves['standBackward'].frames)):
        moves['standBackward'].frames[i].setFrictionX = groundFriction * 0.42
        moves['standBackward'].frames[i].ignoreSpeedCap = True

def createMoveStandAttack():

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

    f = [ move.frameData(138, 4),
          move.frameData(139, 3),
          move.frameData(25, 2, r[0]),
          move.frameData(26, 1, r[0], h[0]),
          move.frameData(27, 2, r[0], h[0]),
          move.frameData(28, 11, r[0]) ]

    moves['standAttack'].append(f, [])


def createMoveTeching():
    f = [ move.frameData(140, 4),
          move.frameData(140, 1)]

    moves['teching'].append(f, [])

def createMoveTechUp():
    f = [ move.frameData(99, 3),
          move.frameData(94, 2) ]

    moves['techUp'].append(f, [])

def createMoveTechForward():
    f = [ move.frameData(20, 1),
          move.frameData(33, 2),
          move.frameData(21, 1),
          move.frameData(24, 2),
          move.frameData(22, 1),
          move.frameData(34, 2),
          move.frameData(19, 1),
          move.frameData(23, 2),
          move.frameData(19, 1),
          move.frameData(23, 2),
          move.frameData(28, 6) ]


    moves['techForward'].append(f, [])

    moves['techForward'].frames[1].setVelX = 25
    moves['techForward'].frames[10].setVelX = 0

    for i in range(len(moves['techForward'].frames)):
        moves['techForward'].frames[i].setFrictionX = groundFriction * 0.75
        moves['techForward'].frames[i].ignoreSpeedCap = True

def createMoveTechBackward():

    f = [ move.frameData(23, 2),
          move.frameData(19, 1),
          move.frameData(23, 2),
          move.frameData(19, 1),
          move.frameData(34, 2),
          move.frameData(22, 1),
          move.frameData(24, 2),
          move.frameData(21, 1),
          move.frameData(33, 2),
          move.frameData(20, 1),
          move.frameData(28, 6) ]


    moves['techBackward'].append(f, [])

    moves['techBackward'].frames[1].setVelX = -25
    moves['techBackward'].frames[10].setVelX = 0

    for i in range(len(moves['techBackward'].frames)):
        moves['techBackward'].frames[i].setFrictionX = groundFriction * 0.75
        moves['techBackward'].frames[i].ignoreSpeedCap = True

def createSuperMove1():
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

    f = [ move.frameData(143, 2),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]),
          move.frameData(144, 1, [], h[0]),
          move.frameData(145, 1, [], h[0]),
          move.frameData(146, 1, [], h[0]) ]

    t = [['exitFrame', move.Transition(-1, None, None, None, 'super1Ending1')]]

    sg = move.SuperMove(n, d, f, t)

    for i in range(len(sg.frames)):
        sg.frames[i].setVelX = 19
        sg.frames[i].setVelY = 0
        sg.frames[i].ignoreSpeedCap = True
        sg.frames[i].ignoreFriction = True

        if (i % 3) == 1:
            sg.frames[i].resetHitPotential = True

    sg.flash = createSuperFlash1()
    sa = move.SuperMove(n, d, f, t)

    for i in range(len(sa.frames)):
        sa.frames[i].setVelX = 14
        sa.frames[i].setVelY = 0
        sa.frames[i].ignoreSpeedCap = True
        sa.frames[i].ignoreFriction = True

        if (i % 3) == 1:
            sa.frames[i].resetHitPotential = True

    sa.flash = createSuperFlash1Air()
    appendSuperMove(sg, sa)
    createSuper1Ending1()

def createSuperFlash1():

    s = move.baseSuperFlash()

    f = [ move.frameData(87, 2),
         move.frameData(87, 16),
         move.frameData(141, 2),
         move.frameData(141, 12),
         move.frameData(142, 12),
         move.frameData(143, 2)]

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

def createSuperFlash1Air():

    s = move.baseSuperFlash()

    f = [ move.frameData(87, 22),
         move.frameData(141, 2),
         move.frameData(141, 1),
         move.frameData(142, 1),
         move.frameData(143, 1)]

    s.append(f, [])
    s.liftOff = True

    for i in range(len(s.frames)):
        s.frames[i].setVelX = 0
        s.frames[i].setVelY = 0

    return s


def createSuper1Ending1():
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
    f = [ move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[1]),
          move.frameData(33, flippingSpeed, r[2]) ]

    t = [['land', move.Transition(None, None, None, None, 'super1EndingLag1')],
         ['exitFrame', move.Transition(-1, None, None, None, 'super1Ending2')]]

    moves['super1Ending1'] = move.Move(f, t)
    moves['super1Ending1'].canDI = False
    moves['super1Ending1'].canRetreat = False

    moves['super1Ending1'].frames[0].ignoreFriction = True
    moves['super1Ending1'].frames[1].ignoreFriction = True

    createSuper1EndingLag1()
    createSuper1Ending2()

def createSuper1EndingLag1():

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

    f = [ move.frameData(147, 8, r[0]),
          move.frameData(148, 14, r[0]) ]

    moves['super1EndingLag1'] = move.Move(f, [])
    moves['super1EndingLag1'].canDI = False
    moves['super1EndingLag1'].canRetreat = False

    moves['super1EndingLag1'].frames[0].setFrictionX = 0.3
    moves['super1EndingLag1'].frames[1].setFrictionX = 0.3

def createSuper1Ending2():
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
    f = [ move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[1]),
          move.frameData(33, flippingSpeed, r[2]),
          move.frameData(24, flippingSpeed, r[3]),
          move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[1]),
          move.frameData(33, flippingSpeed, r[2]),
          move.frameData(24, flippingSpeed, r[3]),
          move.frameData(34, flippingSpeed, r[0]),
          move.frameData(23, flippingSpeed, r[1]),
          move.frameData(33, flippingSpeed, r[2]),
          move.frameData(24, flippingSpeed, r[3]) ]

    t = [['land', move.Transition(None, None, None, None, 'super1EndingLag2')]]

    moves['super1Ending2'] = move.Move(f, t)
    moves['super1Ending2'].canDI = False
    moves['super1Ending2'].canRetreat = False

    createSuper1EndingLag2()

def createSuper1EndingLag2():
    r = [
            [
                (-9, -27, 6, -15),
                (-14, -16, 8, -10),
                (-7, -10, 9, 5)
            ]
        ]

    f = [ move.frameData(86, 16, r[0]) ]

    moves['super1EndingLag2'] = move.Move(f, [])
    moves['super1EndingLag2'].canDI = False
    moves['super1EndingLag2'].canRetreat = False

def createSuperMove2():
    n = "Blazing Ambush"

    d = ("")

    s = move.SuperMove(n, d, [], [])

    superMoves.append(s)
        
def appendSuperMove(ground, air):
    superMoves.append(ground)
    superMovesAir.append(air)

moves = {}
superMoves = []
superMovesAir = []
load()
