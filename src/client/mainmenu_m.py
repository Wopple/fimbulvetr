import os
import sys
import pygame

import mvc

import minimenu
import textrect
import boundint

import scrollingbackground

from common.constants import *

class Model(mvc.Model):
    def __init__(self, fade):
        super(Model, self).__init__()

        self.bg = pygame.Surface(SCREEN_SIZE)
        self.bg = scrollingbackground.ScrollingBackground(pygame.Rect((0, 0), SCREEN_SIZE), MAIN_MENU_BACKGROUND_IMAGE, [0.2, 0.5])
        
        tempRect = pygame.Rect( (50, 50), (200, 0) )
        menuOptions = ["Play Single Player", "Play via Network",
                       "Character Setup", "Options", "Credits", "Exit"]
        self.menu = minimenu.MiniMenu(tempRect, menuOptions,
                                           MAIN_MENU_FONT, MAIN_MENU_COLOR_ON,
                                           MAIN_MENU_COLOR_OFF,
                                           MAIN_MENU_COLOR_BG)
        self.menu.center(ENTIRE_SCREEN, False, True)
        self.menu.rect.left = MAIN_MENU_OFFSET_FROM_SIDE

        self.textMessages = [ ("Fimbulvetr", 3, ALMOST_BLACK, WHITE, 1, True),
                              ("War of the Great Winter", 2, ALMOST_BLACK, WHITE, 1, True)]
        self.textRects = []
        for i in self.textMessages:
            f = FONTS[i[1]]
            size = (SCREEN_SIZE[0], f.get_linesize() + f.get_height())
            tempRect = pygame.Rect( (0, 0), size )
            self.textRects.append(textrect.render_textrect(
                i[0], f, tempRect, i[2], i[3], i[4], i[5]))

        self.transSurface = pygame.Surface(SCREEN_SIZE)
        self.transSurface.fill((INTRO_MAX_FADE, INTRO_MAX_FADE, INTRO_MAX_FADE))
        self.transAlpha = boundint.BoundInt(0, 255, 255)
        self.transChecker = True
        self.transDirection = False

        if not fade:
            self.transAlpha.value = 0
            self.transChecker = False

    def confirm(self):
        if not self.menu.noSelection:
            self.advanceNow = True

    def update(self):
        
        self.bg.update()
        
        if self.transChecker:
            if self.transDirection:
                mult = 1
            else:
                mult = -1
            self.transAlpha.add(MAIN_MENU_FADE_SPEED * mult)
            self.transSurface.set_alpha(self.transAlpha.value)

            if self.transAlpha.atBound():
                self.transChecker = False

    def cancel(self):
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
