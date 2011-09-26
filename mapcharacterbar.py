import os
import sys
import pygame
import copy

import mapinterfaceitem
import energybar
import boundint

from constants import *

class MapCharacterBar(mapinterfaceitem.MapInterfaceItem):
    
    def __init__(self, inPos, inChar):
        super(MapCharacterBar, self).__init__()

        self.character = inChar

        self.createEffectIcons()

        team = self.character.team
        b = MAP_CHAR_BAR_BORDER
        p = MAP_CHAR_BAR_PADDING
        ps = MAP_CHAR_BAR_PADDING_SMALL
        height = (MAP_CHAR_BAR_PORTRAIT_SIZE[1] + (b * 2) + (p * 2))
        width = (MAP_CHAR_BAR_PORTRAIT_SIZE[0] + (b * 2) + (p * 4)
                 + MAP_CHAR_BAR_ENERGY_BAR_SIZE[0] + EFFECT_ICON_SIZE[0])

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

        for s in self.staticSurfaces:
            s.blit(self.character.portrait, ((b+p), (b+p)))


        tempVal = boundint.BoundInt(0, SUPER_ENERGY_MAX,
                                    self.character.getSuperEnergy())
        x = (b + (p*2) + MAP_CHAR_BAR_PORTRAIT_SIZE[0])
        y = (b + p + MAP_CHAR_BAR_PORTRAIT_SIZE[1]
             - MAP_CHAR_BAR_ENERGY_BAR_SIZE[1])
        tempRect = pygame.Rect((x, y), MAP_CHAR_BAR_ENERGY_BAR_SIZE)
        self.superBar = energybar.EnergyBar(tempVal, tempRect,
                                             MAP_CHAR_BAR_ENERGY_BAR_BORDERS,
                                             SUPER_BAR_COLORS, 2)

        tempVal = boundint.BoundInt(0, self.character.getMaxHP(),
                                    self.character.getHP())
        y = y - ps - MAP_CHAR_BAR_ENERGY_BAR_SIZE[1]
        tempRect = pygame.Rect((x, y), MAP_CHAR_BAR_ENERGY_BAR_SIZE)
        self.healthBar = energybar.EnergyBar(self.character.battleChar.hp, tempRect,
                                             MAP_CHAR_BAR_ENERGY_BAR_BORDERS,
                                             HEALTH_BAR_COLORS, 2,
                                             self.character.name, None, 3)

        self.setActive(False)

        self.pastHP = -1
        self.pastSuperEnergy = -1

    def update(self):
        self.remakeImage()

        super(MapCharacterBar, self).update()

    def setActive(self, val):
        if val:
            num = 1
        else:
            num = 0

        self.static = self.staticSurfaces[num]

        self.remakeImage()

    def remakeImage(self):
        self.image = pygame.Surface.copy(self.static)
        self.healthBar.update()
        self.healthBar.draw(self.image)
        self.superBar.update()
        self.superBar.draw(self.image)
        self.drawEffectIcons(self.image)
        self.image.set_alpha(self.alpha.value)


    def createEffectIcons(self):
        if self.character.team == 0:
            alliedTeam = 1
            enemyTeam = 2
        else:
            alliedTeam = 2
            enemyTeam = 1
        contested = 0

        options = ["neutral", "allied", "enemy", "contested"]

        self.territoryEffectIcons = {}

        bgColor = None
        flagColor = None
        
        for o in options:
            flag = copy.copy(INTERFACE_GRAPHICS[5])
        
            if o == "allied":
                flagColor = TERRITORY_FLAG_COLORS[alliedTeam]
                bgColor = EFFECT_COLORS["good"]
            elif o == "enemy":
                flagColor = TERRITORY_FLAG_COLORS[enemyTeam]
                bgColor = EFFECT_COLORS["bad"]
            elif o == "contested":
                flagColor = TERRITORY_FLAG_COLORS[contested]
                bgColor = EFFECT_COLORS["bad"]
            else:
                flag = None
                bgColor = EFFECT_COLORS["neutral"]

            icon = pygame.Surface(EFFECT_ICON_SIZE)
            icon.fill(bgColor)


            if not flag is None:
                colorSwap(flag, FLAG_NEUTRAL_COLOR, flagColor, 30)
                icon.blit(flag, (0,0))

            self.territoryEffectIcons[o] = icon


    def drawEffectIcons(self, image):

        self.drawTerritoryIcon(image)


    def drawTerritoryIcon(self, image):

        icon = self.territoryEffectIcons[self.character.currTerritory]

        x = (self.rect.width - MAP_CHAR_BAR_BORDER - MAP_CHAR_BAR_PADDING -
             EFFECT_ICON_SIZE[0])
        y = MAP_CHAR_BAR_BORDER + MAP_CHAR_BAR_PADDING

        image.blit(icon, (x, y))
            
