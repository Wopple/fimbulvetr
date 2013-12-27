import os
import sys
import pygame
import copy

import textrect
import energybar

import battle_v

from common.constants import *
from client.constants import *

from common.util.rect import Rect

class UnitHUD(object):
    def __init__(self, inTeam, inPlayers):
        self.rect = Rect((0,0), (SCREEN_SIZE[0], UNIT_HUD_HEIGHT))
        self.rect.bottom = SCREEN_SIZE[1]
        self.team = inTeam
        
        self.characters = inPlayers[self.team]

        self.buttonBorderVertLight = pygame.Surface((UNIT_HUD_BUTTON_BORDER_SIZE,
                                               UNIT_HUD_BUTTON_SIZE[1]))
        self.buttonBorderVertLight.fill(UNIT_HUD_BUTTON_COLORS_LIGHT_BORDER[self.team])

        self.buttonBorderVertDark = pygame.Surface((UNIT_HUD_BUTTON_BORDER_SIZE,
                                               UNIT_HUD_BUTTON_SIZE[1]))
        self.buttonBorderVertDark.fill(UNIT_HUD_BUTTON_COLORS_DARK_BORDER[self.team])

        self.buttonBorderHorizLight = pygame.Surface((UNIT_HUD_BUTTON_SIZE[0],
                                                UNIT_HUD_BUTTON_BORDER_SIZE))
        self.buttonBorderHorizLight.fill(UNIT_HUD_BUTTON_COLORS_LIGHT_BORDER[self.team])

        self.buttonBorderHorizDark = pygame.Surface((UNIT_HUD_BUTTON_SIZE[0],
                                                UNIT_HUD_BUTTON_BORDER_SIZE))
        self.buttonBorderHorizDark.fill(UNIT_HUD_BUTTON_COLORS_DARK_BORDER[self.team])
        
        self.blankPortrait = pygame.Surface(UNIT_HUD_PORTRAIT_SIZE)
        self.blankPortrait.fill(UNIT_HUD_BLANK_PORTRAIT_COLORS[self.team])
        
        self.portraitBase = pygame.Surface( (UNIT_HUD_PORTRAIT_SIZE[0] + (UNIT_HUD_PORTRAIT_BORDER_SIZE * 2),
                                             UNIT_HUD_PORTRAIT_SIZE[1] + (UNIT_HUD_PORTRAIT_BORDER_SIZE * 2)))
        self.portraitBase.fill(UNIT_HUD_PORTRAIT_BORDER_COLORS[self.team])
        
        x = ( (UNIT_HUD_BORDER_WIDTH * 4) + (UNIT_HUD_BUTTON_SIZE[0] * 2) + 
        (UNIT_HUD_PORTRAIT_BORDER_SIZE * 2) + UNIT_HUD_PORTRAIT_SIZE[0] )
        y = UNIT_HUD_BORDER_WIDTH
        self.healthBarRect = Rect((x, y), UNIT_HUD_ENERGY_BAR_SIZE)
        y += UNIT_HUD_BORDER_WIDTH + self.healthBarRect.height + ENERGY_BAR_FONT.get_height() - 4
        self.superBarRect = Rect((x, y), UNIT_HUD_ENERGY_BAR_SIZE)
        
        sizeX = SCREEN_SIZE[0] - self.healthBarRect.left - UNIT_HUD_BORDER_WIDTH
        sizeY = UNIT_HUD_STRUCTURE_PANEL_HEIGHT
        self.structureCountPanelRect = Rect( (0, 0), (sizeX, sizeY))
        self.structureCountPanelRect.left = self.healthBarRect.left
        self.structureCountPanelRect.bottom = UNIT_HUD_HEIGHT - UNIT_HUD_BORDER_WIDTH
        
        self.fortressIcon = FORTRESS_COUNT_ICONS[self.team]
        self.fortressIconRect = Rect( (0,0), self.fortressIcon.get_size() )
        self.fortressIconRect.centery = (self.structureCountPanelRect.height / 2)
        
        self.altarIcon = ALTAR_COUNT_ICONS[self.team]
        self.altarIconRect = Rect( (0,0), self.altarIcon.get_size() )
        self.altarIconRect.left = UNIT_HUD_STRUCTURE_PANEL_SPACING
        self.altarIconRect.centery = (self.structureCountPanelRect.height / 2)
        
        self.spireIcon = SPIRE_COUNT_ICONS[self.team]
        self.spireIconRect = Rect( (0,0), self.spireIcon.get_size() )
        self.spireIconRect.left = UNIT_HUD_STRUCTURE_PANEL_SPACING * 2
        self.spireIconRect.centery = (self.structureCountPanelRect.height / 2)
        
        
        
        self.iconRect = Rect((0,0), EFFECT_ICON_SIZE)
        self.iconRect.top = self.healthBarRect.top
        self.iconRect.left = self.healthBarRect.right + UNIT_HUD_BORDER_WIDTH
        
        
        
        self.damageTagRect = Rect((0, 0), (80, 100))
        self.damageTagRect.right = self.rect.width
        self.damageTagRect.top = self.rect.height - 55
        self.damageTag = textrect.render_textrect("Strength", STRUCTURE_COUNT_FONT, self.damageTagRect,
                                                  ALMOST_BLACK, BLACK, 1, True)
        
        self.damagePercentRect = Rect((0, 0), (80, 100))
        self.damagePercentRect.right = self.damageTagRect.right
        self.damagePercentRect.top = self.damageTagRect.top + 18
        

        self.createCharacterButtons()
        self.createTerrainIcons()
        
        self.currCharacter = None
        self.healthBar = None
        self.superBar = None
        self.createBaseImage()
        
        self.createTerritoryIcons()
        self.createSuperIcons()
        self.updateStructureCount(0, 0, 0)
        
    def update(self, val):
        self.changeCharacter(val)
        self.everyFrameUpdate()


    def changeCharacter(self, val):
        
        if self.currCharacter != val:
            self.currCharacter = val
            self.createBaseImage()
            
            if not self.currCharacter is None:
                self.healthBar = energybar.EnergyBar(self.currCharacter.battleChar.hp, self.healthBarRect,
                                                     (UNIT_HUD_ENERGY_BAR_BORDER_SIZE, UNIT_HUD_ENERGY_BAR_BORDER_SIZE),
                                                     HEALTH_BAR_COLORS, 2,
                                                     self.currCharacter.name, None, 0)
                self.superBar = energybar.EnergyBar(self.currCharacter.battleChar.superEnergy, self.superBarRect,
                                                    (UNIT_HUD_ENERGY_BAR_BORDER_SIZE, UNIT_HUD_ENERGY_BAR_BORDER_SIZE),
                                                    SUPER_BAR_COLORS, 2,
                                                    "Energy", None, 0)
                self.healthBar.rect.topleft = self.healthBarRect.topleft
                self.superBar.rect.topleft = self.superBarRect.topleft
            else:
                self.healthBar = None
                self.superBar = None

    def createCharacterButtons(self):

        self.buttons = []
        self.buttonRects = []
        self.buttonBars = []
        
        for i, c in enumerate(self.characters):
            tempList = []
            for j in range(2):
                isOn = (j == 0)
                tempList.append(self.createButton(i, c, isOn))
            self.buttons.append(tempList)
            

    def createButton(self, val, character, isOn):

        faceColorOn = UNIT_HUD_BUTTON_COLORS_FACE_ON[self.team]
        faceColorOff = faceColorOn = UNIT_HUD_BUTTON_COLORS_FACE_OFF[self.team]
        if isOn:
            faceColor = faceColorOn
            borderTop = self.buttonBorderHorizDark
            borderLeft = self.buttonBorderVertDark
            borderBottom = self.buttonBorderHorizLight
            borderRight = self.buttonBorderVertLight
        else:
            faceColor = faceColorOff
            borderTop = self.buttonBorderHorizLight
            borderLeft = self.buttonBorderVertLight
            borderBottom = self.buttonBorderHorizDark
            borderRight = self.buttonBorderVertDark

        button = pygame.Surface(UNIT_HUD_BUTTON_SIZE)
        button.fill(faceColor)

        button.blit(borderTop, (0, 0))
        button.blit(borderLeft, (0, 0))
        button.blit(borderBottom, (0, UNIT_HUD_BUTTON_SIZE[1] -
                                   UNIT_HUD_BUTTON_BORDER_SIZE))
        button.blit(borderRight, (UNIT_HUD_BUTTON_SIZE[0] -
                                   UNIT_HUD_BUTTON_BORDER_SIZE, 0))
        
        textRect = Rect( (UNIT_HUD_BUTTON_BORDER_SIZE, 
                          UNIT_HUD_BUTTON_BORDER_SIZE),
                         (UNIT_HUD_BUTTON_SIZE[0] - (UNIT_HUD_BUTTON_BORDER_SIZE * 2),
                          UNIT_HUD_BUTTON_SIZE[1] - (UNIT_HUD_BUTTON_BORDER_SIZE * 2)) )
        
        textSurface = textrect.render_textrect(character.name, UNIT_HUD_NAMES_FONT, textRect,
                                               ALMOST_BLACK, BLACK, 1, True)
        
        button.blit(textSurface, textRect.topleft)
        
        textSurface = textrect.render_textrect(str(val+1) + ".", UNIT_HUD_NAMES_FONT, textRect,
                                               ALMOST_BLACK, BLACK, 0, True)
        
        button.blit(textSurface, textRect.topleft)
        
        numPerColumn = int(len(self.characters) / 2) + 1
        if numPerColumn > UNIT_HUD_BUTTONS_PER_COLUMN:
            numPerColumn = UNIT_HUD_BUTTONS_PER_COLUMN
        
        if isOn:
            #Rect
            column = int (val / numPerColumn)
            row = val % numPerColumn
            
            x = ((UNIT_HUD_BUTTON_SIZE[0] + UNIT_HUD_BORDER_WIDTH) * column) + UNIT_HUD_BORDER_WIDTH
            y = ((UNIT_HUD_BUTTON_SIZE[1] + UNIT_HUD_BORDER_WIDTH) * row) + UNIT_HUD_BORDER_WIDTH
        
            buttonRect = Rect((x, y), UNIT_HUD_BUTTON_SIZE)
            self.buttonRects.append(Rect(buttonRect))
            
            #Bar
            sizeX = UNIT_HUD_BUTTON_SIZE[0] - (UNIT_HUD_BUTTON_BORDER_SIZE * 2)
            sizeY = 2
            x = buttonRect.left + UNIT_HUD_BUTTON_BORDER_SIZE
            y = buttonRect.bottom - UNIT_HUD_BUTTON_BORDER_SIZE - 4
            barRect = Rect((x, y), (sizeX, sizeY))
            newBar = energybar.EnergyBar(character.battleChar.hp, barRect, (0, 0), HEALTH_BAR_COLORS, 2)
            self.buttonBars.append(newBar)
            
            

        return button
    
    def createTerritoryIcons(self):
        if self.team == 0:
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

    
    def createTerrainIcons(self):
        
        self.terrainEffectIcons = []
        
        for c in self.characters:
        
            tempList = []

            for i in range(7):
                terrainIcon = TERRAIN_ICONS[i]

                effect = c.speedTerrainModifiers[i]

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

                tempList.append(icon)
            
                self.terrainEffectIcons.append(tempList)
                
    def createSuperIcons(self):
        self.superIcons = []
        
        x = self.iconRect.left
        y = self.iconRect.top + self.iconRect.height + UNIT_HUD_BORDER_WIDTH
        
        for c in self.characters:
            icon = battle_v.SuperIcon(Rect((x, y), BATTLE_SUPER_ICON_SIZE),
                                      c.battleChar.getSuperIcon(), c.battleChar.superEnergy)
            
            self.superIcons.append(icon)

    def createBaseImage(self):
        self.baseImage = pygame.Surface(self.rect.size)
        color = UNIT_HUD_COLORS[self.team]
        
        self.baseImage.fill(color)

        
        for i, c in enumerate(self.characters):
            
            if self.currCharacter == c:
                onIndex = 0
            else:
                onIndex = 1
            
            
            self.baseImage.blit(self.buttons[i][onIndex], self.buttonRects[i].topleft)
            
        x = ((UNIT_HUD_BUTTON_SIZE[0] + UNIT_HUD_BORDER_WIDTH) * 2) + UNIT_HUD_BORDER_WIDTH
        y = UNIT_HUD_BORDER_WIDTH
        
        if self.currCharacter is None:
            portrait = self.blankPortrait
        else:
            portrait = self.currCharacter.portrait
            
        finalPortrait = pygame.Surface( (UNIT_HUD_PORTRAIT_SIZE[0] + (UNIT_HUD_PORTRAIT_BORDER_SIZE * 2),
                                             UNIT_HUD_PORTRAIT_SIZE[1] + (UNIT_HUD_PORTRAIT_BORDER_SIZE * 2)) )
        
        finalPortrait.blit(self.portraitBase, (0,0))
        finalPortrait.blit(portrait, (UNIT_HUD_PORTRAIT_BORDER_SIZE, UNIT_HUD_PORTRAIT_BORDER_SIZE))
        
        self.baseImage.blit(finalPortrait, (x, y))
        
    def everyFrameUpdate(self):
        
        self.image = pygame.Surface(self.rect.size)
        
        self.image.blit(self.baseImage, (0, 0))
        
        if (not self.healthBar is None):
            self.healthBar.update()
            self.healthBar.draw(self.image)
            if (not self.currCharacter is None):
                if self.currCharacter.isDead():
                    if self.healthBar.value != self.currCharacter.respawnTime:
                        self.healthBar.value = self.currCharacter.respawnTime
                        self.healthBar.threshold = self.healthBar.value.maximum
                        self.healthBar.changeColor(RESPAWN_BAR_COLOR)
                        self.healthBar.changeFullColors(RESPAWN_BAR_COLOR, RESPAWN_BAR_COLOR)
                else:
                    if self.healthBar.value != self.currCharacter.battleChar.hp:
                        self.healthBar.value = self.currCharacter.battleChar.hp
                        self.healthBar.threshold = self.healthBar.value.maximum
                        self.healthBar.changeColor(HEALTH_BAR_COLORS[0])
                        self.healthBar.changeFullColors(HEALTH_BAR_COLORS[1], HEALTH_BAR_COLORS[2])
             
            
        if (not self.superBar is None):
            self.superBar.update()
            self.superBar.draw(self.image)
            
        for i, b in enumerate(self.buttonBars):
            b.update()
            b.draw(self.image)
            c = self.characters[i]
            if c.isDead():
                if b.value != c.respawnTime:
                    b.value = c.respawnTime
                    b.threshold = b.value.maximum
                    b.changeColor(RESPAWN_BAR_COLOR)
                    b.changeFullColors(RESPAWN_BAR_COLOR, RESPAWN_BAR_COLOR)
            else:
                if b.value != c.battleChar.hp:
                    b.value = c.battleChar.hp
                    b.threshold = b.value.maximum
                    b.changeColor(HEALTH_BAR_COLORS[0])
                    b.changeFullColors(HEALTH_BAR_COLORS[1], HEALTH_BAR_COLORS[2])
            
        terrainIcon = None
        territoryIcon = None
        superIcon = None
        for i, c in enumerate(self.characters):
            if c == self.currCharacter:
                if c.isDead():
                    terrainIcon = NEUTRAL_ICON
                    territoryIcon = NEUTRAL_ICON
                else:
                    terrainIcon = self.terrainEffectIcons[i][self.currCharacter.currTerrain]
                    territoryIcon = self.territoryEffectIcons[self.currCharacter.currTerritory]
                superIcon = self.superIcons[i]
                break
            
        if not terrainIcon is None:
            self.image.blit(terrainIcon, self.iconRect.topleft)
            
        x = self.iconRect.right
        y = self.iconRect.top
            
        if not territoryIcon is None:
            self.image.blit(territoryIcon, (x, y))
            
        if not superIcon is None:
            superIcon.updateImage()
            superIcon.draw(self.image)
            
            
        self.image.blit(self.structureCountPanel, self.structureCountPanelRect.topleft)
        
        self.updateDamagePercent()
        
    def updateDamagePercent(self):
        if (not self.currCharacter is None):
            if not self.currCharacter.isDead():
                self.image.blit(self.damageTag, self.damageTagRect.topleft)
                
                textSurface = textrect.render_textrect(self.currCharacter.getDamagePercentText(), DAMAGE_PERCENT_FONT, self.damagePercentRect,
                                                 ALMOST_BLACK, BLACK, 1, True)
                self.image.blit(textSurface, self.damagePercentRect.topleft)
            
    def updateStructureCount(self, fortressCount, spireCount, altarCount):
        self.fortressCount = fortressCount
        self.spireCount = spireCount
        self.altarCount = altarCount
        
        self.structureCountPanel = pygame.Surface(self.structureCountPanelRect.size)
        self.structureCountPanel.fill(UNIT_HUD_COLORS[self.team])
        
        self.structureCountPanel.blit(self.fortressIcon, self.fortressIconRect.topleft)
        self.structureCountPanel.blit(self.spireIcon, self.spireIconRect.topleft)
        self.structureCountPanel.blit(self.altarIcon, self.altarIconRect.topleft)
        
        textRect = Rect((0,0), (100, STRUCTURE_COUNT_FONT.get_height() + 4))
        
        textSurface = textrect.render_textrect(" x" + str(self.fortressCount), STRUCTURE_COUNT_FONT, textRect,
                                               ALMOST_BLACK, BLACK, 0, True)
        textRect.bottomleft = self.fortressIconRect.bottomright
        self.structureCountPanel.blit(textSurface, textRect.topleft)
        
        
        textSurface = textrect.render_textrect(" x" + str(self.spireCount), STRUCTURE_COUNT_FONT, textRect,
                                               ALMOST_BLACK, BLACK, 0, True)
        textRect.left = self.spireIconRect.right - 3
        self.structureCountPanel.blit(textSurface, textRect.topleft)
        
        textSurface = textrect.render_textrect(" x" + str(self.altarCount), STRUCTURE_COUNT_FONT, textRect,
                                               ALMOST_BLACK, BLACK, 0, True)
        textRect.left = self.altarIconRect.right - 3
        self.structureCountPanel.blit(textSurface, textRect.topleft)
        
        
        
        
            
            
    def getButtonAtPos(self, inPos):
        pos = [inPos[0] - self.rect.left, inPos[1] - self.rect.top]
        
        for i, r in enumerate(self.buttonRects):
            if r.collidepoint(pos):
                return self.characters[i]
            
        return None
            
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        
