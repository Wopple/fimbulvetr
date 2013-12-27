import os
import sys
import pygame

from common import mvc

import textrect
import boundint

from common.constants import *
from client.constants import *

from common.util.rect import Rect


class Model(mvc.Model):
    def __init__(self, fade):
        super(Model, self).__init__()
        
        self.bg = pygame.Surface(SCREEN_SIZE)
        self.bg.fill(BLACK)
        
        creditData =    [
                            ["Christopher \"Southpaw Hare\" Czyzewski", ["Lead Designer", "Lead Programmer", "Creative Director",
                                                                         "Marketing Director", "Distribution Director"]],
                            ["Daniel \"Wopple\" Tashjian", ["Programmer", "Tester"]]
                            ["Matthew Grisham", ["Gameplay Designer", "Map Designer"]],
                            ["Kit", ["Character Artist", "Map Artist", "Background Artist"]],
                            ["Raquel M. Richardson", ["Portrait Artist"]],
                            
                            ["Additional Testers", ["Randy Sabella", "Robert Morris", "Eric Collins", "Fox Zeta", "Coffeefox"]]
                        ]
        
        for data in creditData:
            header = data[0]
            subItems = data[1]
            
            headerRect = Rect((0, 0), (40, SCREEN_SIZE[1]))
            headerImage = textrect.render_textrect(header, CREDITS_HEADER_FONT, headerRect, ALMOST_BLACK, WHITE, 0, True)
            self.credits.append(CreditText(headerRect, headerImage))
        
        self.credits = []


class CreditText(object):
    def __init__(self, inRect, inImage):
        self.image = inImage
        self.rect = inRect
        self.velocity = [0, 0]

    def update(self):
        self.rect.left += self.velocity[0]
        self.rect.top += self.velocity[1]

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
