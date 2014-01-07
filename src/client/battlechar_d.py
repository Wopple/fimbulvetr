import pygame

from common.constants import *
from client.constants import *

from common.util.rect import Rect

from client.drawable import ItemDrawable

class BattleCharDrawable(ItemDrawable):
    def __init__(self, item):
        super(BattleCharDrawable, self).__init__(item)
#        temp = pygame.Surface((50, 80))
#        temp.fill((2, 2, 2))
#        self.setImage(temp, (40, 25))

    def draw(self, screen, inOffset=(0, 0)):
        frame = self.item.getCurrentFrame()
        self.setImage(frame.image, frame.offset)
        screen.blit(self.image, add_points(self.rect.topleft, inOffset))

        if SHOW_HURTBOXES:
            self.drawBoxes(frame.hurtboxes, screen, inOffset)
        if SHOW_HITBOXES:
            self.drawBoxes(frame.hitboxes, screen, inOffset)
        if SHOW_BLOCKBOXES:
            self.drawBoxes(frame.blockboxes, screen, inOffset)

        if SHOW_RED_DOT:
            screen.blit(RED_DOT, add_points(self.item.preciseLoc, inOffset))

    def setImage(self, inImage, o):
        size = inImage.get_size()
        
        if self.item.facingRight:
            offset = o
            self.image = inImage
        else:
            offset = (-o[0] + size[0], o[1])
            self.image = pygame.transform.flip(inImage, True, False)
        
        self.offset = offset
        self.rect = Rect(self.item.getRectPos(), size)

    def drawBoxes(self, boxes, screen, inOffset):
        for b in boxes:
            boxpos = self.item.getBoxAbsRect(b, inOffset).topleft
            screen.blit(b.image, boxpos)

    def getSuperIcon(self):
        icons = SUPER_ICONS_MAP[type(self.item)]

        if self.item.currSuperMove >= len(icons):
            icon = pygame.Surface(BATTLE_SUPER_ICON_SIZE)
            icon.fill(BLACK)
        else:
            icon = icons[self.item.currSuperMove]

        return icon
