import time
import copy

from common.constants import FRAME_RATE

from common import mvc
from common.util.framerate import FrameRate
from common.util.process import process

class ProcessModel(mvc.MVCObject):
    """
    Subclasses of this Model are designed to run in a
    separate process. They do their work at their own
    rate and return a result when they finish by
    putting the result in the given queue.
    """

    def __init__(self, resultQueue=None, stateQueue=None, fps=FRAME_RATE):
        super(ProcessModel, self).__init__()
        self.resultQueue = resultQueue
        self.stateQueue = stateQueue
        self.framerate = FrameRate(fps)
        self.done = False

    def setResult(self, result):
        self.resultQueue.put(result)
        self.done = True

    def start(self):
        self.framerate.start()

        while not self.done:
            self.update()
            self.stateQueue.put(self.getState())
            self.framerate.next()

    def process(self):
        self.resultQueue = process(self.start, queue=self.resultQueue)
