from common import mvc

class QueueModel(mvc.Model):
    def __init__(self, queue):
        super(Model, self).__init__()
        self.queue = queue

    def update(self):
        if not self.queue.empty():
            self.result = self.queue.get()
            self.advanceNow = True
