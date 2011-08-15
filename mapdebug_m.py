import os
import sys
import pygame

import mvc
import gamemap
import util
import incint

import mapchar

import mapmode_m
import hare, fox, cat


from constants import *

class Model(mvc.Model):
    def __init__(self, inMap):
        super(Model, self).__init__()

        inChars = [mapchar.Hare(0, hare.Hare()),
                   mapchar.Fox(0, fox.Fox()),
                   mapchar.Cat(0, cat.Cat()),
                   mapchar.Hare(1, hare.Hare()),
                   mapchar.Fox(1, fox.Fox()),
                   mapchar.Cat(1, cat.Cat()), ]

        self.m = mapmode_m.Model(inMap, inChars, 0)


    def update(self):
        self.m.mousePos = pygame.mouse.get_pos()
        self.m.checkScrolling()

    def leftClick(self):
        pass

    def rightClick(self):
        pass

    def numberKey(self):
        pass

    def key(self, num, b):
        self.m.key(num, b)

    def scrollIn(self):
        self.m.scrollIn()

    def scrollOut(self):
        self.m.scrollOut()
