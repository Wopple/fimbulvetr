import pygame

from common.constants import *
from client.constants import *

from common.util.rect import Rect

from client.drawable import ItemDrawable

IMAGE = 0
OFFSET = 1

class BattleCharDrawable(ItemDrawable):
    def __init__(self, item):
        super(BattleCharDrawable, self).__init__(item)
#        temp = pygame.Surface((50, 80))
#        temp.fill((2, 2, 2))
#        self.setImage(temp, (40, 25))

    def draw(self, screen, camera):
        frame = self.item.getCurrentFrame()
        images = IMAGES_MAP[self.item.type][frame.frameKey]
        self.setImage(images[IMAGE], images[OFFSET])
        screen.blit(self.image, adjustToCamera(self.rect.topleft, camera))

        if SHOW_HURTBOXES:
            self.drawBoxes(frame.hurtboxes, screen, camera)
        if SHOW_HITBOXES:
            self.drawBoxes(frame.hitboxes, screen, camera)
        if SHOW_BLOCKBOXES:
            self.drawBoxes(frame.blockboxes, screen, camera)

        if SHOW_RED_DOT:
            screen.blit(RED_DOT, adjustToCamera(self.item.preciseLoc, camera))

    def setImage(self, inImage, o):
        size = inImage.get_size()
        
        if self.item.facingRight:
            offset = o
            self.image = inImage
        else:
            offset = (-o[0] + size[0], o[1])
            self.image = pygame.transform.flip(inImage, True, False)
        
        self.offset = offset
        self.rect = Rect(self.getRectPos(), size)

    def getRectPos(self):
        return (int(self.item.preciseLoc[0]) - self.offset[0],
                int(self.item.preciseLoc[1]) - self.offset[1])

    def drawBoxes(self, boxes, screen, camera):
        for b in boxes:
            boxLoc = self.item.getBoxLocation(b)
            screen.blit(b.image, adjustToCamera(boxLoc, camera))

    def getSuperIcon(self):
        icons = SUPER_ICONS_MAP[self.item.type]

        if self.item.currSuperMove >= len(icons):
            icon = pygame.Surface(BATTLE_SUPER_ICON_SIZE)
            icon.fill(BLACK)
        else:
            icon = icons[self.item.currSuperMove]

        return icon
