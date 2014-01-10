from client.constants import *

class Drawable(object):
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image

    def draw(self, screen, camera=None):
        if camera is None:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(self.image, adjustToCamera(self.rect.topleft, camera))

class ItemDrawable(Drawable):
    """
    This is intended to wrap a model-only item with a Drawable
    so it can be drawn in a view.
    """

    def __init__(self, item, rect=None, image=None):
        super(ItemDrawable, self).__init__(rect, image)
        self.item = item
