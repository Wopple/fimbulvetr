import os
import sys
import pygame
import copy

import textrect
import energybar

import battle_m

from constants import *

class UnitHUD(object):
    def __init__(self, inTeam, inPlayers):
        self.rect = pygame.Rect((0,0), (SCREEN_SIZE[0], UNIT_HUD_HEIGHT))
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
        self.healthBarRect = pygame.Rect((x, y), UNIT_HUD_ENERGY_BAR_SIZE)
        y += UNIT_HUD_BORDER_WIDTH + self.healthBarRect.height + ENERGY_BAR_FONT.get_height() - 4
        self.superBarRect = pygame.Rect((x, y), UNIT_HUD_ENERGY_BAR_SIZE)
        
        self.iconRect = pygame.Rect((0,0), EFFECT_ICON_SIZE)
        self.iconRect.top = self.healthBarRect.top
        self.iconRect.left = self.healthBarRect.right + UNIT_HUD_BORDER_WIDTH
        

        self.createCharacterButtons()
        self.createTerrainIcons()
        
        self.currCharacter = None
        self.healthBar = None
        self.superBar = None
        self.createBaseImage()
        
        self.createTerritoryIcons()
        
        self.createSuperIcons()
        
    def update(self, val):
        self.changeCharacter(val)
        self.characterSpecificUpdate()


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
        
        textRect = pygame.Rect( (UNIT_HUD_BUTTON_BORDER_SIZE, 
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
            column = int (val / numPerColumn)
            row = val % numPerColumn
            
            x = ((UNIT_HUD_BUTTON_SIZE[0] + UNIT_HUD_BORDER_WIDTH) * column) + UNIT_HUD_BORDER_WIDTH
            y = ((UNIT_HUD_BUTTON_SIZE[1] + UNIT_HUD_BORDER_WIDTH) * row) + UNIT_HUD_BORDER_WIDTH
        
            self.buttonRects.append(pygame.Rect((x, y), UNIT_HUD_BUTTON_SIZE))

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

            for i in range(5):
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
            icon = battle_m.SuperIcon(pygame.Rect((x, y), BATTLE_SUPER_ICON_SIZE),
                                      c.battleChar.getSuperIcon(), c.battleChar.superEnergy)
            
            self.superIcons.append(icon)

    def createBaseImage(self):
        self.baseImage = pygame.Surface(self.rect.size)
        color = UNIT_HUD_COLORS[self.team]
        
        self.baseImage.fill(color)
        
        print self.buttonRects

        
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
        
    def characterSpecificUpdate(self):
        
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
        
            
            
    def getButtonAtPos(self, inPos):
        pos = [inPos[0] - self.rect.left, inPos[1] - self.rect.top]
        
        print pos
        
        for i, r in enumerate(self.buttonRects):
            if r.collidepoint(pos):
                return self.characters[i]
            
        return None
            
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        
