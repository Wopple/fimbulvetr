class BoundInt(object):
    def __init__(self, inMin, inMax, inVal, loop=False):

        if inMin > inMax:
            raise RuntimeError, "Minimum must be smaller than Maximum"
        if (inVal < inMin) or (inVal > inMax):
            raise RuntimeError, "Initial value must be within bounds"

        self.minimum = inMin
        self.maximum = inMax
        self.value = inVal
        self.loop = loop

    def add(self, v):
        self.value += v
        self.checkBounds()

    def sub(self, v):
        self.value -= v
        self.checkBounds()

    def inc(self):
        self.add(1)

    def dec(self):
        self.sub(1)

    def change(self, v):
        self.value = v
        self.checkBounds()

    def checkBounds(self):
        if self.loop:
            if self.value < self.minimum:
                self.value = self.maximum
            if self.value > self.maximum:
                self.value = self.minimum
        else:
            if self.value < self.minimum:
                self.value = self.minimum
            if self.value > self.maximum:
                self.value = self.maximum

    def atBound(self):
        return ((self.value == self.minimum) or (self.value == self.maximum))

    def isMax(self):
        return (self.value == self.maximum)

    def isMin(self):
        return (self.value == self.minimum)

    def setToMin(self):
        self.value = self.minimum

    def setToMax(self):
        self.value = self.maximum
