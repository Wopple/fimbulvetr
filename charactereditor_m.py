import os
import sys
import pygame

import mvc

import minimenu
import textrect
import boundint
import incint

import hare, fox

from constants import *

class Model(mvc.Model):
    def __init__(self):
        super(Model, self).__init__()

        self.stage = 0
        self.charCharacter = None
        self.characterToDisplay = None
        self.makeMenu()

        self.tempNames = ["Blah",
                          "Yo",
                          "Bob",
                          "Aether",
                          "Dude",
                          "Blahhhh",
                          "Earl",
                          "TJ",
                          "Quote",
                          "Bulbasaur",
                          "Shinku Hadouken",
                          "YO!!!",
                          "Yo Momma",
                          "Fat guy"]
        numOfPages = int(len(self.tempNames) / CHAR_EDITOR_NUM_PER_PAGE)
        if ( (int(len(self.tempNames) % CHAR_EDITOR_NUM_PER_PAGE)) == 0):
            numOfPages -= 1
        self.page = incint.IncInt(0, 0, numOfPages)
        self.buildCharMenu(True)

        size = (self.menu.rect.width *  3, self.charMenu.rect.height)
        self.baseSurface = pygame.Surface(size)
        self.baseSurface.fill(CHAR_EDITOR_COLOR_BG)
        self.baseSurfaceRect = pygame.Rect((0,0), size)
        self.baseSurfaceRect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        self.charMenu.rect.topleft = self.baseSurfaceRect.topleft

        self.blackPanel = pygame.Surface((self.menu.rect.width,
                                          self.charMenu.rect.height))
        self.blackPanel.fill(CHAR_EDITOR_BLACK_PANEL_COLOR)
        pos1 = self.charMenu.rect.topleft
        pos2 = (pos1[0] + (self.charMenu.rect.width * 2), pos1[1])
        self.blackPanelPos = [pos1, pos2]
        

    def buildCharMenu(self, firstTime=False):
        low = CHAR_EDITOR_NUM_PER_PAGE * self.page.value
        high = CHAR_EDITOR_NUM_PER_PAGE * (self.page.value + 1)
        if high > len(self.tempNames):
            high = len(self.tempNames)
        
        tempRect = pygame.Rect( (50, 50), (200, 0) )
        self.charMenu = minimenu.MiniMenu(tempRect, self.tempNames[low:high],
                                          CHAR_EDITOR_FONT, CHAR_EDITOR_COLOR_ON,
                                          CHAR_EDITOR_COLOR_OFF,
                                          CHAR_EDITOR_BLACK_PANEL_COLOR)
        if firstTime:
            pos = (0, 0)
        else:
            pos = self.baseSurfaceRect.topleft
        self.charMenu.rect.topleft = pos

    def makeMenu(self):
        if self.stage == 0:
            menuOptions = ["New", "Delete", "Change Power", "Done"]

        elif self.stage == 1:
            menuOptions = []
            self.getSpeciesList()
            for s in self.currSpeciesList:
                menuOptions.append(s.speciesName)

        tempRect = pygame.Rect( (50, 50), (200, 0) )
        self.menu = minimenu.MiniMenu(tempRect, menuOptions,
                                          CHAR_EDITOR_FONT, CHAR_EDITOR_COLOR_ON,
                                          CHAR_EDITOR_COLOR_OFF,
                                          CHAR_EDITOR_COLOR_BG)
        self.menu.rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

    def setStage(self, s):
        self.stage = s
        self.makeMenu()

    def getSpeciesList(self):
        self.currSpeciesList = [ hare.Hare(),
                                 fox.Fox() ]
        
        for s in self.currSpeciesList:
            s.preciseLoc = [self.menu.rect.center[0] + self.menu.rect.width,
                            self.charMenu.rect.center[1] + (self.baseSurfaceRect.height / 8)]
            s.facingRight = False

    def update(self):
        if not self.characterToDisplay is None:
            self.characterToDisplay.staticUpdate()

    def cancel(self):
        self.backNow = True

    def mouseMoved(self, pos):
        val = self.menu.isAreaRect(pos)
        if val > 0:
            self.menu.setVal(val)
            if self.stage == 1:
                self.characterToDisplay = self.currSpeciesList[val-1]
        else:
            self.menu.setVal(-1)
            if self.stage == 1:
                self.characterToDisplay = None
            

    def incMenu(self):
        self.charMenu.inc()
        if self.charMenu.isMin():
            self.incPage()

    def decMenu(self):
        self.charMenu.dec()
        if self.charMenu.isMax():
            self.decPage()

    def incPage(self):
        self.page.inc()
        self.buildCharMenu()
        self.charMenu.setVal(0)

    def decPage(self):
        self.page.dec()
        self.buildCharMenu()
        self.charMenu.setToMax()

    def confirm(self):
        if not self.menu.noSelection:
            if self.stage == 0:
                if self.menu.value() == 1:
                    self.advanceNow = True
                elif self.menu.value() == 4:
                    self.backNow = True
            if self.stage == 1:
                 self.advanceNow = True

    def click(self, pos):
        val = self.charMenu.isAreaRect(pos)
        if val > 0:
            self.charMenu.setVal(val)
        else:
            self.confirm()
