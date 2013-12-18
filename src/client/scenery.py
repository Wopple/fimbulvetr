import os
import sys
import pygame

from common.constants import *
from client.constants import *

FLOOR_POS = BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT
NEUTRAL_POS = (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS)

class Scenery(object):
    
    def __init__(self, terrainLeft, terrainRight):
        
        self.terrainLeft = terrainLeft
        self.terrainRight = terrainRight
        
        self.backgroundItems = []
        self.foregroundItems = []
        
        self.generate()


    def generate(self):
        
        itemDict = {
                    (PLAINS, PLAINS) : (
                                    ("sky01", (BATTLE_ARENA_SIZE[0] / 2, BATTLE_ARENA_SIZE[1] / 2), (1.0, 0.0), False),
                                    ("cloudlarge", (-2000, -1500), (0.95, 0.90), False),
                                    ("cloud01", (2000, -2000), (0.95, 0.90), False),
                                    ("cloud02", (6000, -4000), (0.95, 0.90), False),
                                    ("cloud03", (-4300, -3000), (0.95, 0.90), False),
                                    ("plains2", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 200), (0.8, 0.5), False),
                                    ("ground01", NEUTRAL_POS, (0.0, 0.0), False)
                                ),
                    (SNOW, SNOW) : (
                                    ("sky02", (BATTLE_ARENA_SIZE[0] / 2, BATTLE_ARENA_SIZE[1] / 2), (1.0, 1.0), False),
                                    ("cloud07", (-4300, -3000), (0.95, 0.90), False),
                                    ("cloud08", (6000, -3000), (0.95, 0.90), False),
                                    ("snowyhill03", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 1200), (0.9, 0.9), False),
                                    ("snowyhill02", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 550), (0.5, 0.8), False),
                                    ("snowyhill01", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 300), (0.15, 0.6), False),
                                    ("ground02", NEUTRAL_POS, (0.0, 0.0), False)
                                ),
                    (FOREST, FOREST) : (
                                    ("sky01", (BATTLE_ARENA_SIZE[0] / 2, BATTLE_ARENA_SIZE[1] / 2), (1.0, 0.0), False),
                                    ("cloudlarge", (-2000, 50), (0.95, 0.0), False),
                                    ("cloud01", (2000, 200), (0.95, 0.0), False),
                                    ("cloud02", (6000, 400), (0.95, 0.0), False),
                                    ("cloud03", (-4300, 300), (0.95, 0.0), False),
                                    ("treeline", NEUTRAL_POS, (0.8, -0.01), False),
                                    ("tree03", (-200, FLOOR_POS), (0.5, -0.11), False),
                                    ("tree04", (1000, FLOOR_POS), (0.5, -0.11), False),
                                    ("tree05", (500, FLOOR_POS), (0.4, -0.11), False),
                                    ("tree01", (BATTLE_ARENA_SIZE[0] - 300, FLOOR_POS), (0.25, -0.15), False),
                                    ("tree02", (220, FLOOR_POS), (0.1, -0.18), False),
                                    ("ground01", NEUTRAL_POS, (0.0, 0.0), False)
                                ),
                    (WATER, WATER) : (
                                    ("sky01", (BATTLE_ARENA_SIZE[0] / 2, BATTLE_ARENA_SIZE[1] / 2), (1.0, 0.0), False),
                                    ("cloud04", (26000, -28000), (0.99, 0.99), False),
                                    ("cloud05", (-20000, -20000), (0.99, 0.99), False),
                                    ("lakeshore", ((BATTLE_ARENA_SIZE[0] / 2), FLOOR_POS), (0.99, 0.98), False),
                                    ("waterfront", ((BATTLE_ARENA_SIZE[0] / 2), FLOOR_POS + 18000), (0.99, 0.99), False),
                                    ("raft", NEUTRAL_POS, (0.0, 0.0), False)
                                ),
                    (MOUNTAIN, MOUNTAIN) : (
                                    ("sky01", (BATTLE_ARENA_SIZE[0] / 2, BATTLE_ARENA_SIZE[1] / 2), (1.0, 0.0), False),
                                    ("mountain2", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 1200), (0.95, 0.9), False),
                                    ("mountain1", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 800), (0.75, 0.8), False),
                                    ("rocks", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 200), (0.4, 0.5), False),
                                    ("ground03", NEUTRAL_POS, (0.0, 0.0), False)
                                ),
                    (FORTRESS, PLAINS) : (
                                    ("sky01", (BATTLE_ARENA_SIZE[0] / 2, BATTLE_ARENA_SIZE[1] / 2), (1.0, 0.0), False),
                                    ("mountain3", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS - 2500), (0.95, 0.98), False),
                                    ("plains3", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 400), (0.95, 0.95), False),
                                    ("plains2", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 1000), (0.8, 0.9), False),
                                    ("plains1", (BATTLE_ARENA_SIZE[0] / 2, FLOOR_POS + 1200), (0.70, 0.85), False),
                                    ("fort", NEUTRAL_POS, (0.0, 0.0), False)
                                )
                    }
        
        
        normal = itemDict.get((self.terrainLeft, self.terrainRight))
        flipped = itemDict.get((self.terrainRight, self.terrainLeft))
        
        dataList = None
        if (not normal is None):
            dataList = normal
            flipper = 1
        elif (not flipped is None):
            dataList = flipped
            flipper = -1
            
        if dataList is None:
            if (self.terrainLeft == FORTRESS or self.terrainRight == FORTRESS):
                if self.terrainLeft == SNOW or self.terrainRight == SNOW:
                    dataList = itemDict.get((FORTRESS, SNOW))
                else:
                    dataList = itemDict.get((FORTRESS, PLAINS))
            else:
                if self.terrainLeft == SNOW or self.terrainRight == SNOW:
                    dataList = itemDict.get((SNOW, SNOW))
                else:
                    dataList = itemDict.get((PLAINS, PLAINS))
            
        for data in dataList:
            imageData = SCENERY_IMAGES[data[0]]
            image = imageData[0]
            anchor = imageData[1]
            pos = data[1]
            scale = data[2]
            isFore = data[3]
                
            if isFore:
                itemList = self.foregroundItems
            else:
                itemList = self.backgroundItems
            item = SceneryItem(image, pos, anchor, scale)
            itemList.append(item)
            
        
        
    def update(self):
        pass
    
    def drawForeground(self, screen, inOffset):
        self.draw(self.foregroundItems, screen, inOffset)
    
    def drawBackground(self, screen, inOffset):
        self.draw(self.backgroundItems, screen, inOffset)
        
    def draw(self, itemList, screen, inOffset):
        
        for item in itemList:
            item.draw(screen, inOffset)
        
    
    
    
class SceneryItem(object):
    def __init__(self, image, pos, anchor, scale):
        
        self.image = image
        self.scale = scale
        
        self.rect = pygame.Rect(pos, image.get_size())
        self.rect.left -= anchor[0]
        self.rect.top -= anchor[1]
        self.anchor = anchor
        
        print self.rect.topleft
        
    def draw(self, screen, inOffset):
        rect = pygame.Rect(self.rect.topleft, self.rect.size)
        rect.left += inOffset[0]
        rect.top += inOffset[1]
        
        adjust = [0.0, 0.0]
        for i in range(2):
            screenCenter = (SCREEN_SIZE[i] / 2) - inOffset[i]
            if (i == 1):
                screenCenter += BATTLE_AREA_FLOOR_HEIGHT
            anchoredPos = self.rect.topleft[i] + self.anchor[i]
            difference = screenCenter - anchoredPos
            adjust[i] = (difference * self.scale[i])
            
        rect.left += adjust[0]
        rect.top += adjust[1]
        
        screen.blit(self.image, rect.topleft)
        
    
    
