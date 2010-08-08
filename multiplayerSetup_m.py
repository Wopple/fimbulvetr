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

        tempRect = pygame.Rect( (50, 50), (200, 0) )
        menuOptions = ["Host", "Client"]
        self.menuHostClient = minimenu.MiniMenu(tempRect, menuOptions,
                                           MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF,
                                           MAIN_MENU_COLOR_BG)
        self.menuHostClient.center(ENTIRE_SCREEN, True, True)
        menuOptions = ["Cancel"]
        self.menuCancelWait = minimenu.MiniMenu(tempRect, menuOptions,
                                           MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF,
                                           MAIN_MENU_COLOR_BG)
        self.menuCancelWait.center(ENTIRE_SCREEN, True, True)

        
        self.textHostWaiting = textrect.render_textrect("Listening for Client...",
                                                        MAIN_MENU_FONT, tempRect,
                                                        MAIN_MENU_COLOR_OFF,
                                                        MAIN_MENU_COLOR_BG, 1)
        self.textClientWaiting = textrect.render_textrect("Searching for Host...",
                                                        MAIN_MENU_FONT, tempRect,
                                                        MAIN_MENU_COLOR_OFF,
                                                        MAIN_MENU_COLOR_BG, 1)
        self.textLoc = (self.menuCancelWait.rect.left,
                           self.menuCancelWait.rect.top - tempRect.height)

                                                        

        self.changePhase(1)

    def changePhase(self, n):
        self.phase = n

        if n == 1:
            self.menu = self.menuHostClient
            self.text = None
        if n == 3:
            self.menu = self.menuCancelWait
            self.text = self.textHostWaiting
        if n == 4:
            self.menu = self.menuCancelWait
            self.text = self.textClientWaiting

    def update(self):
        pass
  
    def mouseMoved(self, pos):
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
        if not self.menu.noSelection:
            if self.phase == 3 or self.phase == 4:
                self.backNow = True
            else:
                self.advanceNow = True

    def click(self, pos):
        self.confirm()

    def cancel(self):
        self.backNow = True

