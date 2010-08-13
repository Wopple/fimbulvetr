import os
import sys
import pygame

import mvc

import minimenu
import textrect
import boundint

from constants import *

class Model(mvc.Model):
    def __init__(self):
        super(Model, self).__init__()

        self.tempRect = pygame.Rect( (50, 50), (200, 0) )
        menuOptions = ["Host", "Client"]
        self.menuHostClient = minimenu.MiniMenu(self.tempRect, menuOptions,
                                           MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF,
                                           MAIN_MENU_COLOR_BG)
        self.menuHostClient.center(ENTIRE_SCREEN, True, True)
        
        menuOptions = ["Cancel"]
        self.menuCancelWait = minimenu.MiniMenu(self.tempRect, menuOptions,
                                           MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF,
                                           MAIN_MENU_COLOR_BG)
        self.menuCancelWait.center(ENTIRE_SCREEN, True, True)

        menuOptions = ["Try Again", "Cancel"]
        self.menuTryAgain = minimenu.MiniMenu(self.tempRect, menuOptions,
                                           MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF,
                                           MAIN_MENU_COLOR_BG)
        self.menuTryAgain.center(ENTIRE_SCREEN, True, True)
        
        self.textHostWaiting = textrect.render_textrect("Listening for Client...",
                                                        MAIN_MENU_FONT, self.tempRect,
                                                        MAIN_MENU_COLOR_OFF,
                                                        MAIN_MENU_COLOR_BG, 1)
        self.textClientWaiting = textrect.render_textrect("Searching for Host...",
                                                        MAIN_MENU_FONT, self.tempRect,
                                                        MAIN_MENU_COLOR_OFF,
                                                        MAIN_MENU_COLOR_BG, 1)
        self.textConnTimeout = textrect.render_textrect("Connection timed out",
                                                        MAIN_MENU_FONT, self.tempRect,
                                                        MAIN_MENU_COLOR_OFF,
                                                        MAIN_MENU_COLOR_BG, 1)
        
        self.changePhase(1)

    def changePhase(self, n):
        self.phase = n

        if n == 1:
            self.menu = self.menuHostClient
            self.text = None
        if n == 3:
            self.menu = None
            self.text = self.textHostWaiting
        if n == 4:
            self.menu = None
            self.text = self.textClientWaiting
        if n == 5:
            self.menu = self.menuTryAgain
            self.text = self.textConnTimeout

        if not self.menu is None:
            self.textLoc = (self.menu.rect.left,
                            self.menu.rect.top - self.tempRect.height)
        else:
            self.textLoc = ((SCREEN_SIZE[0] / 2) - (self.tempRect.width / 2),
                            (SCREEN_SIZE[1] / 2) - (self.tempRect.height / 2) )
            

    def update(self):
        pass
  
    def mouseMoved(self, pos):
        if not self.menu is None:
            val = self.menu.isAreaRect(pos)
            if val > 0:
                self.menu.setVal(val)
            else:
                self.menu.setVal(-1)

    def incMenu(self):
        self.menu.inc()

    def decMenu(self):
        self.menu.dec()

    def confirm(self):
        if not self.menu is None:
            if not self.menu.noSelection:
                if self.phase == 1 or self.phase == 5:
                    self.advanceNow = True

    def click(self, pos):
        self.confirm()

    def cancel(self):
        if self.phase == 1:
            self.backNow = True

