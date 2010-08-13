import os
import sys
import pygame

from constantsconcurr import *

import socket
import threading

import netcode

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
        except socket.timeout:
            self.conn = None

    def update(self, outMsg):
        sent = 0
        while (sent == 0):
            sent = netcode.sendMessage(self.conn, outMsg)

        msgSize = NET_MESSAGE_SIZE
        inMsg = ''
        while (inMsg == ''):
            inMsg = netcode.receiveMessage(self.conn, msgSize)

        return inMsg, 2


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
