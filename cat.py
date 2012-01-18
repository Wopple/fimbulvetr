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
        self.dashVelMax = 16.0
        self.runVelMax = 11.0
        self.walkAccel = 2.5
        self.dashAccel = 12.0
        self.groundFriction = 2.8
        self.airAccel = 1.5
        self.airVelMax = 8.5
        self.airFriction = 1.2
        self.airFrictionStunned = self.airFriction * 0.3
        self.vertAccel = 0.6
        self.vertVelMax = 19.5
        self.jumpVel = -15.0
        self.blockFXPoints = [ (9, -35), (33, -32), (9, -35) ]
        self.catEnergy = boundint.BoundInt(0, CAT_ENERGY_MAX, 0)
        self.prevEnergy = self.catEnergy.value
        self.energyDelayTick = CAT_ENERGY_DELAY
        self.energy = self.catEnergy
        super(Cat, self).__init__(1000)
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
        self.createMoveAir()
        self.createMoveFlipping()
        self.createMoveJumping()
        self.createMoveDucking()
        self.createMoveJabA()
        self.createMoveJabB()
        self.createMoveDownA()
        self.createDashAttackA()
        self.createMoveUpB()
        self.createNeutralAirB()

        self.createProjectiles()

        self.createSuperMoves()

    def createSuperMoves(self):
        self.createSuperMove1()
        #self.createSuperMove2()

    def createMoveIdle(self):
        f = [ self.frameData(0, 2) ]
        self.moves['idle'].append(f, [])

    def createMoveWalking(self):
        f = [ self.frameData(1, 3),
              self.frameData(2, 3),
              self.frameData(3, 3),
              self.frameData(4, 3) ]
        self.moves['walking'].append(f, [])

    def createMoveAir(self):
        f = [ self.frameData(5, 2) ]
        self.moves['air'].append(f, [])
        
    def createMoveFlipping(self):
        f = [ self.frameData(5, 2) ]
        self.moves['flipping'].append(f, [])

    def createMoveJumping(self):
        f = [ self.frameData(5, 2) ]
        self.moves['jumping'].append(f, [])

    def createMoveDucking(self):
        f = [ self.frameData(18, 2) ]
        self.moves['ducking'].append(f, [])

    def createMoveJabA(self):
        f = [ self.frameData(14, 3),
              self.frameData(15, 4),
              self.frameData(15, 80) ]
        t = [ ['releaseA', move.Transition(None, None, 2, None, 'jabThrust')],
              ['exitFrame', move.Transition(-1, None, None, None, 'jabThrust')],
              ['doDuck', move.Transition(None, None, 2, None, 'jabCancel')] ]
        self.moves['jabA'].append(f, t)
        self.moves['jabA'].canDI = False

        self.createMoveJabThrust()
        self.createMoveJabCancel()

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


    def createDashAttackA(self):
        f = [ self.frameData(23, 2),
              self.frameData(24, 1),
              self.frameData(25, 1),
              self.frameData(26, 6) ]

        self.moves['dashAttackA'].append(f, [])
        self.moves['dashAttackA'].canDI = False

    def createMoveJabThrust(self):
        f = [ self.frameData(17, 5),
              self.frameData(16, 12) ]
        t = []
        self.moves['jabThrust'] = move.Move(f, t)
        self.moves['jabThrust'].canDI = False
        self.moves['jabThrust'].frames[0].setVelX = 45
        self.moves['jabThrust'].frames[0].ignoreFriction = True
        self.moves['jabThrust'].frames[0].ignoreSpeedCap = True
        self.moves['jabThrust'].frames[1].setVelX = 0

    def createMoveJabCancel(self):
        f = [ self.frameData(14, 5),
              self.frameData(0, 3) ]
        self.moves['jabCancel'] = move.Move(f, [])
        self.moves['jabCancel'].canDI = False

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
        f = [ self.frameData(42, 2),
              self.frameData(43, 5),
              self.frameData(43, 2),
              self.frameData(42, 2),
              self.frameData(18, 2)]

        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'ducking')] ]

        self.moves['downA'].append(f, t)
        self.moves['downA'].canDI = False

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
