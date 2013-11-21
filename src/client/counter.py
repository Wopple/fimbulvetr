class Counter(object):
    def __init__(self, value, minimum, maximum):
        self.value = value
        self.minimum = minimum
        self.maximum = maximum
        self.restricted = False

        if self.minimum > self.maximum:
            raise Exception

        if not self.isWithinBounds():
            raise Exception, ("Out of bounds: " +
                              str(self.minimum) + " <= " +
                              str(self.value) + " <= " +
                              str(self.maximum))

    def isWithinBounds(self):
        return (self.value < self.minimum) or (self.value > self.maximum)

    def inc(self):
        if self.restricted:
            if self.value < self.maximum:
                self.value += 1
        else:
            self.value += 1
            if self.value > self.maximum:
                self.value = self.minimum

    def dec(self):
        if self.restricted:
            if self.value > self.minimum:
                self.value -= 1
        else:
            self.value -= 1
            if self.value < self.minimum:
                self.value = self.maximum

    def isMin(self):
        if self.value == self.minimum:
            return True
        else:
            return False

    def isMax(self):
        if self.value == self.maximum:
            return True
        else:
            return False
