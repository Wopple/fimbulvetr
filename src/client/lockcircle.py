import os
import sys
import pygame
import copy
import math

from common.constants import *

class LockCircle:

    def __init__(self, pos, team):
        self.pos = [int(pos[0]), int(pos[1])]
        self.tick = LOCK_CIRCLE_TICK_MAX
        self.size = 1
        self.team = team
        
    def update(self):
        self.tick += 1
        if self.tick >= LOCK_CIRCLE_TICK_MAX:
            self.tick = 0
            self.size += LOCK_CIRCLE_INCREASE
            
        
    def isRemovable(self):
        return (self.size >= LOCK_CIRCLE_MAX_SIZE)
    
    def draw(self, screen, inZoom, inOffset):

        pos = ( int((self.pos[0] * inZoom) + inOffset[0]),
                int((self.pos[1] * inZoom) + inOffset[1]) )

        color = TERRITORY_DOT_COLORS[self.team]

        pygame.draw.circle(screen, color, pos, self.size, 2)
