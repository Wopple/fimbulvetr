import os
import sys
import pygame

from constants import *

import socket

import netcode

class NetClient(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        self.s.connect((host, MULTIPLAYER_PORT))

    def update(self, outMsg):
        msgSize = NET_MESSAGE_SIZE
        inMsg = ''
        while (inMsg == ''):
            inMsg = netcode.receiveMessage(self.s, msgSize)
            if (inMsg == ''):
                print "No message"
            else:
                print "Message Received: " + str(inMsg)

        sent = 0
        while (sent == 0):
            sent = netcode.sendMessage(self.s, outMsg)
            
        return inMsg, 1
