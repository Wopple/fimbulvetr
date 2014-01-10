from common.constants import *
from client.constants import *

from client.drawable import ItemDrawable
from client.textrect import render_textrect

class CountdownDrawable(ItemDrawable):
    def __init__(self, item):
        super(CountdownDrawable, self).__init__(item, rect=item.rect)

    def draw(self, screen, camera=None):
        if self.item.isValid():
            if self.item.time == 0:
                msg = "GO!"
            else:
                msg = str(self.item.time)

            self.image = render_textrect(msg, COUNTDOWN_FONT, self.item.rect,
                                         COUNTDOWN_COLOR, ALMOST_BLACK, 1, True)

            super(CountdownDrawable, self).draw(screen, camera)
