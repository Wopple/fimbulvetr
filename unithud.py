import os
import sys
import pygame
import copy

import textrect

from constants import *

class UnitHUD(object):
    def __init__(self, inTeam, inPlayers):
        self.rect = pygame.Rect((0,0), (SCREEN_SIZE[0], UNIT_HUD_HEIGHT))
        self.rect.bottom = SCREEN_SIZE[1]
        self.team = inTeam
        self.characters = inPlayers[self.team]

        self.borderVertLight = pygame.Surface((UNIT_HUD_BUTTON_BORDER_SIZE,
                                               UNIT_HUD_BUTTON_SIZE[1]))
        self.borderVertLight.fill(UNIT_HUD_BUTTON_COLORS_LIGHT_BORDER[self.team])

        self.borderVertDark = pygame.Surface((UNIT_HUD_BUTTON_BORDER_SIZE,
                                               UNIT_HUD_BUTTON_SIZE[1]))
        self.borderVertDark.fill(UNIT_HUD_BUTTON_COLORS_DARK_BORDER[self.team])

        self.borderHorizLight = pygame.Surface((UNIT_HUD_BUTTON_SIZE[0],
                                                UNIT_HUD_BUTTON_BORDER_SIZE))
        self.borderHorizLight.fill(UNIT_HUD_BUTTON_COLORS_LIGHT_BORDER[self.team])

        self.borderHorizDark = pygame.Surface((UNIT_HUD_BUTTON_SIZE[0],
                                                UNIT_HUD_BUTTON_BORDER_SIZE))
        self.borderHorizDark.fill(UNIT_HUD_BUTTON_COLORS_DARK_BORDER[self.team])
        
        self.blankPortrait = pygame.Surface(UNIT_HUD_PORTRAIT_SIZE)
        self.blankPortrait.fill(UNIT_HUD_BLANK_PORTRAIT_COLORS[self.team])

        self.createCharacterButtons()
        
        self.currCharacter = None
        self.createImage()


    def changeCharacter(self, val):
        
        if self.currCharacter != val:
            self.currCharacter = val
            self.createImage()

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
            borderTop = self.borderHorizDark
            borderLeft = self.borderVertDark
            borderBottom = self.borderHorizLight
            borderRight = self.borderVertLight
        else:
            faceColor = faceColorOff
            borderTop = self.borderHorizLight
            borderLeft = self.borderVertLight
            borderBottom = self.borderHorizDark
            borderRight = self.borderVertDark

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

    def createImage(self):
        self.image = pygame.Surface(self.rect.size)
        color = UNIT_HUD_COLORS[self.team]
        
        self.image.fill(color)
        
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
            
            self.image.blit(self.buttons[i][onIndex], (x, y))
            
        x = ((UNIT_HUD_BUTTON_SIZE[0] + UNIT_HUD_BORDER_WIDTH) * 2) + UNIT_HUD_BORDER_WIDTH
        y = UNIT_HUD_BORDER_WIDTH
        
        if self.currCharacter is None:
            portrait = self.blankPortrait
        else:
            portrait = self.currCharacter.portrait
        
        self.image.blit(portrait, (x, y))
        
        
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        
