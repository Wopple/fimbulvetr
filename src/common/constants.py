import os

import math

VERSION = "0.1.5"

FRAME_RATE = 40
DEBUG_MODE = True

BATTLE_ARENA_SIZE = (1000, 900)

DASH_BUFFER_MAX = 8

FIMBULVETR_MULTIPLIER = 0.5

RESPAWN_MAX = 75000
RESPAWN_GAIN = 100

BATTLE_TRIGGER_RANGE = 90

STRUCTURE_TRIGGER_RANGE = 65

RETREAT_DISTANCE = 80

KEY_BUFFER = 4

BATTLE_AREA_FLOOR_HEIGHT = 100
BATTLE_PLAYER_START_DISTANCE = 300

PROJECTILE_SCREEN_ALLOWANCE = 100

RETREAT_PROHIBIT_TIME = FRAME_RATE * 8
RETREAT_HOLD_TOTAL = 5000
RETREAT_ADD = 105
RETREAT_ADD_FAST = 170
RETREAT_RECEED = 15
RETREAT_RECEED_FAST = 200

SUPER_ENERGY_MAX = 100000
SUPER_ENERGY_INITIAL_FACTOR = 0
SUPER_ENERGY_GAIN_BASE = 65
SUPER_ENERGY_GAIN_FACTOR = 0.7

SUPER_ENERGY_GAIN_FINAL = [0]

temp = 1.00
for i in range(20):

    SUPER_ENERGY_GAIN_FINAL.append(int(SUPER_ENERGY_GAIN_FINAL[i] +
                                       SUPER_ENERGY_GAIN_BASE * temp))

    temp *= SUPER_ENERGY_GAIN_FACTOR

BATTLE_EDGE_COLLISION_WIDTH = 24

DISPLACEMENT_AMOUNT = 2.2

HARE_ENERGY_MAX = 10000
HARE_ENERGY_USAGE = 3000
HARE_ENERGY_BATTLE_START = 10000
HARE_ENERGY_DELAY = 40
HARE_ENERGY_RECHARGE = 15

CAT_ENERGY_MAX = 1200
CAT_ENERGY_USAGE = 3
CAT_ENERGY_BATTLE_START = 750
CAT_ENERGY_DELAY = 45
CAT_ENERGY_RECHARGE = 24

ATTACK_PROPERTIES = [ "melee",
                      "projectile" ]

DEFAULT_HITSTUN = 2
BLOCKED_KNOCKBACK_FACTOR = 0.9
BLOCKED_LIFT_RESIST = 0.6
BLOCKSTUN_FACTOR = 0.10

PLATFORM_HEIGHT = 25

DEATH_FLY_VERT_VEL_MIN = -12

MAP_PAUSE_TIME_LENGTHS = [10, 20, 25, 10, 999, 10, 40, 10]
BATTLE_ENDING_TIME_LENGTHS = [60, 40, 3, 100, 10]
ENCOUNTER_START_BLINK = 3
ENCOUNTER_END_BLINK = 5

MULTIPLAYER_PORT = 1338
NET_MESSAGE_SIZE = 7
NET_ICON_SPEED = 8

MAP_MODE_NET_MESSAGE_SIZE = 5

CHARACTER_SELECT_NET_MESSAGE_SIZE = 3
CHARACTER_TRANSFER_NET_MESSAGE_SIZE = 30

CHARACTER_NAME_MAX_LENGTH = 10

MAP_COUNTDOWN_LENGTH = 60
ENCOUNTER_COUNTDOWN_LENGTH = 10
BATTLE_COUNTDOWN_LENGTH = 3

TECH_BUFFER_MIN = -10
TECH_BUFFER_MAX = 8

MAP_REGION_SIZE = 100

DIREC_PARENT = ".."
DIREC_RESOURCES = os.path.join(DIREC_PARENT, "resources")
DIREC_DATA = os.path.join(DIREC_RESOURCES, "data")
DIREC_CHARACTER_SAVES = os.path.join(DIREC_DATA, "characters")

CHARACTER_FILE_NAME = "char"
CHARACTER_FILE_EXT = "dat"
MAX_CHARACTER_SAVES = 100

STUN_THRESHOLD_1 = 50
STUN_THRESHOLD_2 = 100
STUN_THRESHOLD_3 = 150

BASE_CHARACTER_SPEED = 1.2

MAX_WAYPOINTS = 10

HARE_MAP_SPEED_BASE = 1.45 * BASE_CHARACTER_SPEED
FOX_MAP_SPEED_BASE = 1.2 * BASE_CHARACTER_SPEED
CAT_MAP_SPEED_BASE = 1.05 * BASE_CHARACTER_SPEED

PLAINS = 0
FOREST = 1
MOUNTAIN = 2
WATER = 3
FORTRESS = 4
SNOW = 5
ICE = 6

HOME_TERRAINS = {"hare" : PLAINS,
                 "fox"  : FOREST,
                 "cat"  : PLAINS}

HOME_TERRAIN_DAMAGE_BONUS = 10
ALTAR_DAMAGE_BONUS = 10
FORTRESS_DAMAGE_BONUS = 15

HARE_MAP_SPEED_TERRAIN_MODIFIERS = [1.0,
                                    0.6,
                                    0.3,
                                    0.3,
                                    1.1,
                                    0.45,
                                    0.7]

FOX_MAP_SPEED_TERRAIN_MODIFIERS = [1.0,
                                   0.7,
                                   0.3,
                                   0.34,
                                   1.1,
                                   0.45,
                                   0.7]

CAT_MAP_SPEED_TERRAIN_MODIFIERS = [1.0,
                                   0.7,
                                   0.32,
                                   0.18,
                                   1.1,
                                   0.45,
                                   0.7]

HARE_MAP_SPEED_TERRITORY_MODIFIERS = {"neutral"   : 1.00,
                                      "allied"    : 1.15,
                                      "enemy"     : 0.90,
                                      "contested" : 0.75 }

FOX_MAP_SPEED_TERRITORY_MODIFIERS  = {"neutral"   : 1.00,
                                      "allied"    : 1.15,
                                      "enemy"     : 0.90,
                                      "contested" : 0.75 }

CAT_MAP_SPEED_TERRITORY_MODIFIERS  = {"neutral"   : 1.00,
                                      "allied"    : 1.15,
                                      "enemy"     : 0.90,
                                      "contested" : 0.75 }

HARE_HEALTH_SPEED_MODIFIER = 0.45
FOX_HEALTH_SPEED_MODIFIER = 0.6
CAT_HEALTH_SPEED_MODIFIER = 0.6

HEALTH_REGAIN_SPEED = 5
FORTRESS_HEALTH_REGAIN_AMOUNT = 6
PASSIVE_HEALTH_REGAIN_AMOUNT = 2

FORTRESS_TERRITORY_RADIUS = 420
SPIRE_TERRITORY_RADIUS = 300
ALTAR_TERRITORY_RADIUS = 180
ORIGIN_TERRITORY_RADIUS = 250

BASE_CAPTURE_RATE = 100
BASE_CAPTURE_DEGRADE = 250
FORTRESS_CAPTURE_TIME = 30000
SPIRE_CAPTURE_TIME = 15000
ALTAR_CAPTURE_TIME = 20000

REZ_TIME = 120

DEATH_FREEZE_FRAME = 20

CHIP_DAMAGE_PERCENTAGE_DEFAULT = 0.25

LOCK_CIRCLE_TICK_MAX = 2
LOCK_CIRCLE_INCREASE = 3
LOCK_CIRCLE_MAX_SIZE = 100

# frame data constants

FD_KEY = 0
FD_LEN = 1
FD_HURT = 2
FD_HIT = 3
FD_BLOCK = 4

def add_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))
    return [ (i[0] + j[0]), (i[1] + j[1]) ]

def mirror_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))
    return [ (i[0] - j[0]), (i[1] + j[1]) ]

def sub_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))
    return [ (i[0] - j[0]), (i[1] - j[1]) ]

def average_points(i, j):
    i = (int(i[0]), int(i[1]))
    j = (int(j[0]), int(j[1]))

    x = (i[0] + j[0]) / 2
    y = (i[1] + j[1]) / 2

    return [x, y]

def average_point_list(points):
    x = 0
    y = 0
    for p in points:
        x += p[0]
        y += p[1]
    x = int(x / len(points))
    y = int(y / len(points))

    return [x, y]

def scale_point(i, s):
    return [i[0] / s, i[1] / s]

def degreesToPoint(deg, mag, pos=[0,0]):
    x = pos[0] + (math.cos(deg) * mag)
    y = pos[1] + (math.sin(deg) * mag)

    return [x, y]
    
def flipRect(i):
    return ( ((i.left * -1) - i.width), i.top )

def getSuperEnergyGain(i):
    if i < len(SUPER_ENERGY_GAIN_FINAL):
        return SUPER_ENERGY_GAIN_FINAL[i]
    else:
        return SUPER_ENERGY_GAIN_FINAL[-1]

def convertIntToBinary(n, digits=16):
    return "".join([str((n >> y) & 1) for y in range(digits-1, -1, -1)])

def convertIntToTwoASCII(n):
    binary = convertIntToBinary(n)
    return chr(int(binary[:8], 2)), chr(int(binary[8:], 2))
