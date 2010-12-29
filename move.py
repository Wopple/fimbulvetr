import os
import sys
import pygame

import incint

import hitbox
import hurtbox

from constants import *

class Move(object):
    def __init__(self, f, t):
        self.frames = []
        
        temp = ['exitFrame', 'doDash', 'noXMove', 'noXVel', 'land', 'jump',
                'doDuck', 'stopDuck', 'attackA', 'attackB', 'releaseA',
                'releaseB', 'attackAUp', 'attackBUp', 'attackADown',
                'attackBDown', 'attackBUpCharge', 'bladelv1', 'bladelv2',
                'bladelv3']
        self.transitions = {}
        for i in temp:
            self.transitions[i] = None

        self.shoot = []

        self.append(f, t)

        self.canDI = True
        self.isJump = False
        self.isStun = False
        self.liftOff = False
        self.reversable = False
        self.chargeBlade = False


    def append(self, f, t):
        for i in f:
            self.frames.append(Frame(i[0], i[1], i[2], i[3], i[4]))

        for i in t:
            self.transitions[i[0]] = i[1]

class SuperMove(Move):
    def __init__(self, inName, inDesc, f, t):
        super(SuperMove, self).__init__(f, t)
        self.name = inName
        self.desc = inDesc

class Frame(object):
    def __init__(self, inImage, inOffset, inLength, hurtboxData, hitboxData):
        self.image = inImage
        self.offset = inOffset
        self.length = inLength
        self.setVelX = None
        self.setVelY = None
        self.addVelX = None
        self.addVelY = None
        self.setVelYIfDrop = None
        self.ignoreSpeedCap = False
        self.ignoreFriction = False
        self.resetHitPotential = False
        self.buildHurtboxes(hurtboxData)
        self.buildHitboxes(hitboxData)

    def buildHurtboxes(self, data):
        self.hurtboxes = []

        for d in data:
            topleft = (d[0], d[1])
            width = d[2] - d[0]
            height = d[3] - d[1]
            size = (width, height)
            rect = pygame.Rect(topleft, size)
            self.hurtboxes.append(hurtbox.Hurtbox(rect))

    def buildHitboxes(self, data):
        self.hitboxes = []

        for d in data:
            topleft = (d[0], d[1])
            width = d[2] - d[0]
            height = d[3] - d[1]
            size = (width, height)
            rect = pygame.Rect(topleft, size)
            damage = d[4]
            stun = d[5]
            knockback = d[6]
            angle = d[7]
            properties = d[8]
            freezeFrame = d[9]
            self.hitboxes.append(hitbox.Hitbox(rect, damage, stun, knockback,
                                               angle, properties, freezeFrame))

class Transition(object):
    def __init__(self, var1, var2, rangeMin, rangeMax, dest):
        self.var1 = var1
        self.var2 = var2
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.destination = dest
        

def baseIdle():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')],
          ['doDash', Transition(None, None, None, None, 'dash')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['doDuck', Transition(None, None, None, None, 'ducking')],
          ['attackAUp', Transition(None, None, None, None, 'upA')],
          ['attackBUp', Transition(None, None, None, None, 'upB')],
          ['attackA', Transition(None, None, None, None, 'jabA')],
          ['attackB', Transition(None, None, None, None, 'jabB')]]
    m = Move([], t)
    m.canDI = False
    return m
    
def baseDash():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'dash')],
          ['noXMove', Transition(None, None, None, None, 'idle')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['doDuck', Transition(None, None, None, None, 'ducking')],
          ['attackAUp', Transition(None, None, None, None, 'upA')],
          ['attackBUp', Transition(None, None, None, None, 'upB')],
          ['attackA', Transition(None, None, None, None, 'dashAttackA')],
          ['attackB', Transition(None, None, None, None, 'dashAttackB')] ]
    m = Move([], t)
    return m

def baseAir():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'air')],
          ['land', Transition(None, None, None, None, 'landing')],
          ['attackA', Transition(None, None, None, None, 'neutralAirA')],
          ['attackB', Transition(None, None, None, None, 'neutralAirB')],
          ['attackAUp', Transition(None, None, None, None, 'upAirA')],
          ['attackBUpCharge', Transition(None, None, None, None, 'upAirB')],
          ['attackADown', Transition(None, None, None, None, 'downAirA')],
          ['attackBDown', Transition(None, None, None, None, 'downAirB')]]
    m = Move([], t)
    return m

def baseLanding():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')] ]
    m = Move([], t)
    m.canDI = False
    return m

def baseJumping():
    m = Move([], [])
    m.canDI = False
    m.isJump = True
    return m

def baseDucking():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'ducking')],
          ['stopDuck', Transition(None, None, None, None, 'idle')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['attackADown', Transition(None, None, None, None, 'downA')],
          ['attackBDown', Transition(None, None, None, None, 'downB')] ]
    m = Move([], t)
    m.canDI = False
    return m

def baseStun():
    m = Move([], [])
    m.canDI = False
    m.isStun = True
    return m

def baseBlank():
    m = Move([], [])
    return m

def baseProjFlying():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'flying')] ]
    m = Move([], t)
    return m
