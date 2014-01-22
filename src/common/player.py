import weakref

from common.constants import *

from common.constants import KEY_TYPES
from common.util import exclusiveKeys

class Player(object):
    def __init__(self, type, char=None, keys=None, socket=None, netID=None):
        self.type = type
        self.char = char
        self.keys = keys
        self.socket = socket
        self.netID = netID

        if keys is None:
            self.keys = makeKeys()

        self.init()

    def __getstate__(self):
        state = self.__dict__.copy()

        if state.has_key('socket'):
            state.pop('socket')

        return state

    def __setstate__(self, state):
        self.__dict__ = state
        self.init()

    def init(self):
        if self.char is not None:
            self.char.player = weakref.ref(self)

    def update(self):
        self.char.update()

    def leftOrRight(self):
        return exclusiveKeys(self.keys[LEFT].isDown, self.keys[RIGHT].isDown)

    def upOrDown(self):
        return exclusiveKeys(self.keys[UP].isDown, self.keys[DOWN].isDown)

class Key(object):
    def __init__(self, isDown, buffer):
        self.isDown = isDown
        self.buffer = buffer

def makeKeys():
    keys = {}

    for key in KEY_TYPES:
        keys[key] = Key(False, 0)

    return keys
