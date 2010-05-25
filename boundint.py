import sys

class BoundInt(object):
    def __init__(self, inMin, inMax, inVal):

        if inMin >= inMax:
            raise RuntimeError, "Minimum must be smaller than Maximum"
        if (inVal < inMin) or (inVal > inMax):
            raise RuntimeError, "Initial value must be within bounds"

        self.minimum = inMin
        self.maximum = inMax
        self.value = inVal

    def add(self, v):
        self.value += v
        self.checkBounds()

    def change(self, v):
        self.value = v
        self.checkBounds()

    def checkBounds(self):
        if self.value < self.minimum:
            self.value = self.minimum
        if self.value > self.maximum:
            self.value = self.maximum
