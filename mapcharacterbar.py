import os
import sys
import pygame
import copy

import mapinterfaceitem

from constants import *

class MapCharacterBar(mapinterfaceitem.MapInterfaceItem):
    def __init__(self, inPos, inChar):
        super(MapCharacterBar, self).__init__()

        self.character = inChar

        team = self.character.team
        b = MAP_CHAR_BAR_BORDER
        p = MAP_CHAR_BAR_PADDING
        height = (MAP_CHAR_BAR_PORTRAIT_SIZE[0] + (b * 2) + (p * 2))
        width = (MAP_CHAR_BAR_PORTRAIT_SIZE[1] + (b * 2) + (p * 2))

        self.rect = pygame.Rect(inPos, (width, height))

        staticSurface = pygame.Surface((width, height))
        staticSurface.fill(MAP_CHAR_BAR_COLOR_BORDER[team])
        staticSurface.fill(MAP_CHAR_BAR_COLOR_BG[team],
                                pygame.Rect((b, b),
                                            (width - (b*2), height - (b*2))))

        staticSurface = staticSurface.convert()

        self.staticSurfaces = []
        for i in range(2):
            self.staticSurfaces.append(copy.copy(staticSurface))

        colorSwap(self.staticSurfaces[1], MAP_CHAR_BAR_COLOR_BORDER[team],
                  MAP_CHAR_BAR_COLOR_SELECTED, 5)

                
        self.setActive(False)

    def setActive(self, val):
        if val:
            num = 1
        else:
            num = 0

        self.static = self.staticSurfaces[num]

    def draw(self, screen):
        print self.image, self.static
        self.image = self.static
        print self.image
        
        super(MapCharacterBar, self).draw(screen)
