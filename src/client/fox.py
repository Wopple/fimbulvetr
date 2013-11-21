import os
import sys
import pygame

import battlechar
import move
import projectile

from common.constants import *

class Fox(battlechar.BattleChar):
    def __init__(self, name="Unnamed Fox", inSpecial=0):
        self.name = name
        self.speciesName = "Fox"
        self.spriteSet = FOX_IMAGES
        self.superIcons = FOX_SUPER_ICONS
        self.groundAccel = 1.2
        self.groundVelMax = 12.5
        self.groundFriction = 2.2
        self.airAccel = 1.6
        self.airVelMax = 7.0
        self.airFriction = 0.9
        self.vertAccel = 1.5
        self.vertVelMax = 15.0
        self.jumpVel = -24.0
        self.youIconHeight = 80
        super(Fox, self).__init__(920)
        self.initSpecMoves()

        self.speciesDesc = ("A master of stealth and trickery capable of" +
                            " sneaking invisibly through enemy lines," +
                            " delivering unexpected ambushes, laying hidden" +
                            " traps across the battlefield, and fighting" +
                            " effectively at long range.")

        if (inSpecial < 0) or (inSpecial >= len(self.superMoves)):
            inSpecial = 0
        self.currSuperMove = inSpecial

    def beginBattle(self):
        super(Fox, self).beginBattle()

    def initSpecMoves(self):
        self.createMoveIdle()
        self.createMoveDash()
        self.createMoveAir()
        self.createMoveLanding()
        self.createMoveJumping()
        self.createMoveJabA()

        self.createProjectiles()

        self.createSuperMoves()

    def createSuperMoves(self):
        self.createSuperMove1()

    def createMoveIdle(self):
        f = [ self.frameData(0, 2) ]
        self.moves['idle'].append(f, [])

    def createMoveAir(self):
        f = [ self.frameData(7, 2) ]
        self.moves['air'].append(f, [])

    def createMoveDash(self):
        f = [ self.frameData(1, 3),
              self.frameData(2, 3),
              self.frameData(3, 3),
              self.frameData(4, 3),
              self.frameData(5, 3),
              self.frameData(6, 3) ]
        self.moves['dash'].append(f, [])

    def createMoveLanding(self):
        f = [ self.frameData(0, 4) ]
        self.moves['landing'].append(f, [])

    def createMoveJumping(self):
        f = [ self.frameData(0, 4) ]
        self.moves['jumping'].append(f, [])

    def createMoveJabA(self):
        f = [ self.frameData(8, 3),
              self.frameData(9, 2),
              self.frameData(10, 4),
              self.frameData(11, 14)]

        t = [ ['releaseA', move.Transition(-1, None, 3, 3, 'throw1')],
              ['exitFrame', move.Transition(-1, None, None, None, 'jabA2')]]
        self.moves['jabA'].append(f, t)
        self.moves['jabA'].canDI = False

        self.createMoveJabAPart2()
        self.createMoveThrow1()
        self.createMoveThrow2()

    def createMoveJabAPart2(self):
        f = [ self.frameData(14, 6),
              self.frameData(15, 30)]

        t = [ ['releaseA', move.Transition(-1, None, 1, 1, 'throw2')],
              ['exitFrame', move.Transition(-1, None, None, None, 'throw2')]]

        self.moves['jabA2'] = move.Move(f, t)
        self.moves['jabA2'].canDI = False

    def createMoveThrow1(self):
        f = [ self.frameData(11, 3),
              self.frameData(12, 1),
              self.frameData(13, 9) ]

        self.moves['throw1'] = move.Move(f, [])
        self.moves['throw1'].canDI = False
        self.moves['throw1'].shoot.append( (1, 0, (35, -46)) )
        self.moves['throw1'].shoot.append( (1, 1, (35, -46)) )
        self.moves['throw1'].shoot.append( (1, 2, (35, -46)) )

    def createMoveThrow2(self):
        f = [ self.frameData(11, 3),
              self.frameData(12, 1),
              self.frameData(13, 9) ]

        self.moves['throw2'] = move.Move(f, [])
        self.moves['throw2'].canDI = False
        self.moves['throw2'].canDI = False
        self.moves['throw2'].shoot.append( (1, 0, (35, -46)) )
        self.moves['throw2'].shoot.append( (1, 1, (35, -46)) )
        self.moves['throw2'].shoot.append( (1, 2, (35, -46)) )
        self.moves['throw2'].shoot.append( (1, 3, (35, -46)) )
        self.moves['throw2'].shoot.append( (1, 4, (35, -46)) )


    def createProjectiles(self):
        self.createProjectile1()
        self.createProjectile2()
        self.createProjectile3()
        self.createProjectile4()
        self.createProjectile5()

    def createProjectile1(self):
        temp = projectile.Projectile()

        f = [ self.frameData(16, 2) ]
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]
        
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 18

        self.createProjectileEnding1(temp)

        self.projectiles.append(temp)

    def createProjectile2(self):
        temp = projectile.Projectile()

        f = [ self.frameData(17, 2) ]
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]
        
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 17.3
        temp.moves['flying'].frames[0].setVelY = -4.6

        self.createProjectileEnding1(temp)

        self.projectiles.append(temp)

    def createProjectile3(self):
        temp = projectile.Projectile()

        f = [ self.frameData(18, 2) ]
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]
        
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 17.8
        temp.moves['flying'].frames[0].setVelY = -2.3

        self.createProjectileEnding1(temp)

        self.projectiles.append(temp)

    def createProjectile4(self):
        temp = projectile.Projectile()

        f = [ self.frameData(19, 2) ]
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]
        
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 16.6
        temp.moves['flying'].frames[0].setVelY = -6.8

        self.createProjectileEnding1(temp)

        self.projectiles.append(temp)

    def createProjectile5(self):
        temp = projectile.Projectile()

        f = [ self.frameData(20, 2) ]
        t = [ ['exitFrame', move.Transition(-1, None, None, None, 'flying')] ]
        
        temp.moves['flying'].append(f, t)
        temp.moves['flying'].frames[0].setVelX = 17.8
        temp.moves['flying'].frames[0].setVelY = 2.3

        self.createProjectileEnding1(temp)

        self.projectiles.append(temp)

    def createProjectileEnding1(self, m):
        f = [ self.frameData(21, 2),
              self.frameData(22, 1),
              self.frameData(23, 1),
              self.frameData(24, 1),
              self.frameData(21, 1),
              self.frameData(22, 1),
              self.frameData(23, 1),
              self.frameData(24, 1),
              self.frameData(21, 1),
              self.frameData(22, 1)]
        t = []

        m.moves['dissolve'].append(f, t)
        m.moves['dissolve'].frames[0].setVelX = -1.2
        m.moves['dissolve'].frames[0].setVelY = -2.5

        m.dissolveOnPhysical = True


    def createSuperMove1(self):
        n = "Shadow Trap"
        
        d = ("Secures the exit areas of the battlefield with traps of" +
             " harmful dark energy, punishing those who try to escape" +
             " from the encounter.")
        
        s = move.SuperMove(n, d, [], [])

        self.superMoves.append(s)
