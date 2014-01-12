import pygame

from common.constants import *
from client.constants import *

from common import fx
from client.drawable import ItemDrawable
from client.textrect import render_textrect

class FXDrawable(ItemDrawable):
    def __init__(self, item):
        super(FXDrawable, self).__init__(item)

    def draw(self, screen, camera=None):
        frame = self.item.frames[self.item.frameNum]
        imageData = FX_IMAGES[frame[fx.IMAGE_DATA]]
        image = imageData[IMAGE]
        offset = imageData[OFFSET]
        size = image.get_size()

        if not self.item.facingRight:
            image = pygame.transform.flip(image, True, False)
            offset = (-offset[0] + size[0], offset[1])

        self.rect = Rect(self.getPos(offset), size)
        self.image = image
        super(FXDrawable, self).draw(screen, camera)

    def getPos(self, offset):
        return (int(self.item.preciseLoc[0]) - offset[0],
                int(self.item.preciseLoc[1]) - offset[1])
