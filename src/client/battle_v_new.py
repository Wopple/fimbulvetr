import os
import sys
import pygame

from common.constants import *
from client.constants import *

from common import mvc

from client import drawable
from client import scenery
from client import energybar
from client.countdown_d import CountdownDrawable
from client.fx_d import FXDrawable
from client.textrect import render_textrect

class View(mvc.View):
    
    def __init__(self, stateQueue, state):
        super(View, self).__init__()
        self.stateQueue = stateQueue
        self.scene = scenery.Scenery(state.terrainLeft, state.terrainRight)

        self.superVeil = pygame.Surface(SCREEN_SIZE)
        self.superVeil.fill(BLACK)
        self.superVeil.set_alpha(100)
        self.cameraPlayer = 0

        self.createEndingText()

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
            FXDrawable(f).draw(self.screen, self.model.rect.topleft)

        for b in self.model.bars:
            b.draw(self.screen)
        self.drawInterfaceExtras()
        
        for i in range(2):
            self.screen.blit(self.model.damageTag, self.model.damageTagRects[i].topleft)
            self.screen.blit(self.model.getDamagePercentText(i), self.model.damagePercentRects[i].topleft)
        
        self.scene.drawForeground(self.screen, self.model.rect.topleft)

        CountdownDrawable(self.model.countdown).draw(self.screen)
        self.drawEndingText()

        if tickClock:
            pygame.display.flip()

    def createEndingText(self):
        tempText = ["is defeated", "is victorious", "retreats"]
        self.endingText = []
        for i in range(2):
            sublist = []
            p = self.model.players[i]
            for j in range(3):
                t = p.name + " " + tempText[j]
                image = render_textrect(t, COUNTDOWN_FONT,
                                        self.model.countdown.rect,
                                        COUNTDOWN_COLOR, ALMOST_BLACK,
                                        1, True)
                sublist.append(image)
            self.endingText.append(sublist)

        sublist = []
        t = "FINISH!"
        image = render_textrect(t, COUNTDOWN_FONT, self.model.countdown.rect,
                                COUNTDOWN_COLOR, ALMOST_BLACK, 1, True)
        sublist.append(image)
        self.endingText.append(sublist)

    def drawEndingText(self):
        endingVal = self.model.endingVal

        if endingVal == 0:
            self.screen.blit(self.endingText[2][0],
                             self.model.countdown.rect.topleft)
        elif endingVal == 3:
            self.screen.blit(self.endingText[0][self.model.returnCode[0]+1],
                             self.model.countdown.rect.topleft)
            self.screen.blit(self.endingText[1][self.model.returnCode[1]+1],
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
            self.youIconRect.centerx = int(p.preciseLoc[0])
            self.youIconRect.bottom = int(p.preciseLoc[1] - p.youIconHeight)
            
            self.screen.blit(self.youIconImage, add_points(self.youIconRect.topleft, offset))
            
    
    def drawToBack(self, p):
        return p.currMove.drawToBack or (self.otherPersonDoingSuperFlash(p))
    
    def otherPersonDoingSuperFlash(self, thisP):
       for p in self.model.players:
           if p == thisP:
               continue
           if p.currMove.isSuperFlash:
               return True

    def setCameraPlayer(self, c):
        if (c >= 0) and (c <= 1):
            self.cameraPlayer = c
        self.createBars()
        
        self.youIconImage = INTERFACE_GRAPHICS[18]
        colorSwap(self.youIconImage, (215, 215, 215, 255), TOKEN_BORDER_HIGHLIGHTED[self.cameraPlayer], 200)
        self.youIconRect = Rect((0, 0), self.youIconImage.get_size())

    def createBars(self):
        self.bars = []
        p = self.players[self.cameraPlayer]
        q = self.players[self.reverse01(self.cameraPlayer)]
        
        x = BATTLE_PORTRAIT_SIZE[0] + HEALTH_BAR_OFFSET[0] + BATTLE_PORTRAIT_OFFSET[0]
        y = HEALTH_BAR_OFFSET[1]

        self.bars.append(energybar.EnergyBar(p.hp,
                                             Rect((x, y), HEALTH_BAR_SIZE),
                                             HEALTH_BAR_BORDERS,
                                             HEALTH_BAR_COLORS,
                                             HEALTH_BAR_PULSE,
                                             p.name)
            )

        x = SCREEN_SIZE[0] - HEALTH_BAR_OFFSET[0] - HEALTH_BAR_SIZE[0] - BATTLE_PORTRAIT_SIZE[0] - BATTLE_PORTRAIT_OFFSET[0]
        y = HEALTH_BAR_OFFSET[1]

        self.bars.append(energybar.EnergyBar(q.hp,
                                             Rect((x, y), HEALTH_BAR_SIZE),
                                             HEALTH_BAR_BORDERS,
                                             HEALTH_BAR_COLORS,
                                             HEALTH_BAR_PULSE,
                                             q.name, None, 2, False)
            )

        x = (SCREEN_SIZE[0] / 2) - (RETREAT_BAR_SIZE[0] / 2)
        y = HEALTH_BAR_OFFSET[1]

        self.retreatBar = energybar.EnergyBar(self.retreatProhibitTime,
                                             Rect((x, y), RETREAT_BAR_SIZE),
                                             RETREAT_BAR_BORDERS,
                                             RETREAT_BAR_COLORS,
                                             5, "Battle", None, 1)
        self.bars.append(self.retreatBar)
        

        x = BATTLE_PORTRAIT_SIZE[0] + HEALTH_BAR_OFFSET[0] + BATTLE_PORTRAIT_OFFSET[0]
        y = HEALTH_BAR_OFFSET[1] + HEALTH_BAR_SIZE[1] + SPECIAL_BAR_OFFSET
        if isinstance(p, hare.Hare):
            self.bars.append(energybar.EnergyBar(p.hareEnergy,
                                                 Rect((x, y), SPECIAL_BAR_SIZE),
                                                 SPECIAL_BAR_BORDERS,
                                                 SPECIAL_BAR_COLORS,
                                                 SPECIAL_BAR_PULSE,
                                                 HARE_ENERGY_NAME,
                                                 HARE_ENERGY_USAGE)
                             )

        if isinstance(p, cat.Cat):
            self.catBar = energybar.EnergyBar(p.catEnergy,
                                                 Rect((x, y), SPECIAL_BAR_SIZE),
                                                 SPECIAL_BAR_BORDERS,
                                                 SPECIAL_BAR_COLORS,
                                                 SPECIAL_BAR_PULSE,
                                                 CAT_ENERGY_NAME,
                                                 CAT_ENERGY_MAX+1)
            self.bars.append(self.catBar)





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
