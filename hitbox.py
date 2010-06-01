import os
import sys
import pygame
import copy

from constants import *

class Hitbox(object):
    def __init__(self, inRect, damage, stun, knockback, angle, properties,
                 hitstunSelf = DEFAULT_HITSTUN, hitstunTarget = DEFAULT_HITSTUN):

        self.rect = inRect
        self.damage = damage
        self.stun = stun
        self.knockback = knockback
        self.angle = angle
        self.properties = properties
        self.hitstunSelf = hitstunSelf
        self.hitstunTarget = hitstunTarget

        self.image = pygame.Surface(self.rect.size)
        self.image.fill(HITBOX_COLOR)
        self.image.set_alpha(HITBOX_ALPHA)
