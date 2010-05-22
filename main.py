import os
import sys
import pygame

import mvc

import debug_m, debug_v, menu_c, mapmode_m, mapmode_v, mapmode_c
import battle_m, battle_v, battle_c

from constants import *


def changeMVC(newM, newV, newC, screen):
    #Changes the Model/View/Controller currently in use
    #Val must be a new value than the previous value in order to
    #register.
    global m
    global v
    global c
    
    m = newM
    v = newV
    c = newC
    m.setView(v)
    c.setView(v)
    c.setModel(m)
    v.setModel(m)
    v.setScreen(screen)

def changeC(newC):
    #Changes only the controller
    global c
    c = newC
    c.setView(v)
    c.setModel(m)


def proceed(clock):
    #Progresses by one frame, updating each component of the MVC system.
    global m
    global v
    global c
    
    m.update()
    v.update()
    c.update()
    checkError()
    clock.tick(FRAME_RATE)

def checkError():
    if (m.checkError()) or (v.checkError()) or (c.checkError()):
        print m.checkError(), v.checkError(), c.checkError()
        criticalError(1)

m = mvc.Model()
v = mvc.View()
c = mvc.Controller()

if DEBUG_MODE:
    changeMVC(debug_m.Model(), debug_v.View(), menu_c.Controller(), screen)
    while not m.advance():
        proceed(clock)
    if m.debugMenu.value() == 1:
        data = battle_m.testData()
        changeMVC(battle_m.Model(data[0], data[1], data[2]), battle_v.View(), battle_c.Controller(), screen)
        while not m.advance():
            proceed(clock)
        sys.exit()
    elif m.debugMenu.value() == 2:
        data = mapmode_m.testData()
        changeMVC(mapmode_m.Model(data[0], data[1]), mapmode_v.View(), mapmode_c.Controller(), screen)
        while not m.advance():
            proceed(clock)
        sys.exit()
    elif m.debugMenu.value() == 4:
        sys.exit()
        
while 1:
    changeMVC(title_m.Model(), title_v.View(), menu_c.Controller(), screen)
    while not m.either():
        proceed(clock)
    if m.back():
        sys.exit()
