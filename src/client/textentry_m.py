import os
import sys
import pygame

from constants import *

import mvc
import string
import textrect

#import win32clipboard, win32con

class Model(mvc.Model):
    def __init__(self, title, banList = [], ip=False, maxLength=None):
        super(Model, self).__init__()

        if maxLength is None:
            self.maxLength = TEXT_ENTRY_LENGTH_MAX
        else:
            self.maxLength = maxLength

        self.ipCheck = ip
        self.font = TEXT_ENTRY_FONT
        self.response = []
        self.banList = banList
        
        size = (TEXT_ENTRY_LINE_WIDTH + (TEXT_ENTRY_BORDER_SIZE * 2),
                self.font.get_linesize() + self.font.get_height() +
                (TEXT_ENTRY_BORDER_SIZE * 2))
        pos = [0, 0]
        for i in range(2):
            pos[i] = (SCREEN_SIZE[i] / 2) - (size[i] / 2)
        self.rect = pygame.Rect(pos, size)

        self.base = pygame.Surface(size)
        self.base.fill(BLACK)
        pygame.draw.rect(self.base, WHITE,
                         (0, 0, size[0], size[1]), 1)
        pygame.draw.rect(self.base, WHITE,
                         (0 + TEXT_ENTRY_BORDER_SIZE,
                          0 + TEXT_ENTRY_BORDER_SIZE,
                          size[0] - (TEXT_ENTRY_BORDER_SIZE * 2),
                          size[1] - (TEXT_ENTRY_BORDER_SIZE * 2)), 1)

        self.updateImage()

        size = (self.rect.width,
                self.font.get_linesize() + self.font.get_height())
        self.titleRect = pygame.Rect((0, 0), size)
        self.titleRect.bottom = self.rect.top
        self.titleRect.left = self.rect.left
        temp = textrect.render_textrect(title, self.font,
                                                   self.titleRect, WHITE,
                                                   BLACK, 1)
        self.titlePanel = pygame.Surface(size)
        self.titlePanel.blit(temp, (0, (size[1]/2) -
                                    (self.font.get_linesize()/2)))

    def updateImage(self):
        self.image = pygame.Surface(self.rect.size)
        self.image.blit(self.base, (0, 0))
        self.image.blit(self.font.render(self.convert(), 0, WHITE)
                        ,(TEXT_ENTRY_BORDER_SIZE + 3,
                          TEXT_ENTRY_BORDER_SIZE + (self.font.get_linesize()/2)))

    def update(self):
        pass

    def key(self, k):
        if len(self.response) < self.maxLength:
            self.response.append(k)
            self.updateImage()

    def backspace(self):
        self.response = self.response[0:-1]
        self.updateImage()

    def escape(self):
        self.backNow = True        

    def enter(self):
        if self.validResponse():
            self.advanceNow = True

    def convert(self):
        return string.join(self.response, "")

    def validEntry(self, k):
        return (k in VALID_INPUT_CHARACTERS)

    def validResponse(self):
        
        if len(self.response) <= 0:
            return False

        if not self.banList is None:
            if self.convert() in self.banList:
                return False

        if self.ipCheck:
            if not self.isValidIP():
                return False

        return True

    def isValidIP(self):
        orig = self.convert()
        sep = orig.split('.')
        
        if not (len(sep) == 4):
            return False

        for x in sep:
            try:
                i = int(x)
                if (i < 0) or (i > 255):
                    return False
            except:
                return False

        return True

    def pasteFromClipboard(self):
        pass
        #win32clipboard.OpenClipboard()
        #text = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        #win32clipboard.CloseClipboard()

        #for i in range(len(text)):
        #    if len(self.response) >= self.maxLength:
        #        break
        #    if self.validEntry(text[i]):
        #        self.key(text[i])
