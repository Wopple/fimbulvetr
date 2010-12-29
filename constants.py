import os
import pygame
import sys

FULL_SCREEN = False
FRAME_RATE = 40
SCREEN_SIZE = (800, 600)
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
ALMOST_BLACK = (3, 3, 3)

BLACK_SCREEN = pygame.Surface(SCREEN_SIZE)
BLACK_SCREEN.fill(BLACK, (0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

RED_DOT = pygame.Surface((1, 1))
RED_DOT.fill((250, 0, 0))

MAIN_MENU_COLOR_ON = (0, 183, 239)
MAIN_MENU_COLOR_OFF = (10, 10, 10)
MAIN_MENU_COLOR_BG = (60, 100, 120)
MAIN_MENU_OFFSET_FROM_SIDE = 50
MAIN_MENU_FADE_SPEED = 5

CHAR_EDITOR_COLOR_ON = (25, 189, 18)
CHAR_EDITOR_COLOR_OFF = (250, 250, 250)
CHAR_EDITOR_COLOR_BG = (96, 75, 55)
CHAR_EDITOR_NUM_PER_PAGE = 12
CHAR_EDITOR_BLACK_PANEL_COLOR = (30, 30, 30)

TEXT_ENTRY_LENGTH_MAX = 20
TEXT_ENTRY_LINE_WIDTH = 350

MAIN_MENU_TITLE_POS = [ ((SCREEN_SIZE[0] / 6), 10),
                        ((SCREEN_SIZE[0] / 6), 50) ]

INTRO_MAX_FADE = 240
INTRO_SPEEDS = [4, 30, 5, 50, 5, 15]

SHOW_RED_DOT = True
SHOW_HURTBOXES = True
SHOW_HITBOXES = True
SHOW_BATTLE_TRIGGER_AREA = False

MAP_INTERFACE_ALPHA_MIN = 50
MAP_INTERFACE_ALPHA_TICK = 10

MAP_CHAR_BAR_COLOR_BG = [(10, 80, 200, 255),
                         (210, 20, 20, 255)]
MAP_CHAR_BAR_COLOR_BORDER = [(0, 0, 150, 255),
                             (150, 0, 0, 255)]
MAP_CHAR_BAR_COLOR_SELECTED = (250, 250, 250, 255)
MAP_CHAR_BAR_BORDER = 5
MAP_CHAR_BAR_PADDING = 10
MAP_CHAR_BAR_PADDING_SMALL = 4
MAP_CHAR_BAR_SPACING = 8
MAP_CHAR_BAR_INIT_POS = (20, 20)
MAP_CHAR_BAR_PORTRAIT_SIZE = (40, 40)
MAP_CHAR_BAR_ENERGY_BAR_SIZE = (140, 12)
MAP_CHAR_BAR_ENERGY_BAR_BORDERS = (2, 2)

TEXT_ENTRY_BORDER_SIZE = 10

MAP_CHAR_TOKEN_SIZE = (32, 32)
TOKEN_BORDER_NEUTRAL = (153, 153, 153, 255)

TOKEN_BORDER_HIGHLIGHTED = [(10, 80, 200, 255),
                            (210, 20, 20, 255)]

TOKEN_BORDER_OFF = [(0, 0, 150, 255),
                   (150, 0, 0, 255)]

TOKEN_BORDER_SELECTED = (250, 250, 250, 255)

TERRAIN_COLORS = [ (18, 109, 24, 255),
                   (230, 230, 230, 255) ]


ZOOM_CLICK = 0.9
ZOOM_MAX = 1.0
ZOOM_MIN = 0.15

MOUNTAIN_FILL_COLOR = (99, 84, 61)
WATER_FILL_COLOR = (39, 69, 209)
FOREST_FILL_COLOR = (12, 69, 16)

SCROLL_AREA_WIDTH = 15
SCROLL_SPEED = 18

BATTLE_TRIGGER_RANGE = 100
BATTLE_TRIGGER_AREA_COLOR = (200, 10, 10)
BATTLE_TRIGGER_AREA_ALPHA = 100
BATTLE_TRIGGER_AREA_COLOR_WITH_ALPHA = (BATTLE_TRIGGER_AREA_COLOR[0],
                                        BATTLE_TRIGGER_AREA_COLOR[1],
                                        BATTLE_TRIGGER_AREA_COLOR[2],
                                        BATTLE_TRIGGER_AREA_ALPHA)
RETREAT_DISTANCE = 80

PAUSE_PLAY_RESIZE_FACTOR = 0.6
PAUSE_PLAY_BIG_FROM_TOP = 10
PAUSE_PLAY_LITTLE_ADJUSTMENT = (25, 20)
PAUSE_PLAY_LITTLE_COLORS = [(10, 80, 200, 255),
                            (210, 20, 20, 255)]
PAUSE_PLAY_ORIG_COLOR = (255, 180, 20, 255)
PAUSE_PLAY_MOVEMENT_SPEED = 3
PAUSE_PLAY_MOVEMENT_DISTANCE = 25

KEY_BUFFER = 4

BATTLE_AREA_FLOOR_HEIGHT = 200
BATTLE_PLAYER_START_DISTANCE = 300

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
RETREAT_BAR_SIZE = (100, 25)
RETREAT_BAR_BORDERS = (6, 4)
RETREAT_BAR_COLORS = ( (236, 209, 13),
                       (236, 209, 13),
                       (236, 209, 13),
                       (20, 20, 20),
                       (200, 200, 10),
                       (10, 10, 10))

SUPER_BAR_COLORS = ( (90, 30, 172),
                     (138, 74, 223),
                     (138, 74, 223),
                     (20, 20, 20),
                     (200, 200, 10),
                     (10, 10, 10) )

RETREAT_PROHIBIT_TIME = FRAME_RATE * 12
RETREAT_HOLD_TIME = int(FRAME_RATE * 1.5)
RETREAT_RECEED = 3
RETREAT_TEAM_COLORS = [(10, 80, 200, 255),
                            (210, 20, 20, 255)]

SUPER_ENERGY_MAX = 100

BATTLE_EDGE_COLLISION_WIDTH = 20

HARE_ENERGY_MAX = 200
HARE_ENERGY_USAGE = 100
HARE_ENERGY_BATTLE_START = 200
HARE_ENERGY_DELAY = 50
HARE_ENERGY_RECHARGE = 1
HARE_ENERGY_NAME = "Cancel"

CAT_ENERGY_MAX = 1200
CAT_ENERGY_USAGE = 3
CAT_ENERGY_BATTLE_START = 700
CAT_ENERGY_DELAY = 30
CAT_ENERGY_RECHARGE = 16
CAT_ENERGY_NAME = "Galdr Blade"

CAT_ENERGY_SECTIONS = (350, 850)
CAT_ENERGY_BAR_COLORS = ( (10, 150, 10),
                          (255, 194, 15),
                          (180, 10, 10) )

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

ATTACK_PROPERTIES = [ "melee",
                      "projectile"  ]

HURTBOX_COLOR = (255, 242, 5)
HURTBOX_ALPHA = 100
HITBOX_COLOR = (255, 10, 10)
HITBOX_ALPHA = 100

DEFAULT_HITSTUN = 2

MULTIPLAYER_PORT = 1338
NET_MESSAGE_SIZE = 14
NET_ICON_SPEED = 8

MAP_MODE_NET_MESSAGE_SIZE = 30

CHARACTER_SELECT_BG_COLOR = (40, 40, 40)
CHARACTER_SELECT_PANEL_COLOR_FILL = (165, 130, 50)
CHARACTER_SELECT_PANEL_COLOR_BORDER = (90, 68, 35)
CHARACTER_SELECT_PANEL_SELECTION_BORDER_COLOR = (10, 80, 200)
CHARACTER_SELECTION_FONT_COLOR = (250, 250, 250)
CHARACTER_SELECTION_READY_COLOR = (0, 150, 0)

CHARACTER_SELECTION_BUTTON_COLOR_ON = (250, 250, 250)
CHARACTER_SELECTION_BUTTON_COLOR_OFF = (60, 60, 60)

CHARACTER_SELECT_PANEL_BORDER_SIZE = 4
CHARACTER_SELECT_PANEL_BORDER_WIDTH = 3
CHARACTER_SELECT_PANEL_SELECTION_BORDER_WIDTH = 6
CHARACTER_SELECT_PANEL_SIZE = (250, 35)
CHARACTER_SELECT_PLAYER_SIZE = (300, 35)
CHARACTER_SELECT_BUTTON_SIZE = (150, 35)
CHARACTER_SELECT_PANELS_PER_COL = 5
CHARACTER_SELECT_GROUP_FROM_TOP = 20
CHARACTER_SELECT_GROUP_SPACING = 25

CHARACTER_SELECT_NET_MESSAGE_SIZE = 3
CHARACTER_TRANSFER_NET_MESSAGE_SIZE = 30

CHARACTER_NAME_MAX_LENGTH = 10

COUNTDOWN_COLOR = (244, 210, 11)
MAP_COUNTDOWN_LENGTH = 10
BATTLE_COUNTDOWN_LENGTH = 3


DIREC_FONTS = "fonts"
DIREC_GRAPHICS = "graphics"
DIREC_DATA = "data"
DIREC_CHARACTER_SAVES = os.path.join(DIREC_DATA, "characters")
DIREC_BACKGROUNDS = os.path.join(DIREC_GRAPHICS, "backgrounds")
DIREC_CHARACTER_GRAPHICS = os.path.join(DIREC_GRAPHICS, "characters")
DIREC_HARE_GRAPHICS = os.path.join(DIREC_CHARACTER_GRAPHICS, "hare")
DIREC_FOX_GRAPHICS = os.path.join(DIREC_CHARACTER_GRAPHICS, "fox")
DIREC_CAT_GRAPHICS = os.path.join(DIREC_CHARACTER_GRAPHICS, "cat")
DIREC_INTERFACE_GRAPHICS = os.path.join(DIREC_GRAPHICS, "interface")
DIREC_PORTRAITS = os.path.join(DIREC_GRAPHICS, "portraits")

CHARACTER_FILE_NAME = "char"
CHARACTER_FILE_EXT = "dat"
MAX_CHARACTER_SAVES = 100

STUN_THRESHOLD_1 = 50
STUN_THRESHOLD_2 = 100

HARE_MAP_SPEED_BASE = 2.5
FOX_MAP_SPEED_BASE = 2.0
CAT_MAP_SPEED_BASE = 1.6

#Terrain types
#0 = PLAINS
#1 = FOREST
#2 = MOUNTAIN
#3 = WATER

HARE_MAP_SPEED_MODIFIERS = [1.0,
                            0.8,
                            0.3,
                            0.3]

FOX_MAP_SPEED_MODIFIERS = [1.0,
                           0.85,
                           0.3,
                           0.34]

CAT_MAP_SPEED_MODIFIERS = [1.0,
                            0.8,
                            0.28,
                            0.18]

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
         ["67.png", (14, 68)],
         ["68.png", (26, 62)],
         ["69.png", (27, 62)],
         ["70.png", (25, 66)],
         ["71.png", (25, 66)],
         ["72.png", (25, 66)],
         ["73.png", (25, 66)],
         ["74.png", (25, 66)],
         ["75.png", (43, 74)],
         ["76.png", (43, 74)],
         ["77.png", (43, 74)],
         ["78.png", (43, 74)],
         ["79.png", (43, 74)],
         ["80.png", (43, 74)],
         ["81.png", (22, 56)],
         ["82.png", (17, 58)],
         ["83.png", (17, 58)],
         ["84.png", (17, 58)],
         ["85.png", (17, 58)],
         ["86.png", (16, 48)]]

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

temp = [ ["00.png", (24, 61)],
         ["01.png", (24, 61)],
         ["02.png", (24, 61)],
         ["03.png", (24, 61)],
         ["04.png", (24, 61)],
         ["05.png", (27, 52)],
         ["06.png", (32, 62)],
         ["07.png", (32, 62)],
         ["08.png", (32, 62)],
         ["09.png", (32, 62)],
         ["10.png", (32, 71)],
         ["11.png", (32, 71)],
         ["12.png", (32, 71)],
         ["13.png", (32, 71)],
         ["14.png", (24, 61)],
         ["15.png", (24, 61)],
         ["16.png", (33, 59)],
         ["17.png", (33, 59)],
         ["18.png", (28, 61)],
         ["19.png", (43, 66)],
         ["20.png", (43, 66)],
         ["21.png", (43, 66)],
         ["22.png", (43, 66)],
         ["23.png", (43, 66)],
         ["24.png", (43, 66)],
         ["25.png", (43, 66)],
         ["26.png", (43, 66)],
         ["27.png", (37, 26)],
         ["28.png", (37, 26)],
         ["29.png", (37, 26)],
         ["30.png", (37, 26)],
         ["31.png", (37, 26)],
         ["32.png", (37, 26)],
         ["33.png", (37, 26)],
         ["34.png", (43, 66)],
         ["35.png", (43, 66)],
         ["36.png", (43, 66)],
         ["37.png", (43, 66)],
         ["38.png", (43, 66)],
         ["39.png", (43, 66)],
         ["40.png", (43, 66)],
         ["41.png", (43, 66)],
         ["42.png", (29, 52)]]

CAT_IMAGES = []
for i in temp:
    CAT_IMAGES.append([pygame.image.load(os.path.join(DIREC_CAT_GRAPHICS, i[0])).convert_alpha(), i[1]])


temp = [ ['face1.png', (28, 66)],
         ['face2.png', (28, 66)],
         ['face2.png', (28, 66)] ]

HARE_TOKENS = []
for i in temp:
    HARE_TOKENS.append([pygame.image.load(os.path.join(DIREC_HARE_GRAPHICS, i[0])).convert_alpha(), i[1]])


temp = [ ['face1.png', (40, 46)],
         ['face2.png', (40, 46)],
         ['face2.png', (40, 46)] ]

FOX_TOKENS = []
for i in temp:
    FOX_TOKENS.append([pygame.image.load(os.path.join(DIREC_FOX_GRAPHICS, i[0])).convert_alpha(), i[1]])


temp = [ ['face1.png', (27, 30)],
         ['face2.png', (27, 30)],
         ['face2.png', (27, 30)] ]

CAT_TOKENS = []
for i in temp:
    CAT_TOKENS.append([pygame.image.load(os.path.join(DIREC_CAT_GRAPHICS, i[0])).convert_alpha(), i[1]])
    

temp = ['pauseicon.png',
        'playicon.png',
        'target.png',
        'networking.png',
        'pagearrow.png']

INTERFACE_GRAPHICS = []
for i in temp:
    INTERFACE_GRAPHICS.append(pygame.image.load(os.path.join(
        DIREC_INTERFACE_GRAPHICS, i)).convert_alpha())

temp = ['hare00.png']

HARE_PORTRAITS = []
for i in temp:
    HARE_PORTRAITS.append(pygame.image.load(os.path.join(
        DIREC_PORTRAITS, i)).convert_alpha())


temp = [ ["fontdata.ttf",10],
         ["fontbars.ttf", 14],
         ["fontslab.ttf", 12],
         ["fontslab.ttf", 30],
         ["fontheadline.ttf", 16],
         ["fontbio.ttf", 26],
         ["fontheadline.ttf", 20],
         ["fontheadline.ttf", 50]]
FONTS = []
for i in temp:
    FONTS.append(pygame.font.Font(
        os.path.join(DIREC_FONTS, i[0]), i[1]))

MINIMENU_FONT = FONTS[0]
ENERGY_BAR_FONT = FONTS[1]
MAIN_MENU_FONT = FONTS[4]
CHAR_EDITOR_FONT = FONTS[4]
TEXT_ENTRY_FONT = FONTS[5]
CHARACTER_SELECTION_FONT = FONTS[6]
COUNTDOWN_FONT = FONTS[7]

VALID_INPUT_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                          'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                          'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                          'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                          'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                          'Y', 'Z', '-', '1', '2', '3', '4', '5', '6', '7',
                          '8', '9', '0', '.']


def add_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))
    return ( (i[0] + j[0]), (i[1] + j[1]) )

def mirror_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))
    return ( (i[0] - j[0]), (i[1] + j[1]) )

def sub_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))
    return ( (i[0] - j[0]), (i[1] - j[1]) )

def flipRect(i):
    return ( ((i.left * -1) - i.width), i.top )

def colorSwap(i, color1, color2, tolerance):
    lowerBound = []
    upperBound = []

    for k in range(4):
        c = color1[k]
        
        d = c - tolerance
        if d < 0:
            d = 0
        lowerBound.append(d)

        d = c + tolerance
        if d > 255:
            d = 255
        upperBound.append(d)
    
    size = i.get_size()
    for x in range(size[0]):
        for y in range(size[1]):
            c = i.get_at((x, y))
            variance = []
            for j in range(4):
                if c[j] <= upperBound[j] and c[j] >= lowerBound[j]:
                    variance.append(c[j] - color1[j])
                else:
                    variance.append(None)

            checker = True
            for j in range(4):
                if variance[j] is None:
                    checker = False

            if checker:
                newColor = []
                for j in range(4):
                    temp = color2[j] + variance[j]
                    if temp < 0:
                        temp = 0
                    if temp > 255:
                        temp = 255
                    newColor.append(temp)

                complete = (newColor[0], newColor[1],
                            newColor[2], newColor[3])

                i.set_at((x,y), complete)
