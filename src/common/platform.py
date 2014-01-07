from common.constants import *
from client.constants import *

from common.util.rect import Rect

class Platform(object):
    def __init__(self, inPos, inLength, inTerrain):
        self.rect = Rect(inPos, (inLength, PLATFORM_HEIGHT))
        self.terrain = inTerrain
