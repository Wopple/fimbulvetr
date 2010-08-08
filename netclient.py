import os
import sys
import pygame

from constantsconcurr import *

import socket

import netcode

class NetClient(object):
    def __init__(self, host):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, MULTIPLAYER_PORT))

    def update(self, outMsg):
        msgSize = NET_MESSAGE_SIZE
        inMsg = ''
        while (inMsg == ''):
            inMsg = netcode.receiveMessage(self.s, msgSize)
            
        sent = 0
        while (sent == 0):
            sent = netcode.sendMessage(self.s, outMsg)
            
        return inMsg, 1

def NetClientConcurr(flagArr, host):
    try:
        flagArr[0] = 1
        conn = NetClient(host)
        flagArr.append(conn)
        flagArr[0] = 2
    except:
        flagArr[0] = -1

