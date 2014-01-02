from common.constants import *
from client.constants import *

from common import boundint
from common.util.rect import Rect

class Countdown(object):
    def __init__(self, time, fps=FRAME_RATE):
        self.time = time
        self.tick = boundint.BoundInt(0, fps, 0, True)

        size = (SCREEN_SIZE[0], COUNTDOWN_FONT.get_linesize() + 4)
        pos = (0, (SCREEN_SIZE[1] / 2) - (size[1] / 2) - 15)
        self.rect = Rect(pos, size)
        self.startFlag = False

    def setTime(self, time):
        self.time = time

    def update(self):
        if self.isValid():
            self.tick.inc()

            if self.tick.isMin():
                self.time -= 1

                if self.time == 0:
                    self.startFlag = True

    def isValid(self):
        return (self.time >= 0)

    def isGoing(self):
        return (self.time > 0)

    def checkStartFlag(self):
        if self.startFlag:
            self.startFlag = False
            return True
        else:
            return False
