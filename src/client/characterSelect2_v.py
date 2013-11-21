import os
import sys
import pygame

import mvc

from common.constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        for bg in self.model.bgs:
            bg.draw(self.screen)
        
        for panel in self.model.characterPanels:
            panel.draw(self.screen)
            
        self.model.mapPanel.draw(self.screen)
        
        for panel in self.model.readyPanels:
            if not panel is None:
                panel.draw(self.screen)
                
        if not self.model.goPanel is None:
                self.model.goPanel.draw(self.screen)
        
        if self.model.subScreen == 1:
            self.model.mapMenu.draw(self.screen)
            
        if self.model.subScreen == 2:
            self.model.speciesDialog.draw(self.screen)
        
        
        if tickClock:
            pygame.display.flip()