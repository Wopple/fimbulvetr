import copy

from common import move

class Projectile(object):
    def __init__(self):
        self.preciseLoc = [50.0, 50.0]
        self.accel = [0.0, 0.0]
        self.vel = [0.0, 0.0]
        self.facingRight = True
        self.actLeft = True
        self.dissolveOnPhysical = False
        self.liveTime = None
        self.shooter = None
        self.hitsRemaining = 1
        self.freezeFrame = 0

        self.initMoves()
        self.setCurrMove('flying')
        self.destroy = False

    def update(self):
        if self.freezeFrame == 0:
            
            if not self.liveTime is None:
                if self.liveTime > 0:
                    self.liveTime -= 1
                if (self.liveTime <= 0 and not self.isEndingAnimation()):
                    if self.hitsRemaining == 0:
                        self.setCurrMove('explode')
                        self.accel = [0.0, 0.0]
                        self.vel = [0.0, 0.0]
                    else:
                        self.setCurrMove('dissolve')
            
            self.proceedFrame()
            self.frameSpecial()
            
            for i in range(2):
                self.vel[i] += self.accel[i]
                self.preciseLoc[i] += self.vel[i]
                
        if self.freezeFrame > 0:
            self.freezeFrame -= 1

    def getCurrentFrame(self):
        return self.currMove.frames[self.currFrame]

    def frameSpecial(self):
        f = self.getCurrentFrame()
        if not f.setVelX is None:
            self.vel[0] = f.setVelX * self.facingMultiplier()
            self.accelToZero()
        if not f.setVelY is None:
            self.vel[1] = f.setVelY
            self.accelToZero()
        if not f.addVelX is None:
            self.vel[0] += f.addVelX * self.facingMultiplier()
        if not f.addVelY is None:
            self.vel[1] += f.addVelY
        if not f.setVelYIfDrop is None:
            if self.vel[1] > 0:
                self.vel[1] = f.setVelYIfDrop
                self.accelToZero()

    def accelToZero(self):
        self.accel = [0.0, 0.0]

    def facingMultiplier(self):
        if self.facingRight:
            return 1
        else:
            return -1

    def initMoves(self):
        self.moves = {}
        self.moves['flying'] = move.baseProjFlying()
        self.moves['dissolve'] = move.baseBlank()
        self.moves['explode'] = move.baseBlank() 

    def setCurrMove(self, index, frame=0):
        self.currMove = self.moves[index]
        self.currFrame = frame
        self.currSubframe = 0

        if len(self.currMove.frames) == 0:
            self.currMove = self.moves['flying']
            self.destroy = True

    def proceedFrame(self):
        frame = self.currMove.frames[self.currFrame]
        self.setImage(frame.image, frame.offset)

        self.currSubframe += 1
        if self.currSubframe == frame.length:
            self.currSubframe = 0
            t = self.actTransition('exitFrame', self.currFrame)
            if not t:
                self.currFrame += 1

        if self.currFrame >= len(self.currMove.frames):
            self.currMove = self.moves['flying']
            self.destroy = True

    def checkTransition(self, key, var1=None, var2=None):
        t = self.currMove.transitions[key]
        if t is None:
            return False

        if not t.rangeMin is None:
            if self.currFrame < t.rangeMin:
                return False

        if not t.rangeMax is None:
            if self.currFrame > t.rangeMax:
                return False

        if (key == 'exitFrame'):
            i = t.var1
            if i == -1:
                i = len(self.currMove.frames) - 1
            if i != var1:
                return False

        return True

    def actTransition(self, key, var1=None, var2=None):
        t = self.currMove.transitions[key]
        if self.actLeft and self.checkTransition(key, var1, var2):
            self.setCurrMove(t.destination)
            if not key == 'exitFrame':
                self.actLeft = False
            return True
        else:
            return False

    def copySelf(self):
        self.preciseLoc = copy.copy(self.preciseLoc)
        self.accel = copy.copy(self.accel)
        self.vel = copy.copy(self.vel)
        return self

    def canHit(self):
        return (self.freezeFrame == 0 and self.hitsRemaining > 0)

    def getHitboxes(self):
        return self.getCurrentFrame().hitboxes

    def getDamageMultiplier(self):
        if not self.shooter is None:
            return self.shooter.getDamageMultiplier()
        else:
            return 1.0

    def performHit(self):
        self.hitsRemaining -= 1

    def isEndingAnimation(self):
        return self.currMove == self.moves['dissolve'] or self.currMove == self.moves['explode']
