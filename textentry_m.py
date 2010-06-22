import os
import sys
import pygame

from constants import *

import mvc
import string

class Model(mvc.Model):
    def __init__(self):
        super(Model, self).__init__()

        self.font = TEXT_ENTRY_FONT
        self.response = []
        
        size = (200 + (TEXT_ENTRY_BORDER_SIZE * 2),
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

    def updateImage(self):
        self.image = pygame.Surface(self.rect.size)
        self.image.blit(self.base, (0, 0))
        self.image.blit(self.font.render(self.convert(), 0, WHITE)
                        ,(TEXT_ENTRY_BORDER_SIZE + 3,
                          TEXT_ENTRY_BORDER_SIZE + (self.font.get_linesize()/2)))

    def update(self):
        pass

    def key(self, k):
        self.response.append(k)
        self.updateImage()

    def backspace(self):
        self.response = self.response[0:-1]
        self.updateImage()

    def escape(self):
        self.backNow = True        

    def enter(self):
        self.advanceNow = True

    def convert(self):
        return string.join(self.response, "")

    def validEntry(self, k):
        return (k in VALID_INPUT_CHARACTERS)
    
