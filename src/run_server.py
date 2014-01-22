#!/usr/bin/python

import settings

import server

if __name__ == "__main__":
    print "running server"
    settings.ENV = settings.SERVER
    server.run()
    print "SUCCESS"
