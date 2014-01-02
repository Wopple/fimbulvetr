from common import mvc

class ResultModel(mvc.Model):
    def __init__(self, resultQueue):
        super(Model, self).__init__()
        self.resultQueue = resultQueue

    def update(self):
        if not self.resultQueue.empty():
            self.result = self.resultQueue.get()
            self.advanceNow = True
