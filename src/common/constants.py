import os

import math

VERSION = "0.1.5"

FRAME_RATE = 40
DEBUG_MODE = True

BATTLE_ARENA_SIZE = (1000, 900)

# player types

# client
P_LOCAL = 0  # player is on the current machine
P_REMOTE = 1 # player is on another machine

# server
P_HUMAN = 2 # player is a human
P_BOT = 3   # player is a bot

NUM_PLAYERS = 4

PLAYER_TYPES = [i for i in xrange(NUM_PLAYERS)]

# key types
K_UP = 0
K_DOWN = 1
K_LEFT = 2
K_RIGHT = 3
K_ATT_A = 4
K_ATT_B = 5
K_JUMP = 6
K_BLOCK = 7
K_SUPER = 8

NUM_KEYS = 9

KEY_TYPES = [i for i in xrange(NUM_KEYS)]

# character types
C_HARE = 0
C_CAT = 1
C_FOX = 2

NUM_CHARS = 3

CHAR_TYPES = [i for i in xrange(NUM_CHARS)]

# moves

M_AIR = 0
M_AIR_BLOCKING = 1
M_AIR_DASHING = 2
M_AIR_LIKE = 3
M_BLOCKING = 4
M_DASH_ATTACK_A = 5
M_DASH_ATTACK_B = 6
M_DASHING = 7
M_DEAD_FALLING = 8
M_DEAD_GROUND_HIT = 9
M_DEAD_LAYING = 10
M_DOWN_A = 11
M_DOWN_A_AIR_LAG = 12
M_DOWN_AIR_A = 13
M_DOWN_AIR_B = 14
M_DOWN_B = 15
M_DOWN_B_AIR_LAG = 16
M_DOWN_B_LAG = 17
M_DROPPING_THROUGH = 18
M_DROP_SLASH_LAG = 19
M_DUCKING = 20
M_FLIPPING = 21
M_FLYING = 22
M_GRABBED = 23
M_GRABBED_2 = 24
M_GRABBED_RELEASE = 25
M_GRABBING = 26
M_GRAB_HOLD = 27
M_GRAB_RELEASE = 28
M_GROUND_HIT = 29
M_HEAD_BOUNCE = 30
M_IDLE = 31
M_IDLE_LIKE = 32
M_JAB_A = 33
M_JAB_A_2 = 34
M_JAB_B = 35
M_JUMPING = 36
M_JUMPING_LIKE = 37
M_LANDING = 38
M_LOW_BLOCKING = 39
M_NEUTRAL_AIR_A = 40
M_NEUTRAL_AIR_B = 41
M_ROLLING_SLASH = 42
M_ROTATE_KICK = 43
M_RUNNING = 44
M_STAND_ATTACK = 45
M_STAND_BACKWARD = 46
M_STAND_FORWARD = 47
M_STAND_UP = 48
M_STOMP = 49
M_STUN_1 = 50
M_STUN_2 = 51
M_STUN_3 = 52
M_STUN_4 = 53
M_SUPER_1_ENDING_1 = 54
M_SUPER_1_ENDING_2 = 55
M_SUPER_1_ENDING_LAG_1 = 56
M_SUPER_1_ENDING_LAG_2 = 57
M_SUPER_FLASH = 58
M_SUPER_FLASH_AIR = 59
M_SUPER_MOVE = 60
M_SUPER_MOVE_AIR = 61
M_TECH_BACKWARD = 62
M_TECH_FORWARD = 63
M_TECHING = 64
M_TECH_UP = 65
M_THROW_BACKWARD = 66
M_THROW_FORWARD = 67
M_THROW_FORWARD_LAG = 68
M_UP_A = 69
M_UP_A_CONFIRM = 70
M_UP_A_DROP_SLASH = 71
M_UP_AIR_A = 72
M_UP_AIR_B = 73
M_UP_A_SIDE_KICK = 74
M_UP_B = 75
M_WALKING = 76

NUM_MOVES = 77

MOVE_TYPES = [i for i in xrange(NUM_MOVES)]

# transitions

T_ATTACK_A = 0
T_ATTACK_A_AT_MAX = 1
T_ATTACK_A_DOWN = 2
T_ATTACK_A_UP = 3
T_ATTACK_B = 4
T_ATTACK_B_AT_MAX = 5
T_ATTACK_B_DOWN = 6
T_ATTACK_B_DOWN_CHARGE = 7
T_ATTACK_B_UP = 8
T_ATTACK_B_UP_CHARGE = 9
T_BACKWARD = 10
T_BLADE_LV_1 = 11
T_BLADE_LV_2 = 12
T_BLADE_LV_3 = 13
T_BLOCK = 14
T_DO_DASH = 15
T_DO_DUCK = 16
T_DO_WALK = 17
T_DOWN_BLOCK = 18
T_DROP_THROUGH = 19
T_EXIT_FRAME = 20
T_FORWARD = 21
T_JUMP = 22
T_LAND = 23
T_NO_X_MOVE = 24
T_NO_X_VEL = 25
T_ON_HIT = 26
T_RELEASE_A = 27
T_RELEASE_B = 28
T_RELEASE_BLOCK = 29
T_STOP_DUCK = 30
T_SUPER = 31
T_TECH = 32
T_UP = 33

NUM_TRANSITIONS = 34

TRANSITION_TYPES = [i for i in xrange(NUM_TRANSITIONS)]

# properties

P_FX = 0
P_GRAB = 1
P_REVERSE_FACING = 2
P_UNBLOCKABLE = 3
P_UNTECHABLE = 4

NUM_PROPERTIES = 5

PROPERTY_TYPES = [i for i in xrange(NUM_PROPERTIES)]

# effects

FX_AIR_ELEMENT_SHOCKWAVE = 1
FX_BLOCK = 2
FX_DUST = 3
FX_FULL_SHOCKWAVE = 4
FX_GRAB = 5
FX_POW = 6
FX_RUNIC_EXPLOSION = 7
FX_RUNIC_FLAME_1 = 8
FX_RUNIC_FLAME_2 = 9
FX_RUNIC_FLAME_3 = 10
FX_SHOCKWAVE = 11
FX_SIDE = 12

NUM_EFFECTS = 13

EFFECT_TYPES = [i for i in xrange(NUM_EFFECTS)]

# packing

PRECISION = 10000.0

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

def flipRectHoriz(rect):
    """ Returns a new Rect flipped over the y-axis. """

    r = rect.copy()
    r.left = -rect.right
    return r

def flipRectVert(rect):
    """ Returns a new Rect flipped over the x-axis. """

    r = rect.copy()
    r.top = -rect.bottom
    return r

def getAdjustedBox(owner, box):
    if owner.facingRight:
        rect = box.rect.copy()
    else:
        rect = flipRectHoriz(box.rect)

    rect.move_ip(owner.preciseLoc[0], owner.preciseLoc[1])
    return rect

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
