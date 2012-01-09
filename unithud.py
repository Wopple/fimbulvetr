import os
import sys
import pygame
import copy

import textrect
import energybar

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
        

        self.createCharacterButtons()
        
        self.currCharacter = None
        self.healthBar = None
        self.superBar = None
        self.createBaseImage()
        
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
                                                    HEALTH_BAR_COLORS, 2,
                                                    "Energy", None, 0)
                self.healthBar.rect.topleft = self.healthBarRect.topleft
                self.superBar.rect.topleft = self.superBarRect.topleft
            else:
                self.healthBar = None
                self.superBar = None

    def createCharacterButtons(self):

        self.buttons = []
        
        for i, c in enumerate(self.characters):
            tempList = []
            for i in range(2):
                isOn = (i == 0)
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
        
        

        return button

    def createBaseImage(self):
        self.baseImage = pygame.Surface(self.rect.size)
        color = UNIT_HUD_COLORS[self.team]
        
        self.baseImage.fill(color)
        
        numPerColumn = int(len(self.characters) / 2) + 1
        if numPerColumn > UNIT_HUD_BUTTONS_PER_COLUMN:
            numPerColumn = UNIT_HUD_BUTTONS_PER_COLUMN

        
        for i, c in enumerate(self.characters):
            
            if self.currCharacter == c:
                onIndex = 0
            else:
                onIndex = 1
            
            column = int (i / numPerColumn)
            row = i % numPerColumn
            
            x = ((UNIT_HUD_BUTTON_SIZE[0] + UNIT_HUD_BORDER_WIDTH) * column) + UNIT_HUD_BORDER_WIDTH
            y = ((UNIT_HUD_BUTTON_SIZE[1] + UNIT_HUD_BORDER_WIDTH) * row) + UNIT_HUD_BORDER_WIDTH
            
            self.baseImage.blit(self.buttons[i][onIndex], (x, y))
            
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
            self.healthBar.draw(self.image)
            if (not self.character is None):
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
                
            
        if (not self.superBar is None):
            self.superBar.draw(self.image)
            
        
        
        
        
        
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        
