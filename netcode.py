import os
import sys
import pygame

from constants import *

import socket


def sendMessage(sock, msg):
    msgSize = len(msg)
    totalsent = 0
    while totalsent < msgSize:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            return 0
        totalsent = totalsent + sent
    return 1

def receiveMessage(sock, msgSize):
    msg = ''
    while len(msg) < msgSize:
        chunk = sock.recv(msgSize-len(msg))
        if chunk == '':
            raise RuntimeError, "socket connection broken"
        msg = msg + chunk
    return msg

