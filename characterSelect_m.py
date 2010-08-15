import os
import sys
import pygame

import mvc

import math

from constants import *

class Model(mvc.Model):
    def __init__(self, theMap):
        super(Model, self).__init__()

        self.theMap = theMap

        self.openEditor = False

        self.bg = pygame.Surface(SCREEN_SIZE)
        self.bg.fill(CHARACTER_SELECT_BG_COLOR)

        self.group = CharacterPanelGroup(10)
        self.currSelected = None

        x = ((CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH * 2) +
             CHARACTER_SELECT_PANEL_SIZE[0])
        y = ((CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH * 2) +
             CHARACTER_SELECT_PANEL_SIZE[1])
        
        self.selectionBorder = pygame.Surface((x, y))
        self.selectionBorder.fill(CHARACTER_SELECT_PANEL_SELECTION_BORDER_COLOR)

    def update(self):
        pass

    def mouseMoved(self, pos):
        test = False
        for p in self.group.characterPanels:
            if p.rect.collidepoint(pos):
                self.currSelected = p
                test = True
                break

        if not test:
            self.currSelected = None

    def click(self):
        if not self.currSelected is None:
            self.openEditor = True

    def getSelectionBorderPos(self):
        if self.currSelected is None:
            return None
        
        x = (self.currSelected.rect.left -
             CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH)
        y = (self.currSelected.rect.top -
             CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH)
        return (x, y)


class CharacterPanel(object):
    def __init__(self, rect, character):
        self.rect = rect
        self.character = character
        self.panel = pygame.Surface(CHARACTER_SELECT_PANEL_SIZE)
        self.panel.fill(CHARACTER_SELECT_PANEL_COLOR_FILL)
        pygame.draw.rect(self.panel, CHARACTER_SELECT_PANEL_COLOR_BORDER,
                         (0 + CHARACTER_SELECT_PANEL_BORDER_SIZE,
                          0 + CHARACTER_SELECT_PANEL_BORDER_SIZE,
                          (CHARACTER_SELECT_PANEL_SIZE[0] -
                           (CHARACTER_SELECT_PANEL_BORDER_SIZE * 2)),
                          (CHARACTER_SELECT_PANEL_SIZE[1] -
                           (CHARACTER_SELECT_PANEL_BORDER_SIZE * 2)) ),
                         CHARACTER_SELECT_PANEL_BORDER_WIDTH)
                         

class CharacterPanelGroup(object):
    def __init__(self, num):
        self.num = num

        numOfCols = int(math.ceil(float(num) /
                                  float(CHARACTER_SELECT_PANELS_PER_COL)))

        numOfPanelsInCol = []
        for i in range(numOfCols):
            numOfPanelsInCol.append(0)

        count = 0
        currCol = 0
        while count < num:
            numOfPanelsInCol[currCol] += 1
            count += 1
            currCol += 1
            if currCol == numOfCols:
                currCol = 0
                

        self.characterPanels = []
        for i in range(len(numOfPanelsInCol)):
            colMid = (SCREEN_SIZE[0] / (len(numOfPanelsInCol) + 1)) * (i+1)
            for j in range(numOfPanelsInCol[i]):
                rect = pygame.Rect((0, 0), CHARACTER_SELECT_PANEL_SIZE)
                rect.centerx = colMid
                rect.top = (CHARACTER_SELECT_GROUP_FROM_TOP +
                            ((CHARACTER_SELECT_PANEL_SIZE[1] +
                             CHARACTER_SELECT_GROUP_SPACING)
                             * j))

                self.characterPanels.append(CharacterPanel(rect, None))

    def draw(self, screen):
        for p in self.characterPanels:
            screen.blit(p.panel, p.rect.topleft)
