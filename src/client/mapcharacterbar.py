import os
import sys
import pygame
import copy

import mapinterfaceitem
import energybar
import boundint

from common.constants import *
from client.constants import *

from common.util.rect import Rect

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

        self.rect = Rect(inPos, (width, height))

        staticSurface = pygame.Surface((width, height))
        staticSurface.fill(MAP_CHAR_BAR_COLOR_BORDER[team])
        staticSurface.fill(MAP_CHAR_BAR_COLOR_BG[team],
                                Rect((b, b),
                                     (width - (b*2), height - (b*2))))

        staticSurface = staticSurface.convert()

        self.staticSurfaces = []
        for i in range(2):
            self.staticSurfaces.append(copy.copy(staticSurface))

        colorSwap(self.staticSurfaces[1], MAP_CHAR_BAR_COLOR_BORDER[team],
                  MAP_CHAR_BAR_COLOR_SELECTED, 5)

        for s in self.staticSurfaces:
            s.blit(self.character.portrait, ((b+p), (b+p)))



        x = (b + (p*2) + MAP_CHAR_BAR_PORTRAIT_SIZE[0])
        y = (b + p + MAP_CHAR_BAR_PORTRAIT_SIZE[1]
             - MAP_CHAR_BAR_ENERGY_BAR_SIZE[1])
        tempRect = Rect((x, y), MAP_CHAR_BAR_ENERGY_BAR_SIZE)
        self.superBar = energybar.EnergyBar(self.character.battleChar.superEnergy, tempRect,
                                             MAP_CHAR_BAR_ENERGY_BAR_BORDERS,
                                             SUPER_BAR_COLORS, 2)

        y = y - ps - MAP_CHAR_BAR_ENERGY_BAR_SIZE[1]
        tempRect = Rect((x, y), MAP_CHAR_BAR_ENERGY_BAR_SIZE)
        self.healthBar = energybar.EnergyBar(self.character.battleChar.hp, tempRect,
                                             MAP_CHAR_BAR_ENERGY_BAR_BORDERS,
                                             HEALTH_BAR_COLORS, 2,
                                             self.character.name, None, 3)

        self.setActive(False)

        self.pastHP = -1
        self.pastSuperEnergy = -1

    def update(self):
        if self.character.isDead():
            if self.healthBar.value != self.character.respawnTime:
                self.healthBar.value = self.character.respawnTime
                self.healthBar.threshold = self.healthBar.value.maximum
                self.healthBar.changeColor(RESPAWN_BAR_COLOR)
                self.healthBar.changeFullColors(RESPAWN_BAR_COLOR, RESPAWN_BAR_COLOR)
        else:
            if self.healthBar.value != self.character.battleChar.hp:
                self.healthBar.value = self.character.battleChar.hp
                self.healthBar.threshold = self.healthBar.value.maximum
                self.healthBar.changeColor(HEALTH_BAR_COLORS[0])
                self.healthBar.changeFullColors(HEALTH_BAR_COLORS[1], HEALTH_BAR_COLORS[2])
        
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


        self.terrainEffectIcons = []

        for i in range(5):
            terrainIcon = TERRAIN_ICONS[i]

            effect = self.character.speedTerrainModifiers[i]

            if effect <= 0.99:
                bgColor = EFFECT_COLORS["bad"]
            elif effect >= 1.01:
                bgColor = EFFECT_COLORS["good"]
            else:
                bgColor = EFFECT_COLORS["neutral"]

            icon = pygame.Surface(EFFECT_ICON_SIZE)
            icon.fill(bgColor)

            if not terrainIcon is None:
                icon.blit(terrainIcon, (0,0))

            self.terrainEffectIcons.append(icon)


    def drawEffectIcons(self, image):

        self.drawTerrainIcon(image)
        self.drawTerritoryIcon(image)

    def drawTerrainIcon(self, image):
        if self.character.isDead():
            icon = NEUTRAL_ICON
        else:
            icon = self.terrainEffectIcons[self.character.currTerrain]

        x = (self.rect.width - MAP_CHAR_BAR_BORDER - MAP_CHAR_BAR_PADDING -
             EFFECT_ICON_SIZE[0])
        y = MAP_CHAR_BAR_BORDER + MAP_CHAR_BAR_PADDING

        image.blit(icon, (x, y))


    def drawTerritoryIcon(self, image):
        if self.character.isDead():
            icon = NEUTRAL_ICON
        else:
            icon = self.territoryEffectIcons[self.character.currTerritory]

        x = (self.rect.width - MAP_CHAR_BAR_BORDER - MAP_CHAR_BAR_PADDING -
             EFFECT_ICON_SIZE[0])
        y = (self.rect.height - MAP_CHAR_BAR_BORDER - MAP_CHAR_BAR_PADDING -
             EFFECT_ICON_SIZE[1])

        image.blit(icon, (x, y))
            
