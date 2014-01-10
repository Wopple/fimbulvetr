from common import mvc

class ResultModel(mvc.Model):
    def __init__(self, resultQueue):
        super(ResultModel, self).__init__()
        self.resultQueue = resultQueue

    def update(self):
        if not self.resultQueue.empty():
            self.result = self.resultQueue.get()
            self.advanceNow = True

    def getResult(self):
        if self.resultQueue.empty():
            return None
        else:
            return self.resultQueue.get()
