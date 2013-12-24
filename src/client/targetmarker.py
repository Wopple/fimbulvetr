import os
import sys
import pygame

from common.constants import *
from client.constants import *

from common.util.rect import Rect

import drawable

class TargetMarker(object):
    def __init__(self, team, waypoint=False):
        if waypoint:
            self.image = INTERFACE_GRAPHICS[11]
        else:
            self.image = INTERFACE_GRAPHICS[2]
            
        colorSwap(self.image, (250, 250, 250, 255), TOKEN_BORDER_OFF[team], 200)
            
        self.rect = Rect((0, 0), self.image.get_size())

    def draw(self, screen, charPos, inZoom, inOffset):
        pos = [0, 0]
        for i in range(2):
            pos[i] = int(charPos[i] * inZoom) + inOffset[i]
        self.rect.center = (pos[0], pos[1])
        screen.blit(self.image, self.rect.topleft)
