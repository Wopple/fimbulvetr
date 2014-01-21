import sys
import copy
import math

import settings

from common.constants import *

from common import mvc
from common import process_m
from common import boundint
from common import countdown
from common import fx
from common import platform
from common import player
from common import hare, fox, cat
from common.util import *
from common.util.rect import Rect

class Model(process_m.ProcessModel):
    def __init__(self, resultQueue, stateQueue, inputQueue, inChars, terrainLeft, terrainRight):
        super(Model, self).__init__(resultQueue)
        self.stateQueue = stateQueue
        self.inputQueue = inputQueue
        self.terrainLeft = terrainLeft
        self.terrainRight = terrainRight
        self.arena = Rect((0, 0), BATTLE_ARENA_SIZE)
        self.players = []

        # create the players
        if settings.ENV is settings.CLIENT:
            self.players.append(player.Player(LOCAL, inChars[0]))

            for c in inChars[1:]:
                self.players.append(player.Player(REMOTE, c))
        elif settings.ENV is settings.SERVER:
            for c in inChars:
                self.players.append(player.Player(HUMAN, c))

        # init the players
        for p in self.players:
            p.char.beginBattle()

        pos = (self.arena.centerx,
               self.arena.height - BATTLE_AREA_FLOOR_HEIGHT)
        self.players[0].char.setLoc(add_points(pos, ((-BATTLE_PLAYER_START_DISTANCE / 2), 0)))
        self.players[0].facingRight = True
        self.players[1].char.setLoc(add_points(pos, ((BATTLE_PLAYER_START_DISTANCE / 2), 0)))
        self.players[1].facingRight = False

        # init the battle
        self.frameByFrame = [0, 0]

        self.returnCode = [0, 0]
        self.projectiles = []
        self.retreatProhibitTime = boundint.BoundInt(0, RETREAT_PROHIBIT_TIME,
                                                     RETREAT_PROHIBIT_TIME)
        self.retreatPhase = 0

        self.resetHitMemory()

        self.endingVal = -1
        self.endingValTick = 0

        self.fx = []

        self.platforms = getPlatforms(terrainLeft, terrainRight)

        self.countdown = countdown.Countdown(BATTLE_COUNTDOWN_LENGTH)

    def getState(self):
        return State(self)

    def setState(self, state):
        self.players = copy.deepcopy(state.players)
        self.returnCode = copy.deepcopy(state.returnCode)
        self.projectiles = copy.deepcopy(state.projectiles)
        self.retreatProhibitTime = copy.deepcopy(state.retreatProhibitTime)
        self.retreatPhase = copy.deepcopy(state.retreatPhase)
        self.endingVal = copy.deepcopy(state.endingVal)
        self.endingValTick = copy.deepcopy(state.endingValTick)
        self.fx = copy.deepcopy(state.fx)
        self.countdown = copy.deepcopy(state.countdown)

    def getLocalPlayer(self):
        for p in self.players:
            if p.type == LOCAL:
                return p

        return None

    def getOtherPlayers(self, player):
        otherPlayers = []

        for p in self.players:
            if p is not player:
                otherPlayers.append(p)

        return otherPlayers

    def update(self):
        # process all the input
        if settings.ENV == settings.CLIENT:
            while not self.inputQueue.empty():
                key = self.inputQueue.get()

                if key is None:
                    sys.exit(0)
                else:
                    self.key(key)

        fbf = self.checkFrameByFrame()

        if not fbf:
            self.checkEnding()

            if self.endingVal >= 0:
                self.endingValTick += 1
                if self.endingValTick >= BATTLE_ENDING_TIME_LENGTHS[self.endingVal]:
                    self.endingValTick = 0
                    self.endingVal += 1
                    if self.endingVal == len(BATTLE_ENDING_TIME_LENGTHS):
                        self.setResult(self.returnCode)
                        #self.advanceNow = True

            self.countdown.update()

            if self.countdown.checkStartFlag():
                for p in self.players:
                    p.char.countdownComplete()

                self.retreatPhase = 1

            isFlash = self.isFlash()

            if self.retreatPhase == 1 and self.endingVal == -1 and not isFlash:
                self.retreatProhibitTime.add(-1)
                if self.retreatProhibitTime.value == 0:
                    self.retreatPhase = 2

            for i, p in enumerate(self.players):
                if (isFlash) and (not p.char.currMove.isSuperFlash):
                    continue

                if self.countdown.isGoing() or self.returnCode[i] == 1:
                    keys = player.makeKeys()
                else:
                    keys = p.keys

                if keys[BLOCK].isDown and keys[BLOCK].buffer == KEY_BUFFER:
                    if p.char.techBuffer == TECH_BUFFER_MIN:
                        p.char.techBuffer = TECH_BUFFER_MAX

                self.updateBuffers(keys)
                self.act(p, keys)
                self.checkReversable(p)
                self.checkForGround(i, p)
                self.checkForEdge(p, isFlash)

                if self.returnCode[i] != 0:
                    p.char.retreat.value = 0

                self.checkForFX(i, p)

                if not p.char.dropThroughPlatform is None:
                    p.char.dropThroughPlatform = self.checkForPlatform(p)

            if not isFlash:
                self.resetHitMemory()

                self.updateProjectiles()

                self.checkForBlock()
                self.checkForProjectileBlock()

                for i, p in enumerate(self.players):
                    if self.returnCode[i] != 1:
                        self.actOnBlock(i, p)

                self.checkForHits()
                self.checkForProjectileHit()

                for i, p in enumerate(self.players):
                    if self.returnCode[i] != 1:
                        self.actOnHit(i, p)

                self.checkGrabPair()

            for i, p in enumerate(self.players):
                if (isFlash) and (not p.currMove.isSuperFlash):
                    continue

                p.update()
                self.checkShoot(p)
                p.char.di()

            if not isFlash:
                self.checkDisplacement()

            newList = []

            for f in self.fx:
                f.update()

                if not f.removeFlag:
                    newList.append(f)

            self.fx = newList

    def checkFrameByFrame(self):
        highest = 0

        # I have no idea what's going on here lol
        for i in xrange(len(self.frameByFrame)):
            if self.frameByFrame[i] > highest:
                highest = self.frameByFrame[i]
            if self.frameByFrame[i] == 2:
                self.frameByFrame[i] = 1

        return (highest == 1)

    def updateProjectiles(self):
        for p in self.projectiles:
            p.update()
            self.checkProjForEdge(p)
            self.checkProjForDissolve(p)

        self.projectiles = filter(lambda p: not p.destroy, self.projectiles)

    def key(self, inKey):
        if settings.ENV == settings.CLIENT:
            key = self.getLocalPlayer().keys[inKey.key]
            key.isDown = inKey.isDown

            if key.isDown:
                key.buffer = KEY_BUFFER

    def updateBuffers(self, keys):
        for k in keys.values():
            if k.buffer > 0:
                k.buffer -= 1

    def wasKeyPressed(self, k, keys):
        if k == -1:
            return ((keys[LEFT].buffer > 0) or (keys[RIGHT].buffer > 0))
        else:
            return (keys[k].buffer > 0)

    def act(self, p, keys):
        char = p.char
        char.actLeft = True
        u, d = p.upOrDown()
        l, r = p.leftOrRight()

        if char.hp.value <= 0 and not char.currMove.isDead:
            char.setCurrMove('deadFalling')
            char.inAir = True
            return

        if not char.keyTowardFacing():
            char.actTransition('noXMove')
        if char.holdJump:
            if char.vel[1] > 0 or (not keys[JUMP].isDown):
                char.unholdJump()
        if char.onHitTrigger:
            char.actTransition('onHit')
        if char.techBuffer >= 0 and char.canTech:
            if char.actTransition('tech'):
                char.techBuffer = TECH_BUFFER_MIN
        if char.canAct():
            if d:
                char.actTransition('doDuck')
            if l or r:
                if (l and self.wasKeyPressed(LEFT, keys)):
                    keys[LEFT].buffer = 0
                    if (char.dashBuffer[0] > 0 and char.dashBuffer[0] < DASH_BUFFER_MAX):
                        if char.actTransitionFacing('doDash', l, r):
                            char.dashBuffer = [0, 0]
                    else:
                        char.dashBuffer[0] = DASH_BUFFER_MAX
                        char.dashBuffer[1] = 0

                if (r and self.wasKeyPressed(RIGHT, keys)):
                    keys[RIGHT].buffer = 0
                    if (char.dashBuffer[1] > 0 and char.dashBuffer[1] < DASH_BUFFER_MAX):
                        if char.actTransitionFacing('doDash', l, r):
                            char.dashBuffer = [0, 0]
                    else:
                        char.dashBuffer[1] = DASH_BUFFER_MAX
                        char.dashBuffer[0] = 0

                char.actTransitionFacing('doWalk', l, r)
                if l:
                    if char.facingRight:
                        char.actTransition('backward')
                    else:
                        char.actTransition('forward')
                elif r:
                    if char.facingRight:
                        char.actTransition('forward')
                    else:
                        char.actTransition('backward')
            if u:
                char.actTransition('up')
            if not d:
                char.actTransition('stopDuck')
            if self.wasKeyPressed(ATT_A, keys):
                if u:
                    if char.actTransition('attackAUp'):
                        keys[ATT_A].buffer = 0
                elif d:
                    if char.actTransition('attackADown'):
                        keys[ATT_A].buffer = 0
                else:
                    if char.actTransition('attackA'):
                        keys[ATT_A].buffer = 0
            if self.wasKeyPressed(ATT_B, keys):
                if u:
                    if char.actTransition('attackBUp'):
                        keys[ATT_B].buffer = 0
                    elif char.aerialCharge:
                        if char.actTransition('attackBUpCharge'):
                            keys[ATT_B].buffer = 0
                            char.aerialCharge = False

                elif d:
                    if char.actTransition('attackBDown'):
                        keys[ATT_B].buffer = 0
                    elif char.aerialCharge:
                        if char.actTransition('attackBDownCharge'):
                            keys[ATT_B].buffer = 0
                            char.aerialCharge = False

                else:
                    if char.actTransition('attackB'):
                        keys[ATT_A].buffer = 0
            if self.wasKeyPressed(JUMP, keys):
                if not self.checkForPlatform(p) is None:
                    if char.actTransition('dropThrough'):
                        self.dropThrough(p)
                if char.actTransitionFacing('jump', l, r):
                    keys[JUMP].buffer = 0
            if keys[BLOCK].isDown:
                if d:
                    if char.actTransition('downBlock'):
                        keys[BLOCK].buffer = 0
                else:
                    if char.actTransition('block'):
                        keys[BLOCK].buffer = 0
            if self.wasKeyPressed(SUPER, keys):
                if char.superEnergy.isMax() and self.endingVal == -1:
                    if char.actTransition('super'):
                        keys[SUPER].buffer = 0
                        char.superEnergy.setToMin()

            if not keys[ATT_A].isDown:
                char.actTransition('releaseA')
            if not keys[ATT_B].isDown:
                char.actTransition('releaseB')
            if not keys[BLOCK].isDown:
                char.actTransition('releaseBlock')

            lev = char.getCatEnergyLevel()
            if lev == 1:
                char.actTransition('bladelv1')
            if lev == 2:
                char.actTransition('bladelv2')
            if lev == 3:
                char.actTransition('bladelv3')

    def checkReversable(self, p):
        if p.char.currFrame == 0 and p.char.currSubframe == 1:
            if p.char.currMove.reversable:
                l, r = p.leftOrRight()

                if l:
                    p.char.facingRight = False
                if r:
                    p.char.facingRight = True

    def checkForGround(self, i, c):
        old = c.char.inAir
        landed = False
        p = self.checkForPlatform(c)
        if p == c.char.dropThroughPlatform:
            p = None
        if (c.char.preciseLoc[1] >= self.arena.height - BATTLE_AREA_FLOOR_HEIGHT):
            c.char.preciseLoc[1] = self.arena.height - BATTLE_AREA_FLOOR_HEIGHT
            landed = True
        elif (not p is None):
            landed = True
            c.char.preciseLoc[1] = p.rect.top

        if landed:
            if (c.char.vel[1] > 0):
                c.char.inAir = False
                c.char.vel[1] = 0.0
                c.char.aerialCharge = True
                if old and (not c.char.currMove.ignoreGroundAir):
                    c.char.transToGround()
                    self.createTransitionDust(i, c)
        else:
            c.char.inAir = True
            if not old and (not c.char.currMove.ignoreGroundAir):
                c.char.transToAir()

    def dropThrough(self, p):
        p.char.dropThroughPlatform = self.checkForPlatform(p)

    def checkForPlatform(self, c):
        if c.char.vel[1] < 0:
            return None

        for p in self.platforms:
            if p.rect.colliderect(c.char.footRect):
                return p
        return None

    def checkDisplacement(self):
        for i in xrange(2):
            m = self.players[i].char.currMove
            if (m.grabPos is not None) or (m.grabVal != 0) or (m.isDead) or (m.isOnGround) or (self.returnCode[i] == 1):
                return

        displace = {}

        for p in self.players:
            displace[p] = 0

        for p, q in combinations(self.players):
            pFoot = p.char.footRect
            qFoot = q.char.footRect

            if pFoot.colliderect(qFoot):
                if pFoot.left <= qFoot.left:
                    displace[p] -= 1
                    displace[q] += 1
                else:
                    displace[p] += 1
                    displace[q] -= 1

        for p in self.players:
            p.char.preciseLoc[0] += displace[p] * DISPLACEMENT_AMOUNT

    def checkForEdge(self, p, isFlash):
        check = False
        if p.char.preciseLoc[0] < BATTLE_EDGE_COLLISION_WIDTH:
            p.char.preciseLoc[0] = BATTLE_EDGE_COLLISION_WIDTH
            check = True
        if p.char.preciseLoc[0] > self.arena.width - BATTLE_EDGE_COLLISION_WIDTH:
            p.char.preciseLoc[0] = self.arena.width - BATTLE_EDGE_COLLISION_WIDTH
            check = True

        if not p.char.currMove.canRetreat:
            check = False

        if p.char.currMove.isDead:
            p.char.retreat.value = 0
        elif self.retreatPhase == 2 and not isFlash:
            if self.endingVal in [-1, 0, 1]: 
                if check:
                    if self.endingVal == -1:
                        amount = RETREAT_ADD
                    else:
                        amount = RETREAT_ADD_FAST
                    p.char.retreat.add(amount)
                else:
                    p.char.retreat.add(-RETREAT_RECEED)
            else:
                p.char.retreat.add(-RETREAT_RECEED_FAST)

    def getHighestRetreat(self):
        high = -1
        highest = None

        for i, p in enumerate(self.players):
            if p.char.retreat.value > high:
                high = p.char.retreat.value
                highest = i

        return highest

    def checkShoot(self, p):
        m = p.char.currMove
        for s in m.shoot:
            if s[0] == p.char.currFrame and p.char.canShoot:
                proj = copy.copy(p.char.projectiles[s[1]].copySelf())
                proj.shooter = p.char
                p.char.canShoot = False

                poffset = s[2]
                temp = p.char.preciseLoc
                y = temp[1] + poffset[1]

                if p.char.facingRight:
                    x = temp[0] + poffset[0]
                else:
                    x = temp[0] - poffset[0]

                proj.facingRight = p.char.facingRight
                proj.preciseLoc = [x, y]
                self.projectiles.append(proj)

    def checkProjForEdge(self, p):
        if ( (p.char.preciseLoc[0] < (0 - PROJECTILE_SCREEN_ALLOWANCE))
             or (p.char.preciseLoc[0] > (self.arena.width + PROJECTILE_SCREEN_ALLOWANCE))
             or (p.char.preciseLoc[1] < (0 - PROJECTILE_SCREEN_ALLOWANCE))
             or (p.char.preciseLoc[1] > (self.arena.height + PROJECTILE_SCREEN_ALLOWANCE)) ):
            p.char.destroy = True

    def checkProjForDissolve(self, p):
        if (p.dissolveOnPhysical) and (not p.isEndingAnimation()):
            if p.preciseLoc[1] >= self.arena.height - BATTLE_AREA_FLOOR_HEIGHT:
                p.liveTime = 0
        if (p.hitsRemaining <= 0):
            p.liveTime = 0

        if (p.isEndingAnimation()) and (p.currFrame == len(p.currMove.frames)-1):
            p.destroy = True
            p.currFrame = 0

    def getChecksum(self):
        tempsum = 0
        for p in self.players:
            for i in p.char.preciseLoc:
                tempsum += int(i)

        checksum = chr(tempsum % 256)

        return checksum

    def reverse01(self, val):
        if val == 0:
            return 1
        elif val == 1:
            return 0
        return val

    def resetHitMemory(self):
        self.hitMemory = [None, None]
        self.blockMemory = [None, None]
        self.fxMemory = [[], []]

    def checkGrabPair(self):
        for i in xrange(2):
            if i == 0:
                a = 0
                b = 1
            else:
                a = 1
                b = 0

            aChar = self.players[a].char
            bChar = self.players[b].char

            if not aChar.currMove.isThrow():
                if ( ((aChar.currMove.isGrab()) and (not bChar.currMove.isGrabbed()))
                     or ((not aChar.currMove.isGrab()) and (bChar.currMove.isGrabbed())) ):
                    aChar.setCurrMove('grabRelease')
                    bChar.setCurrMove('grabbedRelease')
                    return

            if aChar.currMove.isGrab() and bChar.currMove.isGrabbed():
                offset = self.getGrabOffset(aChar, bChar)

                aChar.preciseLoc = sub_points(bChar.preciseLoc, offset)
                bChar.preciseLoc = add_points(aChar.preciseLoc, offset)
                bChar.inAir = False

    def getGrabOffset(self, p1, p2):
        if p1.char.facingRight:
            mult = 1
        else:
            mult = -1

        offset = [ p1.char.currMove.grabPos[0] * mult,
                   p1.char.currMove.grabPos[1] ]

        temp = [ p2.char.currMove.grabPos[0] * (mult * -1),
                 p2.char.currMove.grabPos[1] ]

        return sub_points(offset, temp)

    def checkForBlock(self):
        for i, p in enumerate(self.players):
            for j, q in enumerate(self.players):
                if (q.char is not p.char) and p.char.attackCanHit:
                    for h in p.char.getHitboxes():
                        if h.ignoreBlock():
                            continue

                        for r in q.char.getBlockboxes():
                            hRect = getAdjustedBox(p.char, h)
                            rRect = getAdjustedBox(q.char, r)

                            if hRect.colliderect(rRect):
                                if (self.blockMemory[j] is None):
                                    self.blockMemory[j] = [h, p]
                                    p.char.attackCanHit = False
                                    p.char.onHitTrigger = True

                                if q.char.currMove == q.char.getMoves()['blocking']:
                                    ind = 0
                                elif q.char.currMove == q.char.getMoves()['lowBlocking']:
                                    ind = 1
                                else:
                                    ind = 2

                                self.fxMemory[j].append(q.char.getBlockFXPoint(ind))

    def checkForHits(self):
        if self.blockMemory is None:
            self.fxMemory = [[], []]
        for i, p in enumerate(self.players):
            for j, q in enumerate(self.players):
                if (q.char is not p.char) and p.char.attackCanHit:
                    for h in p.char.getHitboxes():
                        for r in q.char.getHurtboxes():
                            hRect = getAdjustedBox(p.char, h)
                            rRect = getAdjustedBox(q.char, r)

                            if hRect.colliderect(rRect):
                                if q.char.blockstun > 0:
                                    if (self.blockMemory[j] is None):
                                        self.blockMemory[j] = [h, p]
                                        p.char.attackCanHit = False
                                        p.char.onHitTrigger = True
                                else:
                                    if (self.hitMemory[j] is None):
                                        self.hitMemory[j] = [h, p]
                                        p.char.attackCanHit = False
                                        p.char.onHitTrigger = True

                                self.fxMemory[j].append(average_points(
                                    hRect.center, rRect.center))

    def checkForProjectileBlock(self):
        for proj in self.projectiles:
            if not proj.canHit():
                continue

            for j, q in enumerate(self.players):
                if q.char is not proj.shooter:
                    for h in proj.getHitboxes():
                        if h.ignoreBlock():
                            continue
                        for r in q.char.getBlockboxes():
                            hRect = getAdjustedBox(proj, h)
                            rRect = getAdjustedBox(q.char, r)

                            if hRect.colliderect(rRect):
                                if (self.blockMemory[j] is None):
                                    self.blockMemory[j] = [h, proj]

                                if q.char.currMove == q.char.getMoves()['blocking']:
                                    ind = 0
                                elif q.char.currMove == q.char.getMoves()['lowBlocking']:
                                    ind = 1
                                else:
                                    ind = 2

                                self.fxMemory[j].append(q.char.getBlockFXPoint(ind))

    def checkForProjectileHit(self):
        for proj in self.projectiles:
            if not proj.canHit():
                continue

            for j, q in enumerate(self.players):
                if q.char is not proj.shooter:
                    for h in proj.getHitboxes():
                        for r in q.char.getHurtboxes():
                            hRect = getAdjustedBox(proj, h)
                            rRect = getAdjustedBox(q.char, r)

                            if hRect.colliderect(rRect):
                                if (self.hitMemory[j] is None):
                                    self.hitMemory[j] = [h, proj]

                                self.fxMemory[j].append(average_points(
                                    hRect.center, rRect.center))

    def createFX(self, h, hitter, hittee, pointList, blocked):
        fxPos = average_point_list(pointList)

        if blocked:
            self.fx.append(fx.FX(fxPos, hitter.char.facingRight, 'block'))
        elif hitter.char.currMove.isGrab():
            self.fx.append(fx.FX(fxPos, hitter.char.facingRight, 'grab'))
        else:
            if not h.noStandardFX():
                self.fx.append(fx.FX(fxPos, hitter.char.facingRight, 'pow'))
                self.fx.append(fx.FX(fxPos, hitter.char.facingRight, 'side'))

    def actOnBlock(self, i, p):
        self.actOnHit(i, p, True)

    def actOnHit(self, i, p, blocked=False):
        if blocked:
            memory = self.blockMemory
        else:
            memory = self.hitMemory

        if not memory[i] is None:
            mem = memory[i][0]
            hitter = memory[i][1]

            p.char.facingRight = not hitter.char.facingRight

            grab = mem.getGrabData()
            if grab is not None:
                self.actOnGrab(i, p, mem, hitter, grab)
                return

            damage = int(mem.damage * hitter.char.getDamageMultiplier())
            chip = mem.chipDamagePercentage
            stun = mem.stun
            prop = mem.properties

            kb = mem.knockback
            if blocked:
                kb *= BLOCKED_KNOCKBACK_FACTOR

            xVel = math.cos(math.radians(mem.angle)) * kb
            yVel = math.sin(math.radians(mem.angle)) * kb

            if blocked:
                yVel *= BLOCKED_LIFT_RESIST

            yVel *= -1
            if p.char.facingRight:
                xVel *= -1

            if not p.char.inAir:
                if (mem.angle > 180) and (not blocked):
                    yVel *= -1

            if not blocked:
                p.char.getHit(damage, stun, (xVel, yVel))

            p.char.freezeFrame = mem.freezeFrame
            hitter.char.freezeFrame = mem.freezeFrame

            hitter.char.performHit()

            p.char.canTech = not mem.untechable()
            p.char.techBuffer = TECH_BUFFER_MIN

            if blocked:
                damage = int(damage * chip)
                p.char.getBlockstun(damage, stun, (xVel, yVel), prop)

            if mem.reverseUserFacing():
                hitter.facingRight = (not hitter.facingRight)

            if mem.reverseTargetFacing():
                p.char.facingRight = (not p.char.facingRight)

            self.createFX(mem, hitter, p, self.fxMemory[i], blocked)

    def actOnGrab(self, i, p, mem, hitter, grab):
        hitter.char.setCurrMove(grab[1])
        p.char.setCurrMove(grab[2])

        offset = self.getGrabOffset(hitter, p)

        p.char.preciseLoc = add_points(hitter.char.preciseLoc, offset)

        self.createFX(mem, hitter, p, self.fxMemory[i], False)

    def checkForFX(self, i, p):
        if self.returnCode[i] != 1 and p.char.currSubframe == 0 and p.char.canEffect:
            for i in p.char.getCurrentFrame().fx:
                facing = i[2]
                basePos = [i[1][0], i[1][1]]
                if not p.char.facingRight:
                    facing = not facing
                    basePos[0] *= -1
                pos = add_points(p.char.preciseLoc, basePos)
                self.fx.append(fx.FX(pos, facing, i[0]))
                p.char.canEffect = False

    def createTransitionDust(self, i, p):
        if p.char.currMove == p.char.getMoves()['groundHit'] or p.char.currMove.isStun or self.returnCode[i] == 1:
            return

        pos = add_points(p.char.preciseLoc, (0,0))
        self.fx.append(fx.FX(pos, True, 'dust'))
        self.fx.append(fx.FX(pos, False, 'dust'))

    def checkEnding(self):
        if self.endingVal in [-1, 0, 1]:
            for i, p in enumerate(self.players):
                if p.char.retreat.isMax():
                    self.returnCode[i] = 1
                    p.char.retreat.setToMin()
                    p.char.preciseLoc[1] = self.arena.height - BATTLE_AREA_FLOOR_HEIGHT

                    if self.endingVal == -1:
                        self.endingVal = 0

        if self.endingVal == -1:
            anyDead = False

            for p in self.players:
                if p.char.currMove.isDead:
                    anyDead = True

            if anyDead:
                self.endingVal = 0

                for proj in self.projectiles:
                    proj.freezeFrame += DEATH_FREEZE_FRAME

                for i, p in enumerate(self.players):
                    p.char.freezeFrame += DEATH_FREEZE_FRAME
                    if p.char.currMove.isDead:
                        if p.char.vel[1] > DEATH_FLY_VERT_VEL_MIN:
                            p.char.vel[1] = DEATH_FLY_VERT_VEL_MIN
                        self.returnCode[i] = -1
                    else:
                        self.returnCode[i] = 0

    def superDarken(self):
        for p in self.players:
            if p.char.currMove.isSuperFlash:
                return True

        return False

    def isFlash(self):
        for p in self.players:
            if p.char.currMove.isSuperFlash:
                return True

        return False

class State(Model):
    def __init__(self, model):
        self.terrainLeft = copy.deepcopy(model.terrainLeft)
        self.terrainRight = copy.deepcopy(model.terrainRight)
        self.arena = copy.deepcopy(model.arena)
        self.players = copy.deepcopy(model.players)
        self.frameByFrame = copy.deepcopy(model.frameByFrame)
        self.returnCode = copy.deepcopy(model.returnCode)
        self.projectiles = copy.deepcopy(model.projectiles)
        self.retreatProhibitTime = copy.deepcopy(model.retreatProhibitTime)
        self.retreatPhase = copy.deepcopy(model.retreatPhase)
        self.endingVal = copy.deepcopy(model.endingVal)
        self.endingValTick = copy.deepcopy(model.endingValTick)
        self.fx = copy.deepcopy(model.fx)
        self.platforms = copy.deepcopy(model.platforms)
        self.countdown = copy.deepcopy(model.countdown)

def testData():
    heroes = [hare.Hare(), hare.Hare()]

    for h in heroes:
        h.superEnergy.change(h.superEnergy.maximum)

    return [heroes, PLAINS, PLAINS]

def getPlatforms(leftTerrain, rightTerrain):
    platformsLeft = getPlatformsForSingleTerrain(leftTerrain, False)
    platformsRight = getPlatformsForSingleTerrain(rightTerrain, True)
    masterList = []
    masterList.extend(platformsLeft)
    masterList.extend(platformsRight)
    return masterList

def getPlatformsForSingleTerrain(terrain, isRight):
    platforms = []

    HALF_SCREEN = (BATTLE_ARENA_SIZE[0] / 2)

    if terrain == PLAINS:
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 200, terrain ) )
    elif terrain == FOREST:
        platforms.append( platform.Platform(
            (100, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), 175, terrain ) )
        platforms.append( platform.Platform(
            (375, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 280), HALF_SCREEN - 350, terrain ) )
    elif terrain == MOUNTAIN:
        platforms.append( platform.Platform(
            (400, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 400, terrain ) )
        platforms.append( platform.Platform(
            (150, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 280), 140, terrain ) )
        platforms.append( platform.Platform(
            (400, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 380), HALF_SCREEN - 400, terrain ) )
        platforms.append( platform.Platform(
            (150, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 480), 140, terrain ) )
    elif terrain == SNOW:
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 200, terrain ) )
    elif terrain == FORTRESS:
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 180), HALF_SCREEN - 200, terrain ) )
        platforms.append( platform.Platform(
            (200, BATTLE_ARENA_SIZE[1] - BATTLE_AREA_FLOOR_HEIGHT - 380), HALF_SCREEN - 200, terrain ) )

    if isRight:
        for p in platforms:
            p.rect.right = BATTLE_ARENA_SIZE[0] - p.rect.left

    return platforms
