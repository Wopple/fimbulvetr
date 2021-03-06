import os
import sys
import pygame

from common.constants import *
from client.constants import *

import copy

import time

import mapstructure

class GameMap(object):
    def __init__(self, num, name, startingPoints, mapSize, horizAxis, flip,
                 mountains, water, forests, islands, rivers,
                 structures, fimbulvetrSpeed, fimbulvetrDelay,
                 fimbulvetrSpreadSpeed, fimbulvetrSpreadGrowth):

        self.num = num
        self.name = name
        self.horizAxis = horizAxis
        self.flip = flip
        
        self.fimbulvetrSpeed = fimbulvetrSpeed
        self.fimbulvetrDelay = fimbulvetrDelay
        self.fimbulvetrSpreadSpeed = fimbulvetrSpreadSpeed
        self.fimbulvetrSpreadGrowth = fimbulvetrSpreadGrowth
        

        if horizAxis:
            self.mapSize = [mapSize[0], mapSize[1] * 2]
        else:
            self.mapSize = [mapSize[0] * 2, mapSize[1]]

        self.primaryTerrain = 0

        self.surfaceTemplate = pygame.Surface(self.mapSize)
        self.surfaceTemplate.fill(TERRAIN_COLORS[self.primaryTerrain])

        self.mountains = mountains
        self.water = water
        self.forests = forests
        self.islands = islands
        self.rivers = rivers
        self.structures = structures

        self.testCircles = []

        self.mirror(self.mountains)
        self.mirror(self.water)
        self.mirror(self.forests)
        self.mirror(self.islands)
        self.mirror(self.rivers)
        self.mirror(self.structures)

        self.mirrorStartingPoints(startingPoints)

        self.createTerrainMasterList()

    def mirror(self, inList):
        temp = []

        for i in inList:
            p, t = self.flipPoint(i[0])
            if not t:
                temp.append( (p, i[1]) )

        for i in temp:
            inList.append(i)

    def mirrorStartingPoints(self, inPoints):
        self.startingPoints = []

        temp = []
        for i in inPoints:
            temp.append(i)

        self.startingPoints.append(temp)

        temp = []
        for i in inPoints:
            p, t = self.flipPoint(i)
            temp.append(p)

        self.startingPoints.append(temp)

    def flipPoint(self, p):
        if self.flip:
            if self.horizAxis:
                x = p[0]
                y = self.mapSize[1] - p[1]
                t = (y == p[1])
            else:
                x = self.mapSize[0] - p[0]
                y = p[1]
                t = (x == p[0])

        return (x, y), t

    def createTerrainMasterList(self):
        self.terrainMasterList = []

        orderToAdd = [[self.rivers, WATER], [self.forests, FOREST],
                      [self.mountains, MOUNTAIN], [self.islands, PLAINS],
                      [self.water, WATER]]

        for o in orderToAdd:
            for i in range(len(o[0])):
                self.terrainMasterList.append([o[0][i], o[1]])


    def numOfCharactersPerTeam(self):
        return len(self.startingPoints[0])
        

def getMap(s):
    try:
        i = int(s)
    except:
        return None

    if i == 0:
        name = "Lake of Origins"
        startingPoints = [(62, 102),
                          (99, 65),
                          (20, 68),
                          (77, 19),
                          (160, 27)]
        
        mapSize = (3000, 990)
        horizAxis = True
        flip = True
        
        fimbulvetrDelay = 45*40
        fimbulvetrSpeed = 6
        fimbulvetrSpreadSpeed = 2
        fimbulvetrSpreadGrowth = 1
        
        mountains = [((-20, 420), 125),
                     ((60, 435), 80),
                     ((50, 470), 70),
                     ((12, 512), 45),
                     ((975, 289), 100),
                     ((981, 204), 70),
                     ((1007, 148), 45),
                     ((1067, 212), 95),
                     ((1054, 359), 95),
                     ((1175, 345), 110),
                     ((1255, 283), 75),
                     ((1200, 213), 90),
                     ((1255, 223), 65),
                     ((1132, 167), 55),
                     ((971, 147), 20),
                     ((1037, 131), 20),
                     ((1101, 139), 20),
                     ((228, 393), 20),
                     ((246, 398), 20),
                     ((252, 418), 35),
                     ((256, 455), 30),
                     ((251, 493), 25),
                     ((231, 519), 20),
                     ((218, 545), 20),
                     ((236, 544), 25),
                     ((248, 517), 10),
                     ((261, 559), 20),
                     ((279, 574), 15),
                     ((294, 583), 15),
                     ((307, 597), 15),
                     ((323, 597), 15),
                     ((323, 610), 15),
                     ((339, 603), 15),
                     ((357, 602), 15),
                     ((322, 593), 15),
                     ((2742, 377), 60),
                     ((2729, 432), 75),
                     ((2680, 529), 85),
                     ((2665, 616), 95),
                     ((2637, 713), 115),
                     ((2595, 800), 120),
                     ((2647, 809), 115),
                     ((2721, 819), 110),
                     ((2740, 727), 105),
                     ((2762, 608), 90),
                     ((2768, 491), 80),
                     ((2842, 197), 70),
                     ((2901, 146), 95),
                     ((2945, 39), 90),
                     ((2997, 45), 80),
                     ((3019, 120), 80),
                     ((2925, 229), 70),
                     ((3034, 248), 85),
                     ((3009, 305), 95),
                     ((3079, 323), 80),
                     ((3024, 407), 80),
                     ((3049, 505), 90),
                     ((3107, 422), 95),
                     ((3092, 197), 80),
                     ((3045, 619), 85),
                     ((3027, 746), 90),
                     ((3022, 834), 80),
                     ((3127, 802), 80),
                     ((3135, 590), 80),
                     ((3124, 719), 90),
                     ((3163, 479), 80),
                     ((3096, 841), 70),
                     ((2995, 891), 50),
                     ((3019, 947), 50),
                     ((2468, 824), 50),
                     ((2427, 870), 50),
                     ((2387, 905), 50),
                     ((2441, 903), 50),
                     ((2499, 879), 70),
                     ((2588, 878), 60),
                     ((2340, 916), 35),
                     ((2295, 923), 30),
                     ((2261, 919), 20),
                     ((2233, 905), 20),
                     ((915, 224), 20),
                     ((930, 204), 20),
                     ((907, 340), 20),
                     ((1108, 431), 20),
                     ((1088, 435), 20),
                     ((1137, 419), 30),
                     ((1279, 361), 10),
                     ((1290, 350), 10),
                     ((1258, 403), 20),
                     ((1236, 424), 20),
                     ((1176, 444), 20),
                     ((1264, 173), 20)
                     ]
        
        water = [((32, 732), 135),
                 ((140, 686), 105),
                 ((206, 743), 160),
                 ((338, 708), 80),
                 ((434, 722), 95),
                 ((512, 679), 105),
                 ((579, 653), 120),
                 ((702, 555), 130),
                 ((594, 564), 50),
                 ((371, 873), 115),
                 ((211, 899), 125),
                 ((43, 921), 141),
                 ((522, 885), 188),
                 ((693, 749), 108),
                 ((736, 580), 116),
                 ((761, 635), 116),
                 ((787, 691), 124),
                 ((786, 749), 148),
                 ((730, 899), 148),
                 ((341, 993), 95),
                 ((927, 777), 90),
                 ((892, 884), 170),
                 ((880, 990), 235),
                 ((870, 595), 100),
                 ((931, 721), 115),
                 ((912, 771), 145),
                 ((984, 820), 80),
                 ((1525, 234), 50),
                 ((1592, 188), 70),
                 ((1657, 217), 130),
                 ((1817, 241), 125),
                 ((2359, 314), 110),
                 ((2088, 180), 100),
                 ((2227, 294), 120),
                 ((2312, 210), 100),
                 ((2183, 174), 80),
                 ((1969, 214), 100),
                 ((1840, 162), 80),
                 ((1744, 141), 80),
                 ((2021, 144), 80),
                 ((1938, 139), 70),
                 ((1995, 301), 80),
                 ((2111, 321), 100),
                 ((1881, 291), 70),
                 ((2101, 327), 60),
                 ((2232, 402), 100),
                 ((2454, 374), 90),
                 ((2372, 446), 155),
                 ((2425, 281), 115),
                 ((2363, 203), 75),
                 ((1525, 183), 10),
                 ((1682, 97), 15),
                 ((1708, 323), 20),
                 ((1744, 317), 30),
                 ((1924, 339), 20),
                 ((1859, 345), 20),
                 ((2039, 364), 30),
                 ((2011, 369), 20),
                 ((2135, 416), 20),
                 ((2228, 497), 20),
                 ((2238, 135), 20),
                 ((2263, 134), 20),
                 ((2147, 112), 20),
                 ((1888, 107), 20)
                 ]
        
        forests = [((220, 225), 80),
                   ((240, 200), 65),
                   ((275, 200), 70),
                   ((290, 200), 72),
                   ((591, 185), 48),
                   ((654, 235), 60),
                   ((608, 238), 60),
                   ((662, 280), 52),
                   ((707, 292), 36),
                   ((1232, 633), 90),
                   ((1278, 694), 90),
                   ((1325, 617), 85),
                   ((1367, 703), 70),
                   ((1532, 965), 95),
                   ((1528, 997), 95),
                   ((1580, 932), 95),
                   ((1628, 965), 115),
                   ((1700, 952), 90),
                   ((1558, 654), 75),
                   ((1598, 616), 75),
                   ((1630, 682), 75),
                   ((1698, 677), 90),
                   ((1775, 703), 125),
                   ((1886, 742), 120),
                   ((1739, 599), 155),
                   ((1889, 600), 165),
                   ((1429, 979), 90),
                   ((1454, 1041), 90),
                   ((1970, 850), 95),
                   ((2045, 843), 110),
                   ((2002, 724), 70),
                   ((834, 736), 50),
                   ((880, 707), 50),
                   ((877, 756), 45),
                   ((835, 792), 40),
                   ((904, 988), 45),
                   ((956, 973), 50),
                   ((230, 945), 30),
                   ((250, 973), 35),
                   ((212, 959), 30),
                   ((102, 945), 25),
                   ((67, 970), 30),
                   ((98, 983), 25),
                   ((205, 977), 30)
                   ]

        islands = [((127, 955), 60),
                   ((184, 936), 75),
                   ((229, 956), 60),
                   ((614, 978), 30),
                   ((632, 967), 40),
                   ((600, 939), 35),
                   ((640, 936), 30),
                   ((483, 842), 30),
                   ((501, 830), 30),
                   ((535, 814), 30),
                   ((524, 838), 20),
                   ((563, 807), 35),
                   ((592, 798), 40),
                   ((620, 809), 30),
                   ((635, 996), 45),
                   ((124, 998), 90),
                   ((235, 980), 70),
                   ((909, 743), 75),
                   ((828, 734), 65),
                   ((834, 788), 75),
                   ((865, 673), 60),
                   ((889, 1015), 50),
                   ((917, 1015), 55),
                   ((957, 1015), 55),
                   ((987, 1011), 40),
                   ((72, 986), 65)
                   ]
        
        rivers = [((427, 131), 28),
                  ((429, 155), 22),
                  ((452, 147), 36),
                  ((448, 174), 32),
                  ((478, 194), 16),
                  ((487, 196), 18),
                  ((451, 108), 18),
                  ((457, 97), 15),
                  ((470, 87), 15),
                  ((482, 83), 12),
                  ((492, 75), 9),
                  ((503, 67), 9),
                  ((513, 61), 8),
                  ((523, 54), 8),
                  ((534, 43), 16),
                  ((541, 33), 20),
                  ((548, 13), 24),
                  ((552, 25), 32),
                  ((460, 205), 20),
                  ((434, 207), 30),
                  ((401, 214), 15),
                  ((389, 208), 15),
                  ((370, 208), 20),
                  ((360, 224), 15),
                  ((347, 205), 20),
                  ((324, 190), 15),
                  ((311, 188), 15),
                  ((297, 187), 13),
                  ((283, 198), 12),
                  ((280, 213), 15),
                  ((262, 216), 15),
                  ((249, 205), 12),
                  ((252, 193), 9),
                  ((246, 185), 9),
                  ((233, 181), 10),
                  ((220, 187), 12),
                  ((209, 193), 12),
                  ((195, 192), 16),
                  ((207, 211), 14),
                  ((211, 229), 20),
                  ((221, 249), 20),
                  ((208, 269), 20),
                  ((190, 291), 18),
                  ((185, 310), 14),
                  ((176, 324), 16),
                  ((164, 336), 14),
                  ((154, 353), 12),
                  ((144, 373), 14),
                  ((158, 367), 12),
                  ((154, 386), 14),
                  ((156, 401), 14),
                  ((164, 411), 10),
                  ((182, 420), 14),
                  ((188, 439), 16),
                  ((180, 460), 14),
                  ((168, 466), 18),
                  ((155, 488), 20),
                  ((179, 491), 24),
                  ((184, 456), 26),
                  ((193, 476), 18),
                  ((160, 509), 12),
                  ((152, 559), 12),
                  ((152, 547), 12),
                  ((149, 534), 12),
                  ((155, 518), 12),
                  ((151, 504), 10),
                  ((137, 577), 18),
                  ((152, 584), 20),
                  ((595, 35), 60),
                  ((641, 33), 85),
                  ((700, 18), 60),
                  ((764, 11), 35),
                  ((812, -22), 65),
                  ((1119, 239), 15),
                  ((1127, 215), 20),
                  ((1118, 200), 15),
                  ((1136, 190), 25),
                  ((1140, 159), 15),
                  ((1155, 145), 15),
                  ((1158, 127), 15),
                  ((1175, 118), 15),
                  ((1159, 105), 15),
                  ((1149, 95), 15),
                  ((1145, 82), 15),
                  ((1131, 66), 15),
                  ((1113, 57), 15),
                  ((1095, 65), 15),
                  ((1079, 75), 15),
                  ((1063, 67), 24),
                  ((1030, 59), 21),
                  ((1013, 47), 18),
                  ((996, 40), 12),
                  ((977, 33), 15),
                  ((961, 35), 12),
                  ((939, 39), 18),
                  ((923, 37), 12),
                  ((905, 35), 12),
                  ((892, 31), 12),
                  ((851, 23), 24),
                  ((879, 33), 15),
                  ((1043, 338), 15),
                  ((786, 487), 36),
                  ((813, 505), 42),
                  ((836, 510), 39),
                  ((852, 473), 16),
                  ((860, 454), 16),
                  ((856, 438), 12),
                  ((859, 426), 12),
                  ((868, 420), 12),
                  ((880, 409), 16),
                  ((893, 405), 16),
                  ((907, 404), 16),
                  ((928, 403), 16),
                  ((950, 396), 16),
                  ((961, 392), 16),
                  ((973, 385), 16),
                  ((983, 378), 16),
                  ((995, 367), 16),
                  ((993, 352), 16),
                  ((1012, 367), 16),
                  ((1017, 347), 12),
                  ((1034, 342), 12),
                  ((1055, 352), 16),
                  ((2525, 480), 12),
                  ((2539, 475), 10),
                  ((2550, 475), 10),
                  ((2545, 486), 8),
                  ((2558, 488), 12),
                  ((2563, 479), 8),
                  ((2568, 493), 12),
                  ((2575, 499), 8),
                  ((2582, 508), 8),
                  ((2590, 511), 8),
                  ((2600, 511), 5),
                  ((2609, 507), 8),
                  ((2616, 511), 8),
                  ((2625, 516), 8),
                  ((2624, 525), 9),
                  ((2631, 527), 7),
                  ((2643, 535), 8),
                  ((2646, 545), 8),
                  ((2637, 531), 7),
                  ((2537, 483), 11),
                  ((2520, 470), 18),
                  ((2511, 491), 18),
                  ((1481, 229), 20),
                  ((1481, 243), 25),
                  ((1493, 257), 28),
                  ((1455, 237), 10),
                  ((1442, 244), 11),
                  ((1426, 250), 10),
                  ((1412, 242), 11),
                  ((1403, 239), 8),
                  ((1432, 243), 8),
                  ((1392, 246), 9),
                  ((1380, 243), 10),
                  ((1368, 240), 8),
                  ((1357, 239), 8),
                  ((1342, 242), 13),
                  ((1333, 253), 11),
                  ((1346, 258), 13),
                  ((1334, 238), 9),
                  ((1318, 256), 7),
                  ((1307, 256), 6),
                  ((1297, 257), 5),
                  ((1289, 260), 6),
                  ((1301, 254), 6),
                  ((1283, 264), 5),
                  ((1282, 260), 4),
                  ((1276, 263), 7),
                  ((1266, 265), 6)]

        structures = [((77, 19), "O"),
                      ((388, 483), "F"),
                      ((2245, 750), "F"),
                      ((814, 191), "S"),
                      ((151, 990), "S"),
                      ((1340, 990), "F"),
                      ((1840, 990), "S"),
                      ((1404, 200), "A"),
                      ((2875, 990), "A"),
                      ((2644, 223), "S")]
        
    else:
        return None

    return GameMap(i, name, startingPoints, mapSize, horizAxis, flip,
                   mountains, water, forests, islands, rivers,
                   structures, fimbulvetrSpeed, fimbulvetrDelay,
                   fimbulvetrSpreadSpeed, fimbulvetrSpreadGrowth)
    
def getMapList():
    return [getMap("00")]

def drawMap(inMap, isNormal):
    
    if isNormal:
        colorIndex = 0
    else:
        colorIndex = 1
    
    mapImage = pygame.Surface.copy(inMap.surfaceTemplate)
    mapImage.fill(TERRAIN_COLORS[colorIndex])
        
    for i in inMap.water:
        pygame.draw.circle(mapImage, WATER_FILL_COLORS[colorIndex], i[0], i[1])
    for i in inMap.islands:
        pygame.draw.circle(mapImage, TERRAIN_COLORS[colorIndex], i[0], i[1])
    for i in inMap.mountains:
        pygame.draw.circle(mapImage, MOUNTAIN_FILL_COLORS[colorIndex], i[0], i[1])
    for i in inMap.forests:
        pygame.draw.circle(mapImage, FOREST_FILL_COLORS[colorIndex], i[0], i[1])
    for i in inMap.rivers:
        pygame.draw.circle(mapImage, WATER_FILL_COLORS[colorIndex], i[0], i[1])

    if DEBUG_MODE:
        for m in range(2):
            for n in range(2):
                for i in inMap.testCircles:
                    if i[2] == m and i[3] == n:
                        pygame.draw.circle(mapImage, TEST_CIRCLE_COLORS[m][n],
                                           i[0], i[1])
                
    if isNormal:        
        mapImage = fillPattern(mapImage, TERRAIN_FILL_GRAPHICS[0], TERRAIN_COLORS[colorIndex])
        mapImage = fillPattern(mapImage, TERRAIN_FILL_GRAPHICS[1], WATER_FILL_COLORS[colorIndex])
    
    return mapImage


def fillPattern(baseImage, patternImage, replaceColor):
    baseSize = baseImage.get_size()
    patternSize = patternImage.get_size()
    
    baseImage.set_colorkey(replaceColor)
    
    back = pygame.Surface(baseImage.get_size())
    for x in range(0, baseSize[0], patternSize[0]):
        for y in range(0, baseSize[1], patternSize[1]):
            back.blit(patternImage, (x, y))
    
    
    canvas = pygame.Surface(baseImage.get_size())
    canvas.blit(back, (0, 0))
    canvas.blit(baseImage, (0, 0))
    
    return canvas
    

