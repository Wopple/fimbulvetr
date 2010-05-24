import os
import sys
import pygame

from constants import *

import socket

class NetClient(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        self.s.connect((host, MULTIPLAYER_PORT))

    def update(self, outMsg):
        msgSize = NET_MESSAGE_SIZE
        inMsg = ''
        while (inMsg == ''):
            inMsg = self.receiveMessage(msgSize)
            if (inMsg == ''):
                print "No message"
            else:
                print "Message Received: " + str(inMsg)
        return inMsg, 1

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
            chunk = self.s.recv(msgSize-len(msg))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            msg = msg + chunk
        return msg
