import os
import sys
import pygame

import mvc

import debug_m, debug_v, menu_c, mapmode_m, mapmode_v, mapmode_c
import battle_m, battle_v, battle_c
import title_m, title_v
import mainmenu_m, mainmenu_v
import charactereditor_m, charactereditor_v, charactereditor_c
import textentry_m, textentry_v, textentry_c
import cutscene_c
import netclient, netserver
import chardata
import multiplayerSetup_m, multiplayerSetup_v, multiplayerSetup_c

from constants import *


def changeMVC(newM, newV, newC, screen, emptyLists=True):
    #Changes the Model/View/Controller currently in use
    #Val must be a new value than the previous value in order to
    #register.
    global m
    global v
    global c

    global mList
    global vList
    global cList
    
    m = newM
    v = newV
    c = newC
    m.setView(v)
    c.setView(v)
    c.setModel(m)
    v.setModel(m)
    v.setScreen(screen)

    if emptyLists:
        mList = []
        vList = []
        cList = []

def multiMVC(newM, newV, newC, screen):
    global m
    global v
    global c

    global mList
    global vList
    global cList

    if len(mList) == 0:
        mList.append(m)
        vList.append(v)
        cList.append(c)

    mList.append(newM)
    vList.append(newV)
    cList.append(newC)

    changeMVC(newM, newV, newC, screen, False)

def multiMVCBack():
    global m
    global v
    global c

    global mList
    global vList
    global cList

    mList = mList[0:-1]
    vList = vList[0:-1]
    cList = cList[0:-1]

    m = mList[-1]
    v = vList[-1]
    c = cList[-1]

def changeC(newC):
    #Changes only the controller
    global c
    c = newC
    c.setView(v)
    c.setModel(m)


def proceed(clock, net=None):
    #Progresses by one frame, updating each component of the MVC system.
    global m
    global v
    global c
    
    m.update()
    v.update()
    c.update()
    checkError()
    if not net is None:
        recvMsg, p = net.update(m.buildNetMessage())
        m.parseNetMessage(recvMsg, p)
    clock.tick(FRAME_RATE)

def proceedMulti(clock, net=None):
    global m
    global v
    global c

    global mList
    global vList

    for i in range(len(mList)):
        m = mList[i]
        v = vList[i]
        
        mList[i].update()
        if i == len(mList) - 1:
            vList[i].update()
            c.update()
        else:
            vList[i].update(False)
        checkError()
        
    if not net is None:
        recvMsg, p = net.update(m.buildNetMessage())
        m.parseNetMessage(recvMsg, p)
    clock.tick(FRAME_RATE)

def checkError():
    if (m.checkError()) or (v.checkError()) or (c.checkError()):
        print m.checkError(), v.checkError(), c.checkError()
        criticalError(1)

def goBattle(data, netType):
    if netType == 0:
        net = None
        cp = 1
        cam = 0
    elif netType == 1:
        net = netserver.NetServer()
        cp = 1
        cam = 0
    elif netType == 2:
        net = netclient.NetClient()
        cp = 2
        cam = 1
        
    changeMVC(battle_m.Model(data[0], data[1], data[2]), battle_v.View(), battle_c.Controller(), screen)
    c.setPlayer(cp)
    m.setNetPlayer(cp)
    m.setCameraPlayer(cam)
    while not m.advance():
        proceed(clock, net)
    sys.exit()

def goBattlePrompt(data):
    chars = [data[0], data[1]]
    
    print "Battle between " + str(chars[0].name) + " and " + str(chars[1].name)
    result = []
    for i in range(2):
        try:
            temp = int(raw_input("Result for " + str(chars[i].name) + ":"))
        except:
            temp = 0
        if (temp < -1) or (temp > 1):
            temp = 0
        result.append(temp)

    return result

def goTitle():
    changeMVC(title_m.Model(), title_v.View(), cutscene_c.Controller(), screen)
    while not m.advance():
        proceed(clock)


def goMainMenu():
    changeMVC(mainmenu_m.Model(), mainmenu_v.View(), menu_c.Controller(), screen)
    while not m.advance():
        proceed(clock)

    if m.menu.value() == 2:
        multiMVC(multiplayerSetup_m.Model(), multiplayerSetup_v.View(),
                 multiplayerSetup_c.Controller(), screen)
        while not m.back():
            proceedMulti(clock)
            if m.advance():
                m.advanceNow = False
                if m.menu.value() == 1:
                    goMultiplayerSetupServer()
                else:
                    goMultiplayerSetupClient()
                
    elif m.menu.value() == 3:
        multiMVC(charactereditor_m.Model(), charactereditor_v.View(),
                 charactereditor_c.Controller(), screen)
        while not m.back():
            proceedMulti(clock)
            if m.advance():
                m.advanceNow = False
                if m.menu.value() == 1:
                    goCreateCharacter()
                else:
                    goChangeSuper()
                
    if m.menu.value() == 5:
        sys.exit()

def goCreateCharacter():
    multiMVC(textentry_m.Model("Character Name", chardata.getNameList()),
             textentry_v.View(), textentry_c.Controller(), screen)
    while not m.either():
        proceedMulti(clock)
    if m.back():
        multiMVCBack()
    else:
        characterName = m.convert()
        multiMVCBack()
        m.setStage(1)
        while not m.either():
            proceedMulti(clock)
        if m.back():
            m.setStage(0)
        else:
            m.characterToDisplay.name = characterName
            goChangeSuper()

def goChangeSuper():
    m.setStage(2)
    while not m.either():
        proceedMulti(clock)
    if m.back():
        m.setStage(0)
    else:
        cName = m.characterToDisplay.name
        chardata.saveCharacter(m.characterToDisplay)
        m.setStage(0)
        m.setCharacterSelection(cName)

def goMultiplayerSetupClient():
    multiMVC(textentry_m.Model("IP Address", [], True), textentry_v.View(),
             textentry_c.Controller(), screen)
    while not m.either():
        proceedMulti(clock)
    if m.back():
        multiMVCBack()
    else:
        ipAddress = m.convert()
        multiMVCBack()




m = mvc.Model()
v = mvc.View()
c = mvc.Controller()

mList = []
vList = []
cList = []

if DEBUG_MODE:
    debugLoop = True
    while debugLoop:
        changeMVC(debug_m.Model(), debug_v.View(), menu_c.Controller(), screen)
        while not m.advance():
            proceed(clock)
        if m.debugMenu.value() == 1:
            goBattle(battle_m.testData(), 0)
        elif m.debugMenu.value() == 2:
            data = mapmode_m.testData()
            changeMVC(mapmode_m.Model(data[0], data[1], 0), mapmode_v.View(), mapmode_c.Controller(), screen)
            while not m.advance():
                proceed(clock)
                if not m.pendingBattle is None:
                    result = goBattlePrompt(m.pendingBattle)
                    m.resolveBattle(result)
            sys.exit()
        elif m.debugMenu.value() == 3:
            goBattle(battle_m.testData(), 1)
        elif m.debugMenu.value() == 4:
            goBattle(battle_m.testData(), 2)
        elif m.debugMenu.value() == 5:
            debugLoop = False
        elif m.debugMenu.value() == 6:
            sys.exit()


goTitle()
while 1:
    goMainMenu()
