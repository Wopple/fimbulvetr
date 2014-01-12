import pygame

from client.constants import *

from client.drawable import ItemDrawable

class BlockboxDrawable(ItemDrawable):
    def __init__(self, item):
        super(BlockboxDrawable, self).__init__(item, rect=item.rect)

    def draw(self, screen, camera=None):
        frame = self.item.getCurrentFrame()
        images = IMAGES_MAP[self.item.type][frame.frameKey]
        self.setImage(images[IMAGE], images[OFFSET])

        frame = self.item.currMove.frames[self.item.currFrame]
        image = frame.image
        offset = frame.offset

        screen.blit(self.image, adjustToCamera(self.rect.topleft, camera))

        if SHOW_HITBOXES:
            self.drawBoxes(frame.hitboxes, screen, camera)
        if SHOW_RED_DOT:
            screen.blit(RED_DOT, adjustToCamera(self.preciseLoc, camera))

    def setImage(self, inImage, o):
        size = inImage.get_size()

        if self.item.facingRight:
            offset = o
            self.image = inImage
        else:
            offset = (-o[0] + size[0], o[1])
            self.image = pygame.transform.flip(inImage, True, False)

        self.rect = Rect(self.getRectPos(offset), size)

    def getRectPos(self, offset):
        return (int(self.item.preciseLoc[0]) - offset[0],
                int(self.item.preciseLoc[1]) - offset[1])

    def drawBoxes(self, boxes, screen, camera):
        for b in boxes:
            boxpos = self.getBoxAbsRect(b, camera).topleft
            screen.blit(b.image, boxpos)

    def getBoxAbsRect(self, box, camera):
        if self.item.facingRight:
            boxPos = box.rect.topleft
        else:
            boxPos = flipRect(box.rect)

        topleft = add_points(adjustToCamera(self.preciseLoc, boxPos), camera)

        return Rect(topleft, box.rect.size)
