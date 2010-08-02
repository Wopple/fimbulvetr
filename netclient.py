import os
import sys
import pygame

from constants import *

import socket

import netcode

class NetClient(object):
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '5.109.100.0'
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
