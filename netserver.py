import os
import sys
import pygame

from constants import *

import socket
import threading

import netcode

import mapchar

class NetServer(object):
    def __init__(self):
        self.netID = 1
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', MULTIPLAYER_PORT))
        self.s.settimeout(8.0)
        try:
            self.s.listen(1)
            self.conn, addr = self.s.accept()
            print "Connected to client at " + str(addr)
            self.conn.settimeout(None)
        except socket.timeout:
            self.conn = None

    def update(self, outMsg, msgSize=None):            
        netcode.updateSend(self.conn, outMsg)
        inMsg = netcode.updateRecv(self.conn, msgSize)

        return inMsg, 2
    
    def transferPregameData(self, playerChars, expected):
        for i in playerChars:
            outMsg = i.getTextString(True)
            netcode.updateSend(self.conn, outMsg)

        enemyData = []
        for i in range(expected):
            inMsg = netcode.updateRecv(self.conn,
                                       CHARACTER_TRANSFER_NET_MESSAGE_SIZE)
            enemyData.append(inMsg)

        return mapchar.convertNetData(enemyData, 1)


class NetThread(threading.Thread):
    def __init__(self):
        super(NetThread, self).__init__()
        self.flag = "starting"
        self.net = None
    
    def run(self):
        self.flag = "seeking"
        self.net = NetServer()
        if self.net.conn is None:
            self.flag = "failure"
        else:
            self.flag = "success"
