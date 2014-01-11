from common import hitbox
from common import hurtbox
from common import blockbox

from common.constants import *

from common.util.rect import Rect

class Move(object):
    def __init__(self, f, t):
        self.frames = []
        
        temp = ['exitFrame', 'doWalk', 'doDash', 'noXMove', 'noXVel', 'land', 'jump',
                'doDuck', 'stopDuck', 'attackA', 'attackB', 'releaseA',
                'releaseB', 'attackAUp', 'attackBUp', 'attackADown',
                'attackBDown', 'attackBUpCharge', 'attackBDownCharge', 'bladelv1', 'bladelv2',
                'bladelv3', 'onHit', 'attackAAtMax', 'attackBAtMax',
                'block', 'releaseBlock', 'downBlock', 'forward', 'backward',
                'up', 'tech', 'dropThrough', 'super']
        self.transitions = {}
        for i in temp:
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

def makeRect(d):
    topleft = (d[0], d[1])
    width = d[2] - d[0]
    height = d[3] - d[1]
    size = (width, height)
    return Rect(topleft, size)

class Transition(object):
    def __init__(self, var1, var2, rangeMin, rangeMax, dest):
        self.var1 = var1
        self.var2 = var2
        self.rangeMin = rangeMin
        self.rangeMax = rangeMax
        self.destination = dest

def baseIdle():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')],
          ['doWalk', Transition(None, None, None, None, 'walking')],
          ['doDash', Transition(None, None, None, None, 'dashing')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['doDuck', Transition(None, None, None, None, 'ducking')],
          ['attackAUp', Transition(None, None, None, None, 'upA')],
          ['attackBUp', Transition(None, None, None, None, 'upB')],
          ['attackA', Transition(None, None, None, None, 'jabA')],
          ['attackB', Transition(None, None, None, None, 'jabB')],
          ['block', Transition(None, None, None, None, 'blocking')],
          ['downBlock', Transition(None, None, None, None, 'lowBlocking')],
          ['super', Transition(None, None, None, None, 'superFlash')]]
    m = Move([], t)
    m.canDI = False
    return m
    
def baseWalking():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'walking')],
          ['doDash', Transition(None, None, None, None, 'dashing')],
          ['noXMove', Transition(None, None, None, None, 'idle')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['doDuck', Transition(None, None, None, None, 'ducking')],
          ['attackAUp', Transition(None, None, None, None, 'upA')],
          ['attackBUp', Transition(None, None, None, None, 'upB')],
          ['attackA', Transition(None, None, None, None, 'jabA')],
          ['attackB', Transition(None, None, None, None, 'jabB')],
          ['block', Transition(None, None, None, None, 'blocking')],
          ['downBlock', Transition(None, None, None, None, 'lowBlocking')],
          ['super', Transition(None, None, None, None, 'superFlash')]]
    m = Move([], t)
    return m

def baseDashing():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'running')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['doDuck', Transition(None, None, None, None, 'ducking')],
          ['attackAUp', Transition(None, None, None, None, 'upA')],
          ['attackBUp', Transition(None, None, None, None, 'upB')],
          ['attackA', Transition(None, None, None, None, 'dashAttackA')],
          ['attackB', Transition(None, None, None, None, 'dashAttackB')],
          ['block', Transition(None, None, None, None, 'blocking')],
          ['downBlock', Transition(None, None, None, None, 'lowBlocking')],
          ['super', Transition(None, None, None, None, 'superFlash')]]
    m = Move([], t)
    return m

def baseRunning():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'running')],
          ['noXMove', Transition(None, None, None, None, 'idle')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['doDuck', Transition(None, None, None, None, 'ducking')],
          ['attackAUp', Transition(None, None, None, None, 'upA')],
          ['attackBUp', Transition(None, None, None, None, 'upB')],
          ['attackA', Transition(None, None, None, None, 'dashAttackA')],
          ['attackB', Transition(None, None, None, None, 'dashAttackB')],
          ['block', Transition(None, None, None, None, 'blocking')],
          ['downBlock', Transition(None, None, None, None, 'lowBlocking')],
          ['super', Transition(None, None, None, None, 'superFlash')]]
    m = Move([], t)
    return m

def baseAir():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'air')],
          ['land', Transition(None, None, None, None, 'landing')],
          ['attackA', Transition(None, None, None, None, 'neutralAirA')],
          ['attackB', Transition(None, None, None, None, 'neutralAirB')],
          ['attackAUp', Transition(None, None, None, None, 'upAirA')],
          ['attackBUpCharge', Transition(None, None, None, None, 'upAirB')],
          ['attackADown', Transition(None, None, None, None, 'downAirA')],
          ['attackBDown', Transition(None, None, None, None, 'downAirB')],
          ['block', Transition(None, None, None, None, 'airBlocking')],
          ['downBlock', Transition(None, None, None, None, 'airBlocking')],
          ['super', Transition(None, None, None, None, 'superFlashAir')] ]
    m = Move([], t)
    return m

def baseLanding():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')] ]
    m = Move([], t)
    m.canDI = False
    return m

def baseJumping():
    m = Move([], [])
    m.canDI = False
    m.isJump = True
    return m

def baseDucking():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'ducking')],
          ['stopDuck', Transition(None, None, None, None, 'idle')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['dropThrough', Transition(None, None, None, None, 'droppingThrough')],
          ['attackADown', Transition(None, None, None, None, 'downA')],
          ['attackBDown', Transition(None, None, None, None, 'downB')],
          ['downBlock', Transition(None, None, None, None, 'lowBlocking')],
          ['super', Transition(None, None, None, None, 'superFlash')]]
    m = Move([], t)
    m.canDI = False
    return m

def baseGrabbing():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')],
          ['block', Transition(None, None, -1, -1, 'blocking')]]
    m = Move([], t)
    m.canDI = False
    return m

def baseGrabHold():
    t = [ ['exitFrame', Transition(-1, None, None, None, 'grabRelease')],
          ['backward', Transition(None, None, 1, 1, 'throwBackward')],
          ['forward', Transition(None, None, 1, 1, 'throwForward')]]
    m = Move([], t)
    m.canDI = False
    m.grabVal = 1
    m.grabPos = (0, 0)
    return m

def baseGrabbed():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'grabbed2')],
          ['attackA', Transition(None, None, 1, 1, 'idle')],
          ['attackB', Transition(None, None, 1, 1, 'idle')]  ]
    m = Move([], t)
    m.canDI = False
    m.grabVal = -1
    m.grabPos = (0, 0)
    m.drawToBack = True
    return m

def baseGrabbed2():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'grabbed2')] ]
    m = Move([], t)
    m.canDI = False
    m.grabVal = -1
    m.grabPos = (0, 0)
    return m

def baseGrabRelease():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')] ]
    m = Move([], t)
    m.canDI = False
    return m

def baseGrabbedRelease():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')] ]
    m = Move([], t)
    m.canDI = False
    m.drawToBack = True
    return m

def baseThrow():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'idle')] ]
    m = Move([], t)
    m.canDI = False
    m.grabVal = 2
    m.grabPos = (0, 0)
    return m

def baseBlocking():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'blocking')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['releaseBlock', Transition(None, None, None, None, 'idle')],
          ['doDuck', Transition(None, None, None, None, 'lowBlocking')],
          ['attackA', Transition(None, None, None, None, 'grabbing')]]

    m = Move([], t)
    m.canDI = False
    return m

def baseLowBlocking():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'lowBlocking')],
          ['jump', Transition(None, None, None, None, 'jumping')],
          ['releaseBlock', Transition(None, None, None, None, 'ducking')],
          ['stopDuck', Transition(None, None, None, None, 'blocking')],
          ['attackB', Transition(None, None, None, None, 'grabbing')]]

    m = Move([], t)
    m.canDI = False
    return m

def baseAirBlocking():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'airBlocking')],
          ['releaseBlock', Transition(None, None, None, None, 'air')],
          ['land', Transition(None, None, None, None, 'blocking')]]

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
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'standUp')],
          ['up', Transition(None, None, -2, -1, 'standUp')],
          ['forward', Transition(None, None, -2, -1, 'standForward')],
          ['backward', Transition(None, None, -2, -1, 'standBackward')],
          ['attackA', Transition(None, None, -2, -1, 'standAttack')],
          ['tech', Transition(None, None, 0, 0, 'teching')]]
    m = Move([], t)
    m.canDI = False
    m.isOnGround = True
    m.drawToBack = True
    return m

def baseTeching():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'techUp')],
          ['forward', Transition(None, None, 1, 1, 'techForward')],
          ['backward', Transition(None, None, 1, 1, 'techBackward')] ]

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
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'flying')] ]
    m = Move([], t)
    return m

def baseDroppingThrough():
    m = Move([], [])
    m.canDI = False
    return m

def baseDeadFalling():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'deadFalling')],
          ['land', Transition(None, None, None, None, 'deadGroundHit')]]
    m = Move([], t)
    m.canDI = False
    m.isDead = True
    m.drawToBack = True
    return m

def baseDeadGroundHit():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'deadLaying')] ]
    m = Move([], t)
    m.canDI = False
    m.isDead = True
    m.isOnGround = True
    m.drawToBack = True
    return m

def baseDeadLaying():
    t = [ ['exitFrame', Transition(-1, 0, None, None, 'deadLaying')] ]
    m = Move([], t)
    m.canDI = False
    m.isDead = True
    m.isOnGround = True
    m.drawToBack = True
    return m

def baseSuperFlash():
    t = [['exitFrame', Transition(-1, 0, None, None, 'superMove')]]
    
    m = Move([], t)
    m.canDI = False
    m.isSuper = True
    m.isSuperFlash = True
    m.ignoreGroundAir = True
    m.canRetreat = False
    return m

def initBattlecharMoves(moves):
    moves['idle'] = baseIdle()
    moves['idleLike'] = baseBlank()
    moves['walking'] = baseWalking()
    moves['dashing'] = baseDashing()
    moves['running'] = baseRunning()
    moves['air'] = baseAir()
    moves['flipping'] = baseAir()
    moves['airLike'] = baseBlank()
    moves['landing'] = baseLanding()
    moves['jumping'] = baseJumping()
    moves['jumpingLike'] = baseJumping()
    moves['ducking'] = baseDucking()
    moves['jabA'] = baseBlank()
    moves['jabB'] = baseBlank()
    moves['dashAttackA'] = baseBlank()
    moves['dashAttackB'] = baseBlank()
    moves['downA'] = baseBlank()
    moves['downB'] = baseBlank()
    moves['upA'] = baseBlank()
    moves['upB'] = baseBlank()
    moves['neutralAirA'] = baseBlank()
    moves['neutralAirB'] = baseBlank()
    moves['upAirA'] = baseBlank()
    moves['upAirB'] = baseBlank()
    moves['downAirA'] = baseBlank()
    moves['downAirB'] = baseBlank()
    moves['droppingThrough'] = baseDroppingThrough()

    moves['grabbing'] = baseGrabbing()
    moves['grabHold'] = baseGrabHold()
    moves['grabbed'] = baseGrabbed()
    moves['grabbed2'] = baseGrabbed2()
    moves['grabRelease'] = baseGrabRelease()
    moves['grabbedRelease'] = baseGrabbedRelease()

    moves['throwBackward'] = baseThrow()
    moves['throwForward'] = baseThrow()

    moves['blocking'] = baseBlocking()
    moves['lowBlocking'] = baseLowBlocking()
    moves['airBlocking'] = baseAirBlocking()

    moves['stun1'] = baseStun()
    moves['stun2'] = baseStun()
    moves['stun3'] = baseStunNeedTech()
    moves['stun4'] = baseStunNeedTech()

    moves['groundHit'] = baseGroundHit()
    moves['standUp'] = baseStand()
    moves['standForward'] = baseStand()
    moves['standBackward'] = baseStand()
    moves['standAttack'] = baseStand()

    moves['teching'] = baseTeching()
    moves['techUp'] = baseTechRoll()
    moves['techForward'] = baseTechRoll()
    moves['techBackward'] = baseTechRoll()

    moves['deadFalling'] = baseDeadFalling()
    moves['deadGroundHit'] = baseDeadGroundHit()
    moves['deadLaying'] = baseDeadLaying()

    moves['superFlash'] = None
    moves['superMove'] = None

    moves['superFlashAir'] = None
    moves['superMoveAir'] = None

def frameData(key, length, r=[], h=[], b=[]):
    return {FD_KEY : key,
            FD_LEN : length,
            FD_HURT : r,
            FD_HIT : h,
            FD_BLOCK : b}

def setupSuper(moves, superMoves, superMovesAir, superMove=0):
    moves['superMove'] = None
    moves['superFlash'] = None
    moves['superMoveAir'] = None
    moves['superFlashAir'] = None

    m = superMoves[superMove]
    moves['superMove'] = m

    if m is not None:
        moves['superFlash'] = m.flash

    m = superMovesAir[superMove]
    moves['superMoveAir'] = m

    if m is not None:
        moves['superFlashAir'] = m.flash
