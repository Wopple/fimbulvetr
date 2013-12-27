from common import mvc

class Model(mvc.Model):
    def __init__(self, queue):
        super(Model, self).__init__()
        self.queue = queue

    def update(self):
        if not self.queue.empty():
            self.result = self.queue.get()
            self.advanceNow = True
