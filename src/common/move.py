from common import hitbox
from common import hurtbox
from common import blockbox

from common.constants import *

from common.util.rect import Rect

class Move(object):
    def __init__(self, f, t):
        self.frames = []
        self.transitions = {}

        for i in TRANSITION_TYPES:
            self.transitions[i] = None

        self.shoot = []

        self.append(f, t)

        self.canDI = True
        self.canRetreat = True
        self.isJump = False
        self.isStun = False
        self.liftOff = False
        self.reversable = False
        self.chargeBlade = False
        self.needTech = False
        self.grabVal = 0
        self.grabPos = None
        self.isDead = False
        self.isOnGround = False
        self.isSuper = False
        self.isSuperFlash = False
        self.ignoreGroundAir = False
        self.drawToBack = False

    def append(self, f, t):
        for i in f:
            self.frames.append(Frame(i))

        for i in t:
            self.transitions[i[0]] = i[1]

    def isGrab(self):
        return (self.grabVal == 1)

    def isGrabbed(self):
        return (self.grabVal == -1)

    def isThrow(self):
        return (self.grabVal == 2)

class SuperMove(Move):
    def __init__(self, inName, inDesc, f, t):
        super(SuperMove, self).__init__(f, t)
        self.name = inName
        self.desc = inDesc
        self.isSuper = True
        self.flash = None
        self.canRetreat = False

class Frame(object):
    def __init__(self, frameData):
        self.frameKey = frameData[FD_KEY]
        self.length = frameData[FD_LEN]
        self.setVelX = None
        self.setVelY = None
        self.addVelX = None
        self.addVelY = None
        self.setAccelX = None
        self.setAccelY = None
        self.setVelYIfDrop = None
        self.addVelYIfDrop = None
        self.ignoreSpeedCap = False
        self.setSpeedCapX = None
        self.ignoreFriction = False
        self.setFrictionX = None
        self.resetHitPotential = False
        self.buildHurtboxes(frameData[FD_HURT])
        self.buildHitboxes(frameData[FD_HIT])
        self.buildBlockboxes(frameData[FD_BLOCK])
        self.fx = []
        self.resetCanEffect = False

    def buildBlockboxes(self, data):
        self.blockboxes = []

        for d in data:
            self.blockboxes.append(blockbox.Blockbox(makeRect(d)))

    def buildHurtboxes(self, data):
        self.hurtboxes = []

        for d in data:
            self.hurtboxes.append(hurtbox.Hurtbox(makeRect(d)))

    def buildHitboxes(self, data):
        self.hitboxes = []

        for d in data:
            damage = d[4]
            stun = d[5]
            knockback = d[6]
            angle = d[7]
            properties = d[8]
            freezeFrame = d[9]
            if len(d) >= 11:
                chip = d[10]
            else:
                chip = CHIP_DAMAGE_PERCENTAGE_DEFAULT
            self.hitboxes.append(hitbox.Hitbox(makeRect(d), damage, stun, knockback,
                                               angle, properties, freezeFrame, chip))

def makeRect(rectData):
    left = rectData[0]
    top = rectData[1]
    right = rectData[2]
    bottom = rectData[3]

    width = right - left
    height = bottom - top

    return Rect(left, top, width, height)

class Transition(object):
    def __init__(self, var1, var2, rangeMin, rangeMax, dest):
        self.var1 = var1
        self.var2 = var2
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.destination = dest

def baseIdle():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_IDLE)],
          [T_DO_WALK, Transition(None, None, None, None, M_WALKING)],
          [T_DO_DASH, Transition(None, None, None, None, M_DASHING)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_DO_DUCK, Transition(None, None, None, None, M_DUCKING)],
          [T_ATTACK_A_UP, Transition(None, None, None, None, M_UP_A)],
          [T_ATTACK_B_UP, Transition(None, None, None, None, M_UP_B)],
          [T_ATTACK_A, Transition(None, None, None, None, M_JAB_A)],
          [T_ATTACK_B, Transition(None, None, None, None, M_JAB_B)],
          [T_BLOCK, Transition(None, None, None, None, M_BLOCKING)],
          [T_DOWN_BLOCK, Transition(None, None, None, None, M_LOW_BLOCKING)],
          [T_SUPER, Transition(None, None, None, None, M_SUPER_FLASH)]]
    m = Move([], t)
    m.canDI = False
    return m
    
def baseWalking():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_WALKING)],
          [T_DO_DASH, Transition(None, None, None, None, M_DASHING)],
          [T_NO_X_MOVE, Transition(None, None, None, None, M_IDLE)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_DO_DUCK, Transition(None, None, None, None, M_DUCKING)],
          [T_ATTACK_A_UP, Transition(None, None, None, None, M_UP_A)],
          [T_ATTACK_B_UP, Transition(None, None, None, None, M_UP_B)],
          [T_ATTACK_A, Transition(None, None, None, None, M_JAB_A)],
          [T_ATTACK_B, Transition(None, None, None, None, M_JAB_B)],
          [T_BLOCK, Transition(None, None, None, None, M_BLOCKING)],
          [T_DOWN_BLOCK, Transition(None, None, None, None, M_LOW_BLOCKING)],
          [T_SUPER, Transition(None, None, None, None, M_SUPER_FLASH)]]
    m = Move([], t)
    return m

def baseDashing():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_RUNNING)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_DO_DUCK, Transition(None, None, None, None, M_DUCKING)],
          [T_ATTACK_A_UP, Transition(None, None, None, None, M_UP_A)],
          [T_ATTACK_B_UP, Transition(None, None, None, None, M_UP_B)],
          [T_ATTACK_A, Transition(None, None, None, None, M_DASH_ATTACK_A)],
          [T_ATTACK_B, Transition(None, None, None, None, M_DASH_ATTACK_B)],
          [T_BLOCK, Transition(None, None, None, None, M_BLOCKING)],
          [T_DOWN_BLOCK, Transition(None, None, None, None, M_LOW_BLOCKING)],
          [T_SUPER, Transition(None, None, None, None, M_SUPER_FLASH)]]
    m = Move([], t)
    return m

def baseRunning():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_RUNNING)],
          [T_NO_X_MOVE, Transition(None, None, None, None, M_IDLE)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_DO_DUCK, Transition(None, None, None, None, M_DUCKING)],
          [T_ATTACK_A_UP, Transition(None, None, None, None, M_UP_A)],
          [T_ATTACK_B_UP, Transition(None, None, None, None, M_UP_B)],
          [T_ATTACK_A, Transition(None, None, None, None, M_DASH_ATTACK_A)],
          [T_ATTACK_B, Transition(None, None, None, None, M_DASH_ATTACK_B)],
          [T_BLOCK, Transition(None, None, None, None, M_BLOCKING)],
          [T_DOWN_BLOCK, Transition(None, None, None, None, M_LOW_BLOCKING)],
          [T_SUPER, Transition(None, None, None, None, M_SUPER_FLASH)]]
    m = Move([], t)
    return m

def baseAir():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_AIR)],
          [T_LAND, Transition(None, None, None, None, M_LANDING)],
          [T_ATTACK_A, Transition(None, None, None, None, M_NEUTRAL_AIR_A)],
          [T_ATTACK_B, Transition(None, None, None, None, M_NEUTRAL_AIR_B)],
          [T_ATTACK_A_UP, Transition(None, None, None, None, M_UP_AIR_A)],
          [T_ATTACK_B_UP_CHARGE, Transition(None, None, None, None, M_UP_AIR_B)],
          [T_ATTACK_A_DOWN, Transition(None, None, None, None, M_DOWN_AIR_A)],
          [T_ATTACK_B_DOWN, Transition(None, None, None, None, M_DOWN_AIR_B)],
          [T_BLOCK, Transition(None, None, None, None, M_AIR_BLOCKING)],
          [T_DOWN_BLOCK, Transition(None, None, None, None, M_AIR_BLOCKING)],
          [T_SUPER, Transition(None, None, None, None, M_SUPER_FLASH_AIR)] ]
    m = Move([], t)
    return m

def baseLanding():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_IDLE)] ]
    m = Move([], t)
    m.canDI = False
    return m

def baseJumping():
    m = Move([], [])
    m.canDI = False
    m.isJump = True
    return m

def baseDucking():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_DUCKING)],
          [T_STOP_DUCK, Transition(None, None, None, None, M_IDLE)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_DROP_THROUGH, Transition(None, None, None, None, M_DROPPING_THROUGH)],
          [T_ATTACK_A_DOWN, Transition(None, None, None, None, M_DOWN_A)],
          [T_ATTACK_B_DOWN, Transition(None, None, None, None, M_DOWN_B)],
          [T_DOWN_BLOCK, Transition(None, None, None, None, M_LOW_BLOCKING)],
          [T_SUPER, Transition(None, None, None, None, M_SUPER_FLASH)]]
    m = Move([], t)
    m.canDI = False
    return m

def baseGrabbing():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_IDLE)],
          [T_BLOCK, Transition(None, None, -1, -1, M_BLOCKING)]]
    m = Move([], t)
    m.canDI = False
    return m

def baseGrabHold():
    t = [ [T_EXIT_FRAME, Transition(-1, None, None, None, M_GRAB_RELEASE)],
          [T_BACKWARD, Transition(None, None, 1, 1, M_THROW_BACKWARD)],
          [T_FORWARD, Transition(None, None, 1, 1, M_THROW_FORWARD)]]
    m = Move([], t)
    m.canDI = False
    m.grabVal = 1
    m.grabPos = (0, 0)
    return m

def baseGrabbed():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_GRABBED_2)],
          [T_ATTACK_A, Transition(None, None, 1, 1, M_IDLE)],
          [T_ATTACK_B, Transition(None, None, 1, 1, M_IDLE)]  ]
    m = Move([], t)
    m.canDI = False
    m.grabVal = -1
    m.grabPos = (0, 0)
    m.drawToBack = True
    return m

def baseGrabbed2():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_GRABBED_2)] ]
    m = Move([], t)
    m.canDI = False
    m.grabVal = -1
    m.grabPos = (0, 0)
    return m

def baseGrabRelease():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_IDLE)] ]
    m = Move([], t)
    m.canDI = False
    return m

def baseGrabbedRelease():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_IDLE)] ]
    m = Move([], t)
    m.canDI = False
    m.drawToBack = True
    return m

def baseThrow():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_IDLE)] ]
    m = Move([], t)
    m.canDI = False
    m.grabVal = 2
    m.grabPos = (0, 0)
    return m

def baseBlocking():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_BLOCKING)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_RELEASE_BLOCK, Transition(None, None, None, None, M_IDLE)],
          [T_DO_DUCK, Transition(None, None, None, None, M_LOW_BLOCKING)],
          [T_ATTACK_A, Transition(None, None, None, None, M_GRABBING)]]

    m = Move([], t)
    m.canDI = False
    return m

def baseLowBlocking():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_LOW_BLOCKING)],
          [T_JUMP, Transition(None, None, None, None, M_JUMPING)],
          [T_RELEASE_BLOCK, Transition(None, None, None, None, M_DUCKING)],
          [T_STOP_DUCK, Transition(None, None, None, None, M_BLOCKING)],
          [T_ATTACK_B, Transition(None, None, None, None, M_GRABBING)]]

    m = Move([], t)
    m.canDI = False
    return m

def baseAirBlocking():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_AIR_BLOCKING)],
          [T_RELEASE_BLOCK, Transition(None, None, None, None, M_AIR)],
          [T_LAND, Transition(None, None, None, None, M_BLOCKING)]]

    m = Move([], t)
    return m

def baseStun():
    m = Move([], [])
    m.canDI = False
    m.isStun = True
    m.drawToBack = True
    return m

def baseStunNeedTech():
    m = baseStun()
    m.needTech = True
    m.drawToBack = True
    return m
    

def baseGroundHit():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_STAND_UP)],
          [T_UP, Transition(None, None, -2, -1, M_STAND_UP)],
          [T_FORWARD, Transition(None, None, -2, -1, M_STAND_FORWARD)],
          [T_BACKWARD, Transition(None, None, -2, -1, M_STAND_BACKWARD)],
          [T_ATTACK_A, Transition(None, None, -2, -1, M_STAND_ATTACK)],
          [T_TECH, Transition(None, None, 0, 0, M_TECHING)]]
    m = Move([], t)
    m.canDI = False
    m.isOnGround = True
    m.drawToBack = True
    return m

def baseTeching():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_TECH_UP)],
          [T_FORWARD, Transition(None, None, 1, 1, M_TECH_FORWARD)],
          [T_BACKWARD, Transition(None, None, 1, 1, M_TECH_BACKWARD)] ]

    m = Move([], t)
    m.canDI = False
    m.drawToBack = True
    return m

def baseStand():
    m = Move([], [])
    m.canDI = False
    return m

def baseTechRoll():
    m = Move([], [])
    m.canDI = False
    m.drawToBack = True
    return m

def baseBlank():
    m = Move([], [])
    return m

def baseProjFlying():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_FLYING)] ]
    m = Move([], t)
    return m

def baseDroppingThrough():
    m = Move([], [])
    m.canDI = False
    return m

def baseDeadFalling():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_DEAD_FALLING)],
          [T_LAND, Transition(None, None, None, None, M_DEAD_GROUND_HIT)]]
    m = Move([], t)
    m.canDI = False
    m.isDead = True
    m.drawToBack = True
    return m

def baseDeadGroundHit():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_DEAD_LAYING)] ]
    m = Move([], t)
    m.canDI = False
    m.isDead = True
    m.isOnGround = True
    m.drawToBack = True
    return m

def baseDeadLaying():
    t = [ [T_EXIT_FRAME, Transition(-1, 0, None, None, M_DEAD_LAYING)] ]
    m = Move([], t)
    m.canDI = False
    m.isDead = True
    m.isOnGround = True
    m.drawToBack = True
    return m

def baseSuperFlash():
    t = [[T_EXIT_FRAME, Transition(-1, 0, None, None, M_SUPER_MOVE)]]
    
    m = Move([], t)
    m.canDI = False
    m.isSuper = True
    m.isSuperFlash = True
    m.ignoreGroundAir = True
    m.canRetreat = False
    return m

def initBattlecharMoves(moves):
    moves[M_IDLE] = baseIdle()
    moves[M_IDLE_LIKE] = baseBlank()
    moves[M_WALKING] = baseWalking()
    moves[M_DASHING] = baseDashing()
    moves[M_RUNNING] = baseRunning()
    moves[M_AIR] = baseAir()
    moves[M_FLIPPING] = baseAir()
    moves[M_AIR_LIKE] = baseBlank()
    moves[M_LANDING] = baseLanding()
    moves[M_JUMPING] = baseJumping()
    moves[M_JUMPING_LIKE] = baseJumping()
    moves[M_DUCKING] = baseDucking()
    moves[M_JAB_A] = baseBlank()
    moves[M_JAB_B] = baseBlank()
    moves[M_DASH_ATTACK_A] = baseBlank()
    moves[M_DASH_ATTACK_B] = baseBlank()
    moves[M_DOWN_A] = baseBlank()
    moves[M_DOWN_B] = baseBlank()
    moves[M_UP_A] = baseBlank()
    moves[M_UP_B] = baseBlank()
    moves[M_NEUTRAL_AIR_A] = baseBlank()
    moves[M_NEUTRAL_AIR_B] = baseBlank()
    moves[M_UP_AIR_A] = baseBlank()
    moves[M_UP_AIR_B] = baseBlank()
    moves[M_DOWN_AIR_A] = baseBlank()
    moves[M_DOWN_AIR_B] = baseBlank()
    moves[M_DROPPING_THROUGH] = baseDroppingThrough()

    moves[M_GRABBING] = baseGrabbing()
    moves[M_GRAB_HOLD] = baseGrabHold()
    moves[M_GRABBED] = baseGrabbed()
    moves[M_GRABBED_2] = baseGrabbed2()
    moves[M_GRAB_RELEASE] = baseGrabRelease()
    moves[M_GRABBED_RELEASE] = baseGrabbedRelease()

    moves[M_THROW_BACKWARD] = baseThrow()
    moves[M_THROW_FORWARD] = baseThrow()

    moves[M_BLOCKING] = baseBlocking()
    moves[M_LOW_BLOCKING] = baseLowBlocking()
    moves[M_AIR_BLOCKING] = baseAirBlocking()

    moves[M_STUN_1] = baseStun()
    moves[M_STUN_2] = baseStun()
    moves[M_STUN_3] = baseStunNeedTech()
    moves[M_STUN_4] = baseStunNeedTech()

    moves[M_GROUND_HIT] = baseGroundHit()
    moves[M_STAND_UP] = baseStand()
    moves[M_STAND_FORWARD] = baseStand()
    moves[M_STAND_BACKWARD] = baseStand()
    moves[M_STAND_ATTACK] = baseStand()

    moves[M_TECHING] = baseTeching()
    moves[M_TECH_UP] = baseTechRoll()
    moves[M_TECH_FORWARD] = baseTechRoll()
    moves[M_TECH_BACKWARD] = baseTechRoll()

    moves[M_DEAD_FALLING] = baseDeadFalling()
    moves[M_DEAD_GROUND_HIT] = baseDeadGroundHit()
    moves[M_DEAD_LAYING] = baseDeadLaying()

    moves[M_SUPER_FLASH] = None
    moves[M_SUPER_MOVE] = None

    moves[M_SUPER_FLASH_AIR] = None
    moves[M_SUPER_MOVE_AIR] = None

def frameData(key, length, r=[], h=[], b=[]):
    return {FD_KEY : key,
            FD_LEN : length,
            FD_HURT : r,
            FD_HIT : h,
            FD_BLOCK : b}

def setupSuper(moves, superMoves, superMovesAir, superMove=0):
    moves[M_SUPER_MOVE] = None
    moves[M_SUPER_FLASH] = None
    moves[M_SUPER_MOVE_AIR] = None
    moves[M_SUPER_FLASH_AIR] = None

    m = superMoves[superMove]
    moves[M_SUPER_MOVE] = m

    if m is not None:
        moves[M_SUPER_FLASH] = m.flash

    m = superMovesAir[superMove]
    moves[M_SUPER_MOVE_AIR] = m

    if m is not None:
        moves[M_SUPER_FLASH_AIR] = m.flash
