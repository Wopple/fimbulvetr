import os
import sys
import pygame

import mvc
import textrect
import minimenu

import math

import random

import gamemap
import scrollingbackground
import mapchar

import copy

import hare, cat, fox

from constants import *

class Model(mvc.Model):
    def __init__(self, isHost):
        super(Model, self).__init__()
        
        self.bgs = [scrollingbackground.ScrollingBackground(pygame.Rect((0, 0),
                                                                        SCREEN_SIZE), CHARACTER_SELECT_BG_SKY, [0, 0]),
                    
                    scrollingbackground.ScrollingBackground(pygame.Rect((0, SCREEN_SIZE[1] - CHARACTER_SELECT_BG_MOUNTAINS_FAR.get_size()[1] - 70),
                                                                        SCREEN_SIZE), CHARACTER_SELECT_BG_MOUNTAINS_FAR, [-0.3, 0]),
                    
                    scrollingbackground.ScrollingBackground(pygame.Rect((0, SCREEN_SIZE[1] - CHARACTER_SELECT_BG_MOUNTAINS_NEAR.get_size()[1]),
                                                                        SCREEN_SIZE), CHARACTER_SELECT_BG_MOUNTAINS_NEAR, [-0.8, 0])
                    ]
        
        self.starting = False
        self.map = None
        
        self.netMessage = None
        
        self.subScreen = 0
        
        if isHost:
            self.playerNum = 0
        else:
            self.playerNum = 1
            
        #Create Map-selection Panel
        rect = pygame.Rect((0,0), CHARACTER_SELECTION_PANEL_SIZE)
        rect.centerx = SCREEN_SIZE[0] / 2
        rect.top = CHARACTER_SELECTION_PANEL_SPACING
        self.mapPanel = Panel(0, isHost, rect)
        
        self.characterPanels = []
        
        tempRect = pygame.Rect( (50, 50), (200, 0) )
        menuOptions = []
        for map in gamemap.getMapList():
            menuOptions.append(map.name + " (" + str(len(map.startingPoints[0])) + ")")
        menuOptions.append("<RANDOM>")
            
        self.mapMenu = minimenu.MiniMenu(tempRect, menuOptions,
                                         MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                         MAIN_MENU_COLOR_OFF,
                                         MAIN_MENU_COLOR_BG)
        self.mapMenu.center(ENTIRE_SCREEN, True, True)
        
        
        
        #Create Species Selection Menu
        speciesClasses = [(mapchar.Hare, hare.Hare),
                          (mapchar.Cat, cat.Cat)]
        speciesList = []
        for speciesClassGroup in speciesClasses:
            mapClass = speciesClassGroup[0]
            battleClass = speciesClassGroup[1]
            speciesList.append(mapClass(self.playerNum, battleClass()))
            
        self.speciesDialog = DetailDialog(SPECIES_SELECTION_DIALOG_SLOT_SIZE, SPECIES_SELECTION_DIALOG_MARGIN,
                                          SPECIES_SELECTION_DIALOG_SPACING, speciesList, [4, 2] )
                    
        self.currCharacterPanel = None
        
        self.readyPanels = [None, None]
        
        self.goPanel = None
        
        #self.selectMap("00");
        
    def update(self):
        for bg in self.bgs:
            bg.update()
            
        for panel in self.allPanels():
            if not panel is None:
                panel.update()
            
        if self.subScreen == 2:
            self.speciesDialog.update()
    
    def mouseMoved(self, pos):
        for p in self.allPanels():
            if not p is None:
                p.selected = False
            
        if self.subScreen == 0:
            for p in self.allPanels():
                if (not p is None) and p.isOwner and p.rect.collidepoint(pos) and (not isinstance(p.data, ReadyData) or self.canClickReady()):
                    p.selected = True
                    return
        elif self.subScreen == 1:
            val = self.mapMenu.isAreaRect(pos)
            print val
            if val > 0:
                self.mapMenu.setVal(val)
            else:
                self.mapMenu.setVal(-1)
        elif self.subScreen == 2:
            self.speciesDialog.mouseMoved(pos)
        elif self.subScreen == 10:
            possibilities = [self.readyPanels[self.playerNum]]
            if not self.goPanel is None:
                possibilities.append(self.goPanel)
            for p in possibilities:
                if p.isOwner and p.rect.collidepoint(pos):
                    p.selected = True
                    return
                
    def canClickReady(self):
        if self.mapPanel.data is None:
            return False
            
        for p in self.characterPanels:
            if p.isOwner and p.data is None:
                return False
            
        return True
            
    def allPanels(self):
        return self.characterPanels + self.readyPanels + [self.mapPanel, self.goPanel]
    
    def click(self):
        
        #No dialogs
        if self.subScreen == 0:
            if self.mapPanel.selected:
                self.subScreen = 1  #Map Sub-screen
            elif not self.readyPanels[self.playerNum] is None and self.readyPanels[self.playerNum].selected:
                self.readyPanels[self.playerNum].setData(ReadyData(True))
                self.sendReadyMessage()
                self.subScreen = 10
                self.createGoPanel()
            else:
                charPanel = None
                for panel in self.characterPanels:
                    if panel.selected:
                        charPanel = panel
                        break
                    
                if not charPanel is None:
                    self.currCharacterPanel = charPanel
                    self.subScreen = 2
                    
        #Map Selection Dialog
        elif self.subScreen == 1:
            mapSel = self.mapMenu.value()
            if (not self.mapMenu.noSelection) and (not mapSel is None):
                mapSel -= 1
                maps = gamemap.getMapList()
                if (mapSel >= 0) and (mapSel < len(maps)):
                    wasRandom = False
                else:
                    wasRandom = True
                    mapSel = random.randrange(len(maps))
                map = maps[mapSel]
                self.selectMap(map, wasRandom)
                
                if wasRandom:
                    wasRandomChar = "r"
                else:
                    wasRandomChar = "s"
                self.netMessage = "m" + wasRandomChar + "{0:02d}".format(map.num)
                
        #Species Selection Dialog
        elif self.subScreen == 2:
            data = self.speciesDialog.getSelectedData()
            if not data is None:
                self.currCharacterPanel.setData(data)
                self.subScreen = 0
                
                self.sendCharacterMessage()
                
        #Readied
        elif self.subScreen == 10:
            if not self.goPanel is None and self.goPanel.selected:
                self.starting = True
                self.netMessage = "s---"
            elif not self.readyPanels[self.playerNum] is None and self.readyPanels[self.playerNum].selected:
                self.readyPanels[self.playerNum].setData(ReadyData(False))
                self.sendReadyMessage()
                self.subScreen = 0
                self.goPanel = None
                
    def sendReadyMessage(self):
        
        self.netMessage = "r" + str(self.playerNum) + "--"
                
    def sendCharacterMessage(self):
        
        panelNum = None
        for i in range(len(self.characterPanels)):
            if (self.characterPanels[i] == self.currCharacterPanel):
                panelNum = i
                break
        
        self.netMessage = "c-" + "{0:02d}".format(panelNum)
        
                
        
    def getSpeciesList(self):
        return [hare.Hare(), cat.Cat()]           
            
    
    def click2(self):
        pass
    
    def selectMap(self, map, wasRandom):
        
        self.mapPanel.setData(MapData(map, wasRandom))
        
        numOfCharacterSlots = 0
        if not map is None:
            numOfCharacterSlots = len(map.startingPoints[0])
            
        self.characterPanels = []
        
        for i in range(2):
            xMid = (SCREEN_SIZE[0] / 4) * (1 + (i * 2))
            
            yMid = SCREEN_SIZE[1] / 2
            if (numOfCharacterSlots % 2 == 0):
                numToDisplaceFromCenter = (numOfCharacterSlots / 2) - 1
                yMid -= (CHARACTER_SELECTION_PANEL_SPACING / 2) + (CHARACTER_SELECTION_PANEL_SIZE[1] / 2)
            else:
                numToDisplaceFromCenter = int(numOfCharacterSlots / 2)
                
            yMid -= (CHARACTER_SELECTION_PANEL_SPACING + CHARACTER_SELECTION_PANEL_SIZE[1]) * numToDisplaceFromCenter
                
            
            for j in range(numOfCharacterSlots):
                rect = pygame.Rect((0,0), CHARACTER_SELECTION_PANEL_SIZE)
                rect.centerx = xMid
                rect.centery = yMid + ((CHARACTER_SELECTION_PANEL_SPACING + CHARACTER_SELECTION_PANEL_SIZE[1]) * j)
                self.characterPanels.append(Panel(i, (self.playerNum == i), rect))
                
            rect = rect = pygame.Rect((0,0), READY_PANEL_SIZE)
            rect.centerx = xMid
            rect.bottom = SCREEN_SIZE[1] - CHARACTER_SELECTION_PANEL_SPACING
            readyPanel = Panel(i, (self.playerNum == i), rect)
            readyPanel.faceUp = True
            readyPanel.setData(ReadyData(False))
            self.readyPanels[i] = readyPanel
            
        self.subScreen = 0
                
    def buildNetMessage(self):
        
        result = "----"
        
        if not self.netMessage is None:
            result = self.netMessage
            print self.netMessage
            
        self.netMessage = None
        return result
    
    def netMessageSize(self):
        return 4
    
    def parseNetMessage(self, msg, p):
        
        if msg[0] == 'm':
            wasRandom = (msg[1] == 'r')
            map = gamemap.getMap(msg[2:4])
            
            self.selectMap(map, wasRandom)
            
        elif msg[0] == 'c':
            panelNum = int(msg[2:4])
            
            self.characterPanels[panelNum].setData("")
            
        elif msg[0] == 'r':
            panelNum = int(msg[1])
            
            panel = self.readyPanels[panelNum]
            panel.setData(ReadyData(not panel.data.value))
            
            self.goPanel = None
            self.createGoPanel()
            
        elif msg[0] == 's':
            self.starting = True
        
    def createGoPanel(self):
        if (self.playerNum == 0 and
            (not self.readyPanels[0] is None and self.readyPanels[0].data.value == True) and
            (not self.readyPanels[1] is None and self.readyPanels[1].data.value == True)):
            
            rect = pygame.Rect((0,0), GO_PANEL_SIZE)
            rect.centerx = SCREEN_SIZE[0] / 2
            rect.bottom = SCREEN_SIZE[1] - CHARACTER_SELECTION_PANEL_SPACING
            goPanel = Panel(0, True, rect)
            goPanel.setData(GoData())
            
            self.goPanel = goPanel
            
    def getMap(self):
        return self.mapPanel.data.map
    
    def getCharacters(self):
        chars = []

        for p in self.characterPanels:
            if p.isOwner:
                chars.append(p.data)

        return chars
    
    def numEnemiesExpected(self):
        return len(self.getMap().startingPoints[0])
    
    def revealAllCharacters(self, allCharacters):
        pass
                
                
class Panel(object):
    
    def __init__(self, team, isOwner, rect):
        self.team = team
        self.isOwner = isOwner
        self.rect = rect
        self.data = None
        self.redraw = True
        self.selected = False
        self.faceUp = False
        
        self.update()
        
        sizeX = self.rect.width + (CHARACTER_SELECT_PANEL_SELECTION_AURA_WIDTH * 2)
        sizeY = self.rect.height + (CHARACTER_SELECT_PANEL_SELECTION_AURA_WIDTH * 2)
        posX = self.rect.left - CHARACTER_SELECT_PANEL_SELECTION_AURA_WIDTH
        posY = self.rect.top - CHARACTER_SELECT_PANEL_SELECTION_AURA_WIDTH
        self.selectionRect = pygame.Rect((posX, posY), (sizeX, sizeY))
        self.selectionPanel = pygame.Surface(self.selectionRect.size)
        self.selectionPanel.fill(WHITE)
        
        
    def update(self):
        if (self.redraw):
            
            #Draw Panel Surface
            if (self.data is None or (isinstance(self.data, ReadyData) and self.data.value == False)):
                paletteBase = CHARACTER_SELECT_PANEL_BASE_COLORS_OFF
                paletteDecor = CHARACTER_SELECT_PANEL_DECOR_COLORS_OFF
            else:
                paletteBase = CHARACTER_SELECT_PANEL_BASE_COLORS_ON
                paletteDecor = CHARACTER_SELECT_PANEL_DECOR_COLORS_ON
                
            colorBase = paletteBase[self.team]
            colorDecor = paletteDecor[self.team]
            
            self.image = pygame.Surface(self.rect.size)
            self.image.fill(colorBase)
            
            showFront = self.faceUp or self.isOwner
            
            if (showFront):
                decorMargin = CHARACTER_SELECT_PANEL_FACE_DECOR_MARGIN
                decorWidth = CHARACTER_SELECT_PANEL_FACE_DECOR_WIDTH
            else:
                decorMargin = CHARACTER_SELECT_PANEL_BACK_DECOR_MARGIN
                decorWidth = CHARACTER_SELECT_PANEL_BACK_DECOR_WIDTH
                
            decorOuter = pygame.Surface((self.rect.width - (decorMargin * 2), self.rect.height - (decorMargin * 2)))
            decorOuter.fill(colorDecor)
                
            decorInner = pygame.Surface((decorOuter.get_size()[0] - (decorWidth * 2),
                                         decorOuter.get_size()[1] - (decorWidth * 2)))
            decorInner.fill(colorBase)
            
            if (not showFront):
                margins = CHARACTER_SELECT_PANEL_BACK_CIRCLE_MARGINS
                ovalRect = pygame.Rect((margins[0], margins[1]),
                                       (decorInner.get_size()[0] - (margins[0] * 2),
                                        decorInner.get_size()[1] - (margins[1] * 2)))
                pygame.draw.ellipse(decorInner, colorDecor, ovalRect)
            
            decorOuter.blit(decorInner, (decorWidth, decorWidth))
            self.image.blit(decorOuter, (decorMargin, decorMargin))
            
            
            #Fill Data
            fillRect = pygame.Rect(((decorWidth + decorMargin), (decorWidth + decorMargin)), decorInner.get_size())
            if isinstance(self.data, mapchar.MapChar):
                
                font = CHARACTER_SELECTION_CAPTION_FONT
                textHeight = font.get_linesize() + 2
                tRect = pygame.Rect((0,0), (fillRect.width - 10, textHeight))
                tRect.centerx = fillRect.centerx
                tRect.centery = fillRect.centery
                text = textrect.render_textrect(self.data.name, font, tRect,
                                                CHARACTER_SELECTION_FONT_COLOR,
                                                ALMOST_BLACK, 0, True)
                self.image.blit(text, tRect.topleft)
                
                speciesImage = self.data.getSmallImage()
                speciesRect = pygame.Rect((0, 0), speciesImage.get_size())
                speciesRect.right = tRect.right
                speciesRect.centery = self.rect.height / 2
                
                self.image.blit(speciesImage, speciesRect.topleft)
                
                
            elif isinstance(self.data, MapData):
                
                font = CHARACTER_SELECTION_CAPTION_FONT
                textHeight = font.get_linesize() + 2
                tRect = pygame.Rect((0,0), (fillRect.width - 10, textHeight))
                tRect.centerx = fillRect.centerx
                tRect.centery = fillRect.centery
                text = textrect.render_textrect(self.data.map.name, font, tRect,
                                                CHARACTER_SELECTION_FONT_COLOR,
                                                ALMOST_BLACK, 0, True)
                self.image.blit(text, tRect.topleft)
                
                if self.data.wasRandom:
                    image = RANDOM_ICON
                    rect = pygame.Rect((0,0), image.get_size())
                    rect.right = fillRect.right
                    rect.centery = fillRect.centery
                    self.image.blit(image, rect.topleft)
                    
            elif isinstance(self.data, ReadyData):
                
                font = CHARACTER_SELECTION_CAPTION_FONT
                font = CHARACTER_SELECTION_CAPTION_FONT
                textHeight = font.get_linesize() + 2
                tRect = pygame.Rect((0,0), (fillRect.width - 10, textHeight))
                tRect.centerx = fillRect.centerx
                tRect.centery = fillRect.centery
                if self.data.value:
                    color = READY_PANEL_FONT_COLOR_TRUE
                    text = "READY"
                else:
                    color = READY_PANEL_FONT_COLOR_FALSE
                    text = "PREPARING..."
                text = textrect.render_textrect(text, font, tRect,
                                                color, ALMOST_BLACK, 1, True)
                self.image.blit(text, tRect.topleft)
                
            if isinstance(self.data, GoData):
                
                font = CHARACTER_SELECTION_CAPTION_FONT
                font = CHARACTER_SELECTION_CAPTION_FONT
                textHeight = font.get_linesize() + 2
                tRect = pygame.Rect((0,0), (fillRect.width - 10, textHeight))
                tRect.centerx = fillRect.centerx
                tRect.centery = fillRect.centery
                color = READY_PANEL_FONT_COLOR_TRUE
                text = "GO!"
                text = textrect.render_textrect(text, font, tRect,
                                                color, ALMOST_BLACK, 1, True)
                self.image.blit(text, tRect.topleft)
            
            
            self.redraw = False
            
    def setData(self, inData):
        self.data = inData
        self.redraw = True
        
        if isinstance(self.data, MapData):
            self.faceUp = True
                    
    def draw(self, screen):
        if (self.selected):
            screen.blit(self.selectionPanel, self.selectionRect.topleft)
        screen.blit(self.image, self.rect.topleft)
        
        
class MapData(object):
    def __init__(self, map, wasRandom):
        self.map = map
        self.wasRandom = wasRandom
        
        
class DetailDialog(object):
    def __init__(self, itemWidth, marginWidth, spacingWidth, items, itemMatrix):
        
        size = []
        for i in range(2):
            size.append( (itemWidth * itemMatrix[i]) + (spacingWidth * (itemMatrix[i] - 1)) + (marginWidth * 2) )
        self.rect = pygame.Rect((0, 0), size)
        self.rect.centerx = SCREEN_SIZE[0] / 2
        self.rect.centery = SCREEN_SIZE[1] / 2
        
        self.baseSurface = pygame.Surface(self.rect.size)
        self.baseSurface.fill(CHARACTER_SELECTION_DIALOG_BG_COLOR)
        
        self.caption = None
        
        self.createButtons(itemWidth, marginWidth, spacingWidth, items, itemMatrix)
        
    def update(self):
        pass
        
    def draw(self, screen):
        
        newSurface = pygame.Surface(self.rect.size)
        newSurface.blit(self.baseSurface, (0, 0))
        for button in self.buttons:
            button.draw(newSurface)
            
        if not self.caption is None:
            newSurface.blit(self.caption, self.captionRect.topleft)
        
        screen.blit(newSurface, self.rect.topleft)
        
    def getSelectedData(self):
        
        data = None
        
        for button in self.buttons:
            if button.selected:
                data = button.data
                break
            
        if isinstance(data, mapchar.MapChar):
            data = data.mapCloneMethod(data.team, data.battleCloneMethod())
            
        return data
        
        
    def createButtons(self, itemWidth, marginWidth, spacingWidth, items, itemMatrix):
        
        self.buttons = []
        for row in range(itemMatrix[1]):
            for col in range(itemMatrix[0]):
                itemIndex = (itemMatrix[0] * row) + col
                if (itemIndex >= len(items)):
                    return
                
                item = items[itemIndex]
                
                xPos = (itemWidth * col) + (spacingWidth * (col)) + marginWidth
                yPos = (itemWidth * row) + (spacingWidth * (row)) + marginWidth
                
                rect = pygame.Rect((xPos, yPos), (itemWidth, itemWidth))
                
                if (isinstance(item, mapchar.MapChar)):
                    images = []
                    icons = [item.images[0][0], item.images[1][0]]
                    for i in range(len(icons)):
                        icon = icons[i]
                        iconRect = pygame.Rect((0, 0), icon.get_size())
                        iconRect.centerx = (rect.width / 2)
                        iconRect.centery = (rect.height / 2)
                        surface = pygame.Surface(rect.size)
                        surface.fill(CHARACTER_SELECTION_DIALOG_BUTTON_COLOR)
                        surface.blit(icon, iconRect.topleft)
                        images.append(surface)
                
                self.buttons.append(DetailDialogButton(rect, images[0], images[1], item))
                
                
    def mouseMoved(self, pos):
        
        relPos = [pos[0] - self.rect.left, pos[1] - self.rect.top]
        
        for button in self.buttons:
            button.selected = False
            
        curr = None
        for button in self.buttons:
            if button.rect.collidepoint(relPos):
                button.selected = True
                curr = button
                break
        
        self.caption = None
        if not curr is None:
            font = CHARACTER_SELECTION_CAPTION_FONT
            height = font.get_linesize() + 2
            self.captionRect = pygame.Rect((0, 0), (self.rect.width, height))
            self.caption = textrect.render_textrect(curr.data.name, font, self.captionRect,
                                                    CHARACTER_SELECTION_FONT_COLOR,
                                                    ALMOST_BLACK, 1, True)
            self.captionRect.centerx = self.rect.width / 2
            self.captionRect.centery = self.rect.height / 2
        
        
        
class ReadyData(object):
    
    def __init__(self, value):
        self.value = value
        
class GoData(object):
    
    def __init__(self):
        pass
    
        
class DetailDialogButton(object):
    
    def __init__(self, rect, imageBase, imageHover, data):
        self.rect = rect
        self.imageBase = imageBase
        self.imageHover = imageHover
        self.data = data
        self.selected = False
    
    def draw(self, screen):
        if self.selected:
            image = self.imageHover
        else:
            image = self.imageBase
        screen.blit(image, self.rect.topleft)

    