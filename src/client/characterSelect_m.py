import os
import sys
import pygame

import mvc
import textrect

import math

from common.constants import *
from client.constants import *

class Model(mvc.Model):
    def __init__(self, theMap, isHost):
        super(Model, self).__init__()

        self.theMap = theMap

        self.openEditor = False
        self.sendNetMessage = False
        self.starting = False

        self.bg = pygame.Surface(SCREEN_SIZE)
        self.bg.fill(CHARACTER_SELECT_BG_COLOR)

        self.group = CharacterPanelGroup(self.theMap.numOfCharactersPerTeam())
        self.currSelected = None

        x = ((CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH * 2) +
             CHARACTER_SELECT_PANEL_SIZE[0])
        y = ((CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH * 2) +
             CHARACTER_SELECT_PANEL_SIZE[1])
        
        self.selectionBorder = pygame.Surface((x, y))
        self.selectionBorder.fill(CHARACTER_SELECT_PANEL_SELECTION_BORDER_COLOR)

        tempRect = pygame.Rect((0, 0), CHARACTER_SELECT_PLAYER_SIZE)
        tempRect.bottom = SCREEN_SIZE[1] - CHARACTER_SELECT_GROUP_FROM_TOP
        tempRect.centerx = SCREEN_SIZE[0] / 2
        self.clientPanel = PlayerPanel(tempRect, "Client", self.group.num)

        tempRect = pygame.Rect((0, 0), CHARACTER_SELECT_PLAYER_SIZE)
        tempRect.bottom = (self.clientPanel.rect.top -
                           CHARACTER_SELECT_GROUP_SPACING)
        tempRect.centerx = SCREEN_SIZE[0] / 2
        self.hostPanel = PlayerPanel(tempRect, "Host", self.group.num)

        if isHost:
            self.myPanel = self.hostPanel
            self.theirPanel = self.clientPanel
        else:
            self.myPanel = self.clientPanel
            self.theirPanel = self.hostPanel


        tempRect = pygame.Rect((0, 0), CHARACTER_SELECT_BUTTON_SIZE)
        tempRect.left = self.myPanel.rect.right + CHARACTER_SELECT_GROUP_SPACING
        tempRect.top = self.myPanel.rect.top
        self.readyButton = Button(tempRect, "Ready")

        if isHost:
            tempRect = pygame.Rect((0, 0), CHARACTER_SELECT_BUTTON_SIZE)
            tempRect.left = (self.theirPanel.rect.right +
                             CHARACTER_SELECT_GROUP_SPACING)
            tempRect.top = self.theirPanel.rect.top
            self.startButton = Button(tempRect, "Start")
        else:
            self.startButton = None

        x = ((CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH * 2) +
             CHARACTER_SELECT_BUTTON_SIZE[0])
        y = ((CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH * 2) +
             CHARACTER_SELECT_BUTTON_SIZE[1])
        self.selectionBorderButton = pygame.Surface((x, y))
        self.selectionBorderButton.fill(
            CHARACTER_SELECT_PANEL_SELECTION_BORDER_COLOR)

        self.loadingImage = INTERFACE_GRAPHICS[9]
        self.loadingRect = pygame.Rect( (0, 0), self.loadingImage.get_size() )
        self.loadingRect.center = ( SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)


    def update(self):
        pass

    def mouseMoved(self, pos):
        test = False
        for p in self.group.characterPanels:
            if p.rect.collidepoint(pos):
                self.currSelected = p
                test = True
                return

        temp = [self.readyButton, self.startButton]
        for b in temp:
            if not b is None:
                if b.enabled:
                    if b.rect.collidepoint(pos):
                        self.currSelected = b
                        test = True
                        return

        if not test:
            self.currSelected = None

    def click(self):
        if not self.currSelected is None:
            if isinstance(self.currSelected, CharacterPanel):
                if not self.myPanel.ready:
                    self.openEditor = True
                    self.sendNetMessage = True
            elif (self.currSelected is self.readyButton):
                if self.myPanel.ready:
                    self.myPanel.ready = False
                    self.myPanel.changeVal()
                    self.sendNetMessage = True
                else:
                    if self.group.isMax():
                        self.myPanel.ready = True
                        self.myPanel.changeVal()
                        self.sendNetMessage = True
                if not self.startButton is None:
                    self.startButton.setButton((self.myPanel.ready )
                                               and (self.theirPanel.ready))
            elif (self.currSelected is self.startButton):
                if (self.myPanel.ready and self.theirPanel.ready):
                    self.starting = True
                    self.sendNetMessage = True

    def click2(self):
        if not self.currSelected is None:
            if isinstance(self.currSelected, CharacterPanel):
                if not self.myPanel.ready:
                    self.setCharacter(None)
                    self.sendNetMessage = True

    def getSelectionBorder(self):
        if isinstance(self.currSelected, Button):
            border = self.selectionBorderButton
        else:
            border = self.selectionBorder

        if self.currSelected is None:
            loc = None
        else:
            x = (self.currSelected.rect.left -
                 CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH)
            y = (self.currSelected.rect.top -
                 CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH)
            loc = (x, y)
        return border, loc

    def setCharacter(self, c):
        if not (self.alreadyUsed(c)):
            self.currSelected.setCharacter(c)
            num = self.group.getNumActive()
            self.myPanel.changeVal(num)
            self.readyButton.setButton(self.group.isMax())

    def alreadyUsed(self, c):
        if not c is None:
            for p in self.group.characterPanels:
                if not p.character is None:
                    if p.character.name == c.name:
                        return True

        return False


    def buildNetMessage(self):
        if self.sendNetMessage:
            self.sendNetMessage = False
            msg = str(self.group.getNumActive())
            if self.group.getNumActive() < 10:
                msg = "0" + msg

            if self.starting:
                msg = msg + "s"
            elif self.myPanel.ready:
                msg = msg + "r"
            else:
                msg = msg + "0"
        else:
            msg = "-00"

        if len(msg) != CHARACTER_SELECT_NET_MESSAGE_SIZE:
            raise Exception()

        return msg

    def netMessageSize(self):
        return CHARACTER_SELECT_NET_MESSAGE_SIZE

    def parseNetMessage(self, msg, p):
        if msg[0] != "-":
            
            try:
                num = int(msg[0:2])
            except:
                raise

            if msg[2] == "r":
                ready = True
            elif msg[2] == "s":
                self.starting = True
                return
            else:
                ready = False

            self.theirPanel.ready = ready
            self.theirPanel.changeVal(num)

            if not self.startButton is None:
                self.startButton.setButton((self.myPanel.ready )
                                           and (self.theirPanel.ready))

    def getCharacters(self):
        chars = []

        for i in self.group.characterPanels:
            chars.append(i.character)

        return chars

    def numEnemiesExpected(self):
        return self.theirPanel.maxVal

    def getCurrSelectedName(self):
        if ((not self.currSelected is None) and
            (not self.currSelected.character is None)):
            return self.currSelected.character.name
        else:
            return None

class PlayerPanel(object):
    def __init__(self, rect, name, maxVal):
        self.rect = rect
        self.name = name
        self.ready = False
        self.maxVal = maxVal
        self.backPanel = pygame.Surface(self.rect.size)
        self.backPanel.fill(CHARACTER_SELECT_PANEL_COLOR_FILL)
        pygame.draw.rect(self.backPanel, CHARACTER_SELECT_PANEL_COLOR_BORDER,
                         (0 + CHARACTER_SELECT_PANEL_BORDER_SIZE,
                          0 + CHARACTER_SELECT_PANEL_BORDER_SIZE,
                          (self.rect.width -
                           (CHARACTER_SELECT_PANEL_BORDER_SIZE * 2)),
                          (self.rect.height -
                           (CHARACTER_SELECT_PANEL_BORDER_SIZE * 2)) ),
                         CHARACTER_SELECT_PANEL_BORDER_WIDTH)

        self.changeVal(0)

    def changeVal(self, val=None):
        if not val is None:
            self.val = val
        self.panel = pygame.Surface(self.rect.size)
        self.panel.blit(self.backPanel, (0,0))

        font = CHARACTER_SELECTION_FONT
        textHeight = font.get_linesize() + 2
        tempRect = pygame.Rect( (0, 0), (self.rect.width, textHeight) )

        text = textrect.render_textrect(self.name, font, tempRect,
                                        CHARACTER_SELECTION_FONT_COLOR,
                                        ALMOST_BLACK, 0, True)
        tempRect = pygame.Rect((0, 0), text.get_size())
        tempRect.top = ((CHARACTER_SELECT_PANEL_SIZE[1] / 2) -
                         (tempRect.height / 2))
        loc = (tempRect.left + CHARACTER_SELECT_PANEL_BORDER_WIDTH +
               CHARACTER_SELECT_PANEL_BORDER_SIZE,
               tempRect.top)
        self.panel.blit(text, loc)

        if self.ready:
            msg = "READY"
            color = CHARACTER_SELECTION_READY_COLOR
        else:
            msg = str(self.val) + "/" + str(self.maxVal)
            color = CHARACTER_SELECTION_FONT_COLOR
        text = textrect.render_textrect(msg, font, tempRect,
                                        color, ALMOST_BLACK, 2, True)
        loc = (tempRect.left - CHARACTER_SELECT_PANEL_BORDER_WIDTH -
               CHARACTER_SELECT_PANEL_BORDER_SIZE,
               tempRect.top)
        self.panel.blit(text, loc)

    def draw(self, screen):
        screen.blit(self.panel, self.rect.topleft)


class Button(object):
    def __init__(self, rect, msg):
        self.rect = rect
        self.msg = msg
        self.enabled = True
        self.backPanel = pygame.Surface(self.rect.size)
        self.backPanel.fill(CHARACTER_SELECT_PANEL_COLOR_FILL)

        self.setButton(False)

    def setButton(self, val):
        if not (val == self.enabled):
            self.enabled = val
        
            self.panel = pygame.Surface(self.rect.size)
            self.panel.blit(self.backPanel, (0,0))

            if self.enabled:
                color = CHARACTER_SELECTION_BUTTON_COLOR_ON
            else:
                color = CHARACTER_SELECTION_BUTTON_COLOR_OFF

            font = CHARACTER_SELECTION_FONT
            textHeight = font.get_linesize() + 2
            tempRect = pygame.Rect( (0, 0), (self.rect.width, textHeight) )

            text = textrect.render_textrect(self.msg, font, tempRect,
                                            color,
                                            ALMOST_BLACK, 1, True)
            tempRect = pygame.Rect((0, 0), text.get_size())
            tempRect.top = ((CHARACTER_SELECT_PANEL_SIZE[1] / 2) -
                             (tempRect.height / 2))
            self.panel.blit(text, tempRect.topleft)

    def draw(self, screen):
        screen.blit(self.panel, self.rect.topleft)
             

class CharacterPanel(object):
    def __init__(self, rect, character):
        self.rect = rect
        self.backPanel = pygame.Surface(self.rect.size)
        self.backPanel.fill(CHARACTER_SELECT_PANEL_COLOR_FILL)
        pygame.draw.rect(self.backPanel, CHARACTER_SELECT_PANEL_COLOR_BORDER,
                         (0 + CHARACTER_SELECT_PANEL_BORDER_SIZE,
                          0 + CHARACTER_SELECT_PANEL_BORDER_SIZE,
                          (self.rect.width -
                           (CHARACTER_SELECT_PANEL_BORDER_SIZE * 2)),
                          (self.rect.height -
                           (CHARACTER_SELECT_PANEL_BORDER_SIZE * 2)) ),
                         CHARACTER_SELECT_PANEL_BORDER_WIDTH)

        self.setCharacter(None)

    def setCharacter(self, c):
        self.character = c

        self.panel = pygame.Surface(CHARACTER_SELECT_PANEL_SIZE)
        self.panel.blit(self.backPanel, (0, 0))

        if not self.character is None:
            font = CHARACTER_SELECTION_FONT
            msg = self.character.name
            textHeight = font.get_linesize() + 2
            tempRect = pygame.Rect( (0, 0),
                                    (CHARACTER_SELECT_PANEL_SIZE[0],
                                     textHeight) )

            text = textrect.render_textrect(msg, font, tempRect,
                                            CHARACTER_SELECTION_FONT_COLOR,
                                            ALMOST_BLACK, 1, True)
            tempRect = pygame.Rect((0, 0), text.get_size())
            tempRect.left = ((CHARACTER_SELECT_PANEL_SIZE[0] / 2) -
                             (tempRect.width / 2))
            tempRect.top = ((CHARACTER_SELECT_PANEL_SIZE[1] / 2) -
                             (tempRect.height / 2))
            self.panel.blit(text, tempRect.topleft)
            
                         

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

    def getNumActive(self):
        count = 0
        for i in self.characterPanels:
            if not i.character is None:
                count += 1

        return count

    def isMax(self):
        return (self.getNumActive() == self.num)

    def draw(self, screen):
        for p in self.characterPanels:
            screen.blit(p.panel, p.rect.topleft)
