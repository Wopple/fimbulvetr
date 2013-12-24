import os
import sys
import pygame

from common.constants import *
from client.constants import *

from client import mvc

from client import drawable
from client import scenery

class View(mvc.View):
    
    def __init__(self, terrainLeft, terrainRight):
        super(View, self).__init__()
        self.scene = scenery.Scenery(terrainLeft, terrainRight)

        self.superVeil = pygame.Surface(SCREEN_SIZE)
        self.superVeil.fill(BLACK)
        self.superVeil.set_alpha(100)

    def update(self, tickClock=True):
        self.screen.blit(BLACK_SCREEN, (0, 0))
        
        self.scene.drawBackground(self.screen, self.model.rect.topleft)

        for p in self.model.platforms:
            p.draw(self.screen, self.model.rect.topleft)

        for i, p in enumerate(self.model.players):
            if self.model.returnCode[i] != 1 and self.drawToBack(p):
                p.draw(self.screen, self.model.rect.topleft)
                self.drawYouIcon(i, p, self.model.rect.topleft)
                
        if self.model.superDarken():
            self.screen.blit(self.superVeil, (0, 0))
            
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
        
        self.scene.drawForeground(self.screen, self.model.rect.topleft)

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
        self.createInterfaceExtras()

        for p in self.portraits:
            p.draw(screen)
            
        self.superIcon.draw(screen)

    def createInterfaceExtras(self):
        self.portraits = []

        for i in range(2):
            s = pygame.Surface(BATTLE_PORTRAIT_SIZE)
            s.fill(BLACK)
            if (i == 0):
                x = BATTLE_PORTRAIT_OFFSET[0]
            else:
                x = SCREEN_SIZE[0] - BATTLE_PORTRAIT_OFFSET[0] - BATTLE_PORTRAIT_SIZE[0]
            y = BATTLE_PORTRAIT_OFFSET[1]
            p = drawable.Drawable(Rect((x, y), BATTLE_PORTRAIT_SIZE), s)
            self.portraits.append(p)
            
        
        x = self.portraits[0].rect.left
        y = self.portraits[0].rect.bottom + BATTLE_PORTRAIT_OFFSET[1]
        
        c = self.model.players[self.model.cameraPlayer]
        
        self.superIcon = SuperIcon(Rect((x, y), BATTLE_SUPER_ICON_SIZE), c.getSuperIcon(), c.superEnergy)
        
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
        
class SuperIcon(drawable.Drawable):
    def __init__(self, inRect, inImage, energy):
        self.imageBase = inImage
        self.energy = energy
        self.oldValue = self.energy.value
        
        super(SuperIcon, self).__init__(inRect, None)
        
        self.updateImage()
        
    def draw(self, screen):
        
        if self.oldValue != self.energy.value:
            self.oldValue = self.energy.value
            self.updateImage()
            
        super(SuperIcon, self).draw(screen)
        
    def updateImage(self):
        
        temp = pygame.Surface(BATTLE_SUPER_ICON_SIZE)
        temp.fill(BLACK)
        
        if self.energy.isMax():
            temp.blit(self.imageBase, (0,0))
        else:
            percent = float(self.energy.value) / float(self.energy.maximum)
            leftSideWidth = int(BATTLE_SUPER_ICON_SIZE[0] * percent)
            rightSideWidth = int(BATTLE_SUPER_ICON_SIZE[0] * (1 - percent))
            
            leftSide = pygame.Surface((leftSideWidth, BATTLE_SUPER_ICON_SIZE[1]))
            leftSide.blit(self.imageBase, (0, 0))
            leftSide.set_alpha(BATTLE_SUPER_ICON_ALPHA_FILL)
            temp.blit(leftSide, (0, 0))
            
            rightSide = pygame.Surface((rightSideWidth, BATTLE_SUPER_ICON_SIZE[1]))
            rightSide.blit(self.imageBase, (-leftSideWidth, 0))
            rightSide.set_alpha(BATTLE_SUPER_ICON_ALPHA_EMPTY)
            temp.blit(rightSide, (leftSideWidth, 0))
            
        self.image = temp
