import os
import sys
import pygame

import mvc
import gamemap
import util
import incint

from constants import *

class Model(mvc.Model):
    def __init__(self, inMap):
        super(Model, self).__init__()
        self.map = inMap
        self.zoomVal = 1.0
        self.mapRect = None
        self.keys = [False, False, False, False]
        self.mousePos = pygame.mouse.get_pos()
        self.drawOrigMap()

        while (self.zoomVal > ZOOM_MIN) and (not self.canSeeEntireMap()):
            self.scrollOut()

    def canSeeEntireMap(self):
        return ((self.mapRect.width < SCREEN_SIZE[0]) and
                (self.mapRect.height < SCREEN_SIZE[1]))

    def drawOrigMap(self):
        self.mapOrigImage = gamemap.drawMap(self.map)
        self.drawZoomMap()

    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        self.checkScrolling()

    def zoom(self):
        self.drawZoomMap()
        self.adjustMap()

    def drawZoomMap(self):
        newSize = (int(self.map.mapSize[0] * self.zoomVal),
                       int(self.map.mapSize[1] * self.zoomVal))
        
        if not self.mapRect is None:
            diff = ((self.mapRect.width - newSize[0]),
                    (self.mapRect.height - newSize[1]))
            newPos = ((self.mapRect.left + (diff[0] / 2)),
                      (self.mapRect.top + (diff[1] / 2)))
            self.mapRect = pygame.Rect(newPos, newSize)
        else:
            self.mapRect = pygame.Rect((0, 0), newSize)
        self.mapImage = pygame.transform.scale(self.mapOrigImage, newSize)

    def scrollIn(self):
        self.zoomVal /= ZOOM_CLICK
        if self.zoomVal > ZOOM_MAX:
            self.zoomVal = ZOOM_MAX
        self.zoom()

    def scrollOut(self):
        self.zoomVal *= ZOOM_CLICK
        if self.zoomVal < ZOOM_MIN:
            self.zoomVal = ZOOM_MIN
        self.zoom()

    def checkScrolling(self):
        axis = [0, 0]

        for i in range(2):
            if self.mousePos[i] < SCROLL_AREA_WIDTH:
                axis[i] = -1
            if self.mousePos[i] > SCREEN_SIZE[i] - SCROLL_AREA_WIDTH:
                axis[i] = 1

        if self.keys[0] and not self.keys[1]:
            axis[1] = -1
        if self.keys[1] and not self.keys[0]:
            axis[1] = 1
        if self.keys[2] and not self.keys[3]:
            axis[0] = -1
        if self.keys[3] and not self.keys[2]:
            axis[0] = 1
        

        self.mapRect.left -= SCROLL_SPEED * axis[0]
        self.mapRect.top -= SCROLL_SPEED * axis[1]

        if (axis[0] != 0) or (axis[1] != 0):
            self.adjustMap()

    def scrollMap(self):
        
        self.adjustMap()

    def adjustMap(self):
        if self.mapRect.left > 0:
            self.mapRect.left = 0
        if self.mapRect.right < SCREEN_SIZE[0]:
            self.mapRect.right = SCREEN_SIZE[0]
        if self.mapRect.width < SCREEN_SIZE[0]:
            self.mapRect.left = (SCREEN_SIZE[0] / 2) - (self.mapRect.width / 2)

        if self.mapRect.top > 0:
            self.mapRect.top = 0
        if self.mapRect.bottom < SCREEN_SIZE[1]:
            self.mapRect.bottom = SCREEN_SIZE[1]
        if self.mapRect.height < SCREEN_SIZE[1]:
            self.mapRect.top = (SCREEN_SIZE[1] / 2) - (self.mapRect.height / 2)\

    def absMousePos(self):
        temp = []
        for i in range(2):
            temp.append(round(
                (self.mousePos[i] - self.mapRect.topleft[i]) / self.zoomVal, 3))

        return temp

    def key(self, k, t):
        self.keys[k] = t
