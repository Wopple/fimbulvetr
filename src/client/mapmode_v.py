import os
import sys
import pygame

import mvc

import mapchar

from constants import *

class View(mvc.View):
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.screen.blit(self.model.mapImage, self.model.mapRect.topleft)

        for i in self.model.structures:
            i.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        for c in self.model.characters:
            if ((not c is self.model.currHighlighted) and
                (not c is self.model.currSelected)):
                c.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        if ( (isinstance(self.model.currHighlighted, mapchar.MapChar)) and
             (not self.model.currHighlighted is self.model.currSelected) ):
            self.model.currHighlighted.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        if isinstance(self.model.currSelected, mapchar.MapChar):
            self.model.currSelected.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)

        for s in self.model.rezSparks:
            s.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)
            
        for s in self.model.lockCircles:
            s.draw(self.screen, self.model.zoomVal, self.model.mapRect.topleft)
            
        c = self.model.currSelected
        if not c is None:
            if not c.target is None:
                points = [c.target]
                points += c.targetBuffer
                for i in range(len(points)-1):
                    self.model.waypointMarkers[i].draw(self.screen, points[i],
                                             self.model.zoomVal, self.model.mapRect.topleft)
                    
                self.model.targetMarker.draw(self.screen, points[-1],
                                             self.model.zoomVal, self.model.mapRect.topleft)

        for i in self.model.structures:
            i.drawBar(self.screen)

        self.model.bigPausePlayIcon.draw(self.screen)
        for i in self.model.littlePausePlayIcons:
            i.draw(self.screen)

        #for i in self.model.charBars:
        #    i.draw(self.screen)
        
        self.model.unitHUD.draw(screen)

        self.model.countdown.draw(self.screen)


        if tickClock:
            pygame.display.flip()
