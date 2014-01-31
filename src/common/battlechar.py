import struct

from common.constants import *

from common import move
from common import boundint
from common.data import hare_stats
from common.data import hare_moves
from common.data import cat_stats
from common.data import cat_moves
from common.util.rect import Rect

STATS_MAP = {C_HARE : hare_stats,
             C_CAT : cat_stats}

MOVES_MAP = {C_HARE : hare_moves,
             C_CAT : cat_moves}

class BattleChar(object):
    def __init__(self, hp, footRectSize=30):
        self.player = None
        self.hp = boundint.BoundInt(0, hp, hp)
        self.superEnergy = boundint.BoundInt(0, SUPER_ENERGY_MAX,
                    int(SUPER_ENERGY_MAX * SUPER_ENERGY_INITIAL_FACTOR))
        self.preciseLoc = [50.0, 50.0]
        self.accel = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.inAir = False
        self.facingRight = True
        self.holdJump = True
        self.aerialCharge = True
        self.projectiles = []
        self.attackCanHit = True
        self.canShoot = True
        self.retreat = boundint.BoundInt(0, RETREAT_HOLD_TOTAL, 0)
        self.freezeFrame = 0
        self.blockstun = 0
        self.onHitTrigger = False
        self.techBuffer = TECH_BUFFER_MIN
        self.canTech = True
        self.dropThroughPlatform = None
        self.dashBuffer = [0, 0]
        self.canEffect = True
        
        self.damagePercent = 100

        self.currSuperMove = None

        self.setCurrMove(M_IDLE)

        self.createDust = None

        self.footRect = Rect((0, 0), ((footRectSize * 2)+1, 5))
        self.positionFootRect()

    def __getstate__(self):
        state = self.__dict__.copy()

        if state.has_key('player'):
            state.pop('player')

        return state

    def getRenderableState(self):
        packed = ""
        packed = struct.pack('sb', packed, self.type)

        x = int(self.preciseLoc[0] * PRECISION)
        y = int(self.preciseLoc[1] * PRECISION)
        packed = struct.pack('sii', packed, self.type)

        packed = struct.pack('sb', packed, self.facingRight)

    def setRenderableState(self, state):
        pass

    def getNetworkState(self):
        pass

    def setNetworkState(self):
        pass

    def beginBattle(self):
        self.retreat.change(0)
        self.freezeFrame = 0
        self.blockstun = 0
        if self.hp.value == 0:
            self.hp.value = 1
        self.setCurrMove(M_IDLE)
        self.dashBuffer = [0, 0]
        self.inAir = False

    def countdownComplete(self):
        pass

    def setLoc(self, loc):
        self.preciseLoc[0] = float(loc[0])
        self.preciseLoc[1] = float(loc[1])

    def update(self):
        for i in range(2):
            if self.dashBuffer[i] > 0:
                self.dashBuffer[i] -= 1
            
        if self.freezeFrame == 0:
            self.onHitTrigger = False
            self.proceedFrame()
            self.frameSpecial()

        frame = self.getCurrentFrame()

        if not (self.currMove.isStun or (self.currMove == self.getMoves()[M_GROUND_HIT])):
            self.canTech = True

        if self.techBuffer > TECH_BUFFER_MIN:
            self.techBuffer -= 1

        if self.freezeFrame == 0:
            if not frame.setSpeedCapX is None:
                speedCap = frame.setSpeedCapX
            elif self.inAir:
                speedCap = self.getStats().airVelMax
            else:
                if (self.currMove == self.getMoves()[M_DASHING]) or (self.currMove == self.getMoves()[M_GRABBING]):
                    speedCap = self.getStats().dashVelMax
                elif self.currMove == self.getMoves()[M_RUNNING]:
                    speedCap = self.getStats().runVelMax
                else:
                    speedCap = self.getStats().walkVelMax

            for i in range(2):
                self.vel[i] += self.accel[i]
                self.speedCap([speedCap, self.getStats().vertVelMax], i)
                self.preciseLoc[i] += self.vel[i]

        self.positionFootRect()

        if self.freezeFrame > 0:
            self.freezeFrame -= 1
        elif self.blockstun > 0:
            self.blockstun -= 1

    #Updates the character for non-battle viewing, such as
    #in the character editor.
    def staticUpdate(self):
        self.actLeft = True
        self.proceedFrame()
        self.frameSpecial()

    def positionFootRect(self):
        self.footRect.center = add_points(self.preciseLoc, (0, 0))

    def speedCap(self, caps, i):
        if not self.getCurrentFrame().ignoreSpeedCap:
            if self.vel[i] > caps[i]:
                self.vel[i] = caps[i]
            if i == 0:
                if self.vel[i] < -caps[i]:
                    self.vel[i] = -caps[i]

    def frameSpecial(self):
        f = self.getCurrentFrame()
        if not f.setVelX is None:
            self.vel[0] = f.setVelX * self.facingMultiplier()
            self.accel[0] = 0.0
        if not f.setVelY is None:
            self.vel[1] = f.setVelY
            self.accel[1] = 0.0
        if not f.addVelX is None:
            self.vel[0] += f.addVelX * self.facingMultiplier()
        if not f.addVelY is None:
            self.vel[1] += f.addVelY
        if not f.setVelYIfDrop is None:
            if self.vel[1] > 0:
                self.vel[1] = f.setVelYIfDrop
                self.accel[1] = 0.0
        if not f.addVelYIfDrop is None:
            if self.vel[1] > 0:
                self.vel[1] += f.addVelYIfDrop

        if self.currSubframe == 0 and f.resetHitPotential:
            self.attackCanHit = True

    def accelToZero(self):
        self.accel = [0.0, 0.0]

    def testMove(self, t):
        self.accel[0] = self.getStats().airAccel * t

    def facingMultiplier(self):
        if self.facingRight:
            return 1
        else:
            return -1

    def di(self):
        l, r = self.player().leftOrRight()
        if self.freezeFrame == 0:
            if not self.inAir:
                f = self.facingMultiplier()
            else:
                f = 0
                if l:
                    f = -1
                if r:
                    f = 1
                
            if not self.canDI():
                f = 0
            if not self.inAir:
                if self.currMove == self.getMoves()[M_DASHING]:
                    accel = self.getStats().dashAccel
                elif not self.keyTowardFacing():
                    f = 0
                else:
                    accel = self.getStats().walkAccel
            else:
                accel = self.getStats().airAccel

            if not self.getCurrentFrame().setAccelX is None:
                accel = self.getCurrentFrame().setAccelX

            if f == 0 or ((l and self.vel[0] > 0) or(r and self.vel[0] < 0)):
                if not self.getCurrentFrame().ignoreFriction:
                    self.friction()
                else:
                    
                    if self.facingRight:
                        f2 = 1
                    else:
                        f2 = -1
                    
                    if self.getCurrentFrame().setAccelX is None:
                        self.accel[0] = 0.0
                    else:
                        self.accel[0] = self.getCurrentFrame().setAccelX * f2
                        
                    if self.getCurrentFrame().setAccelY is None:
                        self.accel[1] = 0.0
                    else:
                        self.accel[1] = self.getCurrentFrame().setAccelY * f2
            else:
                self.accel[0] = accel * f

            if self.inAir:
                if not self.getCurrentFrame().setAccelY is None:
                    accel = self.getCurrentFrame().setAccelY
                else:
                    accel = self.getStats().vertAccel
                self.accel[1] = accel
            else:
                self.accel[1] = 0

    def friction(self):
        c = self.getCurrentFrame()
        if self.freezeFrame == 0 and self.blockstun == 0:
            if not c.setFrictionX is None:
                friction = c.setFrictionX
            elif self.inAir:
                if self.currMove.isStun:
                    friction = self.getStats().airFrictionStunned
                else:
                    friction = self.getStats().airFriction
            else:
                friction = self.getStats().groundFriction
            
            if self.vel[0] > friction:
                self.accel[0] = -friction
            elif self.vel[0] < -friction:
                self.accel[0] = friction
            else:
                self.accel[0] = 0
                self.vel[0] = 0

    def keyTowardFacing(self):
        l, r = self.player().leftOrRight()

        if l and not self.facingRight:
            return True
        if r and self.facingRight:
            return True

        return False

    def getStats(self):
        return STATS_MAP[self.type]

    def getMoves(self):
        return MOVES_MAP[self.type].moves

    def getSuperMoves(self):
        return MOVES_MAP[self.type].superMoves

    def getSuperMovesAir(self):
        return MOVES_MAP[self.type].superMovesAir

    def setCurrMove(self, index, frame=0):
        self.currMove = self.getMoves()[index]
        self.currFrame = frame
        self.currSubframe = 0
        self.attackCanHit = True
        self.canShoot = True
        self.canEffect = True

        if (self.currMove is None) or (len(self.currMove.frames) == 0):
            if (self.inAir):
                self.currMove = self.getMoves()[M_AIR]
            else:
                self.currMove = self.getMoves()[M_IDLE]

    def getCurrentFrame(self):
        if len(self.currMove.frames) > self.currFrame:
            return self.currMove.frames[self.currFrame]

    def canAct(self):
        if self.blockstun > 0:
            return False
        return True

    def canDI(self):
        return self.currMove.canDI

    def proceedFrame(self):
        frame = self.getCurrentFrame()

        self.currSubframe += 1
        if self.currSubframe == frame.length:
            self.currSubframe = 0
            t = self.actTransition(T_EXIT_FRAME, self.currFrame)
            if not t:
                self.currFrame += 1
                if (not self.getCurrentFrame() is None) and (self.getCurrentFrame().resetCanEffect):
                    self.canEffect = True

        if self.currFrame >= len(self.currMove.frames):
            if self.currMove.isJump:
                self.jump()
                self.setCurrMove(M_FLIPPING)
            elif self.inAir:
                self.setCurrMove(M_AIR)
            else:
                self.setCurrMove(M_IDLE)

    def jump(self):
        self.inAir = True
        self.holdJump = True
        self.vel[1] = self.getStats().jumpVel

    def unholdJump(self):
        self.holdJump = False
        if self.currMove.canDI:
            self.vel[1] /= 3

    def checkTransition(self, key, var1=None, var2=None):
        t = self.currMove.transitions[key]
        if t is None:
            return False

        if not t.rangeMin is None:
            rMin = t.rangeMin
            if rMin < 0:
                rMin = len(self.currMove.frames)+rMin
            if self.currFrame < rMin:
                return False

        if not t.rangeMax is None:
            rMax = t.rangeMax
            if rMax < 0:
                rMax = len(self.currMove.frames)+rMax
            if self.currFrame > rMax:
                return False

        if key == T_EXIT_FRAME:
            i = t.var1
            if i == -1:
                i = len(self.currMove.frames) - 1
            if i != var1:
                return False

        return True
    
    def actTransition(self, key, var1=None, var2=None):
                        
        t = self.currMove.transitions[key]
        
        if (key == T_SUPER) and (not t is None) and (self.getMoves()[t.destination] is None):
            return 
        
        if self.actLeft and self.checkTransition(key, var1, var2):
            
            if t.var1 == 2: #Energy cost to perform
                if self.energy.value < t.var2:
                    return False
                else:
                    self.energy.add(-t.var2)
            elif t.var1 == 3: #Energy minimum to perform
                if self.energy.value < t.var2:
                    return False
            self.setCurrMove(t.destination)
            if not key == T_EXIT_FRAME:
                self.actLeft = False
            return True
        else:
            return False

    def actTransitionFacing(self, key, l, r, var1=None, var2=None):
        c = self.actTransition(key, var1, var2)
        if c:
            if l and not r:
                self.facingRight = False
            elif r and not l:
                self.facingRight = True

        return c

    def transToAir(self):
        if (self.blockstun > 0):
            self.setCurrMove(M_AIR_BLOCKING)
        elif (not self.currMove.liftOff) and (not self.currMove.isStun):
            self.setCurrMove(M_FLIPPING)

    def transToGround(self):
        if self.currMove.isStun:
            if self.currMove.needTech:
                self.setCurrMove(M_GROUND_HIT)
                self.createDust = 0
            return
        c = self.actTransition(T_LAND)
        if not c:
            self.setCurrMove(M_IDLE)

    def getHitboxes(self):
        return self.getCurrentFrame().hitboxes

    def getHurtboxes(self):
        return self.getCurrentFrame().hurtboxes

    def getBlockboxes(self):
        return self.getCurrentFrame().blockboxes

    def getHit(self, damage, stun, vel):
        self.hp.add(-damage)

        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

        if stun <= STUN_THRESHOLD_1:
            self.setCurrMove(M_STUN_1)
        elif stun <= STUN_THRESHOLD_2:
            self.setCurrMove(M_STUN_2)
        elif stun <= STUN_THRESHOLD_3:
            self.setCurrMove(M_STUN_3)
        else:
            self.setCurrMove(M_STUN_4)

    def getBlockstun(self, damage, stun, vel, properties):
        self.hp.add(-damage)
        
        self.blockstun = int(stun * BLOCKSTUN_FACTOR)

        self.vel[0] = vel[0]
        self.vel[1] = vel[1]

    def getSuper(self):
        return self.getSuperMoves()[self.currSuperMove]

    def getCatEnergyLevel(self):
        return 0

    def getBlockFXPoint(self, i):
        p = [self.blockFXPoints[i][0], self.blockFXPoints[i][1]]
        if not self.facingRight:
            p[0] *= -1
        return add_points(self.preciseLoc, p)
    
    def setSuperValue(self, s):
        if (s < 0) or (s >= len(self.getSuperMoves())) or (s >= len(self.getSuperMovesAir())):
            s = 0
            
        self.currSuperMove = s

    def getDamagePercentText(self):
        return str(self.damagePercent) + "%"
    
    def getDamageMultiplier(self):
        return self.damagePercent / 100.0
    
    def performHit(self):
        pass
