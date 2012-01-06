import os
import sys
import pygame
import copy

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

        self.createCharacterButtons()
        
        self.changeCharacter(0)


    def changeCharacter(self, val):

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

        return button

    def createImage(self):
        self.image = pygame.Surface(self.rect.size)
        color = UNIT_HUD_COLORS[self.team]
        
        self.image.fill(color)

        #for i, c in enumerate(self.characters):
            #self.image.blit(self.buttons[i][0], (0, 0))

        self.image.blit(self.buttons[0][0], (5, 5))
        self.image.blit(self.buttons[0][1], (5, 40))
        
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

        
