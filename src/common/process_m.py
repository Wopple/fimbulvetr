from common.constants import FRAME_RATE

from common import mvc

class ProcessModel(mvc.MVCObject):
    """
    Subclasses of this Model are designed to run in a
    separate process. They do their work at their own
    rate and return a result when they finish by
    putting the result in the given queue.
    """

    def __init__(self, queue, fps=FRAME_RATE):
        super(ProcessModel, self).__init__()
        self.queue = queue

    def setResult(self, result):
        self.queue.put(result)
