import os
import sys
import pygame

from common import mvc

from common.constants import *
from client.constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(self.model.baseSurface, self.model.baseSurfaceRect)
        for i in self.model.blackPanelPos:
            self.screen.blit(self.model.blackPanel, i)
        self.model.menu.draw(self.screen)
        if self.model.stage == 0:
            self.model.charMenu.draw(self.screen)
        else:
            if not self.model.descSurface is None:
                screen.blit(self.model.descSurface, self.model.blackPanelPos[0])
        if not self.model.characterToDisplay is None:
            self.model.characterToDisplay.draw(self.screen, (0, 0))

        if not self.model.superMoveNameText is None:
            self.screen.blit( self.model.superMoveNameText,
                               self.model.superMoveNameTextPos)

        if ((not self.model.leftPageArrow is None) and
            (not self.model.rightPageArrow is None)):
            self.model.leftPageArrow.draw(screen)
            self.model.rightPageArrow.draw(screen)


        if tickClock:
            pygame.display.flip()
