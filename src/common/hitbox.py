from common.constants import *

class Hitbox(object):
    def __init__(self, inRect, damage, stun, knockback, angle, properties,
                 freezeFrame, chipDamagePercentage):

        self.rect = inRect
        self.damage = damage
        self.stun = stun
        self.knockback = knockback
        self.angle = angle
        self.properties = properties
        self.freezeFrame = freezeFrame
        self.chipDamagePercentage = chipDamagePercentage

    def ignoreBlock(self):
        for p in self.properties:
            if p[0] == P_GRAB or p[0] == P_UNBLOCKABLE:
                return True
        return False

    def untechable(self):
        for p in self.properties:
            if p[0] == P_UNTECHABLE:
                return True
        return False

    def getGrabData(self):
        for p in self.properties:
            if p[0] == P_GRAB:
                return p
        return None

    def reverseUserFacing(self):
        for p in self.properties:
            if p[0] == P_REVERSE_FACING:
                return p[1]
        return False

    def reverseTargetFacing(self):
        for p in self.properties:
            if p[0] == P_REVERSE_FACING:
                return p[2]
        return False

    def noStandardFX(self):
        for p in self.properties:
            if p[0] == P_FX:
                if p[1] is None:
                    return True
        return False
