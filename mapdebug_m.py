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
        self.magnitude = 5


    def update(self):
        self.m.mousePos = pygame.mouse.get_pos()

        if self.someAreSelected():
            self.moveSelection()
        else:
            self.m.checkScrolling()

    def leftClick(self):
        pos = self.m.absMousePos()
        newC = [[pos[0], pos[1]], 60, 1, 0]

        for c in self.m.map.testCircles:
            c[2] = 0
            c[3] = 0

        self.m.map.testCircles.append(newC)
        self.m.drawOrigMap()

    def rightClick(self):
        pass

    def numberKey(self):
        pass

    def key(self, num, b):
        self.m.key(num, b)

    def scrollIn(self):
        if self.someAreSelected():
            self.scale(False)
        else:
            self.m.scrollIn()

    def scrollOut(self):
        if self.someAreSelected():
            self.scale(True)
        else:
            self.m.scrollOut()

    def changeHighlight(self, b):
        curr = -1
        for i, c in enumerate(self.m.map.testCircles):
            if c[3] == 1:
                curr = i
            c[3] = 0

        if curr == -1:
            self.m.map.testCircles[0][3] = 1
        else:
            if b:
                curr += 1
            else:
                curr -= 1

            if curr == len(self.m.map.testCircles):
                curr = 0
            elif curr < 0:
                curr = len(self.m.map.testCircles) - 1

            self.m.map.testCircles[curr][3] = 1

        self.m.drawOrigMap()

    def removeAll(self):
        b = False
        for i, c in enumerate(self.m.map.testCircles):
            if c[3] == 1:
                c[3] = 0
                b = True

        if not b:
            for i, c in enumerate(self.m.map.testCircles):
                c[2] = 0

        self.m.drawOrigMap()

    def someAreSelected(self):
        for c in self.m.map.testCircles:
            if c[2] == 1:
                return True

        return False

    def moveSelection(self):
        horiz = 0
        vert = 0

        if self.m.keys[0]:
            vert -= self.magnitude
        if self.m.keys[1]:
            vert += self.magnitude
        if self.m.keys[2]:
            horiz -= self.magnitude
        if self.m.keys[3]:
            horiz += self.magnitude

        if (horiz != 0) or (vert != 0):
        
            for c in self.m.map.testCircles:
                if c[2] == 1:
                    c[0][0] += horiz
                    c[0][1] += vert

            self.m.drawOrigMap()

    def scale(self, b):
        val = self.magnitude

        if not b:
            val *= -1

        for c in self.m.map.testCircles:
            if c[2] == 1:
                c[1] += val

        self.m.drawOrigMap()

    def toggleSelected(self):
        for c in self.m.map.testCircles:
            if c[3] == 1:
                if c[2] == 0:
                    c[2] = 1
                else:
                    c[2] = 0

        self.m.drawOrigMap()

    def deleteHighlighted(self):
        temp = []
        for i, c in enumerate(self.m.map.testCircles):
            if c[3] == 0:
                temp.append(self.m.map.testCircles[i])

        self.m.map.testCircles = temp

        self.m.drawOrigMap()

    def changeMagnitude(self, b):
        magChange = 1
        if not b:
            magChange *= -1

        self.magnitude += magChange

        if self.magnitude < 1:
            self.magnitude = 1
        if self.magnitude > 15:
            self.magnitude = 15

        print "Magnitude: ", self.magnitude

    def printListToOutput(self):

        f = open('scrap/easy.txt', 'w')
        for i, c in enumerate(self.m.map.testCircles):
            print c
            f.write ("((" + str(int(c[0][0])) + ", " +
                   str(int(c[0][1])) + "), " +
                   str(int(c[1])) + ")" )
            if i < len(self.m.map.testCircles) - 1:
                f.write(",")
            f.write("\n")

        print "Sent to file."
        
