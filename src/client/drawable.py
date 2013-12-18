import os

import pygame

from common.constants import *
from client.constants import *

class Drawable(object):
    
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

