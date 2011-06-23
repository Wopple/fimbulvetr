import os
import sys
import pygame
import copy

from constants import *

class Hitbox(object):
    def __init__(self, inRect, damage, stun, knockback, angle, properties,
                 freezeFrame):

        self.rect = inRect
        self.damage = damage
        self.stun = stun
        self.knockback = knockback
        self.angle = angle
        self.properties = properties
        self.freezeFrame = freezeFrame

        self.image = pygame.Surface(self.rect.size)
        self.image.fill(HITBOX_COLOR)
        self.image.set_alpha(HITBOX_ALPHA)

    def ignoreBlock(self):
        for p in self.properties:
            if p[0] == 'grab' or p[0] == 'unblockable':
                return True
        return False

    def untechable(self):
        for p in self.properties:
            if p[0] == 'untechable':
                return True
        return False

    def getGrabData(self):
        for p in self.properties:
            if p[0] == 'grab':
                return p
        return None

    def reverseUserFacing(self):
        for p in self.properties:
            if p[0] == 'reverseFacing':
                return p[1]
        return False

    def reverseTargetFacing(self):
        for p in self.properties:
            if p[0] == 'reverseFacing':
                return p[2]
        return False
