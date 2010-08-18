import os
import sys
import pygame

from constants import *

import socket
import threading

import netcode

class NetClient(object):
    def __init__(self, host):
        self.netID = 2
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(8.0)
        try:
            self.s.connect((host, MULTIPLAYER_PORT))
            self.s.settimeout(None)
        except socket.timeout:
            self.s = None

    def update(self, outMsg, msgSize=None):
        inMsg = ''
        while (inMsg == ''):
            inMsg = netcode.receiveMessage(self.s, msgSize)
            
        sent = 0
        while (sent == 0):
            sent = netcode.sendMessage(self.s, outMsg)
            
        return inMsg, 1

class NetThread(threading.Thread):
    def __init__(self, host):
        super(NetThread, self).__init__()
        self.flag = "starting"
        self.net = None
        self.host = host
        
    def run(self):
        self.flag = "seeking"
        self.net = NetClient(self.host)
        if self.net.s is None:
            self.flag = "failure"
        else:
            self.flag = "success"

