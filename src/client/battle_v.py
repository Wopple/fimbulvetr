import pygame

from common.constants import *
from client.constants import *

from common import mvc
from common import hare, cat, fox
from common.util import process
from common.util.rect import Rect

from client import drawable
from client import scenery
from client import energybar
from client.battlechar_d import BattleCharDrawable
from client.countdown_d import CountdownDrawable
from client.fx_d import FXDrawable
from client.platform_d import PlatformDrawable
from client.textrect import render_textrect

class View(mvc.View):
    def __init__(self, stateQueue, state):
        super(View, self).__init__()
        self.stateQueue = stateQueue
        self.state = state
        self.camera = Rect((0, 0), SCREEN_SIZE)
        self.scene = scenery.Scenery(state.terrainLeft, state.terrainRight)

        self.superVeil = pygame.Surface(SCREEN_SIZE)
        self.superVeil.fill(BLACK)
        self.superVeil.set_alpha(100)
        self.cameraPlayer = 0

        self.createEndingText()
        
        self.damageTagRects = []
        self.damagePercentRects = []

        for i in range(2):
            rect = Rect((0, 0), (80, 100))
            if (i == 0):
                rect.left = 0
            else:
                rect.right = SCREEN_SIZE[0]
            rect.top = SCREEN_SIZE[1] - 55
            self.damageTagRects.append(rect)
            
            rect2 = Rect((0, 0), (80, 100))
            if (i == 0):
                rect2.left = 0
            else:
                rect2.right = SCREEN_SIZE[0]
            rect2.top = rect.top + 18
            self.damagePercentRects.append(rect2)

        self.createBars()
        self.youIconImage = INTERFACE_GRAPHICS[18]
        self.youIconRect = Rect((0, 0), self.youIconImage.get_size())

    def update(self, tickClock=True):
        lastState = process.getLast(self.stateQueue)

        if lastState is not None:
            self.state = lastState

        self.screen.blit(BLACK_SCREEN, (0, 0))
        self.scene.drawBackground(self.screen, self.camera)
        isFlash = self.state.isFlash()

        if not isFlash:
            self.centerCamera(self.state.players[self.cameraPlayer])
            self.updateRetreat()

        if self.state.retreatPhase == 1 and self.state.endingVal == -1 and not isFlash:
            if self.state.retreatProhibitTime.value == 0:
                self.retreatBar.createText("Retreat", 1)
                self.retreatBar.value.maximum = RETREAT_HOLD_TOTAL
                self.retreatBar.threshold = self.retreatBar.value.maximum + 1

        for p in self.state.platforms:
            PlatformDrawable(p).draw(self.screen, self.camera)

        for i, p in enumerate(self.state.players):
            if self.state.returnCode[i] != 1 and self.drawToBack(p):
                BattleCharDrawable(p).draw(self.screen, self.camera)
                self.drawYouIcon(i, p, self.camera)
                
        if self.state.superDarken():
            self.screen.blit(self.superVeil, (0, 0))
            
        for i, p in enumerate(self.state.players):
            if self.state.returnCode[i] != 1 and not self.drawToBack(p):
                BattleCharDrawable(p).draw(self.screen, self.camera)
                self.drawYouIcon(i, p, self.camera)

        for p in self.state.projectiles:
            p.draw(self.screen, self.camera)

        for f in self.state.fx:
            FXDrawable(f).draw(self.screen, self.camera)

        # All this bar stuff is very hard coded, this needs abstraction and mappings

        for i, p in enumerate(self.state.players):
            self.hpBars[i].value = p.hp

        p = self.state.players[0]

        if isinstance(p, hare.Hare):
            self.energyBar.value = p.hareEnergy
        elif isinstance(p, cat.Cat):
            self.energyBar.value = p.catEnergy

        if self.catBar is not None:
            self.updateCatBarColors()

        for b in self.hpBars:
            b.update()
            b.draw(self.screen)

        for b in (self.retreatBar, self.energyBar):
            if b is not None:
                b.update()
                b.draw(self.screen)

        self.drawInterfaceExtras()

        damageTag = render_textrect("Strength",
                                    STRUCTURE_COUNT_FONT,
                                    self.damageTagRects[0],
                                    ALMOST_BLACK, BLACK, 1, True)

        for i in range(2):
            self.screen.blit(damageTag, self.damageTagRects[i].topleft)
            self.screen.blit(self.getDamagePercentText(i),
                             self.damagePercentRects[i].topleft)

        self.scene.drawForeground(self.screen, self.camera)

        CountdownDrawable(self.state.countdown).draw(self.screen)
        self.drawEndingText()

        if tickClock:
            pygame.display.flip()

    def updateRetreat(self):
        if self.retreatBar is not None:
            highest = self.state.getHighestRetreat()
            self.retreatBar.changeColor(RETREAT_TEAM_COLORS[highest])
            self.retreatBar.value = self.state.players[highest].retreat

    def centerCamera(self, target):
        self.camera.centerx = int(target.preciseLoc[0])
        self.camera.centery = int(target.preciseLoc[1])

        if self.camera.left < 0:
            self.camera.left = 0
        elif self.camera.right > BATTLE_ARENA_SIZE[0]:
            self.camera.right = BATTLE_ARENA_SIZE[0]

        if self.camera.top < 0:
            self.camera.top = 0
        elif self.camera.bottom > BATTLE_ARENA_SIZE[1]:
            self.camera.bottom = BATTLE_ARENA_SIZE[1]

    def getDamagePercentText(self, i):
        if self.cameraPlayer == 1:
            if i == 0:
                i = 1
            else:
                i = 0

        c = self.state.players[i]
        return render_textrect(c.getDamagePercentText(),
                               DAMAGE_PERCENT_FONT,
                               self.damagePercentRects[i],
                               ALMOST_BLACK, BLACK, 1, True)

    def createEndingText(self):
        tempText = ["is defeated", "is victorious", "retreats"]
        self.endingText = []
        for i in range(2):
            sublist = []
            p = self.state.players[i]
            for j in range(3):
                t = p.name + " " + tempText[j]
                image = render_textrect(t, COUNTDOWN_FONT,
                                        self.state.countdown.rect,
                                        COUNTDOWN_COLOR, ALMOST_BLACK,
                                        1, True)
                sublist.append(image)
            self.endingText.append(sublist)

        sublist = []
        t = "FINISH!"
        image = render_textrect(t, COUNTDOWN_FONT, self.state.countdown.rect,
                                COUNTDOWN_COLOR, ALMOST_BLACK, 1, True)
        sublist.append(image)
        self.endingText.append(sublist)

    def drawEndingText(self):
        endingVal = self.state.endingVal

        if endingVal == 0:
            self.screen.blit(self.endingText[2][0],
                             self.state.countdown.rect.topleft)
        elif endingVal == 3:
            self.screen.blit(self.endingText[0][self.state.returnCode[0]+1],
                             self.state.countdown.rect.topleft)
            self.screen.blit(self.endingText[1][self.state.returnCode[1]+1],
                             self.state.countdown.rect.bottomleft)


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

        c = self.state.players[self.cameraPlayer]

        self.superIcon = SuperIcon(Rect((x, y), BATTLE_SUPER_ICON_SIZE), BattleCharDrawable(c).getSuperIcon(), c.superEnergy)

    def drawYouIcon(self, i, p, camera):
        if i == self.cameraPlayer:
            self.youIconRect.centerx = int(p.preciseLoc[0])
            self.youIconRect.bottom = int(p.preciseLoc[1] - p.youIconHeight)
            self.screen.blit(self.youIconImage, adjustToCamera(self.youIconRect.topleft, camera))

    def drawToBack(self, p):
        return p.currMove.drawToBack or (self.otherPersonDoingSuperFlash(p))
    
    def otherPersonDoingSuperFlash(self, thisP):
       for p in self.state.players:
           if p == thisP:
               continue
           if p.currMove.isSuperFlash:
               return True

    def createBars(self):
        self.hpBars = []
        self.retreatBar = None
        self.catBar = None
        self.energyBar = None

        p = self.state.players[self.cameraPlayer]
        q = self.state.players[(self.cameraPlayer + 1) % 2]

        x = BATTLE_PORTRAIT_SIZE[0] + HEALTH_BAR_OFFSET[0] + BATTLE_PORTRAIT_OFFSET[0]
        y = HEALTH_BAR_OFFSET[1]

        self.hpBars.append(energybar.EnergyBar(p.hp,
                                               Rect((x, y), HEALTH_BAR_SIZE),
                                               HEALTH_BAR_BORDERS,
                                               HEALTH_BAR_COLORS,
                                               HEALTH_BAR_PULSE,
                                               p.name)
            )

        x = SCREEN_SIZE[0] - HEALTH_BAR_OFFSET[0] - HEALTH_BAR_SIZE[0] - BATTLE_PORTRAIT_SIZE[0] - BATTLE_PORTRAIT_OFFSET[0]
        y = HEALTH_BAR_OFFSET[1]

        self.hpBars.append(energybar.EnergyBar(q.hp,
                                             Rect((x, y), HEALTH_BAR_SIZE),
                                             HEALTH_BAR_BORDERS,
                                             HEALTH_BAR_COLORS,
                                             HEALTH_BAR_PULSE,
                                             q.name, None, 2, False)
            )

        x = (SCREEN_SIZE[0] / 2) - (RETREAT_BAR_SIZE[0] / 2)
        y = HEALTH_BAR_OFFSET[1]

        self.retreatBar = energybar.EnergyBar(self.state.retreatProhibitTime,
                                             Rect((x, y), RETREAT_BAR_SIZE),
                                             RETREAT_BAR_BORDERS,
                                             RETREAT_BAR_COLORS,
                                             5, "Battle", None, 1)

        x = BATTLE_PORTRAIT_SIZE[0] + HEALTH_BAR_OFFSET[0] + BATTLE_PORTRAIT_OFFSET[0]
        y = HEALTH_BAR_OFFSET[1] + HEALTH_BAR_SIZE[1] + SPECIAL_BAR_OFFSET

        if isinstance(p, hare.Hare):
            self.energyBar = energybar.EnergyBar(p.hareEnergy,
                                                 Rect((x, y), SPECIAL_BAR_SIZE),
                                                 SPECIAL_BAR_BORDERS,
                                                 SPECIAL_BAR_COLORS,
                                                 SPECIAL_BAR_PULSE,
                                                 HARE_ENERGY_NAME,
                                                 HARE_ENERGY_USAGE)

        if isinstance(p, cat.Cat):
            self.catBar = energybar.EnergyBar(p.catEnergy,
                                                 Rect((x, y), SPECIAL_BAR_SIZE),
                                                 SPECIAL_BAR_BORDERS,
                                                 SPECIAL_BAR_COLORS,
                                                 SPECIAL_BAR_PULSE,
                                                 CAT_ENERGY_NAME,
                                                 CAT_ENERGY_MAX+1)
            self.energyBar = self.catBar

    def updateCatBarColors(self):
        x = len(CAT_ENERGY_SECTIONS)
        for i in range(x):
            if self.catBar.value.value <= CAT_ENERGY_SECTIONS[i]:
                if self.catBar.fillColor is not CAT_ENERGY_BAR_COLORS[i]:
                    self.catBar.changeColor(CAT_ENERGY_BAR_COLORS[i])
                return
        self.catBar.changeColor(CAT_ENERGY_BAR_COLORS[x])

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
