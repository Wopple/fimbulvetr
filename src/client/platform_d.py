import pygame

from common.constants import *
from client.constants import *

from client.drawable import ItemDrawable

class PlatformDrawable(ItemDrawable):
    def __init__(self, item):
        super(PlatformDrawable, self).__init__(item, rect=item.rect)

    def draw(self, screen, inOffset=(0, 0)):
        image = pygame.Surface((self.rect.width, self.rect.height))
        image.fill(BLACK)
        innerImage = pygame.Surface((self.rect.width,
                                     self.rect.height - (PLATFORM_BORDER_SIZE * 2)))
        innerImage.fill(PLATFORM_COLORS[self.item.terrain])
        image.blit(innerImage, (0, PLATFORM_BORDER_SIZE))
        screen.blit(self.image, add_points(self.rect.topleft, inOffset))
