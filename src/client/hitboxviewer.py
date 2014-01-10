import sys
import pygame

import textrect
from pygame.locals import *

from common.constants import *
from client.constants import *

from common import boundint
from common.util import framerate
from common.util.rect import Rect

def setImage():
    global currImage
    global imageLoc
    global zoom
    preImage = images[imageInc.value][0]
    preSize = preImage.get_size()
    currImage = pygame.transform.scale(preImage, (preSize[0] * zoom, preSize[1] * zoom))

    preOffset = images[imageInc.value][1]
    offset = (preOffset[0] * zoom, preOffset[1] * zoom)
    imageLoc = (  (anchorPoint[0] - offset[0]),
                  (anchorPoint[1] - offset[1])  )

def leftClick(newLoc):
    global clickLoc
    global boxList
    
    if clickLoc == [-1, -1]:
        clickLoc = [newLoc[0], newLoc[1]]
    else:
        x1 = getZoomNum(clickLoc[0])
        x2 = getZoomNum(newLoc[0])
        y1 = getZoomNum(clickLoc[1])
        y2 = getZoomNum(newLoc[1])

        if (x1 < x2):
            left = x1
            right = x2
        elif (x1 > x2):
            left = x2
            right = x1
        else:
            return

        if (y1 < y2):
            top = y1
            bottom = y2
        elif (y1 > y2):
            top = y2
            bottom = y1
        else:
            return

        width = right - left
        height = bottom - top
        newSurface = pygame.Surface((width, height))
        newSurface.fill((255, 242, 5))
        newSurface.set_alpha(50)
        
        boxList.append( [newSurface, Rect((left, top), (width, height))] )
        
        clickLoc = [-1, -1]

def rightClick():
    global boxList

    if len(boxList) > 0:
        boxList.pop()

def getZoomPos(inPos):
    global zoom
    return ( getZoomNum(inPos[0]), getZoomNum(inPos[1]) )

def getZoomNum(inNum):
    global zoom
    return (inNum - (inNum % zoom))

def getAnchorZoomPos():
    global zoom
    global anchorPoint
    return getZoomPos(anchorPoint)

def posRelatedToAnchor(pos):
    anchorZoom = getAnchorZoomPos()
    return ( int((pos[0] - anchorZoom[0]) / 4),
             int((pos[1] - anchorZoom[1]) / 4)  )

def printText(screen, mousePos):
    pos = getZoomPos(mousePos)
    pixelPos = posRelatedToAnchor(pos)
    text = textrect.render_textrect(str(pixelPos), FONTS[0],
                                    Rect((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])),
                                    (250, 250, 250), (5, 5, 5), 0, True)
    screen.blit(text, (mousePos[0] + 15, mousePos[1] - 10))

def printList(screen):
    global boxList

    for i, b in enumerate(boxList):
        pos = (0, i * 15)
        line = (str(posRelatedToAnchor(b[1].topleft)) +
                " - " + str(posRelatedToAnchor(b[1].bottomright)) )
        text = textrect.render_textrect(line, FONTS[0],
                                    Rect((0, 0), (SCREEN_SIZE[0], SCREEN_SIZE[1])),
                                    (250, 250, 250), (5, 5, 5), 0, True)
        screen.blit(text, pos)

def printListToOutput():
    global boxList

    f = open('scrap/easy.txt', 'w')
    for i, b in enumerate(boxList):
        tl = posRelatedToAnchor(b[1].topleft)
        br = posRelatedToAnchor(b[1].bottomright)
        f.write ("(" + str(tl[0]) + ", " +
               str(tl[1]) + ", " +
               str(br[0]) + ", " +
               str(br[1]) + ")" )
        if i < len(boxList) - 1:
            f.write(",")
        f.write("\n")
    

if len(sys.argv) != 4:
    print "Usage: hitboxviewer.py imageGroup imageNum showBoxes"
    exit()

try:
    imageGroup = int(sys.argv[1])
    imageNum = int(sys.argv[2])
    showBoxes = int(sys.argv[3])
except:
    print "Arguments must be integers"
    exit()

if imageGroup == 0:
    images = HARE_IMAGES
elif imageGroup == 1:
    images = FOX_IMAGES
elif imageGroup == 2:
    images = CAT_IMAGES
else:
    print "Invalid image group"
    exit()

if (imageNum >= len(images)) or (imageNum < 0):
    print "Image number out of range"
    exit()

if showBoxes == 0:
    showBoxes = False
elif showBoxes == 1:
    showBoxes = True
else:
    print "showBoxes argument must be 0 or 1"
    exit()

zoom = 4
imageInc = boundint.BoundInt(0, len(images) - 1, imageNum)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.init()
pygame.display.set_caption("Hitbox Viewer")
clock = framerate.FrameRate(FRAME_RATE)
bg = pygame.Surface(SCREEN_SIZE)
bg.fill(BLACK)
cursor = pygame.Surface((zoom, zoom))
cursor.fill((10, 50, 200))
clickLoc = [-1, -1]
boxList = []
anchorPoint = (400, 500)
mousePos = (0, 0)
setImage()

while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_LEFT:
                imageInc.dec()
                setImage()
            elif event.key == K_RIGHT:
                imageInc.inc()
                setImage()
            elif event.key == K_SPACE:
                printListToOutput()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                leftClick(pygame.mouse.get_pos())
            elif event.button == 3:
                rightClick()
        elif event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()

    screen.blit(bg, (0, 0))
    screen.blit(currImage, imageLoc)
    for b in boxList:
        screen.blit(b[0], b[1].topleft)
    screen.blit(cursor, getZoomPos(mousePos))
    printText(screen, mousePos)
    printList(screen)
    clock.next()
    pygame.display.flip()
