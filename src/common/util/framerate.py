import time

class FrameRate(object):
    """ Simple frame rate limiter """

    def __init__(self, fps=60):
        self.fps = fps
        self.start()

    # public

    def start(self):
        self.prev = time.time()

    def next(self):
        self.prev = self.endFrame(self.prev)

    # private

    def endFrame(self, prev):
        while True:
            next = time.time()
            diff = (1.0 / self.fps) - (next - prev)

            if diff <= 0:
                break

            if diff > 0.0015:
                time.sleep(0.001)
            else:
                time.sleep(0)

        return next

if __name__ == "__main__":
    fps = 60
    rate = FrameRate(fps)

    for i in range(120):
        print "ping", (i % fps)
        rate.next()
