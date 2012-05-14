import os
import sys
import pygame

import mvc

from constants import *

class View(mvc.View):
    
    def __init__(self, model=None, screen=None):
        super(View, self).__init__()

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.screen.blit(self.model.background, self.model.rect)

        for p in self.model.platforms:
            p.draw(self.screen, self.model.rect.topleft)

        for i, p in enumerate(self.model.players):
            if self.model.returnCode[i] != 1 and self.drawToBack(p):
                p.draw(self.screen, self.model.rect.topleft)
                self.drawYouIcon(i, p, self.model.rect.topleft)
                
        if self.model.superDarken():
            self.screen.blit(self.model.superVeil, (0, 0))
            
        for i, p in enumerate(self.model.players):
            if self.model.returnCode[i] != 1 and not self.drawToBack(p):
                p.draw(self.screen, self.model.rect.topleft)
                self.drawYouIcon(i, p, self.model.rect.topleft)

        for p in self.model.projectiles:
            p.draw(self.screen, self.model.rect.topleft)

        for f in self.model.fx:
            f.draw(self.screen, self.model.rect.topleft)

        for b in self.model.bars:
            b.draw(self.screen)
        self.drawInterfaceExtras()
        
        for i in range(2):
            self.screen.blit(self.model.damageTag, self.model.damageTagRects[i].topleft)
            self.screen.blit(self.model.getDamagePercentText(i), self.model.damagePercentRects[i].topleft)
        

        self.model.countdown.draw(self.screen)
        self.drawEndingText()

        if tickClock:
            pygame.display.flip()

    def drawEndingText(self):
        if self.model.endingVal == 0:
            self.screen.blit(self.model.endingText[2][0],
                             self.model.countdown.rect.topleft)
        elif self.model.endingVal == 3:
            self.screen.blit(self.model.endingText[0][self.model.returnCode[0]+1],
                             self.model.countdown.rect.topleft)
            self.screen.blit(self.model.endingText[1][self.model.returnCode[1]+1],
                             self.model.countdown.rect.bottomleft)


    def drawInterfaceExtras(self):
        for p in self.model.portraits:
            p.draw(screen)
            
        self.model.superIcon.draw(screen)
        
    def drawYouIcon(self, i, p, offset):
        if i == self.model.cameraPlayer:
            self.model.youIconRect.centerx = int(p.preciseLoc[0])
            self.model.youIconRect.bottom = int(p.preciseLoc[1] - p.youIconHeight)
            
            self.screen.blit(self.model.youIconImage, add_points(self.model.youIconRect.topleft, offset))
            
    
    def drawToBack(self, p):
        return p.currMove.drawToBack or (self.otherPersonDoingSuperFlash(p))
    
    def otherPersonDoingSuperFlash(self, thisP):
       for p in self.model.players:
           if p == thisP:
               continue
           if p.currMove.isSuperFlash:
               return True
        