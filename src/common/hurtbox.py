from common.constants import *

class Hurtbox(object):
    def __init__(self, inRect):
        self.rect = inRect
        self.immunity = dict([(x, False) for x in ATTACK_PROPERTIES])
