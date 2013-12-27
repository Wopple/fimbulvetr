class MVCObject(object):
    def __init__(self):
        self.undefUpdate = False

    def update(self):
        self.undefUpdate = True

    def checkError(self):
        return self.undefUpdate

class Model(MVCObject):
    def __init__(self, model=None, view=None):
        super(Model, self).__init__()
        self.view = view
        self.advanceNow = False
        self.backNow = False

    def setView(self, view):
        self.view = view

    def advance(self):
        return self.advanceNow

    def back(self):
        return self.backNow

    def either(self):
        return (self.advance() or self.back())

    def reset(self):
        self.advanceNow = False
        self.backNow = False

class View(MVCObject):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()
        self.model = model
        self.screen = screen

    def setModel(self, model):
        self.model = model

    def setScreen(self, screen):
        self.screen = screen

class Controller(MVCObject):
    def __init__(self, model=None, view=None):
        super(Controller, self).__init__()
        self.model = model
        self.view = view
        
    def setModel(self, model):
        self.model = model
        
    def setView(self, view):
        self.view = view
