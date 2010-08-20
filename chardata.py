import os
import sys
import pygame

from constants import *

import hare, fox, cat

def saveCharacter(c):
    try:
        fileToUse = None
        for i in range(MAX_CHARACTER_SAVES):
            fileName = CHARACTER_FILE_NAME + str(i) + "." + CHARACTER_FILE_EXT
            filePath = os.path.join(DIREC_CHARACTER_SAVES, fileName)
            if os.path.exists(filePath) and os.path.isfile(filePath):
                info = getInfo(filePath)
                if (info.name == c.name) or (not info.valid):
                    fileToUse = filePath
                    break
            else:
                if fileToUse is None:
                    fileToUse = filePath

        if fileToUse is None:
            fileError("Reached save file limit")
        else:
            writeToCharacterFile(c, fileToUse)
        
        
    except:
        fileError("Error accessing save files")


def getNameList():
    names = []
    for i in range(MAX_CHARACTER_SAVES):
        fileName = CHARACTER_FILE_NAME + str(i) + "." + CHARACTER_FILE_EXT
        filePath = os.path.join(DIREC_CHARACTER_SAVES, fileName)
        if os.path.exists(filePath) and os.path.isfile(filePath):
            info = getInfo(filePath)
            if info.valid:
                names.append(info.name)

    return names

def fileError(m):
    print m


def writeToCharacterFile(c, filePath):

    text = getTextString(c)
    fh = open(filePath, "w")
    fh.write(text)
    fh.close()

def getTextString(c, expand=False):
    text = c.name + "#" + c.speciesName + "#" + str(c.currSuperMove) + "#"

    if expand:
        size = len(text)
        if size > CHARACTER_TRANSFER_NET_MESSAGE_SIZE:
            raise
        add = CHARACTER_TRANSFER_NET_MESSAGE_SIZE - size

        for i in range(add):
            text = text + "-"

    return text
    
def getInfo(filePath):

    try:
        fh = open(filePath)
        text = fh.readline()
        info = turnStringIntoInfo(text)
    except:
        info = saveCharInfo("", "", 0, False)

    return info

def turnStringIntoInfo(text):
    vals = text.split('#')
    name = vals[0]
    speciesName = vals[1]
    currSuperMove = int(vals[2])
    return saveCharInfo(name, speciesName, currSuperMove)

def loadCharacter(name):
    for i in range(MAX_CHARACTER_SAVES):
        fileName = CHARACTER_FILE_NAME + str(i) + "." + CHARACTER_FILE_EXT
        filePath = os.path.join(DIREC_CHARACTER_SAVES, fileName)
        if os.path.exists(filePath) and os.path.isfile(filePath):
            info = getInfo(filePath)
            if (info.name == name):
                c = makeCharacterFromInfo(info)
                return c
            
    fileError("Error finding save file for character")
    return None

def deleteCharacter(name):
    for i in range(MAX_CHARACTER_SAVES):
        fileName = CHARACTER_FILE_NAME + str(i) + "." + CHARACTER_FILE_EXT
        filePath = os.path.join(DIREC_CHARACTER_SAVES, fileName)
        if os.path.exists(filePath) and os.path.isfile(filePath):
            info = getInfo(filePath)
            if (info.name == name):
                os.remove(filePath)
                return
            
    fileError("Error finding save file for character")

def makeCharacterFromInfo(info):
    if info.speciesName == "Hare":
        return hare.Hare(info.name, info.currSuperMove)
    elif info.speciesName == "Fox":
        return fox.Fox(info.name, info.currSuperMove)
    elif info.speciesName == "Cat":
        return cat.Cat(info.name, info.currSuperMove)

def convertNetData(dataList):
    charList = []
    for d in dataList:
        #try:
        info = turnStringIntoInfo(d)
        #except:
            #info = saveCharInfo("", "", 0, False)

        charList.append(makeCharacterFromInfo(info))

    return charList

class saveCharInfo(object):
    def __init__(self, name, speciesName, currSuperMove, valid=True):
        self.name = name
        self.speciesName = speciesName
        self.currSuperMove = currSuperMove
        self.valid = valid
