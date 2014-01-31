from common.constants import *
from client.constants import *

from common import boundint

IMAGE_DATA = 0
LENGTH = 1

class FX(object):
    def __init__(self, inPos, inFacing, inType):
        self.preciseLoc = inPos
        self.facingRight = inFacing
        self.frames = self.getFrames(inType)
        self.frameNum = 0
        self.subframeNum = 0
        self.removeFlag = False

    def update(self):
        self.subframeNum += 1
        if self.subframeNum >= self.frames[self.frameNum][LENGTH]:
            self.subframeNum = 0
            self.frameNum += 1
            if self.frameNum == len(self.frames):
                self.removeFlag = True

    def getFrames(self, t):
        f = []

        if t == FX_POW:
            f = [ [0, 3],
                  [1, 1],
                  [2, 1],
                  [3, 1] ]
        elif t == FX_SIDE:
            f = [ [7, 3],
                  [4, 1],
                  [5, 1],
                  [6, 1] ]
        elif t == FX_BLOCK:
            f = [ [8, 3],
                  [9, 1],
                  [10, 1],
                  [11, 1] ]
        elif t == FX_GRAB:
            f = [ [12, 4],
                  [13, 3]]
        elif t == FX_DUST:
            f = [ [14, 3],
                  [15, 2],
                  [16, 2],
                  [17, 2],
                  [18, 2] ]
        elif t == FX_SHOCKWAVE:
            f = [ [19, 2],
                  [20, 1],
                  [21, 1],
                  [22, 1],
                  [23, 1] ]
        elif t == FX_AIR_ELEMENT_SHOCKWAVE:
            f = [ [24, 2],
                  [25, 1],
                  [26, 1],
                  [27, 1],
                  [28, 1] ]
        elif t == FX_RUNIC_EXPLOSION:
            f = [ [29, 2],
                  [30, 1],
                  [31, 2],
                  [32, 2],
                  [33, 2] ]
        elif t == FX_RUNIC_FLAME_1:
            f = [ [35, 3],
                  [36, 1],
                  [37, 1],
                  [38, 1] ]
        elif t == FX_RUNIC_FLAME_2:
            f = [ [39, 3],
                  [40, 2],
                  [41, 1]]
        elif t == FX_RUNIC_FLAME_3:
            f = [ [42, 3],
                  [43, 2],
                  [44, 1]]
        elif t == FX_FULL_SHOCKWAVE:
            f = [ [45, 3],
                  [46, 2],
                  [47, 2],
                  [48, 2],
                  [49, 2],
                  [50, 2] ]

        return f
