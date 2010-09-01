import os
import sys
import pygame

import mvc

import chardata

import minimenu
import textrect
import boundint
import incint

import hare, fox, cat

from constants import *

class Model(mvc.Model):
    def __init__(self, isSelection=False):
        super(Model, self).__init__()
        self.page = None
        self.leftPageArrow = None
        self.rightPageArrow = None

        self.isSelectionScreen = isSelection

        self.setStage(0, True)

        self.idealSize = self.buildIdealSize()

        self.superMoveNameText = None
        
        self.buildCharMenu(True)

        size = (self.menu.rect.width *  3, self.idealSize[1])
        self.baseSurface = pygame.Surface(size)
        self.baseSurface.fill(CHAR_EDITOR_COLOR_BG)
        self.baseSurfaceRect = pygame.Rect((0,0), size)
        self.baseSurfaceRect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        self.charMenu.rect.topleft = self.baseSurfaceRect.topleft

        singlePanelSize = (self.menu.rect.width,
                           self.baseSurfaceRect.height)
        if not (self.leftPageArrow is None or self.rightPageArrow is None):
            self.leftPageArrow.setRect(self.charMenu.rect.topleft,
                                       singlePanelSize)
            self.rightPageArrow.setRect(self.charMenu.rect.topleft,
                                        singlePanelSize)

        self.blackPanel = pygame.Surface(singlePanelSize)
        self.blackPanel.fill(CHAR_EDITOR_BLACK_PANEL_COLOR)
        pos1 = self.charMenu.rect.topleft
        pos2 = (pos1[0] + (self.idealSize[0] * 2), pos1[1])
        self.blackPanelPos = [pos1, pos2]

        self.superMoveNameTextPos = [pos2[0], pos2[1]]
        self.superMoveNameTextPos[1] += self.idealSize[1] - 20
        

        if not self.page is None:
            self.loadCharacter()

    def buildCharMenu(self, firstTime=False):
        if not self.page is None:
            currPage = self.page.value
        else:
            currPage = 0
        numOfPages = int(len(self.savedNames) / CHAR_EDITOR_NUM_PER_PAGE)
        if ( (int(len(self.savedNames) % CHAR_EDITOR_NUM_PER_PAGE)) == 0):
            numOfPages -= 1
        if numOfPages < 0:
            self.page = None
        else:
            self.page = incint.IncInt(currPage, 0, numOfPages)
        
        if not self.page is None:
            low = CHAR_EDITOR_NUM_PER_PAGE * self.page.value
            high = CHAR_EDITOR_NUM_PER_PAGE * (self.page.value + 1)
            if high > len(self.savedNames):
                high = len(self.savedNames)

            nameList = self.savedNames[low:high]
        else:
            nameList = []


        
        
        tempRect = pygame.Rect( (50, 50), (200, 0) )

        
                                            
        self.charMenu = minimenu.MiniMenu(tempRect, nameList,
                                          CHAR_EDITOR_FONT, CHAR_EDITOR_COLOR_ON,
                                          CHAR_EDITOR_COLOR_OFF,
                                          CHAR_EDITOR_BLACK_PANEL_COLOR)
        self.charMenu.setVal(1)
                    
        if firstTime:
            pos = (0, 0)
        else:
            pos = self.baseSurfaceRect.topleft
            if not self.page is None:
                self.loadCharacter()
        self.charMenu.rect.topleft = pos

        if not self.page is None:
            self.leftPageArrow = PageArrow(False, self.page)
            self.rightPageArrow = PageArrow(True, self.page)

            if not firstTime:
                self.leftPageArrow.setRect(self.charMenu.rect.topleft,
                                           self.blackPanel.get_size())
                self.rightPageArrow.setRect(self.charMenu.rect.topleft,
                                            self.blackPanel.get_size())
            

    def buildIdealSize(self):
        tempList = []
        for i in range(CHAR_EDITOR_NUM_PER_PAGE):
            tempList.append("!")

        tempRect = pygame.Rect( (50, 50), (200, 0) )
        temp = minimenu.MiniMenu(tempRect, tempList,
                                 CHAR_EDITOR_FONT, CHAR_EDITOR_COLOR_ON,
                                 CHAR_EDITOR_COLOR_OFF,
                                 CHAR_EDITOR_BLACK_PANEL_COLOR)

        return temp.rect.size
        

    def makeMenu(self):
        if self.stage == 0:
            if self.isSelectionScreen:
                menuOptions = ["New", "Delete", "Change Power", "Select"]
            else:
                menuOptions = ["New", "Delete", "Change Power", "Done"]

        elif self.stage == 1:
            menuOptions = []
            self.getSpeciesList()
            for s in self.currSpeciesList:
                menuOptions.append(s.speciesName)

        elif self.stage == 2:
            menuOptions = []
            for i in self.characterToDisplay.superMoves:
                menuOptions.append(i.name)

        elif self.stage == 101:
            menuOptions = ["Nevermind...", "Delete"]

        tempRect = pygame.Rect( (50, 50), (200, 0) )
        self.menu = minimenu.MiniMenu(tempRect, menuOptions,
                                          CHAR_EDITOR_FONT, CHAR_EDITOR_COLOR_ON,
                                          CHAR_EDITOR_COLOR_OFF,
                                          CHAR_EDITOR_COLOR_BG)
        self.menu.rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)

    def setStage(self, s, firstTime=False):
        self.superMoveNameText = None
        self.stage = s
        self.makeMenu()

        self.advanceNow = False
        self.backNow = False

        if not (self.leftPageArrow is None or self.rightPageArrow is None):
            self.leftPageArrow.visible = (self.stage == 0)
            self.rightPageArrow.visible = (self.stage == 0)

        self.createDescription(None)

        self.mouseMoved(pygame.mouse.get_pos())

        if self.stage == 0:
            self.characterToDisplay = None
            self.superMoveToDisplay = None

            self.savedNames = chardata.getNameList()
            if not firstTime:
                self.buildCharMenu()

        elif self.stage == 101:
            n = "Delete\n" + self.characterToDisplay.name
            d = "Are you sure?"
            self.createDescription(n, d)

    def loadCharacter(self):
        self.characterToDisplay = chardata.loadCharacter(self.charMenu.text())
        self.characterToDisplay.preciseLoc = [self.menu.rect.center[0] + self.menu.rect.width,
                                              self.baseSurfaceRect.center[1] + (self.baseSurfaceRect.height / 8)]
        self.characterToDisplay.facingRight = False

        self.makeSuperNameText(self.characterToDisplay.getSuper())

    def makeSuperNameText(self, s):
        self.superMoveNameText = textrect.render_textrect(s.name, CHAR_EDITOR_FONT,
                                                          pygame.Rect((0, 0), (self.idealSize[0], 20)),
                                                          CHAR_EDITOR_COLOR_OFF,
                                                          CHAR_EDITOR_BLACK_PANEL_COLOR, 1)
        
        

    def getSpeciesList(self):
        self.currSpeciesList = [ hare.Hare(),
                                 fox.Fox(),
                                 cat.Cat()]
        
        for s in self.currSpeciesList:
            s.preciseLoc = [self.menu.rect.center[0] + self.menu.rect.width,
                            self.baseSurfaceRect.center[1] + (self.baseSurfaceRect.height / 8)]
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
                self.createDescription(self.characterToDisplay.speciesName,
                                       self.characterToDisplay.speciesDesc)
            elif self.stage == 2:
                self.superMoveToDisplay = self.characterToDisplay.superMoves[val-1]
                self.createDescription(self.superMoveToDisplay.name,
                                       self.superMoveToDisplay.desc)
        else:
            self.menu.setVal(-1)
            if self.stage == 1:
                self.characterToDisplay = None
                self.superMoveToDisplay = None
                self.createDescription(None)
                
            
    def createDescription(self, name=None, desc=None):
        if name is None:
            self.descSurface = None
        else:
            text = str(name + "\n\n" + desc)

            self.descSurface = textrect.render_textrect(text, CHAR_EDITOR_FONT,
                                                        pygame.Rect(self.charMenu.rect.topleft, self.idealSize),
                                                        CHAR_EDITOR_COLOR_OFF,
                                                        CHAR_EDITOR_BLACK_PANEL_COLOR)
                                                        
                                                        

    def incMenu(self):
        if not self.page is None:
            self.charMenu.inc()
            if self.charMenu.isMin():
                self.incPage()
            self.loadCharacter()

    def decMenu(self):
        if not self.page is None:
            self.charMenu.dec()
            if self.charMenu.isMax():
                self.decPage()
            self.loadCharacter()

    def incPage(self):
        if not self.page is None:
            self.page.inc()
            self.buildCharMenu()
            self.charMenu.setVal(1)
            self.loadCharacter()

    def decPage(self):
        if not self.page is None:
            self.page.dec()
            self.buildCharMenu()
            self.charMenu.setToMax()
            self.loadCharacter()

    def confirm(self):
        if not self.menu.noSelection:
            if self.stage == 0:
                if self.menu.value() == 1:
                    if self.isSelectionScreen:
                        if not self.characterToDisplay is None:
                            self.advanceNow = True
                    else:
                        self.advanceNow = True
                elif self.menu.value() == 2:
                    if not self.characterToDisplay is None:
                        self.setStage(101)
                elif self.menu.value() == 3:
                    self.advanceNow = True
                elif self.menu.value() == 4:
                    self.backNow = True
            elif self.stage == 1:
                self.advanceNow = True
            elif self.stage == 2:
                self.advanceNow = True
                self.characterToDisplay.currSuperMove = self.menu.value() - 1
            elif self.stage == 101:
                if self.menu.value() == 2:
                    checker = False
                    if len(self.charMenu.options) == 1:
                        checker = True
                    chardata.deleteCharacter(self.characterToDisplay.name)
                    if checker:
                        if ((not self.page is None)
                            and (self.page.value > 0)):
                            self.page.dec()
                            self.buildCharMenu()
                            self.charMenu.setToMax()
                        else:
                            self.page = None
                    
                self.setStage(0)

    def click(self, pos):
        if ((not self.leftPageArrow is None) and
            (self.leftPageArrow.mouseIsOver(pos))):
            self.decPage()
        elif ((not self.rightPageArrow is None) and
            (self.rightPageArrow.mouseIsOver(pos))):
            self.incPage()
        else:
            val = self.charMenu.isAreaRect(pos)
            if (val > 0) and (self.stage == 0):
                self.charMenu.setVal(val)
                self.loadCharacter()
            else:
                self.confirm()

    def setCharacterSelection(self, name):
        for i, n in enumerate(self.savedNames):
            if n == name:
                #self.page.value = int(i / CHAR_EDITOR_NUM_PER_PAGE)
                self.charMenu.setVal(int(i % CHAR_EDITOR_NUM_PER_PAGE) + 1)
                self.loadCharacter()
                break

    def returnCharacter(self):
        return self.characterToDisplay


class PageArrow(object):
    def __init__(self, isRight, page):
        self.image = INTERFACE_GRAPHICS[4].copy()
        self.isRight = isRight

        if not isRight:
            self.image = pygame.transform.flip(self.image, True, False)

        self.visible = (page.maximum > 0)

    def setRect(self, pos, size):
        oldRect = pygame.Rect(pos, size)
        
        if self.isRight:
            xRef = oldRect.right
        else:
            xRef = oldRect.left

        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.center = (xRef, oldRect.centery)

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect.topleft)

    def mouseIsOver(self, mousePos):
        if not self.visible:
            return False

        return self.rect.collidepoint(mousePos)
