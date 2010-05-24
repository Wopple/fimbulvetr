import os
import sys
import pygame

from constants import *

import socket

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
            sent = self.sendMessage(outMsg)
        return '', 0

    def sendMessage(self, msg):
        msgSize = len(msg)
        totalsent = 0
        while totalsent < msgSize:
            sent = self.conn.send(msg[totalsent:])
            if sent == 0:
                return 0
            totalsent = totalsent + sent
        return 1

    def receiveMessage(self, msgSize):
        msg = ''
        while len(msg) < msgSize:
            chunk = self.conn.recv(msgSize-len(msg))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            msg = msg + chunk
        return msg

