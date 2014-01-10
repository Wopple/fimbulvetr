import pygame

from common.constants import *
from client.constants import *

from client.drawable import ItemDrawable
from client.textrect import render_textrect

IMAGE_DATA = 0
IMAGE = 0
OFFSET = 1

class FXDrawable(ItemDrawable):
    def __init__(self, item):
        super(FXDrawable, self).__init__(item, rect=item.rect)

    def draw(self, screen, camera=None):
        frame = self.item.frames[self.item.frameNum]
        imageData = FX_IMAGES[frame[IMAGE_DATA]]
        image = imageData[IMAGE]
        offset = imageData[OFFSET]
        width = image.get_size()[0]

        if not self.item.facingRight:
            image = pygame.transform.flip(image, True, False)
            offset = (-offset[0] + width, offset[1])

        self.rect = Rect(self.getPos(offset), width)
        self.image = image
        super(FXDrawable, self).draw(screen, camera)

    def getPos(self, offset):
        return (int(self.item.preciseLoc[0]) - offset[0],
                int(self.item.preciseLoc[1]) - offset[1])
