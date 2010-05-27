import os
import pygame
import sys

FULL_SCREEN = False
FRAME_RATE = 40
SCREEN_SIZE = (800, 700)
ENTIRE_SCREEN = pygame.Rect( (0,0), SCREEN_SIZE )
DEBUG_MODE = True

pygame.init()
pygame.mixer.init()

if FULL_SCREEN:
    screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Fimbulvetr: War of the Great Winter")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (252, 252, 252)

BLACK_SCREEN = pygame.Surface(SCREEN_SIZE)
BLACK_SCREEN.fill(BLACK, (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

RED_DOT = pygame.Surface((1, 1))
RED_DOT.fill((250, 0, 0))
SHOW_RED_DOT = True

MAP_CHAR_TOKEN_SIZE = (32, 32)

TERRAIN_COLORS = [ (15, 91, 20),
                   (230, 230, 230) ]

ZOOM_CLICK = 0.9
ZOOM_MAX = 1.0
ZOOM_MIN = 0.15

MOUNTAIN_FILL_COLOR = (99, 84, 61)

SCROLL_AREA_WIDTH = 15
SCROLL_SPEED = 10

KEY_BUFFER = 4

MULTIPLAYER_PORT = 1338
NET_MESSAGE_SIZE = 14

BATTLE_AREA_FLOOR_HEIGHT = 200

PROJECTILE_SCREEN_ALLOWANCE = 100

HEALTH_BAR_POSITION = (15, 15)
HEALTH_BAR_SIZE = (250, 25)
HEALTH_BAR_BORDERS = (6, 4)
HEALTH_BAR_COLORS = ( (5, 120, 10),
                      (15, 200, 25),
                      (15, 200, 25),
                      (20, 20, 20),
                      (200, 200, 10),
                      (10, 10, 10))
HEALTH_BAR_PULSE = 2

HARE_ENERGY_MAX = 200
HARE_ENERGY_USAGE = 100
HARE_ENERGY_BATTLE_START = 200
HARE_ENERGY_DELAY = 50
HARE_ENERGY_RECHARGE = 1
HARE_ENERGY_NAME = "Cancel"

SPECIAL_BAR_OFFSET = 15
SPECIAL_BAR_SIZE = (250, 16)
SPECIAL_BAR_BORDERS = (3, 2)
SPECIAL_BAR_COLORS = ( (0, 183, 240),
                      (0, 185, 245),
                      (20, 210, 253),
                      (20, 20, 20),
                      (200, 200, 10),
                      (10, 10, 10))
SPECIAL_BAR_PULSE = 5

DIREC_FONTS = "fonts"
DIREC_GRAPHICS = "graphics"
DIREC_BACKGROUNDS = os.path.join(DIREC_GRAPHICS, "backgrounds")
DIREC_CHARACTER_GRAPHICS = os.path.join(DIREC_GRAPHICS, "characters")
DIREC_HARE_GRAPHICS = os.path.join(DIREC_CHARACTER_GRAPHICS, "hare")
DIREC_FOX_GRAPHICS = os.path.join(DIREC_CHARACTER_GRAPHICS, "fox")

temp = []
BACKGROUNDS = []
for i in temp:
    BACKGROUNDS.append(pygame.image.load(os.path.join(DIREC_BACKGROUNDS, i)).convert_alpha())

temp = [ ["00.png", (24, 62)],
         ["01.png", (24, 62)],
         ["02.png", (24, 63)],
         ["03.png", (24, 63)],
         ["04.png", (24, 63)],
         ["05.png", (24, 63)],
         ["06.png", (24, 63)],
         ["07.png", (24, 63)],
         ["08.png", (14, 68)],
         ["09.png", (17, 58)],
         ["10.png", (21, 50)],
         ["11.png", (27, 58)],
         ["12.png", (27, 58)],
         ["13.png", (27, 58)],
         ["14.png", (35, 75)],
         ["15.png", (35, 75)],
         ["16.png", (35, 75)],
         ["17.png", (35, 75)],
         ["18.png", (35, 75)],
         ["19.png", (23, 45)],
         ["20.png", (23, 45)],
         ["21.png", (23, 45)],
         ["22.png", (23, 45)],
         ["23.png", (23, 45)],
         ["24.png", (23, 45)],
         ["25.png", (20, 50)],
         ["26.png", (20, 50)],
         ["27.png", (20, 50)],
         ["28.png", (20, 50)],
         ["29.png", (30, 53)],
         ["30.png", (30, 53)],
         ["31.png", (30, 53)],
         ["32.png", (30, 53)],
         ["33.png", (23, 45)],
         ["34.png", (23, 45)],
         ["35.png", (17, 73)],
         ["36.png", (17, 73)],
         ["37.png", (17, 73)],
         ["38.png", (17, 73)],
         ["39.png", (17, 73)],
         ["40.png", (17, 73)],
         ["41.png", (43, 61)],
         ["42.png", (43, 61)],
         ["43.png", (43, 61)],
         ["44.png", (43, 61)],
         ["45.png", (43, 61)],
         ["46.png", (39, 73)],
         ["47.png", (39, 73)],
         ["48.png", (39, 73)],
         ["49.png", (39, 73)],
         ["50.png", (39, 73)],
         ["51.png", (53, 75)],
         ["52.png", (53, 75)],
         ["53.png", (53, 75)],
         ["54.png", (53, 75)],
         ["55.png", (14, 68)],
         ["56.png", (14, 68)],
         ["57.png", (14, 68)],
         ["58.png", (14, 68)],
         ["59.png", (30, 64)],
         ["60.png", (30, 64)],
         ["61.png", (30, 64)],
         ["62.png", (30, 64)],
         ["63.png", (30, 64)],
         ["64.png", (30, 64)],
         ["65.png", (30, 64)],
         ["66.png", (24, 62)],
         ["67.png", (14, 68)] ]

HARE_IMAGES = []
for i in temp:
    HARE_IMAGES.append([pygame.image.load(os.path.join(DIREC_HARE_GRAPHICS, i[0])).convert_alpha(), i[1]])

temp = [ ["00.png", (43, 67)],
         ["01.png", (43, 67)],
         ["02.png", (43, 67)],
         ["03.png", (43, 67)],
         ["04.png", (43, 67)],
         ["05.png", (43, 67)],
         ["06.png", (43, 67)],
         ["07.png", (38, 67)],
         ["08.png", (43, 69)],
         ["09.png", (43, 69)],
         ["10.png", (43, 69)],
         ["11.png", (43, 69)],
         ["12.png", (43, 69)],
         ["13.png", (43, 69)],
         ["14.png", (43, 69)],
         ["15.png", (43, 69)],
         ["16.png", (4, 2)],
         ["17.png", (3, 2)],
         ["18.png", (4, 3)],
         ["19.png", (4, 4)],
         ["20.png", (3, 2)],
         ["21.png", (3, 4)],
         ["22.png", (7, 4)],
         ["23.png", (7, 7)],
         ["24.png", (3, 7)]]

FOX_IMAGES = []
for i in temp:
    FOX_IMAGES.append([pygame.image.load(os.path.join(DIREC_FOX_GRAPHICS, i[0])).convert_alpha(), i[1]])

temp = [ ["fontdata.ttf",10],
         ["fontbars.ttf", 14] ]
FONTS = []
for i in temp:
    FONTS.append(pygame.font.Font(
        os.path.join(DIREC_FONTS, i[0]), i[1]))

MINIMENU_FONT = FONTS[0]
ENERGY_BAR_FONT = FONTS[1]


def add_points(i, j):
    return ( (i[0] + j[0]), (i[1] + j[1]) )

def mirror_points(i, j):
    return ( (i[0] - j[0]), (i[1] + j[1]) )

def sub_points(i, j):
    return ( (i[0] - j[0]), (i[1] - j[1]) )
