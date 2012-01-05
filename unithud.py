import os
import sys
import pygame
import copy

from constants import *

class UnitHUD(object):
    def __init__(self, inTeam, inPlayers):
        self.rect = pygame.Rect((0,0), (SCREEN_SIZE[0], UNIT_HUD_HEIGHT))
        self.rect.bottom = SCREEN_SIZE[1]
        self.team = inTeam
        
        self.createImage()
        
        
    def createImage(self):
        self.image = pygame.Surface(self.rect.size)
        color = UNIT_HUD_COLORS[self.team]
        
        self.image.fill(color)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)