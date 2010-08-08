import os
import sys
import pygame

from constantsconcurr import *

import socket

import netcode

class NetServer(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', MULTIPLAYER_PORT))
        self.s.listen(1)
        self.conn, addr = self.s.accept()
        print "Connected to client at " + str(addr)

    def update(self, outMsg):
        sent = 0
        while (sent == 0):
            sent = netcode.sendMessage(self.conn, outMsg)

        msgSize = NET_MESSAGE_SIZE
        inMsg = ''
        while (inMsg == ''):
            inMsg = netcode.receiveMessage(self.conn, msgSize)

        return inMsg, 2


def NetServerConcurr(flagArr):
    try:
        flagArr[0] = 1
        conn = NetServer()
        flagArr.append(conn)
        flagArr[0] = 2
    except:
        flagArr[0] = -1
