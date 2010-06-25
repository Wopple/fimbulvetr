import os
import sys
import pygame

from constants import *

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

    text = c.name + "#" + c.speciesName + "#" + str(c.currSuperMove) 
    fh = open(filePath, "w")
    fh.write(text)
    fh.close()
    
def getInfo(filePath):

    try:
        fh = open(filePath)
        text = fh.readline()
        vals = text.split('#')
        name = vals[0]
        speciesName = vals[1]
        currSuperMove = int(vals[2])
        info = saveCharInfo(name, speciesName, currSuperMove)
    except:
        info = saveCharInfo("", "", 0, False)

    return info

class saveCharInfo(object):
    def __init__(self, name, speciesName, currSuperMove, valid=True):
        self.name = name
        self.speciesName = speciesName
        self.currSuperMove = currSuperMove
        self.valid = valid
